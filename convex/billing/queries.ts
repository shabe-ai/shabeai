import { mutation } from '../_generated/server';
import { v } from 'convex/values';

export const upsertSubscription = mutation({
  args: {
    customerId: v.string(),
    subId: v.string(),
    status: v.string(),
    trialEndsAt: v.number(),
  },
  handler: async (ctx, args) => {
    const doc = await ctx.db
      .query('billing')
      .withIndex('by_user', (q) => q.eq('stripeCustomerId', args.customerId))
      .unique();
    if (doc) {
      await ctx.db.patch(doc._id, {
        stripeSubId: args.subId,
        status: args.status,
        trialEndsAt: args.trialEndsAt,
        updatedAt: Date.now(),
      });
    }
  },
});

// ── getUserStatus -------------------------------------------------
import { query } from '../_generated/server';

export const getUserStatus = query({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    const doc = await ctx.db
      .query('billing')
      .withIndex('by_user', (q) => q.eq('userId', userId))
      .unique();
    if (!doc) {
      // brand-new user: 14-day trial starts now
      return {
        status: 'trialing',
        trialEndsAt: Date.now() + 14 * 24 * 3600 * 1000,
      };
    }
    return { status: doc.status, trialEndsAt: doc.trialEndsAt };
  },
}); 