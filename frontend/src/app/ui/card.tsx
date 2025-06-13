import React from "react";

export function Card({ className = "", children }: { className?: string; children: React.ReactNode }) {
  return (
    <div className={`rounded-2xl bg-white/5 backdrop-blur-md ring-1 ring-white/10 shadow-2xl shadow-yellow-500/10 border-0 ${className}`}>
      {children}
    </div>
  );
}

export function CardContent({ className = "", children }: { className?: string; children: React.ReactNode }) {
  return <div className={`p-3 flex flex-col gap-2 ${className}`}>{children}</div>;
} 