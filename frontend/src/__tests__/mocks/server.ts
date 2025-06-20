import { setupServer } from 'msw/node';

// Define handlers that correspond to your API endpoints
export const handlers = [
  // Default handlers can go here
];

export const server = setupServer(...handlers); 