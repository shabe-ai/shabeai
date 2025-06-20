'use client';

import { useAuth } from '@/lib/auth';
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
} from '@/components/ui/dropdown-menu';

export default function AvatarMenu() {
  const { user, logout } = useAuth();
  
  const email = user?.email || '';
  const initials = email.split('@')[0].slice(0, 2).toUpperCase();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-400"
          aria-label="Open user menu"
          data-testid="avatar-menu-trigger"
        >
          {initials}
        </button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>{email}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={logout} className="text-red-600 cursor-pointer">
          Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
} 