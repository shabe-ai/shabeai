'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryStreamedHydration } from '@tanstack/react-query-next-experimental';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ReactNode, useState } from 'react';

interface User {
  id: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

interface ReactQueryProviderProps {
  children: ReactNode;
  initialData?: User | null;
}

export default function ReactQueryProvider({ children, initialData }: ReactQueryProviderProps) {
  // 1 client per browser tab — keep it in state so it's not re-created on
  // every re-render during development (hot-reload)
  const [client] = useState(() => {
    const queryClient = new QueryClient();
    
    // Pre-populate with initial data if available
    if (initialData) {
      queryClient.setQueryData(['me'], initialData);
    }
    
    return queryClient;
  });

  return (
    <QueryClientProvider client={client}>
      <ReactQueryStreamedHydration>{children}</ReactQueryStreamedHydration>
      {process.env.NODE_ENV === 'development' && <ReactQueryDevtools />}
    </QueryClientProvider>
  );
} 