import { Paper, Text, Stack, Progress, Divider, Group } from '@mantine/core';

export function ROIAnalysis() {
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
            Financial Impact
          </Text>
          <Text size="sm" c="dimmed">
            Return on investment analysis
          </Text>
        </div>

        {/* Main ROI */}
        <Stack gap="xs">
          <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
            3-Year ROI
          </Text>
          <Text size="3rem" fw={700} c="#2F9E44" lh={1}>
            640%
          </Text>
          <Text size="sm" c="dimmed">
            $153,900 total savings from $12,000 investment
          </Text>
        </Stack>

        <Divider color="#2C2E33" />

        {/* Payback Progress */}
        <Stack gap="md">
          <div>
            <Text size="sm" fw={600} c="white" mb="xs">
              Investment Recovery
            </Text>
            <Text size="xs" c="dimmed" mb="md">
              $9,360 recovered of $12,000 initial investment
            </Text>
          </div>
          <Progress value={78} color="green" size="xl" />
          <Text size="xs" c="dimmed">
            78% complete • Full payback in 1.1 months
          </Text>
        </Stack>

        <Divider color="#2C2E33" />

        {/* Monthly Breakdown */}
        <Stack gap="md">
          <Text size="sm" fw={600} c="white">
            Monthly Savings: $2,565
          </Text>
          
          <Stack gap="sm">
            <div>
              <Group justify="space-between" mb={4}>
                <Text size="xs" c="dimmed">Energy cost reduction</Text>
                <Text size="xs" fw={600} c="white">$1,850</Text>
              </Group>
              <Progress value={72} color="green" size="sm" />
            </div>

            <div>
              <Group justify="space-between" mb={4}>
                <Text size="xs" c="dimmed">Peak demand savings</Text>
                <Text size="xs" fw={600} c="white">$450</Text>
              </Group>
              <Progress value={18} color="green" size="sm" />
            </div>

            <div>
              <Group justify="space-between" mb={4}>
                <Text size="xs" c="dimmed">Carbon credit value</Text>
                <Text size="xs" fw={600} c="white">$265</Text>
              </Group>
              <Progress value={10} color="green" size="sm" />
            </div>
          </Stack>
        </Stack>

        <Paper p="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
          <Text size="xs" c="dimmed" mb={4}>
            5-Year Net Profit
          </Text>
          <Text size="xl" fw={700} c="#2F9E44">
            $141,900
          </Text>
        </Paper>
      </Stack>
    </Paper>
  );
}
