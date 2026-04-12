---
description: "When the user says /start-8-3 — Module 8 Lesson 8-3: Analisis interactivo con Marimo Notebooks"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1", "start-8-2"]
duration: "~40 min"
level: "intermediate"
tags: ["data", "marimo", "dashboard", "visualization"]
---

# 🎓 Lesson 8-3: Analisis interactivo con Marimo Notebooks

## 📍 Lo que hara en esta sesion

**Lesson 8-3: Dashboard interactivo con Marimo** !

| Elemento | Contenido |
|------|------|
| Objetivo | Construir un dashboard reactivo para datos de BigQuery con Marimo |
| Duracion | ~40 min |
| Habilidades utilizadas | data-analyst, Marimo |
| Requisitos previos | Lesson 8-1 y 8-2 completadas, BigQuery conectado |
| Pagina del curso | [Module 8: Analisis de datos](https://ai-agent.camp/es/course/module-8) como referencia paralela |

**Flujo de la sesion:**
1. Configurar el entorno de Marimo
2. Cargar y visualizar datos de BigQuery
3. Actualizaciones dinamicas de filtros y graficos

Al final de esta sesion, podra crear cuadernos de analisis interactivos.

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

## 🚀 Step 1: Install and Launch Marimo

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Install and Launch Marimo",
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
Por favor, configure el entorno de Marimo.

1. Verifique si Marimo está instalado
2. También verifique los paquetes necesarios (altair, pandas)
3. Instale si no están instalados

Después de la instalación, muestre la versión para verificar el funcionamiento.
```

**Resultado esperado:** Marimo y los paquetes relacionados se instalan y se muestra la version.

---

## 🚀 Step 2: Create a New Marimo Notebook

Cree un notebook para el analisis de GA4:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Create a New Marimo Notebook",
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
Por favor, cree un cuaderno Marimo para análisis de datos GA4.

Archivo: ~/ai-agent-camp/notebooks/ga4_analysis_dashboard.py

Contenido de las celdas iniciales:
1. Importar bibliotecas (marimo, pandas, altair, bigquery)
2. Inicializar cliente BigQuery
3. Título y descripción del dashboard

También muestre cómo iniciar Marimo y abrirlo en el navegador.
```

**Resultado esperado:** Se crea el archivo del cuaderno y se proporciona el comando de inicio.

---

## 🚀 Step 3: Add Interactive UI Components

Agregue componentes de UI para filtrado:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Add Interactive UI Components",
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
Por favor, agregue filtros interactivos al cuaderno Marimo.

Componentes de interfaz a agregar:
1. Selección de rango de fechas (cuadros de texto de fecha de inicio y fin)
2. Menú desplegable de tipo de evento (ALL, view_item, add_to_cart, purchase)
3. Control deslizante de cantidad a mostrar (5-50 elementos)

Genere el código para cada componente.
```

**Resultado esperado:** Se genera codigo Marimo para cada componente de interfaz.

---

## 🚀 Step 4: Reactive Data Fetching

Cree celdas que obtengan datos segun los valores de los componentes de UI:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Reactive Data Fetching",
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
Por favor, cree una celda que use la función de caché de Marimo
para obtener datos GA4 del rango de fechas seleccionado.

Requisitos:
- Habilitar caché con el decorador @mo.cache
- Recibir rango de fechas (date_start, date_end) como parámetros
- Obtener cantidad de eventos diarios y usuarios únicos
- Devolver resultados como DataFrame

Genere el código.
```

**Resultado esperado:** Se genera una funcion de recuperacion de datos con cache.

---

## 🚀 Step 5: Create Charts with Altair

Agregue graficos para visualizar datos:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Create Charts with Altair",
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
Por favor, genere celdas Marimo que creen los siguientes gráficos con Altair.

1. Gráfico de líneas de eventos diarios
   - Eje X: Fecha
   - Eje Y: Cantidad de eventos
   - Tooltip: Fecha, cantidad de eventos, cantidad de usuarios

2. Gráfico de barras por tipo de evento
   - Eje X: Cantidad de eventos
   - Eje Y: Nombre del evento (descendente)
   - Color: Gradiente según el porcentaje

Envuelva cada gráfico con mo.ui.altair_chart().
```

**Resultado esperado:** Se genera codigo de grafico Altair interactivo.

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
      {"id": "trouble_1", "label": "Marimo won't start"},
      {"id": "trouble_2", "label": "Cells not updating (reactivity issue)"},
      {"id": "trouble_3", "label": "BigQuery query is slow"},
      {"id": "trouble_4", "label": "Charts not displaying"}
    ]
  }]
}
```


### Problema 1: "Marimo no se inicia"
**Causa:** La instalacion esta incompleta
**Prompt de solucion:**
```
Por favor, reinstale Marimo.
pip install --upgrade marimo

Después de la instalación, verifique con marimo --version.
```

### Problema 2: "Las celdas no se actualizan (problema de reactividad)"
**Causa:** Nombres de variables duplicados
**Prompt de solucion:**
```
Explique las reglas de nomenclatura de variables de Marimo.
Describa cómo usar diferentes sufijos por celda
(_fetch, _prep, _dyn, etc.).
```

### Problema 3: "La consulta de BigQuery es lenta"
**Causa:** El cache no esta funcionando
**Prompt de solucion:**
```
Muestre el uso correcto del decorador @mo.cache de Marimo.
También muestre cómo limpiar la caché.
```

### Problema 4: "Los graficos no se muestran"
**Causa:** Error de codificacion de Altair
**Prompt de solucion:**
```
Diagnostique el error donde los gráficos de Altair no se muestran.
Verifique si los tipos del DataFrame y la codificación del gráfico
son consistentes.
```

---

## ✅ Punto de control
- [ ] Marimo launched successfully
- [ ] BigQuery client initialized
- [ ] Date input field works
- [ ] Dropdown filter works
- [ ] Slider works
- [ ] Cache function (@mo.cache) works
- [ ] Altair charts update dynamically
- [ ] Verified that multiple cells update in coordination

---

## 📚 Important Marimo Features

### Variable Naming Rules
| Purpose | Suffix | Example |
|------|------|----|
| Data fetch | `_fetch` | `df_daily_fetch` |
| Preprocessing | `_prep` | `df_events_prep` |
| Dynamic filter | `_dyn` | `chart_events_dyn` |
| Statistical calc | `_calc` | `total_events_calc` |

### Commonly Used UI Components
```python
mo.ui.text(...)       # Entrada de texto
mo.ui.dropdown(...)   # Menú desplegable
mo.ui.slider(...)     # Control deslizante
mo.ui.table(...)      # Visualización de tabla
mo.ui.altair_chart()  # Visualización de gráfico
```


---

## 📋 Vista previa de entregables

Los entregables de esta leccion son salidas de terminal.

### Ejemplo de salida esperada
```
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

```
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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-8-4)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-8-4
- finish → Finalizar
