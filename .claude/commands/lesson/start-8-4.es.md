---
description: "When the user says /start-8-4 — Module 8 Lesson 8-4: Visualizacion de datos y creacion de dashboards"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1", "start-8-2", "start-8-3"]
duration: "~35 min"
level: "intermediate"
tags: ["data", "visualization", "dashboard", "matplotlib"]
---

# 🎓 Lesson 8-4: Visualizacion de datos y creacion de dashboards

## 📍 Lo que hara en esta sesion

**Lesson 8-4: Visualizacion y dashboards** !

| Elemento | Contenido |
|------|------|
| Objetivo | Crear graficos con matplotlib/seaborn y construir dashboards |
| Duracion | ~35 min |
| Habilidades utilizadas | data-analyst, bibliotecas de visualizacion |
| Requisitos previos | Lesson 8-1 a 8-3 completadas, BigQuery conectado |
| Pagina del curso | [Module 8: Analisis de datos](https://ai-agent.camp/es/course/module-8) como referencia paralela |

**Flujo de la sesion:**
1. Crear diversos graficos
2. Combinar multiples graficos
3. Completar el dashboard y generar informes

Al final de esta sesion, podra crear informes de analisis y dashboards.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

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

## 🔧 Step 0: Environment Setup (Japanese Font Settings & Data Preparation)

To display Japanese correctly in charts, first configure the fonts. Add the following code at the beginning of your script:

```python
import matplotlib
import matplotlib.pyplot as plt

# Japanese font settings (auto-detect OS)
import platform
_system = platform.system()
if _system == "Darwin":
    matplotlib.rcParams['font.family'] = 'Hiragino Sans'
elif _system == "Windows":
    matplotlib.rcParams['font.family'] = 'MS Gothic'
else:
    matplotlib.rcParams['font.family'] = 'Noto Sans CJK JP'
```

### Fallback When BigQuery Connection Fails

Even if GCP authentication doesn't work, you can proceed with the lesson using sample data. Create a local DataFrame as follows:

```python
import pandas as pd

# Shakespeare-style sample data (no BigQuery required)
sample_data = pd.DataFrame({
    'corpus': ['hamlet', 'macbeth', 'othello', 'kinglear', 'tempest',
               'juliuscaesar', 'romeoand', 'midsummer', 'merchantof', 'twelfthnight'],
    'unique_words': [4828, 3896, 3885, 3766, 3309, 3032, 3000, 2930, 2892, 2780],
    'total_words': [32446, 18314, 27602, 27619, 17780, 20876, 25689, 17121, 22152, 20890]
})

# Time series sample data (GA4-style)
import numpy as np
dates = pd.date_range('2021-01-01', periods=10, freq='D')
sample_timeseries = pd.DataFrame({
    'date': dates,
    'event_count': np.random.randint(500, 2000, size=10)
})
```

> **💡 Hint**: If you already have a BigQuery connection, run queries directly. If you cannot connect, use the sample data above as an alternative.

---

## 🚀 Step 1: Create a Basic Bar Chart

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Create a Basic Bar Chart",
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
```text
Usando el conjunto de datos de Shakespeare de BigQuery,
visualice el número de palabras únicas por obra en un gráfico de barras horizontales.

Consulta:
SELECT corpus, COUNT(DISTINCT word) as unique_words
FROM bigquery-public-data.samples.shakespeare
GROUP BY corpus
ORDER BY unique_words DESC
LIMIT 10

Requisitos del gráfico:
- Gráfico de barras horizontales (barh)
- Título: "Palabras únicas por obra de Shakespeare"
- Etiqueta del eje X: "Número de palabras únicas"
- Guardar en alta resolución (dpi=150)

Salida: ~/ai-agent-camp/output/chart-4-4-bar.png
```

**Resultado esperado:** Se genera un grafico de barras horizontales y se guarda en archivo.

---

## 🚀 Step 2: Time Series Line Chart

Visualice las tendencias de series de tiempo:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Time Series Line Chart",
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
```text
Visualice el número de eventos diarios de GA4 en un gráfico de líneas.

Período: 2021-01-01 a 2021-01-10

Requisitos del gráfico:
- Gráfico de líneas + marcadores
- Eje X: Fecha
- Eje Y: Cantidad de eventos
- Agregar líneas de cuadrícula
- Título: "Tendencia de eventos diarios"
- Guardar en alta resolución (dpi=150)

Salida: ~/ai-agent-camp/output/chart-4-4-line.png
```

**Resultado esperado:** Se genera un grafico de lineas de series temporales.

---

## 🚀 Step 3: Distribution Histogram

Cree un histograma para verificar la distribucion de los datos:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Distribution Histogram",
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
```text
Visualice la distribución de frecuencia de palabras en el conjunto de datos de Shakespeare
como un histograma.

Condiciones:
- Palabras con frecuencia mayor que 0 y menor que 100
- Número de intervalos: 50

Requisitos del gráfico:
- Histograma
- Eje X: "Frecuencia de aparición de palabras"
- Eje Y: "Frecuencia"
- Título: "Distribución de frecuencia de palabras"
- Líneas de cuadrícula en el eje vertical
- Guardar en alta resolución (dpi=150)

Salida: ~/ai-agent-camp/output/chart-4-4-hist.png
```

**Resultado esperado:** Se genera un histograma que muestra la distribucion de ocurrencias.

---

## 🚀 Step 4: Scatter Plot and Correlation Analysis

Visualice la relacion entre 2 variables con un diagrama de dispersion:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Scatter Plot and Correlation Analysis",
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
```text
Visualice la relación entre "Palabras únicas" y "Total de palabras"
de las obras de Shakespeare en un diagrama de dispersión.

Requisitos del gráfico:
- Diagrama de dispersión
- Eje X: Número de palabras únicas
- Eje Y: Total de palabras
- Agregar etiquetas con el nombre de la obra en cada punto
- Líneas de cuadrícula
- Guardar en alta resolución (dpi=150)

Salida: ~/ai-agent-camp/output/chart-4-4-scatter.png
```

**Resultado esperado:** Se genera un diagrama de dispersion que muestra las correlaciones.

---

## 🚀 Step 5: Create a Dashboard

Combine multiples graficos en una sola imagen:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Create a Dashboard",
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
```text
Combine los gráficos creados en el Módulo 8
en un dashboard de 4 paneles.

Disposición:
┌────────────────┬────────────────┐
│  Barras        │  Líneas        │
│ (Categorías)   │ (Series temp.) │
├────────────────┼────────────────┤
│  Dispersión    │  Histograma    │
│ (Correlación)  │ (Distribución) │
└────────────────┴────────────────┘

Tamaño: 16x12 pulgadas
Título general: "Dashboard de análisis de datos GA4 y Shakespeare"
Guardar en alta resolución (dpi=150)

Salida: ~/ai-agent-camp/output/dashboard-4-4.png
```

**Resultado esperado:** Se genera una imagen del dashboard con 4 graficos.

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
      {"id": "trouble_1", "label": "Charts not displaying"},
      {"id": "trouble_2", "label": "Japanese characters are garbled"},
      {"id": "trouble_3", "label": "Memory error occurs"},
      {"id": "trouble_4", "label": "Chart appearance is poor"}
    ]
  }]
}
```


### Problema 1: "Los graficos no se muestran"
**Causa:** Configuracion del backend de matplotlib
**Prompt de solucion:**
```text
Verifique el backend de matplotlib.
Muestre cómo cambiar al backend 'Agg' para guardar archivos.
```

### Problema 2: "Los caracteres japoneses se muestran incorrectamente"
**Causa:** La fuente japonesa no esta configurada
**Prompt de solucion:**
```text
Muestre cómo configurar fuentes para mostrar
japonés correctamente en matplotlib.
Proporcione la configuración para macOS.
```

### Problema 3: "Ocurre un error de memoria"
**Causa:** El volumen de datos es demasiado grande
**Prompt de solucion:**
```text
Muestre cómo optimizar la memoria al graficar grandes cantidades de datos.
Explique los enfoques usando muestreo y agregación.
```

### Problema 4: "Los graficos no tienen buena apariencia"
**Causa:** Configuracion de estilo predeterminada
**Prompt de solucion:**
```text
Muestre cómo mejorar el estilo de los gráficos con seaborn.
Proporcione configuraciones de estilo legibles para presentaciones.
```

---

## ✅ Punto de control
- [ ] Created basic bar chart
- [ ] Expressed time series data as line chart
- [ ] Visualized distribution with histogram
- [ ] Analyzed 2-variable relationship with scatter plot
- [ ] Combined multiple charts into dashboard
- [ ] Saved at high resolution (dpi=150+)

---

## 🛠️ Troubleshooting

- Los graficos no se muestran
- Las fuentes japonesas estan rotas
- Ocurre un error de memoria

### Charts Not Displaying
Check the matplotlib backend and switch to `Agg` for saving if needed.

### Japanese Font Rendering Issues
Add Japanese font settings and adjust font name priority.

### Memory Error Occurs
Sample the data or pre-aggregate before visualization.

### Choosing Between seaborn and matplotlib
- **matplotlib**: Best for fine-grained customization or placing multiple charts in dashboards using `subplot`
- **seaborn**: Best for creating statistical visualizations (heatmaps, pair plots, box plots, etc.) cleanly with less code. Use `sns.set_theme(style='whitegrid')` to improve appearance globally
- You can combine both. A common pattern is to draw with seaborn and adjust axis labels and titles with matplotlib

---

## 📚 How to Choose Chart Types

| Chart Type | Use Case | Example |
|-------------|------|-----|
| Bar chart | Comparison between categories | Sales by country, headcount by dept |
| Line chart | Time series trends | Daily sales trends |
| Scatter plot | 2-variable relationship | Price vs. sales volume |
| Histogram | Distribution check | Age distribution |
| Pie chart | Composition ratio | Market share |
| Heatmap | 2D data density | Correlation matrix |

---

## 🎉 Module 8 Complete!

Congratulations! You have acquired the following skills:
- BigQuery connection and authentication
- Running exploratory data analysis (EDA)
- Interactive analysis with Marimo
- Creating various chart types
- Building dashboards


---

## 📋 Vista previa de entregables

Los entregables de esta leccion son salidas de terminal.

### Ejemplo de salida esperada
```text
┌─────────────────────────────────────┐
│  Resultado de la ejecución               │
│  Estado: ✅ Éxito                        │
│  Registros procesados: N                 │
└─────────────────────────────────────┘
```

> 💡 Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```text
# Verificación de finalización: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado:** Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-9-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-9-1
- finish → Finalizar
