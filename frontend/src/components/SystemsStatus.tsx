import { Paper, Text, Stack, Group, Progress } from '@mantine/core';

export function SystemsStatus() {
  const systems = [
    { name: 'HVAC', load: 65, savings: 15, status: 'Optimal' },
    { name: 'Lighting', load: 45, savings: 22, status: 'Optimal' },
    { name: 'Servers', load: 85, savings: 8, status: 'Active' },
    { name: 'Other Systems', load: 30, savings: 12, status: 'Optimal' },
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
            Building Systems
          </Text>
          <Text size="sm" c="dimmed">
            Real-time status and optimization
          </Text>
        </div>

        <Stack gap="lg">
          {systems.map((system) => (
            <Stack key={system.name} gap="xs">
              <Group justify="space-between">
                <Text size="sm" fw={600} c="white">
                  {system.name}
                </Text>
                <Text size="xs" c="dimmed">
                  {system.status}
                </Text>
              </Group>
              
              <Group justify="space-between" align="flex-end">
                <div style={{ flex: 1 }}>
                  <Text size="xs" c="dimmed" mb={4}>
                    Current Load
                  </Text>
                  <Progress value={system.load} color="gray" size="md" />
                </div>
                <Text size="sm" fw={600} c="#2F9E44" style={{ minWidth: 60, textAlign: 'right' }}>
                  -{system.savings}%
                </Text>
              </Group>
              
              <Text size="xs" c="dimmed">
                {system.load}% load • {system.savings}% energy reduction vs baseline
              </Text>
            </Stack>
          ))}
        </Stack>

        <Paper p="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
          <Group justify="space-between">
            <Text size="sm" fw={600} c="white">
              All Systems Optimal
            </Text>
            <div style={{ 
              width: 8, 
              height: 8, 
              borderRadius: '50%', 
              background: '#2F9E44',
              boxShadow: '0 0 8px #2F9E44'
            }} />
          </Group>
        </Paper>
      </Stack>
    </Paper>
  );
}
