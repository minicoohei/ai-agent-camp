---
nonInteractiveMode: deferred
---

# PDF Page Editor

Un comando para editar (modificar/eliminar) texto en archivos PDF.
Utiliza un formato interactivo AskQuestion para la selección de páginas y texto.

## Pasos de ejecución

### Paso 1: Extracción de parámetros

Extraiga lo siguiente de la entrada del usuario:
- **Ruta del archivo PDF**: El PDF a editar (obligatorio)
- **Contenido de la edición**: Qué texto cambiar y cómo (opcional, se puede confirmar después)

---

### Paso 2: Análisis del PDF

```bash
uv run python tools/pdf_page_editor.py analyze "{ruta_archivo_pdf}"
```

- Se crea un espacio de trabajo (`{nombre_pdf}_workspace/`)
- Se analizan los elementos de texto de cada página
- Obtenga la lista de páginas desde `analysis.yaml`

---

### Paso 3: Selección de página (AskQuestion)

**Utilice la herramienta ask_question para seleccionar una página:**

```yaml
title: "Seleccione una página para editar"
questions:
  - id: "page_select"
    prompt: "¿Qué página desea editar?"
    options:
      # Generado dinámicamente desde analysis.yaml
      # Ejemplo:
      - id: "page_1"
        label: "Página 1 - {primeros 20 caracteres del primer elemento de texto}..."
      - id: "page_2"
        label: "Página 2 - {primeros 20 caracteres del primer elemento de texto}..."
      # ... para todas las páginas
    allow_multiple: false
```

> **Sugerencia de implementación**: Obtenga el primer elemento de texto de cada página en `analysis.yaml`
> e incluya los primeros ~20 caracteres en la etiqueta para ayudar a los usuarios a identificar las páginas.

---

### Paso 4: Mostrar lista de texto

```bash
uv run python tools/pdf_page_editor.py show {espacio_de_trabajo} {número_de_página}
```

- Muestra todos los elementos de texto de esa página como una **lista numerada**
- Ejemplo:
  ```
  Elementos de texto en la página 3:
  [1] Nuevos estándares para el análisis de datos con IA
  [2] Empresa XYZ S.A.
  [3] Diciembre 2024
  [4] Tabla de contenido
  ...
  ```

---

### Paso 5: Selección de texto (AskQuestion)

**Utilice la herramienta ask_question para confirmar el método de selección:**

```yaml
title: "Seleccione el texto a editar"
questions:
  - id: "text_select_method"
    prompt: "Elija el método de selección de texto"
    options:
      - id: "by_number"
        label: "Seleccionar por número (especificar un número de la lista anterior)"
      - id: "by_input"
        label: "Ingresar texto directamente"
    allow_multiple: false
```

#### Si selecciona por número

**Continuar con ask_question para seleccionar el número de texto:**

```yaml
title: "Seleccionar número de texto"
questions:
  - id: "text_number"
    prompt: "Elija el número del texto a editar"
    options:
      # Generado dinámicamente desde la lista mostrada en el Paso 4
      - id: "text_1"
        label: "[1] Nuevos estándares para el análisis de datos con IA"
      - id: "text_2"
        label: "[2] Empresa XYZ S.A."
      # ... para todos los elementos de texto
    allow_multiple: false
```

#### Si ingresa texto directamente

Solicite al usuario que ingrese el texto objetivo.

---

### Paso 6: Selección del tipo de edición (AskQuestion)

**Utilice la herramienta ask_question para seleccionar el tipo de edición:**

```yaml
title: "Seleccione el tipo de edición"
questions:
  - id: "edit_type"
    prompt: "¿Qué tipo de edición desea realizar?"
    options:
      - id: "replace"
        label: "Reemplazo de texto (cambiar a un texto diferente)"
      - id: "delete"
        label: "Eliminación de texto (eliminar el texto)"
      - id: "prompt"
        label: "Descripción libre (instruir a la IA para editar)"
    allow_multiple: false
```

#### Entrada adicional por tipo de edición

- **Reemplazo**: Solicitar el nuevo texto
- **Eliminación**: Solo confirmación (no se necesita entrada adicional)
- **Descripción libre**: Solicitar instrucciones de edición

---

### Paso 7: Ejecutar edición

```bash
# Reemplazo de texto
uv run python tools/pdf_page_editor.py edit {espacio_de_trabajo} {número_de_página} --replace "{texto_anterior}" "{texto_nuevo}"

# Eliminación de texto
uv run python tools/pdf_page_editor.py edit {espacio_de_trabajo} {número_de_página} --delete "{texto_a_eliminar}"

# Descripción libre
uv run python tools/pdf_page_editor.py edit {espacio_de_trabajo} {número_de_página} --prompt "{instrucciones_de_edición}"
```

---

### Paso 8: Mostrar resultados

Después de completar la edición, muestre lo siguiente al usuario:

```
✅ Edición completada

Imagen original: {espacio_de_trabajo}/pages/page_{número:03d}.png
Imagen editada: {espacio_de_trabajo}/edited/page_{número:03d}_edited.png
```

- Utilice el comando `open` para abrir la imagen si es necesario

---

### Paso 9: Selección de la siguiente acción (AskQuestion)

**Utilice la herramienta ask_question para confirmar la siguiente acción:**

```yaml
title: "Siguiente acción"
questions:
  - id: "next_action"
    prompt: "¿Qué desea hacer a continuación?"
    options:
      - id: "same_page"
        label: "Editar otro texto en la misma página"
      - id: "other_page"
        label: "Editar una página diferente"
      - id: "rebuild"
        label: "Finalizar la edición y reconstruir el PDF"
      - id: "exit"
        label: "Terminar la edición (sin reconstruir)"
    allow_multiple: false
```

#### Transiciones por acción

- **Editar otro texto en la misma página**: -> Volver al Paso 4
- **Editar una página diferente**: -> Volver al Paso 3
- **Finalizar la edición y reconstruir el PDF**: -> Ir al Paso 10
- **Terminar la edición (sin reconstruir)**: -> Finalizado

---

### Paso 10: Reconstrucción del PDF (Opcional)

```bash
uv run python tools/pdf_page_editor.py rebuild {espacio_de_trabajo}
```

- Se genera un nuevo PDF con las páginas editadas
- Salida: `{espacio_de_trabajo}/{nombre_pdf}_edited.pdf`

---

## Diagrama de flujo

```
Análisis PDF -> [AskQuestion] Selección de página
                      |
                Mostrar lista de texto
                      |
            [AskQuestion] Método de selección de texto
                 |              |
           Por número     Entrada directa
                 |              |
          [AskQuestion]    Entrada de texto
          Selección número
                 |              |
            [AskQuestion] Selección tipo de edición
                      |
                Ejecutar edición
                      |
               Mostrar resultados
                      |
            [AskQuestion] Siguiente acción
             |      |       |        |
          Misma   Otra   Recons-   Salir
          página  página  truir
             |      |       |
           Paso4  Paso3  Paso10
```

---

## Ejemplo de uso

```
/pdf-editor docs/presentation.pdf
```

-> Análisis PDF -> [AskQuestion] Selección de página -> Mostrar lista de texto -> [AskQuestion] Selección de texto -> [AskQuestion] Tipo de edición -> Ejecutar edición -> [AskQuestion] Siguiente acción

---

## Estructura del espacio de trabajo

```
{nombre_pdf}_workspace/
├── pages/           # Imágenes de páginas extraídas
│   ├── page_001.png
│   └── ...
├── edited/          # Imágenes editadas
│   ├── page_001_edited.png
│   └── ...
├── analysis.yaml    # Resultados del análisis (elementos de texto)
└── {nombre_pdf}_edited.pdf  # Salida final
```

---

## Notas

- Requiere `GEMINI_API_KEY` o `GOOGLE_API_KEY`
- La edición de imágenes es generada por IA, por lo que las fuentes y el diseño pueden cambiar ligeramente
- Dependencias: `pdf2image`, `img2pdf`, `tqdm`, `PyYAML`, `Pillow`, `google-genai`
