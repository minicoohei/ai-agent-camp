---
name: aiagent-check-setup
description: "Habilidad para verificar la configuracion del entorno local de ai-agent-camp. Se activa con solicitudes como 'verificar configuracion', 'chequeo de entorno', '¿esta lista la configuracion inicial?', 'verificar instalacion', 'chequeo de dependencias', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-check-setup
  - verificar configuracion
  - chequeo de entorno
  - configuracion inicial
  - verificar instalacion
  - chequeo de dependencias
  - check setup
  - セットアップ確認
  - 環境チェック
---

## Palabras Clave de Activacion
"verificar configuracion", "chequeo de entorno", "configuracion inicial", "verificar instalacion"

# Verificacion de Configuracion de Agente de IA

Utilice esta habilidad para confirmar que el estudiante puede iniciar el curso de forma segura con Codex.

## Verificaciones
- `git --version`
- `node --version`
- `npm --version`
- `python3 --version`
- `claude --version` y `cursor --version` solo si el usuario desea paridad entre herramientas
- presencia de `.env` o configuracion de credential-store sin imprimir secretos
- presencia de `.git/hooks/pre-commit` despues de `bash scripts/install_hooks.sh`
- si el estudiante ha leido la ruta de seguridad de Codex para secretos y Git

## Flujo de Trabajo
1. Leer `docs/codex-safety.md`.
2. Revisar `courses/aiagent/lesson02-setup/ch01-environment/practice/checklist.md` (omitir si esta ruta no existe).
3. Ejecutar solo verificaciones no destructivas.
4. Reportar los prerequisitos faltantes como una lista ordenada breve.
5. Si la configuracion esta completa, dirigir al estudiante a `aiagent-lesson-runner` con el siguiente id de leccion.

## No Hacer
- Imprimir valores de secretos.
- "Arreglar" la configuracion usando comandos de shell destructivos.
- Asumir que los comandos slash exclusivos de Cursor existen en Codex.
