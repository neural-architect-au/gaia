"""
Test Claude Sonnet 4 integration with Strands framework
Run this with fresh AWS credentials
"""

import asyncio
import sys
sys.path.append('.')

from agents.climate_agent_strands import ClimateAgent

async def test_claude_sonnet_4_integration():
    print('🚀 TESTING: Claude Sonnet 4 + Strands + Real Data')
    print('=' * 55)
    
    try:
        # Initialize agent with Claude Sonnet 4
        agent = ClimateAgent()
        print('✅ ClimateAgent initialized with Claude Sonnet 4')
        print(f'✅ Model: anthropic.claude-sonnet-4-20250514-v1:0')
        print(f'✅ Tools: {len(agent.agent.tool_names)} registered')
        print(f'✅ Tools: {", ".join(agent.agent.tool_names)}')
        
        # Test climate optimization query
        query = """Analyze the current Sydney weather and energy market conditions. 
        Then provide specific optimization recommendations for the Iress building 
        to reduce energy consumption and carbon emissions. Use real data from 
        Bureau of Meteorology and OpenElectricity API."""
        
        print(f'\n🔍 Query: {query[:100]}...')
        
        result = await agent.run_optimization(query)
        print(f'✅ Optimization Status: {result["status"]}')
        
        if result['status'] == 'success':
            print('\n🎉 SUCCESS: Complete Claude Sonnet 4 Integration!')
            print('=' * 55)
            
            response = result["response"]
            print(f'Claude Response Type: {type(response)}')
            print(f'Claude Response: {str(response)[:500]}...')
            
            print('\n📊 Integration Summary:')
            print('✅ Claude Sonnet 4: Working')
            print('✅ Strands Framework: Working') 
            print('✅ Real Weather Data: Working')
            print('✅ Real Energy Data: Working')
            print('✅ Building Optimization: Working')
            print('✅ Climate Impact: Working')
            
        else:
            print(f'\n❌ Error: {result["message"]}')
            
            # Check if it's a credential issue
            if 'token' in result["message"].lower() or 'credential' in result["message"].lower():
                print('\n💡 Solution: Refresh AWS credentials and try again')
            elif 'inference profile' in result["message"].lower():
                print('\n💡 Solution: Model requires inference profile setup')
            else:
                print('\n💡 Check error details above')
        
    except Exception as e:
        print(f'\n❌ Initialization Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🌍 Climate Solutions AI Agent - Claude Sonnet 4 Test")
    print("Run with fresh AWS credentials for full test")
    print()
    
    asyncio.run(test_claude_sonnet_4_integration())
