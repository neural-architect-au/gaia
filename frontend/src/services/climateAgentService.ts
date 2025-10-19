/**
 * Climate Agent Service - Connects to local BedrockAgentCore runtime
 */

const RUNTIME_URL = 'http://localhost:8080/invocations';

export interface AgentResponse {
  status: string;
  query: string;
  response: any;
  timestamp: string;
}

export async function invokeClimateAgent(prompt: string): Promise<AgentResponse> {
  try {
    const response = await fetch(RUNTIME_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      throw new Error(`Agent invocation failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Climate agent error:', error);
    throw error;
  }
}
