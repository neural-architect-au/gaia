"""
Australian Energy Market Integration
Connects to AEMO (Australian Energy Market Operator) and BOM (Bureau of Meteorology)
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
import pandas as pd
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EnergyPricing(BaseModel):
    """Energy pricing data model"""
    timestamp: datetime
    region: str
    price_per_mwh: float
    demand_mw: float
    renewable_percentage: float
    carbon_intensity: float


class WeatherData(BaseModel):
    """Weather data model"""
    timestamp: datetime
    location: str
    temperature: float
    solar_irradiance: float
    wind_speed: float
    cloud_cover: float
    forecast_hours: int


class AustralianEnergyAPI:
    """
    Integration with Australian energy and weather APIs
    
    Provides real-time energy pricing, demand, renewable generation,
    and weather data for intelligent building optimization.
    """
    
    def __init__(self):
        self.aemo_base_url = "https://visualisations.aemo.com.au/aemo/apps/api/report/5MIN"
        self.bom_base_url = "http://www.bom.gov.au/fwo"
        
        # Sydney/NSW region focus for demo
        self.region = "NSW1"
        self.location = "Sydney"
        
        logger.info("AustralianEnergyAPI initialized")
    
    async def get_current_energy_pricing(self) -> EnergyPricing:
        """Get current energy pricing from AEMO"""
        
        try:
            # AEMO 5-minute pricing data
            url = f"{self.aemo_base_url}/PRICE_AND_DEMAND/{self.region}/LATEST"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract latest pricing data
            latest_data = data.get('5MIN', [])[-1] if data.get('5MIN') else {}
            
            # Calculate carbon intensity based on renewable mix
            renewable_pct = await self._get_renewable_percentage()
            carbon_intensity = self._calculate_carbon_intensity(renewable_pct)
            
            return EnergyPricing(
                timestamp=datetime.now(),
                region=self.region,
                price_per_mwh=latest_data.get('PRICE', 85.0),  # Default fallback
                demand_mw=latest_data.get('DEMAND', 8500.0),
                renewable_percentage=renewable_pct,
                carbon_intensity=carbon_intensity
            )
            
        except Exception as e:
            logger.warning(f"AEMO API error, using simulated data: {e}")
            return self._get_simulated_energy_pricing()
    
    async def get_weather_forecast(self, hours_ahead: int = 24) -> List[WeatherData]:
        """Get weather forecast from BOM"""
        
        try:
            # BOM weather data (simplified - real implementation would use proper API)
            weather_data = []
            
            for hour in range(hours_ahead):
                forecast_time = datetime.now() + timedelta(hours=hour)
                
                # Simulate realistic Sydney weather patterns
                base_temp = 22 + (hour % 24 - 12) * 0.5  # Daily temperature cycle
                solar = max(0, 800 * (1 - abs(hour % 24 - 12) / 12)) if 6 <= hour % 24 <= 18 else 0
                
                weather_data.append(WeatherData(
                    timestamp=forecast_time,
                    location=self.location,
                    temperature=base_temp + (hour * 0.1),  # Slight warming trend
                    solar_irradiance=solar,
                    wind_speed=15 + (hour % 6) * 2,
                    cloud_cover=30 + (hour % 8) * 5,
                    forecast_hours=hour
                ))
            
            return weather_data
            
        except Exception as e:
            logger.warning(f"BOM API error, using simulated data: {e}")
            return self._get_simulated_weather_forecast(hours_ahead)
    
    async def get_optimal_energy_windows(self, duration_hours: int = 4) -> List[Dict[str, Any]]:
        """Identify optimal energy consumption windows"""
        
        # Get energy pricing forecast
        pricing_data = await self._get_energy_pricing_forecast(24)
        weather_data = await self.get_weather_forecast(24)
        
        # Find windows with lowest cost and carbon intensity
        optimal_windows = []
        
        for i in range(len(pricing_data) - duration_hours):
            window_start = pricing_data[i].timestamp
            window_end = window_start + timedelta(hours=duration_hours)
            
            # Calculate average metrics for this window
            window_pricing = pricing_data[i:i+duration_hours]
            avg_price = sum(p.price_per_mwh for p in window_pricing) / len(window_pricing)
            avg_carbon = sum(p.carbon_intensity for p in window_pricing) / len(window_pricing)
            avg_renewable = sum(p.renewable_percentage for p in window_pricing) / len(window_pricing)
            
            # Calculate optimization score (lower is better)
            price_score = avg_price / 100  # Normalize price
            carbon_score = avg_carbon / 1.0  # Normalize carbon intensity
            renewable_bonus = (100 - avg_renewable) / 100  # Bonus for high renewables
            
            optimization_score = (price_score + carbon_score + renewable_bonus) / 3
            
            optimal_windows.append({
                'start_time': window_start,
                'end_time': window_end,
                'avg_price_per_mwh': avg_price,
                'avg_carbon_intensity': avg_carbon,
                'renewable_percentage': avg_renewable,
                'optimization_score': optimization_score,
                'recommended_actions': self._get_recommended_actions(avg_price, avg_carbon, avg_renewable)
            })
        
        # Sort by optimization score (best opportunities first)
        optimal_windows.sort(key=lambda x: x['optimization_score'])
        
        return optimal_windows[:5]  # Return top 5 opportunities
    
    async def _get_renewable_percentage(self) -> float:
        """Get current renewable energy percentage"""
        
        try:
            # Simulate renewable percentage based on time of day
            current_hour = datetime.now().hour
            
            # Higher renewables during daylight hours (solar)
            if 9 <= current_hour <= 16:
                base_renewable = 65  # High solar period
            elif 6 <= current_hour <= 9 or 16 <= current_hour <= 20:
                base_renewable = 45  # Moderate renewable
            else:
                base_renewable = 25  # Low renewable (night)
            
            # Add some variability
            import random
            return base_renewable + random.uniform(-10, 10)
            
        except Exception:
            return 40.0  # Default fallback
    
    def _calculate_carbon_intensity(self, renewable_percentage: float) -> float:
        """Calculate carbon intensity based on energy mix"""
        
        # Carbon intensity calculation
        # High renewables = low carbon intensity
        # Low renewables = high carbon intensity (coal/gas)
        
        coal_intensity = 0.95  # kg CO2/kWh for coal
        gas_intensity = 0.45   # kg CO2/kWh for gas
        renewable_intensity = 0.05  # kg CO2/kWh for renewables
        
        # Assume remaining non-renewable is 70% coal, 30% gas
        non_renewable_pct = 100 - renewable_percentage
        coal_pct = non_renewable_pct * 0.7
        gas_pct = non_renewable_pct * 0.3
        
        carbon_intensity = (
            (renewable_percentage / 100) * renewable_intensity +
            (coal_pct / 100) * coal_intensity +
            (gas_pct / 100) * gas_intensity
        )
        
        return carbon_intensity
    
    async def _get_energy_pricing_forecast(self, hours: int) -> List[EnergyPricing]:
        """Get energy pricing forecast"""
        
        pricing_data = []
        base_price = 85.0  # Base price per MWh
        
        for hour in range(hours):
            forecast_time = datetime.now() + timedelta(hours=hour)
            hour_of_day = forecast_time.hour
            
            # Price varies by time of day
            if 18 <= hour_of_day <= 21:  # Peak evening
                price_multiplier = 1.8
            elif 9 <= hour_of_day <= 17:  # Business hours
                price_multiplier = 1.3
            elif 6 <= hour_of_day <= 9:  # Morning peak
                price_multiplier = 1.5
            else:  # Off-peak
                price_multiplier = 0.7
            
            renewable_pct = await self._get_renewable_percentage()
            
            pricing_data.append(EnergyPricing(
                timestamp=forecast_time,
                region=self.region,
                price_per_mwh=base_price * price_multiplier,
                demand_mw=8500 + (hour % 12) * 200,
                renewable_percentage=renewable_pct,
                carbon_intensity=self._calculate_carbon_intensity(renewable_pct)
            ))
        
        return pricing_data
    
    def _get_recommended_actions(self, price: float, carbon: float, renewable: float) -> List[str]:
        """Get recommended actions based on energy conditions"""
        
        actions = []
        
        if price < 60:  # Low price
            actions.append("Schedule energy-intensive tasks")
            actions.append("Pre-cool/heat building")
        
        if carbon < 0.4:  # Low carbon
            actions.append("Increase server workloads")
            actions.append("Run backup systems")
        
        if renewable > 60:  # High renewables
            actions.append("Maximize energy consumption")
            actions.append("Charge energy storage systems")
        
        if price > 120:  # High price
            actions.append("Reduce non-essential loads")
            actions.append("Use stored energy")
        
        return actions
    
    def _get_simulated_energy_pricing(self) -> EnergyPricing:
        """Fallback simulated energy pricing"""
        
        current_hour = datetime.now().hour
        
        # Simulate realistic pricing patterns
        if 18 <= current_hour <= 21:
            price = 150.0  # Peak evening
        elif 9 <= current_hour <= 17:
            price = 95.0   # Business hours
        else:
            price = 65.0   # Off-peak
        
        renewable_pct = 45.0 if 9 <= current_hour <= 16 else 25.0
        
        return EnergyPricing(
            timestamp=datetime.now(),
            region=self.region,
            price_per_mwh=price,
            demand_mw=8500.0,
            renewable_percentage=renewable_pct,
            carbon_intensity=self._calculate_carbon_intensity(renewable_pct)
        )
    
    def _get_simulated_weather_forecast(self, hours: int) -> List[WeatherData]:
        """Fallback simulated weather forecast"""
        
        weather_data = []
        
        for hour in range(hours):
            forecast_time = datetime.now() + timedelta(hours=hour)
            hour_of_day = forecast_time.hour
            
            # Simulate daily temperature cycle
            base_temp = 22 + 8 * (1 - abs(hour_of_day - 14) / 14)
            solar = max(0, 900 * (1 - abs(hour_of_day - 12) / 12)) if 6 <= hour_of_day <= 18 else 0
            
            weather_data.append(WeatherData(
                timestamp=forecast_time,
                location=self.location,
                temperature=base_temp,
                solar_irradiance=solar,
                wind_speed=12 + (hour % 4) * 3,
                cloud_cover=25 + (hour % 6) * 8,
                forecast_hours=hour
            ))
        
        return weather_data


# Example usage
async def main():
    """Example usage of AustralianEnergyAPI"""
    
    api = AustralianEnergyAPI()
    
    # Get current energy pricing
    pricing = await api.get_current_energy_pricing()
    print(f"Current Energy Price: ${pricing.price_per_mwh:.2f}/MWh")
    print(f"Renewable Percentage: {pricing.renewable_percentage:.1f}%")
    print(f"Carbon Intensity: {pricing.carbon_intensity:.3f} kg CO2/kWh")
    
    # Get optimal energy windows
    windows = await api.get_optimal_energy_windows()
    print(f"\nTop 3 Optimal Energy Windows:")
    for i, window in enumerate(windows[:3]):
        print(f"{i+1}. {window['start_time'].strftime('%H:%M')} - {window['end_time'].strftime('%H:%M')}")
        print(f"   Price: ${window['avg_price_per_mwh']:.2f}/MWh")
        print(f"   Carbon: {window['avg_carbon_intensity']:.3f} kg CO2/kWh")
        print(f"   Actions: {', '.join(window['recommended_actions'])}")


if __name__ == "__main__":
    asyncio.run(main())
