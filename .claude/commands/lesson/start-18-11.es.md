---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module18-pm-sysdef/chapter.yaml"
duration: "~25 min"
category: "lesson"
prerequisites: ["start-18-10", "output/pm/wbs.md", "output/pm/requirements-spec.md"]
level: "intermediate"
tags: ["pm", "notion", "tracker", "collaboration"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 18-11: Integración con Notion

| Elemento | Detalles |
|------|------|
| Objetivo | Crear una base de datos de seguimiento de requisitos en Notion y gestionar los requisitos de TaskFlow |
| Duración | ~25 min |
| Habilidades utilizadas | habilidad notion-db |
| Requisitos previos | Lesson 18-10 completada, output/pm/requirements-spec.md existe. Clave API de Notion configurada |
| Página del material | [Module 18](https://ai-agent.camp/es/course/module-18) |

---

## 📍 Paso 1: Verificación de la conexión API de Notion

### 🚀 Contenido

Verifique el estado de conexión de la API de Notion y configure la clave API según sea necesario.

```json
{
  "type": "AskQuestion",
  "question": "Cual es el estado de la configuracion de su API de Notion?",
  "options": [
    {
      "label": "Ya configurado",
      "value": "ready",
      "description": "La clave de API de Notion esta configurada en las variables de entorno"
    },
    {
      "label": "Configurar ahora",
      "value": "setup_now",
      "description": "Obteniendo y configurando la clave de API ahora"
    },
    {
      "label": "Deseo omitir la integracion con Notion",
      "value": "skip",
      "description": "Usar un rastreador basado en markdown como alternativa"
    },
    {
      "label": "Tengo problemas",
      "value": "troubleshoot",
      "description": "Hay problemas con la configuracion de conexion"
    }
  ],
  "conditional": {
    "setup_now": "🔧 Como obtener la clave de API de Notion\n\n1. Inicie sesion en el sitio web de Notion (https://www.notion.so)\n2. Settings → Developer → My integrations → New integration\n3. Name: Ingrese 'TaskFlow PM Tracker'\n4. Capabilities: Seleccione Read content, Update content, Insert content\n5. Associated workspace: Seleccione el espacio de trabajo objetivo\n6. Haga clic en Show API key\n7. Configure las siguientes variables de entorno:\n   - NOTION_API_KEY=YOUR_NOTION_SECRET_HERE\n   - NOTION_DATABASE_ID=xxxxxxxx... (configurar despues de crear la BD)",
    "skip": "✅ Si omite Notion\n\nUse la siguiente alternativa:\n- Rastreador de requisitos en formato Markdown\n- Tipo: output/pm/requirement-tracker.md\n- Se requieren actualizaciones manuales\n\nSin embargo, los puntos de verificacion de esta leccion no se implementaran.",
    "troubleshoot": "⚠️ Resolucion de problemas\n\n[Error] \"NOTION_API_KEY not found\"\n→ La variable de entorno no esta configurada. Consulte el metodo de configuracion de la clave de API anterior.\n\n[Error] \"Unauthorized\"\n→ Verifique si la clave de API es correcta. Obtengala nuevamente desde show API key.\n\n[Error] \"Rate limit exceeded\"\n→ Espere 15 segundos e intente de nuevo.\n\nConsulte docs/setup-guides/ para mas detalles"
  }
}
```

### ⚠️ Elementos de verificación

- [ ] La clave API de Notion esta configurada en variables de entorno
- [ ] Se ha verificado que la clave API de Notion es válida
- [ ] Existen permisos para el espacio de trabajo objetivo
- [ ] La biblioteca API se puede instalar en el entorno Node.js

---

## 📍 Paso 2: Creación de base de datos de seguimiento de requisitos

### 🚀 Contenido

Cree una base de datos de gestión de requisitos en Notion. Seleccione la configuración de columnas.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione la configuracion de columnas del rastreador",
  "options": [
    {
      "label": "Simple (5 columnas)",
      "value": "simple",
      "description": "Solo informacion basica: ID / Nombre / Categoria / Estado / Prioridad"
    },
    {
      "label": "Estandar (8 columnas)",
      "value": "standard",
      "description": "Simple + Responsable / Casos de uso relacionados / Notas"
    },
    {
      "label": "Detallado (12 columnas)",
      "value": "detailed",
      "description": "Estandar + ID de caso de prueba / Fecha de finalizacion prevista / Documentos relacionados / Stack tecnologico"
    },
    {
      "label": "Personalizado",
      "value": "custom",
      "description": "Combinar columnas libremente"
    }
  ]
}
```

### 📋 Esquema de base de datos

#### Configuración simple (5 columnas)

| Columna | Tipo | Descripción | Obligatorio |
|---------|----|----|------|
| ID de requisito | Text | REQ-001, REQ-002, etc. | Yes |
| Nombre del requisito | Title | Nombre del requisito | Yes |
| Categoría | Select | Funcional / No funcional / Otro | Yes |
| Estado | Select | No iniciado / En diseño / En implementación / En pruebas / Completado | Yes |
| Prioridad | Select | Must / Should / Could / Won't | Yes |

#### Configuración estándar (8 columnas)

Además de la configuración simple:

| Columna | Tipo | Descripción | Obligatorio |
|---------|----|----|------|
| Responsable | People | Persona responsable de esta tarea | No |
| Casos de uso relacionados | Relation | Enlace a UC-XXX | No |
| Notas | Text | Información adicional y memorandos | No |

#### Configuración detallada (12 columnas)

Además de la configuración estándar:

| Columna | Tipo | Descripción | Obligatorio |
|---------|----|----|------|
| ID de caso de prueba | Text | TC-001, etc. | No |
| Fecha objetivo de finalización | Date | Fecha objetivo de finalización | No |
| Documentos relacionados | URL | Especificaciones y enlaces | No |
| Stack tecnologico | Multi-select | React / Node.js, etc. | No |

### 🚀 Pasos de ejecución

```bash
# 1. Crear BD con la habilidad notion-db
/notion-db create \
  --db-name "TaskFlow Requirements Tracker" \
  --workspace-name "TaskFlow PM" \
  --icon "📋" \
  --columns-template "standard"

# Ejemplo de salida:
# ✓ Database created
# Database ID: abc123def456...
# URL: https://notion.so/abc123def456...
# Configure la variable de entorno NOTION_DATABASE_ID
```

### ✅ Verificación de éxito

- [ ] La base de datos se ha creado en Notion
- [ ] URL: `https://notion.so/{DATABASE_ID}` es accesible
- [ ] Todas las columnas se han creado correctamente
- [ ] La variable de entorno `NOTION_DATABASE_ID` esta configurada

---

## 📍 Paso 3: Importación de datos de requisitos

### 🚀 Contenido

Extraiga los requisitos de requirements-spec.md e importelos a la BD de Notion.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el metodo de importacion de datos",
  "options": [
    {
      "label": "Extraer automaticamente de requirements-spec.md",
      "value": "auto_extract",
      "description": "Analizar e importar automaticamente los requisitos de la especificacion existente (recomendado)"
    },
    {
      "label": "Manualmente uno por uno",
      "value": "manual",
      "description": "Agregar uno a la vez mediante entrada de formulario"
    },
    {
      "label": "Importacion masiva con datos de muestra",
      "value": "sample",
      "description": "Importar masivamente 15 requisitos de muestra para pruebas"
    }
  ]
}
```

### 📋 Procedimiento de extracción automática

```bash
# 1. Cargar requirements-spec.md
/notion-db import \
  --source-file "output/pm/requirements-spec.md" \
  --database-id "${NOTION_DATABASE_ID}" \
  --parse-mode "markdown" \
  --map-config '{
    "title": "requirement_name",
    "id": "requirement_id",
    "category": "category_field",
    "priority": "priority_field",
    "status": "initial_status:Sin iniciar"
  }'

# 2. Verificar resultados de importacion
# Cantidad importada: 10-15 elementos
# Cantidad exitosa: XX elementos
# Cantidad de errores: 0 elementos
```

### 📋 Ejemplo de datos de muestra

```markdown
| ID Req | Nombre del requisito | Categoria | Estado | Prioridad | Casos de uso relacionados | Notas |
|--------|--------|---------|----------|--------|---------------|------|
| REQ-001 | Registro de usuario | Funcional | Sin iniciar | Must | UC-01 | Incluye verificacion de correo |
| REQ-002 | Inicio de sesion | Funcional | Sin iniciar | Must | UC-02 | Funcion de restablecimiento de contrasena |
| REQ-003 | Visualizacion del panel | Funcional | Sin iniciar | Must | UC-05 | No se requieren actualizaciones en tiempo real |
| REQ-004 | Visualizacion lista de tareas | Funcional | Sin iniciar | Must | UC-06 | Incluye filtrado |
| REQ-005 | Crear/editar tareas | Funcional | Sin iniciar | Must | UC-07 | Multiples niveles de prioridad |
| REQ-006 | Eliminar tarea | Funcional | Sin iniciar | Should | UC-08 | Eliminacion logica |
| REQ-007 | Notificaciones | Funcional | Sin iniciar | Should | UC-09 | Soporte correo/push |
| REQ-008 | Alerta de vencimiento | Funcional | Sin iniciar | Should | UC-10 | Notificar 24 horas antes |
| REQ-009 | Diseno responsivo | No funcional | Sin iniciar | Must | UC-11 | Movil/Tableta/Escritorio |
| REQ-010 | Tiempo de carga de pagina | No funcional | Sin iniciar | Should | N/A | Menos de 3 segundos |
| REQ-011 | Seguridad (Cifrado) | No funcional | Sin iniciar | Must | N/A | SSL/TLS requerido |
| REQ-012 | Optimizacion de base de datos | No funcional | Sin iniciar | Could | N/A | Configuracion de indices |
```

### ✅ Verificación de importación

- [ ] Se han importado 10 o más requisitos a la BD de Notion
- [ ] Todos los campos obligatorios (ID/Nombre/Categoría/Estado) se han completado
- [ ] La prioridad esta configurada adecuadamente (Must: 40-50%, Should: 30-40%, Could: 10-20%)
- [ ] Es posible visualizar, buscar y filtrar en Notion

---

## 📍 Paso 4: Exportación a Markdown

### 🚀 Contenido

Exporte el contenido de la BD de Notion en formato markdown y cree documentación.

```json
{
  "type": "AskQuestion",
  "question": "Seleccione el formato de exportacion",
  "options": [
    {
      "label": "Formato de tabla Markdown",
      "value": "markdown_table",
      "description": "Exportar en formato de tabla Markdown (recomendado)"
    },
    {
      "label": "CSV",
      "value": "csv",
      "description": "Exportar como archivo CSV"
    },
    {
      "label": "JSON",
      "value": "json",
      "description": "Exportar como JSON estructurado"
    },
    {
      "label": "Todos",
      "value": "all",
      "description": "Generar en los 3 formatos: Markdown + CSV + JSON"
    }
  ]
}
```

### 🚀 Ejecutar exportación

```bash
# 1. Exportar BD de Notion
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "markdown" \
  --output-file "output/pm/notion-export.md" \
  --include-metadata true \
  --include-stats true

# 2. Tambien exportar en formato CSV (recomendado)
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "csv" \
  --output-file "output/pm/notion-export.csv"

# 3. Exportar en formato JSON
/notion-db export \
  --database-id "${NOTION_DATABASE_ID}" \
  --output-format "json" \
  --output-file "output/pm/notion-export.json"
```

### 📋 Ejemplo de formato de exportación

```markdown
# TaskFlow Requirements Tracker - Export

**Fecha/hora de exportacion**: 2024-01-15 14:30:00 JST
**ID de base de datos**: abc123def456...
**URL**: https://notion.so/abc123def456...

## 📊 Estadisticas

| Elemento | Cantidad |
|------|------|
| Requisitos totales | 15 |
| Sin iniciar | 15 |
| En diseno | 0 |
| En desarrollo | 0 |
| En pruebas | 0 |
| Completado | 0 |

### Por prioridad

| Prioridad | Cantidad | Porcentaje |
|--------|------|------|
| Must | 7 | 46.7% |
| Should | 6 | 40.0% |
| Could | 2 | 13.3% |
| Won't | 0 | 0.0% |

### Por categoria

| Categoria | Cantidad | Porcentaje |
|---------|------|------|
| Funcional | 12 | 80% |
| No funcional | 3 | 20% |

## 📋 Lista de requisitos

| ID Req | Nombre del requisito | Categoria | Estado | Prioridad | UC relacionado | Notas |
|--------|--------|---------|----------|--------|--------|------|
| REQ-001 | Registro de usuario | Funcional | Sin iniciar | Must | UC-01 | Incluye verificacion de correo |
| REQ-002 | Inicio de sesion | Funcional | Sin iniciar | Must | UC-02 | Funcion de restablecimiento de contrasena |
| ... | ... | ... | ... | ... | ... | ... |

---

**Generated by TaskFlow PM Training Platform**
```

### ✅ Verificación de exportación

- [ ] Se ha generado el archivo output/pm/notion-export.md
- [ ] Se incluyen estadísticas (cantidad de requisitos, distribución de estados, distribución de prioridades)
- [ ] Todos los requisitos se muestran en formato de tabla
- [ ] El formato de tabla es correcto (legible por analizadores Markdown)
- [ ] También se ha exportado CSV si es necesario

---

## 🎯 EntregablesLista de verificación

### Archivos y datos obligatorios

```json
{
  "type": "AskQuestion",
  "question": "Estan completos los siguientes entregables? Marque todos los que correspondan",
  "options": [
    {
      "label": "✓ Configuracion de Notion (conexion API verificada)",
      "value": "step1_done"
    },
    {
      "label": "✓ BD del rastreador de requisitos creada",
      "value": "step2_done"
    },
    {
      "label": "✓ Datos de requisitos importados (10+ elementos)",
      "value": "step3_done"
    },
    {
      "label": "✓ Exportacion Markdown completada",
      "value": "step4_done"
    },
    {
      "label": "✓ Archivo output/pm/notion-export.md generado",
      "value": "export_done"
    }
  ]
}
```

### ✅ Criterios de éxito

- **Conexión API de Notion**: Las variables de entorno `NOTION_API_KEY` y `NOTION_DATABASE_ID` estan configuradas correctamente
- **Creación de BD**: La BD de seguimiento de requisitos es visible y accesible en el panel de Notion
- **Importación de datos**: Al menos 10, idealmente 15 requisitos existen en la BD
- **Distribución de estados**: Todos configurados como "No iniciado" en el estado inicial
- **Distribución de prioridades**: Must 40-50%, Should 30-40%, Could 10-20% aproximadamente
- **Exportación completada**: Se ha generado output/pm/notion-export.md, con estadísticas y una lista completa de requisitos

---

## ⚠️ Solución de problemas

### Error: "NOTION_API_KEY not found"

```text
Causa: La variable de entorno no esta configurada
Solucion:
1. Obtener clave de API de Notion (https://www.notion.so/settings/integrations)
2. Ejecute lo siguiente:
   export NOTION_API_KEY="YOUR_NOTION_SECRET_HERE"          # Mac/Linux/WSL
3. Ejecutar nuevamente
```

### Error: "Unauthorized - Invalid API key"

```text
Causa: La clave de API es invalida o ha expirado
Solucion:
1. Generar una nueva clave de API desde la configuracion de Notion
2. Actualizar variable de entorno
3. Ejecutar nuevamente
```

### Error: "Database not found"

```text
Causa: NOTION_DATABASE_ID es incorrecto, o falta permiso de acceso a la BD
Solucion:
1. Verifique el ID correcto desde la URL de la BD de Notion
   Extraer ID de https://notion.so/[ID de 32 caracteres]
2. Corregir variable de entorno
3. Verificar que la integracion tiene acceso a la BD
```

### Error: "Rate limit exceeded"

```text
Causa: La frecuencia de solicitudes de API es demasiado alta
Solucion:
1. Esperar 15 segundos
2. Ejecutar nuevamente
3. Usar la bandera --delay al importar grandes datos
```

### Error: "Fallo en el análisis de Markdown"

```text
Causa: El formato de requirements-spec.md es incorrecto
Solucion:
1. Verificar el formato de requirements-spec.md
2. Importar manualmente uno a la vez (modo manual)
3. O intentar con datos de muestra
```

### No se generan los archivos

```text
Causa: El directorio output/pm/ no existe, o permisos insuficientes
Solucion:
1. Crear directorio: mkdir -p output/pm
2. Verificar permisos: ls -la output/
3. Ejecutar nuevamente
```


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/pm/
└── test-cases.md  (Lista de casos de prueba)
```

### Comandos de verificación
```bash
# Verificar existencia y tamano del archivo
ls -lh output/pm/test-cases.md

# Verificar el inicio (primeras 30 lineas)
head -30 output/pm/test-cases.md
```

> 💡 Texto completo: Ejecute `cat output/pm/test-cases.md` para mostrar el texto completo

---

## ➡️ Siguientes pasos

### 🎓 Lesson 18-12: Diseño de UI

**Progreso de fase**: Fase B (Definición de requisitos y diseño) completada!

La siguiente lección avanza a la Fase C (Diseño e implementación).

- Crear prototipos de UI de TaskFlow
- Diseño de wireframes
- Definición del sistema de diseño
- Preparación para la implementación del frontend

**Duración**: ~30 min
**Habilidades utilizadas**: habilidad figma-design / wireframe

---

## 📚 Recursos de referencia

### Documentación de API de Notion
- [Notion API Documentation](https://developers.notion.com/)
- [Database API Reference](https://developers.notion.com/reference/database)
- [Query Database](https://developers.notion.com/reference/post-database-query)

### Módulo PM de TaskFlow
- Module 18: Definición de requisitos del sistema (Planificación → Requisitos → Diseño → Implementación → Pruebas → Resumen)

### Lecciones relacionadas
- Lesson 18-10: Creación de especificación de requisitos (Análisis de requisitos)
- Lesson 18-12: Diseño de UI (Fase de diseño e implementación)
- Lesson 18-13: Creación de plan de implementación (Fase de implementación)

---

**Created**: 2024-01-15
**Last Updated**: 2024-01-15
**Module**: 14-PM-System Definition
**Level**: Intermediate
