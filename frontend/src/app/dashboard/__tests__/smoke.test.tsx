import { render, screen } from '@testing-library/react';
import DashboardHome from '@/app/(secure)/dashboard/page';
import SecureLayout from '@/app/(secure)/layout';
import DashboardLayout from '@/app/(secure)/dashboard/layout';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode } from 'react';
import { vi } from 'vitest';

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

const renderWithProviders = (ui: React.ReactElement) => {
  const testQueryClient = createTestQueryClient();
  const { rerender, ...result } = render(
    <QueryClientProvider client={testQueryClient}>{ui}</QueryClientProvider>
  );
  return {
    ...result,
    rerender: (rerenderUi: React.ReactElement) =>
      rerender(
        <QueryClientProvider client={testQueryClient}>{rerenderUi}</QueryClientProvider>
      ),
  };
};

test('navbar appears for authenticated user', async () => {
  renderWithProviders(
    <SecureLayout>
      <DashboardLayout>
        <DashboardHome />
      </DashboardLayout>
    </SecureLayout>
  );
  expect(await screen.findByRole('link', { name: /pipeline/i })).toBeInTheDocument();
}); 