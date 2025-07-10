import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';
import { internal } from '@/convex/_generated/api';
import { ConvexHttpClient } from 'convex/browser';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-06-30.basil',
});
const convex = new ConvexHttpClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export async function POST(req: NextRequest) {
  const sig = req.headers.get('stripe-signature')!;
  const body = await req.text();

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!,
    );
  } catch (err) {
    return new NextResponse(`Webhook Error: ${err}`, { status: 400 });
  }

  if (
    event.type === 'customer.subscription.created' ||
    event.type === 'customer.subscription.updated'
  ) {
    const sub = event.data.object as Stripe.Subscription;
    await convex.mutation(internal.billing.upsertSubscription, {
      customerId: sub.customer as string,
      subId: sub.id,
      status: sub.status,
      trialEndsAt: (sub.trial_end ?? 0) * 1000,
    });
  }
  return NextResponse.json({ received: true });
} 