'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginForm({ onSubmit, onSuccess }: { onSubmit?: (email: string, pw: string) => Promise<unknown>, onSuccess?: () => void }) {
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (onSubmit) {
        await onSubmit(email, pw);
      } else {
        // Simple demo login - in production you'd use Convex auth
        if (email === 'demo@example.com' && pw === 'password') {
          if (onSuccess) {
            onSuccess();
          } else {
            router.push('/dashboard');
          }
        } else {
          throw new Error('Invalid credentials');
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-4 max-w-sm mx-auto mt-16"
    >
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="input input-bordered"
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={pw}
        onChange={(e) => setPw(e.target.value)}
        className="input input-bordered"
        placeholder="Password"
        required
      />
      <button
        type="submit"
        disabled={isLoading}
        className="btn btn-primary"
      >
        {isLoading ? 'Signing in…' : 'Sign in'}
      </button>
      {error && (
        <p className="text-red-600 text-sm mt-2">
          {error}
        </p>
      )}
      <p className="text-sm text-gray-600 text-center mt-4">
        Demo: demo@example.com / password
      </p>
    </form>
  );
} 