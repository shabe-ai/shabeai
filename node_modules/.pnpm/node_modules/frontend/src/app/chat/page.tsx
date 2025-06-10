"use client";

import { useState, useRef, useEffect } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { streamChat } from "../../lib/streamClient";

type Message = {
  role: "user" | "assistant";
  text: string;
};

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const chatRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    const el = chatRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [messages]);

  async function handleSend() {
    if (!input.trim()) return;

    // Add the pending user message immediately
    const userEntry = { role: "user" as const, text: input };
    const aiEntry = { role: "assistant" as const, text: "" };
    setMessages(prev => [...prev, userEntry, aiEntry]);
    setInput("");

    try {
      // Stream the reply
      await streamChat(input, messages, (chunk: string) => {
        aiEntry.text += chunk;  // mutate reference
        setMessages(prev => [...prev]);  // trigger re-render
      });
    } catch (err: any) {
      console.error(err);
      aiEntry.text = "⚠️ Error talking to server";
      setMessages(prev => [...prev]);
    }
  }

  return (
    <main className="max-w-xl mx-auto flex flex-col gap-4 py-10">
      <div 
        ref={chatRef}
        className="max-h-[70vh] overflow-y-auto space-y-4"
      >
        {messages.map((msg, i) => (
          <Card 
            key={i} 
            className={`p-4 ${
              msg.role === "user" 
                ? "bg-blue-50 ml-auto" 
                : "bg-gray-50"
            }`}
          >
            <span className={msg.role === "user" ? "font-semibold" : ""}>
              {msg.text}
            </span>
          </Card>
        ))}
      </div>

      <Textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Say something…"
        className="min-h-[80px]"
      />
      <Button onClick={handleSend}>Send</Button>
    </main>
  );
} 