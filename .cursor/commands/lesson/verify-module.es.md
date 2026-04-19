---
description: "Lesson command"
---

# /verify-module [número de módulo]

Verifica automáticamente el estado de finalización de todas las lecciones de un módulo, y la IA proporciona una evaluación integral y retroalimentación.

## Pasos

### Step 1: Ejecutar verificación factual

```bash
uv run python tools/verify_module.py --module $ARGUMENTS --json
```

### Step 2: Evaluación de IA

Lea los resultados JSON anteriores y evalue desde las siguientes 3 perspectivas.

#### Perspectiva 1: Existencia y validez de los entregables
- Verifique `exists` / `valid` en `outputs`
- Para directorios, verifique `file_count`
- Señale específicamente cualquier archivo faltante o inválido

#### Perspectiva 2: Logro de puntos de verificación
- Determine automáticamente los puntos de verificación que se pueden inferir de los entregables (archivo existe -> "generado" se considera logrado)
- Para elementos subjetivos como "comprendido" o "confirmado", **pregunte al usuario via AskUserQuestion**

#### Perspectiva 3: Evaluación de calidad
- Si los entregables existen, **lea** los archivos reales para verificar su contenido
- Visualice archivos de imagen con Read para verificar la calidad
- Verifique la estructura y calidad del código para archivos JSON/HTML/Python

### Step 3: Mostrar resultados

Muestre los resultados en el siguiente formato:

```
## Modulo N: [Nombre del modulo] Resultados de verificacion de finalizacion

### Resumen
| Elemento | Resultado |
|----------|-----------|
| Calificacion general | A / B / C / D |
| Lecciones completadas | X / Y |
| Entregables | X confirmados / Y faltantes |
| Puntos de verificacion | X / Y logrados |

### Criterios de calificacion
- **A**: Todas las lecciones completas, todos los entregables OK, buena calidad
- **B**: Todas las lecciones completas, problemas menores en algunos entregables
- **C**: Lecciones principales completas, algunas no iniciadas
- **D**: Mayoria incompleta

### Detalles por leccion
(Mostrar el estado de entregables y logro de puntos de verificacion para cada leccion en formato de tabla)

### Retroalimentacion
(Sugerencias especificas de correccion y mejora para elementos faltantes)

### Siguientes pasos
(Si todo esta completo, guiar al siguiente modulo; si esta incompleto, indicar lecciones a repetir)
```

### Step 4: Siguiente acción

Presente las siguientes opciones via AskUserQuestion:
1. Trabajar en las lecciones faltantes -> Guiar al `/start-X-Y` correspondiente
2. Avanzar al siguiente módulo -> Guiar a `/verify-module N+1`
3. Guardar resultados como JSON -> `uv run python tools/verify_module.py --module N --json --output .cursor/module_verify_N.json`
