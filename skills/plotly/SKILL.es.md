---
name: plotly
description: "Skill para crear gráficos interactivos y dashboards con Plotly. Compatible con hover, zoom y desplazamiento. Se activa con solicitudes como 'gráfico interactivo', 'chart con plotly', 'gráfico dinámico', etc."
triggers:
  - crear un gráfico interactivo
  - crear un chart con plotly
  - gráfico interactivo
  - plotly
  - gráfico para dashboard
  - gráfico dinámico
license: MIT license
metadata:
    skill-author: K-Dense Inc.
source: github.com/K-Dense-AI/claude-scientific-skills@main
---

# Plotly

Biblioteca de gráficos en Python para crear visualizaciones interactivas de calidad profesional con más de 40 tipos de gráficos.

## Inicio Rápido

Instalar Plotly:
```bash
uv add plotly
```

Uso básico con Plotly Express (API de alto nivel):
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = px.scatter(df, x='x', y='y', title='Mi Primer Gráfico')
fig.show()
```

## Elegir Entre APIs

### Usar Plotly Express (px)
Para visualizaciones rápidas y estándar con valores predeterminados razonables:
- Trabajar con DataFrames de pandas
- Crear tipos de gráficos comunes (scatter, línea, barra, histograma, etc.)
- Necesidad de codificación automática de colores y leyendas
- Querer código mínimo (1-5 líneas)

Consulte [reference/plotly-express.md](reference/plotly-express.md) para la guía completa.

### Usar Graph Objects (go)
Para control detallado y visualizaciones personalizadas:
- Tipos de gráficos no disponibles en Plotly Express (malla 3D, isosuperficie, gráficos financieros complejos)
- Construir figuras complejas multi-traza desde cero
- Necesidad de control preciso sobre componentes individuales
- Crear visualizaciones especializadas con formas y anotaciones personalizadas

Consulte [reference/graph-objects.md](reference/graph-objects.md) para la guía completa.

**Nota:** Plotly Express devuelve objetos Figure de graph objects, por lo que puede combinar enfoques:
```python
fig = px.scatter(df, x='x', y='y')
fig.update_layout(title='Título Personalizado')  # Usar métodos de go en figura de px
fig.add_hline(y=10)                               # Agregar formas
```

## Capacidades Principales

### 1. Tipos de Gráficos

Plotly soporta más de 40 tipos de gráficos organizados en categorías:

**Gráficos Básicos:** scatter, línea, barra, circular, área, burbuja

**Gráficos Estadísticos:** histograma, diagrama de caja, violín, distribución, barras de error

**Gráficos Científicos:** mapa de calor, contorno, ternario, visualización de imágenes

**Gráficos Financieros:** velas, OHLC, cascada, embudo, series temporales

**Mapas:** mapas de dispersión, coropletas, mapas de densidad (visualización geográfica)

**Gráficos 3D:** scatter3d, superficie, malla, cono, volumen

**Especializados:** sunburst, treemap, sankey, coordenadas paralelas, indicador

Para ejemplos detallados y uso de todos los tipos de gráficos, consulte [reference/chart-types.md](reference/chart-types.md).

### 2. Diseños y Estilos

**Subgráficos:** Crear figuras multi-gráfico con ejes compartidos:
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=2, subplot_titles=('A', 'B', 'C', 'D'))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
```

**Plantillas:** Aplicar estilos coordinados:
```python
fig = px.scatter(df, x='x', y='y', template='plotly_dark')
# Incluidas: plotly_white, plotly_dark, ggplot2, seaborn, simple_white
```

**Personalización:** Controlar cada aspecto de la apariencia:
- Colores (secuencias discretas, escalas continuas)
- Fuentes y texto
- Ejes (rangos, marcas, cuadrículas)
- Leyendas
- Márgenes y dimensionamiento
- Anotaciones y formas

Para opciones completas de diseño y estilos, consulte [reference/layouts-styling.md](reference/layouts-styling.md).

### 3. Interactividad

Funciones interactivas integradas:
- Tooltips de hover con datos personalizables
- Desplazamiento y zoom
- Alternancia de leyenda
- Selección de caja/lazo
- Rangesliders para series temporales
- Botones y menús desplegables
- Animaciones

```python
# Plantilla de hover personalizada
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Valor: %{y:.2f}<extra></extra>'
)

# Agregar rangeslider
fig.update_xaxes(rangeslider_visible=True)

# Animaciones
fig = px.scatter(df, x='x', y='y', animation_frame='year')
```

Para la guía completa de interactividad, consulte [reference/export-interactivity.md](reference/export-interactivity.md).

### 4. Opciones de Exportación

**HTML Interactivo:**
```python
fig.write_html('chart.html')                       # Independiente completo
fig.write_html('chart.html', include_plotlyjs='cdn')  # Archivo más pequeño
```

**Imágenes Estáticas (requiere kaleido):**
```bash
uv add kaleido
```

```python
fig.write_image('chart.png')   # PNG
fig.write_image('chart.pdf')   # PDF
fig.write_image('chart.svg')   # SVG
```

Para opciones completas de exportación, consulte [reference/export-interactivity.md](reference/export-interactivity.md).

## Flujos de Trabajo Comunes

### Visualización de Datos Científicos

```python
import plotly.express as px

# Gráfico de dispersión con línea de tendencia
fig = px.scatter(df, x='temperature', y='yield', trendline='ols')

# Mapa de calor desde matriz
fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu')

# Gráfico de superficie 3D
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data)])
```

### Análisis Estadístico

```python
# Comparación de distribuciones
fig = px.histogram(df, x='values', color='group', marginal='box', nbins=30)

# Diagrama de caja con todos los puntos
fig = px.box(df, x='category', y='value', points='all')

# Gráfico de violín
fig = px.violin(df, x='group', y='measurement', box=True)
```

### Series Temporales y Financieras

```python
# Serie temporal con rangeslider
fig = px.line(df, x='date', y='price')
fig.update_xaxes(rangeslider_visible=True)

# Gráfico de velas
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### Dashboards Multi-Gráfico

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Dispersión', 'Barras', 'Histograma', 'Caja'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'box'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2]), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Box(y=data), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
```

## Integración con Dash

Para aplicaciones web interactivas, use Dash (framework de apps web de Plotly):

```bash
uv add dash
```

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    html.H1('Dashboard'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

## Archivos de Referencia

- **[plotly-express.md](reference/plotly-express.md)** - API de alto nivel para visualizaciones rápidas
- **[graph-objects.md](reference/graph-objects.md)** - API de bajo nivel para control detallado
- **[chart-types.md](reference/chart-types.md)** - Catálogo completo de más de 40 tipos de gráficos con ejemplos
- **[layouts-styling.md](reference/layouts-styling.md)** - Subgráficos, plantillas, colores, personalización
- **[export-interactivity.md](reference/export-interactivity.md)** - Opciones de exportación y funciones interactivas

## Recursos Adicionales

- Documentación oficial: https://plotly.com/python/
- Referencia de API: https://plotly.com/python-api-reference/
- Foro de la comunidad: https://community.plotly.com/
