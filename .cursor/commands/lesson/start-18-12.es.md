---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-11", "output/pm/wireframes.md"]
level: "intermediate"
tags: ["pm", "ui", "design", "pencil-mcp"]
nonInteractiveMode: deferred
---
# 🎓 Lección 18-12: Diseño de UI (Pencil MCP)

| Elemento | Detalles |
|------|------|
| Objetivo | Disenar las pantallas principales de TaskFlow (panel, lista de tareas, detalle de tareas) usando Pencil MCP |
| Duración | ~30 min |
| Habilidades utilizadas | Pencil MCP |
| Requisitos previos | Lección 18-11 completada, output/pm/wireframes.md existe. Pencil MCP esta conectado a Cursor |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

> **💡 Información de la herramienta**: Esta lección utiliza Pencil MCP. Esta disponible en el espacio de trabajo actual, Claude Code (CLI/escritorio) y otros entornos. En algunos entornos como Codex CLI, puede encontrar un error `request_user_input is not supported`. En ese caso, consulte la sección "Flujo de trabajo alternativo".

## 📍 Paso 1: Definición del sistema de diseño

Primero, cree un archivo de diseño en el proyecto usando Pencil MCP:
```bash
mkdir -p output/pm/ui-design
open_document("output/pm/ui-design/taskflow-ui.pen")
```
> **Ubicación de guardado**: `output/pm/ui-design/taskflow-ui.pen`

Defina la paleta de colores base, la tipografía, el espaciado y los estilos de sombra para el diseño. Estos son elementos que se utilizan de manera consistente en todas las pantallas.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el tono de diseno para TaskFlow",
  "options": [
    {
      "label": "Profesional (azul)",
      "value": "professional",
      "description": "Orientado a negocios. Enfatiza confianza y estabilidad. Primario: azul (#0066CC), secundario: gris"
    },
    {
      "label": "Moderno (purpura)",
      "value": "modern",
      "description": "Avanzado y refinado. Enfatiza la innovacion. Primario: purpura (#7C3AED), secundario: indigo"
    },
    {
      "label": "Amigable (verde)",
      "value": "friendly",
      "description": "Accesible y tranquilo. Enfatiza la facilidad de uso. Primario: verde (#10B981), secundario: esmeralda"
    },
    {
      "label": "Personalizado",
      "value": "custom",
      "description": "Especifique su propia paleta de colores"
    }
  ],
  "required": true,
  "hint": "Seleccione segun el posicionamiento de su proyecto para determinar el tono general del diseno"
}
```

### 🚀 Tarea de definición del sistema de diseño

Basandose en el tono seleccionado, defina los siguientes elementos:

#### Paleta de colores
- **Primary Color**: Se usa para acciones principales y elementos importantes
- **Secondary Color**: Se usa para elementos de soporte y acciones secundarias
- **Accent Color**: Se usa para expresiones de estado como advertencias, éxito e información
- **Background Colors**: Fondo principal, fondo secundario (para contenedores)
- **Text Colors**: Texto del cuerpo, encabezados, texto complementario

#### Tipografía
- **Encabezados**: Tamaño de fuente 28px/24px/20px, peso Bold/SemiBold
- **Cuerpo**: Tamaño de fuente 16px/14px, peso Regular
- **Complementario**: Tamaño de fuente 12px, peso Regular, opacidad 70%
- **Fuentes recomendadas**: Inter, Segoe UI o SF Pro Display

#### Reglas de espaciado
- **Unidad base**: 4px
- **Espaciado estándar**: 8px, 12px, 16px, 24px, 32px
- **Dentro de componentes**: 12px - 16px
- **Entre secciones**: 24px - 32px
- **Margenes de página**: 16px (móvil) / 24px (escritorio)

#### Bordes y radio de esquinas
- **Border Radius**: 4px (pequeño) / 8px (mediano) / 16px (grande)
- **Border Color**: neutral-200 / neutral-300
- **Border Width**: 1px estándar

#### Estilos de sombra
- **Soft Shadow**: `0 1px 3px rgba(0,0,0,0.1)`
- **Medium Shadow**: `0 4px 12px rgba(0,0,0,0.15)`
- **Elevated Shadow**: `0 10px 30px rgba(0,0,0,0.2)`

---

## 📍 Paso 2: Diseño de la pantalla del panel

Diseñe el panel de control, la pantalla principal de TaskFlow. Como la primera pantalla que ven los usuarios, debe ser intuitiva con una estructura de información clara.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el diseno del panel de control",
  "options": [
    {
      "label": "Diseno de tarjetas (estadisticas + lista de tareas)",
      "value": "card_layout",
      "description": "Tarjetas de estadisticas + lista de tareas. Equilibrado y mas comun"
    },
    {
      "label": "Diseno Kanban (columnas de estado)",
      "value": "kanban_layout",
      "description": "Muestra tareas en columnas por estado. Gestion visual del progreso facil"
    },
    {
      "label": "Diseno de linea de tiempo",
      "value": "timeline_layout",
      "description": "Muestra tareas cronologicamente. Para gestion de horarios"
    },
    {
      "label": "Obtener sugerencias de IA",
      "value": "ai_suggest",
      "description": "Sugerir diseno optimo basado en la escala y el proposito del proyecto"
    }
  ],
  "required": true,
  "hint": "Seleccione considerando el numero de tareas y el estilo de gestion del proyecto"
}
```

### 🚀 Elementos de diseño del panel de control

#### Area del encabezado (Altura: 56px / 64px)
- Logo/nombre de marca (izquierda)
- Título de página "Panel de control"
- Menu de usuario/notificaciones (derecha)
- Soporte de dispositivos: Visualización compacta en teléfonos móviles

#### Barra lateral (Ancho: 256px / 200px)
- Menu de navegación
  - Panel de control (actual)
  - Lista de tareas
  - Proyectos
  - Equipo
  - Configuración
- Función plegable (soporte móvil)

#### Area de contenido principal
**Tarjetas de estadísticas (Cuadricula: 4 columnas → 2 columnas → 1 columna)**
- Tareas de hoy: 🎯 Valor + barra
- Tasa de finalización: 📊 Porcentaje + progreso circular
- Tareas vencidas: ⚠️ Valor + color de advertencia
- Actividad del equipo: 👥 Cantidad de actividades

**Sección "Tareas de hoy" (Altura: 320px)**
- Controles de filtro/ordenación (arriba)
- Lista de tareas (desplazable)
  - Indicador de prioridad
  - Título de la tarea
  - Avatar del responsable
  - Visualización de fecha de vencimiento
  - Insignia de estado
- Botón "Ver todo"

**Sección de actividad reciente (Altura: 240px)**
- Vista de línea de tiempo
- Elementos de actividad
  - Icono de tipo de acción
  - Información del ejecutor
  - Marca de tiempo (tiempo relativo)

---

## 📍 Paso 3: Diseño de pantallas de lista/detalle de tareas

Diseñe las pantallas principales para la gestión de tareas. Deben mostrar eficientemente grandes cantidades de información de tareas, permitiendo a los usuarios acceder rápidamente a la información que necesitan.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el formato de visualizacion de la lista de tareas",
  "options": [
    {
      "label": "Vista de tabla",
      "value": "table_view",
      "description": "Formato de tabla. Muestra muchas columnas a la vez. Para grandes conjuntos de datos"
    },
    {
      "label": "Vista de tarjetas",
      "value": "card_view",
      "description": "Formato de tarjeta. Informacion visual de tareas. Visualizacion de informacion limitada"
    },
    {
      "label": "Vista Kanban",
      "value": "kanban_view",
      "description": "Columnas por estado. Cambios de estado mediante arrastrar y soltar"
    },
    {
      "label": "Alternancia lista + tarjeta",
      "value": "hybrid_view",
      "description": "Muestra vista de lista y panel de detalle en paralelo. Flexible y con muchas funciones"
    }
  ],
  "required": true,
  "hint": "Seleccione considerando como los usuarios desean gestionar sus tareas"
}
```

### 🚀 Diseño de la pantalla de lista de tareas

#### Barra de operaciones superior (Altura: 56px)
- Título "Lista de tareas"
- Cuadro de busqueda
  - Marcador de posición: "Buscar tareas"
  - Icono de busqueda
- Botón de filtro
  - Estado
  - Prioridad
  - Responsable
  - Fecha de vencimiento
- Menu de ordenación
  - Fecha (más reciente/más antigua)
  - Prioridad
  - Nombre (A-Z)
- Botón de crear nuevo (Botón primario)

#### Panel de filtro/ordenación (expandido)
- Pestanas: Filtro / Ordenación
- Lista de casillas de verificación
- Botón de reinicio
- Botón de aplicar

#### Elementos de la lista de tareas (según el formato seleccionado)

**Para vista de tabla:**
- Encabezados de columna: ☑️ | Nombre de tarea | Prioridad | Responsable | Fecha límite | Estado | Acciones
- Altura de fila: 48px
- Efecto hover: Cambio de color de fondo + visualización del menu de acciones
- Selección: Casilla de verificación
- Iconos ↑↓ en columnas ordenables

**Para vista de tarjetas:**
- Diseño de cuadricula (3 columnas → 2 columnas → 1 columna)
- Contenido de la tarjeta:
  - Nombre de la tarea (negrita)
  - Descripción (1-2 líneas)
  - Etiquetas
  - Insignia de prioridad
  - Avatar del responsable
  - Fecha/hora de vencimiento
  - Insignia de estado
  - Al pasar el cursor: Acciones rapidas (editar, eliminar, compartir)

**Para vista Kanban:**
- Columnas de estado (Sin asignar / Planificado / En progreso / Revisión / Completado)
- Encabezado de cada columna: Nombre del estado + cantidad de tareas
- Area de arrastrar y soltar
- Visualización de tarjetas (igual que la vista de tarjetas)
- Botón "Agregar nuevo" (parte inferior de la columna)

**Para alternancia lista + tarjeta:**
- Panel izquierdo: Lista de tareas (visualización estrecha)
- Panel derecho: Visualización detallada de la tarea seleccionada
- Redimensionador (ajuste de ancho del panel)
- Actualización en tiempo real al seleccionar elementos en el panel izquierdo

#### Paginación (parte inferior)
- Visualización de información de página (ej: 1-25 de 127)
- Selección de cantidad de páginas
- Botones Anterior / Siguiente

---

### 📍 Diseño de la pantalla de detalle de tarea

#### Diseño
- **Visualización de página completa**: Usa todo el navegador (pantallas grandes)
- **Modal/panel lateral**: Se muestra sobre la lista existente (pantallas pequeñas a medianas)

#### Sección del encabezado (Altura: 72px)
- Nombre de la tarea (editable)
- Insignia de prioridad
- Desplegable de estado
- Botón "×" cerrar / botón atras

#### Contenido principal (desplazable)

**Sección de información básica**
- Nombre de la tarea
- Descripción/notas (compatible con Markdown)
- Selector de prioridad
- Estado
- Responsable
- Fecha/hora de vencimiento

**Sección de información detallada**
- Proyecto
- Etiquetas
- Esfuerzo estimado
- Tasa de finalización
- Tarea padre (si existe)
- Tareas relacionadas

**Sección de archivos adjuntos**
- Area de carga
- Lista de archivos

**Sección de actividad/comentarios**
- Vista de línea de tiempo
- Campo de entrada de comentarios
- Visualización de comentarios existentes

#### Barra lateral (derecha)
- Lista de verificación (subtareas)
- Información del responsable
- Seguimiento del tiempo
- Enlaces relacionados

#### Barra de acciones inferior
- Botón de eliminar
- Botón de cancelar
- Botón de guardar (primario)

---

## 📍 Paso 4: Revisión de diseño

Verifique que el diseño creado cumpla con los requisitos y sea de alta calidad.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione la perspectiva de revision del diseno",
  "options": [
    {
      "label": "Consistencia de UI",
      "value": "consistency",
      "description": "Verificar la consistencia de colores, tipografia y formas de componentes"
    },
    {
      "label": "Accesibilidad",
      "value": "accessibility",
      "description": "Verificar soporte para daltonismo, relacion de contraste y operacion con teclado"
    },
    {
      "label": "Usabilidad",
      "value": "usability",
      "description": "Verificar facilidad de operacion, facilidad de busqueda de informacion y eficiencia del flujo de tareas"
    },
    {
      "label": "Todos",
      "value": "all",
      "description": "Verificar las 3 perspectivas anteriores (mas recomendado)"
    }
  ],
  "required": true,
  "hint": "Se recomienda seleccionar 'Todos' para una mayor calidad"
}
```

### 🚀 Lista de verificación de consistencia de UI

- [ ] La paleta de colores es consistente en todas las pantallas
  - Uso del Primary Color (botones, elementos de énfasis)
  - Uso del Secondary Color (fondos, elementos auxiliares)
  - Los colores de advertencia/error/éxito estan estandarizados
- [ ] Las especificaciones de fuente son consistentes
  - Los encabezados siempre son Bold/SemiBold
  - El texto del cuerpo siempre es Regular
  - Se usan los tamaños estándar 28/24/20/16/14/12px
- [ ] El espaciado (margen/relleno) es en multiplos de 4px
  - Dentro de componentes: 12px / 16px
  - Entre secciones: 24px / 32px
- [ ] Las formas de los componentes son consistentes
  - Botones: Misma altura (44px / 40px), mismo radio de borde (8px)
  - Tarjetas: Mismo radio de borde (8px), misma sombra
  - Campos de entrada: Misma altura (40px), mismo estilo de borde
- [ ] Los iconos son consistentes
  - Mismo conjunto de iconos (Material Icons / Heroicons, etc.)
  - Mismo tamaño (16px / 20px / 24px)
  - Mismo peso de trazo

### ⚠️ Lista de verificación de accesibilidad

- [ ] La relación de contraste cumple con los estándares WCAG AA
  - Texto: Mínimo 4.5:1 (texto normal) / 3:1 (texto grande)
  - Elementos gráficos: Mínimo 3:1
  - Especialmente verifique las combinaciones de color de fondo y texto
- [ ] La información no se transmite solo por color
  - Prioridad: Color + icono + texto
  - Estado: Color + insignia + etiqueta
  - Errores: Color + icono + texto del mensaje
- [ ] Los estados de enfoque son claramente visibles
  - Los estados hover/enfoque de los botones son visibles
  - Los indicadores de enfoque son claros (contorno, etc.)
- [ ] Los tamaños de texto son suficientes
  - Cuerpo: Mínimo 14px
  - Subtitulos: Mínimo 12px (aunque se debe evitar)
- [ ] Los tamaños de objetivo de elementos interactivos son suficientes
  - Botones: Mínimo 44px x 44px (objetivo tactil)
  - Enlaces: Mínimo 16px de altura

### ✅ Lista de verificación de usabilidad

- [ ] Las tareas principales del usuario se pueden realizar eficientemente
  - Busqueda de tareas: Dentro de 3 clics
  - Creación de tareas: Dentro de 4 pasos
  - Edición de tareas: Edición en línea directa posible
  - Cambio de estado: Un clic (kanban)
- [ ] La jerarquía de información es clara
  - La información más importante (nombre de tarea, estado) es fácilmente visible
  - La información secundaria (fecha límite, responsable) tiene un tamaño adecuado
  - La información complementaria (fecha de creación, etc.) es discreta
- [ ] La ubicación de acciones (botones) es lógica
  - Las acciones primarias (guardar, crear) estan en la posición inferior derecha o prominente
  - Las acciones destructivas (eliminar) usan color de advertencia + diálogo de confirmación
  - Las acciones secundarias (cancelar) estan en el lado izquierdo
- [ ] El manejo de errores es claro
  - Los errores de validación se muestran directamente debajo del campo de entrada
  - Los mensajes de error son específicos e incluyen soluciones
  - Expresado con color + icono + texto
- [ ] La retroalimentación responsiva es inmediata
  - Clic de botón: Cambio visual (color, animación)
  - Envio de datos: Visualización de estado de carga
  - Error: Visualización de advertencia (dentro de 300ms)
- [ ] Consistencia con los wireframes
  - El diseño del panel de control coincide con wireframes.md
  - El diseño de la lista de tareas cumple con las especificaciones
  - Todos los elementos requeridos (filtro, busqueda, etc.) estan incluidos

---

## ✅ Entregables

Archivos y formatos creados en esta lección:

### Archivos .pen (gestionados por Pencil MCP)
- `dashboard.pen` - Diseño de pantalla del panel de control
- `task-list.pen` - Diseño de pantalla de lista de tareas
- `task-detail.pen` - Diseño de pantalla de detalle de tarea
- `design-system.pen` - Sistema de diseño (colores, tipografía, componentes)

### Documentos (referencia)
- `output/pm/design-system.md` - Especificación del sistema de diseño
  - Definición de paleta de colores (códigos HEX/RGB)
  - Reglas de tipografía
  - Reglas de espaciado
  - Especificaciones de diseño de componentes
  - Pautas de accesibilidad

---

## 🚀 Pasos de implementación

### 1. Verificar la conexión de Pencil MCP
```bash
cursor /pencil status
```
- Status: Connected
- Versión: 1.0+

### 2. Crear el sistema de diseño
```bash
cursor /pencil create-system \
  --name "TaskFlow" \
  --primary "#0066CC" \
  --secondary "#F3F4F6" \
  --accent "#EF4444"
```

### 3. Crear el diseño de cada pantalla
- Panel de control: `/pencil design-screen dashboard --layout card_layout`
- Lista de tareas: `/pencil design-screen task-list --layout table_view`
- Detalle de tarea: `/pencil design-screen task-detail --layout full-page`

### 4. Diseño de componentes (elementos reutilizables)
- Button（Primary / Secondary / Danger）
- Input Field
- Card
- Badge
- Avatar
- Dialog / Modal
- Dropdown
- Tabs

### 5. Exportar
```bash
cursor /pencil export --format png --output output/pm/designs/
cursor /pencil export --format figma --output output/pm/designs/figma-link
```

---

## 🔄 Flujo de trabajo alternativo (para entornos sin GUI)

En entornos donde Pencil MCP no esta disponible (Claude Code, Codex CLI, SSH, etc.), cree maquetas de UI directamente con HTML + Tailwind CSS.

1. Consulte `output/pm/wireframes.md` para verificar los requisitos de diseño
2. Escriba la definición del sistema de diseño del Paso 1 en Markdown en `output/pm/design-system.md`
3. Implemente cada pantalla (panel de control, lista de tareas, detalle de tarea) con HTML + Tailwind CSS CDN:
   ```bash
   mkdir -p output/pm/designs
   ```
4. Cree `output/pm/designs/dashboard.html`, `task-list.html`, `task-detail.html`
5. Tome capturas de pantalla con Playwright y guardelas como PNG:
   ```bash
   npx playwright screenshot output/pm/designs/dashboard.html output/pm/designs/dashboard.png
   ```
6. La lista de verificación de revisión de diseño del Paso 4 se puede aplicar tal cual

> Los archivos HTML seran los entregables en lugar de archivos .pen. Puede continuar directamente a la Lección 18-13.

---

## ⚠️ Solución de problemas comunes

### Pencil MCP no esta conectado
**Causa**: La extensión de Cursor no esta cargada

**Solución**:
1. Verifique MCP en la configuración de Cursor: Settings > Extensions > Pencil MCP
2. Reiniciar: `cursor restart`
3. Prueba de conexión: `cursor /pencil status`

### No sabe como editar el diseño
**Pasos de referencia**:
1. Haga clic derecho en el componente relevante en Pencil
2. Seleccione "Edit"
3. Ajuste color/tamaño/ubicación en el panel de propiedades
4. Verifique en la vista previa
5. Save（Ctrl+S）

### Como elegir una paleta de colores
**Criterios de decisión**:
- **Profesional**: Para B2B/empresarial, financiero, herramientas de gestión de negocios
- **Moderno**: SaaS, startups, enfocado en innovación
- **Amigable**: Orientado al consumidor, aprendizaje/educación, salud
- **Personalizado**: Cuando hay colores de marca existentes

### Diferencias con los wireframes
**Puntos de verificación**:
- Abra `output/pm/wireframes.md`
- Verifique si el diseño de cada sección coincide con el diseño
- Si hay discrepancias, priorice los wireframes para las correcciones

### Reutilización de componentes
**Método recomendado**:
1. Abra "Library" en Pencil
2. Arrastre componentes predefinidos (botones, tarjetas, etc.)
3. Use los mismos componentes en multiples pantallas
4. Todas las pantallas se actualizan automáticamente cuando se actualizan los componentes

---

## 📍 Punto de control

Una vez completados los siguientes elementos, esta lección esta completa:

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "title": "Sistema de diseno definido",
      "description": "La paleta de colores, la tipografia y las reglas de espaciado estan guardadas en .pen",
      "verification": "cursor /pencil list-components | grep 'design-system'"
    },
    {
      "title": "Diseno de pantalla del panel de control completado",
      "description": "Se incluyen encabezado, barra lateral, tarjetas de estadisticas, lista de tareas y seccion de actividad",
      "verification": "ls output/pm/designs/dashboard.png"
    },
    {
      "title": "Diseno de pantalla de lista de tareas completado",
      "description": "Se incluyen filtro, ordenacion, visualizacion de tareas (formato seleccionado) y paginacion",
      "verification": "ls output/pm/designs/task-list.png"
    },
    {
      "title": "Diseno de pantalla de detalle de tarea completado",
      "description": "Se incluyen informacion de tarea, actividad/comentarios, barra lateral y acciones",
      "verification": "ls output/pm/designs/task-detail.png"
    },
    {
      "title": "Archivos .pen guardados",
      "description": "dashboard.pen, task-list.pen, task-detail.pen, design-system.pen estan todos guardados en Pencil MCP",
      "verification": "cursor /pencil list-files | wc -l >= 4"
    }
  ]
}
```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/ui-design/
├── taskflow-ui.pen       ← Archivo de diseno Pencil (principal)
├── dashboard.png         ← Captura de pantalla del panel de control
├── task-list.png         ← Captura de pantalla de lista de tareas
└── task-detail.png       ← Captura de pantalla de detalle de tarea
```

### Comandos de verificación
```bash
# Verificar archivos .pen y capturas de pantalla
ls -lh output/pm/ui-design/

# Abrir imagenes (macOS: open / Linux: xdg-open)
open output/pm/ui-design/
```

> 💡 **Claude Code**: `Read output/pm/ui-design/dashboard.png` para vista previa en el chat
> 💡 **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar
> 💡 **Archivos .pen**: Puede verificar el contenido con `batch_get` o `get_screenshot` de Pencil MCP

---

## ➡️ Siguientes pasos

Después de completar esta lección, continue con **Lección 18-13: Prototipo HTML + Tailwind CSS**.

Convierta los diseños creados con Pencil MCP en código real:

- Crear estructura HTML
- Estilizado con Tailwind CSS
- Diseño responsivo (móvil / tableta / escritorio)
- Implementación de interacciones (hover, clic, animación)

**Iniciar**: `cursor /lesson start-18-13`

---

## 📚 Referencias

- [Documentación de Pencil MCP](https://pencil.dev/docs)
- [Mejores prácticas de sistemas de diseño](https://www.designsystems.com/)
- [Pautas de accesibilidad WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [Colección de componentes Tailwind CSS](https://tailwindui.com/)
- [Pautas de Material Design 3](https://m3.material.io/)
