# Cambios de Diseño - CodeNormative

## Inspiración: Units (https://www.awwwards.com/sites/units)

Se rediseñó CodeNormative siguiendo la estética minimalista y profesional del sitio Units, respetando sus tipografías, colores y principios de espaciado.

---

## Tipografías

### Antes
- **Body**: Inter
- **Títulos**: Inter (peso 800-900)

### Después
- **Body**: **Inter** (300, 400, 500, 600, 700, 800, 900 pesos)
  - Para párrafos, labels, texto normal
- **Títulos (h1, h2, .brand)**: **Playfair Display** (serif elegante, peso 700-900)
  - Para el logo CodeNormative
  - Para títulos principales (h1)
  - Para subtítulos (h2)

**Beneficio**: Playfair Display añade elegancia profesional como en Units, mientras Inter mantiene la legibilidad del body.

---

## Paleta de Colores

### Antes
```css
--bg: #eef1f4          /* Gris azulado */
--accent: #126b60      /* Verde azulado */
--ink: #1b2430         /* Gris oscuro */
```

### Después (Inspirado en Units)
```css
--bg: #f5f3f0          /* Beige cálido (igual a Units) */
--accent: #ffc300      /* Amarillo vibrante (como Units) */
--accent-strong: #ffb300
--ink: #1a1a1a         /* Negro puro */
--muted: #7a7a7a       /* Gris neutro */
--line: #e8e8e8        /* Bordes sutiles */
```

**Beneficio**: Los colores ahora coinciden con la paleta de Units, creando coherencia visual.

---

## Componentes Actualizados

### Brand Logo
- Tipografía: **Playfair Display** (serif)
- Tamaño aumentado de 0.95rem → 1.1rem
- Letter-spacing más negativo: -0.3px → -0.5px
- Bordes más finos (1.5px)

### Botones
- Bordes: 2px con color accent
- Hover: Transform translateY(-1px) + box-shadow sutil
- Botones secundarios: Outline style con bordes

### Inputs/Selects
- Bordes: 1.5px (más sutiles)
- Focus: Highlight amarillo (#ffc300)
- Padding: 12px para más aire

### Sidebar
- Padding: 40px (más generoso, como Units)
- Bordes: 1px border-right (separación sutil)
- Fondo: Blanco puro
- Texto: Negro (no gris claro)

### Workspace
- Padding: 40px (espaciado generoso)
- Gap entre elementos: 32px
- Tipografía: Mejorada con pesos y letter-spacing

### Tablas
- Headers: Uppercase, font-weight 700, letter-spacing 0.2px
- Bordes sutiles y hover effects
- Tipografía mejorada

### Gráficos
- Fondo: #fafaf9 (gris muy claro)
- Grid lines: #f0f0f0 (casi invisible)
- Curves: Opacidad 0.85 para mejor contraste

---

## Cambios Responsive

### Desktop (1100px+)
- Dos columnas: Sidebar (340-400px) + Workspace

### Tablet (768px-1100px)
- Sidebar se convierte en banner superior
- Border-right → border-bottom

### Mobile (<768px)
- Stack vertical
- Padding reducido (24px)
- Grid de métricas: 1 columna

---

## Resultado Final

La interfaz ahora es:
✓ **Más elegante** - Serif Playfair en títulos
✓ **Más limpia** - Colores neutros y fondo beige
✓ **Más profesional** - Espaciado generoso (Units-inspired)
✓ **Más accesible** - Mejor contraste y legibilidad
✓ **Más moderna** - Interacciones suaves (hover, focus)

---

## Google Fonts Importados

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@700;800;900&display=swap');
```

Sin dependencias adicionales, solo CSS estándar.
