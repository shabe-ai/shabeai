import { middleware } from '../middleware';
import { NextRequest } from 'next/server';
import { vi, test, expect } from 'vitest';

test('redirects when trial expired', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      status: 'past_due',
      trialEndsAt: Date.now() - 1000,
    }),
  }) as unknown as typeof fetch);

  const req = new NextRequest(new URL('http://localhost/dashboard'));
  const res = await middleware(req);
  expect(res?.status).toBe(307);
}); 