import os
from typing import List, Optional, Tuple
from google import genai
from google.genai import types
from .model_factory import IModelAdapter
from .retry_handler import RetryConfig, call_with_retry
from ..domain.schemas import Message


class GeminiAdapter(IModelAdapter):
    MODEL: str = "models/gemini-2.5-flash"

    def __init__(self) -> None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY no está configurada en las variables de entorno")
        self._client = genai.Client(api_key=api_key)

    def _normalize_role_for_gemini(self, role: str) -> str:
        """Convert generic roles to Gemini-specific roles.
        Gemini expects: 'user' -> 'USER', 'assistant' -> 'MODEL'
        """
        role_lower = role.lower()
        if role_lower in ['user']:
            return 'USER'
        elif role_lower in ['assistant', 'bot']:
            return 'MODEL'
        return role

    def complete(self, system_prompt: str, user_message: str, history: Optional[List[Message]] = None) -> Tuple[str, Optional[int]]:
        contents = []
        if history:
            for msg in history:
                contents.append(
                    types.Content(
                        role=self._normalize_role_for_gemini(msg.role),
                        parts=[types.Part.from_text(text=msg.content)]
                    )
                )
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            )
        )

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=800,
            temperature=0.3
        )

        def _make_request():
            response = self._client.models.generate_content(
                model=self.MODEL,
                contents=contents,
                config=config,
            )
            return response.text or "", None

        try:
            return call_with_retry(_make_request, RetryConfig(max_attempts=3, initial_delay=1.0))
        except Exception as e:
            raise RuntimeError(f"Error al generar contenido con Gemini: {e}")