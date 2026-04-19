---
name: ui-ux-pro-max
description: "Guía de diseño UI/UX. Soporta 50 estilos, 97 paletas, 57 combinaciones de fuentes y 9 stacks. Se activa con solicitudes como 'Diseñar la interfaz', 'Crear un sistema de diseño', 'Revisión de pantalla', etc."
source: github.com/nextlevelbuilder/ui-ux-pro-max-skill@main
triggers:
  - Diseño de interfaz
  - Revisión UX
  - Crear un sistema de diseño
  - Crear una página de destino
  - Diseño de pantalla
  - Elegir esquema de colores
  - ui-ux-pro-max
  - color palette
---

## Palabras de Activación
"Diseño UI", "Revisión UX", "Diseño", "Página de destino", "Diseño de pantalla"

**Palabras clave soportadas:**
- Acciones: planificar, construir, crear, diseñar, implementar, revisar, corregir, mejorar, optimizar, refactorizar, verificar
- Proyectos: sitio web, página de destino, panel de control, panel de administración, comercio electrónico, SaaS, portafolio, blog, aplicación móvil, .html, .tsx, .vue, .svelte
- Elementos: botón, modal, barra de navegación, barra lateral, tarjeta, tabla, formulario, gráfico
- Estilos: glassmorphism, claymorphism, minimalismo, brutalismo, neumorphism, bento grid, modo oscuro, responsive, skeuomorphism, diseño plano
- Temas: paleta de colores, accesibilidad, animación, diseño, tipografía, emparejamiento de fuentes, espaciado, hover, sombra, gradiente
- Integraciones: shadcn/ui MCP para búsqueda de componentes y ejemplos

# UI/UX Pro Max - Inteligencia de Diseño

Guía completa de diseño para aplicaciones web y móviles. Contiene más de 50 estilos, 97 paletas de colores, 57 emparejamientos de fuentes, 99 directrices UX y 25 tipos de gráficos en 9 stacks tecnológicos. Base de datos consultable con recomendaciones basadas en prioridad.

## Cuándo Aplicar

Consulte estas directrices cuando:
- Diseñe nuevos componentes UI o páginas
- Elija paletas de colores y tipografía
- Revise código para problemas de UX
- Construya páginas de destino o paneles de control
- Implemente requisitos de accesibilidad

## Categorías de Reglas por Prioridad

| Prioridad | Categoría | Impacto | Dominio |
|-----------|----------|---------|---------|
| 1 | Accesibilidad | CRÍTICO | `ux` |
| 2 | Táctil e Interacción | CRÍTICO | `ux` |
| 3 | Rendimiento | ALTO | `ux` |
| 4 | Diseño y Responsive | ALTO | `ux` |
| 5 | Tipografía y Color | MEDIO | `typography`, `color` |
| 6 | Animación | MEDIO | `ux` |
| 7 | Selección de Estilo | MEDIO | `style`, `product` |
| 8 | Gráficos y Datos | BAJO | `chart` |

## Referencia Rápida

### 1. Accesibilidad (CRÍTICO)

- `color-contrast` - Ratio mínimo 4.5:1 para texto normal
- `focus-states` - Anillos de enfoque visibles en elementos interactivos
- `alt-text` - Texto alternativo descriptivo para imágenes significativas
- `aria-labels` - aria-label para botones solo con icono
- `keyboard-nav` - Orden de tabulación coincide con orden visual
- `form-labels` - Usar label con atributo for

### 2. Táctil e Interacción (CRÍTICO)

- `touch-target-size` - Objetivos táctiles mínimos de 44x44px
- `hover-vs-tap` - Usar clic/tap para interacciones primarias
- `loading-buttons` - Deshabilitar botón durante operaciones asíncronas
- `error-feedback` - Mensajes de error claros cerca del problema
- `cursor-pointer` - Agregar cursor-pointer a elementos clicables

### 3. Rendimiento (ALTO)

- `image-optimization` - Usar WebP, srcset, carga diferida
- `reduced-motion` - Verificar prefers-reduced-motion
- `content-jumping` - Reservar espacio para contenido asíncrono

### 4. Diseño y Responsive (ALTO)

- `viewport-meta` - width=device-width initial-scale=1
- `readable-font-size` - Texto de cuerpo mínimo 16px en móvil
- `horizontal-scroll` - Asegurar que el contenido cabe en el ancho del viewport
- `z-index-management` - Definir escala de z-index (10, 20, 30, 50)

### 5. Tipografía y Color (MEDIO)

- `line-height` - Usar 1.5-1.75 para texto de cuerpo
- `line-length` - Limitar a 65-75 caracteres por línea
- `font-pairing` - Emparejar personalidades de fuentes de encabezado/cuerpo

### 6. Animación (MEDIO)

- `duration-timing` - Usar 150-300ms para micro-interacciones
- `transform-performance` - Usar transform/opacity, no width/height
- `loading-states` - Pantallas esqueleto o spinners

### 7. Selección de Estilo (MEDIO)

- `style-match` - Hacer coincidir el estilo con el tipo de producto
- `consistency` - Usar el mismo estilo en todas las páginas
- `no-emoji-icons` - Usar iconos SVG, no emojis

### 8. Gráficos y Datos (BAJO)

- `chart-type` - Hacer coincidir tipo de gráfico con tipo de datos
- `color-guidance` - Usar paletas de colores accesibles
- `data-table` - Proporcionar alternativa de tabla para accesibilidad

## Cómo Usar

Busque dominios específicos usando la herramienta CLI a continuación.

---

## Prerrequisitos

Verificar si Python está instalado:

```bash
python3 --version || python --version
```

Si Python no está instalado, instálelo según el sistema operativo:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## Cómo Usar Esta Habilidad

Cuando el usuario solicite trabajo UI/UX (diseñar, construir, crear, implementar, revisar, corregir, mejorar), siga este flujo de trabajo:

### Paso 1: Analizar Requisitos del Usuario

Extraer información clave de la solicitud del usuario:
- **Tipo de producto**: SaaS, comercio electrónico, portafolio, panel de control, página de destino, etc.
- **Palabras clave de estilo**: minimalista, lúdico, profesional, elegante, modo oscuro, etc.
- **Industria**: salud, fintech, gaming, educación, etc.
- **Stack**: React, Vue, Next.js, o por defecto `html-tailwind`

### Paso 2: Generar Sistema de Diseño (REQUERIDO)

**Siempre comience con `--design-system`** para obtener recomendaciones completas con razonamiento:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<tipo_producto> <industria> <palabras_clave>" --design-system [-p "Nombre del Proyecto"]
```

Este comando:
1. Busca en 5 dominios en paralelo (producto, estilo, color, landing, tipografía)
2. Aplica reglas de razonamiento de `ui-reasoning.csv` para seleccionar las mejores coincidencias
3. Devuelve sistema de diseño completo: patrón, estilo, colores, tipografía, efectos
4. Incluye anti-patrones a evitar

**Ejemplo:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Paso 2b: Persistir Sistema de Diseño (Patrón Maestro + Sobrescrituras)

Para guardar el sistema de diseño para **recuperación jerárquica entre sesiones**, agregue `--persist`:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<consulta>" --design-system --persist -p "Nombre del Proyecto"
```

Esto crea:
- `design-system/MASTER.md` -- Fuente de Verdad Global con todas las reglas de diseño
- `design-system/pages/` -- Carpeta para sobrescrituras específicas de página

**Con sobrescritura específica de página:**
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<consulta>" --design-system --persist -p "Nombre del Proyecto" --page "dashboard"
```

Esto también crea:
- `design-system/pages/dashboard.md` -- Desviaciones específicas de página respecto al Maestro

**Cómo funciona la recuperación jerárquica:**
1. Al construir una página específica (ej., "Checkout"), primero verifique `design-system/pages/checkout.md`
2. Si el archivo de página existe, sus reglas **sobrescriben** el archivo Maestro
3. Si no, use `design-system/MASTER.md` exclusivamente

**Prompt de recuperación contextual:**
```
Estoy construyendo la página [Nombre de Página]. Por favor lea design-system/MASTER.md.
También verifique si existe design-system/pages/[nombre-pagina].md.
Si el archivo de página existe, priorice sus reglas.
Si no, use las reglas del Maestro exclusivamente.
Ahora, genere el código...
```

### Paso 3: Complementar con Búsquedas Detalladas (según sea necesario)

Después de obtener el sistema de diseño, use búsquedas por dominio para obtener detalles adicionales:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<palabra_clave>" --domain <dominio> [-n <max_resultados>]
```

**Cuándo usar búsquedas detalladas:**

| Necesidad | Dominio | Ejemplo |
|-----------|---------|---------|
| Más opciones de estilo | `style` | `--domain style "glassmorphism dark"` |
| Recomendaciones de gráficos | `chart` | `--domain chart "real-time dashboard"` |
| Mejores prácticas UX | `ux` | `--domain ux "animation accessibility"` |
| Fuentes alternativas | `typography` | `--domain typography "elegant luxury"` |
| Estructura de landing | `landing` | `--domain landing "hero social-proof"` |

### Paso 4: Directrices de Stack (Predeterminado: html-tailwind)

Obtenga mejores prácticas específicas de implementación. Si el usuario no especifica un stack, **por defecto use `html-tailwind`**.

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<palabra_clave>" --stack html-tailwind
```

Stacks disponibles: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Referencia de Búsqueda

### Dominios Disponibles

| Dominio | Usar Para | Palabras Clave de Ejemplo |
|---------|-----------|---------------------------|
| `product` | Recomendaciones de tipo de producto | SaaS, e-commerce, portafolio, salud, belleza, servicio |
| `style` | Estilos UI, colores, efectos | glassmorphism, minimalismo, modo oscuro, brutalismo |
| `typography` | Emparejamiento de fuentes, Google Fonts | elegante, lúdico, profesional, moderno |
| `color` | Paletas de colores por tipo de producto | saas, ecommerce, salud, belleza, fintech, servicio |
| `landing` | Estructura de página, estrategias CTA | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | Tipos de gráficos, recomendaciones de bibliotecas | tendencia, comparación, línea de tiempo, embudo, circular |
| `ux` | Mejores prácticas, anti-patrones | animación, accesibilidad, z-index, carga |
| `react` | Rendimiento React/Next.js | waterfall, bundle, suspense, memo, rerender, cache |
| `web` | Directrices de interfaz web | aria, focus, keyboard, semantic, virtualize |
| `prompt` | Prompts de IA, palabras clave CSS | (nombre de estilo) |

### Stacks Disponibles

| Stack | Enfoque |
|-------|---------|
| `html-tailwind` | Utilidades Tailwind, responsive, a11y (PREDETERMINADO) |
| `react` | Estado, hooks, rendimiento, patrones |
| `nextjs` | SSR, enrutamiento, imágenes, rutas API |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Componentes, Navegación, Listas |
| `flutter` | Widgets, Estado, Diseño, Temas |
| `shadcn` | Componentes shadcn/ui, temas, formularios, patrones |
| `jetpack-compose` | Composables, Modifiers, State Hoisting, Recomposition |

---

## Ejemplo de Flujo de Trabajo

**Solicitud del usuario:** "Crear una página de destino para un servicio profesional de cuidado de piel"

### Paso 1: Analizar Requisitos
- Tipo de producto: Servicio de belleza/spa
- Palabras clave de estilo: elegante, profesional, suave
- Industria: Belleza/Bienestar
- Stack: html-tailwind (predeterminado)

### Paso 2: Generar Sistema de Diseño (REQUERIDO)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Salida:** Sistema de diseño completo con patrón, estilo, colores, tipografía, efectos y anti-patrones.

### Paso 3: Complementar con Búsquedas Detalladas (según sea necesario)

```bash
# Obtener directrices UX para animación y accesibilidad
python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux

# Obtener opciones alternativas de tipografía si es necesario
python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury serif" --domain typography
```

### Paso 4: Directrices de Stack

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

**Luego:** Sintetizar sistema de diseño + búsquedas detalladas e implementar el diseño.

---

## Formatos de Salida

La bandera `--design-system` soporta dos formatos de salida:

```bash
# Caja ASCII (predeterminado) - mejor para visualización en terminal
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown - mejor para documentación
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Consejos para Mejores Resultados

1. **Sea específico con las palabras clave** - "healthcare SaaS dashboard" > "app"
2. **Busque múltiples veces** - Diferentes palabras clave revelan diferentes perspectivas
3. **Combine dominios** - Estilo + Tipografía + Color = Sistema de diseño completo
4. **Siempre verifique UX** - Busque "animation", "z-index", "accessibility" para problemas comunes
5. **Use la bandera de stack** - Obtenga mejores prácticas específicas de implementación
6. **Itere** - Si la primera búsqueda no coincide, intente diferentes palabras clave

---

## Reglas Comunes para UI Profesional

Estos son problemas frecuentemente pasados por alto que hacen que la UI luzca poco profesional:

### Iconos y Elementos Visuales

| Regla | Hacer | No Hacer |
|-------|-------|----------|
| **Sin emojis como iconos** | Usar iconos SVG (Heroicons, Lucide, Simple Icons) | Usar emojis como iconos de UI |
| **Estados hover estables** | Usar transiciones de color/opacidad en hover | Usar transformaciones de escala que desplacen el diseño |
| **Logos de marca correctos** | Investigar SVG oficial de Simple Icons | Adivinar o usar rutas de logo incorrectas |
| **Tamaño de iconos consistente** | Usar viewBox fijo (24x24) con w-6 h-6 | Mezclar diferentes tamaños de iconos aleatoriamente |

### Interacción y Cursor

| Regla | Hacer | No Hacer |
|-------|-------|----------|
| **Cursor pointer** | Agregar `cursor-pointer` a todas las tarjetas clicables/hoverable | Dejar cursor por defecto en elementos interactivos |
| **Retroalimentación hover** | Proporcionar retroalimentación visual (color, sombra, borde) | Sin indicación de que el elemento es interactivo |
| **Transiciones suaves** | Usar `transition-colors duration-200` | Cambios de estado instantáneos o muy lentos (>500ms) |

### Contraste Modo Claro/Oscuro

| Regla | Hacer | No Hacer |
|-------|-------|----------|
| **Tarjeta glass modo claro** | Usar `bg-white/80` o mayor opacidad | Usar `bg-white/10` (muy transparente) |
| **Contraste de texto claro** | Usar `#0F172A` (slate-900) para texto | Usar `#94A3B8` (slate-400) para texto de cuerpo |
| **Texto atenuado claro** | Usar `#475569` (slate-600) como mínimo | Usar gray-400 o más claro |
| **Visibilidad de bordes** | Usar `border-gray-200` en modo claro | Usar `border-white/10` (invisible) |

### Diseño y Espaciado

| Regla | Hacer | No Hacer |
|-------|-------|----------|
| **Navbar flotante** | Agregar espaciado `top-4 left-4 right-4` | Pegar navbar a `top-0 left-0 right-0` |
| **Padding de contenido** | Considerar altura de navbar fijo | Dejar que el contenido se oculte detrás de elementos fijos |
| **Max-width consistente** | Usar el mismo `max-w-6xl` o `max-w-7xl` | Mezclar diferentes anchos de contenedor |

---

## Lista de Verificación Pre-Entrega

Antes de entregar código UI, verifique estos elementos:

### Calidad Visual
- [ ] No se usan emojis como iconos (usar SVG en su lugar)
- [ ] Todos los iconos de un conjunto consistente (Heroicons/Lucide)
- [ ] Logos de marca correctos (verificados de Simple Icons)
- [ ] Estados hover no causan desplazamiento del diseño
- [ ] Usar colores del tema directamente (bg-primary) no envoltorio var()

### Interacción
- [ ] Todos los elementos clicables tienen `cursor-pointer`
- [ ] Estados hover proporcionan retroalimentación visual clara
- [ ] Transiciones son suaves (150-300ms)
- [ ] Estados de enfoque visibles para navegación por teclado

### Modo Claro/Oscuro
- [ ] Texto en modo claro tiene contraste suficiente (mínimo 4.5:1)
- [ ] Elementos glass/transparentes visibles en modo claro
- [ ] Bordes visibles en ambos modos
- [ ] Probar ambos modos antes de la entrega

### Diseño
- [ ] Elementos flotantes tienen espaciado apropiado desde los bordes
- [ ] Sin contenido oculto detrás de navbars fijos
- [ ] Responsive en 375px, 768px, 1024px, 1440px
- [ ] Sin scroll horizontal en móvil

### Accesibilidad
- [ ] Todas las imágenes tienen texto alternativo
- [ ] Entradas de formulario tienen etiquetas
- [ ] El color no es el único indicador
- [ ] `prefers-reduced-motion` respetado
