# API Stitch Integration - Documentación

## 🌐 Rutas Disponibles

### Frontend (HTML)
- `GET /` - Página de inicio antigua
- `GET /stitch-ui` - Portal central de Stitch UI
- `GET /stitch-ui/landing` - Landing page completa
- `GET /chat` - Chat Desktop optimizado
- `GET /mobile/chat` - Chat Mobile responsivo
- `GET /app` - Chat UI antigua

### API Endpoints

#### Health Check
```
GET /health
```
Verifica el estado del servidor.

**Respuesta:**
```json
{
  "status": "ok"
}
```

#### Información del Proyecto
```
GET /api/info
```
Obtiene información sobre el proyecto.

**Respuesta:**
```json
{
  "nombre": "Cafetería Selecto Granos",
  "descripcion": "The Curated Ritual - Chat IA para recomendaciones de café",
  "version": "1.0",
  "providers": ["gemini", "openai", "claude", "deepseek"],
  "url_stitch": "/stitch-ui"
}
```

#### Chat
```
POST /api/chat
```
Envía un mensaje al asistente IA.

**Body:**
```json
{
  "pregunta": "¿Qué café me recomiendas?",
  "provider": "gemini",
  "historial": [
    {
      "role": "user",
      "content": "Hola"
    },
    {
      "role": "assistant",
      "content": "¡Bienvenido a Selecto Granos!"
    }
  ]
}
```

**Respuesta:**
```json
{
  "respuesta": "Te recomendaría nuestro Etiopía Sidamo...",
  "provider": "gemini",
  "tokens_usados": 125
}
```

**Providers Soportados:**
- `gemini` - Google Gemini (Defecto)
- `openai` - OpenAI GPT
- `claude` - Anthropic Claude
- `deepseek` - DeepSeek
- `langchain` - LangChain

#### Menú Completo
```
GET /api/menu
```
Obtiene todo el menú con precios.

**Respuesta:**
```json
{
  "status": "ok",
  "content": "# Menú Completo...",
  "items": {
    "etiopía sidamo": 4.50,
    "flat white ai": 5.25,
    "cold brew selecto": 6.00
  },
  "combos": {
    "combo matutino": 12.50
  }
}
```

#### Recomendaciones
```
GET /api/recommendations?preference=suave
```
Obtiene recomendaciones personalizadas.

**Parámetros:**
- `preference` (opcional): `suave`, `fuerte`, `cremoso`, `refrescante`, `dulce`

**Respuesta:**
```json
{
  "status": "ok",
  "recomendacion": {
    "titulo": "Etiopía Sidamo",
    "descripcion": "Notas suaves, cítricas y de jazmín...",
    "precio": 4.50,
    "origen": "Etiopía"
  }
}
```

#### Horarios
```
GET /api/horarios
```
Obtiene información de horarios.

**Respuesta:**
```json
{
  "caffeteria": "Cafetería Selecto Granos",
  "horarios": {
    "lunes_viernes": "7:00 AM - 8:00 PM",
    "sabado": "8:00 AM - 9:00 PM",
    "domingo": "Cerrado"
  },
  "telefono": "+1-555-CAFÉ",
  "ubicacion": "The Curated Ritual District"
}
```

---

## 🚀 Uso Desde JavaScript

### Importar helpers
```javascript
// Los scripts se cargan automáticamente en chat.html y mobile-chat.html
// window.api - APIHelper instance
// window.dataManager - DataManager instance
// window.eventDispatcher - EventDispatcher instance
```

### Ejemplos

#### Obtener menú
```javascript
const menu = await window.api.getMenu();
console.log(menu.items);
```

#### Obtener recomendación
```javascript
const rec = await window.api.getRecommendations('dulce');
console.log(rec.recomendacion);
```

#### Obtener horarios
```javascript
const hours = await window.api.getHours();
console.log(hours.horarios);
```

#### Suscribirse a eventos
```javascript
window.eventDispatcher.on('message-received', (data) => {
  console.log('Nuevos tickets:', data.tokens_usados);
});

window.eventDispatcher.on('provider-changed', (event) => {
  console.log('Provider cambiado a:', event.provider);
});
```

#### Guardar/Cargar datos
```javascript
// Guardar preferencias
window.dataManager.savePreferences({ provider: 'openai' });

// Cargar preferencias
const prefs = window.dataManager.loadPreferences();
console.log(prefs.provider);

// Guardar/Cargar historial de chat
window.dataManager.saveChatHistory(messages);
const history = window.dataManager.loadChatHistory();
```

---

## 🔧 Configuración

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# Google Gemini
GOOGLE_API_KEY=tu_api_key

# OpenAI
OPENAI_API_KEY=tu_api_key

# Anthropic Claude
ANTHROPIC_API_KEY=tu_api_key

# DeepSeek
DEEPSEEK_API_KEY=tu_api_key
```

---

## 📱 Rutas por Dispositivo

| Dispositivo | URL | Descripción |
|------------|-----|-------------|
| Desktop | `/chat` | Chat optimizado para escritorio (2560x2048px) |
| Mobile | `/mobile/chat` | Chat optimizado para móvil (780x1768px) |
| Cualquiera | `/stitch-ui/landing` | Landing page responsivo |
| Cualquiera | `/stitch-ui` | Portal de navegación |

---

## 🎨 Paleta de Diseño

**Colores (Material Design 3):**
- Primario: `#6f4627` (Marrón café)
- Secundario: `#566250` (Verde grisáceo)
- Terciario: `#634a3e` (Marrón oscuro)
- Background: `#fff8f0` (Beige claro)

**Tipografía:**
- Títulos: Noto Serif
- Cuerpo: Manrope
- Etiquetas: Manrope

---

## 📊 Estructura de Datos

### ChatRequest
```python
{
  "pregunta": str,           # La pregunta/mensaje del usuario
  "provider": AIProvider,    # Proveedor de IA (gemini, openai, claude, deepseek)
  "historial": List[Message] # Historial de conversación
}
```

### ChatResponse
```python
{
  "respuesta": str,          # Respuesta del asistente
  "provider": AIProvider,    # Proveedor que procesó la pregunta
  "tokens_usados": int|None  # Tokens consumidos (si aplica)
}
```

### Message
```python
{
  "role": str,      # "user" o "assistant"
  "content": str    # Contenido del mensaje
}
```

---

## ✨ Características

✅ Multi-provider IA  
✅ Historial persistente  
✅ Almacenamiento local  
✅ Sistema de eventos  
✅ Manejo de errores  
✅ Formateo de respuestas  
✅ Responsive design  
✅ Chat persistente entre sesiones  
✅ Sugerencias dinámicas  
✅ Indicadores de carga  

---

## 🐛 Troubleshooting

### El chat no se carga
1. Verifica que el servidor esté corriendo: `http://localhost:8000/health`
2. Revisa la consola del navegador (F12 > Console)
3. Verifica que los scripts estén siendo cargados

### No se guardan mensajes
1. Asegúrate que localStorage esté habilitado
2. Verifica espacio disponible en el navegador
3. Prueba en otra pestaña o navegador

### Error "No se pudo obtener respuesta del servidor"
1. Verifica que el servidor esté corriendo
2. Revisa que tengas las variables de entorno configuradas
3. Verifica los logs del servidor
