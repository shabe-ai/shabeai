import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// Define handlers that correspond to your API endpoints
export const handlers = [
  http.get('http://localhost:8000/api/users/me', () => {
    return HttpResponse.json({
      id: 'test-user',
      email: 'test@example.com',
      full_name: 'Test User',
    });
  }),
  http.get('http://localhost:8000/users/me', () => {
    return HttpResponse.json({
      id: 'test-user',
      email: 'test@example.com',
      full_name: 'Test User',
    });
  }),
];

export const server = setupServer(...handlers); 