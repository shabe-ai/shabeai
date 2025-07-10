"use client";
import type { ReactNode } from 'react';

export default function BillingLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col items-center">
      <header className="w-full border-b p-4 text-center font-semibold">
        Billing
      </header>
      <main className="flex-1 w-full max-w-xl p-6">{children}</main>
    </div>
  );
} 