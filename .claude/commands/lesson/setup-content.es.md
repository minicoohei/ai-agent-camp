---
description: "Lesson command — configuración inicial del contenido"
duration: "~3 min"
prerequisites: ["Carpeta ai-agent-camp abierta en Cursor / Codex / Claude Code", "git disponible"]
level: "beginner"
nonInteractiveMode: deferred
tags: ["setup", "content", "module-0"]
---

# /setup-content -- configuración inicial del contenido

> Referenciado desde la slide del Module 0 S45 de aiagent-course (`HowToUpdateContent`).
> Prepara el entorno local para que puedas mantener el contenido del curso al día.

## Qué hace

`/setup-content` es una **preparación única** que deja el workspace listo para
actualizaciones continuas. El flujo de actualización real corre luego
`git fetch origin && git log HEAD..origin/main --oneline  # diff con upstream`.

## Qué hace la IA por debajo

1. Confirma que el sparse-checkout del repo está configurado (lo activa si hace falta)
2. `git status` — asegura que el working tree esté limpio
3. `git fetch origin` — trae las refs más recientes
4. Busca the upstream sync helper:
   - Si existe → ejecuta `python -c "import pathlib; print('ok' if pathlib.Path('.git').exists() else 'missing')"` para un smoke
   - Si no existe → indica al usuario que haga `git pull` y termina
5. Imprime "siguiente: ejecuta `git fetch origin && git log HEAD..origin/main --oneline  # diff con upstream`"

## Cómo verificar

```bash
git fetch origin && git log HEAD..origin/main --oneline  # diff con upstream
```

## Comportamiento en modo no interactivo

`nonInteractiveMode: deferred`.

- Pasos 1–3 (operaciones git de solo lectura) corren normalmente
- La verificación de the upstream sync helper se ejecuta
- Si la herramienta no está o se necesita confirmar algo, escribe un
  `setup-resume.md` con "re-ejecuta `/setup-content` en modo interactivo" y sale

## Ver también

- aiagent-course Module 0 S45 (`HowToUpdateContent`) — slide de actualización de contenido
- Spec común: [`_lib/non-interactive.md`](../_lib/non-interactive.md)
