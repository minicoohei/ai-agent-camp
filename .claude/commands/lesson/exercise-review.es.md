---
description: "Lesson command"
nonInteractiveMode: compliant
---
# Revisión de ejercicios

## Uso
```
/exercise-review [numero de ejercicio] [carpeta de salida]
```

Ejemplos:
```
/exercise-review 4-2 output/ex4-2
/exercise-review 7-3 ~/projects/gas-demo
```

## Proceso

### 1. Análisis de entregables
- Verificar archivos en la carpeta de salida
- Evaluar la calidad del código
- Verificar la estructura

### 2. Verificación de requisitos
Verificar los requisitos de ejercicios de cada Módulo y evaluar el logro:
- Cumplimiento de requisitos obligatorios
- Estado de implementación de requisitos opcionales
- Cumplimiento de mejores prácticas

### 3. Retroalimentación de mejora
- Sugerencias de mejora de calidad de código
- Recomendaciones de patrones de diseño
- Consideraciones de seguridad y rendimiento

### 4. Sugerencias de siguientes pasos
- Temas adicionales para estudiar
- Ejercicios prácticos relacionados
- Expansión a proyectos del mundo real

## Criterios de evaluación

### Calidad del código
| Elemento | Criterios |
|----------|-----------|
| Legibilidad | Convenciones de nomenclatura, comentarios, estructura |
| Mantenibilidad | Separación de modulos, dependencias |
| Pruebas | Cobertura, casos límite |
| Manejo de errores | Manejo de excepciones, salida de registros |

### Cumplimiento de funcionalidad
| Nivel | Descripción |
|-------|-------------|
| A | Todos los requisitos cumplidos + funciones adicionales |
| B | Todos los requisitos obligatorios cumplidos |
| C | Requisitos principales cumplidos |
| D | Solo algunos requisitos cumplidos |

## Formato de salida

```markdown
## Resultados de revision del ejercicio [numero]

### Resumen
- Calificacion general: [A/B/C/D]
- Completitud: [XX%]
- Fortalezas principales:
- Areas de mejora:

### Evaluacion detallada

#### Requisitos funcionales
| Requisito | Estado | Comentarios |
|-----------|--------|-------------|
| Requisito 1 | OK/NG | ... |
| Requisito 2 | OK/NG | ... |

#### Calidad del codigo
- Legibilidad: [X/5]
- Mantenibilidad: [X/5]
- Pruebas: [X/5]
- Manejo de errores: [X/5]

### Sugerencias de mejora
1. [Prioridad: Alta] ...
2. [Prioridad: Media] ...
3. [Prioridad: Baja] ...

### Siguientes pasos
- Ejercicios relacionados: start-X-X
- Materiales de referencia: [URL]
```

## Lista de ejercicios

### Módulo 6: Desarrollo de agentes
- 6-1: Creación de Commands
- 6-2: Creación de Skills
- 6-3: Mejores prácticas
- 6-4: Ingenieria de prompts
- 6-5: Depuración

### Módulo 7: Creación de Skill/Commands
- 7-1 a 7-8: Práctica de Skill/Commands

### Módulo 8: Análisis de datos
- 8-1: Procesamiento de CSV/JSON
- 8-2: Integración con bases de datos
- 8-3: Integración con API
- 8-4: Visualización

### Módulo 9: Integración con Slack
- 9-1: Conexión MCP con Slack
- 9-2: Automatización de mensajes

### Módulo 10: GAS
- 10-1: Conceptos básicos de Clasp
- 10-2: Integración con Calendar
- 10-3: Integración con Sheets

### Módulo 11: GitHub Actions
- 11-1: Creación de Workflow
- 11-2: Configuración de Secrets

### Módulo 12: Notion
- 12-1: Conexión MCP
- 12-2: Operaciones de BD
- 12-3 a 12-6: Integración con Notion CLI

## Notas
- Error si la carpeta de salida no existe
- Error si el número de ejercicio es invalido
- Use los resultados de revisión como información de referencia
