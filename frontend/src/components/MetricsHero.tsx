import { Paper, Group, Text, Stack, SimpleGrid, Skeleton } from '@mantine/core';
import { useEffect, useState } from 'react';
import { fetchLiveMetrics, LiveMetrics } from '../services/metricsService';

export function MetricsHero() {
  const [isLoading, setIsLoading] = useState(true);
  const [metrics, setMetrics] = useState<LiveMetrics>({
    costSavingsToday: 0,
    carbonReduced: 0,
    efficiencyGain: 0,
    temperature: 0,
    solarIrradiance: 0,
    energyPrice: 0,
    renewablePct: 0,
    sustainabilityScore: 0,
  });

  useEffect(() => {
    // Fetch live data immediately
    fetchLiveMetrics().then(data => {
      setMetrics(data);
      setIsLoading(false);
    });
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      fetchLiveMetrics().then(setMetrics);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const displayMetrics = [
    {
      label: 'Cost Savings Today',
      value: `$${metrics.costSavingsToday.toFixed(2)}`,
      subtitle: 'On track for $31,207 this year',
      color: '#2F9E44',
    },
    {
      label: 'Carbon Reduced Today',
      value: `${metrics.carbonReduced.toFixed(0)} kg CO₂`,
      subtitle: 'Equivalent to 450 km of driving',
      color: '#2F9E44',
    },
    {
      label: 'Energy Efficiency Gain',
      value: `${metrics.efficiencyGain.toFixed(1)}%`,
      subtitle: '288 kWh saved from 2,400 kWh baseline',
      color: '#2F9E44',
    },
    {
      label: 'Return on Investment',
      value: '300%',
      subtitle: 'Payback period: 4.7 months',
      color: '#2F9E44',
    },
  ];

  if (isLoading) {
    return (
      <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="lg">
        {[1, 2, 3, 4].map((i) => (
          <Paper key={i} p="xl" style={{ background: '#18191c', border: '1px solid #2C2E33' }}>
            <Stack gap="md">
              <Skeleton height={12} width="60%" />
              <Skeleton height={40} width="80%" />
              <Skeleton height={10} width="90%" />
            </Stack>
          </Paper>
        ))}
      </SimpleGrid>
    );
  }

  return (
    <SimpleGrid cols={{ base: 1, sm: 2, lg: 4 }} spacing="lg">
      {displayMetrics.map((metric) => (
        <Paper
          key={metric.label}
          p="xl"
          style={{
            background: '#18191c',
            border: '1px solid #2C2E33',
            transition: 'all 0.3s ease',
            cursor: 'pointer',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-4px)';
            e.currentTarget.style.boxShadow = '0 8px 24px rgba(47, 158, 68, 0.2)';
            e.currentTarget.style.borderColor = '#2F9E44';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = 'none';
            e.currentTarget.style.borderColor = '#2C2E33';
          }}
        >
          <Stack gap="md">
            <Text size="sm" c="dimmed" tt="uppercase" fw={500} lts={0.5}>
              {metric.label}
            </Text>
            <Text size="2.5rem" fw={700} c="white" lh={1}>
              {metric.value}
            </Text>
            <Text size="sm" c="dimmed" lh={1.4}>
              {metric.subtitle}
            </Text>
            <div style={{ 
              height: 3, 
              background: metric.color,
              borderRadius: 2,
              marginTop: 'auto'
            }} />
          </Stack>
        </Paper>
      ))}
    </SimpleGrid>
  );
}
