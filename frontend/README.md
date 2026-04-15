# NeoCafeIA Frontend

Frontend de Next.js 15 con TypeScript para NeoCafeIA.

## Stack

- **Next.js 15** — Framework React con App Router
- **TypeScript** — Type safety estricta
- **Tailwind CSS** — Estilos Utility-first
- **React 19** — Interfaz de usuario interactiva

## Estructura

```
frontend/
├── src/
│   ├── app/                # App Router (Next.js 15)
│   │   ├── page.tsx        # Landing page
│   │   ├── chat/
│   │   │   └── page.tsx    # Página de chat
│   │   ├── layout.tsx      # Layout raíz
│   │   └── globals.css     # Estilos globales
│   ├── components/         # Componentes reutilizables
│   │   ├── ChatInput.tsx
│   │   ├── MessageBubble.tsx
│   │   ├── ProviderSelector.tsx
│   │   └── SuggestionChips.tsx
│   └── types/              # Tipos TypeScript
│       └── index.ts
├── public/                 # Archivos estáticos
├── tailwind.config.ts      # Configuración Tailwind
├── tsconfig.json           # Configuración TypeScript
├── next.config.js          # Configuración Next.js
└── package.json
```

## Inicio Rápido

### Instalación

```bash
cd frontend
npm install
# o
yarn install
```

### Desarrollo

```bash
npm run dev
# o
yarn dev
```

Accede a [http://localhost:3000](http://localhost:3000) en tu navegador.

### Build para Producción

```bash
npm run build
npm start
# o
yarn build
yarn start
```

## Componentes Principales

### `ChatPage` (`src/app/chat/page.tsx`)

- Interfaz de chat interactiva
- Selector de proveedores de IA
- Historial de mensajes
- Sugerencias contextuales

### `MessageBubble`

Renderiza mensajes de usuario/asistente con timestamp.

### `ChatInput`

Input con soporte para Shift+Enter (salto de línea) y Enter (enviar).

### `ProviderSelector`

Dropdown para elegir entre Gemini, OpenAI, Claude, etc.

## Configuración

### Variables de entorno

Crea un archivo `.env.local` basado en `.env.example`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Despliegue en Vercel

1. Push al repositorio de GitHub
2. Conecta en Vercel dashboard
3. Configura variables de entorno
4. Deploy automático 🚀

## TypeScript Strict

El proyecto usa `strict: true` en `tsconfig.json` para máxima seguridad de tipos.

## Tailwind CSS

Colores personalizados de cafetería:

- `primary` — Marrón café (#6F4E37)
- `accent` — Caramelo (#D4A574)
- `dark` — Negro café (#2C1810)

---

Disfruta construyendo con NeoCafeIA Frontend 🚀
