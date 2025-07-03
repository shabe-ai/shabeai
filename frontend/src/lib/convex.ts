'use client';

import { ConvexProvider, ConvexReactClient } from "convex/react";
import { useState } from "react";

export function ConvexClientProvider({ children }: { children: React.ReactNode }) {
  const [convex] = useState(() => new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!));
  
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
} 