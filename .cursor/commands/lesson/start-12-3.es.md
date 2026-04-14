---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module12-notion"
duration: "~30 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["notion", "mcp", "api"]
---

# 🎓 Lesson 12-3: Creacion de paginas de Notion

## 📍 Lo que hara en esta sesion

**Lesson 12-3** !

| Elemento | Contenido |
|------|------|
| Objetivo | Operar paginas y bases de datos de Notion desde Claude Code usando MCP/Notion API |
| Duracion | ~30 min |
| Habilidades utilizadas | Notion API, MCP（Model Context Protocol） |
| Requisitos previos | Cuenta de Notion, permisos de creacion de integracion |
| Pagina del curso | [Module 12: Notion](https://ai-agent.camp/es/course/module-12)  como referencia paralela |

**Flujo de la sesion:**
1. Crear una integración de Notion
2. Obtener la clave API y el ID de la base de datos
3. Leer y escribir páginas y bases de datos

Al final de esta sesion, podra operar Notion desde Claude Code.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

---

## Browser Authentication at Lesson Start (Notion MCP)

Al proceder con `/start-12-3`, puede abrirse una pantalla de **"Connect with Notion MCP"** en el navegador del lado de Notion. Esto se muestra cuando el MCP local recibe tokens a través de una URL de callback `127.0.0.1`.

**Puntos clave de operación en pantalla:**

1. **Título**: Dirá algo como "Connect with Notion MCP" o "Grant 127.0.0.1 access to Notion", indicando que es una conexión a una aplicación local.
2. **Select workspace**: Elija el espacio de trabajo para conectar del menú desplegable.
3. **Descripción de permisos**: Se enumeran elementos como el respeto al acceso de páginas/bases de datos, operaciones basadas en sus permisos, búsqueda (según el plan) y visualización de información del usuario.
4. **Cuadro de advertencia amarillo**: Se muestra una URL como **`http://127.0.0.1:<puerto>/callback`** como destino de redirección. **El número de puerto puede cambiar cada vez que se inicia**.
5. **"I recognize and trust this URL."**: **Continue** puede no activarse/avanzar a menos que **marque esta casilla**. Verifique que el contenido es un callback local antes de marcar.
6. Complete la autenticación con **Continue** y regrese al editor o al lado del cliente MCP.

Pantalla de referencia:

![Notion MCP Connect with Notion MCP (confirmación de callback local)](../../../docs/images/notion-mcp-connect-oauth.png)

> **Nota**: El texto y los elementos de la interfaz pueden cambiar con las actualizaciones de Notion. Si el contenido difiere significativamente, consulte la ayuda oficial o las instrucciones más recientes del curso.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Create Notion Integration

**Requisito previo:** El servidor Notion MCP debe estar configurado.
Si no está configurado, ejecute `/setup-notion` primero.

**What the AI automatically verifies:**
1. Verificar que el servidor `notion` está definido en el archivo de configuración MCP:
   - Claude Code: Leer `~/.claude/mcp_settings.json` y verificar que existe `mcpServers.notion`
   - Cursor: Leer `.cursor/mcp.json` y verificar que existe `mcpServers.notion`
2. Si ya está configurado -> proceder al Step 2 (creación del archivo de configuración MCP)
3. Si no está configurado -> guiar la ejecución de `/setup-notion`

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verificar integración de Notion",
  "questions": [{
    "id": "step_action",
    "prompt": "Verificaremos el estado de configuración de NOTION_API_KEY.",
    "options": [
      {"id": "check", "label": "Verificar estado de configuración"},
      {"id": "setup_notion", "label": "Configurar con /setup-notion"},
      {"id": "skip", "label": "Omitir (si ya está configurado)"}
    ]
  }]
}
```

(check → Verificar la entrada notion en el archivo de configuración MCP. Si está configurado, proceder al Step 2)
(setup_notion → Guiar la ejecución de /setup-notion)
(skip → Proceder al Step 2)

---

## 🚀 Step 2: Create MCP Configuration File

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear archivo de configuración MCP",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, cree el archivo de configuración MCP para Claude Code.

Archivo: ~/.claude/mcp_settings.json

Contenido (reemplace NOTION_API_KEY con su token real):
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@notionhq/notion-mcp-server"
      ],
      "env": {
        "NOTION_API_KEY": "secret_your_token_here"
      }
    }
  }
}

Por favor, cree el archivo.
```

**Resultado esperado:** Se crea el archivo de configuracion MCP. Reemplace el token real manualmente.

---

## 🚀 Step 3: Grant Workspace Access Permission

Si aparece **Connect with Notion MCP** en el navegador, siga las instrucciones de **"Autenticación del navegador al inicio de la lección (Notion MCP)"** al comienzo de este documento, revise la explicación de la URL de redirección, marque **"I recognize and trust this URL."** y luego haga clic en **Continue**.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Permiso de acceso al espacio de trabajo",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, explique cómo otorgar permisos de acceso a la integración en Notion.

Pasos:
1. Abrir una página en Notion
2. Menú "..." en la esquina superior derecha > Connections
3. Añadir la integración creada "Claude MCP Integration"

Nota: Solo las páginas debajo de la página donde se añadió la integración serán accesibles.
```

**Resultado esperado:** Se explican los pasos para configurar permisos de acceso a paginas de Notion.

---

## 🚀 Step 4: Connection Test

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Prueba de conexión",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Realizaremos una prueba de conexión de Notion MCP.

Por favor, verifique lo siguiente:
1. El archivo de configuración MCP (~/.claude/mcp_settings.json) existe
2. NOTION_API_KEY está configurado
3. Reinicie Claude Code y verifique que MCP se cargue

Como prueba de conexión, conéctese a Notion y liste las páginas accesibles.
```

**Resultado esperado:** Si MCP esta configurado correctamente, se muestra una lista de paginas de Notion.

---

## 🚀 Step 5: Basic Operations Test

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Prueba de operaciones básicas",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, pruebe las siguientes operaciones en Notion:

1. Prueba de creación de página:
   - Crear una página llamada "Prueba de conexión MCP"
   - Escribir "¡Prueba de conexión MCP desde Claude Code exitosa!" como contenido
   - También añadir la hora actual

2. Prueba de lectura de página:
   - Leer y mostrar el contenido de la página creada

3. Prueba de actualización de página:
   - Añadir "Fecha de actualización: [hora actual]" a la página

Por favor, informe los resultados de cada operación.
```

**Resultado esperado:** Se pueden crear, leer y actualizar paginas de Notion desde Claude Code.

---

## ⚠️ Problemas comunes y soluciones

Utilice AskQuestion para seleccionar el problema y luego siga las indicaciones.

**Configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "Could not connect to Notion"},
      {"id": "trouble_2", "label": "Insufficient permissions"},
      {"id": "trouble_3", "label": "El servidor MCP no se inicia"},
      {"id": "trouble_4", "label": "Página no encontrada"}
    ]
  }]
}
```


### Problema 1: "Could not connect to Notion"
**Causa:** La clave API es incorrecta o la ruta del archivo de configuracion MCP es incorrecta
**Prompt de solucion:**
```
Por favor, verifique lo siguiente:
1. La ruta ~/.claude/mcp_settings.json es correcta
2. El valor de NOTION_API_KEY comienza con "secret_"
3. La sintaxis JSON es correcta (comas, corchetes, etc.)
```

### Problema 2: "Insufficient permissions"
**Causa:** La integracion no se ha anadido a la pagina
**Prompt de solucion:**
```
Abra la página objetivo en Notion, y verifique desde "..." en la esquina superior derecha > Connections
si se ha añadido "Claude MCP Integration".
Añadir la integración a una página principal también otorga acceso a las páginas secundarias.
```

### Problema 3: El servidor MCP no se inicia
**Causa:** La version de Node.js es antigua o npx no esta disponible
**Prompt de solucion:**
```
Por favor, verifique lo siguiente:
1. Verificar que node --version sea v18 o superior
2. Verificar que npx esté disponible con npx --version
3. Instalar npx con npm install -g npx
```

### Problema 4: Pagina no encontrada
**Causa:** La integracion no tiene permisos de acceso
**Prompt de solucion:**
```
En el espacio de trabajo de Notion, añada la integración a la página
o página principal a la que desea acceder.
Para otorgar acceso a todo el espacio de trabajo, añádala a la página de nivel superior.
```

---

## ✅ Punto de control
- [ ] La integración de Notion ha sido creada
- [ ] Se ha obtenido el token secreto
- [ ] El archivo de configuración MCP ha sido creado
- [ ] La integración se ha añadido a la página de Notion
- [ ] Se pueden crear, leer y actualizar páginas

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestran el estado completado/incompleto y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-12-4)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-12-4
- finish → Finalizar
