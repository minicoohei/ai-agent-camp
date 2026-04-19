---
description: Obtener las habilidades más recientes desde upstream
category: utility
---

# Actualizar habilidades a la última versión

## Uso
```text
/update-skills
```

## Descripción general
Incorpora las últimas actualizaciones de habilidades desde el repositorio original (minicoohei/ai-agent-camp).
Internamente, ejecuta `git fetch upstream` + `git merge upstream/main`.
Funciona de la misma manera que `/update-material`, pero proporciona orientación específica para actualizaciones de habilidades.

## Pasos de ejecución

Ejecute el siguiente comando.

```bash
uv run python tools/skill_manager.py update-upstream
```

El script realiza automáticamente lo siguiente:

1. Verifica el remote `upstream` (lo agrega si no está configurado)
2. Obtiene lo más reciente con `git fetch upstream`
3. Fusiona en la rama actual con `git merge upstream/main`

## Si ocurren conflictos
Los conflictos pueden ocurrir cuando las habilidades que ha modificado también fueron actualizadas en el repositorio original. En ese caso:

- Abra los archivos en conflicto en su editor, revise los marcadores `<<<<<<<` / `=======` / `>>>>>>>` y resuelva manualmente
- Después de la resolución: `git add <archivo>` -> `git commit` para completar la fusión

## Verificación posterior a la actualización

```bash
# Verificar la lista actual de habilidades
uv run python tools/skill_manager.py list
```

## Notas
- **Destinatario**: Esto es para repositorios que copió para uso personal (Import / clone+push)
- **Seguridad**: Nunca se ejecuta `git push --force`. Solo se realiza la fusión
- Envíe al remoto con `git push origin main` según sea necesario
