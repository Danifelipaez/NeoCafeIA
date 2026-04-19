"""
Cliente MCP HTTP para invocar tools remotas desde el ciclo ReAct.
"""

import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional

import httpx

from src.services.react_agent import ToolInvoker


logger = logging.getLogger(__name__)


class MCPClient(ToolInvoker):
    """
    Implementación de ToolInvoker contra endpoint MCP HTTP/JSON-RPC.

    Requiere MCP_URL y opcionalmente MCP_AUTH_TOKEN para endpoints protegidos.
    """

    def __init__(
        self,
        base_url: str,
        timeout_seconds: float = 10.0,
        auth_token: Optional[str] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.auth_token = auth_token or os.getenv("MCP_AUTH_TOKEN")

    def _build_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def _rpc(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": method,
            "params": params,
        }

        try:
            with httpx.Client(timeout=self.timeout_seconds) as client:
                response = client.post(
                    self.base_url,
                    headers=self._build_headers(),
                    json=payload,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code if exc.response else "N/A"
            body = exc.response.text if exc.response else ""
            raise RuntimeError(
                f"MCP devolvió status {status}: {body}"
            ) from exc
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Error de red al invocar MCP: {exc}") from exc

    def _normalize_arguments(self, tool_name: str, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        if "arguments" in kwargs and isinstance(kwargs["arguments"], dict):
            return kwargs["arguments"]

        if "query" not in kwargs:
            return kwargs

        query_value = kwargs.get("query")

        if tool_name == "buscar_bebida":
            return {"nombre": query_value}

        if tool_name == "obtener_recomendacion":
            return {"preferencia": query_value or "suave"}

        return {}

    def invoke(self, tool_name: str, **kwargs: Any) -> str:
        arguments = self._normalize_arguments(tool_name, kwargs)

        try:
            rpc_response = self._rpc(
                method="tools/call",
                params={
                    "name": tool_name,
                    "arguments": arguments,
                },
            )
        except Exception as exc:
            logger.error("[MCPClient] Error invocando tool %s: %s", tool_name, exc)
            return json.dumps({"error": str(exc), "tool": tool_name}, ensure_ascii=False)

        if "error" in rpc_response:
            error = rpc_response["error"]
            return json.dumps({"error": error, "tool": tool_name}, ensure_ascii=False)

        result = rpc_response.get("result", {})

        if isinstance(result, str):
            return result

        if isinstance(result, dict):
            content = result.get("content")
            if isinstance(content, list):
                text_parts: List[str] = [
                    item.get("text", "")
                    for item in content
                    if isinstance(item, dict) and item.get("type") == "text"
                ]
                if text_parts:
                    return "\n".join(part for part in text_parts if part)

        return json.dumps(result, ensure_ascii=False)

    def list_tools(self) -> List[str]:
        try:
            rpc_response = self._rpc(method="tools/list", params={})
            result = rpc_response.get("result", {})
            tools = result.get("tools", [])
            names = [tool.get("name") for tool in tools if isinstance(tool, dict)]
            return [name for name in names if isinstance(name, str) and name]
        except Exception as exc:
            logger.warning("[MCPClient] No se pudo listar tools remotas: %s", exc)
            # Fallback mínimo para no romper el ciclo ReAct si MCP no responde.
            return [
                "buscar_bebida",
                "listar_menu",
                "obtener_recomendacion",
                "consultar_granos_disponibles",
                "verificar_promocion_activa",
            ]
