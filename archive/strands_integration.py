"""
Strands SDK Integration for ClimateSolutionsAI Agent
AWS AI Agent Global Hackathon 2025
"""

import asyncio
import json
from typing import Dict, Any, List
from strands import Agent, tool
from strands.hooks import BeforeInvocationEvent, AfterInvocationEvent, MessageAddedEvent, HookProvider

class ClimateSolutionsMemoryHooks(HookProvider):
    """Enhanced memory hooks with persistent storage"""
    
    def __init__(self):
        from ..services.memory_service import ClimateMemoryService
        self.memory_service = ClimateMemoryService()
    
    async def before_invocation(self, event: BeforeInvocationEvent):
        """Hook before agent invocation - load building context from persistent memory"""
        building_id = event.context.get("building_id", "default")
        climate_context = await self.memory_service.get_building_context(building_id)
        event.context.update(climate_context)
    
    async def after_invocation(self, event: AfterInvocationEvent):
        """Hook after agent invocation - save optimization results to persistent memory"""
        if "optimization_result" in event.response:
            building_id = event.context.get("building_id", "default")
            await self.memory_service.save_optimization_result(building_id, event.response["optimization_result"])
    
    async def message_added(self, event: MessageAddedEvent):
        """Hook when message is added - extract and save user preferences"""
        message_lower = event.message.lower()
        building_id = event.context.get("building_id", "default")
        
        preferences = {}
        if "comfort is important" in message_lower:
            preferences["comfort_priority"] = "high"
        elif "save money" in message_lower:
            preferences["cost_priority"] = "high"
        elif "environment" in message_lower:
            preferences["environmental_priority"] = "high"
        
        if preferences:
            await self.memory_service.update_user_preferences(building_id, preferences)


class ClimateSolutionsStrandsAgent(Agent):
    """
    Climate Solutions Agent using AWS Strands framework
    HACKATHON SUBMISSION: AWS AI Agent Global Hackathon
    """
    
    def __init__(self):
        # Initialize tools with proper @tool decorators
        tools = [
            self.optimize_building_energy,
            self.analyze_energy_market, 
            self.calculate_climate_impact,
            self.get_building_status,
            self.predict_energy_demand,
            self.get_optimization_insights,
            self.get_weather_conditions,
            self.optimize_spot_instances
        ]
        
        super().__init__(
            name="ClimateSolutionsAI",
            description="Autonomous AI agent for building energy optimization and climate solutions - AWS AI Agent Global Hackathon Submission",
            model="anthropic.claude-sonnet-4-5-20250929-v1:0",
            tools=tools,
            hooks=ClimateSolutionsMemoryHooks()
        )
    
    @tool
    async def optimize_building_energy(self, building_data: dict) -> dict:
        """Optimize building energy consumption using AI-powered decisions"""
        from .climate_agent import ClimateSolutionsAgent
        
        climate_agent = ClimateSolutionsAgent()
        metrics = await climate_agent.autonomous_optimization_cycle(building_data)
        
        return {
            "optimization_complete": True,
            "energy_savings_kwh": metrics.current_consumption_kwh - metrics.optimized_consumption_kwh,
            "cost_savings_aud": metrics.cost_savings_aud,
            "carbon_reduction_kg": metrics.carbon_reduction_kg,
            "efficiency_improvement_pct": metrics.efficiency_improvement_pct
        }
    
    @tool
    async def analyze_energy_market(self, region: str = "NSW1") -> dict:
        """Analyze Australian energy market conditions using official AEMO data"""
        import os
        from ..services.open_electricity_api import OpenElectricityAPI
        
        api_key = os.getenv('OPENELECTRICITY_API_KEY')
        
        async with OpenElectricityAPI(api_key=api_key) as api:
            market_data = await api.get_current_market_data(region)
            optimal_windows = await api.get_optimal_energy_windows(region)
        
        return {
            "current_price_per_mwh": market_data.price_aud_per_mwh,
            "renewable_percentage": market_data.renewable_pct,
            "carbon_intensity": 0.75 - (market_data.renewable_pct / 100 * 0.5),
            "optimal_windows": optimal_windows[:3],
            "recommendation": "Excellent time for energy-intensive tasks" if market_data.renewable_pct > 70 else "Standard energy conditions",
            "data_source": "OpenElectricity Official AEMO Data"
        }
    
    @tool
    async def get_weather_conditions(self, location: str = "Sydney") -> dict:
        """Get current weather and solar conditions from official Bureau of Meteorology"""
        from ..services.weather_api import OfficialWeatherAPI
        
        try:
            async with OfficialWeatherAPI() as weather:
                current = await weather.get_current_weather(location)
                solar = await weather.get_solar_conditions(location)
            
            return {
                "temperature": current.temperature,
                "humidity": current.humidity,
                "wind_speed": current.wind_speed,
                "solar_irradiance": current.solar_irradiance,
                "cloud_cover": current.cloud_cover,
                "solar_potential": solar["solar_potential"],
                "data_source": "Bureau of Meteorology Official",
                "optimization_recommendation": self._get_weather_optimization_advice(current.temperature, solar["solar_potential"])
            }
        except Exception as e:
            return {
                "error": f"Official weather data unavailable: {str(e)}",
                "recommendation": "Using standard optimization parameters"
            }
    
    @tool
    async def optimize_spot_instances(self, workload_type: str = "big_data") -> dict:
        """Optimize AWS Spot Instance usage based on energy market and carbon conditions"""
        from ..services.spot_optimization import SpotInstanceClimateOptimizer
        
        optimizer = SpotInstanceClimateOptimizer()
        recommendations = await optimizer.get_workload_recommendations(workload_type)
        
        return {
            "workload_type": workload_type,
            "best_window": recommendations["best_window"],
            "top_windows": recommendations["top_3_windows"],
            "climate_benefit": "Running during optimal windows reduces carbon footprint by up to 60%",
            "cost_benefit": "Spot instance optimization can save 50-90% on compute costs",
            "recommendation": f"Schedule {workload_type} workloads during high renewable energy periods"
        }
    
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Process user message with climate optimization context
        
        Examples:
        - "Optimize the Sydney office building"
        - "What's the current energy market situation?"
        - "How much CO2 can we save today?"
        """
        
        # Add building context if provided
        if context:
            building_context = await self.memory_hooks.retrieve_climate_context(
                context.get("building_id", "default")
            )
            context.update(building_context)
        
        # Process message through Strands framework
        response = await self.invoke_with_context(message, context)
        
        return response
    
    async def _calculate_climate_impact(self, energy_savings_kwh: float) -> Dict[str, Any]:
        """Tool: Calculate climate impact of energy savings"""
        
        carbon_intensity = 0.75  # kg CO2/kWh average for NSW
        cost_per_kwh = 0.35  # AUD per kWh
        
        carbon_reduction = energy_savings_kwh * carbon_intensity
        cost_savings = energy_savings_kwh * cost_per_kwh
        
        # Scale calculations
        annual_carbon_reduction = carbon_reduction * 365
        cars_equivalent = annual_carbon_reduction / 4600  # Average car emissions per year
        
        return {
            "carbon_reduction_kg": carbon_reduction,
            "cost_savings_aud": cost_savings,
            "annual_impact": {
                "carbon_reduction_tonnes": annual_carbon_reduction / 1000,
                "equivalent_cars_removed": int(cars_equivalent),
                "annual_cost_savings": cost_savings * 365
            },
            "environmental_message": f"Preventing {carbon_reduction:.0f}kg CO2 is equivalent to removing a car from the road for {carbon_reduction/0.4:.0f}km"
        }

    async def _optimize_spot_instances(self, workload_type: str = "big_data") -> Dict[str, Any]:
        """Tool: Optimize AWS Spot Instance usage based on energy market and carbon conditions"""
        
        from ..services.spot_optimization import SpotInstanceClimateOptimizer
        
        optimizer = SpotInstanceClimateOptimizer()
        recommendations = await optimizer.get_workload_recommendations(workload_type)
        
        return {
            "workload_type": workload_type,
            "best_window": recommendations["best_window"],
            "top_windows": recommendations["top_3_windows"],
            "avoid_periods": recommendations["avoid_periods"],
            "climate_benefit": f"Running during optimal windows reduces carbon footprint by up to 60%",
            "cost_benefit": f"Spot instance optimization can save 50-90% on compute costs",
            "recommendation": f"Schedule {workload_type} workloads during high renewable energy periods"
        }

    async def _get_weather_conditions(self, location: str = "Sydney") -> Dict[str, Any]:
        """Tool: Get current weather and solar conditions from official BOM data"""
        
        from ..services.weather_api import OfficialWeatherAPI
        
        try:
            async with OfficialWeatherAPI() as weather:
                current = await weather.get_current_weather(location)
                solar = await weather.get_solar_conditions(location)
            
            return {
                "temperature": current.temperature,
                "humidity": current.humidity,
                "wind_speed": current.wind_speed,
                "solar_irradiance": current.solar_irradiance,
                "cloud_cover": current.cloud_cover,
                "solar_potential": solar["solar_potential"],
                "data_source": "Bureau of Meteorology Official",
                "optimization_recommendation": self._get_weather_optimization_advice(current, solar),
                "hvac_impact": "Reduce cooling load" if current.temperature < 20 else "Increase cooling efficiency"
            }
        except Exception as e:
            return {
                "error": f"Unable to fetch official weather data: {str(e)}",
                "recommendation": "Weather data unavailable - using standard optimization parameters"
            }
    
    def _get_weather_optimization_advice(self, weather, solar) -> str:
        """Generate weather-based optimization advice"""
        
        advice = []
        
        if weather.temperature < 18:
            advice.append("Reduce HVAC heating - mild conditions")
        elif weather.temperature > 28:
            advice.append("Optimize cooling systems - high temperature")
        
        if solar["solar_potential"] == "high":
            advice.append("Excellent time for energy-intensive tasks - high solar generation")
        elif weather.solar_irradiance > 600:
            advice.append("Good solar conditions - moderate energy optimization")
        
        if weather.wind_speed > 20:
            advice.append("High wind - good for natural ventilation")
        
        return "; ".join(advice) if advice else "Standard weather conditions"
    
    async def _get_optimization_insights(self, building_id: str = "default") -> Dict[str, Any]:
        """Tool: Get optimization insights from memory"""
        return await self.memory_hooks.memory_service.get_optimization_insights(building_id)
    
    async def _get_building_status(self, building_id: str = "default") -> Dict[str, Any]:
        """Tool: Get current building status and metrics"""
        return {
            "building_id": building_id,
            "current_consumption_kwh": 2400,
            "occupancy": 450,
            "systems_status": {
                "hvac": "optimal",
                "lighting": "energy_saving_mode", 
                "servers": "high_load"
            },
            "last_optimization": "2 hours ago",
            "daily_savings": {"kwh": 288, "cost_aud": 85, "co2_kg": 180}
        }
    
    async def _predict_energy_demand(self, hours_ahead: int = 24) -> Dict[str, Any]:
        """Tool: Predict energy demand for optimization planning"""
        return {
            "prediction_horizon_hours": hours_ahead,
            "predicted_peak_demand": "2:00 PM - 4:00 PM",
            "optimal_task_windows": ["11:00 PM - 6:00 AM", "12:00 PM - 1:00 PM"],
            "renewable_energy_peaks": ["10:00 AM - 2:00 PM"],
            "recommendation": "Schedule energy-intensive tasks during solar peak hours"
        }
    
    async def _optimize_building_energy(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tool: Optimize building energy consumption"""
        
        # Import the main climate agent
        from .climate_agent import ClimateSolutionsAgent
        
        climate_agent = ClimateSolutionsAgent()
        metrics = await climate_agent.autonomous_optimization_cycle(building_data)
        
        return {
            "optimization_complete": True,
            "energy_savings_kwh": metrics.current_consumption_kwh - metrics.optimized_consumption_kwh,
            "cost_savings_aud": metrics.cost_savings_aud,
            "carbon_reduction_kg": metrics.carbon_reduction_kg,
            "efficiency_improvement_pct": metrics.efficiency_improvement_pct
        }
    
    async def _analyze_energy_market(self, region: str = "NSW1") -> Dict[str, Any]:
        """Tool: Analyze energy market conditions using Open Electricity API"""
        
        import os
        from ..services.open_electricity_api import OpenElectricityAPI
        
        api_key = os.getenv('OPENELECTRICITY_API_KEY')
        
        async with OpenElectricityAPI(api_key=api_key) as api:
            market_data = await api.get_current_market_data(region)
            optimal_windows = await api.get_optimal_energy_windows(region)
        
        return {
            "current_price_per_mwh": market_data.price_aud_per_mwh,
            "renewable_percentage": market_data.renewable_pct,
            "carbon_intensity": 0.75 - (market_data.renewable_pct / 100 * 0.5),
            "optimal_windows": optimal_windows[:3],
            "recommendation": "Excellent time for energy-intensive tasks" if market_data.renewable_pct > 70 else "Standard energy conditions",
            "market_status": "High renewables" if market_data.renewable_pct > 60 else "Mixed generation",
            "data_source": "OpenElectricity Official AEMO Data"
        }
    
    async def _get_building_status(self, building_id: str = "default") -> Dict[str, Any]:
        """Tool: Get current building status and metrics"""
        return {
            "building_id": building_id,
            "current_consumption_kwh": 2400,
            "occupancy": 450,
            "systems_status": {
                "hvac": "optimal",
                "lighting": "energy_saving_mode", 
                "servers": "high_load"
            },
            "last_optimization": "2 hours ago",
            "daily_savings": {"kwh": 288, "cost_aud": 85, "co2_kg": 180}
        }
    
    async def _predict_energy_demand(self, hours_ahead: int = 24) -> Dict[str, Any]:
        """Tool: Predict energy demand for optimization planning"""
        return {
            "prediction_horizon_hours": hours_ahead,
            "predicted_peak_demand": "2:00 PM - 4:00 PM",
            "optimal_task_windows": ["11:00 PM - 6:00 AM", "12:00 PM - 1:00 PM"],
            "renewable_energy_peaks": ["10:00 AM - 2:00 PM"],
            "recommendation": "Schedule energy-intensive tasks during solar peak hours"
        }
        """Tool: Calculate climate impact of energy savings"""
        
        carbon_intensity = 0.75  # kg CO2/kWh average for NSW
        cost_per_kwh = 0.35  # AUD per kWh
        
        carbon_reduction = energy_savings_kwh * carbon_intensity
        cost_savings = energy_savings_kwh * cost_per_kwh
        
        # Scale calculations
        annual_carbon_reduction = carbon_reduction * 365
        cars_equivalent = annual_carbon_reduction / 4600  # Average car emissions per year
        
        return {
            "carbon_reduction_kg": carbon_reduction,
            "cost_savings_aud": cost_savings,
            "annual_impact": {
                "carbon_reduction_tonnes": annual_carbon_reduction / 1000,
                "equivalent_cars_removed": int(cars_equivalent),
                "annual_cost_savings": cost_savings * 365
            },
            "environmental_message": f"Preventing {carbon_reduction:.0f}kg CO2 is equivalent to removing a car from the road for {carbon_reduction/0.4:.0f}km"
        }


# Example usage and conversation flows
async def demo_strands_conversation():
    """Demonstrate Strands conversational capabilities"""
    
    agent = ClimateSolutionsStrandsAgent()
    
    # Example conversations
    conversations = [
        "Hello! Can you help me optimize my office building's energy consumption?",
        "What's the current energy market situation in Australia?",
        "Optimize the Iress Sydney office building with 450 people and 2400 kWh consumption",
        "How much CO2 can we save if we reduce energy by 300 kWh?",
        "What's the best time today to run energy-intensive tasks?"
    ]
    
    print("🤖 ClimateSolutionsAI Strands Agent - Conversation Demo")
    print("=" * 60)
    
    for i, message in enumerate(conversations, 1):
        print(f"\n👤 User {i}: {message}")
        
        # Add building context for optimization requests
        context = None
        if "optimize" in message.lower() and "iress" in message.lower():
            context = {
                "building_id": "iress_sydney_office",
                "current_consumption_kwh": 2400,
                "occupancy_count": 450,
                "weather": {"temperature": 24, "solar_irradiance": 850},
                "energy_price_per_kwh": 0.35,
                "carbon_intensity_kg_per_kwh": 0.75
            }
        
        response = await agent.chat(message, context)
        print(f"🤖 Agent: {response}")


if __name__ == "__main__":
    asyncio.run(demo_strands_conversation())
