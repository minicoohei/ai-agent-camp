---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-4-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "drive"]
---

# 🎓 Lesson 4-5: Operaciones de Google Drive

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-5: Operaciones de Google Drive**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Listar, descargar y subir archivos en Drive usando gogcli |
| Duracion | ~25 min |
| Skills utilizados | gogcli drive |
| Requisitos previos | Configuracion de autenticacion de gogcli completada (start-4-1 finalizado) |

**Flujo de la sesion:**
1. Listar y buscar archivos en Drive
2. Descargar archivos
3. Subir archivos

Al finalizar esta sesion, podra operar archivos de Google Drive usando gogcli.

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

## 🚀 Step 1: Listar y buscar archivos en Drive

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Lista y búsqueda de archivos",
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

Listemos los archivos en Google Drive:

```bash
# Lista de archivos de la carpeta raiz (ultimos 10)
gog drive ls --account your-email@gmail.com --max 10

# Buscar por nombre de archivo
gog drive ls --account your-email@gmail.com --query "name contains 'actas'"

# Filtrar por tipo MIME (solo hojas de cálculo)
gog drive ls --account your-email@gmail.com --query "mimeType='application/vnd.google-apps.spreadsheet'"

# Solo Google Docs
gog drive ls --account your-email@gmail.com --query "mimeType='application/vnd.google-apps.document'"

# Solo archivos PDF
gog drive ls --account your-email@gmail.com --query "mimeType='application/pdf'"

# Lista de archivos en una carpeta específica
gog drive ls --account your-email@gmail.com --query "'<ID-de-carpeta>' in parents"

# Archivos modificados recientemente
gog drive ls --account your-email@gmail.com --query "modifiedTime > '2026-03-01'" --max 10
```

**Tipos MIME principales:**

| Formato de Google | Tipo MIME |
|-----------|-----------|
| Google Docs | `application/vnd.google-apps.document` |
| Google Sheets | `application/vnd.google-apps.spreadsheet` |
| Google Slides | `application/vnd.google-apps.presentation` |
| Carpeta | `application/vnd.google-apps.folder` |

**Resultado esperado**: Se listan los IDs de archivos, nombres de archivos, tipos MIME y fechas de ultima modificacion.

---

## 🚀 Step 2: Descargar archivos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Descarga de archivos",
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

Descargue usando los IDs de archivo obtenidos en el Step 1:

```bash
# Descargar archivos regulares (PDF, imágenes, etc.)
gog drive download <ID-de-archivo> --account your-email@gmail.com --out ./downloads/filename.pdf

# Google Docs → Convertir a PDF y descargar
gog drive download <ID-de-archivo> --account your-email@gmail.com --format pdf --out ./downloads/document.pdf

# Google Sheets → Convertir a CSV y descargar
gog drive download <ID-de-archivo> --account your-email@gmail.com --format csv --out ./downloads/sheet.csv

# Google Sheets → Convertir a Excel y descargar
gog drive download <ID-de-archivo> --account your-email@gmail.com --format xlsx --out ./downloads/sheet.xlsx

# Google Slides → Convertir a PPTX y descargar
gog drive download <ID-de-archivo> --account your-email@gmail.com --format pptx --out ./downloads/slides.pptx
```

**Lista de formatos de exportacion:**

| Formato de Google | Formatos exportables |
|-----------|---------------------|
| Google Docs | PDF, DOCX, TXT, HTML, EPUB |
| Google Sheets | CSV, XLSX, PDF, TSV |
| Google Slides | PPTX, PDF, TXT |

**Resultado esperado**: Los archivos se descargan a la ubicacion de salida especificada.

> **💡 Consejo**: Los archivos en formato de Google (Docs/Sheets/Slides) no se pueden descargar directamente, por lo que debe especificar el formato de conversion con `--format`.

---

## 🚀 Step 3: Subir archivos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Subida de archivos",
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

Suba archivos locales a Google Drive:

```bash
# Crear archivo de prueba
echo "Esta es una prueba de subida de gogcli." > /tmp/test-upload.txt

# Subir archivo (a la carpeta raiz)
gog drive upload /tmp/test-upload.txt --account your-email@gmail.com

# Subir a una carpeta especifica
gog drive upload /tmp/test-upload.txt --account your-email@gmail.com --parent <ID-de-carpeta>

# Subir multiples archivos (solicitar a la IA)
# Ingrese el siguiente prompt en Cursor:
```

**Avanzado: Subida por lotes usando IA**
```text
Por favor, suba todos los archivos PNG de la carpeta output/ a una carpeta especifica de Google Drive.
Cuenta: your-email@gmail.com
ID de carpeta: <ID-de-carpeta>
Por favor, utilice el comando gogcli drive upload.
```

**Resultado esperado**: Los archivos se suben a Google Drive y se devuelven los IDs de archivo. Puede verificar en la pagina web de Google Drive.

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
      {"id": "trouble_1", "label": "La lista de archivos está vacía"},
      {"id": "trouble_2", "label": "La descarga produce un error"},
      {"id": "trouble_3", "label": "La subida falla"},
      {"id": "trouble_4", "label": "No sé cómo encontrar el ID de la carpeta"}
    ]
  }]
}
```

### Problema 1: "La lista de archivos esta vacia"
**Causa**: Las condiciones de la consulta son demasiado estrictas, o esta viendo un drive sin permisos de acceso
**Prompt de solucion**:
```text
Primero intente gog drive ls --account <email> --max 5 sin condiciones.
Los archivos en drives compartidos pueden no mostrarse de forma predeterminada.
```

### Problema 2: "La descarga produce un error"
**Causa**: No se especifico --format para archivos de formato de Google
**Prompt de solucion**:
```text
Para Google Docs/Sheets/Slides, necesita especificar el formato de conversión con --format.
Ejemplo: --format pdf (conversión a PDF)
Ejemplo: --format csv (conversión a CSV)
```

### Problema 3: "La subida falla"
**Causa**: La ruta del archivo es incorrecta, o el tamano del archivo es demasiado grande
**Prompt de solucion**:
```text
Verifique que la ruta del archivo sea correcta: ls -la <ruta-del-archivo>
Los archivos grandes (cientos de MB o más) pueden causar un tiempo de espera agotado.
```

### Problema 4: "No se sabe como encontrar el ID de la carpeta"
**Causa**: No sabe como obtener el ID de la carpeta
**Prompt de solucion**:
```text
Método 1: Obtener lista de carpetas con gog drive ls (elementos con tipo MIME folder)
gog drive ls --account <email> --query "mimeType='application/vnd.google-apps.folder'"

Método 2: Abra la carpeta en la página web de Google Drive. El final de la URL es el ID de la carpeta.
https://drive.google.com/drive/folders/<este-es-el-ID-de-la-carpeta>
```

---

## ✅ Punto de control
- [ ] Pudo listar archivos en Drive
- [ ] Pudo buscar por nombre de archivo y tipo MIME
- [ ] Pudo descargar archivos (incluyendo descargas con conversion de formato de Google)
- [ ] Pudo subir archivos


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
Ejecute los siguientes comandos de gogcli para verificar que las operaciones de Drive funcionen correctamente:
1. gog drive ls --account <su-correo> --max 5
2. Seleccione un elemento de los resultados anteriores y descargue con gog drive download
3. Verifique que el archivo descargado exista (ls -la)
Confirme que todo funcione correctamente.
```

**Resultado esperado**: El listado de archivos y la descarga se completan sin errores.

---

## 🎉 Siguientes pasos

Las operaciones de Google Drive estan completas. En la siguiente leccion, aprendera las operaciones de Google Sheets.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/start-4-6)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-6)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /start-4-6（Operaciones de Google Sheets)
- next_window → Abrir nueva ventana con /start-4-6
- finish → Finalizar
