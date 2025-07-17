import { NextRequest, NextResponse } from 'next/server';
import { api } from '../../../../convex/_generated/api';
import { ConvexHttpClient } from 'convex/browser';

// Use local deployment URL if environment variable is not set
const convexUrl = process.env.NEXT_PUBLIC_CONVEX_URL || 'http://127.0.0.1:3210';
const convex = new ConvexHttpClient(convexUrl);

export async function GET(req: NextRequest) {
  try {
    const authId = req.headers.get('x-auth-id') ?? '';
    // public query lives under billing/queries
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const data = await convex.query((api as any)['billing/queries'].getUserStatus, {
      userId: authId,
    });
    return NextResponse.json(data);
  } catch (error) {
    console.error('Billing status error:', error);
    return NextResponse.json({ error: 'Billing service unavailable' }, { status: 503 });
  }
} 