---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~20 min"
prerequisites: ["start-29-2"]
level: "intermediate"
tags: ["slide", "assets", "vision"]
nonInteractiveMode: incompatible
---
# 🎓 Lesson 29-4: obtener imagenes reales con fetch-assets

## 📍 Lo que hara en esta sesion

**Lesson 29-4: obtener imagenes reales con fetch-assets** !

| Elemento | Contenido |
|------|------|
| Objetivo | Agregar de forma segura logotipos, fotos de perfil e imagenes de producto reales a un trabajo existente |
| Duracion | ~20 min |
| Habilidades utilizadas | slide-forge, fetch-assets, verificacion con vision |
| Requisitos previos | Lesson 29-2 |
| Pagina del curso | Use [Module 29: slide-forge](https://ai-agent.camp/es/course/module-29?slideId=fetch-assets) como referencia paralela |

**Flujo de la sesion:**
1. Confirmar el trabajo objetivo y la configuracion de claves
2. Confirmar derechos de imagen y responsabilidad de uso
3. Ejecutar fetch-assets
4. Revisar los resultados y el deck actualizado

Al final de esta sesion, entendera como usar solo imagenes reales que pasan la verificacion con vision.

> **💡 Consejo**: El usuario es responsable de comprobar los derechos de imagen y el uso permitido. No pegue secretos ni claves de API en el chat.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a para ejecutar fetch-assets?",
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
(check_prereq → Verificar la salida de Lesson 29-2, GEMINI_API_KEY, SERPAPI_KEY y responsabilidad sobre derechos de imagen)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Confirm the Target Job and Key Setup

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Confirm the Target Job and Key Setup",
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
Confirm the target job and key setup for fetch-assets.

Check:
1. Existing job --out path, for example ./out/job1
2. Confirm that .env has GEMINI_API_KEY
3. SERPAPI_KEY is recommended for Google Images search
4. Do not display key values
5. Confirm that the meeting notes contain real company, product, or person names
```

**Resultado esperado:** El objetivo y la configuracion para fetch-assets quedan claros.

---

## 🚀 Step 2: Confirm Image Rights and Usage Responsibility

Confirme la politica de manejo para imagenes obtenidas desde la web.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Confirm Image Rights and Usage Responsibility",
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
Before running fetch-assets, confirm image rights and usage responsibility.

Important:
1. Users are responsible for checking image rights and permitted use
2. Source URLs remain in catalog[].note in the result JSON
3. Materials with low vision verification scores are not used
4. Slides without accepted assets stay as diagrams
5. If you do not want web fetching, use --photo-catalog with a local image catalog JSON
```

**Resultado esperado:** El limite de uso y la responsabilidad quedan claros.

---

## 🚀 Step 3: Run fetch-assets

Inyecte imagenes reales en el trabajo existente.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Run fetch-assets",
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
Run fetch-assets on the existing job.

python cli.py fetch-assets --out ./out/job1

To fetch assets during a new generation:
python cli.py generate --input examples/loop_engineering.md \
  --type ゴールデンサークル --scenario ビジョン駆動 --tone コーポレート・ネイビー \
  --goal 共有して知ってほしい --target 社外・初対面 \
  --tastes navy --formats pptx pdf png html --out ./out/job1 --fetch-assets

Notes:
- GEMINI_API_KEY is required for extraction and vision verification
- SERPAPI_KEY is recommended for Google Images search
- Do not display secret values
- If no asset passes verification, the slide stays as a diagram
```

**Resultado esperado:** Se obtienen imagenes candidatas y solo los recursos que pasan vision se reflejan en el deck.

---

## 🚀 Step 4: Review the Results and Updated Deck

Revise el JSON de resultado y el deck actualizado.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Review the Results and Updated Deck",
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
Review the fetch-assets result and updated deck.

Check:
1. Source URLs remain in catalog[].note in the result JSON
2. The name and image actually match
3. Low-score assets are not forced into the deck
4. The user still needs to verify image rights and permitted use
5. Fixed chrome and editable PPTX text are preserved
```

**Resultado esperado:** Las URL de origen, los resultados de verificacion y los cambios del deck quedan claros.

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
      {"id": "trouble_1", "label": "Falta GEMINI_API_KEY"},
      {"id": "trouble_2", "label": "No se aceptaron recursos"},
      {"id": "trouble_3", "label": "Aparece logo incorrecto"},
      {"id": "trouble_4", "label": "Preocupacion por derechos"}
    ]
  }]
}
```

### Problema 1: falta `GEMINI_API_KEY`
**Causa**: La clave requerida para extraccion y verificacion con vision no esta configurada
**Prompt de solucion**:
```
Check only whether GEMINI_API_KEY exists in .env. Do not display the value, and guide safe setup if it is missing.
```

### Problema 2: no se aceptaron recursos
**Causa**: El score de verificacion fue demasiado bajo o no se encontro candidato
**Prompt de solucion**:
```
Review the fetch-assets result JSON, summarize low-score or missing-candidate reasons, and explain that keeping the diagram is acceptable.
```

### Problema 3: aparece logo incorrecto
**Causa**: La busqueda mezclo una empresa con nombre similar
**Prompt de solucion**:
```
Check candidate names, source URLs, and vision verification results in catalog, then exclude assets whose name and image do not match.
```

### Problema 4: preocupacion por derechos
**Causa**: No se han revisado los terminos de uso de las imagenes web obtenidas
**Prompt de solucion**:
```
List the source URLs for fetched images and create a checklist for the user to verify rights and permitted use.
```

---

## ✅ Punto de control
- [ ] Confirmo la ruta `--out` del trabajo existente
- [ ] Confirmo que `GEMINI_API_KEY` existe sin imprimir su valor
- [ ] Entendio cuando `SERPAPI_KEY` es util
- [ ] Entendio que el usuario es responsable de derechos de imagen y uso permitido
- [ ] Ejecuto `python cli.py fetch-assets --out ./out/job1`
- [ ] Reviso `catalog[].note` en el JSON de resultado y el deck actualizado
- [ ] No pego secretos ni claves de API en el chat

---

## 📚 Vista previa del artefacto

Los artefactos de esta leccion son los resultados de verificacion de imagenes y el deck actualizado.

### Salida esperada
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/deck.html
./out/job1/deck/navy/contact_sheet.png
```

> 💡 Revise las URL de origen en `catalog[].note`. Los derechos y el uso permitido deben ser evaluados por el usuario.

---

## ✅ Comprobacion de finalizacion
Pegue lo siguiente en el chat de Cursor para comprobar la finalizacion:

```
# Completion check: review the fetch-assets result JSON and updated deck.pptx, then judge source URLs, vision verification, and remaining image-rights checks.
```

**Resultado esperado:** Cursor informa que esta completo y que falta.

---

## ➡️ Siguiente paso

Esta seccion esta completa. Inicie otra leccion en una nueva ventana si hace falta.

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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-29-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abra una nueva ventana y ejecute /start-29-1
- finish → Terminar
