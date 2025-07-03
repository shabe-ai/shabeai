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

export default nextConfig;
