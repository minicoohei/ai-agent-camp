---
description: Slash /module-18-google-auth — Módulo 18 Lección 4-1 — Asistir con la autenticación de Google (gog auth) y verificación de Gmail/Calendar
---

## Comience aquí (lo más rápido)

Ejecute **`/module-18-google-auth`** en el chat para cargar todas las instrucciones de esta lección en el contexto de una sola vez. **Es más rápido y confiable que escribir prompts largos manualmente.**

# Módulo 18 — Prueba de autenticación de Google (Lección 4-1 Auth)

El usuario está trabajando con el material del curso "Módulo 18 - Prueba de autenticación." **Mediante este comando,** **el usuario no necesita escribir nada directamente en la terminal.** El agente debe ejecutar `gog` (gogcli) y reportar los resultados.

## Pasos

1. Si no está autenticado, primero completar **`/module-18-gcp-quick`** (registro de OAuth incluido y `gog auth add`).
2. Ejecutar `gog gmail search --query "is:inbox" --max 5` para verificar la obtención de la bandeja de entrada.
3. Ejecutar `gog calendar events --days 7` para verificar la obtención de eventos.
4. En caso de fallo, comparar con la configuración OAuth de `slideId=lesson-18-1-gcp-appendix` (GCP autogestionado) del material del curso.

## Referencias

- Curso: `slideId=lesson-18-1-auth` (ej.: `/es/course/module-18?slideId=lesson-18-1-auth`)
