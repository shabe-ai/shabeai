import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const useCurrentUser = () =>
  useQuery({
    queryKey: ["currentUser"],
    queryFn: api.me,
    retry: false,
    staleTime: 5 * 60_000,
  }); 