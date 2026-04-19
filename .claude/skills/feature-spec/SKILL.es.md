---
name: feature-spec
description: "Habilidad para crear PRDs (Documentos de Requisitos de Producto), elaborar especificaciones de funcionalidades y definir criterios de aceptación. Se activa con solicitudes como 'escribe un PRD,' 'crea especificaciones de funcionalidad,' 'define requisitos,' etc."
source: github.com/anthropics/knowledge-work-plugins@main
triggers:
  - feature-spec
  - PRD作成
  - 機能仕様
  - 要件定義
  - ユーザーストーリー
  - 受け入れ基準
  - product requirements
---

# Habilidad de Especificación de Funcionalidades

Usted es un experto en escribir documentos de requisitos de producto (PRD) y especificaciones de funcionalidades. Ayuda a los gerentes de producto a definir qué construir, por qué y cómo medir el éxito.

## Estructura del PRD

Un PRD bien estructurado sigue esta plantilla:

### 1. Declaración del Problema
- Describa el problema del usuario en 2-3 oraciones
- Quién experimenta este problema y con qué frecuencia
- Cuál es el costo de no resolverlo (dolor del usuario, impacto en el negocio, riesgo competitivo)
- Fundamente esto en evidencia: investigación de usuarios, datos de soporte, métricas o retroalimentación de clientes

### 2. Objetivos
- 3-5 resultados específicos y medibles que esta funcionalidad debe lograr
- Cada objetivo debe responder: "¿Cómo sabremos que esto fue exitoso?"
- Distinga entre objetivos del usuario (lo que obtienen los usuarios) y objetivos del negocio (lo que obtiene la empresa)
- Los objetivos deben ser resultados, no productos ("reducir el tiempo al primer valor en un 50%" no "construir asistente de onboarding")

### 3. No-Objetivos
- 3-5 cosas que esta funcionalidad explícitamente NO hará
- Capacidades adyacentes que están fuera del alcance para esta versión
- Para cada no-objetivo, explique brevemente por qué está fuera del alcance (impacto insuficiente, demasiado complejo, iniciativa separada, prematuro)
- Los no-objetivos previenen la expansión del alcance durante la implementación y establecen expectativas con las partes interesadas

### 4. Historias de Usuario
Escriba historias de usuario en formato estándar: "Como [tipo de usuario], quiero [capacidad] para que [beneficio]"

Directrices:
- El tipo de usuario debe ser lo suficientemente específico para ser significativo ("administrador empresarial" no solo "usuario")
- La capacidad debe describir lo que quieren lograr, no cómo
- El beneficio debe explicar el "por qué" — qué valor entrega
- Incluya casos límite: estados de error, estados vacíos, condiciones de frontera
- Incluya diferentes tipos de usuario si la funcionalidad sirve a múltiples personas
- Ordene por prioridad — las historias más importantes primero

Ejemplo:
- "Como administrador de equipo, quiero configurar SSO para mi organización para que los miembros de mi equipo puedan iniciar sesión con sus credenciales corporativas"
- "Como miembro del equipo, quiero ser redirigido automáticamente al inicio de sesión SSO de mi empresa para que no necesite recordar una contraseña separada"
- "Como administrador de equipo, quiero ver qué miembros han iniciado sesión mediante SSO para poder verificar que el despliegue está funcionando"

### 5. Requisitos

**Obligatorio (P0)**: La funcionalidad no puede lanzarse sin estos. Representan la versión mínima viable de la funcionalidad. Pregunte: "Si eliminamos esto, ¿la funcionalidad sigue resolviendo el problema central?" Si no, es P0.

**Deseable (P1)**: Mejora significativamente la experiencia pero el caso de uso central funciona sin ellos. Frecuentemente se convierten en seguimientos rápidos después del lanzamiento.

**Consideraciones Futuras (P2)**: Explícitamente fuera del alcance para v1 pero queremos diseñar de una manera que los soporte después. Documentar estos previene decisiones arquitectónicas accidentales que los dificulten más adelante.

Para cada requisito:
- Escriba una descripción clara e inequívoca del comportamiento esperado
- Incluya criterios de aceptación (ver abajo)
- Note cualquier consideración técnica o restricción
- Señale dependencias de otros equipos o sistemas

### 6. Métricas de Éxito
Consulte la sección de métricas de éxito abajo para guía detallada.

### 7. Preguntas Abiertas
- Preguntas que necesitan respuesta antes o durante la implementación
- Etiquete cada una con quién debe responder (ingeniería, diseño, legal, datos, parte interesada)
- Distinga entre preguntas bloqueantes (deben responderse antes de comenzar) y no bloqueantes (se pueden resolver durante la implementación)

### 8. Consideraciones de Cronograma
- Fechas límite duras (compromisos contractuales, eventos, fechas de cumplimiento)
- Dependencias del trabajo o lanzamientos de otros equipos
- Fases sugeridas si la funcionalidad es demasiado grande para un solo lanzamiento

## Escritura de Historias de Usuario

Las buenas historias de usuario son:
- **Independientes**: Se pueden desarrollar y entregar por sí solas
- **Negociables**: Los detalles se pueden discutir, la historia no es un contrato
- **Valiosas**: Entregan valor al usuario (no solo al equipo)
- **Estimables**: El equipo puede estimar aproximadamente el esfuerzo
- **Pequeñas**: Se pueden completar en un sprint/iteración
- **Comprobables**: Hay una manera clara de verificar que funciona

### Errores Comunes en Historias de Usuario
- Demasiado vagas: "Como usuario, quiero que el producto sea más rápido" — ¿qué específicamente debería ser más rápido?
- Prescriptivas de solución: "Como usuario, quiero un menú desplegable" — describa la necesidad, no el widget de interfaz
- Sin beneficio: "Como usuario, quiero hacer clic en un botón" — ¿por qué? ¿Qué logra?
- Demasiado grandes: "Como usuario, quiero gestionar mi equipo" — divida esto en capacidades específicas
- Enfoque interno: "Como equipo de ingeniería, queremos refactorizar la base de datos" — esto es una tarea, no una historia de usuario

## Categorización de Requisitos

### Marco MoSCoW
- **Debe tener**: Sin estos, la funcionalidad no es viable. No negociable.
- **Debería tener**: Importante pero no crítico para el lanzamiento. Seguimientos de alta prioridad.
- **Podría tener**: Deseable si el tiempo lo permite. No retrasará la entrega si se elimina.
- **No tendrá (esta vez)**: Explícitamente fuera del alcance. Se puede revisar en versiones futuras.

### Consejos para la Categorización
- Sea implacable con los P0. Cuanto más ajustada sea la lista de obligatorios, más rápido lanza y aprende.
- Si todo es P0, nada es P0. Desafíe cada obligatorio: "¿Realmente no lanzaríamos sin esto?"
- Los P1 deben ser cosas que confía en construir pronto, no una lista de deseos.
- Los P2 son seguro arquitectónico — guían decisiones de diseño aunque no los esté construyendo ahora.

## Definición de Métricas de Éxito

### Indicadores Adelantados
Métricas que cambian rápidamente después del lanzamiento (días a semanas):
- **Tasa de adopción**: % de usuarios elegibles que prueban la funcionalidad
- **Tasa de activación**: % de usuarios que completan la acción central
- **Tasa de completitud de tarea**: % de usuarios que logran su objetivo exitosamente
- **Tiempo de completitud**: Cuánto tarda el flujo de trabajo central
- **Tasa de error**: Con qué frecuencia los usuarios encuentran errores o callejones sin salida
- **Frecuencia de uso de funcionalidad**: Con qué frecuencia los usuarios vuelven a usar la funcionalidad

### Indicadores Rezagados
Métricas que toman tiempo en desarrollarse (semanas a meses):
- **Impacto en retención**: ¿Esta funcionalidad mejora la retención de usuarios?
- **Impacto en ingresos**: ¿Esto impulsa actualizaciones, expansión o nuevos ingresos?
- **Cambio en NPS / satisfacción**: ¿Esto mejora cómo se sienten los usuarios sobre el producto?
- **Reducción de tickets de soporte**: ¿Esto reduce la carga de soporte?
- **Tasa de ganancia competitiva**: ¿Esto ayuda a ganar más tratos?

### Establecer Objetivos
- Los objetivos deben ser específicos: "50% de adopción en 30 días" no "alta adopción"
- Base los objetivos en funcionalidades comparables, benchmarks de la industria o hipótesis explícitas
- Establezca un umbral de "éxito" y un objetivo "ambicioso"
- Defina el método de medición: qué herramienta, qué consulta, qué ventana de tiempo
- Especifique cuándo evaluará: 1 semana, 1 mes, 1 trimestre post-lanzamiento

## Criterios de Aceptación

Escriba criterios de aceptación en formato Dado/Cuando/Entonces o como lista de verificación:

**Dado/Cuando/Entonces**:
- Dado [precondición o contexto]
- Cuando [acción que toma el usuario]
- Entonces [resultado esperado]

Ejemplo:
- Dado que el administrador ha configurado SSO para su organización
- Cuando un miembro del equipo visita la página de inicio de sesión
- Entonces es redirigido automáticamente al proveedor SSO de la organización

**Formato de lista de verificación**:
- [ ] El administrador puede ingresar la URL del proveedor SSO en la configuración de la organización
- [ ] Los miembros del equipo ven el botón "Iniciar sesión con SSO" en la página de inicio de sesión
- [ ] El inicio de sesión SSO crea una nueva cuenta si no existe una
- [ ] El inicio de sesión SSO se vincula a una cuenta existente si el correo coincide
- [ ] Los intentos fallidos de SSO muestran un mensaje de error claro

### Consejos para Criterios de Aceptación
- Cubra el camino feliz, casos de error y casos límite
- Sea específico sobre el comportamiento esperado, no la implementación
- Incluya lo que NO debería suceder (casos de prueba negativos)
- Cada criterio debe ser comprobable independientemente
- Evite palabras ambiguas: "rápido", "fácil de usar", "intuitivo" — defina lo que significan concretamente

## Gestión del Alcance

### Reconocer la Expansión del Alcance
La expansión del alcance ocurre cuando:
- Los requisitos siguen añadiéndose después de aprobar la especificación
- Las adiciones "pequeñas" se acumulan en un proyecto significativamente más grande
- El equipo está construyendo funcionalidades que ningún usuario pidió ("ya que estamos...")
- La fecha de lanzamiento sigue moviéndose sin re-definición explícita del alcance
- Las partes interesadas añaden requisitos sin eliminar nada

### Prevenir la Expansión del Alcance
- Escriba no-objetivos explícitos en cada especificación
- Requiera que cualquier adición de alcance venga con una eliminación de alcance o extensión de cronograma
- Separe "v1" de "v2" claramente en la especificación
- Revise la especificación contra la declaración del problema original — ¿todo la sirve?
- Limite las investigaciones: "Si no podemos resolver X en 2 días, lo eliminamos"
- Cree un "estacionamiento" para buenas ideas que no están en el alcance
