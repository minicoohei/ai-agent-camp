---
description: Sincronizar habilidades a nivel global u otros proyectos
category: utility
nonInteractiveMode: compliant
---
# Sincronización de habilidades

## Uso
```text
/sync-skills
```

## Descripción general
Copia y sincroniza las habilidades de `.claude/skills/` del proyecto a nivel global (`~/.claude/skills/`) o a otros proyectos. También puede ver la lista de habilidades y acceder a la guía de instalación de plugins oficiales.

## Subcomandos

### 1. Mostrar lista de habilidades
Ver las habilidades en los directorios del proyecto y global, y verificar las diferencias.
```bash
uv run python tools/skill_manager.py list
```

### 2. Sincronizar a nivel global
Copiar las habilidades del proyecto a `~/.claude/skills/`. Esto hace que las habilidades estén disponibles en todos los proyectos.
```bash
# Sincronizar todas las habilidades
uv run python tools/skill_manager.py sync-global

# Sincronizar solo habilidades específicas
uv run python tools/skill_manager.py sync-global --skills banner-creator diagram-generator

# Sobrescribir habilidades existentes
uv run python tools/skill_manager.py sync-global --force

# Especificar un destino personalizado
uv run python tools/skill_manager.py sync-global --target /path/to/target/skills
```

### 3. Sincronizar a otro proyecto
Copiar las habilidades del proyecto a `.claude/skills/` de otro proyecto.
```bash
# Sincronizar todas las habilidades
uv run python tools/skill_manager.py sync-project /path/to/other-project

# Sincronizar solo habilidades específicas
uv run python tools/skill_manager.py sync-project /path/to/other-project --skills banner-creator

# Sobrescribir habilidades existentes
uv run python tools/skill_manager.py sync-project /path/to/other-project --force
```

### 4. Guía de instalación de plugins oficiales
Mostrar instrucciones para instalar plugins del repositorio anthropics/skills.
```bash
uv run python tools/skill_manager.py plugin-guide
```

## Opciones

| Opción | Comandos aplicables | Descripción |
|--------|-------------------|-------------|
| `--force` | sync-global, sync-project | Sobrescribir habilidades existentes (por defecto se omiten) |
| `--skills NAME...` | sync-global, sync-project | Especificar nombres de habilidades a copiar (por defecto todas) |
| `--target DIR` | sync-global | Cambiar el directorio de destino |

## Notas
- Sin `--force`, las habilidades que ya existen en el destino se omiten
- Dado que utiliza copia (no enlaces simbólicos), las habilidades sincronizadas son copias independientes
- Si actualiza una habilidad, necesita sincronizar nuevamente
