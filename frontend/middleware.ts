import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(req: NextRequest) {
  const isLoggedIn = !!req.cookies.get('crm-auth');
  
  if (!isLoggedIn && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
  
  return NextResponse.next();
} 