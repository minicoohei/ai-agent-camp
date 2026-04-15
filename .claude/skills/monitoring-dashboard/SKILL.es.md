---
name: monitoring-dashboard
description: "Usado para dashboards de marimo y visualización de progreso de proyectos. Se activa con solicitudes como 'crear un dashboard', 'visualizar progreso', 'mostrar resultados de pruebas', etc."
triggers:
  - crear un dashboard
  - visualizar progreso
  - mostrar resultados de pruebas
  - monitoring-dashboard
  - dashboard de progreso del proyecto
  - monitoreo
---

# Monitoring Dashboard - Dashboard de Monitoreo de Proyectos

Genera dashboards para visualizar el progreso del proyecto, resultados de pruebas y trazabilidad de requisitos usando marimo Run Mode.

## Flujo de Trabajo

1. Especificar la fuente de datos (JSON/CSV)
2. Seleccionar el diseño del dashboard (progreso/pruebas/integrado)
3. Auto-generar un notebook marimo (.py)
4. Lanzar con `marimo run` y verificar en el navegador

## Tipos de Dashboard

### 1. Dashboard de Progreso del Proyecto

Visualiza lo siguiente a partir de datos de progreso WBS:
- Tasa de completación de tareas (general/por fase)
- Gráfico burndown
- Carga de trabajo por responsable
- Alertas de tareas retrasadas

**Formato de datos:** `dummy-wbs-progress.json`
```json
{
  "tasks": [
    {
      "id": "WBS-001",
      "name": "Nombre de tarea",
      "phase": "Fase A",
      "assignee": "Responsable",
      "progress": 75,
      "start_date": "2025-01-01",
      "due_date": "2025-01-15",
      "status": "in_progress"
    }
  ]
}
```

### 2. Dashboard de Resultados de Pruebas

Visualiza lo siguiente a partir de resultados de ejecución de pruebas:
- Tasa de éxito/fallo/omisión por suite de pruebas
- Tendencia de cobertura de pruebas
- Lista de pruebas fallidas (por severidad)
- Análisis de tiempo de ejecución de pruebas

**Formato de datos:** `dummy-test-results.json`
```json
{
  "suites": [
    {
      "name": "Nombre de suite",
      "tests": [
        {
          "id": "TC-001",
          "name": "Nombre de prueba",
          "status": "passed",
          "duration_ms": 150,
          "severity": "high"
        }
      ]
    }
  ]
}
```

### 3. Dashboard de Trazabilidad de Requisitos

Seguimiento desde requisitos hasta diseño y pruebas:
- Matriz de cobertura de requisitos
- Resaltado de requisitos sin pruebas
- Distribución de estado de requisitos (gráfico circular)

## Estructura del Notebook marimo

```python
import marimo as mo
import pandas as pd
import plotly.express as px
import json

app = mo.App()

@app.cell
def load_data():
    """Cargar datos"""
    with open("path/to/data.json") as f:
        data = json.load(f)
    return pd.DataFrame(data["tasks"])

@app.cell
def progress_chart(df):
    """Gráfico de progreso"""
    fig = px.bar(df, x="name", y="progress", color="phase",
                 title="Tasa de Progreso de Tareas")
    mo.ui.plotly(fig)

@app.cell
def summary_metrics(df):
    """Métricas de resumen"""
    total = len(df)
    completed = len(df[df["progress"] == 100])
    mo.md(f"""
    ## Resumen del Proyecto
    - Total de tareas: **{total}**
    - Completadas: **{completed}**
    - Tasa de completación: **{completed/total*100:.1f}%**
    """)
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| data_source | Sí | - | Ruta al archivo de datos (JSON/CSV) |
| dashboard_type | No | integrated | Tipo de dashboard (progress/test/traceability/integrated) |
| output | No | output/pm/dashboard.py | Ruta del archivo de salida |
| title | No | Project Dashboard | Título del dashboard |

## Formato de Salida

Genera un notebook marimo (.py):
- `output/pm/dashboard.py` -- Lanzar con `marimo run output/pm/dashboard.py`

## Requisitos

- Python 3.10+
- marimo (`uv add marimo`)
- pandas (`uv add pandas`)
- plotly (`uv add plotly`)

## Ejemplo

```
Use el skill monitoring-dashboard para crear un dashboard integrado de proyecto a partir de datos de prueba.
Datos: Cualquier JSON o CSV de progreso
-> Se genera output/pm/dashboard.py -> Lanzar con marimo run
```
