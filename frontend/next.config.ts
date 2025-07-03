import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
      {
        source: '/users/:path*',
        destination: 'http://localhost:8000/users/:path*',
      },
    ];
  },
};

// Only check for Convex URL during build, not during linting
if (process.env.NODE_ENV === 'production' && !process.env.NEXT_PUBLIC_CONVEX_URL) {
  throw new Error('NEXT_PUBLIC_CONVEX_URL is missing');
}

export default nextConfig;
