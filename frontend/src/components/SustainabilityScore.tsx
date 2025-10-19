import { Paper, Text, Stack, RingProgress, Group, Progress, Skeleton } from '@mantine/core';
import { useEffect, useState } from 'react';

interface CategoryScore {
  name: string;
  score: number;
  color: string;
}

export function SustainabilityScore() {
  const [overallScore, setOverallScore] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [categories, setCategories] = useState<CategoryScore[]>([
    { name: 'Energy Efficiency', score: 0, color: '#2F9E44' },
    { name: 'Carbon Footprint', score: 0, color: '#2F9E44' },
    { name: 'Resource Optimization', score: 0, color: '#4CAF50' },
    { name: 'Waste Reduction', score: 0, color: '#2F9E44' },
  ]);
  const [performanceText, setPerformanceText] = useState('Loading...');
  const [performanceDesc, setPerformanceDesc] = useState('Calculating sustainability metrics...');
  const [recommendations, setRecommendations] = useState<string[]>([]);
  
  useEffect(() => {
    const fetchScore = async () => {
      try {
        const response = await fetch('/api/invocations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            prompt: 'Calculate current sustainability score with category breakdowns' 
          }),
        });
        
        const json = await response.json();
        
        if (json.status === 'success' && json.data) {
          if (json.data.sustainability_score) {
            const score = json.data.sustainability_score;
            setOverallScore(score);
            setIsLoading(false);
            
            // Set performance text based on score
            if (score >= 80) {
              setPerformanceText('Excellent Performance');
              setPerformanceDesc('Your infrastructure exceeds AWS sustainability best practices');
            } else if (score >= 60) {
              setPerformanceText('Good Performance');
              setPerformanceDesc('Meeting most sustainability targets with room for improvement');
            } else if (score >= 40) {
              setPerformanceText('Needs Improvement');
              setPerformanceDesc('Several opportunities to enhance sustainability performance');
            } else {
              setPerformanceText('Action Required');
              setPerformanceDesc('Significant improvements needed to meet sustainability goals');
            }
          }
          
          // Extract recommendations from structured data or use defaults
          if (json.data?.recommendations && Array.isArray(json.data.recommendations)) {
            const recs = json.data.recommendations.map((rec: any) => 
              `${rec.action} → ${rec.impact}`
            );
            setRecommendations(recs);
          } else if (json.data?.sustainability_score) {
            // Generate recommendations based on score
            const score = json.data.sustainability_score;
            const defaultRecs = [];
            if (score < 70) {
              defaultRecs.push('Shift workloads to high renewable energy periods');
              defaultRecs.push('Optimize HVAC settings during peak demand');
              defaultRecs.push('Schedule cloud computing during low-carbon windows');
            } else {
              defaultRecs.push('Maintain current optimization strategies');
              defaultRecs.push('Monitor for renewable energy opportunities');
              defaultRecs.push('Continue efficient resource utilization');
            }
            setRecommendations(defaultRecs);
          }
          
          // Parse categories from response text
          const energyMatch = text.match(/energy.*?(\d+\.?\d*)/i);
          const carbonMatch = text.match(/carbon.*?(\d+\.?\d*)/i);
          const resourceMatch = text.match(/resource.*?(\d+\.?\d*)/i);
          const wasteMatch = text.match(/waste.*?(\d+\.?\d*)/i);
          
          if (energyMatch || carbonMatch || resourceMatch || wasteMatch) {
            setCategories([
              { name: 'Energy Efficiency', score: energyMatch ? parseFloat(energyMatch[1]) : 94, color: '#2F9E44' },
              { name: 'Carbon Footprint', score: carbonMatch ? parseFloat(carbonMatch[1]) : 88, color: '#2F9E44' },
              { name: 'Resource Optimization', score: resourceMatch ? parseFloat(resourceMatch[1]) : 82, color: '#4CAF50' },
              { name: 'Waste Reduction', score: wasteMatch ? parseFloat(wasteMatch[1]) : 85, color: '#2F9E44' },
            ]);
          }
        }
      } catch (error) {
        console.error('Failed to fetch sustainability score:', error);
        setIsLoading(false);
      }
    };
    
    fetchScore();
    const interval = setInterval(fetchScore, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 90) return '#2F9E44';
    if (score >= 75) return '#4CAF50';
    return '#FFA500';
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
      {isLoading ? (
        <Stack gap="xl">
          <div>
            <Skeleton height={24} width={200} mb={8} />
            <Skeleton height={16} width={250} />
          </div>
          <Group justify="center">
            <Skeleton height={180} width={180} circle />
          </Group>
          <Skeleton height={100} />
          <Stack gap="md">
            <Skeleton height={16} width={150} />
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} height={40} />
            ))}
          </Stack>
        </Stack>
      ) : (
        <Stack gap="xl">
          <div>
            <Text size="lg" fw={600} c="white" mb={4}>
              Sustainability Score
            </Text>
            <Text size="sm" c="dimmed">
              AWS Well-Architected Framework
            </Text>
          </div>

          {/* Overall Score */}
          <Group justify="center">
            <RingProgress
              size={180}
              thickness={16}
              sections={[{ value: overallScore, color: getScoreColor(overallScore) }]}
              label={
                <Stack gap={0} align="center">
                  <Text size="3rem" fw={700} c="white" lh={1}>
                    {overallScore}
                  </Text>
                  <Text size="xs" c="dimmed" tt="uppercase">
                    out of 100
                  </Text>
                </Stack>
              }
            />
          </Group>

          <Paper p="md" style={{ background: 'rgba(47, 158, 68, 0.1)', border: '1px solid rgba(47, 158, 68, 0.3)' }}>
            <Text size="sm" fw={600} c="#2F9E44" mb={4}>
              {performanceText}
            </Text>
            <Text size="xs" c="dimmed">
              {performanceDesc}
            </Text>
          </Paper>

        {/* Category Breakdown */}
        <Stack gap="md">
          <Text size="sm" fw={600} c="white">
            Category Breakdown
          </Text>
          {categories.map((category) => (
            <Stack key={category.name} gap={4}>
              <Group justify="space-between">
                <Text size="xs" c="dimmed">
                  {category.name}
                </Text>
                <Text size="xs" fw={600} c="white">
                  {category.score}/100
                </Text>
              </Group>
              <Progress value={category.score} color="green" size="sm" />
            </Stack>
          ))}
        </Stack>

        {/* Top Recommendations */}
        <Paper p="md" style={{ background: '#0f1012', border: '1px solid #2C2E33' }}>
          <Text size="sm" fw={600} c="white" mb="xs">
            Top Recommendations
          </Text>
          <Stack gap="xs">
            {recommendations.slice(0, 3).map((rec, i) => (
              <Text key={i} size="xs" c="dimmed">
                • {rec}
              </Text>
            ))}
          </Stack>
        </Paper>
      </Stack>
      )}
    </Paper>
  );
}
