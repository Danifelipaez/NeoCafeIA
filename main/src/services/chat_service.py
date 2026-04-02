from main.src.domain.schemas import ChatRequest, ChatResponse, AIProvider
from main.src.infrastructure.model_factory import AIModelFactory
from main.src.infrastructure.context_loader import ContextLoader


class ChatService:
    def __init__(self, context: str):
        self._context = context

    def respond(self, request: ChatRequest) -> ChatResponse:
        adapter = AIModelFactory.create(request.provider)
        respuesta, tokens = adapter.complete(self._context, request.pregunta, request.historial)
        return ChatResponse(respuesta=respuesta, provider=request.provider, tokens_usados=tokens)