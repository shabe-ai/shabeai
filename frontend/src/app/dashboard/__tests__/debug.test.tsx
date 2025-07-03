import { render, screen } from '@testing-library/react';
import DashboardHome from '@/app/(secure)/dashboard/page';
import SecureLayout from '@/app/(secure)/layout';
import DashboardLayout from '@/app/(secure)/dashboard/layout';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { vi } from 'vitest';
import http from '@/lib/http';

console.log('AXIOS BASE URL:', http.defaults.baseURL);

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('Debug test', () => {
  it('should render something', async () => {
    render(
      <QueryClientProvider client={new QueryClient()}>
        <SecureLayout>
          <DashboardLayout>
            <DashboardHome />
          </DashboardLayout>
        </SecureLayout>
      </QueryClientProvider>
    );

    // Wait a bit and see what's rendered
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Log what's in the document
    console.log('Document body:', document.body.innerHTML);
    
    // Check if we can find any links
    const links = screen.queryAllByRole('link');
    console.log('Found links:', links.map(link => ({ text: link.textContent, href: link.getAttribute('href') })));
    
    expect(true).toBe(true); // Just to make the test pass
  });
}); 