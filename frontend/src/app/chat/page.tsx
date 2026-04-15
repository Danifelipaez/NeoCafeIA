'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { Message as MessageType, AIProvider } from '@/types';
import { MessageBubble } from '@/components/MessageBubble';
import { ChatInput } from '@/components/ChatInput';
import { ProviderSelector } from '@/components/ProviderSelector';
import { SuggestionChips } from '@/components/SuggestionChips';

const SUGGESTIONS = [
  '¿Qué bebidas tienen?',
  '¿Cuál es el menú de hoy?',
  'Recomiéndame algo',
  '¿Hay promociones?',
];

export default function ChatPage() {
  const [messages, setMessages] = useState<MessageType[]>([
    {
      role: 'assistant',
      content: '👋 ¡Hola! Soy tu asistente de cafetería. ¿En qué puedo ayudarte hoy?',
      timestamp: new Date(),
    },
  ]);
  const [selectedProvider, setSelectedProvider] = useState<AIProvider>('gemini');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = React.useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: MessageType = {
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pregunta: text,
          provider: selectedProvider,
          historial: [...messages, userMessage].map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);

      const data = await response.json();

      const assistantMessage: MessageType = {
        role: 'assistant',
        content: data.respuesta || 'Sin respuesta',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: MessageType = {
        role: 'assistant',
        content: `❌ Error: ${error instanceof Error ? error.message : 'Desconocido'}. Por favor intenta nuevamente.`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 flex flex-col">
      {/* Header */}
      <header className="bg-blue-900 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <span className="text-2xl">☕</span>
            <span className="font-bold text-xl">NeoCafeIA Chat</span>
          </Link>
          <nav className="text-sm">
            <Link href="/" className="hover:text-blue-200 transition-colors">
              ← Volver al inicio
            </Link>
          </nav>
        </div>
      </header>

      {/* Main Chat Area */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 py-8 flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 bg-white rounded-lg shadow-lg p-6 mb-6 overflow-y-auto">
          {messages.map((message, index) => (
            <MessageBubble key={`msg-${index}-${message.timestamp?.getTime() ?? index}`} message={message} />
          ))}
          {loading && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-100 text-gray-700 px-4 py-3 rounded-lg">
                <div className="flex gap-2">
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {messages.length === 1 && (
          <div className="mb-6">
            <p className="text-sm font-semibold text-gray-600 mb-3">Sugerencias:</p>
            <SuggestionChips
              suggestions={SUGGESTIONS}
              onSelect={handleSendMessage}
            />
          </div>
        )}

        {/* Provider Selector */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          <ProviderSelector
            value={selectedProvider}
            onChange={(provider) => setSelectedProvider(provider)}
          />
        </div>

        {/* Input Area */}
        <div className="bg-white rounded-lg shadow-lg p-4">
          <ChatInput onSend={handleSendMessage} disabled={loading} />
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center text-gray-600 text-sm py-4">
        <p>NeoCafeIA © 2025 | Asistente inteligente de cafetería</p>
      </footer>
    </div>
  );
}
