// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/** Combines Tailwind classes & dedups variants */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
} 