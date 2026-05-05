---
description: "Lesson command — Setup de Freee MCP"
duration: "~30 min"
prerequisites: ["cuenta de Freee MCP"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-20"]
---

# /setup-freee -- Setup de Freee MCP

> Conéctate a freee Contabilidad vía MCP. Requiere OAuth de navegador + Client ID/Secret.

**Punto clave**: App en Freee Developer + OAuth de navegador obligatorio

## Pasos de setup

1. Crea una app en el Freee Developer Portal

   ```bash
   https://app.secure.freee.co.jp/developers/applications
   ```

2. Guarda Client ID / Client Secret — `(solo navegador)`

3. Instala freee-mcp (versión fijada) — `npm install -g freee-mcp@0.26.0`

4. Registra el MCP — `claude mcp add --transport stdio freee -- npx freee-mcp@0.26.0`

5. Autoriza con el flujo OAuth del navegador — `sigue las indicaciones del MCP`

## Tropezones

- Obtén tu company ID con `freee_get_companies` → guárdalo en `~/.config/freee-mcp/config.json`
- Sandbox y producción son apps distintas. Prueba en sandbox y luego cambia a la app de producción

## Modo no interactivo

El OAuth en navegador es obligatorio — no termina bajo `claude -p` / `cursor-agent --print`. Re-ejecuta en modo interactivo.

## Slides relacionadas

- aiagent-course Module 20: see slide deck for the full visual walkthrough
