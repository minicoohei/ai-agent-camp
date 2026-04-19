---
name: screenshot-analyzer
description: "Habilidad que genera automáticamente diagnósticos de errores o tutoriales de operación a partir de capturas de pantalla. Se activa con solicitudes como 'Analizar esta captura', 'Verificar el error de pantalla', 'Crear pasos de operación'."
triggers:
  - Analizar esta captura
  - Verificar el error de pantalla
  - Crear pasos de operación
  - Análisis de captura de pantalla
  - Diagnosticar pantalla de error
  - screenshot-analyzer
  - screenshot analysis
---

# Screenshot Analyzer

Analiza capturas de pantalla para diagnóstico de errores o generación de tutoriales de operación.

## Modos

1. **Analyze**: Detectar errores, identificar causas, sugerir soluciones
2. **Tutorial**: Generar guías de operación paso a paso con anotaciones

## Uso

```bash
# Análisis de errores (por defecto)
python scripts/analyze.py "{screenshot}" --mode analyze

# Generación de tutorial
python scripts/analyze.py "{screenshot}" --mode tutorial
```

## Parámetros

| Parámetro | Requerido | Por defecto | Descripción |
|-----------|-----------|-------------|-------------|
| screenshot | Sí | - | Ruta a la captura de pantalla |
| --mode, -m | No | analyze | Modo: analyze o tutorial |
| --output, -o | No | auto | Ruta HTML de salida |
| --no-annotate | No | false | Omitir generación de anotaciones |

## Salida

### Modo Analyze
- Descripción de la pantalla
- Detección de errores (mensaje, tipo, ubicación)
- Análisis de causa raíz
- Sugerencias de solución (Siguiente paso)

### Modo Tutorial
- Descripción general de la pantalla
- Pasos de operación numerados
- Capturas de pantalla anotadas por paso
- Consejos y advertencias

## Ejemplos

```bash
# Analizar captura de pantalla con error
python scripts/analyze.py "error_console.png"

# Generar tutorial
python scripts/analyze.py "settings_menu.png" --mode tutorial

# Especificar salida
python scripts/analyze.py "login.png" --mode tutorial --output "docs/login_guide.html"

# Omitir anotaciones
python scripts/analyze.py "error.png" --no-annotate
```

## Requisitos

- GEMINI_API_KEY o GOOGLE_API_KEY en el entorno
- Paquetes de Python: google-genai, Pillow, python-dotenv

## Descripción general

Habilidad que genera automáticamente diagnósticos de errores o tutoriales de operación a partir de capturas de pantalla. Reconoce elementos de UI con la API de Gemini Vision y genera análisis de causa raíz, sugerencias de solución o guías de operación paso a paso.

## Solución de problemas

| Error | Solución |
|-------|----------|
| API key not found | Establezca `GEMINI_API_KEY` o `GOOGLE_API_KEY` como variable de entorno |
| Analysis returned empty results | La captura de pantalla puede ser poco clara. Use una imagen de mayor resolución |

## Criterios de éxito

- [ ] Modo analyze: Se generan el contenido del error y las soluciones
- [ ] Modo tutorial: Se genera una guía de operación con pasos numerados
- [ ] El archivo HTML de salida se genera correctamente
