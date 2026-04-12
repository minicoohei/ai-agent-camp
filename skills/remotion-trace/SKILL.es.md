---
name: remotion-trace
description: "Habilidad de flujo de trabajo para reproducir videos Remotion de calidad profesional a partir de videos de referencia. Se activa con 'Quiero recrear a partir de un video de referencia', 'Trazado de video', 'Quiero hacer un PV', 'Quiero crear un video Remotion basado en referencia'."
triggers:
  - Quiero recrear a partir de un video de referencia
  - Trazado de video
  - Quiero hacer un PV
  - Quiero crear un video Remotion
  - Crear video basado en referencia
  - remotion-trace
  - Remotion
---


# Remotion Video Trace

Habilidad de flujo de trabajo para reproducir videos Remotion de calidad profesional a partir de videos de referencia.
Una metodología establecida a través de proyectos reales de producción de PV corporativo (16 iteraciones), sistematizada en un marco reutilizable.

## Palabras clave de activación
"Quiero crear un video Remotion", "Quiero hacer un PV", "Recrear a partir de video de referencia", "Trazado de video"

## Prerrequisitos
- Node.js + Remotion (proyecto `mv-composer/` o nuevo)
- ffmpeg (extracción de fotogramas / procesamiento de audio)
- yt-dlp (descarga de videos de referencia)

---

## Parte 1: Investigación de referencia

### 1.1 Fuentes de videos de referencia

Use diferentes fuentes según el propósito:

| Fuente | URL | Propósito |
|--------|-----|-----------|
| Vimeo Staff Picks | `vimeo.com/channels/staffpicks` | Transiciones, gradación de color |
| Art of the Title | `artofthetitle.com` | Secuencias de títulos, motion graphics |
| Stash Media | `stashmedia.tv` | Tendencias de videos publicitarios/promocionales |
| YouTube | Buscar por industria/competidores | Comprender estándares de la industria para PVs corporativos |
| Trailers de juegos | Brikk etc. | Cortes dinámicos y efectos |

### 1.2 Recolección de clips

Recolecte **clips de 5-10 segundos** a nivel de "quiero la expresión de esta escena". Enfóquese en direcciones/transiciones específicas, no en videos completos.

```bash
# Descargar clips de YouTube/Vimeo
yt-dlp --download-sections "*57-59" -o "data/video_refs/{project}/{id}_%(section_start)s-%(section_end)s.%(ext)s" "https://youtube.com/watch?v={id}"

# Para Vimeo
yt-dlp --download-sections "*20-30" -o "data/video_refs/{project}/vimeo_{id}_0020-0030.%(ext)s" "https://vimeo.com/{id}"
```

### 1.3 Gestión de archivos

```
data/video_refs/{nombre_proyecto}/
├── {videoId}_{inicioSeg}-{finSeg}.mp4   # Clips de referencia
├── frames/                               # Fotogramas extraídos (generados en Parte 2)
└── README.md                            # Notas de fuente/propósito para cada clip
```

**Siempre registre las fuentes en README.md**:
```markdown
## {videoId}_{inicio}-{fin}.mp4
- Fuente: PV oficial de {Nombre de empresa} (YouTube)
- Propósito: Efecto wipe de presentación de persona (fondo oscuro → dispersión de rectángulos → revelación de foto)
```

---

## Parte 2: Análisis de fotogramas

### 2.1 Extracción de fotogramas

```bash
# Extraer fotogramas del video de referencia (6-10fps recomendado)
ffmpeg -i data/video_refs/{project}/clip.mp4 \
  -vf "fps=8" \
  data/video_refs/{project}/frames/clip_%04d.png

# Extraer solo sección específica
ffmpeg -i clip.mp4 -ss 2.0 -t 3.0 -vf "fps=10" frames/%04d.png
```

### 2.2 Lista de verificación de análisis visual

Abra los fotogramas extraídos con la herramienta Read y analice desde estas perspectivas:

- [ ] **Técnica de transición**: Wipe/fade/scale/clipPath/slide
- [ ] **Temporización y easing**: spring/ease-out/linear/escalonado
- [ ] **Expresión de texto**: Punch-in/máquina de escribir/cascada/slide-in
- [ ] **Tratamiento de fondo**: Oscurecimiento/blur/partículas/gradiente/superposición de imagen
- [ ] **Color y contraste**: Colores de marca/temperatura de color/balance luz-oscuridad
- [ ] **Diseño**: Grid/full-bleed/dividido/centrado
- [ ] **Puntos de sincronización BGM**: Cambios de corte en caídas de beat/apariciones de texto

### 2.3 Registro de resultados de análisis

Describa lo siguiente para cada clip:
```
## clip: {videoId}_{inicio}-{fin}.mp4
### Desglose de animación
- 0.0s: Fondo oscuro + rectángulos blancos dispersos en posiciones aleatorias
- 0.5s: clipPath inset hace wipe de foto de izquierda a derecha
- 1.5s: Foto en pantalla completa + subtítulo de nombre en esquina inferior izquierda (texto blanco con sombra)
- 3.0s: División en 3 tiras, cada tira muestra ángulo diferente
### Notas de implementación en Remotion
- clipPath: Lograble con `inset(0 ${100 - progress}% 0 0)`
- Dispersión de rectángulos: position:absolute + top/left/rotation aleatorios
```

---

## Parte 3: Análisis BPM y audio

### 3.1 Análisis BPM

```bash
# Extraer audio del video de referencia
ffmpeg -i reference.mp4 -vn -acodec pcm_s16le ref_audio.wav

# Conteo manual: Contar beats en 10 segundos y multiplicar por 6
ffmpeg -i ref_audio.wav -af "showinfo" -f null - 2>&1 | head -50
```

### 3.2 Diseño de duración alineada al beat

```
BPM = 103:
1 beat = 60/103 = 0.5825s
5 beats = 2.91s
9 beats = 5.24s
```

**sectionDurations siempre deben ser múltiplos enteros de la duración del beat**. Esto asegura que los beats del BGM se sincronicen naturalmente con las transiciones de escena.

### 3.3 Generación de BGM (fal.ai Stable Audio)

**Stable Audio 2.5** (recomendado): Puede generar hasta 190 segundos de una vez. Sin problemas de juntura.

```javascript
// fal.ai Stable Audio 2.5 (máximo 190 segundos)
const result = await fal.subscribe("fal-ai/stable-audio-25/text-to-audio", {
  input: { prompt: "...", seconds_total: 80 },
});
const url = result.data?.audio?.url;
```

```bash
# Aplicar fade-out al final (4 segundos) y convertir a mp3
ffmpeg -y -i raw.wav -af "afade=t=out:st=76:d=4" -q:a 2 bgm_final.mp3
```

### 3.4 Generación de narración (ElevenLabs TTS)

Flujo de trabajo establecido en TaxAccountantDemo v34-v40. Consulte el archivo fuente para detalles completos de implementación sobre generación de voz, contramedidas de contaminación de pronunciación china, evaluación de pronunciación con Gemini, ajuste de velocidad atempo e integración con Remotion.

### 3.5 Reglas de audio
- **Sin SE, impulsar con una sola pista de BGM** es el estilo básico
- Considerar cambios de tonalidad solo para videos de más de 45 segundos
- Al insertar metraje en vivo directamente, usar `muted` para prevenir interferencia con BGM
- **Videos con narración**: Bajar el volumen del BGM a 0.20-0.25 para destacar la narración
- **Alineación subtítulo-narración**: El texto de los subtítulos debe coincidir con el contenido de la narración (unificar también la notación de % para números)

---

## Parte 4: Storyboard

### 4.1 Tabla de división de escenas

Defina todas las escenas usando la siguiente plantilla antes de comenzar la implementación:

| Escena | Duración | Beats | Clip de referencia | Resumen de dirección | Nombre de componente |
|--------|----------|-------|-------------------|---------------------|---------------------|
| 01 | 2.91 | 5 | {clip_id} | Logo blur→focus + partículas | LogoFocusIn |
| 02 | 2.91 | 5 | {clip_id} | Punch-in de propuesta de valor | ValuePunch |
| 03 | 5.24 | 9 | {clip_id} | Wipe de presentación de miembros | MemberShowcase |
| ... | | | | | |

### 4.2 Diseño de interfaz Props

```typescript
interface CompositionProps {
  // Común a todas las escenas
  bgmSrc?: string;
  sectionDurations?: number[];  // Alineadas al beat

  // Props específicos de escena
  logoSrc?: string;
  // ...
}

export const DEFAULT_PROPS: CompositionProps = {
  sectionDurations: [2.91, 2.91, 5.24, 5.24, 12.23, 6.99, 8.74], // Múltiplos de BPM
  bgmSrc: '{project}/audio/bgm.mp3',
  // ...
};
```

### 4.3 Prioridad de sectionDurations

**Finalice primero el array sectionDurations** → Cada componente de escena recibe el conteo de fotogramas y distribuye internamente. El `durationInFrames` de Root.tsx se calcula automáticamente como `Math.round(sum(sectionDurations) * FPS)`.

---

## Parte 5: Patrones de implementación (Colección de técnicas Remotion)

13 técnicas establecidas a través de producción de PV corporativo. Directamente aplicables a nuevos proyectos. Consulte el archivo fuente para los patrones completos P1-P13 con ejemplos de código.

---

## Parte 6: Bucle de comparación

### 6.1 Renderizado

```bash
cd mv-composer
npx remotion render src/index.ts {CompositionId} out/{Name}_v{N}.mp4
```

### 6.2 Análisis de comparación

Coloque los fotogramas del video de referencia y los fotogramas de salida lado a lado, verificando desde la **perspectiva de un creador de video profesional**:

- [ ] Discrepancias de temporización (comparación fotograma por fotograma)
- [ ] Calidad del easing (mecánico vs. orgánico)
- [ ] Diferencias de temperatura de color/contraste
- [ ] Tamaño de texto, ubicación, legibilidad
- [ ] Recorte de imagen, relación de aspecto (recorte de rostros)
- [ ] Discrepancias en puntos de sincronización BGM
- [ ] "Fotogramas muertos" (secciones estáticas sin movimiento por 0.5s+)
- [ ] Fotogramas negros entre escenas (oscurecimientos no intencionales)
- [ ] Visualización duplicada (mismo texto/imagen apareciendo dos veces)

**Las iteraciones de v1→v18 son normales. 5-10 iteraciones es el estándar para convergencia.**

---

## Parte 7: Lecciones aprendidas (Prohibido y recomendado)

### Prohibido
| Regla | Razón |
|-------|-------|
| No usar emoji como iconos | Fuente faltante en entorno de renderizado → Usar SVG/imágenes |
| No depender de i2v (Kling/fal.ai etc.) | La calidad es mediocre, CSS de Remotion puede sustituir |
| No usar spring() para conteo | Oscila — los números suben y bajan |
| No usar objectFit "cover" para fotos de personas | Recorta rostros → "contain" + fondo borroso |
| Sin barras negras para subtítulos | Se ve mal → text-shadow para legibilidad |
| No usar imágenes de más de 7MB tal cual | Error de decodificación → `sips --resampleWidth 1200` |
| No recrear logos con texto | Desajuste de fuentes → Usar imágenes de logo |

### Recomendado
| Regla | Razón |
|-------|-------|
| Sin SE, una pista de BGM | Crea impulso dinámico |
| sectionDurations como múltiplos de BPM | Sincronización natural de beats |
| Redimensionar imágenes a 1200px de ancho o menos | Estabilidad de decodificación de Remotion |
| Superponer escenas ±5 fotogramas | Previene fotogramas negros |
| Subtítulos de nombre una vez por escena | Dos veces se siente incómodo |
| Distribuir imágenes de panel con baseOffset | Previene que todos los paneles muestren la misma imagen |
| Insertar metraje en vivo como muted | Previene interferencia con BGM |
| Obtener colores de marca del OGP/sitio oficial | La estimación visual es imprecisa |

---

## Flujo de trabajo general

```
[1. Investigación de referencia]
  ↓ Recolectar clips de referencia (unidades de 5-10 segundos)
[2. Análisis de fotogramas]
  ↓ Extraer fotogramas → Descomponer dirección
[3. BPM y audio]
  ↓ Análisis de tempo → Finalizar sectionDurations → Generar BGM
[4. Storyboard]
  ↓ Tabla de división de escenas → Diseño de Props
[5. Implementación]
  ↓ Implementar usando colección de patrones (P1-P13)
[6. Bucle de comparación]  ←─── 5-10 iteraciones
  ↓ Renderizar → Comparación de fotogramas → Corregir
[7. Verificación final]
  ↓ Verificación de lecciones aprendidas → Completar
```
