import { action } from '../_generated/server';
import { v } from 'convex/values';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2025-06-30.basil' });

export const createCheckoutSession = action({
  args: { priceId: v.string() },
  handler: async (ctx, { priceId }) => {
    const user = await ctx.auth.getUserIdentity();
    if (!user) throw new Error('unauth');

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price: priceId, quantity: 1 }],
      customer_email: user.email,
      success_url: `${process.env.NEXT_PUBLIC_BASE_URL}/dashboard?checkout=success`,
      cancel_url: `${process.env.NEXT_PUBLIC_BASE_URL}/billing?canceled=1`,
      subscription_data: { trial_period_days: 14 },
      metadata: { authId: user.subject },
    });

    return session.url;
  },
}); 