'use client';

import { useAuth } from '@/lib/auth';

export default function AvatarMenu() {
  const { user, logout } = useAuth();
  
  const email = user?.email || '';
  const initials = email.split('@')[0].slice(0, 2).toUpperCase();

  return (
    <div data-testid="avatar-menu" className="flex items-center gap-4">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-medium">
          {initials}
        </div>
        <span className="text-sm text-gray-700">{email}</span>
      </div>
      <button
        onClick={() => logout()}
        className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-md transition-colors"
      >
        Sign out
      </button>
    </div>
  );
} 