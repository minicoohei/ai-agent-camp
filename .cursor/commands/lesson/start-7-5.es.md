---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-6-1", "start-6-2"]
level: "intermediate"
tags: ["skill", "command", "agent", "analysis"]
---

# 🎓 Lesson 7-5: Comprension y análisis de la estructura de Skill/Command existentes

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-5: Comprension y análisis de la estructura de Skill/Command existentes**!

| Elemento | Contenido |
|------|------|
| Objetivo | Comprender la estructura de los Skills y Commands existentes y adquirir los conocimientos fundamentales para crear los propios |
| Duración | ~30 min |
| Habilidades utilizadas | Exploracion del sistema de archivos, Markdown |
| Requisitos previos | Lessons 6-1 y 6-2 completadas (fundamentos de Command/Skill del módulo de desarrollo de agentes) |

**Flujo de la sesion:**
1. Explorar la estructura de `.cursor/commands/` y `.claude/commands/`
2. Explorar la estructura de `skills/` (SKILL.md, scripts/)
3. Analizar patrones comunes en los comandos existentes (frontmatter, estructura de Steps, checklists)
4. Analizar patrones comunes en los skills existentes (estructura de SKILL.md, integración con scripts)

Al final de está sesion, tendrá una comprension sistemática de los patrones de diseño de Skill y Command, y los conocimientos para crear los propios.

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

## 🚀 Step 1: Explorar la estructura del directorio de Commands

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Explorar la estructura del directorio de Commands",
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

Los Commands se colocan en dos ubicaciones:
- `.cursor/commands/` — Comandos personalizados para el workspace actual
- `.claude/commands/` — Comandos personalizados para Claude Code

Entrada:
```
Examine the following directory structures and create a report:

1. List of subdirectories in .cursor/commands/ with file count for each
2. List of subdirectories in .claude/commands/ with file count for each
3. Command file naming convention (start-X-Y.md pattern)

Also explain the difference in roles for each directory:
- lesson/ → Lesson commands (linked to the learning curriculum)
- utility/ → Utility commands (general-purpose tools)
```

**Resultado esperado**: Se establece una vision general de la estructura del directorio de Commands, y se comprende la distincion entre lesson/ y utility/.

---

## 🚀 Step 2: Explorar la estructura del directorio de Skills

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Explorar la estructura del directorio de Skills",
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

Los Skills se colocan en `skills/`, y cada skill es un directorio independiente.

Entrada:
```
Explore the skills/ directory and report on the following:

1. Skill list (directory names) with a brief description of each
2. Analyze the common structure of each skill directory:
   - Presence of SKILL.md
   - Presence of scripts/ directory
   - Other files (references/, templates/, etc.)

3. Select 3 representative skills and display each directory structure as a tree:
   - banner-creator (image generation)
   - data-analyst (data analysis)
   - check-inbox (communication)

4. Extract common sections from SKILL.md:
   - Sections common to all skills
   - Sections that vary by skill
```

**Resultado esperado**: Se comprende la estructura estandar del directorio de Skills (SKILL.md + scripts/ + archivos opcionales).

---

## 🚀 Step 3: Analizar patrones comunes en los comandos existentes

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Analizar patrones comunes en los comandos existentes",
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

Los comandos de lección tienen una "plantilla" común. Comprender está plantilla le permite producir sus propios comandos en masa.

Entrada:
```
Read the following 3 lesson commands and analyze common patterns:

1. .cursor/commands/lesson/start-6-1.md
2. .cursor/commands/lesson/start-7-1.md
3. .cursor/commands/lesson/start-1-1.md

Analyze from these perspectives and create a "Command Template":

### Common YAML Frontmatter Items
- How to write description, duration, prerequisites, level, tags

### Common Body Structure
- 📍 What You'll Do (table format)
- 🎯 Readiness Check (AskQuestion)
- 🚀 Step N: (structure of each step)
- ⚠️ Common Issues
- ✅ Checkpoint / Completion Check
- ➡️ Next Steps

### AskQuestion Patterns
- 3 choices per Step (practice / review / skip)
- Trouble selection
- Next step selection

Compile the analysis into a "Command Creation Cheat Sheet".
```

**Resultado esperado**: Se extraen los patrones comunes de los comandos de lección y se crea un cheat sheet reutilizable.

---

## 🚀 Step 4: Analizar patrones comunes en los skills existentes

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Analizar patrones comunes en los skills existentes",
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

SKILL.md es el "documento de especificaciones" de un skill, y el archivo más importante para que el agente de IA comprenda el skill.

Entrada:
```
Read the SKILL.md of the following 3 skills and analyze common patterns:

1. skills/banner-creator/SKILL.md
2. skills/data-analyst/SKILL.md
3. skills/check-inbox/SKILL.md

Analyze from these perspectives and create a "SKILL.md Template":

### Standard SKILL.md Structure
- Metadata (name, description, version, dependencies)
- Overview/Purpose section
- Quick start (command examples)
- Parameters/Options
- Output examples
- Troubleshooting

### Integration Patterns with scripts/ Directory
- How SKILL.md references Python scripts in scripts/
- Script I/O patterns (CLI arguments, file input, standard output)

### Progressive Disclosure in Practice
- Stage 1 (Metadata): Description under 100 words
- Stage 2 (SKILL.md body): Details under 5,000 words
- Stage 3 (scripts/references/): Loaded only when needed

Compile the analysis into a "SKILL.md Creation Cheat Sheet".
```

**Resultado esperado**: Se extraen los patrones estandar de SKILL.md y se crea una plantilla reutilizable.

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
      {"id": "trouble_1", "label": "La estructura de directorios es demasiado compleja para entender"},
      {"id": "trouble_2", "label": "No entiendo la diferencia entre Command y Skill"},
      {"id": "trouble_3", "label": "No se como escribir SKILL.md"},
      {"id": "trouble_4", "label": "No se que buscar en el analisis de patrones"}
    ]
  }]
}
```

### Problema 1: La estructura de directorios es demasiado compleja para entender
**Causa**: Demasiados skills/commands hacen difícil ver el panorama general
**Prompt de solución**:
```
Focus on just these 2 for now:
1. .cursor/commands/lesson/start-1-1.md (the simplest lesson)
2. skills/banner-creator/ (the simplest skill)
Fully understand the structure of these 2 before expanding to others.
```

### Problema 2: No entiendo la diferencia entre Command y Skill
**Causa**: Ambos son archivos Markdown y se ven similares
**Prompt de solución**:
```
Simply put:
- Command = "Recipe" (procedure document). An instruction sheet called by the user with /command-name
- Skill = "Toolbox" (toolkit). A capability that the AI agent uses automatically

Remember: Commands are read by humans, Skills are read by agents.
```

### Problema 3: No se cómo escribir SKILL.md
**Causa**: Falta de ejemplos concretos
**Prompt de solución**:
```
Read skills/banner-creator/SKILL.md as the simplest SKILL.md example.
The minimum requirements are just 3 things: name, description, and usage (command examples).
```

### Problema 4: No se que buscar en el análisis de patrones
**Causa**: No está claro que comparar
**Prompt de solución**:
```
Analyze by answering these 3 questions:
1. What is "always present"? (common structure)
2. What "sometimes exists and sometimes doesn't"? (optional elements)
3. What is "written differently"? (variations)
```

---

## ✅ Punto de control
- [ ] Confirmo la estructura de directorios de .cursor/commands/ y .claude/commands/
- [ ] Confirmo la estructura de directorios de skills/
- [ ] Analizo los patrones comunes de los comandos de lección (frontmatter, estructura de Steps, AskQuestion)
- [ ] Analizo los patrones comunes de SKILL.md (metadata, quick start, parametros)
- [ ] Creo el "Cheat Sheet de creación de Commands"
- [ ] Creo el "Cheat Sheet de creación de SKILL.md"


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
# Verify skill directory structure
tree skills/{skill_name}/ 2>/dev/null || find skills/{skill_name}/ -maxdepth 2 -type f | head -15

# Check the beginning of SKILL.md
head -30 skills/{skill_name}/SKILL.md
```

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat para verificar la finalización:

```
# Completion check: Verify that the following cheat sheets have been created:
# 1. Command Creation Cheat Sheet (common patterns, frontmatter, Step structure)
# 2. SKILL.md Creation Cheat Sheet (standard structure, Progressive Disclosure)
```

**Resultado esperado**: Ambos cheat sheets están completos y está listo/a para crear su propio Command/Skill en la siguiente lección.

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-7-6)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-7-6
- finish → Finalizar
