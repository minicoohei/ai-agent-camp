---
description: "When the user says /start-7-6 — Module 7 Lesson 7-6: Creación de Commands para su propio flujo de trabajo"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~35 min"
prerequisites: ["start-7-5"]
level: "intermediate"
tags: ["skill", "command", "workflow", "customization"]
---

# 🎓 Lesson 7-6: Creación de Commands para su propio flujo de trabajo

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-6: Creación de Commands para su propio flujo de trabajo**!

| Elemento | Contenido |
|------|------|
| Objetivo | Crear 3 Commands personalizados adaptados a sus flujos de trabajo |
| Duración | ~35 min |
| Habilidades utilizadas | Markdown (YAML frontmatter), Cursor Commands |
| Requisitos previos | Lesson 7-5 completada (comprension de la estructura de Skill/Command existentes) |

**Flujo de la sesion:**
1. Identificar los flujos de trabajo diarios (usando AskUserQuestion)
2. Crear Command 1: Generador de plantilla de informe diario/semanal
3. Crear Command 2: Checklist de preparación de reuniones
4. Crear Command 3: Guía de revisión de código
5. Verificar el funcionamiento (ejecutar con /command-name)

Al final de está sesion, tendrá 3 Commands personalizados directamente vinculados a sus tareas de trabajo diarias.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Las respuestas pueden detenerse a mitad de camino dependiendo de la herramienta, pero no es un mal funcionamiento.

---

## 🎯 Verificación de preparación

Primero verifiquemos que todo esté listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Está listo/a?",
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
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar URL de la página del curso https://ai-agent.camp/es/course/module-7)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Identificar los flujos de trabajo diarios

Primero, organicemos sus tareas diarias y encontremos las que se pueden automatizar o convertir en plantillas.

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Identificacion de flujos de trabajo",
  "questions": [{
    "id": "workflow_type",
    "prompt": "Cual es la tarea mas repetitiva en su trabajo?",
    "options": [
      {"id": "reporting", "label": "Creacion de informes diarios/semanales/mensuales"},
      {"id": "meeting", "label": "Preparacion de reuniones y actas"},
      {"id": "review", "label": "Revisiones de codigo o documentos"},
      {"id": "planning", "label": "Planificacion de tareas o sprints"},
      {"id": "custom", "label": "Otro (quiero escribir el mio)"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Independientemente de la tarea que elija, los Commands se construyen en estos 3 pasos:

1. **Qué hacer** — Definir el propósito de la tarea en una línea
2. **Qué pasos** — Procedimiento de operación paso a paso
3. **Qué salida** — Entregables esperados

Entrada:
```
Answer the following questions to organize your work workflows:

1. What is your role/job title? (e.g., Engineer, PM, Designer, Sales)
2. List 3 tasks you repeat daily or weekly
3. Is there anything you "always write in the same format"?
4. Are there any "check items you tend to forget every time"?
5. How much time could you save if this task were automated?

Based on your answers, suggest 3 workflows that should be turned into Commands.
```

**Resultado esperado**: Se determinan los 3 flujos de trabajo que se convertiran en Commands.

---

## 🚀 Step 2: Crear Command (1) Plantilla de informe diario/semanal

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Command de plantilla de informe diario/semanal",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar (crear con su propio contenido de trabajo)"},
      {"id": "review", "label": "Solo ver el ejemplo (ver muestra)"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Utilice la siguiente muestra cómo referencia y cree un comando adaptado a su trabajo.

Entrada:
```
Create .cursor/commands/utility/daily-report.md with the following content:

---
description: "Generate a daily/weekly report template"
---

# Daily/Weekly Report Template Generator

## How to Use
Running this command generates a daily report template with today's date.

## Daily Report Template

Create a daily report following this template:

### 📅 Daily Report: [Today's Date]

**Author**: [Name]

#### 🎯 Today's Goals
- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

#### ✅ Completed Tasks
| Task | Category | Time Spent | Notes |
|------|----------|-----------|-------|
| - | - | - | - |

#### 🔄 In-Progress Tasks
| Task | Progress | Blockers | Expected Completion |
|------|----------|----------|-------------------|
| - | - | - | - |

#### 💡 Learnings & Insights
-

#### ⚠️ Handoff for Tomorrow
-

#### 📊 Work Hours
- Start:
- End:
- Break:

---

## Weekly Report Template

To create a weekly report, instruct "in weekly report mode".

### 📅 Weekly Report: [This Week's Period]

**Author**: [Name]

#### This Week's Highlights (up to 3)
1.
2.
3.

#### KPT Retrospective
- **Keep (things to continue)**:
- **Problem (issues)**:
- **Try (things to try next)**:

#### Next Week's Plan
| Priority | Task | Deadline |
|----------|------|----------|
| High | - | - |
| Medium | - | - |
| Low | - | - |
```

**Resultado esperado**: Se crea el comando `/daily-report` y genera una plantilla de informe diario al ejecutarse.

---

## 🚀 Step 3: Crear Command (2) Checklist de preparación de reuniones

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Command de checklist de preparacion de reuniones",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar (crear con su estilo de reuniones)"},
      {"id": "review", "label": "Solo ver el ejemplo (ver muestra)"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Entrada:
```
Create .cursor/commands/utility/meeting-prep.md with the following content:

---
description: "Generate a meeting preparation checklist"
---

# Meeting Preparation Checklist

## How to Use
Enter the meeting name to generate a preparation checklist.

## Enter Meeting Information

Answer the following questions:
1. What is the meeting name?
2. Who are the participants? (names and roles)
3. What is the meeting purpose? (decision-making / information sharing / brainstorming / progress report)
4. How long is the meeting?
5. What materials need to be prepared in advance?

## 📋 Meeting Preparation Checklist

### 🔔 3 Days Before the Meeting
- [ ] Draft the agenda
- [ ] Send advance notice/invitations to participants
- [ ] Identify required materials

### 📝 Day Before the Meeting
- [ ] Finalize and share the agenda
- [ ] Prepare and pre-share materials
- [ ] Confirm meeting room/online tool reservation
- [ ] Review previous meeting minutes and action items

### ⏰ Just Before the Meeting (15 min)
- [ ] Test material projection
- [ ] Confirm recording settings
- [ ] Assign a timekeeper
- [ ] Assign a note-taker

### 📊 Agenda Template

| Time | Topic | Owner | Purpose |
|------|-------|-------|---------|
| 0:00-0:05 | Opening / Previous review | Facilitator | Info sharing |
| 0:05-0:20 | Topic 1 | - | - |
| 0:20-0:35 | Topic 2 | - | - |
| 0:35-0:45 | Topic 3 | - | - |
| 0:45-0:55 | Action items review | All | Decision |
| 0:55-1:00 | Closing | Facilitator | Summary |

### 🔄 After the Meeting
- [ ] Create and share meeting minutes (within 24 hours)
- [ ] Finalize action item owners and deadlines
- [ ] Register follow-up tasks
```

**Resultado esperado**: Se crea el comando `/meeting-prep` y genera un checklist de preparación apropiado al tipo de reunion.

---

## 🚀 Step 4: Crear Command (3) Guía de revisión de código

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Command de guia de revision de codigo",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar (crear con sus criterios de revision)"},
      {"id": "review", "label": "Solo ver el ejemplo (ver muestra)"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Entrada:
```
Create .cursor/commands/utility/code-review.md with the following content:

---
description: "Code review guidelines and checklist"
---

# Code Review Guide

## How to Use
Enter the file name or PR number to review, and review points will be generated.

## 🔍 Review Checklist

### 1. Readability
- [ ] Are variable/function names clear in intent
- [ ] Do comments explain "why" (not "what")
- [ ] Does each function focus on a single responsibility (target: under 20 lines)
- [ ] Is nesting not too deep (within 3 levels)

### 2. Correctness
- [ ] Are edge cases handled (null, empty arrays, boundary values)
- [ ] Is error handling appropriate (try-catch, validation)
- [ ] Are there no type mismatches
- [ ] Do all existing tests pass

### 3. Security
- [ ] Are there no hardcoded secrets (API keys, passwords)
- [ ] Is user input sanitized
- [ ] Are proper access controls configured

### 4. Performance
- [ ] Are there no unnecessary loops or computations
- [ ] Will N+1 problems not occur
- [ ] Is there no risk of memory leaks when processing large data

### 5. Testing
- [ ] Are tests added for new logic
- [ ] Do tests cover edge cases
- [ ] Can tests run independently

## 💬 Review Comment Templates

### Blocker (Must Fix)
```
🚫 [Blocker] XX is YY. Please fix to ZZ.
Reason: ...
```

### Suggestion
```
💡 [Suggestion] Changing XX to YY would improve ZZ.
Reference: ...
```

### Question
```
❓ [Question] What is the intent of doing XX here?
What happens in the YY case?
```

### Praise
```
👏 [Nice!] The XX implementation is excellent. The YY aspect is particularly good.
```
```

**Resultado esperado**: Se crea el comando `/code-review` y se puede utilizar cómo guía durante las revisiones.

---

## 🚀 Step 5: Verificar el funcionamiento y mejorar

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificar el funcionamiento y mejorar",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Entrada:
```
Verify the operation of the 3 commands you created:

1. Confirm each command file is in the correct location
   - .cursor/commands/utility/daily-report.md
   - .cursor/commands/utility/meeting-prep.md
   - .cursor/commands/utility/code-review.md

2. Validate YAML frontmatter syntax
   - description is set
   - Correctly enclosed by ---

3. Run each command
   - /daily-report → Does the daily report template display?
   - /meeting-prep → Does the checklist display?
   - /code-review → Does the review guide display?

4. Make improvements if needed
   - Remove/add items that don't fit your work
   - Adjust wording to be generic enough for team sharing
```

**Resultado esperado**: Los 3 comandos funcionan correctamente y están listos para uso práctico.

---

## ⚠️ Problemas comunes y soluciones

Utilice AskQuestion para seleccionar el problema y luego siga las indicaciones.

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "El comando no se puede invocar con /command-name"},
      {"id": "trouble_2", "label": "El contenido de la plantilla no se ajusta a mi trabajo"},
      {"id": "trouble_3", "label": "Se produce un error en el YAML frontmatter"},
      {"id": "trouble_4", "label": "Quiero compartir los comandos con mi equipo"}
    ]
  }]
}
```

### Problema 1: El comando no se puede invocar con /command-name
**Causa**: La ubicacion del archivo es incorrecta
**Prompt de solución**:
```
Check the following:
1. Is the file under .cursor/commands/? (subdirectories are OK)
2. Is the file extension .md?
3. Restart Cursor and check in the Command Palette (Cmd+Shift+P)
```

### Problema 2: El contenido de la plantilla no se ajusta a mi trabajo
**Causa**: Las muestras pueden no funcionar tal cuál para todos
**Prompt de solución**:
```
Templates are just a "starting point". Customize with these steps:
1. Remove unnecessary sections
2. Add items specific to your work
3. Replace with terminology used in your team
4. Use for one week and adjust based on experience
```

### Problema 3: Se produce un error en el YAML frontmatter
**Causa**: Problema de sintaxis YAML
**Prompt de solución**:
```
Common causes:
- description value contains a colon (:) → Wrap in double quotes
- Indentation uses tabs → Change to 2 spaces
- Extra whitespace before/after --- → Remove it
```

### Problema 4: Quiero compartir los comandos con mi equipo
**Causa**: No sabe el método de compartir
**Prompt de solución**:
```
There are 2 methods:
1. Commit .cursor/commands/ to the Git repository (available for everyone who clones)
2. Place the same files in .claude/commands/ as well (for Claude Code users)
```

---

## ✅ Punto de control
- [ ] Identifico 3 o más flujos de trabajo diarios
- [ ] Creo daily-report.md (plantilla de informe diario/semanal)
- [ ] Creo meeting-prep.md (checklist de preparación de reuniones)
- [ ] Creo code-review.md (guía de revisión de código)
- [ ] Verifico el funcionamiento de los 3 comandos
- [ ] Personalizo para ajustar a su trabajo


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 skills/{skill_name}/
├── SKILL.md  (definicion del skill)
├── scripts/    (scripts de ejecucion)
└── tests/      (archivos de prueba)
```

### Comandos de verificación
```bash
# Check skill directory structure
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Check the beginning of SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat para verificar la finalización:

```
# Completion check: Verify that the following command files have been created:
# 1. .cursor/commands/utility/daily-report.md
# 2. .cursor/commands/utility/meeting-prep.md
# 3. .cursor/commands/utility/code-review.md
# Also check that YAML frontmatter (description) is set in each file.
```

**Resultado esperado**: Los 3 archivos de comando están creados correctamente.

---

## 🎉 Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar una nueva sección.

Utilice AskQuestion para elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-7-7)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-7-7
- finish → Finalizar
