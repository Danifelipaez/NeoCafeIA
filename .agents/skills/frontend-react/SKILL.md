---
name: frontend-react
version: 1.0.0
description: Skill para documentar y extender el frontend de NeoCafeIA en Next.js 15 + React 19 + TypeScript estricto.
compatibility:
  react: 19
  nextjs: 15
  typescript: 5.3
  tailwindcss: 3.4
---

# Frontend React Skill (NeoCafeIA)

Esta skill describe la implementacion frontend actual de NeoCafeIA, basada en Next.js 15 (App Router), React 19 y TypeScript estricto.

## 1) Descripcion semantica

El frontend expone una experiencia de cafeteria asistida por IA con dos objetivos principales:

- Descubrimiento de valor del producto (landing de presentacion).
- Conversacion en tiempo real con el asistente (pantalla de chat) para consultas de menu, promociones y recomendaciones.

Pantallas disponibles:

- `/` (landing): presenta marca, caracteristicas y CTA hacia chat.
- `/chat`: interfaz conversacional con historial, sugerencias, selector de proveedor y envio de prompts.

Design system usado:

- Base conceptual: Material Design 3, tomando como referencia y fuente de verdad de tokens [DESIGN.md](../../../../DESIGN.md).
- Implementacion actual: Tailwind CSS con extensiones en `frontend/tailwind.config.ts` y utilidades globales en `frontend/src/app/globals.css`.

## 2) Estructura especifica del proyecto

### `frontend/src/app/`

App Router de Next.js 15.

- `layout.tsx`: layout raiz de la app.
- `globals.css`: estilos globales y utilidades (`gradient-primary`, `btn-primary`, `card`, etc.).
- `page.tsx`: landing principal (`/`).
- `chat/page.tsx`: pagina de chat (`/chat`) y orquestacion de estado/conexion al backend.

### `frontend/src/components/`

Componentes reutilizables y tipados:

- `ChatInput.tsx`
  - Props: `onSend: (message: string) => void`, `disabled?: boolean`
- `MessageBubble.tsx`
  - Props: `message: Message`
- `ProviderSelector.tsx`
  - Props: `value: AIProvider`, `onChange: (provider: AIProvider) => void`
- `SuggestionChips.tsx`
  - Props: `suggestions: string[]`, `onSelect: (suggestion: string) => void`

### `frontend/src/types/index.ts`

Tipos base compartidos del frontend:

- `AIProvider`
- `Message`
- `ChatRequest`
- `ChatResponse`

### `frontend/tailwind.config.ts`

Define colores custom y tipografia para el frontend actual. Se usa para centralizar tokens visuales consumidos por componentes y clases utilitarias.

## 3) Tokens de diseno activos

Tokens de [DESIGN.md](../../../../DESIGN.md) que si estan alineados/activos en la implementacion Tailwind actual:

- `on-primary: #ffffff` (equivalente funcional a `text-white`)
- `surface-container-lowest: #ffffff` (equivalente funcional a `bg-white`)

Tokens de paleta cafetera implementados en Tailwind (version actual de frontend):

- `primary: #6F4E37`
- `primary-light: #8B6F47`
- `primary-dark: #4A3728`
- `accent: #D4A574`
- `accent-light: #E8C5A5`
- `dark: #2C1810`
- `light: #FBF8F3`
- `success: #10B981`

Nota tecnica: la base conceptual del sistema es M3 de `DESIGN.md`, pero el frontend actual usa una adaptacion cafetera en `tailwind.config.ts`. Si se requiere paridad 1:1 con M3, normalizar los hex en la config de Tailwind.

## 4) Como agregar un nuevo componente

Patron recomendado (igual al existente):

1. Crear archivo en `frontend/src/components/` con `use client` si tiene estado/eventos.
2. Definir interfaz `Props` explicita y exportar componente con nombre.
3. Tipar callbacks y payloads (sin `any`).
4. Reusar tokens de Tailwind (ej. `primary`, `accent`, `dark`) y utilidades comunes.
5. Integrar el componente en una pagina de `frontend/src/app/`.

Ejemplo: nuevo componente `QuickStats.tsx`.

```tsx
'use client';

import React from 'react';

interface QuickStatsProps {
  totalMessages: number;
  providerLabel: string;
}

export function QuickStats({ totalMessages, providerLabel }: QuickStatsProps) {
  return (
    <section className="bg-white rounded-lg shadow p-4 text-dark">
      <p className="text-sm">Mensajes en sesion: {totalMessages}</p>
      <p className="text-sm">Proveedor activo: {providerLabel}</p>
    </section>
  );
}
```

Uso en `frontend/src/app/chat/page.tsx`:

```tsx
import { QuickStats } from '@/components/QuickStats';

<QuickStats
  totalMessages={messages.length}
  providerLabel={selectedProvider}
/>
```

## 5) Como agregar un nuevo provider de IA al selector

Cambios minimos requeridos:

1. Actualizar union type en `frontend/src/types/index.ts`:

```ts
export type AIProvider =
  | 'gemini'
  | 'openai'
  | 'claude'
  | 'deepseek'
  | 'langchain'
  | 'react'
  | 'mistral';
```

2. Agregar opcion en `frontend/src/components/ProviderSelector.tsx`:

```tsx
<option value="mistral">Mistral</option>
```

3. Verificar que la pagina `frontend/src/app/chat/page.tsx` envia el nuevo valor en `provider` (ya queda automatico por estado tipado).
4. Confirmar soporte del provider en backend (factory/adaptador), de lo contrario `/api/chat` respondera error de proveedor no soportado.

## 6) Como conectar con el backend (`/api/chat`)

Flujo actual en `frontend/src/app/chat/page.tsx`:

1. Usuario envia mensaje desde `ChatInput`.
2. `handleSendMessage` agrega el mensaje de usuario al estado local.
3. Se hace `fetch('/api/chat', { method: 'POST', headers, body })`.
4. Payload enviado:

```json
{
  "pregunta": "texto del usuario",
  "provider": "gemini",
  "historial": [
    { "role": "assistant", "content": "..." },
    { "role": "user", "content": "..." }
  ]
}
```

5. La respuesta esperada (tipada como `ChatResponse`) incluye `respuesta`, `provider` y `tokens_usados`.
6. El frontend agrega el mensaje del asistente al historial o un mensaje de error si falla la peticion.

## 7) Referencias

- Next.js 15 (App Router): https://nextjs.org/docs/app
- React 19: https://react.dev/
- TypeScript: https://www.typescriptlang.org/docs/
- Tailwind CSS: https://tailwindcss.com/docs
- Design tokens del proyecto: [DESIGN.md](../../../../DESIGN.md)
- Guia del frontend del proyecto: [frontend/README.md](../../../../frontend/README.md)
