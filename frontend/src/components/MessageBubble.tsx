'use client';

import React from 'react';
import { Message as MessageType } from '@/types';

interface MessageBubbleProps {
  message: MessageType;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-xs md:max-w-md px-4 py-3 rounded-lg ${
          isUser
            ? 'bg-primary text-white rounded-br-none'
            : 'bg-gray-100 text-dark rounded-bl-none'
        }`}
      >
        <p className="text-sm md:text-base break-words">{message.content}</p>
        {message.timestamp && (
          <p className={`text-xs mt-1 ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {message.timestamp.toLocaleTimeString('es-ES', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        )}
      </div>
    </div>
  );
}
