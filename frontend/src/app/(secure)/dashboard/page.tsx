'use client';

import AvatarMenu from '@/components/AvatarMenu';

export default function DashboardPage() {
  return (
    <div>
      <div className="border-b border-gray-200 bg-white px-6 py-4">
        <div className="flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-900">Shabe AI CRM</h1>
          <AvatarMenu />
        </div>
      </div>
      <main className="p-10">
        <h2 className="text-2xl font-semibold mb-2">Welcome to your Dashboard</h2>
        <p>This is your Home base. Coming soon: pipeline, tasks, GPT chat…</p>
      </main>
    </div>
  );
} 