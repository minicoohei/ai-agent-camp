---
name: x-research
version: 1.0.0
author: ai-agent-camp
description: "Realiza búsquedas en tiempo real en X (Twitter) para recopilar y analizar tweets sobre un tema. Produce resultados de búsqueda como informes estructurados (Markdown + JSON + TXT). Se activa con 'Buscar en X', 'Investigar en Twitter', 'Analizar tweets', etc."
triggers:
  - Buscar en X
  - Investigar en Twitter
  - Analizar tweets
  - Verificar reacciones en X
  - Investigación de redes sociales
  - Investigar tendencias
  - x-research
  - search tweets
dependencies:
  - requests>=2.28.0
  - python-dotenv>=0.19.0
---

# X Research - Búsqueda y Análisis en Tiempo Real de X (Twitter)

## Descripción

Utiliza el endpoint de Búsqueda Reciente de la API X v2 para buscar, recopilar y analizar tweets en tiempo real sobre un tema especificado.
Clasifica los tweets obtenidos por engagement y produce informes estructurados incluyendo análisis de hashtags, distribución temporal y lista de URLs compartidas
en formatos Markdown + JSON + texto plano.

## Inicio Rápido

```bash
# Búsqueda básica
python skills/x-research/scripts/x_research.py --topic "IA generativa"

# Buscar en inglés, excluir retweets
python skills/x-research/scripts/x_research.py --topic "Claude AI" --lang en --no-retweets

# Últimos 3 días, ordenados por relevancia
python skills/x-research/scripts/x_research.py --topic "OpenAI" --days 3 --sort relevancy
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| --topic, -t | Sí | - | Tema/palabra clave de búsqueda |
| --query, -q | No | auto | Consulta de búsqueda personalizada (especificar directamente en lugar de topic) |
| --lang, -l | No | ja | Filtro de idioma: ja, en, all |
| --days, -d | No | 7 | Período de búsqueda (días, máximo 7) |
| --sort, -s | No | relevancy | Ordenar: relevancy, recency |
| --no-retweets | No | false | Excluir retweets |
| --no-replies | No | false | Excluir respuestas |
| --media-only | No | false | Solo tweets con medios adjuntos |
| --from-user | No | - | Solo tweets de usuario específico |
| --min-likes | No | 0 | Mínimo de likes (filtro post-obtención) |
| --max-results, -m | No | 50 | Máximo de resultados por página (máximo 100) |
| --max-pages | No | 3 | Máximo de páginas |
| --top-n | No | 10 | Número de tweets principales a mostrar |
| --output, -o | No | output/x-research/ | Directorio de salida |
| --session | No | auto | Nombre de sesión (usado en nombre de carpeta de salida) |
| --dry-run | No | false | Solo mostrar consulta sin ejecutar |
| --raw-json | No | false | Producir respuesta cruda de API a stderr |

## Guía de Sintaxis de Consulta

Al especificar directamente con `--query`, se pueden usar operadores de búsqueda de X API v2:

| Operador | Ejemplo | Descripción |
|----------|---------|-------------|
| palabra clave | `IA generativa` | Búsqueda básica por palabra clave |
| "frase" | `"Claude Code"` | Coincidencia exacta de frase |
| from: | `from:OpenAI` | Publicaciones de usuario específico |
| to: | `to:username` | Menciones a usuario específico |
| -is:retweet | `-is:retweet` | Excluir retweets |
| -is:reply | `-is:reply` | Excluir respuestas |
| has:media | `has:media` | Solo con medios adjuntos |
| has:links | `has:links` | Solo con enlaces adjuntos |
| lang: | `lang:ja` | Especificación de idioma |
| #hashtag | `#IA` | Búsqueda por hashtag |
| OR | `IA OR inteligencia artificial` | Búsqueda OR |
| -keyword | `-publicidad` | Excluir palabra clave |

## Formato de Salida

Se generan tres archivos en `output/x-research/YYYYMMDD_HHMMSS_{topic}/`:

1. **`{topic}_report.md`** - Informe Markdown
   - Estadísticas de resumen (cantidad de tweets, usuarios únicos, total de likes, etc.)
   - Tweets principales (por engagement)
   - Análisis de hashtags
   - Distribución temporal
   - Lista de URLs compartidas

2. **`{topic}_data.json`** - JSON estructurado
   - Metadatos (consulta, parámetros, marca de tiempo de generación)
   - Estadísticas
   - Datos de todos los tweets (texto, métricas, información del autor)

3. **`{topic}_raw.txt`** - Resumen en texto plano

## Ejemplos de Uso

```bash
# Buscar "IA generativa" en japonés (configuración predeterminada)
python skills/x-research/scripts/x_research.py --topic "IA generativa"

# Buscar "Claude" en inglés, excluir retweets/respuestas
python skills/x-research/scripts/x_research.py \
  --topic "Claude AI" --lang en --no-retweets --no-replies

# Buscar publicaciones de usuario específico
python skills/x-research/scripts/x_research.py \
  --topic "AI" --from-user AnthropicAI --lang en

# Solo tweets con medios adjuntos, últimos 3 días
python skills/x-research/scripts/x_research.py \
  --topic "AI art" --media-only --days 3 --lang en

# Búsqueda avanzada con consulta personalizada
python skills/x-research/scripts/x_research.py \
  --query '"Claude Code" OR "Cursor AI" -is:retweet lang:en' --topic "AI IDE"

# Dry-run para verificar consulta
python skills/x-research/scripts/x_research.py \
  --topic "prueba" --no-retweets --lang ja --dry-run
```

## Configuración del Entorno

### Requerido: Token Bearer de X

```bash
# Agregar a .env
X_BEARER_TOKEN=your_bearer_token_here
```

Cómo obtener:
1. Visite el [Portal de Desarrolladores de X](https://developer.x.com/en/portal/dashboard)
2. Cree un proyecto/app
3. Obtenga el Bearer Token
4. Agregue `X_BEARER_TOKEN=...` al archivo `.env`

### Límites de API

| Plan | Límite de Búsqueda | Período |
|------|-------------------|---------|
| Gratuito | No disponible | - |
| Basic ($100/mes) | 60 solicitudes/15 min | Últimos 7 días |
| Pro ($5,000/mes) | 300 solicitudes/15 min | Últimos 7 días |

## Ejemplo de Salida

```
=== Salida Completa ===
  Markdown: output/x-research/20260210_053000_IA_generativa/IA_generativa_report.md
  JSON:     output/x-research/20260210_053000_IA_generativa/IA_generativa_data.json
  Text:     output/x-research/20260210_053000_IA_generativa/IA_generativa_raw.txt

--- Resumen ---
  Cantidad de tweets: 30
  Autores únicos:     28
  Total de likes:     1,234
  Total de retweets:  56
  Total de respuestas: 12
  Período:            2026-02-03 ~ 2026-02-10
```

## Dependencias

```text
requests>=2.28.0
python-dotenv>=0.19.0
```
