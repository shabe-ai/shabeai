import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

interface CheckoutResponse {
  url: string;
}

export function useBilling() {
  const { data: subscription, isLoading } = useQuery({
    queryKey: ["billing", "subscription"],
    queryFn: () => api.get("/billing/subscription"),
    retry: false,
    staleTime: 5 * 60_000,
  });

  const { data: payments } = useQuery({
    queryKey: ["billing", "payments"],
    queryFn: () => api.get("/billing/payments"),
    retry: false,
    staleTime: 5 * 60_000,
  });

  const createCheckoutSession = useMutation({
    mutationFn: async (priceId: string): Promise<CheckoutResponse> => {
      const response = await api.post("/billing/checkout", { priceId });
      return response.data as CheckoutResponse;
    },
    onSuccess: (data: CheckoutResponse) => {
      if (data.url) {
        window.location.href = data.url;
      }
    },
  });

  const startCheckout = async (priceId: string) => {
    try {
      await createCheckoutSession.mutateAsync(priceId);
    } catch (error) {
      console.error("Failed to create checkout session:", error);
      throw error;
    }
  };

  return {
    startCheckout,
    subscription: subscription?.data,
    payments: payments?.data,
    isLoading,
    isCreatingCheckout: createCheckoutSession.isPending,
  };
} 