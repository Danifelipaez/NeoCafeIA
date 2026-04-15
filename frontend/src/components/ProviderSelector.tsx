'use client';

import React from 'react';
import type { AIProvider } from '@/types';

interface ProviderSelectorProps {
  value: AIProvider;
  onChange: (provider: AIProvider) => void;
}

export function ProviderSelector({ value, onChange }: ProviderSelectorProps) {
  return (
    <div className="flex flex-col gap-2">
      <label htmlFor="provider" className="font-semibold text-dark">
        Proveedor de IA:
      </label>
      <select
        id="provider"
        value={value}
        onChange={(e) => onChange(e.target.value as AIProvider)}
        className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
      >
        <option value="gemini">Gemini (Recomendado)</option>
        <option value="openai">OpenAI GPT-4</option>
        <option value="claude">Claude</option>
        <option value="deepseek">DeepSeek</option>
        <option value="langchain">LangChain</option>
        <option value="react">ReAct Agent</option>
      </select>
    </div>
  );
}
