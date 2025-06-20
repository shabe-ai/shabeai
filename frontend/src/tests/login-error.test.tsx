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

describe('LoginForm – error', () => {
  it('shows error message on invalid credentials', async () => {
    const onSuccess = vi.fn();
    
    // Mock 401 error response
    vi.spyOn(global, 'fetch').mockRejectedValueOnce(
      new Error('Invalid credentials')
    );

    renderWithProviders(<LoginForm onSuccess={onSuccess} />);

    await userEvent.type(screen.getByPlaceholderText(/email/i), 'wrong@example.com');
    await userEvent.type(screen.getByPlaceholderText(/password/i), 'wrongpass');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
    
    // Verify no redirect occurred
    expect(onSuccess).not.toHaveBeenCalled();
  });
}); 