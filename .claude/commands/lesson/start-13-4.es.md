---
description: "When the user says /start-13-4 — Module 13 Lesson 13-4: Diseño de Landing Page - Crear una Landing Page funcional"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-3"]
duration: "~30 min"
level: "intermediate"
tags: ["lp", "html", "tailwind", "implementation"]
---

# 🎓 Lección 13-4: Crear una Landing Page funcional (HTML/CSS/JS)

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 13-4: Implementación de Landing Page**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Convertir el diseño de Pencil en una Landing Page funcional con HTML/CSS(Tailwind)/JS |
| Duración | ~30 min |
| Habilidades utilizadas | lp-designer, Pencil MCP (guías de code/tailwind), cursor-ide-browser |
| Requisitos previos | Lección 13-3 completada (archivo de diseño .pen existe) |
| Página del curso | Consulte [Módulo 13: Diseño de Landing Page/Sitio web](https://ai-agent.camp/es/course/module-13) en paralelo |

> **💡 Información de herramientas**: Esta lección usa Pencil MCP. Está disponible en el espacio de trabajo actual y en Claude Code (CLI/Escritorio). En algunos entornos cómo Codex CLI, puede aparecer un error `request_user_input is not supported`. En ese caso, consulte la sección "Flujo de trabajo alternativo".

**Flujo de la sesión:**
1. Obtener las guías de conversión a código
2. Crear la estructura del proyecto
3. Implementar HTML/CSS(Tailwind)/JS
4. Agregar diseño responsive y animaciones
5. Verificar en el navegador

Al finalizar la sesión, una Landing Page/sitio web que funciona en el navegador estará completa.

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
(check_prereq → Verificar existencia del archivo .pen)
(view_html → Mostrar la ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Paso 1: Obtener guías de conversión a código

Obtener las guías para convertir diseños de Pencil a código.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Guías de conversión a código",
  "questions": [{
    "id": "tech_stack",
    "prompt": "Seleccione el stack tecnológico para la implementación",
    "options": [
      {"id": "tailwind", "label": "HTML + Tailwind CSS (recomendado, CDN)"},
      {"id": "vanilla", "label": "HTML + CSS puro"},
      {"id": "react", "label": "React + Tailwind CSS"},
      {"id": "nextjs", "label": "Next.js + Tailwind CSS"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Obtenga las guías de conversión a código de Pencil MCP.

Pasos:
1. Obtener guías de codificación con get_guidelines(topic="code")
2. Obtener reglas específicas de Tailwind con get_guidelines(topic="tailwind")
3. Cargar el diseño del archivo .pen con batch_get
4. Resumir el enfoque de conversión de diseño a código

Verificar específicamente:
- Códigos de color (convertir a nombres de clase de Tailwind)
- Tamaños de fuente (mapeo a text-sm, text-lg, etc.)
- Espaciado/márgenes (mapeo a p-4, m-8, etc.)
- Estructura de diseño (uso de flex, grid)
```

**Resultado esperado**: La información necesaria para la conversión a código está organizada.

---

## 🚀 Paso 2: Crear estructura del proyecto

Crear la estructura de archivos para la Landing Page.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Estructura del proyecto",
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
Cree la estructura del proyecto para la Landing Page.

Creación de directorios:
mkdir -p output/lp-project/images
mkdir -p output/lp-project/css
mkdir -p output/lp-project/js

Creación de archivos:
- output/lp-project/index.html   # HTML principal
- output/lp-project/css/style.css # CSS personalizado
- output/lp-project/js/main.js   # Interacciones
- output/lp-project/package.json  # Para despliegue en Vercel

Contenido de package.json:
{
  "name": "lp-project",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "npx serve ."
  }
}
```

**Resultado esperado**: Se crea la estructura del proyecto de Landing Page.

---

## 🚀 Paso 3: Implementar HTML/CSS(Tailwind)/JS

Implementar el código basándose en el diseño de Pencil.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Implementación del código",
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
Implemente output/lp-project/index.html basándose en el archivo .pen de Pencil
y output/lp-brief.md.

Requisitos:
1. Usar Tailwind CSS CDN
   <script src="https://cdn.tailwindcss.com"></script>

2. Estructura de secciones (basada en output/lp-brief.md):
   - Header: Logo + Nav + Botón CTA (header fijo)
   - Hero: Titular + Subtítulo + CTA + Imagen Hero
   - Pain Points: Tarjetas de iconos en 3 columnas
   - Solution: 2 columnas (texto + imagen)
   - Features: Tarjetas de características en 3-4 columnas
   - Social Proof: Testimonios (carrusel o cuadrícula)
   - FAQ: Formato de acordeón
   - Final CTA: Sección CTA con color de fondo
   - Footer: Grupos de enlaces + copyright

3. Reproducción fiel del diseño:
   - Usar colores y fuentes de la guía de estilo de Pencil
   - Ajustar espaciado y márgenes al diseño
   - Estilos de botones (esquinas redondeadas, efectos hover)

4. Diseño responsive:
   - Mobile-first (sm: → md: → lg:)
   - 1 columna en móvil, 2-4 columnas en escritorio

5. OGP y metaetiquetas:
   - Configurar title, description, og:image

Implemente con un diseño hermoso y moderno.
```

**Resultado esperado**: Se implementa HTML/CSS/JS completó.

---

## 🚀 Paso 4: Agregar animaciones e interacciones

Agregar animaciones de scroll e interacciones.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Agregar animaciones",
  "questions": [{
    "id": "animation_level",
    "prompt": "Seleccione el nivel de animación",
    "options": [
      {"id": "minimal", "label": "Mínimo (solo efectos hover)"},
      {"id": "standard", "label": "Estándar (fade-in con scroll + hover)"},
      {"id": "rich", "label": "Rico (parallax + contador + slide-in)"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Agregue animaciones a output/lp-project/js/main.js.

Funcionalidades a agregar:
1. Fade-in con scroll (Intersection Observer)
   - Cada sección aparece con fade-in al entrar al viewport
   - Animación: opacity 0→1, translateY 20px→0

2. Scroll suave
   - Scroll suave al hacer clic en enlaces de navegación

3. Acordeón de FAQ
   - Expandir/colapsar respuestas al hacer clic en la pregunta

4. Header fijo
   - Agregar sombra al header al hacer scroll

5. CSS personalizado (output/lp-project/css/style.css)
   - Variables CSS y keyframes para animaciones
   - Soporte de modo oscuro (opcional)

Implementar con JS puro, sin bibliotecas externas.
```

**Resultado esperado**: Se agregan animaciones e interacciones.

---

## 🚀 Paso 5: Verificar en el navegador

Verificar la Landing Page creada en un navegador.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 5: Verificación en el navegador",
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
Verifique la Landing Page creada en un navegador.

Pasos:
1. Iniciar servidor local
   cd output/lp-project && npx serve .

2. Abrir http://localhost:3000 en un navegador
   (Usando cursor-ide-browser MCP)

3. Verificar lo siguiente:
   - Vista de escritorio (ancho 1280px)
   - Vista móvil (ancho 375px)
   - Comportamiento de animaciones
   - Clics en el botón CTA
   - Comportamiento del acordeón FAQ
   - Scroll suave

4. Corregir cualquier problema

Guarde capturas de pantalla de los resultados de verificación.
```

**Resultado esperado**: Se confirma que la Landing Page funciona correctamente en el navegador.

---

## 🔄 Flujo de trabajo alternativo (para entornos sin GUI)

En entornos dónde Pencil MCP no está disponible (Claude Code, Codex CLI, SSH, etc.), cree HTML directamente sin archivo .pen.

1. Si creó una maqueta HTML con el flujo de trabajo alternativo en 13-3, proceda directamente al Paso 2 en adelante de está lección
2. Consulte `output/lp-brief.md` y `output/lp-wireframe.txt` para confirmar las especificaciones de diseño
3. Omita la parte de Pencil MCP del Paso 1 "Guías de conversión a código" y consulte la documentación de Tailwind CSS en su lugar
4. Los Pasos 3 en adelante (implementación HTML/CSS/JS, animaciones, verificación en navegador) se pueden realizar tal cuál

> Incluso sin archivo .pen, puede implementar directamente desde el wireframe y el brief usando HTML + Tailwind CSS.

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
      {"id": "trouble_1", "label": "Tailwind CSS no funciona"},
      {"id": "trouble_2", "label": "El diseño responsive está roto"},
      {"id": "trouble_3", "label": "Las animaciones no funcionan"},
      {"id": "trouble_4", "label": "Las imágenes no se muestran"}
    ]
  }]
}
```

### Problema 1: Tailwind CSS no funciona
**Solución**: Verifique que `<script src="https://cdn.tailwindcss.com"></script>` esté dentro de `<head>`.

### Problema 2: El diseño responsive está roto
**Solución**: Verifique que exista `<meta name="viewport" content="width=device-width, initial-scale=1.0">`. Confirme que los breakpoints de Tailwind (sm: md: lg:) se usan correctamente.

### Problema 3: Las animaciones no funcionan
**Solución**: Verifique que `main.js` se carga correctamente. Coloque `<script src="js/main.js" defer></script>` antes de `</body>`.

### Problema 4: Las imágenes no se muestran
**Solución**: Verifique que las rutas de imágenes sean rutas relativas correctas. Confirme que los archivos existen en el directorio `images/`.

---

## ✅ Punto de control
- [ ] Las guías de conversión a código han sido obtenidas
- [ ] La estructura del proyecto está creada
- [ ] index.html está completó
- [ ] El diseño responsive está implementado
- [ ] Las animaciones funcionan
- [ ] Verificado en el navegador


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/lp/
├── index.html  (Landing Page)
├── style.css
└── assets/
```

### Comandos de verificación
```bash
# Lista de archivos
ls -lh output/lp/

# Abrir en el navegador (macOS: open / Linux: xdg-open)
open output/lp/index.html
```

> 💡 Verificar estructura HTML: `head -30 output/lp/index.html`

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```text
Muestre la lista de archivos de output/lp-project/,
y verifique el número de secciones y el tamaño del archivo index.html.
```

**Resultado esperado**: Se muestra la lista de archivos del proyecto y sus tamaños.

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
      {"id": "next_auto", "label": "Iniciar la siguiente sección (Despliegue en Vercel)"},
      {"id": "next_window", "label": "Abrir /start-13-5 en una nueva ventana"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_auto → Ejecutar /start-13-5
- next_window → Abrir /start-13-5 en una nueva ventana
- finish → Finalizar
