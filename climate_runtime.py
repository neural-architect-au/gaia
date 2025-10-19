"""
Climate Solutions AI Agent - AgentCore Runtime Entrypoint
AWS AI Agent Global Hackathon 2025
"""

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from backend.agents.climate_agent_strands import ClimateAgent
import logging
import time
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = BedrockAgentCoreApp()

# Simple in-memory cache
cache = {}
CACHE_TTL = 300  # 5 minutes

@app.entrypoint
async def invoke(payload):
    """
    AgentCore entrypoint for Climate Solutions agent
    
    Expected payload:
    {
        "prompt": "Optimize building energy for maximum efficiency"
    }
    """
    try:
        query = payload.get("prompt", "Optimize building energy for maximum efficiency and carbon reduction")
        
        # Create cache key from query
        cache_key = hashlib.md5(query.encode()).hexdigest()
        current_time = time.time()
        
        # Check cache
        if cache_key in cache:
            cached_data = cache[cache_key]
            if current_time - cached_data['timestamp'] < CACHE_TTL:
                logger.info(f"Cache HIT for: {query[:50]}...")
                return cached_data['response']
        
        logger.info(f"Cache MISS - Processing: {query}")
        
        # Create fresh agent instance for each request
        agent = ClimateAgent()
        result = await agent.run_optimization(query)
        
        response = {
            "status": "success",
            "query": query,
            "response": result["text"],
            "data": result.get("data")
        }
        
        # Store in cache
        cache[cache_key] = {
            'response': response,
            'timestamp': current_time
        }
        
        # Clean old cache entries (keep cache size manageable)
        if len(cache) > 100:
            oldest_key = min(cache.keys(), key=lambda k: cache[k]['timestamp'])
            del cache[oldest_key]
        
        return response
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    app.run()
