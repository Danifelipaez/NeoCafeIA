from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from ..domain.schemas import AIProvider, Message


class IModelAdapter(ABC):
    @abstractmethod
    def complete(self, system_prompt: str, user_message: str, history: Optional[List[Message]] = None) -> Tuple[str, Optional[int]]:
        pass


class AIModelFactory:
    @staticmethod
    def create(provider: AIProvider) -> IModelAdapter:
        from .gemini_adapter import GeminiAdapter
        from .openai_adapter import OpenAIAdapter
        from .claude_adapter import ClaudeAdapter
        from .deepseek_adapter import DeepSeekAdapter
        from .langchain_adapter import LangChainAdapter
        from .react_adapter import ReactAdapter

        adapters = {
            AIProvider.GEMINI: GeminiAdapter,
            AIProvider.OPENAI: OpenAIAdapter,
            AIProvider.CLAUDE: ClaudeAdapter,
            AIProvider.DEEPSEEK: DeepSeekAdapter,
            AIProvider.LANGCHAIN: LangChainAdapter,
            AIProvider.REACT: ReactAdapter,
        }

        adapter_class = adapters.get(provider)
        if not adapter_class:
            raise ValueError(f"Proveedor de IA no soportado: {provider}")
        return adapter_class()