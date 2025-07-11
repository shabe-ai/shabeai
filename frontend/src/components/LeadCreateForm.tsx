'use client';
import { useState } from 'react';
import { useMutation } from 'convex/react';
import { api } from '@/convex/_generated/api';
import CompanyTypeahead from './CompanyTypeahead';

export default function LeadCreateForm() {
  const [leadName, setLeadName] = useState('');
  const [companyId, setCompanyId] = useState<string | null>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const createLead = useMutation((api as any)['leads/mutations'].createLead);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!leadName) return;
    await createLead({ name: leadName, companyId });
    setLeadName('');
    setCompanyId(null);
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 w-full">
      <input
        className="input input-bordered flex-1"
        placeholder="Lead name…"
        value={leadName}
        onChange={(e) => setLeadName(e.target.value)}
      />
      <CompanyTypeahead onSelect={setCompanyId} />
      <button type="submit" className="btn btn-primary">Add</button>
    </form>
  );
} 