---
description: "Lesson command"
duration: "~15 min"
prerequisites: ["Navegador disponible", "Claude Code o Cursor instalado"]
level: "beginner"
tags: ["setup", "pencil", "mcp", "design"]
nonInteractiveMode: deferred
---
# Configuración de Pencil MCP

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-pencil` para mostrar el progreso
2. Detectar automáticamente la configuración existente:
   - Para Claude Code: Verificar si el servidor `pencil` está definido en `~/.claude/mcp_settings.json`
   - Para Cursor: Verificar si el servidor `pencil` está definido en `.cursor/mcp.json`
   - Si ya está configurado, solo ejecutar Step 4 (prueba de conexión) y marcar como completado

## Lo que hará en esta sesión

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar la aplicación de escritorio Pencil y habilitar la operación de archivos de diseño (.pen) desde Claude Code/Cursor a través del servidor MCP |
| Duración | ~15 minutos |
| Requisitos previos | Navegador disponible, Claude Code o Cursor ya instalado |
| Nivel de operación | Instalación de aplicación + configuración MCP (asistido por IA) |

**Flujo de la sesión:**
1. Descargar e instalar la aplicación de escritorio Pencil
2. Iniciar Pencil y completar la configuración inicial
3. Agregar el servidor Pencil al archivo de configuración MCP
4. Prueba de conexión MCP

> **Consejo**: Si la IA deja de responder a mitad del proceso, escriba "por favor continúa" o "se detuvo" para reanudar.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Confirmación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "already_installed", "label": "Pencil ya está instalado"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(check_prereq -> Indicar: "Si Claude Code o Cursor ya está instalado, está listo para continuar")
(already_installed -> Saltar al Step 3 (configuración MCP))
(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Descargar la aplicación de escritorio Pencil

**Lo que hace la IA:**
1. Detectar automáticamente el sistema operativo (Mac / Windows / Linux)
2. Abrir la página de descarga de Pencil en el navegador:

```bash
# Mac:
open https://pencil.evolves.dev/download
# Windows:
start https://pencil.evolves.dev/download
# Linux:
xdg-open https://pencil.evolves.dev/download
```

**Una vez que se abra el navegador, mostrar el siguiente AskQuestion:**

```json
{
  "title": "Step 1: Descargar la aplicación Pencil",
  "questions": [{
    "id": "download_status",
    "prompt": "¿Se abrió la página de descarga de Pencil en su navegador?\n\nPasos:\n1. Descargue el instalador correspondiente a su sistema operativo (Mac / Windows)\n2. Ejecute el archivo descargado para instalar\n   - Mac: Abra el .dmg y arrastre a la carpeta Aplicaciones\n   - Windows: Ejecute el .exe y siga el asistente\n\n¿Pudo instalarlo?",
    "options": [
      {"id": "installed", "label": "¡Instalado!"},
      {"id": "browser_not_open", "label": "El navegador no se abrió"},
      {"id": "download_issue", "label": "No puedo descargar"},
      {"id": "mac_security", "label": "Aparece una advertencia de seguridad de Mac"}
    ]
  }]
}
```

(installed -> Ir al Step 2)
(browser_not_open -> Indicar: "Abra esta URL directamente en su navegador: https://pencil.evolves.dev/download")
(download_issue -> Indicar: "Verifique su conexión a internet. Si la descarga es lenta, espere un momento")
(mac_security -> Indicar: "Vaya a Configuración del Sistema -> Privacidad y Seguridad -> haga clic en 'Abrir de todos modos'. Alternativamente, haga clic derecho en la aplicación en Finder y seleccione 'Abrir'")

---

## Step 2: Iniciar y configurar inicialmente la aplicación Pencil

**Mensaje para mostrar al usuario:**

```text
Inicie la aplicación Pencil:

┌─────────────────────────────────────────────────────────────┐
│ 1. Inicie "Pencil" desde sus Aplicaciones                   │
│ 2. Si se requiere crear una cuenta o iniciar sesión en      │
│    el primer inicio, siga las instrucciones en pantalla     │
│ 3. Está listo cuando aparezca la pantalla del editor        │
│                                                             │
│ * Pencil es una aplicación de escritorio para crear y       │
│   editar archivos de diseño en formato .pen                 │
└─────────────────────────────────────────────────────────────┘
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 2: Iniciar la aplicación Pencil",
  "questions": [{
    "id": "app_status",
    "prompt": "¿Pudo iniciar la aplicación Pencil?",
    "options": [
      {"id": "running", "label": "¡Pencil está funcionando!"},
      {"id": "cant_find", "label": "No puedo encontrar la aplicación"},
      {"id": "crash", "label": "Se bloquea al iniciar"},
      {"id": "login_issue", "label": "Tengo problemas con el inicio de sesión/creación de cuenta"}
    ]
  }]
}
```

(running -> Ir al Step 3)
(cant_find -> Mac: Verificar la carpeta "Aplicaciones" / Windows: Verificar el menú Inicio. Si la instalación no se completó, volver al Step 1)
(crash -> Indicar: "Asegúrese de que su sistema operativo esté actualizado. Si el problema persiste, intente desinstalar y reinstalar")
(login_issue -> Indicar: "Puede crear una cuenta en el sitio web de Pencil (https://pencil.evolves.dev). Puede registrarse con su dirección de correo electrónico")

---

## Step 3: Agregar el servidor Pencil al archivo de configuración MCP

**Lo que la IA ejecuta automáticamente:**

1. Determinar la herramienta en uso (Claude Code o Cursor)
2. Guiar la configuración del servidor Pencil MCP

**Método de conexión de Pencil MCP:**

Pencil MCP está integrado en la aplicación de escritorio Pencil. Cuando la aplicación está en ejecución, se hace disponible automáticamente como servidor MCP.

**Para Claude Code:** Agregue lo siguiente a `~/.claude/mcp_settings.json`:
```json
{
  "mcpServers": {
    "pencil": {
      "url": "http://localhost:13742/sse"
    }
  }
}
```

**Para Cursor:** Agregue lo siguiente a `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "pencil": {
      "url": "http://localhost:13742/sse"
    }
  }
}
```

> **Nota**: Si ya tiene un archivo de configuración MCP, agregue la entrada `pencil` dentro de `mcpServers`. No elimine las configuraciones de otros servidores.

**Configuración de AskQuestion:**
```json
{
  "title": "Step 3: Configuración MCP",
  "questions": [{
    "id": "config_status",
    "prompt": "¿Ha agregado la configuración del servidor Pencil al archivo de configuración MCP?",
    "options": [
      {"id": "done", "label": "¡Configuración agregada!"},
      {"id": "auto_setup", "label": "Quiero que la IA lo configure automáticamente"},
      {"id": "existing_config", "label": "Ya tengo un archivo de configuración y quiero saber cómo agregar"},
      {"id": "help", "label": "No sé cómo configurarlo"}
    ]
  }]
}
```

(done -> Ir al Step 4)
(auto_setup -> La IA crea/actualiza automáticamente el archivo de configuración. Las configuraciones de servidores existentes se conservan)
(existing_config -> Leer el contenido del archivo existente y guiar cómo agregar la entrada `pencil` a `mcpServers`)
(help -> Guiar con pasos detallados para cada herramienta)

---

## Step 4: Prueba de conexión MCP

**Lo que hace la IA:**

1. Guiar el reinicio de Claude Code / Cursor:

```text
Necesita reiniciar su herramienta para aplicar la configuración MCP.

Para Claude Code:
  -> Salga con 'exit' y reinicie claude

Para Cursor:
  -> Presione Cmd+Shift+P (Mac) / Ctrl+Shift+P (Windows) para
    abrir la Paleta de Comandos y ejecute "Reload Window"
```

**Configuración de AskQuestion:**
```json
{
  "title": "Step 4: Prueba de conexión MCP",
  "questions": [{
    "id": "restart_status",
    "prompt": "¿Ha reiniciado su herramienta? (Confirme también que la aplicación Pencil esté en ejecución)",
    "options": [
      {"id": "restarted", "label": "¡Reiniciado! Ejecute la prueba"},
      {"id": "how_restart", "label": "No sé cómo reiniciar"},
      {"id": "skip_test", "label": "Omitir la prueba"}
    ]
  }]
}
```

(restarted -> Ejecutar prueba de conexión MCP)

2. Prueba de conexión MCP:
   - Ejecutar `get_editor_state()` para obtener el estado de Pencil
   - Conexión exitosa: Mostrar "Conexión exitosa al servidor Pencil MCP"
   - Conexión fallida: Ir a solución de problemas

**Al tener éxito en la prueba:**
```text
¡La configuración de Pencil MCP está completa!

Resultado de la prueba: Conexión exitosa al servidor Pencil MCP.
Ahora puede crear y editar archivos .pen directamente desde Claude Code/Cursor.

Herramientas disponibles:
- get_editor_state(): Obtener el estado del editor
- open_document(): Crear/abrir documentos
- batch_design(): Insertar, actualizar y eliminar elementos de diseño
- get_screenshot(): Tomar capturas de pantalla
- get_guidelines(): Obtener guías de diseño
```

**AskQuestion en caso de fallo en la prueba:**
```json
{
  "title": "Resultado de la prueba: Ocurrió un error",
  "questions": [{
    "id": "test_error",
    "prompt": "Ocurrió un error durante la prueba de conexión MCP. Verifiquemos las posibles causas.",
    "options": [
      {"id": "retry", "label": "Intentar la prueba de nuevo"},
      {"id": "check_app", "label": "Verificar si la aplicación Pencil está en ejecución"},
      {"id": "check_config", "label": "Verificar el archivo de configuración MCP"},
      {"id": "check_port", "label": "Verificar si el puerto 13742 está disponible"},
      {"id": "skip_test", "label": "Omitir la prueba y continuar"}
    ]
  }]
}
```

(retry -> Volver a ejecutar la prueba)
(check_app -> Indicar: "No se puede conectar al servidor MCP si la aplicación Pencil no está en ejecución. Inicie la aplicación Pencil e intente la prueba de nuevo")
(check_config -> Verificar el contenido del archivo de configuración MCP. Comprobar que la URL sea correcta y la sintaxis JSON sea válida)
(check_port -> Verificar el uso del puerto con `lsof -i :13742`)
(skip_test -> Indicar: "Prueba omitida. Puede verificar la conexión cuando use Pencil MCP en la Lección 13-3")

---

## Solución de problemas comunes

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda",
    "options": [
      {"id": "trouble_connect", "label": "No puedo conectar al servidor MCP"},
      {"id": "trouble_app", "label": "La aplicación Pencil no se inicia"},
      {"id": "trouble_port", "label": "El puerto ya está en uso"},
      {"id": "trouble_cost", "label": "Me preocupa el precio"}
    ]
  }]
}
```

### Problema 1: No se puede conectar al servidor MCP
**Causa**: La aplicación Pencil no está en ejecución, o la URL de configuración MCP es incorrecta
**Lo que hace la IA**:
1. Guiar la verificación de si la aplicación Pencil está en ejecución
2. Verificar que la URL del archivo de configuración MCP sea `http://localhost:13742/sse`
3. Verificar el estado de escucha del puerto con `lsof -i :13742`

### Problema 2: La aplicación Pencil no se inicia
**Causa**: Instalación incompleta o incompatibilidad del sistema operativo
**Lo que hace la IA**:
1. Verificar la versión del sistema operativo
2. Guiar la reinstalación
3. Verificar la configuración de seguridad de Mac (Gatekeeper)

### Problema 3: El puerto ya está en uso
**Causa**: Otro proceso está usando el puerto 13742
**Lo que hace la IA**:
1. Verificar el proceso que usa el puerto con `lsof -i :13742`
2. Guiar la detención del proceso en conflicto

### Problema 4: Preocupación por el precio
**Indicación de la IA**: "La aplicación Pencil tiene un plan gratuito. Las funciones básicas, incluida la integración MCP, están disponibles de forma gratuita. Consulte https://pencil.evolves.dev para más detalles"

---

## Punto de verificación
- [ ] Descargó e instaló la aplicación de escritorio Pencil
- [ ] La aplicación Pencil se inicia correctamente
- [ ] Agregó la configuración del servidor Pencil al archivo de configuración MCP
- [ ] Reinició Claude Code / Cursor
- [ ] La prueba de conexión MCP fue exitosa (get_editor_state funciona)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¡La configuración de Pencil MCP está completa! ¿Qué desea hacer ahora?",
    "options": [
      {"id": "start_design", "label": "Iniciar diseño de LP (/start-13-3)"},
      {"id": "try_pencil", "label": "Probar las operaciones básicas de Pencil"},
      {"id": "setup_other", "label": "Configurar otras API (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

- start_design -> Guiar a /start-13-3
- try_pencil -> Guiar las operaciones básicas: get_editor_state, open_document, batch_design
- setup_other -> Guiar a /start-0-1
- finish -> Finalizar

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-pencil` para actualizar el progreso
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "A continuación, comencemos el diseño de LP con Pencil usando `/start-13-3`"
