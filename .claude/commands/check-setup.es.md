---
description: "Alias de nivel superior — el cuerpo completo está en lesson/check-setup.es.md."
duration: "~2 min"
level: "beginner"
nonInteractiveMode: deferred
tags: ["setup", "check", "alias"]
---

# /check-setup -- comprobación automática del entorno (alias)

## Propósito

Wrapper fino para que los usuarios puedan invocar `/check-setup` sin tener
que recordar el namespace de subcarpeta (`/lesson:check-setup`). Toda la
lógica real vive en [`lesson/check-setup.es.md`](./lesson/check-setup.es.md).

## Instrucciones para la IA

1. Cuando se invoque este comando, **lee** `.claude/commands/lesson/check-setup.es.md`
   y sigue sus pasos como si fueran propios.
2. Si el runtime es no interactivo (`claude -p`, `cursor-agent --print`, sin TTY,
   o env vars `CLAUDE_CODE_NON_INTERACTIVE=1` / `CURSOR_AGENT_PRINT=1`), usa
   **modo diferido**:
   - Ejecuta las comprobaciones de solo lectura con normalidad.
   - Imprime el informe.
   - Reemplaza cualquier bloque `AskQuestion` por la línea: *"Vuelve a ejecutar
     `/check-setup` en modo interactivo para elegir el siguiente paso."* Luego sal.
3. En modo interactivo, muestra los bloques `AskQuestion` del archivo fuente tal cual.

## Ver también

- Especificación común de modo no interactivo: [`_lib/non-interactive.md`](./_lib/non-interactive.md)
- Variantes de idioma: [`check-setup.md`](./check-setup.md), [`check-setup.en.md`](./check-setup.en.md)
