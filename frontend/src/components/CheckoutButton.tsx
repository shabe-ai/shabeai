'use client';
import { useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';

export default function CheckoutButton() {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const createSession = useMutation((api as any)['billing/actions'].createCheckoutSession);

  return (
    <button
      className="btn btn-primary"
      onClick={async () => {
        const url = await createSession({ priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_ID! });
        if (url) window.location.href = url;
      }}
    >
      Start free trial
    </button>
  );
} 