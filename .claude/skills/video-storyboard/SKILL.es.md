---
name: video-storyboard
description: "Habilidad para crear storyboards (tableros visuales) a partir de guiones de video usando generación de imágenes con IA. Se activa con 'Crear un storyboard', 'Generar storyboard', 'Crear imágenes desde guión', etc."
triggers:
  - Crear un storyboard
  - Generar storyboard
  - Crear imágenes desde guión
  - Generar imágenes de fotogramas de video
  - Crear imágenes de escena
  - video-storyboard
  - storyboard
---

## Palabras de Activación
"Storyboard", "Tablero visual", "Generar imágenes desde guión de video", "Planificación de video"

# Habilidad de Storyboard de Video

## Propósito
Convertir guiones de video en storyboards visuales con imágenes generadas por IA.

## Prerrequisitos
- Configuración de clave API de Gemini (establecer variable de entorno `GEMINI_API_KEY` o pasar como `$KEY`)
- El directorio de salida `frames/` existe en el proyecto (se crea automáticamente si no está presente)

## Uso
Entrada: Un guión de `video-scriptwriter` con descripciones de escenas.

## Proceso
1. Extraer descripciones visuales de cada escena
2. Generar prompts de imagen (inglés, detallados, cinemáticos)
3. Llamar a la API de Gemini con `responseModalities: ["TEXT", "IMAGE"]`
4. Guardar fotogramas como `scene_XX.png`

## Directrices para Prompts de Imagen
- Describir composición, iluminación, paleta de colores
- Especificar estilo: "cinemático", "anime", "ilustración plana", etc.
- Incluir ángulo de cámara y encuadre
- Mantener estilo visual consistente entre escenas

## API
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=$KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Generate an image: ..."}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"]}}'
```

## Salida
- `frames/scene_01.png` ... `scene_NN.png`
- Cada imagen: 1024x1024 o relación de aspecto nativa

## Integración
La salida alimenta fal.ai i2V para generación de clips de video.
