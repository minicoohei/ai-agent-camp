---
description: "When the user says /start-4-1 — Module 4 Lesson 4-1: Configuracion de autenticacion de gogcli"
chapter: "courses/aiagent/lesson03-core/module04-google-workspace/chapter.yaml"
duration: "~25 min"
prerequisites: ["start-0-1"]
level: "beginner"
tags: ["google", "workspace", "gogcli", "auth"]
---

# 🎓 Lesson 4-1: Configuracion de autenticacion de gogcli

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 4-1: Configuracion de autenticacion de gogcli**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Autenticarse con una cuenta de Google usando gogcli para habilitar Gmail/Calendar/Drive |
| Duracion | ~25 min |
| Skills utilizados | gogcli (gog) |
| Requisitos previos | Configuracion del entorno completada (start-0-1 finalizado) |

**Flujo de la sesion:**
1. Verificar la instalacion de gogcli
2. Agregar una cuenta de Google mediante autenticacion OAuth
3. Verificar el estado de autenticacion y prueba de operacion basica

Al finalizar esta sesion, gogcli tendra acceso a Gmail, Calendar y Drive.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de iniciar la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo/a?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Verificar instalacion de gogcli

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Verificar la instalacion de gogcli",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:

Verifique que gogcli esta instalado. Ejecute los siguientes comandos:

```bash
# Verificar version
gog --version

# Si no esta instalado
brew install gogcli
# Si Homebrew no esta disponible, descargue de GitHub Releases:
# https://github.com/steipete/gogcli/releases
```

**Resultado esperado**: Se muestra el numero de version de gogcli (por ejemplo, `gog version 0.x.x`).

> **📝 Nota**: gogcli no requiere crear un cliente OAuth en la consola de GCP. Utiliza credenciales OAuth integradas para la autenticacion, lo que hace que la configuracion sea muy sencilla.

---

## 🚀 Step 2: Agregar cuenta de Google via OAuth

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Agregar una cuenta de Google mediante autenticacion OAuth",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:

Autentique su cuenta de Google. Ejecute el siguiente comando:

```bash
# Agregar cuenta de Google (se abrira el navegador)
gog auth add your-email@gmail.com
```

**Pasos:**
1. Al ejecutar el comando, el navegador se abrira automaticamente
2. Inicie sesion con su cuenta de Google
3. Apruebe los permisos de acceso para gogcli (Gmail, Calendar, Drive, Sheets, etc.)
4. Una vez que se muestre "Autenticacion completada", puede cerrar el navegador

```bash
# Verificar lista de cuentas autenticadas
gog auth list

# Verificar subcomandos disponibles
gog --help
```

**Resultado esperado**: `gog auth list` muestra su direccion de correo electronico.

> **⚠️ Advertencia**: Las credenciales de autenticacion se almacenan de forma segura en su maquina local. Los tokens se almacenan en el directorio `.gog/`.

---

## 🚀 Step 3: Prueba de operacion basica

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Prueba de operacion basica",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:

Verifique que cada servicio esta funcionando correctamente:

```bash
# Gmail: Buscar los 5 correos mas recientes
gog gmail search "newer_than:1d" --account your-email@gmail.com

# Calendar: Listar los eventos de hoy
gog calendar list --account your-email@gmail.com --days 1

# Drive: Listar archivos en la carpeta raiz
gog drive ls --account your-email@gmail.com --max 5
```

**Resultado esperado**: Se muestran datos de Gmail/Calendar/Drive con cada comando. Si no aparecen errores, la autenticacion se ha completado exitosamente.

> **💡 Consejo**: El indicador `--account` es obligatorio para todos los comandos de gogcli. Debe especificar su direccion de correo electronico cada vez.

---

## ⚠️ Problemas comunes y soluciones

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No se puede instalar gogcli"},
      {"id": "trouble_2", "label": "El navegador no se abre"},
      {"id": "trouble_3", "label": "No se puede acceder despues de la autenticacion"},
      {"id": "trouble_4", "label": "Error de permiso denegado"}
    ]
  }]
}
```

### Problema 1: "No se puede instalar gogcli"
**Causa**: Homebrew no esta instalado o PATH no esta configurado
**Prompt de solucion**:
```text
Verifique el metodo de instalacion de gogcli.
Si Homebrew esta disponible, intente brew install gogcli.
Si Homebrew no esta disponible, descargue el binario de https://github.com/steipete/gogcli/releases.
```

### Problema 2: "El navegador no se abre"
**Causa**: Se esta ejecutando en un entorno remoto o sin interfaz grafica
**Prompt de solucion**:
```text
Copie la URL que se muestra al ejecutar gog auth add y peguelo en su navegador manualmente.
Ingrese el codigo de autenticacion en la terminal cuando se emita.
```

### Problema 3: "No se puede acceder despues de la autenticacion"
**Causa**: El almacenamiento del token fallo, o alcance insuficiente
**Prompt de solucion**:
```text
Elimine la autenticacion con gog auth remove your-email@gmail.com,
luego vuelva a autenticarse con gog auth add your-email@gmail.com.
```

### Problema 4: "Error de permiso denegado"
**Causa**: Los permisos de acceso son insuficientes en el lado de la cuenta de Google
**Prompt de solucion**:
```text
Verifique que las "Aplicaciones menos seguras" no esten bloqueadas en la configuracion de seguridad de su cuenta de Google.
Si un administrador de Google Workspace ha establecido restricciones de API, consulte al administrador.
```

---

## ✅ Punto de control
- [ ] gogcli esta instalado (`gog --version` funciona)
- [ ] La autenticacion de la cuenta de Google esta completa (`gog auth list` lo muestra)
- [ ] La busqueda de Gmail funciona (`gog gmail search` muestra correos)
- [ ] El listado del calendario funciona (`gog calendar list` muestra eventos)
- [ ] El listado de archivos de Drive funciona (`gog drive ls` muestra archivos)


---

## 📋 Vista previa de resultados

El entregable de esta leccion es la salida de la terminal.

### Salida esperada
```text
┌─────────────────────────────────────┐
│  Resultado de ejecución del comando    │
│  Estado: ✅ Éxito                       │
│  Elementos procesados: N               │
└─────────────────────────────────────┘
```

> Consejo: Para guardar la salida en un archivo, agregue ` > output/result.txt` al final del comando

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Codex para verificar la finalizacion:

```text
Ejecute los siguientes comandos para verificar el estado de autenticacion de gogcli:
1. gog auth list
2. gog gmail search "newer_than:1d" --account <su-correo>
3. gog calendar list --account <su-correo> --days 1
Verifique que todos los comandos funcionen correctamente.
```

**Resultado esperado**: Los tres comandos se ejecutan sin errores.

---

## 🎉 Siguientes pasos

La configuracion de autenticacion de gogcli esta completa! En la siguiente leccion, aprendera busqueda y visualizacion de Gmail.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/start-4-2)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-4-2)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /start-4-2（Busqueda y visualizacion de Gmail)
- next_window → Abrir nueva ventana con /start-4-2
- finish → Finalizar
