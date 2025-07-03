import type { NextConfig } from "next";

if (!process.env.NEXT_PUBLIC_CONVEX_URL) {
  throw new Error('NEXT_PUBLIC_CONVEX_URL is missing');
}

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

export default nextConfig;
