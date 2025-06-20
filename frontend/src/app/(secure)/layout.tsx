import ProtectedRoute from '@/components/ProtectedRoute';

export default function SecureLayout({ children }: { children: React.ReactNode }) {
  return <ProtectedRoute>{children}</ProtectedRoute>;
} 