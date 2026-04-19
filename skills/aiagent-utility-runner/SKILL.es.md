---
name: aiagent-utility-runner
description: "Habilidad para ejecutar comandos de utilidad y configuracion de ai-agent-camp en Codex. Se activa con solicitudes como 'ejecutar /guide', '/setup-api-key', 'comando de utilidad', 'usar utilidad de Cursor', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-utility-runner
  - comando de utilidad
  - /guide
  - /setup-api-key
  - ejecutar utilidad
  - utility runner
  - ユーティリティコマンド
---

# Ejecutor de Utilidades de Agente de IA

Utilice esta habilidad para reproducir flujos de trabajo de comandos de utilidad y configuracion en Codex.

## Flujo de Trabajo
1. Resolver el id canonico del comando desde `data/codex-command-manifest.json`.
2. Abrir el archivo fuente de comando markdown listado en el manifiesto.
3. Reutilizar una habilidad de Codex existente si alguna ya coincide con la tarea.
4. De lo contrario, seguir las instrucciones del comando fuente directamente, usando scripts y archivos locales en lugar de simular que existe un entorno de ejecucion slash.
5. Cuando sea util para pruebas o depuracion, mostrar la traza del manejador de `tools/codex_command_router.py --trace`.

## Referencias Requeridas
- `data/codex-command-manifest.json`
- `tools/codex_command_router.py`
- `.cursor/commands/utility/*.md`
- `.cursor/commands/*.md`

## Salida
- El id de utilidad resuelto
- El archivo fuente que se esta siguiendo
- Los pasos o scripts locales ejecutados en Codex
