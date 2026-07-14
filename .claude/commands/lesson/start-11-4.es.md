---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "~25 min"
prerequisites: ["start-11-2"]
level: "intermediate"
tags: ["github-actions", "claude-code", "codex", "ai", "automation", "code-review"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-4: Llamar a Claude Code / Codex / Cursor desde GitHub Actions

## 📍 Lo que hara en esta sesion

**Leccion 11-4: Llamar a AI CLI desde GitHub Actions**!

| Elemento | Contenido |
|------|------|
| Objetivo | Ejecutar Claude Code CLI / Codex CLI dentro de flujos de trabajo de GitHub Actions para realizar revisiones de codigo y generacion automatica de PRs |
| Duracion | ~25 min |
| Habilidades utilizadas | GitHub Actions, Claude Code CLI, Codex CLI, gh CLI |
| Requisitos previos | Leccion 11-2 completada (comprension de la configuracion de Secrets) |

**Flujo de la sesion:**
1. Descripcion general de herramientas AI CLI y patrones de uso
2. Ejecucion de Claude Code en un flujo de trabajo
3. Creacion de un flujo de trabajo de revision automatica de PRs
4. Ejecucion de Codex CLI en un flujo de trabajo
5. Ejercicio practico: Pipeline Issue → Implementacion AI → Creacion automatica de PR

Al final de esta sesion, tendra flujos de trabajo construidos que aprovechan las herramientas AI CLI en GitHub Actions.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar.

---

## 🎯 Verificacion de preparacion

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
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar que la Leccion 11-2 esta completada. Verificar el estado de preparacion de las API keys)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Descripcion general de herramientas AI CLI

```json
{
  "title": "🚀 Step 1: Descripcion general de herramientas AI CLI",
  "questions": [{
    "id": "step_action",
    "prompt": "Revisaremos las herramientas AI CLI disponibles para usar en GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar las diferencias entre herramientas"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

| Herramienta | Comando | API Key | Uso principal |
|--------|---------|---------|---------|
| Claude Code | `claude -p "prompt"` | `ANTHROPIC_API_KEY` | Revision de codigo, implementacion, analisis |
| Codex CLI | `codex -q "prompt"` | `OPENAI_API_KEY` | Generacion de codigo, correcciones, preguntas y respuestas |

**Patron comun en GitHub Actions:**
```yaml
# Las API keys siempre se pasan via Secrets
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**API keys a configurar en Secrets:**
- `ANTHROPIC_API_KEY`: Para Claude Code (obtener en la consola de Anthropic)
- `OPENAI_API_KEY`: Para Codex (obtener en la consola de OpenAI)

**Resultado esperado**: Comprender las diferencias entre cada herramienta y la configuracion necesaria.

---

## 🚀 Step 2: Ejecucion de Claude Code en un flujo de trabajo

```json
{
  "title": "🚀 Step 2: Flujo de trabajo de Claude Code",
  "questions": [{
    "id": "step_action",
    "prompt": "Crearemos un flujo de trabajo que ejecuta Claude Code CLI en GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar las opciones del CLI de claude"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/claude-review.yml`:

```yaml
name: Claude Code Review
on:
  pull_request:
    types: [opened, synchronize]
  workflow_dispatch:
    inputs:
      prompt:
        description: 'Prompt para enviar a Claude'
        type: string
        default: 'Analiza la calidad del codigo de este repositorio'

jobs:
  claude-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Claude Code review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          if [ "${{ github.event_name }}" = "pull_request" ]; then
            DIFF=$(git diff ${{ github.event.pull_request.base.sha }}..HEAD)
            PROMPT="Revisa el siguiente diff. Resume los problemas, sugerencias de mejora y puntos positivos:\n\n$DIFF"
          else
            PROMPT="${{ inputs.prompt }}"
          fi
          claude -p "$PROMPT" --output-format text > review_result.txt

      - name: Post review comment
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review_result.txt', 'utf8');
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: `## 🤖 Claude Code Review\n\n${review}`
            });
```

**Puntos clave:**
- `claude -p` pasa el prompt directamente (modo no interactivo)
- En el trigger de PR, se pasa el `git diff` para la revision
- `actions/github-script` publica el resultado de la revision como comentario en el PR

**Resultado esperado**: Cuando se crea un PR, Claude Code realiza una revision automatica y publica un comentario.

---

## 🚀 Step 3: Flujo de trabajo de revision automatica de PRs

```json
{
  "title": "🚀 Step 3: Revision automatica de PRs",
  "questions": [{
    "id": "step_action",
    "prompt": "Mejoraremos el flujo de trabajo para analizar los cambios del PR y publicar comentarios de revision estructurados.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar los criterios de revision"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Mejorar el prompt de revision:

```yaml
      - name: Run structured review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          DIFF=$(git diff ${{ github.event.pull_request.base.sha }}..HEAD)
          cat <<'PROMPT' > /tmp/review_prompt.txt
          Revisa el siguiente diff.

          ## Criterios de revision
          1. **Riesgo de bugs**: Bugs potenciales o casos limite
          2. **Seguridad**: Vulnerabilidades o secretos hardcodeados
          3. **Rendimiento**: Procesamiento ineficiente o problemas N+1
          4. **Legibilidad**: Adecuacion de nombres, estructura y comentarios
          5. **Tests**: Falta de cobertura de pruebas

          ## Formato de salida
          Para cada criterio, responda con "✅ Sin problemas" o "⚠️ Requiere revision: indicacion especifica".

          ## Diff
          PROMPT
          echo "$DIFF" >> /tmp/review_prompt.txt
          claude -p "$(cat /tmp/review_prompt.txt)" --output-format text > review_result.txt
```

**Resultado esperado**: Se publican comentarios de revision estructurados en el PR.

---

## 🚀 Step 4: Ejecucion de Codex CLI en un flujo de trabajo

```json
{
  "title": "🚀 Step 4: Codex CLI",
  "questions": [{
    "id": "step_action",
    "prompt": "Crearemos un flujo de trabajo que ejecuta Codex CLI en GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar las opciones de Codex CLI"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/codex-task.yml`:

```yaml
name: Codex Task Runner
on:
  workflow_dispatch:
    inputs:
      task:
        description: 'Tarea a ejecutar por Codex'
        type: string
        required: true

jobs:
  codex-run:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Codex CLI
        run: npm install -g @openai/codex

      - name: Run Codex
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex -q "${{ inputs.task }}" --approval-mode full-auto
          
      - name: Check for changes
        id: changes
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            echo "has_changes=true" >> $GITHUB_OUTPUT
          fi

      - name: Create PR with changes
        if: steps.changes.outputs.has_changes == 'true'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BRANCH="codex/auto-$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"
          git add -A
          git commit -m "feat: Implementacion automatica por Codex — ${{ inputs.task }}"
          git push origin "$BRANCH"
          gh pr create \
            --title "🤖 Codex: ${{ inputs.task }}" \
            --body "Implementacion automatica por Codex CLI.\n\nTarea: ${{ inputs.task }}" \
            --base main
```

**Puntos clave:**
- `--approval-mode full-auto` para ejecucion completamente automatica
- Si hay cambios, se crea automaticamente un PR
- `GITHUB_TOKEN` es proporcionado automaticamente por GitHub

**Resultado esperado**: Al especificar una tarea con `gh workflow run`, Codex la implementa y crea un PR.

---

## 🚀 Step 5: Ejercicio practico — Pipeline Issue → Implementacion AI → PR

```json
{
  "title": "🚀 Step 5: Ejercicio practico",
  "questions": [{
    "id": "step_action",
    "prompt": "Construiremos un pipeline donde al crear un Issue, la IA lo implementa automaticamente y crea un PR.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar el mecanismo del trigger de Issues"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/ai-implement.yml`:

```yaml
name: AI Auto-Implement
on:
  issues:
    types: [labeled]

jobs:
  implement:
    if: contains(github.event.issue.labels.*.name, 'ai-implement')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Implement from issue
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          TITLE="${{ github.event.issue.title }}"
          BODY="${{ github.event.issue.body }}"
          claude -p "Implementa el siguiente Issue:\n\nTitulo: $TITLE\n\nContenido:\n$BODY" \
            --output-format text > implementation_log.txt

      - name: Create PR
        if: ${{ success() }}
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          if [ -n "$(git status --porcelain)" ]; then
            BRANCH="ai/issue-${{ github.event.issue.number }}"
            git checkout -b "$BRANCH"
            git add -A
            git commit -m "feat: Implementacion AI del #${{ github.event.issue.number }}"
            git push origin "$BRANCH"
            gh pr create \
              --title "🤖 Implementacion AI: ${{ github.event.issue.title }}" \
              --body "Closes #${{ github.event.issue.number }}\n\nImplementacion automatica por Claude Code." \
              --base main
          fi
```

**Pasos de prueba:**
1. Crear un Issue (ejemplo: "Agregar seccion Contributing al README")
2. Asignar la etiqueta `ai-implement`
3. El flujo de trabajo se ejecuta automaticamente → Se crea un PR

**Resultado esperado**: Se genera automaticamente un PR a partir de un Issue con la etiqueta correspondiente.

---

## ⚠️ Problemas comunes y soluciones

```json
{
  "title": "⚠️ Solucion de problemas",
  "questions": [{
    "id": "trouble",
    "prompt": "Ha encontrado algun problema?",
    "options": [
      {"id": "trouble_1", "label": "Error de API key"},
      {"id": "trouble_2", "label": "Comando claude / codex no encontrado"},
      {"id": "trouble_3", "label": "Error de permisos al crear PR"},
      {"id": "trouble_4", "label": "El comentario de revision no se publica"}
    ]
  }]
}
```

### Problema 1: "Error de API key"
**Causa**: La API key no esta configurada en Secrets o la clave es invalida.
**Solucion**:
```text
Verifique en Settings → Secrets and variables → Actions del repositorio de GitHub que ANTHROPIC_API_KEY esta configurado. La clave debe comenzar con sk-ant-.
```

### Problema 2: "Comando claude / codex no encontrado"
**Causa**: La instalacion con npm ha fallado.
**Solucion**:
```text
Revise los errores en el paso de npm install en los logs del flujo de trabajo. Verifique que la version de Node.js sea 18 o superior.
```

### Problema 3: "Error de permisos al crear PR"
**Causa**: La configuracion de `permissions` es insuficiente.
**Solucion**:
```text
Verifique que el flujo de trabajo incluye contents: write y pull-requests: write en permissions. Verifique que en Settings → Actions → General → Workflow permissions este habilitado "Read and write permissions".
```

### Problema 4: "El comentario de revision no se publica"
**Causa**: Hay un error en el script de `actions/github-script` o falta el permiso pull-requests: write.
**Solucion**:
```text
Revise los errores en el paso de actions/github-script en los logs del flujo de trabajo. Si review_result.txt esta vacio, verifique el resultado de la ejecucion de Claude Code.
```

---

## ✅ Punto de control

- [ ] Claude Code CLI se ejecuta correctamente dentro del flujo de trabajo
- [ ] Se publican comentarios de revision al activarse por PR
- [ ] Codex CLI se ejecuta correctamente dentro del flujo de trabajo
- [ ] El pipeline Issue → Implementacion AI → PR funciona
- [ ] Las API keys estan almacenadas de forma segura en Secrets

---

## 📋 Vista previa de entregables

**Flujos de trabajo creados:**
```text
.github/workflows/
├── claude-review.yml      # Revision automatica de PRs
├── codex-task.yml         # Ejecucion de tareas con Codex
└── ai-implement.yml       # Issue → Implementacion AI → PR
```

---

## ➡️ Siguientes pasos

```json
{
  "title": "➡️ Siguientes pasos",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_auto", "label": "Avanzar a la Leccion 11-5 (Despliegue y generacion de archivos) → /start-11-5"},
      {"id": "review_module", "label": "Revisar los entregables de esta leccion"},
      {"id": "finish", "label": "Terminar por hoy"}
    ]
  }]
}
```
