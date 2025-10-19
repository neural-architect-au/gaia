#!/usr/bin/env python3
"""
Deploy Climate Solutions Agent using Bedrock AgentCore
Lab 3 (Gateway) -> Lab 4 (Runtime) progression
"""

import asyncio
import boto3
import json

async def deploy_climate_agent():
    """Deploy climate solutions agent to AgentCore Runtime"""
    
    print("🌍 Deploying Climate Solutions Agent to AgentCore...")
    
    # Use direct AWS API calls since bedrock_agentcore_starter_toolkit may not be available
    client = boto3.client('bedrock-agentcore-control', region_name='ap-southeast-2')
    
    # Agent configuration
    agent_config = {
        "agentName": "climate_solutions_agent",
        "description": "Autonomous AI agent for building energy optimization and climate solutions",
        "modelId": "anthropic.claude-sonnet-4-5-20250929-v1:0",
        "runtimeType": "lambda",
        "handler": "lambda_function.lambda_handler",
        "environment": {
            "AWS_REGION": "ap-southeast-2",
            "AGENT_NAME": "climate_solutions_agent",
            "LOG_LEVEL": "INFO"
        }
    }
    
    try:
        # Create agent runtime
        response = client.create_agent_runtime(**agent_config)
        agent_arn = response['agentRuntimeArn']
        
        print(f"✅ Agent configured successfully!")
        print(f"🚀 Agent deployed with ARN: {agent_arn}")
        
        return agent_arn
        
    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        print("💡 This may be expected if AgentCore toolkit is not installed")
        print("📋 Agent configuration ready for manual deployment")
        return None

if __name__ == "__main__":
    asyncio.run(deploy_climate_agent())
