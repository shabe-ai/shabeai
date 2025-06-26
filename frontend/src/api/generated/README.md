# Generated API Types

This directory contains TypeScript types generated from the backend OpenAPI specification.

## Workflow

1. **Generate OpenAPI JSON from backend:**
   ```bash
   pnpm --filter shabeai-backend openapi-json
   ```

2. **Copy OpenAPI JSON to frontend:**
   ```bash
   pnpm --filter frontend update-api
   ```

3. **Or run the complete workflow:**
   ```bash
   pnpm generate-openapi
   ```

## Manual Type Generation

Since the automatic code generation tool has path resolution issues, the types are currently maintained manually based on the OpenAPI schema.

### Available Types

- `Lead.ts` - Lead-related types (LeadCreate, LeadOut, Lead)
- `Company.ts` - Company-related types (CompanyCreate, CompanyOut, Company)
- `Deal.ts` - Deal-related types (DealCreate, DealOut, Deal)
- `Task.ts` - Task-related types (TaskCreate, TaskOut, Task)
- `index.ts` - Exports all types and common error types

### Usage

```typescript
import { LeadCreate, LeadOut, Company } from '@/api/generated';

// Use the types in your components
const newLead: LeadCreate = {
  email: 'test@example.com',
  firstName: 'John',
  lastName: 'Doe',
  phone: '+1234567890'
};
```

## Future Improvements

- Fix the OpenAPI code generation tool path resolution issues
- Set up automatic type generation in CI/CD pipeline
- Add runtime validation using Zod schemas 