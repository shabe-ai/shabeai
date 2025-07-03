import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginForm from '@/components/LoginForm';

describe('LoginForm – success', () => {
  it('calls onSuccess on valid login', async () => {
    const onSuccess = vi.fn();

    render(<LoginForm onSuccess={onSuccess} />);

    await userEvent.type(screen.getByPlaceholderText(/email/i), 'demo@example.com');
    await userEvent.type(screen.getByPlaceholderText(/password/i), 'password');
    await userEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => expect(onSuccess).toHaveBeenCalled());
  });
}); 