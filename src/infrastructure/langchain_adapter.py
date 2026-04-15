import os
import logging
from typing import List, Optional, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .model_factory import IModelAdapter
from .retry_handler import RetryConfig, call_with_retry
from ..domain.schemas import Message


logger = logging.getLogger(__name__)


class LangChainAdapter(IModelAdapter):
    """Adaptador LangChain que implementa LCEL (LangChain Expression Language).
    
    El flujo LCEL usa el operador | (pipe) para composición explícita:
    chain = prompt | llm | output_parser
    """

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
        self._llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=api_key)
        logger.info("[LangChainAdapter] Inicializado con Gemini 2.0 Flash Exp")

    def _build_lcel_chain(self, system_prompt: str):
        """Construye la cadena LCEL explícita.
        
        Flujo:
        1. prompt: ChatPromptTemplate con system + human
        2. llm: ChatGoogleGenerativeAI
        3. output_parser: StrOutputParser
        
        Uso del operador |:
        chain = prompt | llm | output_parser
        """
        # Paso 1: Definir el prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        # Paso 2: Definir el output parser
        output_parser = StrOutputParser()
        
        # Paso 3: Componer la cadena con LCEL (mediante operador |)
        # Esta es la forma explícita que muestra claramente el flujo
        chain = prompt | self._llm | output_parser
        
        logger.debug("[LangChainAdapter] LCEL chain construída: prompt | llm | output_parser")
        
        return chain

    def complete(self, system_prompt: str, user_message: str, history: Optional[List[Message]] = None) -> Tuple[str, Optional[int]]:
        """Completa un usuario mensaje usando la cadena LCEL.
        
        Args:
            system_prompt: Instrucciones del sistema
            user_message: Mensaje del usuario
            history: Historial anterior (no usado en este flujo simple)
            
        Returns:
            Tupla (respuesta, tokens_usados)
        """
        # Construir la cadena LCEL
        chain = self._build_lcel_chain(system_prompt)
        
        def _make_request():
            """Ejecuta la cadena LCEL."""
            logger.info(f"[LangChainAdapter] Ejecutando LCEL chain con input: {user_message[:50]}...")
            response = chain.invoke({"input": user_message})
            logger.info(f"[LangChainAdapter] Respuesta recibida: {len(response)} caracteres")
            return response, None  # LangChain no proporciona fácilmente token count

        try:
            return call_with_retry(_make_request, RetryConfig(max_attempts=3, initial_delay=1.0))
        except Exception as e:
            logger.error(f"[LangChainAdapter] Error durante LCEL execution: {e}")
            raise RuntimeError(f"Error al generar contenido con LangChain LCEL: {e}")