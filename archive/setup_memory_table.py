#!/usr/bin/env python3
"""
Setup DynamoDB table for Climate Agent Memory
"""

import boto3
from botocore.exceptions import ClientError

def create_memory_table():
    """Create DynamoDB table for climate agent memory"""
    
    dynamodb = boto3.resource('dynamodb')
    table_name = 'climate-agent-memory'
    
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'building_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'building_id',
                    'AttributeType': 'S'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        print(f"Creating table {table_name}...")
        table.wait_until_exists()
        print(f"Table {table_name} created successfully!")
        
        return table
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table {table_name} already exists")
            return dynamodb.Table(table_name)
        else:
            print(f"Error creating table: {e}")
            return None

if __name__ == "__main__":
    create_memory_table()
