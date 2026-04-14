---
description: "Configuración de Notion CLI (ncli) + MCP (Guía completa)"
duration: "~15 min"
prerequisites: ["Tener cuenta de Notion (plan gratuito OK)", "Navegador disponible", "Node.js 18+"]
level: "beginner"
tags: ["setup", "notion", "ncli", "mcp", "api"]
---

# Configuración de Notion CLI (ncli) + MCP

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-notion` para mostrar el progreso
2. Detectar automáticamente la configuración existente:
   - `which ncli` para verificar si ncli está instalado
   - Para Claude Code: verificar si el servidor `notion` está definido en `~/.claude/mcp_settings.json`
   - Para Cursor: verificar si el servidor `notion` está definido en `.cursor/mcp.json`
   - Si ncli está instalado y MCP está configurado, puede ejecutar solo el Step 6 (prueba de conexión) y marcarlo como completado

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar ncli (Notion CLI), crear una integración de Notion y habilitar Claude Code/Cursor para operar páginas y bases de datos de Notion a través del terminal + servidor MCP |
| Duración | ~15 minutos |
| Requisitos previos | Tener cuenta de Notion (plan gratuito OK), Node.js 18+, navegador disponible |
| Nivel de operación | No se necesitan comandos CLI (todo lo ejecuta automáticamente la IA + solo operaciones de GUI) |

**Flujo de la sesión:**
1. Instalar ncli (@sakasegawa/ncli) (la IA lo ejecuta automáticamente)
2. Abrir la página de integraciones de Notion en el navegador (la IA abre el navegador automáticamente)
3. Crear una integración y obtener la clave de API (solo hacer clic en botones en pantalla)
4. Crear el archivo de configuración MCP (la IA lo crea automáticamente)
5. Compartir la integración con las páginas de Notion
6. Prueba de conexión de ncli + MCP

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
      {"id": "chrome", "label": "Automatizar operaciones del navegador con /chrome"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "which_tool", "label": "Quiero confirmar si uso Claude Code o Cursor"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(chrome -> Después de abrir el navegador en el Step 2, seguir la sección "Automatización con integración Chrome" para la ejecución automática)
(check_prereq -> Indicar: "Está listo/a si tiene una cuenta de Notion (plan gratuito OK), Node.js 18+ y puede iniciar sesión a través de su navegador.")
(which_tool -> Explicar: "La ubicación del archivo de configuración difiere entre Claude Code y Cursor. El Step 4 le guiará con los pasos para cada uno.")
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

## Step 2: Abrir la página de integraciones de Notion en el navegador

**Lo que hace la IA:**
1. Detectar automáticamente el SO (Mac / Windows / Linux)
2. Ejecutar el siguiente comando para abrir el navegador automáticamente:

```bash
# Mac:
open https://www.notion.so/my-integrations
# Windows:
start https://www.notion.so/my-integrations
# Linux:
xdg-open https://www.notion.so/my-integrations
```

**Después de que se abra el navegador, mostrar la siguiente AskQuestion:**

```json
{
  "title": "Step 2: Crear una integración",
  "questions": [{
    "id": "browser_status",
    "prompt": "¿Se abrió el navegador? Siga estos pasos para crear una integración:\n\n1. Inicie sesión en Notion\n2. Haga clic en el botón 'New integration' (Nueva integración)\n3. Establezca el nombre como 'AIAgent Bootcamp'\n4. Seleccione 'Internal' como tipo\n5. En Capabilities, marque 'Read content', 'Update content' e 'Insert content'\n6. Haga clic en 'Submit' (Enviar)\n\n¿Creó la integración?",
    "options": [
      {"id": "created", "label": "¡Creé la integración!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "no_button", "label": "No encuentro el botón 'New integration'"},
      {"id": "login_issue", "label": "No puedo iniciar sesión en Notion"}
    ]
  }]
}
```

(created -> Ir al Step 3)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://www.notion.so/my-integrations")
(no_button -> Indicar: "Espere a que la página se cargue completamente. Cuando visite https://www.notion.so/my-integrations con sesión iniciada en Notion, verá el botón 'New integration' cerca de la esquina superior derecha.")
(login_issue -> Indicar: "Si no tiene cuenta de Notion, puede crear una gratis en https://www.notion.so/signup. Si ya tiene una cuenta, inicie sesión con su dirección de correo electrónico o cuenta de Google.")

---

## Automatización con integración Chrome (modo `/chrome`)

**Requisito previo:** La extensión "Claude in Chrome" (v1.0.36+) debe estar instalada en Chrome, y debe haber iniciado con `claude --chrome` o ejecutado `/chrome` en la sesión.

**Lo que la IA ejecuta automáticamente con la integración Chrome:**
1. Abrir https://www.notion.so/my-integrations en el navegador
2. Usar la integración Chrome para realizar las siguientes operaciones en orden:
   - Hacer clic en el botón "New integration"
   - Ingresar "AIAgent Bootcamp" en el campo Name
   - Seleccionar el espacio de trabajo predeterminado en Associated workspace
   - Seleccionar "Internal" como Type
   - Marcar Read content, Update content e Insert content en Capabilities
   - Hacer clic en "Submit"
3. Una vez que aparezca el Internal Integration Secret, indicar al usuario "Haga clic en el botón Copy junto al secreto para copiarlo"
4. Ir al Step 4

**Nota:** No leer el valor del secreto desde la pantalla del navegador. El usuario lo copia manualmente.

Si la integración Chrome no está disponible, siga las instrucciones anteriores manualmente.

---

## Step 3: Copiar la clave de API

**Mensaje para mostrar al usuario:**

```text
Después de crear la integración, siga estos pasos para copiar la clave de API:

1. Se mostrará la página de configuración de la integración creada
2. Se muestra un token en la sección "Internal Integration Secret"
   (una cadena que comienza con secret_xxx)
3. Haga clic en el botón "Copy" para copiar el token

⚠️ No pegue el token copiado en este chat.
   En el siguiente paso, la IA lo escribirá de forma segura en el archivo de configuración.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Copiar la clave de API",
  "questions": [{
    "id": "copy_status",
    "prompt": "¿Copió el Internal Integration Secret (la cadena que comienza con secret_xxx)?",
    "options": [
      {"id": "copied", "label": "¡Copié la clave de API!"},
      {"id": "no_secret", "label": "No encuentro el token"},
      {"id": "help_capabilities", "label": "No entiendo la configuración de Capabilities"}
    ]
  }]
}
```

(copied -> Ir al Step 4)
(no_secret -> Indicar: "Haga clic en el nombre de la integración que creó desde la lista de integraciones (https://www.notion.so/my-integrations) para ir a la página de configuración. Encontrará un token que comienza con secret_ en la sección 'Internal Integration Secret'.")
(help_capabilities -> Indicar: "En la página de configuración de la integración, vaya a la pestaña 'Capabilities' y marque 'Read content', 'Update content' e 'Insert content'. Esto habilita la lectura y escritura de páginas a través de la API.")

---

## Step 4: Crear el archivo de configuración MCP

**Lo que la IA ejecuta automáticamente:**

1. Determinar la herramienta utilizada (Claude Code o Cursor)
2. Crear el archivo de configuración MCP correspondiente con un marcador de posición
3. Hacer que el usuario reemplace el marcador de posición con la clave de API

**Archivo de configuración MCP que la IA crea:**

**Para Claude Code:** `~/.claude/mcp_settings.json`
**Para Cursor:** `~/.cursor/mcp.json` (directorio principal; NO escribir en `.cursor/mcp.json` dentro del repositorio)

Contenido de la configuración (si `mcpServers` ya existe, agregar la entrada `notion`):
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "YOUR_NOTION_TOKEN_HERE"
      }
    }
  }
}
```

3. Después de que la IA cree el archivo, mostrar este mensaje al usuario:

```text
Se creó el archivo de configuración MCP. Por favor configure la clave de API:

┌─────────────────────────────────────────────────────────────┐
│ Abra el siguiente archivo en un editor de texto:            │
│                                                             │
│ Claude Code: ~/.claude/mcp_settings.json                    │
│ Cursor:      ~/.cursor/mcp.json                             │
│                                                             │
│ Reemplace YOUR_NOTION_TOKEN_HERE en el archivo con          │
│ la clave de API que copió (secret_xxx...).                   │
│ Después de guardar, regrese a este chat.                    │
└─────────────────────────────────────────────────────────────┘

⚠️ No pegue la clave de API en este chat.
   Al editar el archivo directamente en un editor, no queda en los registros del chat.
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 4: Crear el archivo de configuración MCP",
  "questions": [{
    "id": "config_status",
    "prompt": "¿Reemplazó la clave de API en el archivo de configuración MCP?",
    "options": [
      {"id": "done", "label": "¡Configuré la clave de API!"},
      {"id": "editor_help", "label": "No sé cómo abrir el archivo"},
      {"id": "existing_config", "label": "Ya tengo un archivo de configuración y quiero saber cómo agregar"},
      {"id": "security_question", "label": "Tengo una pregunta sobre seguridad"}
    ]
  }]
}
```

(done -> La IA lee el archivo de configuración y verifica que `YOUR_NOTION_TOKEN_HERE` ya no esté presente (sin mostrar el valor de la clave). Si está bien, ir al Step 5)
(editor_help -> Indicar: "Ejecute lo siguiente en su terminal para abrirlo en un editor: Mac: `open ~/.claude/mcp_settings.json` / Cursor: `code ~/.cursor/mcp.json`. O muestre los archivos ocultos en Finder/Explorador y abra el archivo.")
(existing_config -> Leer el contenido del archivo existente y guiar para agregar la entrada `notion` a `mcpServers`. Preservar las configuraciones existentes de otros servidores MCP)
(security_question -> Explicar: "El archivo de configuración MCP está en su directorio principal y no se incluye en el repositorio Git. La clave de API se almacena solo en este archivo y se pasa como variable de entorno cuando se inicia el servidor MCP.")

---

## Step 5: Compartir la integración con las páginas

**Importante: Si omite este paso, el MCP no podrá acceder a sus páginas de Notion.**

**Mensaje para mostrar al usuario:**

```text
La API de Notion requiere que especifique explícitamente a qué páginas puede acceder la integración.
Siga estos pasos para compartir la integración con las páginas que desea acceder:

┌─────────────────────────────────────────────────────────────┐
│ 1. Abra la página de Notion a la que desea acceder          │
│ 2. Haga clic en "..." (menú de tres puntos) en la esquina   │
│    superior derecha                                         │
│ 3. Seleccione "Add connections" (Agregar conexiones)         │
│ 4. Escriba "AIAgent Bootcamp" en el campo de búsqueda       │
│ 5. Haga clic en el nombre de la integración que aparece      │
│ 6. Haga clic en "Confirm" en el diálogo de confirmación     │
│                                                             │
│ * Compartir una página padre se aplica automáticamente       │
│   a las páginas hijas                                       │
│ * Para acceder a múltiples páginas, repita esto para cada    │
│   página o configúrelo en una página padre común             │
└─────────────────────────────────────────────────────────────┘
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 5: Compartir la integración con las páginas",
  "questions": [{
    "id": "share_status",
    "prompt": "¿Compartió la integración con su página de Notion?",
    "options": [
      {"id": "shared", "label": "¡Configuré la compartición!"},
      {"id": "no_connection", "label": "No encuentro 'Add connections'"},
      {"id": "no_integration", "label": "No aparece el nombre de la integración"},
      {"id": "skip_share", "label": "Lo configuraré más tarde (omitir)"}
    ]
  }]
}
```

(shared -> Ir al Step 6)
(no_connection -> Indicar: "Abra el menú '...' en la esquina superior derecha de la página, y encontrará 'Add connections' cerca de la parte inferior. Si no lo encuentra, verifique que tenga permisos de propietario en la página. No aparece con permisos de invitado.")
(no_integration -> Indicar: "Puede tardar un momento en aparecer la integración justo después de crearla. Recargue la página e inténtelo de nuevo. Si sigue sin aparecer, verifique que la integración se haya creado correctamente en https://www.notion.so/my-integrations.")
(skip_share -> Indicar: "Puede configurar esto más tarde. Esta configuración es necesaria cuando accede a páginas a través de MCP. Por favor configúrela antes de usar Notion en /start-12-1." Luego ir al Step 6)

---

## Step 6: Prueba de conexión MCP

**Lo que hace la IA:**

1. Guiar al usuario para reiniciar Claude Code / Cursor:

```text
Es necesario reiniciar la herramienta para aplicar la configuración MCP.

Para Claude Code:
  → Salga con exit, luego inicie claude nuevamente

Para Cursor:
  → Presione Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) para abrir
    la Paleta de comandos y ejecute "Reload Window"
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 6: Prueba de conexión MCP",
  "questions": [{
    "id": "restart_status",
    "prompt": "¿Reinició la herramienta?",
    "options": [
      {"id": "restarted", "label": "¡Reinicié! Ejecute la prueba por favor"},
      {"id": "how_restart", "label": "No sé cómo reiniciar"},
      {"id": "skip_test", "label": "Omitir la prueba"}
    ]
  }]
}
```

(restarted -> Ejecutar la prueba de conexión MCP)

2. Prueba de conexión MCP:
   - Verificar si la herramienta MCP de Notion está disponible
   - Si está disponible: obtener la lista de páginas de Notion para confirmar la conexión exitosa
   - Mostrar "Se obtuvieron X páginas de Notion. La conexión MCP funciona correctamente."

**En caso de éxito:**
```text
¡La configuración de Notion MCP se completó!

Resultado de la prueba: Se conectó exitosamente a Notion a través del servidor MCP.
Ahora puede operar páginas y bases de datos de Notion directamente desde Claude Code/Cursor.
```

**En caso de fallo - AskQuestion:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de conexión MCP. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Ejecutar la prueba de nuevo"},
      {"id": "check_config", "label": "Verificar el archivo de configuración MCP"},
      {"id": "recheck_key", "label": "Verificar la clave de API de nuevo (volver al Step 2)"},
      {"id": "show_error", "label": "Quiero ver los detalles del error"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(check_config -> Verificar el contenido del archivo de configuración MCP. Comprobar que NOTION_TOKEN no siga siendo el marcador de posición y que la sintaxis JSON sea correcta)
(recheck_key -> Volver al Step 2)
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
      {"id": "trouble_mcp_start", "label": "El servidor MCP no se inicia"},
      {"id": "trouble_invalid", "label": "Obtengo un error 'token_invalid'"},
      {"id": "trouble_permissions", "label": "Obtengo un error 'insufficient_permissions'"},
      {"id": "trouble_not_found", "label": "Obtengo un error 'object_not_found'"},
      {"id": "trouble_npx", "label": "No se encuentra el comando npx"},
      {"id": "trouble_cost", "label": "Me preocupan los costos"},
      {"id": "trouble_other", "label": "Otro error"}
    ]
  }]
}
```

### Problema 1: El servidor MCP no se inicia
**Causa**: Node.js no está instalado, npx no está disponible, o el JSON del archivo de configuración MCP está mal formado
**Lo que hace la IA**:
1. Verificar la existencia y versión de Node.js (se requiere 18 o superior) con `node --version`
2. Verificar si npx está disponible con `npx --version`
3. Validar el JSON del archivo de configuración MCP (verificación de sintaxis con `python -m json.tool`)
4. Si Node.js no está instalado: indicar "Instale la versión LTS desde https://nodejs.org/"

### Problema 2: Error "token_invalid"
**Causa**: La clave de API no se copió correctamente, o la clave es inválida
**Lo que hace la IA**:
1. Verificar el archivo de configuración MCP (solo comprobar que comience con `secret_`, sin mostrar el valor de la clave)
2. Verificar si sigue siendo el marcador de posición (`secret_your_token_here`)
3. Si hay un problema: indicar "Regenere el token en https://www.notion.so/my-integrations, luego actualice el archivo de configuración MCP"

### Problema 3: Error "insufficient_permissions"
**Causa**: La configuración de Capabilities de la integración es insuficiente, o la página no está compartida
**Lo que hace la IA**:
1. Indicar: "Verifique las Capabilities de la integración en https://www.notion.so/my-integrations. ¿Están marcados Read content / Update content / Insert content?"
2. Indicar: "¿Está compartida la integración con la página de Notion objetivo? Por favor revise las instrucciones del Step 5."

### Problema 4: Error "object_not_found"
**Causa**: La página objetivo no tiene la integración compartida
**Indicación de la IA**: "La integración no está compartida con la página de Notion a la que desea acceder a través de la API. Siga las instrucciones del Step 5 para agregar la integración desde 'Add connections' de la página. Agregarla a una página padre también se aplica a las páginas hijas."

### Problema 5: No se encuentra el comando npx
**Causa**: Node.js no está instalado, o el PATH no está configurado
**Lo que hace la IA**:
1. Verificar con `node --version`. Si no está instalado, guiar a https://nodejs.org/
2. Si está instalado pero es un problema de PATH, guiar para especificar la ruta completa (`/usr/local/bin/npx`) en el archivo de configuración

### Problema 6: Preocupación por los costos
**Indicación de la IA**: "Notion está disponible en plan gratuito. No hay costos adicionales por el uso de la API. Todas las funciones de la API están disponibles en el plan gratuito. El servidor MCP de Notion (@notionhq/notion-mcp-server) también es gratuito y de código abierto."

### Problema 7: Otros errores
**Lo que hace la IA**: Verificar el contenido del mensaje de error, identificar la causa e indicar la solución

---

## Punto de control
- [ ] ncli (@sakasegawa/ncli) está instalado
- [ ] Creó una integración (AIAgent Bootcamp) en la página de integraciones de Notion
- [ ] Copió el Internal Integration Secret (secret_xxx)
- [ ] Agregó la configuración del servidor Notion al archivo de configuración MCP
- [ ] Compartió la integración con las páginas de Notion a las que desea acceder
- [ ] Reinició Claude Code / Cursor
- [ ] La prueba de conexión MCP fue exitosa (pudo acceder a las páginas de Notion)

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
