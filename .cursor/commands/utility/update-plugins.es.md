---
description: Actualizar habilidades externas instaladas
category: utility
---

# Actualizar plugins externos

## Uso
```text
/update-plugins
```

## Descripción general
Actualiza las habilidades externas instaladas mediante `plugin-install` a las versiones especificadas en el registro (`external-plugins.yaml`).

## Subcomandos

### 1. Actualizar todas las habilidades externas
```bash
uv run python tools/skill_manager.py plugin-update
```

### 2. Actualizar solo un plugin específico
```bash
uv run python tools/skill_manager.py plugin-update --plugin knowledge-work-plugins
```

### 3. Vista previa de actualizaciones
```bash
uv run python tools/skill_manager.py plugin-update --dry-run
```

### 4. Limpiar caché
Eliminar las cachés de clonación de repositorios para liberar espacio en disco.
```bash
uv run python tools/skill_manager.py plugin-clean
```

## Opciones

| Opción | Descripción |
|--------|-------------|
| `--plugin NAME` | Especificar el nombre del plugin de destino |
| `--dry-run` | Solo mostrar los detalles de la actualización (no actualiza realmente) |

## Notas
- Solo las habilidades con un campo `source:` en SKILL.md son elegibles para actualizaciones
- Se requiere conexión a la red ya que se obtiene la última versión del repositorio durante las actualizaciones
- Limpiar la caché con `plugin-clean` significa que se requiere una nueva clonación la próxima vez que instale/actualice
