---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-18"]
level: "intermediate"
tags: ["pm", "dashboard", "marimo", "monitoring"]
---

# 🎓 Lesson 18-19: Panel de control marimo

| Elemento | Detalles |
|------|------|
| Objetivo | Crear un panel integrado para el proyecto TaskFlow usando marimo Run Mode (con datos ficticios) |
| Duración | ~30 min |
| Habilidades utilizadas | habilidades monitoring-dashboard, data-analyst |
| Requisitos previos | Lesson 18-18 completada |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 📍 Paso 1: Verificación del entorno marimo

marimo es un entorno de notebook reactivo construido sobre Python. A diferencia de Jupyter, las celdas rastrean automáticamente las dependencias y recalculan los cambios. En esta lección, construirá un panel de control integrado del proyecto usando marimo.

```json
{
  "type": "AskQuestion",
  "question": "Tiene experiencia con marimo?",
  "options": [
    "Primera vez usandolo",
    "Tengo experiencia con Jupyter",
    "Tengo experiencia con marimo",
    "Solo ayudeme con la configuracion"
  ],
  "multiple": false
}
```

### Configuración de marimo

Según su selección, prepare el entorno con los siguientes comandos:

```bash
# Verificar Python 3.10 o superior
python3 --version    # En Windows: python --version

# Instalar marimo
pip install marimo pandas plotly numpy

# Verificar instalacion
marimo --version
```

**Tutorial rápido para usuarios nuevos:**
- Las celdas de marimo son campos de texto que contienen código Python
- Los cambios de variables dentro de una celda actualizan automáticamente otras celdas dependientes
- Modo `marimo run`: Solo lectura (para distribución del panel de control)
- Modo `marimo edit`: Edición interactiva (para desarrollo)

Opcionalmente, ejecute el tutorial oficial con el comando `marimo tutorial`.

## 📍 Paso 2: Carga de datos ficticios

Verifique los datos de prueba del proyecto TaskFlow y prepare los datos para mostrar en el panel de control.

```json
{
  "type": "AskQuestion",
  "question": "Que datos desea utilizar?",
  "options": [
    "Datos de progreso WBS",
    "Datos de resultados de pruebas",
    "Ambos",
    "Agregar datos personalizados tambien"
  ],
  "multiple": false
}
```

### Verificación de archivos de datos

Utilice los siguientes datos de prueba para el panel de control (estructura de datos integrada en la lección):

Estructura de **dummy-wbs-progress.json**:
```json
{
  "project_id": "taskflow-v1",
  "phases": [
    {
      "phase_name": "Planificaci\u00f3n",
      "start_date": "2024-01-01",
      "planned_end": "2024-02-28",
      "actual_end": "2024-02-25",
      "status": "completed",
      "completion_rate": 100,
      "tasks": 5,
      "completed_tasks": 5
    }
  ],
  "current_phase": "Implementaci\u00f3n",
  "overall_progress": 65,
  "requirements": [
    {"req_id": "REQ-001", "title": "Autenticaci\u00f3n de usuario", "status": "Completado", "test_cases": 12},
    {"req_id": "REQ-002", "title": "CRUD de tareas", "status": "Completado", "test_cases": 20},
    {"req_id": "REQ-003", "title": "Notificaciones", "status": "Completado", "test_cases": 8},
    {"req_id": "REQ-004", "title": "B\u00fasqueda/Filtro", "status": "En progreso", "test_cases": 5},
    {"req_id": "REQ-005", "title": "Visualizaci\u00f3n del panel", "status": "En progreso", "test_cases": 3},
    {"req_id": "REQ-006", "title": "Exportaci\u00f3n de reportes", "status": "En espera", "test_cases": 0},
    {"req_id": "REQ-007", "title": "Integraci\u00f3n con API externa", "status": "Rechazado", "test_cases": 0}
  ]
}
```

Estructura de **dummy-test-results.json**:
```json
{
  "test_execution_date": "2024-07-15",
  "test_suites": [
    {
      "suite_name": "Prueba de autenticaci\u00f3n de usuario",
      "total_cases": 12,
      "passed": 11,
      "failed": 1,
      "skipped": 0,
      "success_rate": 91.67
    }
  ],
  "overall_pass_rate": 87.5,
  "failed_tests": [
    {
      "test_id": "TC-AUTH-007",
      "name": "Restablecimiento de contrase\u00f1a - Manejo de token inv\u00e1lido",
      "error": "Expected status 400, got 500"
    }
  ]
}
```

### Ejemplo de código de carga de datos

Defina y utilice datos de prueba directamente dentro del panel de control (consulte la estructura JSON anterior).

```python
import json
import pandas as pd

# Definir datos ficticios directamente (usando la estructura anterior)
wbs_data = {
    "project_id": "taskflow-v1",
    "phases": [
        {"phase_name": "Planificaci\u00f3n", "start_date": "2024-01-01", "planned_end": "2024-02-28",
         "actual_end": "2024-02-25", "status": "completed", "completion_rate": 100,
         "tasks": 5, "completed_tasks": 5},
        # ... Definir otras fases de manera similar
    ],
    "current_phase": "Implementaci\u00f3n",
    "overall_progress": 65,
    "requirements": [
        {"req_id": "REQ-001", "title": "Autenticaci\u00f3n de usuario", "status": "Completado", "test_cases": 12},
        {"req_id": "REQ-002", "title": "CRUD de tareas", "status": "Completado", "test_cases": 20},
        {"req_id": "REQ-003", "title": "Notificaciones", "status": "Completado", "test_cases": 8},
        {"req_id": "REQ-004", "title": "B\u00fasqueda/Filtro", "status": "En progreso", "test_cases": 5},
        {"req_id": "REQ-005", "title": "Visualizaci\u00f3n del panel", "status": "En progreso", "test_cases": 3},
        {"req_id": "REQ-006", "title": "Exportaci\u00f3n de reportes", "status": "En espera", "test_cases": 0},
        {"req_id": "REQ-007", "title": "Integraci\u00f3n con API externa", "status": "Rechazado", "test_cases": 0}
    ]
}

test_data = {
    "test_execution_date": "2024-07-15",
    "test_suites": [
        {"suite_name": "Prueba de autenticaci\u00f3n de usuario", "total_cases": 12, "passed": 11,
         "failed": 1, "skipped": 0, "success_rate": 91.67},
        # ... Definir otras suites de manera similar
    ],
    "overall_pass_rate": 87.5,
    "failed_tests": [
        {"test_id": "TC-AUTH-007", "name": "Restablecimiento de contrase\u00f1a - Manejo de token inv\u00e1lido",
         "error": "Expected status 400, got 500"}
    ]
}

# Conversi\u00f3n a DataFrame
phases_df = pd.DataFrame(wbs_data["phases"])
test_suites_df = pd.DataFrame(test_data["test_suites"])

print("WBS Progress Data:")
print(phases_df.head())
print("\nTest Results Data:")
print(test_suites_df.head())
```

## 📍 Paso 3: Configuración de panel de 3 paneles

Muestre las métricas clave del proyecto TaskFlow en 3 paneles. Cada panel visualiza un aspecto diferente de la gestión del proyecto.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el diseno del panel de control",
  "options": [
    "3 paneles lado a lado",
    "Cambio de pestanas",
    "Tipo desplazamiento",
    "Dejar que la IA sugiera el diseno optimo"
  ],
  "multiple": false
}
```

### Panel 1: Progreso del proyecto

Mostrar el progreso general del proyecto desde multiples perspectivas:

**Contenido a mostrar:**
- Barra de progreso general (actualmente 65%)
- Tabla de progreso por fase (Planificación 100%, Diseño 92%, Implementación 65%, Pruebas 20%)
- Gráfico de tendencia de progreso (tasas de progreso semanales)
- Alerta de retraso (fase de implementación es -3 dias vs. cronograma)

**Ejemplo de código Plotly:**
```python
import plotly.graph_objects as go
import plotly.express as px

# Barra de progreso por fase
fig_phase = go.Figure(data=[
    go.Bar(y=['Planificaci\u00f3n', 'Dise\u00f1o', 'Implementaci\u00f3n', 'Pruebas', 'Operaciones'],
           x=[100, 92, 65, 20, 0],
           orientation='h',
           marker=dict(color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6']))
])
fig_phase.update_layout(title="Progreso por fase",
                        xaxis_title="Tasa de progreso (%)",
                        height=300)

# Medidor de progreso general
fig_gauge = go.Figure(data=[
    go.Indicator(mode="gauge+number",
                 value=65,
                 title={'text': "Progreso general"},
                 domain={'x': [0, 1], 'y': [0, 1]},
                 gauge={'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffcccc"},
                            {'range': [50, 80], 'color': "#ffffcc"},
                            {'range': [80, 100], 'color': "#ccffcc"}]})
])
```

### Panel 2: Resultados de pruebas

Resultados de ejecución de pruebas y métricas de calidad:

**Contenido a mostrar:**
- Gráfico circular de tasa de éxito general de pruebas (87.5%)
- Lista de resultados por suite de pruebas (tasa de éxito, cantidad de pruebas)
- Lista de pruebas fallidas (ID de prueba, razon de fallo, severidad)
- Tendencia de calidad (tendencia de tasa de éxito en las últimas 4 semanas)

**Ejemplo de código Plotly:**
```python
# Gr\u00e1fico circular de tasa de \u00e9xito de pruebas
success_rate = test_data["overall_pass_rate"]
failure_rate = 100 - success_rate

fig_pie = go.Figure(data=[
    go.Pie(labels=['\u00c9xito', 'Fallo'],
           values=[success_rate, failure_rate],
           marker=dict(colors=['#2ecc71', '#e74c3c']),
           hole=0.3)
])
fig_pie.update_layout(title="Tasa de \u00e9xito general de pruebas")

# Barra por suite de pruebas
fig_suites = px.bar(test_suites_df,
                    x='suite_name',
                    y='success_rate',
                    color='success_rate',
                    color_continuous_scale='RdYlGn',
                    range_color=[70, 100],
                    title="Tasa de \u00e9xito por suite de pruebas")

# Tabla de pruebas fallidas
failed_df = pd.DataFrame(test_data["failed_tests"])
```

### Panel 3: Rastreador de requisitos

Cobertura de requisitos y seguimiento de estado:

**Contenido a mostrar:**
- Distribución de estado de requisitos (implementado, en progreso, en espera, rechazado)
- Tasa de cobertura de pruebas (92% de todos los requisitos implementados y probados)
- Mapeo de pruebas por requisito (número de casos de prueba vinculados a cada requisito)
- Indicadores de requisitos de alto riesgo (requisitos con 0 casos de prueba)

**Ejemplo de código Plotly:**
```python
# Distribuci\u00f3n de estado de requisitos
status_counts = {
    'Implementado': 42,
    'En progreso': 8,
    'En espera': 2,
    'Rechazado': 1
}

fig_status = go.Figure(data=[
    go.Bar(x=list(status_counts.keys()),
           y=list(status_counts.values()),
           marker=dict(color=['#2ecc71', '#f39c12', '#3498db', '#95a5a6']))
])
fig_status.update_layout(title="Distribuci\u00f3n de estado de requisitos",
                        yaxis_title="N\u00famero de requisitos")

# Tasa de cobertura de pruebas
coverage = 92
fig_coverage = go.Figure(data=[
    go.Indicator(mode="gauge+number+delta",
                 value=coverage,
                 title={'text': "Cobertura de pruebas"},
                 gauge={'axis': {'range': [0, 100]},
                        'threshold': {'line': {'color': "red"}, 'thickness': 4, 'value': 80}})
])
```

## 📍 Paso 4: Iniciar y verificar con marimo run

Ejecute el panel de control completado en marimo y verifique que todos los paneles se rendericen correctamente.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el metodo de inicio",
  "options": [
    "marimo run (solo lectura)",
    "marimo edit (modo de edicion)",
    "Verificar con capturas de pantalla"
  ],
  "multiple": false
}
```

### Estructura del archivo Python del panel de control

Crear con la siguiente estructura como `output/pm/dashboard.py`:

```python
import marimo as mo
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

app = mo.App()

# ============= Celda 1: Entorno y dependencias =============
@app.cell
def environment():
    import sys
    print(f"Python {sys.version}")
    print(f"marimo version: {mo.__version__}")
    return

# ============= Celda 2: Definici\u00f3n de datos =============
@app.cell
def load_data():
    # Definir datos ficticios directamente
    wbs_data = {
        "project_id": "taskflow-v1",
        "phases": [
            {"phase_name": "Planificaci\u00f3n", "start_date": "2024-01-01", "planned_end": "2024-02-28",
             "actual_end": "2024-02-25", "status": "completed", "completion_rate": 100,
             "tasks": 5, "completed_tasks": 5},
            {"phase_name": "Dise\u00f1o", "start_date": "2024-03-01", "planned_end": "2024-04-30",
             "actual_end": "2024-04-28", "status": "completed", "completion_rate": 92,
             "tasks": 8, "completed_tasks": 7},
            {"phase_name": "Implementaci\u00f3n", "start_date": "2024-05-01", "planned_end": "2024-07-31",
             "actual_end": None, "status": "in_progress", "completion_rate": 65,
             "tasks": 12, "completed_tasks": 8},
            {"phase_name": "Pruebas", "start_date": "2024-08-01", "planned_end": "2024-09-15",
             "actual_end": None, "status": "planned", "completion_rate": 20,
             "tasks": 6, "completed_tasks": 1},
            {"phase_name": "Operaciones", "start_date": "2024-09-16", "planned_end": "2024-10-31",
             "actual_end": None, "status": "planned", "completion_rate": 0,
             "tasks": 4, "completed_tasks": 0}
        ],
        "current_phase": "Implementaci\u00f3n",
        "overall_progress": 65,
        "requirements": [
            {"req_id": "REQ-001", "title": "Autenticaci\u00f3n de usuario", "status": "Completado", "test_cases": 12},
            {"req_id": "REQ-002", "title": "CRUD de tareas", "status": "Completado", "test_cases": 20},
            {"req_id": "REQ-003", "title": "Notificaciones", "status": "Completado", "test_cases": 8},
            {"req_id": "REQ-004", "title": "B\u00fasqueda/Filtro", "status": "En progreso", "test_cases": 5},
            {"req_id": "REQ-005", "title": "Visualizaci\u00f3n del panel", "status": "En progreso", "test_cases": 3},
            {"req_id": "REQ-006", "title": "Exportaci\u00f3n de reportes", "status": "En espera", "test_cases": 0},
            {"req_id": "REQ-007", "title": "Integraci\u00f3n con API externa", "status": "Rechazado", "test_cases": 0}
        ]
    }

    test_data = {
        "test_execution_date": "2024-07-15",
        "test_suites": [
            {"suite_name": "Prueba de autenticaci\u00f3n de usuario", "total_cases": 12, "passed": 11,
             "failed": 1, "skipped": 0, "success_rate": 91.67},
            {"suite_name": "Prueba de gesti\u00f3n de tareas", "total_cases": 20, "passed": 17,
             "failed": 2, "skipped": 1, "success_rate": 85.0},
            {"suite_name": "Prueba de notificaciones", "total_cases": 8, "passed": 7,
             "failed": 1, "skipped": 0, "success_rate": 87.5}
        ],
        "overall_pass_rate": 87.5,
        "failed_tests": [
            {"test_id": "TC-AUTH-007", "name": "Restablecimiento de contrase\u00f1a - Manejo de token inv\u00e1lido",
             "error": "Expected status 400, got 500"}
        ]
    }

    phases_df = pd.DataFrame(wbs_data["phases"])
    test_suites_df = pd.DataFrame(test_data["test_suites"])

    return wbs_data, test_data, phases_df, test_suites_df

# ============= Celda 3: Panel 1 - Progreso del proyecto =============
@app.cell
def panel_progress(wbs_data):
    mo.md(f"""
    # 📊 Panel 1: Progreso del proyecto

    **Progreso general: {wbs_data['overall_progress']}%**

    Fase actual: {wbs_data['current_phase']}
    """)

# ============= Celda 4: Panel 2 - Resultados de pruebas =============
@app.cell
def panel_tests(test_data):
    mo.md(f"""
    # ✅ Panel 2: Resultados de pruebas

    **Tasa de \u00e9xito general: {test_data['overall_pass_rate']}%**

    Pruebas fallidas: {len(test_data['failed_tests'])}
    """)

# ============= Celda 5: Panel 3 - Rastreador de requisitos =============
@app.cell
def panel_requirements(wbs_data):
    total = len(wbs_data.get("requirements", []))
    done = sum(1 for r in wbs_data.get("requirements", []) if r.get("status") == "Completado")
    in_progress = sum(1 for r in wbs_data.get("requirements", []) if r.get("status") == "En progreso")
    coverage = round(done / total * 100) if total > 0 else 0
    mo.md(f"""
    # 📋 Panel 3: Rastreador de requisitos

    **Cobertura de pruebas: {coverage}%**

    Requisitos implementados: {done}
    Requisitos en progreso: {in_progress}
    """)

# ============= Celda 6: Integraci\u00f3n del panel de control =============
@app.cell
def dashboard(wbs_data):
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    mo.md(f"""
    # 🎯 Panel de control integrado del proyecto TaskFlow

    Cada panel (Panel 1-3) se muestra individualmente en las celdas anteriores.

    ---

    **\u00daltima actualizaci\u00f3n**: {now}

    **Fuente de datos**: Datos ficticios (samples/)
    """)

if __name__ == "__main__":
    app.run()
```

### Comandos de ejecución

```bash
# Iniciar en modo solo lectura (para distribuci\u00f3n del panel de control)
marimo run output/pm/dashboard.py

# O iniciar en modo de edici\u00f3n (para desarrollo y ajustes)
marimo edit output/pm/dashboard.py
```

### Lista de verificación

```json
{
  "type": "AskQuestion",
  "question": "Se inicio el panel de control correctamente?",
  "options": [
    "Exito - Todos los paneles se muestran",
    "Error parcial - Se necesitan correcciones",
    "Inicio fallido - Se necesita soporte de depuracion",
    "La verificacion por captura de pantalla es suficiente"
  ],
  "multiple": false
}
```

**Visualización esperada:**
- Panel 1 (Progreso del proyecto): Barras por fase, medidor de progreso general
- Panel 2 (Resultados de pruebas): Gráfico circular de tasa de éxito, lista de pruebas fallidas
- Panel 3 (Rastreador de requisitos): Distribución de estado, tasa de cobertura

Si todo se muestra correctamente, esta lección esta completa.

---

## ✅ Entregables

- `output/pm/dashboard.py` - Panel de control integrado en formato de notebook marimo

## 🚀 Solución de problemas

| Problema | Solución |
|------|--------|
| No se puede instalar marimo | Verifique Python 3.10+. Reintente después de `pip install --upgrade pip` |
| Faltan datos | Consulte la estructura de datos de prueba integrada en la lección para complementar las definiciones |
| Los gráficos Plotly no se muestran | Instale la versión más reciente con `pip install plotly` |
| marimo run no se inicia | Verifique errores de sintaxis con `marimo edit` |


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── presentation.md  (materiales de presentacion)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/presentation.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/presentation.md
```

> 💡 Texto completo: Ejecute `cat output/pm/presentation.md` para mostrar el texto completo

## ➡️ Siguientes pasos

→ [Lesson 18-20: Ejercicio integral (Capstone)](start-18-20.md)
