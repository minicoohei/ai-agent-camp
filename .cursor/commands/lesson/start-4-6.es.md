---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~30 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "sheets"]
---

# 🎓 Lesson 4-6: Operaciones de Google Sheets

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-6: Operaciones de Google Sheets**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Leer y escribir hojas de calculo usando gogcli |
| Duracion | ~30 min |
| Skills utilizados | gogcli sheets |
| Requisitos previos | Configuracion de autenticacion de gogcli completada (start-4-1 finalizado) |

**Flujo de la sesion:**
1. Buscar hojas de calculo desde Drive
2. Obtener datos de la hoja (salida CSV)
3. Analizar datos obtenidos con IA

Al finalizar esta sesion, podra leer y analizar datos de Google Sheets usando gogcli.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de iniciar la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo/a?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → `gog auth list`  para verificar estado de autenticacion)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Buscar hojas de calculo desde Drive

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Búsqueda de hojas de cálculo",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:

Primero, identifiquemos la hoja de calculo objetivo:

```bash
# Buscar hojas de cálculo desde Drive
gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'" --account your-email@gmail.com

# Nota: gogcli v0.9.0 no tiene un comando `gog sheets list`.
# Verifique los nombres de hojas (pestañas) en la interfaz de Google Sheets, o
# especifique el nombre de la hoja al obtener datos con gog sheets get.
```

**Como obtener el ID de la hoja de calculo:**
- URL de Google Sheets: `https://docs.google.com/spreadsheets/d/<este-es-el-ID-de-la-hoja>/edit`
- O use el ID de archivo de los resultados de `gog drive ls`

**Resultado esperado**: Se muestra una lista de archivos de hojas de calculo en Drive (nombres de archivo e IDs).

> **💡 Consejo**: Si no tiene una hoja de calculo de practica, cree una nueva hoja de calculo en Google Sheets e ingrese algunas filas de datos de muestra (nombres, ventas, fechas, etc.).

---

## 🚀 Step 2: Obtener datos de la hoja (salida CSV)

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Obtención de datos",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:

Obtenga datos de la hoja de calculo:

```bash
# Obtener todos los datos de la hoja
gog sheets get <ID-de-hoja-de-cálculo> "Sheet1" --account your-email@gmail.com

# Obtener un rango especifico (A1:D10)
gog sheets get <ID-de-hoja-de-cálculo> "Sheet1!A1:D10" --account your-email@gmail.com

# Guardar como archivo CSV
gog sheets get <ID-de-hoja-de-cálculo> "Sheet1" --account your-email@gmail.com > /tmp/sheet_data.csv

# Alternativa: Descargar CSV via Drive
gog drive download <ID-de-hoja-de-cálculo> --format csv --out ./downloads/sheet_data.csv --account your-email@gmail.com
```

**Formato de especificacion de rango:**

| Formato | Descripcion | Ejemplo |
|------|------|-----|
| `Sheet1` | Hoja completa | `"Sheet1"` |
| `Sheet1!A1:D10` | Rango especifico | `"Sheet1!A1:D10"` |
| `Sheet1!A:A` | Columna completa | `"Sheet1!A:A"` |
| `Sheet1!1:5` | Rango de filas | `"Sheet1!1:5"` |
| `'Datos de ventas'!A1:Z` | Nombre de hoja en japones | Envuelva el nombre de la hoja entre comillas simples |

**Resultado esperado**: Los datos de la hoja de calculo se muestran en la terminal. Si se redirige a CSV, se guarda en un archivo.

> **⚠️ Advertencia**: Cuando use nombres de hojas en japones, envuelvalos entre comillas simples (por ejemplo, `'Datos de ventas'!A1:D10`).

---

## 🚀 Step 3: Analizar datos obtenidos con IA

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Análisis de datos con IA",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:

Hagamos que la IA analice los datos de la hoja de calculo obtenidos:

```bash
# Obtener datos y guardar en archivo
gog sheets get <ID-de-hoja-de-cálculo> "Sheet1" --account your-email@gmail.com > /tmp/sheet_data.csv
```

Cargue el archivo CSV guardado en Cursor y solicite el analisis:

```text
Analice los datos en /tmp/sheet_data.csv:
1. Resumen de datos (número de filas, columnas, tipos de datos)
2. Estadísticas básicas (media, máximo, mínimo de columnas numéricas)
3. Cualquier tendencia o patrón observado
4. Señale cualquier problema de calidad de datos (valores faltantes, valores atípicos)
```

**Avanzado: Generacion de reportes**
```text
Cree un resumen del reporte mensual a partir de los datos de la hoja de cálculo anterior:
- Puntos destacados de KPI principales
- Cambios mes a mes
- Tendencias notables
- Sugerencias de mejora
Guarde en formato Markdown en output/reports/.
```

**Avanzado: Visualizacion de datos**
```text
Visualice los datos anteriores con matplotlib de Python:
- Gráfico de tendencia mensual de ventas
- Gráfico circular por categoría
- Gráfico de barras de los 10 principales
Guarde los gráficos en output/images/.
```

**Resultado esperado**: La IA genera resultados de analisis, estadisticas y explicaciones de tendencias para los datos.

---

## ⚠️ Problemas comunes y soluciones

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No se conoce el ID de la hoja de cálculo"},
      {"id": "trouble_2", "label": "La especificación de rango produce un error"},
      {"id": "trouble_3", "label": "Los datos tienen problemas de codificación"},
      {"id": "trouble_4", "label": "No hay datos de práctica disponibles"}
    ]
  }]
}
```

### Problema 1: "No se conoce el ID de la hoja de calculo"
**Causa**: No sabe como obtener el ID
**Prompt de solucion**:
```text
Abra Google Sheets y verifique la URL:
https://docs.google.com/spreadsheets/d/<esta-parte-es-el-ID>/edit
O busque hojas de cálculo con gog drive ls y use el ID del archivo.
```

### Problema 2: "La especificacion de rango produce un error"
**Causa**: El nombre de la hoja es incorrecto, o el rango no existe
**Prompt de solucion**:
```text
gogcli no tiene un comando `gog sheets list`.
Verifique el nombre de la hoja (pestaña) en la interfaz de Google Sheets.
Los nombres de hojas en japonés deben estar entre comillas simples: 'Datos de ventas'!A1:D10
```

### Problema 3: "Los datos tienen problemas de codificacion"
**Causa**: Problema de codificacion
**Prompt de solucion**:
```text
Redirija la salida a un archivo y verifique la codificación:
gog sheets get ... > /tmp/data.csv
file /tmp/data.csv
Si no es UTF-8, convierta con iconv: iconv -f SHIFT_JIS -t UTF-8 /tmp/data.csv
```

### Problema 4: "No hay datos de practica disponibles"
**Causa**: No hay hoja de calculo disponible para pruebas
**Prompt de solucion**:
```text
Cree una nueva hoja de cálculo en Google Sheets e ingrese los siguientes datos de muestra:
A1: Nombre, B1: Departamento, C1: Ventas, D1: Mes
A2: Tanaka, B2: Ventas, C2: 500000, D2: Enero
A3: Suzuki, B3: Marketing, C3: 350000, D3: Enero
(5-10 filas son suficientes)
```

---

## ✅ Punto de control
- [ ] Pudo buscar hojas de calculo desde Drive
- [ ] Pudo obtener datos de un rango especifico
- [ ] Pudo guardar datos como archivo CSV
- [ ] Pudo hacer que la IA analice los datos y confirmar los resultados


---

## 📋 Vista previa de resultados

El entregable de esta leccion es la salida de la terminal.

### Salida esperada
```text
┌─────────────────────────────────────┐
│  Resultado de ejecución del comando    │
│  Estado: ✅ Éxito                       │
│  Elementos procesados: N               │
└─────────────────────────────────────┘
```

> Consejo: Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Codex para verificar la finalizacion:

```text
Ejecute los siguientes comandos de gogcli para verificar que las operaciones de Sheets funcionen correctamente:
1. gog drive ls --query "mimeType='application/vnd.google-apps.spreadsheet'" --account <direccion-de-correo>
2. Seleccione uno de la lista anterior y obtenga datos con gog sheets get <ID-de-hoja-de-calculo> "Sheet1" --account <direccion-de-correo>
3. Verifique que los datos obtenidos se muestren correctamente
Por favor, confirme que todo funciona correctamente.
```

**Resultado esperado**: El listado de hojas y la obtencion de datos se completan sin errores.

---

## 🎉 Siguientes pasos

Las operaciones de Google Sheets estan completas! En la siguiente leccion, construira un flujo de trabajo de secretaria IA integrando Gmail, Calendar, Drive y Sheets.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/start-4-7)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-7)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /start-4-7（Integracion de flujo de trabajo de secretaria IA)
- next_window → Abrir nueva ventana con /start-4-7
- finish → Finalizar
