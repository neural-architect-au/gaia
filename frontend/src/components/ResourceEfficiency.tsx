import { Paper, Text, Stack, Group, SimpleGrid, Progress, Badge } from '@mantine/core';

export function ResourceEfficiency() {
  const rightsizing = [
    {
      resource: 'prod-api-server',
      type: 'm5.2xlarge',
      utilization: 35,
      recommendation: 'm5.xlarge',
      savings: '$156/month',
      status: 'over-provisioned',
    },
    {
      resource: 'analytics-db',
      type: 'db.r5.4xlarge',
      utilization: 42,
      recommendation: 'db.r5.2xlarge',
      savings: '$312/month',
      status: 'over-provisioned',
    },
    {
      resource: 'ml-training',
      type: 'p3.2xlarge',
      utilization: 88,
      recommendation: 'Optimal',
      savings: '$0',
      status: 'optimal',
    },
  ];

  const gravitonComparison = {
    current: { type: 'x86 (m5.large)', cost: 192, performance: 100 },
    graviton: { type: 'Graviton (m6g.large)', cost: 154, performance: 105 },
    savings: 20,
    performanceGain: 5,
  };

  const idleResources = [
    { name: 'dev-test-instance', type: 'EC2', idle: '18 hours/day', waste: '$45/month' },
    { name: 'staging-db', type: 'RDS', idle: '20 hours/day', waste: '$89/month' },
    { name: 'old-snapshot-vol', type: 'EBS', idle: 'Unused', waste: '$12/month' },
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
            Resource Efficiency
          </Text>
          <Text size="sm" c="dimmed">
            Right-sizing and optimization opportunities
          </Text>
        </div>

        {/* Potential Savings */}
        <SimpleGrid cols={3} spacing="lg">
          <Stack gap={4}>
            <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
              Right-sizing Savings
            </Text>
            <Text size="2rem" fw={700} c="#2F9E44" lh={1}>
              $468
            </Text>
            <Text size="xs" c="dimmed">
              per month
            </Text>
          </Stack>

          <Stack gap={4}>
            <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
              Idle Resource Waste
            </Text>
            <Text size="2rem" fw={700} c="#FFA500" lh={1}>
              $146
            </Text>
            <Text size="xs" c="dimmed">
              per month
            </Text>
          </Stack>

          <Stack gap={4}>
            <Text size="xs" c="dimmed" tt="uppercase" fw={500}>
              Total Opportunity
            </Text>
            <Text size="2rem" fw={700} c="#2F9E44" lh={1}>
              $614
            </Text>
            <Text size="xs" c="dimmed">
              per month
            </Text>
          </Stack>
        </SimpleGrid>

        {/* Right-sizing Recommendations */}
        <div>
          <Text size="sm" fw={600} c="white" mb="md">
            Right-sizing Recommendations
          </Text>
          <Stack gap="md">
            {rightsizing.map((item) => (
              <Paper
                key={item.resource}
                p="md"
                style={{
                  background: '#0f1012',
                  border: '1px solid #2C2E33',
                }}
              >
                <Stack gap="sm">
                  <Group justify="space-between">
                    <Text size="sm" fw={600} c="white">
                      {item.resource}
                    </Text>
                    <Badge
                      size="sm"
                      color={item.status === 'optimal' ? 'green' : 'orange'}
                      variant="light"
                    >
                      {item.status}
                    </Badge>
                  </Group>

                  <Group justify="space-between">
                    <div style={{ flex: 1 }}>
                      <Text size="xs" c="dimmed" mb={4}>
                        Current: {item.type} • {item.utilization}% utilized
                      </Text>
                      <Progress value={item.utilization} color={item.utilization > 70 ? 'green' : 'orange'} size="sm" />
                    </div>
                  </Group>

                  {item.status !== 'optimal' && (
                    <Group justify="space-between">
                      <Text size="xs" c="dimmed">
                        Recommended: {item.recommendation}
                      </Text>
                      <Text size="xs" fw={600} c="#2F9E44">
                        Save {item.savings}
                      </Text>
                    </Group>
                  )}
                </Stack>
              </Paper>
            ))}
          </Stack>
        </div>

        {/* Graviton Migration */}
        <Paper p="lg" style={{ background: '#0f1012', border: '1px solid #2C2E33' }}>
          <Text size="sm" fw={600} c="white" mb="md">
            Graviton Migration Opportunity
          </Text>
          <Group grow>
            <Stack gap={4}>
              <Text size="xs" c="dimmed">Current (x86)</Text>
              <Text size="lg" fw={600} c="white">$192/mo</Text>
              <Text size="xs" c="dimmed">100% baseline</Text>
            </Stack>
            <Stack gap={4}>
              <Text size="xs" c="dimmed">Graviton</Text>
              <Text size="lg" fw={600} c="#2F9E44">$154/mo</Text>
              <Text size="xs" c="dimmed">105% performance</Text>
            </Stack>
          </Group>
          <Paper p="sm" mt="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
            <Text size="xs" c="white">
              💡 Migrate to Graviton for 20% cost savings + 5% better performance + 60% less energy
            </Text>
          </Paper>
        </Paper>

        {/* Idle Resources */}
        <div>
          <Text size="sm" fw={600} c="white" mb="md">
            Idle Resources Detected
          </Text>
          <Stack gap="sm">
            {idleResources.map((resource) => (
              <Group key={resource.name} justify="space-between" p="sm" style={{ background: '#0f1012', borderRadius: 4 }}>
                <div>
                  <Text size="sm" c="white">{resource.name}</Text>
                  <Text size="xs" c="dimmed">{resource.type} • {resource.idle}</Text>
                </div>
                <Text size="sm" fw={600} c="#FFA500">
                  {resource.waste}
                </Text>
              </Group>
            ))}
          </Stack>
        </div>

        <Paper p="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
          <Text size="sm" c="white" mb={4}>
            <strong>Auto-scaling enabled on 12 resources</strong>
          </Text>
          <Text size="xs" c="dimmed">
            Resources automatically scale down during off-peak hours, reducing waste by 35%
          </Text>
        </Paper>
      </Stack>
    </Paper>
  );
}
