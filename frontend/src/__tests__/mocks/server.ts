import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// Define handlers that correspond to your API endpoints
export const handlers = [
  http.get('http://localhost:8000/users/me', () => {
    return HttpResponse.json({
      id: '1',
      email: 'test@example.com',
      is_active: true,
      is_superuser: false,
      is_verified: true,
    });
  }),
];

export const server = setupServer(...handlers); 