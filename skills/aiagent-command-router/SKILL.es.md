---
name: aiagent-command-router
description: "Habilidad para enrutar comandos slash de ai-agent-camp en Codex. Se activa con solicitudes como 'ejecutar /start-0-1', 'quiero usar comandos slash', 'enrutamiento de comandos', 'usar comandos de Cursor', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-command-router
  - enrutamiento de comandos
  - comando slash
  - /start-
  - comandos de Cursor
  - command routing
  - slash command
  - コマンドルーティング
---

# Enrutador de Comandos de Agente de IA

Utilice esta habilidad cuando un usuario escribe una cadena de comando existente de ai-agent-camp en Codex.

## Flujo de Trabajo
1. Resolver el comando a traves de `data/codex-command-manifest.json`.
2. Si el comando es una ruta de leccion, delegar a `aiagent-lesson-runner` con el id de leccion resuelto.
3. Si el comando es una ruta de utilidad, delegar a `aiagent-utility-runner` con el id de utilidad resuelto.
4. Si el comando no esta mapeado, indicar que aun no es compatible con Codex y mostrar la ruta del archivo fuente mas cercano.

## Referencias Requeridas
- `data/codex-command-manifest.json`
- `tools/codex_command_router.py`
- `skills/aiagent-lesson-runner/SKILL.md`
- `skills/aiagent-utility-runner/SKILL.md`

## Salida
- El manejador resuelto y el id canonico
- La siguiente accion tomada en Codex
- Un mensaje claro de no mapeado cuando no existe ruta
