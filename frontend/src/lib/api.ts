import http from './http';

export const api = {
  async me() {
    const res = await http.get('/users/me');
    return res.data;
  },
  
  async get<T>(url: string) {
    const res = await http.get<T>(url);
    return res;
  },
  
  async post<T>(url: string, data?: unknown) {
    const res = await http.post<T>(url, data);
    return res;
  },
  
  async put<T>(url: string, data?: unknown) {
    const res = await http.put<T>(url, data);
    return res;
  },
  
  async delete<T>(url: string) {
    const res = await http.delete<T>(url);
    return res;
  },
}; 