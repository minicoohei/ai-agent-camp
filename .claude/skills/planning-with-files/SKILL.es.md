---
name: planning-with-files
version: "2.10.0"
description: "Skill para gestión de planes basada en archivos para tareas complejas. Crea task_plan.md, findings.md y progress.md. Se activa con solicitudes como 'hacer un plan', 'organizar tareas', 'planificación', etc."
triggers:
  - hacer un plan
  - organizar tareas
  - planificación
  - planning-with-files
  - crear un plan de trabajo
  - task plan
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
hooks:
  PreToolUse:
    - matcher: "Write|Edit|Bash|Read|Glob|Grep"
      hooks:
        - type: command
          command: "cat task_plan.md 2>/dev/null | head -30 || true"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[planning-with-files] Archivo actualizado. Si esto completa una fase, actualice el estado en task_plan.md.'"
  Stop:
    - hooks:
        - type: command
          command: |
            SCRIPT_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/planning-with-files}/scripts"

            IS_WINDOWS=0
            if [ "${OS-}" = "Windows_NT" ]; then
              IS_WINDOWS=1
            else
              UNAME_S="$(uname -s 2>/dev/null || echo '')"
              case "$UNAME_S" in
                CYGWIN*|MINGW*|MSYS*) IS_WINDOWS=1 ;;
              esac
            fi

            if [ "$IS_WINDOWS" -eq 1 ]; then
              if command -v pwsh >/dev/null 2>&1; then
                pwsh -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                sh "$SCRIPT_DIR/check-complete.sh"
              else
                powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                sh "$SCRIPT_DIR/check-complete.sh"
              fi
            else
              sh "$SCRIPT_DIR/check-complete.sh"
            fi
source: github.com/OthmanAdi/planning-with-files@master
---

# Planificación con Archivos

Trabaje como Manus: Use archivos markdown persistentes como su "memoria de trabajo en disco."

Para la guía completa incluyendo recuperación de sesión, reglas de ubicación de archivos, inicio rápido, patrón central, reglas críticas, protocolo de error de 3 intentos, matriz de decisión lectura vs escritura, prueba de reinicio de 5 preguntas, plantillas, scripts y anti-patrones, consulte el SKILL.md original.
