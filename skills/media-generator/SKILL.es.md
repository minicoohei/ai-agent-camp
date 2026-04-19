---
name: media-generator
description: "Sub-agente para generar y editar banners, diagramas, diapositivas e imágenes. Usa la API de Generación de Imágenes de Gemini para generar diversos medios. Se activa con solicitudes como 'crear un banner', 'generar un diagrama', 'crear diapositivas', 'generar una imagen', etc."
triggers:
  - crear un banner
  - generación de banner
  - crear un diagrama
  - infografía
  - diagrama
  - generar diapositivas
  - generar una imagen
  - editar una imagen
  - imagen para X
  - para Instagram
  - para Facebook
---

# Sub-agente Media Generator

Sub-agente que ejecuta la generación y edición de banners/diagramas/diapositivas/imágenes en un contexto dedicado.

## Propósito

Separa el procesamiento de generación de medios del contexto del agente principal para:
- Optimizar el procesamiento que incluye múltiples imágenes de referencia
- Aplicar presets específicos por plataforma
- Devolver solo la información de ruta de archivos generados

## Lista de Funcionalidades

| Funcionalidad | Script | Descripción |
|---------------|--------|-------------|
| Generación de banners | `banner_creator.py` | Generación de banners para redes sociales/publicidad |
| Generación de diagramas | `generate_diagram.py` | Generación de infografías/diagramas |
| Generación de diapositivas | `generate_slide.py` | Generación de imágenes de diapositivas para clases |
| Generación general de imágenes | `nanobanana.py` | Texto a imagen, edición de imágenes |

## 1. Generación de Banners (`tools/banner_creator.py`)

### Presets por Plataforma

| Preset | Tamaño | Relación de Aspecto | Caso de Uso |
|--------|--------|---------------------|-------------|
| `x_post` | 1200x675 | 16:9 | Publicación en timeline de X |
| `x_card` | 800x418 | 16:9 | Tarjeta de enlace de X |
| `facebook` | 1200x630 | 16:9 | Publicación de enlace de Facebook |
| `facebook_story` | 1080x1920 | 9:16 | Facebook Stories |
| `instagram_feed` | 1080x1080 | 1:1 | Feed de Instagram |
| `instagram_story` | 1080x1920 | 9:16 | Instagram Stories |
| `prtimes` | 1200x630 | 16:9 | Nota de prensa PRTimes |
| `youtube_thumbnail` | 1280x720 | 16:9 | Miniatura de YouTube |
| `line` | 1200x628 | 16:9 | Cuenta oficial de LINE |
| `web_banner` | 1200x628 | 16:9 | Banner publicitario web |

### Uso

```bash
# Generar banner para X
uv run python tools/banner_creator.py \
  --platform x_post \
  --topic "Anuncio de lanzamiento de nuevo servicio" \
  --tone professional \
  --output-dir docs/generated/banners

# Usar imágenes de referencia
uv run python tools/banner_creator.py \
  --platform instagram_feed \
  --topic "Campaña de verano" \
  --reference-images image1.png image2.png \
  --output-dir docs/generated/banners

# Generar con texto de copy
uv run python tools/banner_creator.py \
  --platform prtimes \
  --topic "Para nota de prensa" \
  --with-copy \
  --output-dir docs/generated/banners
```

## 2. Generación de Diagramas/Infografías (`tools/generate_diagram.py`)

### Estilos

| Estilo | Descripción |
|--------|-------------|
| `colorful_infographic` | Colores brillantes, iconos, diseño legible |
| `sketch` | Estilo dibujado a mano, textura de lápiz/carboncillo |
| `photorealistic` | Calidad realista tipo fotografía |
| `minimalist` | Simple, enfocado en espacio en blanco, colores limitados |
| `claymation` | Estilo clay 3D, iluminación suave |
| `pixel_art` | Estilo retro de videojuego, diseño en bloques |

### Uso

```bash
# Generar diagrama desde un tema
uv run python tools/generate_diagram.py \
  --topic "Embudo de marketing" \
  --style colorful_infographic \
  --aspect-ratio 16:9 \
  --output-dir reports/visualizations

# Infografía desde texto largo
uv run python tools/generate_diagram.py \
  --topic "$(cat article.txt)" \
  --style minimalist \
  --output-dir reports/visualizations
```

## 3. Generación/Edición General de Imágenes (`tools/nanobanana.py`)

### Uso

```bash
# Generación de texto a imagen
uv run python tools/nanobanana.py \
  --prompt "A futuristic city at sunset" \
  --aspect-ratio 16:9 \
  --output-dir docs/generated

# Edición de imagen (imagen de referencia + instrucciones)
uv run python tools/nanobanana.py \
  --prompt "Make the background blue" \
  --reference reference.png \
  --output-dir docs/generated

# Uso de múltiples imágenes de referencia
uv run python tools/nanobanana.py \
  --prompt "Combine these styles" \
  --reference image1.png image2.png \
  --output-dir docs/generated
```

### Relaciones de Aspecto

| Relación de Aspecto | Caso de Uso |
|---------------------|-------------|
| `1:1` | Instagram, imágenes de perfil |
| `4:3` | Horizontal general |
| `3:4` | Vertical general |
| `16:9` | YouTube, presentaciones |
| `9:16` | Stories, Reels |
| `21:9` | Ultra ancho |

## Patrón de Llamada del Sub-agente

El agente principal llama a este sub-agente usando el siguiente patrón:

```python
Task(
    subagent_type="generalPurpose",
    model="fast",
    description="Banner generation",
    prompt="""
    Lea y ejecute este skill: skills/media-generator/SKILL.md
    
    Tarea: {instrucciones del usuario}
    Plataforma: {x_post / instagram_feed / etc.}
    Tema: {contenido a generar}
    
    Devuelva la ruta de la imagen generada.
    """
)
```

## Formato de Retorno

Los resultados del procesamiento se devuelven en el siguiente formato:

```yaml
status: success
generated_files:
  - path: docs/generated/banners/x_post_20260127_143022.png
    platform: x_post
    size: 1200x675
    aspect_ratio: 16:9
copy_text: |
  [Lanzamiento de Nuevo Servicio]
  ¡Ha llegado una herramienta de eficiencia empresarial potenciada por IA!
  #IA #EficienciaEmpresarial
```

## Dependencias

```txt
google-generativeai>=0.3.0
Pillow>=9.0.0
python-dotenv>=1.0.0
```

## Variables de Entorno

```bash
# Requerido
GEMINI_API_KEY=your_api_key
# o
GOOGLE_API_KEY=your_api_key
```

## Notas

- Las imágenes generadas se guardan automáticamente bajo `docs/generated/`
- Especificar un nombre de sesión organiza los archivos en subcarpetas
- Instruya explícitamente cuando incluya texto en japonés
- Máximo 5 imágenes de referencia
