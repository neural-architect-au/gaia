#!/usr/bin/env python3
"""
Deploy Climate Solutions Agent using proper AgentCore pattern
Following Lab 4 methodology with BedrockAgentCoreApp
"""

import boto3
import json
from bedrock_agentcore_starter_toolkit import Runtime

def create_execution_role():
    """Create IAM execution role for AgentCore Runtime"""
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    role_name = "ClimateSolutionsAgentExecutionRole"
    
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Execution role for Climate Solutions Agent"
        )
        
        # Attach required policies
        policies = [
            'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
            'arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
        ]
        
        for policy in policies:
            iam.attach_role_policy(RoleName=role_name, PolicyArn=policy)
        
        return response['Role']['Arn']
        
    except iam.exceptions.EntityAlreadyExistsException:
        response = iam.get_role(RoleName=role_name)
        return response['Role']['Arn']

def setup_cognito():
    """Setup Cognito for authentication"""
    cognito = boto3.client('cognito-idp')
    
    try:
        # Create user pool
        user_pool = cognito.create_user_pool(
            PoolName='ClimateSolutionsUserPool',
            Policies={
                'PasswordPolicy': {
                    'MinimumLength': 8,
                    'RequireUppercase': False,
                    'RequireLowercase': False,
                    'RequireNumbers': False,
                    'RequireSymbols': False
                }
            }
        )
        
        user_pool_id = user_pool['UserPool']['Id']
        
        # Create user pool client
        client = cognito.create_user_pool_client(
            UserPoolId=user_pool_id,
            ClientName='ClimateSolutionsClient',
            GenerateSecret=True,
            ExplicitAuthFlows=['ADMIN_NO_SRP_AUTH']
        )
        
        client_id = client['UserPoolClient']['ClientId']
        
        # Get discovery URL
        discovery_url = f"https://cognito-idp.ap-southeast-2.amazonaws.com/{user_pool_id}/.well-known/openid_configuration"
        
        return {
            'client_id': client_id,
            'user_pool_id': user_pool_id,
            'discovery_url': discovery_url
        }
        
    except Exception as e:
        print(f"Cognito setup error: {e}")
        return None

def deploy_climate_agent():
    """Deploy climate solutions agent using proper AgentCore pattern"""
    
    print("🌍 Deploying Climate Solutions Agent with AgentCore Runtime...")
    print("🤖 Using Claude Sonnet 4.5 for superior climate intelligence")
    
    # Create execution role
    print("🔐 Creating execution role...")
    execution_role_arn = create_execution_role()
    print(f"✅ Execution role: {execution_role_arn}")
    
    # Setup Cognito
    print("🔑 Setting up Cognito authentication...")
    cognito_config = setup_cognito()
    if not cognito_config:
        print("❌ Cognito setup failed")
        return None
    print(f"✅ Cognito configured: {cognito_config['client_id']}")
    
    # Initialize Runtime
    agentcore_runtime = Runtime()
    
    # Configure deployment
    print("⚙️ Configuring AgentCore Runtime...")
    response = agentcore_runtime.configure(
        entrypoint="climate_runtime.py",
        execution_role=execution_role_arn,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        region="ap-southeast-2",
        agent_name="climate_solutions_agent",
        authorizer_configuration={
            "customJWTAuthorizer": {
                "allowedClients": [cognito_config['client_id']],
                "discoveryUrl": cognito_config['discovery_url'],
            }
        },
    )
    print(f"✅ Configuration completed: {response}")
    
    # Launch the agent
    print("🚀 Launching Climate Solutions Agent...")
    launch_result = agentcore_runtime.launch()
    agent_arn = launch_result.agent_arn
    
    print(f"🎉 Climate Solutions Agent deployed successfully!")
    print(f"📋 Agent ARN: {agent_arn}")
    print(f"🔑 Client ID: {cognito_config['client_id']}")
    print(f"🌍 Ready to optimize building energy and reduce carbon emissions!")
    
    return {
        'agent_arn': agent_arn,
        'cognito_config': cognito_config,
        'runtime': agentcore_runtime
    }

if __name__ == "__main__":
    deploy_climate_agent()
