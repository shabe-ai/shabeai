'use client';
import dynamic from 'next/dynamic';

const LeadCreateForm = dynamic(() => import('@/components/LeadCreateForm'), {
  ssr: false,
});

export default function ChatPage() {
  return (
    <main className="p-6 max-w-xl mx-auto flex flex-col gap-6">
      <h1 className="text-2xl font-semibold">Chat ➜ Lead demo</h1>
      <LeadCreateForm />
      {/* TODO: render chat history / lead list */}
    </main>
  );
} 