---
name: banner-creator
description: "Habilidad para generar banners/creativos para diversas plataformas de redes sociales y publicidad. Compatible con X, Facebook, Instagram, PRTimes, YouTube, LINE y anuncios web. Se activa con solicitudes como 'crear un banner', 'generar imagen publicitaria', 'imagen para redes sociales', 'produccion creativa', etc."
triggers:
  - banner-creator
  - crear un banner
  - generar imagen publicitaria
  - imagen para redes sociales
  - produccion creativa
  - creacion de banner
  - banner publicitario
  - banner
  - バナーを作って
  - 広告画像を生成
---

# Creador de Banners - Generacion de Banners/Creativos Publicitarios

Genera banners/creativos para diversas plataformas de redes sociales y publicidad.

## Funciones

1. **Preajustes por plataforma**: X, Facebook, Instagram, PRTimes, YouTube, LINE, anuncios web
2. **Configuracion de tono y estilo**: Profesional, pop, elegante y mas
3. **Busqueda de imagenes de referencia**: Obtiene imagenes de referencia mediante busqueda web a partir de palabras clave
4. **Generacion de texto de copia**: Genera simultaneamente texto de publicacion, hashtags y CTAs

## Tamanos por Plataforma

| Plataforma | Tamano | Relacion de Aspecto |
|------------|--------|---------------------|
| x_post | 1200x675 | 16:9 |
| x_card | 800x418 | 1.91:1 |
| facebook | 1200x630 | 1.91:1 |
| facebook_story | 1080x1920 | 9:16 |
| instagram_feed | 1080x1080 | 1:1 |
| instagram_story | 1080x1920 | 9:16 |
| prtimes | 1200x630 | 1.91:1 |
| youtube | 1280x720 | 16:9 |
| line | 1040x1040 | 1:1 |
| web_horizontal | 1200x628 | 1.91:1 |
| web_vertical | 300x600 | 1:2 |

## Uso

```bash
# Uso basico
python scripts/banner_creator.py --platform x_post --message "Frase publicitaria"

# Con generacion de texto de copia
python scripts/banner_creator.py --platform instagram_feed --message "Lanzamiento de nuevo producto" --with-copy

# Con busqueda de imagen de referencia
python scripts/banner_creator.py --platform facebook --message "Oferta" --search-ref "banner oferta EC"

# Todas las opciones
python scripts/banner_creator.py \
  --platform x_post \
  --message "Mensaje principal" \
  --sub-copy "Sub copia" \
  --cta "Registrese ahora" \
  --tone professional \
  --color-scheme cool \
  --font-style bold \
  --priority ctr \
  --brand-name "Nombre de la empresa" \
  --session "nombre_campana" \
  --with-copy \
  --variants 3
```

## Parametros

| Parametro | Requerido | Predeterminado | Descripcion |
|-----------|-----------|----------------|-------------|
| --platform | Si | - | Plataforma objetivo (ver tabla arriba) |
| --message | Si | - | Titular principal/frase publicitaria |
| --sub-copy | No | - | Subtitular o detalles |
| --cta | No | - | Texto de llamada a la accion |
| --tone | No | professional | Tono: professional, casual, pop, elegant, urgent, minimal, tech, natural |
| --color-scheme | No | auto | Color: warm, cool, mono, pastel, vivid, dark, o codigo HEX |
| --font-style | No | auto | Fuente: gothic, mincho, handwritten, bold, script, geometric |
| --priority | No | ctr | Enfoque: ctr, brand, info, emotion, product, event |
| --brand-name | No | - | Nombre de marca/empresa a mostrar |
| --reference | No | - | Ruta local o URL de imagen de referencia |
| --search-ref | No | - | Palabras clave para buscar imagenes de referencia |
| --session | No | - | Nombre de sesion para organizar la salida |
| --with-copy | No | false | Generar texto de copia junto con la imagen |
| --variants | No | 1 | Numero de variaciones a generar |
| --output | No | auto | Ruta del archivo de salida |

## Salida

- **Imagen**: `docs/generated/banners/{fecha}_{sesion}/{nombre_archivo}.png`
- **Texto de copia** (cuando se usa --with-copy): Guardado como `{nombre_archivo}_copy.md`
  - 3 variaciones de texto de publicacion
  - Sugerencias de hashtags
  - Frases CTA

## Ejemplos

### Banner para Publicacion en X
```bash
python scripts/banner_creator.py \
  --platform x_post \
  --message "Reforma laboral en la era de la IA" \
  --sub-copy "Webinar gratuito" \
  --cta "Registrese ahora" \
  --tone professional \
  --with-copy
```

### Feed de Instagram con Busqueda de Referencia
```bash
python scripts/banner_creator.py \
  --platform instagram_feed \
  --message "Coleccion de Verano" \
  --tone pop \
  --color-scheme vivid \
  --search-ref "fashion summer sale instagram"
```

### Imagen de Nota de Prensa PRTimes
```bash
python scripts/banner_creator.py \
  --platform prtimes \
  --message "Anuncio de lanzamiento de nuevo servicio" \
  --brand-name "Empresa S.A." \
  --tone professional \
  --priority info
```

## Requisitos

- GEMINI_API_KEY o GOOGLE_API_KEY en el entorno
- Paquetes Python: google-genai, Pillow, python-dotenv, requests

## Descripcion General

Habilidad para generar automaticamente banners/creativos para diversas plataformas de redes sociales y publicidad (X, Facebook, Instagram, PRTimes, YouTube, LINE, anuncios web) usando la API de Generacion de Imagenes de Gemini. Compatible con preajustes por plataforma, busqueda de imagenes de referencia y generacion simultanea de texto de copia.

## Solucion de Problemas

| Error | Solucion |
|-------|----------|
| API key not found | Configurar `GEMINI_API_KEY` o `GOOGLE_API_KEY` como variable de entorno |
| Image generation failed | Posible limite de tasa de API de Gemini. Espere unos segundos y reintente |
| Unknown platform | Especifique el nombre de preajuste correcto para `--platform` (x_post, instagram_feed, etc.) |

## Criterios de Exito

- [ ] La imagen se genera en el tamano correcto para la plataforma especificada
- [ ] El archivo de salida se guarda en `docs/generated/banners/`
- [ ] Cuando se especifica `--with-copy`, tambien se genera el archivo `.md` de texto de copia
