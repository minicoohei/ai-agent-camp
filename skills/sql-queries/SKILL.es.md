---
name: sql-queries
description: "Habilidad para escribir SQL preciso y de alto rendimiento en los principales dialectos de almacenes de datos. Se activa con solicitudes como 'Escribir SQL', 'Optimizar consulta', 'Agregar en BigQuery', etc."
triggers:
  - Escribir SQL
  - Optimizar consulta
  - Agregar en BigQuery
  - Usar funciones de ventana
  - Convertir dialecto SQL
  - sql-queries
  - SQL query
  - Snowflake
---

# Habilidad de Consultas SQL

Escriba SQL correcto, eficiente y legible en todos los principales dialectos de almacenes de datos.

## Referencia por Dialecto

### PostgreSQL (incluyendo Aurora, RDS, Supabase, Neon)

**Fecha/hora:**
```sql
-- Fecha/hora actual
CURRENT_DATE, CURRENT_TIMESTAMP, NOW()

-- Aritmética de fechas
date_column + INTERVAL '7 days'
date_column - INTERVAL '1 month'

-- Truncar a período
DATE_TRUNC('month', created_at)

-- Extraer partes
EXTRACT(YEAR FROM created_at)
EXTRACT(DOW FROM created_at)  -- 0=Domingo

-- Formato
TO_CHAR(created_at, 'YYYY-MM-DD')
```

**Funciones de cadena:**
```sql
-- Concatenación
first_name || ' ' || last_name
CONCAT(first_name, ' ', last_name)

-- Coincidencia de patrones
column ILIKE '%pattern%'  -- sin distinción de mayúsculas
column ~ '^regex_pattern$'  -- regex

-- Manipulación de cadenas
LEFT(str, n), RIGHT(str, n)
SPLIT_PART(str, delimiter, position)
REGEXP_REPLACE(str, pattern, replacement)
```

**Arrays y JSON:**
```sql
-- Acceso a JSON
data->>'key'  -- texto
data->'nested'->'key'  -- json
data#>>'{path,to,key}'  -- texto anidado

-- Operaciones con arrays
ARRAY_AGG(column)
ANY(array_column)
array_column @> ARRAY['value']
```

**Consejos de rendimiento:**
- Use `EXPLAIN ANALYZE` para perfilar consultas
- Cree índices en columnas filtradas/unidas frecuentemente
- Use `EXISTS` en lugar de `IN` para subconsultas correlacionadas
- Índices parciales para condiciones de filtro comunes
- Use connection pooling para acceso concurrente

---

### Snowflake

**Fecha/hora:**
```sql
-- Fecha/hora actual
CURRENT_DATE(), CURRENT_TIMESTAMP(), SYSDATE()

-- Aritmética de fechas
DATEADD(day, 7, date_column)
DATEDIFF(day, start_date, end_date)

-- Truncar a período
DATE_TRUNC('month', created_at)

-- Extraer partes
YEAR(created_at), MONTH(created_at), DAY(created_at)
DAYOFWEEK(created_at)

-- Formato
TO_CHAR(created_at, 'YYYY-MM-DD')
```

**Funciones de cadena:**
```sql
-- Sin distinción de mayúsculas por defecto (depende del collation)
column ILIKE '%pattern%'
REGEXP_LIKE(column, 'pattern')

-- Analizar JSON
column:key::string  -- notación de punto para VARIANT
PARSE_JSON('{"key": "value"}')
GET_PATH(variant_col, 'path.to.key')

-- Aplanar arrays/objetos
SELECT f.value FROM table, LATERAL FLATTEN(input => array_col) f
```

**Datos semiestructurados:**
```sql
-- Acceso a tipo VARIANT
data:customer:name::STRING
data:items[0]:price::NUMBER

-- Aplanar estructuras anidadas
SELECT
    t.id,
    item.value:name::STRING as item_name,
    item.value:qty::NUMBER as quantity
FROM my_table t,
LATERAL FLATTEN(input => t.data:items) item
```

**Consejos de rendimiento:**
- Use claves de clustering en tablas grandes (no índices tradicionales)
- Filtre por columnas de clave de clustering para poda de particiones
- Configure el tamaño apropiado del warehouse para la complejidad de la consulta
- Use `RESULT_SCAN(LAST_QUERY_ID())` para evitar re-ejecutar consultas costosas
- Use tablas transitorias para datos de staging/temporales

---

### BigQuery (Google Cloud)

**Fecha/hora:**
```sql
-- Fecha/hora actual
CURRENT_DATE(), CURRENT_TIMESTAMP()

-- Aritmética de fechas
DATE_ADD(date_column, INTERVAL 7 DAY)
DATE_SUB(date_column, INTERVAL 1 MONTH)
DATE_DIFF(end_date, start_date, DAY)
TIMESTAMP_DIFF(end_ts, start_ts, HOUR)

-- Truncar a período
DATE_TRUNC(created_at, MONTH)
TIMESTAMP_TRUNC(created_at, HOUR)

-- Extraer partes
EXTRACT(YEAR FROM created_at)
EXTRACT(DAYOFWEEK FROM created_at)  -- 1=Domingo

-- Formato
FORMAT_DATE('%Y-%m-%d', date_column)
FORMAT_TIMESTAMP('%Y-%m-%d %H:%M:%S', ts_column)
```

**Funciones de cadena:**
```sql
-- Sin ILIKE, use LOWER()
LOWER(column) LIKE '%pattern%'
REGEXP_CONTAINS(column, r'pattern')
REGEXP_EXTRACT(column, r'pattern')

-- Manipulación de cadenas
SPLIT(str, delimiter)  -- devuelve ARRAY
ARRAY_TO_STRING(array, delimiter)
```

**Arrays y structs:**
```sql
-- Operaciones con arrays
ARRAY_AGG(column)
UNNEST(array_column)
ARRAY_LENGTH(array_column)
value IN UNNEST(array_column)

-- Acceso a struct
struct_column.field_name
```

**Consejos de rendimiento:**
- Siempre filtre por columnas de partición (generalmente fecha) para reducir bytes escaneados
- Use clustering para columnas filtradas frecuentemente dentro de particiones
- Use `APPROX_COUNT_DISTINCT()` para estimaciones de cardinalidad a gran escala
- Evite `SELECT *` -- la facturación es por byte escaneado
- Use `DECLARE` y `SET` para scripts parametrizados
- Previsualice el costo de la consulta con dry run antes de ejecutar consultas grandes

---

### Redshift (Amazon)

**Fecha/hora:**
```sql
-- Fecha/hora actual
CURRENT_DATE, GETDATE(), SYSDATE

-- Aritmética de fechas
DATEADD(day, 7, date_column)
DATEDIFF(day, start_date, end_date)

-- Truncar a período
DATE_TRUNC('month', created_at)

-- Extraer partes
EXTRACT(YEAR FROM created_at)
DATE_PART('dow', created_at)
```

**Funciones de cadena:**
```sql
-- Sin distinción de mayúsculas
column ILIKE '%pattern%'
REGEXP_INSTR(column, 'pattern') > 0

-- Manipulación de cadenas
SPLIT_PART(str, delimiter, position)
LISTAGG(column, ', ') WITHIN GROUP (ORDER BY column)
```

**Consejos de rendimiento:**
- Diseñe claves de distribución para joins colocados (DISTKEY)
- Use claves de ordenamiento para columnas filtradas frecuentemente (SORTKEY)
- Use `EXPLAIN` para verificar el plan de consulta
- Evite movimiento de datos entre nodos (observe DS_BCAST y DS_DIST)
- Ejecute `ANALYZE` y `VACUUM` regularmente
- Use vistas de enlace tardío para flexibilidad de esquema

---

### Databricks SQL

**Fecha/hora:**
```sql
-- Fecha/hora actual
CURRENT_DATE(), CURRENT_TIMESTAMP()

-- Aritmética de fechas
DATE_ADD(date_column, 7)
DATEDIFF(end_date, start_date)
ADD_MONTHS(date_column, 1)

-- Truncar a período
DATE_TRUNC('MONTH', created_at)
TRUNC(date_column, 'MM')

-- Extraer partes
YEAR(created_at), MONTH(created_at)
DAYOFWEEK(created_at)
```

**Características de Delta Lake:**
```sql
-- Viaje en el tiempo
SELECT * FROM my_table TIMESTAMP AS OF '2024-01-15'
SELECT * FROM my_table VERSION AS OF 42

-- Describir historial
DESCRIBE HISTORY my_table

-- Merge (upsert)
MERGE INTO target USING source
ON target.id = source.id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```

**Consejos de rendimiento:**
- Use `OPTIMIZE` y `ZORDER` de Delta Lake para rendimiento de consultas
- Aproveche el motor Photon para consultas intensivas en cómputo
- Use `CACHE TABLE` para conjuntos de datos de acceso frecuente
- Particione por columnas de fecha de baja cardinalidad

---

## Patrones Comunes de SQL

### Funciones de Ventana

```sql
-- Ranking
ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC)
RANK() OVER (PARTITION BY category ORDER BY revenue DESC)
DENSE_RANK() OVER (ORDER BY score DESC)

-- Totales acumulados / promedios móviles
SUM(revenue) OVER (ORDER BY date_col ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total
AVG(revenue) OVER (ORDER BY date_col ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg_7d

-- Lag / Lead
LAG(value, 1) OVER (PARTITION BY entity ORDER BY date_col) as prev_value
LEAD(value, 1) OVER (PARTITION BY entity ORDER BY date_col) as next_value

-- Primer / Último valor
FIRST_VALUE(status) OVER (PARTITION BY user_id ORDER BY created_at ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
LAST_VALUE(status) OVER (PARTITION BY user_id ORDER BY created_at ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)

-- Porcentaje del total
revenue / SUM(revenue) OVER () as pct_of_total
revenue / SUM(revenue) OVER (PARTITION BY category) as pct_of_category
```

### CTEs para Legibilidad

```sql
WITH
-- Paso 1: Definir la población base
base_users AS (
    SELECT user_id, created_at, plan_type
    FROM users
    WHERE created_at >= DATE '2024-01-01'
      AND status = 'active'
),

-- Paso 2: Calcular métricas a nivel de usuario
user_metrics AS (
    SELECT
        u.user_id,
        u.plan_type,
        COUNT(DISTINCT e.session_id) as session_count,
        SUM(e.revenue) as total_revenue
    FROM base_users u
    LEFT JOIN events e ON u.user_id = e.user_id
    GROUP BY u.user_id, u.plan_type
),

-- Paso 3: Agregar a nivel de resumen
summary AS (
    SELECT
        plan_type,
        COUNT(*) as user_count,
        AVG(session_count) as avg_sessions,
        SUM(total_revenue) as total_revenue
    FROM user_metrics
    GROUP BY plan_type
)

SELECT * FROM summary ORDER BY total_revenue DESC;
```

### Retención de Cohortes

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', first_activity_date) as cohort_month
    FROM users
),
activity AS (
    SELECT
        user_id,
        DATE_TRUNC('month', activity_date) as activity_month
    FROM user_activity
)
SELECT
    c.cohort_month,
    COUNT(DISTINCT c.user_id) as cohort_size,
    COUNT(DISTINCT CASE
        WHEN a.activity_month = c.cohort_month THEN a.user_id
    END) as month_0,
    COUNT(DISTINCT CASE
        WHEN a.activity_month = c.cohort_month + INTERVAL '1 month' THEN a.user_id
    END) as month_1,
    COUNT(DISTINCT CASE
        WHEN a.activity_month = c.cohort_month + INTERVAL '3 months' THEN a.user_id
    END) as month_3
FROM cohorts c
LEFT JOIN activity a ON c.user_id = a.user_id
GROUP BY c.cohort_month
ORDER BY c.cohort_month;
```

### Análisis de Embudo

```sql
WITH funnel AS (
    SELECT
        user_id,
        MAX(CASE WHEN event = 'page_view' THEN 1 ELSE 0 END) as step_1_view,
        MAX(CASE WHEN event = 'signup_start' THEN 1 ELSE 0 END) as step_2_start,
        MAX(CASE WHEN event = 'signup_complete' THEN 1 ELSE 0 END) as step_3_complete,
        MAX(CASE WHEN event = 'first_purchase' THEN 1 ELSE 0 END) as step_4_purchase
    FROM events
    WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)
SELECT
    COUNT(*) as total_users,
    SUM(step_1_view) as viewed,
    SUM(step_2_start) as started_signup,
    SUM(step_3_complete) as completed_signup,
    SUM(step_4_purchase) as purchased,
    ROUND(100.0 * SUM(step_2_start) / NULLIF(SUM(step_1_view), 0), 1) as view_to_start_pct,
    ROUND(100.0 * SUM(step_3_complete) / NULLIF(SUM(step_2_start), 0), 1) as start_to_complete_pct,
    ROUND(100.0 * SUM(step_4_purchase) / NULLIF(SUM(step_3_complete), 0), 1) as complete_to_purchase_pct
FROM funnel;
```

### Deduplicación

```sql
-- Mantener el registro más reciente por clave
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY entity_id
            ORDER BY updated_at DESC
        ) as rn
    FROM source_table
)
SELECT * FROM ranked WHERE rn = 1;
```

## Manejo de Errores y Depuración

Cuando una consulta falla:

1. **Errores de sintaxis**: Verifique la sintaxis específica del dialecto (por ejemplo, `ILIKE` no disponible en BigQuery, `SAFE_DIVIDE` solo en BigQuery)
2. **Columna no encontrada**: Verifique los nombres de columna contra el esquema -- revise errores tipográficos, sensibilidad a mayúsculas (PostgreSQL distingue mayúsculas en identificadores entrecomillados)
3. **Incompatibilidad de tipos**: Convierta explícitamente al comparar tipos diferentes (`CAST(col AS DATE)`, `col::DATE`)
4. **División por cero**: Use `NULLIF(denominator, 0)` o división segura específica del dialecto
5. **Columnas ambiguas**: Siempre califique los nombres de columna con alias de tabla en JOINs
6. **Errores de GROUP BY**: Todas las columnas no agregadas deben estar en GROUP BY (excepto en BigQuery que permite agrupar por alias)
