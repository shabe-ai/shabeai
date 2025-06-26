import { render, screen } from '@testing-library/react';
import LeadsPage from '../app/(secure)/leads/page';
import { vi } from 'vitest';

vi.mock('../hooks/useLeads', () => ({
  useLeads: () => ({
    data: [
      {
        id: '1',
        email: 'test@example.com',
        firstName: 'John',
        lastName: 'Doe',
        companyId: 'c1',
        phone: '+1234567890',
        createdAt: '2024-01-01T00:00:00Z',
        linkedinUrl: null,
        company: { name: 'TestCo' },
      },
    ],
    isLoading: false,
  }),
}));

describe('LeadsPage', () => {
  it('renders a table of leads', () => {
    render(<LeadsPage />);
    expect(screen.getByText('Leads')).toBeInTheDocument();
    expect(screen.getByText('test@example.com')).toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('TestCo')).toBeInTheDocument();
  });
}); 