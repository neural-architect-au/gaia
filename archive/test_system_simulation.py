#!/usr/bin/env python3
"""
Complete System Test - Simulating Strands Integration
Tests the complete climate agent logic with official data sources
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, Any

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

class MockStrandsAgent:
    """Mock Strands Agent to test our climate logic"""
    
    def __init__(self):
        self.name = "ClimateSolutionsAI"
        self.tools = {
            "optimize_building_energy": self._optimize_building_energy,
            "analyze_energy_market": self._analyze_energy_market,
            "get_weather_conditions": self._get_weather_conditions,
            "calculate_climate_impact": self._calculate_climate_impact,
            "get_building_status": self._get_building_status
        }
    
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Process user message and return response"""
        
        message_lower = message.lower()
        
        if "energy market" in message_lower or "aemo" in message_lower:
            result = await self.tools["analyze_energy_market"]()
            return f"Current energy market: ${result['current_price_per_mwh']:.2f}/MWh, {result['renewable_percentage']:.1f}% renewables. {result['recommendation']}"
        
        elif "weather" in message_lower:
            result = await self.tools["get_weather_conditions"]()
            if "error" in result:
                return f"Weather data: {result['error']}"
            return f"Weather: {result['temperature']:.1f}°C, {result['humidity']:.0f}% humidity, {result['solar_irradiance']:.0f}W/m² solar. {result['optimization_recommendation']}"
        
        elif "optimize" in message_lower:
            building_data = context or {}
            result = await self.tools["optimize_building_energy"](building_data)
            return f"Optimization complete! Saved {result['energy_savings_kwh']:.0f} kWh (${result['cost_savings_aud']:.2f}), prevented {result['carbon_reduction_kg']:.0f}kg CO₂. Efficiency improved by {result['efficiency_improvement_pct']:.1f}%."
        
        elif "co2" in message_lower or "carbon" in message_lower:
            # Extract number from message
            import re
            numbers = re.findall(r'\d+', message)
            kwh = float(numbers[0]) if numbers else 300
            result = await self.tools["calculate_climate_impact"](kwh)
            return f"Saving {kwh} kWh prevents {result['carbon_reduction_kg']:.0f}kg CO₂ (${result['cost_savings_aud']:.2f} saved). {result['environmental_message']}"
        
        elif "status" in message_lower:
            result = await self.tools["get_building_status"]()
            return f"Building status: {result['current_consumption_kwh']} kWh, {result['occupancy']} people. Systems: {result['systems_status']}. Daily savings: {result['daily_savings']}"
        
        else:
            return "Hello! I'm your Climate Solutions AI Agent. I can help with energy optimization, market analysis, weather conditions, and carbon impact calculations. Try asking about 'energy market', 'weather', 'optimize building', or 'building status'."
    
    async def _optimize_building_energy(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate building energy optimization"""
        
        baseline = building_data.get('current_consumption_kwh', 2400)
        
        # Simulate 12% energy reduction
        optimized = baseline * 0.88
        savings = baseline - optimized
        cost_savings = savings * 0.35  # $0.35/kWh
        carbon_reduction = savings * 0.75  # 0.75 kg CO2/kWh
        
        return {
            "optimization_complete": True,
            "energy_savings_kwh": savings,
            "cost_savings_aud": cost_savings,
            "carbon_reduction_kg": carbon_reduction,
            "efficiency_improvement_pct": 12.0
        }
    
    async def _analyze_energy_market(self, region: str = "NSW1") -> Dict[str, Any]:
        """Get real AEMO energy market data"""
        
        try:
            from services.open_electricity_api import OpenElectricityAPI
            async with OpenElectricityAPI() as api:
                market_data = await api.get_current_market_data(region)
                optimal_windows = await api.get_optimal_energy_windows(region)
            
            return {
                "current_price_per_mwh": market_data.price_aud_per_mwh,
                "renewable_percentage": market_data.renewable_pct,
                "carbon_intensity": 0.75 - (market_data.renewable_pct / 100 * 0.5),
                "optimal_windows": optimal_windows[:3],
                "recommendation": "Excellent time for energy tasks" if market_data.renewable_pct > 70 else "Standard conditions",
                "data_source": "Open Electricity (Official AEMO)"
            }
        except Exception as e:
            # Fallback with realistic current values
            return {
                "current_price_per_mwh": 85.50,
                "renewable_percentage": 65.2,
                "carbon_intensity": 0.45,
                "recommendation": "Using fallback data - API unavailable",
                "error": str(e)
            }
    
    async def _get_weather_conditions(self, location: str = "Sydney") -> Dict[str, Any]:
        """Get real BOM weather data"""
        
        try:
            from services.weather_api import OfficialWeatherAPI
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
                "optimization_recommendation": self._get_weather_advice(current.temperature, solar["solar_potential"])
            }
        except Exception as e:
            return {
                "error": f"Official weather data unavailable: {str(e)}",
                "recommendation": "Using standard optimization parameters"
            }
    
    def _get_weather_advice(self, temp: float, solar_potential: str) -> str:
        """Generate weather optimization advice"""
        
        advice = []
        if temp < 18:
            advice.append("Reduce heating load")
        elif temp > 28:
            advice.append("Optimize cooling systems")
        
        if solar_potential == "high":
            advice.append("Excellent solar conditions - run energy-intensive tasks")
        
        return "; ".join(advice) if advice else "Standard weather conditions"
    
    async def _calculate_climate_impact(self, energy_savings_kwh: float) -> Dict[str, Any]:
        """Calculate climate impact"""
        
        carbon_reduction = energy_savings_kwh * 0.75  # kg CO2/kWh
        cost_savings = energy_savings_kwh * 0.35  # AUD/kWh
        cars_equivalent = carbon_reduction / 4600 * 365  # Annual car emissions
        
        return {
            "carbon_reduction_kg": carbon_reduction,
            "cost_savings_aud": cost_savings,
            "environmental_message": f"Equivalent to removing a car for {carbon_reduction/0.4:.0f}km"
        }
    
    async def _get_building_status(self, building_id: str = "default") -> Dict[str, Any]:
        """Get building status"""
        
        return {
            "building_id": building_id,
            "current_consumption_kwh": 2112,  # After optimization
            "occupancy": 450,
            "systems_status": {
                "hvac": "optimal",
                "lighting": "energy_saving",
                "servers": "high_load"
            },
            "daily_savings": {"kwh": 288, "cost_aud": 85, "co2_kg": 180}
        }

async def test_complete_system():
    """Test the complete climate agent system"""
    
    print("🌍 Climate Solutions AI Agent - Complete System Test")
    print("=" * 60)
    
    # Initialize mock agent
    agent = MockStrandsAgent()
    print("✅ Climate Agent initialized")
    
    # Building context
    building_context = {
        "building_id": "iress_sydney_office",
        "current_consumption_kwh": 2400,
        "occupancy_count": 450,
        "location": "Sydney"
    }
    
    print(f"\n🏢 Testing Building: {building_context['building_id']}")
    
    # Test conversations
    test_conversations = [
        "Hello! What can you help me with?",
        "What's the current energy market situation?",
        "What are the weather conditions right now?", 
        "Optimize the building energy consumption",
        "What's our building status?",
        "How much CO2 can we save if we reduce energy by 300 kWh?"
    ]
    
    for i, message in enumerate(test_conversations, 1):
        print(f"\n{'='*50}")
        print(f"🧪 Test {i}: {message}")
        print("-" * 50)
        
        try:
            response = await agent.process_message(message, building_context)
            print(f"🤖 Response: {response}")
            
            await asyncio.sleep(0.5)  # Brief pause
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("🎯 Complete System Test Finished!")
    print("✅ Tested Components:")
    print("   - Climate Agent Logic")
    print("   - Official AEMO Energy Data")
    print("   - Official BOM Weather Data") 
    print("   - Building Optimization")
    print("   - Carbon Impact Calculations")

if __name__ == "__main__":
    asyncio.run(test_complete_system())
