---
nonInteractiveMode: compliant
---

# Generate Lecture Slide con Nano Banana Pro

Este comando utiliza `tools/generate_slide.py` para generar diapositivas profesionales para conferencias.
Simplemente ingrese un tema, y automáticamente recopilará las explicaciones necesarias y creará una diapositiva con un diseño unificado.

## Especificaciones de diseño

Todas las diapositivas se generan con el siguiente diseño unificado:

| Elemento | Especificación |
|----------|----------------|
| Fondo | Blanco |
| Color principal | Azul (#2563EB) |
| Color secundario | Amarillo (#FBBF24) |
| Estilo | Diseño plano (flat design) |
| Tamaño de fuente | 14pt o mayor |
| Cantidad de texto | Mínima (apariencia organizada) |
| Relación de aspecto | 16:9 |

## Pasos

1. **Extraer parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Tema**: El tema de la diapositiva (obligatorio) ej.: "Cómo funcionan las herramientas de agentes de IA"
   - **Estilo**: `auto` (predeterminado), `title`, `content`, `diagram`, `summary`
   - **Ruta de salida**: Si se omite, se usa `docs/slides/{nombre_tema}_{timestamp}.png`

2. **Ejecutar la herramienta**:
   Ejecute el comando en el siguiente formato.
   ```bash
   uv run python tools/generate_slide.py "{tema}" --style "{estilo}" --output "{ruta_salida}"
   ```

3. **Verificar resultados**:
   - Verifique la ruta de la imagen de diapositiva generada e informe al usuario.
   - Si ocurre un error, muestre el mensaje de error.

## Referencia de estilos de diapositiva

| Estilo | Descripción |
|--------|-------------|
| `auto` | La IA selecciona automáticamente el diseño óptimo según el contenido (predeterminado) |
| `title` | Diapositiva de título (título grande + subtítulo) |
| `content` | Diapositiva de contenido (puntos, texto explicativo) |
| `diagram` | Diapositiva de diagrama (diagrama conceptual, estilo diagrama de flujo) |
| `summary` | Diapositiva de resumen (puntos clave organizados) |

## Ejemplos de uso

### Uso básico (estilo automático)
```
/generate-slide Cómo funcionan las herramientas de agentes de IA
```

### Generar una diapositiva de título
```
/generate-slide Seminario de introducción al aprendizaje automático --style title
```

### Generar una diapositiva de diagrama
```
/generate-slide Flujo de solicitudes API --style diagram
```

### Generar una diapositiva de contenido
```
/generate-slide Normalización de bases de datos --style content
```

### Generar una diapositiva de resumen
```
/generate-slide Puntos de aprendizaje de hoy --style summary
```

### Especificar ruta de salida
```
/generate-slide Arquitectura en la nube --output docs/slides/cloud_arch.png
```

### Combinar múltiples opciones
```
/generate-slide Principios de diseño de API REST --style diagram --output docs/training/api_design.png
```

## Flujo de procesamiento

1. **Generación de contenido** (Gemini 2.5 Flash)
   - Recopilar automáticamente explicaciones y puntos clave necesarios para la conferencia a partir del tema
   - Organizar en texto conciso adecuado para diapositivas

2. **Optimización del prompt** (Gemini 2.5 Flash)
   - Crear un prompt de generación de diapositivas que refleje las especificaciones de diseño
   - Generar instrucciones de disposición según el estilo

3. **Generación de diapositiva** (Nano Banana Pro)
   - Generar una imagen de diapositiva usando el prompt optimizado
   - Producir una diapositiva de conferencia profesional en formato 16:9

## Notas

- Requiere que `GEMINI_API_KEY` (recomendado) esté configurada en las variables de entorno (o `.env`).
- Cada diapositiva generada es un único archivo de imagen (formato PNG).
- Si necesita múltiples diapositivas, ejecute el comando varias veces.
- Se admiten temas en japonés. El texto en la diapositiva generada también se muestra en japonés.
