# DESIGN.md

Guía de diseño base para NeoCafeIA (Stitch UI). Este documento consolida los tokens y patrones existentes en static/stitch-ui y es la fuente única de verdad para nuevas pantallas.

## 1) Tokens de color (Material Design 3)

Tokens principales (no modificar):

- primary: #6f4627
- on-primary: #ffffff
- secondary: #566250
- on-secondary: #ffffff
- tertiary: #634a3e
- on-tertiary: #ffffff
- background: #fff8f0
- on-background: #1e1b14
- surface-container-lowest: #ffffff
- surface-container-low: #fbf3e6
- surface-container: #f5ede0
- outline-variant: #d5c3b8

Tokens extendidos usados en Stitch:

- primary-container: #8b5e3c
- primary-fixed: #ffdcc5
- primary-fixed-dim: #f4bb92
- secondary-container: #d9e7d0
- secondary-fixed: #d9e7d0
- secondary-fixed-dim: #bdcbb5
- tertiary-container: #7d6255
- tertiary-fixed: #ffdbcb
- tertiary-fixed-dim: #e1c0b0
- surface: #fff8f0
- surface-dim: #e1d9cc
- surface-bright: #fff8f0
- surface-container-high: #efe7da
- surface-container-highest: #e9e2d5
- surface-variant: #e9e2d5
- outline: #83746b
- inverse-surface: #343027
- inverse-on-surface: #f8f0e3
- inverse-primary: #f4bb92
- error: #ba1a1a
- error-container: #ffdad6
- on-error: #ffffff
- on-error-container: #93000a

## 2) Tipografía

Familias:

- Headline: Noto Serif
- Body: Manrope
- Label: Manrope

Escala recomendada según pantallas existentes:

- Display/Hero: 56px-144px (landing hero)
- Headline: 30px-48px
- Title: 20px-24px
- Body: 14px-18px
- Label/Overline: 9px-12px, uppercase con tracking amplio

## 3) Border radius

- DEFAULT: 1rem
- lg: 2rem
- xl: 3rem
- full: 9999px

## 4) Espaciado

Escala visible en Stitch:

- 0.5rem (2)
- 0.75rem (3)
- 1rem (4)
- 1.5rem (6)
- 2rem (8)
- 3rem (12)
- 4rem (16)
- 6rem (24)
- 8rem (32)

Regla: usar separaciones amplias en desktop y compactar en mobile sin romper jerarquía visual.

## 5) Patrones de componentes

### Botones
- Primario: fondo primary, texto on-primary, forma full o redondeada.
- Secundario/sutil: fondo surface-container-lowest con hover a surface-container-low.
- Estados: hover, active:scale-95, focus-visible obligatorio.

### Tarjetas
- Fondo en superficies claras (surface-container-low/lowest).
- Bordes suaves o gradiente leve.
- Titular en Noto Serif, supporting text en Manrope.

### Chips
- Forma full.
- Texto uppercase en tamaño label.
- Hover de intensidad suave.

### Inputs
- Fondo surface-container-lowest.
- Bordes suaves.
- Placeholder en tono neutral.
- Focus ring o outline con primary.

### Iconografía
- Material Symbols Outlined.
- Botones solo icono deben llevar aria-label.

## 6) Accesibilidad y foco

Regla global para elementos interactivos:

- focus-visible: 2px solid primary
- outline-offset: 2px

Aplicar a:

- button
- a
- input
- textarea
- elementos con role="button"

## 7) Animación y movimiento

Solo CSS transitions (sin librerías JS de animación).

- Duración base: 200-300ms
- Curva principal: cubic-bezier(0.4, 0, 0.2, 1)
- Drawer: transform translateX o translateY + transición de transform

Respetar reduced motion:

- Encapsular transiciones en @media (prefers-reduced-motion: no-preference)

## 8) Layout responsive

Breakpoints prácticos del sistema:

- Mobile: <= 768px
- Desktop: > 768px

Comportamiento esperado:

- Drawer lateral en desktop
- Bottom sheet en mobile
- CTAs full-width en mobile cuando sea acción primaria de pantalla
