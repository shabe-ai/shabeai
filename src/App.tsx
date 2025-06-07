import { useEffect, useState } from 'react';
import { Box, Heading, Text, Spinner, Stack } from '@chakra-ui/react';
import axios from 'axios';

interface Game {
  id: number;
  home_team: {
    full_name: string;
  };
  visitor_team: {
    full_name: string;
  };
  home_team_score: number;
  visitor_team_score: number;
  status: string;
}

function App() {
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchGames = async () => {
      try {
        // Fetch the latest games (limit to 5 for demonstration)
        const response = await axios.get('https://www.balldontlie.io/api/v1/games?per_page=5');
        console.log('API Response:', response.data); // Debug log
        setGames(response.data.data);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching games:', err); // Debug log
        setError('Failed to fetch games');
        setLoading(false);
      }
    };

    fetchGames();
  }, []);

  if (loading) {
    return (
      <Box textAlign="center" mt={8}>
        <Spinner size="xl" borderWidth={4} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box textAlign="center" mt={8}>
        <Text color="red.500">{error}</Text>
      </Box>
    );
  }

  if (games.length === 0) {
    return (
      <Box textAlign="center" mt={8}>
        <Text>No games found. Please try again later.</Text>
      </Box>
    );
  }

  return (
    <Box p={8}>
      <Heading mb={6}>Latest NBA Scores</Heading>
      <Stack gap={4}>
        {games.map((game) => (
          <Box key={game.id} p={4} borderWidth={1} borderRadius="md">
            <Text>
              {game.home_team.full_name} {game.home_team_score} - {game.visitor_team_score} {game.visitor_team.full_name}
            </Text>
            <Text fontSize="sm" color="gray.500">
              Status: {game.status}
            </Text>
          </Box>
        ))}
      </Stack>
    </Box>
  );
}

export default App;
