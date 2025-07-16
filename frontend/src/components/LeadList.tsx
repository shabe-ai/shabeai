'use client';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';
import LeadStatusPill from './LeadStatusPill';
import { useState } from 'react';

type SortKey = 'createdAt' | 'status' | 'name';

export default function LeadList() {
  const [sortKey, setSortKey] = useState<SortKey>('createdAt');
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const leads = useQuery((api as any)['leads/queries'].listByUser, { userId: 'demo-user' }) ?? [];

  const sorted = [...leads].sort((a, b) => {
    if (sortKey === 'createdAt') return b.createdAt - a.createdAt;
    if (sortKey === 'status') return a.status.localeCompare(b.status);
    return a.name.localeCompare(b.name);
  });

  return (
    <div>
      <div className="flex gap-2 mb-2">
        <label>Sort by:</label>
        <select
          className="select select-bordered select-sm"
          value={sortKey}
          onChange={(e) => setSortKey(e.target.value as SortKey)}
        >
          <option value="createdAt">Newest</option>
          <option value="status">Status</option>
          <option value="name">Name</option>
        </select>
      </div>
      <table className="table w-full">
        <thead>
          <tr>
            <th>Name</th>
            <th>Company</th>
            <th>Status</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((lead) => (
            <tr key={lead._id}>
              <td>{lead.name}</td>
              <td>{lead.companyId ?? '—'}</td>
              <td><LeadStatusPill status={lead.status} /></td>
              <td>{new Date(lead.createdAt).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 