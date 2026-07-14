---
description: "Lesson command"
category: "lesson"
chapter: "courses/aiagent/lesson03-core/module22-discord"
duration: "~60 min"
prerequisites: ["start-21-1", "setup-discord"]
level: "intermediate"
tags: ["discord", "bot", "channels", "plugin"]
nonInteractiveMode: incompatible
---
# Lesson 22-1: Introduccion a la integracion con Discord

## Lo que hara en esta sesion

Aprenda a combinar un **Bot de Discord** con el **plugin oficial discord de Claude Code Channels** para que Claude Code pueda leer y escribir canales y DMs de Discord de forma segura.

## Requisitos previos

- Tener una cuenta de Discord y un servidor donde pueda invitar un bot
- Poder iniciar Claude Code en modo interactivo
- Ejecutar `/setup-discord` primero para confirmar la instalacion del plugin oficial y el arranque con `--channels`

## Objetivos

1. Explicar como crear un bot en Discord Developer Portal y activar MESSAGE CONTENT INTENT
2. Confirmar el flujo oficial desde `/plugin install discord@claude-plugins-official` hasta `claude --channels plugin:discord@claude-plugins-official`
3. Manejar tokens y control de acceso de forma segura con `/discord:configure`, variables de entorno locales y allowlist
4. Entender que puede y no puede hacer el bot, y elegir entre canales privados por cliente y bot como hub

## Pagina relacionada

- Pagina del material: [Module 22](https://ai-agent.camp/es/course/module-22?slideId=module-overview)

## Siguientes pasos

A continuacion, ejecute `/start-23-1` para continuar con la operacion de cuentas oficiales de LINE.
