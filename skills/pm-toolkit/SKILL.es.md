---
name: pm-toolkit
description: "Usado para generar PRDs, especificaciones de requisitos, documentos de solicitud y revisiones. Se activa con solicitudes como 'crear un PRD', 'escribir especificaciones de requisitos', 'revisar esto', 'analizar actas de reunión', etc."
triggers:
  - crear un PRD
  - escribir especificaciones de requisitos
  - revisar esto
  - analizar actas de reunión
  - pm-toolkit
  - PRD
  - crear documento de solicitud
---

# PM Toolkit - Kit de Herramientas de Gestión de Producto

Proporciona plantillas y prompts para las fases de planificación y definición de requisitos del desarrollo de productos.

## Flujo de Trabajo

1. El usuario especifica el entregable a crear (PRD / especificación de requisitos / revisión, etc.)
2. Aplicar la plantilla correspondiente y recopilar información de forma interactiva
3. Generar un documento estructurado en `output/pm/`

## Plantillas

### Plantilla de PRD (Método Working Backwards)

```markdown
# PRD: {Nombre del Producto}

## 1. Comunicado de Prensa
### Titular
{Título de una línea que transmite el valor}

### Subtítulo
{Usuarios objetivo y beneficio principal}

### Problema
{3 puntos de dolor del usuario}

### Solución
{Cómo el producto los resuelve}

### Testimonio del Cliente (Hipotético)
{Reacción ideal del usuario}

### Cómo Funciona
{Explicar en 3 pasos}

### CTA
{Siguiente acción}

## 2. FAQ
### FAQ para Usuarios (5 preguntas)
### FAQ para Stakeholders (5 preguntas)

## 3. Historias de Usuario
| ID | Persona | Como... | Quiero... | Para que... | Prioridad |
|----|---------|---------|-----------|-------------|-----------|

## 4. Alcance
### Dentro del Alcance (MVP)
### Fuera del Alcance (v2+)

## 5. Métricas de Éxito (KPIs)
| Métrica | Actual | Objetivo | Método de Medición |
|---------|--------|----------|-------------------|
```

### Plantilla de Especificación de Requisitos (Conforme a IPA)

```markdown
# Especificación de Requisitos: {Nombre del Sistema}

## 1. Descripción General
### 1.1 Propósito
### 1.2 Alcance
### 1.3 Glosario

## 2. Requisitos Funcionales
### 2.1 Lista de Funcionalidades
| ID | Nombre de Función | Resumen | Prioridad | Pantalla |
|----|-------------------|---------|-----------|----------|

### 2.2 Detalle de Funcionalidades
#### FR-001: {Nombre de la Función}
- Entrada:
- Procesamiento:
- Salida:
- Restricciones:

## 3. Requisitos No Funcionales
### 3.1 Requisitos de Rendimiento
| Elemento | Requisito | Justificación |
|----------|-----------|---------------|
| Tiempo de Respuesta | Transición de página en 3 segundos | Estándar de UX |
| Usuarios Simultáneos | 100 usuarios | Base de usuarios esperada |

### 3.2 Requisitos de Seguridad
### 3.3 Requisitos de Disponibilidad
### 3.4 Requisitos de Migración

## 4. Interfaces Externas
### 4.1 Interfaz de Usuario
### 4.2 Integración con Sistemas Externos

## 5. Restricciones y Supuestos
```

### Plantilla de Documento de Solicitud

```markdown
# Documento de Solicitud: {Nombre del Proyecto}

## Requisitos Funcionales (Método MoSCoW)
### Must Have (Obligatorio)
### Should Have (Recomendado)
### Could Have (Deseable)
### Won't Have (Fuera del Alcance)

## Requisitos No Funcionales
| Categoría | Requisito | Prioridad | Notas |
|-----------|-----------|-----------|-------|
```

### Prompts de Revisión

#### Revisión de Abogado del Diablo
La IA proporciona contraargumentos y críticas desde las siguientes perspectivas:
- ¿Esta funcionalidad es realmente necesaria? ¿Cuál es la evidencia?
- ¿Existe una alternativa más simple?
- ¿Cuál es el peor escenario? ¿El riesgo es aceptable?
- ¿El usuario objetivo realmente quiere esto?
- ¿Es técnicamente viable? ¿El costo es razonable?

#### Revisión de Seguridad (STRIDE)
| Amenaza | Descripción | Área Aplicable | Contramedida |
|---------|-------------|----------------|--------------|
| Spoofing | Suplantación de identidad | Autenticación | |
| Tampering | Manipulación de datos | Datos de tareas | |
| Repudiation | Negación de acciones | Registros de operación | |
| Information Disclosure | Fuga de datos | Datos de usuario | |
| Denial of Service | Interrupción del servicio | API | |
| Elevation of Privilege | Escalada de privilegios | Funciones de administración | |

#### Revisión de Caso de Negocio
```markdown
## Caso de Negocio
### Tamaño de Mercado (TAM/SAM/SOM)
### Análisis Competitivo (Análisis 3C)
### Modelo de Ingresos
### Proyección de P&L (3 Años)
| Elemento | Año 1 | Año 2 | Año 3 |
|----------|-------|-------|-------|
```

### Plantillas de Reunión

#### Plantilla de Agenda
```markdown
# Agenda de {Nombre de la Reunión}
- Fecha/Hora:
- Asistentes:
- Propósito:

## Temas
1. {Tema 1} (10 min)
2. {Tema 2} (15 min)
3. Revisión de Acciones Pendientes (5 min)
```

#### Plantilla de Actas de Reunión
```markdown
# Actas: {Nombre de la Reunión}
- Fecha/Hora:
- Asistentes:
- Relator:

## Decisiones
1.

## Contenido de la Discusión

## Elementos de Acción
| # | Elemento | Responsable | Fecha Límite | Estado |
|---|----------|-------------|--------------|--------|
```

#### Prompt de Extracción de Cambios de Especificación desde Actas
Analice las siguientes actas de reunión y extraiga las secciones que constituyen cambios de especificación:
- Detalle del cambio
- Alcance del impacto (IDs de requisitos relacionados)
- Razón del cambio
- Prioridad de respuesta

## Parámetros

| Parámetro | Requerido | Predeterminado | Descripción |
|-----------|-----------|----------------|-------------|
| template | Sí | - | Plantilla a usar (prd/requirements/review/meeting) |
| product_name | No | TaskFlow | Nombre del producto |
| output_dir | No | output/pm/ | Directorio de salida |

## Formato de Salida

Genera documentos Markdown en el directorio especificado:
- PRD -> `output/pm/prd.md`
- Especificación de Requisitos -> `output/pm/requirements-spec.md`
- Documento de Solicitud -> `output/pm/requirements-brief.md`
- Revisión -> `output/pm/review-{type}.md`
- Actas de Reunión -> `output/pm/meeting-minutes.md`

## Ejemplo

```
Use el skill pm-toolkit para crear un PRD de TaskFlow con el método Working Backwards.
-> Se generará output/pm/prd.md
```
