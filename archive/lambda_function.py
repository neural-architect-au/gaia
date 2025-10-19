"""
Lambda handler for Climate Solutions Agent Runtime deployment
Compatible with AWS Bedrock AgentCore Lab 4 (Runtime)
"""

import json
import asyncio
from backend.agents.strands_integration import ClimateSolutionsStrandsAgent

# Global agent instance
climate_agent = None

def lambda_handler(event, context):
    """
    Standard Lambda handler for AgentCore Runtime deployment
    Replaces BedrockAgentCoreApp pattern for container compatibility
    """
    global climate_agent
    
    # Initialize agent if not already done
    if climate_agent is None:
        climate_agent = ClimateSolutionsStrandsAgent()
    
    try:
        # Extract message and context from event
        message = event.get('message', '')
        building_context = event.get('context', {})
        
        # Process message asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        response = loop.run_until_complete(
            climate_agent.process_message(message, building_context)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'response': response,
                'agent': 'ClimateSolutionsAI',
                'timestamp': context.aws_request_id if context else None
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'agent': 'ClimateSolutionsAI'
            })
        }
    
    finally:
        if 'loop' in locals():
            loop.close()
