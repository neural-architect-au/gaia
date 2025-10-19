"""
Simple test of Strands integration without AWS dependencies
"""

import asyncio
import sys
sys.path.append('.')

from agents.climate_agent_strands import get_weather_data, get_energy_market_data, optimize_building_energy

async def test_tools_directly():
    """Test the tools directly without the agent"""
    print("Testing Strands tools directly...")
    
    # Test weather data tool
    weather_result = await get_weather_data("Sydney")
    print(f"✅ Weather tool: {weather_result['status']}")
    
    # Test energy market data tool
    energy_result = await get_energy_market_data("NSW1")
    print(f"✅ Energy tool: {energy_result['status']}")
    
    # Test building optimization tool
    optimization_result = await optimize_building_energy("iress-sydney")
    print(f"✅ Optimization tool: {optimization_result['status']}")
    
    if optimization_result['status'] == 'success':
        opt_data = optimization_result['optimization']
        print(f"   Energy saved: {opt_data['energy_saved_kwh']} kWh")
        print(f"   Cost savings: ${opt_data['cost_savings_aud']}")
        print(f"   Carbon reduction: {opt_data['carbon_reduction_kg']} kg CO2")

if __name__ == "__main__":
    asyncio.run(test_tools_directly())
