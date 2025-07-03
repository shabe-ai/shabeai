"use client";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { redirect } from "next/navigation";
import AppShell from "@/components/layout/AppShell";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { data, error, isLoading } = useCurrentUser();
  if (isLoading) return <p>Loading…</p>;
  if (error) return redirect("/login");
  return (
    <AppShell>
      <header className="p-4">Hey {data.full_name || data.email}! 👋</header>
      {children}
    </AppShell>
  );
} 