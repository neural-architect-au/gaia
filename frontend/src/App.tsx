import { MantineProvider, createTheme, AppShell, Container, Grid, Title, Text, Group, Stack, Box, ActionIcon, Tooltip, Button, Badge } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Notifications } from '@mantine/notifications';
import { IconBolt, IconCloud, IconCurrencyDollar, IconLeaf, IconChartBar, IconServer, IconDownload, IconBell } from '@tabler/icons-react';
import { useState, useEffect } from 'react';
import { MetricsHero } from './components/MetricsHero';
import { EnergyChart } from './components/EnergyChart';
import { SystemsStatus } from './components/SystemsStatus';
import { FloatingChat } from './components/FloatingChat';
import { BIDashboard } from './components/BIDashboard';
import { ROIAnalysis } from './components/ROIAnalysis';
import { AWSSpotOptimization } from './components/AWSSpotOptimization';
import { ResourceEfficiency } from './components/ResourceEfficiency';
import { SustainabilityScore } from './components/SustainabilityScore';
import { RegionalCarbonMap } from './components/RegionalCarbonMap';
import { fetchLiveMetrics, LiveMetrics } from './services/metricsService';
import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';

const queryClient = new QueryClient();

const theme = createTheme({
  colorScheme: 'dark',
  primaryColor: 'green',
  colors: {
    dark: [
      '#E0F7E9',
      '#C1C2C5',
      '#A6A7AB',
      '#909296',
      '#5c5f66',
      '#373A40',
      '#2C2E33',
      '#1f2023',
      '#18191c',
      '#0f1012',
    ],
    green: [
      '#E0F7E9',
      '#b2f2bb',
      '#8ce99a',
      '#69db7c',
      '#4CAF50',
      '#40c057',
      '#37b24d',
      '#2F9E44',
      '#2b8a3e',
      '#12400E',
    ],
  },
  defaultRadius: 'md',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
});

function App() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [liveMetrics, setLiveMetrics] = useState<LiveMetrics>({
    costSavingsToday: 85.50,
    carbonReduced: 180,
    efficiencyGain: 12,
    temperature: 24,
    solarIrradiance: 300,
    energyPrice: 65,
    renewablePct: 55,
    sustainabilityScore: 87,
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    fetchLiveMetrics().then(setLiveMetrics);
    const interval = setInterval(() => {
      fetchLiveMetrics().then(setLiveMetrics);
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const quickLinks = [
    { id: 'energy', label: 'Energy', icon: IconBolt },
    { id: 'regions', label: 'Regions', icon: IconCloud },
    { id: 'aws', label: 'AWS', icon: IconServer },
    { id: 'efficiency', label: 'Efficiency', icon: IconChartBar },
    { id: 'roi', label: 'ROI', icon: IconCurrencyDollar },
    { id: 'sustainability', label: 'Sustainability', icon: IconLeaf },
  ];

  return (
    <QueryClientProvider client={queryClient}>
      <MantineProvider theme={theme} defaultColorScheme="dark">
        <Notifications position="top-right" />
        <style>
          {`
            @keyframes pulse {
              0%, 100% {
                opacity: 1;
                box-shadow: 0 0 8px #2F9E44;
              }
              50% {
                opacity: 0.5;
                box-shadow: 0 0 16px #2F9E44;
              }
            }
          `}
        </style>
        <Box
          style={{
            minHeight: '100vh',
            background: '#0f1012',
            overflowY: 'auto',
          }}
          sx={{
            '&::-webkit-scrollbar': {
              width: '12px',
            },
            '&::-webkit-scrollbar-track': {
              background: '#18191c',
            },
            '&::-webkit-scrollbar-thumb': {
              background: '#2F9E44',
              borderRadius: '6px',
            },
            '&::-webkit-scrollbar-thumb:hover': {
              background: '#4CAF50',
            },
          }}
        >
            <Container size="xl" py="xl">
              {/* Header */}
              <Stack gap="md" mb="xl" pb="xl" style={{ borderBottom: '1px solid #2C2E33' }}>
                <Group justify="space-between">
                  <div>
                    <Group gap="xs">
                      <Text size="2.5rem" lh={1}>🌱</Text>
                      <Title order={1} c="white" fw={600}>
                        GAIA
                      </Title>
                    </Group>
                    <Text size="sm" c="dimmed" mt={4} ml={48}>
                      Guardian of Earth's Resources
                    </Text>
                  </div>
                  <Group gap="md">
                    <Stack gap={4} align="flex-end">
                      <Group gap="xs">
                        <div style={{ 
                          width: 8, 
                          height: 8, 
                          borderRadius: '50%', 
                          background: '#2F9E44',
                          boxShadow: '0 0 8px #2F9E44',
                          animation: 'pulse 2s ease-in-out infinite',
                        }} />
                        <Text size="sm" c="dimmed">Live</Text>
                      </Group>
                      <Text size="xs" c="dimmed">
                        {currentTime.toLocaleTimeString()}
                      </Text>
                    </Stack>
                    <ActionIcon.Group>
                      <Tooltip label="3 new optimizations">
                        <ActionIcon size="lg" variant="light" color="green" style={{ position: 'relative' }}>
                          <IconBell size={20} />
                          <Badge
                            size="xs"
                            variant="filled"
                            color="red"
                            style={{
                              position: 'absolute',
                              top: -4,
                              right: -4,
                              padding: '2px 6px',
                            }}
                          >
                            3
                          </Badge>
                        </ActionIcon>
                      </Tooltip>
                      <Tooltip label="Export Report">
                        <ActionIcon size="lg" variant="light" color="green">
                          <IconDownload size={20} />
                        </ActionIcon>
                      </Tooltip>
                    </ActionIcon.Group>
                  </Group>
                </Group>

                {/* Horizontal Navigation Tabs */}
                <Group gap="xs" grow>
                  {quickLinks.map((link) => (
                    <Button
                      key={link.id}
                      variant="light"
                      color="green"
                      leftSection={<link.icon size={20} />}
                      onClick={() => scrollToSection(link.id)}
                      size="lg"
                      fullWidth
                    >
                      {link.label}
                    </Button>
                  ))}
                </Group>
                
                <Group gap="xl">
                  <Group gap="xs">
                    <Text size="xl" fw={700} c="#2F9E44">${liveMetrics.costSavingsToday.toFixed(2)}/day</Text>
                    <Text size="sm" c="dimmed">cost savings</Text>
                  </Group>
                  <Group gap="xs">
                    <Text size="xl" fw={700} c="#2F9E44">{liveMetrics.carbonReduced.toFixed(0)}kg CO₂</Text>
                    <Text size="sm" c="dimmed">reduced daily</Text>
                  </Group>
                  <Group gap="xs">
                    <Text size="xl" fw={700} c="#2F9E44">{liveMetrics.efficiencyGain.toFixed(1)}%</Text>
                    <Text size="sm" c="dimmed">efficiency gain</Text>
                  </Group>
                  <Group gap="xs">
                    <Text size="xl" fw={700} c="#2F9E44">{liveMetrics.renewablePct.toFixed(0)}%</Text>
                    <Text size="sm" c="dimmed">renewable energy</Text>
                  </Group>
                </Group>
              </Stack>

              <Stack gap="xl">
                {/* Hero Metrics */}
                <MetricsHero />

                {/* Main Content Grid */}
                <Grid gutter="xl">
                  <Grid.Col span={{ base: 12, lg: 8 }}>
                    <Stack gap="xl">
                      <div id="energy">
                        <EnergyChart />
                      </div>
                      <div id="regions">
                        <RegionalCarbonMap />
                      </div>
                      <div id="aws">
                        <AWSSpotOptimization />
                      </div>
                      <div id="efficiency">
                        <ResourceEfficiency />
                      </div>
                      <BIDashboard />
                    </Stack>
                  </Grid.Col>

                  <Grid.Col span={{ base: 12, lg: 4 }}>
                    <Stack gap="xl">
                      <div id="sustainability">
                        <SustainabilityScore />
                      </div>
                      <div id="roi">
                        <ROIAnalysis />
                      </div>
                      <SystemsStatus />
                    </Stack>
                  </Grid.Col>
                </Grid>
              </Stack>
            </Container>
          </Box>
        
        {/* Floating Chat Button */}
        <FloatingChat />
      </MantineProvider>
    </QueryClientProvider>
  );
}

export default App;
