---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module08-data-analysis"
prerequisites: ["start-8-1"]
duration: "~30 min"
level: "intermediate"
tags: ["data", "bigquery", "eda", "analysis"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 8-2: Ejecucion de EDA (Analisis exploratorio de datos)

## 📍 Lo que hara en esta sesion

**Lesson 8-2: EDA con BigQuery** !

| Elemento | Contenido |
|------|------|
| Objetivo | Realizar EDA en datos de muestra de GA4 para comprender estadisticas basicas, valores faltantes y distribuciones |
| Duracion | ~30 min |
| Habilidades utilizadas | data-analyst, BigQuery |
| Requisitos previos | Lesson 8-1 completada, BigQuery conectado |
| Pagina del curso | [Module 8: Analisis de datos](https://ai-agent.camp/es/course/module-8) como referencia paralela |

**Flujo de la sesion:**
1. Comprender la vision general del conjunto de datos
2. Verificar estadisticas basicas y valores faltantes
3. Visualizar distribuciones

Al final de esta sesion, podra explorar datos de BigQuery.

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

## 🚀 Step 1: Verify Table Schema

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verify Table Schema",
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
Por favor, verifique la estructura de la tabla GA4 en el conjunto de datos público de BigQuery.

Tabla: bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_20210101

Información a mostrar:
- Número de filas en la tabla
- Número de columnas
- Nombre, tipo de dato y descripción de cada columna

Explique en detalle las columnas principales (event_timestamp, event_name, user_pseudo_id,
geo.country, device.browser, ecommerce).
```

**Resultado esperado:** La informacion del esquema de la tabla se organiza y muestra.

---

## 🚀 Step 2: Calculate Basic Statistics

Calcule las estadisticas basicas de los datos:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Calculate Basic Statistics",
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
Por favor, calcule las estadísticas básicas de los datos de muestra de GA4.

Período: 2021-01-01 a 2021-01-03

Estadísticas a calcular:
- Número total de eventos
- Número de usuarios únicos
- Número de sesiones
- Eventos más comunes
- Marcas de tiempo del primer y último evento

Por favor, muestre los resultados de forma clara.
```

**Resultado esperado:** Las estadisticas basicas se muestran en formato de tabla.

---

## 🚀 Step 3: Check Missing Values

Verifique los valores faltantes para comprobar la calidad de los datos:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Check Missing Values",
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
Por favor, verifique los valores faltantes en los datos de GA4.

Fecha objetivo: 2021-01-01

Columnas a verificar:
- user_pseudo_id
- event_name
- geo.country
- device.browser
- ecommerce.purchase_revenue

Calcule el número y la tasa de valores faltantes por columna,
y proporcione observaciones sobre la calidad de los datos.
```

**Resultado esperado:** Se muestra la tasa de valores faltantes por columna y las consideraciones de calidad de datos.

---

## 🚀 Step 4: Check Categorical Data Distribution

Verifique la distribucion de eventos y regiones:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Check Categorical Data Distribution",
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
Por favor, analice la distribución de variables categóricas en los datos de GA4.

1. Distribución de tipos de evento (TOP 15)
   - Nombre del evento, cantidad, usuarios únicos, porcentaje

2. Distribución de usuarios por país (TOP 10)
   - Nombre del país, cantidad de eventos, usuarios únicos, ingreso promedio

3. Uso por tipo de navegador (TOP 10)
   - Nombre del navegador, cantidad de eventos, porcentaje

Muestre cada resultado de análisis en formato de tabla.
```

**Resultado esperado:** La distribucion de cada categoria se muestra en una tabla organizada.

---

## 🚀 Step 5: Time Series Analysis

Analice las tendencias diarias y por hora:

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Time Series Analysis",
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
Por favor, realice un análisis de series temporales de los datos de GA4.

Período: 2021-01-01 a 2021-01-10

Contenido del análisis:
1. Agregación diaria
   - Fecha, total de eventos, usuarios únicos, sesiones, ingresos

2. Tendencias por franja horaria
   - Cantidad de eventos y usuarios por franja horaria (0-23h)

Muestre los resultados y proporcione observaciones sobre las tendencias.
```

**Resultado esperado:** Se muestran los datos de series temporales y el analisis de tendencias.

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
      {"id": "trouble_1", "label": "Query times out"},
      {"id": "trouble_2", "label": "Quota exceeded error"},
      {"id": "trouble_3", "label": "Don't know how to handle NULL"},
      {"id": "trouble_4", "label": "Cannot access nested columns"}
    ]
  }]
}
```


### Problema 1: "La consulta agota el tiempo de espera"
**Causa:** El volumen de datos es demasiado grande
**Prompt de solucion:**
```text
Por favor, mejore el rendimiento de la consulta.
Considere los siguientes métodos:
- Reducir el rango de fechas
- Agregar una cláusula LIMIT
- Usar muestreo
```

### Problema 2: "Error de cuota excedida"
**Causa:** Se ha excedido la cuota de BigQuery
**Prompt de solucion:**
```text
Se produjo un error de cuota de BigQuery.
Muestre cómo reducir los costos de consulta.
También muestre cómo verificar el uso actual de la cuota.
```

### Problema 3: "No se como manejar los NULL"
**Causa:** El metodo de agregacion de valores NULL es desconocido
**Prompt de solucion:**
```text
Muestre cómo manejar valores NULL en BigQuery.
- Contar NULLs con COUNTIF
- Reemplazar NULLs con COALESCE
- Convertir a NULL con NULLIF
```

### Problema 4: "No se puede acceder a columnas anidadas"
**Causa:** Desconoce la sintaxis de tipos STRUCT y ARRAY
**Prompt de solucion:**
```text
Muestre cómo acceder a columnas anidadas (tipo STRUCT)
en BigQuery.
Ejemplo: geo.country, device.browser, ecommerce.purchase_revenue
```

---

## ✅ Punto de control
- [ ] Verified table schema
- [ ] Calculated basic statistics
- [ ] Checked missing values
- [ ] Checked categorical data distribution
- [ ] Analyzed time series data
- [ ] Understood e-commerce data characteristics

---

## 📚 Common EDA Patterns

### Check Distribution
```sql
SELECT column_name, COUNT(*) as count
FROM table
GROUP BY column_name
ORDER BY count DESC
```

### Time Series Trends
```sql
SELECT DATE(timestamp) as date, COUNT(*) as count
FROM table
GROUP BY date
ORDER BY date
```

### Preparation for Correlation Analysis
```sql
SELECT column_a, column_b, COUNT(*) as count
FROM table
GROUP BY column_a, column_b
```


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
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-8-3)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-8-3
- finish → Finalizar
