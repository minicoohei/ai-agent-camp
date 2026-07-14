---
nonInteractiveMode: compliant
---

# Generate PlantUML Diagram con Nano Banana Pro

Este comando utiliza `tools/generate_plantuml_diagram.py` para generar imágenes de diagramas de flujo modernos estilo plantilla de Visio Flowchart a partir de archivos PlantUML.

## Especificaciones de diseño

### Disposición

- El flujo general sigue una dirección vertical (de arriba hacia abajo)
- Cada "participant" definido en el PlantUML obtiene su propio carril vertical (swimlane)
- Los bordes del carril son gris claro (#CCCCCC), el fondo es blanco
- Cada paso se coloca dentro del carril de su participante correspondiente

### Estilos de figuras

| Tipo de figura | Estilo |
|----------------|--------|
| Proceso general | Rectángulo redondeado (blanco, borde #4A90E2, sombra ligera) |
| Proceso interno (auto-llamada) | Rectángulo redondeado azul claro (#E8F1FF) |
| Recepción/entrada (de otro participante) | Rectángulo redondeado verde claro (#E9F7EC) |
| Bifurcación condicional (alt/else/opt) | Rombo (borde #7B61FF) |

### Flechas (líneas de flujo)

- Todas son líneas rectas o en ángulo de 90 grados, color gris oscuro (#555555)
- Las puntas de flecha son claras y altamente visibles
- Las bifurcaciones condicionales se dividen a izquierda y derecha desde la parte inferior del rombo, con etiquetas alt/else

### Iconos

- Iconos planos pequeños colocados en la esquina superior izquierda de las figuras para indicar la naturaleza del proceso
- El grosor de línea del icono es de 1.5-2px para consistencia
- Se asignan automáticamente iconos apropiados según los nombres de los participantes y el contenido del proceso

### Paleta de colores

| Elemento | Color |
|----------|-------|
| Fondo | Gris claro (#F7F7F7) |
| Proceso general | Blanco |
| Proceso interno | Azul claro (#E8F1FF) |
| Recepción/entrada | Verde claro (#E9F7EC) |
| Etiquetas de bifurcación | Gris oscuro (#444444) |

### Fuente

- Sans-serif (Segoe UI, Helvetica, Noto Sans, etc.)
- Texto dentro de figuras: aproximadamente 18px
- Etiquetas (alt, else, opt): 14px

### Espaciado

- La distancia vertical entre figuras es uniforme de 40-60px
- Los carriles están alineados con anchos iguales
- Se mantienen márgenes generales, con figuras alineadas horizontalmente para una disposición ordenada

### Estética general

- Diseño moderno y simple estilo UI
- Decoraciones mínimas, enfocado en la legibilidad
- Sombras muy ligeras, evitando efectos 3D excesivos
- Equilibrio y alineación claros de las figuras en general

## Pasos

1. **Extraer parámetros**:
   Extraiga la siguiente información de la entrada del usuario.
   - **Ruta del archivo PlantUML**: El archivo PlantUML a convertir (obligatorio)
   - **Relación de aspecto**: `auto` (predeterminado), `16:9`, `1:1`, `4:3`, `3:4`, `9:16`
   - **Ruta de salida**: Si se omite, se usa `docs/diagrams/{nombre_archivo}_{timestamp}.png`

2. **Ejecutar la herramienta**:
   Ejecute el comando en el siguiente formato.
   ```bash
   uv run python tools/generate_plantuml_diagram.py "{ruta_archivo_plantuml}" --aspect_ratio "{relación_de_aspecto}" --output "{ruta_salida}"
   ```

3. **Verificar resultados**:
   - Verifique la ruta de la imagen del diagrama generado e informe al usuario.
   - Si ocurre un error, muestre el mensaje de error.

## Referencia de parámetros

| Parámetro | Obligatorio | Predeterminado | Descripción |
|-----------|-------------|----------------|-------------|
| `plantuml_path` | Sí | - | Ruta al archivo PlantUML (.puml) |
| `--output`, `-o` | - | Generado automáticamente | Ruta de la imagen de salida |
| `--aspect_ratio`, `-a` | - | `auto` | Relación de aspecto (auto determina desde la estructura PlantUML) |

## Detección automática de relación de aspecto

Cuando se especifica `auto`, se aplican las siguientes reglas:

| Condición | Relación de aspecto |
|-----------|---------------------|
| 5 o más participantes | `21:9` (horizontal) |
| 3-4 participantes | `16:9` |
| Secuencia larga (20+ pasos) | `9:16` (vertical) |
| Otro | `16:9` |

## Ejemplos de uso

### Uso básico (relación de aspecto automática)
```
/generate-plantuml-diagram work/06.Porimu/sequence.puml
```

### Especificar relación de aspecto
```
/generate-plantuml-diagram work/project/flow.puml --aspect_ratio 16:9
```

### Especificar ruta de salida
```
/generate-plantuml-diagram sequence.puml --output docs/diagrams/my_flow.png
```

### Combinar múltiples opciones
```
/generate-plantuml-diagram work/api_flow.puml --aspect_ratio 9:16 --output docs/api_sequence.png
```

## Flujo de procesamiento

1. **Leer PlantUML**
   - Leer el código PlantUML del archivo
   - Analizar la estructura de participantes, mensajes, bifurcaciones, etc.

2. **Generar prompt** (Gemini 2.5 Flash)
   - Analizar la estructura PlantUML y crear un prompt que refleje las especificaciones de diseño
   - Especificar carriles, tipos de figuras y codificación de colores

3. **Generar diagrama** (Nano Banana Pro)
   - Generar una imagen de diagrama de flujo usando el prompt optimizado
   - Producir un diagrama moderno y profesional estilo Visio

## Notas

- Requiere que `GEMINI_API_KEY` o `GOOGLE_API_KEY` estén configuradas en las variables de entorno (o `.env`).
- El diagrama generado es un único archivo de imagen (formato PNG).
- Los diagramas PlantUML complejos (muchos participantes, muchos pasos) pueden tardar más en generarse.
- Se admiten etiquetas en japonés. El texto en el diagrama generado también se muestra en japonés.
