---
name: narration-qa
description: "Skill para verificar automáticamente la calidad del audio de narración generado con ElevenLabs. Se activa con solicitudes como 'verificación de narración', 'verificación de audio', 'verificación de pronunciación', etc."
triggers:
  - verificación de narración
  - verificación de audio
  - verificación de pronunciación
  - narration-qa
  - verificación de calidad de narración
  - verificación de TTS
---

# Skill de QA de Narración

Un skill para verificar automáticamente la calidad del audio de narración generado con ElevenLabs.
**Siempre siga el flujo de este skill al generar narración.**

## Disparadores

- Solicitudes de verificación de calidad después de la generación de narración
- "Verificación de narración", "Verificación de audio", "Verificación de pronunciación"
- **Todas las tareas de producción de MV que incluyan generación de narración** (aplicado automáticamente)

Para el flujo de trabajo completo incluyendo reglas de texto de entrada TTS, reglas de romanización japonesa, reglas de expansión de números, configuración de ElevenLabs, verificación de transcripción con Gemini Flash, criterios de determinación de NG, árbol de decisión del bucle de regeneración, ajuste de balance de volumen y formato de reporte de resultados de QA, consulte el SKILL.md original.
