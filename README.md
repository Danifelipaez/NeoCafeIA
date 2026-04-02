# Cafetería Selecto Granos - Chat IA

Chatbot inteligente para la Cafetería Selecto Granos con arquitectura hexagonal simplificada, FastAPI como backend y modelos de IA (Gemini, OpenAI, Claude, DeepSeek, LangChain).

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Navega al directorio del proyecto:**
   ```bash
   cd proyecto-cafeteria-ai
   ```

2. **Crea un entorno virtual (opcional pero recomendado):**
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

### Configuración

1. **Crea un archivo `.env`** en la raíz del proyecto basándote en `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo `.env`** y añade tus API keys:
   ```
   GEMINI_API_KEY=tu_gemini_api_key_aqui
   OPENAI_API_KEY=tu_openai_api_key_aqui
   ANTHROPIC_API_KEY=tu_anthropic_api_key_aqui
   DEEPSEEK_API_KEY=tu_deepseek_api_key_aqui
   ```

### Ejecución

1. **Inicia el servidor FastAPI:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Accede a la aplicación:**
   - **Chat Web:** http://localhost:8000/webchat
   - **Documentación API:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

## 📁 Estructura del Proyecto

```
proyecto-cafeteria-ai/
├── main.py                 # Entrypoint de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── .env.example           # Template de variables de entorno
├── vercel.json            # Configuración para despliegue Vercel
├── system_prompt/         # Instrucciones del sistema (IA)
│   └── asistente.md
├── rules/                 # Reglas de comportamiento
│   └── comportamiento.md
├── knowledge/             # Base de conocimiento
│   ├── negocio.md
│   ├── menu.md
│   ├── promociones.md
│   └── recomendaciones.md
└── src/                   # Código fuente
    ├── domain/
    │   └── schemas.py     # Modelos Pydantic
    ├── services/
    │   └── chat_service.py
    └── infrastructure/
        ├── model_factory.py
        ├── gemini_adapter.py
        ├── openai_adapter.py
        ├── claude_adapter.py
        ├── deepseek_adapter.py
        ├── langchain_adapter.py
        ├── context_loader.py
        └── web_frontend.py
```

## 🔌 Proveedores de IA Disponibles

- **Gemini 2.5 Flash** (Recomendado - Gratuito)
- **OpenAI** (GPT-4o Mini)
- **Claude** (Anthropic)
- **DeepSeek** (DeepSeek Chat)
- **LangChain + Gemini** (Cadena LangChain)

## 📝 Endpoints de la API

### GET `/health`
Verifica el estado del servidor.

**Respuesta:**
```json
{
  "status": "ok"
}
```

### GET `/webchat`
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
  "respuesta": "En la Cafetería Aroma & Código tenemos...",
  "provider": "gemini",
  "tokens_usados": null
}
```

## 🎯 Cómo Usar el Webchat

1. Accede a http://localhost:8000/webchat
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
3. Añade el adaptador al `AIModelFactory` en `model_factory.py`
4. Agrega el proveedor al enum `AIProvider` en `domain/schemas.py`

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'uvicorn'"
Asegúrate de haber ejecutado:
```bash
pip install -r requirements.txt
```

### Error: "GEMINI_API_KEY no está configurada"
Verifica que el archivo `.env` existe y contiene la clave API:
```bash
GEMINI_API_KEY=tu_clave_aqui
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