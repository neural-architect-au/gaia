import { Paper, Text, Stack, Group, Progress, Badge, SimpleGrid } from '@mantine/core';

export function RegionalCarbonMap() {
  const regions = [
    {
      name: 'ap-southeast-2',
      location: 'Sydney',
      renewable: 45,
      carbonIntensity: 0.75,
      status: 'moderate',
      color: 'yellow',
    },
    {
      name: 'ap-southeast-4',
      location: 'Melbourne',
      renewable: 78,
      carbonIntensity: 0.32,
      status: 'excellent',
      color: 'green',
      recommended: true,
    },
    {
      name: 'us-west-2',
      location: 'Oregon',
      renewable: 82,
      carbonIntensity: 0.28,
      status: 'excellent',
      color: 'green',
    },
    {
      name: 'eu-north-1',
      location: 'Stockholm',
      renewable: 95,
      carbonIntensity: 0.08,
      status: 'best',
      color: 'green',
    },
    {
      name: 'us-east-1',
      location: 'Virginia',
      renewable: 38,
      carbonIntensity: 0.82,
      status: 'high',
      color: 'orange',
    },
    {
      name: 'ap-south-1',
      location: 'Mumbai',
      renewable: 28,
      carbonIntensity: 0.92,
      status: 'high',
      color: 'orange',
    },
  ];

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      best: '🌟 Best',
      excellent: '✅ Excellent',
      moderate: '⚠️ Moderate',
      high: '🔴 High Carbon',
    };
    return labels[status] || status;
  };

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
            AWS Regional Carbon Footprint
          </Text>
          <Text size="sm" c="dimmed">
            Choose regions with higher renewable energy mix
          </Text>
        </div>

        {/* Regions Grid */}
        <SimpleGrid cols={2} spacing="md">
          {regions.map((region) => (
            <Paper
              key={region.name}
              p="md"
              style={{
                background: region.recommended ? 'rgba(47, 158, 68, 0.1)' : '#0f1012',
                border: region.recommended
                  ? '2px solid rgba(47, 158, 68, 0.5)'
                  : '1px solid #2C2E33',
              }}
            >
              <Stack gap="sm">
                <Group justify="space-between">
                  <div>
                    <Text size="sm" fw={600} c="white">
                      {region.location}
                    </Text>
                    <Text size="xs" c="dimmed">
                      {region.name}
                    </Text>
                  </div>
                  {region.recommended && (
                    <Badge size="sm" color="green" variant="light">
                      Recommended
                    </Badge>
                  )}
                </Group>

                <Stack gap={4}>
                  <Group justify="space-between">
                    <Text size="xs" c="dimmed">
                      Renewable Energy
                    </Text>
                    <Text size="xs" fw={600} c={region.color === 'green' ? '#2F9E44' : region.color}>
                      {region.renewable}%
                    </Text>
                  </Group>
                  <Progress value={region.renewable} color={region.color} size="sm" />
                </Stack>

                <Group justify="space-between">
                  <Text size="xs" c="dimmed">
                    Carbon Intensity
                  </Text>
                  <Text size="xs" fw={600} c="white">
                    {region.carbonIntensity} kg/kWh
                  </Text>
                </Group>

                <Text size="xs" c="dimmed">
                  {getStatusLabel(region.status)}
                </Text>
              </Stack>
            </Paper>
          ))}
        </SimpleGrid>

        {/* Recommendation */}
        <Paper
          p="md"
          style={{
            background: 'rgba(47, 158, 68, 0.1)',
            border: '1px solid rgba(47, 158, 68, 0.3)',
          }}
        >
          <Text size="sm" fw={600} c="white" mb={4}>
            💡 Regional Optimization
          </Text>
          <Text size="sm" c="white" mb="xs">
            <strong>Melbourne (ap-southeast-4)</strong> is your best choice in Australia
          </Text>
          <Text size="xs" c="dimmed">
            78% renewable energy mix (mostly hydro and wind) vs Sydney's 45%. Migrating workloads
            to Melbourne could reduce your carbon footprint by 57% while maintaining low latency
            for Australian users.
          </Text>
        </Paper>

        {/* Quick Stats */}
        <Group grow>
          <Stack gap={4}>
            <Text size="xs" c="dimmed">
              Cleanest Region
            </Text>
            <Text size="sm" fw={600} c="#2F9E44">
              Stockholm (95%)
            </Text>
          </Stack>
          <Stack gap={4}>
            <Text size="xs" c="dimmed">
              Best in APAC
            </Text>
            <Text size="sm" fw={600} c="#2F9E44">
              Melbourne (78%)
            </Text>
          </Stack>
          <Stack gap={4}>
            <Text size="xs" c="dimmed">
              Potential Savings
            </Text>
            <Text size="sm" fw={600} c="#2F9E44">
              57% CO₂
            </Text>
          </Stack>
        </Group>
      </Stack>
    </Paper>
  );
}
