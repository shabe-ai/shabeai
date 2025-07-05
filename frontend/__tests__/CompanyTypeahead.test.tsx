import { render, screen, fireEvent } from '@testing-library/react';
import CompanyTypeahead from '../src/components/CompanyTypeahead';
import { vi } from 'vitest';

// Stub convex/react so hooks don't look for ConvexProvider
vi.mock('convex/react', () => ({
  useQuery: (_fn: any, _args: any) => ({ data: [{ _id: 'c1', name: 'Acme' }] }),
}));

test('selects company', () => {
  const onSelect = vi.fn();
  render(<CompanyTypeahead onSelect={onSelect} />);
  fireEvent.change(screen.getByPlaceholderText(/company/i), { target: { value: 'Ac' } });
  fireEvent.click(screen.getByText('Acme'));
  expect(onSelect).toHaveBeenCalledWith('c1');
}); 