import { useState, useRef, useEffect } from 'react';
import { Paper, TextInput, ActionIcon, Stack, Box, Text, Group, Avatar } from '@mantine/core';
import { IconSend, IconRobot, IconSparkles } from '@tabler/icons-react';
import ReactMarkdown from 'react-markdown';

interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'agent';
  timestamp: Date;
}

export function IntegratedChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const lastMessageRef = useRef<HTMLDivElement>(null);

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

  const callAgent = async (query: string): Promise<string> => {
    try {
      const response = await fetch('/api/invocations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: query }),
      });
      
      const json = await response.json();
      
      if (json.status === 'error') {
        return `⚠️ ${json.message}`;
      }
      
      return json.response || 'No response';
    } catch (error) {
      console.error('Agent error:', error);
      return '❌ Error connecting to agent';
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

    const agentResponse = await callAgent(query);
    
    const agentMessage: ChatMessage = {
      id: (Date.now() + 1).toString(),
      content: agentResponse,
      sender: 'agent',
      timestamp: new Date(),
    };
    
    setMessages((prev) => [...prev, agentMessage]);
    setIsTyping(false);
  };

  return (
    <Paper
      p="xl"
      style={{
        background: '#18191c',
        border: '1px solid #2C2E33',
        position: 'sticky',
        top: 20,
        zIndex: 10,
      }}
    >
      <Stack gap="md">
        {/* Header */}
        <Group gap="sm">
          <IconSparkles size={24} color="#2F9E44" />
          <div>
            <Text size="lg" fw={600} c="white">
              Ask GAIA
            </Text>
            <Text size="xs" c="dimmed">
              Your AI climate assistant
            </Text>
          </div>
        </Group>

        {/* Input */}
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

        {/* Messages */}
        {messages.length > 0 && (
          <Box
            ref={scrollContainerRef}
            style={{
              height: '300px',
              overflowY: 'auto',
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
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
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
          </Box>
        )}
      </Stack>
    </Paper>
  );
}
