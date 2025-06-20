import './globals.css';
import { Metadata } from 'next';
import { Figtree } from 'next/font/google';
import ReactQueryProvider from '@/components/ReactQueryProvider';
import { cookies } from 'next/headers';

const bodyFont = Figtree({ subsets:['latin'], weight:['400'] });

export const metadata: Metadata = { title: 'Shabe AI CRM' };

async function getInitialData() {
  const cookieStore = await cookies();
  const authCookie = cookieStore.get('crm-auth');
  
  if (!authCookie) {
    return null;
  }

  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'}/users/me`, {
      headers: {
        Cookie: `crm-auth=${authCookie.value}`,
      },
    });

    if (response.ok) {
      const userData = await response.json();
      return userData;
    }
  } catch (error) {
    console.error('Failed to fetch initial user data:', error);
  }

  return null;
}

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const initialData = await getInitialData();

  return (
    <html lang="en" className={bodyFont.className}>
      <body className="min-h-screen">
        <ReactQueryProvider initialData={initialData}>
          {children}
        </ReactQueryProvider>
      </body>
    </html>
  );
} 