---
name: agent-designer
description: "Kit de herramientas para el diseno de arquitectura de sistemas multiagente. Se activa con solicitudes como 'disenar un agente', 'configuracion multiagente', 'arquitectura de agentes', 'diseno de orquestacion', etc."
source: github.com/alirezarezvani/claude-skills@main
triggers:
  - agent-designer
  - diseno de agentes
  - multiagente
  - arquitectura de agentes
  - diseno de orquestacion
  - multi-agent
  - agent architecture
  - エージェント設計
  - マルチエージェント
---
# Disenador de Agentes - Arquitectura de Sistemas Multiagente

**Nivel:** POTENTE  
**Categoria:** Ingenieria  
**Etiquetas:** Agentes de IA, arquitectura, diseno de sistemas, orquestacion, sistemas multiagente

## Descripcion General

Agent Designer es un kit de herramientas integral para disenar, arquitectar y evaluar sistemas multiagente. Proporciona enfoques estructurados para patrones de arquitectura de agentes, principios de diseno de herramientas, estrategias de comunicacion y marcos de evaluacion de rendimiento para construir sistemas de agentes de IA robustos y escalables.

## Capacidades Principales

### 1. Patrones de Arquitectura de Agentes

#### Patron de Agente Unico
- **Caso de Uso:** Tareas simples y enfocadas con limites claros
- **Ventajas:** Complejidad minima, depuracion facil, comportamiento predecible
- **Desventajas:** Escalabilidad limitada, punto unico de fallo
- **Implementacion:** Interaccion directa usuario-agente con acceso integral a herramientas

#### Patron Supervisor
- **Caso de Uso:** Descomposicion jerarquica de tareas con control centralizado
- **Arquitectura:** Un agente supervisor coordinando multiples agentes especialistas
- **Ventajas:** Estructura de mando clara, toma de decisiones centralizada
- **Desventajas:** Cuello de botella del supervisor, logica de coordinacion compleja
- **Implementacion:** El supervisor recibe tareas, delega a especialistas, agrega resultados

#### Patron Enjambre
- **Caso de Uso:** Resolucion distribuida de problemas con colaboracion entre pares
- **Arquitectura:** Multiples agentes autonomos con objetivos compartidos
- **Ventajas:** Alto paralelismo, tolerancia a fallos, inteligencia emergente
- **Desventajas:** Coordinacion compleja, conflictos potenciales, mas dificil de predecir
- **Implementacion:** Descubrimiento de agentes, mecanismos de consenso, asignacion distribuida de tareas

#### Patron Jerarquico
- **Caso de Uso:** Sistemas complejos con multiples capas organizacionales
- **Arquitectura:** Estructura de arbol con gerentes y trabajadores en diferentes niveles
- **Ventajas:** Mapeo organizacional natural, responsabilidades claras
- **Desventajas:** Sobrecarga de comunicacion, cuellos de botella potenciales en cada nivel
- **Implementacion:** Delegacion multinivel con ciclos de retroalimentacion

#### Patron Pipeline
- **Caso de Uso:** Procesamiento secuencial con etapas especializadas
- **Arquitectura:** Agentes organizados en pipeline de procesamiento
- **Ventajas:** Flujo de datos claro, optimizacion especializada por etapa
- **Desventajas:** Cuellos de botella secuenciales, orden de procesamiento rigido
- **Implementacion:** Colas de mensajes entre etapas, transferencias de estado

### 2. Definicion de Roles de Agentes

#### Marco de Especificacion de Roles
- **Identidad:** Nombre, declaracion de proposito, competencias principales
- **Responsabilidades:** Tareas principales, limites de decision, criterios de exito
- **Capacidades:** Herramientas requeridas, dominios de conocimiento, limites de procesamiento
- **Interfaces:** Formatos de entrada/salida, protocolos de comunicacion
- **Restricciones:** Limites de seguridad, limites de recursos, directrices operativas

#### Arquetipos Comunes de Agentes

**Agente Coordinador**
- Orquesta flujos de trabajo multiagente
- Toma decisiones de alto nivel y asigna recursos
- Monitorea la salud y el rendimiento del sistema
- Maneja escalaciones y resolucion de conflictos

**Agente Especialista**
- Experiencia profunda en un dominio especifico (codigo, datos, investigacion)
- Herramientas y conocimiento optimizados para tareas especializadas
- Salida de alta calidad dentro de un alcance estrecho
- Protocolos claros de transferencia para solicitudes fuera de alcance

**Agente de Interfaz**
- Maneja interacciones externas (usuarios, APIs, sistemas)
- Traduccion de protocolos y conversion de formatos
- Gestion de autenticacion y autorizacion
- Optimizacion de la experiencia del usuario

**Agente Monitor**
- Monitoreo de salud del sistema y alertas
- Recopilacion y analisis de metricas de rendimiento
- Deteccion y reporte de anomalias
- Mantenimiento de cumplimiento y registro de auditoria

### 3. Principios de Diseno de Herramientas

#### Diseno de Esquemas
- **Validacion de Entrada:** Tipado fuerte, parametros requeridos vs opcionales
- **Consistencia de Salida:** Formatos de respuesta estandarizados, manejo de errores
- **Documentacion:** Descripciones claras, ejemplos de uso, casos limite
- **Versionado:** Compatibilidad retroactiva, rutas de migracion

#### Patrones de Manejo de Errores
- **Degradacion Elegante:** Funcionalidad parcial cuando las dependencias fallan
- **Logica de Reintentos:** Retroceso exponencial, disyuntores, intentos maximos
- **Propagacion de Errores:** Respuestas de error estructuradas, clasificacion de errores
- **Estrategias de Recuperacion:** Metodos alternativos, enfoques diferentes

#### Requisitos de Idempotencia
- **Operaciones Seguras:** Operaciones de lectura sin efectos secundarios
- **Escrituras Idempotentes:** La misma operacion puede repetirse de forma segura
- **Gestion de Estado:** Seguimiento de versiones, resolucion de conflictos
- **Atomicidad:** Completacion de operacion todo-o-nada

### 4. Patrones de Comunicacion

#### Paso de Mensajes
- **Mensajeria Asincrona:** Agentes desacoplados, colas de mensajes
- **Formato de Mensaje:** Cargas estructuradas con metadatos
- **Garantias de Entrega:** Semantica de al-menos-una-vez, exactamente-una-vez
- **Enrutamiento:** Mensajeria directa, publicacion-suscripcion, difusion

#### Estado Compartido
- **Almacenes de Estado:** Repositorios de datos centralizados
- **Modelos de Consistencia:** Consistencia fuerte, eventual, debil
- **Patrones de Acceso:** Cargas pesadas de lectura, escritura, mixtas
- **Resolucion de Conflictos:** Ultimo-escritor-gana, estrategias de fusion

#### Arquitectura Dirigida por Eventos
- **Event Sourcing:** Registros de eventos inmutables, reconstruccion de estado
- **Tipos de Eventos:** Eventos de dominio, eventos de sistema, eventos de integracion
- **Procesamiento de Eventos:** Tiempo real, por lotes, procesamiento de flujos
- **Esquema de Eventos:** Formatos de eventos versionados, compatibilidad retroactiva

### 5. Barreras de Proteccion y Seguridad

#### Validacion de Entrada
- **Aplicacion de Esquemas:** Campos requeridos, verificacion de tipos, validacion de formato
- **Filtrado de Contenido:** Deteccion de contenido danino, eliminacion de PII
- **Limitacion de Tasa:** Regulacion de solicitudes, cuotas de recursos
- **Autenticacion:** Verificacion de identidad, verificaciones de autorizacion

#### Filtrado de Salida
- **Moderacion de Contenido:** Eliminacion de contenido danino, verificaciones de calidad
- **Validacion de Consistencia:** Verificaciones logicas, verificacion de restricciones
- **Formato:** Formatos de salida estandarizados, presentacion limpia
- **Registro de Auditoria:** Registros de decisiones, registros de cumplimiento

#### Humano en el Ciclo
- **Flujos de Aprobacion:** Puntos de control de decisiones criticas
- **Disparadores de Escalacion:** Umbrales de confianza, evaluacion de riesgos
- **Mecanismos de Anulacion:** Precedencia del juicio humano
- **Ciclos de Retroalimentacion:** Las correcciones humanas mejoran el comportamiento del sistema

### 6. Marcos de Evaluacion

#### Metricas de Completacion de Tareas
- **Tasa de Exito:** Porcentaje de tareas completadas exitosamente
- **Completacion Parcial:** Medicion de progreso para tareas complejas
- **Clasificacion de Tareas:** Criterios de exito por tipo de tarea
- **Analisis de Fallos:** Identificacion y categorizacion de causa raiz

#### Evaluacion de Calidad
- **Calidad de Salida:** Medidas de precision, relevancia, completitud
- **Consistencia:** Variabilidad de respuesta en entradas similares
- **Coherencia:** Flujo logico y consistencia interna
- **Satisfaccion del Usuario:** Puntuaciones de retroalimentacion, patrones de uso

#### Analisis de Costos
- **Uso de Tokens:** Consumo de tokens de entrada/salida por tarea
- **Costos de API:** Uso y cargos de servicios externos
- **Recursos de Computo:** Utilizacion de CPU, memoria, almacenamiento
- **Tiempo hasta el Valor:** Costo por completacion exitosa de tarea

#### Distribucion de Latencia
- **Tiempo de Respuesta:** Tiempo de completacion de tarea de extremo a extremo
- **Etapas de Procesamiento:** Identificacion de cuellos de botella por etapa
- **Tiempos de Cola:** Tiempos de espera en pipelines de procesamiento
- **Contencion de Recursos:** Impacto de operaciones concurrentes

### 7. Estrategias de Orquestacion

#### Orquestacion Centralizada
- **Motor de Flujo de Trabajo:** Coordinador central gestiona todos los agentes
- **Gestion de Estado:** Seguimiento centralizado del estado del flujo de trabajo
- **Logica de Decision:** Reglas complejas de enrutamiento y ramificacion
- **Monitoreo:** Visibilidad integral de todas las operaciones

#### Orquestacion Descentralizada
- **Peer-to-Peer:** Los agentes se coordinan directamente entre si
- **Descubrimiento de Servicios:** Registro y busqueda dinamica de agentes
- **Protocolos de Consenso:** Toma de decisiones distribuida
- **Tolerancia a Fallos:** Sin punto unico de fallo

#### Enfoques Hibridos
- **Limites de Dominio:** Centralizado dentro de dominios, federado entre ellos
- **Coordinacion Jerarquica:** Multiples niveles de orquestacion
- **Dependiente del Contexto:** Seleccion de estrategia basada en tipo de tarea
- **Balanceo de Carga:** Distribuir responsabilidad de coordinacion

### 8. Patrones de Memoria

#### Memoria a Corto Plazo
- **Ventanas de Contexto:** Memoria de trabajo para tareas actuales
- **Estado de Sesion:** Datos temporales para interacciones en curso
- **Gestion de Cache:** Estrategias de optimizacion de rendimiento
- **Presion de Memoria:** Manejo de restricciones de capacidad

#### Memoria a Largo Plazo
- **Almacenamiento Persistente:** Datos durables entre sesiones
- **Base de Conocimiento:** Conocimiento de dominio acumulado
- **Reproduccion de Experiencia:** Aprendizaje de interacciones pasadas
- **Consolidacion de Memoria:** Transferencia de corto a largo plazo

#### Memoria Compartida
- **Conocimiento Colaborativo:** Aprendizaje compartido entre agentes
- **Sincronizacion:** Estrategias de mantenimiento de consistencia
- **Control de Acceso:** Acceso a memoria basado en permisos
- **Particionamiento de Memoria:** Aislamiento entre grupos de agentes

### 9. Consideraciones de Escalabilidad

#### Escalado Horizontal
- **Replicacion de Agentes:** Multiples instancias del mismo tipo de agente
- **Distribucion de Carga:** Enrutamiento de solicitudes entre instancias de agentes
- **Agrupacion de Recursos:** Recursos de computo y almacenamiento compartidos
- **Distribucion Geografica:** Despliegues en multiples regiones

#### Escalado Vertical
- **Mejora de Capacidades:** Agentes individuales mas potentes
- **Expansion de Herramientas:** Acceso mas amplio a herramientas por agente
- **Expansion de Contexto:** Mayor capacidad de memoria de trabajo
- **Poder de Procesamiento:** Mayor rendimiento por agente

#### Optimizacion de Rendimiento
- **Estrategias de Cache:** Cache de respuestas, cache de resultados de herramientas
- **Procesamiento Paralelo:** Ejecucion concurrente de tareas
- **Optimizacion de Recursos:** Utilizacion eficiente de recursos
- **Eliminacion de Cuellos de Botella:** Ajuste sistematico del rendimiento

### 10. Manejo de Fallos

#### Mecanismos de Reintento
- **Retroceso Exponencial:** Retrasos crecientes entre reintentos
- **Jitter:** Variacion aleatoria de retraso para prevenir efecto manada
- **Intentos Maximos:** Comportamiento de reintento acotado
- **Condiciones de Reintento:** Clasificacion de fallos transitorios vs permanentes

#### Estrategias de Respaldo
- **Degradacion Elegante:** Funcionalidad reducida cuando los sistemas fallan
- **Enfoques Alternativos:** Metodos diferentes para los mismos objetivos
- **Respuestas Predeterminadas:** Comportamientos de respaldo seguros
- **Comunicacion con el Usuario:** Mensajes claros de fallo

#### Disyuntores
- **Deteccion de Fallos:** Monitoreo de tasas de fallo y tiempos de respuesta
- **Gestion de Estado:** Estados de circuito abierto, cerrado, semiabierto
- **Pruebas de Recuperacion:** Retorno gradual a la operacion normal
- **Prevencion de Fallos en Cascada:** Proteccion de sistemas ascendentes

## Directrices de Implementacion

### Proceso de Decision de Arquitectura
1. **Analisis de Requisitos:** Comprender objetivos del sistema, restricciones, escala
2. **Seleccion de Patron:** Elegir el patron de arquitectura apropiado
3. **Diseno de Agentes:** Definir roles, responsabilidades, interfaces
4. **Arquitectura de Herramientas:** Disenar esquemas de herramientas y manejo de errores
5. **Diseno de Comunicacion:** Seleccionar patrones de mensajes y protocolos
6. **Implementacion de Seguridad:** Construir barreras de proteccion y validacion
7. **Planificacion de Evaluacion:** Definir metricas de exito y monitoreo
8. **Estrategia de Despliegue:** Planificar escalado y manejo de fallos

### Aseguramiento de Calidad
- **Estrategia de Pruebas:** Enfoques de pruebas unitarias, de integracion y de sistema
- **Monitoreo:** Seguimiento en tiempo real de la salud y el rendimiento del sistema
- **Documentacion:** Documentacion de arquitectura y manuales operativos
- **Revision de Seguridad:** Modelado de amenazas y evaluaciones de seguridad

### Mejora Continua
- **Monitoreo de Rendimiento:** Analisis continuo del rendimiento del sistema
- **Retroalimentacion del Usuario:** Incorporacion de mejoras en la experiencia del usuario
- **Pruebas A/B:** Experimentos controlados para mejoras del sistema
- **Actualizaciones de Base de Conocimiento:** Aprendizaje y adaptacion continuos

Esta habilidad proporciona la base para disenar sistemas multiagente robustos y escalables que pueden manejar tareas complejas mientras mantienen la seguridad, confiabilidad y rendimiento a escala.
