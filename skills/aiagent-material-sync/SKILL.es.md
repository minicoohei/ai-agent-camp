---
name: aiagent-material-sync
description: "Habilidad para sincronizar de forma segura los materiales del curso ai-agent-camp desde upstream. Se activa con solicitudes como 'actualizar materiales', 'sincronizar desde upstream', 'sincronizar cursos', 'git pull', 'actualizar materiales del curso', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-material-sync
  - actualizar materiales
  - sincronizar desde upstream
  - sincronizar cursos
  - actualizar materiales del curso
  - material sync
  - 教材を最新に
  - upstreamから更新
---

# Sincronizacion de Materiales de Agente de IA

Utilice esta habilidad para actualizaciones seguras del curriculo.

## Flujo de Trabajo
1. Verificar `git status`.
2. Advertir sobre cambios locales y archivos sin seguimiento antes de sincronizar.
3. Verificar `git remote -v` y elegir un remoto valido.
4. Si `upstream` existe, preferir `git fetch upstream` y `git merge upstream/main`.
5. Si `upstream` no existe, usar el remoto predeterminado rastreado, generalmente `origin/main`.
6. Si ningun remoto es utilizable, detenerse e indicar al usuario que nombre de remoto falta.
7. Explicar conflictos y recuperacion sin usar force push o limpieza destructiva.

## Ejemplo de Mensaje de Error
- `upstream` no esta configurado en este clon. Use `origin` en su lugar o agregue `upstream` antes de sincronizar.

## Referencias
- `README.md`
- `docs/codex-safety.md`

## Seguridad
- No usar `git reset --hard`.
- No usar `git clean -fd`.
- No hacer force push como "solucion".
