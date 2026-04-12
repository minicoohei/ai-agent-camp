---
name: nanobanana
description: "Skill para generar imágenes a partir de texto y editar imágenes existentes usando la API de Generación de Imágenes de Gemini. Se activa con solicitudes como 'generar una imagen', 'crear una ilustración', 'editar una foto', etc."
triggers:
  - generar una imagen
  - crear una ilustración
  - editar una foto
  - crear una imagen
  - nanobanana
  - image generation
  - diseñar un logo
---

# Nano Banana Pro - Generación y Edición de Imágenes

Genere o edite imágenes usando la API de Generación de Imágenes de Gemini.

## Modos

1. **Texto a Imagen**: Generar nuevas imágenes a partir de prompts de texto
2. **Edición de Imagen**: Editar imágenes existentes con instrucciones

## Uso

```bash
# Texto a imagen
python scripts/nanobanana.py "{prompt}" --aspect-ratio "{ratio}"

# Edición de imagen
python scripts/nanobanana.py "{prompt}" --input "{image_path}"

# Múltiples imágenes de referencia
python scripts/nanobanana.py "{prompt}" --input "{image1}" --input "{image2}"
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| prompt | Sí | - | Instrucción de generación/edición |
| --input, -i | No | - | Imagen(es) de entrada para edición |
| --output, -o | No | auto | Ruta de salida |
| --aspect-ratio, -ar | No | 16:9 | Relación de aspecto de salida |
| --session, -s | No | - | Nombre de sesión para organizar la salida |
| --force-ar | No | false | Forzar relación de aspecto en modo edición |

## Relaciones de Aspecto

`1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `21:9`

## Ejemplos

```bash
# Generar paisaje
python scripts/nanobanana.py "Mt. Fuji at sunset, photorealistic"

# Editar imagen
python scripts/nanobanana.py "Remove the background" --input photo.jpg

# Combinar imágenes
python scripts/nanobanana.py "Merge these into one composition" --input img1.png --input img2.png

# Con organización por sesión
python scripts/nanobanana.py "Company logo design" --session "brand_assets" --aspect-ratio 1:1
```

## Requisitos

- GEMINI_API_KEY o GOOGLE_API_KEY en el entorno
- Paquetes Python: google-genai, Pillow, python-dotenv

## Descripción General

Un skill de generación de imágenes de propósito general que usa la API de Generación de Imágenes de Gemini para generar imágenes a partir de prompts de texto o editar imágenes existentes. También soporta la composición de múltiples imágenes de referencia.

## Solución de Problemas

| Error | Solución |
|-------|----------|
| Clave API no encontrada | Configure `GEMINI_API_KEY` o `GOOGLE_API_KEY` como variable de entorno |
| Imagen de entrada no encontrada | Especifique la ruta correcta del archivo con `--input`. Las rutas relativas se basan en el directorio de ejecución |

## Criterios de Éxito

- [ ] La imagen se genera con la relación de aspecto especificada
- [ ] En modo edición, los cambios a la imagen fuente se reflejan correctamente
- [ ] Se completó sin errores
