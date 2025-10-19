#!/usr/bin/env python3
"""
Setup infrastructure for Climate Solutions Agent
Creates necessary AWS resources for AgentCore deployment
"""

import boto3
import json
import zipfile
import os
from pathlib import Path

def create_lambda_package():
    """Create deployment package for Lambda"""
    print("📦 Creating Lambda deployment package...")
    
    # Create a zip file with the lambda function
    with zipfile.ZipFile('climate-agent-lambda.zip', 'w') as zipf:
        zipf.write('lambda_function.py')
        
        # Add backend modules
        for root, dirs, files in os.walk('backend'):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path)
    
    print("✅ Lambda package created: climate-agent-lambda.zip")
    return 'climate-agent-lambda.zip'

def create_iam_role():
    """Create IAM role for the agent"""
    print("🔐 Creating IAM role for Climate Solutions Agent...")
    
    iam = boto3.client('iam')
    
    # Trust policy for Lambda
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
    
    role_name = "ClimateSolutionsAgentRole"
    
    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role for Climate Solutions Agent"
        )
        
        # Attach basic Lambda execution policy
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        
        # Attach Bedrock access policy
        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
        )
        
        role_arn = response['Role']['Arn']
        print(f"✅ IAM role created: {role_arn}")
        return role_arn
        
    except iam.exceptions.EntityAlreadyExistsException:
        response = iam.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        print(f"✅ Using existing IAM role: {role_arn}")
        return role_arn

def create_lambda_function(role_arn, package_path):
    """Create Lambda function"""
    print("⚡ Creating Lambda function...")
    
    lambda_client = boto3.client('lambda')
    function_name = "climate-solutions-agent"
    
    with open(package_path, 'rb') as f:
        zip_content = f.read()
    
    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.11',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zip_content},
            Description='Climate Solutions AI Agent with Claude 4.5',
            Timeout=300,
            MemorySize=512,
            Environment={
                'Variables': {
                    'AWS_REGION': 'ap-southeast-2',
                    'AGENT_NAME': 'climate_solutions_agent',
                    'LOG_LEVEL': 'INFO',
                    'MODEL_ID': 'anthropic.claude-sonnet-4-5-20250929-v1:0'
                }
            }
        )
        
        function_arn = response['FunctionArn']
        print(f"✅ Lambda function created: {function_arn}")
        return function_arn
        
    except lambda_client.exceptions.ResourceConflictException:
        # Update existing function
        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        
        response = lambda_client.get_function(FunctionName=function_name)
        function_arn = response['Configuration']['FunctionArn']
        print(f"✅ Lambda function updated: {function_arn}")
        return function_arn

def main():
    """Setup complete infrastructure"""
    print("🌍 Setting up Climate Solutions Agent Infrastructure...")
    print("🤖 Using Claude Sonnet 4.5 for superior climate intelligence")
    
    try:
        # Create deployment package
        package_path = create_lambda_package()
        
        # Create IAM role
        role_arn = create_iam_role()
        
        # Wait a moment for role to propagate
        import time
        print("⏳ Waiting for IAM role to propagate...")
        time.sleep(10)
        
        # Create Lambda function
        function_arn = create_lambda_function(role_arn, package_path)
        
        print("\n🎉 Infrastructure setup complete!")
        print(f"📋 Function ARN: {function_arn}")
        print(f"🔐 Role ARN: {role_arn}")
        print("\n🚀 Ready for AgentCore deployment!")
        
        # Clean up
        os.remove(package_path)
        
        return {
            'function_arn': function_arn,
            'role_arn': role_arn
        }
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        return None

if __name__ == "__main__":
    main()
