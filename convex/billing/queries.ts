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