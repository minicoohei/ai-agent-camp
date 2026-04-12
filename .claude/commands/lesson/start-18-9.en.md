---
description: "When the user says /start-18-9 — Module 18 Lesson 18-9: PM - System Architecture & API Design"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~30 min"
category: "lesson"
prerequisites: ["start-18-8", "output/pm/er-diagram.puml"]
level: "intermediate"
tags: ["pm", "architecture", "api", "network"]
---

# 🎓 Lesson 18-9: System Architecture & API Design

| Item | Details |
|------|------|
| Goal | Create TaskFlow system architecture diagrams, network diagrams (PlantUML), and API specifications (OpenAPI YAML) |
| Duration | ~30 min |
| Skills Used | diagram-generator skill |
| Prerequisites | Lesson 18-8 completed、output/pm/er-diagram.puml exists |
| Lesson Page | [Module 18](https://ai-agent.camp/en/course/module-18) |

---

## 📍 Step 1: System Architecture Diagram (PlantUML)

Represent the overall system architecture in a diagram. Visualize TaskFlow's components, layer structure, and dependencies.

```json
{
  "type": "AskQuestion",
  "id": "architecture_choice",
  "question": "Select the architecture for TaskFlow",
  "description": "Determine the overall system design pattern. Consider scale, complexity, and scalability.",
  "options": [
    {
      "label": "Monolith (Simple)",
      "value": "monolith_simple",
      "description": "Frontend, backend, DB are tightly coupled. For initial stage, emphasis on development speed"
    },
    {
      "label": "Monolith + External Services",
      "value": "monolith_external",
      "description": "Email sending, push notifications integrated with external SaaS. Improved scalability"
    },
    {
      "label": "Microservices",
      "value": "microservices",
      "description": "Services separated by function: auth, tasks, projects, notifications. High complexity, high scalability"
    },
    {
      "label": "Serverless",
      "value": "serverless",
      "description": "Utilizing AWS Lambda, Cloud Functions, etc. Low operational cost, maximum scalability"
    }
  ]
}
```

### System Architecture Diagram Elements

Draw the following components according to the selected architecture:

**Common Components:**
- **Frontend Layer**: React/Next.js, TypeScript, Tailwind CSS
- **API Gateway / Load Balancer**: Request routing, caching
- **Backend Layer**: Node.js/Express, RESTful API, business logic
- **Database Layer**: PostgreSQL (main DB), Redis (cache)
- **Authentication/Authorization**: JWT, OAuth2, session management

**Optional Components (by architecture):**
- Monolith + external: Email sending (SendGrid/AWS SES), push notifications (Firebase Cloud Messaging)
- Microservices: Auth Service, Task Service, Project Service, Notification Service, Message Queue (RabbitMQ/Kafka)
- Serverless: Lambda Functions, DynamoDB, S3, API Gateway (AWS)

**Output file**: `output/pm/system-architecture.puml`

```plaintext
PlantUML syntax example:
@startuml SystemArchitecture
!define AWSPUML https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/v18.0/dist
!include AWSPUML/ApplicationIntegration/APIGateway.puml
!include AWSPUML/ApplicationIntegration/SimpleQueueService.puml
!include AWSPUML/Compute/Lambda.puml
!include AWSPUML/Database/RDS.puml

rectangle "Client Layer" {
  component [Web UI\n(React/Next.js)] as WebUI
  component [Mobile App\n(React Native)] as MobileApp
}

rectangle "API Layer" {
  component [API Gateway] as Gateway
}

rectangle "Business Logic Layer" {
  component [Authentication Service] as Auth
  component [Task Service] as TaskSvc
  component [Project Service] as ProjectSvc
  component [Notification Service] as NotifSvc
}

rectangle "Data Layer" {
  component [PostgreSQL] as MainDB
  component [Redis Cache] as Cache
}

rectangle "External Integration" {
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

## 🚀 Step 2: Network Architecture Diagram（PlantUML）

Represent the production environment infrastructure configuration in a diagram. Include VPC, subnets, security groups, CDN, etc.

```json
{
  "type": "AskQuestion",
  "id": "deployment_env",
  "question": "Select the deployment environment",
  "description": "Select the cloud provider or on-premises for the production environment. Architecture differs for each environment.",
  "options": [
    {
      "label": "AWS",
      "value": "aws",
      "description": "EC2/ECS, RDS, S3, CloudFront, ALB, VPC, Route 53. Industry standard, rich services"
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
      "label": "On-premises",
      "value": "onpremise",
      "description": "Physical servers, own data center. High initial investment, full control"
    }
  ]
}
```

### Network Architecture Diagram Elements

Draw the following according to the selected environment:

**AWS Configuration:**
- **Internet Zone**: Route 53 (DNS), CloudFront (CDN)
- **VPC**: CIDR 10.0.0.0/16
  - Public Subnet (AZ-a): 10.0.1.0/24 → ALB, NAT Gateway
  - Private Subnet (AZ-a): 10.0.10.0/24 → ECS/EC2
  - Private Subnet (AZ-b): 10.0.11.0/24 → RDS（Multi-AZ）
- **Security Groups**: ALB-SG, App-SG, DB-SG
- **ELB**: Application Load Balancer（80, 443）
- **Compute**: ECS on EC2 / EC2 Auto Scaling Group
- **Storage**: RDS PostgreSQL (Multi-AZ), S3 (user files, logs)
- **Other**: CloudWatch, VPC Flow Logs, NAT Gateway

**GCP Configuration:**
- Cloud Load Balancing (external)
- VPC Network（default）
  - Public Subnetwork: Cloud NAT, Cloud Router
  - Private Subnetwork: GKE Cluster / Compute Engine
- Cloud SQL（PostgreSQL）
- Cloud Storage (user files)
- Cloud CDN

**Azure Configuration:**
- Azure Front Door（Global Load Balancer）
- Virtual Network
  - Subnet 1: Application Gateway, NAT Gateway
  - Subnet 2: Virtual Machines / AKS
- Azure SQL Database（PostgreSQL）
- Blob Storage
- Azure CDN

**Output file**: `output/pm/network-diagram.puml`

```plaintext
PlantUML syntax example (AWS):
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

## ⚠️ Step 3: API List and Specification (OpenAPI/Swagger YAML)

Define all RESTful API endpoints in detail. Describe request/response formats, parameters, authentication methods, status codes, and error handling.

```json
{
  "type": "AskQuestion",
  "id": "api_style",
  "question": "Select the API design style",
  "description": "There are different API design paradigms. Consider maintainability, client-side implementation difficulty, and scalability.",
  "options": [
    {
      "label": "RESTful",
      "value": "restful",
      "description": "Utilizes HTTP methods (GET/POST/PUT/DELETE). Clear design conventions, easy caching"
    },
    {
      "label": "GraphQL",
      "value": "graphql",
      "description": "Client specifies required data. Reduces over-fetching, handles complex response schemas"
    },
    {
      "label": "REST + GraphQL Hybrid",
      "value": "hybrid",
      "description": "REST-based with GraphQL `/graphql` endpoint for complex queries. Gradual migration possible"
    }
  ]
}
```

### API Specification Elements

**OpenAPI 3.0 YAML Format:**
- **Basic information**: title, version, description, servers, info.contact
- **Authentication**: securitySchemes (JWT Bearer Token, OAuth2)
- **Endpoint definitions**:
  - Path, HTTP method
  - Description, summary
  - Parameters (path, query, header, cookie)
  - Request body (request body schema)
  - Response (schema per status code)
  - Security requirements

### TaskFlow API Endpoint List

**Authentication**
1. `POST /auth/register` - User registration
2. `POST /auth/login` - Login (JWT issuance)
3. `POST /auth/refresh` - Token refresh
4. `POST /auth/logout` - Logout
5. `POST /auth/password-reset` - Password reset request

**Users**
6. `GET /users/me` - Get current user info
7. `PUT /users/me` - Update user info (profile)
8. `DELETE /users/me` - Delete account
9. `GET /users/{userId}` - Get user details
10. `GET /users` - Search user list (admin only)

**Projects**
11. `GET /projects` - Get project list (with filter and pagination)
12. `POST /projects` - Create project
13. `GET /projects/{projectId}` - Get project details
14. `PUT /projects/{projectId}` - Update project
15. `DELETE /projects/{projectId}` - Delete project
16. `GET /projects/{projectId}/members` - List project members
17. `POST /projects/{projectId}/members` - Invite member
18. `DELETE /projects/{projectId}/members/{userId}` - Remove member

**Tasks**
19. `GET /tasks` - Get task list (filter by project, status, assignee)
20. `POST /tasks` - Create task
21. `GET /tasks/{taskId}` - Get task details
22. `PUT /tasks/{taskId}` - Update task (status, deadline, description, etc.)
23. `DELETE /tasks/{taskId}` - Delete task
24. `POST /tasks/{taskId}/assign` - Assign task
25. `GET /tasks/{taskId}/comments` - List comments
26. `POST /tasks/{taskId}/comments` - Add comment
27. `POST /tasks/{taskId}/attachments` - Attach file

**Notifications**
28. `GET /notifications` - Get notification list
29. `POST /notifications/{notificationId}/read` - Mark notification as read
30. `DELETE /notifications/{notificationId}` - Delete notification
31. `PUT /notifications/settings` - Change notification settings (email, push, etc.)

**Output file**: `output/pm/api-spec.yaml`

```yaml
openapi: 3.0.3
info:
  title: TaskFlow API
  description: Task Management and Project Collaboration Platform API
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
      summary: User Registration
      description: Create a new user account
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
          description: User created successfully
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
          description: Request format error
        '409':
          description: User already exists

  /auth/login:
    post:
      summary: Login
      description: Login with email and password to obtain JWT token
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
          description: Login successful
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
          description: Authentication failed (invalid email or password)

  /users/me:
    get:
      summary: Get Current User Info
      tags:
        - Users
      responses:
        '200':
          description: User information
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Authentication failed

    put:
      summary: Update User Info
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
          description: Update successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          description: Request format error
        '401':
          description: Authentication failed

  /projects:
    get:
      summary: Get Project List
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
          description: Project list
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
      summary: Create Project
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
          description: Project created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '400':
          description: Request format error

  /tasks:
    get:
      summary: Get Task List
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
          description: Task list
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
      summary: Create Task
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
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '400':
          description: Request format error
```

---

## ✅ Step 4: Architecture Review

Review whether the created system architecture diagram, network architecture diagram, and API specification are appropriate for implementation needs from multiple perspectives.

```json
{
  "type": "AskQuestion",
  "id": "review_perspective",
  "question": "Select the review perspective",
  "description": "Evaluate the proposed architecture from the following perspectives. Multiple selections possible.",
  "options": [
    {
      "label": "Scalability",
      "value": "scalability",
      "description": "Can it handle increased users and data volume? Room for horizontal and vertical scaling"
    },
    {
      "label": "Security",
      "value": "security",
      "description": "Data encryption, authentication/authorization, network security. OWASP Top 10 compliance, privacy (GDPR, etc.)"
    },
    {
      "label": "Cost Optimization",
      "value": "cost_optimization",
      "description": "Infrastructure costs, operational costs, personnel costs. ROI, initial investment vs long-term operational costs"
    },
    {
      "label": "All",
      "value": "all",
      "description": "Comprehensive review from all perspectives: scalability, security, and cost optimization"
    }
  ]
}
```

### Review Items

**Scalability perspective:**
- [ ] Is load balancing via load balancer designed?
- [ ] Is database replication/sharding strategy specified?
- [ ] Can read performance be improved by utilizing cache layer (Redis, etc.)?
- [ ] Can delivery latency be reduced by CDN static asset delivery?
- [ ] Can traffic spikes be handled by API rate limiting and queuing mechanisms?
- [ ] Can the impact of long-running processes be mitigated by async processing (Job Queue, etc.)?

**Security perspective:**
- [ ] Is all communication encrypted with HTTPS/TLS 1.2 or higher?
- [ ] Is JWT/OAuth2 authentication/authorization implemented?
- [ ] Is password hashing (bcrypt, etc.) and salt generation implemented?
- [ ] Are SQL injection countermeasures (prepared statements) implemented?
- [ ] Is CORS configuration appropriate (Origin restrictions)?
- [ ] Is communication restricted by VPC and security groups?
- [ ] Is database encryption (at-rest) and backup strategy in place?
- [ ] Are log monitoring and alert mechanisms (CloudWatch, etc.) configured?
- [ ] Are rate limiting and DDoS protection (AWS Shield, etc.) enabled?

**Cost optimization perspective:**
- [ ] Is there no waste in the cloud provider's pay-per-use pricing?
- [ ] Is there potential to use reserved/spot instances?
- [ ] Are CDN and object storage costs estimated?
- [ ] Are database capacity and backup retention period optimal?
- [ ] Can costs be reduced by limiting monitoring/log retention periods?
- [ ] Can operational costs be reduced by using managed services (RDS, ElastiCache, etc.)?
- [ ] Is multi-region deployment needed, or is a single region sufficient?

---

## 📊 Checklist

Verify that the following deliverables have been generated:

```json
{
  "type": "Checkpoint",
  "items": [
    {
      "item": "System architecture diagram created",
      "file": "output/pm/system-architecture.puml",
      "validation": "PlantUML syntax is valid, component diagram depicts 5 or more major system components"
    },
    {
      "item": "Network configuration diagram created",
      "file": "output/pm/network-diagram.puml",
      "validation": "Region, subnet, and security group for the selected cloud environment (AWS/GCP/Azure) are specified"
    },
    {
      "item": "10 or more API endpoints defined",
      "file": "output/pm/api-spec.yaml",
      "validation": "10 or more path definitions including GET/POST/PUT/DELETE in OpenAPI 3.0 format, with requestBody and responses defined for each endpoint"
    },
    {
      "item": "OpenAPI YAML valid",
      "file": "output/pm/api-spec.yaml",
      "validation": "No YAML syntax errors. Can be validated with online validator (swagger.io)"
    },
    {
      "item": "All 3 files generated",
      "files": [
        "output/pm/system-architecture.puml",
        "output/pm/network-diagram.puml",
        "output/pm/api-spec.yaml"
      ],
      "validation": "All 3 files exist in the specified directory and are not empty"
    }
  ]
}
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|------|----------|
| PlantUML syntax error | Enclose correctly with `@startuml` and `@enduml`. Check component, rectangle, arrow syntax. Verify with online editor (plantuml.com) |
| OpenAPI YAML parse error | Unify indentation with 2 spaces. Check hierarchy of `components`, `schemas`, `paths`. Validate at https://www.swagger.io/tools/swagger-editor/ |
| Difficulty choosing architecture | Consider TaskFlow scale, schedule, team size. Monolith recommended for initial stage (development speed) → consider microservices as growth occurs |
| Insufficient AWS network knowledge | Review basic concepts of VPC CIDR (/16), Subnet CIDR (/24), Route Table, Network ACL, Security Group. AZ = Availability Zone (fault isolation) |
| Difficulty deciding REST vs GraphQL | REST: Simple queries, caching focus → RESTful recommended. Complex response structures, client diversity → GraphQL recommended |
| PlantUML file saving | Save .puml files in UTF-8 encoding. Use slash `/` as path separator |


---

## 📋 Deliverables Preview

### Expected Output
```text
📁 output/pm/
└── system-architecture.puml  (System Architecture Diagram)
```

### Verification Commands
```bash
# Check file existence and size
ls -lh output/pm/system-architecture.puml

# Check the beginning (first 30 lines)
head -30 output/pm/system-architecture.puml
```

> 💡 Full text: Run `cat output/pm/system-architecture.puml` to display the full text

---

## ➡️ Next: Lesson 18-10

In the next lesson, you will create a **WBS (Work Breakdown Structure)** and **Gantt chart** for the TaskFlow project. Based on the system architecture diagrams and API specifications, you will plan specific development tasks, resource allocation, and schedules.

- **WBS**: Decompose the project by feature and module
- **Gantt Chart**: Visualize start dates, end dates, dependencies, and resource allocation (PM, engineers, etc.) for each task
- **Milestones**: Important events such as alpha, beta, GA releases

→ [Lesson 18-10: WBS & Gantt Chart](./start-18-10.md)
