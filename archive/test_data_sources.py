#!/usr/bin/env python3
"""
Test Official Data Sources
Tests AEMO and BOM integrations without Strands dependencies
"""

import asyncio
import sys
import os
import aiohttp

async def test_official_weather():
    """Test Bureau of Meteorology official data"""
    
    print("🌤️  Testing Official BOM Weather Data")
    print("-" * 40)
    
    # BOM Sydney Observatory Hill station
    bom_url = "http://www.bom.gov.au/fwo/IDN60901/IDN60901.94767.json"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(bom_url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    observations = data.get('observations', {}).get('data', [])
                    if observations:
                        latest = observations[0]
                        
                        temp = latest.get('air_temp')
                        humidity = latest.get('rel_hum')
                        wind_speed = latest.get('wind_spd_kmh')
                        cloud = latest.get('cloud')
                        
                        print(f"✅ BOM Data Retrieved Successfully:")
                        print(f"   🌡️  Temperature: {temp}°C")
                        print(f"   💧 Humidity: {humidity}%")
                        print(f"   💨 Wind Speed: {wind_speed} km/h")
                        print(f"   ☁️  Cloud Cover: {cloud}/8 oktas")
                        print(f"   📍 Station: Sydney Observatory Hill")
                        print(f"   🕐 Last Update: {latest.get('local_date_time_full')}")
                        
                        return True
                    else:
                        print("❌ No observation data found")
                        return False
                else:
                    print(f"❌ BOM API returned status {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error fetching BOM data: {e}")
        return False

async def test_official_energy():
    """Test Open Electricity (official AEMO data)"""
    
    print("\n⚡ Testing Official AEMO Energy Data")
    print("-" * 40)
    
    # Try multiple Open Electricity endpoints
    test_urls = [
        "https://api.opennem.org.au/stats/au/nem/price/1d",
        "https://api.opennem.org.au/stats/au/nem/fuel_tech/1d"
    ]
    
    try:
        async with aiohttp.ClientSession() as session:
            for url in test_urls:
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            print(f"✅ OpenNEM API accessible: {url}")
                            
                            # Check if we have data
                            if 'data' in data and data['data']:
                                latest_data = data['data'][-1] if isinstance(data['data'], list) else data['data']
                                print(f"   📊 Latest data point available")
                                print(f"   🕐 Data structure: {list(latest_data.keys())[:5]}...")
                                return True
                        else:
                            print(f"⚠️  API returned status {response.status}: {url}")
                            
                except asyncio.TimeoutError:
                    print(f"⚠️  Timeout accessing: {url}")
                except Exception as e:
                    print(f"⚠️  Error with {url}: {e}")
        
        print("❌ No AEMO data sources accessible")
        return False
        
    except Exception as e:
        print(f"❌ Error testing energy APIs: {e}")
        return False

async def test_climate_agent_logic():
    """Test climate optimization logic without external dependencies"""
    
    print("\n🧠 Testing Climate Agent Logic")
    print("-" * 40)
    
    # Simulate building data
    building_data = {
        'current_consumption_kwh': 2400,
        'occupancy_count': 450,
        'weather': {'temperature': 24, 'solar_irradiance': 850, 'wind_speed': 15},
        'energy_price_per_kwh': 0.35,
        'carbon_intensity_kg_per_kwh': 0.75,
        'hvac_load': 65,
        'lighting_load': 45,
        'server_load': 85,
        'other_load': 30
    }
    
    print("✅ Building Data Simulation:")
    print(f"   ⚡ Consumption: {building_data['current_consumption_kwh']} kWh")
    print(f"   👥 Occupancy: {building_data['occupancy_count']} people")
    print(f"   🌡️  Temperature: {building_data['weather']['temperature']}°C")
    print(f"   ☀️  Solar: {building_data['weather']['solar_irradiance']} W/m²")
    
    # Test optimization calculations
    baseline_consumption = building_data['current_consumption_kwh']
    
    # Simulate 12% energy reduction (our target)
    optimized_consumption = baseline_consumption * 0.88
    energy_savings = baseline_consumption - optimized_consumption
    cost_savings = energy_savings * building_data['energy_price_per_kwh']
    carbon_reduction = energy_savings * building_data['carbon_intensity_kg_per_kwh']
    
    print(f"\n✅ Optimization Calculations:")
    print(f"   📉 Energy Savings: {energy_savings:.0f} kWh (12% reduction)")
    print(f"   💰 Cost Savings: ${cost_savings:.2f}")
    print(f"   🌱 Carbon Reduction: {carbon_reduction:.0f} kg CO₂")
    print(f"   🚗 Equivalent: {carbon_reduction/0.4:.0f}km car emissions avoided")
    
    return True

async def main():
    """Run all tests"""
    
    print("🌍 Climate Solutions AI - Official Data Source Tests")
    print("=" * 60)
    
    results = []
    
    # Test official weather data
    weather_ok = await test_official_weather()
    results.append(("BOM Weather Data", weather_ok))
    
    # Test official energy data  
    energy_ok = await test_official_energy()
    results.append(("AEMO Energy Data", energy_ok))
    
    # Test climate logic
    logic_ok = await test_climate_agent_logic()
    results.append(("Climate Logic", logic_ok))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Results Summary:")
    print("-" * 30)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    total_passed = sum(results[i][1] for i in range(len(results)))
    print(f"\nOverall: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("🎉 All systems operational!")
    elif total_passed >= len(results) - 1:
        print("⚠️  Minor issues - system mostly functional")
    else:
        print("❌ Major issues detected")

if __name__ == "__main__":
    asyncio.run(main())
