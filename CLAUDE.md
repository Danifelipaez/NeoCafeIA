# CLAUDE.md

## Contexto del proyecto
NeoCafeIA es un asistente de IA para cafeterías con backend en FastAPI y una arquitectura modular separada por dominio, servicios e infraestructura.

## Stack tecnológico
- FastAPI para la API HTTP y el backend principal.
- Pydantic v2 para validación y esquemas.
- LangChain para el flujo de razonamiento y composición de contexto.
- FastMCP para el servidor MCP y sus tools.
- Tailwind CSS para el frontend.
- Next.js como objetivo de migración del frontend.

## Arquitectura del repositorio
- El patrón Factory vive en `src/infrastructure/model_factory.py`.
- Toda integración con modelos o proveedores de IA debe ir en `src/infrastructure/`.
- Los contratos de dominio viven en `src/domain/schemas.py`.
- La lógica de negocio y orquestación vive en `src/services/`.
- La carga de contexto y conocimiento debe delegarse a `src/infrastructure/context_loader.py`.
- La API de entrada actual se expone desde `api/index.py` y `app.py`.

## Convenciones de trabajo
- Mantener la lógica de proveedor desacoplada mediante adaptadores.
- Preferir cambios pequeños y localizados sobre refactors amplios.
- Conservar nombres descriptivos y consistentes con el dominio cafetero.
- Los modelos, servicios y adaptadores deben seguir una estructura explícita y fácil de rastrear.

## Rutas protegidas
No escribir directamente en estas rutas salvo necesidad explícita del proyecto:
- `knowledge/`
- `system_prompt/`
- `.env`

## Reglas de nombres
- Archivos Python: `snake_case.py`.
- Clases: `PascalCase`.
- Funciones, métodos y variables: `snake_case`.
- Enum y constantes compartidas: nombres claros y estables.

## Notas operativas
- El contenido de negocio debe venir de los archivos Markdown existentes, no de texto hardcodeado en el prompt.
- Si aparece un nuevo proveedor de IA, añadir su adaptador en `src/infrastructure/` y registrarlo en la factory.
- Evitar escribir documentación o prompts generados dentro de las carpetas de conocimiento sin revisión.