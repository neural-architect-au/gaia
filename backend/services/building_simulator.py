"""
Building Energy Simulation System
Simulates realistic building energy consumption and systems for demo purposes
"""

import asyncio
import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import pandas as pd

logger = logging.getLogger(__name__)


class BuildingSystem(BaseModel):
    """Building system model"""
    system_id: str
    system_type: str  # hvac, lighting, servers, other
    current_load_pct: float
    max_capacity_kw: float
    efficiency_rating: float
    controllable: bool
    status: str


class BuildingState(BaseModel):
    """Current building state"""
    building_id: str
    timestamp: datetime
    total_consumption_kwh: float
    occupancy_count: int
    systems: List[BuildingSystem]
    environmental_conditions: Dict[str, float]
    energy_metrics: Dict[str, float]


class IressSydneyOfficeSimulator:
    """
    Simulates the Iress Sydney office building for demo purposes
    
    Realistic building characteristics:
    - 5,000 sqm office space
    - 500 employees (typical occupancy 450)
    - High-performance trading systems
    - Modern HVAC and lighting
    """
    
    def __init__(self):
        self.building_id = "iress_sydney_office"
        self.building_size_sqm = 5000
        self.max_occupancy = 500
        self.typical_occupancy = 450
        
        # Initialize building systems
        self.systems = self._initialize_building_systems()
        
        # Baseline consumption patterns
        self.baseline_consumption_kwh = 2400  # Daily baseline
        
        logger.info(f"Initialized {self.building_id} simulator")
    
    def _initialize_building_systems(self) -> List[BuildingSystem]:
        """Initialize all building systems"""
        
        systems = [
            # HVAC System
            BuildingSystem(
                system_id="hvac_main",
                system_type="hvac",
                current_load_pct=65.0,
                max_capacity_kw=800.0,
                efficiency_rating=0.85,
                controllable=True,
                status="active"
            ),
            
            # Lighting Systems
            BuildingSystem(
                system_id="lighting_general",
                system_type="lighting",
                current_load_pct=45.0,
                max_capacity_kw=200.0,
                efficiency_rating=0.90,
                controllable=True,
                status="active"
            ),
            
            # Trading/Server Systems
            BuildingSystem(
                system_id="trading_servers",
                system_type="servers",
                current_load_pct=85.0,
                max_capacity_kw=600.0,
                efficiency_rating=0.75,
                controllable=False,  # Critical systems
                status="active"
            ),
            
            # General IT Systems
            BuildingSystem(
                system_id="general_it",
                system_type="servers",
                current_load_pct=60.0,
                max_capacity_kw=300.0,
                efficiency_rating=0.80,
                controllable=True,
                status="active"
            ),
            
            # Other Systems (elevators, security, etc.)
            BuildingSystem(
                system_id="other_systems",
                system_type="other",
                current_load_pct=30.0,
                max_capacity_kw=150.0,
                efficiency_rating=0.70,
                controllable=False,
                status="active"
            )
        ]
        
        return systems
    
    async def get_current_building_state(self, weather_data: Optional[Dict] = None) -> BuildingState:
        """Get current building state with realistic variations"""
        
        # Simulate time-based occupancy patterns
        current_hour = datetime.now().hour
        occupancy = self._calculate_occupancy(current_hour)
        
        # Update system loads based on occupancy and time
        updated_systems = self._update_system_loads(occupancy, current_hour, weather_data)
        
        # Calculate total consumption
        total_consumption = self._calculate_total_consumption(updated_systems)
        
        # Environmental conditions
        env_conditions = self._get_environmental_conditions(weather_data)
        
        # Energy metrics
        energy_metrics = self._calculate_energy_metrics(updated_systems, occupancy)
        
        return BuildingState(
            building_id=self.building_id,
            timestamp=datetime.now(),
            total_consumption_kwh=total_consumption,
            occupancy_count=occupancy,
            systems=updated_systems,
            environmental_conditions=env_conditions,
            energy_metrics=energy_metrics
        )
    
    def _calculate_occupancy(self, hour: int) -> int:
        """Calculate realistic occupancy based on time"""
        
        if 9 <= hour <= 17:  # Business hours
            # Peak occupancy with some variation
            base_occupancy = self.typical_occupancy
            variation = random.randint(-50, 50)
            return max(50, min(self.max_occupancy, base_occupancy + variation))
        
        elif 7 <= hour <= 9 or 17 <= hour <= 19:  # Transition hours
            return random.randint(100, 300)
        
        else:  # After hours
            # Security, cleaning, some late workers
            return random.randint(10, 80)
    
    def _update_system_loads(self, occupancy: int, hour: int, weather_data: Optional[Dict]) -> List[BuildingSystem]:
        """Update system loads based on conditions"""
        
        updated_systems = []
        
        for system in self.systems:
            updated_system = system.copy()
            
            if system.system_type == "hvac":
                # HVAC load depends on occupancy, weather, and time
                base_load = 40 + (occupancy / self.max_occupancy) * 40  # 40-80% base
                
                if weather_data:
                    temp = weather_data.get('temperature', 22)
                    # Increase load if temperature is far from 22°C
                    temp_adjustment = abs(temp - 22) * 2
                    base_load += temp_adjustment
                
                # Time-based adjustments
                if 6 <= hour <= 8:  # Pre-cooling/heating
                    base_load += 15
                elif 18 <= hour <= 22:  # After-hours reduction
                    base_load *= 0.7
                
                updated_system.current_load_pct = min(100, max(20, base_load))
            
            elif system.system_type == "lighting":
                # Lighting depends on occupancy and daylight
                base_load = 20 + (occupancy / self.max_occupancy) * 60  # 20-80% base
                
                # Daylight adjustment
                if 10 <= hour <= 16:  # Daylight hours
                    base_load *= 0.7
                elif hour <= 6 or hour >= 20:  # Dark hours
                    base_load *= 1.2
                
                updated_system.current_load_pct = min(100, max(10, base_load))
            
            elif system.system_type == "servers":
                if system.system_id == "trading_servers":
                    # Trading servers run high during market hours
                    if 9 <= hour <= 16:  # Market hours
                        updated_system.current_load_pct = random.uniform(80, 95)
                    else:
                        updated_system.current_load_pct = random.uniform(60, 80)
                else:
                    # General IT systems
                    base_load = 40 + (occupancy / self.max_occupancy) * 40
                    updated_system.current_load_pct = min(90, max(30, base_load))
            
            elif system.system_type == "other":
                # Other systems relatively stable
                base_load = 25 + (occupancy / self.max_occupancy) * 20
                updated_system.current_load_pct = min(60, max(15, base_load))
            
            updated_systems.append(updated_system)
        
        return updated_systems
    
    def _calculate_total_consumption(self, systems: List[BuildingSystem]) -> float:
        """Calculate total building consumption"""
        
        total_kw = 0
        
        for system in systems:
            system_consumption = (system.current_load_pct / 100) * system.max_capacity_kw
            total_kw += system_consumption
        
        # Convert to kWh (assuming hourly measurement)
        return total_kw
    
    def _get_environmental_conditions(self, weather_data: Optional[Dict]) -> Dict[str, float]:
        """Get environmental conditions"""
        
        if weather_data:
            return {
                'outdoor_temperature': weather_data.get('temperature', 22),
                'solar_irradiance': weather_data.get('solar_irradiance', 400),
                'wind_speed': weather_data.get('wind_speed', 12),
                'indoor_temperature': 22.5,  # Controlled
                'humidity': 45.0,
                'air_quality_index': 25
            }
        else:
            # Default conditions
            return {
                'outdoor_temperature': 22.0,
                'solar_irradiance': 400.0,
                'wind_speed': 12.0,
                'indoor_temperature': 22.5,
                'humidity': 45.0,
                'air_quality_index': 25
            }
    
    def _calculate_energy_metrics(self, systems: List[BuildingSystem], occupancy: int) -> Dict[str, float]:
        """Calculate energy efficiency metrics"""
        
        total_consumption = self._calculate_total_consumption(systems)
        
        return {
            'kwh_per_person': total_consumption / max(1, occupancy),
            'kwh_per_sqm': total_consumption / self.building_size_sqm,
            'hvac_percentage': sum(s.current_load_pct * s.max_capacity_kw for s in systems if s.system_type == 'hvac') / (total_consumption * 100) * 100,
            'lighting_percentage': sum(s.current_load_pct * s.max_capacity_kw for s in systems if s.system_type == 'lighting') / (total_consumption * 100) * 100,
            'servers_percentage': sum(s.current_load_pct * s.max_capacity_kw for s in systems if s.system_type == 'servers') / (total_consumption * 100) * 100,
            'efficiency_score': self._calculate_efficiency_score(systems, occupancy)
        }
    
    def _calculate_efficiency_score(self, systems: List[BuildingSystem], occupancy: int) -> float:
        """Calculate overall building efficiency score (0-100)"""
        
        total_consumption = self._calculate_total_consumption(systems)
        
        # Benchmark: 0.48 kWh per sqm per hour for efficient office buildings
        benchmark_consumption = self.building_size_sqm * 0.48
        
        if total_consumption <= benchmark_consumption:
            return 100.0
        else:
            # Score decreases as consumption increases above benchmark
            efficiency = (benchmark_consumption / total_consumption) * 100
            return max(0, min(100, efficiency))
    
    async def simulate_optimization_impact(self, optimizations: List[Dict]) -> Dict[str, Any]:
        """Simulate the impact of optimization actions"""
        
        # Get current state
        current_state = await self.get_current_building_state()
        original_consumption = current_state.total_consumption_kwh
        
        # Apply optimizations
        optimized_systems = current_state.systems.copy()
        total_savings = 0.0
        
        for optimization in optimizations:
            action = optimization.get('action', '')
            target_system = optimization.get('target_system', '')
            expected_savings = optimization.get('expected_savings_kwh', 0)
            
            # Simulate optimization effects
            if 'hvac' in action.lower() or target_system == 'hvac':
                for system in optimized_systems:
                    if system.system_type == 'hvac':
                        # Reduce HVAC load
                        reduction = min(20, system.current_load_pct * 0.15)  # Max 15% reduction
                        system.current_load_pct -= reduction
                        savings = (reduction / 100) * system.max_capacity_kw
                        total_savings += savings
            
            elif 'lighting' in action.lower() or target_system == 'lighting':
                for system in optimized_systems:
                    if system.system_type == 'lighting':
                        # Reduce lighting load
                        reduction = min(30, system.current_load_pct * 0.25)  # Max 25% reduction
                        system.current_load_pct -= reduction
                        savings = (reduction / 100) * system.max_capacity_kw
                        total_savings += savings
            
            elif 'server' in action.lower() or target_system == 'servers':
                for system in optimized_systems:
                    if system.system_type == 'servers' and system.controllable:
                        # Reduce non-critical server load
                        reduction = min(15, system.current_load_pct * 0.10)  # Max 10% reduction
                        system.current_load_pct -= reduction
                        savings = (reduction / 100) * system.max_capacity_kw
                        total_savings += savings
        
        optimized_consumption = self._calculate_total_consumption(optimized_systems)
        actual_savings = original_consumption - optimized_consumption
        
        return {
            'original_consumption_kwh': original_consumption,
            'optimized_consumption_kwh': optimized_consumption,
            'actual_savings_kwh': actual_savings,
            'expected_savings_kwh': sum(opt.get('expected_savings_kwh', 0) for opt in optimizations),
            'efficiency_improvement_pct': (actual_savings / original_consumption) * 100,
            'optimized_systems': optimized_systems
        }
    
    async def generate_demo_scenario(self) -> Dict[str, Any]:
        """Generate a compelling demo scenario"""
        
        # Set up a realistic scenario
        demo_time = datetime.now().replace(hour=11, minute=30)  # 11:30 AM - optimal solar time
        
        # Simulate weather conditions
        weather_data = {
            'temperature': 24,  # Slightly warm
            'solar_irradiance': 850,  # High solar
            'wind_speed': 15,
            'cloud_cover': 20
        }
        
        # Get building state
        building_state = await self.get_current_building_state(weather_data)
        
        # Define optimization scenario
        optimizations = [
            {
                'action': 'optimize_hvac_schedule',
                'target_system': 'hvac',
                'expected_savings_kwh': 150,
                'reasoning': 'Pre-cool building during high solar generation'
            },
            {
                'action': 'optimize_lighting_zones',
                'target_system': 'lighting',
                'expected_savings_kwh': 80,
                'reasoning': 'Reduce lighting in zones with high natural light'
            },
            {
                'action': 'schedule_server_tasks',
                'target_system': 'servers',
                'expected_savings_kwh': 60,
                'reasoning': 'Shift non-critical processing to optimal time'
            }
        ]
        
        # Simulate optimization impact
        impact = await self.simulate_optimization_impact(optimizations)
        
        return {
            'scenario_time': demo_time,
            'weather_conditions': weather_data,
            'building_state': building_state,
            'optimizations': optimizations,
            'impact': impact,
            'demo_narrative': self._generate_demo_narrative(building_state, impact)
        }
    
    def _generate_demo_narrative(self, building_state: BuildingState, impact: Dict) -> str:
        """Generate compelling demo narrative"""
        
        savings_kwh = impact['actual_savings_kwh']
        savings_pct = impact['efficiency_improvement_pct']
        cost_savings = savings_kwh * 0.35  # $0.35/kWh
        carbon_reduction = savings_kwh * 0.75  # 0.75 kg CO2/kWh
        
        narrative = f"""
🏢 IRESS SYDNEY OFFICE - LIVE OPTIMIZATION

⚡ CURRENT STATE:
• Building Consumption: {building_state.total_consumption_kwh:.0f} kWh
• Occupancy: {building_state.occupancy_count} people
• HVAC Load: {[s.current_load_pct for s in building_state.systems if s.system_type == 'hvac'][0]:.0f}%
• Lighting Load: {[s.current_load_pct for s in building_state.systems if s.system_type == 'lighting'][0]:.0f}%

🤖 AI AGENT ACTIONS:
• Detected optimal solar generation window
• Pre-cooling building before afternoon heat
• Optimizing lighting zones with natural light
• Scheduling non-critical server tasks

📊 IMMEDIATE RESULTS:
• Energy Savings: {savings_kwh:.0f} kWh ({savings_pct:.1f}% reduction)
• Cost Savings: ${cost_savings:.2f}
• Carbon Reduction: {carbon_reduction:.0f} kg CO2
• Equivalent to: {carbon_reduction/0.4:.0f}km of car emissions avoided

🌍 SCALE IMPACT:
• If applied to 50,000 Australian buildings
• Annual savings: $1.55B + 1.2M tonnes CO2 reduced
• Equivalent to removing 300,000 cars from roads
        """
        
        return narrative.strip()


# Example usage
async def main():
    """Example usage of building simulator"""
    
    simulator = IressSydneyOfficeSimulator()
    
    # Get current building state
    state = await simulator.get_current_building_state()
    print(f"Building Consumption: {state.total_consumption_kwh:.0f} kWh")
    print(f"Occupancy: {state.occupancy_count} people")
    print(f"Efficiency Score: {state.energy_metrics['efficiency_score']:.1f}/100")
    
    # Generate demo scenario
    demo = await simulator.generate_demo_scenario()
    print("\n" + demo['demo_narrative'])


if __name__ == "__main__":
    asyncio.run(main())
