---
description: "Verificación de finalización de módulo (con evaluación de IA)"
nonInteractiveMode: compliant
---
# /verify-module [número de módulo]

Verificar automáticamente el estado de finalización de todas las lecciones de un módulo, y obtener una evaluación integral y retroalimentación de la IA.

## Pasos

### Paso 1: Ejecutar verificación de hechos

```bash
uv run python tools/verify_module.py --module $ARGUMENTS --json
```

### Paso 2: Evaluación de IA

Leer los resultados JSON anteriores y evaluar desde estas 3 perspectivas:

#### Perspectiva 1: Existencia y validez de resultados
- Verificar `exists` / `valid` en `outputs`
- Para directorios, verificar `file_count`
- Señalar específicamente archivos faltantes o inválidos

#### Perspectiva 2: Logro de puntos de control
- Evaluar automáticamente los puntos de control inferibles de los resultados (archivo existe → "pudo generar" se considera logrado)
- Para elementos subjetivos como "comprendió" o "confirmó," **preguntar al usuario mediante AskUserQuestion**

#### Perspectiva 3: Evaluación de calidad
- Si existen resultados, **leer** los archivos reales para verificar el contenido
- Para archivos de imagen, leer para mostrar y verificar la calidad
- Para archivos JSON/HTML/Python, verificar estructura y calidad del código

### Paso 3: Mostrar resultados

Mostrar los resultados en este formato:

```
## Módulo N: [Nombre del módulo] Resultados de verificación de finalización

### Resumen
| Elemento | Resultado |
|----------|-----------|
| Calificación general | A / B / C / D |
| Lecciones completadas | X / Y |
| Resultados | X confirmados / Y faltantes |
| Puntos de control | X / Y logrados |

### Criterios de calificación
- **A**: Todas las lecciones completadas, todos los resultados OK, buena calidad
- **B**: Todas las lecciones completadas, problemas menores en algunos resultados
- **C**: Lecciones principales completadas, algunas sin iniciar
- **D**: La mayoría sin completar

### Detalle por lección
(Mostrar el estado de resultados y logro de puntos de control para cada lección en formato de tabla)

### Retroalimentación
(Pasos específicos de corrección y sugerencias de mejora para elementos faltantes)

### Siguientes pasos
(Si todo está completo, guiar al siguiente módulo; si está incompleto, listar las lecciones a repetir)
```

### Paso 4: Siguiente acción

Presentar estas opciones mediante AskUserQuestion:
1. Trabajar en lecciones faltantes → Guiar al `/start-X-Y` correspondiente
2. Pasar al siguiente módulo → Guiar a `/verify-module N+1`
3. Guardar resultados como JSON → `uv run python tools/verify_module.py --module N --json --output .cursor/module_verify_N.json`
