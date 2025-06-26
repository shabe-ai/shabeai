'use client';
import { useState } from 'react';
import Link from 'next/link';
import { Sheet, SheetTrigger, SheetContent } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/lib/auth';

export default function AppShell({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const { logout } = useAuth();

  const nav = (
    <nav className="flex flex-col gap-2 p-4">
      {['home', 'pipeline', 'tasks', 'chat', 'settings'].map(p => (
        <Link key={p} href={`/dashboard/${p}`}
              className="rounded-lg px-3 py-2 text-sm font-medium hover:bg-muted">
          {p.charAt(0).toUpperCase() + p.slice(1)}
        </Link>
      ))}
      <Link href="/secure/leads"
            className="rounded-lg px-3 py-2 text-sm font-medium hover:bg-muted">
        Leads
      </Link>
    </nav>
  );

  return (
    <div className="flex h-screen">
      <aside className="hidden w-56 flex-shrink-0 border-r bg-background md:block">
        {nav}
      </aside>

      <Sheet open={open} onOpenChange={setOpen}>
        <SheetTrigger className="p-2 md:hidden">☰</SheetTrigger>
        <SheetContent side="left">{nav}</SheetContent>
      </Sheet>

      <main className="flex flex-1 flex-col">
        {/* top-bar */}
        <header className="flex items-center justify-between border-b px-4 py-2">
          <h1 className="text-lg font-semibold">Shabe AI CRM</h1>
          <Button variant="ghost" onClick={() => logout()}>Sign out</Button>
        </header>

        <section className="flex-1 overflow-auto p-4">{children}</section>
      </main>
    </div>
  );
} 