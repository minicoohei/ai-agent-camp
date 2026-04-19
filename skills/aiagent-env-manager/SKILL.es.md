---
name: aiagent-env-manager
description: "Habilidad para gestionar de forma segura las variables de entorno y credenciales en ai-agent-camp. Se activa con solicitudes como 'configurar clave API', 'gestionar .env', 'configurar variables de entorno', 'usar credential manager', 'gestionar secretos', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-env-manager
  - configurar clave API
  - configurar variables de entorno
  - gestion de .env
  - credential manager
  - gestionar secretos
  - configurar credenciales
  - set API key
  - APIキーを設定
---

# Gestor de Entorno de Agente de IA

Utilice esta habilidad para una configuracion de entorno segura.

## Inicio Rapido
- Verifique las claves esperadas en `.env.example`.
- Prefiera `uv run python tools/credential_manager.py store <KEY>` en lugar de editar secretos en markdown.
- Use `uv run python tools/credential_manager.py status` para verificar la configuracion sin imprimir valores.

## Archivos Principales
- `.env.example`
- `tools/credential_manager.py`
- `docs/codex-safety.md`

## Flujo de Trabajo
1. Verificar si el usuario desea gestion simple de `.env` o almacenamiento de credenciales del SO.
2. Preferir `uv run python tools/credential_manager.py store <KEY>` cuando sea posible.
3. Si se requiere `.env`, limitar la guia a nombres de claves y ubicaciones de archivos.
4. Verificar la configuracion con `uv run python tools/credential_manager.py status` o verificaciones de archivos enmascarados.

## Seguridad
- Nunca mostrar valores de secretos en texto plano.
- Recordar al usuario que `.env` es solo local y debe mantenerse fuera de git.
- Si una leccion depende de una clave faltante, indicar al usuario que nombre de clave se requiere.
