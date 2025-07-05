'use client';
import { useState } from 'react';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';

// Type for company data
interface Company {
  _id: string;
  name: string;
}

export default function CompanyTypeahead({ onSelect }: { onSelect: (companyId: string) => void }) {
  const [input, setInput] = useState('');
  const { data } = useQuery(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (api as any)["companies/queries"].searchCompanies,
    { q: input }
  );

  return (
    <div className="relative">
      <input
        className="input input-bordered w-full"
        placeholder="Company…"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      {input && data?.length > 0 && (
        <ul className="absolute z-10 mt-1 w-full bg-white border rounded shadow">
          {data.map((c: Company) => (
            <li
              key={c._id}
              className="px-3 py-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => {
                onSelect(c._id);
                setInput(c.name);
              }}
            >
              {c.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
} 