---
nonInteractiveMode: compliant
---

# Extract Tasks - Extracción de tareas

Extraiga tareas de múltiples fuentes de datos y lístelas con clasificación de prioridad.

## Fuentes de datos

1. **Git** - Información de los últimos commits, ejecutar git pull
2. **Activity Logger** - Resumen del registro de trabajo reciente
3. **SpecStory** - Tareas en progreso (con TODOs pendientes)
4. **Slack-sync** - Solicitudes de cada espacio de trabajo
5. **Output** - Calendario, Gmail, notas de voz
6. **Notion** - Base de datos de tareas (cuando NOTION_API_KEY está configurada)

## Pasos

### Paso 1: Extraer parámetros

Extraiga lo siguiente de la entrada del usuario:
- **Días**: Número de días para el alcance de SpecStory (predeterminado: 3)
- **Espacio de trabajo**: Objetivo de Slack (predeterminado: all)
- **git pull**: Si se ejecuta o no (predeterminado: sí)

### Paso 2: Ejecutar la herramienta

```bash
uv run python tools/extract_tasks.py --days {días} --workspaces {espacio_de_trabajo}
```

### Paso 3: Mostrar resultados

Presente el Markdown de salida al usuario.

## Opciones

| Opción | Descripción | Predeterminado |
|--------|-------------|----------------|
| `--days INT` | Número de días para el alcance de SpecStory | 3 |
| `--workspaces TEXT` | Objetivos de Slack (separados por comas) | all |
| `--output PATH` | Ruta del archivo de salida | stdout |
| `--format TEXT` | Formato de salida: markdown / json / html | markdown |
| `--git-pull` | Ejecutar git pull | True |
| `--no-git-pull` | Omitir git pull | - |
| `--notion-db TEXT` | ID de base de datos de Notion | Variable de entorno |
| `--no-notion` | Omitir obtención de Notion | - |
| `--howtodo` | Generar procedimientos HowToDo | - |

## Ejemplos de uso

### Ejecución básica

```
/extract-tasks
```

Se ejecuta con la configuración predeterminada (3 días, todos los espacios de trabajo).

### Especificar número de días

```
/extract-tasks 7 días
```

Se ejecuta con `--days 7`.

### Solo espacios de trabajo específicos

```
/extract-tasks solo workspace-1 y workspace-2
```

Se ejecuta con `--workspaces workspace-1,workspace-2`.

### Sin git pull

```
/extract-tasks sin git pull
```

Se ejecuta con `--no-git-pull`.

### Salida en formato JSON

```
/extract-tasks en formato json
```

Se ejecuta con `--format json`.

## Formato de salida

### Prioridad A: Tareas en progreso
- Sesiones de SpecStory con TODOs pendientes

### Prioridad B: Solicitudes de Slack
- Mensajes recientes de cada espacio de trabajo
- Los mensajes con menciones se muestran con mayor prioridad

### Prioridad C: Tareas recurrentes
- Eventos del calendario de hoy
- Correos electrónicos recientes
- Notas de voz

## Notas

- git pull se ejecuta automáticamente a menos que se especifique `--no-git-pull`
- Activity Logger muestra los últimos 2 días
- Cuando hay una gran cantidad de datos, los resultados se limitan a aproximadamente los 5 principales
