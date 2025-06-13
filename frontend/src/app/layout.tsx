import './globals.css';
import type { Metadata } from 'next';
import { Bricolage_Grotesque, Figtree } from "next/font/google";
import ReactQueryProvider from '@/components/ReactQueryProvider';

const headingFont = Bricolage_Grotesque({ subsets: ["latin"], weight:["700"]});
const bodyFont    = Figtree({ subsets: ["latin"], weight:["400"]});

export const metadata: Metadata = { title: 'Shabe AI CRM' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={bodyFont.className}>
      <head>
        <link
          href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700&family=Figtree:wght@400&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-halo">
        <ReactQueryProvider>
          {children}
        </ReactQueryProvider>
      </body>
    </html>
  );
} 