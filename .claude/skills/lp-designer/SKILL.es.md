---
name: lp-designer
description: "Flujo de trabajo para creación de LP/HP. Guía el flujo completo desde entrevista → organización de mensajes → wireframe → diseño en Pencil → implementación HTML → despliegue en Vercel. Se activa con solicitudes como 'crear un LP', 'creación de landing page', 'diseño de HP', 'producción de página web', etc."
triggers:
  - crear un LP
  - crear una landing page
  - quiero hacer una HP
  - producción de página principal
  - crear una página web
  - lp-designer
  - landing page
---

# LP/HP Designer - Skill de Producción de Landing Page y Página Principal

Skill de flujo de trabajo integrado para producir LP (Landing Page) / HP (Página Principal) desde cero.
Se completa en 6 fases desde la entrevista con AskQuestionTool hasta el despliegue en Vercel.

## Frases de Activación

- "Crear un LP", "Crear una landing page"
- "Quiero hacer una HP", "Producción de página principal"
- "Crear una página web", "Quiero hacer un sitio"
- "Diseñar con Pencil e implementar"

## Requisitos Previos

- ai-agent-camp abierto en Cursor IDE
- Pencil MCP habilitado (para operaciones con archivos .pen)
- Node.js 18+ instalado (para despliegue en Vercel)
- Clave de API de Gemini configurada (para diagram-generator)

## Resumen del Flujo de Trabajo

```
Fase 1: Entrevista (AskQuestion)
    | Resumen del servicio, objetivo, eje de mensajes
Fase 2: Organización de Mensajes
    | Persona, beneficios, copy
Fase 3: Creación de WF
    | ASCII WF + WF Visual
Fase 4: Diseño en Pencil
    | Archivo de diseño .pen
Fase 5: Implementación de Código
    | HTML/CSS(Tailwind)/JS
Fase 6: Despliegue en Vercel
    | URL pública
```

---

## Fase 1: Entrevista (AskQuestion)

Primero, use AskQuestionTool para recopilar estructuralmente los requisitos del LP/HP a crear.

### Paso 1-1: Confirmación del Tipo de Proyecto

```json
{
  "title": "Entrevista de Producción LP/HP",
  "questions": [{
    "id": "project_type",
    "prompt": "¿Qué tipo de página desea crear?",
    "options": [
      {"id": "lp", "label": "LP (Landing Page) - Enfocada en un solo CTA"},
      {"id": "hp", "label": "HP (Página Principal) - Múltiples secciones con navegación"},
      {"id": "product", "label": "Página de Producto - Centrada en funcionalidades"},
      {"id": "event", "label": "Página de Evento/Campaña"}
    ]
  }]
}
```

### Paso 1-2: Información del Servicio/Producto

```json
{
  "title": "Información del Servicio",
  "questions": [
    {
      "id": "service_category",
      "prompt": "Seleccione la categoría del servicio",
      "options": [
        {"id": "saas", "label": "SaaS / Servicio Web"},
        {"id": "ec", "label": "Comercio Electrónico / Retail"},
        {"id": "consulting", "label": "Consultoría / Servicios Profesionales"},
        {"id": "education", "label": "Educación / Escuela"},
        {"id": "event", "label": "Evento / Seminario"},
        {"id": "portfolio", "label": "Portafolio / Personal"},
        {"id": "other", "label": "Otro"}
      ]
    },
    {
      "id": "design_tone",
      "prompt": "Seleccione el tono del diseño",
      "options": [
        {"id": "professional", "label": "Profesional / Confiable"},
        {"id": "modern", "label": "Moderno / Elegante"},
        {"id": "playful", "label": "Pop / Amigable"},
        {"id": "luxury", "label": "Lujo / Elegante"},
        {"id": "minimal", "label": "Minimal / Simple"},
        {"id": "tech", "label": "Tech / Avanzado"}
      ]
    }
  ]
}
```

### Paso 1-3: Entrevista Adicional (Entrada Libre)

Después de AskQuestion, confirme lo siguiente mediante entrada libre:

- **Nombre del servicio**: Nombre oficial
- **Ideas de eslogan**: Si hay alguno (de lo contrario se genera)
- **Objetivo**: Para quién es la página
- **Puntos de venta principales**: Aproximadamente 3
- **Sitios de referencia**: URLs si los hay
- **Propósito del CTA**: Consulta / Registro / Solicitud de materiales / Compra, etc.

---

## Fase 2: Organización de Mensajes

Genere el siguiente documento basado en los resultados de la entrevista de la Fase 1.

### Salida: `output/lp-brief.md`

```markdown
# Brief del LP

## Persona
- Nombre: {ej.: Juan Pérez}
- Edad: {ej.: 35 años}
- Ocupación: {ej.: Gerente de Marketing}
- Desafío: {ej.: La creación de LP toma demasiado tiempo}

## Eje de Mensajes (3 Beneficios)
1. {Beneficio principal}
2. {Sub beneficio 1}
3. {Sub beneficio 2}

## Copy
- Titular: {ej.: Cree LPs 10 veces más rápido con IA}
- Subtitular: {ej.: La IA apoya todo, desde la entrevista hasta el despliegue}
- Texto del CTA: {ej.: Comenzar Gratis}

## Estructura de Secciones
1. Hero (Titular + CTA)
2. Pain Points (Planteamiento del problema)
3. Solution (Introducción de la solución)
4. Features (Funcionalidades / Características 3-4 elementos)
5. Social Proof (Resultados / Testimonios)
6. Pricing / Plan (Precios/planes) *Opcional
7. FAQ (Preguntas frecuentes)
8. Final CTA (Acción final)
```

---

## Fase 3: Creación de WF (Wireframe)

### Paso 3-1: Wireframe ASCII

Diseñe la estructura de cada sección en formato basado en texto:

```
+----------------------------------+
|           HEADER / NAV           |
+----------------------------------+
|                                  |
|     [Imagen / Video Hero]        |
|                                  |
|     Titular (H1)                |
|     Subtitular                   |
|     [ Botón CTA ]              |
|                                  |
+----------------------------------+
|     Sección Pain Points          |
|   +------+ +------+ +------+    |
|   |Prob 1| |Prob 2| |Prob 3|    |
|   +------+ +------+ +------+    |
+----------------------------------+
|     Sección Solution             |
|   [Imagen]  Texto descriptivo    |
+----------------------------------+
|     Sección Features             |
|   +-------+ +-------+           |
|   |Func 1 | |Func 2 |           |
|   +-------+ +-------+           |
|   +-------+ +-------+           |
|   |Func 3 | |Func 4 |           |
|   +-------+ +-------+           |
+----------------------------------+
|     Social Proof                 |
|     ***** Testimonios            |
+----------------------------------+
|     FAQ                          |
|     P1 / R1                      |
|     P2 / R2                      |
+----------------------------------+
|     Final CTA                    |
|     [ Botón CTA ]              |
+----------------------------------+
|           FOOTER                 |
+----------------------------------+
```

### Paso 3-2: Generación de WF Visual

Genere un wireframe visual usando diagram-generator:

```bash
uv run python tools/generate_diagram.py --topic "LP wireframe: {estructura de secciones}" --style minimalist
```

Salida: `output/images/lp-wireframe.png`

---

## Fase 4: Diseño en Pencil

Cree archivos de diseño .pen usando Pencil MCP.
Como los archivos .pen están encriptados, siempre use las herramientas Pencil MCP en lugar de Read/Grep.

### Paso 4-0: Abrir el Editor Pencil

Primero verifique el estado actual del editor. Cree un nuevo archivo si no hay ninguno abierto.

```
# 1) Verificar estado del editor
CallMcpTool: user-pencil / get_editor_state
  arguments: {}

# -> Devuelve error si no hay archivo abierto
# -> Devuelve lista de nodos si ya hay un archivo abierto

# 2-A) Crear un nuevo documento
CallMcpTool: user-pencil / open_document
  arguments: { "filePathOrTemplate": "new" }

# 2-B) Abrir un archivo .pen existente
CallMcpTool: user-pencil / open_document
  arguments: { "filePathOrTemplate": "path/to/design.pen" }

# 3) Después de abrir, verificar la estructura de nodos con get_editor_state
CallMcpTool: user-pencil / get_editor_state
  arguments: {}
```

**Importante**: `open_document` es una operación para abrir el archivo objetivo dentro de la aplicación Pencil.
`user-pencil` debe estar habilitado en la configuración de MCP de Cursor.

### Paso 4-1: Obtener Directrices de Diseño LP

Recupere reglas de diseño específicas para LP (estructura de secciones, diseño del hero, diseño del footer, etc.):

```
CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "landing-page" }
```

Estas directrices incluyen:
- Estructura de secciones recomendada para SaaS/LP (Hero -> Features -> Social Proof -> Pricing -> FAQ -> CTA -> Footer)
- Mejores prácticas para la sección Hero
- Principio de orden contenido-antes-visual
- Ejemplos de creación de contenedor de página con batch_design

### Paso 4-2: Obtener Guía de Estilo

Recupere una guía de estilo que coincida con el tono del diseño:

```
# 1) Verificar etiquetas disponibles
CallMcpTool: user-pencil / get_style_guide_tags
  arguments: {}

# -> Devuelve etiquetas como minimal, modern, clean, warm, tech, brutalist, etc.

# 2) Seleccionar etiquetas que coincidan con el tono del resultado de la entrevista
CallMcpTool: user-pencil / get_style_guide
  arguments: { "tags": ["minimal", "clean", "whitespace", "website"] }
```

La guía de estilo incluye:
- Sistema de color (fondo, texto, colores de acento)
- Tipografía (fuente, tamaño, peso)
- Valores de espaciado, border-radius, sombra
- Patrones de componentes (botones, tarjetas, navegación, etc.)

### Paso 4-3: Crear Contenedor de Página

Cree un frame que envuelva todo el LP con `batch_design`:

```
# Las operaciones de batch_design se escriben en formato de script
CallMcpTool: user-pencil / batch_design
  arguments: {
    "operations": "page=I(document, {type: \"frame\", name: \"Landing Page\", placeholder: true, layout: \"vertical\", width: 1440, height: \"fit_content(4000)\", fill: \"#FFFFFF\", clip: true})"
  }
```

**Sintaxis básica de operaciones batch_design:**

| Operación | Sintaxis | Descripción |
|-----------|----------|-------------|
| Insert | `foo=I("parentId", {...})` | Insertar hijo en nodo padre |
| Copy | `bar=C("nodeId", "parentId", {...})` | Copiar un nodo |
| Update | `U("nodeId", {...})` | Actualizar propiedades |
| Replace | `R("nodeId", {...})` | Reemplazar un nodo |
| Delete | `D("nodeId")` | Eliminar un nodo |
| Move | `M("nodeId", "parentId", index)` | Mover un nodo |
| Image | `G("nodeId", "ai", "prompt")` | Generación de imagen con IA |

**Reglas importantes:**
- Siempre establezca `placeholder: true` en frames en progreso, cambie a `false` cuando esté completo
- Siempre establezca `fill` en el texto (el valor predeterminado es transparente e invisible)
- Máximo 25 operaciones por llamada a batch_design
- `x`, `y` se ignoran para hijos flexbox (use `fill_container` / `fit_content`)
- No existe un tipo de nodo de imagen. Aplique imágenes a frames con `G()`

### Paso 4-4: Crear Secciones Secuencialmente

Cree las siguientes secciones de 1 a 2 a la vez usando `batch_design`:

1. **Header**: Logo + enlaces de navegación + botón CTA (disposición horizontal `space_between`)
2. **Sección Hero**: Badge, titular, subtitular, botón CTA (centrado)
3. **Features**: Encabezado de sección + tarjetas de 3 columnas (icono + título + descripción)
4. **How It Works**: Proceso de 3 pasos numerados (números en círculo + título + descripción)
5. **Stats/Social Proof**: Estadísticas con fondo oscuro + tarjetas de testimonios de clientes
6. **Final CTA**: Fondo de color de acento + titular + botón CTA
7. **Footer**: Fondo oscuro + columnas de enlaces + copyright

### Paso 4-5: Revisión y Ajuste del Diseño

Después de agregar cada sección, confirme visualmente con capturas de pantalla:

```
# Revisar toda la página
CallMcpTool: user-pencil / get_screenshot
  arguments: { "nodeId": "pageId" }

# Ampliar sección específica
CallMcpTool: user-pencil / get_screenshot
  arguments: { "nodeId": "heroId" }

# Verificar estructura de diseño numéricamente (efectivo para detectar desalineación)
CallMcpTool: user-pencil / snapshot_layout
  arguments: { "parentId": "pageId", "maxDepth": 3 }
```

Corrija problemas con `batch_design` `U()`.
Una vez que todas las secciones estén completas, libere el placeholder:

```
CallMcpTool: user-pencil / batch_design
  arguments: { "operations": "U(\"pageId\", {placeholder: false})" }
```

---

## Fase 5: Implementación de Código

Convierta el diseño de Pencil en HTML/CSS/JS funcional.

### Paso 5-1: Obtener Directrices de Código

```
CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "code" }

CallMcpTool: user-pencil / get_guidelines
  arguments: { "topic": "tailwind" }
```

### Paso 5-2: Estructura del Proyecto

```
lp-project/
├── index.html          # HTML principal
├── css/
│   └── style.css       # CSS personalizado (usando Tailwind CDN)
├── js/
│   └── main.js         # Interacciones
├── images/             # Activos de imagen
└── package.json        # Para despliegue en Vercel
```

### Paso 5-3: Puntos de Implementación

- **Tailwind CSS CDN**: Use inmediatamente con `<script src="https://cdn.tailwindcss.com"></script>`
- **Responsivo**: Implemente mobile-first (breakpoints sm: / md: / lg:)
- **Animaciones**: Intersection Observer para elementos que aparecen con fade al hacer scroll
- **Formularios**: Integración con servicios externos como Formspree o Netlify Forms

### Paso 5-4: Verificación en Navegador

Verifique la visualización usando cursor-ide-browser MCP:

```
CallMcpTool: cursor-ide-browser / browser_navigate
  arguments: { "url": "file:///path/to/lp-project/index.html" }
```

---

## Fase 6: Despliegue en Vercel

### Paso 6-1: Instalar Vercel CLI

```bash
npm i -g vercel
```

### Paso 6-2: Despliegue de Vista Previa

```bash
vercel lp-project
```

Se requiere inicio de sesión y configuración del proyecto la primera vez.

### Paso 6-3: Despliegue en Producción

```bash
vercel --prod
```

### Paso 6-4: Dominio Personalizado (Opcional)

```bash
vercel domains add su-dominio.com
```

---

## 3 Niveles de Experiencia

Este skill se puede utilizar en tres niveles:

### Nivel 1: LP Basado en Texto (Principiante)
- Entrevista con AskQuestion
- Diseño de estructura con ASCII WF
- Generar HTML/CSS directamente (sin Pencil)
- Verificar localmente

### Nivel 2: Producción de HP (Intermedio)
- Estructura de múltiples páginas (principal + sub-páginas)
- Implementación de navegación
- WF visual con diagram-generator
- Soporte responsivo

### Nivel 3: Diseño en Pencil → LP (Avanzado)
- Crear diseños profesionales con Pencil MCP
- Conversión de diseño a código
- Animaciones e interacciones
- Publicar con despliegue en Vercel

---

## Skills Relacionados

- **diagram-generator**: Generación de WF y diagramas de estructura
- **nanobanana**: Generación de imagen Hero y OGP
- **banner-creator**: Creación de banners para anuncios en redes sociales
- **screenshot-annotator**: Agregar anotaciones para revisión de diseño
