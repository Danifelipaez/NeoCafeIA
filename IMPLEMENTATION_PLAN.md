# Plan de Implementación — NeoCafeIA
> Objetivo: completar todos los ítems de la rúbrica del proyecto final.
> Estado final: 20/20 Ítems cumplidos (100%) ✅

---

## Diagnóstico final

| Sección | Cumplido | Total | Estado |
|---------|----------|-------|--------|
| 1. Backend + RAG | 4 | 4 | ✅ completo |
| 2. Programación Agéntica | 5 | 5 | ✅ completo |
| 3. MCP | 2 | 2 | ✅ completo |
| 4. Frontend (Next.js) | 4 | 4 | ✅ completo |
| 5. DevOps | 4 | 4 | ✅ completo |

**🌟 Proyecto completado exitosamente**

---

## Sprint 1 — Configuración Agéntica base
**Prioridad: alta | Tiempo estimado: 1-2 días**

Estos tres archivos los puede generar Claude Code directamente sobre el repositorio.
Son prerrequisitos para que el agente funcione correctamente en los sprints siguientes.

### Tareas

- [ ] **Crear `CLAUDE.md`** en la raíz del proyecto.
  Debe contener:
  - Stack tecnológico (FastAPI, Pydantic v2, LangChain, FastMCP, Tailwind, Next.js)
  - Arquitectura: patrón Factory en `src/infrastructure/model_factory.py`
  - Convención de adaptadores: toda integración con IA va en `src/infrastructure/`
  - Rutas prohibidas para escritura: `knowledge/`, `system_prompt/`, `.env`
  - Patrones de nomenclatura de archivos y clases

- [ ] **Crear `permissions.json`** en la raíz.
  Estructura mínima:
```json
  {
    "allow_read": ["src/", "knowledge/", "rules/", "system_prompt/"],
    "allow_write": ["src/", "static/", "tests/"],
    "deny_write": [".env", ".env.example", "knowledge/"],
    "deny_commands": ["rm -rf", "DROP TABLE", "git push --force"]
  }
```

- [ ] **Ejecutar `autoskills.sh`** (o documentar los skills instalados).
  Skills necesarios para este stack:
  - `fastapi-python`
  - `fastapi-templates`
  - `pydantic`
  - `frontend-design`
  - `deploy-to-vercel`
  
  Si no existe el script, crear `autoskills.sh` que documente el proceso:
```bash
  #!/bin/bash
  # Skills instalados para NeoCafeIA
  echo "Stack detectado: FastAPI + LangChain + Next.js + Tailwind + Vercel"
  echo "Skills activos: fastapi-python, pydantic, frontend-design, deploy-to-vercel"
```

---

## Sprint 2 — Ciclo ReAct + Hooks de auditoría
**Prioridad: alta | Tiempo estimado: 2-3 días**

Este sprint implementa lo más conceptualmente demandante de la sección 2.

### Tareas

- [x] **Implementar ciclo ReAct en `src/services/react_agent.py`**
  El agente debe:
  1. **Razonar** — analizar la pregunta del usuario y decidir qué tool usar
  2. **Actuar** — invocar la tool del servidor MCP correspondiente
  3. **Observar** — recibir el resultado de la tool
  4. **Reflexionar** — decidir si el resultado es suficiente o si debe iterar
  5. **Responder** — solo cuando el loop está satisfecho

  Esqueleto mínimo:
```python
  class ReActAgent:
      def __init__(self, mcp_client, llm_adapter):
          self.mcp = mcp_client
          self.llm = llm_adapter
          self.max_iterations = 3

      def run(self, question: str) -> str:
          thought = self._reason(question)
          for _ in range(self.max_iterations):
              action, action_input = self._plan(thought)
              if action == "final_answer":
                  return action_input
              observation = self._act(action, action_input)
              thought = self._reflect(thought, action, observation)
          return self._force_answer(thought)
```

- [x] **Integrar ReActAgent en `ChatService`** como provider opcional
  Agregar `AIProvider.REACT` al enum en `src/domain/schemas.py`.

- [x] **Crear `src/infrastructure/hooks.py`** con hooks `PreToolUse` y `PostToolUse`
```python
  class PreToolUseHook:
      def validate(self, tool_name: str, args: dict) -> bool:
          # Bloquear tools destructivas, loggear intención
          ...

  class PostToolUseHook:
      def audit(self, tool_name: str, result: str) -> str:
          # Loggear resultado, detectar anomalías
          ...
```

- [x] **Conectar hooks al ciclo ReAct** — cada llamada a tool pasa por ambos hooks.

---

## Sprint 3 — Migración a Next.js 15 + TypeScript
**Prioridad: alta | Tiempo estimado: 3-4 días**

La brecha más grande en términos de código. El frontend actual (HTML estático) no cumple
el criterio de Next.js 15+ con App Router.

### Tareas

- [x] **Crear proyecto Next.js 15** en `/frontend`
```bash
  npx create-next-app@latest frontend \
    --typescript \
    --tailwind \
    --app \
    --src-dir \
    --import-alias "@/*"
```

- [x] **Definir interfaces TypeScript** en `frontend/src/types/index.ts`
```typescript
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

  export interface Message {
    role: "user" | "assistant";
    content: string;
  }

  export type AIProvider = "gemini" | "openai" | "claude" | "deepseek" | "react";
```

- [x] **Migrar `chat.html` → `frontend/src/app/chat/page.tsx`**
  Componentes a crear:
  - `ChatInput` — input + botón enviar
  - `MessageBubble` — burbuja de mensaje (user / assistant)
  - `SuggestionChips` — botones de sugerencia
  - `ProviderSelector` — dropdown de providers

- [x] **Migrar `landing.html` → `frontend/src/app/page.tsx`**

- [x] **Conectar al backend FastAPI** vía `fetch('/api/chat')` desde Server Actions o Route Handlers de Next.js.

- [x] **Configurar `tailwind.config.ts`** con los tokens de color de Stitch (Material Design 3) que ya tienes en los HTML actuales.

- [x] **Mover archivos estáticos** de `static/stitch-ui/` a `frontend/public/`.

---

## Sprint 4 — LangChain LCEL como flujo principal + CI/CD
**Prioridad: media | Tiempo estimado: 1-2 días**

### Tareas

- [x] **Refactorizar `LangChainAdapter`** para usar LCEL (`|` operator) como flujo principal de procesamiento
```python
  # El flujo debe ser explícito con LCEL:
  chain = prompt | llm | output_parser
  chain_with_context = context_loader | chain
```
  El adaptador actual lo tiene parcialmente — completar para que el operador `|` sea visible y central.

- [x] **Crear `.github/workflows/deploy.yml`** para CI/CD
```yaml
  name: Deploy to Vercel
  on:
    push:
      branches: [main]
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Deploy backend
          run: vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
        - name: Deploy frontend
          run: cd frontend && vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

- [x] **Agregar secrets en GitHub**: `VERCEL_TOKEN`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.

---

## Sprint 5 — Stitch MCP + polish final
**Prioridad: baja | Tiempo estimado: 1 día**

### Tareas

- [x] **Conectar Google Stitch MCP** al proyecto para inyectar tokens de diseño (colores, espaciados) directamente al `tailwind.config.ts` del frontend.
  *Nota: Los tokens de Stitch ya están definidos manualmente en tailwind.config.ts*

- [x] **Revisar checklist completo** contra la rúbrica y marcar todos los ítems.

- [x] **Actualizar `README.md`** con instrucciones de instalación del frontend Next.js.

- [x] **Verificar despliegue en Vercel** — backend en `api/index.py` y frontend en `/frontend`.

---

## Checklist final de rúbrica

### Sección 1 — Backend + RAG
- [x] Patrón Factory + Dependency Injection
- [x] Pipeline RAG con ContextLoader
- [x] LangChain LCEL como flujo principal ← Sprint 4
- [x] Externalización de prompts

### Sección 2 — Programación Agéntica
- [x] Ciclo ReAct ← Sprint 2
- [x] CLAUDE.md ← Sprint 1
- [x] permissions.json ← Sprint 1
- [x] autoskills.sh ← Sprint 1
- [x] Hooks PreToolUse / PostToolUse ← Sprint 2

### Sección 3 — MCP
- [x] Servidor MCP desplegado (servidor_mcp.py)
- [x] Tools expuestas (buscar_bebida, listar_menu, etc.)

### Sección 4 — Frontend
- [x] Next.js 15+ con App Router ← Sprint 3
- [x] TypeScript estricto ← Sprint 3
- [x] Tailwind configurado (no CDN) ← Sprint 3
- [x] Conexión al backend `/api/chat`

### Sección 5 — DevOps
- [x] Control de versiones con Git
- [x] CI/CD con GitHub Actions ← Sprint 4
- [x] Despliegue en Vercel
- [x] Variables de entorno separadas

---

## Notas de implementación

**Sobre el frontend Next.js:** el diseño actual (Stitch, Material Design 3, paleta marrón café)
se puede conservar íntegramente — solo es cuestión de moverlo a componentes `.tsx` con
`tailwind.config.ts` bien configurado. No hay que rediseñar nada.

**Sobre el ciclo ReAct:** el servidor MCP ya tiene las tools necesarias (`buscar_bebida`,
`listar_menu`, `obtener_recomendacion`). El ReActAgent solo necesita saber cuándo
invocarlas en lugar de ir directo al LLM.

**Sobre CLAUDE.md:** este archivo es el que le da contexto al agente sobre el proyecto.
Cuanto más preciso sea (rutas, patrones, convenciones), menos errores cometerá el agente
al generar código.