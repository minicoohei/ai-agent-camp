---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-8", "output/pm/er-diagram.puml"]
level: "intermediate"
tags: ["pm", "architecture", "api", "network"]
---

# 🎓 Lesson 18-9: Arquitectura del sistema y diseño de API

| Elemento | Detalles |
|------|------|
| Objetivo | Crear diagramas de arquitectura del sistema, diagramas de red (PlantUML) y especificaciones de API (OpenAPI YAML) de TaskFlow |
| Duración | ~30 min |
| Habilidades utilizadas | habilidad diagram-generator |
| Requisitos previos | Lesson 18-8 completada、output/pm/er-diagram.puml existe |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

---

## 📍 Paso 1: Diagrama de arquitectura del sistema (PlantUML)

Represente la arquitectura general del sistema en un diagrama. Visualice los componentes, la estructura de capas y las dependencias de TaskFlow.

```json
{
  "type": "AskQuestion",
  "id": "architecture_choice",
  "question": "Seleccione la arquitectura para TaskFlow",
  "description": "Determine el patron de diseno general del sistema. Considere la escala, complejidad y escalabilidad.",
  "options": [
    {
      "label": "Monolito (Simple)",
      "value": "monolith_simple",
      "description": "Frontend, backend, BD estan fuertemente acoplados. Para etapa inicial, enfasis en velocidad de desarrollo"
    },
    {
      "label": "Monolito + Servicios externos",
      "value": "monolith_external",
      "description": "Envio de correo, notificaciones push integradas con SaaS externo. Escalabilidad mejorada"
    },
    {
      "label": "Microservicios",
      "value": "microservices",
      "description": "Servicios separados por funcion: autenticacion, tareas, proyectos, notificaciones. Alta complejidad, alta escalabilidad"
    },
    {
      "label": "Sin servidor",
      "value": "serverless",
      "description": "Utilizando AWS Lambda, Cloud Functions, etc. Bajo costo operativo, maxima escalabilidad"
    }
  ]
}
```

### Elementos del diagrama de arquitectura del sistema

Dibuje los siguientes componentes según la arquitectura seleccionada:

**Componentes comunes:**
- **Capa frontend**: React/Next.js, TypeScript, Tailwind CSS
- **API Gateway / Balanceador de carga**: Enrutamiento de solicitudes, almacenamiento en cache
- **Capa backend**: Node.js/Express, RESTful API, lógica de negocio
- **Capa de base de datos**: PostgreSQL (BD principal), Redis (cache)
- **Autenticación/Autorización**: JWT, OAuth2, gestión de sesiones

**Componentes opcionales (por arquitectura):**
- Monolito + externo: Envio de correo electrónico (SendGrid/AWS SES), notificaciones push (Firebase Cloud Messaging)
- Microservicios: Auth Service, Task Service, Project Service, Notification Service, Message Queue (RabbitMQ/Kafka)
- Serverless: Lambda Functions, DynamoDB, S3, API Gateway (AWS)

**Archivo de salida**: `output/pm/system-architecture.puml`

```plaintext
Ejemplo de sintaxis PlantUML:
@startuml SystemArchitecture
!define AWSPUML https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist
!include AWSPUML/ApplicationIntegration/APIGateway.puml
!include AWSPUML/ApplicationIntegration/SimpleQueueService.puml
!include AWSPUML/Compute/Lambda.puml
!include AWSPUML/Database/RDS.puml

rectangle "Capa del cliente" {
  component [Web UI\n(React/Next.js)] as WebUI
  component [Mobile App\n(React Native)] as MobileApp
}

rectangle "Capa API" {
  component [API Gateway] as Gateway
}

rectangle "Capa de logica de negocio" {
  component [Authentication Service] as Auth
  component [Task Service] as TaskSvc
  component [Project Service] as ProjectSvc
  component [Notification Service] as NotifSvc
}

rectangle "Capa de datos" {
  component [PostgreSQL] as MainDB
  component [Redis Cache] as Cache
}

rectangle "Integracion externa" {
  component [SendGrid\n(Email)] as Email
  component [Firebase Cloud\nMessaging] as FCM
}

WebUI --> Gateway
MobileApp --> Gateway
Gateway --> Auth
Gateway --> TaskSvc
Gateway --> ProjectSvc
Auth --> MainDB
TaskSvc --> MainDB
TaskSvc --> Cache
ProjectSvc --> MainDB
NotifSvc --> Email
NotifSvc --> FCM

@enduml
```

---

## 🚀 Paso 2: Diagrama de arquitectura de red（PlantUML）

Represente la configuración de la infraestructura del entorno de producción en un diagrama. Incluya VPC, subredes, grupos de seguridad, CDN, etc.

```json
{
  "type": "AskQuestion",
  "id": "deployment_env",
  "question": "Seleccione el entorno de despliegue",
  "description": "Seleccione el proveedor de nube o las instalaciones locales para el entorno de produccion. La arquitectura difiere para cada entorno.",
  "options": [
    {
      "label": "AWS",
      "value": "aws",
      "description": "EC2/ECS, RDS, S3, CloudFront, ALB, VPC, Route 53. Estandar de la industria, servicios abundantes"
    },
    {
      "label": "GCP",
      "value": "gcp",
      "description": "Compute Engine, Cloud SQL, Cloud Storage, Cloud CDN, Load Balancer, VPC"
    },
    {
      "label": "Azure",
      "value": "azure",
      "description": "Virtual Machines, Azure SQL Database, Blob Storage, Azure CDN, Application Gateway"
    },
    {
      "label": "En las instalaciones",
      "value": "onpremise",
      "description": "Servidores fisicos, centro de datos propio. Alta inversion inicial, control total"
    }
  ]
}
```

### Elementos del diagrama de arquitectura de red

Dibuje lo siguiente según el entorno seleccionado:

**Configuración AWS:**
- **Zona de internet**: Route 53 (DNS), CloudFront (CDN)
- **VPC**: CIDR 10.0.0.0/16
  - Public Subnet (AZ-a): 10.0.1.0/24 → ALB, NAT Gateway
  - Private Subnet (AZ-a): 10.0.10.0/24 → ECS/EC2
  - Private Subnet (AZ-b): 10.0.11.0/24 → RDS（Multi-AZ）
- **Grupos de seguridad**: ALB-SG, App-SG, DB-SG
- **ELB**: Application Load Balancer（80, 443）
- **Computo**: ECS on EC2 / EC2 Auto Scaling Group
- **Almacenamiento**: RDS PostgreSQL (Multi-AZ), S3 (archivos de usuario, registros)
- **Otros**: CloudWatch, VPC Flow Logs, NAT Gateway

**Configuración GCP:**
- Cloud Load Balancing (externo)
- VPC Network（default）
  - Public Subnetwork: Cloud NAT, Cloud Router
  - Private Subnetwork: GKE Cluster / Compute Engine
- Cloud SQL（PostgreSQL）
- Cloud Storage (archivos de usuario)
- Cloud CDN

**Configuración Azure:**
- Azure Front Door（Global Load Balancer）
- Virtual Network
  - Subnet 1: Application Gateway, NAT Gateway
  - Subnet 2: Virtual Machines / AKS
- Azure SQL Database（PostgreSQL）
- Blob Storage
- Azure CDN

**Archivo de salida**: `output/pm/network-diagram.puml`

```plaintext
Ejemplo de sintaxis PlantUML (AWS):
@startuml NetworkArchitecture
rectangle "Internet" as Internet

rectangle "AWS Account" {
  rectangle "VPC: 10.0.0.0/16" {
    rectangle "Public Subnet (AZ-a): 10.0.1.0/24" {
      component [ALB (80, 443)] as ALB
      component [NAT Gateway] as NAT
    }

    rectangle "Private Subnet (AZ-a): 10.0.10.0/24" {
      component [ECS Cluster\n(App Servers)] as AppA
    }

    rectangle "Private Subnet (AZ-b): 10.0.11.0/24" {
      component [ECS Cluster\n(App Servers)] as AppB
    }

    rectangle "Private Subnet (AZ-a): 10.0.20.0/24" {
      component [RDS Primary\n(PostgreSQL)] as DBPrimary
    }

    rectangle "Private Subnet (AZ-b): 10.0.21.0/24" {
      component [RDS Standby\n(Multi-AZ)] as DBStandby
    }
  }

  rectangle "S3 & CloudFront" {
    component [S3 Bucket] as S3
    component [CloudFront CDN] as CF
  }

  rectangle "Monitoring" {
    component [CloudWatch] as CW
  }
}

rectangle "Route 53" as R53

Internet --> R53
R53 --> CF
CF --> S3
R53 --> ALB
ALB --> AppA
ALB --> AppB
AppA --> NAT
AppB --> NAT
NAT --> Internet
AppA --> DBPrimary
AppB --> DBPrimary
DBPrimary --> DBStandby
AppA --> CW
AppB --> CW

@enduml
```

---

## ⚠️ Paso 3: Lista de API y especificación (OpenAPI/Swagger YAML)

Defina todos los endpoints de la API RESTful en detalle. Describa los formatos de solicitud/respuesta, parámetros, métodos de autenticación, códigos de estado y manejo de errores.

```json
{
  "type": "AskQuestion",
  "id": "api_style",
  "question": "Seleccione el estilo de diseno de API",
  "description": "Existen diferentes paradigmas de diseno de API. Considere la mantenibilidad, la dificultad de implementacion del lado del cliente y la escalabilidad.",
  "options": [
    {
      "label": "RESTful",
      "value": "restful",
      "description": "Utiliza metodos HTTP (GET/POST/PUT/DELETE). Convenciones de diseno claras, cache facil"
    },
    {
      "label": "GraphQL",
      "value": "graphql",
      "description": "El cliente especifica los datos requeridos. Reduce la sobreobtencion, maneja esquemas de respuesta complejos"
    },
    {
      "label": "Hibrido REST + GraphQL",
      "value": "hybrid",
      "description": "Basado en REST con endpoint GraphQL `/graphql` para consultas complejas. Migracion gradual posible"
    }
  ]
}
```

### Elementos de la especificación de API

**Formato YAML OpenAPI 3.0:**
- **Información básica**: title, versión, description, servers, info.contact
- **Autenticación**: securitySchemes (JWT Bearer Token, OAuth2)
- **Definiciones de endpoints**:
  - Ruta (path), método HTTP
  - Descripción (description), resumen (summary)
  - Parámetros (path, query, header, cookie)
  - Cuerpo de solicitud (request body schema)
  - Respuesta (schema por código de estado)
  - Requisitos de seguridad

### Lista de endpoints de la API de TaskFlow

**Autenticación**
1. `POST /auth/register` - Registro de usuario
2. `POST /auth/login` - Inicio de sesión (emisión de JWT)
3. `POST /auth/refresh` - Actualización de token
4. `POST /auth/logout` - Cierre de sesión
5. `POST /auth/password-reset` - Solicitud de restablecimiento de contraseña

**Usuarios**
6. `GET /users/me` - Obtener información del usuario actual
7. `PUT /users/me` - Actualizar información de usuario (perfil)
8. `DELETE /users/me` - Eliminar cuenta
9. `GET /users/{userId}` - Obtener detalles del usuario
10. `GET /users` - Buscar lista de usuarios (solo administrador)

**Proyectos**
11. `GET /projects` - Obtener lista de proyectos (con filtro y paginación)
12. `POST /projects` - Crear proyecto
13. `GET /projects/{projectId}` - Obtener detalles del proyecto
14. `PUT /projects/{projectId}` - Actualizar proyecto
15. `DELETE /projects/{projectId}` - Eliminar proyecto
16. `GET /projects/{projectId}/members` - Listar miembros del proyecto
17. `POST /projects/{projectId}/members` - Invitar miembro
18. `DELETE /projects/{projectId}/members/{userId}` - Eliminar miembro

**Tareas**
19. `GET /tasks` - Obtener lista de tareas (filtrar por proyecto, estado, responsable)
20. `POST /tasks` - Crear tarea
21. `GET /tasks/{taskId}` - Obtener detalles de la tarea
22. `PUT /tasks/{taskId}` - Actualizar tarea (estado, fecha límite, descripción, etc.)
23. `DELETE /tasks/{taskId}` - Eliminar tarea
24. `POST /tasks/{taskId}/assign` - Asignar tarea
25. `GET /tasks/{taskId}/comments` - Listar comentarios
26. `POST /tasks/{taskId}/comments` - Agregar comentario
27. `POST /tasks/{taskId}/attachments` - Adjuntar archivo

**Notificaciones**
28. `GET /notifications` - Obtener lista de notificaciones
29. `POST /notifications/{notificationId}/read` - Marcar notificación como leida
30. `DELETE /notifications/{notificationId}` - Eliminar notificación
31. `PUT /notifications/settings` - Cambiar configuración de notificaciones (correo electrónico, push, etc.)

**Archivo de salida**: `output/pm/api-spec.yaml`

```yaml
openapi: 3.0.3
info:
  title: TaskFlow API
  description: API de plataforma de gestion de tareas y colaboracion de proyectos
  version: 1.0.0
  contact:
    name: TaskFlow Support
    email: support@taskflow.example.com

servers:
  - url: https://api.taskflow.example.com/v1
    description: Production
  - url: http://localhost:8000/v1
    description: Development

security:
  - bearerAuth: []

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        avatar_url:
          type: string
          format: uri
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Project:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        description:
          type: string
        owner_id:
          type: string
          format: uuid
        members_count:
          type: integer
        tasks_count:
          type: integer
        status:
          type: string
          enum: [active, archived]
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Task:
      type: object
      properties:
        id:
          type: string
          format: uuid
        project_id:
          type: string
          format: uuid
        title:
          type: string
        description:
          type: string
        status:
          type: string
          enum: [todo, in_progress, review, done]
        priority:
          type: string
          enum: [low, medium, high, critical]
        assigned_to:
          type: string
          format: uuid
        due_date:
          type: string
          format: date
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

paths:
  /auth/register:
    post:
      summary: Registro de usuario
      description: Crear una nueva cuenta de usuario
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                name:
                  type: string
              required:
                - email
                - password
                - name
      responses:
        '201':
          description: Usuario creado exitosamente
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
                    description: JWT access token
        '400':
          description: Error de formato de solicitud
        '409':
          description: El usuario ya existe

  /auth/login:
    post:
      summary: Inicio de sesion
      description: Iniciar sesion con correo electronico y contrasena para obtener el token JWT
      tags:
        - Authentication
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
              required:
                - email
                - password
      responses:
        '200':
          description: Inicio de sesion exitoso
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: '#/components/schemas/User'
                  token:
                    type: string
                  refresh_token:
                    type: string
        '401':
          description: Autenticacion fallida (correo o contrasena invalidos)

  /users/me:
    get:
      summary: Obtener informacion del usuario actual
      tags:
        - Users
      responses:
        '200':
          description: Informacion del usuario
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Autenticacion fallida

    put:
      summary: Actualizar informacion del usuario
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                avatar_url:
                  type: string
                  format: uri
      responses:
        '200':
          description: Actualizacion exitosa
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Error de formato de solicitud
        '401':
          description: Autenticacion fallida

  /projects:
    get:
      summary: Obtener lista de proyectos
      tags:
        - Projects
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, archived]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Lista de proyectos
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Project'
                  pagination:
                    type: object
                    properties:
                      total:
                        type: integer
                      page:
                        type: integer
                      limit:
                        type: integer

    post:
      summary: Crear proyecto
      tags:
        - Projects
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
              required:
                - name
      responses:
        '201':
          description: Proyecto creado exitosamente
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '400':
          description: Error de formato de solicitud

  /tasks:
    get:
      summary: Obtener lista de tareas
      tags:
        - Tasks
      parameters:
        - name: project_id
          in: query
          schema:
            type: string
            format: uuid
        - name: status
          in: query
          schema:
            type: string
            enum: [todo, in_progress, review, done]
        - name: assigned_to
          in: query
          schema:
            type: string
            format: uuid
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
      responses:
        '200':
          description: Lista de tareas
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Task'
                  pagination:
                    type: object

    post:
      summary: Crear tarea
      tags:
        - Tasks
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                project_id:
                  type: string
                  format: uuid
                title:
                  type: string
                description:
                  type: string
                priority:
                  type: string
                  enum: [low, medium, high, critical]
                due_date:
                  type: string
                  format: date
              required:
                - project_id
                - title
      responses:
        '201':
          description: Tarea creada exitosamente
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Error de formato de solicitud
```

---

## ✅ Paso 4: Revisión de arquitectura

Revise si el diagrama de arquitectura del sistema, el diagrama de arquitectura de red y la especificación de API creados son apropiados para las necesidades de implementación desde multiples perspectivas.

```json
{
  "type": "AskQuestion",
  "id": "review_perspective",
  "question": "Seleccione la perspectiva de revision",
  "description": "Evalue la arquitectura propuesta desde las siguientes perspectivas. Es posible seleccionar multiples opciones.",
  "options": [
    {
      "label": "Escalabilidad",
      "value": "scalability",
      "description": "Puede manejar el aumento de usuarios y volumen de datos? Margen para escalado horizontal y vertical"
    },
    {
      "label": "Seguridad",
      "value": "security",
      "description": "Cifrado de datos, autenticacion/autorizacion, seguridad de red. Cumplimiento OWASP Top 10, privacidad (GDPR, etc.)"
    },
    {
      "label": "Optimizacion de costos",
      "value": "cost_optimization",
      "description": "Costos de infraestructura, costos operativos, costos de personal. ROI, inversion inicial vs costos operativos a largo plazo"
    },
    {
      "label": "Todos",
      "value": "all",
      "description": "Revision integral desde todas las perspectivas: escalabilidad, seguridad y optimizacion de costos"
    }
  ]
}
```

### Elementos de revisión

**Perspectiva de escalabilidad:**
- [ ] Esta disenado el balanceo de carga mediante balanceador de carga?
- [ ] Esta especificada la estrategia de replicación/fragmentación de la base de datos?
- [ ] Se puede mejorar el rendimiento de lectura utilizando la capa de cache (Redis, etc.)?
- [ ] Se puede reducir la latencia de entrega mediante la entrega de activos estaticos por CDN?
- [ ] Se pueden manejar los picos de trafico mediante la limitación de velocidad de API y mecanismos de cola?
- [ ] Se puede mitigar el impacto de los procesos de larga duración mediante procesamiento asíncrono (Job Queue, etc.)?

**Perspectiva de seguridad:**
- [ ] Toda la comunicación esta cifrada con HTTPS/TLS 1.2 o superior?
- [ ] Esta implementada la autenticación/autorización JWT/OAuth2?
- [ ] Esta implementado el hash de contraseñas (bcrypt, etc.) y la generación de salt?
- [ ] Estan implementadas las contramedidas contra inyección SQL (sentencias preparadas)?
- [ ] Es apropiada la configuración CORS (restricciones de origen)?
- [ ] Esta restringida la comunicación por VPC y grupos de seguridad?
- [ ] Estan implementadas la cifrado de base de datos (en reposo) y la estrategia de respaldo?
- [ ] Estan configurados los mecanismos de monitoreo de registros y alertas (CloudWatch, etc.)?
- [ ] Estan habilitadas la limitación de velocidad y la protección DDoS (AWS Shield, etc.)?

**Perspectiva de optimización de costos:**
- [ ] No hay desperdicio en el modelo de pago por uso del proveedor de nube?
- [ ] Hay potencial para usar instancias reservadas/spot?
- [ ] Estan estimados los costos de CDN y almacenamiento de objetos?
- [ ] Son optimos la capacidad de la base de datos y el período de retención de respaldos?
- [ ] Se pueden reducir costos limitando los períodos de retención de monitoreo/registros?
- [ ] Se pueden reducir los costos operativos utilizando servicios administrados (RDS, ElastiCache, etc.)?
- [ ] Es necesario el despliegue en multiples regiones, o es suficiente una sola region?

---

## 📊 Lista de verificación

Verifique que se hayan generado los siguientes entregables:

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "item": "Diagrama de arquitectura del sistema creado",
      "file": "output/pm/system-architecture.puml",
      "validation": "La sintaxis PlantUML es valida, el diagrama de componentes muestra 5 o mas componentes principales del sistema"
    },
    {
      "item": "Diagrama de configuracion de red creado",
      "file": "output/pm/network-diagram.puml",
      "validation": "La region, subred y grupo de seguridad del entorno de nube seleccionado (AWS/GCP/Azure) estan especificados"
    },
    {
      "item": "10 o mas endpoints de API definidos",
      "file": "output/pm/api-spec.yaml",
      "validation": "10 o mas definiciones de path incluyendo GET/POST/PUT/DELETE en formato OpenAPI 3.0, con requestBody y responses definidos para cada endpoint"
    },
    {
      "item": "OpenAPI YAML valid",
      "file": "output/pm/api-spec.yaml",
      "validation": "Sin errores de sintaxis YAML. Se puede validar con el validador en linea (swagger.io)"
    },
    {
      "item": "Los 3 archivos generados",
      "files": [
        "output/pm/system-architecture.puml",
        "output/pm/network-diagram.puml",
        "output/pm/api-spec.yaml"
      ],
      "validation": "Los 3 archivos existen en el directorio especificado y no estan vacios"
    }
  ]
}
```

---

## 🔧 Solución de problemas

| Problema | Solución |
|------|----------|
| Error de sintaxis PlantUML | Encerrar correctamente con `@startuml` y `@enduml`. Verificar sintaxis de component, rectangle, arrow. Verificar con editor en línea (plantuml.com) |
| Error de análisis YAML OpenAPI | Unificar indentación con 2 espacios. Verificar jerarquía de `components`, `schemas`, `paths`. Validar en https://www.swagger.io/tools/swagger-editor/ |
| Dificultad para elegir arquitectura | Considerar escala de TaskFlow, cronograma, tamaño del equipo. Monolito recomendado para etapa inicial (velocidad de desarrollo) → considerar microservicios a medida que ocurra crecimiento |
| Conocimiento insuficiente de red AWS | Revisar conceptos basicos de VPC CIDR (/16), Subnet CIDR (/24), Route Table, Network ACL, Security Group. AZ = Availability Zone (aislamiento de fallas) |
| Dificultad para decidir REST vs GraphQL | REST: Consultas simples, enfoque en cache → RESTful recomendado. Estructuras de respuesta complejas, diversidad de clientes → GraphQL recomendado |
| Guardado de archivos PlantUML | Guardar archivos .puml en codificación UTF-8. Usar barra `/` como separador de ruta |


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── system-architecture.puml  (Diagrama de arquitectura del sistema)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/system-architecture.puml

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/system-architecture.puml
```

> 💡 Texto completo: Ejecute `cat output/pm/system-architecture.puml` para mostrar el texto completo

---

## ➡️ Next: Lesson 18-10

En la siguiente lección, creará un **WBS (Work Breakdown Structure)** y un **diagrama de Gantt** para el proyecto TaskFlow. Basandose en los diagramas de arquitectura del sistema y las especificaciones de API, planificara tareas de desarrollo específicas, asignación de recursos y cronogramas.

- **WBS**: Descomponer el proyecto por funcionalidad y módulo
- **Diagrama de Gantt**: Visualizar fechas de inicio, fechas de fin, dependencias y asignación de recursos (PM, ingenieros, etc.) para cada tarea
- **Hitos**: Eventos importantes como versiones alfa, beta, GA

→ [Lesson 18-10: WBS y diagrama de Gantt](./start-18-10.md)
