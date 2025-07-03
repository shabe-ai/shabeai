'use client';

import { ConvexProvider, ConvexReactClient } from "convex/react";
import { useState } from "react";

export function ConvexClientProvider({ children }: { children: React.ReactNode }) {
  const [convex] = useState(() => {
    const url = process.env.NEXT_PUBLIC_CONVEX_URL;
    if (!url) {
      console.warn('NEXT_PUBLIC_CONVEX_URL not found, using fallback');
      return new ConvexReactClient('https://precious-eel-928.convex.cloud');
    }
    return new ConvexReactClient(url);
  });
  
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
} 