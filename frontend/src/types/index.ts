/**
 * Tipos TypeScript para el frontend de NeoCafeIA
 */

export type AIProvider = 'gemini' | 'openai' | 'claude' | 'deepseek' | 'langchain' | 'react';

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatRequest {
  pregunta: string;
  provider: AIProvider;
  historial: Message[];
}

export interface ChatResponse {
  respuesta: string;
  provider: AIProvider;
  tokens_usados: number | null;
}

export interface Product {
  id: string;
  nombre: string;
  precio: number;
  descripcion?: string;
  categoria?: string;
}

export interface Combo {
  id: string;
  nombre: string;
  items: Product[];
  precioCombinado: number;
  descuento?: number;
}
