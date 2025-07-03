import { render, screen } from '@testing-library/react';
import DashboardHome from '@/app/(secure)/dashboard/page';
import SecureLayout from '@/app/(secure)/layout';
import DashboardLayout from '@/app/(secure)/dashboard/layout';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

vi.mock('@/hooks/useCurrentUser', () => ({
  useCurrentUser: () => ({
    data: {
      id: 'test-user',
      email: 'test@example.com',
      full_name: 'Test User',
    },
    error: null,
    isLoading: false,
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
  expect(await screen.findByRole('link', { name: /Pipeline/i })).toBeInTheDocument();
}); 