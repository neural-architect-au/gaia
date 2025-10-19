import { BedrockAgentRuntimeClient, InvokeAgentCommand } from "@aws-sdk/client-bedrock-agent-runtime";

const AGENT_ARN = "arn:aws:bedrock-agentcore:ap-southeast-2:117982239532:runtime/climate_core-7Zp6WKHpg4";
const REGION = "ap-southeast-2";

// Initialize client with credentials from environment
const client = new BedrockAgentRuntimeClient({
  region: REGION,
  credentials: {
    accessKeyId: import.meta.env.VITE_AWS_ACCESS_KEY_ID || "",
    secretAccessKey: import.meta.env.VITE_AWS_SECRET_ACCESS_KEY || "",
    sessionToken: import.meta.env.VITE_AWS_SESSION_TOKEN,
  },
});

export async function invokeAgent(prompt: string): Promise<string> {
  const command = new InvokeAgentCommand({
    agentId: AGENT_ARN,
    sessionId: crypto.randomUUID(),
    inputText: prompt,
  });

  const response = await client.send(command);
  
  // Parse streaming response
  if (response.completion) {
    let fullResponse = "";
    for await (const event of response.completion) {
      if (event.chunk?.bytes) {
        const text = new TextDecoder().decode(event.chunk.bytes);
        fullResponse += text;
      }
    }
    return fullResponse;
  }
  
  return "No response from agent";
}
