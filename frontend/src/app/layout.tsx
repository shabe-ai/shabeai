import './globals.css';
import { Metadata } from 'next';
import { Figtree } from 'next/font/google';
import { ConvexClientProvider } from '@/lib/convex';

const bodyFont = Figtree({ subsets:['latin'], weight:['400'] });

export const metadata: Metadata = { title: 'Shabe AI CRM' };

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={bodyFont.className}>
      <body className="min-h-screen">
        <ConvexClientProvider>
          {children}
        </ConvexClientProvider>
      </body>
    </html>
  );
} 