'use client';

import { QueryClient, QueryClientProvider, useMutation } from 'react-query';

export default function RQTest() {
  const client = new QueryClient(); // new each render – OK for a test

  const mutation = useMutation({
    mutationFn: async () => 'pong',
  });

  return (
    <QueryClientProvider client={client}>
      <button onClick={() => mutation.mutate()}>
        {mutation.status === 'success' ? mutation.data : 'Ping'}
      </button>
    </QueryClientProvider>
  );
} 