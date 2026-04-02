import os
from typing import List, Optional, Tuple
from openai import OpenAI
from .model_factory import IModelAdapter
from ..domain.schemas import Message


class DeepSeekAdapter(IModelAdapter):
    MODEL: str = "deepseek-chat"

    def __init__(self) -> None:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY no está configurada en las variables de entorno")
        self._client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def complete(self, system_prompt: str, user_message: str, history: Optional[List[Message]] = None) -> Tuple[str, Optional[int]]:
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})
        messages.append({"role": "user", "content": user_message})

        try:
            response = self._client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                max_tokens=800,
                temperature=0.3
            )
            return response.choices[0].message.content or "", response.usage.total_tokens if response.usage else None
        except Exception as e:
            raise RuntimeError(f"Error al generar contenido con DeepSeek: {e}")