# NeoCafeIA - Asistente de IA para Cafetería

Chatbot inteligente para cafeterías con arquitectura hexagonal simplificada, FastAPI como backend y múltiples modelos de IA (Gemini, OpenAI, Claude, DeepSeek, LangChain).

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Navega al directorio del proyecto:**
   ```bash
   cd NeoCafeIA
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
   pip install -r main/requirements.txt
   ```

### Configuración

1. **Crea un archivo `.env`** basado en el template:
   ```bash
   cp .env.example .env
   ```

2. **Edita el archivo `.env`** y añade tus API keys reales:
   ```bash
   # Edita .env y reemplaza los valores de ejemplo con tus claves reales
   GOOGLE_API_KEY=tu_clave_real_de_google_gemini
   OPENAI_API_KEY=tu_clave_real_de_openai
   # etc.
   ```

   **⚠️ Importante:** Nunca subas el archivo `.env` al repositorio. Está incluido en `.gitignore` para mantener tus claves seguras.

### Ejecución

1. **Inicia el servidor FastAPI:**
   ```bash
   uvicorn app:app --reload
   ```

2. **Accede a la aplicación:**
   - **Chat Web:** http://localhost:8000/webchat
   - **Documentación API:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

## 📁 Estructura del Proyecto

```
NeoCafeIA/
├── app.py                 # Entrypoint de la aplicación FastAPI
├── codigo.py              # Código adicional
├── README.md              # Este archivo
├── .env.example           # Template de variables de entorno
├── .gitignore             # Archivos a ignorar en git
├── .env                   # Variables de entorno (crear basado en ejemplo)
├── main/                  # Paquete principal
│   ├── __init__.py
│   ├── requirements.txt   # Dependencias del proyecto
│   ├── vercel.json        # Configuración para despliegue Vercel
│   ├── knowledge/         # Base de conocimiento
│   │   ├── bebidas.md
│   │   ├── granos.md
│   │   ├── menu.md
│   │   ├── negocio.md
│   │   ├── postres.md
│   │   ├── promociones.md
│   │   └── recomendaciones.md
│   ├── rules/             # Reglas de comportamiento
│   │   └── comportamiento.md
│   ├── skills/            # Habilidades del asistente
│   │   └── asistente-cafeteria.md
│   ├── system_prompt/     # Instrucciones del sistema (IA)
│   │   └── asistente.md
│   └── src/               # Código fuente
│       ├── domain/
│       │   └── schemas.py # Modelos Pydantic
│       ├── services/
│       │   └── chat_service.py
│       └── infrastructure/
│           ├── model_factory.py
│           ├── gemini_adapter.py
│           ├── openai_adapter.py
│           ├── claude_adapter.py
│           ├── deepseek_adapter.py
│           ├── langchain_adapter.py
│           ├── context_loader.py
│           └── web_frontend.py
```

## 🔌 Proveedores de IA Disponibles

- **Gemini 2.5 Flash** (Recomendado - Gratuito)
- **OpenAI** (GPT-4o Mini)
- **Claude** (Anthropic)
- **DeepSeek** (DeepSeek Chat)
- **LangChain + Gemini** (Cadena LangChain)
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
Edita el archivo `main/system_prompt/asistente.md` para cambiar las instrucciones base.

### Agregar Nuevas Reglas
Añade reglas adicionales en `main/rules/comportamiento.md`.

### Actualizar la Base de Conocimiento
Modifica o crea nuevos archivos `.md` en la carpeta `main/knowledge/`.

### Soportar un nuevo Proveedor de IA
1. Crea un nuevo archivo `main/src/infrastructure/nuevo_adapter.py`
2. Implementa la clase heredando de `IModelAdapter`
3. Añade el adaptador al `AIModelFactory` en `main/src/infrastructure/model_factory.py`
4. Agrega el proveedor al enum `AIProvider` en `main/src/domain/schemas.py`

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'uvicorn'"
Asegúrate de haber ejecutado:
```bash
pip install -r main/requirements.txt
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
pip install -r main/requirements.txt --no-cache-dir
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