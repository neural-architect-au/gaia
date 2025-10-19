"""
Strands SDK API Endpoints
AWS AI Agent Global Hackathon 2025
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from ..agents.strands_integration import ClimateSolutionsStrandsAgent

router = APIRouter(prefix="/strands", tags=["Strands SDK"])

# Global Strands agent instance
strands_agent = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str

@router.on_event("startup")
async def initialize_strands_agent():
    """Initialize Strands agent on startup"""
    global strands_agent
    try:
        strands_agent = ClimateSolutionsStrandsAgent()
    except Exception as e:
        print(f"Warning: Strands SDK not available: {e}")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_strands_agent(request: ChatRequest):
    """
    Chat with the ClimateSolutionsAI agent using Strands SDK
    
    Provides natural language interface for:
    - Building energy optimization
    - Energy market analysis  
    - Climate impact calculations
    """
    
    if not strands_agent:
        raise HTTPException(
            status_code=503, 
            detail="Strands agent not available. This may be a demo environment."
        )
    
    try:
        response = await strands_agent.chat(request.message, request.context)
        
        return ChatResponse(
            response=response,
            session_id=request.session_id or "default",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")

@router.get("/demo")
async def strands_demo():
    """
    Demonstrate Strands SDK capabilities
    
    Shows example conversations and tool usage
    """
    
    demo_conversations = [
        {
            "user": "Hello! Can you help me optimize my office building?",
            "agent": "Hello! I'm ClimateSolutionsAI, your autonomous agent for building energy optimization. I can help you reduce energy consumption, save costs, and prevent carbon emissions. What building would you like to optimize?"
        },
        {
            "user": "Optimize the Iress Sydney office with 450 people and 2400 kWh consumption",
            "agent": "I'll optimize the Iress Sydney office for you. Let me analyze the building systems and current energy conditions... ✅ Optimization complete! I've reduced energy consumption by 288 kWh (12% improvement), saving $101 and preventing 216kg of CO2 emissions today."
        },
        {
            "user": "What's the best time to run energy-intensive tasks?",
            "agent": "Based on current Australian energy market conditions, the optimal window is 11:30 AM - 3:30 PM when solar generation is highest (65% renewable energy) and prices are lowest at $67/MWh. This timing will minimize both costs and carbon emissions."
        }
    ]
    
    return {
        "strands_integration": "active",
        "capabilities": [
            "Natural language building optimization",
            "Conversational energy market analysis", 
            "Interactive climate impact calculations",
            "Multi-turn conversation memory",
            "Tool-based autonomous actions"
        ],
        "demo_conversations": demo_conversations,
        "tools_available": [
            "optimize_building_energy",
            "analyze_energy_market", 
            "calculate_climate_impact"
        ]
    }
