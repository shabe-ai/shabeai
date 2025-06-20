import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import LoginForm from '@/components/LoginForm';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

function renderWithProviders(component: React.ReactElement) {
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
}

describe('LoginForm – success', () => {
  it('calls onSuccess on valid login', async () => {
    const onSuccess = vi.fn();
    vi.spyOn(global, 'fetch').mockResolvedValueOnce(
      new Response(null, { status: 204 }),
    );

    renderWithProviders(<LoginForm onSuccess={onSuccess} />);

    await userEvent.type(screen.getByPlaceholderText(/email/i), 'demo@example.com');
    await userEvent.type(screen.getByPlaceholderText(/password/i), 'demodemo');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => expect(onSuccess).toHaveBeenCalled());
  });
}); 