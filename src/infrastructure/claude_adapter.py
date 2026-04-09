import os
from typing import List, Optional, Tuple
from anthropic import Anthropic
from .model_factory import IModelAdapter
from .retry_handler import RetryConfig, call_with_retry
from ..domain.schemas import Message


class ClaudeAdapter(IModelAdapter):
    MODEL: str = "claude-3-5-sonnet-20241022"

    def __init__(self) -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no está configurada en las variables de entorno")
        self._client = Anthropic(api_key=api_key)

    def _normalize_role(self, role: str) -> str:
        """Normalize roles to Anthropic format (lowercase).
        Anthropic expects: 'user' and 'assistant'
        """
        role_lower = role.lower()
        if role_lower in ['bot']:
            return 'assistant'
        return role_lower

    def complete(self, system_prompt: str, user_message: str, history: Optional[List[Message]] = None) -> Tuple[str, Optional[int]]:
        messages = []
        if history:
            for msg in history:
                messages.append({"role": self._normalize_role(msg.role), "content": msg.content})
        messages.append({"role": "user", "content": user_message})

        def _make_request():
            response = self._client.messages.create(
                model=self.MODEL,
                system=system_prompt,
                messages=messages,
                max_tokens=800,
                temperature=0.3
            )
            return response.content[0].text, response.usage.input_tokens + response.usage.output_tokens if response.usage else None

        try:
            return call_with_retry(_make_request, RetryConfig(max_attempts=3, initial_delay=1.0))
        except Exception as e:
            raise RuntimeError(f"Error al generar contenido con Claude: {e}")