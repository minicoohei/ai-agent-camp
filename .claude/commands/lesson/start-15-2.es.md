---
description: "When the user says /start-15-2 — Module 15 Lesson 15-2: Crear animaciones de texto estilo slide-shoot con Remotion"
chapter: "courses/aiagent/lesson03-core/module15-video"
duration: "~40 min"
prerequisites: ["setup-remotion"]
level: "intermediate"
tags: ["video", "remotion", "animation", "text", "slide-shoot"]
---

# Lección 15-2: Fundamentos de Animación con Remotion — Animación de Texto Slide-Shoot

## Objetivos de Aprendizaje

Usa `spring` / `interpolate` de Remotion para crear animaciones de texto con efecto slide-in.

| Elemento | Detalles |
|----------|---------|
| Meta | Crear videos con animación de texto estilo slide-shoot usando spring / interpolate |
| Duración | ~40 min |
| Herramientas | Remotion (React + renderizado local FFmpeg) |
| Prerequisitos | Node.js 18+, setup-remotion completado |
| Costo | **$0** (completamente local, sin APIs externas) |
| Página del curso | [Módulo 15: Generación de Video](https://ai-agent.camp/es/course/module-15) |

**Flujo de la sesión:**
1. Entender los conceptos básicos de Remotion
2. Aprender `useCurrentFrame` / `spring` / `interpolate`
3. Construir una animación de texto slide-shoot
4. Agregar efectos stagger para texto multilínea
5. Renderizar el video

---

## Paso 1: Conceptos Básicos de Remotion

Remotion es un framework para **crear videos con React**:

- **Animación basada en frames**: `useCurrentFrame()` obtiene el número de frame actual
- **spring()**: Física de resorte natural. Controla con `damping`, `mass`, `stiffness`
- **interpolate()**: Mapea números de frame a valores
- **Renderizado**: Exportación local con FFmpeg a MP4. Sin API, costo $0

```tsx
import { useCurrentFrame, spring, interpolate, useVideoConfig } from "remotion";

const frame = useCurrentFrame();
const { fps } = useVideoConfig();

const progress = spring({ frame, fps, config: { damping: 16, mass: 0.5, stiffness: 120 } });
const translateX = interpolate(progress, [0, 1], [200, 0]);
const opacity = interpolate(progress, [0, 1], [0, 1]);
```

---

## Paso 2: Crear un Texto Slide-In Básico

```
Crea un componente de texto slide-in en el directorio mv-composer.

■ Archivo: src/components/scenes/SlideShootText.tsx
■ Especificaciones:
- Fondo negro (#000000)
- Texto se desliza de derecha a izquierda con fade-in
- Spring: damping: 16, mass: 0.5, stiffness: 120
- Fuente: blanca, negrita, 60px

■ Referencia: patrón WordReveal de CinematicTextHook.tsx
```

---

## Paso 3: Agregar Efectos Stagger (Texto Multilínea)

```
Extiende SlideShootText para animación stagger multilínea.

■ Especificaciones:
- Acepta array de texto (ej: ["AI Agent Camp", "La Era del Video", "Comienza Gratis"])
- Cada línea se desliza secuencialmente (stagger: 15 frames de diferencia)
- delayFrames configurable por línea
- Última línea aparece más lento (menor stiffness)

■ Registrar en Root.tsx:
- id: "SlideShootDemo", durationInFrames: 150, fps: 30, 1920x1080
```

---

## Paso 4: Variaciones de Animación

```
Agrega variantes de dirección (prop direction):
1. "right" — deslizar desde la derecha (predeterminado)
2. "left" — deslizar desde la izquierda
3. "bottom" — deslizar hacia arriba
4. "scale" — escala 0.5 → 1.0 con fade-in central

Registrar: "SlideShoot-Right", "SlideShoot-Left", "SlideShoot-Bottom", "SlideShoot-Scale"
```

---

## Paso 5: Renderizar Videos

```bash
cd mv-composer
npx remotion render src/index.ts SlideShootDemo out/slide-shoot-demo.mp4
npx remotion render src/index.ts SlideShoot-Right out/slide-shoot-right.mp4
npx remotion render src/index.ts SlideShoot-Left out/slide-shoot-left.mp4
npx remotion render src/index.ts SlideShoot-Bottom out/slide-shoot-bottom.mp4
npx remotion render src/index.ts SlideShoot-Scale out/slide-shoot-scale.mp4
```

---

## Paso 6: Control de Calidad con /motion-review

**Después de renderizar, siempre ejecuta una revisión de calidad.**

```
/motion-review

Revisa la calidad del componente SlideShootText renderizado.

■ Objetivos:
- src/components/scenes/SlideShootText.tsx
- out/slide-shoot-demo.mp4

■ Verificar:
- Transiciones: sin frames negros, fades naturales
- Calidad de movimiento: sin artefactos de spring
- Tipografía: tamaño de fuente y legibilidad
- Calidad general
```

`/motion-review` ejecuta un checklist de 26 puntos. Los problemas se clasifican P1/P2/P3.

**Si hay problemas P1/P2**: Corregir, re-renderizar y re-verificar.

---

## Paso 7 (Avanzado): Crea Tu Propio Tema

Prueba crear un video slide-shoot original:
- Presentación personal (Nombre → Título → Mensaje)
- Producto (Servicio → Eslogan → URL)
- Evento (Fecha → Lugar → Título)

---

## Solución de Problemas

- **Studio no inicia**: Verificar Node.js ≥ 18, ejecutar `npm install`
- **Error de renderizado**: Verificar `ffmpeg -version`, confirmar id de Composition
- **Animación irregular**: Aumentar damping (14-20), reducir stiffness (100-150)
- **Fuente japonesa faltante**: Configurar fontFamily "Noto Sans JP", sans-serif

---

## ✅ Lista de Verificación
- [ ] Entendí useCurrentFrame / spring / interpolate
- [ ] El slide-in de texto único funciona
- [ ] La animación stagger multilínea funciona
- [ ] Probé las 4 variantes de dirección
- [ ] Rendericé a MP4

---

## ➡️ Próximos Pasos

```json
{
  "title": "Elige el próximo paso",
  "questions": [{
    "id": "next_step",
    "prompt": "¿Qué te gustaría hacer?",
    "options": [
      {"id": "next_auto", "label": "Iniciar siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Abrir nueva ventana (/start-15-3)"},
      {"id": "finish", "label": "Terminar aquí"}
    ]
  }]
}
```
