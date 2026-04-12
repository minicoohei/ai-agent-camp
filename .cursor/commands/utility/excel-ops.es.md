# Excel Operations - Operaciones con archivos Excel

Lea, escriba y analice archivos Excel utilizando openpyxl.

## Funcionalidades

- Lectura de hojas y conversión a Markdown
- Análisis de la estructura del libro de trabajo
- Creación de nuevos archivos Excel
- Actualización de celdas

## Pasos

### Paso 1: Extraer parámetros

Extraiga lo siguiente de la entrada del usuario:
- **Comando**: read / to-markdown / analyze / write / list-sheets
- **Ruta del archivo**: Ruta al archivo Excel
- **Nombre de la hoja**: Si se especifica una hoja en particular
- **Destino de salida**: Ruta del archivo (se muestra en pantalla si se omite)

### Paso 2: Ejecutar la herramienta

```bash
# Lectura
uv run python tools/excel_ops.py read <file.xlsx>

# Convertir a Markdown
uv run python tools/excel_ops.py to-markdown <file.xlsx>

# Analizar
uv run python tools/excel_ops.py analyze <file.xlsx>

# Listar hojas
uv run python tools/excel_ops.py list-sheets <file.xlsx>
```

### Paso 3: Mostrar resultados

Presente los datos de salida al usuario.

## Opciones

### Comando read

| Opción | Descripción |
|--------|-------------|
| `--sheet TEXT` / `-s` | Leer una hoja específica |
| `--max-rows INT` / `-n` | Filas máximas (predeterminado: 100) |
| `--format TEXT` / `-f` | Formato de salida: text / json |

### Comando to-markdown

| Opción | Descripción |
|--------|-------------|
| `--sheet TEXT` / `-s` | Convertir una hoja específica |
| `--max-rows INT` / `-n` | Filas máximas |
| `--output PATH` / `-o` | Ruta del archivo de salida |

### Comando write

| Opción | Descripción |
|--------|-------------|
| `--data JSON` / `-d` | Datos en formato JSON (obligatorio) |
| `--output PATH` / `-o` | Salida a un archivo separado |

## Ejemplos de uso

### Leer un archivo

```
/excel-ops read report.xlsx
```

### Convertir una hoja específica a Markdown

```
/excel-ops to-markdown data.xlsx --sheet "Datos de ventas" -o sales.md
```

### Analizar un libro de trabajo

```
/excel-ops analyze financial_report.xlsx --format json
```

### Crear un nuevo archivo

```
/excel-ops write new.xlsx --data '{"headers":["Nombre","Edad"],"rows":[["Tanaka",30],["Sato",25]]}'
```

## Formatos de salida

### read (formato texto)

```
Sheet: Sheet1
Dimensions: A1:D100
Rows: 99

Headers: ['Nombre', 'Departamento', 'Ventas', 'Tasa de logro']

Sample rows (first 5):
  1: ['Taro Tanaka', 'Depto. Ventas', '1500000', '120%']
  2: ['Hanako Sato', 'Depto. Planificación', '980000', '98%']
```

### to-markdown

```markdown
# report.xlsx

**Sheet**: Sheet1
**Dimensions**: A1:D100
**Rows**: 99 (max 100)

| Nombre | Departamento | Ventas | Tasa de logro |
|--------|-------------|--------|---------------|
| Taro Tanaka | Depto. Ventas | 1500000 | 120% |
| Hanako Sato | Depto. Planificación | 980000 | 98% |
```

### analyze

```
Informe de análisis: report.xlsx
==================================================
Sheets: 3
Total rows: 150
Estimated cells: 600

Sheet1
   Dimensions: A1:D50
   Rows: 50, Columns: 4
   Headers: ['Nombre', 'Departamento', 'Ventas', 'Tasa de logro']
```

## Requisitos previos

Se requiere la biblioteca openpyxl:

```bash
pip install openpyxl
```

## Comandos relacionados

- `/pptx-ops` - Operaciones con PowerPoint
- `/fetch-slides` - Obtención de Google Slides
