"""
Hooks de validación y auditoría para el ciclo ReAct.
Cada invocación de tool pasa por PreToolUseHook (validación)
y PostToolUseHook (auditoría) para garantizar seguridad y trazabilidad.
"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


# Lista de tools destructivas que no deben permitirse
DESTRUCTIVE_TOOLS = {
    "delete_beverage",
    "delete_menu",
    "delete_user",
    "drop_database",
    "reset_system",
}

# Lista de tools permitidas (whitelist) para cafetería
ALLOWED_TOOLS = {
    "buscar_bebida",
    "listar_menu",
    "obtener_recomendacion",
    "buscar_combo",
    "listar_bebidas",
    "obtener_precio",
    "obtener_promociones",
    "search_item",
}


class PreToolUseHook:
    """
    Hook ejecutado ANTES de invocar una tool.
    Valida intención, bloquea tools destructivas, loggea operación.
    """

    @staticmethod
    def validate(tool_name: str, args: Dict[str, Any]) -> bool:
        """
        Valida si la tool puede ejecutarse.

        Args:
            tool_name: Nombre de la tool a ejecutar
            args: Argumentos de la tool

        Returns:
            True si la tool es segura, False en caso contrario
        """
        # Bloquear tools destructivas
        if tool_name in DESTRUCTIVE_TOOLS:
            logger.warning(
                f"[PreToolUse] Tool destructiva bloqueada: {tool_name}",
                extra={"timestamp": datetime.utcnow().isoformat()},
            )
            return False

        # Log de intención (auditoría)
        logger.info(
            f"[PreToolUse] Ejecutando tool: {tool_name} con args: {args}",
            extra={"timestamp": datetime.utcnow().isoformat()},
        )

        return True

    @staticmethod
    def log_intent(tool_name: str, args: Dict[str, Any], question: str) -> None:
        """
        Registra la intención del usuario antes de ejecutar la tool.

        Args:
            tool_name: Nombre de la tool
            args: Argumentos de la tool
            question: Pregunta original del usuario
        """
        logger.info(
            f"[Intent] Usuario preguntó '{question}' -> "
            f"Tool '{tool_name}' con {len(args)} parámetros",
            extra={"timestamp": datetime.utcnow().isoformat()},
        )


class PostToolUseHook:
    """
    Hook ejecutado DESPUÉS de invocar una tool.
    Audit resultado, detecta anomalías, valida respuesta.
    """

    @staticmethod
    def audit(tool_name: str, result: str, execution_time_ms: float) -> str:
        """
        Audita el resultado de la tool.

        Args:
            tool_name: Nombre de la tool ejecutada
            result: Resultado de la tool (generalmente JSON o string)
            execution_time_ms: Tiempo de ejecución en milisegundos

        Returns:
            El resultado (puede ser modificado si es necesario)
        """
        # Detectar anomalías
        if not result or result.strip() == "":
            logger.warning(
                f"[PostToolUse] Tool '{tool_name}' retornó resultado vacío",
                extra={"timestamp": datetime.utcnow().isoformat()},
            )

        if execution_time_ms > 5000:  # > 5 segundos
            logger.warning(
                f"[PostToolUse] Tool '{tool_name}' tardó {execution_time_ms}ms "
                f"(considerar timeout)",
                extra={"timestamp": datetime.utcnow().isoformat()},
            )

        # Log de auditoría estándar
        logger.info(
            f"[PostToolUse] Tool '{tool_name}' completada en {execution_time_ms}ms "
            f"con resultado de {len(str(result))} caracteres",
            extra={"timestamp": datetime.utcnow().isoformat()},
        )

        return result

    @staticmethod
    def detect_anomalies(tool_name: str, result: str) -> Optional[str]:
        """
        Detección simple de anomalías en la respuesta.

        Args:
            tool_name: Nombre de la tool
            result: Resultado de la tool

        Returns:
            None si no hay anomalías, mensaje de alerta si las hay
        """
        # Detectar respuestas sospechosas
        if "error" in result.lower() and len(result) < 50:
            anomaly = (
                f"Posible error en tool '{tool_name}': "
                f"respuesta corta con palabra 'error'"
            )
            logger.error(
                f"[Anomaly] {anomaly}",
                extra={"timestamp": datetime.utcnow().isoformat()},
            )
            return anomaly

        # Detectar respuestas vacías o muy cortas
        if len(result.strip()) < 5:
            logger.warning(
                f"[Anomaly] Tool '{tool_name}' retornó respuesta muy corta",
                extra={"timestamp": datetime.utcnow().isoformat()},
            )

        return None
