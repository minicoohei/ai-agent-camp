---
description: "When the user says /start-16-6 — Module 16 Lesson 16-6: Registro en Resend y configuración de dominio - Configuración automática de Vercel DNS"
chapter: "courses/aiagent/lesson03-core/module16-email-automation/chapter.yaml"
category: "lesson"
duration: "30 min"
prerequisites: ["start-13-1"]
level: "beginner"
tags: ["email", "resend", "domain", "dns", "vercel", "spf", "dkim"]
---

# Lección 16-6: Registro en Resend y Configuración de Dominio

## Lo Que Hará en Esta Sesión

Bienvenido a **Lección 16-6: Registro en Resend y Configuración de Dominio**!

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear una cuenta de Resend y completar la configuración DNS (SPF, DKIM) del dominio en Vercel |
| Duración | ~30 min |
| Herramientas utilizadas | Resend CLI (`resend-cli`), Vercel Dashboard |
| Requisitos previos | El dominio debe estar administrado en Vercel |
| Página del curso | Consulte [Module 16: Automatización de Correo](https://ai-agent.camp/es/course/module-16) en paralelo |

> **Consejo**: Si ya tiene una Landing Page o sitio web desplegado en Vercel, puede usar ese dominio directamente con Resend.

---

## Paso 1: Registro de Cuenta en Resend

1. Visite [resend.com](https://resend.com) y cree una cuenta
2. Ingrese la información de la organización (nombre de empresa, dirección, etc.)
3. Complete la verificación por correo electrónico

---

## Paso 2: Instalación y Autenticación de Resend CLI

**Instalar Resend CLI:**
```bash
# Instalar con npm
npm install -g resend-cli

# O con Homebrew (Mac)
brew install resend/cli/resend
```

**Verificar instalación:**
```bash
resend --version
```

---

## Paso 3: Agregar Dominio y Configuración Automática de Vercel DNS

**Agregar dominio con Resend CLI:**
```bash
resend domains create --name su-dominio.com --region ap-northeast-1
```

**Configuración automática de DNS en Vercel Dashboard:**
1. Dashboard de Resend -> Domains -> dominio agregado -> pestaña Records
2. Haga clic en el boton "Auto configure"
3. Los registros MX, SPF, DKIM se agregaran automáticamente al DNS de Vercel

**Verificar lista de dominios con CLI:**
```bash
resend domains list
```

---

## Paso 4: Verificación del Dominio

**Ejecutar verificación del dominio con CLI:**
```bash
resend domains verify --domain-id <domain-id>
```

**Verificar estado:**
```bash
resend domains list
```

La propagación de los registros DNS puede tardar de minutos a horas. Cuando el estado sea `verified`, esta completo.

---

## Problemas Comunes y Soluciones

| Problema | Solución |
|----------|----------|
| La verificación DNS no se completa | La propagación DNS puede tardar varias horas. Re-verifique con `resend domains verify` |
| Auto configure no funciona | Verifique que el dominio esté correctamente configurado en Vercel. Agregue registros TXT/MX manualmente |
| resend CLI no encontrado | Reinstale con `npm install -g resend-cli` |

---

## Punto de Control

- [ ] Creó una cuenta de Resend
- [ ] Instaló Resend CLI y se autentico
- [ ] Agregó el dominio y configuró los registros DNS (SPF, DKIM)
- [ ] La verificación del dominio se completó (estado `verified`)

---

## Siguientes Pasos

**Configuración de AskQuestion:**
```json
{
  "title": "Leccion 16-6 completada!",
  "questions": [{
    "id": "next_action",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_lesson", "label": "Ir a Leccion 16-7 -> Creacion de clave API y primer envio"},
      {"id": "practice", "label": "Quiero verificar mas la configuracion DNS"},
      {"id": "review", "label": "Revisar la descripcion general del Module 16"},
      {"id": "end", "label": "Terminar por hoy"}
    ]
  }]
}
```
