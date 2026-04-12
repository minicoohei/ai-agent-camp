---
name: article-writer
description: "Habilidad de redaccion de articulos que genera esquemas a partir de temas, aplica perfiles de estilo y produce articulos en Markdown. Soporta insercion automatica de marcadores de ilustracion y unificacion de estilo a traves de perfiles de style-analyzer. Se activa con solicitudes como 'escribir un articulo', 'crear un blog', 'generar articulo del tema', etc."
triggers:
  - article-writer
  - escribir un articulo
  - crear blog
  - generar articulo del tema
  - redaccion de articulos
  - crear esquema
  - articulo Markdown
  - 記事を書いて
  - ブログ作成
---

# Redactor de Articulos - Motor de Redaccion de Articulos con IA

Genera automaticamente articulos Markdown estructurados simplemente ingresando un tema. Soporta unificacion de tono a traves de perfiles de estilo e insercion automatica de marcadores de ilustracion, produciendo articulos consistentes y de alta calidad.

## Flujo de Trabajo

```
Entrada de tema -> Generacion de esquema -> Aplicacion de estilo -> Redaccion de secciones -> Insercion de marcadores de ilustracion -> Verificacion de consistencia -> Salida Markdown
```

1. **Analisis del tema y generacion de esquema**: Disena automaticamente la estructura de secciones, encabezados y puntos clave a partir del tema
2. **Carga del perfil de estilo**: El estilo (tono, terminaciones de oraciones, nivel de vocabulario, etc.) se puede especificar via archivo YAML
3. **Redaccion de borrador seccion por seccion**: Genera cada seccion a traves de la API de Gemini siguiendo el esquema
4. **Insercion automatica de marcadores de ilustracion**: Coloca automaticamente puntos de insercion para figuras/imagenes como comentarios HTML
5. **Verificacion de consistencia general**: Verifica la consistencia de estilo y terminologia y produce el Markdown final

## Uso

```bash
# Generacion basica de articulos
python scripts/article_writer.py --theme "Como usar agentes de IA" --output output/article.md

# Con perfil de estilo
python scripts/article_writer.py --theme "Como usar agentes de IA" --style style_profile.yaml --output output/article.md

# Con audiencia objetivo
python scripts/article_writer.py --theme "Como usar agentes de IA" --audience "Profesionales de negocios no ingenieros" --style style_profile.yaml

# Especificar cantidad de palabras y secciones
python scripts/article_writer.py --theme "Introduccion al analisis de datos" --word-count 5000 --sections 7

# Desactivar marcadores de ilustracion
python scripts/article_writer.py --theme "Gestion de proyectos" --illustrations none

# Modo de prueba (sin llamada API)
python scripts/article_writer.py --test
```

## Parametros

| Parametro | Requerido | Predeterminado | Descripcion |
|-----------|-----------|----------------|-------------|
| --theme | Si | - | Tema/topico del articulo |
| --style | No | - | Ruta al archivo YAML del perfil de estilo |
| --audience | No | - | Audiencia objetivo (ej: "Profesionales de negocios no ingenieros") |
| --output | No | auto | Ruta del archivo de salida (predeterminado: output/article_{timestamp}.md) |
| --word-count | No | 3000 | Cantidad objetivo de palabras |
| --sections | No | auto | Numero de secciones (auto determina a partir del tema) |
| --illustrations | No | auto | Marcadores de ilustracion: auto (insercion automatica) / manual (solo posicion) / none (ninguno) |
| --test | No | false | Modo de prueba (genera articulo de muestra sin llamadas API) |

## Formato de Marcadores de Ilustracion

Los puntos de insercion de ilustraciones se indican en el articulo usando el siguiente formato de comentario HTML. Las imagenes reales se pueden generar con habilidades posteriores (nanobanana, diagram-generator, etc.).

```html
<!-- illustration: type=diagram description="Diagrama de flujo: pasos de procesamiento del agente de IA" -->

<!-- illustration: type=image description="Persona usando IA en una oficina moderna" -->
```

| tipo | Descripcion | Habilidad Recomendada |
|------|-------------|----------------------|
| diagram | Diagramas de flujo, diagramas de arquitectura, diagramas UML | diagram-generator |
| image | Estilo fotografico, ilustraciones, imagenes conceptuales | nanobanana |
| chart | Graficos, visualizaciones de datos | data-analyst |
| screenshot | Capturas de pantalla de interfaz | screenshot-annotator |

## Formato del Perfil de Estilo

El estilo se especifica via archivo YAML (se puede generar automaticamente con la habilidad style-analyzer).

```yaml
tone: professional        # professional / casual / academic / friendly
formality: high            # high / medium / low
sentence_ending: formal    # formal / informal / mixed
vocabulary_level: general   # general / technical / simple
paragraph_length: medium    # short / medium / long
use_examples: true
use_metaphors: false
target_audience: "Profesionales de negocios"
brand_voice: "Confiable y facil de entender"
avoid_words:
  - "basicamente"
  - "honestamente"
preferred_expressions:
  - "especificamente"
  - "por ejemplo"
```

## Formato de Salida

Archivo de articulo en formato Markdown. Se produce con la siguiente estructura.

```markdown
# Titulo del Articulo

> Parrafo introductorio (resumen/introduccion del articulo)

## Tabla de Contenidos

- [Seccion 1](#seccion-1)
- [Seccion 2](#seccion-2)
- ...

## Seccion 1

Texto del cuerpo...

<!-- illustration: type=diagram description="..." -->

## Seccion 2

Texto del cuerpo...

<!-- illustration: type=image description="..." -->

## Conclusion

Texto de conclusion...
```

## Ejecucion en Paralelo

Cuando se generan articulos para multiples temas simultaneamente, se pueden lanzar multiples agentes para procesamiento en paralelo.

```bash
# Ejecucion en paralelo para multiples temas
python scripts/article_writer.py --theme "Aplicaciones de IA" --output output/ia.md &
python scripts/article_writer.py --theme "Promocion de DX" --output output/dx.md &
wait
```

## Requisitos

- **Clave API**: Configurar GEMINI_API_KEY o GOOGLE_API_KEY como variable de entorno
- **Paquetes Python**: google-genai, pyyaml, python-dotenv

## Habilidades Relacionadas

| Habilidad | Integracion |
|-----------|-------------|
| **style-analyzer** | Genera automaticamente perfil de estilo a partir de texto de referencia -> pasar a --style |
| **proofreading-agent** | Correccion y revision de articulos generados |
| **fact-checker** | Verifica la precision factual en articulos |
| **nanobanana** | Genera imagenes reales a partir de marcadores de ilustracion (type=image) |
| **diagram-generator** | Genera diagramas de flujo etc. a partir de marcadores de ilustracion (type=diagram) |
