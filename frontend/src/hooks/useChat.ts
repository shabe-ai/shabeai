import { useMutation } from '@tanstack/react-query';
import { http } from '@/lib/http';

export function useChat(onReply: (text: string) => void) {
  return useMutation({
    mutationFn: (message: string) =>
      http.post<{ reply: string }>('/chat', { message }),
    onSuccess: (res) => onReply(res.data.reply),
  });
} 