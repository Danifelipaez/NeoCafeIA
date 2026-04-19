"""
ReactAdapter: Adaptador que implementa IModelAdapter usando el ciclo ReAct.

Integra el ReActAgent con el sistema de adaptadores existente.
"""

from typing import List, Optional, Tuple
import logging
import os

from src.domain.schemas import Message
from src.infrastructure.model_factory import IModelAdapter
from src.infrastructure.mcp_client import MCPClient
from src.services.react_agent import ReActAgent, MockToolInvoker


logger = logging.getLogger(__name__)


class ReactAdapter(IModelAdapter):
    """
    Adaptador que implementa el interface IModelAdapter usando ReActAgent.

    ReAct: Reasoning + Acting ciclo para responder preguntas con herramientas.
    """

    def __init__(self, max_iterations: int = 3):
        """
        Inicializa el ReactAdapter.

        Args:
            max_iterations: Máximo número de iteraciones en el ciclo ReAct
        """
        self.max_iterations = max_iterations

        mcp_url = os.getenv("MCP_URL", "").strip()
        if mcp_url:
            self.tool_invoker = MCPClient(base_url=mcp_url)
            logger.info(
                "[ReactAdapter] MCPClient activo con URL pública: %s",
                mcp_url,
            )
        else:
            self.tool_invoker = MockToolInvoker()
            logger.info("[ReactAdapter] MCP_URL no configurado, usando mock")

        logger.info(
            f"[ReactAdapter] Inicializado con {max_iterations} iteraciones máximas"
        )

    def complete(
        self,
        system_prompt: str,
        user_message: str,
        history: Optional[List[Message]] = None,
    ) -> Tuple[str, Optional[int]]:
        """
        Completa una pregunta usando el ciclo ReAct.

        Args:
            system_prompt: Instrucciones del sistema
            user_message: Pregunta del usuario
            history: Historial de conversación anterior

        Returns:
            Tupla (respuesta, tokens_usados)
            Nota: tokens_usados es None porque ReAct no usa tokens del LLM
        """
        try:
            # Crear agente ReAct
            agent = ReActAgent(
                system_prompt=system_prompt,
                tool_invoker=self.tool_invoker,
                max_iterations=self.max_iterations,
            )

            # Ejecutar ciclo ReAct
            respuesta = agent.run(user_message, history=history or [])

            logger.info(f"[ReactAdapter] Respuesta generada: {respuesta[:100]}...")

            # Retornar respuesta sin conteo de tokens (ReAct no usa LLM de forma directa)
            return respuesta, None

        except Exception as e:
            logger.error(f"[ReactAdapter] Error durante ciclo ReAct: {e}")
            return f"Disculpa, ocurrió un error: {str(e)}", None
