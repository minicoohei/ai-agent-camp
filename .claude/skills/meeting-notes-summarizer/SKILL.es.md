---
name: meeting-notes-summarizer
description: "Skill para generar automáticamente actas de reunión estructuradas a partir de texto y notas de reuniones. Se activa con solicitudes como 'resumir las actas', 'organizar notas de reunión', 'extraer elementos de acción', etc."
triggers:
  - resumir las actas
  - organizar notas de reunión
  - extraer elementos de acción
  - resumir las notas de la reunión
  - listar las decisiones
  - meeting-notes-summarizer
  - organizar los puntos clave de esta reunión
---

# meeting-notes-summarizer - Skill de Generación Automática de Actas de Reunión

Lee notas de reunión, transcripciones y registros de chat, y los formatea en actas de reunión estructuradas en Markdown. Cuando la entrada tiene información faltante, se nota explícitamente como `No especificado`, `Por confirmar` o `Fecha límite pendiente` en lugar de adivinar.

## Cuándo Usar

Use cuando reciba las siguientes solicitudes:

- Crear actas de reunión a partir de texto o notas de reunión
- Extraer decisiones y elementos de acción
- Estructurar y organizar notas de reunión para facilitar la lectura
- Formatear notas de reunión en formato Markdown

Frases de activación representativas:

- "Resumir las actas"
- "Organizar notas de reunión"
- "Extraer elementos de acción"
- "Resumir las notas de la reunión"
- "Estructurar las notas de la reunión"
- "Organizar los puntos clave de esta reunión"
- "Resumir los puntos clave de esta reunión"
- "Listar las decisiones"

## Flujo de Trabajo

Siga estos pasos. Siempre ejecute al menos una ronda de auto-revisión y bucle de mejora después de la generación inicial.

### Paso 1: Recibir el Texto de Entrada

- Recibir notas de reunión, transcripciones de audio, registros de chat o notas con viñetas
- Determinar el formato de entrada y separar fecha/hora, participantes, etiquetas de hablantes y contenido de discusión
- No sobre-complementar la información faltante; manejarla como `No especificado` o `Por confirmar` en secciones posteriores

### Paso 2: Extraer Participantes

- Extraer candidatos a participantes de listas de participantes, nombres de hablantes y etiquetas de intervención
- Unificar variaciones de nombres como la misma persona
- Si los participantes no están explícitamente indicados, notar `Participantes desconocidos`

### Paso 3: Identificar Puntos de Agenda

- Organizar los temas principales cronológicamente o por punto de discusión
- Resumir brevemente el contenido de la discusión para cada tema
- Si hay exceso de conversación casual o ruido, retener solo las intervenciones relacionadas con el tema principal

### Paso 4: Extraer Decisiones

- Extraer elementos confirmados de expresiones como "se decidió", "se acordó", "se aprobó", "se determinó"
- Agregar una nota de una línea sobre el contexto o justificación de cada decisión
- Si no se encuentran decisiones, notar explícitamente `No se tomaron decisiones`

### Paso 5: Extraer Elementos de Acción

- Extraer tareas de expresiones como "lo haré", "me encargo", "confirmaré", "para la próxima reunión"
- Asociar cada tarea con un responsable, fecha límite y prioridad
- Si el responsable es desconocido, notar `Por confirmar`; si la fecha límite es desconocida, notar `Fecha límite pendiente`

### Paso 6: Generar Borrador Inicial

- Leer `references/output-template.md` y crear el borrador inicial siguiendo el mismo orden y estructura de encabezados
- No dejar elementos desconocidos en blanco; usar `No especificado`, `Por confirmar`, `Fecha límite pendiente` explícitamente
- En esta etapa, priorizar completar todas las secciones requeridas sin omisiones sobre la perfección

### Paso 7: Realizar Auto-Revisión

- Auto-verificar el borrador inicial contra la siguiente lista de verificación
- Evaluar cada elemento como `OK` / `Requiere corrección` / `Requiere confirmación` con una justificación de una línea

Lista de verificación de auto-revisión:

1. ¿Están todos los participantes reflejados en el cuerpo o la sección de participantes?
2. ¿Están los puntos de agenda o temas principales organizados sin exceso ni deficiencia?
3. ¿Están las decisiones claras y se nota explícitamente `No se tomaron decisiones` cuando aplica?
4. ¿Cada elemento de acción tiene responsable, fecha límite y prioridad? ¿Se insertó `Por confirmar` / `Fecha límite pendiente` cuando falta?
5. ¿La sección de notas de discusión retiene contexto importante como antecedentes, preocupaciones y elementos pendientes?
6. ¿Se indica explícitamente la programación de la próxima reunión o su ausencia?
7. ¿La salida sigue el orden de encabezados y el idioma principal de `references/output-template.md`?

### Paso 8: Ejecutar Bucle de Mejora

- Revisar el borrador según los resultados de la auto-revisión
- Limitar las mejoras a un máximo de 2 rondas, registrando brevemente "qué se corrigió" en cada ronda
- Detener la mejora cuando se cumpla cualquiera de los siguientes:
  - Todos los elementos de la lista de verificación están en `OK`
  - Se han completado 2 rondas de mejora
  - La diferencia con la versión anterior es mínima con poco margen de mejora
- Los problemas no resueltos después de 2 rondas se notan como `Problemas pendientes` en la salida final

### Paso 9: Formatear Salida Final con Diferencias

- Leer `references/output-template.md` y formatear siguiendo el mismo orden y estructura de encabezados
- Devolver la salida en Markdown
- Antes de la versión final, resumir los cambios desde el borrador inicial como un `diff`
- Mostrar el diff en al menos 3 categorías: `Agregado`, `Modificado`, `Requiere confirmación`
- Si se necesita salida en archivo, guardar en `output/` o el `outputs/` del repositorio actual

## Formato de Salida

La salida sigue la plantilla en `references/output-template.md`. Como mínimo, incluir estas secciones:

- Información Básica
- Agenda
- Decisiones
- Elementos de Acción
- Notas de Discusión
- Próxima Reunión

Los elementos de acción se organizan en formato de tabla con columnas para responsable, tarea, fecha límite y prioridad.

Cuando se use Refinamiento Iterativo, se puede agregar lo siguiente antes del cuerpo de la plantilla:

- `## Resultados de Auto-Revisión`
- `## Diff de Revisión`
- `## Problemas Pendientes` (solo cuando sea necesario)

## Estructura de Prompts de Refinamiento Iterativo

Procesar internamente en este orden:

1. Generación del borrador inicial
   - "Crear un borrador de actas de reunión en Markdown conforme a la plantilla a partir del texto de entrada. No adivinar información faltante; indicarla explícitamente"
2. Auto-revisión
   - "Evaluar el borrador contra la lista de verificación de 7 elementos, devolviendo `OK` / `Requiere corrección` / `Requiere confirmación` con justificación"
3. Generación de versión mejorada
   - "Actualizar las actas de reunión abordando solo los elementos marcados como `Requiere corrección` o `Requiere confirmación` en la revisión, listando lo que se modificó"
4. Confirmación final
   - "Mostrar la diferencia entre el borrador inicial y la versión mejorada como `Agregado` / `Modificado` / `Requiere confirmación`, luego generar la versión final"

## Manejo de Casos Límite

### Sin Elementos de Acción

- Notar `No hay elementos de acción para esta reunión` en la sección de `Elementos de Acción`
- No tratar las reuniones con solo decisiones como un error

### Participantes Desconocidos

- Si es parcialmente inferible del contenido de las intervenciones, agregar `(estimado)`
- Si es completamente desconocido, notar `Participantes: Desconocidos (no especificado en el texto)`

### Idiomas Mixtos

- Generar la salida en el idioma principal del texto de entrada
- Preservar nombres propios, nombres de productos y términos técnicos en su idioma original
- Cuando japonés e inglés están mezclados, usar japonés como idioma principal

### Texto de Entrada Demasiado Corto

- Crear actas de reunión con la información mínima identificable
- Notar explícitamente los elementos faltantes como `No especificado`

### Formato de Registro de Chat

- Analizar marcas de tiempo y hablantes
- Excluir conversación casual y publicaciones duplicadas, extrayendo la esencia de la discusión
- Si existen hilos, organizar por tema antes de integrar en las actas generales
