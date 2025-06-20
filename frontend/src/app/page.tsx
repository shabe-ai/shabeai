'use client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useRef, useEffect } from 'react';
import Image from 'next/image';
import { useChat } from '@/hooks/useChat';

function TypingDots() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const interval = setInterval(() => {
      setCount((prev) => (prev < 3 ? prev + 1 : 0));
    }, 350);
    return () => clearInterval(interval);
  }, []);
  return (
    <span className="typing-dots font-mono pl-3 pr-5">
      {'.'.repeat(count) + '\u00A0'.repeat(3 - count)}
    </span>
  );
}

export default function ChatHome() {
  const [client] = useState(() => new QueryClient());
  const [messages, setMessages] = useState([
    { text: 'Welcome to Shabe AI! Ask me anything…', isUser: false }
  ]);
  const [input, setInput] = useState('');
  const listRef = useRef<HTMLDivElement>(null);

  /* auto-scroll */
  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  /* create an empty assistant bubble when we start streaming */
  const { mutate: sendChat, status } = useChat(
    (partial: string) => setMessages(m => {
      const next = [...m];
      next[next.length - 1] = { text: partial, isUser: false };
      return next;
    }),
    (final: string) => setMessages(m => {
      const next = [...m];
      next[next.length - 1] = { text: final, isUser: false };
      return next;
    })
  );

  const send = () => {
    const text = input.trim();
    if (!text) return;
    setMessages(m => [
      ...m,
      { text, isUser: true },      // user bubble
      { text: '', isUser: false }  // placeholder assistant bubble
    ]);
    setInput('');
    sendChat(text);
  };

  return (
    <QueryClientProvider client={client}>
      {/* translucent card / glass effect */}
      <div id="chat-frame" className="mx-auto my-4 max-w-[720px] rounded-3xl bg-white/5 shadow-2xl shadow-black/10 ring-1 ring-white/20 backdrop-blur-lg flex flex-col h-[calc(100dvh-2rem)]">
        {/* inner column keeps current id for your existing styles */}
        <div id="chat-root" className="flex-1 flex flex-col">
          {/* header */}
          <header>
            <Image src="/logo-mark.png" alt="Shabe AI logo" width={32} height={32} />
            <span className="title">shabe ai</span>
          </header>

          {/* 1. message stream */}
          <div ref={listRef} className="message-list">
            {messages.map((m, i) => (
              <div key={i} className={`w-full flex ${m.isUser ? 'justify-end' : 'justify-start'} fade-in`}>
                <div className={m.isUser ? 'user-message' : 'assistant-message'}>
                  <div className="message-content">
                    {status === 'pending' && i === messages.length - 1 && !m.isUser
                      ? <TypingDots />       // show dots while streaming latest bubble
                      : m.text}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* 2. input row after the list */}
          <div className="chat-input-wrap">
            <input
              className="chat-input"
              placeholder="Type your message…"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && send()}
            />
            <button className="send-button" onClick={send}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-6 h-6">
                <path d="M3 20l18-8-18-8v7l13 1-13 1v7z" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}