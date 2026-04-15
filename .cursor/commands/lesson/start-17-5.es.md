---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module17-marketing"
duration: "Aprox. 30 min"
prerequisites: ["start-17-4"]
level: "intermediate"
tags: ["marketing", "typefully", "x", "threads", "sns", "api"]
---

# 🎓 Lesson 17-5: Automatizar publicaciones en X/Threads con Typefully

## 📍 Qué harás en esta sesión

¡Bienvenido a **Lesson 17-5: Automatizar publicaciones en X/Threads con Typefully**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Automatizar publicaciones en X (Twitter) y Threads usando la API de Typefully |
| Duración | Aprox. 30 min |
| Habilidades | API de Typefully (creación de borradores, programación, hilos) |
| Requisitos previos | Cuenta de Typefully creada, clave API obtenida |
| Página del curso | Consulta [Módulo 17: Marketing](https://ai-agent.camp/es/course/module-17) en paralelo |

> **💡 Info de herramientas**: Esta lección usa la API de Typefully. Funciona con Cursor IDE y Claude Code (CLI/Escritorio). En algunos entornos como Codex CLI, puede aparecer el error `request_user_input is not supported`. En ese caso, consulta la sección "Flujo de trabajo alternativo".

**Flujo de la sesión:**
1. Comprender la descripción general de la API de Typefully y configurar cuenta/clave API
2. Crear borradores y configurar publicaciones programadas
3. Probar la publicación simultánea en X (Twitter) y Threads
4. Automatizar publicaciones secuenciales en formato hilo
5. Verificar resultados y guardar registros en output/typefully/

Al final de esta sesión, podrás crear borradores, programar publicaciones y automatizar hilos a través de la API de Typefully.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad, escribe "continúa" o "sigue" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificación de preparación

Primero confirmemos que todo está configurado.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Estás listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Empecemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la página del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar requisitos previos)
(view_html → Mostrar ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Step 1: Descripción general de la API de Typefully y configuración de cuenta

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Descripción general de la API y configuración de cuenta",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Por favor, explica la descripción general de la API de Typefully. Cubre lo siguiente:

1. Qué es Typefully — herramienta de gestión y programación de publicaciones para X (Twitter) / Threads
2. Qué puede hacer la API — creación de borradores, programación, publicación en hilos
3. Pasos de configuración de cuenta:
   a. Crear una cuenta en https://typefully.com
   b. Conectar tu cuenta de X (Twitter)
   c. Conectar tu cuenta de Threads (si es compatible)
4. Obtener la clave API:
   a. Ir a Typefully Settings → Integrations → API & Integrations
   b. Generar y copiar la clave API
5. Configurar la clave API como variable de entorno:
   export TYPEFULLY_API_KEY="your-api-key-here"
```

**Resultado esperado**: Comprendes la descripción general de Typefully y has completado la configuración de la clave API.

---

## 🚀 Step 2: Creación de borradores y programación

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Creación de borradores y programación",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Usa la API de Typefully para crear un borrador y configurar una publicación programada.

Pasos:
1. mkdir -p output/typefully
2. Crear un borrador con el siguiente comando curl:

curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "¡Los agentes de IA están cambiando drásticamente la eficiencia del trabajo!\n\nTécnicas prácticas que cualquiera puede usar, sin necesidad de ser ingeniero.\n\n#AIAgent #Productividad",
    "schedule-date": "next-free-slot"
  }'

3. Registrar el ID del borrador de la respuesta
4. Verificar las opciones de programación (next-free-slot / fecha específica)
5. Guardar el resultado en output/typefully/draft-result.json
```

**Resultado esperado**: Se crea un borrador en Typefully con la programación configurada.

---

## 🚀 Step 3: Publicación simultánea en X (Twitter) y Threads

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Publicación simultánea en X y Threads",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Crea un borrador con la API de Typefully que publique simultáneamente en X (Twitter) y Threads.

Pasos:
1. Especificar los destinos de publicación con el parámetro share:

curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "¡Prueba de publicación automática desde la API de Typefully!\n\nDistribuyendo simultáneamente a X y Threads.\n\n#AutoPost #TypefullyAPI",
    "schedule-date": "next-free-slot",
    "share": true
  }'

2. Verificar los destinos de publicación (X / Threads) en el panel de Typefully
3. Guardar resultados en output/typefully/multi-post-result.json
4. Verificar los límites de caracteres y las diferencias de formato entre plataformas
```

**Resultado esperado**: Se crea un borrador para publicación simultánea en X y Threads.

---

## 🚀 Step 4: Automatización de publicaciones secuenciales en formato hilo

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Automatización de hilos",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Crea una publicación secuencial en formato hilo usando la API de Typefully.

Pasos:
1. Usa cuatro saltos de línea (\n\n\n\n) como separador de hilo en el campo content:

curl -X POST "https://api.typefully.com/v1/drafts/" \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "[Guía de Agentes IA 1/3]\n\nUn agente de IA es una IA que ejecuta tareas de forma autónoma basándose en instrucciones.\n\n\n\n[2/3]\n\nCasos de uso prácticos:\n- Respuestas automáticas de correo\n- Gestión de agenda\n- Generación de informes de análisis de datos\n\n\n\n[3/3]\n\n¡Empezar es fácil!\nPrueba automatizando una tarea primero.\n\nMás información en el enlace del bio 👇",
    "schedule-date": "next-free-slot",
    "threadify": true
  }'

2. Verificar que el hilo se divide correctamente en tweets individuales
3. Guardar resultados en output/typefully/thread-result.json
```

**Resultado esperado**: Se crea un hilo de 3 tweets como borrador.

---

## 🚀 Step 5: Verificación de resultados y registro

AskUserQuestion (AskQuestion) te permite elegir "Continuar / Solo ver ejemplos / Saltar".

**Configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificación de resultados y registro",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué quieres hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver ejemplos"},
      {"id": "skip", "label": "Saltar"}
    ]
  }]
}
```

**Guía después de la selección:**
Entrada:
```
Verifica los resultados de las publicaciones y crea un resumen.

Pasos:
1. Verificar la lista de borradores creados en el panel de Typefully
2. Verificar el estado de cada borrador (Borrador / Programado / Publicado)
3. Crear un resumen en output/typefully/summary.md que cubra:
   - Número de borradores creados
   - Detalles de programación
   - Destinos de publicación (X / Threads)
   - Estructura de publicaciones en hilo
4. Sugerir 3 puntos de mejora para futuras automatizaciones
```

**Resultado esperado**: Se guarda un resumen de resultados de publicación en output/typefully/.

---

## ⚠️ Solución de problemas comunes

AskUserQuestion (AskQuestion) te permite seleccionar el problema para recibir orientación.

**Configuración de AskQuestion:**
```json
{
  "title": "Selecciona tu problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Selecciona el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "Error de autenticación de clave API"},
      {"id": "trouble_2", "label": "Error al crear borrador"},
      {"id": "trouble_3", "label": "El hilo no se divide correctamente"},
      {"id": "trouble_4", "label": "Las publicaciones no aparecen en Threads"}
    ]
  }]
}
```


### Problema 1: "Error de autenticación de clave API"
**Causa**: Clave API inválida o variable de entorno no configurada correctamente
**Prompt de solución**:
```
Verifica que la variable de entorno TYPEFULLY_API_KEY esté configurada correctamente.
Ejecuta [[ -n "$TYPEFULLY_API_KEY" ]] && echo "configurado" || echo "no configurado" para verificar la existencia,
y verifica que la clave sea válida en Typefully Settings → API & Integrations.
```

### Problema 2: "Error al crear borrador"
**Causa**: Formato JSON inválido en el cuerpo de la solicitud o campos obligatorios faltantes
**Prompt de solución**:
```
Verifica el cuerpo JSON en tu comando curl.
El campo content es obligatorio.
Verifica que el encabezado Content-Type: application/json esté incluido.
Usa jq para formatear la respuesta y facilitar la depuración.
```

### Problema 3: "El hilo no se divide correctamente"
**Causa**: Separador de hilo (cuatro saltos de línea) incorrecto
**Prompt de solución**:
```
Los separadores de hilo usan \n\n\n\n (cuatro saltos de línea).
Verifica que los saltos de línea sean correctos en el campo content.
También verifica que el parámetro threadify esté configurado como true.
```

### Problema 4: "Las publicaciones no aparecen en Threads"
**Causa**: Cuenta de Threads no conectada a Typefully
**Prompt de solución**:
```
Verifica si tu cuenta de Threads está conectada en
Typefully Settings → Accounts.
También consulta la documentación más reciente de Typefully sobre el soporte de la API de Threads.
```

---

## ✅ Punto de control
- [ ] Comprendida la descripción general de la API de Typefully y configurada la clave API
- [ ] Creado un borrador y configurada la publicación programada
- [ ] Probada la publicación simultánea en X (Twitter) y Threads
- [ ] Automatizada la publicación secuencial en formato hilo
- [ ] Resultados de publicación guardados en output/typefully/


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 output/typefully/
├── draft-result.json          ← Resultado de creación de borrador individual
├── multi-post-result.json     ← Resultado de publicación simultánea X/Threads
├── thread-result.json         ← Resultado de publicación en hilo
└── summary.md                 ← Resumen de resultados de publicación
```
> Formato: JSON / Markdown

### Comandos de verificación
```bash
# Verificar archivos de salida
ls -lh output/typefully/

# Verificar resultado del borrador
cat output/typefully/draft-result.json | jq .

# Verificar resumen
cat output/typefully/summary.md
```

> 💡 **Claude Code**: `Read output/typefully/summary.md` para vista previa en chat
> 💡 **Cursor**: Haz clic en el archivo en el explorador de archivos para previsualizar

---

## ✅ Verificación de finalización
Pega lo siguiente en el chat de Cursor para verificar el estado de finalización:

```
# Verificación de finalización: Verifica que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra el estado de completado/incompleto y los elementos faltantes.

---

## ➡️ Próximos pasos

¡Has completado todas las lecciones del Módulo 17: Marketing!

AskUserQuestion (AskQuestion) te permite elegir.

**Configuración de AskQuestion:**
```json
{
  "title": "Elige el próximo paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elige tu próxima acción",
    "options": [
      {"id": "next_module", "label": "Iniciar siguiente módulo (/start-18-1)"},
      {"id": "review_module", "label": "Revisar Módulo 17"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Guía después de la selección:**
- next_module → /start-18-1 para ir al módulo de Requisitos/Desarrollo de Sistemas
- review_module → Revisar cada lección del Módulo 17
- finish → Finalizar sesión
