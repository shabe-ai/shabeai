import { query, mutation } from '../_generated/server';
import { v } from 'convex/values';

export const getOrCreate = mutation({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    const existing = await ctx.db
      .query('billing')
      .withIndex('userId', (q) => q.eq('userId', userId))
      .unique();
    if (existing) return existing;

    const now = Date.now();
    return ctx.db.insert('billing', {
      userId,
      status: 'trialing',
      trialEndsAt: now + 14 * 24 * 3600 * 1000,
      updatedAt: now,
    });
  },
}); 