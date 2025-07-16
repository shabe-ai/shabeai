import defineSchema from 'convex/schema';
import defineTable from 'convex/schema';
import { v } from 'convex/values';

export default defineSchema({
  users: defineTable({              // placeholder to satisfy foreign keys
    authId: v.string(),
    email: v.string(),
  }),

  /* ---------- Billing ---------- */
  billing: defineTable({
    userId: v.id('users'),
    stripeCustomerId: v.optional(v.string()),
    stripeSubId: v.optional(v.string()),
    status: v.union(
      v.literal('trialing'),
      v.literal('active'),
      v.literal('past_due'),
      v.literal('canceled')
    ),
    trialEndsAt: v.number(),
    updatedAt: v.number(),
  }).index('by_user', ['userId']),
}); 