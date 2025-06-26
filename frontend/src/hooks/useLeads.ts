import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Lead, LeadCreate } from '@/api/generated';
import { api } from '@/lib/api';

export const useLeads = () =>
  useQuery({
    queryKey: ['leads'],
    queryFn: () => api.get<Lead[]>('/leads/').then(r => r.data),
  });

export const useCreateLead = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: LeadCreate) => api.post<Lead>('/leads/', payload).then(r => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['leads'] }),
  });
}; 