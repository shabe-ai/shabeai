'use client';  
import { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from 'react-query';

const client = new QueryClient();

export default function Providers({ children }: { children: ReactNode }) {
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>;
} 