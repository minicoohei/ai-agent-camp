---
name: tmux-session-manager
description: "Gestiona sesiones tmux de Claude Code en Lightsail vía SSH. Se activa con solicitudes como 'Verificar sesiones', 'Sincronizar PRs', 'Estado de tmux', etc."
triggers:
  - Verificar sesiones
  - Lista de sesiones
  - Estado de tmux
  - Verificar progreso de PR
  - Enviar instrucciones a la sesión
  - tmux-session-manager
  - sync-prs
---
# Habilidad de Gestión de Sesiones Tmux

Habilidad para gestionar sesiones tmux de Claude Code en ejecución en Lightsail vía SSH.
Maneja verificación de estado de sesiones, envío de instrucciones y sincronización de PRs por Issue/PR.

## Activadores

Se activa con las siguientes palabras clave:
- "Verificar sesiones", "Lista de sesiones", "Estado de tmux"
- "Progreso de PR", "Estado de trabajo del Issue"
- "Crear sesión", "Sincronizar PRs", "sync-prs"
- "Panel de control", "tmux dashboard"
- "Enviar instrucciones a sesión", "send-keys"

## Rutas de Scripts

En remoto (Lightsail):
```
REPO=/home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata
CC=$REPO/ops/tmux-manager/cc-session.sh
SYNC=$REPO/ops/tmux-manager/sync-prs.sh
```

## Ejecución de Comandos

Todos los comandos se ejecutan vía SSH. El alias `ssh lightsail` está configurado en `~/.ssh/config`.

### Mostrar Panel de Control

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh dashboard"
```

### Listar Sesiones

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh list"
```

### Verificar Estado de Sesión

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh status PR-45"
```

### Capturar Salida de Sesión

```bash
# 100 líneas por defecto
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh capture PR-45"

# Especificar número de líneas
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh capture PR-45 200"
```

### Crear Sesión

```bash
# Para PR
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh create PR-45"

# Para Issue
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh create ISSUE-123"
```

### Enviar Instrucciones (send-keys)

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh send PR-45 'Atender los comentarios de revisión de este PR y hacer push'"
```

### Sincronizar Todos los PRs Abiertos

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/sync-prs.sh --cleanup"
```

### Terminar Sesión

```bash
ssh lightsail "cd /home/runner/actions-runner/_work/githubactions_fordata/githubactions_fordata && bash ops/tmux-manager/cc-session.sh kill PR-45"
```

## Flujos de Trabajo

### 1. Verificación de Estado General

Cuando el usuario pregunta "Verificar sesiones" o "¿Cuál es el estado actual?":

1. Mostrar vista general con el comando `dashboard`
2. Verificar detalles individuales con `status` según sea necesario
3. Resumir y reportar resultados al usuario en formato comprensible

### 2. Sincronización de PRs + Creación de Sesiones

Cuando el usuario dice "Sincronizar PRs" o "Crear sesiones para todos los PRs":

1. Sincronizar todos los PRs abiertos con `sync-prs.sh --cleanup`
2. Reportar resultados (cantidad creada, cantidad omitida, cantidad limpiada)

### 3. Envío de Instrucciones a Sesión Específica

Cuando el usuario dice "Que PR-45 atienda la revisión":

1. Verificar estado actual con `status PR-45`
2. Si está inactiva, enviar instrucciones con `send PR-45 "contenido de la instrucción"`
3. Si está trabajando, confirmar "Actualmente trabajando. ¿Desea esperar a que termine?"

### 4. Verificación/Resumen de Salida de Sesión

Cuando el usuario pregunta "¿Qué está haciendo PR-45?":

1. Obtener última salida con `capture PR-45 100`
2. Resumir el contenido y reportar al usuario

## Notas

- Si la conexión SSH expira, agregar `-o ConnectTimeout=10`
- No enviar send-keys a sesiones que estén trabajando activamente (siempre verificar estado primero)
- Se recomienda mantener las sesiones simultáneas en 5 o menos (restricciones de recursos de Lightsail)
- Los logs se guardan en `ops/tmux-manager/logs/`
