---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module01-banner"
prerequisites: ["start-1-1"]
duration: "~30 min"
level: "beginner"
tags: ["image", "nanobanana", "gemini", "editing"]
---

# 🎓 Lesson 1-3: Edición de imágenes con nanobanana

## 📍 Lo que hará en está sesion

Bienvenido a **Lesson 1-3: Edición de imágenes con nanobanana**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Generar imágenes a partir de texto y editar imágenes existentes usando el Skill nanobanana |
| Duración | ~30 min |
| Skills utilizados | nanobanana (Gemini Image Generation API) |
| Requisitos previos | Lesson 1-1 completada, clave de Gemini API configurada |
| Página del curso | Consulte [Module 1: Generación de banners e imágenes](https://ai-agent.camp/es/course/module-1) en paralelo |

**Flujo de la sesion:**
1. Generar imágenes a partir de texto
2. Generar imágenes de escenas específicas
3. Editar imágenes existentes (opcional)

Al finalizar está sesion, las imágenes generadas y editadas estarán guardadas en outputs.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificación de preparación

Verifiquemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificación de requisitos previos)
(view_html → Mostrar ruta de la página del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Generar imágenes a partir de texto

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Generar imagenes a partir de texto",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
Entrada:
```
Use nanobanana para generar la siguiente imagen:
- Estilo: Diseno plano
- Tema: Trabajo en equipo
- Proposito: Presentacion de negocios
Salida: ~/ai-agent-camp/output/nanobanana-teamwork.png
```

**Resultado esperado**: Se genera una imagen de diseño plano con el tema de trabajo en equipo.

---

## 🚀 Step 2: Generar imágenes de escenas específicas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Generar imagenes de escenas especificas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
Entrada:
```
Genere una imagen de "escena de oficina moderna" con nanobanana.
Condiciones:
- Diseno plano, minimalista
- Tonos de colores brillantes
- Incluir un escritorio, plantas de interior y ventanas
Salida: ~/ai-agent-camp/output/nanobanana-office.png
```

**Resultado esperado**: Se genera una imagen de oficina que cumple con las condiciones especificadas.

---

## 🚀 Step 3: Editar imágenes existentes

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Editar imagenes existentes",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
Entrada:
```
Edite la imagen de oficina generada anteriormente (nanobanana-office.png):
- Cambie el fondo a un cielo de atardecer
- Agregue efectos de iluminacion calida
Salida: ~/ai-agent-camp/output/nanobanana-office-sunset.png
```

**Resultado esperado**: Se genera una imagen basada en la original con el fondo cambiado a un cielo de atardecer.

---

## 🚀 Step 4: Generar imágenes estilo logo e iconos

Cree imágenes listas para uso empresarial usando los siguientes prompts:

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Generar imagenes estilo logo e iconos",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
Entrada:
```
Genere las siguientes 2 imagenes con nanobanana:

1. Imagen estilo logo de una cafeteria
   - Simple, diseno plano
   - Silueta de taza de cafe
   - Salida: ~/ai-agent-camp/output/logo-coffee.png

2. Icono que represente un agente de IA
   - Sensacion tecnologica, futurista
   - Colores base azul y blanco
   - Salida: ~/ai-agent-camp/output/icon-ai.png
```

**Resultado esperado**: Se generan una imagen estilo logo y un icono.

---

## 🚀 Step 5: Comparar diferentes estilos

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Comparar diferentes estilos",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
Entrada:
```
Genere imagenes con el tema "Negocio en crecimiento" en 3 estilos diferentes:

1. Diseno plano (simple, minimalista)
2. Estilo ilustracion 3D (dimensional, pop)
3. Estilo acuarela (aspecto dibujado a mano, calido)

Guarde cada una como un archivo separado.
```

**Resultado esperado**: Se generan tres imágenes con el mismo tema pero diferentes estilos para comparar.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "La imagen generada difiere de lo esperado"},
      {"id": "trouble_2", "label": "Las ediciones de imagen no se reflejan"},
      {"id": "trouble_3", "label": "Error de limite de solicitudes de API"},
      {"id": "trouble_4", "label": "El logo es demasiado complejo"}
    ]
  }]
}
```


### Problema 1: "La imagen generada difiere de lo esperado"
**Causa**: El prompt es demasiado abstracto
**Prompt de solución**:
```
Reescriba su prompt de forma mas especifica:
Mal ejemplo: "una imagen bonita"
Buen ejemplo: "Una familia haciendo un picnic en cesped verde bajo un cielo azul,
              diseno plano, tonos de colores brillantes, relacion de aspecto 16:9"
```

### Problema 2: "Las ediciones de imagen no se reflejan"
**Causa**: Las instrucciones de edición no son claras, o la ruta de la imagen es incorrecta
**Prompt de solución**:
```
Verifique la ruta de la imagen de entrada:
ls ~/ai-agent-camp/output/nanobanana-office.png

Si el archivo existe, haga las instrucciones de edicion mas especificas:
"Cambiar solo el fondo" "Mantener el sujeto"
```

### Problema 3: "Error de limite de solicitudes de API"
**Causa**: Se enviaron demasiadas solicitudes en poco tiempo
**Prompt de solución**:
```
Se alcanzo el limite de solicitudes de API.
Espere aproximadamente 1 minuto e intente de nuevo.
Para generacion continua, agregue una espera de 5 segundos entre cada solicitud.
```

### Problema 4: "El logo es demasiado complejo"
**Causa**: Especificación insuficiente de simplicidad
**Prompt de solución**:
```
Regenere el logo con restricciones mas simples:
- Maximo 3 colores
- Solo un simbolo
- Sin texto
- Fondo transparente o de color solido
```

---

## ✅ Punto de control
- [ ] Genero imágenes a partir de texto
- [ ] Genero imágenes con condiciones específicas
- [ ] Edito imágenes existentes
- [ ] Genero imágenes estilo logo e iconos
- [ ] Genero imágenes del mismo tema en diferentes estilos para comparar


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 docs/generated/banners/
├── banner-{nombre-del-tema}.png
└── (variaciones)
```
> Formato: PNG | Tamaño: Configuración automática

### Comandos de verificación
```bash
# Listado de archivos
ls -la docs/generated/banners/

# Abrir imagenes (macOS: open / Linux: xdg-open)
open docs/generated/banners/
```

> 💡 **Claude Code**: Especifique la ruta del archivo con la herramienta Read para previsualizar imágenes en el chat
> 💡 **Cursor**: Haga clic en la imagen en el explorador de archivos para previsualizar

---

## ✅ Verificación de finalización
Pegue lo siguiente en el chat de Cursor para verificar la finalización:

```
# Verificacion de finalizacion: Verifique que los archivos de salida esperados se hayan generado en la carpeta output/.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta sección está completa. Inicie la siguiente sección o abra una nueva ventana para comenzar una nueva sección.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccionar siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija su siguiente accion",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente seccion (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en una nueva ventana (/start-2-1)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Después de la selección (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-2-1
- finish → Finalizar
