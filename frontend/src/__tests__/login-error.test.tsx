import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from '@/components/LoginForm';

describe('LoginForm – error', () => {
  it('shows error when creds are wrong', async () => {
    const onSuccess = vi.fn();

    render(<LoginForm onSuccess={onSuccess} />);

    await userEvent.type(screen.getByPlaceholderText(/email/i), 'bad@example.com');
    await userEvent.type(screen.getByPlaceholderText(/password/i), 'wrongpass');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument();
    });
    
    // Verify no redirect occurred
    expect(onSuccess).not.toHaveBeenCalled();
  });
}); 