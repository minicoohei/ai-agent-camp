---
name: create-cowork-plugin
description: "Habilidad para crear plugins desde cero durante una sesión de Cowork. Se activa con solicitudes como 'crea un plugin,' 'desarrollo de plugin,' 'crear plugin,' etc. Genera archivos .plugin en modo Cowork."
compatibility: Requires Cowork desktop app environment with access to the outputs directory for delivering .plugin files.
source: github.com/anthropics/knowledge-work-plugins@main
triggers:
  - create-cowork-plugin
  - プラグインを作って
  - プラグイン開発
  - plugin作成
  - プラグイン設計
  - cowork plugin
---

# Crear Plugin de Cowork

Construya un nuevo plugin desde cero a través de una conversación guiada. Guíe al usuario a través del descubrimiento, planificación, diseño, implementación y empaquetado — entregando un archivo `.plugin` listo para instalar al final.

## Descripción General

Un plugin es un directorio autónomo que extiende las capacidades de Claude con comandos, habilidades, agentes, hooks e integraciones de servidor MCP. Esta habilidad codifica la arquitectura completa de plugins y un flujo de trabajo de cinco fases para crear uno de forma conversacional.

El proceso:
1. **Descubrimiento** — entender qué quiere construir el usuario
2. **Planificación de Componentes** — determinar qué tipos de componentes se necesitan
3. **Diseño y Preguntas Clarificadoras** — especificar cada componente en detalle
4. **Implementación** — crear todos los archivos del plugin
5. **Revisión y Empaquetado** — entregar el archivo `.plugin`

> **Salida no técnica**: Mantenga toda la conversación con el usuario en lenguaje simple. No exponga detalles de implementación como rutas de archivos, estructuras de directorios o campos de esquema a menos que el usuario lo solicite. Enmarque todo en términos de lo que hará el plugin.

## Arquitectura del Plugin

### Estructura de Directorios

Cada plugin sigue este diseño:

```
nombre-del-plugin/
├── .claude-plugin/
│   └── plugin.json           # Requerido: manifiesto del plugin
├── commands/                 # Comandos slash (archivos .md)
├── agents/                   # Definiciones de subagentes (archivos .md)
├── skills/                   # Habilidades (subdirectorios con SKILL.md)
│   └── nombre-habilidad/
│       ├── SKILL.md
│       └── references/
├── .mcp.json                 # Definiciones de servidor MCP
└── README.md                 # Documentación del plugin
```


**Reglas:**
- `.claude-plugin/plugin.json` siempre es requerido
- Los directorios de componentes (`commands/`, `agents/`, `skills/`) van en la raíz del plugin, no dentro de `.claude-plugin/`
- Solo cree directorios para los componentes que el plugin realmente usa
- Use kebab-case para todos los nombres de directorios y archivos

### Manifiesto plugin.json

Ubicado en `.claude-plugin/plugin.json`. El campo mínimo requerido es `name`.

```json
{
  "name": "nombre-del-plugin",
  "version": "0.1.0",
  "description": "Breve explicación del propósito del plugin",
  "author": {
    "name": "Nombre del Autor"
  }
}
```

**Reglas de nombre:** kebab-case, minúsculas con guiones, sin espacios ni caracteres especiales.
**Versión:** formato semver (MAYOR.MENOR.PARCHE). Comience en `0.1.0`.

Campos opcionales: `homepage`, `repository`, `license`, `keywords`.

Se pueden especificar rutas personalizadas de componentes (complementa, no reemplaza, el auto-descubrimiento):
```json
{
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

### Esquemas de Componentes

Los esquemas detallados para cada tipo de componente están en `references/component-schemas.md`. Resumen:

| Componente | Ubicación | Formato |
|------------|----------|---------|
| Comandos | `commands/*.md` | Markdown + frontmatter YAML |
| Habilidades | `skills/*/SKILL.md` | Markdown + frontmatter YAML |
| Servidores MCP | `.mcp.json` | JSON |
| Agentes (poco comunes en Cowork) | `agents/*.md` | Markdown + frontmatter YAML |
| Hooks (raro en Cowork) | `hooks/hooks.json` | JSON |

Este esquema se comparte con el sistema de plugins de Claude Code, pero usted está creando un plugin para Claude Cowork, una aplicación de escritorio para trabajo de conocimiento.
Los usuarios de Cowork generalmente encontrarán más útiles los comandos y las habilidades.

### Plugins personalizables con marcadores `~~`

> **No use ni pregunte sobre este patrón por defecto.** Solo introduzca marcadores `~~` si el usuario dice explícitamente que quiere que personas fuera de su organización usen el plugin.
> Puede mencionar que esta es una opción si parece que el usuario quiere distribuir el plugin externamente, pero no pregunte proactivamente sobre esto con AskUserQuestion.

Cuando un plugin está destinado a ser compartido con otros fuera de su empresa, puede tener partes que necesitan adaptarse a usuarios individuales.
Podría necesitar hacer referencia a herramientas externas por categoría en lugar de producto específico (por ejemplo, "gestor de proyectos" en lugar de "Jira").
Cuando se necesita compartir, use lenguaje genérico y marque estos como que requieren personalización con dos caracteres de tilde como `create an issue in ~~project tracker`.
Si usó alguna categoría de herramienta, escriba un archivo `CONNECTORS.md` en la raíz del plugin para explicar:

```markdown
# Conectores

## Cómo funcionan las referencias de herramientas

Los archivos del plugin usan `~~categoría` como marcador para cualquier herramienta que el usuario
conecte en esa categoría. Los plugins son agnósticos de herramienta — describen
flujos de trabajo en términos de categorías en lugar de productos específicos.

## Conectores para este plugin

| Categoría | Marcador | Opciones |
|-----------|----------|----------|
| Chat | `~~chat` | Slack, Microsoft Teams, Discord |
| Gestor de proyectos | `~~project tracker` | Linear, Asana, Jira |
```

### Variable ${CLAUDE_PLUGIN_ROOT}

Use `${CLAUDE_PLUGIN_ROOT}` para todas las referencias de rutas internas del plugin en hooks y configuraciones MCP. Nunca use rutas absolutas codificadas.

## Flujo de Trabajo Guiado

Cuando le pregunte algo al usuario, use AskUserQuestion. No asuma que los valores predeterminados "estándar de la industria" son correctos. Nota: AskUserQuestion siempre incluye un botón Saltar y un cuadro de entrada de texto libre para respuestas personalizadas, así que no incluya `Ninguno` u `Otro` como opciones.

### Fase 1: Descubrimiento

**Objetivo**: Entender qué quiere construir el usuario y por qué.

Pregunte (solo lo que no está claro — omita preguntas si la solicitud inicial del usuario ya las responde):

- ¿Qué debería hacer este plugin? ¿Qué problema resuelve?
- ¿Quién lo usará y en qué contexto?
- ¿Se integra con alguna herramienta o servicio externo?
- ¿Hay algún plugin o flujo de trabajo similar como referencia?

Resuma la comprensión y confirme antes de proceder.

**Salida**: Declaración clara del propósito y alcance del plugin.

### Fase 2: Planificación de Componentes

**Objetivo**: Determinar qué tipos de componentes necesita el plugin.

Basándose en las respuestas del descubrimiento, determine:

- **Habilidades** — ¿Necesita conocimiento especializado que Claude debe cargar bajo demanda? (experiencia en el dominio, esquemas de referencia, guías de flujo de trabajo)
- **Comandos** — ¿Hay acciones iniciadas por el usuario? (desplegar, configurar, analizar, revisar)
- **Servidores MCP** — ¿Necesita integración con servicios externos? (bases de datos, APIs, herramientas SaaS)
- **Agentes (poco común)** — ¿Hay tareas autónomas de múltiples pasos? (validación, generación, análisis)
- **Hooks (raro)** — ¿Debe ocurrir algo automáticamente en ciertos eventos? (aplicar políticas, cargar contexto, validar operaciones)

Presente una tabla de plan de componentes, incluyendo tipos de componentes que decidió no crear:

```
| Componente | Cantidad | Propósito |
|------------|----------|-----------|
| Habilidades | 1 | Conocimiento del dominio para X |
| Comandos | 2 | /hacer-cosa, /verificar-cosa |
| Agentes | 0 | No necesario |
| Hooks | 1 | Validar escrituras |
| MCP | 1 | Conectar al servicio Y |
```

Obtenga confirmación o ajustes del usuario antes de proceder.

**Salida**: Lista confirmada de componentes a crear.

### Fase 3: Diseño y Preguntas Clarificadoras

**Objetivo**: Especificar cada componente en detalle. Resolver todas las ambigüedades antes de la implementación.

Para cada tipo de componente en el plan, haga preguntas de diseño dirigidas. Presente las preguntas agrupadas por tipo de componente. Espere las respuestas antes de proceder.

**Habilidades:**
- ¿Qué consultas del usuario deberían activar esta habilidad?
- ¿Qué dominios de conocimiento cubre?
- ¿Debería incluir archivos de referencia para contenido detallado?

**Comandos:**
- ¿Qué argumentos acepta cada comando?
- ¿Qué herramientas necesita cada comando? (Read, Write, Bash, Grep, etc.)
- ¿Es cada comando interactivo o automatizado?

**Agentes:**
- ¿Debería cada agente activarse proactivamente o solo cuando se solicite?
- ¿Qué herramientas necesita?
- ¿Cuál debería ser el formato de salida?

**Hooks:**
- ¿Qué eventos? (PreToolUse, PostToolUse, Stop, SessionStart, etc.)
- ¿Qué comportamiento — validar, bloquear, modificar, añadir contexto?
- ¿Basado en prompt (impulsado por LLM) o basado en comando (script determinístico)?

**Servidores MCP:**
- ¿Qué tipo de servidor? (stdio para local, SSE para alojado con OAuth, HTTP para APIs REST)
- ¿Qué método de autenticación?
- ¿Qué herramientas deberían exponerse?

Si el usuario dice "lo que usted crea mejor," proporcione recomendaciones específicas y obtenga confirmación explícita.

**Salida**: Especificación detallada para cada componente.

### Fase 4: Implementación

**Objetivo**: Crear todos los archivos del plugin siguiendo las mejores prácticas.

**Orden de operaciones:**
1. Crear la estructura de directorios del plugin
2. Crear el manifiesto `plugin.json`
3. Crear cada componente (consulte `references/component-schemas.md` para formatos exactos)
4. Crear `README.md` documentando el plugin

**Guías de implementación:**

- Los **comandos** son instrucciones PARA Claude, no mensajes al usuario. Escríbalos como directivas sobre qué hacer.
- Las **habilidades** usan divulgación progresiva: cuerpo de SKILL.md conciso (menos de 3,000 palabras), contenido detallado en `references/`. La descripción del frontmatter debe ser en tercera persona con frases de activación específicas.
- Los **agentes** necesitan una descripción con bloques `<example>` mostrando condiciones de activación, más un prompt de sistema en el cuerpo markdown.
- La configuración de **hooks** va en `hooks/hooks.json`. Use `${CLAUDE_PLUGIN_ROOT}` para rutas de scripts. Prefiera hooks basados en prompt para lógica compleja.
- Las **configuraciones MCP** van en `.mcp.json` en la raíz del plugin. Use `${CLAUDE_PLUGIN_ROOT}` para rutas de servidores locales. Documente las variables de entorno requeridas en el README.

### Fase 5: Revisión y Empaquetado

**Objetivo**: Entregar el plugin terminado.

1. Resuma lo que se creó — liste cada componente y su propósito
2. Pregunte si el usuario quiere algún ajuste
3. Ejecute `claude plugin validate <ruta-a-plugin-json>`; corrija cualquier error y advertencia
4. Empaquete como archivo `.plugin`:

```bash
zip -r /tmp/nombre-del-plugin.plugin /ruta/al/directorio-del-plugin/. -x "*.DS_Store" && cp /tmp/nombre-del-plugin.plugin /ruta/a/outputs/nombre-del-plugin.plugin
```

> **Importante**: Siempre cree el zip en `/tmp/` primero, luego copie a la carpeta de salidas. Escribir directamente en la carpeta de salidas puede fallar por permisos.

> **Nomenclatura**: Use el nombre del plugin de `plugin.json` para el archivo `.plugin` (por ejemplo, si el nombre es `code-reviewer`, genere `code-reviewer.plugin`).

El archivo `.plugin` aparecerá en el chat como una vista previa enriquecida donde el usuario puede explorar los archivos y aceptar el plugin presionando un botón.

## Mejores Prácticas

- **Comience pequeño**: Empiece con el conjunto mínimo viable de componentes. Un plugin con una habilidad bien elaborada es más útil que uno con cinco componentes a medias.
- **Divulgación progresiva para habilidades**: Conocimiento central en SKILL.md, material de referencia detallado en `references/`, ejemplos funcionales en `examples/`.
- **Frases de activación claras**: Las descripciones de habilidades deben incluir frases específicas que los usuarios dirían. Las descripciones de agentes deben incluir bloques `<example>`.
- **Los comandos son para Claude**: Escriba el contenido del comando como instrucciones para que Claude las siga, no documentación para que el usuario lea.
- **Estilo de escritura imperativo**: Use instrucciones con verbo al inicio en las habilidades ("Parsee el archivo de configuración," no "Debería parsear el archivo de configuración").
- **Portabilidad**: Siempre use `${CLAUDE_PLUGIN_ROOT}` para rutas internas del plugin, nunca rutas codificadas.
- **Seguridad**: Use variables de entorno para credenciales, HTTPS para servidores remotos, acceso a herramientas con privilegio mínimo.

## Recursos Adicionales

- **`references/component-schemas.md`** — Especificaciones de formato detalladas para cada tipo de componente (comandos, habilidades, agentes, hooks, MCP, CONNECTORS.md)
- **`references/example-plugins.md`** — Tres estructuras completas de plugins de ejemplo en diferentes niveles de complejidad
