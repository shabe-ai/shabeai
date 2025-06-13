export function Card({ className = "", children }: { className?: string; children: React.ReactNode }) {
  return <div className={`glass-card ${className}`}>{children}</div>;
}

export function CardContent({ className = "", children }: { className?: string; children: React.ReactNode }) {
  return <div className={`p-6 ${className}`}>{children}</div>;
} 