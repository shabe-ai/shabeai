import { query, mutation } from '../_generated/server';
import { v } from 'convex/values';

export const upsertSubscription = mutation({
  args: {
    customerId: v.string(),
    subId: v.string(),
    status: v.union(
      v.literal('trialing'),
      v.literal('active'),
      v.literal('past_due'),
      v.literal('canceled')
    ),
    trialEndsAt: v.number(),
  },
  handler: async (ctx, args) => {
    const doc = await ctx.db
      .query('billing')
      .filter((q) => q.eq(q.field('stripeCustomerId'), args.customerId))
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

export const getUserStatus = query({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    // For demo purposes, we'll return a default trial status
    // In a real app, you'd look up the user by auth ID and get their user ID
    // For now, we'll skip the database query and return a mock trial status
    return {
      status: 'trialing' as const,
      trialEndsAt: Date.now() + 14 * 24 * 3600 * 1000,
    };
  },
}); 