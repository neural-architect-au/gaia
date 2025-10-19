import { useState } from 'react';
import {
  TextInput,
  ScrollArea,
  Text,
  Group,
  Avatar,
  Stack,
  ActionIcon,
  Box,
  Button,
} from '@mantine/core';
import { IconSend, IconRobot, IconUser, IconSparkles } from '@tabler/icons-react';
import ReactMarkdown from 'react-markdown';
import {
  EnergyStatusCard,
  CostSavingsCard,
  CarbonImpactCard,
  OptimizationActionCard,
  SpotWindowCard,
  QuickMetricsGrid,
} from './StreamableComponents';

interface Message {
  id: string;
  content: string | React.ReactNode;
  sender: 'user' | 'agent';
  timestamp: Date;
}

export function ClimateAgentChat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "👋 Hi! I'm GAIA, your AI partner in sustainable infrastructure. I help optimize energy, reduce costs, and minimize carbon emissions. What would you like to explore?",
      sender: 'agent',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [useRealAgent, setUseRealAgent] = useState(true); // Toggle for demo

  const quickActions = [
    '⚡ Energy Status',
    '💰 Cost Analysis',
    '🌱 Carbon Impact',
    '☁️ AWS Spot',
    '🔧 Optimize',
    '📊 Metrics',
  ];

  // Call real agent
  const callRealAgent = async (query: string): Promise<string> => {
    try {
      const response = await fetch('/api/invocations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query }),
      });
      
      const json = await response.json();
      console.log('Response:', json);
      
      if (json.status === 'error') {
        return `⚠️ Agent error: ${json.message}`;
      }
      
      return json.response || 'No response from agent';
    } catch (error) {
      console.error('Agent error:', error);
      return '❌ Error connecting to agent. Check if runtime is running.';
    }
  };

  // Generate UI components based on query
  const generateUIResponse = (query: string): React.ReactNode => {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('energy') || lowerQuery.includes('status')) {
      return (
        <Stack gap="sm">
          <Text size="md" c="white">Great question! Here's your current energy performance:</Text>
          <EnergyStatusCard
            data={{
              consumption: 2112,
              efficiency: 12,
            }}
          />
          <Text size="sm" c="dimmed">
            You're doing fantastic! 12% better than baseline means you're saving 288 kWh daily. Keep it up! 🌱
          </Text>
        </Stack>
      );
    }

    if (lowerQuery.includes('cost') || lowerQuery.includes('savings')) {
      return (
        <Stack gap="sm">
          <Text size="md" c="white">Let me show you the financial impact:</Text>
          <CostSavingsCard
            data={{
              today: 85.5,
              month: 2565,
            }}
          />
          <Text size="sm" c="dimmed">
            Excellent progress! You're on track to save $31,207 this year - that's 28% above target! 💰
          </Text>
        </Stack>
      );
    }

    if (lowerQuery.includes('carbon') || lowerQuery.includes('co2') || lowerQuery.includes('impact')) {
      return (
        <Stack gap="sm">
          <Text size="md" c="white">Here's your environmental impact:</Text>
          <CarbonImpactCard
            data={{
              reduced: 180,
              baseline: 240,
              carKm: 450,
            }}
          />
          <Text size="sm" c="dimmed">
            Amazing! That's like removing 45 cars from the road every single day. Your planet thanks you! 🌍
          </Text>
        </Stack>
      );
    }

    if (lowerQuery.includes('spot') || lowerQuery.includes('aws')) {
      return (
        <Stack gap="sm">
          <Text size="md" c="white">I found the perfect compute window for you:</Text>
          <SpotWindowCard
            data={{
              timeWindow: '2:00 PM - 6:00 PM',
              renewable: 72,
              spotPrice: 0.052,
              savings: 73,
              recommendation: 'Peak solar - best for ML training',
            }}
          />
          <Text size="sm" c="dimmed">
            Pro tip: Schedule your workloads during this window to maximize renewable energy and minimize costs! ☀️
          </Text>
        </Stack>
      );
    }

    if (lowerQuery.includes('optimize') || lowerQuery.includes('recommendation')) {
      return (
        <Stack gap="sm">
          <Text size="md" c="white">I've identified some opportunities for you:</Text>
          <OptimizationActionCard
            data={{
              description: 'Migrate 3 workloads to AWS Graviton processors for better performance per watt',
              savings: 468,
            }}
          />
          <OptimizationActionCard
            data={{
              description: 'Right-size over-provisioned instances (prod-api-server, analytics-db)',
              savings: 312,
            }}
          />
          <Text size="sm" c="dimmed">
            These changes could save you $780/month while reducing energy consumption. Want me to help implement them? 🚀
          </Text>
        </Stack>
      );
    }

    if (lowerQuery.includes('metric') || lowerQuery.includes('summary')) {
      return (
        <Stack gap="sm">
          <Text size="md" c="white">Here's your quick snapshot:</Text>
          <QuickMetricsGrid
            data={{
              metrics: [
                { label: 'Energy Efficiency', value: '+12%', positive: true },
                { label: 'Cost Savings Today', value: '$85.50', positive: true },
                { label: 'Carbon Reduced', value: '180 kg CO₂', positive: true },
                { label: 'AWS Spot Savings', value: '75%', positive: true },
                { label: 'Sustainability Score', value: '87/100', positive: true },
              ],
            }}
          />
          <Text size="sm" c="dimmed">
            All systems are performing excellently! You're exceeding targets across the board. 📊
          </Text>
        </Stack>
      );
    }

    // Default text response
    return (
      <Text size="md" c="white">
        I can help you with energy optimization, cost analysis, carbon tracking, AWS infrastructure, and sustainability insights. What interests you most?
      </Text>
    );
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const query = input;
    setInput('');
    setIsTyping(true);

    try {
      if (useRealAgent) {
        // Call real AWS agent
        const agentResponse = await callRealAgent(query);
        
        // Check if we should render UI components based on query
        const lowerQuery = query.toLowerCase();
        const shouldRenderUI = lowerQuery.includes('energy') || lowerQuery.includes('cost') || 
                               lowerQuery.includes('carbon') || lowerQuery.includes('spot') ||
                               lowerQuery.includes('optimize') || lowerQuery.includes('metric');
        
        const agentMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: shouldRenderUI ? (
            <Stack gap="sm">
              <Box sx={{ 
                '& p': { margin: 0, lineHeight: 1.6 },
                '& strong': { color: '#4ade80', fontWeight: 600 },
              }}>
                <ReactMarkdown>{agentResponse}</ReactMarkdown>
              </Box>
              {generateUIResponse(query)}
            </Stack>
          ) : agentResponse,
          sender: 'agent',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, agentMessage]);
      } else {
        // Use demo UI components
        setTimeout(() => {
          const agentMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: generateUIResponse(query),
            sender: 'agent',
            timestamp: new Date(),
          };
          setMessages((prev) => [...prev, agentMessage]);
        }, 1000);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickAction = (action: string) => {
    const prompts: Record<string, string> = {
      '⚡ Energy Status': 'Show me current energy status',
      '💰 Cost Analysis': 'Show me cost savings',
      '🌱 Carbon Impact': 'Show me carbon impact',
      '☁️ AWS Spot': 'Show me AWS spot windows',
      '🔧 Optimize': 'Show me optimization opportunities',
      '📊 Metrics': 'Show me quick metrics',
    };
    setInput(prompts[action] || action);
  };

  return (
    <Stack gap={0} h="100%" style={{ display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box p="xl" style={{ borderBottom: '1px solid #2C2E33' }}>
        <Group gap="sm" mb="md">
          <IconSparkles size={32} color="#2F9E44" />
          <div>
            <Text size="xl" fw={700} c="white">
              GAIA
            </Text>
            <Text size="sm" c="dimmed">
              Guardian of Earth's Resources
            </Text>
          </div>
        </Group>

        {/* Quick Actions */}
        <Group gap="xs">
          {quickActions.map((action) => (
            <Button
              key={action}
              size="xs"
              variant="light"
              color="green"
              onClick={() => handleQuickAction(action)}
              styles={{
                root: {
                  fontSize: '10px',
                  height: '24px',
                  padding: '0 8px',
                },
              }}
            >
              {action}
            </Button>
          ))}
        </Group>
      </Box>

      {/* Messages */}
      <ScrollArea 
        style={{ flex: 1 }} 
        p="md" 
        type="auto"
        styles={{
          scrollbar: {
            '&[data-orientation="vertical"] .mantine-ScrollArea-thumb': {
              backgroundColor: '#2F9E44',
            },
          },
        }}
      >
        <Stack gap="md">
          {messages.map((msg) => (
            <Group
              key={msg.id}
              align="flex-start"
              gap="sm"
              justify={msg.sender === 'user' ? 'flex-end' : 'flex-start'}
              wrap="nowrap"
            >
              {msg.sender === 'agent' && (
                <Avatar size="sm" color="green" variant="light" style={{ flexShrink: 0 }}>
                  <IconRobot size={18} />
                </Avatar>
              )}
              <Box
                style={{
                  maxWidth: msg.sender === 'user' ? '85%' : '100%',
                  width: msg.sender === 'agent' ? '100%' : 'auto',
                }}
              >
                {typeof msg.content === 'string' ? (
                  <Box
                    p="md"
                    style={{
                      background:
                        msg.sender === 'agent'
                          ? 'rgba(47, 158, 68, 0.1)'
                          : 'rgba(59, 130, 246, 0.1)',
                      border:
                        msg.sender === 'agent'
                          ? '1px solid rgba(47, 158, 68, 0.3)'
                          : '1px solid rgba(59, 130, 246, 0.3)',
                      borderRadius: 8,
                    }}
                  >
                    <Box sx={{ 
                      '& p': { margin: 0, lineHeight: 1.6 },
                      '& strong': { color: '#4ade80', fontWeight: 600 },
                      '& ul, & ol': { marginTop: '0.5rem', marginBottom: '0.5rem' },
                      '& li': { marginBottom: '0.25rem' }
                    }}>
                      <ReactMarkdown>{msg.content as string}</ReactMarkdown>
                    </Box>
                    <Text size="sm" c="dimmed" mt="xs">
                      {msg.timestamp.toLocaleTimeString()}
                    </Text>
                  </Box>
                ) : (
                  <Box>
                    {msg.content}
                    <Text size="xs" c="dimmed" mt="xs">
                      {msg.timestamp.toLocaleTimeString()}
                    </Text>
                  </Box>
                )}
              </Box>
              {msg.sender === 'user' && (
                <Avatar size="sm" color="blue" variant="light" style={{ flexShrink: 0 }}>
                  <IconUser size={18} />
                </Avatar>
              )}
            </Group>
          ))}
          {isTyping && (
            <Group align="flex-start" gap="sm">
              <Avatar size="sm" color="green" variant="light">
                <IconRobot size={18} />
              </Avatar>
              <Box
                p="md"
                style={{
                  background: 'rgba(47, 158, 68, 0.1)',
                  border: '1px solid rgba(47, 158, 68, 0.3)',
                  borderRadius: 8,
                }}
              >
                <Group gap="xs">
                  <Text size="sm" c="dimmed">
                    GAIA is analyzing
                  </Text>
                  <style>
                    {`
                      @keyframes blink {
                        0%, 20% { opacity: 0.2; }
                        40% { opacity: 1; }
                        60%, 100% { opacity: 0.2; }
                      }
                      .typing-dot { animation: blink 1.4s infinite; }
                      .typing-dot:nth-child(2) { animation-delay: 0.2s; }
                      .typing-dot:nth-child(3) { animation-delay: 0.4s; }
                    `}
                  </style>
                  <Group gap={2}>
                    <div className="typing-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#2F9E44' }} />
                    <div className="typing-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#2F9E44' }} />
                    <div className="typing-dot" style={{ width: 6, height: 6, borderRadius: '50%', background: '#2F9E44' }} />
                  </Group>
                </Group>
              </Box>
            </Group>
          )}
        </Stack>
      </ScrollArea>

      {/* Input */}
      <Box p="md" style={{ borderTop: '1px solid #2C2E33' }}>
        <Group gap="xs">
          <TextInput
            flex={1}
            placeholder="Ask about energy, costs, carbon, AWS..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            styles={{
              input: {
                background: '#0f1012',
                border: '1px solid #2C2E33',
                color: 'white',
              },
            }}
          />
          <ActionIcon
            size="lg"
            variant="filled"
            color="green"
            onClick={handleSend}
            disabled={!input.trim()}
          >
            <IconSend size={18} />
          </ActionIcon>
        </Group>
      </Box>
    </Stack>
  );
}
