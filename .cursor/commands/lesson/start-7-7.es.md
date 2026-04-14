---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module07-skill-commands/chapter.yaml"
duration: "~40 min"
prerequisites: ["start-7-5", "start-7-1"]
level: "intermediate"
tags: ["skill", "skill-design", "python", "SKILL.md"]
---

# 🎓 Lesson 7-7: Desarrollo de skills dirigido por SKILL.md

## 📍 Lo que hará en está sesion

Bienvenido/a a **Lesson 7-7: Desarrollo de skills dirigido por SKILL.md**!

| Elemento | Contenido |
|------|------|
| Objetivo | Crear un skill desde cero con SKILL.md cómo núcleo |
| Duración | ~40 min |
| Habilidades utilizadas | SKILL.md, Python |
| Requisitos previos | Lesson 7-5 completada (comprension de estructura), Lesson 7-1 recomendada (fundamentos de diseño de skills) |

**Flujo de la sesion:**
1. Decidir la idea del skill (usando AskUserQuestion)
2. Crear el borrador de SKILL.md (propósito, entrada/salida, uso)
3. Implementar un script Python en el directorio scripts/
4. Finalizar SKILL.md (cumplir con las mejores practicas de Anthropic)
5. Ejecutar pruebas de funcionamiento

Al final de está sesion, tendrá su propio skill original completado y gestionado cómo la version oficial en `skills/`.

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

## 🚀 Step 1: Decidir la idea del skill

Primero, decidamos que tipo de skill crear. Elija de las categorias a continuacion o ingrese su propia idea.

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Decidir la idea del skill",
  "questions": [{
    "id": "skill_idea",
    "prompt": "Qué tipo de skill desea crear?",
    "options": [
      {"id": "doc_creation", "label": "Document Creation (creacion de documentos)"},
      {"id": "workflow_auto", "label": "Workflow Automation (automatizacion de flujos)"},
      {"id": "data_processing", "label": "Data Processing (procesamiento de datos)"},
      {"id": "custom", "label": "Quiero crear con mi propia idea (escribirla)"}
    ]
  }]
}
```

**Ejemplos de ideas por categoria:**

### Document Creation (Creación de documentos)
| Nombre del skill | Descripción | Entrada | Salida |
|-----------------|-------------|---------|--------|
| changelog-generator | Generar CHANGELOG desde historial de Git | Repositorio Git | CHANGELOG.md |
| email-drafter | Generar texto de correo desde puntos clave | Notas/memo | Cuerpo del correo |
| invoice-generator | Generación automática de facturas | Info del cliente + items | PDF/Markdown |

### Workflow Automation (Automatización de flujos)
| Nombre del skill | Descripción | Entrada | Salida |
|-----------------|-------------|---------|--------|
| file-organizer | Organizar y renombrar archivos | Directorio | Arbol organizado |
| csv-transformer | Conversión y limpieza de formato CSV | CSV | CSV transformado |
| git-branch-cleanup | Limpieza masiva de ramas innecesarias | Repositorio Git | Informe |

### Data Processing (Procesamiento de datos)
| Nombre del skill | Descripción | Entrada | Salida |
|-----------------|-------------|---------|--------|
| log-analyzer | Análisis y resumen de archivos de log | Archivo de log | Informe de análisis |
| json-schema-validator | Validacion de esquemas JSON | JSON + esquema | Resultados de validacion |
| text-summarizer | Resumen de textos largos | Texto | Resumen |

Entrada (para su propia idea):
```
Flesh out your skill idea with the following information:

1. Skill name (English, hyphen-separated): e.g., changelog-generator
2. One-line description: e.g., Auto-generate CHANGELOG from Git history
3. Category: Document Creation / Workflow Automation / Data Processing
4. Input: What does it receive
5. Output: What does it generate
6. Who uses it: Engineer / PM / Designer / Everyone
7. Difference from existing skills: Does it overlap with existing skills in this project

Once the skill name and category are decided, proceed to Step 2.
```

**Resultado esperado**: El nombre del skill, la categoria y la entrada/salida están claramente definidos.

---

## 🚀 Step 2: Crear el borrador de SKILL.md

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear el borrador de SKILL.md",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar (crear para su propio skill)"},
      {"id": "review", "label": "Solo ver el ejemplo (ver SKILL.md de muestra)"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Cree el SKILL.md con la siguiente estructura. Basandose en Progressive Disclosure, mantenga los metadatos en menos de 100 palabras y el cuerpo en menos de 5,000 palabras.

Entrada (ejemplo para changelog-generator):
```
Create the following directory and file:

mkdir -p skills/[skill-name]/scripts

Then create skills/[skill-name]/SKILL.md with the following structure:

---
name: [skill-name]
description: "[one-line description]"
version: 1.0.0
author: [your name]
dependencies:
  python: "3.9+"
  packages: ["required packages"]
---

# /[skill-name] - [Skill Display Name]

## Overview
[2-3 sentences explaining the skill's purpose and value]

## Quick Start

### Basic Usage
```bash
python skills/[skill-name]/scripts/main.py --input [input] --output [output]
```

### With Options
```bash
python skills/[skill-name]/scripts/main.py --input [input] --format markdown --verbose
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --input | Yes | - | Input file/directory |
| --output | No | stdout | Output destination (file path or stdout) |
| --format | No | markdown | Output format (markdown / json / text) |
| --verbose | No | false | Verbose log output |

## Output Example

[Include actual output sample]

## Trigger Phrases

This skill activates on requests like:
- "[Phrase 1]"
- "[Phrase 2]"
- "[Phrase 3]"

## Notes
- [Constraint 1]
- [Constraint 2]
```

**Resultado esperado**: Se completa el borrador de SKILL.md y el diseño general del skill queda claro.

---

## 🚀 Step 3: Implementar el script Python

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Implementar el script Python",
  "questions": [{
    "id": "step_action",
    "prompt": "Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar (crear un script para su skill)"},
      {"id": "review", "label": "Solo ver el ejemplo (ver script de muestra)"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la selección:**

Implemente scripts/main.py siguiendo el patrón estandar a continuacion.

Entrada:
```
Create skills/[skill-name]/scripts/main.py.

Implement following this pattern:

#!/usr/bin/env python3
"""
[skill-name] - [one-line description]

Usage:
    python main.py --input <input> [--output <output>] [--format <format>]
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="[skill description]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --input data.csv
    python main.py --input data.csv --output report.md --format markdown
        """
    )
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", default=None, help="Output file path (defaults to stdout)")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "text"], default="markdown", help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose log output")
    parser.add_argument("--test", action="store_true", help="Run in test mode")
    return parser.parse_args()


def validate_input(input_path: str) -> Path:
    """Verify input file exists"""
    path = Path(input_path)
    if not path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    return path


def process(input_path: Path, output_format: str, verbose: bool) -> str:
    """Main processing (implement skill-specific logic here)"""
    if verbose:
        print(f"Processing: {input_path}", file=sys.stderr)

    # TODO: Implement skill-specific processing here
    result = f"# Processing Result\n\n- Input: {input_path}\n- Format: {output_format}\n- Processed at: {datetime.now().isoformat()}\n"

    return result


def output_result(result: str, output_path: str = None):
    """Output results"""
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(result, encoding="utf-8")
        print(f"Output complete: {output_path}", file=sys.stderr)
    else:
        print(result)


def run_test():
    """Test mode"""
    print("=== Test Mode ===")
    test_input = Path("/tmp/test_input.txt")
    test_input.write_text("Test data", encoding="utf-8")

    result = process(test_input, "markdown", verbose=True)
    print(result)
    print("=== Test Complete ===")

    test_input.unlink(missing_ok=True)


def main():
    args = parse_args()

    if args.test:
        run_test()
        return

    input_path = validate_input(args.input)
    result = process(input_path, args.format, args.verbose)
    output_result(result, args.output)


if __name__ == "__main__":
    main()

---

Replace the "TODO" section in the template above with your skill-specific processing.
Rewrite the contents of the process() function to match your skill's purpose.
```

**Resultado esperado**: main.py está completado y se puede verificar con `python main.py --test`.

---

## 🚀 Step 4: Finalizar SKILL.md

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Finalizar SKILL.md",
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

Refleje lo implementado en el Step 3 y finalice el SKILL.md. Verifique el cumplimiento con las mejores practicas de Anthropic.

Entrada:
```
Improve the SKILL.md created in Step 2 from the following perspectives:

### Anthropic Best Practices Checklist

1. **Progressive Disclosure**
   - [ ] Is metadata (name + description) under 100 words
   - [ ] Is SKILL.md body under 5,000 words
   - [ ] Is scripts/ configured to load only when needed

2. **Trigger Accuracy**
   - [ ] Are there 5+ phrases that should correctly activate
   - [ ] Are there 3+ phrases that should NOT activate
   - [ ] Is there no trigger collision with existing skills

3. **Input/Output Clarity**
   - [ ] Are input specifications (format, required/optional) documented
   - [ ] Are output samples included
   - [ ] Is error behavior explained

4. **Practicality**
   - [ ] Do quick start command examples work with copy-paste
   - [ ] Is the parameter table complete
   - [ ] Are notes/constraints documented

Update the SKILL.md based on this checklist.
```

**Resultado esperado**: SKILL.md se convierte en la version finalizada conforme a las mejores practicas.

---

## 🚀 Step 5: Pruebas de funcionamiento

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Pruebas de funcionamiento",
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
Run operation tests on the skill you created:

1. Verify directory structure
   tree skills/[skill-name]/

   Expected structure:
   [skill-name]/
   ├── SKILL.md
   └── scripts/
       └── main.py

2. Run in test mode
   python skills/[skill-name]/scripts/main.py --test

3. Run with real data
   python skills/[skill-name]/scripts/main.py --input [actual file] --verbose

4. Verify error cases
   python skills/[skill-name]/scripts/main.py --input nonexistent_file.txt
   → Is an appropriate error message displayed?

5. Verify output formats
   python skills/[skill-name]/scripts/main.py --input [file] --format json
   python skills/[skill-name]/scripts/main.py --input [file] --format text

If all tests pass, the skill is complete.
```

**Resultado esperado**: Tanto los casos normales cómo los de error se comportan cómo se espera.

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
      {"id": "trouble_1", "label": "El script Python no se ejecuta"},
      {"id": "trouble_2", "label": "No se como escribir SKILL.md"},
      {"id": "trouble_3", "label": "El skill no es reconocido por Claude Code"},
      {"id": "trouble_4", "label": "No se me ocurre una idea"}
    ]
  }]
}
```

### Problema 1: El script Python no se ejecuta
**Causa**: Problemas de ruta o paquetes de dependencias
**Prompt de solución**:
```
Check the following:
1. Is python3 --version 3.9 or higher
2. Are required packages installed (pip install [package-name])
3. Does the script have execution permissions (chmod +x scripts/main.py)
4. Is the file encoding UTF-8
```

### Problema 2: No se cómo escribir SKILL.md
**Causa**: La plantilla es demasiado abstracta
**Prompt de solución**:
```
The simplest SKILL.md only needs these 3 sections:
1. Metadata (name, description)
2. Quick start (one command example)
3. Parameter table
Write just these 3 first, then add more later.
```

### Problema 3: El skill no es reconocido por Claude Code
**Causa**: Problema de ubicacion del directorio
**Prompt de solución**:
```
Skills must be placed in skills/[skill-name]/.
Check the following:
1. Is SKILL.md at skills/[skill-name]/SKILL.md
2. Is the filename exactly SKILL.md (case-sensitive)
3. Restart Claude Code and try invoking with /skill-name
```

### Problema 4: No se me ocurre una idea
**Causa**: El concepto de skills es abstracto
**Prompt de solución**:
```
Answer these questions:
1. What did you find "tedious" in yesterday's work?
2. What task do you repeat every week?
3. What have you thought "I wish this could be automated"?
That answer is your skill idea.
```

---

## ✅ Punto de control
- [ ] La idea del skill (nombre, categoria, entrada/salida) está decidida
- [ ] El borrador de SKILL.md está creado
- [ ] scripts/main.py está implementado
- [ ] SKILL.md cumple con las mejores practicas de Anthropic
- [ ] Verifico el funcionamiento en modo de prueba (--test)
- [ ] Verifico el funcionamiento con datos reales
- [ ] Verifico el comportamiento en casos de error


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
# Completion check: Verify the following:
# 1. Does skills/[skill-name]/SKILL.md exist
# 2. Does skills/[skill-name]/scripts/main.py exist
# 3. Does python skills/[skill-name]/scripts/main.py --test succeed
```

**Resultado esperado**: La estructura del directorio del skill es correcta y las pruebas pasan.

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-7-8)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Tras la selección:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-7-8
- finish → Finalizar
