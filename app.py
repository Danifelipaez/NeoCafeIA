from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
import logging
from pathlib import Path
from dotenv import load_dotenv
from src.domain.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.infrastructure.context_loader import ContextLoader

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar contexto al iniciar
try:
    context = ContextLoader.load_full_context()
    chat_service = ChatService(context)
except Exception as e:
    logger.error(f"Error al cargar contexto: {e}")
    raise

app = FastAPI(title="API Cafetería Selecto Granos")

# Montar archivos estáticos
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def landing():
    """Servir landing page de Stitch (nuevo frontend)"""
    html_file = Path(__file__).parent / "static" / "stitch-ui" / "landing.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Landing page no encontrada</h1>"

@app.get("/app", response_class=HTMLResponse)
def chat_ui():
    """Servir interfaz de chat desktop de Stitch (nuevo frontend)"""
    html_file = Path(__file__).parent / "static" / "stitch-ui" / "chat.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Chat interface no encontrada</h1>"

@app.get("/stitch-ui", response_class=HTMLResponse)
def stitch_portal():
    """Servir portal de Stitch UI"""
    html_file = Path(__file__).parent / "static" / "stitch-ui" / "index.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Portal no encontrado</h1>"

@app.get("/stitch-ui/landing", response_class=HTMLResponse)
def stitch_landing():
    """Servir landing page de Stitch"""
    html_file = Path(__file__).parent / "static" / "stitch-ui" / "landing.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Landing page no encontrada</h1>"

@app.get("/chat", response_class=HTMLResponse)
def stitch_chat():
    """Servir interfaz de chat desktop de Stitch"""
    html_file = Path(__file__).parent / "static" / "stitch-ui" / "chat.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Chat interface no encontrada</h1>"

@app.get("/mobile/chat", response_class=HTMLResponse)
def stitch_mobile_chat():
    """Servir interfaz de chat mobile de Stitch"""
    html_file = Path(__file__).parent / "static" / "stitch-ui" / "mobile-chat.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "<h1>Mobile chat interface no encontrada</h1>"

@app.post("/api/chat", response_model=ChatResponse)
def chat_api(request: ChatRequest):
    try:
        response = chat_service.respond(request)
        return response
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(status_code=400, detail="Datos de entrada inválidos")
    except Exception as e:
        logger.error(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# ============= NUEVOS ENDPOINTS DE API =============

@app.get("/api/info")
def get_project_info():
    """Obtener información del proyecto"""
    return {
        "nombre": "Cafetería Selecto Granos",
        "descripcion": "The Curated Ritual - Chat IA para recomendaciones de café",
        "version": "1.0",
        "providers": ["gemini", "openai", "claude", "deepseek"],
        "url_stitch": "/stitch-ui"
    }


@app.get("/api/menu")
def get_menu():
    """Obtener menú completo"""
    try:
        menu_path = Path("knowledge/menu.md")
        if menu_path.exists():
            with open(menu_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "status": "ok",
                "content": content,
                "items": chat_service.menu_prices,
                "combos": chat_service.combo_prices
            }
        return {"status": "error", "message": "Menú no encontrado", "items": {}, "combos": {}}
    except Exception as e:
        logger.error(f"Error al obtener menú: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener menú")


@app.get("/api/recommendations")
def get_recommendations(preference: str = None):
    """Obtener recomendación personalizada"""
    try:
        # Opciones válidas: suave, fuerte, cremoso, refrescante, dulce
        valid_preferences = ["suave", "fuerte", "cremoso", "refrescante", "dulce"]
        
        if preference and preference.lower() not in valid_preferences:
            return {
                "status": "error",
                "message": f"Preferencia no válida. Opciones: {', '.join(valid_preferences)}"
            }
        
        # Aquí se podría integrar lógica más compleja
        recommendations = {
            "suave": {
                "titulo": "Etiopía Sidamo",
                "descripcion": "Notas suaves, cítricas y de jazmín. Ideal para quien busca delicadeza.",
                "precio": 4.50,
                "origen": "Etiopía"
            },
            "fuerte": {
                "titulo": "Geisha Reserve",
                "descripcion": "Sabor intenso y complejo. El pináculo del café de especialidad.",
                "precio": 12.00,
                "origen": "Panamá"
            },
            "cremoso": {
                "titulo": "Flat White AI",
                "descripcion": "Textura perfecta con leche vaporizada. Ideal para quienes aman la cremosidad.",
                "precio": 5.25,
                "origen": "Blend"
            },
            "refrescante": {
                "titulo": "Cold Brew Selecto",
                "descripcion": "18 horas de infusión lenta. Perfecto para días calurosos.",
                "precio": 6.00,
                "origen": "Blend Premium"
            },
            "dulce": {
                "titulo": "V60 Especial",
                "descripcion": "Notas dulces naturales. Pureza máxima en cada filtrado.",
                "precio": 5.50,
                "origen": "Colombia"
            }
        }
        
        if preference:
            return {
                "status": "ok",
                "recomendacion": recommendations.get(preference.lower(), recommendations["suave"])
            }
        
        return {
            "status": "ok",
            "todas_recomendaciones": recommendations
        }
    except Exception as e:
        logger.error(f"Error al obtener recomendaciones: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener recomendaciones")


@app.get("/api/horarios")
def get_hours():
    """Obtener horarios de atención"""
    return {
        "caffeteria": "Cafetería Selecto Granos",
        "horarios": {
            "lunes_viernes": "7:00 AM - 8:00 PM",
            "sabado": "8:00 AM - 9:00 PM",
            "domingo": "Cerrado"
        },
        "telefono": "+1-555-CAFÉ",
        "ubicacion": "The Curated Ritual District"
    }
