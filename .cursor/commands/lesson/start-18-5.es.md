---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-4", "output/pm/prd.md", "output/pm/requirements-brief.md"]
level: "intermediate"
tags: ["pm", "requirements-spec", "ipa"]
---

# 🎓 Lesson 18-5: Creación de especificación de requisitos

Tema: Crear una especificación de requisitos para TaskFlow basada en el formato IPA (Agencia de Promoción de Tecnologías de la Información).

## 📍 Lo que hará en esta sesión

| Elemento | Detalles |
|------|------|
| Objetivo | Crear un documento de definición de requisitos de TaskFlow basado en el formato IPA |
| Duración | ~25 min |
| Habilidades utilizadas | habilidad pm-toolkit |
| Requisitos previos | Lesson 18-4 completada, output/pm/prd.md y output/pm/requirements-brief.md existen |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

## 🎯 Verificación de preparación

```json
{
  "type": "AskQuestion",
  "question": "Antes de comenzar esta sesion, verifique lo siguiente. Cuales de los siguientes elementos estan completados?",
  "options": [
    {
      "label": "✓ Todo completado (continuar)",
      "value": "ready",
      "next": "step1"
    },
    {
      "label": "⚠️ 16-4 aun no esta completada",
      "value": "missing_14_4",
      "next": "abort_14_4"
    },
    {
      "label": "⚠️ No se encuentra el directorio output/pm/",
      "value": "missing_output",
      "next": "abort_output"
    }
  ],
  "hint": "Necesita los documentos de resumen de PRD y requisitos. Verifique los archivos creados en 16-4."
}
```

**Puntos de verificación de preparación:**
- [ ] La Lección 18-4 esta completada
- [ ] El archivo `output/pm/prd.md` existe
- [ ] El archivo `output/pm/requirements-brief.md` existe
- [ ] La habilidad pm-toolkit esta disponible

---

## 🚀 Paso 1: Carga de documentos PRD/requisitos y explicación de métodos de conversión

En este paso, aprenda la metodología para convertir el PRD y los documentos de requisitos creados hasta ahora en una especificación de requisitos en formato IPA.

```json
{
  "type": "AskQuestion",
  "question": "Tiene experiencia con la definicion de requisitos?",
  "options": [
    {
      "label": "Es mi primera vez",
      "value": "beginner",
      "detail": "Explicaremos cuidadosamente desde lo basico"
    },
    {
      "label": "Conozco los conceptos",
      "value": "intermediate",
      "detail": "Nos centraremos en los puntos clave del formato IPA"
    },
    {
      "label": "Tengo experiencia practica",
      "value": "experienced",
      "detail": "Sugeriremos un enfoque eficiente"
    }
  ],
  "hint": "El nivel de explicacion se ajustara segun su experiencia seleccionada."
}
```

**Explicación del Paso 1:**

La especificación de requisitos es un documento crítico que aclara "que construir." El formato IPA es el estándar oficial de Japon, con las siguientes características:

1. **Método de descripción estructurado**
   - Separar claramente requisitos funcionales y no funcionales
   - Asignar IDs unicos (ej., REQ-001) a cada requisito
   - Asegurar la trazabilidad

2. **Proceso de conversión de PRD a requisitos**
   ```text
   PRD (Especificacion del producto)
   → Extraccion de escenarios de usuario
   → Descomposicion de funcionalidades
   → Descripcion de requisitos
   → Revision y finalizacion
   ```

3. **Secciones principales del formato IPA**
   - Visión general del sistema
   - Requisitos funcionales (por pantalla/caso de uso)
   - Requisitos no funcionales (rendimiento, seguridad, disponibilidad, etc.)
   - Restricciones y dependencias
   - Definiciones de terminología y requisitos previos

**Resultado esperado:**
- Comprender el contenido del PRD y extraer elementos de requisitos
- Se comprende la estructura del formato IPA
- Listo para proceder al siguiente paso (detalle de requisitos funcionales)

---

## 🚀 Paso 2: Detallado de requisitos funcionales

En este paso, expanda las funciones descritas en el PRD por pantalla y defina la entrada, procesamiento, salida y restricciones de cada pantalla.

```json
{
  "type": "AskQuestion",
  "question": "Como desea organizar los requisitos funcionales?",
  "options": [
    {
      "label": "Definir por pantalla",
      "value": "screen_based",
      "detail": "Definicion de requisitos centrada en UI/pantalla. Facil de colaborar con disenadores UI"
    },
    {
      "label": "Definir por caso de uso",
      "value": "usecase_based",
      "detail": "Centrado en flujo de negocio. Mas abstracto y flexible"
    },
    {
      "label": "Obtener sugerencias de IA",
      "value": "ai_suggest",
      "detail": "Generar automaticamente la clasificacion optima a partir del PRD"
    }
  ],
  "hint": "TaskFlow es una herramienta centrada en UI, por lo que se recomienda definir por pantalla."
}
```

**Detalles del Paso 2:**

**Formato de descripción de requisitos funcionales:**

```text
REQ-F-001: Pantalla de creacion de tareas
  Descripcion: Pantalla para que los usuarios creen nuevas tareas

  Entrada:
    - Nombre de tarea (texto, obligatorio, maximo 100 caracteres)
    - Prioridad (desplegable: Alta/Media/Baja)
    - Fecha de vencimiento (selector de fecha, opcional)
    - Descripcion (area de texto, opcional, maximo 500 caracteres)

  Procesamiento:
    - Verificacion de validez de valores de entrada
    - Guardar tarea en la BD
    - Redirigir a la pantalla de lista de tareas

  Salida:
    - Mensaje de guardado exitoso
    - Agregar nueva tarea a la lista

  Restricciones:
    - El usuario debe estar autenticado
    - Se pueden crear multiples tareas con el mismo nombre
```

**Funciones principales en la definición de requisitos de TaskFlow (ejemplos):**

1. **REQ-F-001: Creación de espacio de trabajo**
   - Entrada: Nombre del espacio de trabajo, descripción, configuración de miembros
   - Procesamiento: Inicialización de permisos de miembros, generación de tareas iniciales
   - Salida: Agregado a la lista de espacios de trabajo

2. **REQ-F-002: Creación de tareas**
   - Entrada: Título, descripción, prioridad, fecha límite, responsable
   - Procesamiento: Generación de ID de tarea, inicialización de estado
   - Salida: Navegar a la pantalla de detalle de tarea

3. **REQ-F-003: Actualización de estado de tarea**
   - Entrada: ID de tarea, nuevo estado
   - Procesamiento: Verificación de reglas de transición de estado, registro de marca de tiempo
   - Salida: Mensaje de confirmación de actualización

4. **REQ-F-004: Busqueda/filtro de tareas**
   - Entrada: Palabras clave, prioridad, estado, responsable
   - Procesamiento: Busqueda con condiciones multiples, ordenamiento
   - Salida: Lista de tareas coincidentes

5. **REQ-F-005: Agregar comentario**
   - Entrada: ID de tarea, texto del comentario
   - Procesamiento: Guardado de comentario, notificación de mención
   - Salida: Agregado al area de visualización de comentarios

De manera similar, detalle 10 o más funciones a continuación.

**Resultado esperado:**
- Se han definido al menos 10 requisitos funcionales
- Se documentan la entrada, procesamiento, salida y restricciones de cada función
- La sección de requisitos funcionales de requirements-spec.md esta completada

---

## 🚀 Paso 3: Cuantificación de requisitos no funcionales

Los requisitos no funcionales son atributos de calidad del sistema. Es importante establecer valores numéricos específicos en lugar de términos vagos como "rápido" o "seguro."

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el nivel de requisitos no funcionales",
  "options": [
    {
      "label": "Para startups (flexible)",
      "value": "startup",
      "detail": "Requisitos en etapa MVP. Estandares de calidad minimos"
    },
    {
      "label": "Para empresas (estandar)",
      "value": "enterprise",
      "detail": "Estandar SaaS general. Criterios equilibrados"
    },
    {
      "label": "Para finanzas/salud (estricto)",
      "value": "strict",
      "detail": "Enfocado en cumplimiento. Alta disponibilidad y seguridad"
    }
  ],
  "hint": "Si TaskFlow aspira a ser un SaaS B2B, se recomienda el nivel empresarial (estandar)."
}
```

**Detalles del Paso 3:**

**Requisitos de rendimiento (ejemplos de estándar de startup):**

| Elemento | Requisito | Justificación |
|------|------|------|
| Tiempo de respuesta (visualización de página) | Menos de 2 segundos | La tasa de abandono de usuarios aumenta a los 3 segundos |
| Tiempo de respuesta (API) | Menos de 500ms | Menos de 2 segundos incluyendo procesamiento frontend |
| Conexiones simultaneas (inicial) | 100 | Número de usuarios asumido en etapa MVP |
| Tiempo de ejecución de consulta BD | Menos de 100ms | Multiples consultas dentro de la respuesta API |

**Requisitos de rendimiento (ejemplos de estándar empresarial):**

| Elemento | Requisito | Justificación |
|------|------|------|
| Tiempo de respuesta (visualización de página) | Menos de 1 segundo | Estándar de productividad de usuarios empresariales |
| Tiempo de respuesta (API) | Menos de 200ms | Requisito de SLA 99.5% |
| Conexiones simultaneas | 1000+ | Demanda asumida en etapa de crecimiento |
| Tiempo de ejecución de consulta BD | Menos de 50ms | Diseño de índices más estricto |

**Requisitos de disponibilidad:**

| Elemento | Requisito (empresarial) | Justificación |
|------|------|------|
| Tiempo de actividad | 99.5% | Tiempo de inactividad mensual 3.6 horas |
| Mantenimiento planificado | Una vez al mes, máximo 4 horas | Evitar dias festivos japoneses |
| Tiempo de respuesta de emergencia | Dentro de 15 minutos | Desde la detección de fallo hasta el inicio de respuesta |
| Tiempo de recuperación (RTO) | Dentro de 1 hora | Recuperación desde respaldo de BD |

**Requisitos de seguridad:**

| Elemento | Requisito | Método de implementación |
|------|------|------|
| Autenticación | OAuth 2.0 + soporte MFA | Inicio de sesión Google/GitHub, TOTP |
| Comunicación | HTTPS (TLS 1.2+) | Cifrado de todos los endpoints |
| Contraseña | Hash SHA-256 con salt | Usando biblioteca bcrypt |
| Autenticación API | JWT (expiración de 24 horas) | Detección de alteración mediante firma de token |
| Retención de registros | 12 meses | Cumplimiento de auditoría |

**Requisitos de escalabilidad:**

| Elemento | Requisito | Implementación planificada |
|------|------|------|
| Almacenamiento | Supuesto de crecimiento 1TB/año | S3 + cache CloudFront |
| Número de usuarios | Soporte hasta 10,000 usuarios | Diseño de escalado horizontal |
| Base de datos | Soporte de replica de lectura | Configuración maestro-esclavo |

**Resultado esperado:**
- Los requisitos de rendimiento estan cuantificados (ej., "menos de 2 segundos")
- Se han definido los requisitos de disponibilidad, seguridad y escalabilidad
- Cada requisito tiene documentado el fundamento (objetivos de negocio o mejores prácticas)
- La sección de requisitos no funcionales de requirements-spec.md esta completada

---

## 🚀 Paso 4: Generación de requirements-spec.md

En este paso, genere los requisitos funcionales y no funcionales definidos hasta ahora como un archivo integrado requirements-spec.md.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el formato de salida",
  "options": [
    {
      "label": "Version de documento completo",
      "value": "full",
      "detail": "Version completa que cubre todos los requisitos (equivalente a 15-20 paginas)"
    },
    {
      "label": "Version resumida",
      "value": "summary",
      "detail": "Version concisa con solo los requisitos principales (equivalente a 5-8 paginas)"
    },
    {
      "label": "Version con revision de IA",
      "value": "with_review",
      "detail": "Version donde la IA verifica requisitos faltantes o contradictorios"
    }
  ],
  "hint": "Para principiantes, se recomienda la version de documento completo. Puede reorganizar despues."
}
```

**Detalles del Paso 4:**

Genere requirements-spec.md usando la habilidad pm-toolkit:

```bash
pm-toolkit generate-requirements-spec \
  --prd output/pm/prd.md \
  --brief output/pm/requirements-brief.md \
  --format full \
  --include-nfr true \
  --output output/pm/requirements-spec.md
```

**Estructura del archivo generado:**

1. **Encabezado del documento**
   - Título: Especificación de requisitos de TaskFlow
   - Versión: 1.0
   - Fecha de creación: [fecha de hoy]
   - Última actualización: [fecha de hoy]

2. **Tabla de contenidos**
   - Generada automáticamente

3. **1. Introducción**
   - Visión general del sistema
   - Alcance
   - Partes interesadas

4. **2. Documentos de referencia**
   - Enlace al PRD (prd.md)
   - Enlace al informe de requisitos (requirements-brief.md)

5. **3. Requisitos funcionales**
   - REQ-F-001〜REQ-F-XXX
   - Entrada, procesamiento, salida y restricciones para cada requisito

6. **4. Requisitos no funcionales**
   - 4.1 Requisitos de rendimiento (REQ-NFR-P-001, etc.)
   - 4.2 Disponibilidad/fiabilidad (REQ-NFR-A-001, etc.)
   - 4.3 Requisitos de seguridad (REQ-NFR-S-001, etc.)
   - 4.4 Escalabilidad (REQ-NFR-SC-001, etc.)

7. **5. Requisitos de interfaz externa**
   - Lista de endpoints API
   - Especificaciones de integración de datos

8. **6. Restricciones y precondiciones**
   - Restricciones técnicas
   - Restricciones de negocio

9. **7. Definiciones de terminología**
   - Términos importantes utilizados dentro del sistema

10. **8. Matriz de trazabilidad**
    - Mapeo de requisitos del PRD ↔ requisitos de la especificación de requisitos

**Verificaciones posteriores a la generación:**

- [ ] El archivo se ha generado en output/pm/requirements-spec.md
- [ ] El tamaño del archivo es 10KB o más (el contenido es sustancial)
- [ ] Se han definido 10 o más requisitos funcionales
- [ ] Los requisitos no funcionales incluyen valores numéricos
- [ ] Se ha creado la matriz de trazabilidad

**Resultado esperado:**
- Se ha generado el archivo output/pm/requirements-spec.md
- Todos los requisitos estan organizados en formato IPA
- Se asegura la trazabilidad
- El documento que sirve como entrada para el siguiente paso (descripción de casos de uso) esta completo

---

## ⚠️ Problemas comunes y soluciones

```json
{
  "type": "AskQuestion",
  "question": "Que problema esta experimentando?",
  "options": [
    {
      "label": "Archivos PRD/requisitos no encontrados",
      "value": "missing_files"
    },
    {
      "label": "Demasiadas funcionalidades para organizar",
      "value": "too_many_features"
    },
    {
      "label": "Indeciso sobre los valores de requisitos no funcionales",
      "value": "nfr_numbers"
    },
    {
      "label": "Error de generacion de requirements-spec.md",
      "value": "generation_error"
    },
    {
      "label": "La matriz de trazabilidad esta en blanco",
      "value": "traceability_blank"
    }
  ],
  "hint": "Seleccione el problema aplicable y se mostrara la solucion."
}
```

**Soluciones por tipo de problema:**

### Archivos de PRD/requisitos no encontrados

**Causa:** Se omitio la Lección 18-4, o el archivo se guardo en una ubicación diferente

**Comandos de verificación:**
```bash
ls -la output/pm/
find . -name "prd.md"
find . -name "requirements-brief.md"
```

**Solución:**
1. Vuelva a la Lección 18-4 y cree el PRD
2. Una vez generado el archivo, copielo al directorio output/pm/
```bash
cp ~/prd.md output/pm/prd.md
```

### Demasiadas funciones para organizar

**Causa:** Intentando incluir todas las funciones descritas en el PRD como requisitos

**Use el método MoSCoW:**
- **Must have (imprescindible)**: Necesario en la etapa MVP
- **Should have (recomendable)**: Implementar en la siguiente fase
- **Could have (deseable)**: En una fase futura
- **Won't have (innecesario)**: Fuera de alcance

**Respuesta:**
1. Clasifique las funciones del PRD en 3 categorías
2. Límite la especificación de requisitos solo a Must have (aproximadamente 10-15)
3. Documente Should/Could en un documento separado (backlog.md)

### Inseguro sobre los valores de requisitos no funcionales

**Valores de referencia de mejores prácticas generales:**

**Para startups:**
- Tiempo de respuesta: 2-3 segundos
- Conexiones simultaneas: 100-500
- Tiempo de actividad: 99%
- Autenticación multifactor: Opcional

**Para SaaS empresarial:**
- Tiempo de respuesta: Menos de 1 segundo
- Conexiones simultaneas: 1000+
- Tiempo de actividad: 99.5%
- Autenticación multifactor: Obligatoria

**Solución:**
1. Calcule hacia atras desde los objetivos de negocio (ingresos, proyecciones de usuarios)
2. Consulte los SLA de productos competidores
3. Si no esta seguro, marque como "TBD" (a revisar más adelante)

### Error de generación de requirements-spec.md

**Errores comunes:**

```text
Error: prd.md not found
```
→ Verifique la ruta del archivo. Especifique la ruta completa.

```text
Error: Invalid YAML header
```
→ Verifique el front matter YAML de requirements-brief.md.

**Solución:**
```bash
# Verificar existencia del archivo
test -f output/pm/prd.md && echo "OK" || echo "NOT FOUND"

# Validacion JSON (incluyendo YAML)
python3 -c "import yaml; yaml.safe_load(open('output/pm/requirements-brief.md'))"  # En Windows, use python en lugar de python3

# Verificar version de pm-toolkit
pm-toolkit version
```

### La matriz de trazabilidad esta en blanco

**Causa:** No se ha realizado el mapeo de IDs de requisitos entre el PRD y requirements-spec.md

**Solución:**
1. Agregue IDs a cada requisito del PRD (ej., PR-001, PR-002)
2. En requirements-spec.md, documente cada requisito para hacer referencia a PR-XXX
3. Cree manualmente la matriz de trazabilidad

**Plantilla:**

| ID PRD | Requisito PRD | ID especificación de requisito | Estado |
|--------|--------|---------|----------|
| PR-001 | Gestión de espacio de trabajo | REQ-F-001 | ✓ |
| PR-002 | Gestión de tareas | REQ-F-002 a REQ-F-005 | ✓ |

---

## ✅ Punto de control

Cuando se complete esta sesión, verifique que todos los siguientes elementos esten marcados:

- [ ] **Paso 1: Carga del PRD**
  - [ ] Se comprende el contenido del PRD (prd.md)
  - [ ] El propósito de la definición de requisitos es claro
  - [ ] Se comprende la estructura del formato IPA

- [ ] **Paso 2: Definición de requisitos funcionales**
  - [ ] Se han definido 10 o más requisitos funcionales
  - [ ] Se documentan la entrada, procesamiento y salida de cada función
  - [ ] Numerados secuencialmente como REQ-F-001 hasta REQ-F-XXX
  - [ ] Las restricciones estan documentadas

- [ ] **Paso 3: Cuantificación de requisitos no funcionales**
  - [ ] Los requisitos de rendimiento tienen valores numéricos específicos
  - [ ] Se han definido los requisitos de disponibilidad (tiempo de actividad, RTO, etc.)
  - [ ] Los requisitos de seguridad estan documentados
  - [ ] Se han definido los requisitos de escalabilidad

- [ ] **Paso 4: Generación de archivos**
  - [ ] El archivo output/pm/requirements-spec.md existe
  - [ ] El tamaño del archivo es 10KB o más
  - [ ] La tabla de contenidos se genera automáticamente en el documento
  - [ ] Se incluye la matriz de trazabilidad

- [ ] **General**
  - [ ] No han ocurrido problemas
  - [ ] Se ha previsualizado el archivo generado y verificado el contenido
  - [ ] Listo para comenzar la Lección 18-6


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── requirements-spec.md  (Especificacion de requisitos)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/requirements-spec.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/requirements-spec.md
```

> 💡 Texto completo: Ejecute `cat output/pm/requirements-spec.md` para mostrar el texto completo

---

## ➡️ Siguientes pasos

```json
{
  "type": "AskQuestion",
  "question": "Seleccione la siguiente accion para esta sesion",
  "options": [
    {
      "label": "✓ Todos los puntos de verificacion completados → Continuar a 18-6",
      "value": "proceed_14_6",
      "next": "start-18-6"
    },
    {
      "label": "⚠️ Quiero revisar los requisitos nuevamente",
      "value": "review_requirements",
      "detail": "Reeditar requirements-spec.md"
    },
    {
      "label": "❓ El problema no se ha resuelto",
      "value": "troubleshoot",
      "detail": "Volver a la resolucion de problemas"
    },
    {
      "label": "📚 Quiero consultar el material del curso",
      "value": "reference",
      "detail": "Mostrar la explicacion detallada del Modulo 18"
    }
  ],
  "hint": "Si todos los puntos de verificacion estan completados, continue con la Leccion 18-6 (Descripcion de casos de uso y diagramas de secuencia)."
}
```

**Que hacer en 18-6:**

En la siguiente sesión "Lección 18-6: Descripción de casos de uso y diagramas de secuencia":

1. **Creación de diagramas de casos de uso (UML)**
   - Definición de actores (usuarios, administradores, sistemas externos)
   - Relaciones de casos de uso (include, extend)

2. **Descripciones detalladas de casos de uso**
   - Precondiciones y postcondiciones
   - Flujo principal y flujo de excepción
   - Manejo de excepciones

3. **Creación de diagramas de secuencia**
   - Representación cronologica de los principales procesos de negocio
   - Interacciones entre sistemas

4. **Archivos de salida**
   - usecase-diagram.md (diagrama de casos de uso)
   - usecases-detail.md (casos de uso detallados)
   - sequence-diagrams.md (diagramas de secuencia)

---

**Ha completado esta sesión. Felicidades! 🎉**

Si tiene preguntas o problemas, consulte la sección de "Solución de problemas" anterior.
