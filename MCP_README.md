# MCP README

## Qué es el servidor MCP
El servidor MCP de NeoCafeIA expone tools de cafetería para que un cliente MCP consulte menú, recomendaciones, granos y promociones.

## Cómo correrlo localmente
```bash
python servidor_mcp.py
```

## URL de producción
La URL pública del servidor MCP es [https://conscious-green-bass.fastmcp.app/mcp](https://conscious-green-bass.fastmcp.app/mcp).

Esta URL está registrada también en [MCP_URL.txt](MCP_URL.txt).

Nota operativa: el endpoint de producción requiere token Bearer para invocar métodos MCP.

## Tools disponibles
| Tool | Descripción | Parámetros de entrada | Ejemplo de respuesta |
|---|---|---|---|
| buscar_bebida | Busca una bebida por nombre y devuelve precio y descripción. | nombre: str | Latte      — $3.50 — Espresso + mucha leche — Suave y reconfortante |
| listar_menu | Devuelve el menú completo de bebidas, postres y promos. | Ninguno | ═══ MENÚ NEOCAFEÍA ═══ ... ☕ BEBIDAS ... 🍰 POSTRES ... 🌟 PROMOCIONES ... |
| obtener_recomendacion | Recomienda según preferencia del cliente. | preferencia: str (suave, fuerte, cremoso, refrescante, dulce) | Te recomendamos un Latte o Cappuccino — perfectos para disfrutar sin intensidad |
| consultar_granos_disponibles | Lista granos con origen, perfil y stock. | Ninguno | 🌍 SELECCIÓN DE GRANOS PREMIUM: ... 🇨🇴 ... 🇪🇹 ... 🇵🇪 ... |
| verificar_promocion_activa | Muestra promociones activas del día. | Ninguno | 🎉 PROMOCIONES ACTIVAS HOY: ... ✅ HAPPY HOUR ... ✅ VIERNES GOURMET ... |

## Cómo conectar un cliente al servidor
Ejemplo mínimo con httpx y JSON-RPC (endpoint MCP HTTP en /mcp):

```python
import httpx

base_url = "http://localhost:8000"

with httpx.Client(timeout=10) as client:
	payload = {
		"jsonrpc": "2.0",
		"id": 1,
		"method": "tools/call",
		"params": {
			"name": "buscar_bebida",
			"arguments": {"nombre": "latte"}
		}
	}
	r = client.post(f"{base_url}/mcp", json=payload)
	r.raise_for_status()
	print(r.json())
```

## Cómo agregar una nueva tool
1. Define una función Python tipada en [servidor_mcp.py](servidor_mcp.py).
2. Decórala con @mcp.tool().
3. Reinicia el servidor y prueba la tool desde tu cliente MCP.

Ejemplo:

```python
@mcp.tool()
def saludar_cliente(nombre: str) -> str:
	return f"Hola {nombre}, bienvenido a NeoCafeIA"
```

## Variables de entorno requeridas
- `MCP_URL`: URL del servidor MCP remoto usado por el adaptador ReAct.
- `MCP_AUTH_TOKEN` (opcional): token Bearer para endpoints MCP protegidos.
- Ejemplo: `MCP_URL=https://conscious-green-bass.fastmcp.app/mcp`

## Fuente
Implementación de tools en [servidor_mcp.py](servidor_mcp.py).
