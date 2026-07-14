---
description: "Lesson command"
chapter: "courses/aiagent/lesson03-core/module11-github-actions"
duration: "~25 min"
prerequisites: ["start-11-1"]
level: "intermediate"
tags: ["github-actions", "deploy", "artifact", "release", "vercel", "github-pages"]
nonInteractiveMode: deferred
---
# 🎓 Lesson 11-5: Despliegue y generacion de archivos con GitHub Actions

## 📍 Lo que hara en esta sesion

**Leccion 11-5: Despliegue y generacion de archivos con GitHub Actions**!

| Elemento | Contenido |
|------|------|
| Objetivo | Generar artefactos de compilacion, desplegar en GitHub Pages / Vercel y generar notas de release automaticamente con GitHub Actions |
| Duracion | ~25 min |
| Habilidades utilizadas | GitHub Actions, GitHub Pages, Vercel CLI, gh CLI |
| Requisitos previos | Leccion 11-1 completada (comprension basica de flujos de trabajo) |

**Flujo de la sesion:**
1. Script de generacion de artefactos de compilacion
2. Subida y almacenamiento como artifact
3. Despliegue en GitHub Pages
4. Despliegue automatico en Vercel
5. Generacion automatica de notas de release

Al final de esta sesion, tendra construido un pipeline automatizado de compilacion → despliegue → release.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continue" o "siga adelante" para reanudar.

---

## 🎯 Verificacion de preparacion

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
      {"id": "different_lesson", "label": "Ir a otra leccion"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Verificar que la Leccion 11-1 esta completada)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Generacion de artefactos de compilacion

```json
{
  "title": "🚀 Step 1: Generacion de artefactos",
  "questions": [{
    "id": "step_action",
    "prompt": "Crearemos un paso que genera archivos estaticos con un script Python / Node.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar los tipos de artefactos de compilacion"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `tools/build_site.py` (generador de sitio estatico simple):

```python
#!/usr/bin/env python3
"""Generador de sitio estatico simple"""
import os
import json
from datetime import datetime

def build():
    os.makedirs("dist", exist_ok=True)
    
    # Generar index.html
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>AI Agent Camp — Artefacto de compilacion</title>
  <style>
    body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
    .meta {{ color: #666; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>AI Agent Camp</h1>
  <p class="meta">Fecha de compilacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  <p>Pagina generada automaticamente con GitHub Actions.</p>
</body>
</html>"""
    
    with open("dist/index.html", "w") as f:
        f.write(html)
    
    # Generar build-info.json
    info = {
        "built_at": datetime.utcnow().isoformat(),
        "commit": os.environ.get("GITHUB_SHA", "local"),
        "ref": os.environ.get("GITHUB_REF", "local"),
    }
    with open("dist/build-info.json", "w") as f:
        json.dump(info, f, indent=2)
    
    print("Compilacion completada: artefactos generados en el directorio dist/")

if __name__ == "__main__":
    build()
```

```bash
python tools/build_site.py && ls -la dist/
```

**Resultado esperado**: Se generan `index.html` y `build-info.json` en el directorio `dist/`.

---

## 🚀 Step 2: Subida y almacenamiento de artifacts

```json
{
  "title": "🚀 Step 2: Gestion de artifacts",
  "questions": [{
    "id": "step_action",
    "prompt": "Crearemos un flujo de trabajo que almacena los artefactos de compilacion como artifacts de GitHub Actions.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar el mecanismo de artifacts"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/build-and-deploy.yml`:

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build site
        run: python tools/build_site.py

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: site-build-${{ github.run_number }}
          path: dist/
          retention-days: 30

      - name: Build summary
        run: |
          echo "## Artefactos de compilacion" >> $GITHUB_STEP_SUMMARY
          echo "| Archivo | Tamano |" >> $GITHUB_STEP_SUMMARY
          echo "|---------|-------|" >> $GITHUB_STEP_SUMMARY
          for f in dist/*; do
            SIZE=$(wc -c < "$f" | tr -d ' ')
            echo "| $(basename $f) | ${SIZE} bytes |" >> $GITHUB_STEP_SUMMARY
          done
```

**Puntos clave:**
- `actions/upload-artifact@v4` almacena los artefactos de compilacion
- `retention-days` especifica el periodo de retencion (por defecto 90 dias)
- `$GITHUB_STEP_SUMMARY` muestra la informacion de compilacion en el resumen del flujo de trabajo

**Resultado esperado**: Despues de la ejecucion del flujo de trabajo, aparece un enlace de descarga del artifact en el Summary de la pestana Actions.

---

## 🚀 Step 3: Despliegue en GitHub Pages

```json
{
  "title": "🚀 Step 3: Despliegue en GitHub Pages",
  "questions": [{
    "id": "step_action",
    "prompt": "Desplegaremos los artefactos de compilacion en GitHub Pages.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar como configurar GitHub Pages"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Agregar el job de despliegue de Pages al flujo de trabajo:

```yaml
  deploy-pages:
    needs: build
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build site
        run: python tools/build_site.py

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist/

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**Configuracion previa:**
1. Settings del repositorio → Pages
2. Source: Seleccionar "GitHub Actions"

**Resultado esperado**: El sitio se publica en `https://<owner>.github.io/<repo>/`.

---

## 🚀 Step 4: Despliegue automatico en Vercel

```json
{
  "title": "🚀 Step 4: Despliegue en Vercel",
  "questions": [{
    "id": "step_action",
    "prompt": "Desplegaremos desde GitHub Actions usando Vercel CLI.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar como configurar Vercel"},
      {"id": "skip", "label": "Omitir (usar solo GitHub Pages)"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/vercel-deploy.yml`:

```yaml
name: Vercel Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build
        run: python tools/build_site.py

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Deploy to Vercel
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
        run: |
          vercel deploy dist/ --prod --token=$VERCEL_TOKEN \
            --yes --cwd .
```

**Valores a configurar en Secrets:**
- `VERCEL_TOKEN`: Generar en el dashboard de Vercel → Settings → Tokens
- `VERCEL_ORG_ID`: Obtener de `.vercel/project.json` despues de ejecutar `vercel link`
- `VERCEL_PROJECT_ID`: Igual que el anterior

**Resultado esperado**: Cada push despliega automaticamente en Vercel y se emite una URL de preview.

---

## 🚀 Step 5: Generacion automatica de notas de release

```json
{
  "title": "🚀 Step 5: Generacion automatica de notas de release",
  "questions": [{
    "id": "step_action",
    "prompt": "Generaremos notas de release automaticamente al hacer push de un tag.",
    "options": [
      {"id": "practice", "label": "Continuar"},
      {"id": "review", "label": "Revisar el uso de gh release"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Indicaciones tras la seleccion (ejemplo)**:

Crear `.github/workflows/release.yml` (o extender uno existente):

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build
        run: python tools/build_site.py

      - name: Create release archive
        run: |
          cd dist && tar czf ../release-${{ github.ref_name }}.tar.gz .
          cd .. && zip -r release-${{ github.ref_name }}.zip dist/

      - name: Generate release notes
        run: |
          # Obtener log de commits desde el tag anterior hasta el actual
          PREV_TAG=$(git tag --sort=-creatordate | head -2 | tail -1)
          echo "## Cambios" > release_notes.md
          echo "" >> release_notes.md
          git log ${PREV_TAG}..HEAD --pretty=format:"- %s (%h)" >> release_notes.md

      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create ${{ github.ref_name }} \
            --title "Release ${{ github.ref_name }}" \
            --notes-file release_notes.md \
            release-${{ github.ref_name }}.tar.gz \
            release-${{ github.ref_name }}.zip
```

**Pasos de prueba:**
```bash
# Crear y hacer push del tag
git tag v1.0.0
git push origin v1.0.0

# Verificar el release
gh release list
```

**Resultado esperado**: Al hacer push del tag, se crea automaticamente un release con los artefactos de compilacion adjuntos.

---

## ⚠️ Problemas comunes y soluciones

```json
{
  "title": "⚠️ Solucion de problemas",
  "questions": [{
    "id": "trouble",
    "prompt": "Ha encontrado algun problema?",
    "options": [
      {"id": "trouble_1", "label": "Fallo en el despliegue de GitHub Pages"},
      {"id": "trouble_2", "label": "Error en el despliegue de Vercel"},
      {"id": "trouble_3", "label": "No se puede descargar el artifact"},
      {"id": "trouble_4", "label": "No se crea el release"}
    ]
  }]
}
```

### Problema 1: "Fallo en el despliegue de GitHub Pages"
**Causa**: El Source de Pages no esta configurado como "GitHub Actions" o faltan permisos.
**Solucion**:
```text
Verifique que en Settings → Pages → Source del repositorio esta seleccionado "GitHub Actions". Verifique que el flujo de trabajo tiene los permisos pages: write e id-token: write.
```

### Problema 2: "Error en el despliegue de Vercel"
**Causa**: `VERCEL_TOKEN` es invalido o el proyecto no esta vinculado.
**Solucion**:
```text
Ejecute vercel link localmente para vincular el proyecto. Obtenga ORG_ID y PROJECT_ID de .vercel/project.json y configurelos en Secrets.
```

### Problema 3: "No se puede descargar el artifact"
**Causa**: El periodo de `retention-days` ha expirado o la ruta esta mal especificada.
**Solucion**:
```text
Revise la salida del paso upload-artifact en los logs del flujo de trabajo. Verifique que existen archivos en el directorio especificado en path.
```

### Problema 4: "No se crea el release"
**Causa**: El formato del tag no coincide con `v*` o falta el permiso permissions: contents: write.
**Solucion**:
```text
Verifique que el formato del git tag comienza con v, como v1.0.0. Pruebe el comando gh release create localmente para ver el mensaje de error.
```

---

## ✅ Punto de control

- [ ] `tools/build_site.py` genera archivos en `dist/`
- [ ] Los artefactos se suben como artifact
- [ ] Se puede desplegar en GitHub Pages o Vercel
- [ ] El push de un tag crea automaticamente un release
- [ ] Los artefactos de compilacion estan adjuntos al release

---

## 📋 Vista previa de entregables

**Archivos creados:**
```text
tools/
└── build_site.py              # Generador de sitio estatico

.github/workflows/
├── build-and-deploy.yml       # Compilacion + Despliegue en Pages
├── vercel-deploy.yml          # Despliegue en Vercel (opcional)
└── release.yml                # Generacion automatica de notas de release

dist/                          # Artefactos de compilacion (generados en ejecucion)
├── index.html
└── build-info.json
```

---

## ➡️ Siguientes pasos

```json
{
  "title": "➡️ Siguientes pasos",
  "questions": [{
    "id": "next_step",
    "prompt": "Que desea hacer a continuacion?",
    "options": [
      {"id": "next_auto", "label": "Avanzar al Modulo 12 (Integracion con Notion) → /start-12-1"},
      {"id": "review_module", "label": "Revisar los entregables del Modulo 11"},
      {"id": "finish", "label": "Terminar por hoy"}
    ]
  }]
}
```
