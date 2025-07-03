import ProtectedRoute from '@/components/ProtectedRoute';
import Providers from '../(providers)/react-query';

export default function SecureLayout({ children }: { children: React.ReactNode }) {
  return (
    <Providers>
      <ProtectedRoute>{children}</ProtectedRoute>
    </Providers>
  );
} 