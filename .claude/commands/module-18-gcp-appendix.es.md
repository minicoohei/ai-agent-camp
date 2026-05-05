---
description: Slash /module-18-gcp-appendix — Módulo 18 — GCP autogestionado (lista de verificación del procedimiento de consola)
nonInteractiveMode: incompatible
---
## Comience aquí (lo más rápido)

Ejecute **`/module-18-gcp-appendix`** en el chat para cargar el contexto de soporte del procedimiento de la consola de GCP.

# Módulo 18 — GCP autogestionado (Apéndice)

El usuario está trabajando con el material del curso "Módulo 18 - Para quienes desean gestionar GCP por su cuenta (`slideId=lesson-18-1-gcp-appendix`)." Las operaciones de Google Cloud Console se realizan **manualmente en el navegador del usuario**; el agente debe proporcionar **listas de verificación para cada paso, consejos de solución de problemas y explicaciones breves de terminología.**

## Pasos (correspondientes a los 4 pasos del curso)

1. **Proyecto y APIs**: Verificar que se ha creado un proyecto y se han habilitado las APIs de Gmail / Calendar / Drive / Sheets / Google Docs.
2. **Facturación**: Verificar que se ha vinculado una cuenta de facturación al proyecto.
3. **Cliente OAuth**: Verificar que se ha completado "Crear credenciales" → ID de cliente OAuth → **Externo** → **Aplicación de escritorio** → y se ha descargado el JSON.
4. **Pantalla de consentimiento OAuth**: Verificar que se han ingresado los campos obligatorios en Branding y se ha agregado la propia cuenta de Google del usuario como **Usuario de prueba**.

## Solución de problemas

- Si el asistente requiere completar la pantalla de consentimiento primero, guiar al usuario para completar el Paso 4 (Branding) antes de volver al Paso 3.
- El JSON descargado **no debe ser committeado a Git**. Hacer referencia a él mediante `.env` o Credential Manager.

## Referencias

- Curso: `/es/course/module-18?slideId=lesson-18-1-gcp-appendix` (ajustar el idioma según sea necesario)
