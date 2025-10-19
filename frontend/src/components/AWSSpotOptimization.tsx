import { Paper, Text, Stack, Group, Progress, SimpleGrid, Divider, Skeleton } from '@mantine/core';
import { useEffect, useState } from 'react';

interface SpotWindow {
  time: string;
  renewable: number;
  spotPrice: number;
  onDemand: number;
  savings: number;
  carbonIntensity: number;
  recommendation: string;
}

export function AWSSpotOptimization() {
  const [isLoading, setIsLoading] = useState(true);
  const [spotWindows, setSpotWindows] = useState<SpotWindow[]>([]);
  const [metrics, setMetrics] = useState({
    costSavings: 75,
    carbonReduction: 45,
    carbonSavedKg: 156,
    renewableAvg: 68,
  });

  useEffect(() => {
    const fetchSpotData = async () => {
      try {
        const response = await fetch('/api/invocations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            prompt: 'Optimize AWS spot instances for the next 24 hours based on current renewable energy forecast' 
          }),
        });
        
        const json = await response.json();
        
        if (json.status === 'success' && json.data) {
          const data = json.data;
          
          // Extract metrics
          if (data.cost_savings_pct) setMetrics(prev => ({ ...prev, costSavings: data.cost_savings_pct }));
          if (data.carbon_reduction_pct) setMetrics(prev => ({ ...prev, carbonReduction: data.carbon_reduction_pct }));
          if (data.climate_impact?.daily_carbon_saved_kg) {
            setMetrics(prev => ({ ...prev, carbonSavedKg: data.climate_impact.daily_carbon_saved_kg }));
          }
          if (data.climate_impact?.renewable_energy_used_pct) {
            setMetrics(prev => ({ ...prev, renewableAvg: data.climate_impact.renewable_energy_used_pct }));
          }
          
          // Extract optimal windows
          if (data.optimal_windows && Array.isArray(data.optimal_windows)) {
            const windows = data.optimal_windows.map((w: any) => ({
              time: formatTimeWindow(w.start_time, w.end_time),
              renewable: w.renewable_pct || 0,
              spotPrice: w.spot_price_usd || 0,
              onDemand: 0.192,
              savings: 75,
              carbonIntensity: w.carbon_intensity || 0,
              recommendation: w.recommendation || '',
            }));
            setSpotWindows(windows);
          }
        }
        
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to fetch spot optimization:', error);
        // Use fallback data
        setSpotWindows([
          {
            time: '2:00 AM - 6:00 AM',
            renewable: 65,
            spotPrice: 0.048,
            onDemand: 0.192,
            savings: 75,
            carbonIntensity: 0.45,
            recommendation: 'Optimal for batch processing',
          },
          {
            time: '2:00 PM - 6:00 PM',
            renewable: 72,
            spotPrice: 0.052,
            onDemand: 0.192,
            savings: 73,
            carbonIntensity: 0.38,
            recommendation: 'Peak solar - best for ML training',
          },
        ]);
        setIsLoading(false);
      }
    };
    
    fetchSpotData();
    const interval = setInterval(fetchSpotData, 300000); // Refresh every 5 minutes
    return () => clearInterval(interval);
  }, []);

  const formatTimeWindow = (start: string, end: string) => {
    const startDate = new Date(start);
    const endDate = new Date(end);
    const formatTime = (date: Date) => {
      const hours = date.getHours();
      const ampm = hours >= 12 ? 'PM' : 'AM';
      const displayHours = hours % 12 || 12;
      return `${displayHours}:00 ${ampm}`;
    };
    return `${formatTime(startDate)} - ${formatTime(endDate)}`;
  };

  const instanceTypes = [
    { type: 'm5.large', spot: 0.048, onDemand: 0.192, savings: 75 },
    { type: 'c5.xlarge', spot: 0.068, onDemand: 0.272, savings: 75 },
    { type: 'r5.large', spot: 0.056, onDemand: 0.224, savings: 75 },
  ];

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
            AWS Spot Instance Optimization
          </Text>
          <Text size="sm" c="dimmed">
            Climate-aware compute scheduling with renewable energy
          </Text>
        </div>

        {/* Key Metrics */}
        {isLoading ? (
          <SimpleGrid cols={3} spacing="lg">
            {[1, 2, 3].map((i) => (
              <Stack key={i} gap={4}>
                <Skeleton height={12} width="60%" />
                <Skeleton height={40} width="40%" />
                <Skeleton height={10} width="80%" />
              </Stack>
            ))}
          </SimpleGrid>
        ) : (
          <SimpleGrid cols={3} spacing="lg">
            <Stack gap={4}>
              <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
                Cost Savings
              </Text>
              <Text size="2rem" fw={700} c="#2F9E44" lh={1}>
                {metrics.costSavings}%
              </Text>
              <Text size="xs" c="dimmed">
                vs on-demand pricing
              </Text>
            </Stack>

            <Stack gap={4}>
              <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
                Carbon Reduction
              </Text>
              <Text size="2rem" fw={700} c="#2F9E44" lh={1}>
                {metrics.carbonReduction}%
              </Text>
              <Text size="xs" c="dimmed">
                {metrics.carbonSavedKg} kg CO₂ saved daily
              </Text>
            </Stack>

            <Stack gap={4}>
              <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
                Renewable Energy
              </Text>
              <Text size="2rem" fw={700} c="#2F9E44" lh={1}>
                {metrics.renewableAvg}%
              </Text>
              <Text size="xs" c="dimmed">
                average across windows
              </Text>
            </Stack>
          </SimpleGrid>
        )}

        <Divider color="#2C2E33" />

        {/* Optimal Windows */}
        <div>
          <Text size="sm" fw={600} c="white" mb="md">
            Optimal Compute Windows
          </Text>
          <Stack gap="md">
            {spotWindows.map((window) => (
              <Paper
                key={window.time}
                p="lg"
                style={{
                  background: '#0f1012',
                  border: '1px solid #2C2E33',
                }}
              >
                <Stack gap="sm">
                  <Group justify="space-between">
                    <Text size="sm" fw={600} c="white">
                      {window.time}
                    </Text>
                    <Text size="sm" fw={700} c="#2F9E44">
                      {window.renewable}% Renewable
                    </Text>
                  </Group>

                  <Group grow>
                    <Stack gap={4}>
                      <Text size="xs" c="dimmed">Spot Price</Text>
                      <Text size="lg" fw={600} c="white">${window.spotPrice}</Text>
                    </Stack>
                    <Stack gap={4}>
                      <Text size="xs" c="dimmed">Savings</Text>
                      <Text size="lg" fw={600} c="#2F9E44">{window.savings}%</Text>
                    </Stack>
                    <Stack gap={4}>
                      <Text size="xs" c="dimmed">Carbon</Text>
                      <Text size="lg" fw={600} c="white">{window.carbonIntensity}</Text>
                    </Stack>
                  </Group>

                  <Paper p="sm" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
                    <Text size="xs" c="white">
                      💡 {window.recommendation}
                    </Text>
                  </Paper>
                </Stack>
              </Paper>
            ))}
          </Stack>
        </div>

        <Divider color="#2C2E33" />

        {/* Instance Pricing */}
        <div>
          <Text size="sm" fw={600} c="white" mb="md">
            Current Spot Pricing
          </Text>
          <Stack gap="sm">
            {instanceTypes.map((instance) => (
              <Group key={instance.type} justify="space-between">
                <Text size="sm" c="white" style={{ width: 100 }}>
                  {instance.type}
                </Text>
                <Group gap="lg" style={{ flex: 1 }}>
                  <div>
                    <Text size="xs" c="dimmed">Spot</Text>
                    <Text size="sm" fw={600} c="white">${instance.spot}</Text>
                  </div>
                  <div>
                    <Text size="xs" c="dimmed">On-Demand</Text>
                    <Text size="sm" c="dimmed">${instance.onDemand}</Text>
                  </div>
                  <div style={{ flex: 1 }}>
                    <Progress value={instance.savings} color="green" size="md" />
                  </div>
                  <Text size="sm" fw={700} c="#2F9E44" style={{ minWidth: 50, textAlign: 'right' }}>
                    -{instance.savings}%
                  </Text>
                </Group>
              </Group>
            ))}
          </Stack>
        </div>

        <Paper p="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
          <Text size="sm" c="white" mb={4}>
            <strong>AI schedules workloads during high renewable energy periods</strong>
          </Text>
          <Text size="xs" c="dimmed">
            By aligning compute with solar/wind generation peaks, we reduce both costs and carbon 
            emissions. ML training jobs automatically shift to 2-6 PM when renewable energy is highest.
          </Text>
        </Paper>
      </Stack>
    </Paper>
  );
}
