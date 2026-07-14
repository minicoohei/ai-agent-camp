---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module29-slide-forge"
duration: "~15 min"
prerequisites: ["start-29-2"]
level: "beginner"
tags: ["slide", "revise"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 29-3: revisar un trabajo existente con revise

## 📍 Lo que hara en esta sesion

**Lesson 29-3: revisar un trabajo existente con revise** !

| Elemento | Contenido |
|------|------|
| Objetivo | Aplicar una instruccion de revision a un trabajo existente y regenerar solo las paginas necesarias |
| Duracion | ~15 min |
| Habilidades utilizadas | slide-forge, revise, revision de diferencias |
| Requisitos previos | Lesson 29-2 |
| Pagina del curso | Use [Module 29: slide-forge](https://ai-agent.camp/es/course/module-29?slideId=revise) como referencia paralela |

**Flujo de la sesion:**
1. Elegir el trabajo objetivo y la instruccion de revision
2. Ejecutar revise
3. Revisar los artefactos actualizados
4. Comprobar cambios innecesarios

Al final de esta sesion, habra revisado un deck generado y revisado las salidas actualizadas PPTX / PDF / HTML / PNG.

> **💡 Consejo**: No agregue numeros ni nombres propios ausentes de la fuente. No pegue secretos ni claves de API en el chat.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a para revisar un trabajo existente?",
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
(check_prereq → Verificar la carpeta de salida de Lesson 29-2 y la instruccion de revision)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Choose the Target Job and Revision Instruction

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Choose the Target Job and Revision Instruction",
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
Confirm the target job and revision instruction.

Check:
1. Target --out path, for example ./out/job1
2. A one-sentence instruction, such as "make p3 stronger" or "shorten the cover title"
3. Do not add numbers or proper nouns absent from the source
4. Do not display secrets or API key values
```

**Resultado esperado:** Se deciden la ruta `--out` y el texto de `--instruction`.

---

## 🚀 Step 2: Run revise

Ejecute `revise` siguiendo la forma del comando del README / quickstart.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Run revise",
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
Run revise with the confirmed job and instruction.

Example:
python cli.py revise --out ./out/job1 --tastes navy --instruction "p3をもっと強く"

Notes:
- Only changed page body images are regenerated
- Do not add information absent from the source
- Do not display secret values
```

**Resultado esperado:** Se actualizan los artefactos del trabajo existente.

---

## 🚀 Step 3: Review the Updated Artifacts

Abra las salidas actualizadas y confirme que la revision se aplico.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Review the Updated Artifacts",
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
Review the updated artifacts.

Artifacts:
1. ./out/job1/deck/navy/deck.pptx
2. ./out/job1/deck/navy/deck.pdf
3. ./out/job1/deck/navy/deck.html
4. ./out/job1/deck/navy/contact_sheet.png

Check:
- The revision instruction is reflected
- PPTX text remains editable
- Fixed chrome coordinates are still aligned
```

**Resultado esperado:** La mejora de la pagina objetivo es visible.

---

## 🚀 Step 4: Check for Unnecessary Changes

Confirme que las paginas fuera del objetivo no cambiaron de forma inesperada.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Check for Unnecessary Changes",
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
Compare the outputs before and after revise, then check for unnecessary changes outside the target page.

Check:
1. Non-target pages keep the same story
2. Fixed chrome aligns across all pages
3. No new numbers or proper nouns absent from the source were added
4. If another revision is needed, write it as one focused sentence
```

**Resultado esperado:** La operacion revise queda dentro del alcance previsto.

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
      {"id": "trouble_1", "label": "No se encuentra --out"},
      {"id": "trouble_2", "label": "Revision no reflejada"},
      {"id": "trouble_3", "label": "Cambiaron paginas no relacionadas"},
      {"id": "trouble_4", "label": "Preocupacion por claves API"}
    ]
  }]
}
```

### Problema 1: no se encuentra `--out`
**Causa**: La ruta difiere de la carpeta de salida de Lesson 29-2
**Prompt de solucion**:
```
Find the out folder generated in Lesson 29-2 and identify the correct --out path for revise.
```

### Problema 2: revision no reflejada
**Causa**: La instruccion es ambigua o no identifica la pagina objetivo
**Prompt de solucion**:
```
Rewrite the revision instruction as one sentence that names the page and target element, such as "shorten the p3 headline".
```

### Problema 3: cambiaron paginas no relacionadas
**Causa**: El alcance de la instruccion fue demasiado amplio
**Prompt de solucion**:
```
Narrow the revise instruction to one page and one target element so unrelated pages do not change.
```

### Problema 4: preocupacion por claves API
**Causa**: El flujo intenta imprimir valores secretos
**Prompt de solucion**:
```
Check only whether required keys exist in .env. Do not display values, and do not paste secrets into chat.
```

---

## ✅ Punto de control
- [ ] Confirmo la ruta `--out` objetivo
- [ ] Escribio una instruccion de revision de una frase
- [ ] No pego secretos ni claves de API en el chat
- [ ] Ejecuto el comando completo `python cli.py revise` mostrado arriba
- [ ] Reviso las salidas actualizadas PPTX / PDF / HTML / PNG
- [ ] Confirmo que las paginas no objetivo no cambiaron inesperadamente

---

## 📚 Vista previa del artefacto

El artefacto de esta leccion es el trabajo existente actualizado por revise.

### Salida esperada
```
./out/job1/deck/navy/deck.pptx
./out/job1/deck/navy/deck.pdf
./out/job1/deck/navy/deck.html
./out/job1/deck/navy/contact_sheet.png
```

> 💡 Al aplicar mas revisiones, mantenga cada instruccion enfocada en una pagina y un cambio.

---

## ✅ Comprobacion de finalizacion
Pegue lo siguiente en el chat de Cursor para comprobar la finalizacion:

```
# Completion check: review the revised deck.pptx / deck.pdf / deck.html / contact_sheet.png and judge whether the revision was applied without unnecessary changes.
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
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-29-4)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abra una nueva ventana y ejecute /start-29-4
- finish → Terminar
