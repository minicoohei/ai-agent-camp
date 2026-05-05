---
description: "Lesson command — Setup de M365 CLI"
duration: "~20 min"
prerequisites: ["cuenta de Microsoft 365 CLI (PnP CLI)"]
level: "intermediate"
nonInteractiveMode: deferred
tags: ["setup", "module-19"]
---

# /setup-m365cli -- Setup de M365 CLI

> Maneja Microsoft 365 (Outlook / SharePoint / Teams) desde un único CLI: `@pnp/cli-microsoft365`. Auth por device code, nada más.

**Punto clave**: Sin PAT — solo OAuth device code

## Pasos de setup

1. Confirma Node.js 18+ — `node -v`

2. Instala @pnp/cli-microsoft365 (versión fijada) — `npm install -g @pnp/cli-microsoft365@7.x`

3. Inicia sesión con device code

   ```bash
   m365 login
# Abre la URL impresa en el navegador e introduce el código
   ```

4. Verifica — `m365 status`

## Tropezones

- Evita `m365 logout` si quieres mantener la sesión — el token persiste hasta caducar
- En WSL, abre la URL en tu navegador de Windows (el CLI no lanza navegador allí)

## Modo no interactivo

Necesita navegador, así que en modo `-p` solo ejecuta los chequeos read-only, escribe `setup-resume.md` y sale.

## Slides relacionadas

- aiagent-course Module 19: see slide deck for the full visual walkthrough
