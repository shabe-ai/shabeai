import Cookies from 'js-cookie';
import { QueryClient } from '@tanstack/react-query';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export async function login(email: string, password: string) {
  const body = new URLSearchParams({ username: email, password }).toString();
  await fetch(`${API}/auth/jwt/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
    credentials: 'include',            // let browser keep crm-auth cookie
  });
  // cookie arrives as Set-Cookie; js-cookie is only needed for reading later
  return Cookies.get('crm-auth');
}

export function logout() {
  Cookies.remove('crm-auth');
}

export const queryClient = new QueryClient();

// API functions for the hook
const loginApi = async (email: string, pw: string) => {
  const body = new URLSearchParams({ username: email, password: pw }).toString();
  await fetch(`${API}/auth/jwt/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
    credentials: 'include',
  });
};

const logoutApi = async () => {
  await fetch(`${API}/auth/jwt/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  Cookies.remove('crm-auth');
};

const getMe = async () => {
  const response = await fetch(`${API}/users/me`, {
    credentials: 'include',
  });
  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }
  return response.json();
};

export function useAuth() {
  const queryClient = useQueryClient();
  const router = useRouter();
  
  const { data: me } = useQuery({ 
    queryKey: ['me'], 
    queryFn: getMe, 
    retry: false 
  });
  
  const login = async (email: string, pw: string) => {
    await loginApi(email, pw);
    await queryClient.invalidateQueries({ queryKey: ['me'] });
  };
  
  const logout = async () => {
    await logoutApi();
    queryClient.clear();
    router.push('/login');
  };
  
  return { 
    user: me, 
    isAuthenticated: !!me, 
    login, 
    logout 
  };
} 