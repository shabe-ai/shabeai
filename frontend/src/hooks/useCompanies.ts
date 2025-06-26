import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Company, CompanyCreate } from '@/api/generated';
import { api } from '@/lib/api';

export const useCompanies = () =>
  useQuery({
    queryKey: ['companies'],
    queryFn: () => api.get<Company[]>('/companies/').then(r => r.data),
  });

export const useCreateCompany = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CompanyCreate) => api.post<Company>('/companies/', payload).then(r => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['companies'] }),
  });
}; 