---
description: "Configuración automática de seguridad"
duration: "~5 min"
prerequisites: ["La carpeta ai-agent-camp está abierta en Cursor"]
level: "beginner"
tags: ["setup", "security"]
---

# /setup-security -- Configuración automática de seguridad

## Step 0: Verificar progreso de configuración

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py show --current setup-security` para mostrar el progreso
2. Verificar si ya está configurado:
   - Si `.gitignore` está correctamente configurado
   - Si el hook pre-commit está configurado
   - Si ambos están configurados, preguntar "La configuración de seguridad ya está completa. ¿Desea omitirla?"

## Función de este comando

Este comando **configura automáticamente los ajustes de seguridad para evitar que información confidencial como claves API y contraseñas se publique accidentalmente en GitHub**. La IA se encarga de todo en segundo plano.
No necesita usar el terminal en absoluto. Todo lo ejecuta la IA automáticamente.

| Elemento | Contenido |
|----------|-----------|
| Objetivo | Configurar automáticamente .gitignore y hooks pre-commit para prevenir la filtración de información confidencial |
| Duración | ~5 minutos |
| Requisitos previos | La carpeta ai-agent-camp está abierta en Cursor |
| Acción del usuario | Solo presionar botones (no se necesitan comandos CLI) |

---

## ¿Por qué necesita configuración de seguridad?

> **Explicación con un ejemplo cotidiano:**
>
> Imagine que escribió el "código de la llave de su casa" en un cuaderno y dejó ese cuaderno en un banco del parque -- cualquiera podría entrar a su casa, ¿verdad?
>
> La "clave API" de un servicio de IA equivale a ese "código de llave". Si una clave API se publica en GitHub (un repositorio de código en línea):
>
> - **Otros pueden hacer uso indebido de su clave API** (se envían solicitudes masivas bajo su cuenta, lo que podría resultar en cargos elevados)
> - **Información personal o de la empresa podría filtrarse**
> - **Su cuenta podría ser comprometida**
>
> Esta configuración de seguridad crea un **mecanismo que previene automáticamente la exposición accidental de claves API**.

---

## Verificación de preparación

**Configuración de AskQuestion:**
```json
{
  "title": "Comenzar la configuración de seguridad",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "Comencemos"},
      {"id": "more_info", "label": "Quiero saber más detalles"},
      {"id": "different_lesson", "label": "Ir a otra lección"}
    ]
  }]
}
```

(ready -> Ir al Step 1)
(more_info -> Mostrar lo siguiente)

> **Tres mecanismos de seguridad que configura este comando:**
>
> 1. **.gitignore** -- Una lista que le dice a Git "no subas estos archivos a GitHub". Establece archivos .env que contienen claves API como excluidos de la subida.
>
> 2. **Hook pre-commit** -- Un mecanismo que ejecuta automáticamente una verificación de "¿está seguro?" justo antes de subir a GitHub. Si intenta subir accidentalmente un archivo que contiene claves API, lo bloquea automáticamente.
>
> 3. **Verificación del estado actual** -- La IA verifica automáticamente si alguna clave API ya ha sido expuesta.

(different_lesson -> Mostrar lista de módulos)

---

## Step 1: Verificar y configurar .gitignore

**Lo que la IA ejecuta automáticamente:**

1. Leer el archivo `.gitignore` en la raíz del proyecto
2. Verificar si las siguientes entradas están incluidas:

```text
# Información confidencial (claves API y tokens)
.env
.env.local
.env.*.local

# Credenciales
credentials/
*.key
*.pem

# Archivos generados por el sistema operativo
.DS_Store
Thumbs.db
```

3. **Si faltan entradas**: Agregarlas automáticamente a `.gitignore`

4. Mostrar los resultados al usuario:

```text
Se verificó .gitignore.

| Regla de exclusión | Estado | Descripción |
|-------------------|--------|-------------|
| .env | Agregado | Archivo de claves API |
| .env.local | Agregado | Variables de entorno locales |
| .env.*.local | Agregado | Variables locales por entorno |
| credentials/ | Agregado | Carpeta de credenciales |
| *.key | Agregado | Archivos de clave privada |
| *.pem | Agregado | Archivos de certificado |

Se actualizó .gitignore.
Esto previene que información confidencial como claves API se publique en GitHub.
```

5. **Si todas las entradas ya están presentes**:
```text
.gitignore ya está correctamente configurado. No se necesitan cambios adicionales.
```

**Nota: Toda la verificación y edición de archivos la realiza la IA automáticamente. El usuario no necesita ingresar ningún comando.**

---

## Step 2: Configurar hook pre-commit

**Lo que la IA ejecuta automáticamente:**

1. Verificar si `.git/hooks/pre-commit` existe
2. Si no existe, o no incluye la verificación de .env, crearlo con el siguiente contenido:

```bash
#!/bin/sh
# Verificación de seguridad: Bloquear commits que contengan archivos confidenciales
# Este hook fue generado automáticamente por el comando /setup-security

# Bloquear commits de archivos .env
BLOCKED_FILES=$(git diff --cached --name-only | grep -E '^\\.env$|^\\.env\\.|credentials/|.*\\.key$|.*\\.pem$')

if [ -n "$BLOCKED_FILES" ]; then
    echo ""
    echo "============================================"
    echo "  Advertencia de seguridad: Commit bloqueado"
    echo "============================================"
    echo ""
    echo "Los siguientes archivos pueden contener información confidencial:"
    echo "$BLOCKED_FILES"
    echo ""
    echo "Publicar estos archivos en GitHub podría resultar en"
    echo "uso indebido de claves API o filtración de datos."
    echo ""
    echo "Cómo solucionarlo:"
    echo "  1. Ejecute git reset HEAD <nombre_archivo> para quitar del staging"
    echo "  2. Solo si es absolutamente necesario, use git commit --no-verify para forzar el commit"
    echo ""
    exit 1
fi
```

3. Otorgar permisos de ejecución (la IA ejecuta `chmod +x .git/hooks/pre-commit` en segundo plano)

4. Mostrar los resultados al usuario:
```text
Se configuró el hook de seguridad.

Esto bloqueará automáticamente commits accidentales de los siguientes archivos:
- .env (archivo de claves API)
- .env.local / .env.*.local (archivos de variables de entorno)
- Archivos en la carpeta credentials/
- *.key / *.pem (claves privadas y certificados)

Si intenta accidentalmente hacer commit de estos archivos,
aparecerá un mensaje de advertencia y el commit se detendrá, así que puede estar tranquilo.
```

5. **Si el hook ya está configurado**:
```text
El hook pre-commit ya está configurado. No se necesitan cambios adicionales.
```

**Nota: Toda la creación de archivos y configuración de permisos la realiza la IA automáticamente. El usuario no necesita ingresar ningún comando.**

---

## Step 3: Verificación de seguridad actual

**Lo que la IA ejecuta automáticamente:**

1. Ejecutar `git status` en segundo plano para verificar si los archivos .env están siendo rastreados
2. Ejecutar `git log --all --full-history -- .env .env.local .env.*.local` en segundo plano para verificar si .env fue commitido en el pasado
3. Ejecutar `git ls-files -- .env .env.local` en segundo plano para verificar si están actualmente bajo gestión de Git

4. Mostrar los resultados al usuario:

**Si no hay problemas:**
```text
## Resultados de la verificación de seguridad

| Elemento verificado | Resultado |
|--------------------|-----------|
| ¿.env está siendo rastreado por Git? | No rastreado (seguro) |
| ¿.env fue commitido en el pasado? | Sin historial de commits (seguro) |
| ¿.env está actualmente en staging? | No está en staging (seguro) |

Todas las verificaciones pasaron. La información confidencial se está gestionando de forma segura.
```

**Si hay problemas (.env está siendo rastreado):**
```text
## Resultados de la verificación de seguridad

| Elemento verificado | Resultado |
|--------------------|-----------|
| ¿.env está siendo rastreado por Git? | Está siendo rastreado (necesita corrección) |

Se detectó un problema. El archivo .env está siendo rastreado por Git.
```

**Configuración de AskQuestion:**
```json
{
  "title": "¿Desea corregir el problema automáticamente?",
  "questions": [{
    "id": "fix",
    "prompt": "Se eliminará el archivo .env del rastreo de Git. Esto evita que el archivo .env se suba a GitHub en el futuro.",
    "options": [
      {"id": "yes", "label": "Corregir automáticamente"},
      {"id": "explain", "label": "Explíqueme más sobre lo que se cambiará"},
      {"id": "skip", "label": "Omitir por ahora"}
    ]
  }]
}
```

(yes -> La IA ejecuta automáticamente lo siguiente)
- Ejecutar `git rm --cached .env` en segundo plano (solo elimina el rastreo de Git, el archivo en sí no se borra)
- Volver a verificar que .env esté incluido en `.gitignore`
- Mostrar: "Corrección completa. El archivo .env aún existe localmente pero ya no se subirá a GitHub"

(explain -> Mostrar explicación detallada y volver a mostrar AskQuestion)

(skip -> Continuar)

**Si hay problemas (.env fue commitido en el pasado):**
```text
Existe historial de archivos .env que fueron commitidos en el pasado.
Si se hizo push a GitHub, sus claves API podrían haber sido expuestas.

Acciones recomendadas:
1. Regenerar las claves API afectadas (invalidar las claves antiguas)
2. Emitir una nueva clave desde Google AI Studio
3. Actualizar el archivo .env con la nueva clave

Consulte /start-0-3 (configuración de API de Gemini) para saber cómo regenerar claves API.
```

**Nota: Todas las operaciones de Git se ejecutan en segundo plano por la IA. El usuario no necesita ingresar ningún comando.**

---

## Solución de problemas comunes

**Configuración de AskQuestion:**
```json
{
  "title": "¿Tiene algún problema?",
  "questions": [{
    "id": "trouble",
    "prompt": "¿Hay algún problema?",
    "options": [
      {"id": "trouble_1", "label": "Error de 'permission denied'"},
      {"id": "trouble_2", "label": "Los cambios en .gitignore no surten efecto"},
      {"id": "trouble_3", "label": "El hook pre-commit no funciona"},
      {"id": "no_trouble", "label": "Sin problemas, continuar"}
    ]
  }]
}
```

### Problema 1: Error de "permission denied"
**Causa**: No tiene permisos de escritura para el archivo
**Lo que hace la IA**:
1. Verificar permisos del archivo (la IA ejecuta `ls -la .git/hooks/pre-commit` en segundo plano)
2. Si los permisos son insuficientes, la IA corrige automáticamente
3. Mostrar "Los permisos han sido corregidos"

### Problema 2: Los cambios en .gitignore no surten efecto
**Causa**: Los archivos ya rastreados por Git no se excluyen solo agregándolos a .gitignore
**Lo que hace la IA**:
1. La IA ejecuta `git rm --cached <nombre_archivo>` en segundo plano (el archivo en sí no se elimina)
2. Mostrar "Se eliminó el rastreo de Git. Este archivo ya no se subirá a GitHub"

### Problema 3: El hook pre-commit no funciona
**Causa**: El archivo no tiene permisos de ejecución, o la ruta del archivo es incorrecta
**Lo que hace la IA**:
1. Verificar la existencia y permisos de `.git/hooks/pre-commit` (la IA lo ejecuta en segundo plano)
2. Si hay un problema, recrear automáticamente y volver a otorgar permisos
3. Verificar con un commit de prueba (la IA ejecuta una prueba segura como `git stash && echo "test" > .env_test && git add .env_test && git reset HEAD .env_test && rm .env_test` en segundo plano)
4. Mostrar "Se verificó el funcionamiento del hook"

---

## Punto de verificación

- [ ] .gitignore incluye .env / credentials/ / *.key / *.pem
- [ ] El hook pre-commit está configurado (.git/hooks/pre-commit existe y es ejecutable)
- [ ] El archivo .env no está siendo rastreado por Git
- [ ] No hay historial de .env commitido en el pasado (o ya fue resuelto)

---

## Siguientes pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Elegir siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¿Qué desea hacer ahora?",
    "options": [
      {"id": "check", "label": "Ejecutar verificación integral del entorno (/check-setup)"},
      {"id": "extensions", "label": "Configurar extensiones (/setup-extensions)"},
      {"id": "api", "label": "Configurar claves API (/start-0-3)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

(check -> Guiar a /check-setup)
(extensions -> Guiar a /setup-extensions)
(api -> Guiar a /start-0-3)
(finish -> Mostrar "Buen trabajo. La configuración de seguridad está completa")

---

## Procesamiento de finalización

**Lo que la IA ejecuta automáticamente:**
1. Ejecutar `uv run python tools/setup_progress.py complete setup-security` para actualizar el progreso
2. Se muestra automáticamente el resumen de progreso actualizado
3. Guiar al usuario al siguiente paso: "A continuación, ejecutemos la verificación final con `/check-setup`"
