export interface TaskCreate {
  title: string;
  dueDate: string; // ISO date-time string
  isDone?: boolean;
  leadId?: string | null;
}

export interface TaskOut {
  title: string;
  dueDate: string; // ISO date-time string
  isDone?: boolean;
  leadId?: string | null;
  id: string;
}

export interface Task {
  id: string;
  title: string;
  dueDate: string; // ISO date-time string
  isDone: boolean;
  leadId?: string | null;
  createdAt: string;
} 