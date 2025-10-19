import { useState, useRef, useEffect } from 'react';
import { Paper, TextInput, ActionIcon, Stack, Box, Text, Group, Avatar, Modal, Badge, Button } from '@mantine/core';
import { IconSend, IconRobot, IconSparkles, IconX, IconBolt, IconCurrencyDollar, IconLeaf, IconCloud, IconTool, IconChartBar } from '@tabler/icons-react';
import ReactMarkdown from 'react-markdown';
import {
  EnergyStatusCard,
  CostSavingsCard,
  CarbonImpactCard,
  OptimizationActionCard,
  SpotWindowCard,
  QuickMetricsGrid,
} from './StreamableComponents';

interface ChatMessage {
  id: string;
  content: string | React.ReactNode;
  sender: 'user' | 'agent';
  timestamp: Date;
}

export function FloatingChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const lastMessageRef = useRef<HTMLDivElement>(null);

  const quickActions = [
    { label: 'Energy Status', icon: IconBolt },
    { label: 'Cost Analysis', icon: IconCurrencyDollar },
    { label: 'Carbon Impact', icon: IconLeaf },
    { label: 'AWS Spot', icon: IconCloud },
    { label: 'Optimize', icon: IconTool },
    { label: 'Metrics', icon: IconChartBar },
  ];

  const generateUIResponse = (query: string, data?: any): React.ReactNode => {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('energy') || lowerQuery.includes('status')) {
      return (
        <Stack gap="sm">
          <EnergyStatusCard data={{ 
            consumption: data?.consumption || 2112, 
            efficiency: data?.efficiency || 12 
          }} />
        </Stack>
      );
    }

    if (lowerQuery.includes('cost') || lowerQuery.includes('savings')) {
      return (
        <Stack gap="sm">
          <CostSavingsCard data={{ 
            today: data?.cost_savings || 85.5, 
            month: 2565 
          }} />
        </Stack>
      );
    }

    if (lowerQuery.includes('carbon') || lowerQuery.includes('co2') || lowerQuery.includes('impact')) {
      return (
        <Stack gap="sm">
          <CarbonImpactCard data={{ 
            reduced: data?.carbon_reduced || 180, 
            baseline: 240, 
            carKm: 450 
          }} />
        </Stack>
      );
    }

    if (lowerQuery.includes('spot') || lowerQuery.includes('aws')) {
      return (
        <Stack gap="sm">
          <SpotWindowCard
            data={{
              timeWindow: data?.time_window || '2:00 PM - 6:00 PM',
              renewable: data?.renewable_pct || 72,
              spotPrice: data?.spot_price || 0.052,
              savings: data?.savings_pct || 73,
              recommendation: 'Peak solar - best for ML training',
            }}
          />
        </Stack>
      );
    }

    if (lowerQuery.includes('optimize') || lowerQuery.includes('recommendation')) {
      return (
        <Stack gap="sm">
          <OptimizationActionCard
            data={{
              description: 'Migrate 3 workloads to AWS Graviton processors',
              savings: data?.optimization_savings || 468,
            }}
          />
        </Stack>
      );
    }

    if (lowerQuery.includes('metric') || lowerQuery.includes('summary')) {
      return (
        <Stack gap="sm">
          <QuickMetricsGrid
            data={{
              metrics: [
                { label: 'Energy Efficiency', value: `+${data?.efficiency || 12}%`, positive: true },
                { label: 'Cost Savings Today', value: `$${data?.cost_savings || 85.50}`, positive: true },
                { label: 'Carbon Reduced', value: `${data?.carbon_reduced || 180} kg CO₂`, positive: true },
                { label: 'Renewable Energy', value: `${data?.renewable_pct || 55}%`, positive: true },
              ],
            }}
          />
        </Stack>
      );
    }

    return null;
  };

  const scrollToLastMessage = () => {
    if (scrollContainerRef.current && lastMessageRef.current) {
      const container = scrollContainerRef.current;
      const lastMessage = lastMessageRef.current;
      const scrollTop = lastMessage.offsetTop - container.offsetTop;
      container.scrollTo({ top: scrollTop, behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToLastMessage();
  }, [messages]);

  const callAgent = async (query: string, onChunk?: (text: string) => void): Promise<{ text: string; data?: any }> => {
    try {
      const response = await fetch('/api/invocations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query, stream: false }),
      });
      
      const json = await response.json();
      
      if (json.status === 'error') {
        return { text: `⚠️ ${json.message}` };
      }
      
      return { 
        text: json.response || 'No response',
        data: json.data
      };
    } catch (error) {
      console.error('Agent error:', error);
      return { text: '❌ Error connecting to agent' };
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const query = input;
    setInput('');
    setIsTyping(true);

    // Get response
    const agentResult = await callAgent(query);
    setIsTyping(false);

    // Generate UI component if applicable
    const uiComponent = generateUIResponse(query, agentResult.data);
    
    const agentMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      content: uiComponent ? (
        <Stack gap="sm">
          <Box sx={{ 
            '& p': { margin: 0, lineHeight: 1.6 },
            '& strong': { color: '#4ade80', fontWeight: 600 },
          }}>
            <ReactMarkdown>{agentResult.text}</ReactMarkdown>
          </Box>
          {uiComponent}
        </Stack>
      ) : agentResult.text,
      sender: 'agent',
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, agentMessage]);
    
    if (!isOpen) {
      setUnreadCount((prev) => prev + 1);
    }
  };

  const handleQuickAction = (action: string) => {
    const prompts: Record<string, string> = {
      'Energy Status': 'Show me current energy status',
      'Cost Analysis': 'Show me cost savings',
      'Carbon Impact': 'Show me carbon impact',
      'AWS Spot': 'Show me AWS spot windows',
      'Optimize': 'Show me optimization opportunities',
      'Metrics': 'Show me quick metrics',
    };
    setInput(prompts[action] || action);
  };

  const handleOpen = () => {
    setIsOpen(true);
    setUnreadCount(0);
  };

  return (
    <>
      {/* Floating Button */}
      <Box
        style={{
          position: 'fixed',
          bottom: 32,
          right: 32,
          zIndex: 1000,
        }}
      >
        <style>
          {`
            @keyframes chatPulse {
              0%, 100% {
                box-shadow: 0 12px 32px rgba(47, 158, 68, 0.5);
              }
              50% {
                box-shadow: 0 12px 48px rgba(47, 158, 68, 0.8);
              }
            }
          `}
        </style>
        <Stack gap={8} align="center">
          <ActionIcon
            size={80}
            radius="xl"
            variant="filled"
            color="green"
            onClick={handleOpen}
            style={{
              boxShadow: '0 12px 32px rgba(47, 158, 68, 0.5)',
              transition: 'all 0.3s ease',
              animation: 'chatPulse 2s ease-in-out infinite',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.15)';
              e.currentTarget.style.boxShadow = '0 16px 48px rgba(47, 158, 68, 0.8)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
              e.currentTarget.style.boxShadow = '0 12px 32px rgba(47, 158, 68, 0.5)';
            }}
          >
            <IconSparkles size={40} />
          </ActionIcon>
          <Text 
            size="sm" 
            fw={600} 
            c="white"
            style={{
              textShadow: '0 2px 8px rgba(0, 0, 0, 0.5)',
              pointerEvents: 'none',
            }}
          >
            Ask GAIA
          </Text>
        </Stack>
        {unreadCount > 0 && (
          <Badge
            size="lg"
            variant="filled"
            color="red"
            style={{
              position: 'absolute',
              top: -4,
              right: -4,
              minWidth: 24,
              height: 24,
            }}
          >
            {unreadCount}
          </Badge>
        )}
      </Box>

      {/* Chat Modal */}
      <Modal
        opened={isOpen}
        onClose={() => setIsOpen(false)}
        size="xl"
        padding={0}
        withCloseButton={false}
        centered
        styles={{
          content: {
            background: '#18191c',
            border: '1px solid #2C2E33',
            maxWidth: '900px',
            height: '80vh',
          },
          body: {
            height: '100%',
            padding: 0,
          },
        }}
      >
        <Box style={{ height: '100%', width: '100%', position: 'relative', display: 'flex', flexDirection: 'column' }}>
          {/* Header */}
          <Box
            p="lg"
            style={{
              borderBottom: '1px solid #2C2E33',
              background: '#0f1012',
              flexShrink: 0,
            }}
          >
            <Group justify="space-between">
              <Group gap="sm">
                <IconSparkles size={24} color="#2F9E44" />
                <div>
                  <Text size="lg" fw={600} c="white">
                    GAIA
                  </Text>
                  <Text size="xs" c="dimmed">
                    Guardian of Earth's Resources
                  </Text>
                </div>
              </Group>
              <ActionIcon
                variant="subtle"
                color="gray"
                onClick={() => setIsOpen(false)}
              >
                <IconX size={20} />
              </ActionIcon>
            </Group>
          </Box>

          {/* Quick Actions */}
          <Box p="md" style={{ borderBottom: '1px solid #2C2E33' }}>
            <Group gap="xs">
              {quickActions.map((action) => (
                <Button
                  key={action.label}
                  size="xs"
                  variant="light"
                  color="green"
                  leftSection={<action.icon size={14} />}
                  onClick={() => handleQuickAction(action.label)}
                  styles={{
                    root: {
                      fontSize: '11px',
                      height: '28px',
                      padding: '0 10px',
                    },
                  }}
                >
                  {action.label}
                </Button>
              ))}
            </Group>
          </Box>

          {/* Messages */}
          <Box
            ref={scrollContainerRef}
            style={{
              flex: 1,
              overflowY: 'auto',
              padding: '16px',
            }}
            sx={{
              '&::-webkit-scrollbar': {
                width: '8px',
              },
              '&::-webkit-scrollbar-track': {
                background: '#18191c',
              },
              '&::-webkit-scrollbar-thumb': {
                background: '#2F9E44',
                borderRadius: '4px',
              },
            }}
          >
            {messages.length === 0 ? (
              <Box style={{ textAlign: 'center', padding: '48px 16px' }}>
                <IconSparkles size={48} color="#2F9E44" style={{ margin: '0 auto 16px' }} />
                <Text size="lg" fw={600} c="white" mb="xs">
                  Hi! I'm GAIA
                </Text>
                <Text size="sm" c="dimmed">
                  Ask me about energy optimization, costs, carbon impact, or AWS infrastructure
                </Text>
              </Box>
            ) : (
              <Stack gap="md">
                {messages.map((msg, index) => (
                  <Box
                    key={msg.id}
                    ref={index === messages.length - 1 ? lastMessageRef : null}
                    p="md"
                    style={{
                      background: msg.sender === 'agent' ? 'rgba(47, 158, 68, 0.1)' : 'rgba(59, 130, 246, 0.1)',
                      border: msg.sender === 'agent' ? '1px solid rgba(47, 158, 68, 0.3)' : '1px solid rgba(59, 130, 246, 0.3)',
                      borderRadius: 8,
                    }}
                  >
                    <Group align="flex-start" gap="sm" mb="xs">
                      <Avatar size="sm" color={msg.sender === 'agent' ? 'green' : 'blue'} variant="light">
                        {msg.sender === 'agent' ? <IconRobot size={16} /> : msg.content[0]}
                      </Avatar>
                      <Text size="xs" c="dimmed" fw={500}>
                        {msg.sender === 'agent' ? 'GAIA' : 'You'}
                      </Text>
                    </Group>
                    <Box
                      ml={36}
                      sx={{
                        '& p': { margin: 0, lineHeight: 1.6 },
                        '& strong': { color: '#4ade80', fontWeight: 600 },
                        '& ul, & ol': { marginTop: '0.5rem', marginBottom: '0.5rem' },
                        '& li': { marginBottom: '0.25rem' },
                      }}
                    >
                      {typeof msg.content === 'string' ? (
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      ) : (
                        msg.content
                      )}
                    </Box>
                  </Box>
                ))}
                {isTyping && (
                  <Box
                    p="md"
                    style={{
                      background: 'rgba(47, 158, 68, 0.1)',
                      border: '1px solid rgba(47, 158, 68, 0.3)',
                      borderRadius: 8,
                    }}
                  >
                    <Group gap="xs">
                      <Avatar size="sm" color="green" variant="light">
                        <IconRobot size={16} />
                      </Avatar>
                      <Text size="sm" c="dimmed">GAIA is analyzing...</Text>
                    </Group>
                  </Box>
                )}
              </Stack>
            )}
          </Box>

          {/* Input */}
          <Box
            p="md"
            style={{
              borderTop: '1px solid #2C2E33',
              background: '#0f1012',
              flexShrink: 0,
            }}
          >
            <Group gap="xs">
              <TextInput
                flex={1}
                placeholder="Ask about energy, costs, carbon, AWS..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                styles={{
                  input: {
                    background: '#18191c',
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
        </Box>
      </Modal>
    </>
  );
}
