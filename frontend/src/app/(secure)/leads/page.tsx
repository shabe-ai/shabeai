'use client';

import { useLeads } from '@/hooks/useLeads';

// Define a type for Lead
type Lead = {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  company?: { name?: string };
};

export default function LeadsPage() {
  const { data, isLoading } = useLeads();
  if (isLoading) return <>Loading…</>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Leads</h1>
      <table className="w-full text-sm">
        <thead className="text-left border-b">
          <tr>
            <th>Email</th>
            <th>Name</th>
            <th>Company</th>
          </tr>
        </thead>
        <tbody>
          {(data as Lead[])?.map((l) => (
            <tr key={l.id} className="border-b">
              <td>{l.email}</td>
              <td>{l.firstName} {l.lastName}</td>
              <td>{l.company?.name ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 