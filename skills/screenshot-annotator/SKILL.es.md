---
name: screenshot-annotator
description: "Habilidad que agrega automáticamente anotaciones como recuadros rojos, flechas y globos de texto a capturas de pantalla. Se activa con solicitudes como 'Agregar anotaciones a la captura', 'Agregar flechas a la pantalla', 'Anotaciones para el manual'."
triggers:
  - Agregar anotaciones a la captura
  - Agregar flechas a la pantalla
  - Anotaciones para el manual
  - Agregar recuadro rojo
  - Agregar globo de texto
  - screenshot-annotator
  - annotate screenshot
---

# Screenshot Annotator

Agrega anotaciones a capturas de pantalla sin modificar la imagen original. Las anotaciones se superponen encima.

## Flujo de trabajo

1. Analizar la captura de pantalla para identificar el elemento objetivo
2. Generar superposición de anotaciones usando la API de Gemini Vision
3. Generar imagen anotada como archivo separado

## Uso

```bash
python scripts/annotate.py "{ruta_imagen}" "{instrucción}" --style "{estilo}" --text "{etiqueta}" --output "{ruta_salida}"
```

## Parámetros

| Parámetro | Requerido | Por defecto | Descripción |
|-----------|-----------|-------------|-------------|
| image_path | Sí | - | Ruta a la captura de pantalla |
| instruction | Sí | - | Qué anotar (ej., "el botón de Inicio de sesión") |
| --style | No | red_box | Estilo de anotación |
| --text | No | - | Etiqueta de texto a agregar |
| --output | No | auto | Ruta de salida |

## Estilos

| Estilo | Descripción |
|--------|-------------|
| red_box | Rectángulo rojo + flecha (por defecto) |
| arrow | Flecha roja apuntando al elemento |
| callout | Globo de texto con texto |
| highlight | Superposición amarilla semitransparente |
| circle | Círculo rojo alrededor del elemento |
| number | Marcador numerado para pasos |

## Ejemplos

```bash
# Anotación básica
python scripts/annotate.py "login.png" "el botón de Inicio de sesión"

# Con etiqueta de texto
python scripts/annotate.py "settings.png" "el ícono de engranaje" --text "Haga clic aquí"

# Estilo globo de texto
python scripts/annotate.py "form.png" "campo de email" --style callout --text "Ingrese su email"
```

## Requisitos

- GEMINI_API_KEY o GOOGLE_API_KEY en el entorno
- Paquetes de Python: google-genai, Pillow, python-dotenv

## Descripción general

Habilidad que agrega automáticamente anotaciones como recuadros rojos, flechas, globos de texto y resaltados a capturas de pantalla. Ideal para crear documentación técnica, manuales de usuario y tutoriales.

## Solución de problemas

| Error | Solución |
|-------|----------|
| API key not found | Establezca `GEMINI_API_KEY` o `GOOGLE_API_KEY` como variable de entorno |
| Element not found in screenshot | Describa la `instruction` más específicamente (ej., "el ícono de engranaje en la esquina superior izquierda") |

## Criterios de éxito

- [ ] Se genera un archivo anotado sin modificar la imagen original
- [ ] Las anotaciones se aplican correctamente al elemento de UI especificado
- [ ] Se completa sin errores
