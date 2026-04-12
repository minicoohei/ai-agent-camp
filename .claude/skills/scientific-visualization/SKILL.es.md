---
name: scientific-visualization
description: "Meta-habilidad para crear gráficos y figuras de calidad de publicación para envío a revistas. Se activa con solicitudes como 'Crear un gráfico para un artículo', 'Crear una figura para Nature', 'Visualización de calidad de publicación'."
triggers:
  - Crear un gráfico para un artículo
  - Crear figuras de calidad de publicación
  - Figura para Nature
  - Crear figuras académicas
  - Gráfico compatible con daltonismo
  - scientific-visualization
  - publication-ready figure
license: MIT license
metadata:
    skill-author: K-Dense Inc.
source: github.com/K-Dense-AI/claude-scientific-skills@main
---

# Visualización científica

## Descripción general

La visualización científica transforma datos en figuras claras y precisas para publicación. Cree gráficos listos para revistas con diseños de múltiples paneles, barras de error, marcadores de significancia y paletas seguras para daltónicos. Exporte como PDF/EPS/TIFF usando matplotlib, seaborn y plotly para manuscritos.

## Cuándo usar esta habilidad

Esta habilidad debe usarse cuando:
- Crea gráficos o visualizaciones para manuscritos científicos
- Prepara figuras para envío a revistas (Nature, Science, Cell, PLOS, etc.)
- Necesita asegurar que las figuras sean accesibles para daltónicos
- Hace figuras de múltiples paneles con estilo consistente
- Exporta figuras en la resolución y formato correctos
- Sigue directrices de publicación específicas
- Mejora figuras existentes para cumplir estándares de publicación
- Crea figuras que necesitan funcionar tanto en color como en escala de grises

## Guía de inicio rápido

### Figura básica de calidad de publicación

```python
import matplotlib.pyplot as plt
import numpy as np

# Aplicar estilo de publicación (de scripts/style_presets.py)
from style_presets import apply_publication_style
apply_publication_style('default')

# Crear figura con tamaño apropiado (columna simple = 3.5 pulgadas)
fig, ax = plt.subplots(figsize=(3.5, 2.5))

# Graficar datos
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Etiquetado adecuado con unidades
ax.set_xlabel('Tiempo (segundos)')
ax.set_ylabel('Amplitud (mV)')
ax.legend(frameon=False)

# Eliminar bordes innecesarios
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Guardar en formatos de publicación (de scripts/figure_export.py)
from figure_export import save_publication_figure
save_publication_figure(fig, 'figure1', formats=['pdf', 'png'], dpi=300)
```

### Usando estilos preconfigurados

Aplique estilos específicos de revistas usando los archivos de estilo matplotlib en `assets/`:

```python
import matplotlib.pyplot as plt

# Opción 1: Usar archivo de estilo directamente
plt.style.use('assets/nature.mplstyle')

# Opción 2: Usar el helper style_presets.py
from style_presets import configure_for_journal
configure_for_journal('nature', figure_width='single')

# Ahora cree figuras - coincidirán automáticamente con las especificaciones de Nature
fig, ax = plt.subplots()
# ... su código de graficación ...
```

## Principios fundamentales y mejores prácticas

### 1. Resolución y formato de archivo

**Requisitos críticos** (detallados en `references/publication_guidelines.md`):
- **Imágenes rasterizadas** (fotos, microscopía): 300-600 DPI
- **Arte lineal** (gráficos, plots): 600-1200 DPI o formato vectorial
- **Formatos vectoriales** (preferidos): PDF, EPS, SVG
- **Formatos rasterizados**: TIFF, PNG (nunca JPEG para datos científicos)

### 2. Selección de colores - Accesibilidad para daltónicos

**Siempre use paletas amigables para daltónicos** (detallado en `references/color_palettes.md`):

**Recomendado: paleta Okabe-Ito** (distinguible por todos los tipos de daltonismo):
```python
# Opción 1: Usar assets/color_palettes.py
from color_palettes import OKABE_ITO_LIST, apply_palette
apply_palette('okabe_ito')

# Opción 2: Especificación manual
okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442',
             '#0072B2', '#D55E00', '#CC79A7', '#000000']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=okabe_ito)
```

**Para mapas de calor/datos continuos:**
- Usar mapas de colores perceptualmente uniformes: `viridis`, `plasma`, `cividis`
- Evitar mapas divergentes rojo-verde (usar `PuOr`, `RdBu`, `BrBG` en su lugar)
- Nunca usar mapas de colores `jet` o `rainbow`

**Siempre pruebe las figuras en escala de grises** para asegurar la interpretabilidad.

### 3. Tipografía y texto

**Directrices de fuentes** (detalladas en `references/publication_guidelines.md`):
- Fuentes sans-serif: Arial, Helvetica, Calibri
- Tamaños mínimos al **tamaño de impresión final**:
  - Etiquetas de ejes: 7-9 pt
  - Etiquetas de marcas: 6-8 pt
  - Etiquetas de panel: 8-12 pt (negrita)
- Capitalización de oración para etiquetas: "Tiempo (horas)" no "TIEMPO (HORAS)"
- Siempre incluir unidades entre paréntesis

### 4. Dimensiones de figura

**Anchos específicos por revista** (detallados en `references/journal_requirements.md`):
- **Nature**: Simple 89 mm, Doble 183 mm
- **Science**: Simple 55 mm, Doble 175 mm
- **Cell**: Simple 85 mm, Doble 178 mm

### 5. Figuras de múltiples paneles

**Mejores prácticas:**
- Etiquetar paneles con letras en negrita: **A**, **B**, **C** (mayúsculas para la mayoría de revistas, minúsculas para Nature)
- Mantener estilo consistente en todos los paneles
- Alinear paneles a lo largo de los bordes donde sea posible
- Usar espacio blanco adecuado entre paneles

## Rigor estadístico

**Siempre incluir:**
- Barras de error (DE, EEM, o IC - especificar cuál en el pie de figura)
- Tamaño de muestra (n) en la figura o pie de figura
- Marcadores de significancia estadística (*, **, ***)
- Puntos de datos individuales cuando sea posible (no solo estadísticas resumidas)

## Lista de verificación final

Antes de enviar figuras, verifique:

- [ ] La resolución cumple los requisitos de la revista (300+ DPI)
- [ ] El formato de archivo es correcto (vectorial para gráficos, TIFF para imágenes)
- [ ] El tamaño de la figura coincide con las especificaciones de la revista
- [ ] Todo el texto es legible al tamaño final (>=6 pt)
- [ ] Los colores son amigables para daltónicos
- [ ] La figura funciona en escala de grises
- [ ] Todos los ejes etiquetados con unidades
- [ ] Barras de error presentes con definición en el pie de figura
- [ ] Etiquetas de panel presentes y consistentes
- [ ] Sin efectos decorativos innecesarios ni efectos 3D
- [ ] Fuentes consistentes en todas las figuras
- [ ] Significancia estadística claramente marcada
- [ ] La leyenda es clara y completa

Use esta habilidad para asegurar que las figuras científicas cumplan los más altos estándares de publicación mientras permanecen accesibles para todos los lectores.

Para documentación completa incluyendo integración con seaborn, técnicas avanzadas de plotly y ejemplos detallados de código, consulte el archivo SKILL.md fuente.
