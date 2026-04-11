from fastmcp import FastMCP

# 1. Crear el servidor con un nombre descriptivo
mcp = FastMCP("NeoCafeIA")


# 2. Decorar funciones Python con @mcp.tool()
@mcp.tool()
def buscar_bebida(nombre: str) -> str:
    """
    Busca una bebida en el menú de NeoCafeIA.
    Retorna descripción, precio y recomendaciones de preparación.
    """
    bebidas = {
        "espresso":     "Espresso   — $2.500 — Café concentrado intenso — Grano premium",
        "cappuccino":   "Cappuccino — $4.000 — Espresso + leche vaporizada — Cremoso y suave",
        "latte":        "Latte      — $4.500 — Espresso + mucha leche — Suave y reconfortante",
        "americano":    "Americano  — $3.000 — Espresso + agua caliente — Clásico y fuerte",
        "macchiato":    "Macchiato  — $3.500 — Espresso + poco vapor — Equilibrado",
        "mocca":        "Moca       — $5.000 — Espresso + chocolate + leche — Delicioso",
    }
    resultado = bebidas.get(nombre.lower(), f"'{nombre}' no disponible en nuestro menú")
    return resultado


@mcp.tool()
def listar_menu() -> str:
    """
    Lista el menú completo de NeoCafeία con bebidas, postres y promociones especiales.
    """
    return """═══ MENÚ NEOCAFEÍA ═══
    
☕ BEBIDAS CON ESPRESSO:
    • Espresso      — $2.500
    • Americano     — $3.000
    • Macchiato     — $3.500
    • Cappuccino    — $4.000
    • Latte         — $4.500
    • Moca          — $5.000

🍰 POSTRES FRESCOS:
    • Brownie de chocolate    — $3.500
    • Cheesecake frutal       — $4.000
    • Croissant relleno       — $2.500
    • Galletas artesanales    — $1.500 / 3 unidades

🌟 PROMOCIONES ESPECIALES:
    • Combo Mañana: Espresso + Croissant — $4.500 (-$1.500)
    • Happy Hour: 2 bebidas por $7.000 (5-7 PM)
    • Estudiante: -20% con carnet"""


@mcp.tool()
def obtener_recomendacion(preferencia: str) -> str:
    """
    Proporciona una recomendación personalizada basada en la preferencia del cliente.
    Opciones: 'suave', 'fuerte', 'cremoso', 'refrescante', 'dulce'
    """
    recomendaciones = {
        "suave":       "Te recomendamos un Latte o Cappuccino — perfectos para disfrutar sin intensidad",
        "fuerte":      "Un Espresso o Americano es lo tuyo — café puro y con carácter",
        "cremoso":     "Prueba nuestro Cappuccino o Moca — cremosidad en cada sorbo",
        "refrescante": "Iced Americano o Iced Cappuccino — ideal para estos días",
        "dulce":       "Moca con extra chocolate o Latte con caramelo — indulgencia pura",
    }
    resultado = recomendaciones.get(preferencia.lower(), 
                                   "Cuéntanos tu preferencia: suave, fuerte, cremoso, refrescante o dulce")
    return resultado


@mcp.tool()
def consultar_granos_disponibles() -> str:
    """
    Lista los granos de café disponibles con su origen, perfil de sabor y disponibilidad.
    """
    return """🌍 SELECCIÓN DE GRANOS PREMIUM:

🇨🇴 GRANO COLOMBIANO
    Origen: Eje Cafetero
    Perfil: Balance perfecto, notas de chocolate y nuez
    Disponibilidad: 50 kg en stock

🇪🇹 GRANO ETÍOPE YIRGACHEFFE
    Origen: Etiopía
    Perfil: Floral, afrutado, notas de arándano
    Disponibilidad: 25 kg en stock

🇵🇪 GRANO PERUANO
    Origen: Cusco
    Perfil: Suave, cremoso, notas de caramelo
    Disponibilidad: 35 kg en stock"""


@mcp.tool()
def verificar_promocion_activa() -> str:
    """
    Verifica qué promociones están activas hoy en NeoCafeía.
    """
    return """🎉 PROMOCIONES ACTIVAS HOY:

✅ HAPPY HOUR (5:00 PM - 7:00 PM)
   Dos bebidas por $7.000 (ahorro de hasta $3.500)

✅ VIERNES GOURMET
   Todos los mochas con chocolatería artesanal -30%

✅ CLIENTE FRECUENTE
   Cada 5 bebidas, la 6ª a mitad de precio

✅ COMBO ESTUDIANTE
   Bebida + Postre por $6.500 (presentar carnet)"""


# 3. Punto de entrada para Vercel
if __name__ == "__main__":
    mcp.run()