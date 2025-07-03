'use client';

import { useMutation } from '@tanstack/react-query';

export default function RQTest() {
  const mutation = useMutation({
    mutationFn: async () => 'pong',
  });

  return (
    <button onClick={() => mutation.mutate()}>
      {mutation.status === 'success' ? mutation.data : 'Ping'}
    </button>
  );
} 