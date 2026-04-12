---
name: aiagent-guide
description: "Habilidad de orientacion y navegacion para el repositorio ai-agent-camp. Se activa con solicitudes como 'guia del repositorio', '¿cual es la siguiente leccion?', '¿por donde empiezo?', 'diferencias entre herramientas', 'resumen de aiagent', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-guide
  - guia del repositorio
  - siguiente leccion
  - por donde empezar
  - diferencias de herramientas
  - resumen de aiagent
  - guide
  - リポジトリ案内
  - 次のレッスン
---

## Palabras Clave de Activacion
"guia del repositorio", "siguiente leccion", "por donde empezar", "diferencias de herramientas", "resumen de aiagent"

# Guia de Agente de IA

Utilice esta habilidad para orientar al usuario dentro de `ai-agent-camp`.

## Flujo de Trabajo
1. Leer `AGENTS.md`.
2. Leer `README.md` si se necesita una vision general mas amplia.
3. Si el usuario pregunta por donde empezar, recomendar:
   - `aiagent-check-setup` para la preparacion del entorno
   - `aiagent-lesson-runner` para cualquier id de leccion `start-*`
4. Explicar el modelo de lecciones compartido y las diferencias entre Codex, Claude Code y Cursor solo al nivel que los estudiantes necesiten.
5. Para tareas mas grandes, indicar al usuario que haga un plan breve antes de la implementacion.
6. Mantener las explicaciones breves y vincularlas a archivos reales.

## Referencias Requeridas
- `AGENTS.md`
- `CLAUDE.md` -- Instrucciones del proyecto Claude Code
- `docs/codex-guide.md`

## Salida
- Un resumen breve de orientacion
- Las diferencias relevantes entre herramientas cuando sea necesario
- El siguiente archivo o habilidad a utilizar
- Cualquier advertencia de seguridad relevante para la tarea solicitada
