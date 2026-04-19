---
name: motion-review
description: "Revisa la calidad de composiciones Remotion con una lista de verificación de 20 elementos. Se activa con solicitudes como 'revisión de video', 'motion review', 'verificación de calidad Remotion', etc."
triggers:
  - revisión de video
  - verificación de calidad de video
  - motion review
  - motion-review
  - verificación de calidad Remotion
  - revisión de PV
  - video review
---

# Skill de Revisión de Motion

Un skill que revisa composiciones Remotion desde la perspectiva de un creador de video profesional y proporciona instrucciones de mejora de calidad.
Se invoca automáticamente en el paso de Revisión de Calidad del GTM Manager / Campaign Orchestrator.

## Palabras de Activación

`motion review`, `video review`, `revisión de video`, `revisión de PV`, `verificación de calidad Remotion`

## Entrada

- Ruta al archivo de composición Remotion (`.tsx`)
- (Opcional) Ruta al mp4 renderizado

## Flujo de Ejecución

```
1. Leer composición .tsx
2. Ejecutar lista de verificación de 26 puntos (categorías A-I abajo)
3. Generar revisión estructurada con calificaciones P1/P2/P3
4. Si existe algún P1 -> VEREDICTO: CORRECCIÓN_REQUERIDA
5. Si solo P2 -> VEREDICTO: CORRECCIÓN_RECOMENDADA
6. Si solo P3 -> VEREDICTO: APROBADO
```

## Tono (Estilo de Salida de Revisión)

- Use el tono de "un director de video profesional haciendo una verificación final antes de la entrega"
- Cada elemento de verificación se formatea como "OK -- razón" o "P1/P2/P3 -- estado actual -> instrucción de corrección". Sin impresiones subjetivas ni adjetivos vagos
- Reconozca 1-2 puntos positivos antes de listar problemas
- Las instrucciones de corrección deben incluir el conjunto de 3 puntos: "nombre de archivo:número de línea + código actual + código corregido"

## Criterios de Decisión de Compensaciones

- Corregir todos los P1 > corregir muchos P2 (incluso un P1 significa CORRECCIÓN_REQUERIDA)
- Estasis confiable con interpolate > spring visualmente atractivo con riesgo de oscilación
- Dividir escenas para reducir densidad de información > comprimir en una escena para ahorrar duración
- OVERLAP más grande (12f) para margen de seguridad > mínimo (4f) para extender duración de escena

---

## Lista de Verificación Pro de 26 Puntos

### Categoría A: Transiciones

#### A1. Fotogramas Negros Entre Escenas [P1]
**Verificar**: ¿La Secuencia se superpone por OVERLAP fotogramas?
- NG: Secuencia sin superposición
- OK: `from={starts[i] - OVERLAP}`, `durationInFrames={frames[i] + OVERLAP * 2}`
- **Criterio**: P1 si aparecen 2+ fotogramas negros

#### A1.5. Transición Crossfade + Zoom [P1]
**Verificar**: ¿Las fases están conectadas suavemente con CrossFadeWrap (fade de opacidad + escala sutil)?

#### A2. Diversidad de Métodos de Transición [P2]
**Verificar**: ¿Todas las escenas usan el mismo patrón de entrada/salida?
- OK si existen 3+ métodos de transición diferentes

#### A3. Continuidad de clipPath [P2]

---

### Categoría B: Calidad de Movimiento

#### B1. Diferenciación de Perfiles Spring [P1]
**Verificar**: ¿Se usan diferentes configuraciones spring según el peso del elemento?
- NG: Todos los elementos usan el mismo config
- OK: Al menos 4 niveles (snappy / balanced / weighty / liquid) diferenciados
- **Criterio**: P1 si hay 2 o menos variantes

#### B2. Movimiento Secundario [P2]
#### B3. Sincronización BPM [P2]

---

### Categoría C: Pulido Visual

#### C1. Animación de Film Grain [P1]
**Verificar**: ¿El Film Grain cambia en cada fotograma?
- **Criterio**: P1 si existe Film Grain con seed fijo (eliminar o corregir)

#### C2. Ken Burns de Fondo [P2]
#### C3. Vignette + Grain + ScanLines [P3]

---

### Categoría D: Tipografía

#### D1. Legibilidad del Tamaño de Fuente [P1]
**Verificar**: ¿El texto más pequeño es legible en video 1080p?
- **Criterio**: P1 si algún texto del cuerpo está por debajo de 18px

#### D2. Configuración Base de Tipografía [P3]

---

### Categoría E: Color y Diseño

#### E1. Cambio de Temperatura de Color [P3]
#### E2. Asimetría del Diseño [P2]

---

### Categoría F: Integridad de Contenido y Temporización

#### F1. Cálculo de Fotogramas de Animación de Escritura [P1]
#### F2. Desenfoque por Renderizado Sub-píxel [P1]
#### F3. Legibilidad de Texto sobre Fondos [P1]
#### F4. Transparencia de Logo/Imagen e Interferencia de Fondo [P2]
#### F5. Alineación de Rango de Scroll y Volumen de Contenido [P2]
#### F6. Stagger de Tarjetas Excediendo Duración de Sección [P1]
#### F7. Desajuste entre Duración de BGM y Duración de Video [P2]
#### F8. Consistencia de Etiquetas/Encabezados [P2]

---

### Categoría G: Calidad de Implementación de Producción

#### G1. Fallo de Sobreescritura de Valores Predeterminados con --props [P1]
#### G2. Reversión de Archivos por Linter/Herramientas Externas [P1]
#### G3. Desbordamiento de Pantalla en Zoom de Enfoque [P1]
#### G4. Tiempo de Visualización Insuficiente de Subtítulos [P2]
#### G5. Tamaños de Fuente Inconsistentes en Subtítulos [P2]
#### G6. Residuo de Texto en Límites de Escena [P2]
#### G7. Desajuste entre Cantidad de Fotos y Diseño [P2]
#### G8. Diferenciación de Prompts para Generación de BGM [P3]
#### G9. Selección de Visualización Permanente vs Secuencial [P3]

---

### Categoría H: Calidad de Contenido

#### H9. Consistencia de Color de UI de Claude Code [P1]
**Verificar**: ¿La representación de UI de Claude Code usa negro (oficial) en lugar de púrpura (estilo Cursor)?

#### H10. Consistencia de Iconos de Marca [P2]
#### H11. Alineación Central de Diagramas SVG [P2]

Para detalles completos sobre cada elemento de verificación, consulte el SKILL.md original que contiene ejemplos de código de implementación y patrones de corrección para cada elemento.
