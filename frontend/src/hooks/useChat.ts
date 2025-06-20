import { useMutation } from '@tanstack/react-query';

/** remove all newlines */
const collapseAllLF = (str: string) => str.replace(/\n+/g, '');

/**
 * Returns:
 *   mutate(prompt)            – send a user prompt
 *   status === 'pending'      – true while we're streaming
 */
export function useChat(
  onChunk: (partial: string) => void,   // called on every chunk
  onDone:  (full:   string) => void     // called when the stream ends
) {
  return useMutation<void, Error, string>({
    async mutationFn(prompt) {
      const res = await fetch('/api/chat/stream', {          // ← keeps Next.js rewrite
        method : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body   : JSON.stringify({ message: prompt }),
      });

      // -- browser streaming plumbing
      const reader = res.body!
        .pipeThrough(new TextDecoderStream())
        .getReader();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) {
          onDone(collapseAllLF(buffer).trim());            // ← final clean-up
          break;
        }

        buffer += collapseAllLF(value);
        onChunk(buffer);                                      // live aggregate
      }
    }
  });
} 