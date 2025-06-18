import axios from 'axios';
import { useQuery } from '@tanstack/react-query';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000',
  withCredentials: true, // ← include crm-auth cookie
});

// Global error interceptor for 401/403 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Clear auth cookie
      document.cookie = 'crm-auth=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      // Redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const login = (email: string, pw: string) => 
  api.post('/auth/jwt/login', `username=${email}&password=${pw}`, { 
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' } 
  });

export const currentUser = () => api.get('/users/me');

export const logout = () => api.post('/auth/jwt/logout');

export const useCurrentUser = () =>
  useQuery({ queryKey: ['me'], queryFn: currentUser, staleTime: 30 * 60 * 1000 }); 