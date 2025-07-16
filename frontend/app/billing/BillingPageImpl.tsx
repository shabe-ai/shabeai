"use client";
import CheckoutButton from '@/components/CheckoutButton';

export default function BillingPageImpl() {
  return (
    <main className="p-6 flex flex-col items-center gap-4">
      <h1 className="text-2xl font-semibold">Billing</h1>
      <p>Activate your subscription to continue using Shabe AI.</p>
      <CheckoutButton />
    </main>
  );
} 