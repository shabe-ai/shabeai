'use client';

import { ReactNode, useState } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';

export default function Providers({ children }: { children: ReactNode }) {
  // one client – memoised on first render
  const [client] = useState(() => new QueryClient());

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
} 