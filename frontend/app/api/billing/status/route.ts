import { NextRequest, NextResponse } from 'next/server';
import { internal } from '../../../../convex/_generated/api';
import { ConvexHttpClient } from 'convex/browser';

const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export async function GET(req: NextRequest) {
  const authId = req.headers.get('x-auth-id') ?? '';
  const data = await convex.query(internal.billing.getUserStatus, { userId: authId });
  return NextResponse.json(data);
} 