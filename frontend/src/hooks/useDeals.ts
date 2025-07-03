import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Deal, DealCreate } from '@/api/generated';
import { api } from '@/lib/api';

export const useDeals = () =>
  useQuery({
    queryKey: ['deals'],
    queryFn: () => api.get<Deal[]>('/deals/').then(r => r.data),
  });

export const useCreateDeal = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: DealCreate) => api.post<Deal>('/deals/', payload).then(r => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['deals'] }),
  });
}; 