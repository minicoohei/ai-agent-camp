---
name: jupyter-to-marimo
description: "Habilidad para convertir cuadernos Jupyter (.ipynb) a cuadernos marimo (.py). Se activa con solicitudes como 'convertir Jupyter,' 'ipynb a marimo,' 'conversión de cuadernos,' etc."
source: github.com/marimo-team/skills@main
triggers:
  - jupyter-to-marimo
  - Jupyter変換
  - ipynb変換
  - marimoに変換
  - ノートブック変換
  - marimo convert
---

## Palabras Clave de Activación
"Conversión de Jupyter," "conversión de ipynb," "convertir a marimo," "conversión de cuadernos"

# Conversión de Cuadernos Jupyter a Marimo

**IMPORTANTE**: Cuando se le pida traducir un cuaderno, SIEMPRE ejecute `uvx marimo convert <notebook.ipynb> -o <notebook.py>` PRIMERO antes de leer cualquier archivo. Esto ahorra tokens valiosos - leer cuadernos grandes puede consumir más de 30k tokens, mientras que el archivo .py convertido es mucho más pequeño y fácil de trabajar.

## Pasos

1. **Convertir usando la CLI**

Ejecute el comando marimo convert mediante `uvx` para que no sea necesaria la instalación:

```bash
uvx marimo convert <notebook.ipynb> -o <notebook.py>
```

Esto genera un archivo `.py` compatible con marimo a partir del cuaderno Jupyter.

2. **Ejecutar `marimo check` en la salida**

```bash
uvx marimo check <notebook.py>
```

Corrija cualquier problema reportado antes de continuar.

3. **Revisar y limpiar el cuaderno convertido**

Lea el archivo `.py` generado y aplique las siguientes mejoras:

- Asegúrese de que el bloque de metadatos del script liste todos los paquetes requeridos. El convertidor puede omitir algunos.
- Elimine artefactos residuales de Jupyter como llamadas a `display()`, o comandos `%magic` que no aplican en marimo.
- Asegúrese de que la expresión final de cada celda sea el valor a renderizar. Las expresiones con sangría o condicionales no se mostrarán.
- Si el cuaderno original requiere variables de entorno mediante una entrada, considere agregar el widget `EnvConfig` de wigglystuff. Los detalles se pueden encontrar [aquí](https://koaning.github.io/wigglystuff/reference/env-config.md).
- Si el cuaderno original usa ipywidgets, reemplácelos con la interfaz de usuario correspondiente de marimo. Un slider, por ejemplo, se reemplazaría con `mo.ui.slider()`.

4. **Ejecute `marimo check` nuevamente** después de sus ediciones para confirmar que nada se haya roto.
