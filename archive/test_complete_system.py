#!/usr/bin/env python3
"""
Complete System Test for Climate Solutions AI Agent
Tests all integrations: Strands, Memory, Official Data Sources
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.agents.strands_integration import ClimateSolutionsStrandsAgent

async def test_complete_system():
    """Test the complete climate agent system"""
    
    print("🌍 Climate Solutions AI Agent - Complete System Test")
    print("=" * 60)
    
    # Initialize the agent
    try:
        agent = ClimateSolutionsStrandsAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return
    
    # Test conversations with building context
    building_context = {
        "building_id": "iress_sydney_office",
        "current_consumption_kwh": 2400,
        "occupancy_count": 450,
        "location": "Sydney"
    }
    
    test_conversations = [
        "Hello! What can you help me with?",
        "What's the current energy market situation in Australia?",
        "What are the weather conditions right now?",
        "Optimize the building energy consumption",
        "What are our optimization insights and history?",
        "When should we run energy-intensive tasks today?",
        "How much CO2 can we save if we reduce energy by 300 kWh?"
    ]
    
    print(f"\n🏢 Testing with building: {building_context['building_id']}")
    print(f"📍 Location: {building_context['location']}")
    print(f"⚡ Current consumption: {building_context['current_consumption_kwh']} kWh")
    print(f"👥 Occupancy: {building_context['occupancy_count']} people")
    
    for i, message in enumerate(test_conversations, 1):
        print(f"\n{'='*60}")
        print(f"🧪 Test {i}/7: {message}")
        print("-" * 60)
        
        try:
            # Process message with context
            response = await agent.process_message(message, building_context)
            print(f"🤖 Agent Response:")
            print(f"{response}")
            
            # Add delay between tests
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in test {i}: {e}")
            print(f"   Message: {message}")
    
    print(f"\n{'='*60}")
    print("🎯 System Test Complete!")
    print("✅ All integrations tested:")
    print("   - Strands Agent Framework")
    print("   - Memory Persistence (DynamoDB)")
    print("   - Official AEMO Energy Data")
    print("   - Official BOM Weather Data")
    print("   - Climate Optimization Tools")

async def test_individual_components():
    """Test individual components separately"""
    
    print("\n🔧 Testing Individual Components")
    print("-" * 40)
    
    # Test Official Weather API
    print("\n1. Testing Official Weather Data...")
    try:
        from backend.services.weather_api import OfficialWeatherAPI
        async with OfficialWeatherAPI() as weather:
            current = await weather.get_current_weather("Sydney")
            print(f"   ✅ BOM Weather: {current.temperature}°C, {current.humidity}% humidity")
            
            solar = await weather.get_solar_conditions("Sydney")
            print(f"   ✅ Solar: {solar['current_solar_irradiance']:.0f}W/m², {solar['solar_potential']} potential")
    except Exception as e:
        print(f"   ❌ Weather API Error: {e}")
    
    # Test Official Energy Market API
    print("\n2. Testing Official Energy Market Data...")
    try:
        from backend.services.open_electricity_api import OpenElectricityAPI
        async with OpenElectricityAPI() as energy:
            market_data = await energy.get_current_market_data("NSW1")
            print(f"   ✅ AEMO Data: ${market_data.price_aud_per_mwh:.2f}/MWh, {market_data.renewable_pct:.1f}% renewables")
            
            windows = await energy.get_optimal_energy_windows("NSW1")
            print(f"   ✅ Optimal Windows: {len(windows)} opportunities found")
    except Exception as e:
        print(f"   ❌ Energy Market API Error: {e}")
    
    # Test Memory Service
    print("\n3. Testing Memory Service...")
    try:
        from backend.services.memory_service import ClimateMemoryService
        memory = ClimateMemoryService()
        context = await memory.get_building_context("test_building")
        print(f"   ✅ Memory Service: Building context retrieved")
        print(f"   📊 Baseline consumption: {context.get('baseline_consumption', 0)} kWh")
    except Exception as e:
        print(f"   ❌ Memory Service Error: {e}")

if __name__ == "__main__":
    print("Starting Complete System Test...")
    
    # Run individual component tests first
    asyncio.run(test_individual_components())
    
    # Run complete system test
    asyncio.run(test_complete_system())
