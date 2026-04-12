---
description: "When the user says /start-13-3 — Module 13 Lesson 13-3: Diseño de Landing Page - Creación de archivo de diseño con Pencil"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-2", "setup-pencil"]
duration: "~30 min"
level: "intermediate"
tags: ["lp", "pencil", "design", "mockup"]
---

# 🎓 Lección 13-3: Creación de archivo de diseño (Pencil MCP)

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 13-3: Creación de archivo de diseño**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear un archivo de diseño (.pen) de Landing Page/sitio web usando Pencil MCP |
| Duración | ~30 min |
| Habilidades utilizadas | lp-designer, Pencil MCP (user-pencil) |
| Requisitos previos | Lección 13-2 completada (output/lp-wireframe.txt existe), Pencil MCP configurado (/setup-pencil) |
| Página del curso | Consulte [Módulo 13: Diseño de Landing Page/Sitio web](https://ai-agent.camp/es/course/module-13) en paralelo |

> **💡 Información de herramientas**: Esta lección usa Pencil MCP. Está disponible en el espacio de trabajo actual y en Claude Code (CLI/Escritorio). En algunos entornos cómo Codex CLI, puede aparecer un error `request_user_input is not supported`. En ese caso, consulte la sección "Flujo de trabajo alternativo".

**Flujo de la sesión:**
1. Crear archivo de diseño en `output/lp/lp-design.pen` con Pencil
2. Obtener las guías de diseño de Landing Page
3. Aplicar la guía de estilo
4. Crear el diseño de cada sección
5. Revisar el diseño y exportar capturas de pantalla

Al finalizar la sesión, un archivo de diseño de calidad profesional estará completó.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar. Las respuestas pueden pausarse dependiendo de la herramienta, pero no es un error.

---

## 🎯 Verificación de preparación

Primero, confirmemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la página del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Paso 1)
(check_prereq → Verificar conexión de Pencil MCP)
(view_html → Mostrar la ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Paso 1: Crear nuevo documento Pencil

Crear un nuevo archivo .pen con Pencil MCP.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Crear documento Pencil",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Cree un nuevo documento para diseño de Landing Page con Pencil MCP.

Pasos:
1. Crear directorio de destino con mkdir -p output/lp
2. Verificar estado actual con get_editor_state()
3. Crear archivo .pen con open_document("output/lp/lp-design.pen")
4. Confirmar que el archivo está abierto

Destino: output/lp/lp-design.pen
```

**Resultado esperado**: Se crea y abre un archivo de diseño en `output/lp/lp-design.pen`.

---

## 🚀 Paso 2: Obtener guías de diseño de Landing Page

Obtener las guías de diseño de Landing Page de Pencil.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Guías de diseño",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Obtenga las guías de diseño de Landing Page de Pencil MCP.

Pasos:
1. Obtener reglas de diseño de LP con get_guidelines(topic="landing-page")
2. Resumir los puntos clave de las guías
3. Destacar las reglas especialmente importantes (diseño, tipografía, color)

Seguiremos estas guías para el diseño.
```

**Resultado esperado**: Se muestran las reglas de diseño y mejores prácticas de Landing Page.

---

## 🚀 Paso 3: Aplicar guía de estilo

Seleccionar y aplicar una guía de estilo que coincida con el tono de diseño.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Selección de guía de estilo",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Lea el tono de diseño de output/lp-brief.md y aplique una guía de estilo
usando Pencil MCP.

Pasos:
1. Obtener lista de etiquetas con get_style_guide_tags
2. Seleccionar etiquetas que coincidan con el tono de diseño del brief
3. Obtener estilo con get_style_guide(tags=["landing-page", "{tono}", "{categoría}"])
4. Revisar la paleta de colores, fuentes y patrones de diseño del estilo

Resuma la vista general del estilo seleccionado.
```

**Resultado esperado**: Se aplica una guía de estilo que coincide con el tono de diseño.

---

## 🚀 Paso 4: Creación del diseño de secciones

Crear cada sección usando batch_design.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Diseño de secciones",
  "questions": [{
    "id": "design_approach",
    "prompt": "Seleccione el enfoque de diseño",
    "options": [
      {"id": "all_at_once", "label": "Crear todas las secciones a la vez"},
      {"id": "step_by_step", "label": "Crear una sección a la vez con revisión"},
      {"id": "hero_first", "label": "Crear solo la sección Hero primero"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Consulte output/lp-brief.md y output/lp-wireframe.txt,
y cree el diseño de la Landing Page usando batch_design de Pencil MCP.

Cree las siguientes secciones en orden:

1. **Sección Hero**
   - Fondo: degradado o imagen
   - Titular (H1): Usar copy del brief
   - Subtítulo
   - Botón CTA (color prominente, esquinas redondeadas)
   - Imagen Hero o maqueta

2. **Sección Pain Points**
   - Título de sección
   - 3 tarjetas de desafíos (icono + texto)

3. **Sección Solution**
   - Izquierda: texto explicativo (3 beneficios)
   - Derecha: captura de pantalla del servicio o ilustración

4. **Sección Features**
   - Título de sección
   - 3-4 tarjetas de características (icono + título + descripción)

5. **Sección Social Proof**
   - Tarjetas de testimonios (foto + nombre + empresa + comentario)
   - Calificación con estrellas

6. **Sección FAQ**
   - Q&A en formato acordeón, 3-5 elementos

7. **Sección Final CTA**
   - Color de fondo
   - Titular + botón CTA

8. **Footer**
   - Grupos de enlaces + copyright

Verifique cada sección con get_screenshot después de la creación.
```

**Resultado esperado**: Se completa un archivo .pen con todas las secciones diseñadas.

---

## 🚀 Paso 5: Revisión y ajuste del diseño

Revisar visualmente el diseño completado.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 5: Revisión del diseño",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Obtenga una captura de pantalla del diseño completo con get_screenshot de Pencil MCP
y revise desde las siguientes perspectivas:

1. **Consistencia**: ¿Los colores, fuentes y espaciado coinciden con la guía de estilo?
2. **Jerarquía visual**: ¿Los titulares son prominentes y los CTAs son fáciles de encontrar?
3. **Espacios en blanco**: ¿El espaciado entre secciones es apropiado?
4. **Contraste**: ¿La legibilidad del texto es suficiente?
5. **CTA**: ¿Los botones son prominentes e invitan a hacer clic?

Si hay problemas, corrija con batch_design y verifique nuevamente con get_screenshot.

Finalmente, guarde una captura de pantalla del diseño completado:
1. mkdir -p output/lp/design
2. Obtener captura de pantalla de página completa con get_screenshot()
3. Guardar en output/lp/design/lp-full.png
```

**Resultado esperado**: El diseño es revisado, ajustado, y una captura de pantalla se guarda en `output/lp/design/lp-full.png`.

---

## 🔄 Flujo de trabajo alternativo (para entornos sin GUI)

En entornos dónde Pencil MCP no está disponible (Claude Code, Codex CLI, SSH, etc.), cree la maqueta de diseño directamente con HTML + Tailwind CSS.

1. Consulte `output/lp-wireframe.txt` y `output/lp-brief.md` para confirmar los requisitos de diseño
2. Implemente la maqueta directamente con HTML + Tailwind CSS CDN en `output/lp-project/`:
   ```bash
   mkdir -p output/lp-project
   ```
3. Cree cada sección (Hero, Pain Points, Solution, Features, Social Proof, FAQ, CTA, Footer) en HTML
4. Aplique colores, fuentes y espaciado equivalentes a la guía de estilo con clases de utilidad de Tailwind
5. Use el archivo HTML completado cómo entregable en lugar de un archivo .pen, y proceda directamente a 13-4

> Con esté método, puede omitir los pasos de "requisito de archivo .pen" en 13-4 y trabajar directamente en la implementación HTML.

---

## ⚠️ Problemas comunes y soluciones

En Codex, normalmente se presentan opciones en el chat para que el usuario seleccione su problema y reciba orientación al instante.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "No puedo conectar con Pencil MCP"},
      {"id": "trouble_2", "label": "batch_design da error"},
      {"id": "trouble_3", "label": "No se encuentra la guía de estilo"},
      {"id": "trouble_4", "label": "El diseño se ve roto"}
    ]
  }]
}
```

### Problema 1: No puedo conectar con Pencil MCP
**Solución**: Verifique que user-pencil esté habilitado en la configuración MCP de Cursor. Puede verificar en Configuración → MCP Servers.

### Problema 2: batch_design da error
**Solución**: Verifique que la sintaxis de la operación sea correcta. Puede obtener las reglas de sintaxis más recientes con `get_guidelines`.

### Problema 3: No se encuentra la guía de estilo
**Solución**: Verifique las etiquetas disponibles con `get_style_guide_tags` y seleccione la más cercana.

### Problema 4: El diseño se ve roto
**Solución**: Verifique la estructura del diseño con `snapshot_layout` y ajuste la ubicación de los nodos.

---

## ✅ Punto de control
- [ ] `output/lp/lp-design.pen` ha sido creado
- [ ] Las guías de diseño de Landing Page han sido revisadas
- [ ] La guía de estilo ha sido aplicada
- [ ] Todas las secciones (Hero hasta Footer) están diseñadas
- [ ] Captura de pantalla guardada en `output/lp/design/lp-full.png`


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/lp/
├── lp-design.pen          ← Archivo de diseño Pencil (principal)
└── design/
    └── lp-full.png        ← Captura de pantalla del diseño
```

### Comandos de verificación
```bash
# Verificar existencia del archivo .pen
ls -lh output/lp/lp-design.pen

# Verificar capturas de pantalla
ls -la output/lp/design/

# Abrir imagen (macOS: open / Linux: xdg-open)
open output/lp/design/lp-full.png
```

> 💡 **Claude Code**: `Read output/lp/design/lp-full.png` para vista previa en el chat
> 💡 **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar
> 💡 **Archivo .pen**: Use `batch_get` o `get_screenshot` de Pencil MCP para inspeccionar el contenido

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat para verificar la finalización:

```text
Verifique si existen los siguientes archivos:
1. output/lp/lp-design.pen (archivo de diseño Pencil)
2. output/lp/design/lp-full.png (captura de pantalla)

También, verifique el estado actual del documento con get_editor_state()
y muestre una lista de las secciones (nodos) creados.
```

**Resultado esperado**: Se confirma la existencia del archivo .pen y la captura de pantalla, y se muestra la lista de elementos de diseño.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar.

En Codex, normalmente puede seleccionar entre opciones en el chat.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione qué hacer a continuación",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (Implementación de LP)"},
      {"id": "next_window", "label": "Abrir /start-13-4 en una nueva ventana"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → Ejecutar /start-13-4
- next_window → Abrir /start-13-4 en una nueva ventana
- finish → Finalizar
