---
name: pdf-compressor
description: "Skill para comprimir archivos PDF grandes. Reducción de tamaño de archivo hasta 98%. Se activa con solicitudes como 'comprimir el PDF', 'hacer el PDF más liviano', 'reducir el tamaño del archivo', etc."
triggers:
  - comprimir el PDF
  - hacer el PDF más liviano
  - reducir el tamaño del archivo
  - pdf-compressor
  - PDF compress
  - el PDF es muy pesado
---

# PDF Compressor

Comprima archivos PDF convirtiendo páginas en imágenes optimizadas y reconstruyendo el PDF.

## Flujo de Trabajo

1. Convertir páginas del PDF a imágenes con el DPI especificado
2. Redimensionar imágenes al ancho objetivo (manteniendo la relación de aspecto)
3. Comprimir como JPEG con la configuración de calidad
4. Reconstruir el PDF a partir de las imágenes comprimidas

## Uso

```bash
python scripts/compress.py "{pdf_path}" --width {width} --quality {quality} --output "{output_path}"
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| pdf_path | Sí | - | Ruta al archivo PDF a comprimir |
| --width | No | 1920 | Ancho de página en píxeles |
| --quality | No | 85 | Calidad JPEG (1-100) |
| --dpi | No | 150 | DPI para la conversión de PDF a imagen |
| --output, -o | No | auto | Ruta de salida (predeterminado: {nombre}_compressed.pdf) |

## Presets de Calidad

| Caso de Uso | Ancho | Calidad | Reducción Esperada |
|-------------|-------|---------|-------------------|
| Web/Email | 1280 | 75 | ~95% |
| Estándar | 1920 | 85 | ~90% |
| Alta Calidad | 2560 | 90 | ~80% |
| Impresión | 3840 | 95 | ~60% |

## Ejemplos

```bash
# Compresión básica (configuración predeterminada)
python scripts/compress.py "large_presentation.pdf"

# Optimizado para web (archivo más pequeño)
python scripts/compress.py "slides.pdf" --width 1280 --quality 75

# Alta calidad para presentaciones
python scripts/compress.py "report.pdf" --width 2560 --quality 90

# Ruta de salida personalizada
python scripts/compress.py "document.pdf" -o "document_small.pdf"
```

## Requisitos

- Paquetes Python: pdf2image, Pillow, img2pdf
- Sistema: poppler (para pdf2image)
  - macOS: `brew install poppler`
  - Ubuntu: `apt-get install poppler-utils`
  - Windows: Obtener binarios de [poppler-windows](https://github.com/oschwartz10612/poppler-windows) y agregar al PATH

## Notas

- El PDF original no se modifica
- El texto se convierte en rasterizado (no buscable)
- Mejor para presentaciones y diapositivas con muchas imágenes
- Para documentos con mucho texto, considere usar Ghostscript en su lugar
