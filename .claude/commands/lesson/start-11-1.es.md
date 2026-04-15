---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
prerequisites: ["start-0-1"]
duration: "~35 min"
level: "intermediate"
tags: ["github-actions", "ci-cd", "automation"]
---

# 🎓 Lesson 11-1: Fundamentos de GitHub Actions

## 📍 Lo que hara en esta sesion

**Lección 11-1: Introducción a GitHub Actions**!

| Elemento | Contenido |
|------|------|
| Objetivo | Construir pipelines CI/CD con GitHub Actions (pruebas y despliegue automatizados) |
| Duracion | ~35 min |
| Habilidades utilizadas | GitHub Actions, flujos de trabajo YAML |
| Requisitos previos | Repositorio GitHub, se recomienda completar la Leccion 0-1 (gh CLI) |
| Pagina del curso | [Module 11: GitHub Actions](https://ai-agent.camp/es/course/module-11)  como referencia paralela |

**Flujo de la sesion:**
1. Crear el directorio de flujos de trabajo
2. Flujo de trabajo Hello World
3. Flujo de trabajo de configuración del entorno Python
4. Flujo de trabajo de ejecución programada
5. Flujo de trabajo de múltiples trabajos

Al final de esta sesion, las pruebas y despliegues se ejecutaran automaticamente al hacer push.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
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
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Create Workflow Directory

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Crear directorio de flujos de trabajo",
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
Por favor, cree el directorio de flujos de trabajo de GitHub Actions en el proyecto ai-agent-camp.

mkdir -p .github/workflows

Verifique que el directorio se haya creado.
```

**Resultado esperado:** Se crea el directorio `.github/workflows/`.

---

## 🚀 Step 2: Hello World Workflow

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Flujo de trabajo Hello World",
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
Por favor, cree el archivo .github/workflows/hello.yml con el siguiente contenido:

name: Hello World

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest

    steps:
      - name: Say Hello
        run: echo "Hello, GitHub Actions!"

      - name: Print Date
        run: date

      - name: Print Environment
        run: |
          echo "GitHub Actor: ${{ github.actor }}"
          echo "GitHub Repository: ${{ github.repository }}"
          echo "GitHub Event: ${{ github.event_name }}"
```

**Resultado esperado:** Se crea un archivo YAML. Se ejecuta automaticamente al hacer push a GitHub.

---

## 🚀 Step 3: Python Environment Setup Workflow

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Flujo de trabajo de configuración del entorno Python",
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
Por favor, cree el archivo .github/workflows/python-ci.yml con el siguiente contenido:

name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          # uv は自動で最新のパッケージを管理します
          uv add pytest
          if [ -f pyproject.toml ]; then uv sync; fi

      - name: Run simple test
        run: |
          python -c "print('Python CI is working!')"
          python --version
```

**Resultado esperado:** Se crea un flujo de trabajo para configurar el entorno Python y ejecutar pruebas.

---

## 🚀 Step 4: Scheduled Execution Workflow

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Flujo de trabajo de ejecución programada",
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
Por favor, cree el archivo .github/workflows/scheduled.yml con el siguiente contenido:

name: Scheduled Task

on:
  schedule:
    # Ejecutar diariamente a las 09:00 UTC (18:00 JST)
    - cron: '0 9 * * *'
  workflow_dispatch:
    inputs:
      task_name:
        description: 'Nombre de la tarea'
        required: true
        default: 'daily_check'
        type: choice
        options:
          - daily_check
          - weekly_report

jobs:
  scheduled-task:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run scheduled task
        run: |
          echo "Running scheduled task at $(date)"
          echo "Task: ${{ github.event.inputs.task_name || 'daily_check' }}"

      - name: Check files
        run: |
          echo "Repository files:"
          ls -la
```

**Resultado esperado:** Se crea un flujo de trabajo que soporta tanto la ejecucion programada como los triggers manuales.

---

## 🚀 Step 5: Multi-Job Workflow

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Flujo de trabajo de múltiples trabajos",
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
Por favor, cree el archivo .github/workflows/multi-job.yml con el siguiente contenido:

name: Multi-Job Workflow

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      build_status: ${{ steps.build.outputs.status }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build
        id: build
        run: |
          echo "Building project..."
          echo "status=success" >> $GITHUB_OUTPUT
          echo "Build completed!"

  test:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Test
        run: |
          echo "Build status: ${{ needs.build.outputs.build_status }}"
          echo "Running tests..."
          echo "Tests passed!"

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test]
    if: github.ref == 'refs/heads/main'

    steps:
      - name: Deploy
        run: |
          echo "Deploying to production..."
          echo "Deployment completed!"
```

**Resultado esperado:** Se crea un flujo de trabajo de multiples trabajos que se ejecuta en orden build -> test -> deploy.

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
      {"id": "trouble_1", "label": "Workflow file invalid"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Command not found"},
      {"id": "trouble_4", "label": "La ejecución programada no funciona"}
    ]
  }]
}
```


### Problema 1: "Workflow file invalid"
**Causa:** Error de sintaxis YAML
**Prompt de solucion:**
```
Por favor, verifique la sintaxis del archivo YAML.
Verifique que la indentación use 2 espacios de manera consistente.
Verifique que haya un espacio después de los dos puntos.
```

### Problema 2: "Permission denied"
**Causa:** El script no tiene permisos de ejecucion
**Prompt de solucion:**
```
Por favor, añada un paso para ejecutar chmod +x script.sh dentro del flujo de trabajo.
```

### Problema 3: "Command not found"
**Causa:** Los programas necesarios no estan instalados
**Prompt de solucion:**
```
Por favor, añada acciones de configuración como actions/setup-python y actions/setup-node.
Añada un paso para instalar los paquetes necesarios.
```

### Problema 4: La ejecucion programada no funciona
**Causa:** Error de configuracion de Cron o no se ejecuta en la rama predeterminada
**Prompt de solucion:**
```
Por favor, verifique que la expresión cron sea correcta (especificada en hora UTC).
Verifique que el flujo de trabajo exista en la rama predeterminada (main).
Ejecute manualmente con workflow_dispatch para verificar el funcionamiento.
```

---

## ✅ Punto de control
- [ ] El directorio .github/workflows/ existe
- [ ] hello.yml ha sido creado
- [ ] python-ci.yml ha sido creado
- [ ] scheduled.yml ha sido creado
- [ ] multi-job.yml ha sido creado
- [ ] Los flujos de trabajo se muestran en GitHub


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 .github/workflows/
└── {workflow}.yml  (flujo de trabajo de GitHub Actions)
```

### Comandos de verificacion
```bash
# Lista de archivos de flujo de trabajo
ls -la .github/workflows/

# Verificar contenido del archivo
cat .github/workflows/{workflow}.yml

# Verificar estado de ejecución en GitHub
gh run list --limit 5
```

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestran el estado completado/incompleto y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-11-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-11-2
- finish → Finalizar
