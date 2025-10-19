import { Grid, Card, Text, Progress, Group, Badge, Stack } from '@mantine/core';
import { useQuery } from '@tanstack/react-query';

interface BuildingMetrics {
  consumption_kwh: number;
  cost_savings_aud: number;
  carbon_reduction_kg: number;
  efficiency_pct: number;
  renewable_pct: number;
  spot_price: number;
}

export function BuildingDashboard() {
  const { data: metrics, isLoading } = useQuery<BuildingMetrics>({
    queryKey: ['building-metrics'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/dashboard');
      if (!response.ok) throw new Error('Failed to fetch metrics');
      return response.json();
    },
    refetchInterval: 30000
  });

  if (isLoading) {
    return <Text>Loading climate data...</Text>;
  }

  return (
    <Stack p="md">
      <Text size="xl" fw={700}>🌍 Climate Solutions AI Dashboard</Text>
      
      <Grid>
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg">
            <Text size="sm" c="dimmed">Energy Consumption</Text>
            <Text size="xl" fw={700}>{metrics?.consumption_kwh || 2112} kWh</Text>
            <Progress value={88} color="green" size="sm" mt="xs" />
            <Text size="xs" c="green">12% reduction achieved</Text>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg">
            <Text size="sm" c="dimmed">Daily Savings</Text>
            <Text size="xl" fw={700}>${metrics?.cost_savings_aud || 85}</Text>
            <Badge color="green" size="sm" mt="xs">+$85/day</Badge>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg">
            <Text size="sm" c="dimmed">CO₂ Prevented</Text>
            <Text size="xl" fw={700}>{metrics?.carbon_reduction_kg || 180}kg</Text>
            <Text size="xs" c="blue">≈ 450km car emissions</Text>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={3}>
          <Card shadow="sm" padding="lg">
            <Text size="sm" c="dimmed">Renewables</Text>
            <Text size="xl" fw={700}>{metrics?.renewable_pct || 75}%</Text>
            <Badge color="teal" size="sm" mt="xs">High Solar</Badge>
          </Card>
        </Grid.Col>
      </Grid>
      
      <Grid>
        <Grid.Col span={6}>
          <Card shadow="sm" padding="lg">
            <Text fw={600} mb="md">🏢 System Status</Text>
            <Group>
              <Badge color="green">HVAC: Optimal</Badge>
              <Badge color="yellow">Lighting: Energy Saving</Badge>
              <Badge color="red">Servers: High Load</Badge>
            </Group>
          </Card>
        </Grid.Col>
        
        <Grid.Col span={6}>
          <Card shadow="sm" padding="lg">
            <Text fw={600} mb="md">☁️ AWS Spot Pricing</Text>
            <Text size="lg">${metrics?.spot_price || 0.048}/hour</Text>
            <Text size="xs" c="dimmed">m5.large ap-southeast-2</Text>
          </Card>
        </Grid.Col>
      </Grid>
    </Stack>
  );
}
