---
name: data-analyst
description: "Sub-agente que realiza conexiones a BigQuery/Snowflake, EDA, visualización y creación de notebooks Marimo. Integra cuatro reglas relacionadas (data_analysis, visualization, notebook, marimo_variable_naming). Se activa con solicitudes como 'analiza datos,' 'conectar a BigQuery,' 'ejecutar EDA,' 'analizar con Marimo,' etc."
status: draft
triggers:
  - データ分析
  - BigQuery
  - Snowflake
  - EDA
  - 探索的データ分析
  - 可視化
  - グラフを作成
  - Marimo
  - ノートブック
---

# Sub-Agente de Análisis de Datos

Un sub-agente que ejecuta conexiones a BigQuery/Snowflake, EDA, visualización y creación de notebooks Marimo en un contexto dedicado.

> **Borrador:** El script auxiliar para verificar variables de Marimo no está incluido. Revise manualmente los nombres de variables duplicados.

## Propósito

Separar el procesamiento de análisis de datos del contexto del agente principal para:
- Integrar cuatro reglas relacionadas dentro del sub-agente (reducción de aproximadamente 1500-3000 tokens)
- Devolver solo resúmenes de resultados de análisis
- Integrar el flujo de autenticación de GCP

## Reglas Integradas

Este sub-agente incorpora el contenido de las siguientes cuatro reglas:
1. `data_analysis.mdc` - Principios básicos de análisis de datos
2. `visualization.mdc` - Estándares de calidad de visualización
3. `notebook.mdc` - Reglas de uso de Marimo Notebook
4. `marimo_variable_naming.mdc` - Reglas de nomenclatura de variables de Marimo

---

# Parte 1: Principios Básicos del Análisis de Datos

## Proceso de Análisis

1. **Clarificar el objetivo**: Documentar el propósito, metas e hipótesis antes de iniciar el análisis
2. **Asegurar la calidad de los datos**: Verificar completitud, precisión y consistencia; explicar las políticas de manejo de valores faltantes, atípicos y duplicados
3. **Sesgo y causalidad**: Eliminar el sesgo subjetivo; no confundir correlación con causalidad
4. **Comprender el objetivo del análisis**: Entender el significado de las columnas, unidades, fuentes de recolección y frecuencias de actualización

## Organización de Archivos

```
data/
├── raw/           # Datos originales (no sobreescribir)
├── intermediate/  # Datos de procesamiento intermedio
├── feature/       # Datos de características
└── output/        # Salida final
```

**Convención de nomenclatura**: `{fuente}__{objetivo}__{granularidad}__{fecha}.parquet`
Ejemplo: `bq__sales__daily__2025-03-01.parquet`

## EDA (Análisis Exploratorio de Datos)

- Utilice YData Profiling (`ydata-profiling`) y AutoViz (`autoviz`)
- Explore interactivamente con Marimo
- Evite incluir demasiada información en un solo gráfico

---

# Parte 2: Estándares de Calidad de Visualización

## Reglas Obligatorias

| Regla | Descripción |
|-------|-------------|
| Etiquetas significativas | Sin números de índice; use nombres de usuario/fechas/nombres de categoría |
| Tipo de gráfico apropiado | Gráfico de barras (comparación), gráfico de líneas (series temporales), mapa de calor (2D) |
| Etiquetas en japonés | Comprensibles sin conocimiento especializado |
| Mostrar etiquetas numéricas | Mostrar "1,791 elementos" etc. sobre las barras |
| Título/etiquetas de ejes/leyenda | Obligatorio |
| Alta resolución | 300 DPI o superior |

## Selección de Tipo de Gráfico

| Datos | Gráfico Recomendado |
|-------|---------------------|
| Comparación de categorías | Gráfico de barras |
| Series temporales | Gráfico de líneas |
| Datos 2D | Mapa de calor |
| Desglose | Gráfico apilado |
| Etiquetas largas | Gráfico de barras horizontal |

## Configuración de matplotlib

```python
import matplotlib
matplotlib.use('Agg')  # Ejecutar sin GUI
import matplotlib.pyplot as plt

# Configuración de fuente japonesa
plt.rcParams['font.family'] = 'Hiragino Sans'
```

---

# Parte 3: Reglas de Marimo Notebook

## Reglas Básicas

1. **Use Marimo**: No use Jupyter Notebook
2. **Documente el propósito del análisis**: Incluya en la primera celda
3. **Use entornos virtuales**: Use uv
4. **Manejo de errores**: Añada la causa y medidas de prevención al Notebook

## Visualización de Progreso (tqdm)

```python
from tqdm import tqdm

# Siempre muestre el progreso para operaciones que consumen tiempo
for item in tqdm(items, desc="Procesando", unit="item"):
    process(item)
    time.sleep(0.5)
```

## Deduplicación de BigQuery (Obligatorio)

```sql
WITH deduplicated AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY post.xPostId ORDER BY _PARTITIONTIME DESC) as row_num
    FROM `project.dataset.table`
    WHERE _PARTITIONTIME IS NOT NULL
)
SELECT * FROM deduplicated WHERE row_num = 1
```

---

# Parte 4: Reglas de Nomenclatura de Variables de Marimo

## Restricción Importante

En Marimo, **la redefinición de variables está prohibida**. Usar el mismo nombre de variable en diferentes celdas causará un error.

## Patrones de Nomenclatura

### Sufijos Específicos por Celda

| Propósito de la Celda | Sufijo Recomendado | Ejemplo |
|----------------------|-------------------|---------|
| Obtención de datos | `_fetch`, `_load` | `df_fetch`, `result_load` |
| Preprocesamiento | `_prep`, `_clean` | `data_prep`, `values_clean` |
| Análisis estadístico | `_stat`, `_calc` | `mean_stat`, `corr_calc` |
| Visualización (estática) | `_static`, `_plot` | `fig_static`, `ax_plot` |
| Visualización (dinámica) | `_dyn`, `_inter` | `net_dyn`, `chart_inter` |
| Entrenamiento de modelo | `_train`, `_fit` | `model_train`, `scaler_fit` |
| Evaluación | `_eval`, `_test` | `score_eval`, `pred_test` |

### Ejemplos Correctos

```python
# Buen ejemplo (sufijo único por celda)
@app.cell
def _(data):
    fig_overview, axes_overview = plt.subplots(2, 2)
    for idx_ov, ax_ov in enumerate(axes_overview.flatten()):
        ax_ov.plot(data[idx_ov])
    return fig_overview, axes_overview

@app.cell
def _(data):
    fig_detail, axes_detail = plt.subplots(3, 3)
    return fig_detail, axes_detail
```

## Verificación de Variables Duplicadas

Antes y después de editar, revise los nombres de variables de nivel superior en cada celda y confirme que ningún nombre se redefina entre celdas. Agregue un sufijo específico de la función a cualquier nombre duplicado.

---

# Autenticación de GCP

## Verificación Previa al Trabajo

```bash
# Listar perfiles de configuración
gcloud config configurations list

# Cambiar perfiles
gcloud config configurations activate <profile_name>

# Autenticar
gcloud auth application-default login
```

## Perfiles Disponibles

| Nombre del Perfil | ID del Proyecto | Propósito |
|-------------------|-----------------|-----------|
| `default` | - | Entorno predeterminado |
| `my-profile` | my-gcp-project | Análisis de datos de producción |
| `my-dev` | my-dev-project | Análisis de desarrollo |

---

# Patrón de Invocación del Sub-Agente

El agente principal invoca este sub-agente usando el siguiente patrón:

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Data analysis",
    prompt="""
    Lea y ejecute esta habilidad: skills/data-analyst/SKILL.md
    
    Tarea: {instrucciones del usuario}
    Fuente de datos: {BigQuery / Snowflake / CSV, etc.}
    Propósito del análisis: {EDA / visualización / generación de reportes, etc.}
    
    Devuelva un resumen de los resultados del análisis.
    """
)
```

---

# Formato de Retorno

```yaml
status: success
analysis_type: EDA
data_source: BigQuery (my-dev-project)
summary:
  total_rows: 150000
  columns: 25
  date_range: "2025-01-01 ~ 2025-12-31"
  key_findings:
    - "Promedio de publicaciones diarias: 1,200/día"
    - "Horas pico: 12:00-13:00"
    - "Los fines de semana disminuyen un 30% comparado con días laborales"
visualizations:
  - path: reports/daily_posts.png
    description: "Tendencia del conteo diario de publicaciones"
  - path: reports/hourly_heatmap.png
    description: "Mapa de calor por hora"
notebook:
  path: notebooks/eda_analysis.py
  status: "Creación completada"
```

---

# Dependencias

```txt
marimo>=0.5.0
pandas>=2.0.0
plotly>=5.0.0
matplotlib>=3.7.0
google-cloud-bigquery>=3.0.0
ydata-profiling>=4.0.0
tqdm>=4.65.0
```

---

# Casos de Uso

1. **EDA de BigQuery**: Comprensión de estructura de tablas, estadísticas básicas, análisis de distribución
2. **Análisis de series temporales**: Tendencias, estacionalidad, detección de valores atípicos
3. **Análisis de cohortes**: Segmentos de usuarios, retención
4. **Reportes de visualización**: Dashboards, materiales de presentación
5. **Creación de notebooks Marimo**: Construcción de entornos de análisis interactivos

## Solución de Problemas

| Error | Solución |
|-------|----------|
| Error de autenticación de GCP | Ejecute `gcloud auth application-default login` |
| Tabla de BigQuery no encontrada | Verifique los perfiles con `gcloud config configurations list` y cambie al apropiado |
| Error de redefinición de variable en Marimo | Revise las variables de nivel superior de cada celda y agregue sufijos únicos a los nombres duplicados |

## Criterios de Éxito

- [ ] Se ha devuelto el resumen de resultados del análisis (formato YAML)
- [ ] Los gráficos de visualización incluyen etiquetas, títulos y leyendas en japonés
- [ ] Los archivos de salida están guardados en `data/output/` o `reports/`

## Descripción General

Una habilidad de sub-agente que ejecuta conexiones a BigQuery/Snowflake, EDA (Análisis Exploratorio de Datos), visualización y creación de notebooks Marimo en un contexto dedicado. Integra cuatro reglas para análisis de datos, visualización y creación de notebooks, devolviendo solo resúmenes de resultados de análisis.

## Uso

Consulte las secciones "Patrón de Invocación del Sub-Agente" y "Autenticación de GCP" anteriores. Ejemplo de ejecución básica:

```bash
# Iniciar análisis con un notebook Marimo
marimo edit notebooks/eda_analysis.py
```
