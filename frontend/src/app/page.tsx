'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useRef, useEffect } from 'react';
import { useChat } from '@/hooks/useChat';

export default function ChatHome() {
  const [client] = useState(() => new QueryClient());
  const [messages, setMessages] = useState([
    { text:'Welcome to Shabe AI! Ask me anything…', isUser: false },
  ]);
  const [input, setInput] = useState('');
  const listRef = useRef<HTMLDivElement>(null);

  /* auto-scroll */
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior:'smooth' });
  }, [messages]);

  /* backend call */
  const { mutate: sendChat, status } = useChat(reply =>
    setMessages(m => [...m, { text: reply, isUser: false }]),
  );

  const send = () => {
    const text = input.trim();
    if (!text) return;
    setMessages(m => [...m, { text, isUser: true }]);
    setInput('');
    sendChat(text);
  };

  return (
    <QueryClientProvider client={client}>
      <div id="chat-root">
        {/* header */}
        <header>
          <img src="/logo-mark.png" alt="Shabe AI logo" />
          <span className="title">shabe ai</span>
        </header>

        {/* messages */}
        <div ref={listRef} className="message-list">
          {messages.map((m,i) => (
            <div
              key={i}
              className={`w-full flex ${m.isUser ? 'justify-end' : 'justify-start'} fade-in`}
            >
              <div className={m.isUser ? 'user-message' : 'assistant-message'}>
                <div className="message-content">{m.text}</div>
              </div>
            </div>
          ))}
          {status === 'pending' && (
            <div className="w-full flex justify-start fade-in">
              <div className="assistant-message">
                <div className="message-content">⏳ Shabe is thinking…</div>
              </div>
            </div>
          )}
        </div>

        {/* input */}
        <div className="chat-input-wrap">
          <input
            className="chat-input"
            placeholder="Type your message…"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key==='Enter' && send()}
          />
          <button className="send-button" onClick={send}>
            <svg viewBox="0 0 24 24" stroke="currentColor" fill="none">
              <path d="M5 12h14M13 5l7 7-7 7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </QueryClientProvider>
  );
}