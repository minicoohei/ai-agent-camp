---
name: aiagent-lesson-runner
description: "Habilidad para iniciar y avanzar en las lecciones de ai-agent-camp en Codex. Se activa con solicitudes como 'iniciar leccion', 'siguiente leccion', 'quiero empezar start-0-1', 'leccion en Codex', 'leccion de comando slash', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-lesson-runner
  - iniciar leccion
  - siguiente leccion
  - ejecutar leccion
  - leccion Codex
  - start-0-1
  - lesson runner
  - レッスン開始
  - 次のレッスン
---

## Palabras Clave de Activacion
"iniciar leccion", "siguiente leccion", "ejecutar leccion", "comando slash", "leccion Codex"

# Ejecutor de Lecciones de Agente de IA

Utilice esta habilidad para reproducir el flujo de trabajo `start-*` en Codex.

## Entradas
- Un id de leccion como `start-0-1`

## Flujo de Trabajo
1. Validar que el id de leccion coincida con `^start-\d+-\d+$`. Rechazar cualquier otro valor.
2. Verificar que `.cursor/commands/lesson/<lesson-id>.md` exista antes de leerlo.
3. Abrir `.cursor/commands/lesson/<lesson-id>.md`.
4. Extraer el objetivo de la leccion, prerequisitos, puntos de control, referencias de comandos y archivos referenciados.
5. Resolver la fuente del curriculo en este orden:
   - frontmatter `chapter` cuando apunta a un `courses/aiagent/**/chapter*.yaml`
   - documentos hermanos `practice/` y `final/` junto a ese capitulo
   - si `chapter` falta, inferir la mejor fuente de `courses/lessons.manifest.yaml`, la URL de la leccion y el numero de modulo `start-X-Y`
6. Tratar el JSON embebido `AskQuestion` / `AskUserQuestion` como un plano de conversacion. En Codex, convertirlo en opciones numeradas o con vinetas concisas en el chat normal en lugar de simular la interfaz de Cursor.
7. Para `/setup-start`, `/setup-github`, `/check-setup` y flujos de configuracion similares, no decirle al usuario que ejecute el comando slash de Cursor literalmente. Ejecutar o describir las verificaciones subyacentes y separar los pasos que requieren GUI de los pasos ejecutables por IA.
8. Si la leccion toca Git, secretos, MCP o APIs externas, indicar al usuario que documento de seguridad leer primero y verificar prerequisitos antes de intentar la tarea.
9. Guiar al usuario a traves de:
   - verificacion de prerequisitos
   - archivos a leer
   - acciones a realizar
   - criterios de completacion
   - siguiente leccion recomendada

## Referencias Requeridas
- `.cursor/commands/lesson/start-*.md`
- `courses/aiagent/**/chapter*.yaml` correspondiente cuando este disponible
- documentos hermanos `practice/` o `final/` para el capitulo resuelto
- `courses/lessons.manifest.yaml` como tabla de busqueda de respaldo cuando al markdown de leccion le falta `chapter`

## Seguridad
- Si la leccion implica cambios en Git o el entorno, consultar tambien `docs/codex-safety.md`.
- Nunca simular que el usuario puede ejecutar el archivo de comando markdown de Cursor directamente en Codex.
- Nunca pedir al usuario que pegue valores de secretos en el chat. Reutilizar el flujo de credenciales del repositorio.

## Salida Esperada
- Resumen de la leccion
- Proximas acciones ordenadas
- Archivos relevantes
- Criterios de completacion
- Leccion de seguimiento sugerida
- Cuando la leccion contiene opciones estructuradas, presentar las opciones compatibles con Codex en linea en la respuesta
