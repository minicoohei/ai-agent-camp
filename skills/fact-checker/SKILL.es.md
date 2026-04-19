---
name: fact-checker
description: "Habilidad que extrae automáticamente afirmaciones factuales (números, fechas, nombres propios, estadísticas) de artículos y las verifica mediante búsqueda web. Se activa con solicitudes como 'verifica los hechos,' 'confirma la información,' 'comprueba las fuentes,' etc. Genera un reporte con puntuaciones de confianza."
version: 1.0.0
author: ai-agent-camp
dependencies:
  - google-genai>=1.0.0
  - pyyaml>=6.0
  - python-dotenv>=0.19.0
triggers:
  - fact-checker
  - ファクトチェック
  - 事実確認
  - 裏付け確認
  - 情報の真偽
  - fact check
---

## Palabras Clave de Activación
"Verificación de hechos," "confirmar información," "comprobar fuentes," "verificar veracidad"

# Verificador de Hechos - Agente de Verificación Factual

## Descripción General

Una habilidad que extrae automáticamente afirmaciones factuales de artículos y documentos y las verifica mediante búsqueda web.
Utiliza la API de Gemini para extraer afirmaciones como datos estructurados, luego realiza búsquedas de fundamentación para verificar cada afirmación.
Finalmente, genera un reporte en Markdown con puntuaciones de confianza.

## Categorías de Afirmaciones

| Categoría | Clave | Descripción | Ejemplo |
|-----------|-------|-------------|---------|
| **Números y Estadísticas** | `numbers` | Afirmaciones que contienen números | "El tamaño del mercado es $50 mil millones," "Tasa de crecimiento del 15%" |
| **Fechas y Cronología** | `dates` | Descripciones relacionadas con fechas o líneas temporales | "Anunciado en 2024," "10 años desde la fundación" |
| **Nombres Propios** | `names` | Personas, organizaciones, nombres de productos | "El CEO de OpenAI Sam Altman" |
| **Causalidad** | `causation` | Afirmaciones del tipo "X causó Y" | "La expansión de la IA cambió las estructuras de empleo" |
| **Citas y Fuentes** | `citations` | Precisión de citas y fuentes existentes | "Según un estudio de Gartner..." |

## Niveles de Verificación

| Veredicto | Significado | Criterio |
|-----------|-------------|----------|
| Verificado | Corroborado por múltiples fuentes confiables | 2+ fuentes independientes coinciden |
| Necesita Revisión | Coincide parcialmente, o la información puede estar desactualizada | Solo 1 fuente, o discrepancia numérica menor |
| Discrepancia | Se encontró información contradictoria de fuentes | Contradice claramente fuentes confiables |
| No Verificable | No se encontró corroboración mediante búsqueda | No se puede confirmar como información pública |

## Inicio Rápido

```bash
# Verificar un artículo completo
python skills/fact-checker/scripts/fact_checker.py --input article.md

# Verificar solo números y estadísticas
python skills/fact-checker/scripts/fact_checker.py --input article.md --category numbers

# Modo detallado con salida especificada
python skills/fact-checker/scripts/fact_checker.py --input article.md --output report.md --depth thorough

# Modo de prueba (sin API necesaria, ejecuta con artículo de muestra)
python skills/fact-checker/scripts/fact_checker.py --test
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|----------|----------------|-------------|
| --input, -i | Sí* | - | Ruta del archivo de entrada (Markdown/texto) |
| --output, -o | No | `output/fact_report_{timestamp}.md` | Ruta del reporte de salida |
| --category, -c | No | `all` | Categoría a verificar: `all`, `numbers`, `dates`, `names`, `causation`, `citations` |
| --depth, -d | No | `quick` | Profundidad de verificación: `quick` (rápido, solo afirmaciones principales), `thorough` (todas las afirmaciones en detalle) |
| --test | No | false | Modo de prueba (sin API necesaria, ejecuta con artículo de muestra) |

*`--input` no es requerido cuando se usa `--test`

## Formato de Salida

Se genera un reporte en Markdown:

```markdown
# Reporte de Verificación de Hechos

**Archivo objetivo**: article.md
**Fecha de verificación**: 2026-02-12 15:30:00
**Profundidad de verificación**: quick

## Resumen
- Afirmaciones detectadas: 12
- Verificadas: 7
- Necesitan Revisión: 3
- Discrepancia: 1
- No Verificables: 1

## Detalles

### Afirmación 1: "El tamaño del mercado de IA alcanzará $190 mil millones para 2025"
- **Categoría**: Números y Estadísticas
- **Veredicto**: Necesita Revisión
- **Confianza**: 65%
- **Razón**: Los números difieren ligeramente de los datos más recientes. Múltiples fuentes muestran un rango de $184-200 mil millones
- **Fuentes**:
  - [Statista - Tamaño del Mercado de IA](https://example.com/source1)
  - [Grand View Research](https://example.com/source2)

### Afirmación 2: "OpenAI fue fundada en San Francisco en 2015"
- **Categoría**: Nombres Propios / Fechas y Cronología
- **Veredicto**: Verificado
- **Confianza**: 95%
- **Razón**: Confirmado por múltiples fuentes oficiales
- **Fuentes**:
  - [Wikipedia - OpenAI](https://example.com/source3)
  - [Sitio Web Oficial de OpenAI](https://example.com/source4)
```

## Flujo de Procesamiento

1. **Leer artículo**: Cargar el archivo de entrada (Markdown/texto)
2. **Extraer afirmaciones**: Usar la API de Gemini para extraer afirmaciones factuales como JSON estructurado
3. **Generar consultas de búsqueda**: Crear consultas de búsqueda óptimas para cada afirmación
4. **Ejecutar verificación**: Verificar cada afirmación usando la búsqueda de fundamentación de Gemini
5. **Generar reporte**: Generar los resultados de verificación como reporte en Markdown

## Configuración del Entorno

### Requerido: Clave API de Gemini

```bash
# Añadir a .env
GEMINI_API_KEY=your_api_key_here
# o
GOOGLE_API_KEY=your_api_key_here
```

### Dependencias

```txt
google-genai>=1.0.0
pyyaml>=6.0
python-dotenv>=0.19.0
```

## Ejemplos de Uso

```bash
# Verificar una publicación de blog
python skills/fact-checker/scripts/fact_checker.py \
  --input docs/blog-post.md --depth thorough

# Verificar solo números en un artículo de noticias
python skills/fact-checker/scripts/fact_checker.py \
  --input news_article.txt --category numbers

# Verificar nombres propios y fechas en un comunicado de prensa
python skills/fact-checker/scripts/fact_checker.py \
  --input press_release.md --category names --output output/press_check.md

# Ejecución de prueba (sin clave API necesaria)
python skills/fact-checker/scripts/fact_checker.py --test
```

## Habilidades Relacionadas

- **article-writer**: Habilidad de escritura de artículos (se puede usar para verificación después de la creación)
- **proofreading-agent**: Agente de corrección (verificación de gramática y expresión)
- **seo-audit**: Auditoría SEO (complementaria para verificación de precisión del contenido)
