---
name: content-optimizer
version: 1.0.0
author: ai-agent-camp
description: "Habilidad de planificacion para apoyar pruebas A/B de contenido y ciclos de auto-mejora. Cubre el ciclo completo de investigacion de tendencias de mercado -> generacion de hipotesis -> diseno de experimentos -> recopilacion de metricas -> analisis y mejora. Se activa con solicitudes como 'optimizar contenido', 'mejorar publicaciones', 'crear ideas de publicaciones a partir del analisis de tendencias', 'mejorar engagement', etc."
triggers:
  - content-optimizer
  - optimizar contenido
  - mejorar publicaciones
  - analisis de tendencias
  - mejorar engagement
  - ciclo de mejora de contenido
  - Typefully
  - content optimization
  - コンテンツを最適化
---

# Optimizador de Rendimiento de Contenido - Ciclo de Auto-Mejora de Contenido

## Descripcion

Recopila datos de mercado de 5 fuentes (X, Google Search, Google Trends, Reddit/HN, cuentas de competidores),
realiza analisis integrado con LLM y genera automaticamente hipotesis y variantes A/B.
Registra las variantes de publicaciones generadas como borradores en Typefully, mide el rendimiento posterior a la publicacion y aprende,
habilitando un ciclo de auto-mejora continua para el contenido.

## Descripcion General del Flujo de Trabajo

```
1. Investigacion de mercado -> 2. Generacion de hipotesis -> 3. Creacion de variantes -> 4. Publicacion (Typefully) -> 5. Recopilacion de metricas -> 6. Analisis y aprendizaje -> Volver a 1.
```

## Inicio Rapido

```bash
# Generacion de hipotesis (de extremo a extremo: investigacion de tendencias -> hipotesis -> variantes)
python skills/content-optimizer/scripts/hypothesis_generator.py --topic "Agentes de IA" --channel x_twitter

# Recopilacion de metricas (medicion de rendimiento post-publicacion)
python skills/content-optimizer/scripts/collect_metrics.py --tweet-ids "123,456" --experiment-id exp-001

# Ejecucion en seco (sin llamadas API)
python skills/content-optimizer/scripts/hypothesis_generator.py --topic "SaaS" --dry-run
```

## Lista de Scripts

| Script | Proposito |
|--------|-----------|
| hypothesis_generator.py | Investigacion de mercado -> generacion de hipotesis -> creacion de variantes |
| collect_metrics.py | Recopilacion de metricas de tweets y comparacion de variantes |
| typefully_client.py | Cliente de API v2 de Typefully |

## Parametros de hypothesis_generator.py

| Parametro | Requerido | Predeterminado | Descripcion |
|-----------|-----------|----------------|-------------|
| --topic, -t | Si | - | Topico de investigacion |
| --channel, -c | No | x_twitter | Canal: x_twitter, email, linkedin |
| --competitors | No | - | Cuentas de competidores (separadas por coma) |
| --lang, -l | No | ja | Idioma: ja, en, all |
| --days, -d | No | 7 | Periodo de investigacion |
| --num-hypotheses | No | 5 | Numero de hipotesis a generar |
| --auto-draft | No | false | Crear borradores automaticamente en Typefully |
| --output, -o | No | output/content-optimizer/ | Destino de salida |
| --dry-run | No | false | Vista previa sin llamadas API |
| --test | No | false | Auto-prueba |

## Parametros de collect_metrics.py

| Parametro | Requerido | Predeterminado | Descripcion |
|-----------|-----------|----------------|-------------|
| --tweet-ids | No | - | IDs de tweets para recuperacion de metricas (separados por coma) |
| --username | No | - | Recuperar publicaciones recientes del usuario |
| --experiment-id | No | - | Vincular y comparar por ID de experimento |
| --days-after | No | 3 | Dias de metricas a recuperar despues de publicar |
| --output, -o | No | output/content-optimizer/ | Destino de salida |
| --test | No | false | Auto-prueba |

## Fuentes de Datos

| Fuente | API | Datos Recuperados | Variable de Entorno |
|--------|-----|-------------------|---------------------|
| X (Twitter) | X API v2 Recent Search | Publicaciones virales (mayor engagement) | X_BEARER_TOKEN |
| Google Search | Gemini Google Search grounding | Articulos tendencia, mejores practicas | GEMINI_API_KEY |
| Google Trends | Gemini grounding | Tendencias de volumen de busqueda, topicos en alza | GEMINI_API_KEY |
| Reddit / HN | Reddit JSON API + HN Algolia API | Discusiones de la comunidad, sentimiento | No requerido |
| Cuentas de competidores | X API v2 User Tweets | Publicaciones de alto rendimiento de competidores | X_BEARER_TOKEN |

## Formato de Salida

```
output/content-optimizer/hypotheses/YYYYMMDD_HHMMSS_{topico}/
├── market_report.md       # Informe de tendencias
├── hypotheses.yaml        # Lista de hipotesis (priorizada)
├── experiment_design.yaml # Documento de diseno de experimento
├── raw_data.json          # Datos brutos de todas las fuentes
└── drafts/                # Borradores de publicaciones con variantes A/B
    ├── variant_a.md
    └── variant_b.md
```

## Configuracion del Entorno

### Variables de Entorno Requeridas

```bash
# Agregar a .env
X_BEARER_TOKEN=su_token_bearer_x_aqui   # Busqueda y recuperacion de usuarios X API v2
GEMINI_API_KEY=su_clave_api_gemini_aqui   # Google Search grounding + analisis LLM
```

### Variables de Entorno Opcionales

```bash
TYPEFULLY_API_KEY=su_clave_typefully_aqui  # Al usar la opcion --auto-draft
```

### Como Obtener

- **X_BEARER_TOKEN**: Obtener despues de crear un proyecto en [X Developer Portal](https://developer.x.com/en/portal/dashboard) (plan Basic o superior)
- **GEMINI_API_KEY**: Obtener en [Google AI Studio](https://aistudio.google.com/apikey) (gratuito)
- **TYPEFULLY_API_KEY**: Obtener en [Typefully Settings](https://typefully.com/settings/integrations) seccion API

## Como Usar el Ciclo de Auto-Mejora

1. Use `hypothesis_generator.py` para analisis de tendencias -> hipotesis -> generacion de variantes
2. Publique variantes A/B via Typefully (manual o con el flag `--auto-draft`)
3. Despues de 2-3 dias, mida el rendimiento con `collect_metrics.py`
4. Genere las siguientes hipotesis basandose en los resultados (el aprendizaje se acumula)

## Ejemplos de Uso

```bash
# Generar hipotesis sobre agentes de IA para X (japones)
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "Agentes de IA" --channel x_twitter --lang ja

# Tambien investigar cuentas de competidores y auto-registrar variantes en Typefully
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "SaaS" --competitors "user_a,user_b" --auto-draft

# Generar 5 hipotesis para contenido de LinkedIn en ingles
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "productivity" --channel linkedin --lang en --num-hypotheses 5

# Recopilar metricas para IDs de tweets especificados
python skills/content-optimizer/scripts/collect_metrics.py \
  --tweet-ids "1234567890,0987654321" --experiment-id exp-001

# Recuperar y analizar publicaciones recientes del usuario
python skills/content-optimizer/scripts/collect_metrics.py \
  --username micuenta --days-after 7

# Ejecucion en seco para verificar que datos se recuperarian
python skills/content-optimizer/scripts/hypothesis_generator.py \
  --topic "IA generativa" --dry-run
```

## Dependencias

```text
requests>=2.28.0
python-dotenv>=0.19.0
pyyaml>=6.0
google-genai>=0.5.0
```

## Habilidades Relacionadas

- `x-research` -- Recopilacion de datos de busqueda de X
- `ab-test-setup` -- Marco detallado de diseno de experimentos
- `social-content` -- Estrategia de contenido para redes sociales
- `content-strategy` -- Planificacion de contenido
- `analytics-tracking` -- Medicion de metricas
