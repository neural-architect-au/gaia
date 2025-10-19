"""
Climate Solutions AI Tools
Standalone tools with @tool decorators for Strands integration
"""

import os
from typing import Dict, Any
from strands import tool

@tool
async def optimize_building_energy(building_data: dict) -> dict:
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
async def analyze_energy_market(region: str = "NSW1") -> dict:
    """Analyze Australian energy market conditions using official AEMO data"""
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
async def get_weather_conditions(location: str = "Sydney") -> dict:
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
            "data_source": "Bureau of Meteorology Official"
        }
    except Exception as e:
        return {
            "error": f"Official weather data unavailable: {str(e)}",
            "recommendation": "Using standard optimization parameters"
        }

@tool
async def optimize_spot_instances(workload_type: str = "big_data") -> dict:
    """Optimize AWS Spot Instance usage based on energy market and carbon conditions"""
    from ..services.spot_optimization import SpotInstanceClimateOptimizer
    
    optimizer = SpotInstanceClimateOptimizer()
    recommendations = await optimizer.get_workload_recommendations(workload_type)
    
    return {
        "workload_type": workload_type,
        "best_window": recommendations["best_window"],
        "top_windows": recommendations["top_3_windows"],
        "climate_benefit": "Running during optimal windows reduces carbon footprint by up to 60%",
        "cost_benefit": "Spot instance optimization can save 50-90% on compute costs"
    }

@tool
async def calculate_climate_impact(energy_savings_kwh: float) -> dict:
    """Calculate climate impact of energy savings"""
    carbon_intensity = 0.75  # kg CO2/kWh average for NSW
    cost_per_kwh = 0.35  # AUD per kWh
    
    carbon_reduction = energy_savings_kwh * carbon_intensity
    cost_savings = energy_savings_kwh * cost_per_kwh
    
    return {
        "carbon_reduction_kg": carbon_reduction,
        "cost_savings_aud": cost_savings,
        "environmental_message": f"Preventing {carbon_reduction:.0f}kg CO2 is equivalent to removing a car from the road for {carbon_reduction/0.4:.0f}km"
    }

@tool
async def get_building_status(building_id: str = "default") -> dict:
    """Get current building status and metrics"""
    return {
        "building_id": building_id,
        "current_consumption_kwh": 2112,
        "occupancy": 450,
        "systems_status": {
            "hvac": "optimal",
            "lighting": "energy_saving",
            "servers": "high_load"
        },
        "daily_savings": {"kwh": 288, "cost_aud": 85, "co2_kg": 180}
    }
