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

// MSW setup is assumed to be in setupTests.ts and mocks/server.ts

describe('Dashboard navigation', () => {
  it('shows nav links and Pipeline link points to correct URL', async () => {
    render(
      <QueryClientProvider client={new QueryClient()}>
        <SecureLayout>
          <DashboardLayout>
            <DashboardHome />
          </DashboardLayout>
        </SecureLayout>
      </QueryClientProvider>
    );

    // Wait for nav links to appear
    const pipelineLink = await screen.findByRole('link', { name: /Pipeline/i });
    expect(pipelineLink).toBeInTheDocument();
    expect(pipelineLink).toHaveAttribute('href', '/dashboard/pipeline');
    expect(screen.getByRole('link', { name: /Tasks/i })).toHaveAttribute('href', '/dashboard/tasks');
    expect(screen.getByRole('link', { name: /Chat/i })).toHaveAttribute('href', '/dashboard/chat');
    expect(screen.getByRole('link', { name: /Settings/i })).toHaveAttribute('href', '/dashboard/settings');
  });
}); 