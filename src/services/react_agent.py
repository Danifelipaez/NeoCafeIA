"""
ReActAgent: Ciclo ReAct (Reasoning + Acting) para agente inteligente de cafetería.

El ciclo completo es:
1. Razonar: Analizar la pregunta y decidir qué tool usar
2. Actuar: Invocar la tool (con validación de hooks)
3. Observar: Recibir el resultado
4. Reflexionar: Decidir si el resultado es suficiente o continuar
5. Responder: Retornar la respuesta final
"""

import logging
import json
import time
from typing import List, Optional, Tuple, Dict, Any
from abc import ABC, abstractmethod

from src.domain.schemas import Message, AIProvider
from src.infrastructure.hooks import PreToolUseHook, PostToolUseHook
from src.infrastructure.context_loader import ContextLoader


logger = logging.getLogger(__name__)


class ToolInvoker(ABC):
    """
    Interfaz abstracta para un invoker de tools.
    Permite inyectar diferentes implementaciones (MCP real, mock, etc.).
    """

    @abstractmethod
    def invoke(self, tool_name: str, **kwargs) -> str:
        """
        Invoca una tool con los argumentos dados.

        Args:
            tool_name: Nombre de la tool
            **kwargs: Argumentos de la tool

        Returns:
            Resultado de la tool como string
        """
        pass

    @abstractmethod
    def list_tools(self) -> List[str]:
        """Lista las tools disponibles."""
        pass


class MockToolInvoker(ToolInvoker):
    """
    Mock de ToolInvoker para desarrollo y testing.
    Simula respuestas de tools sin conexión real a MCP.
    """

    def invoke(self, tool_name: str, **kwargs) -> str:
        """Simula invocación de herramientas."""
        if tool_name == "buscar_bebida":
            return json.dumps(
                {
                    "bebida": kwargs.get("nombre", "Cappuccino"),
                    "descripcion": "Café con leche espumada",
                    "precio": 4.50,
                }
            )
        elif tool_name == "listar_menu":
            return json.dumps(
                {
                    "bebidas": ["Cappuccino", "Americano", "Latte"],
                    "combos": ["Combo Mañana", "Combo Tarde"],
                }
            )
        elif tool_name == "obtener_recomendacion":
            return json.dumps(
                {
                    "recomendacion": "Te recomiendo nuestro Cappuccino",
                    "razon": "Es nuestra bebida más popular",
                }
            )
        else:
            return json.dumps({"error": f"Tool '{tool_name}' no simulada"})

    def list_tools(self) -> List[str]:
        return [
            "buscar_bebida",
            "listar_menu",
            "obtener_recomendacion",
            "buscar_combo",
        ]


class ReActAgent:
    """
    Agente ReAct para cafetería.

    Ciclo:
    1. Razonar: ¿Qué herramienta necesito?
    2. Actuar: Ejecutar la herramienta (con hooks de validación)
    3. Observar: Recibir resultado
    4. Reflexionar: ¿Es suficiente o debo continuar?
    5. Responder: Retornar respuesta al usuario
    """

    def __init__(
        self,
        system_prompt: str,
        tool_invoker: Optional[ToolInvoker] = None,
        max_iterations: int = 3,
    ):
        """
        Inicializa el ReActAgent.

        Args:
            system_prompt: Prompt del sistema que guía el razonamiento
            tool_invoker: Implementación de ToolInvoker (default: MockToolInvoker)
            max_iterations: Máximo número de iteraciones del ciclo
        """
        self.system_prompt = system_prompt
        self.tool_invoker = tool_invoker or MockToolInvoker()
        self.max_iterations = max_iterations
        self.thought_history: List[str] = []
        self.action_history: List[Dict[str, Any]] = []

    def run(self, question: str, history: Optional[List[Message]] = None) -> str:
        """
        Ejecuta el ciclo ReAct completo.

        Args:
            question: Pregunta del usuario
            history: Historial de conversación anterior

        Returns:
            Respuesta final del agente
        """
        logger.info(f"[ReAct Start] Pregunta: {question}")

        history = history or []
        self.thought_history = []
        self.action_history = []

        # Fase 1: Razonar (Reasoning)
        thought = self._reason(question, history)
        self.thought_history.append(thought)
        logger.info(f"[ReAct Thought] {thought[:100]}...")

        # Ciclo: Actuar -> Observar -> Reflexionar
        for iteration in range(self.max_iterations):
            logger.info(f"[ReAct Iteration] {iteration + 1}/{self.max_iterations}")

            # Fase 2: Decidir acción (Decide Action)
            action, action_input = self._plan(thought)
            logger.info(f"[ReAct Action] {action} con input: {action_input}")

            # Si la acción es respuesta final, terminar
            if action == "final_answer":
                logger.info("[ReAct Final] Respondiendo directamente")
                return action_input

            # Fase 3: Actuar (Act) — invocar tool con hooks
            observation = self._act(action, action_input)
            logger.info(f"[ReAct Observation] {observation[:200]}...")

            # Fase 4: Reflexionar (Reflect)
            is_sufficient = self._is_sufficient(observation, thought)
            if is_sufficient:
                logger.info("[ReAct Reflect] Resultado suficiente, terminando")
                return self._format_answer(observation)

            # Reflexionar y actualizar pensamiento
            thought = self._reflect(thought, action, observation)
            self.thought_history.append(thought)
            logger.info(f"[ReAct Thought Update] {thought[:100]}...")

        # Si agotamos iteraciones, retornar la mejor respuesta con lo que tenemos
        logger.warning(
            "[ReAct Max Iterations] Agotadas iteraciones, retornando respuesta parcial"
        )
        return self._force_answer(thought)

    def _reason(self, question: str, history: List[Message]) -> str:
        """
        Fase 1: Razonar sobre la pregunta.
        Analiza qué información se necesita.

        Returns:
            Pensamiento inicial (string descriptivo)
        """
        context_str = "\n".join(
            [f"- {msg.role}: {msg.content[:100]}" for msg in history[-3:]]
        )
        thought = (
            f"Pregunta: {question}\n"
            f"Contexto previo:\n{context_str}\n"
            f"Tools disponibles: {', '.join(self.tool_invoker.list_tools())}\n"
            f"Debo elegir la mejor herramienta para responder."
        )
        return thought

    def _plan(self, thought: str) -> Tuple[str, str]:
        """
        Fase 2: Planificar qué acción tomar (mimics LLM decision).

        Returns:
            Tupla (action_name, action_input)
        """
        # Lógica simple de routing: si la pregunta menciona cierta palabra, usar cierta tool
        # En una versión real, esto sería llamada a LLM para decidir inteligentemente
        thought_lower = thought.lower()

        if "precio" in thought_lower or "cuesta" in thought_lower:
            return ("buscar_bebida", "precio")
        elif "menu" in thought_lower or "qué tienen" in thought_lower:
            return ("listar_menu", "")
        elif (
            "recomiend" in thought_lower
            or "suger" in thought_lower
            or "recomend" in thought_lower
        ):
            return ("obtener_recomendacion", "")
        elif "combo" in thought_lower:
            return ("buscar_combo", "combo")
        else:
            # Acción por defecto: buscar en el menú
            return ("listar_menu", "")

    def _act(self, action: str, action_input: str) -> str:
        """
        Fase 3: Actuar — ejecutar la tool con validación de hooks.

        Args:
            action: Nombre del action (tool)
            action_input: Entrada para la tool

        Returns:
            Resultado de la tool
        """
        # Hook PreToolUse: Validar
        is_valid = PreToolUseHook.validate(action, {"input": action_input})
        if not is_valid:
            logger.error(f"[ReAct Act] Tool bloqueada: {action}")
            return json.dumps(
                {
                    "error": f"Tool '{action}' no permitida por política de seguridad"
                }
            )

        # Registrar intención
        PreToolUseHook.log_intent(action, {"input": action_input}, "")

        # Invocar tool y medir tiempo
        start_time = time.time()
        try:
            result = self.tool_invoker.invoke(action, query=action_input)
        except Exception as e:
            logger.error(f"[ReAct Act] Error invocando tool: {e}")
            result = json.dumps({"error": str(e)})

        execution_time_ms = (time.time() - start_time) * 1000

        # Hook PostToolUse: Auditar
        result = PostToolUseHook.audit(action, result, execution_time_ms)

        # Detectar anomalías
        anomaly = PostToolUseHook.detect_anomalies(action, result)
        if anomaly:
            logger.warning(f"[ReAct Anomaly] {anomaly}")

        # Registrar acción
        self.action_history.append(
            {
                "action": action,
                "input": action_input,
                "result": result[:200],
                "execution_ms": execution_time_ms,
            }
        )

        return result

    def _is_sufficient(self, observation: str, thought: str) -> bool:
        """
        Fase 4a: Decide si la observación es suficiente para responder.

        Returns:
            True si la observación es satisfactoria, False si hay que continuar
        """
        # Heurísticas simples
        obs_lower = observation.lower()

        # Si hay error, no es suficiente
        if "error" in obs_lower:
            return False

        # Si la respuesta es muy corta, podría no ser suficiente
        if len(observation.strip()) < 10:
            return False

        # Si contiene información útil (datos JSON con contenido), es suficiente
        if "precio" in obs_lower or "bebida" in obs_lower or "menu" in obs_lower:
            return True

        return True  # Por defecto, aceptar si no es error

    def _reflect(self, thought: str, action: str, observation: str) -> str:
        """
        Fase 4b: Reflexionar sobre la acción y actualizar pensamiento.

        Returns:
            Pensamiento actualizado
        """
        updated_thought = (
            f"{thought}\n\n"
            f"Ejecuté: {action}\n"
            f"Resultado: {observation[:150]}...\n"
            f"Reflexión: El resultado proporciona información sobre "
            f"la pregunta original. Puedo usarlo para formar una respuesta."
        )
        return updated_thought

    def _format_answer(self, observation: str) -> str:
        """
        Fase 5: Formatear la respuesta final a partir de la observación.

        Returns:
            Respuesta formateada para el usuario
        """
        try:
            data = json.loads(observation)
            if isinstance(data, dict):
                if "error" in data:
                    return f"Disculpa, no pude obtener esa información: {data['error']}"
                # Construir respuesta a partir de los datos
                parts = []
                for key, value in data.items():
                    if isinstance(value, (str, int, float)):
                        parts.append(f"{key}: {value}")
                return "; ".join(parts)
            else:
                return str(data)
        except json.JSONDecodeError:
            return observation

    def _force_answer(self, thought: str) -> str:
        """
        Retorna una respuesta cuando se agotan las iteraciones.

        Returns:
            Respuesta basada en el pensamiento acumulado
        """
        if self.action_history:
            last_result = self.action_history[-1]["result"]
            return self._format_answer(last_result)
        return "Disculpa, no pude obtener la información que solicitaste. Por favor, intenta con otra pregunta."
