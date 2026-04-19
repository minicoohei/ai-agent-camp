---
name: tutorial-generator
description: "Genera automáticamente tutoriales de operación a partir de capturas de pantalla usando la API de Gemini Vision. Se activa con solicitudes como 'Crear un manual de operación', 'Generar instrucciones desde capturas', 'Crear guía de uso', etc."
triggers:
  - Crear un manual de operación
  - Generar instrucciones desde capturas
  - Crear guía de uso
  - Crear un tutorial
  - Explicar desde captura de pantalla
  - tutorial-generator
  - guía paso a paso
---

# Generador de Tutoriales

Analiza capturas de pantalla y genera instrucciones de operación paso a paso.

## Flujo de Trabajo

1. Proporcionar captura de pantalla de la interfaz/pantalla
2. Gemini Vision analiza los elementos visibles (botones, formularios, menús)
3. Genera un tutorial estructurado con pasos accionables
4. Produce un tutorial HTML con imagen incrustada

## Uso

```bash
python scripts/generate_tutorial.py "{screenshot_path}" --output "{output_path}"
```

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| screenshot_path | Sí | - | Ruta a la captura de pantalla |
| --output | No | auto | Ruta del HTML de salida |
| --context | No | - | Contexto adicional sobre la pantalla |

## Formato de Salida

El HTML generado incluye:
- Vista general de la pantalla (para qué sirve esta pantalla)
- Captura de pantalla original
- Pasos de operación numerados
- Ubicaciones y descripciones de elementos
- Consejos y advertencias

## Ejemplo

```bash
# Uso básico
python scripts/generate_tutorial.py "login_screen.png"

# Con contexto
python scripts/generate_tutorial.py "settings.png" --context "Página de configuración de usuario para cambiar contraseña"

# Especificar salida
python scripts/generate_tutorial.py "dashboard.png" --output "docs/tutorials/dashboard_guide.html"
```

## Requisitos

- GEMINI_API_KEY o GOOGLE_API_KEY en las variables de entorno
- Paquetes Python: google-genai, Pillow, python-dotenv
