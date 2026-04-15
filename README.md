# NeoCafeIA - Asistente de IA para Cafetería

Chat inteligente para cafeterías con backend en FastAPI, frontend en Next.js 15, arquitectura hexagonal simplificada, y múltiples modelos de IA (Gemini, OpenAI, Claude, DeepSeek, LangChain, ReAct).

## 🏗️ Arquitectura

- **Backend:** FastAPI con adaptadores de IA y ciclo ReAct
- **Frontend:** Next.js 15 con TypeScript y Tailwind CSS
- **Base de Conocimiento:** Markdown en `/knowledge/`
- **Orquestación:** MCP (Model Context Protocol) con tools de consulta

## 🚀 Inicio Rápido

### Backend (FastAPI)

#### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

#### Instalación

1. **Navega al directorio del proyecto:**
   ```bash
   cd NeoCafeIA
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activa el entorno virtual:**
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Crea un archivo `.env`** basado en el template:
   ```bash
   cp .env.example .env
   ```

6. **Edita el archivo `.env`** y añade tus API keys:
   ```bash
   GOOGLE_API_KEY=tu_clave_real_de_google_gemini
   OPENAI_API_KEY=tu_clave_real_de_openai
   ANTHROPIC_API_KEY=tu_clave_real_de_claude
   DEEPSEEK_API_KEY=tu_clave_real_de_deepseek
   ```

7. **Inicia el servidor:**
   ```bash
   uvicorn app:app --reload
   ```

### Frontend (Next.js 15)

#### Requisitos Previos
- Node.js 20+ (recomendado)
- npm o yarn

#### Instalación

1. **Navega al directorio del frontend:**
   ```bash
   cd frontend
   ```

2. **Instala las dependencias:**
   ```bash
   npm install
   # o
   yarn install
   ```

3. **Crea archivo `.env.local`:**
   ```bash
   cp .env.example .env.local
   ```

4. **Inicia el servidor de desarrollo:**
   ```bash
   npm run dev
   # o
   yarn dev
   ```

5. **Accede a:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend: [http://localhost:8000](http://localhost:8000)
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   ```

   **⚠️ Importante:** Nunca subas el archivo `.env` al repositorio. Está incluido en `.gitignore` para mantener tus claves seguras.

### Ejecución

1. **Inicia el servidor FastAPI:**
   ```bash
   uvicorn app:app --reload
   ```

2. **Accede a la aplicación:**
   - **Chat Web:** http://localhost:8000/app
   - **Landing y Stitch UI:** http://localhost:8000/stitch-ui
   - **Documentación API:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

## 📁 Estructura del Proyecto

```
NeoCafeIA/
├── app.py                 # Entrypoint de la aplicación FastAPI
├── README.md              # Este archivo
├── SECURITY.md            # Política de seguridad del proyecto
├── .env.example           # Template de variables de entorno
├── .gitignore             # Archivos a ignorar en git
├── requirements.txt       # Dependencias del proyecto
├── servidor_mcp.py        # Servidor MCP para herramientas y consultas
├── knowledge/             # Base de conocimiento
│   ├── bebidas.md
│   ├── granos.md
│   ├── menu.md
│   ├── negocio.md
│   ├── postres.md
│   ├── promociones.md
│   └── recomendaciones.md
├── rules/                 # Reglas de comportamiento
│   └── comportamiento.md
├── skills/                # Habilidades del asistente
│   └── asistente-cafeteria.md
├── system_prompt/         # Instrucciones del sistema (IA)
│   └── asistente.md
├── src/                   # Código fuente
│   ├── domain/
│   │   └── schemas.py
│   ├── services/
│   │   └── chat_service.py
│   └── infrastructure/
│       ├── model_factory.py
│       ├── gemini_adapter.py
│       ├── openai_adapter.py
│       ├── claude_adapter.py
│       ├── deepseek_adapter.py
│       ├── langchain_adapter.py
│       ├── context_loader.py
│       └── web_frontend.py
├── static/                # Frontend estático
│   └── stitch-ui/
```

## 🔌 Proveedores de IA Disponibles

- **Gemini 2.5 Flash** (Recomendado - Gratuito)
- **OpenAI** (GPT-4o Mini)
- **Claude** (Anthropic)
- **DeepSeek** (DeepSeek Chat)
- **LangChain + Gemini** (Cadena LangChain)

## 🤖 Servidor MCP (Model Context Protocol)

NeoCafeIA incluye un servidor MCP para integración avanzada con herramientas de IA.

### Características del Servidor MCP

- **Búsqueda de bebidas** — Información detallada de cada bebida del menú
- **Listado de menú completo** — Bebidas, postres y promociones
- **Recomendaciones personalizadas** — Basadas en preferencias del usuario
- **Consulta de granos** — Información de granos de café disponibles
- **Verificación de promociones** — Promociones activas del día

### Ejecución del Servidor MCP

```bash
python servidor_mcp.py
```

El servidor expone herramientas que pueden ser utilizadas por clientes MCP para consultas especializadas sobre el catálogo de NeoCafeía.

## 📝 Endpoints de la API

### GET `/health`
Verifica el estado del servidor.

**Respuesta:**
```json
{
  "status": "ok"
}
```

### GET `/app`
Devuelve la interfaz web interactiva del chat.

### POST `/chat`
Envía un mensaje y obtiene una respuesta del chatbot.

**Request:**
```json
{
  "pregunta": "¿Qué bebidas tienen?",
  "provider": "gemini",
  "historial": []
}
```

**Response:**
```json
{
  "respuesta": "En Selecto Granos tenemos...",
  "provider": "gemini",
  "tokens_usados": null
}
```

## 🎯 Cómo Usar el Webchat

1. Accede a http://localhost:8000/app
2. Selecciona el proveedor de IA en el dropdown
3. Escribe tu pregunta en el campo de texto
4. Presiona "Enviar" o Enter
5. Recibe la respuesta del chatbot

## 🛠️ Personalización

### Cambiar el System Prompt
Edita el archivo `system_prompt/asistente.md` para cambiar las instrucciones base.

### Agregar Nuevas Reglas
Añade reglas adicionales en `rules/comportamiento.md`.

### Actualizar la Base de Conocimiento
Modifica o crea nuevos archivos `.md` en la carpeta `knowledge/`.

### Soportar un nuevo Proveedor de IA
1. Crea un nuevo archivo `src/infrastructure/nuevo_adapter.py`
2. Implementa la clase heredando de `IModelAdapter`
3. Añade el adaptador al `AIModelFactory` en `src/infrastructure/model_factory.py`
4. Agrega el proveedor al enum `AIProvider` en `src/domain/schemas.py`

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'uvicorn'"
Asegúrate de haber ejecutado:
```bash
pip install -r requirements.txt
```

### Error: "GOOGLE_API_KEY no está configurada"
Verifica que el archivo `.env` existe y contiene la clave API:
```bash
GOOGLE_API_KEY=tu_clave_aqui
```

### El servidor no inicia
Intenta limpiar el caché:
```bash
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

## 🚀 Despliegue en Vercel

1. Sube el proyecto a un repositorio de GitHub
2. Conecta tu repositorio en Vercel
3. Configura las variables de entorno en el dashboard
4. Despliega automáticamente

Para más información: [Documentación de Vercel](https://vercel.com/docs)

## 📄 Licencia

Este proyecto está disponible bajo la licencia MIT.

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

---

**¡Disfruta tu chatbot de cafetería! ☕**