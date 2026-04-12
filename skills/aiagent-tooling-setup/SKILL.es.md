---
name: aiagent-tooling-setup
description: "Habilidad para configurar las herramientas de Codex para ai-agent-camp. Se activa con solicitudes como 'configurar servidor MCP', 'instalar hooks', 'configuracion de Codex', 'configuracion de herramientas', 'instalar Codex CLI', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-tooling-setup
  - configurar servidor MCP
  - instalar hooks
  - configuracion de Codex
  - configuracion de herramientas
  - Codex CLI
  - tooling setup
  - MCPサーバー設定
  - ツールセットアップ
---

# Configuracion de Herramientas de Agente de IA

Codex CLI es un asistente de codificacion basado en terminal proporcionado por OpenAI.

Utilice esta habilidad cuando el usuario necesite orientacion especifica sobre herramientas de Codex.

## Flujo de Trabajo
1. Leer `docs/codex-mcp.md`.
2. Identificar si la solicitud es sobre herramientas del repositorio, hooks del repositorio o servidores MCP.
3. Preferir scripts existentes del repositorio sobre instrucciones de shell ad hoc.
4. Mantener la respuesta final enfocada en la ruta exacta de herramientas que el estudiante necesita.

## Comandos del Repositorio
- `bash scripts/install_hooks.sh`
- `uv run python tools/check_command_paths.py`
- `uv run python tools/credential_manager.py status`

## Instalacion y Autenticacion de Codex CLI

### Instalacion
```bash
npm install -g @openai/codex
codex --version   # verificar instalacion
```
Requiere Node.js 18+.

### Autenticacion
Configure la clave API de OpenAI mediante variable de entorno:
```bash
export OPENAI_API_KEY="su-clave-api-aqui"
```
O agregue `OPENAI_API_KEY=...` al archivo `.env` del repositorio (nunca haga commit de este archivo).

### Configuracion de Ejecucion Recomendada
| Configuracion | Valor | Razon |
|---------------|-------|-------|
| Sandbox | `workspace-write` | Restringe escrituras al directorio del repositorio |
| Aprobacion | `on-request` | Pregunta antes de comandos externos |

Ejecute con:
```bash
codex -a on-request
```

Evite `danger-full-access` para flujos de aprendizaje normales. Consulte `docs/codex-safety.md`.

### Flujo de Primera Vez
1. Instalar Codex CLI (`npm install -g @openai/codex`)
2. Configurar `OPENAI_API_KEY`
3. Abrir ai-agent-camp y ejecutar `bash scripts/install_hooks.sh`
4. Usar la habilidad `aiagent-check-setup` para verificar el entorno
5. Iniciar lecciones a traves de la habilidad `aiagent-lesson-runner`

## Recordatorios
- Mantener las reglas del proyecto en `AGENTS.md`.
- Mantener configuraciones especificas de la maquina en la capa de configuracion de Codex.
- Evitar implicar que los archivos de comandos de Cursor son ejecutables en Codex.
