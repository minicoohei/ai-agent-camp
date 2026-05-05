---
description: "Lesson command"
duration: "~10 min"
prerequisites: ["Tener cuenta de Notion (plan gratuito OK)", "Navegador disponible", "Node.js 18+"]
level: "beginner"
tags: ["setup", "notion", "ncli", "mcp", "oauth"]
---

# Configuración de Notion CLI (ncli) + Hosted MCP (solo OAuth)

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-notion` para mostrar el progreso
2. Detectar automáticamente la configuración existente:
   - `which ncli` para verificar si ncli está instalado
   - Para Claude Code: verificar si el servidor `notion` está definido en `~/.claude/mcp_settings.json`
   - Para Cursor: verificar si el servidor `notion` está definido en `~/.cursor/mcp.json`
   - Si ncli está instalado y MCP está configurado, puede ejecutar solo el Step 6 (prueba de conexión) y marcarlo como completado

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Conectar ncli (Notion CLI) y el Hosted MCP oficial de Notion mediante **OAuth**, para operar Notion desde el terminal y desde herramientas compatibles con MCP |
| Duración | ~10 minutos |
| Requisitos previos | Cuenta de Notion (plan gratuito OK), Node.js 18+, navegador |
| Nivel de operación | No se necesitan comandos CLI (todo lo ejecuta automáticamente la IA + una sola aprobación OAuth en el navegador) |
| Método de autenticación | **Solo OAuth**. No se utilizan claves API (Internal Integration Token). |

**Flujo de la sesión:**
1. Instalar ncli (@sakasegawa/ncli) (la IA lo ejecuta automáticamente)
2. Ejecutar `ncli login` y aprobar el OAuth de Notion en el navegador
3. Verificar con `ncli whoami` / `ncli search`
4. Añadir el Notion Hosted MCP (OAuth) al archivo de configuración MCP (la IA lo escribe automáticamente)
5. Reiniciar Claude Code / Cursor y aprobar el diálogo OAuth en el primer uso
6. Prueba de conexión MCP

> **¿Por qué solo OAuth?** Con el flujo antiguo de Internal Integration Token había que crear una integración en Notion y compartir cada página individualmente con "Add connections". Con OAuth, un único inicio de sesión en el navegador concede acceso a todo el workspace, por lo que **no es necesario** compartir página por página.

> **Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación antes de la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está preparado/a?",
    "options": [
      {"id": "ready", "label": "¡Preparado/a! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "which_tool", "label": "Quiero confirmar si uso Claude Code o Cursor"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(check_prereq -> Indicar: "Está listo/a si tiene una cuenta de Notion (plan gratuito OK), puede iniciar sesión por navegador y tiene Node.js 18 o superior instalado.")
(which_tool -> Explicar: "La ubicación del archivo de configuración MCP difiere entre Claude Code y Cursor. El Step 4 le guiará con los pasos para cada uno.")
(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Instalar ncli (Notion CLI)

**Lo que hace la IA:**
1. Verificar la versión de Node.js: `node --version` (se requiere 18 o superior)
2. Verificar si ncli ya está instalado: `which ncli`
3. Si no está instalado, ejecutar el siguiente comando:

```bash
npm install -g @sakasegawa/ncli
```

4. Después de la instalación, verificar con `ncli --version`

**Configuración de AskQuestion:**
```json
{
  "title": "Step 1: Instalar ncli",
  "questions": [{
    "id": "ncli_status",
    "prompt": "Se ejecutó la instalación de ncli. Verifique el resultado.",
    "options": [
      {"id": "installed", "label": "Se instaló correctamente"},
      {"id": "npm_error", "label": "Hubo un error con npm install"},
      {"id": "no_node", "label": "Node.js no está instalado"},
      {"id": "command_not_found", "label": "No se encuentra el comando ncli"}
    ]
  }]
}
```

(installed -> Ir al Step 2)
(npm_error -> Ejecutar `npm cache clean --force` y reintentar. Si hay error de permisos, indicar `sudo npm install -g @sakasegawa/ncli`)
(no_node -> Indicar: "Instale la versión LTS (18 o superior) desde https://nodejs.org/")
(command_not_found -> Verificar la instalación con `npm list -g @sakasegawa/ncli`. Si es un problema de PATH, verificar con `npm bin -g` e indicar cómo agregar al PATH)

---

## Step 2: Iniciar sesión en Notion mediante OAuth con ncli

**Lo que hace la IA:**
1. Ejecutar en el terminal:

```bash
ncli login
```

2. ncli abre automáticamente la pantalla OAuth de Notion en el navegador
3. El usuario sigue el flujo en pantalla:
   - Iniciar sesión en Notion (si no lo está)
   - Seleccionar el workspace al que conceder acceso
   - Hacer clic en "Allow access"
4. Si tiene éxito, el terminal muestra "Logged in as ..."

**Mensaje para mostrar al usuario:**

```text
Se abrió la pantalla OAuth de Notion en el navegador.

1. Si no ha iniciado sesión en Notion, inicie sesión
2. Seleccione el workspace al que desea conceder acceso
3. Haga clic en "Allow access" para aprobar

Tras la aprobación, la pestaña del navegador se cierra automáticamente y el terminal mostrará un mensaje de inicio de sesión exitoso.

No es necesario introducir ninguna clave API (secret_xxx). Todo se completa con el flujo OAuth en el navegador.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Inicio de sesión OAuth en Notion",
  "questions": [{
    "id": "login_status",
    "prompt": "¿Se completó el flujo OAuth de ncli login?",
    "options": [
      {"id": "logged_in", "label": "¡Inicié sesión correctamente!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "login_denied", "label": "No puedo iniciar sesión / la aprobación falló"},
      {"id": "wrong_workspace", "label": "Aprobé el workspace equivocado"}
    ]
  }]
}
```

(logged_in -> Ir al Step 3)
(browser_not_open -> Indicar: "Busque la URL de OAuth impresa en el terminal. Cópiela y péguela manualmente en el navegador.")
(login_denied -> Indicar: "Si no tiene cuenta de Notion, puede crear una gratis en https://www.notion.so/signup. Si la aprobación falla, ejecute `ncli login` de nuevo.")
(wrong_workspace -> Indicar: "Ejecute primero `ncli logout`, luego `ncli login` y seleccione el workspace correcto.")

---

## Step 3: Verificar ncli (whoami / search)

**Lo que hace la IA:**
1. Verificar el estado de sesión actual:

```bash
ncli whoami
```

2. Prueba de humo de búsqueda en el workspace (basta con que devuelva uno o dos resultados):

```bash
ncli search ""
```

O especificar una palabra clave:

```bash
ncli search "test"
```

3. Si aparecen resultados, OAuth ha concedido correctamente acceso a todo el workspace

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Verificación de ncli",
  "questions": [{
    "id": "smoke_test",
    "prompt": "¿Los comandos whoami / search devolvieron resultados esperados?",
    "options": [
      {"id": "ok", "label": "Aparece mi usuario y la búsqueda devuelve resultados"},
      {"id": "whoami_fail", "label": "whoami dice que no he iniciado sesión"},
      {"id": "search_empty", "label": "La búsqueda devolvió 0 resultados"},
      {"id": "other_error", "label": "Apareció otro error"}
    ]
  }]
}
```

(ok -> Ir al Step 4)
(whoami_fail -> Indicar: "Ejecute `ncli login` de nuevo. Si alterna entre varias cuentas de Notion, ejecute `ncli logout` primero por seguridad.")
(search_empty -> Indicar: "Cero resultados solo significa que no hay páginas en el workspace. Cree una página de prueba en Notion y vuelva a probar `ncli search`.")
(other_error -> Inspeccionar el mensaje de error y orientar sobre la causa)

---

## Step 4: Añadir Notion Hosted MCP (OAuth) al archivo de configuración MCP

El Hosted MCP oficial de Notion está alojado en `https://mcp.notion.com/mcp` y utiliza Streamable HTTP + OAuth. **No** se incluyen tokens ni variables de entorno en la configuración.

**Lo que la IA ejecuta automáticamente:**

1. Determinar la herramienta utilizada (Claude Code o Cursor)
2. Añadir una entrada `notion` al archivo de configuración MCP (preservar el `mcpServers` existente)

**Archivo de configuración MCP que la IA escribe:**

**Para Claude Code:** `~/.claude/mcp_settings.json`
**Para Cursor:** `~/.cursor/mcp.json` (directorio principal; NO escribir en `.cursor/mcp.json` dentro del repositorio)

Contenido de la configuración (si `mcpServers` ya existe, agregar la entrada `notion`):
```json
{
  "mcpServers": {
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

**Importante:**
- **No** incluir `command` / `args` / `env` (es un Hosted MCP; no se ejecuta localmente)
- **No** establecer `NOTION_TOKEN` ni ningún otro secreto (OAuth gestiona la autenticación)
- `type` debe ser `http` (Streamable HTTP)

**Configuración de AskQuestion:**
```json
{
  "title": "Step 4: Crear el archivo de configuración MCP",
  "questions": [{
    "id": "config_status",
    "prompt": "¿Añadió la entrada Notion al archivo de configuración MCP?",
    "options": [
      {"id": "done", "label": "¡Lo añadí!"},
      {"id": "editor_help", "label": "No sé dónde está el archivo"},
      {"id": "existing_config", "label": "Ya tengo otros servidores MCP configurados y quiero saber cómo agregar este"},
      {"id": "security_question", "label": "Tengo una pregunta sobre la seguridad de OAuth"}
    ]
  }]
}
```

(done -> La IA lee el archivo y verifica que la entrada `notion` tenga `type: "http"` y `url: "https://mcp.notion.com/mcp"`, sin que se cuele ningún `NOTION_TOKEN` ni `command`. Si está bien, ir al Step 5)
(editor_help -> Indicar: "En macOS, ejecute `open ~/.claude/mcp_settings.json` o `open ~/.cursor/mcp.json`. Si el archivo no existe, créelo.")
(existing_config -> Leer el contenido del archivo existente y agregar la entrada `notion` al objeto `mcpServers`, preservando las demás configuraciones)
(security_question -> Explicar: "El Hosted MCP lo opera la propia Notion y la autenticación se realiza mediante OAuth en el navegador. Los tokens nunca se almacenan en el archivo de configuración: se guardan en el almacén seguro de la herramienta (Claude Code / Cursor).")

---

## Step 5: Reiniciar la herramienta y aprobar el diálogo OAuth

**Mensaje que muestra la IA:**

```text
Es necesario reiniciar la herramienta para aplicar la configuración MCP.

Para Claude Code:
  -> Salga con exit, luego inicie claude nuevamente

Para Cursor:
  -> Presione Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) para abrir
    la Paleta de comandos y ejecute "Reload Window"

Tras el reinicio, la primera vez que se invoque una herramienta MCP de Notion,
el navegador abrirá el diálogo de aprobación OAuth de Notion.
Haga clic en "Allow access" para aprobar.
(Una vez aprobado, la sesión se mantiene automáticamente.)
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 5: Reinicio y aprobación OAuth",
  "questions": [{
    "id": "restart_status",
    "prompt": "¿Reinició la herramienta?",
    "options": [
      {"id": "restarted", "label": "¡Reinicié! A la prueba"},
      {"id": "how_restart", "label": "No sé cómo reiniciar"},
      {"id": "no_oauth_dialog", "label": "El diálogo OAuth no aparece"}
    ]
  }]
}
```

(restarted -> Ir al Step 6)
(how_restart -> Reexplicar los pasos de reinicio por herramienta)
(no_oauth_dialog -> Indicar: "El diálogo se abre la **primera vez** que se invoca una herramienta MCP. Ejecute la prueba del Step 6 y debería aparecer automáticamente. Si sigue sin aparecer, revise los logs de la herramienta (Claude Code: `claude --debug`; Cursor: la sección MCP del panel Output).")

---

## Step 6: Prueba de conexión MCP

**Lo que hace la IA:**

1. Verificar que las herramientas MCP de Notion (por ejemplo `notion-search`, `notion-fetch`) están disponibles
2. Emitir una solicitud sencilla para obtener información del workspace
3. En la primera ejecución, el navegador abre el diálogo OAuth: pedir al usuario que lo apruebe
4. Mostrar "Se obtuvieron N páginas de Notion. La conexión MCP funciona."

**En caso de éxito:**
```text
¡La configuración del Notion Hosted MCP se completó!

Resultado de la prueba: Se conectó exitosamente a Notion a través del servidor MCP.
Ahora puede operar páginas y bases de datos de Notion directamente desde Claude Code/Cursor.
```

**En caso de fallo - AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de conexión MCP. Verifiquemos la causa.",
    "options": [
      {"id": "retry", "label": "Ejecutar la prueba de nuevo"},
      {"id": "check_config", "label": "Verificar el archivo de configuración MCP"},
      {"id": "reauth", "label": "Volver a aprobar OAuth"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba. Si aparece el diálogo OAuth, pedir al usuario que lo apruebe)
(check_config -> Verificar la configuración: `type: "http"` y `url: "https://mcp.notion.com/mcp"`, y que el JSON sea válido)
(reauth -> Indicar al usuario que borre el estado de autenticación de Notion en el almacén de la herramienta y reinicie. Claude Code: por ejemplo `claude mcp logout notion`)
(show_error -> Mostrar el mensaje de error e indicar la causa y la solución)
(skip_test -> Indicar: "Se omitió la prueba. Puede verificarla más tarde con /check-setup.")

---

## Problemas comunes y soluciones

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el tipo de problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda a su situación",
    "options": [
      {"id": "trouble_oauth_fail", "label": "La aprobación OAuth falla"},
      {"id": "trouble_mcp_no_response", "label": "No hay respuesta del servidor MCP"},
      {"id": "trouble_no_pages", "label": "No se obtienen páginas (workspace incorrecto)"},
      {"id": "trouble_ncli_login", "label": "ncli login no funciona"},
      {"id": "trouble_cost", "label": "Me preocupan los costos"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: La aprobación OAuth falla
**Causa**: El navegador bloquea ventanas emergentes, o el usuario canceló la aprobación en Notion
**Lo que hace la IA**:
1. Pedir al usuario que permita ventanas emergentes / redirecciones en el navegador
2. Volver a ejecutar `ncli login` o invocar de nuevo la herramienta MCP para reintentar OAuth
3. Si sigue fallando, cerrar sesión de Notion en el navegador y volver a intentarlo

### Problema 2: No hay respuesta del servidor MCP
**Causa**: Archivo MCP mal configurado, herramienta no reiniciada, o `https://mcp.notion.com` bloqueado en la red
**Lo que hace la IA**:
1. Verificar la configuración MCP (`type: "http"`, `url: "https://mcp.notion.com/mcp"`)
2. Validar la sintaxis JSON (Claude Code: `python -m json.tool ~/.claude/mcp_settings.json` / Cursor: `python -m json.tool ~/.cursor/mcp.json`)
3. Reiniciar completamente la herramienta (Claude Code / Cursor)
4. Comprobar la conectividad con `curl -I https://mcp.notion.com/mcp`

### Problema 3: No se obtienen páginas
**Causa**: Se seleccionó el workspace equivocado durante la aprobación OAuth
**Lo que hace la IA**:
1. Ejecutar `ncli logout` -> `ncli login` y elegir el workspace correcto
2. En el lado MCP, cerrar sesión de Notion en el almacén de autenticación de la herramienta y volver a autenticar

### Problema 4: ncli login no funciona
**Causa**: Node.js demasiado antiguo, ncli desactualizado, o el puerto del listener OAuth está en uso
**Lo que hace la IA**:
1. Verificar Node.js >= 18 con `node --version`
2. Actualizar con `npm install -g @sakasegawa/ncli@latest`
3. Si hay conflicto de puertos, detener otros servidores locales (especialmente servidores de desarrollo) y reintentar

### Problema 5: Preocupación por los costos
**Indicación de la IA**: "Notion está disponible en plan gratuito. No hay costos adicionales por el uso de la API mediante OAuth. El Hosted MCP oficial de Notion (`mcp.notion.com`) también es gratuito. ncli (@sakasegawa/ncli) es de código abierto y gratuito."

### Problema 6: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar la solución

---

## Punto de control
- [ ] ncli (@sakasegawa/ncli) está instalado
- [ ] El OAuth en navegador con `ncli login` está completo
- [ ] `ncli whoami` muestra el usuario con sesión iniciada
- [ ] `ncli search` devuelve páginas del workspace
- [ ] El archivo de configuración MCP tiene una entrada `notion` (`type: http`, `url: https://mcp.notion.com/mcp`)
- [ ] Reinició Claude Code / Cursor
- [ ] La prueba de conexión MCP fue exitosa (tras la aprobación OAuth, puede acceder a las páginas de Notion)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de Notion MCP se completó! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "try_notion_mcp", "label": "Probar operaciones de Notion MCP (/start-12-1)"},
      {"id": "try_notion_db", "label": "Operar bases de datos de Notion (/start-12-2)"},
      {"id": "setup_other", "label": "Configurar también otras API (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- try_notion_mcp -> Dirigir a /start-12-1
- try_notion_db -> Dirigir a /start-12-2
- setup_other -> Dirigir a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-notion` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, pruebe las operaciones de Notion MCP con `/start-12-1`"
