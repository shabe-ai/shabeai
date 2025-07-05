import { useQuery } from 'convex/react';
import { api } from '@/convex/_generated/api';

// Convex codegen doesn't expose string-keyed modules as typed props.
// Cast to any for now; revisit when Convex fixes the limitation.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const { data } = useQuery(
  (api as any)['companies/queries'].searchCompanies,
  { q: input },
  { enabled: input.length > 1 },
); 