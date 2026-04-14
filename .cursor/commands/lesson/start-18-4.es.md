---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~40 min"
category: "lesson"
prerequisites: ["start-18-3", "output/pm/prd.md"]
level: "intermediate"
tags: ["pm", "review", "devils-advocate", "security", "business"]
---

# 🎓 Lesson 18-4: Tres revisiones

## 📍 Lo que hará en esta sesión

**Lesson 18-4: Tres revisiones**  — Bienvenido!

| Elemento | Detalles |
|------|------|
| Objetivo | Revisar el PRD desde 3 perspectivas diferentes (Abogado del diablo, Seguridad, Planificación de negocios) |
| Duración | ~40 min |
| Habilidades utilizadas | habilidad pm-toolkit |
| Requisitos previos | Lesson 18-3 completada、output/pm/prd.md existe |
| Página del material | [Module 18: PM y definición de requisitos del sistema](https://ai-agent.camp/es/course/module-18) como referencia paralela |

**Flujo de la sesión:**
1. Revisión Devil's Advocate (la IA asume el rol de opositor)
2. Revisión de seguridad (STRIDE + análisis de flujo de datos)
3. Revisión de planificación empresarial (caso de negocio, tamaño de mercado, P&L)
4. Integración de resultados de revisión y reflejo de mejoras

Al final de esta sesión, los tres documentos de resultados de revisión de TaskFlow estaran completos.

Entregables:
- `output/pm/review-devils-advocate.md`
- `output/pm/review-security.md`
- `output/pm/review-business-case.md`

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "continuar" o "seguir" para reanudar. Las respuestas pueden pausarse debido al procesamiento de herramientas, pero no es un error.

---

## 🎯 Verificación de preparación

Ha terminado la Lección 18-3 y esta listo para las tres revisiones? Verifiquemos.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Confirmacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar si la Leccion 18-3 esta completada"},
      {"id": "view_html", "label": "Ver primero la pagina del material"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Continuar al Paso 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar la ruta de la página del material)
(different_lesson → Mostrar la lista de módulos)

---

## 🚀 Paso 1: Revisión Devil's Advocate

Revise rigurosamente el prd.md creado en la lección anterior desde la perspectiva de inversores y escepticos.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Severidad de la revision Devil's Advocate",
  "questions": [{
    "id": "review_severity",
    "prompt": "Seleccione el nivel de severidad de la revision",
    "options": [
      {"id": "soft", "label": "Suave (enfocado en retroalimentacion constructiva)"},
      {"id": "balanced", "label": "Estandar (equilibrado)"},
      {"id": "harsh", "label": "Severo (perspectiva del inversionista)"},
      {"id": "ultra_harsh", "label": "Ultra severo (refutar cada punto)"}
    ]
  }]
}
```

(soft → Iniciar revisión constructiva)
(balanced → Iniciar revisión equilibrada)
(harsh → Iniciar revisión desde perspectiva de inversor)
(ultra_harsh → Iniciar revisión ultra-estricta)

**Después de la selección (ejemplo)**:
Entrada:
```text
Basandose en output/pm/prd.md, actue como Devil's Advocate y
revise rigurosamente la propuesta de TaskFlow.

Elementos clave de revision:

[Validez de negocio]
1. Es realmente necesaria esta funcion? Cual es la base?
   - Es suficiente la evidencia de las necesidades del usuario?
   - Ha sido mencionado por multiples usuarios?
   - Por que las herramientas existentes (Asana, Trello) no son suficientes?

2. El mercado objetivo realmente quiere esto?
   - Cual es la base para las estimaciones de TAM/SAM/SOM?
   - Cuales son los puntos de diferenciacion con la competencia?
   - Por que este tamano de empresa (10-100 empleados) es optimo?

3. Es apropiado el alcance del MVP?
   - Hay funciones que se pueden eliminar?
   - Hay alternativas mas simples?
   - Es realmente necesario todo para el MVP?

[Validez tecnica]
4. Es tecnicamente viable?
   - Cual es la base para las estimaciones?
   - Cuales son los riesgos tecnicos?
   - Esta garantizada la escalabilidad?

5. Es razonable el costo/ROI?
   - Costo de desarrollo: Es preciso? Hay costos ocultos?
   - Monetizacion: Cual es el ingreso por usuario?
   - Cual es el periodo de recuperacion?
   - Se puede justificar el retorno de la inversion?

[Riesgo / Escenarios del peor caso]
6. Cual es el peor escenario?
   - Que pasa si los usuarios no lo adoptan?
   - Que pasa si hay fallos tecnicos en las funciones clave?
   - Que pasa si la competencia lanza las mismas funciones?
   - Son aceptables estos riesgos?

[Propuesta general]
7. Es convincente la estrategia del producto?
   - Por que esta solucion?
   - Se han considerado otros enfoques?
   - Es clara la vision a largo plazo?

Proporcione criticas y preguntas especificas para cada elemento.
Resuma las propuestas de mejora al final.
```

**Resultado esperado**: Se generan resultados de revisión rigurosa desde la perspectiva de Devil's Advocate.

---

## 🚀 Paso 2: Revisión de seguridad (STRIDE)

Analice los riesgos de seguridad de TaskFlow utilizando el marco STRIDE.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Alcance de la revision de seguridad",
  "questions": [{
    "id": "security_scope",
    "prompt": "Seleccione el alcance de la revision de seguridad",
    "options": [
      {"id": "stride_only", "label": "Solo analisis STRIDE"},
      {"id": "stride_dataflow", "label": "STRIDE + diagrama de flujo de datos"},
      {"id": "stride_full", "label": "STRIDE + flujo de datos + propuestas de contramedidas"},
      {"id": "comprehensive", "label": "Evaluacion de seguridad completa"}
    ]
  }]
}
```

(stride_only → Analizar las 6 categorías STRIDE)
(stride_dataflow → Análisis adicional de diagrama de flujo de datos)
(stride_full → Incluir propuestas de contramedidas)
(comprehensive → Incluir evaluación de riesgos y priorización)

**Después de la selección (ejemplo)**:
Entrada:
```text
Para TaskFlow en output/pm/prd.md,
realice un analisis de seguridad STRIDE.

[Analisis de 6 categorias STRIDE]

1. **Spoofing (Suplantacion de identidad)**
   Objetivo: Autenticacion de usuario
   Preguntas:
   - Cual es el metodo de autenticacion? (email/password, OAuth, SSO)
   - Cual es el riesgo de ataques de suplantacion?
   - Contramedidas: Politica de contrasenas robusta, MFA, gestion de sesiones

2. **Tampering (Manipulacion de datos)**
   Objetivo: Datos de tareas
   Preguntas:
   - Se garantiza la integridad de los datos de tareas?
   - Cual es el riesgo de modificacion no autorizada de datos?
   - Contramedidas: Firmas digitales, registros de auditoria, gestion de transacciones

3. **Repudiation (No repudio)**
   Objetivo: Registros de operaciones y pistas de auditoria
   Preguntas:
   - Se puede rastrear quien hizo que?
   - Existe la posibilidad de que los usuarios nieguen sus acciones?
   - Contramedidas: Registros completos de operaciones, marcas de tiempo, prevencion de manipulacion

4. **Information Disclosure (Fuga de datos)**
   Objetivo: Datos de usuario (tareas, mensajes, etc.)
   Preguntas:
   - Cual es el riesgo de acceder a datos de otros usuarios?
   - Esta encriptada la base de datos?
   - Esta encriptada la comunicacion?
   - Contramedidas: TLS/SSL, almacenamiento encriptado, control de acceso

5. **Denial of Service (Denegacion de servicio)**
   Objetivo: API, servidores web
   Preguntas:
   - Cual es la resistencia contra ataques de sobrecarga intencionales?
   - Estan implementadas las contramedidas DDoS?
   - Que hay sobre la limitacion de velocidad?
   - Contramedidas: WAF, limitacion de velocidad, planificacion de capacidad

6. **Elevation of Privilege (Escalada de privilegios)**
   Objetivo: Funciones de administrador, permisos de equipo
   Preguntas:
   - Cual es el riesgo de que usuarios regulares obtengan privilegios de administrador?
   - Es apropiado el diseno de control de acceso basado en roles (RBAC)?
   - Contramedidas: Verificacion estricta de privilegios, registros de auditoria, revision periodica de privilegios

[Diagrama de flujo de datos]
Ilustre el flujo de datos entre los siguientes componentes:
- Navegador del usuario <-> Servidor web
- Servidor web <-> Servidor API
- Servidor API <-> Base de datos
- Servidor API <-> Servicio de notificaciones (email/Slack)

Verifique la seguridad en cada punto de conexion.

[Formato de tabla de amenazas/contramedidas]
| Categoria de amenaza | Amenaza | Impacto | Riesgo | Contramedida | Implementado |
|------------|-----|--------|--------|------|---------|
| Spoofing | Fuga de credenciales | Alto | Fuga de datos de usuario | MFA | ✗ |
| Tampering | Manipulacion de tareas | Medio | Corrupcion de datos | Registros de auditoria | ✓ |

Genere el analisis completado en formato markdown.
```

**Resultado esperado**: Se completa la revisión de seguridad basada en el análisis STRIDE.

---

## 🚀 Paso 3: Revisión de planificación empresarial (Caso de negocio)

Analice el caso de negocio de TaskFlow en detalle.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Profundidad del caso de negocio",
  "questions": [{
    "id": "business_depth",
    "prompt": "Seleccione la profundidad del caso de negocio",
    "options": [
      {"id": "simple", "label": "Simple (tamano de mercado + competencia solamente)"},
      {"id": "standard", "label": "Estandar (+ modelo de ingresos)"},
      {"id": "detailed", "label": "Detallado (+ pronostico P&L a 3 anos)"},
      {"id": "full", "label": "Completo (+ presentacion para inversionistas)"}
    ]
  }]
}
```

(simple → Tamaño de mercado y análisis competitivo)
(standard → Agregar también modelo de ingresos)
(detailed → Incluir pronostico P&L a 3 años)
(full → Versión completa para presentación a inversores)

**Después de la selección (ejemplo)**:
Entrada:
```text
Basandose en output/pm/prd.md y output/pm/customer-needs.md,
realice un analisis de caso de negocio para TaskFlow.

[1. Dimensionamiento del mercado]

TAM (Total Addressable Market):
- Objetivo: Mercado de software de gestion de proyectos para empresas japonesas con 10-100 empleados
- Metodo de estimacion del tamano del mercado (de arriba hacia abajo):
  * Numero de empresas en Japon: aprox. 3.8 millones
  * Empresas con 10-100 empleados: aprox. 100,000 (de datos existentes)
  * Tasa de adopcion de herramientas de gestion de tareas: actualmente 15% (estimado)
  * Monto promedio de compra: 500K JPY/ano/empresa (5 usuarios x 100K JPY/usuario)
  * TAM = 100K x 500K = 5 mil millones JPY/ano

SAM (Serviceable Addressable Market):
- Mercado al que se dirige TaskFlow
- Objetivo: Empresas con 10-100 empleados insatisfechas con Asana/Trello
- Estimacion: 30% del TAM = 1.5 mil millones JPY/ano

SOM (Serviceable Obtainable Market):
- Cuota de mercado alcanzable en 5 anos
- Objetivo: 1% = 150 millones JPY/ano
- Esto equivale a 300 empresas x 500K JPY por ano

[2. Analisis 3C]

**Customer (Clientes)**
- Primario: PM/lideres en empresas medianas con 10-100 empleados
- Secundario: Gerentes de ventas, lideres de equipos de produccion/desarrollo
- Necesidades:
  * Quieren resolver las ineficiencias en la gestion de tareas con Excel/correo
  * Visibilidad de tareas en todo el equipo
  * Automatizacion de la gestion de plazos

**Competitor (Competencia)**
- Competidores directos: Asana, Trello, Notion, Monday.com
  * Asana: Rico en funciones pero costoso (1,350 JPY/usuario/mes), complejo
  * Trello: Simple pero debil en funciones de analisis de equipo
  * Notion: De uso general con una curva de aprendizaje pronunciada
  * Monday.com: Moderno pero con soporte insuficiente para el idioma japones
- Competidores indirectos: Excel, Google Sheets, Slack
  * Ya presentes en las empresas, costo de adopcion cero
  * Inferiores en funcionalidad pero sustitutos muy fuertes

**Company (Empresa)**
- Fortalezas de TaskFlow:
  * Interfaz simple e intuitiva (optimizada para empresas japonesas)
  * Sugerencias de prioridad impulsadas por IA
  * Notificaciones mediante integracion con Slack
  * Precios accesibles (estimado 500 JPY/usuario/mes)
- Debilidades:
  * Reconocimiento de marca cero
  * Tiempo necesario para construir el mercado inicial
  * Muchas startups compitiendo

[3. Modelo de ingresos]

Modelo B2B SaaS:
- Precio: 500-1,000 JPY/usuario/mes
- Unidad minima de contrato: 5 usuarios = 2,500-5,000 JPY/mes
- Soporte: Correo/chat (gratuito en el primer ano)
- Upsell: Plan premium (API, SSO, analisis avanzado)

LTV (Life Time Value) y CAC (Customer Acquisition Cost):
- Periodo promedio de contrato: 2 anos (24 meses)
- Tasa promedio de cancelacion: 5%/mes (etapa inicial)
- LTV = 3,000 JPY/mes x 24 meses = 72,000 JPY
- Objetivo CAC: 18,000 JPY (25% del LTV)

[4. Pronostico P&L a 3 anos]

**Year 1:**
- Inicio: Ingresos recurrentes mensuales 1M JPY (400 clientes iniciales)
- Tasa de crecimiento: 10%/mes (valor tipico SaaS)
- Ingresos recurrentes anuales: 18M JPY
- Costo de desarrollo: 15M JPY (costos de personal)
- Marketing: 5M JPY
- Infraestructura/otros: 3M JPY
- **EBITDA: -13M JPY (perdida)**

**Year 2:**
- Ingresos recurrentes mensuales: 2M JPY (800 clientes)
- Ingresos recurrentes anuales: 36M JPY
- Costo de desarrollo: 20M JPY
- Marketing: 10M JPY
- Infraestructura/otros: 5M JPY
- **EBITDA: -9M JPY (mejorando)**

**Year 3:**
- Ingresos recurrentes mensuales: 4M JPY (1,600 clientes)
- Ingresos recurrentes anuales: 72M JPY
- Costo de desarrollo: 25M JPY (expansion organizacional)
- Marketing: 15M JPY
- Infraestructura/otros: 8M JPY
- **EBITDA: 4M JPY (punto de equilibrio)**

[5. Riesgos y oportunidades]

**Riesgos a la baja:**
1. Caida de precios de la competencia
   - Asana baja a 100 JPY/usuario/ano
   - Contramedida: Continuar diferenciandose con funciones de IA

2. Tasa de cancelacion mas alta de lo esperado (10%/mes)
   - Impacto: Punto de equilibrio retrasado al Ano 2
   - Contramedida: Mejorar onboarding, construir casos de exito

3. Endurecimiento regulatorio (GDPR, etc.)
   - Contramedida: Implementar cumplimiento de forma proactiva

**Oportunidades al alza:**
1. Adquisicion de contratos grandes con 50 empresas
   - Ingresos adicionales de 1.5M JPY/mes
   - Reducir las perdidas del Ano 1 en un 20%

2. Ventas indirectas a traves de socios de API/integracion
   - Integracion con SaaS existentes (HR, ERP)

3. Expansion internacional (Sudeste Asiatico)
   - A gran escala desde el Ano 3, desarrollo de nuevos mercados

Genere el analisis completado en formato markdown.
```

**Resultado esperado**: Se completa el análisis del caso de negocio (tamaño de mercado, 3C, modelo de ingresos, pronostico P&L).

---

## 🚀 Paso 4: Integración de resultados de revisión

Consolide los tres resultados de revisión y cree un plan de acción de mejora.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Incorporacion de resultados de revision",
  "questions": [{
    "id": "integration_method",
    "prompt": "Como desea incorporar los resultados de la revision?",
    "options": [
      {"id": "auto_update", "label": "Actualizar automaticamente el PRD"},
      {"id": "action_list", "label": "Crear solo una lista de mejoras"},
      {"id": "important_only", "label": "Incorporar solo los hallazgos criticos"},
      {"id": "review_first", "label": "Revisar todo antes de decidir"}
    ]
  }]
}
```

(auto_update → Ejecutar actualización automática del PRD)
(action_list → Crear lista de mejoras)
(important_only → Crear lista priorizada)
(review_first → Crear informe integrado para revisión)

**Después de la selección (ejemplo)**:
Entrada:
```text
Consolide los tres resultados de revision (Devil's Advocate, Seguridad, Caso de negocio)
y cree output/pm/review-summary.md.

Formato:

# Informe de revision integrado de TaskFlow

## Resumen ejecutivo
- Calificacion general: (en escala de 5 puntos)
- Hallazgos clave: 3-5 elementos
- Acciones recomendadas: por prioridad

## 1. Resultados de la revision Devil's Advocate
### Hallazgos criticos
- [ ] Hallazgo 1
- [ ] Hallazgo 2
- [ ] Hallazgo 3

### Propuestas de mejora
- Propuesta 1: Dificultad de implementacion (Baja/Media/Alta), Prioridad (P0/P1/P2)
- Propuesta 2: ...

## 2. Resultados de la revision de seguridad
### Amenazas de alto riesgo (implementacion obligatoria)
- Amenaza 1 → Contramedida y cronograma de implementacion

### Amenazas de riesgo medio (implementacion temprana recomendada)
- Amenaza 2 → Contramedida y cronograma de implementacion

### Amenazas de bajo riesgo (pueden abordarse despues)
- Amenaza 3 → Contramedida y cronograma de implementacion

## 3. Resultados de la revision del caso de negocio
### Decision de gestion
- Es suficiente el tamano del mercado: Si / No / Base del juicio
- Expectativa de ROI: Apropiada / Margen de mejora
- Ventaja competitiva: Esta asegurada?

### Acciones
- Inversion en marketing: Decision de aumentar/mantener/reducir
- Alcance de desarrollo: Necesidad de ajuste

## 4. Juicio integrado y proximos pasos

### Decision Go/No-Go
- Actual: Go → Con las siguientes condiciones
  * Condicion 1: Cumplir XXX
  * Condicion 2: Implementar XXX

O en caso de No-Go:
- Propuesta: Reconsiderar despues de mejorar XXX

### Plan de accion por prioridad

**Fase 0 (Decision Go/No-Go):**
- Accion 1: XXX (responsable, duracion)
- Accion 2: XXX (responsable, duracion)

**Fase 1 (Antes del desarrollo MVP):**
- Accion 1: Crear documento de diseno de seguridad (Ingeniero de seguridad, 1 semana)
- Accion 2: Validacion de mercado (PM, 2 semanas)

**Fase 2 (Durante el desarrollo MVP):**
- Accion 1: Pruebas de seguridad (QA, continuo)
- Accion 2: Recopilacion de retroalimentacion del cliente (CS, continuo)

**Fase 3 (Post-MVP):**
- Accion 1: Auditoria de seguridad (externa, 1 mes)
- Accion 2: Aceleracion de marketing (Ventas y Marketing)

## 5. Riesgos y preocupaciones
| Riesgo | Impacto | Contramedida |
|--------|------|------|
| R1 | Alto | ... |
| R2 | Medio | ... |

Guarde este informe despues de completarlo.
```

**Resultado esperado**: Se completa el plan de mejora que integra las tres revisiones.

---

## ⚠️ Problemas comunes y soluciones

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el que corresponda",
    "options": [
      {"id": "trouble_1", "label": "El Devil's Advocate es demasiado severo"},
      {"id": "trouble_2", "label": "No entiendo el analisis STRIDE"},
      {"id": "trouble_3", "label": "No se como estimar el tamano del mercado"},
      {"id": "trouble_4", "label": "prd.md no existe"}
    ]
  }]
}
```

### Problema 1: Devil's Advocate es demasiado severo
**Solución**: Cambie la severidad de la revisión a "suave." Al indicar "enfocarse en comentarios constructivos" en el prompt, obtendra consejos más accionables.

Depuración:
```text
Diga a la IA "intentelo de nuevo en un nivel suave," o
vuelva a ejecutar con severity="soft" en la nueva entrada
```

### Problema 2: No entiende el análisis STRIDE
**Solución**: Revise la definición de cada categoría STRIDE:

| Amenaza | Descripción | Ejemplo |
|------|------|-----|
| Spoofing | Suplantación de autenticación de usuario | Interceptación de contraseñas, secuestro de sesión |
| Tampering | Falsificación de datos | Modificación no autorizada de datos de tareas, manipulación directa de BD |
| Repudiation | Negación de acciones | Afirmar "No realice esa operación" |
| Information Disclosure | Fuga de información | Filtración de datos de usuario, interceptación |
| Denial of Service | Interrupción del servicio | DDoS, ataques de sobrecarga |
| Elevation of Privilege | Escalada de privilegios | Usuario regular obteniendo privilegios de administrador |

Solicite a la IA que "también muestre ejemplos específicos de STRIDE."

### Problema 3: No sabe como estimar el tamaño del mercado
**Solución**: Hay dos enfoques para la estimación del tamaño del mercado:

**Método descendente (top-down):**
```text
1. Numero de empresas nacionales (estadisticas) -> Empresas objetivo -> Tasa de adopcion -> Monto promedio de compra
2. Ejemplo: 3.8M empresas x 3% x 50% x 500K JPY = 28.5B JPY
```

**Método ascendente (bottom-up):**
```text
1. Clientes existentes (historial) -> Mercado alcanzable -> Tasa de crecimiento
2. Ejemplo: 100 empresas x 100 x 20% crecimiento = tamano de mercado de 2,000 empresas
```

Si no esta seguro, indique explícitamente multiples supuestos y muestre un análisis de sensibilidad de "que sucede cuando cambian los supuestos."

### Problema 4: prd.md no existe
**Solución**: Comience desde la Lección 18-3. Alternativamente, cree un PRD simplificado:

```markdown
# TaskFlow - PRD (Version simplificada)

## Descripcion general
Aplicacion web de gestion de tareas para empresas con 10-100 empleados

## Funciones principales
- Creacion y gestion de tareas
- Uso compartido en equipo
- Sugerencias de prioridad por IA
- Integracion con Slack

## Objetivo
PM/lideres en empresas medianas con 10-100 empleados

## Precios
500 JPY/usuario/mes
```

Proceda utilizando esta versión simplificada como base.

### Problema 5: Los archivos generados no se producen
**Solución**: Verifique si el directorio `output/pm/` existe:

```bash
mkdir -p output/pm
# Luego vuelva a ejecutar la generacion de revision
```

---

## ✅ Punto de control
- [ ] Recibio 3 o más observaciones de la revisión Devil's Advocate
- [ ] Analizo las 6 categorías STRIDE
- [ ] Creo el caso de negocio (tamaño de mercado o modelo de ingresos)
- [ ] Se ha generado output/pm/review-devils-advocate.md
- [ ] Se ha generado output/pm/review-security.md
- [ ] Se ha generado output/pm/review-business-case.md
- [ ] Extrajo las acciones de mejora clave de las tres revisiones
- [ ] Tomo una decisión de Go/No-Go


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── review-*.md  (coleccion de documentos de revision)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/review-*.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/review-*.md
```

> 💡 Texto completo: Ejecute `cat output/pm/review-*.md` para mostrar el texto completo

---

## ✅ Verificación de finalización
Introduzca lo siguiente en el chat de Codex para verificar el estado de finalización:

```text
Muestre una lista de archivos relacionados con la revision en output/pm/:

1. Numero de hallazgos en review-devils-advocate.md
2. Numero de amenazas de alto riesgo en review-security.md
3. Estimacion P&L a 3 anos en review-business-case.md

Verifique que estos tres archivos esten presentes.
```

**Resultado esperado**: Se verifica la completitud de los documentos de revisión.

---

## ➡️ Siguientes pasos

La Lección 18-4 (Fase A "Planificación") esta completa. A continuación, proceda a la Fase B "Definición de requisitos y diseño."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione como proceder",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente leccion (Especificacion de requisitos)"},
      {"id": "next_window", "label": "Iniciar /start-18-5 en una nueva ventana"},
      {"id": "review", "label": "Revisar los resultados una vez mas"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

- next_auto → Ejecutar /start-18-5
- next_window → Abrir /start-18-5 en una nueva ventana
- review → Volver a mostrar documentos de revisión
- finish → Finalizar

**Nota**: Fase A (Planificación) completada! A continuación, en la Fase B (Definición de requisitos y diseño), cree especificaciones de requisitos más detalladas.

