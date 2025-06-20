import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { http, HttpResponse } from 'msw';
import { server } from './mocks/server';
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
  it('shows error when creds are wrong', async () => {
    const onSuccess = vi.fn();
    
    server.use(
      http.post('http://localhost:8000/auth/jwt/login', () =>
        HttpResponse.json({ detail: 'LOGIN_BAD_CREDENTIALS' }, { status: 401 }),
      ),
    );

    renderWithProviders(<LoginForm onSuccess={onSuccess} />);

    await userEvent.type(screen.getByPlaceholderText(/email/i), 'bad@example.com');
    await userEvent.type(screen.getByPlaceholderText(/password/i), 'wrongpass');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText(/LOGIN_BAD_CREDENTIALS/i)).toBeInTheDocument();
    });
    
    // Verify no redirect occurred
    expect(onSuccess).not.toHaveBeenCalled();
  });
}); 