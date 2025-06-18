'use client';

import { useMutation } from '@tanstack/react-query';
import { login } from '@/lib/auth';      // your helper
import { useState } from 'react';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');

  const m = useMutation({
    mutationFn: () => login(email, pw),
    onSuccess: () => window.location.replace('/dashboard'),
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        m.mutate();
      }}
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
        disabled={m.isPending}
        className="btn btn-primary"
      >
        {m.isPending ? 'Signing in…' : 'Sign in'}
      </button>
      {m.isError && (
        <p className="text-red-600 text-sm mt-2">
          {(m.error as Error).message}
        </p>
      )}
    </form>
  );
} 