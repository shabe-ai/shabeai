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
    const pipelineLink = await screen.findByRole('link', { name: /pipeline/i });
    expect(pipelineLink).toBeInTheDocument();
    expect(pipelineLink).toHaveAttribute('href', '/dashboard/pipeline');
    expect(screen.getByRole('link', { name: /tasks/i })).toHaveAttribute('href', '/dashboard/tasks');
    expect(screen.getByRole('link', { name: /chat/i })).toHaveAttribute('href', '/dashboard/chat');
    expect(screen.getByRole('link', { name: /settings/i })).toHaveAttribute('href', '/dashboard/settings');
  });
}); 