---
description: Slash /module-18-gcp-quick — Módulo 18 Lección 4-1 — Autenticar gog con OAuth incluido (sin necesidad de escribir en la terminal)
nonInteractiveMode: incompatible
---
## Comience aquí (lo más rápido)

**El estudiante solo necesita ejecutar `/module-18-gcp-quick` en el chat.** Los comandos bash a continuación son para el agente (o para quienes deseen solucionar problemas manualmente).

Ejecute **`/module-18-gcp-quick`** en el chat para cargar todas las instrucciones de esta lección en el contexto de una sola vez.

# Módulo 18 — Autenticación rápida de Google (Lección 4-1 GCP Principal)

El usuario está trabajando con el material del curso "Módulo 18 - Autenticación rápida de Google (`slideId=lesson-18-1-gcp`)." **El usuario no necesita escribir comandos directamente en la terminal.** El agente debe ejecutar `gog` (gogcli) y reportar los resultados.

## Requisitos previos

- El directorio de trabajo debe ser la **raíz del repositorio ai-agent-camp** (ya clonado).
- Ruta del JSON del cliente OAuth (según el material del curso): `credentials/google-workspace-desktop-oauth.json`

## Pasos

### Para el agente: Verificar disponibilidad de gog y estado de autenticación

Ejecute los siguientes comandos **en este orden** y resuma los resultados para el usuario (no pida al estudiante que escriba en la terminal).

```bash
# Verificar si gog está en el PATH (si no se encuentra, se necesita instalación)
command -v gog || echo "gog: not found in PATH"

gog --version

gog auth --help

gog auth list
```

- Si `gog` no se encuentra → Guiar al usuario para instalar gogcli (gog) vía **Módulo 15-1** o similar, luego continuar.
- Si `gog auth list` ya muestra una cuenta, evitar adiciones duplicadas y solo ejecutar `gog auth add` cuando sea necesario.

### Configuración de OAuth

1. Verificar que `credentials/google-workspace-desktop-oauth.json` existe. Si no, guiar al usuario al Apéndice del material del curso (`slideId=lesson-18-1-gcp-appendix`) u obtener el JSON de los administradores del curso.
2. Ejecutar `gog auth credentials set credentials/google-workspace-desktop-oauth.json` **desde la raíz del repositorio** para registrar el cliente compartido.
3. Preguntar al usuario el **correo electrónico de la cuenta de Google que desea usar para iniciar sesión**, luego ejecutar `gog auth add <correo>`. Cuando se abra el navegador, guiarlo a través de las **4 capturas de pantalla de OAuth** en la diapositiva del curso `lesson-18-1-gcp` (Autenticación rápida de Google) (el orden puede variar):
   - **Aplicación no verificada**: Hacer clic en "Avanzado" → hacer clic en el enlace **Continuar a Cursor Bootcamp** en la parte inferior (la visualización del desarrollador mostrando `user@example.com` etc. es esperada).
   - **Consentimiento básico**: Confirmar perfil y correo, luego proceder con "Siguiente" o similar.
   - **Alcances**: Seleccionar todos si es necesario y otorgar/continuar.
   - **Interfaz de cuenta Gog** (si se muestra): Verificar conexión y permisos mediante las insignias DEFAULT y por servicio.
4. Ejecutar `gog auth list` para confirmar que la cuenta ha sido registrada (opcionalmente también usar la interfaz de gestión local de Gog).
5. Al tener éxito, proceder a **`/module-18-google-auth`** (prueba de autenticación) para verificar la conectividad de Gmail/Calendar.

## Referencias

- Curso: `slideId=lesson-18-1-gcp` (principal), `slideId=lesson-18-1-gcp-appendix` (GCP autogestionado)
- Ejemplo: `/es/course/module-18?slideId=lesson-18-1-gcp`
