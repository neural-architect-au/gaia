"""
AgentCore Memory Service for Climate Solutions
Persistent memory for optimization history and user preferences
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

class ClimateMemoryService:
    """AgentCore Memory integration for climate agent"""
    
    def __init__(self, table_name: str = "climate-agent-memory"):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)
    
    async def get_building_context(self, building_id: str) -> Dict[str, Any]:
        """Retrieve building optimization history and preferences"""
        try:
            response = self.table.get_item(Key={'building_id': building_id})
            if 'Item' in response:
                return response['Item']
            
            # Return default context for new buildings
            return {
                'building_id': building_id,
                'baseline_consumption': 2400,
                'optimization_history': [],
                'user_preferences': {
                    'comfort_priority': 'medium',
                    'cost_priority': 'high',
                    'environmental_priority': 'high'
                },
                'created_at': datetime.now().isoformat()
            }
        except ClientError as e:
            print(f"Error retrieving building context: {e}")
            return {}
    
    async def save_optimization_result(self, building_id: str, optimization: Dict[str, Any]):
        """Save optimization result to memory"""
        try:
            # Get existing context
            context = await self.get_building_context(building_id)
            
            # Add new optimization to history
            optimization_record = {
                'timestamp': datetime.now().isoformat(),
                'energy_savings_kwh': optimization.get('energy_savings_kwh', 0),
                'cost_savings_aud': optimization.get('cost_savings_aud', 0),
                'carbon_reduction_kg': optimization.get('carbon_reduction_kg', 0),
                'efficiency_improvement_pct': optimization.get('efficiency_improvement_pct', 0),
                'actions_taken': optimization.get('executed_actions', [])
            }
            
            context['optimization_history'].append(optimization_record)
            
            # Keep only last 50 optimizations
            if len(context['optimization_history']) > 50:
                context['optimization_history'] = context['optimization_history'][-50:]
            
            # Update last optimization timestamp
            context['last_optimization'] = datetime.now().isoformat()
            context['total_optimizations'] = len(context['optimization_history'])
            
            # Calculate cumulative savings
            context['cumulative_savings'] = {
                'energy_kwh': sum(opt['energy_savings_kwh'] for opt in context['optimization_history']),
                'cost_aud': sum(opt['cost_savings_aud'] for opt in context['optimization_history']),
                'carbon_kg': sum(opt['carbon_reduction_kg'] for opt in context['optimization_history'])
            }
            
            # Save to DynamoDB
            self.table.put_item(Item=context)
            
        except ClientError as e:
            print(f"Error saving optimization result: {e}")
    
    async def update_user_preferences(self, building_id: str, preferences: Dict[str, Any]):
        """Update user preferences for building optimization"""
        try:
            context = await self.get_building_context(building_id)
            context['user_preferences'].update(preferences)
            context['preferences_updated_at'] = datetime.now().isoformat()
            
            self.table.put_item(Item=context)
            
        except ClientError as e:
            print(f"Error updating preferences: {e}")
    
    async def get_optimization_insights(self, building_id: str) -> Dict[str, Any]:
        """Get insights from optimization history"""
        context = await self.get_building_context(building_id)
        history = context.get('optimization_history', [])
        
        if not history:
            return {'message': 'No optimization history available'}
        
        # Calculate trends
        recent_optimizations = history[-10:]  # Last 10 optimizations
        avg_savings = sum(opt['energy_savings_kwh'] for opt in recent_optimizations) / len(recent_optimizations)
        
        return {
            'total_optimizations': len(history),
            'average_energy_savings': avg_savings,
            'best_optimization': max(history, key=lambda x: x['energy_savings_kwh']),
            'cumulative_savings': context.get('cumulative_savings', {}),
            'optimization_trend': 'improving' if len(history) > 1 and history[-1]['energy_savings_kwh'] > history[-2]['energy_savings_kwh'] else 'stable'
        }
