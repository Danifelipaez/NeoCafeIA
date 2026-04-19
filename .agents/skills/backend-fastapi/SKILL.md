---
name: backend-fastapi
version: 1.0.0
description: Skill específico de NeoCafeIA / Selecto Granos para documentar su backend FastAPI con Clean Architecture, Factory Pattern e IModelAdapter.
compatibility:
  python: "3.9+"
  fastapi: "0.115.0"
  fastmcp: "3.2.3"
---

# Backend FastAPI de NeoCafeIA para Selecto Granos

Este skill describe la arquitectura real del backend de Selecto Granos. El backend de NeoCafeIA actúa como un asistente conversacional para cafetería specialty, con foco en menú, recomendaciones, precios, contexto de negocio y herramientas MCP para consultas estructuradas.

La arquitectura combina Clean Architecture simplificada, Factory Pattern e interfaz `IModelAdapter` para desacoplar proveedores de IA. El dominio vive en esquemas Pydantic, la lógica de negocio en servicios, y la integración con modelos o herramientas externas queda en infraestructura.

## Arquitectura Semántica

- El backend responde preguntas de clientes sobre café specialty, bebidas, postres, combos, promociones y granos.
- El conocimiento no se codifica en prompts fijos: se carga desde archivos Markdown del directorio `knowledge/` y de los prompts/reglas del sistema.
- La respuesta puede venir de un proveedor de IA, de la lógica de negocio del menú o del ciclo ReAct, según el proveedor seleccionado.
- El diseño prioriza trazabilidad: cada capa tiene una responsabilidad clara y los adaptadores aíslan el proveedor concreto.

## Estructura Específica del Proyecto

### `src/domain/schemas.py`
Define los contratos de dominio y los modelos de intercambio del chat.

- `AIProvider`: enum con `gemini`, `openai`, `claude`, `deepseek`, `langchain` y `react`.
- `Message`: estructura de historial con `role` y `content`.
- `ChatRequest`: entrada principal del chat con `pregunta`, `provider` e `historial`.
- `ChatResponse`: salida del chat con `respuesta`, `provider` y `tokens_usados`.

Este módulo es la frontera de datos entre API, servicios e infraestructura.

### `src/services/chat_service.py`
Contiene la lógica de negocio del chat.

- Decide cuándo responder con lógica propia y cuándo delegar en un adaptador de IA.
- Extrae precios desde `knowledge/menu.md` para resolver consultas de precio sin llamar al modelo.
- Normaliza preguntas, busca el último contexto relevante y mantiene coherencia con recomendaciones previas.
- Ajusta respuestas para que las recomendaciones de combos conserven el precio final visible.

En Selecto Granos, este servicio es la capa que protege la experiencia comercial: precio, catálogo y seguimiento de conversación.

### `src/infrastructure/model_factory.py`
Implementa el contrato de integración con modelos.

- `IModelAdapter`: ABC que obliga a exponer `complete(system_prompt, user_message, history)`.
- `AIModelFactory`: selecciona el adaptador correcto según `AIProvider`.
- La factory importa los adaptadores concretos bajo demanda para evitar acoplamiento innecesario.

Aquí viven los puntos de extensión para Gemini, OpenAI, Claude, DeepSeek, LangChain y ReAct.

### `src/infrastructure/context_loader.py`
Carga el contexto de negocio desde Markdown.

- `load_system_prompt()` lee `system_prompt/asistente.md`.
- `load_rules()` lee `rules/comportamiento.md`.
- `load_knowledge_files()` recorre `knowledge/*.md` y concatena su contenido.
- `load_full_context()` unifica prompt, reglas y conocimiento en un solo contexto.

La base de conocimiento de Selecto Granos debe mantenerse en Markdown para conservar trazabilidad y edición no técnica.

### `src/infrastructure/react_adapter.py` y `src/services/react_agent.py`
Implementan el ciclo ReAct para razonamiento con herramientas.

- `ReactAdapter` adapta el ciclo ReAct al contrato `IModelAdapter`.
- `ReActAgent` ejecuta las fases de razonamiento, acción, observación y reflexión.
- `MockToolInvoker` simula tools mientras no exista conexión MCP real.
- Los hooks de seguridad validan y auditan la ejecución de tools.

Este camino se usa cuando la interacción requiere decidir herramientas antes de responder, no solo completar texto.

### `servidor_mcp.py`
Expone las tools MCP disponibles para Selecto Granos.

Tools actuales:

- `buscar_bebida(nombre)`
- `listar_menu()`
- `obtener_recomendacion(preferencia)`
- `consultar_granos_disponibles()`
- `verificar_promocion_activa()`

El servidor se crea con `FastMCP("NeoCafeIA")` y usa decoradores `@mcp.tool()` para registrar funciones.

## Cómo Agregar un Nuevo Proveedor de IA

Sigue estos pasos cuando quieras incorporar otro proveedor manteniendo la arquitectura:

1. Crea un adaptador nuevo en `src/infrastructure/`, por ejemplo `mistral_adapter.py`.
2. Haz que la clase implemente `IModelAdapter` y su método `complete()`.
3. Añade el proveedor al enum `AIProvider` en `src/domain/schemas.py`.
4. Registra el nuevo adaptador en `AIModelFactory.create()`.
5. Si el proveedor necesita contexto o configuración especial, encapsúlala dentro del adaptador, no en `chat_service.py`.

Ejemplo mínimo:

```python
# src/infrastructure/mistral_adapter.py
from typing import List, Optional, Tuple
from src.domain.schemas import Message
from src.infrastructure.model_factory import IModelAdapter


class MistralAdapter(IModelAdapter):
    def complete(
        self,
        system_prompt: str,
        user_message: str,
        history: Optional[List[Message]] = None,
    ) -> Tuple[str, Optional[int]]:
        prompt = f"{system_prompt}\n\nUsuario: {user_message}"
        return "Respuesta de Mistral", 0
```

```python
# src/domain/schemas.py
class AIProvider(str, Enum):
    MISTRAL = "mistral"
```

```python
# src/infrastructure/model_factory.py
from .mistral_adapter import MistralAdapter

adapters = {
    AIProvider.MISTRAL: MistralAdapter,
    # ... resto de proveedores
}
```

Regla práctica: la factory decide qué clase instanciar; el adaptador decide cómo hablar con el proveedor.

## Cómo Agregar una Nueva Tool al Servidor MCP

Para extender `servidor_mcp.py` con una tool nueva:

1. Define una función Python clara y tipada.
2. Decórala con `@mcp.tool()`.
3. Devuelve texto o JSON serializable, porque los clientes MCP consumen el resultado como payload de tool.
4. Mantén la función orientada al dominio de Selecto Granos: bebidas, granos, promociones, stock o catálogo.
5. Si la tool será usada por ReAct, añade una ruta de simulación en `MockToolInvoker` mientras no exista integración real.

Ejemplo:

```python
from fastmcp import FastMCP

mcp = FastMCP("NeoCafeIA")


@mcp.tool()
def consultar_origen_grano(nombre: str) -> str:
    granos = {
        "colombiano": "Origen: Eje Cafetero. Perfil: balanceado, notas de chocolate y nuez.",
        "etiope": "Origen: Etiopía. Perfil: floral, afrutado, notas brillantes.",
    }
    return granos.get(nombre.lower(), "Grano no encontrado en Selecto Granos")
```

Si la nueva tool cambia la experiencia conversacional, documenta también cómo será consumida por el agente ReAct o por el chat normal.

## Referencias

- [FastAPI docs](https://fastapi.tiangolo.com/)
- [FastMCP docs](https://gofastmcp.com/)
- [README del proyecto](../../../README.md)

## Regla de Oro del Proyecto

En Selecto Granos, el backend no debe convertirse en una bolsa de prompts. La base de conocimiento vive en Markdown, la lógica de negocio vive en servicios, los proveedores viven en infraestructura y el dominio se expresa con modelos Pydantic claros.
