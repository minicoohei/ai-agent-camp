---
description: "When the user says /start-13-2 — Module 13 Lesson 13-2: Diseño de Landing Page - Creación de wireframe"
chapter: "courses/aiagent/lesson03-core/module13-lp/chapter.yaml"
prerequisites: ["start-13-1"]
duration: "~25 min"
level: "intermediate"
tags: ["lp", "wireframe", "design", "information-architecture"]
---

# 🎓 Lección 13-2: Creación de wireframe (ASCII + WF visual)

## 📍 Lo que hará en está sesión

Bienvenido a **Lección 13-2: Creación de wireframe**.

| Elemento | Detalles |
|----------|----------|
| Objetivo | Diseñar la estructura de secciones de la Landing Page/sitio web usando WF ASCII y WF visual |
| Duración | ~25 min |
| Habilidades utilizadas | lp-designer, diagram-generator |
| Requisitos previos | Lección 13-1 completada (output/lp-brief.md existe) |
| Página del curso | Consulte [Módulo 13: Diseño de Landing Page/Sitio web](https://ai-agent.camp/es/course/module-13) en paralelo |

**Flujo de la sesión:**
1. Carga del brief y confirmación de secciones
2. Creación del wireframe ASCII
3. Generación de WF visual con diagram-generator
4. Revisión del diseño de información entre secciones

Al finalizar la sesión, el diseño estructural de la Landing Page estará completó.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continúe" o "se detuvo" para reanudar. Las respuestas pueden pausarse dependiendo de la herramienta, pero no es un error.

---

## 🎯 Verificación de preparación

Primero, confirmemos que todo está listo.

**Configuración de AskQuestion:**
```json
{
  "title": "🎯 Verificación previa a la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver la página del curso primero"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Paso 1)
(check_prereq → Verificar existencia de output/lp-brief.md)
(view_html → Mostrar la ruta de la página del curso)
(different_lesson → Mostrar lista de módulos)

---

## 🚀 Paso 1: Carga del brief

Revisar el brief creado en 13-1.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 1: Carga del brief",
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

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Cargue output/lp-brief.md y verifique lo siguiente:

1. ¿La estructura de secciones es clara?
2. ¿El contenido necesario está definido para cada sección?
3. ¿El flujo lógico entre secciones es apropiado?

Muestre los resultados de verificación como un resumen.
```

**Resultado esperado**: El contenido del brief se muestra cómo un resumen.

---

## 🚀 Paso 2: Creación del wireframe ASCII

Diseñar la estructura de la Landing Page usando wireframes basados en texto.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 2: Wireframe ASCII",
  "questions": [{
    "id": "wf_style",
    "prompt": "Seleccione el estilo de wireframe",
    "options": [
      {"id": "single_column", "label": "Columna única (para Landing Pages simples)"},
      {"id": "two_column", "label": "Diseño de 2 columnas (texto + imagen en paralelo)"},
      {"id": "card_grid", "label": "Cuadrícula de tarjetas (para presentación de características)"},
      {"id": "full_width", "label": "Ancho completo (enfocado en impacto)"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Cree un wireframe ASCII basado en la estructura de secciones de output/lp-brief.md.

Formato:
- Use caracteres de dibujo de cajas (┌─┐│└─┘)
- Represente visualmente las proporciones de ancho/alto de cada sección
- Muestre la ubicación de texto, imágenes y botones con [ ]
- Incluya los cambios de diseño responsive

Salida en: output/lp-wireframe.txt

Incluya las siguientes secciones:
1. Header / Navegación
2. Sección Hero
3. Sección Pain Points
4. Sección Solution
5. Sección Features
6. Sección Social Proof
7. Sección FAQ
8. Sección Final CTA
9. Footer
```

**Resultado esperado**: El wireframe ASCII se guarda en `output/lp-wireframe.txt`.

---

## 🚀 Paso 3: Generación de WF visual (diagram-generator)

Usar diagram-generator para crear un wireframe visual.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 3: Generación de WF visual",
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

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Genere un wireframe visual a partir del WF ASCII de output/lp-wireframe.txt
usando diagram-generator.

Comando de ejecución:
uv run python tools/generate_diagram.py --topic "Wireframe de LP: diagrama de composición Hero→PainPoints→Solution→Features→SocialProof→FAQ→CTA. Ilustrar la ubicación y elementos de contenido de cada sección" --style minimalist

Salida en: output/images/lp-wireframe.png

Después de la generación, verifique que la estructura de secciones sea correcta.
```

**Resultado esperado**: Se genera un WF visual en `output/images/lp-wireframe.png`.

---

## 🚀 Paso 4: Revisión del diseño de información

Revisar el diseño de información del WF generado y verificar mejoras.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "🚀 Paso 4: Revisión del diseño de información",
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

**Instrucciones posteriores a la selección (ejemplo)**:
Entrada:
```text
Revise el WF creado (output/lp-wireframe.txt y output/images/lp-wireframe.png),
y proporcione sugerencias de mejora desde las siguientes perspectivas:

## Criterios de revisión
1. **Flujo narrativo**: ¿El flujo de problema → solución → evidencia → acción es natural?
2. **Ubicación del CTA**: ¿Hay suficientes CTAs en la primera vista y al final?
3. **Balance de información**: ¿La cantidad de información en cada sección es apropiada (demasiada/poca)?
4. **Escaneabilidad**: ¿Se pueden captar los puntos clave al leer rápidamente?
5. **Soporte móvil**: ¿Hay problemas con el diseño para móviles?

Si se necesitan mejoras, actualice output/lp-wireframe.txt.
```

**Resultado esperado**: Los resultados de la revisión y el WF mejorado están completos.

---

## ⚠️ Problemas comunes y soluciones

En Codex, normalmente se presentan opciones en el chat para que el usuario seleccione su problema y reciba orientación al instante.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione su problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione el problema que aplica",
    "options": [
      {"id": "trouble_1", "label": "No se encuentra el archivo del brief"},
      {"id": "trouble_2", "label": "diagram-generator da error"},
      {"id": "trouble_3", "label": "El diseño del WF está roto"},
      {"id": "trouble_4", "label": "No estoy seguro de la estructura de secciones"}
    ]
  }]
}
```

### Problema 1: No se encuentra el archivo del brief
**Solución**: Cree un brief con `/start-13-1`, o genere uno con contenido ficticio.

### Problema 2: diagram-generator da error
**Solución**: Verifique si `GEMINI_API_KEY` está configurada (`echo $GEMINI_API_KEY`).

### Problema 3: El diseño del WF está roto
**Solución**: Asegúrese de que se muestre con una fuente monoespaciada. Se recomienda verlo en la terminal de Cursor.

### Problema 4: No estoy seguro de la estructura de secciones
**Solución**: Use la plantilla básica (Hero → Pain → Solution → Features → Proof → CTA), luego elimine secciones innecesarias después.

---

## ✅ Punto de control
- [ ] El brief ha sido cargado
- [ ] El WF ASCII está guardado en `output/lp-wireframe.txt`
- [ ] El WF visual está generado en `output/images/lp-wireframe.png`
- [ ] La revisión del diseño de información está completa
- [ ] El flujo entre secciones es lógico


---

## 📋 Vista previa de entregables

### Salida esperada
```text
📁 output/lp/
├── index.html  (Landing Page)
├── style.css
└── assets/
```

### Comandos de verificación
```bash
# Lista de archivos
ls -lh output/lp/

# Abrir en el navegador (macOS: open / Linux: xdg-open)
open output/lp/index.html
```

> 💡 Verificar estructura HTML: `head -30 output/lp/index.html`

---

## ✅ Verificación de finalización
Ingrese lo siguiente en el chat de Codex para verificar la finalización:

```text
Verifique si output/lp-wireframe.txt y output/images/lp-wireframe.png existen,
y muestre un resumen de la estructura de secciones.
```

**Resultado esperado**: Se muestra la verificación de existencia de archivos WF y el resumen de la estructura.

---

## ➡️ Siguientes pasos

Esta sección está completa. A continuación, configure Pencil MCP y proceda a la creación del archivo de diseño.

En Codex, normalmente puede seleccionar entre opciones en el chat.

**Ejemplo de configuración de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione qué hacer a continuación",
    "options": [
      {"id": "setup_pencil", "label": "Iniciar configuración de Pencil (/setup-pencil)"},
      {"id": "skip_pencil", "label": "Pencil ya configurado → Ir a creación de diseño (/start-13-3)"},
      {"id": "next_window", "label": "Abrir /setup-pencil en una nueva ventana"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```

**Instrucciones posteriores a la selección (ejemplo)**:
- setup_pencil → Ejecutar /setup-pencil (si Pencil no está instalado)
- skip_pencil → Ejecutar /start-13-3 (si Pencil ya está instalado)
- next_window → Abrir /setup-pencil en una nueva ventana
- finish → Finalizar
