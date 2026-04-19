---
description: "Guiar el procedimiento para configurar claves de API y tokens de forma segura (para principiantes)"
---

# Guía de configuración de claves de API

Cuando el usuario solicite "Quiero configurar una clave de API" o "Quiero ingresar una clave de Gemini," guíelo usando **solo este procedimiento**. No permita que pegue secretos en el chat.

## Regla de máxima prioridad

- **No permita que los usuarios peguen claves de API o tokens en el chat.** Si lo hacen, simplemente diga "Ese enfoque es riesgoso. Por favor, péguelo en `.env.local`, no en el chat."

## Procedimiento (seguir este orden)

1. **Preparar**  
   Ejecute lo siguiente en la raíz del proyecto para agregar la entrada de clave en `.env.local`:
   ```bash
   uv run python tools/credential_manager.py prepare-dotenv KEY_NAME
   ```
   (Ejemplos de `KEY_NAME`: `GEMINI_API_KEY`, `GITHUB_TOKEN`. Para múltiples claves, listarlas: `KEY_NAME1 KEY_NAME2`.)

2. **Pegar**  
   Indique al usuario: "Abra [`.env.local`](.env.local) y pegue el valor **solo a la derecha de** `KEY_NAME=`, luego guarde. Una vez guardado, escriba 'guardado' para continuar."  
   No permita que peguen el valor ni el archivo completo en el chat.

3. **Migrar**  
   Una vez que el usuario diga "guardado," ejecute:
   ```bash
   uv run python tools/credential_manager.py import-dotenv --delete KEY_NAME
   ```
   Esto mueve el valor al Credential Store del sistema operativo y elimina la línea de `.env.local`.

4. **Verificar**  
   ```bash
   uv run python tools/credential_manager.py status
   ```
   Confirme que la clave objetivo aparece como `stored`.

5. **Ejecutar scripts que usan secretos**  
   Siga las instrucciones de cada lección o proyecto. Para inyectar del Credential Store a variables de entorno, use `inject_to_environ` (consulte comandos de lección como `setup-fal.md`).

## Notas

- `NEXT_PUBLIC_*` y configuraciones públicas de Firebase pueden permanecer en `.env.local`. Solo elimine las líneas de claves importadas.
- Para configuración solo por terminal, `uv run python tools/credential_manager.py store KEY_NAME` también funciona (la entrada se oculta de la pantalla).

## Referencias

- Curso: Módulo 0, diapositiva "Gestionar claves de API de forma segura" (slideId=api-key-management)
  - Ejemplo de ruta URL: `/es/course/module-0?slideId=api-key-management` (reemplace `es` con `ja` / `en`)
  - Abrir en el navegador localmente (macOS, servidor de desarrollo en puerto 3000):
    ```bash
    open "http://localhost:3000/es/course/module-0?slideId=api-key-management"
    ```
  - Abrir module-0 sin `slideId` redirige al hub de configuración. Siempre incluya `slideId` para ir directamente a la diapositiva.
