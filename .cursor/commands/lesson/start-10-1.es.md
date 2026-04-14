---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module10-gas"
duration: "~25 min"
prerequisites: ["start-0-1"]
level: "intermediate"
tags: ["gas", "clasp", "google", "automation"]
---

# 🎓 Lesson 10-1: Configuracion del entorno GAS con Clasp

## 📍 Lo que hara en esta sesion

**Lección 10-1: Configuración del entorno de desarrollo GAS**!

| Elemento | Contenido |
|------|------|
| Objetivo | Habilitar la gestion local y el despliegue de proyectos GAS con Clasp |
| Duracion | ~25 min |
| Habilidades utilizadas | gas-clasp-ops, clasp CLI |
| Requisitos previos | Node.js instalado, cuenta de Google, Apps Script API habilitada, Lesson 0-1 completada |
| Pagina del curso | [Module 10: GAS](https://ai-agent.camp/es/course/module-10)  como referencia paralela |

**Flujo de la sesion:**
1. Instalar Clasp
2. Crear un proyecto GAS y hacer push
3. Desplegar y verificar operación

Al final de esta sesion, podra editar y desplegar GAS desde su entorno local.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar. Este es un comportamiento de Cursor, no un mal funcionamiento.

---

## 🎯 Verificacion de preparacion

Primero verifiquemos que todo este listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Verificacion previa a la sesion",
  "questions": [{
    "id": "readiness",
    "prompt": "Esta listo/a?",
    "options": [
      {"id": "ready", "label": "Listo! Comencemos"},
      {"id": "check_prereq", "label": "Verificar requisitos previos"},
      {"id": "view_html", "label": "Ver primero la pagina del curso"},
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Install Clasp and Verify Apps Script API

Primero, verifique que la Google Apps Script API esté habilitada.
Si está deshabilitada, clasp login y clasp create fallarán.

**Apps Script API Activation Check:**
1. Acceder a https://script.google.com/home/usersettings
2. Verificar que el interruptor de "Google Apps Script API" está **ON**
3. Si está OFF, cambiar a ON

> **Importante**: Si la Apps Script API está deshabilitada, todas las operaciones después de `clasp login` (`clasp create`, `clasp push`, etc.) fallarán. Asegúrese de habilitarla primero.

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Instalación de Clasp",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, verifique que Clasp funciona correctamente.
Ejecute npx -y @google/clasp --version para verificar.
```

**Resultado esperado:** Se muestra el numero de version de Clasp (por ejemplo, 2.4.2)

---

## 🚀 Step 2: Google Authentication

> **Relación con gogcli**: Completó la autenticación OAuth de Google de gogcli (`gog auth login`) en 4-1, pero clasp usa sus propias credenciales. Como la autenticación de gogcli y clasp se gestionan por separado, necesita ejecutar `clasp login` aquí.
>
> - **Autenticación gogcli**: Guardada en `~/.config/gogcli/` -> para acceso a APIs de Gmail, Calendar, Drive, Sheets
> - **Autenticación clasp**: Guardada en `~/.clasprc.json` -> para gestionar y desplegar proyectos Apps Script

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Autenticación de Google (clasp login)",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, ejecute npx -y @google/clasp login para iniciar sesión con su cuenta de Google.
Se abrirá un navegador, complete la autenticación.
Después de la autenticación, verifique que se haya creado ~/.clasprc.json.

Nota: La autenticación de Google para gogcli se completó en 4-1,
pero clasp requiere su propia autenticación. Inicie sesión con la misma cuenta de Google.
```

**Resultado esperado:** Despues de autenticarse en el navegador, se muestra "Authorization successful".

---

## 🚀 Step 3: Create a GAS Project

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear un proyecto GAS",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, cree el siguiente directorio y proyecto GAS:

1. Crear el directorio ~/ai-agent-camp/gas-example
2. Ejecutar npx -y @google/clasp create --type standalone en ese directorio
3. Mostrar el contenido de los archivos .clasp.json y appsscript.json creados
```

**Resultado esperado:** El ID del script aparece en `.clasp.json` y la configuracion de zona horaria se incluye en `appsscript.json`.

---

## 🚀 Step 4: Create Hello World Script

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Crear script Hello World",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, cree un archivo Code.gs en el directorio gas-example con el siguiente contenido:

function helloWorld() {
  Logger.log("Hello World from GAS!");
  return "Success";
}

function getExecutionInfo() {
  const info = {
    user: Session.getActiveUser().getEmail(),
    timezone: Session.getScriptTimeZone(),
    timestamp: new Date().toISOString()
  };
  Logger.log(JSON.stringify(info));
  return info;
}

Luego sincronice con npx -y @google/clasp push.
```

**Resultado esperado:** Se muestra "Pushed X files." y los cambios se reflejan en Google Drive.

---

## 🚀 Step 5: Verify in GAS Editor

Utilice AskQuestion para elegir "Continuar / Solo ver el ejemplo / Omitir".

**Configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Verificar en el editor de GAS",
  "questions": [{
    "id": "step_action",
    "prompt": "Que desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Solo ver el ejemplo"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
Entrada:
```
Por favor, ejecute npx -y @google/clasp open para abrir el editor de Google Apps Script en el navegador.
Ejecute la función helloWorld en el editor y verifique los registros.
```

**Resultado esperado:** Se abre el editor GAS y al ejecutar la funcion helloWorld se muestra "Hello World from GAS!" en el registro.

---

## ⚠️ Problemas comunes y soluciones

Utilice AskQuestion para seleccionar el problema y luego siga las indicaciones.

**Configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que corresponda",
    "options": [
      {"id": "trouble_1", "label": "clasp: command not found"},
      {"id": "trouble_2", "label": "Permission denied"},
      {"id": "trouble_3", "label": "Push failed: File name contains invalid characters"},
      {"id": "trouble_4", "label": "Script ID is invalid"},
      {"id": "trouble_5", "label": "Apps Script API has not been used / is not enabled"}
    ]
  }]
}
```


### Problema 1: "clasp: command not found"
**Causa:** Clasp no esta instalado o no se ha agregado al PATH
**Prompt de solucion:**
```
Por favor, vuelva a ejecutar npx -y @google/clasp --version y revise el error. Asegúrese de que Node.js y npm estén instalados correctamente.
```

### Problema 2: "Permission denied"
**Causa:** La autenticacion de Google no esta completa
**Prompt de solucion:**
```
Por favor, ejecute npx -y @google/clasp logout y luego ejecute npx -y @google/clasp login nuevamente.
Proporcione los detalles del error de autenticación.
```

### Problema 3: "Push failed: File name contains invalid characters"
**Causa:** El nombre del archivo contiene caracteres no ASCII como japones
**Prompt de solucion:**
```
Por favor, verifique los nombres de archivo en el directorio gas-example y corrija para usar solo caracteres alfanuméricos y guiones bajos.
```

### Problema 4: "Script ID is invalid"
**Causa:** .clasp.json no existe o esta corrupto
**Prompt de solucion:**
```
Por favor, elimine el archivo .clasp.json y vuelva a ejecutar npx -y @google/clasp create --type standalone.
```

### Problema 5: "Apps Script API has not been used in project / User has not enabled the Apps Script API"
**Causa:** Google Apps Script API esta deshabilitada
**Pasos de resolución**:
1. Acceder a https://script.google.com/home/usersettings
2. Cambiar el interruptor de "Google Apps Script API" a **ON**
3. Después del cambio, repetir desde `clasp login`

> Esta configuración es por cuenta de Google. Una vez habilitada, se puede usar para todos los proyectos GAS posteriores.

---

## ✅ Punto de control
- [ ] Clasp está disponible (verificar con npx -y @google/clasp --version)
- [ ] La autenticación de Google está completa (~/.clasp.json existe)
- [ ] El proyecto GAS está inicializado
- [ ] Code.gs ha sido creado
- [ ] npx -y @google/clasp push tiene éxito
- [ ] Se puede ejecutar en el editor de GAS


---

## 📋 Vista previa de entregables

### Salida esperada
```
📁 output/gas/
└── Code.gs  (script GAS)
```

### Comandos de verificacion
```bash
# Verificar archivos de script locales
ls -la output/gas/

# Verificar el inicio del contenido del script
head -30 output/gas/Code.gs

# Verificar en el editor de GAS
npx -y @google/clasp open
```

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat para verificar la finalizacion:

```
# Verificación de finalización: Verifique lo siguiente.
# 1. npx -y @google/clasp --version muestra la versión
# 2. gas-example/.clasp.json existe
# 3. gas-example/Code.gs existe
# 4. npx -y @google/clasp push tiene éxito (ejecutar en el directorio gas-example)
# 5. npx -y @google/clasp open abre el editor de GAS
```

**Resultado esperado:** Todos los elementos pasan y el proyecto GAS se puede gestionar y desplegar desde local.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Utilice AskQuestion para elegir.

**Configuracion de AskQuestion:**
```json
{
  "title": "Elija el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Elija que hacer a continuacion",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente sección (/start-10-2)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-10-2)"},
      {"id": "finish", "label": "Terminar aqui"}
    ]
  }]
}
```

**Indicaciones tras la seleccion:**
- next_auto → /start-10-2
- next_window → Abrir nueva ventana con /start-10-2
- finish → Finalizar
