"""
FastAPI endpoints for Climate Solutions AI Agent with Strands integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.climate_agent_strands import ClimateAgent

app = FastAPI(title="Climate Solutions AI Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
climate_agent = None

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class OptimizationRequest(BaseModel):
    building_id: str = "iress-sydney"
    include_spot: bool = True

@app.on_event("startup")
async def startup_event():
    """Initialize the climate agent on startup"""
    global climate_agent
    try:
        climate_agent = ClimateAgent()
        print("✅ Climate Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Climate Agent: {e}")

@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Climate Solutions AI Agent API",
        "status": "running",
        "agent_ready": climate_agent is not None
    }

@app.post("/chat")
async def chat_with_agent(request: ChatMessage) -> Dict[str, Any]:
    """Chat with the Climate Solutions AI Agent"""
    if not climate_agent:
        raise HTTPException(status_code=503, detail="Climate agent not initialized")
    
    try:
        result = await climate_agent.run_optimization(request.message)
        return {
            "success": True,
            "response": result["response"] if result["status"] == "success" else result["message"],
            "status": result["status"],
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.post("/optimize")
async def run_optimization(request: OptimizationRequest) -> Dict[str, Any]:
    """Run complete climate optimization"""
    if not climate_agent:
        raise HTTPException(status_code=503, detail="Climate agent not initialized")
    
    try:
        query = f"Analyze current Sydney weather and energy conditions, optimize the {request.building_id} building"
        if request.include_spot:
            query += ", and provide AWS spot instance recommendations for climate-aware computing"
        
        result = await climate_agent.run_optimization(query)
        return {
            "success": True,
            "optimization": result["response"] if result["status"] == "success" else None,
            "error": result["message"] if result["status"] == "error" else None,
            "building_id": request.building_id,
            "timestamp": result["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Optimization error: {str(e)}")

@app.get("/status")
async def get_status() -> Dict[str, Any]:
    """Get agent and system status"""
    return {
        "agent_initialized": climate_agent is not None,
        "tools_available": len(climate_agent.agent.tool_names) if climate_agent else 0,
        "tools": list(climate_agent.agent.tool_names) if climate_agent else [],
        "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "framework": "Strands + FastAPI"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
