---
name: csv-analyzer
description: "Habilidad para obtener el conteo de filas/columnas, estimar tipos de datos, detectar valores faltantes y generar información estadística de columnas numéricas en archivos CSV. Se activa con solicitudes como 'analiza el CSV,' 'verifica el contenido del CSV,' 'muéstrame un resumen de los datos,' etc."
triggers:
  - csv-analyzer
  - CSV分析
  - CSVファイル解析
  - データ概要
  - 欠損値チェック
  - CSV統計
  - CSVプロファイリング
---

## Palabras Clave de Activación
"Análisis CSV," "Análisis de archivo CSV," "Resumen de datos," "Verificación de valores faltantes," "Estadísticas CSV"

# Habilidad de Análisis de CSV

## Descripción General
Una habilidad que analiza archivos CSV y realiza estimación de tipos de datos e información estadística.

## Funcionalidades
- Obtención del conteo de filas y columnas
- Estimación de tipos de datos (detección automática del tipo de cada columna)
- Información estadística (estadísticas básicas para columnas numéricas)
- Detección de valores faltantes (detección de valores NULL y NA)
- Detección de codificación

## Uso

### Ejecución por Línea de Comandos
```bash
python skills/csv-analyzer/scripts/analyzer.py --input data.csv
```

### Uso en Python
```python
from scripts.analyzer import CSVAnalyzer

analyzer = CSVAnalyzer("data.csv")
result = analyzer.analyze()
print(result)
```

## Formato de Salida
```json
{
  "filename": "data.csv",
  "rows": 1000,
  "columns": 5,
  "encoding": "utf-8",
  "file_size_mb": 2.5,
  "columns_info": []
}
```

## Dependencias
- pandas >= 2.0
- chardet >= 5.0

## Instalación
```bash
uv sync
```
