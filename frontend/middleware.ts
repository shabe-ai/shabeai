import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const isLoggedIn = !!req.cookies.get('crm-auth');
  
  // Protect both /dashboard and /secure routes
  if (!isLoggedIn && (req.nextUrl.pathname.startsWith('/dashboard') || req.nextUrl.pathname.startsWith('/secure'))) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
  
  return NextResponse.next();
} 