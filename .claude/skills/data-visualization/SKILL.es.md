---
name: data-visualization
description: "Habilidad para visualización de datos usando Python (matplotlib, seaborn, plotly). Se activa con solicitudes como 'crea un gráfico,' 'hacer una gráfica,' 'visualiza los datos,' etc. Incluye selección de gráficos, principios de diseño y consideraciones de accesibilidad."
source: github.com/anthropics/knowledge-work-plugins@main
triggers:
  - data-visualization
  - グラフを作って
  - チャート作成
  - データ可視化
  - 可視化して
  - matplotlib
  - plotly
---

# Habilidad de Visualización de Datos

Guía de selección de gráficos, patrones de código de visualización en Python, principios de diseño y consideraciones de accesibilidad para crear visualizaciones de datos efectivas.

## Guía de Selección de Gráficos

### Elegir por Relación de Datos

| Lo Que Muestra | Mejor Gráfico | Alternativas |
|---|---|---|
| **Tendencia en el tiempo** | Gráfico de líneas | Gráfico de área (si muestra acumulativo o composición) |
| **Comparación entre categorías** | Gráfico de barras vertical | Barras horizontales (muchas categorías), gráfico de piruleta |
| **Ranking** | Gráfico de barras horizontal | Gráfico de puntos, gráfico de pendiente (comparando dos períodos) |
| **Composición parte-del-todo** | Gráfico de barras apiladas | Treemap (jerárquico), gráfico waffle |
| **Composición en el tiempo** | Gráfico de área apilada | Barras apiladas al 100% (para enfoque en proporciones) |
| **Distribución** | Histograma | Diagrama de caja (comparando grupos), gráfico de violín, gráfico de tiras |
| **Correlación (2 variables)** | Gráfico de dispersión | Gráfico de burbujas (añadir 3a variable como tamaño) |
| **Correlación (muchas variables)** | Mapa de calor (matriz de correlación) | Gráfico de pares |
| **Patrones geográficos** | Mapa coroplético | Mapa de burbujas, mapa hexagonal |
| **Flujo / proceso** | Diagrama Sankey | Gráfico de embudo (etapas secuenciales) |
| **Red de relaciones** | Grafo de red | Diagrama de cuerdas |
| **Rendimiento vs. objetivo** | Gráfico bullet | Indicador (solo para un KPI) |
| **Múltiples KPI a la vez** | Múltiplos pequeños | Dashboard con gráficos separados |

### Cuándo NO Usar Ciertos Gráficos

- **Gráficos circulares**: Evite a menos que haya <6 categorías y las proporciones exactas importen menos que la comparación aproximada. Los humanos son malos comparando ángulos. Use gráficos de barras en su lugar.
- **Gráficos 3D**: Nunca. Distorsionan la percepción y no añaden información.
- **Gráficos de doble eje**: Use con precaución. Pueden engañar al implicar correlación. Etiquete claramente ambos ejes si los usa.
- **Barras apiladas (muchas categorías)**: Difícil comparar segmentos intermedios. Use múltiplos pequeños o barras agrupadas en su lugar.
- **Gráficos de dona**: Ligeramente mejores que los gráficos circulares pero con los mismos problemas fundamentales. Use como máximo para mostrar un solo KPI.

## Patrones de Código de Visualización en Python

### Configuración y Estilo

```python
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd
import numpy as np

# Configuración de estilo profesional
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.figsize': (10, 6),
    'figure.dpi': 150,
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
})

# Paletas amigables para daltonismo
PALETTE_CATEGORICAL = ['#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8172B3', '#937860']
PALETTE_SEQUENTIAL = 'YlOrRd'
PALETTE_DIVERGING = 'RdBu_r'
```

### Gráfico de Líneas (Series Temporales)

```python
fig, ax = plt.subplots(figsize=(10, 6))

for label, group in df.groupby('category'):
    ax.plot(group['date'], group['value'], label=label, linewidth=2)

ax.set_title('Tendencia de Métrica por Categoría', fontweight='bold')
ax.set_xlabel('Fecha')
ax.set_ylabel('Valor')
ax.legend(loc='upper left', frameon=True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Formatear fechas en el eje x
fig.autofmt_xdate()

plt.tight_layout()
plt.savefig('trend_chart.png', dpi=150, bbox_inches='tight')
```

### Gráfico de Barras (Comparación)

```python
fig, ax = plt.subplots(figsize=(10, 6))

# Ordenar por valor para fácil lectura
df_sorted = df.sort_values('metric', ascending=True)

bars = ax.barh(df_sorted['category'], df_sorted['metric'], color=PALETTE_CATEGORICAL[0])

# Añadir etiquetas de valor
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
            f'{width:,.0f}', ha='left', va='center', fontsize=10)

ax.set_title('Métrica por Categoría (Clasificado)', fontweight='bold')
ax.set_xlabel('Valor de la Métrica')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('bar_chart.png', dpi=150, bbox_inches='tight')
```

### Histograma (Distribución)

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(df['value'], bins=30, color=PALETTE_CATEGORICAL[0], edgecolor='white', alpha=0.8)

# Añadir líneas de media y mediana
mean_val = df['value'].mean()
median_val = df['value'].median()
ax.axvline(mean_val, color='red', linestyle='--', linewidth=1.5, label=f'Media: {mean_val:,.1f}')
ax.axvline(median_val, color='green', linestyle='--', linewidth=1.5, label=f'Mediana: {median_val:,.1f}')

ax.set_title('Distribución de Valores', fontweight='bold')
ax.set_xlabel('Valor')
ax.set_ylabel('Frecuencia')
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('histogram.png', dpi=150, bbox_inches='tight')
```

### Mapa de Calor

```python
fig, ax = plt.subplots(figsize=(10, 8))

# Pivotar datos para formato de mapa de calor
pivot = df.pivot_table(index='row_dim', columns='col_dim', values='metric', aggfunc='sum')

sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Valor de la Métrica'})

ax.set_title('Métrica por Dimensión de Fila y Dimensión de Columna', fontweight='bold')
ax.set_xlabel('Dimensión de Columna')
ax.set_ylabel('Dimensión de Fila')

plt.tight_layout()
plt.savefig('heatmap.png', dpi=150, bbox_inches='tight')
```

### Múltiplos Pequeños

```python
categories = df['category'].unique()
n_cats = len(categories)
n_cols = min(3, n_cats)
n_rows = (n_cats + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows), sharex=True, sharey=True)
axes = axes.flatten() if n_cats > 1 else [axes]

for i, cat in enumerate(categories):
    ax = axes[i]
    subset = df[df['category'] == cat]
    ax.plot(subset['date'], subset['value'], color=PALETTE_CATEGORICAL[i % len(PALETTE_CATEGORICAL)])
    ax.set_title(cat, fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

# Ocultar subgráficos vacíos
for j in range(i+1, len(axes)):
    axes[j].set_visible(False)

fig.suptitle('Tendencias por Categoría', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('small_multiples.png', dpi=150, bbox_inches='tight')
```

### Funciones Auxiliares de Formato Numérico

```python
def format_number(val, format_type='number'):
    """Formatear números para etiquetas de gráficos."""
    if format_type == 'currency':
        if abs(val) >= 1e9:
            return f'${val/1e9:.1f}B'
        elif abs(val) >= 1e6:
            return f'${val/1e6:.1f}M'
        elif abs(val) >= 1e3:
            return f'${val/1e3:.1f}K'
        else:
            return f'${val:,.0f}'
    elif format_type == 'percent':
        return f'{val:.1f}%'
    elif format_type == 'number':
        if abs(val) >= 1e9:
            return f'{val/1e9:.1f}B'
        elif abs(val) >= 1e6:
            return f'{val/1e6:.1f}M'
        elif abs(val) >= 1e3:
            return f'{val/1e3:.1f}K'
        else:
            return f'{val:,.0f}'
    return str(val)

# Uso con formateador de eje
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, p: format_number(x, 'currency')))
```

### Gráficos Interactivos con Plotly

```python
import plotly.express as px
import plotly.graph_objects as go

# Gráfico de líneas interactivo simple
fig = px.line(df, x='date', y='value', color='category',
              title='Tendencia Interactiva de Métrica',
              labels={'value': 'Valor de la Métrica', 'date': 'Fecha'})
fig.update_layout(hovermode='x unified')
fig.write_html('interactive_chart.html')
fig.show()

# Dispersión interactiva con datos al pasar el cursor
fig = px.scatter(df, x='metric_a', y='metric_b', color='category',
                 size='size_metric', hover_data=['name', 'detail_field'],
                 title='Análisis de Correlación')
fig.show()
```

## Principios de Diseño

### Color

- **Use el color con propósito**: El color debe codificar datos, no decorar
- **Resalte la historia**: Use un color de acento brillante para el insight clave; ponga en gris todo lo demás
- **Datos secuenciales**: Use un gradiente de un solo tono (claro a oscuro) para valores ordenados
- **Datos divergentes**: Use un gradiente de dos tonos con punto medio neutral para datos con un centro significativo
- **Datos categóricos**: Use tonos distintos, máximo 6-8 antes de que se vuelva confuso
- **Evite solo rojo/verde**: El 8% de los hombres son daltónicos rojo-verde. Use azul/naranja como par principal

### Tipografía

- **El título declara el insight**: "Los ingresos crecieron 23% interanual" supera a "Ingresos por Mes"
- **El subtítulo añade contexto**: Rango de fechas, filtros aplicados, fuente de datos
- **Las etiquetas de ejes son legibles**: Nunca rotadas 90 grados si es evitable. Acorte o ajuste en su lugar
- **Las etiquetas de datos añaden precisión**: Use en puntos clave, no en cada barra
- **Las anotaciones resaltan**: Señale puntos específicos con anotaciones de texto

### Diseño

- **Reduzca el ruido gráfico**: Elimine líneas de cuadrícula, bordes, fondos que no llevan información
- **Ordene significativamente**: Categorías ordenadas por valor (no alfabéticamente) a menos que haya un orden natural (meses, etapas)
- **Relación de aspecto apropiada**: Series temporales más anchas que altas (3:1 a 2:1); las comparaciones pueden ser más cuadradas
- **El espacio en blanco es bueno**: No apriete los gráficos. Dé a cada visualización espacio para respirar

### Precisión

- **Los gráficos de barras comienzan en cero**: Siempre. Una barra de 95 a 100 exagera una diferencia del 5%
- **Los gráficos de líneas pueden tener líneas base distintas de cero**: Cuando el rango de variación es significativo
- **Escalas consistentes entre paneles**: Al comparar múltiples gráficos, use el mismo rango de ejes
- **Muestre la incertidumbre**: Barras de error, intervalos de confianza o rangos cuando los datos son inciertos
- **Etiquete sus ejes**: Nunca haga que el lector adivine qué significan los números

## Consideraciones de Accesibilidad

### Daltonismo

- Nunca dependa solo del color para distinguir series de datos
- Añada rellenos con patrones, diferentes estilos de línea (sólida, discontinua, punteada) o etiquetas directas
- Pruebe con un simulador de daltonismo (por ejemplo, Coblis, Sim Daltonism)
- Use la paleta amigable para daltonismo: `sns.color_palette("colorblind")`

### Lectores de Pantalla

- Incluya texto alternativo describiendo el hallazgo clave del gráfico
- Proporcione una tabla de datos alternativa junto a la visualización
- Use títulos y etiquetas semánticos

### Accesibilidad General

- Contraste suficiente entre elementos de datos y fondo
- Tamaño de texto mínimo de 10pt para etiquetas, 12pt para títulos
- Evite transmitir información solo a través de posición espacial (añada etiquetas)
- Considere la impresión: ¿funciona el gráfico en blanco y negro?

### Lista de Verificación de Accesibilidad

Antes de compartir una visualización:
- [ ] El gráfico funciona sin color (patrones, etiquetas o estilos de línea diferencian las series)
- [ ] El texto es legible al nivel de zoom estándar
- [ ] El título describe el insight, no solo los datos
- [ ] Los ejes están etiquetados con unidades
- [ ] La leyenda es clara y posicionada sin ocultar datos
- [ ] La fuente de datos y el rango de fechas están anotados
