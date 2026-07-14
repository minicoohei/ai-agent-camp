---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~30 min"
prerequisites: ["start-29-1"]
level: "intermediate"
tags: ["slide", "generation", "ai"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 29-2: generacion de produccion desde notas con cinco preguntas

## 📍 Lo que hara en esta sesion

**Lesson 29-2: generacion de produccion desde notas con cinco preguntas** !

| Elemento | Contenido |
|------|------|
| Objetivo | Generar un deck de propuesta editable desde notas de reunion seleccionando cinco parametros |
| Duracion | ~30 min |
| Habilidades utilizadas | slide-forge, generate, AskUserQuestion |
| Requisitos previos | Lesson 29-1 |
| Pagina del curso | Use [Module 29: slide-forge](https://ai-agent.camp/es/course/module-29?slideId=generate) como referencia paralela |

**Flujo de la sesion:**
1. Confirmar entradas y manejo de secretos
2. Seleccionar las cinco respuestas
3. Ejecutar generate
4. Revisar los cuatro formatos de salida

Al final de esta sesion, habra generado PPTX / PDF / PNG / HTML desde sus propias notas.

> **💡 Consejo**: No pegue secretos ni claves de API en el chat. Solo confirme si los valores existen en `.env`.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a para generar un deck de produccion desde notas?",
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
(check_prereq → Verificar Lesson 29-1, `.env`, `config.yaml` y archivos de entrada)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Confirm Inputs and Secret Handling

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Confirm Inputs and Secret Handling",
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
Confirm the inputs and settings for slide-forge production generation.

Check:
1. Meeting notes file (.md / .txt / .json / .pdf) or direct text
2. If a separate outline exists, treat it as --outline
3. Confirm that .env has OPENAI_API_KEY and LLM_BACKEND without printing values
4. Confirm that config.yaml exists
5. Do not display secrets or API key values in chat or logs
6. Do not invent proper nouns, numbers, dates, costs, or KPIs that are absent from the source material
```

**Resultado esperado:** Las entradas, configuraciones y politica de generacion quedan claras.

---

## 🚀 Step 2: Select the Five Answers

Elija el tipo de deck, escenario, tono, objetivo y audiencia usando las opciones de `config.yaml`.

Utilice AskQuestion para seleccionar las cinco respuestas.

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Select the Five Answers",
  "questions": [
    {
      "id": "deck_type",
      "prompt": "Choose the structure type",
      "options": [
        {"id": "SCQA", "label": "SCQA"},
        {"id": "PREP", "label": "PREP"},
        {"id": "golden_circle", "label": "Golden Circle"},
        {"id": "TAPS", "label": "TAPS"},
        {"id": "whole_part", "label": "Whole-part"}
      ]
    },
    {
      "id": "scenario",
      "prompt": "Choose the scenario",
      "options": [
        {"id": "problem", "label": "Problem-driven"},
        {"id": "vision", "label": "Vision-driven"},
        {"id": "capital", "label": "Capital-driven"},
        {"id": "people", "label": "People-driven"}
      ]
    },
    {
      "id": "tone",
      "prompt": "Choose the tone",
      "options": [
        {"id": "light", "label": "Light"},
        {"id": "navy", "label": "Corporate navy"},
        {"id": "dark", "label": "Cinema dark"},
        {"id": "editorial", "label": "Editorial white"}
      ]
    },
    {
      "id": "goal",
      "prompt": "Choose the goal",
      "options": [
        {"id": "approval", "label": "Win approval"},
        {"id": "share", "label": "Share for awareness"},
        {"id": "move", "label": "Move people with a vision"}
      ]
    },
    {
      "id": "target",
      "prompt": "Choose the target audience",
      "options": [
        {"id": "external", "label": "External first-time audience"},
        {"id": "internal", "label": "Internal decision makers"},
        {"id": "partner", "label": "Existing partners"}
      ]
    }
  ]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Map the selected five answers to --type / --scenario / --tone / --goal / --target.

If you need the course example, use:
- input: examples/loop_engineering.md
- type: Golden Circle
- scenario: Vision-driven
- tone: Corporate navy
- goal: Share and inform
- target: External first-time audience
```

**Resultado esperado:** Los cinco valores de CLI quedan decididos.

---

## 🚀 Step 3: Run generate

Ejecute la generacion siguiendo la forma del comando del README.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Run generate",
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
Run slide-forge generate with the confirmed input and five answers.

Example:
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1

Notes:
- --input / --outline can be provided multiple times
- Use pptx pdf png html for --formats
- The OpenAI key is used only for image generation, not passed to the LLM agent
- Do not display secret values
```

**Resultado esperado:** Se crea un trabajo bajo `./out/job1` y `artifacts` en JSON lista las rutas bajo `./out/job1/deck/navy/`.

---

## 🚀 Step 4: Review the Four Output Formats

Revise las salidas PPTX / PDF / PNG / HTML generadas.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Review the Four Output Formats",
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
Review the generated artifacts and collect their absolute paths.

Artifacts:
1. ./out/job1/deck/navy/deck.pptx
2. ./out/job1/deck/navy/deck.pdf
3. ./out/job1/deck/navy/contact_sheet.png
4. ./out/job1/deck/navy/deck.html

Check:
- Fixed chrome aligns at the same coordinates on every page
- Headline, lead, and footer remain editable text in PPTX
- The deck does not add proper nouns, numbers, dates, costs, or KPIs absent from the source
- Write one sentence for anything you want to revise next
```

**Resultado esperado:** Los cuatro formatos y el objetivo de revision siguiente quedan claros.

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
      {"id": "trouble_1", "label": "OPENAI_API_KEY is not available"},
      {"id": "trouble_2", "label": "Falta claude / codex CLI"},
      {"id": "trouble_3", "label": "Fallo render"},
      {"id": "trouble_4", "label": "El deck se alejo de la fuente"}
    ]
  }]
}
```

### Problema 1: `OPENAI_API_KEY is not available`
**Causa**: La clave de generacion de imagen no esta configurada en `.env`
**Prompt de solucion**:
```
Check only whether OPENAI_API_KEY exists in .env. Do not display the key value, and guide safe setup if it is missing.
```

### Problema 2: falta `claude` / `codex` CLI
**Causa**: La CLI para `LLM_BACKEND` no esta en PATH
**Prompt de solucion**:
```
Check the LLM_BACKEND value and whether the matching claude / codex CLI is on PATH, then guide the needed setup.
```

### Problema 3: fallo render
**Causa**: Falta Playwright Chromium, ImageMagick o Poppler
**Prompt de solucion**:
```
Read the render failure log and isolate whether Chromium, ImageMagick, or Poppler is missing.
```

### Problema 4: el deck se alejo de la fuente
**Causa**: El deck infirio informacion que no esta en la entrada
**Prompt de solucion**:
```
Compare the deck against the source and remove or mark as pending any proper nouns, numbers, dates, costs, or KPIs not present in the input.
```

---

## ✅ Punto de control
- [ ] Confirmo el archivo de entrada o texto directo
- [ ] Confirmo que existen `.env` y `config.yaml`
- [ ] No pego secretos ni claves de API en el chat
- [ ] Selecciono las cinco respuestas
- [ ] Ejecuto el comando completo `python cli.py generate` mostrado arriba
- [ ] Reviso las salidas PPTX / PDF / PNG / HTML

---

## 📚 Vista previa del artefacto

Los artefactos de esta leccion son las salidas del deck de propuesta generado desde notas.

### Salida esperada
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/contact_sheet.png
./out/job1/deck/navy/deck.html
```

> 💡 En Lesson 29-3, revisara el trabajo existente una vez.

---

## ✅ Comprobacion de finalizacion
Pegue lo siguiente en el chat de Cursor para comprobar la finalizacion:

```
# Completion check: confirm that PPTX / PDF / PNG / HTML were generated under ./out/job1/deck/navy, and that fixed chrome plus editable text were inspected.
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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-29-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abra una nueva ventana y ejecute /start-29-3
- finish → Terminar
