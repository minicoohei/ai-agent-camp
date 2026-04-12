# Create Banner - Generación de banners/creativos publicitarios

Este comando utiliza `tools/banner_creator.py` para generar banners/creativos para diversas plataformas de redes sociales y publicidad.

## Importante: Lista de verificación previa a la ejecución

**Antes de ejecutar este comando, debe utilizar la herramienta `ask_question` para confirmar la siguiente información.**

## Paso 1: Recopilar información con ask_question

Utilice la herramienta `ask_question` para hacer las siguientes preguntas:

```json
{
  "title": "Creación de banner/creativo publicitario",
  "questions": [
    {
      "id": "platform",
      "prompt": "¿Para qué plataforma es este banner?",
      "options": [
        {"id": "x_post", "label": "X (Twitter) - Publicación en timeline (1200x675)"},
        {"id": "x_card", "label": "X (Twitter) - Vista de tarjeta (800x418)"},
        {"id": "facebook", "label": "Facebook - Publicación con enlace (1200x630)"},
        {"id": "facebook_story", "label": "Facebook - Stories (1080x1920)"},
        {"id": "instagram_feed", "label": "Instagram - Publicación en feed (1080x1080)"},
        {"id": "instagram_story", "label": "Instagram - Stories (1080x1920)"},
        {"id": "prtimes", "label": "PR Times - Comunicado de prensa (1200x630)"},
        {"id": "youtube", "label": "YouTube - Miniatura (1280x720)"},
        {"id": "line", "label": "LINE - Mensaje enriquecido (1040x1040)"},
        {"id": "web_horizontal", "label": "Anuncio web - Horizontal (1200x628)"},
        {"id": "web_vertical", "label": "Anuncio web - Vertical (300x600)"},
        {"id": "custom", "label": "Tamaño personalizado"}
      ],
      "allow_multiple": false
    },
    {
      "id": "tone",
      "prompt": "Seleccione el tono/ambiente del banner",
      "options": [
        {"id": "professional", "label": "Profesional - Orientado a negocios, confiable"},
        {"id": "casual", "label": "Casual - Accesible, amigable"},
        {"id": "pop", "label": "Pop - Brillante, divertido, orientado a jóvenes"},
        {"id": "elegant", "label": "Elegante - Lujoso, sofisticado"},
        {"id": "urgent", "label": "Urgente - Oferta, tiempo limitado, actúe ahora"},
        {"id": "minimal", "label": "Minimalista - Simple, aprovechando el espacio en blanco"},
        {"id": "tech", "label": "Tech - Avanzado, aspecto digital"},
        {"id": "natural", "label": "Natural - Naturaleza, orgánico"}
      ],
      "allow_multiple": false
    },
    {
      "id": "color_scheme",
      "prompt": "Seleccione la dirección de color",
      "options": [
        {"id": "brand", "label": "Especificar colores de marca (ingresar después)"},
        {"id": "warm", "label": "Tonos cálidos - Rojo, naranja, amarillo"},
        {"id": "cool", "label": "Tonos fríos - Azul, verde, púrpura"},
        {"id": "mono", "label": "Monocromo - Blanco, negro, gris"},
        {"id": "pastel", "label": "Pastel - Colores claros y suaves"},
        {"id": "vivid", "label": "Vívido - Colores primarios brillantes"},
        {"id": "dark", "label": "Oscuro - Base negra, aspecto lujoso"},
        {"id": "auto", "label": "Dejar que la IA decida"}
      ],
      "allow_multiple": false
    },
    {
      "id": "font_style",
      "prompt": "Seleccione el estilo de fuente",
      "options": [
        {"id": "gothic", "label": "Gótica (Sans-serif) - Legible, moderna"},
        {"id": "mincho", "label": "Mincho (Serif) - Tradicional, lujosa"},
        {"id": "handwritten", "label": "Manuscrita - Accesible, única"},
        {"id": "bold", "label": "Negrita/Impacto - Fuerte, llamativa"},
        {"id": "script", "label": "Script - Elegante, femenina"},
        {"id": "geometric", "label": "Geométrica - Futurista, orientada a tecnología"},
        {"id": "auto", "label": "Dejar que la IA decida"}
      ],
      "allow_multiple": false
    },
    {
      "id": "priority",
      "prompt": "¿Qué es lo más importante para este banner?",
      "options": [
        {"id": "ctr", "label": "Tasa de clics (CTR) - Llamativo, llamada a la acción"},
        {"id": "brand", "label": "Reconocimiento de marca - Enfatizar logo/nombre de empresa"},
        {"id": "info", "label": "Entrega de información - Transmitir contenido con precisión"},
        {"id": "emotion", "label": "Apelación emocional - Evocar empatía, emoción"},
        {"id": "product", "label": "Apelación del producto - Mostrar productos de forma atractiva"},
        {"id": "event", "label": "Anuncio de evento - Mostrar claramente fecha/ubicación"}
      ],
      "allow_multiple": false
    },
    {
      "id": "reference_type",
      "prompt": "¿Cómo desea especificar una imagen de referencia?",
      "options": [
        {"id": "search", "label": "Buscar por palabra clave (referencia de competidores/creativos similares)"},
        {"id": "url", "label": "Especificar URL de imagen directamente"},
        {"id": "local", "label": "Especificar archivo local"},
        {"id": "none", "label": "Sin imagen de referencia (generar desde texto)"}
      ],
      "allow_multiple": false
    }
  ]
}
```

## Paso 2: Recopilar información adicional

Según las respuestas anteriores, solicite la siguiente información adicional mediante entrada de texto:

1. **Mensaje principal/eslogan**: Texto para mostrar en el banner
2. **Texto secundario (opcional)**: Información complementaria, detalles
3. **CTA (llamada a la acción)**: ej., "Regístrese ahora", "Más información"
4. **Nombre de marca/logo (opcional)**: Nombre de empresa o servicio a mostrar
5. **Colores de marca (cuando se selecciona "brand" en color_scheme)**: Código HEX ej., #FF5733
6. **Tamaño personalizado (cuando se selecciona "custom")**: ancho x alto ej., 1200x800
7. **Palabras clave de búsqueda/URL/ruta de imagen de referencia (según la selección de reference_type)**
8. **Nombre de sesión**: Nombre de la carpeta de salida (ej., summer_sale_campaign)

## Paso 3: Ejecutar la herramienta

Usando la información recopilada, ejecute el siguiente comando (también se puede delegar al sub-agente media-generator):

```bash
uv run python tools/banner_creator.py \
  --platform "{platform}" \
  --message "{mensaje_principal}" \
  --tone "{tone}" \
  --color-scheme "{color_scheme}" \
  --font-style "{font_style}" \
  --priority "{priority}" \
  --session "{nombre_sesión}" \
  --with-copy
```

### Argumentos opcionales

| Argumento | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--platform` | Plataforma (obligatorio) | `x_post`, `instagram_feed` |
| `--message` | Mensaje principal (obligatorio) | `"Oferta de verano"` |
| `--tone` | Tono | `professional`, `pop` |
| `--color-scheme` | Esquema de colores | `warm`, `cool`, `#FF5733` |
| `--font-style` | Fuente | `gothic`, `bold` |
| `--priority` | Punto de enfoque | `ctr`, `brand` |
| `--sub-copy` | Texto secundario | `"Hasta 50% de descuento"` |
| `--cta` | Texto CTA | `"Revíselo ahora"` |
| `--brand-name` | Nombre de marca | `"MyCompany"` |
| `--reference` | Ruta/URL de imagen de referencia | `./ref.png` o URL |
| `--search-ref` | Buscar imágenes de referencia | `"banner publicitario SaaS"` |
| `--session` | Nombre de sesión | `"summer_campaign"` |
| `--with-copy` | Generar también texto de publicación | Indicador |
| `--variants` | Número de variantes | `3` |
| `--output` | Destino de salida | `./output/banner.png` |

## Paso 4: Informar resultados

Después de completar la generación, informe lo siguiente:

1. **Ruta de la imagen de banner generada**
2. **Texto de copia generado** (cuando se especifica --with-copy)
   - 3 variaciones de texto de publicación
   - Sugerencias de hashtags
   - Frases CTA
3. **Variantes** (cuando se especifica --variants)

## Ejemplos de uso

### Banner para publicación en X
```bash
uv run python tools/banner_creator.py \
  --platform x_post \
  --message "Reforma laboral en la era de la IA" \
  --sub-copy "Webinar gratuito" \
  --cta "Regístrese ahora" \
  --tone professional \
  --color-scheme cool \
  --font-style bold \
  --priority ctr \
  --session "webinar_promotion" \
  --with-copy
```

### Feed de Instagram (con búsqueda de imagen de referencia)
```bash
uv run python tools/banner_creator.py \
  --platform instagram_feed \
  --message "Lanzamiento de nuevo producto" \
  --tone pop \
  --color-scheme vivid \
  --search-ref "cosméticos nuevo producto anuncio Instagram" \
  --with-copy
```

### Imagen de comunicado de prensa para PR Times
```bash
uv run python tools/banner_creator.py \
  --platform prtimes \
  --message "Empresa X anuncia nuevo servicio" \
  --brand-name "Empresa X" \
  --tone professional \
  --color-scheme "#1E40AF" \
  --font-style gothic \
  --priority info
```

## Notas

- Requiere que `GEMINI_API_KEY` o `GOOGLE_API_KEY` estén configuradas en las variables de entorno
- Las imágenes generadas se guardan en `docs/generated/banners/{fecha}_{nombre_sesión}/`
- La opción `--with-copy` también genera texto de publicación simultáneamente
- Se utilizan herramientas de navegador para la obtención de imágenes de referencia mediante búsqueda web
