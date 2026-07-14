---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~20 min"
prerequisites: ["start-0-3"]
level: "beginner"
tags: ["slide", "pptx", "demo"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 29-1: demo de slide-forge sin clave de API

## 📍 Lo que hara en esta sesion

**Lesson 29-1: demo de slide-forge sin clave de API** !

| Elemento | Contenido |
|------|------|
| Objetivo | Generar PPTX y HTML desde la muestra incluida sin una clave de OpenAI |
| Duracion | ~20 min |
| Habilidades utilizadas | slide-forge, build-only, revision de PPTX |
| Requisitos previos | Lesson 0-3 |
| Pagina del curso | Use [Module 29: slide-forge](https://ai-agent.camp/es/course/module-29?slideId=first-run) como referencia paralela |

**Flujo de la sesion:**
1. Verificar el area de trabajo y las dependencias
2. Obtener slide-forge
3. Ejecutar la demo sin clave
4. Revisar las salidas PPTX y HTML

Al final de esta sesion, habra revisado un deck de slide-forge con chrome fijo sin usar una clave de API.

> **💡 Consejo**: No pegue secretos ni claves de API en el chat. Esta leccion no requiere una clave de OpenAI.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a para ejecutar la demo sin clave?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar Python 3.11+, Node.js, ImageMagick y Poppler)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Check the Workspace and Dependencies

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Check the Workspace and Dependencies",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Before running the slide-forge no-key demo, check the workspace and dependencies.

Check:
1. Do not overwrite an existing slide-forge directory without confirmation
2. Python 3.11+ is available
3. Node.js is available
4. ImageMagick magick is available
5. Poppler pdfinfo / pdftoppm are available
6. macOS: brew install imagemagick poppler / Windows and Linux: install ImageMagick and Poppler with each package manager

Do not display secrets or API key values.
```

**Resultado esperado:** Las dependencias faltantes y el estado del directorio quedan claros.

---

## 🚀 Step 2: Get slide-forge

Si el repositorio aun no existe, clone el repositorio oficial.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Get slide-forge",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
If slide-forge is not already present, get it with:

git clone --depth 1 --branch v0.1.0 https://github.com/minicoohei/slide-forge.git
cd slide-forge

Use the verified fixed version as a supply-chain precaution.
If the directory or checkout already exists, do not overwrite it without confirmation. Later setup commands must not overwrite existing .env or config.yaml files.
```

**Resultado esperado:** Esta en la raiz del repositorio slide-forge.

---

## 🚀 Step 3: Run the No-key Demo

Use las imagenes de muestra incluidas para generar PPTX y HTML sin clave de OpenAI.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Run the No-key Demo",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Install dependencies and run the no-key demo.

pip install -r requirements.txt
cd pipeline/lib && npm ci && npx playwright install chromium && cd ../..
cp -n .env.example .env
cp -n config.default.yaml config.yaml
python cli.py build-only --manifest examples/sample_manifest.json \
  --tastes lime --formats pptx html --no-regen --out examples/sample

Notes:
- Existing .env / config.yaml files are not overwritten because the commands use cp -n
- The offline demo must use --out examples/sample --tastes lime
- Changing those values can produce an empty deck with missing_bodies
- No OpenAI API key is required
```

**Resultado esperado:** Se generan `examples/sample/lime/deck.pptx` y `examples/sample/lime/deck.html`.

---

## 🚀 Step 4: Review the PPTX and HTML Outputs

Abra los archivos generados y revise el chrome fijo.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Review the PPTX and HTML Outputs",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Open and inspect the generated PPTX and HTML.

open examples/sample/lime/deck.pptx

Check:
1. Headline, lead, and footer are editable text
2. Fixed chrome aligns at the same coordinates on every page
3. Only the body illustration is an image
4. deck.html shows the same deck in the browser
```

**Resultado esperado:** Puede revisar el deck de muestra en PPTX y HTML.

---

## ⚠️ Problemas comunes y soluciones

Utilice AskQuestion para seleccionar el problema y luego siga las indicaciones.

**Configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "Aparece missing_bodies"},
      {"id": "trouble_2", "label": "Falta magick / pdfinfo"},
      {"id": "trouble_3", "label": "Falta Playwright Chromium"},
      {"id": "trouble_4", "label": "PPTX no se abre"}
    ]
  }]
}
```

### Problema 1: aparece `missing_bodies`
**Causa**: El comando no uso los valores fijos `--out examples/sample --tastes lime`
**Prompt de solucion**:
```
Re-run the slide-forge no-key demo with --out examples/sample --tastes lime, and explain why those values are fixed.
```

### Problema 2: falta `magick` / `pdfinfo`
**Causa**: ImageMagick o Poppler no esta instalado
**Prompt de solucion**:
```
Guide me through installing ImageMagick and Poppler on macOS, then verify magick / pdfinfo / pdftoppm.
```

### Problema 3: falta Playwright Chromium
**Causa**: No se ejecuto `npx playwright install chromium`
**Prompt de solucion**:
```
Show the steps to reinstall Chromium from slide-forge/pipeline/lib.
```

### Problema 4: PPTX no se abre
**Causa**: La generacion fallo o el deck esta vacio
**Prompt de solucion**:
```
Check whether deck.pptx exists, its file size, and the build-only JSON output to isolate the failure.
```

---

## ✅ Punto de control
- [ ] Confirmo el directorio de trabajo de slide-forge
- [ ] Verifico Python 3.11+, Node.js, ImageMagick y Poppler
- [ ] Ejecuto la demo sin clave con `--out examples/sample --tastes lime`
- [ ] Abrio `examples/sample/lime/deck.pptx`
- [ ] Reviso `examples/sample/lime/deck.html`
- [ ] No pego secretos ni claves de API en el chat

---

## 📚 Vista previa del artefacto

Los artefactos de esta leccion son el deck de muestra generado sin clave de API.

### Salida esperada
```
examples/sample/lime/deck.pptx
examples/sample/lime/deck.html
```

> 💡 Para revisar tambien PDF / PNG, agregue `--formats pdf png`.

---

## ✅ Comprobacion de finalizacion
Pegue lo siguiente en el chat de Cursor para comprobar la finalizacion:

```
# Completion check: confirm that examples/sample/lime/deck.pptx and deck.html were generated, and that fixed chrome plus editable text were inspected.
```

**Resultado esperado:** Cursor informa que esta completo y que falta.

---

## ➡️ Siguiente paso

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para la siguiente seccion.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-29-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abra una nueva ventana y ejecute /start-29-2
- finish → Terminar
