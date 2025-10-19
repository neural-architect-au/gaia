"""
Official Bureau of Meteorology API Integration
Using official BOM data feeds from ftp.bom.gov.au
"""

import aiohttp
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    wind_speed: float
    solar_irradiance: float
    cloud_cover: float
    location: str
    timestamp: datetime

class OfficialWeatherAPI:
    """Official Bureau of Meteorology data integration"""
    
    def __init__(self):
        # Official BOM data feeds
        self.bom_observations = {
            "Sydney": "http://www.bom.gov.au/fwo/IDN60901/IDN60901.94767.json",
            "Melbourne": "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94868.json", 
            "Brisbane": "http://www.bom.gov.au/fwo/IDQ60901/IDQ60901.94576.json",
            "Perth": "http://www.bom.gov.au/fwo/IDW60901/IDW60901.94608.json",
            "Adelaide": "http://www.bom.gov.au/fwo/IDS60901/IDS60901.94675.json"
        }
        
        # Official BOM forecast XML feeds
        self.bom_forecasts = {
            "Sydney": "http://www.bom.gov.au/fwo/IDN11060.xml",
            "Melbourne": "http://www.bom.gov.au/fwo/IDV10753.xml",
            "Brisbane": "http://www.bom.gov.au/fwo/IDQ11295.xml",
            "Perth": "http://www.bom.gov.au/fwo/IDW14199.xml",
            "Adelaide": "http://www.bom.gov.au/fwo/IDS10044.xml"
        }
        
        self.session = None
    
    async def __aenter__(self):
        # Use proper headers to avoid 403 errors
        headers = {
            'User-Agent': 'ClimateSolutionsAI/1.0 (Climate Optimization Agent)',
            'Accept': 'application/json, application/xml, text/xml'
        }
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_current_weather(self, location: str = "Sydney") -> WeatherData:
        """Get current weather from official BOM observations"""
        
        url = self.bom_observations.get(location, self.bom_observations["Sydney"])
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_bom_observations(data, location)
                else:
                    print(f"BOM API returned status {response.status}")
                    raise Exception(f"BOM API returned status {response.status}")
                    
        except Exception as e:
            print(f"Error fetching BOM data: {e}")
            raise Exception("Unable to fetch official weather data")
    
    async def get_weather_forecast(self, location: str = "Sydney", hours: int = 24) -> List[Dict[str, Any]]:
        """Get official BOM forecast data"""
        
        url = self.bom_forecasts.get(location, self.bom_forecasts["Sydney"])
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    xml_data = await response.text()
                    return self._parse_bom_forecast(xml_data, hours)
                else:
                    raise Exception(f"BOM forecast API returned status {response.status}")
                    
        except Exception as e:
            print(f"Error fetching BOM forecast: {e}")
            raise Exception("Unable to fetch official forecast data")
    
    async def get_solar_conditions(self, location: str = "Sydney") -> Dict[str, Any]:
        """Get solar conditions from official BOM data"""
        
        weather = await self.get_current_weather(location)
        
        # Calculate solar irradiance based on official cloud data and time
        current_hour = datetime.now().hour
        is_daylight = 6 <= current_hour <= 18
        
        if not is_daylight:
            solar_irradiance = 0
            solar_potential = "none"
        else:
            # Use BOM cloud cover data to estimate solar irradiance
            clear_sky_irradiance = self._calculate_clear_sky_irradiance(current_hour)
            cloud_factor = (100 - weather.cloud_cover) / 100
            solar_irradiance = clear_sky_irradiance * cloud_factor
            
            if solar_irradiance > 800:
                solar_potential = "high"
            elif solar_irradiance > 400:
                solar_potential = "medium"
            else:
                solar_potential = "low"
        
        return {
            "current_solar_irradiance": solar_irradiance,
            "cloud_cover_pct": weather.cloud_cover,
            "solar_potential": solar_potential,
            "daylight_hours_remaining": max(0, 18 - current_hour) if is_daylight else 0,
            "data_source": "Bureau of Meteorology Official"
        }
    
    def _parse_bom_observations(self, data: Dict, location: str) -> WeatherData:
        """Parse official BOM JSON observations with robust error handling"""
        
        observations = data.get('observations', {}).get('data', [])
        if not observations:
            raise Exception("No observation data available")
        
        latest = observations[0]  # Most recent observation
        
        # Extract official BOM data with safe conversion
        def safe_float(value, default=0.0):
            if value is None or value == '-' or value == '':
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        temperature = safe_float(latest.get('air_temp'), 20.0)
        humidity = safe_float(latest.get('rel_hum'), 60.0)
        wind_speed = safe_float(latest.get('wind_spd_kmh'), 10.0)
        
        # Cloud cover from BOM (oktas to percentage)
        cloud_oktas = safe_float(latest.get('cloud'), 4.0)
        cloud_cover = (cloud_oktas / 8) * 100
        
        # Calculate solar irradiance from cloud cover and time
        current_hour = datetime.now().hour
        solar_irradiance = self._calculate_solar_from_clouds(current_hour, cloud_cover)
        
        return WeatherData(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            solar_irradiance=solar_irradiance,
            cloud_cover=cloud_cover,
            location=location,
            timestamp=datetime.now()
        )
    
    def _parse_bom_forecast(self, xml_data: str, hours: int) -> List[Dict[str, Any]]:
        """Parse official BOM XML forecast"""
        
        try:
            root = ET.fromstring(xml_data)
            forecast = []
            
            # Extract forecast periods from BOM XML
            for area in root.findall('.//area'):
                area_desc = area.get('description', '')
                if any(city in area_desc for city in ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide']):
                    for forecast_period in area.findall('.//forecast-period'):
                        start_time = forecast_period.get('start-time-local')
                        if start_time:
                            try:
                                # Parse BOM datetime format
                                dt = datetime.fromisoformat(start_time.replace('Z', '+00:00').replace('+10:00', '').replace('+11:00', ''))
                            except:
                                dt = datetime.now() + timedelta(hours=len(forecast))
                            
                            # Extract forecast elements
                            temp_max = None
                            temp_min = None
                            cloud_oktas = 4  # Default
                            
                            for element in forecast_period.findall('.//element'):
                                elem_type = element.get('type')
                                if elem_type == 'air_temperature_maximum' and element.text:
                                    temp_max = float(element.text)
                                elif elem_type == 'air_temperature_minimum' and element.text:
                                    temp_min = float(element.text)
                                elif elem_type == 'cloud_cover_oktas' and element.text:
                                    cloud_oktas = float(element.text)
                            
                            temperature = temp_max if temp_max else (temp_min if temp_min else 20)
                            cloud_cover = (cloud_oktas / 8) * 100
                            solar_irradiance = self._calculate_solar_from_clouds(dt.hour, cloud_cover)
                            
                            forecast.append({
                                'datetime': dt.isoformat(),
                                'temperature': temperature,
                                'cloud_cover': cloud_cover,
                                'solar_irradiance': solar_irradiance,
                                'hour_offset': (dt - datetime.now()).total_seconds() / 3600,
                                'data_source': 'BOM Official'
                            })
            
            return forecast[:hours]
            
        except Exception as e:
            print(f"Error parsing BOM XML: {e}")
            raise Exception("Unable to parse official forecast data")
    
    def _calculate_clear_sky_irradiance(self, hour: int) -> float:
        """Calculate theoretical clear sky solar irradiance for Australian cities"""
        
        if not (6 <= hour <= 18):
            return 0
        
        # Solar elevation angle approximation for Australian latitudes
        # Peak irradiance ~1200 W/m² at solar noon
        hour_angle = abs(12 - hour)
        elevation_factor = max(0, 1 - (hour_angle / 6) ** 2)
        
        return 1200 * elevation_factor
    
    def _calculate_solar_from_clouds(self, hour: int, cloud_cover_pct: float) -> float:
        """Calculate solar irradiance from cloud cover and time"""
        
        clear_sky = self._calculate_clear_sky_irradiance(hour)
        cloud_factor = (100 - cloud_cover_pct) / 100
        
        return clear_sky * cloud_factor
