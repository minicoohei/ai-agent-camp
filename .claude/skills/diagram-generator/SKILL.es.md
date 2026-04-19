---
name: diagram-generator
description: "Habilidad para generar diagramas, infografías e ilustraciones visuales a partir de texto usando la API de Generación de Imágenes de Gemini. Se activa con solicitudes como 'crea un diagrama,' 'genera una infografía,' 'ilustra este proceso,' etc."
triggers:
  - diagram-generator
  - 図を作って
  - ダイアグラム生成
  - インフォグラフィック
  - 図解して
  - diagram
  - フローチャート作成
---

# Generador de Diagramas

Genera diagramas visuales e infografías a partir de descripciones de texto.

## Flujo de Trabajo

1. Proporcione el tema/texto a visualizar
2. Gemini Flash optimiza el prompt de generación de imagen
3. Gemini Image genera la visualización
4. Genera imagen PNG

## Uso

```bash
python scripts/generate_diagram.py "{tema}" --style "{estilo}" --aspect_ratio "{relación}"
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|----------|----------------|-------------|
| topic | Sí | - | Tema o texto a visualizar |
| --style | No | colorful_infographic | Estilo visual |
| --aspect_ratio | No | 16:9 | Relación de aspecto de salida |
| --output | No | auto | Ruta de salida |

## Estilos

| Estilo | Descripción |
|--------|-------------|
| colorful_infographic | Iconos vibrantes, diseño organizado (predeterminado) |
| sketch | Dibujado a mano, textura de lápiz |
| minimalist | Limpio, formas geométricas simples |
| photorealistic | Aspecto fotográfico de alta calidad |
| claymation | Textura de arcilla 3D, lúdico |
| pixel_art | Estilo de juego retro |

## Relaciones de Aspecto

`16:9`, `1:1`, `4:3`, `3:4`, `9:16`, `21:9`

## Ejemplos

```bash
# Diagrama básico
python scripts/generate_diagram.py "Cómo funciona la fotosíntesis"

# Estilo minimalista
python scripts/generate_diagram.py "Pipeline de aprendizaje automático" --style minimalist

# Formato vertical
python scripts/generate_diagram.py "Organigrama de la empresa" --aspect_ratio 9:16

# Desde texto largo
python scripts/generate_diagram.py "Gemini es un modelo de IA multimodal que puede entender texto, imágenes y código..." --style colorful_infographic
```

## Requisitos

- GEMINI_API_KEY o GOOGLE_API_KEY en las variables de entorno
- Paquetes de Python: google-genai, Pillow, python-dotenv

## Descripción General

Una habilidad que genera automáticamente infografías, diagramas y visuales a partir de temas o descripciones de texto usando la API de Generación de Imágenes de Gemini. Ideal para ayudas visuales en presentaciones y documentación.

## Solución de Problemas

| Error | Solución |
|-------|----------|
| Clave API no encontrada | Configure `GEMINI_API_KEY` o `GOOGLE_API_KEY` en las variables de entorno |
| La generación de imagen devolvió vacío | El tema puede ser muy corto. Proporcione una descripción más detallada |

## Criterios de Éxito

- [ ] Imagen PNG generada con la relación de aspecto correcta
- [ ] La imagen generada representa visualmente el contenido del tema
- [ ] Completado sin errores
