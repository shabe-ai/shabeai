/**
 * Root layout for all /dashboard routes.
 * Next.js app router requires every page tree to have a layout.tsx.
 * We keep it minimal for now; nav/sidebar can be added later.
 */

import type { ReactNode } from 'react';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Placeholder top-nav */}
      <header className="px-4 py-2 border-b">
        <h1 className="text-lg font-semibold">Shabe Dashboard</h1>
      </header>

      <main className="flex-1 p-4">{children}</main>
    </div>
  );
} 