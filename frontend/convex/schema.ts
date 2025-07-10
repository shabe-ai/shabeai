import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    email: v.string(),
    fullName: v.optional(v.string()),
    isActive: v.boolean(),
    isSuperuser: v.boolean(),
    isVerified: v.boolean(),
    createdAt: v.number(),
    passwordHash: v.optional(v.string()),
    stripeCustomerId: v.optional(v.string()),
  }).index("by_email", ["email"]),

  companies: defineTable({
    name: v.string(),
    website: v.optional(v.string()),
    linkedinUrl: v.optional(v.string()),
    createdAt: v.number(),
  }).index("by_name", ["name"]),

  leads: defineTable({
    email: v.string(),
    firstName: v.string(),
    lastName: v.string(),
    phone: v.optional(v.string()),
    linkedinUrl: v.optional(v.string()),
    companyId: v.optional(v.id("companies")),
    createdAt: v.number(),
  })
    .index("by_email", ["email"])
    .index("by_company", ["companyId"]),

  deals: defineTable({
    title: v.string(),
    value: v.number(),
    stage: v.string(),
    companyId: v.id("companies"),
    createdAt: v.number(),
  }).index("by_company", ["companyId"]),

  tasks: defineTable({
    title: v.string(),
    dueDate: v.number(),
    isDone: v.boolean(),
    leadId: v.optional(v.id("leads")),
    createdAt: v.number(),
  }).index("by_lead", ["leadId"]),

  // Billing tables
  subscriptions: defineTable({
    userId: v.id("users"),
    stripeCustomerId: v.string(),
    stripeSubscriptionId: v.string(),
    status: v.string(), // active, canceled, past_due, etc.
    currentPeriodStart: v.number(),
    currentPeriodEnd: v.number(),
    cancelAtPeriodEnd: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_stripe_customer", ["stripeCustomerId"])
    .index("by_stripe_subscription", ["stripeSubscriptionId"]),

  payments: defineTable({
    userId: v.id("users"),
    stripePaymentIntentId: v.string(),
    stripeInvoiceId: v.optional(v.string()),
    amount: v.number(),
    currency: v.string(),
    status: v.string(), // succeeded, processing, failed, etc.
    createdAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_stripe_payment_intent", ["stripePaymentIntentId"]),

  // ---------- Billing ----------
  billing: defineTable({
    userId: v.string(),
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
  }).index("userId", ["userId"]),
}); 