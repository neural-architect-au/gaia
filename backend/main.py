"""
ClimateSolutionsAI Agent - FastAPI Backend
Professional autonomous AI agent for climate solutions
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agents.climate_agent import ClimateSolutionsAgent, ClimateMetrics
from services.australian_energy_api import AustralianEnergyAPI
from services.building_simulator import IressSydneyOfficeSimulator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
climate_agent = None
energy_api = None
building_simulator = None
optimization_history = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup"""
    global climate_agent, energy_api, building_simulator
    
    logger.info("Initializing ClimateSolutionsAI services...")
    
    # Initialize services
    climate_agent = ClimateSolutionsAgent()
    energy_api = AustralianEnergyAPI()
    building_simulator = IressSydneyOfficeSimulator()
    
    logger.info("Services initialized successfully")
    yield
    
    logger.info("Shutting down services...")


# Create FastAPI app
app = FastAPI(
    title="ClimateSolutionsAI Agent",
    description="Autonomous AI Agent for Climate Solutions",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class OptimizationRequest(BaseModel):
    building_id: str = "iress_sydney_office"
    duration_hours: int = 1
    include_weather: bool = True


class OptimizationResponse(BaseModel):
    success: bool
    optimization_id: str
    metrics: Optional[ClimateMetrics]
    message: str
    timestamp: datetime


class DashboardData(BaseModel):
    current_consumption: float
    optimized_consumption: float
    cost_savings: float
    carbon_reduction: float
    efficiency_improvement: float
    energy_pricing: Dict[str, Any]
    weather_data: Dict[str, Any]
    building_systems: List[Dict[str, Any]]
    optimization_history: List[Dict[str, Any]]


# API Endpoints

@app.get("/")
async def root():
    """API information"""
    return {
        "name": "ClimateSolutionsAI Agent",
        "description": "Autonomous AI Agent for Climate Solutions",
        "version": "1.0.0",
        "endpoints": {
            "optimize": "/optimize - Run climate optimization",
            "dashboard": "/dashboard - Get dashboard data",
            "status": "/status - System status",
            "demo": "/demo - Generate demo scenario"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "climate_agent": climate_agent is not None,
            "energy_api": energy_api is not None,
            "building_simulator": building_simulator is not None
        }
    }


@app.post("/optimize", response_model=OptimizationResponse)
async def run_optimization(request: OptimizationRequest, background_tasks: BackgroundTasks):
    """Run autonomous climate optimization"""
    
    try:
        logger.info(f"Starting optimization for {request.building_id}")
        
        # Get current energy and weather data
        energy_data = await energy_api.get_current_energy_pricing()
        weather_forecast = await energy_api.get_weather_forecast(24)
        
        # Get building state
        weather_dict = {
            'temperature': weather_forecast[0].temperature,
            'solar_irradiance': weather_forecast[0].solar_irradiance,
            'wind_speed': weather_forecast[0].wind_speed
        } if request.include_weather else None
        
        building_state = await building_simulator.get_current_building_state(weather_dict)
        
        # Prepare data for climate agent
        building_data = {
            'current_consumption_kwh': building_state.total_consumption_kwh,
            'occupancy_count': building_state.occupancy_count,
            'weather': weather_dict,
            'energy_price_per_kwh': energy_data.price_per_mwh / 1000,
            'carbon_intensity_kg_per_kwh': energy_data.carbon_intensity,
            'hvac_load': next(s.current_load_pct for s in building_state.systems if s.system_type == 'hvac'),
            'lighting_load': next(s.current_load_pct for s in building_state.systems if s.system_type == 'lighting'),
            'server_load': sum(s.current_load_pct for s in building_state.systems if s.system_type == 'servers') / 2,
            'other_load': next(s.current_load_pct for s in building_state.systems if s.system_type == 'other')
        }
        
        # Run autonomous optimization
        metrics = await climate_agent.autonomous_optimization_cycle(building_data)
        
        # Generate optimization ID
        optimization_id = f"opt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store in history
        optimization_record = {
            'id': optimization_id,
            'timestamp': datetime.now(),
            'building_id': request.building_id,
            'metrics': metrics.dict(),
            'energy_data': energy_data.dict(),
            'building_data': building_data
        }
        optimization_history.append(optimization_record)
        
        # Keep only last 50 records
        if len(optimization_history) > 50:
            optimization_history.pop(0)
        
        logger.info(f"Optimization complete: {metrics.efficiency_improvement_pct:.1f}% improvement")
        
        return OptimizationResponse(
            success=True,
            optimization_id=optimization_id,
            metrics=metrics,
            message=f"Optimization complete: {metrics.efficiency_improvement_pct:.1f}% efficiency improvement",
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
