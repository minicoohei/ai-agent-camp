---
description: "Lesson command — Setup de Salesforce CLI (sf)"
duration: "~15 min"
prerequisites: ["cuenta de Salesforce CLI (sf)"]
level: "intermediate"
nonInteractiveMode: incompatible
tags: ["setup", "module-24"]
---

# /setup-salesforce -- Setup de Salesforce CLI (sf)

> Maneja organizaciones Salesforce desde el CLI `sf`. Sin Connected App — basta OAuth de navegador.

**Punto clave**: Sin Connected App — solo OAuth de navegador

## Pasos de setup

1. Instala Salesforce CLI (versión fijada, npm recomendado) — `npm install -g @salesforce/cli@2.x`

2. Inicia sesión en Producción — `sf org login web --alias prod`

3. Para Sandbox — `sf org login web --alias dev --instance-url https://test.salesforce.com`

4. Verifica — `sf org list`

## Tropezones

- `sf` v1 (`sfdx`) y v2 (`sf`) tienen comandos distintos — usa v2
- Para Sandbox pon siempre `--instance-url https://test.salesforce.com`

## Modo no interactivo

El OAuth en navegador es obligatorio — no termina bajo `claude -p` / `cursor-agent --print`. Re-ejecuta en modo interactivo.

## Slides relacionadas

- aiagent-course Module 24: see slide deck for the full visual walkthrough
