import { NextRequest, NextResponse } from 'next/server';

const PUBLIC = ['/billing', '/api/stripe/webhook', '/_next', '/favicon.ico'];

export async function middleware(req: NextRequest) {
  if (PUBLIC.some((p) => req.nextUrl.pathname.startsWith(p))) {
    return NextResponse.next();
  }

  // Pass session/user info via header; here we stub as 'demo-user'
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || req.nextUrl.origin;
  const res = await fetch(`${baseUrl}/api/billing/status`, {
    headers: { 'x-auth-id': 'demo-user' },
  });

  if (!res.ok) return NextResponse.next();

  const { status, trialEndsAt } = (await res.json()) as {
    status: string;
    trialEndsAt: number;
  };

  if (status !== 'active' && Date.now() > trialEndsAt) {
    const url = req.nextUrl.clone();
    url.pathname = '/billing';
    return NextResponse.redirect(url);
  }
  return NextResponse.next();
}

export const config = { matcher: ['/(.*)'] }; 