from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional


class AIProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    DEEPSEEK = "deepseek"
    LANGCHAIN = "langchain"


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    pregunta: str = Field(..., max_length=1000, min_length=1)
    provider: AIProvider = AIProvider.GEMINI
    historial: List[Message] = []


class ChatResponse(BaseModel):
    respuesta: str
    provider: AIProvider
    tokens_usados: Optional[int] = None