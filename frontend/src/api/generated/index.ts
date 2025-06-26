// Generated TypeScript types from OpenAPI schema

export * from './Lead';
export * from './Company';
export * from './Deal';
export * from './Task';

// Common types
export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
} 