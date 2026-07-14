---
description: Instalar habilidades desde complementos externos
category: utility
nonInteractiveMode: compliant
---
# Instalación de complementos externos

## Uso
```text
/install-plugins
```

## Descripción general
Instale habilidades seleccionadas de registros de complementos externos (`external-plugins.yaml`) definidos en 6 repositorios. Basado en el artículo de SkillsBench, en lugar de instalar todas las habilidades de una vez, recomendamos combinar 2-3 módulos adaptados a la tarea en cuestión.

## Referencia de subcomandos

### 1. Listar habilidades disponibles
Muestre todos los complementos registrados y las habilidades recomendadas del registro.
```bash
# Vista resumida
uv run python tools/skill_manager.py plugin-list

# También mostrar el estado de instalación de cada habilidad
uv run python tools/skill_manager.py plugin-list --verbose
```

### 2. Instalar habilidades recomendadas en lote
Instale todas las habilidades recomendadas de todos los complementos (aproximadamente 17) de una vez.
```bash
uv run python tools/skill_manager.py plugin-install --all-recommended
```

### 3. Instalar desde un complemento específico
```bash
# Especificar un complemento (solo habilidades recomendadas)
uv run python tools/skill_manager.py plugin-install --plugin knowledge-work-plugins

# Especificar complemento + nombres de habilidades
uv run python tools/skill_manager.py plugin-install --plugin claude-scientific-skills --skill matplotlib plotly

# Sobrescribir habilidades existentes
uv run python tools/skill_manager.py plugin-install --plugin marimo-skills --force
```

## Complementos disponibles

| Complemento | Repositorio | Habilidades recomendadas |
|-------------|-----------|--------------------------|
| knowledge-work-plugins | anthropics/knowledge-work-plugins | 5 |
| ui-ux-pro-max-skill | nextlevelbuilder/ui-ux-pro-max-skill | 1 |
| planning-with-files | OthmanAdi/planning-with-files | 1 |
| claude-scientific-skills | K-Dense-AI/claude-scientific-skills | 5 |
| claude-skills | alirezarezvani/claude-skills | 3 |
| marimo-skills | marimo-team/skills | 2 |

## Opciones

| Opción | Descripción |
|--------|-------------|
| `--plugin NAME` | Especificar el nombre del complemento objetivo |
| `--skill NAME...` | Especificar nombres de habilidades a instalar |
| `--all-recommended` | Instalar todas las habilidades recomendadas |
| `--force` | Sobrescribir habilidades existentes |

## Notas
- Se agrega automáticamente un campo `source:` al SKILL.md de las habilidades instaladas (para rastreo de origen)
- Si un nombre entra en conflicto con una habilidad existente del proyecto, se omitirá (use `--force` para sobrescribir)
- Se requiere conexión a la red para la primera ejecución ya que se clonarán los repositorios
