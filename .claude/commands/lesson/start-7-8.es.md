---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-7-6", "start-7-7"]
level: "intermediate"
tags: ["skill", "command", "testing", "debugging", "iteration"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 7-8: Pruebas, depuración e iteración

## 📍 Lo que hará en esta sesión

Bienvenido/a a **Lesson 7-8: Pruebas, depuración e iteración**!

| Elemento | Contenido |
|------|------|
| Objetivo | Verificar y mejorar la calidad de los Skills/Commands que creo |
| Duración | ~30 min |
| Habilidades utilizadas | Pruebas, depuración, iteración |
| Requisitos previos | Lesson 7-6 (creación de Commands) y Lesson 7-7 (creación de Skills) completadas |

**Flujo de la sesión:**
1. Pruebas de funcionamiento de Commands (casos límite, manejo de errores)
2. Pruebas de funcionamiento de Skills (casos normales, casos de error)
3. Auto-revisión (usando checklist)
4. Iteración de mejoras (retroalimentación → corrección → re-prueba)
5. Mantenimiento de documentación (agregar guía de uso)

Al final de esta sesión, los Skills/Commands que creo estaran pulidos a "calidad lista para entregar a otros".

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Las respuestas pueden detenerse a mitad de camino dependiendo de la herramienta, pero no es un mal funcionamiento.

---

## 🎯 Verificación de preparación

Primero verifiquemos que todo este listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a?",
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
(check_prereq → Verificar los entregables creados en 7-6 y 7-7)
(view_html → Mostrar URL de la página del curso https://ai-agent.camp/es/course/module-7)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Step 1: Pruebas de funcionamiento de Commands

Pruebe los 3 Commands creados en la Lesson 7-6.

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Pruebas de funcionamiento de Commands",
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

**Indicaciones tras la selección:**

Pruebe cada Command desde estas 3 perspectivas.

Entrada:
```
Test the 3 Commands created in 7-6 from the following perspectives:

### Test 1: Normal Case Tests
Run each command with /command-name and verify expected output:

- /daily-report → Does the daily report template display correctly?
  - Is the date correct?
  - Is the table format intact?
  - Do checkboxes function?

- /meeting-prep → Does the meeting preparation checklist display correctly?
  - Are all check items displayed without omissions?
  - Is the agenda template table intact?

- /code-review → Does the review guide display correctly?
  - Is categorization appropriate?
  - Can comment templates be used with copy-paste?

### Test 2: Edge Case Tests
- If the command description is too long, does the display break?
- Are all Markdown notations (code blocks, tables, checkboxes) rendered correctly?
- Does mixed Japanese and English display without issues?

### Test 3: Usability Tests
- Can a first-time user understand how to use it?
- Is there unnecessary information (information overload)?
- Is there missing information?

Report test results in the following format:

| Command | Normal | Edge Cases | Usability | Overall |
|---------|--------|-----------|-----------|---------|
| daily-report | OK/NG | OK/NG | OK/NG | PASS/FAIL |
| meeting-prep | OK/NG | OK/NG | OK/NG | PASS/FAIL |
| code-review | OK/NG | OK/NG | OK/NG | PASS/FAIL |
```

**Resultado esperado**: Los informes de resultados de pruebas para los 3 Commands estan completos y los problemas estan identificados.

---

## 🚀 Step 2: Pruebas de funcionamiento de Skills

Pruebe el Skill creado en la Lesson 7-7.

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Pruebas de funcionamiento de Skills",
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

**Indicaciones tras la selección:**

Entrada:
```
Verify the skill created in 7-7 with the following test cases:

### Test 1: Test Mode
python skills/[skill-name]/scripts/main.py --test

Expected: Test succeeds and sample output is displayed

### Test 2: Normal Case (Minimal Input)
python skills/[skill-name]/scripts/main.py --input [minimal test data]

Expected: Correct output is generated

### Test 3: Normal Case (Full Options)
python skills/[skill-name]/scripts/main.py --input [test data] --output output.md --format markdown --verbose

Expected: Output to file in specified format

### Test 4: Error Case (Non-existent File)
python skills/[skill-name]/scripts/main.py --input nonexistent_file.txt

Expected: Appropriate error message displayed and exits abnormally

### Test 5: Error Case (Invalid Arguments)
python skills/[skill-name]/scripts/main.py

Expected: Usage message is displayed

### Test 6: Error Case (Empty File)
touch /tmp/empty_test.txt
python skills/[skill-name]/scripts/main.py --input /tmp/empty_test.txt

Expected: Appropriate handling of empty file (warning or empty result)

Report test results in the following format:

| Test Case | Expected Result | Actual Result | Verdict |
|-----------|----------------|--------------|---------|
| Test mode | Test succeeds | - | PASS/FAIL |
| Normal (minimal) | Correct output | - | PASS/FAIL |
| Normal (full) | File output | - | PASS/FAIL |
| Error (not found) | Error message | - | PASS/FAIL |
| Error (no args) | Usage display | - | PASS/FAIL |
| Error (empty file) | Appropriate handling | - | PASS/FAIL |
```

**Resultado esperado**: Se registran los resultados de 6 casos de prueba y se identifican los elementos que necesitan corrección.

---

## 🚀 Step 3: Auto-revisión

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Auto-revision",
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

**Indicaciones tras la selección:**

Auto-evalue la calidad de sus Commands/Skills utilizando el siguiente checklist.

Entrada:
```
Evaluate the deliverables from 7-6/7-7 based on this self-review checklist:

## Command Self-Review (for each command)

### Structure/Format
- [ ] Is YAML frontmatter valid syntax
- [ ] Is description concise and clear (under 50 characters recommended)
- [ ] Are Markdown heading levels appropriate (one H1, structured with H2+)
- [ ] Do code blocks have language specifications (```bash, ```python, etc.)

### Content/Quality
- [ ] Can a first-time user understand "what it does" in 10 seconds
- [ ] Are there no remaining TODO/placeholders in templates
- [ ] Is the language natural and readable
- [ ] Is the information volume appropriate (not too much, not too little)

### Practicality
- [ ] Can it be used daily/weekly in actual work
- [ ] Are there parts ready for immediate copy-paste use
- [ ] Is there room for customization

## Skill Self-Review

### SKILL.md
- [ ] Is metadata (name, description) under 100 words
- [ ] Is body under 5,000 words
- [ ] Do quick start commands work with copy-paste
- [ ] Is the parameter table complete
- [ ] Are output samples included
- [ ] Are there 5+ trigger phrases

### scripts/main.py
- [ ] Does --help display usage
- [ ] Does --test run tests
- [ ] Does it return appropriate messages and exit codes on errors
- [ ] Does it support UTF-8 encoding
- [ ] Are there no remaining unnecessary print statements or debug code

### Overall
- [ ] Does the directory structure follow the standard pattern
- [ ] Can someone else clone and use it immediately

Mark each item as PASS / FAIL / NA, and provide improvement suggestions for FAIL items.
```

**Resultado esperado**: Se registran los resultados de la auto-revisión y los elementos de mejora se organizan por prioridad.

---

## 🚀 Step 4: Iteración de mejoras

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Iteracion de mejoras",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar (corregir problemas del Step 3)"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Corrija los problemas encontrados en los Steps 1-3. Corrija en orden de "mayor impacto primero".

Entrada:
```
Improve based on the test/review results from Steps 1-3:

### Improvement Priority
1. **Critical (fix immediately)**: Doesn't work, errors occur
2. **High (fix in this session)**: Major usability issues
3. **Medium (OK for next time)**: Minor improvements
4. **Low (someday)**: Nice-to-have feature additions

### Improvement Iteration Cycle

For each issue, run through this cycle:

1. **Identify the problem**: What is the issue, reproduction steps
2. **Analyze the cause**: Why is this happening
3. **Apply the fix**: Fix with minimal changes
4. **Re-test**: Verify with the same test case after fix

### Fix Report

| Issue | Priority | Cause | Fix | Re-test Result |
|-------|----------|-------|-----|---------------|
| - | Critical/High/Medium/Low | - | - | PASS/FAIL |

Fix all Critical/High issues before proceeding to the next Step.
```

**Resultado esperado**: Todos los problemas Critical/High estan corregidos y las re-pruebas pasan.

---

## 🚀 Step 5: Mantenimiento de documentación

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Mantenimiento de documentacion",
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

**Indicaciones tras la selección:**

Finalmente, mantenga la documentación para que otros puedan usar los Commands/Skills que creo.

Entrada:
```
Maintain the following documentation:

### 1. Command Usage Guide

Check that each Command file has a "How to Use" section at the top,
and add if missing:
- What it does (one-line description)
- How to use it (execution method)
- Output example (what results to expect)

### 2. Skill Usage Guide

Check that SKILL.md includes the following, and add if missing:
- Quick start (copy-paste-ready command examples)
- Common use cases (3+ patterns)
- Troubleshooting (common errors and solutions)

### 3. Deliverables List

Create a list of all deliverables created in this module (7-1 through 7-8):

| File | Type | Overview |
|------|------|---------|
| .cursor/commands/utility/daily-report.md | Command | Daily/weekly report template |
| .cursor/commands/utility/meeting-prep.md | Command | Meeting preparation checklist |
| .cursor/commands/utility/code-review.md | Command | Code review guide |
| skills/[skill-name]/SKILL.md | Skill | [Skill description] |
| skills/[skill-name]/scripts/main.py | Script | [Script description] |

### 4. Retrospective

Answer the following questions:
1. What was the most valuable learning from this module?
2. What Command/Skill ideas do you want to create in the future?
3. What would you like to improve?
```

**Resultado esperado**: La documentación esta mantenida y la lista de entregables y la retrospectiva estan completas.

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
      {"id": "trouble_1", "label": "Error inesperado en las pruebas"},
      {"id": "trouble_2", "label": "El mismo error vuelve a ocurrir despues de corregir"},
      {"id": "trouble_3", "label": "Demasiados puntos de revision, no se por donde empezar"},
      {"id": "trouble_4", "label": "No se como escribir la documentacion"}
    ]
  }]
}
```

### Problema 1: Error inesperado en las pruebas
**Causa**: El entorno de pruebas difiere de las suposiciones del script
**Prompt de solución**:
```
Paste the full error message. We'll isolate the cause in this order:
1. What is the Python version? (python3 --version)
2. Are all required packages installed? (uv pip list)
3. Is the file path correct? (verify with ls -la)
4. Are environment variables set? (echo $VARIABLE_NAME)
```

### Problema 2: El mismo error vuelve a ocurrir después de corregir
**Causa**: Ubicación de corrección incorrecta o problema de cache
**Prompt de solución**:
```
Try the following:
1. Re-save the file (Cmd+S / Ctrl+S)
2. Delete Python cache: find . -name "__pycache__" -exec rm -rf {} +
3. Verify changes are reflected: cat [file-path] | head -20
4. Try running in a different terminal window
```

### Problema 3: Demasiados puntos de revisión, no se por donde empezar
**Causa**: Caer en el perfeccionismo
**Prompt de solución**:
```
Apply the 80% rule:
1. First check only "does it work or not" (Critical)
2. Then check "is it usable" (High)
3. The rest is "nice to have" level (Medium/Low)
Fixing only Critical and High completes this lesson.
```

### Problema 4: No se como escribir la documentación
**Causa**: No ha visto ejemplos de buena documentación
**Prompt de solución**:
```
Refer to these existing skill SKILL.md files:
- skills/banner-creator/SKILL.md (simple example)
- skills/data-analyst/SKILL.md (detailed example)

Write documentation with this standard: "Can I understand it when reading it 3 months from now?"
```

---

## ✅ Punto de control
- [ ] Pruebas de funcionamiento de los 3 Commands (normal / casos límite / usabilidad) completadas
- [ ] Pruebas de funcionamiento del Skill (6 casos de prueba) completadas
- [ ] Auto-revisión (Command: 11 elementos, Skill: 16 elementos) completada
- [ ] Todos los problemas Critical/High estan corregidos
- [ ] Documentación (guía de uso) mantenida
- [ ] Lista de entregables creada
- [ ] Retrospectiva completada


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
# Completion check: Verify all Module 7 deliverables:
# 1. Do the 3 Commands (daily-report, meeting-prep, code-review) work
# 2. Does the 1 Skill (SKILL.md + scripts/main.py) pass tests
# 3. Is documentation maintained for each deliverable
# 4. Is the test result report created
```

**Resultado esperado**: Todos los entregables del Module 7 cumplen con los estándares de calidad.

---

## 🎉 Siguientes pasos

Module 7 "Creación de Skill/Commands" esta completo con las 8 lecciones. Felicitaciones!

Habilidades adquiridas:
- Capacidad para analizar estructuras existentes de Command/Skill
- Capacidad para crear Commands adaptados a flujos de trabajo
- Capacidad de desarrollo de skills dirigido por SKILL.md
- Experiencia práctica con pruebas, depuración e iteración

Utilice AskQuestion para elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_module", "label": "Avanzar al Module 8 Analisis de datos (/start-8-1)"},
      {"id": "review_all", "label": "Revisar los entregables del Module 7"},
      {"id": "share", "label": "Aprender a compartir Commands/Skills con su equipo"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_module → /start-8-1 (Module 8 Análisis de datos)
- review_all → Mostrar todos los entregables del Module 7
- share → Guía para Git push → procedimiento de compartir con el equipo
- finish → Finalizar
