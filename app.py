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
    """Servir landing page desde archivo estático"""
    html_file = Path(__file__).parent / "static" / "landing.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Error: Landing page not found</h1>
    </body>
    </html>
    """

@app.get("/app", response_class=HTMLResponse)
def chat_ui():
    """Servir interfaz de chat desde archivo estático"""
    html_file = Path(__file__).parent / "static" / "index.html"
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            return f.read()
    return """
    <!DOCTYPE html>
    <html>
    <body>
    <h1>Error: Chat UI not found</h1>
    </body>
    </html>
    """

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        response = chat_service.respond(request)
        return response
    except ValidationError as e:
        logger.error(f"Error de validación: {e}")
        raise HTTPException(status_code=400, detail="Datos de entrada inválidos")
    except Exception as e:
        logger.error(f"Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
