---
name: session-retrospective
description: "Habilidad que genera automáticamente Issues de auto-mejora al final de una sesión. Se activa con solicitudes como 'Crear Issue de retrospectiva', 'Retrospectiva', 'Crear Issues de mejora'."
triggers:
  - Crear Issue de retrospectiva
  - Retrospectiva
  - Crear Issues de mejora
  - Issue de auto-mejora
  - Retrospectiva de sesión
  - session-retrospective
  - session-retro
version: 1.0.0
author: ai-agent-camp
dependencies: []
---

# Session Retrospective - Generación de Issues de auto-mejora de sesión

## Descripción general

Habilidad que revisa los problemas encontrados, ineficiencias y áreas de mejora al final de una sesión (conversación), y los registra automáticamente como GitHub Issues.

## Activadores

Se activa con solicitudes como:
- "Crear Issue de retrospectiva", "Issue de auto-mejora"
- "Retrospectiva", "session-retro"
- "Crear Issues de mejora"
- Como rutina automática al final de la sesión

## Flujo de trabajo

### Fase 1: Revisión de sesión (Análisis automático)

Extraer puntos de mejora del historial de conversación en las siguientes categorías:

| Categoría | Etiqueta | Patrón de detección |
|-----------|----------|---------------------|
| **Problemas de autenticación/configuración** | `auth` | Fallo en obtención de token, errores de autenticación de API, inconsistencias de variables de entorno |
| **Falta de rutas/convenciones** | `convention` | Variaciones de formato, inconsistencias en convenciones de nombres, plantillas no conformes |
| **Falta de herramientas/scripts** | `tooling` | Áreas manejadas con scripts de un solo uso, trabajo manual que debería automatizarse |
| **Inconsistencias de documentación** | `docs` | Contradicciones entre CLAUDE.md y MEMORY, entradas desactualizadas, gestión de información duplicada |
| **Ineficiencias de flujo de trabajo** | `workflow` | Áreas con excesivo ensayo y error, procesos que necesitaron alternativas |
| **Manejo de errores** | `error` | Errores inesperados, mensajes de error poco útiles, procesos que necesitaron reintentos |

### Fase 2: Generación de borrador de Issue

Generar un Issue para cada punto de mejora con la siguiente estructura:

```markdown
## Contexto
(Qué estaba haciendo cuando ocurrió el problema)

## Problema
(Descripción específica del problema. Incluir mensajes de error o comandos si están disponibles)

## Propuesta
(1-3 sugerencias de mejora, específicas y accionables)

## Situación
(En qué sesión/tarea ocurrió)
```

### Fase 3: Confirmación del usuario

Mostrar cada candidato de Issue mediante AskUserQuestion y permitir que elijan si registrar:
- "Registrar todos"
- "Seleccionar y registrar" (confirmar uno por uno)
- "Editar y registrar" (editar contenido antes de registrar)

### Fase 4: Registro de GitHub Issue

```bash
# Obtener GH_TOKEN (extraer de URL remota de git)
export GH_TOKEN=$(git remote get-url origin | grep -oP '(?<=https://)[^@]+(?=@)' | sed 's/x-access-token://')

# Registrar Issue (usar --body-file. heredoc causa problemas de escape con bloques de código Markdown)
cat > /tmp/issue_body.md << 'EOF'
Cuerpo del Issue (Markdown)
EOF
gh issue create --repo minicoohei/ai-agent-camp \
  --title "Mejora: <Título>" \
  --body-file /tmp/issue_body.md
```

## Métodos de ejecución

### Método 1: Invocación de habilidad

```text
Crear Issue de retrospectiva
```

### Método 2: Ejecución directa de script (Generar Issues desde plantilla)

```bash
# Registro masivo desde archivo JSON
python skills/session-retrospective/scripts/create_issues.py --input issues.json

# Modo de prueba (ejecución en seco, no registra realmente)
python skills/session-retrospective/scripts/create_issues.py --input issues.json --dry-run
```

## Directrices de calidad de Issues

### Buenos Issues
- Descripción de problema reproducible y específica
- Incluye comandos ejecutados y mensajes de error
- 1 Issue = 1 punto de mejora (alcance claro)
- Las propuestas son implementables y específicas

### Malos Issues (no deben crearse)
- Contenido vago como "quiero mejorarlo"
- Problemas temporales específicos de la sesión (no recurrirán)
- Problemas causados por error del usuario
- Contenido que duplica Issues existentes

## Plantilla de análisis

Marco de pensamiento para revisar sesiones:

1. **Bloqueos**: ¿Hubo momentos en que el trabajo se detuvo? → ¿Cuál fue la causa raíz?
2. **Soluciones alternativas**: ¿Hubo lugares donde usó una solución alternativa en vez del método apropiado?
3. **Repetición**: ¿Hubo lugares donde hizo el mismo trabajo 2+ veces?
4. **Consulta de documentación**: ¿Qué preguntas no pudieron responderse consultando CLAUDE.md o MEMORY?
5. **Trabajo manual**: ¿Qué trabajo manual podría haberse automatizado con scripts o herramientas?

## Salida

- GitHub Issues (repositorio minicoohei/ai-agent-camp)
- URLs de Issues mostradas en consola como lista
