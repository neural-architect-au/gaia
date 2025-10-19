import { Paper, Text, Stack, Group, Progress, Divider } from '@mantine/core';
import { useEffect, useState } from 'react';
import { fetchLiveMetrics, LiveMetrics } from '../services/metricsService';

export function EnergyChart() {
  const [currentConsumption, setCurrentConsumption] = useState(2400);
  const [optimizedConsumption, setOptimizedConsumption] = useState(2112);
  const [liveData, setLiveData] = useState<LiveMetrics>({
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
    fetchLiveMetrics().then(setLiveData);
    
    const interval = setInterval(() => {
      setCurrentConsumption((prev) => prev + (Math.random() - 0.5) * 20);
      setOptimizedConsumption((prev) => prev + (Math.random() - 0.5) * 15);
      fetchLiveMetrics().then(setLiveData);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const savings = currentConsumption - optimizedConsumption;
  const savingsPercent = (savings / currentConsumption) * 100;

  return (
    <Paper
      p="xl"
      style={{
        background: '#18191c',
            transition: 'all 0.3s ease',
        border: '1px solid #2C2E33',
      }}
    >
      <Stack gap="xl">
        <div>
          <Text size="lg" fw={600} c="white" mb={4}>
            Energy Consumption
          </Text>
          <Text size="sm" c="dimmed">
            Real-time monitoring and optimization
          </Text>
        </div>

        {/* Main Comparison */}
        <Group grow align="flex-start">
          <Stack gap="xs">
            <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
              Without AI Optimization
            </Text>
            <Text size="3rem" fw={700} c="white" lh={1}>
              {currentConsumption.toFixed(0)}
            </Text>
            <Text size="sm" c="dimmed">
              kWh per day
            </Text>
            <Progress value={100} color="gray" size="lg" mt="md" />
          </Stack>

          <Stack gap="xs">
            <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
              With AI Optimization
            </Text>
            <Text size="3rem" fw={700} c="#2F9E44" lh={1}>
              {optimizedConsumption.toFixed(0)}
            </Text>
            <Text size="sm" c="dimmed">
              kWh per day
            </Text>
            <Progress value={(optimizedConsumption / currentConsumption) * 100} color="green" size="lg" mt="md" />
          </Stack>
        </Group>

        <Paper p="lg" style={{ background: '#0f1012', border: '1px solid #2C2E33' }}>
          <Group justify="space-between">
            <div>
              <Text size="xs" c="dimmed" mb={4}>
                Energy Saved
              </Text>
              <Text size="xl" fw={700} c="#2F9E44">
                {savings.toFixed(0)} kWh
              </Text>
            </div>
            <div>
              <Text size="xs" c="dimmed" mb={4}>
                Efficiency Gain
              </Text>
              <Text size="xl" fw={700} c="#2F9E44">
                {savingsPercent.toFixed(1)}%
              </Text>
            </div>
            <div>
              <Text size="xs" c="dimmed" mb={4}>
                Cost Saved
              </Text>
              <Text size="xl" fw={700} c="#2F9E44">
                ${(savings * 0.35).toFixed(2)}
              </Text>
            </div>
          </Group>
        </Paper>

        <Divider color="#2C2E33" />

        {/* Current Conditions */}
        <div>
          <Text size="sm" fw={600} c="white" mb="md">
            Current Conditions
          </Text>
          <Group grow>
            <Stack gap={4}>
              <Text size="xs" c="dimmed">
                Sydney Weather
              </Text>
              <Text size="lg" fw={600} c="white">
                {liveData.temperature > 0 ? `${liveData.temperature.toFixed(1)}°C` : 'Loading...'}
              </Text>
              <Text size="xs" c="dimmed">
                {liveData.solarIrradiance > 0 
                  ? `${liveData.solarIrradiance} W/m² solar` 
                  : 'Night time (no solar)'}
              </Text>
            </Stack>
            <Stack gap={4}>
              <Text size="xs" c="dimmed">
                Energy Price
              </Text>
              <Text size="lg" fw={600} c="white">
                {liveData.energyPrice > 0 ? `$${(liveData.energyPrice / 1000).toFixed(2)}/kWh` : 'Loading...'}
              </Text>
              <Text size="xs" c="dimmed">
                {liveData.renewablePct > 0 ? `${liveData.renewablePct}% renewable mix` : 'Loading...'}
              </Text>
            </Stack>
            <Stack gap={4}>
              <Text size="xs" c="dimmed">
                Occupancy
              </Text>
              <Text size="lg" fw={600} c="white">
                450/500
              </Text>
              <Text size="xs" c="dimmed">
                90% capacity
              </Text>
            </Stack>
          </Group>
        </div>
      </Stack>
    </Paper>
  );
}
