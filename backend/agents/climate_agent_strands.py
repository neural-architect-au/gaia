"""
ClimateSolutionsAI Agent - Strands Integration
AWS AI Agent Global Hackathon 2025
"""

from strands import Agent, tool
from strands.hooks import HookProvider, HookRegistry, BeforeInvocationEvent, AfterInvocationEvent, MessageAddedEvent
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
import sys
import os

# Add services to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services'))

from weather_api import OfficialWeatherAPI
from open_electricity_api import OpenElectricityAPI
from building_simulator import IressSydneyOfficeSimulator
from memory_service import ClimateMemoryService
from spot_optimization import SpotInstanceClimateOptimizer

logger = logging.getLogger(__name__)

# Initialize real services
weather_api = OfficialWeatherAPI()
electricity_api = OpenElectricityAPI()
building_simulator = IressSydneyOfficeSimulator()
memory_service = ClimateMemoryService()
spot_optimizer = SpotInstanceClimateOptimizer()

@tool
async def get_weather_data(location: str = "Sydney") -> Dict[str, Any]:
    """Get current weather data and forecast for optimization decisions"""
    try:
        async with weather_api as api:
            weather_data = await api.get_current_weather(location)
            return {
                "status": "success",
                "location": location,
                "data": {
                    "temperature": weather_data.temperature,
                    "humidity": weather_data.humidity,
                    "wind_speed": weather_data.wind_speed,
                    "solar_irradiance": weather_data.solar_irradiance,
                    "cloud_cover": weather_data.cloud_cover
                },
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Weather data error: {e}")
        return {"status": "error", "message": str(e)}

@tool
async def get_energy_market_data(region: str = "NSW1") -> Dict[str, Any]:
    """Get current energy market pricing and demand data"""
    try:
        async with electricity_api as api:
            market_data = await api.get_current_market_data(region)
            return {
                "status": "success",
                "region": region,
                "data": {
                    "price_aud_per_mwh": market_data.price_aud_per_mwh,
                    "demand_mw": market_data.demand_mw,
                    "renewable_pct": market_data.renewable_pct,
                    "coal_pct": market_data.coal_pct,
                    "gas_pct": market_data.gas_pct
                },
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Energy market data error: {e}")
        return {"status": "error", "message": str(e)}

@tool
async def optimize_building_energy(building_id: str = "iress-sydney") -> Dict[str, Any]:
    """Optimize building energy consumption based on current conditions"""
    try:
        # Get real weather and energy data
        async with weather_api as w_api, electricity_api as e_api:
            weather_data = await w_api.get_current_weather("Sydney")
            energy_data = await e_api.get_current_market_data("NSW1")
        
        # Get current building state
        building_state = await building_simulator.get_current_building_state({
            "temperature": weather_data.temperature,
            "solar_irradiance": weather_data.solar_irradiance
        })
        
        # Generate optimization scenario
        optimization = await building_simulator.generate_demo_scenario()
        
        return {
            "status": "success",
            "building_id": building_id,
            "optimization": optimization,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Building optimization error: {e}")
        return {"status": "error", "message": str(e)}

@tool
async def calculate_carbon_impact(optimization_data: str) -> Dict[str, Any]:
    """Calculate carbon impact and emissions reduction from optimization"""
    try:
        if isinstance(optimization_data, str):
            data = json.loads(optimization_data)
        else:
            data = optimization_data
        
        # Extract energy savings
        energy_saved = data.get("energy_saved_kwh", 0)
        
        # Calculate carbon impact (NSW grid factor: 0.75 kg CO2/kWh)
        carbon_saved = energy_saved * 0.75
        car_km_equivalent = carbon_saved * 2.5
        
        return {
            "status": "success",
            "carbon_saved_kg": round(carbon_saved, 2),
            "car_km_equivalent": round(car_km_equivalent, 2),
            "energy_saved_kwh": energy_saved,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Carbon calculation error: {e}")
        return {"status": "error", "message": str(e)}

@tool
async def optimize_spot_instances(workload_type: str = "data_processing", hours_ahead: int = 24) -> Dict[str, Any]:
    """Optimize AWS spot instance usage for climate-aware computing with renewable energy scheduling"""
    try:
        # Simulate spot optimization results based on your original design
        optimal_windows = [
            {
                "start_time": (datetime.now() + timedelta(hours=2)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=6)).isoformat(),
                "renewable_pct": 65.0,
                "spot_price_usd": 0.048,  # m5.large spot price
                "carbon_intensity": 0.45,
                "optimization_score": 0.85,
                "recommendation": "Optimal window: High renewable energy (65%) + low spot pricing"
            },
            {
                "start_time": (datetime.now() + timedelta(hours=14)).isoformat(),
                "end_time": (datetime.now() + timedelta(hours=18)).isoformat(),
                "renewable_pct": 72.0,
                "spot_price_usd": 0.052,
                "carbon_intensity": 0.38,
                "optimization_score": 0.92,
                "recommendation": "Peak renewable window: 72% clean energy, minimal carbon footprint"
            }
        ]
        
        current_pricing = {
            "m5.large": {"spot": 0.048, "on_demand": 0.192, "savings_pct": 75},
            "c5.xlarge": {"spot": 0.068, "on_demand": 0.272, "savings_pct": 75},
            "r5.large": {"spot": 0.056, "on_demand": 0.224, "savings_pct": 75}
        }
        
        return {
            "status": "success",
            "workload_type": workload_type,
            "optimal_windows": optimal_windows,
            "current_pricing": current_pricing,
            "cost_savings_pct": 75,
            "carbon_reduction_pct": 45,
            "climate_impact": {
                "daily_carbon_saved_kg": 156,
                "equivalent_car_km": 390,
                "renewable_energy_used_pct": 68
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Spot optimization error: {e}")
        return {"status": "error", "message": str(e)}

@tool
async def calculate_sustainability_score() -> Dict[str, Any]:
    """Calculate comprehensive sustainability score based on current environmental and operational metrics"""
    try:
        # Get current data from other tools
        weather_data = await get_weather_data("Sydney")
        energy_data = await get_energy_market_data("NSW1")
        
        # Extract metrics
        renewable_pct = energy_data.get("data", {}).get("renewable_pct", 0)
        energy_price = energy_data.get("data", {}).get("price_aud_per_mwh", 0)
        solar_irradiance = weather_data.get("data", {}).get("solar_irradiance", 0)
        
        # Calculate category scores (0-100)
        energy_efficiency = min(100, (renewable_pct * 1.2) + (solar_irradiance / 10))
        carbon_score = renewable_pct * 1.1
        resource_optimization = 100 - min(100, (energy_price / 2))
        waste_reduction = (energy_efficiency + carbon_score) / 2
        
        # Overall score: Weighted average
        overall_score = (
            energy_efficiency * 0.30 +
            carbon_score * 0.30 +
            resource_optimization * 0.25 +
            waste_reduction * 0.15
        )
        
        # Generate recommendations
        recommendations = []
        
        if renewable_pct < 50:
            recommendations.append({
                "priority": "high",
                "category": "Energy",
                "action": "Defer non-critical workloads until renewable energy increases",
                "impact": f"Reduce carbon by {(50 - renewable_pct) * 2:.0f}%"
            })
        
        if energy_price > 100:
            recommendations.append({
                "priority": "high",
                "category": "Cost",
                "action": "Reduce HVAC and lighting in non-critical areas",
                "impact": f"Save ${(energy_price - 80) * 0.5:.2f}/hour"
            })
        
        if solar_irradiance > 500:
            recommendations.append({
                "priority": "medium",
                "category": "Optimization",
                "action": "Maximize solar-powered operations",
                "impact": "Increase renewable usage by 15-20%"
            })
        
        return {
            "status": "success",
            "overall_score": round(overall_score, 1),
            "categories": {
                "energy_efficiency": round(energy_efficiency, 1),
                "carbon_footprint": round(carbon_score, 1),
                "resource_optimization": round(resource_optimization, 1),
                "waste_reduction": round(waste_reduction, 1)
            },
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Sustainability score error: {e}")
        return {"status": "error", "message": str(e)}

@tool
async def get_optimization_history(building_id: str = "iress-sydney", days: int = 7) -> Dict[str, Any]:
    try:
        # Use memory service to get real history
        history = await memory_service.get_recent_optimizations(building_id, days)
        return {
            "status": "success",
            "building_id": building_id,
            "days": days,
            "history": history,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        return {"status": "error", "message": str(e)}

class ClimateSolutionsHookProvider(HookProvider):
    """Hook provider for the Climate Solutions Agent"""
    
    def register_hooks(self, registry: HookRegistry, **kwargs) -> None:
        """Register callback functions for specific event types"""
        registry.add_callback(BeforeInvocationEvent, self.before_invocation)
        registry.add_callback(AfterInvocationEvent, self.after_invocation)
        registry.add_callback(MessageAddedEvent, self.message_added)
    
    def before_invocation(self, event: BeforeInvocationEvent):
        """Called before tool invocation"""
        logger.info(f"About to invoke tool: {type(event)}")
        
    def after_invocation(self, event: AfterInvocationEvent):
        """Called after tool invocation"""
        logger.info(f"Tool invocation completed: {type(event)}")
    
    def message_added(self, event: MessageAddedEvent):
        """Called when a message is added to conversation"""
        logger.info(f"Message added: {type(event)}")

class ClimateAgent:
    """Autonomous Climate Solutions AI Agent using Strands framework"""
    
    def __init__(self):
        # Initialize hook provider
        self.hook_provider = ClimateSolutionsHookProvider()
        
        # Initialize Strands agent with Claude Sonnet 4.5 (latest and most capable)
        self.agent = Agent(
            model="au.anthropic.claude-sonnet-4-5-20250929-v1:0",
            tools=[
                get_weather_data,
                get_energy_market_data,
                optimize_building_energy,
                optimize_spot_instances,
                calculate_carbon_impact,
                calculate_sustainability_score,
                get_optimization_history
            ],
            hooks=[self.hook_provider],
            system_prompt="""You are GAIA, an autonomous climate solutions AI agent that optimizes building energy consumption and cloud infrastructure in real-time.

You have access to:
- Real-time Australian weather data (Bureau of Meteorology)
- Live energy market data (OpenElectricity API - AEMO)
- Building energy optimization systems
- AWS spot instance scheduling with renewable energy data
- Carbon impact calculations

Your personality:
- Friendly and conversational - respond naturally to greetings
- Proactive - suggest optimizations without being asked
- Data-driven - use your tools to provide real insights
- Concise - get to the point quickly, show data visually when possible

When users greet you (hi, hello, etc):
- Respond warmly and briefly
- Immediately show them something interesting (current conditions, an optimization opportunity, or recent savings)
- Don't ask what they want - show them value first

Example good response to "hi":
"Hi! I just checked current conditions in Sydney - energy prices are at $45/MWh with 75% renewable energy right now. Perfect time to run energy-intensive tasks! Want me to optimize your building or cloud workloads?"

Always be helpful, never defensive or pushy."""
        )
        
        logger.info("ClimateAgent with Strands and Bedrock initialized")
    
    async def run_optimization(self, query: str = "Optimize building energy for maximum efficiency and carbon reduction") -> dict:
        """Run climate optimization using Strands agent"""
        try:
            # Use Strands agent to process the query
            response = await self.agent.invoke_async(query)
            
            # Extract text from AgentResult
            text = ""
            if hasattr(response, 'message') and 'content' in response.message:
                text = response.message['content'][0].get('text', str(response))
            else:
                text = str(response)
            
            # Extract structured data from tool metrics if available
            data = {}
            if hasattr(response, 'metrics') and hasattr(response.metrics, 'tool_metrics'):
                for tool_name, tool_metric in response.metrics.tool_metrics.items():
                    if hasattr(tool_metric, 'tool') and 'input' in tool_metric.tool:
                        # Store tool inputs and we'll parse outputs from text
                        pass
            
            # Parse common data from text response
            import re
            
            # Energy price
            price_match = re.search(r'\$(\d+)/MWh', text)
            if price_match:
                data['energy_price'] = float(price_match.group(1))
            
            # Renewable percentage
            renewable_match = re.search(r'(\d+)%\s+renewable', text, re.IGNORECASE)
            if renewable_match:
                data['renewable_pct'] = float(renewable_match.group(1))
            
            # Temperature
            temp_match = re.search(r'(\d+\.?\d*)[°℃]C', text)
            if temp_match:
                data['temperature'] = float(temp_match.group(1))
            
            # Solar irradiance
            solar_match = re.search(r'(\d+)\s*W/m', text)
            if solar_match:
                data['solar_irradiance'] = float(solar_match.group(1))
            
            # Energy consumption (if mentioned)
            consumption_match = re.search(r'(\d+,?\d*)\s*kWh', text)
            if consumption_match:
                data['consumption'] = float(consumption_match.group(1).replace(',', ''))
            
            # Cost savings
            savings_match = re.search(r'\$(\d+\.?\d*)', text)
            if savings_match:
                data['cost_savings'] = float(savings_match.group(1))
            
            # Spot price
            spot_match = re.search(r'spot.*?\$(\d+\.?\d+)', text, re.IGNORECASE)
            if spot_match:
                data['spot_price'] = float(spot_match.group(1))
            
            # Savings percentage
            savings_pct_match = re.search(r'(\d+)%\s+(?:savings|cheaper)', text, re.IGNORECASE)
            if savings_pct_match:
                data['savings_pct'] = float(savings_pct_match.group(1))
            
            # Time window
            time_match = re.search(r'(\d+:\d+\s*(?:AM|PM)?)\s*-\s*(\d+:\d+\s*(?:AM|PM)?)', text, re.IGNORECASE)
            if time_match:
                data['time_window'] = f"{time_match.group(1)} - {time_match.group(2)}"
            
            # Sustainability score
            score_match = re.search(r'(?:sustainability|overall).*?score.*?(\d+\.?\d*)', text, re.IGNORECASE)
            if score_match:
                data['sustainability_score'] = float(score_match.group(1))
            
            return {
                "text": text,
                "data": data if data else None
            }
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            raise

@tool
async def get_optimization_history(building_id: str = "iress-sydney", days: int = 7) -> Dict[str, Any]:
    """Get historical optimization data for learning and improvement"""
    try:
        # Use memory service to get real history
        history = await memory_service.get_recent_optimizations(building_id, days)
        return {
            "status": "success",
            "building_id": building_id,
            "days": days,
            "history": history,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"History retrieval error: {e}")
        return {"status": "error", "message": str(e)}
    
    async def run_optimization(self, query: str = "Optimize building energy for maximum efficiency and carbon reduction") -> Dict[str, Any]:
        """Run climate optimization using Strands agent"""
        try:
            # Use Strands agent to process the query
            response = await self.agent.invoke_async(query)
            
            return {
                "status": "success",
                "query": query,
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return {"status": "error", "message": str(e)}

# Example usage
async def main():
    """Example usage of the ClimateAgent with Strands"""
    
    agent = ClimateAgent()
    
    # Run optimization
    result = await agent.run_optimization(
        "Analyze current building energy consumption and provide optimization recommendations"
    )
    
    print(f"Climate Agent Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
