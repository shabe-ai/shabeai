'use client';
import { useState } from 'react';
import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';

export default function CompanyTypeahead({ onSelect }: { onSelect: (id: string) => void }) {
  const [input, setInput] = useState('');
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const { data } = useQuery(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (api as any)['companies/queries'].searchCompanies,
    { q: input }
  );

  return (
    <div className="relative w-full">
      <input
        className="input input-bordered w-full"
        placeholder="Company…"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      {input && data?.length ? (
        <ul className="absolute z-10 w-full bg-white border rounded mt-1 shadow">
          {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
          {data.map((c: any) => (
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
      ) : null}
    </div>
  );
} 