---
description: "Configuración automática de extensiones"
duration: "~5 min"
prerequisites: ["Cursor está en ejecución"]
level: "beginner"
tags: ["setup", "extensions"]
---

# /setup-extensions -- Configuración automática de extensiones

## Step 0: Verificar el progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-extensions` para mostrar el progreso
2. Verificar las extensiones ya instaladas; si todas están presentes, confirmar "Las extensiones ya están instaladas. ¿Desea omitir?"

## Función de este comando

La IA **verifica e instala automáticamente** las extensiones de Cursor / VS Code.
No necesita ejecutar ningún comando en la terminal. La IA se encarga de todo.

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Instalar automáticamente todas las extensiones necesarias para el curso |
| Duración | ~5 minutos |
| Requisitos previos | Cursor (o VS Code) está en ejecución |
| Acción del usuario | Solo presionar botones (no se necesitan comandos CLI) |

> **Punto clave**: Todas las operaciones de este comando son ejecutadas automáticamente por la IA. No necesita escribir comandos en la terminal.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Iniciando la configuración de extensiones",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está preparado/a?",
    "options": [
      {"id": "ready", "label": "Comencemos"},
      {"id": "what_is_this", "label": "¿Qué son las extensiones? Quiero una explicación primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(what_is_this -> Mostrar lo siguiente)

> **¿Qué son las extensiones?**
> Son como "paquetes de funcionalidades" que puede agregar a Cursor (el editor).
> Por ejemplo, al instalar la "extensión de Python", se habilita el resaltado de sintaxis y el autocompletado para código Python.
> Esta configuración instala automáticamente las extensiones necesarias para el curso.

(different_lesson -> Mostrar la lista de módulos)

---

## Step 1: Verificar las extensiones actuales

**Lo que la IA ejecuta automáticamente:**

1. La IA ejecuta el siguiente comando **internamente** para obtener la lista de extensiones instaladas:
```bash
cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null
```

2. Mostrar la lista en formato de tabla fácil de leer:
```text
Extensiones actualmente instaladas:
| # | ID de extensión | Descripción |
|---|----------------|-------------|
| 1 | ms-python.python | Python |
| 2 | ... | ... |

Total: XX extensiones están instaladas.
```

3. Si el comando falla (no se encuentra ni `cursor` ni `code`):
   - Mostrar "No se encontró la herramienta de línea de comandos de Cursor"
   - **Para Cursor**: Indicar: "Abra el menú de Cursor > Paleta de comandos (Cmd+Shift+P / Ctrl+Shift+P) > seleccione 'Shell Command: Install 'cursor' command'"
   - **Para VS Code**: Indicar: "Abra la Paleta de comandos > seleccione 'Shell Command: Install 'code' command in PATH'"
   - Después de resolverlo, volver a ejecutar el Step 1

**Nota: No pida al usuario que escriba comandos. La IA ejecuta todo automáticamente y solo muestra los resultados.**

---

## Step 2: Instalación automática de extensiones requeridas

**Lo que la IA ejecuta automáticamente:**

1. Comparar la "lista de extensiones requeridas" a continuación con los resultados del Step 1 e identificar las faltantes:

| ID de extensión | Propósito |
|----------------|-----------|
| `marp-team.marp-vscode` | Crear presentaciones en Markdown (Marp) |
| `hediet.vscode-drawio` | Crear y editar diagramas en el editor (Draw.io) |
| `jebbs.plantuml` | Generar automáticamente diagramas UML a partir de texto (PlantUML) |
| `nicepkg.aide-pro` | Asistente de desarrollo con IA (AIDE Pro) |
| `ms-python.python` | Ejecución y depuración de código Python |
| `ms-python.vscode-pylance` | Autocompletado y verificación de tipos de alta precisión para Python |
| `esbenp.prettier-vscode` | Formateo automático de código (Prettier) |

2. Si se encuentran extensiones faltantes, informar al usuario e instalar:
```text
Las siguientes extensiones no están instaladas. Instalando automáticamente:
- marp-team.marp-vscode (Presentaciones en Markdown)
- hediet.vscode-drawio (Editor de diagramas)

Instalando...
```

3. Instalar cada extensión con el siguiente comando **internamente**:
```bash
cursor --install-extension {ID_extensión} 2>/dev/null || code --install-extension {ID_extensión}
```

4. Si todas ya están instaladas:
```text
Todas las extensiones requeridas ya están instaladas (7/7).
```

5. Informar los resultados de instalación uno por uno:
```text
| Extensión | Estado |
|-----------|--------|
| Marp | Instalación completada |
| Draw.io | Instalación completada |
| PlantUML | Ya instalada |
| ... | ... |
```

**Nota: La IA ejecuta los comandos de instalación automáticamente. Solo se muestran los resultados al usuario.**

---

## Step 3: Extensiones recomendadas

**Configuración de AskQuestion:**
```json
{
  "title": "¿Instalar también las extensiones recomendadas?",
  "questions": [{
    "id": "optional_install",
    "prompt": "Las siguientes extensiones no son obligatorias pero son útiles. ¿Desea instalarlas?\n- Git Graph: Visualizar el historial de Git\n- GitLens: Mostrar el historial de cambios de cada línea\n- Markdown All in One: Conjunto de funciones convenientes para Markdown",
    "options": [
      {"id": "yes_all", "label": "Instalar todas"},
      {"id": "choose", "label": "Quiero elegir cuáles instalar"},
      {"id": "skip", "label": "Omitir por ahora"}
    ]
  }]
}
```

(yes_all -> Instalar automáticamente todas las siguientes)
(choose -> Permitir al usuario seleccionar individualmente vía AskQuestion)
(skip -> Ir al Step 4)

**Lista de extensiones recomendadas:**

| ID de extensión | Propósito |
|----------------|-----------|
| `mhutchie.git-graph` | Mostrar el historial de Git como un gráfico (ver el flujo de ramas de un vistazo) |
| `eamodio.gitlens` | Mostrar el último autor y fecha de cada línea |
| `yzhang.markdown-all-in-one` | Funciones convenientes de edición de Markdown (tabla de contenidos automática, atajos, etc.) |

**Lo que la IA ejecuta automáticamente:**
- Instalar las extensiones seleccionadas con `cursor --install-extension {ID} 2>/dev/null || code --install-extension {ID}`
- Informar los resultados en formato de tabla

**(Para choose) Configuración de AskQuestion:**
```json
{
  "title": "Seleccionar extensiones para instalar",
  "questions": [
    {
      "id": "git_graph",
      "prompt": "¿Instalar Git Graph (visualizar historial de Git)?",
      "options": [
        {"id": "yes", "label": "Instalar"},
        {"id": "no", "label": "Omitir"}
      ]
    },
    {
      "id": "gitlens",
      "prompt": "¿Instalar GitLens (mostrar historial de cambios por línea)?",
      "options": [
        {"id": "yes", "label": "Instalar"},
        {"id": "no", "label": "Omitir"}
      ]
    },
    {
      "id": "markdown",
      "prompt": "¿Instalar Markdown All in One (funciones convenientes de Markdown)?",
      "options": [
        {"id": "yes", "label": "Instalar"},
        {"id": "no", "label": "Omitir"}
      ]
    }
  ]
}
```

---

## Step 4: Verificar los resultados de instalación

**Lo que la IA ejecuta automáticamente:**

1. Volver a ejecutar `cursor --list-extensions 2>/dev/null || code --list-extensions 2>/dev/null` **internamente**
2. Verificar que todas las extensiones requeridas estén instaladas
3. Mostrar los resultados finales en formato de tabla:

```text
## Resultados de la configuración de extensiones

### Extensiones requeridas (7)
| Extensión | Propósito | Estado |
|-----------|-----------|--------|
| Marp | Creación de presentaciones | Instalada |
| Draw.io | Creación de diagramas | Instalada |
| PlantUML | Generación de diagramas UML | Instalada |
| AIDE Pro | Asistente de desarrollo con IA | Instalada |
| Python | Desarrollo Python | Instalada |
| Pylance | Autocompletado Python | Instalada |
| Prettier | Formateo de código | Instalada |

### Extensiones recomendadas
| Extensión | Estado |
|-----------|--------|
| Git Graph | Instalada / No instalada |
| GitLens | Instalada / No instalada |
| Markdown All in One | Instalada / No instalada |
```

4. Si todas están instaladas: Mostrar "La configuración de extensiones se completó"
5. Si alguna extensión falló al instalarse:
   - Mostrar "Las siguientes extensiones no se pudieron instalar"
   - Indicar con instrucciones de GUI: "Abra el panel de extensiones (Cmd+Shift+X / Ctrl+Shift+X), busque '{nombre de extensión}' e instálela manualmente"

---

## Problemas comunes y soluciones

**Configuración de AskQuestion:**
```json
{
  "title": "¿Tiene algún problema?",
  "questions": [{
    "id": "trouble",
    "prompt": "¿Tiene algún problema?",
    "options": [
      {"id": "trouble_1", "label": "La instalación de extensiones está fallando"},
      {"id": "trouble_2", "label": "No se encuentra el comando cursor"},
      {"id": "trouble_3", "label": "Lo instalé pero no funciona"},
      {"id": "no_trouble", "label": "Sin problemas, continuar"}
    ]
  }]
}
```

### Problema 1: La instalación de extensiones falla
**Causa**: Problemas de conexión de red o interrupción del servidor del marketplace
**Lo que hace la IA**:
1. Verificar la conexión de red (la IA ejecuta internamente):
```bash
# Mac / Linux
ping -c 1 marketplace.visualstudio.com

# Windows
ping -n 1 marketplace.visualstudio.com
```
2. Si la conexión es correcta, reintentar
3. Si aún falla -> Indicar con instrucciones de GUI:
   "Abra el panel de extensiones (Cmd+Shift+X / Ctrl+Shift+X) y busque/instale manualmente"

### Problema 2: No se encuentra el comando cursor
**Causa**: La herramienta de línea de comandos de Cursor no está agregada al PATH
**Lo que hace la IA**:
- Indicar: "Abra la Paleta de comandos (Cmd+Shift+P / Ctrl+Shift+P), escriba 'Shell Command: Install' y seleccione el elemento que aparece"
- "Luego reinicie Cursor y vuelva a ejecutar este comando"

### Problema 3: Instalado pero no funciona
**Causa**: Cursor necesita recargarse
**Lo que hace la IA**:
- Indicar: "Abra la Paleta de comandos (Cmd+Shift+P / Ctrl+Shift+P) y seleccione 'Developer: Reload Window'"

---

## Punto de control

- [ ] Las 7 extensiones requeridas están instaladas
- [ ] Se puede confirmar en el panel de extensiones (Cmd+Shift+X / Ctrl+Shift+X)
- [ ] El resaltado de sintaxis está activo al abrir un archivo Python

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¿Qué desea hacer ahora?",
    "options": [
      {"id": "security", "label": "Configurar ajustes de seguridad (/setup-security)"},
      {"id": "check", "label": "Verificar todo el entorno (/check-setup)"},
      {"id": "lesson", "label": "Comenzar una lección (/start-0-1)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

(security -> Dirigir a /setup-security)
(check -> Dirigir a /check-setup)
(lesson -> Dirigir a /start-0-1)
(finish -> Mostrar "¡Buen trabajo!")

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-extensions` para actualizar el progreso
2. El resumen de progreso actualizado se muestra automáticamente
3. Indicar al usuario el siguiente paso: "A continuación, configure los ajustes de seguridad con `/setup-security`"
