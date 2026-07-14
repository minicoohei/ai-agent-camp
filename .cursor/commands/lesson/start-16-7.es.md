---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "25 min"
prerequisites: ["start-16-6"]
level: "beginner"
tags: ["email", "resend", "api-key", "resend-cli", "send"]
nonInteractiveMode: deferred
---
# Lección 16-7: Creación de Clave API y Primer Envió de Correo

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-7: Creación de Clave API y Primer Envió de Correo**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear una clave API de Resend y enviar correos con CLI y SDK |
| Duración | ~25 min |
| Herramientas utilizadas | Resend CLI (`resend-cli`), Resend SDK (TypeScript) |
| Requisitos previos | Lección 16-6 completada (dominio verificado) |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

> **Importante**: La clave API se muestra solo una vez. Guardela en .env y no la incluya en commits de Git.

---

## Paso 1: Crear la Clave API

**Crear en el Dashboard de Resend:**
1. Settings -> API Keys -> Create API Key
2. Nombre: a elección (ejemplo: `dev-key`)
3. Permiso: `Full access` (desarrollo) o `Sending access` (producción)
4. Dominio: Seleccione el dominio verificado

**Diferencia de permisos:**
| Permiso | Capacidades | Uso recomendado |
|---------|-------------|-----------------|
| Full access | Envió de correo + gestión de dominios + gestión de Audience | Desarrollo y pruebas |
| Sending access | Solo envío de correo | Producción (principio de mínimo privilegio) |

**Guardar la clave API en .env:**
```bash
echo "RESEND_API_KEY=re_xxxxxxxx" >> .env
```

---

## Paso 2: Enviar Correo con Resend CLI

**Envió de prueba con CLI:**
```bash
resend emails send \
  --from "noreply@su-dominio.com" \
  --to "su-email@gmail.com" \
  --subject "Prueba de envio con Resend CLI" \
  --html "<p>Este es un correo de prueba enviado desde Resend CLI!</p>"
```

**Verificar resultado del envío:**
```bash
resend emails list
```

**Envió programado (compatible con lenguaje natural):**
```bash
resend emails send \
  --from "noreply@su-dominio.com" \
  --to "su-email@gmail.com" \
  --subject "Prueba de envio programado" \
  --html "<p>Este correo llegara en 1 hora</p>" \
  --scheduled-at "in 1 hour"
```

---

## Paso 3: Enviar con Resend SDK

**Instalar SDK:**
```bash
npm install resend
```

**Envió de correo con TypeScript:**
```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'noreply@su-dominio.com',
  to: 'su-email@gmail.com',
  subject: 'Prueba de envio con Resend SDK',
  html: '<p>Este es un correo de prueba enviado desde Resend SDK!</p>',
});

if (error) {
  console.error('Error de envio:', error);
} else {
  console.log('Envio exitoso:', data);
}
```

---

## Paso 4: Gestión Segura de la Clave API con .env

**Agregar .env a .gitignore:**
```bash
echo ".env" >> .gitignore
```

**Verificar:**
```bash
cat .gitignore | grep .env
```

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| `API key is invalid` | Verifique que la clave API fue copiada correctamente. Puede ser necesario recrearla |
| `Domain not verified` | Regrese a 16-6 y complete la verificación del dominio |
| `The from address is not verified` | Verifique que el dominio de la dirección de envío este verificado |
| El correo no llega | Verifique la carpeta de correo no deseado. Revise la configuración SPF/DKIM |

---

## Punto de Control

- [ ] Creó la clave API y la guardo en .env
- [ ] Envió un correo de prueba con Resend CLI
- [ ] Envió un correo con Resend SDK (TypeScript)
- [ ] .gitignore incluye .env

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-7 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_lesson", "label": "Ir a Leccion 16-8 -> Campana de goteo con Resend Sequence"},
      {"id": "practice", "label": "Quiero probar mas envios de correo"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
