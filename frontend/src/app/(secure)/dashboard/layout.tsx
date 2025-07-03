"use client";
import AppShell from "@/components/layout/AppShell";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AppShell>
      <header className="p-4">Hey User! 👋</header>
      {children}
    </AppShell>
  );
} 