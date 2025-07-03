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
}); 