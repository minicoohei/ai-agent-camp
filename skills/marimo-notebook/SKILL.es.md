---
name: marimo-notebook
description: "Skill para crear notebooks marimo como archivos Python en el formato correcto. Se activa con solicitudes como 'crear un notebook marimo', 'notebook interactivo', 'notebook de Python', etc."
triggers:
  - crear un notebook marimo
  - notebook interactivo
  - creación de notebook Python
  - marimo-notebook
  - marimo
  - crear un notebook
source: github.com/marimo-team/skills@main
---

## Palabras de Activación
"notebook marimo", "notebook interactivo", "notebook de Python", "marimo"

# Notas para Notebooks marimo

## Ejecución de Notebooks Marimo

```bash
# Ejecutar como script (no interactivo, para pruebas)
uv run <notebook.py>

# Ejecutar interactivamente en el navegador
uv run marimo run <notebook.py>

# Editar interactivamente
uv run marimo edit <notebook.py>
```

## Detección del Modo Script

Use `mo.app_meta().mode == "script"` para detectar CLI vs interactivo:

```python
@app.cell
def _(mo):
    is_script_mode = mo.app_meta().mode == "script"
    return (is_script_mode,)
```

## Principio Clave: Manténgalo Simple

**Muestre todos los elementos de UI siempre.** Solo cambie la fuente de datos en modo script.

- Sliders, botones y widgets siempre deben crearse y mostrarse
- En modo script, simplemente use datos sintéticos/predeterminados en lugar de esperar entrada del usuario
- No envuelva todo en condicionales `if not is_script_mode`
- No use try/except para flujo de control normal

### Patrón Correcto

```python
# Siempre mostrar el widget
@app.cell
def _(ScatterWidget, mo):
    scatter_widget = mo.ui.anywidget(ScatterWidget())
    scatter_widget
    return (scatter_widget,)

# Solo cambiar la fuente de datos según el modo
@app.cell
def _(is_script_mode, make_moons, scatter_widget, np, torch):
    if is_script_mode:
        # Usar datos sintéticos para pruebas
        X, y = make_moons(n_samples=200, noise=0.2)
        X_data = torch.tensor(X, dtype=torch.float32)
        y_data = torch.tensor(y)
        data_error = None
    else:
        # Usar datos del widget en modo interactivo
        X, y = scatter_widget.widget.data_as_X_y
        # ... procesar datos ...
    return X_data, y_data, data_error

# Siempre mostrar sliders - usar su .value en ambos modos
@app.cell
def _(mo):
    lr_slider = mo.ui.slider(start=0.001, stop=0.1, value=0.01)
    lr_slider
    return (lr_slider,)

# Ejecutar automáticamente en modo script, esperar botón en interactivo
@app.cell
def _(is_script_mode, train_button, lr_slider, run_training, X_data, y_data):
    if is_script_mode:
        # Ejecutar automáticamente con valores predeterminados del slider
        results = run_training(X_data, y_data, lr=lr_slider.value)
    else:
        # Esperar clic del botón
        if train_button.value:
            results = run_training(X_data, y_data, lr=lr_slider.value)
    return (results,)
```

## No Proteja las Celdas con Sentencias `if`

La reactividad de marimo significa que las celdas solo se ejecutan cuando sus dependencias están listas. No agregue guardas innecesarias:

```python
# MAL - la sentencia if impide que el gráfico se muestre
@app.cell
def _(plt, training_results):
    if training_results:  # INCORRECTO - no haga esto
        fig, ax = plt.subplots()
        ax.plot(training_results['losses'])
        fig
    return

# BIEN - deje que marimo maneje la dependencia
@app.cell
def _(plt, training_results):
    fig, ax = plt.subplots()
    ax.plot(training_results['losses'])
    fig
    return
```

La celda no se ejecutará hasta que `training_results` tenga un valor de todos modos.

## No Use try/except para Flujo de Control

No envuelva código en bloques try/except a menos que esté manejando una excepción específica y esperada. Deje que los errores surjan naturalmente.

```python
# MAL - ocultando errores detrás de try/except
@app.cell
def _(scatter_widget, np, torch):
    try:
        X, y = scatter_widget.widget.data_as_X_y
        X = np.array(X, dtype=np.float32)
        # ...
    except Exception as e:
        return None, None, f"Error: {e}"

# BIEN - deje que falle si algo está mal
@app.cell
def _(scatter_widget, np, torch):
    X, y = scatter_widget.widget.data_as_X_y
    X = np.array(X, dtype=np.float32)
    # ...
```

Solo use try/except cuando:
- Esté manejando un tipo de excepción específico y conocido
- La excepción sea esperada en operación normal (ej., archivo no encontrado)
- Tenga una acción de recuperación significativa

## Renderizado de Salida de Celda

Marimo solo renderiza la **expresión final** de una celda. Las expresiones indentadas o condicionales no se renderizarán:

```python
# MAL - la expresión indentada no se renderizará
@app.cell
def _(mo, condition):
    if condition:
        mo.md("¡Esto no se mostrará!")  # INCORRECTO - indentado
    return

# BIEN - la expresión final se renderiza
@app.cell
def _(mo, condition):
    result = mo.md("¡Se muestra!") if condition else mo.md("¡También se muestra!")
    result  # Esto se renderiza porque es la expresión final
    return
```

## Nomenclatura de Variables en Marimo

Las variables en bucles `for` que podrían entrar en conflicto entre celdas necesitan el prefijo de guión bajo:

```python
# Use _name, _model para hacerlas privadas de la celda
for _name, _model in items:
    ...
```

## Dependencias PEP 723

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "torch>=2.0.0",
# ]
# ///
```

## Prefiera pathlib sobre os.path

Use `pathlib.Path` para operaciones de rutas de archivo en lugar de `os.path`:

```python
# BIEN - usar pathlib
from pathlib import Path
data_dir = Path(tempfile.mkdtemp())
parquet_file = data_dir / "data.parquet"

# MAL - evitar os.path
import os
parquet_file = os.path.join(temp_dir, "data.parquet")
```


## marimo check 

Cuando trabaje en un notebook es importante verificar si el notebook puede ejecutarse. Por eso marimo proporciona un comando `check` que actúa como linter para encontrar errores comunes. 

```bash
uvx marimo check <notebook.py>
```

Asegúrese de que estos se verifiquen antes de entregar un notebook al usuario.

## Documentación de la API

Si el usuario específicamente quiere que use una función de marimo, puede verificar la documentación localmente via: 

```
uv --with marimo run python -c "import marimo as mo; help(mo.ui.form)"
```

## Recursos adicionales

- Para uso de SQL en marimo vea [SQL.md](references/SQL.md)
- Para elementos de UI en marimo [UI.md](references/UI.md)
- Para exponer funciones/clases como importaciones de nivel superior [TOP-LEVEL-IMPORTS.md](references/TOP-LEVEL-IMPORTS.md)
