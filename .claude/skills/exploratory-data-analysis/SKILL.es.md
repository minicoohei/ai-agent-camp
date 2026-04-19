---
name: exploratory-data-analysis
description: "Habilidad de análisis exploratorio de datos (EDA) compatible con más de 200 formatos de archivo. Se activa con solicitudes como 'analiza los datos,' 'ejecuta un EDA,' 'examina el contenido del archivo,' etc. Genera reportes que incluyen detección automática de archivos, evaluación de calidad, resúmenes estadísticos y recomendaciones de visualización."
license: MIT license
metadata:
    skill-author: K-Dense Inc.
source: github.com/K-Dense-AI/claude-scientific-skills@main
triggers:
  - exploratory-data-analysis
  - EDA
  - データ探索
  - 探索的データ分析
  - ファイル解析
  - データ品質チェック
  - データプロファイリング
---

## Palabras Clave de Activación
"Análisis de datos," "EDA," "Análisis de archivo," "Exploración de datos," "Análisis CSV"

# Análisis Exploratorio de Datos

## Descripción General

Realice análisis exploratorio de datos (EDA) integral en archivos de datos científicos de múltiples dominios. Esta habilidad proporciona detección automática de tipo de archivo, análisis específico por formato, evaluación de calidad de datos y genera reportes detallados en markdown adecuados para documentación y planificación de análisis posteriores.

**Capacidades Clave:**
- Detección y análisis automático de más de 200 formatos de archivos científicos
- Extracción integral de metadatos específicos por formato
- Evaluación de calidad e integridad de datos
- Resúmenes estadísticos y distribuciones
- Recomendaciones de visualización
- Sugerencias de análisis posteriores
- Generación de reportes en markdown

## Cuándo Usar Esta Habilidad

Use esta habilidad cuando:
- El usuario proporciona una ruta a un archivo de datos científicos para análisis
- El usuario pide "explorar", "analizar" o "resumir" un archivo de datos
- El usuario quiere entender la estructura y contenido de datos científicos
- El usuario necesita un reporte integral de un conjunto de datos antes del análisis
- El usuario quiere evaluar la calidad o completitud de los datos
- El usuario pregunta qué tipo de análisis es apropiado para un archivo

## Categorías de Archivos Soportados

La habilidad tiene cobertura integral de formatos de archivos científicos organizados en seis categorías principales:

### 1. Formatos de Química y Molecular (60+ extensiones)
Archivos de estructura, salidas de química computacional, trayectorias de dinámica molecular y bases de datos químicas.

**Tipos de archivo incluyen:** `.pdb`, `.cif`, `.mol`, `.mol2`, `.sdf`, `.xyz`, `.smi`, `.gro`, `.log`, `.fchk`, `.cube`, `.dcd`, `.xtc`, `.trr`, `.prmtop`, `.psf`, y más.

**Archivo de referencia:** `references/chemistry_molecular_formats.md`

### 2. Formatos de Bioinformática y Genómica (50+ extensiones)
Datos de secuencias, alineamientos, anotaciones, variantes y datos de expresión.

**Tipos de archivo incluyen:** `.fasta`, `.fastq`, `.sam`, `.bam`, `.vcf`, `.bed`, `.gff`, `.gtf`, `.bigwig`, `.h5ad`, `.loom`, `.counts`, `.mtx`, y más.

**Archivo de referencia:** `references/bioinformatics_genomics_formats.md`

### 3. Formatos de Microscopía e Imágenes (45+ extensiones)
Imágenes de microscopía, imágenes médicas, imágenes de portaobjetos completos y microscopía electrónica.

**Tipos de archivo incluyen:** `.tif`, `.nd2`, `.lif`, `.czi`, `.ims`, `.dcm`, `.nii`, `.mrc`, `.dm3`, `.vsi`, `.svs`, `.ome.tiff`, y más.

**Archivo de referencia:** `references/microscopy_imaging_formats.md`

### 4. Formatos de Espectroscopía y Química Analítica (35+ extensiones)
RMN, espectrometría de masas, IR/Raman, UV-Vis, rayos X, cromatografía y otras técnicas analíticas.

**Tipos de archivo incluyen:** `.fid`, `.mzML`, `.mzXML`, `.raw`, `.mgf`, `.spc`, `.jdx`, `.xy`, `.cif` (cristalografía), `.wdf`, y más.

**Archivo de referencia:** `references/spectroscopy_analytical_formats.md`

### 5. Formatos de Proteómica y Metabolómica (30+ extensiones)
Proteómica por espectrometría de masas, metabolómica, lipidómica y datos multi-ómicos.

**Tipos de archivo incluyen:** `.mzML`, `.pepXML`, `.protXML`, `.mzid`, `.mzTab`, `.sky`, `.mgf`, `.msp`, `.h5ad`, y más.

**Archivo de referencia:** `references/proteomics_metabolomics_formats.md`

### 6. Formatos de Datos Científicos Generales (30+ extensiones)
Arrays, tablas, datos jerárquicos, archivos comprimidos y formatos científicos comunes.

**Tipos de archivo incluyen:** `.npy`, `.npz`, `.csv`, `.xlsx`, `.json`, `.hdf5`, `.zarr`, `.parquet`, `.mat`, `.fits`, `.nc`, `.xml`, y más.

**Archivo de referencia:** `references/general_scientific_formats.md`

## Flujo de Trabajo

### Paso 1: Detección del Tipo de Archivo

Cuando un usuario proporciona una ruta de archivo, primero identifique el tipo de archivo:

1. Extraiga la extensión del archivo
2. Busque la extensión en el archivo de referencia apropiado
3. Identifique la categoría del archivo y la descripción del formato
4. Cargue la información específica del formato

**Ejemplo:**
```
Usuario: "Analiza data.fastq"
-> Extensión: .fastq
-> Categoría: bioinformatics_genomics
-> Formato: Formato FASTQ (datos de secuencia con puntuaciones de calidad)
-> Referencia: references/bioinformatics_genomics_formats.md
```

### Paso 2: Cargar Información Específica del Formato

Basándose en el tipo de archivo, lea el archivo de referencia correspondiente para entender:
- **Datos Típicos:** Qué tipo de datos contiene este formato
- **Casos de Uso:** Aplicaciones comunes para este formato
- **Bibliotecas de Python:** Cómo leer el archivo en Python
- **Enfoque de EDA:** Qué análisis son apropiados para este tipo de datos

Busque en el archivo de referencia la extensión específica (por ejemplo, busque "### .fastq" en `bioinformatics_genomics_formats.md`).

### Paso 3: Realizar el Análisis de Datos

Use el script `scripts/eda_analyzer.py` O implemente un análisis personalizado:

**Opción A: Use el script del analizador**
```python
# El script automáticamente:
# 1. Detecta el tipo de archivo
# 2. Carga la información de referencia
# 3. Realiza análisis específico por formato
# 4. Genera reporte en markdown

python scripts/eda_analyzer.py <ruta_archivo> [salida.md]
```

**Opción B: Análisis personalizado en la conversación**
Basándose en la información del formato del archivo de referencia, realice el análisis apropiado:

Para datos tabulares (CSV, TSV, Excel):
- Cargue con pandas
- Verifique dimensiones, tipos de datos
- Analice valores faltantes
- Calcule estadísticas resumen
- Identifique valores atípicos
- Verifique duplicados

Para datos de secuencia (FASTA, FASTQ):
- Cuente secuencias
- Analice distribuciones de longitud
- Calcule contenido GC
- Evalúe puntuaciones de calidad (FASTQ)

Para imágenes (TIFF, ND2, CZI):
- Verifique dimensiones (X, Y, Z, C, T)
- Analice profundidad de bits y rango de valores
- Extraiga metadatos (canales, marcas de tiempo, calibración espacial)
- Calcule estadísticas de intensidad

Para arrays (NPY, HDF5):
- Verifique forma y dimensiones
- Analice tipo de datos
- Calcule resúmenes estadísticos
- Verifique valores faltantes/inválidos

### Paso 4: Generar Reporte Integral

Cree un reporte en markdown con las siguientes secciones:

#### Secciones Requeridas:
1. **Título y Metadatos**
   - Nombre del archivo y marca de tiempo
   - Tamaño del archivo y ubicación

2. **Información Básica**
   - Propiedades del archivo
   - Identificación del formato

3. **Detalles del Tipo de Archivo**
   - Descripción del formato desde la referencia
   - Contenido típico de datos
   - Casos de uso comunes
   - Bibliotecas de Python para lectura

4. **Análisis de Datos**
   - Estructura y dimensiones
   - Resúmenes estadísticos
   - Evaluación de calidad
   - Características de los datos

5. **Hallazgos Clave**
   - Patrones notables
   - Problemas potenciales
   - Métricas de calidad

6. **Recomendaciones**
   - Pasos de preprocesamiento
   - Análisis apropiados
   - Herramientas y métodos
   - Enfoques de visualización

#### Ubicación de la Plantilla
Use `assets/report_template.md` como guía para la estructura del reporte.

### Paso 5: Guardar Reporte

Guarde el reporte en markdown con un nombre descriptivo:
- Patrón: `{nombre_archivo_original}_eda_report.md`
- Ejemplo: `experiment_data.fastq` -> `experiment_data_eda_report.md`

## Solución de Problemas

### Bibliotecas Faltantes

Muchos formatos científicos requieren bibliotecas especializadas:

**Problema:** Error de importación al intentar leer un archivo

**Solución:** Proporcione instrucciones claras de instalación
```python
try:
    from Bio import SeqIO
except ImportError:
    print("Instale Biopython: uv add biopython")
```

Requisitos comunes por categoría:
- **Bioinformática:** `biopython`, `pysam`, `pyBigWig`
- **Química:** `rdkit`, `mdanalysis`, `cclib`
- **Microscopía:** `tifffile`, `nd2reader`, `aicsimageio`, `pydicom`
- **Espectroscopía:** `nmrglue`, `pymzml`, `pyteomics`
- **General:** `pandas`, `numpy`, `h5py`, `scipy`

### Tipos de Archivo Desconocidos

Si una extensión de archivo no está en las referencias:

1. Pregunte al usuario sobre el formato del archivo
2. Verifique si es una variante específica del proveedor
3. Intente un análisis genérico basado en la estructura del archivo (texto vs binario)
4. Proporcione recomendaciones generales

### Archivos Grandes

Para archivos muy grandes:

1. Use estrategias de muestreo (primeros N registros)
2. Use acceso mapeado en memoria (para HDF5, NPY)
3. Procese en bloques (para CSV, FASTQ)
4. Proporcione estimaciones basadas en muestras

## Uso del Script

El `scripts/eda_analyzer.py` se puede usar directamente:

```bash
# Uso básico
python scripts/eda_analyzer.py data.csv

# Especificar archivo de salida
python scripts/eda_analyzer.py data.csv output_report.md

# El script:
# 1. Auto-detecta el tipo de archivo
# 2. Carga referencias de formato
# 3. Realiza el análisis apropiado
# 4. Genera reporte en markdown
```

## Recursos

### scripts/
- `eda_analyzer.py`: Script de análisis integral que se puede ejecutar directamente o importar

### references/
- `chemistry_molecular_formats.md`: 60+ formatos de archivos de química/molecular
- `bioinformatics_genomics_formats.md`: 50+ formatos de bioinformática
- `microscopy_imaging_formats.md`: 45+ formatos de imágenes
- `spectroscopy_analytical_formats.md`: 35+ formatos de espectroscopía
- `proteomics_metabolomics_formats.md`: 30+ formatos ómicos
- `general_scientific_formats.md`: 30+ formatos generales

### assets/
- `report_template.md`: Plantilla integral en markdown para reportes de EDA
