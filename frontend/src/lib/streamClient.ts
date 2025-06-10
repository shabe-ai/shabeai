export async function streamChat(prompt: string, history: Array<{ role: string; text: string }> = [], onToken: (chunk: string) => void) {
  const res = await fetch('http://localhost:8000/api/chat/stream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      message: prompt, 
      history: history.map(msg => ({
        role: msg.role,
        content: msg.text
      }))
    })
  });
  if (!res.ok) throw new Error(await res.text());

  const reader = res.body?.getReader();
  if (!reader) throw new Error('No reader available');
  
  const decoder = new TextDecoder();   // defaults to utf-8
  let done, value;
  
  while (true) {
    ({ done, value } = await reader.read());
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    onToken(chunk);   // push partial text to caller
  }
} 