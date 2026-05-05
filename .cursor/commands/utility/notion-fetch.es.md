---
nonInteractiveMode: compliant
---

# Notion Fetch - Integración con Notion

Obtiene páginas y bases de datos de Notion y las exporta en formato Markdown.

## Funcionalidades

- Obtener y convertir páginas individuales a Markdown
- Salida de bases de datos en formato de tabla
- Búsqueda dentro de Notion
- Conversión de texto enriquecido (negrita, cursiva, código, etc.)
- Soporte para varios tipos de bloques (encabezados, listas, código, citas, etc.)

## Pasos de ejecución

### Paso 1: Extracción de parámetros

Extraiga lo siguiente de la entrada del usuario:
- **Comando**: page / database / search
- **ID/URL**: ID o URL de la página de Notion
- **Destino de salida**: Ruta del archivo (se muestra en pantalla si se omite)

### Paso 2: Ejecución de la herramienta

```bash
# Obtener una página
python src/notion_fetcher.py page <page_id_or_url>

# Obtener una base de datos
python src/notion_fetcher.py database <database_id_or_url>

# Buscar
python src/notion_fetcher.py search "palabra clave"
```

### Paso 3: Mostrar resultados

Presente el Markdown generado al usuario.

## Opciones

### Comando page

| Opción | Descripción |
|--------|-------------|
| `--output PATH` / `-o` | Ruta del archivo de salida |

### Comando database

| Opción | Descripción |
|--------|-------------|
| `--output PATH` / `-o` | Ruta del archivo de salida |
| `--include-content` / `-c` | Incluir el contenido de cada página |

### Comando search

| Opción | Descripción |
|--------|-------------|
| `--type TEXT` / `-t` | Filtro: page / database |

## Ejemplos de uso

### Obtener una página

```
/notion-fetch https://www.notion.so/myworkspace/Page-Name-abc123
```

### Obtener una base de datos

```
/notion-fetch database abc123def456 --output tasks.md
```

### Buscar

```
/notion-fetch search "plan del proyecto"
```

### Salida detallada de base de datos

```
/notion-fetch database abc123 --include-content
```

## Formato de salida

### Página

```markdown
---
id: abc123...
created: 2026-01-15T10:00:00.000Z
modified: 2026-01-16T14:30:00.000Z
title: Título de la página
url: https://www.notion.so/...
---

# Título de la página

## Sección 1

Texto del cuerpo...

- Elemento de lista 1
- Elemento de lista 2

> Texto citado

```python
bloque de código
```
```

### Base de datos

```markdown
---
id: def456...
type: database
title: Gestión de tareas
total_items: 25
---

# Gestión de tareas

| Nombre de tarea | Estado | Responsable | Fecha límite |
|-----------------|--------|-------------|--------------|
| Tarea A | En progreso | Tanaka | 2026-01-20 |
| Tarea B | Completada | Sato | 2026-01-18 |
```

## Requisitos previos

Es necesario configurar la variable de entorno `NOTION_API_KEY`.

### Pasos de configuración

1. Cree una integración en https://www.notion.so/my-integrations
2. Obtenga la clave API (comienza con `secret_`)
3. Conecte la integración a la página/base de datos de destino

Detalles:

```bash
uv run python tools/api_setup_wizard.py guide notion
```

## Tipos de bloques soportados

| Tipo | Estado de soporte |
|------|-------------------|
| paragraph | ✅ |
| heading_1/2/3 | ✅ |
| bulleted_list_item | ✅ |
| numbered_list_item | ✅ |
| to_do | ✅ |
| toggle | ✅ |
| code | ✅ |
| quote | ✅ |
| callout | ✅ |
| divider | ✅ |
| image | ✅ |
| bookmark | ✅ |
| child_page | ✅ (solo título) |
| child_database | ✅ (solo título) |
| table | ⚠️ (soporte básico) |

## Comandos relacionados

- `/api-setup-wizard` - Configuración de la API de Notion
- `/extract-tasks` - Extracción de tareas (integración con Notion planificada)
