import { query } from '../_generated/server';
import { v } from 'convex/values';

export const listByUser = query({
  args: { userId: v.string() },
  handler: async (ctx, { userId }) => {
    return ctx.db
      .query('leads')
      .withIndex('by_owner', (q) => q.eq('ownerId', userId))
      .order('desc')
      .take(100);             // cap for now
  },
}); 