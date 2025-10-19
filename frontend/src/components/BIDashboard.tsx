import { Paper, Text, Stack, Group, SimpleGrid, Divider } from '@mantine/core';

export function BIDashboard() {
  const trends = [
    { period: 'Today', actual: 85, target: 80, status: 'ahead' },
    { period: 'This Week', actual: 595, target: 560, status: 'ahead' },
    { period: 'This Month', actual: 2565, target: 2400, status: 'ahead' },
    { period: 'This Year', actual: 31207, target: 29200, status: 'ahead' },
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
            Performance Trends
          </Text>
          <Text size="sm" c="dimmed">
            Savings vs targets across time periods
          </Text>
        </div>

        {/* Trend Comparison */}
        <SimpleGrid cols={2} spacing="lg">
          {trends.map((trend) => (
            <Paper
              key={trend.period}
              p="lg"
              style={{
                background: '#0f1012',
                border: '1px solid #2C2E33',
              }}
            >
              <Stack gap="sm">
                <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
                  {trend.period}
                </Text>
                <Group justify="space-between" align="flex-end">
                  <div>
                    <Text size="2rem" fw={700} c="white" lh={1}>
                      ${trend.actual.toLocaleString()}
                    </Text>
                    <Text size="xs" c="dimmed" mt={4}>
                      Target: ${trend.target.toLocaleString()}
                    </Text>
                  </div>
                  <Text size="lg" fw={700} c="#2F9E44">
                    +{Math.round((trend.actual / trend.target - 1) * 100)}%
                  </Text>
                </Group>
              </Stack>
            </Paper>
          ))}
        </SimpleGrid>

        <Divider color="#2C2E33" />

        {/* Key Insights */}
        <Stack gap="md">
          <Text size="sm" fw={600} c="white">
            Key Insights
          </Text>
          
          <Paper p="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
            <Text size="sm" c="white" mb={4}>
              <strong>Exceeding targets by 7% on average</strong>
            </Text>
            <Text size="xs" c="dimmed">
              Your building is performing better than projected across all time periods. 
              Current trajectory suggests $37,500 in annual savings, 28% above target.
            </Text>
          </Paper>

          <Paper p="md" style={{ background: '#0f1012', border: '1px solid #2C2E33' }}>
            <Text size="sm" c="white" mb={4}>
              <strong>Peak optimization window: 2-4 PM daily</strong>
            </Text>
            <Text size="xs" c="dimmed">
              AI has identified consistent opportunities during afternoon hours when solar 
              generation peaks and grid prices are lowest. Additional 8% savings possible.
            </Text>
          </Paper>
        </Stack>
      </Stack>
    </Paper>
  );
}
