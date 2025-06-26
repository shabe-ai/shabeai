import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Task, TaskCreate } from '@/api/generated';
import { api } from '@/lib/api';

export const useTasks = () =>
  useQuery({
    queryKey: ['tasks'],
    queryFn: () => api.get<Task[]>('/tasks/').then(r => r.data),
  });

export const useCreateTask = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: TaskCreate) => api.post<Task>('/tasks/', payload).then(r => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['tasks'] }),
  });
}; 