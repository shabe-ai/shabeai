"use client";
import type { ReactNode } from 'react';
import { ConvexClientProvider } from '../../src/lib/convex';
import { AppProviders } from '../../src/app/providers';

export default function BillingLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ConvexClientProvider>
          <AppProviders>{children}</AppProviders>
        </ConvexClientProvider>
      </body>
    </html>
  );
} 