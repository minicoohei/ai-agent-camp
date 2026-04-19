---
name: aiagent-verify-module
description: "Habilidad para verificar el estado de completacion de modulos mediante evaluacion de IA. Se activa con solicitudes como 'verificar modulo', 'logro del modulo 1', 'verificacion de leccion completada', 'verificar progreso', etc."
version: 1.0.0
author: AI Brain Partners
dependencies: []
triggers:
  - aiagent-verify-module
  - verificar modulo
  - logro del modulo
  - verificar leccion completada
  - verificar progreso
  - verify module
  - モジュール確認
  - モジュールの達成度
---

# Verificador de Modulos de Agente de IA

Utilice esta habilidad para verificar si un estudiante ha completado exitosamente todas las lecciones de un modulo dado.

## Entradas
- Un numero de modulo (ej. `1` para Modulo 1: Generacion de Banner/Imagen)

## Flujo de Trabajo
1. Ejecutar el script de verificacion para recopilar datos factuales:
   ```bash
   uv run python tools/verify_module.py --module <N> --json
   ```
2. Analizar la salida JSON para comprender:
   - Que lecciones existen en el modulo
   - Que archivos de salida se esperaban y si existen/son validos
   - Que puntos de control define cada leccion
3. Para cada leccion con archivos de salida existentes, **leer los archivos** para evaluar la calidad.
4. Para puntos de control subjetivos (ej. "comprendio X"), pedir confirmacion al usuario.
5. Producir un informe de evaluacion estructurado:
   - **Calificacion**:
     - A: Todas las lecciones completadas + archivos de salida en formato correcto + esfuerzo creativo adicional
     - B: Todas las lecciones completadas + archivos de salida en formato correcto
     - C: Algunas lecciones incompletas pero tareas principales completadas
     - D: Tareas principales incompletas
   - **Detalles por leccion**: estado de salida, logro de puntos de control
   - **Retroalimentacion**: pasos especificos de remediacion para elementos faltantes
   - **Proximos pasos**: que lecciones repetir o a que modulo avanzar

## Referencias Requeridas
- `.cursor/commands/lesson/start-*.md` -- definiciones de lecciones con puntos de control y rutas de salida
- `tools/verify_module.py` -- script de verificacion factual
- `tools/lesson_progress.py` -- utilidades de seguimiento de progreso

## Seguridad
- Esta habilidad es de solo lectura. No modifica ningun archivo ni estado de progreso.
- Nunca simular que el usuario puede ejecutar comandos slash de Cursor directamente en Codex.

## Salida Esperada
- Tabla de resumen de completacion del modulo
- Desglose por leccion con estado de salida
- Calificacion general (A/B/C/D)
- Retroalimentacion accionable y proximos pasos
