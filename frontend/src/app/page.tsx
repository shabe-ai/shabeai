'use client';
import { QueryClient, QueryClientProvider } from 'react-query';
import { useState, useRef, useEffect } from 'react';
import { useChat } from '@/hooks/useChat';

export default function ChatHome() {
  const [client] = useState(() => new QueryClient());
  const [messages, setMessages] = useState([
    { role: 'assist', text: 'Welcome to Shabe AI! Ask me anything…' },
  ]);
  const [input, setInput] = useState('');
  const listRef = useRef<HTMLDivElement>(null);

  // auto-scroll
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  // React Query mutation
  const { mutate: sendChat, status } = useChat((reply) => {
    setMessages((prev) => [...prev, { role: 'assist', text: reply }]);
  });

  const send = () => {
    const text = input.trim();
    if (!text) return;
    // add user message
    setMessages((prev) => [...prev, { role: 'user', text }]);
    setInput('');
    // call backend
    sendChat(text);
  };

  return (
    <QueryClientProvider client={client}>
      <div id="chat-root">
        <header>
          <img src="/logo-mark.png" alt="Shabe logo" />
          <span className="title">shabe ai</span>
        </header>

        <div ref={listRef} className="message-list">
          {messages.map((m, i) => (
            <div
              key={i}
              className={m.role === 'user' ? 'user-message message' : 'assistant-message message'}
            >
              <div className="message-content">{m.text}</div>
            </div>
          ))}
          {status === 'pending' && (
            <div className="assistant-message message">
              <div className="message-content">⏳ Shabe is thinking…</div>
            </div>
          )}
        </div>

        <div className="chat-input-wrap">
          <input
            className="chat-input"
            placeholder="Type your message…"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && send()}
          />
          <button className="send-button" onClick={send}>
            <svg stroke="currentColor" fill="none" viewBox="0 0 24 24">
              <path d="M5 12h14M13 5l7 7-7 7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </QueryClientProvider>
  );
}