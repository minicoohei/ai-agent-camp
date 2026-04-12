---
description: "When the user says /start-17-4 — Module 17 Lesson 17-4: Mockups de Diseño con Pencil MCP"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "~35 min"
prerequisites: ["start-17-3"]
level: "intermediate"
tags: ["marketing", "pencil", "design", "mockup"]
---

# Lección 17-4: Mockups de Diseño con Pencil MCP

## Lo Qué Hará en Esta Sesion

Bienvenido a **Lección 17-4: Mockups de Diseño con Pencil MCP**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear mockups de diseño de banners de marketing con Pencil MCP |
| Duración | ~35 min |
| Habilidades utilizadas | Pencil MCP (get_editor_state, batch_design, get_screenshot) |
| Requisitos previos | Pencil MCP habilitado |
| Página del curso | Consulte [Module 17: Marketing](https://ai-agent.camp/es/course/module-17) en paralelo |

> **Información de herramientas**: Esta lección utiliza Pencil MCP. Esta disponible tanto en Cursor IDE cómo en Claude Code (CLI/escritorio). En algunos entornos cómo Codex CLI, puede aparecer el error `request_user_input is not supported`. En ese caso, consulte la sección "Flujo de trabajo alternativo".

**Flujo de la sesion:**
1. Comprender las operaciones básicas de Pencil MCP (get_editor_state, batch_design)
2. Crear un mockup de banner publicitario
3. Capturar con get_screenshot y guardar en output/pencil/

Al finalizar está sesion, estarán completos 1 mockup de diseño de banner y 1 captura de imagen.

> **Consejo**: Si la respuesta de la IA se detiene a mitad, escriba "por favor continue" para reanudar.

---

## Verificación de Preparación

Primero, confirmemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Está listo?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la pagina del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra leccion"}
    ]
  }]
}
```

(ready -> Ir al Paso 1)
(check_prereq -> Ejecutar verificación de requisitos previos)
(view_html -> Mostrar la ruta de la página del curso)
(different_lesson -> Mostrar lista de modulos)

---

## Paso 1: Comprender las Operaciones Basicas de Pencil MCP

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 1: Comprender las operaciones basicas de Pencil MCP",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones (ejemplo)**:
```
Explique las operaciones basicas de Pencil MCP. Describa el uso de las siguientes herramientas:

1. get_editor_state() - Obtener el estado actual del editor
2. open_document() - Crear un nuevo documento / abrir uno existente
3. batch_design() - Insertar, actualizar y eliminar elementos de diseno
   - I() (Insert): Insertar un nuevo elemento
   - U() (Update): Actualizar un elemento existente
   - D() (Delete): Eliminar un elemento
4. get_screenshot() - Obtener una captura de pantalla del diseno
5. batch_get() - Obtener informacion de nodos

Explique el uso basico y los argumentos de cada herramienta.
```

**Resultado esperado**: Se obtienen las instrucciones de uso y los argumentos de las 5 herramientas principales de Pencil MCP.

---

## Paso 2: Crear un Mockup de Banner Publicitario

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 2: Crear un mockup de banner publicitario",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones (ejemplo)**:
```
Use Pencil MCP para crear un mockup de banner publicitario con las siguientes especificaciones.

Procedimiento:
1. mkdir -p output/pencil
2. open_document("output/pencil/marketing-banner.pen") para crear el archivo .pen
3. Disenar el banner con las siguientes especificaciones

Especificaciones del banner:
- Tamano: 1200x628px (tamano de anuncio de Facebook/Instagram)
- Tema: Promocion de "Cursor Bootcamp"
- Textos:
  - Texto principal: "Con el poder de la IA, su trabajo cambiara"
  - Subtexto: "Capacitacion en agentes de IA para no ingenieros"
  - CTA: "Inscribase ahora"
- Diseno:
  - Fondo: Degradado (azul oscuro -> purpura)
  - Texto: Color blanco, texto principal en negrita y tamano grande
  - Boton CTA: Boton redondeado de color naranja
  - Ubicacion del logo: Texto del logo de Cursor Bootcamp en la esquina inferior derecha
```

**Resultado esperado**: Se crea un mockup de banner publicitario en el editor de Pencil MCP.

---

## Paso 3: Capturar con get_screenshot y Guardar

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "Paso 3: Capturar la pantalla y guardar",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Instrucciones (ejemplo)**:
```
Obtenga una captura de pantalla del mockup de banner creado y
guardelo en la siguiente ruta:

Destino de salida: output/pencil/marketing-banner-mockup.png
Archivo de diseno: output/pencil/marketing-banner.pen (creado en el Paso 2)

Procedimiento:
1. Obtener la captura de pantalla del mockup con get_screenshot()
2. Guardar la imagen en output/pencil/marketing-banner-mockup.png
3. Verificar la ruta y el tamano del archivo guardado

Ademas, enumere 3 puntos de retroalimentacion sobre el diseno
(desde las perspectivas de combinacion de colores, diseno de pagina, tipografia, etc.).
```

**Resultado esperado**: La imagen del mockup del banner se guarda en output/pencil/ y se presentan puntos de mejora.

---

## Flujo de Trabajo Alternativo (para entornos sin GUI)

En entornos dónde Pencil MCP no está disponible (Claude Code, Codex CLI, SSH, etc.), cree mockups directamente con HTML + Tailwind CSS.

1. Crear el directorio `output/pencil/`
2. Crear un mockup de banner con HTML + Tailwind CSS CDN:
   ```bash
   mkdir -p output/pencil
   ```
3. Implementar el diseño del banner en `output/pencil/marketing-banner-mockup.html`
   - Usar `<script src="https://cdn.tailwindcss.com"></script>`
   - Aplicar directamente las especificaciones del banner del Paso 2 (tamaño, textos, colores)
4. Abrir en el navegador y tomar una captura de pantalla, o capturar con Playwright:
   ```bash
   npx playwright screenshot output/pencil/marketing-banner-mockup.html output/pencil/marketing-banner-mockup.png
   ```

---

## Problemas Comunes y Soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir orientación.

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No se puede conectar a Pencil MCP"},
      {"id": "trouble_2", "label": "Ocurre un error en batch_design"},
      {"id": "trouble_3", "label": "No se puede obtener la captura de pantalla"},
      {"id": "trouble_4", "label": "El diseno difiere de la intencion"}
    ]
  }]
}
```

### Problema 1: "No se puede conectar a Pencil MCP"
**Causa**: El servidor Pencil MCP está deshabilitado
**Solución**:
```
Verifique que Pencil MCP este habilitado.
Compruebe el estado del servidor MCP en la configuracion de Cursor
y confirme que el servidor user-pencil este habilitado.
```

### Problema 2: "Ocurre un error en batch_design"
**Causa**: Error en la sintaxis de la operación o especificación incorrecta del ID del nodo padre
**Solución**:
```
Verifique la sintaxis de operacion de batch_design.
Primero obtenga el estado actual con get_editor_state(),
confirme los IDs de nodo validos y luego ejecute la operacion.
Escriba las operaciones en formato de una por linea:
Ejemplo: foo=I("parent", { ... })
```

### Problema 3: "No se puede obtener la captura de pantalla"
**Causa**: No hay un documento abierto en el editor
**Solución**:
```
Verifique el estado actual del editor con get_editor_state().
Si no hay un documento abierto,
cree uno nuevo con open_document("new").
```

### Problema 4: "El diseño difiere de la intención"
**Causa**: Las instrucciones de diseño no son lo suficientemente específicas o la colocacion de los nodos está desalineada
**Solución**:
```
Verifique el diseno actual con snapshot_layout
y comprenda la posicion y el tamano de cada nodo.
Luego ajuste la posicion y el estilo con la operacion U() (Update).
Es efectivo verificar los resultados con get_screenshot mientras ajusta de forma iterativa.
```

---

## Punto de Control
- [ ] Comprendio las operaciones básicas de Pencil MCP (get_editor_state, batch_design, get_screenshot)
- [ ] Creo un mockup de banner publicitario con Pencil MCP
- [ ] Obtuvo una captura de pantalla con get_screenshot
- [ ] La imagen del mockup del banner se guardo en output/pencil/

---

## Vista Previa de Entregables

### Salida esperada
```
output/pencil/
  marketing-banner.pen             <- Archivo de diseno Pencil (principal)
  marketing-banner-mockup.png      <- Captura de pantalla (1200x628px)
  marketing-banner-mockup.html     (Alternativa: version HTML)
```
> Formato: PNG | Tamaño: 1200x628px (tamaño de anuncio de Facebook/Instagram)

### Comandos de verificación
```bash
# Verificar el archivo .pen y la captura de pantalla
ls -lh output/pencil/marketing-banner.pen
ls -lh output/pencil/marketing-banner-mockup.png

# Abrir la imagen (macOS: open / Linux: xdg-open)
open output/pencil/marketing-banner-mockup.png
```

> **Claude Code**: Previsualice en el chat con `Read output/pencil/marketing-banner-mockup.png`
> **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar
> **Archivos .pen**: Puede verificar el contenido con `batch_get` o `get_screenshot` de Pencil MCP

---

## Verificación de Finalización
Pegue lo siguiente en el chat de Cursor para verificar el estado de finalización:

```
# Verificacion de finalizacion: Compruebe si los archivos de salida esperados se generaron en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de finalización/incompleto y los elementos faltantes.

---

## Siguientes Pasos

Ha completado todas las lecciones del Module 17: Marketing!

Use AskUserQuestion (AskQuestion) para seleccionar su siguiente accion.

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente accion",
    "options": [
      {"id": "next_module", "label": "Iniciar el siguiente modulo (/start-18-1)"},
      {"id": "review_module", "label": "Revisar el Module 17"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- next_module -> Ir al módulo de definición de requisitos/desarrollo de sistemas con /start-18-1
- review_module -> Revisar cada lección del Module 17
- finish -> Finalizar
