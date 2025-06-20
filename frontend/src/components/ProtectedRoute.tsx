'use client';

import { useAuth } from '@/lib/auth';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isAuthenticated, user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (user === undefined) {
      // Still loading, don't redirect yet
      return;
    }
    
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, user, router]);

  if (user === undefined) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading…</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  return <>{children}</>;
} 