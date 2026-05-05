---
description: "Lesson command — Setup de Figma + Serendie MCP"
duration: "~20 min"
prerequisites: ["cuenta de Figma + Serendie MCP"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-21"]
---

# /setup-figma -- Setup de Figma + Serendie MCP

> Conecta el plugin oficial de Figma (escritor) y Serendie MCP (fuente de conocimiento).

**Punto clave**: Sin PAT — login OAuth de navegador resuelve todo

## Pasos de setup

1. Instala el plugin Figma en Claude Code — `/plugin install figma@claude-plugins-official`

2. Inicia sesión en Figma con OAuth — `/mcp → figma → Authenticate → 'Allow Access' en el navegador`

3. Añade el MCP de Serendie — `claude mcp add --transport http serendie-mcp https://serendie.design/mcp`

4. Verifica — `claude mcp list`

5. Lleva el Serendie UI Kit a tu equipo en Figma

   ```bash
   https://www.figma.com/community/file/1433690846108785966
   ```

## Tropezones

- No podrás 'Publicar biblioteca' hasta mover el UI Kit de Community a tu equipo
- En cuentas Figma corporativas, un admin debe aprobar la app primero

## Modo no interactivo

El OAuth en navegador es obligatorio — no termina bajo `claude -p` / `cursor-agent --print`. Re-ejecuta en modo interactivo.

## Slides relacionadas

- aiagent-course Module 21: see slide deck for the full visual walkthrough
