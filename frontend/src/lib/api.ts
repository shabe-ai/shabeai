import axios from 'axios';
import { useQuery } from '@tanstack/react-query';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use((config) => {
  // TODO: Add authentication token when implemented
  // const token = getAuthToken();
  // if (token) {
  //   config.headers.Authorization = `Bearer ${token}`;
  // }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors (401, 403, 500, etc.)
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login';
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