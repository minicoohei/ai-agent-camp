---
description: "When the user says /start-6-2 — Module 6 Lesson 6-2: Fundamentos de creacion de skills"
chapter: "courses/aiagent/lesson03-core/module06-agent-development"
prerequisites: ["start-6-1"]
duration: "~35 min"
level: "intermediate"
tags: ["agent", "skill", "skills"]
---

# 🎓 Lesson 6-2: Fundamentos de creacion de skills

## 📍 Lo que hara en esta sesion

Bienvenido a **Lesson 6-2: Fundamentos de creacion de skills**

| Elemento | Detalles |
|----------|----------|
| Objetivo | Crear Skills reutilizables en `skills/` en un formato que pueda ser referenciado desde Codex / Claude Code / Cursor |
| Duracion | ~35 min |
| Skills utilizados | SKILL.md, Python |
| Requisitos previos | Leccion 6-1 completada, entorno Python configurado |
| Pagina del curso | [Module 6: Desarrollo de agentes](https://ai-agent.camp/es/course/module-6) en paralelo |

**Flujo de la sesion:**
1. Crear la estructura del directorio de Skills
2. Implementar SKILL.md y scripts
3. Verificar el funcionamiento y reflejar en la guia de uso

Al finalizar esta sesion, podra gestionar Skills personalizados en el directorio compartido `skills/`.

> **💡 Consejo**: Si la respuesta de la IA se detiene a mitad de camino, escriba "por favor continua" o "se detuvo" para reanudar. Este es un comportamiento de Cursor, no un error.

---

## 🎯 Verificacion de preparacion

Verifiquemos que todo esta listo.

**Configuracion de AskQuestion:**
```json
{
  "title": "🎯 Confirmación antes de iniciar la sesión",
  "questions": [{
    "id": "readiness",
    "prompt": "¿Está listo/a?",
    "options": [
      {"id": "ready", "label": "¡Listo! Comencemos"},
      {"id": "check_prereq", "label": "Quiero verificar los requisitos previos"},
      {"id": "view_html", "label": "Quiero ver primero la página del curso"},
      {"id": "different_lesson", "label": "Quiero ir a otra lección"}
    ]
  }]
}
```

(ready → Ir al Step 1)
(check_prereq → Ejecutar verificacion de requisitos previos)
(view_html → Mostrar ruta de la pagina del curso)
(different_lesson → Mostrar lista de modulos)

---

## 🚀 Step 1: Crear estructura de directorio de skill

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 1: Crear la estructura del directorio de Skills",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el directorio skills/csv-analyzer y prepare la siguiente estructura:

mkdir -p skills/csv-analyzer/scripts
mkdir -p skills/csv-analyzer/tests
mkdir -p skills/csv-analyzer/examples

touch skills/csv-analyzer/SKILL.md
touch skills/csv-analyzer/requirements.txt

Verifique la estructura de directorios.
```

**Resultado esperado**: Se crea la estructura del directorio de Skills.

---

## 🚀 Step 2: Crear documento SKILL.md

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 2: Crear documento SKILL.md",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo skills/csv-analyzer/SKILL.md con el siguiente contenido:

---
name: csv-analyzer
description: Un Skill que analiza archivos CSV y proporciona estadisticas e inferencia de tipos de datos
version: 1.0.0
author: nombre-de-usuario
dependencies:
  - python: "3.8+"
  - packages: ["pandas", "chardet"]
---

# CSV Analyzer Skill

## Descripcion general
Un Skill que analiza archivos CSV y proporciona estadisticas e inferencia de tipos de datos.

## Funciones
- Obtener numero de filas y columnas
- Inferencia de tipos de datos (deteccion automatica del tipo de cada columna)
- Estadisticas (estadisticas basicas para columnas numericas)
- Deteccion de valores faltantes (deteccion de valores NULL y NA)
- Deteccion de codificacion

## Modo de uso

### Ejecucion en linea de comandos
```bash
python skills/csv-analyzer/scripts/analyzer.py --input data.csv
```

### Uso en Python
```python
from scripts.analyzer import CSVAnalyzer

analyzer = CSVAnalyzer('data.csv')
result = analyzer.analyze()
print(result)
```

## Formato de salida
```json
{
  "filename": "data.csv",
  "rows": 1000,
  "columns": 5,
  "encoding": "utf-8",
  "file_size_mb": 2.5,
  "columns_info": []
}
```

## Dependencias
- pandas >= 2.0
- chardet >= 5.0

## Instalacion
```bash
pip install -r requirements.txt
```
```

**Resultado esperado**: Se crea el documento SKILL.md.

---

## 🚀 Step 3: Crear implementacion en Python

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 3: Crear implementación en Python",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo skills/csv-analyzer/scripts/analyzer.py con el siguiente contenido:

import pandas as pd
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List

class CSVAnalyzer:
    """Clase para analizar archivos CSV"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def analyze(self) -> Dict[str, Any]:
        """Analizar archivo CSV"""
        df = pd.read_csv(self.file_path)
        file_size_mb = self.file_path.stat().st_size / (1024 * 1024)

        return {
            "filename": self.file_path.name,
            "rows": len(df),
            "columns": len(df.columns),
            "file_size_mb": round(file_size_mb, 2),
            "columns_info": self._analyze_columns(df)
        }

    def _analyze_columns(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Analizar cada columna"""
        columns_info = []
        for col in df.columns:
            col_data = df[col]
            col_info = {
                "name": col,
                "type": str(col_data.dtype),
                "null_count": int(col_data.isna().sum()),
                "unique_values": int(col_data.nunique())
            }

            # Agregar estadisticas para columnas numericas
            if pd.api.types.is_numeric_dtype(col_data):
                col_info["stats"] = {
                    "min": float(col_data.min()) if not col_data.isna().all() else None,
                    "max": float(col_data.max()) if not col_data.isna().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isna().all() else None
                }

            columns_info.append(col_info)
        return columns_info

    def to_json(self, output_path: str = None) -> str:
        """Exportar resultados del analisis en formato JSON"""
        result = self.analyze()
        json_str = json.dumps(result, indent=2, ensure_ascii=False)

        if output_path:
            Path(output_path).write_text(json_str, encoding='utf-8')

        return json_str

def main():
    parser = argparse.ArgumentParser(description="Analizar archivos CSV")
    parser.add_argument("--input", required=True, help="Ruta del archivo CSV de entrada")
    parser.add_argument("--output", help="Ruta del archivo JSON de salida (se imprime en stdout si se omite)")
    args = parser.parse_args()

    analyzer = CSVAnalyzer(args.input)
    result = analyzer.to_json(args.output)

    if not args.output:
        print(result)

if __name__ == "__main__":
    main()
```

**Resultado esperado**: Se implementa la clase CSVAnalyzer.

---

## 🚀 Step 4: Crear requirements.txt

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 4: Crear requirements.txt",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo skills/csv-analyzer/requirements.txt con el siguiente contenido:

pandas>=2.0.0
chardet>=5.0.0
pytest>=7.4.0
```

**Resultado esperado**: Se crea el archivo de dependencias.

---

## 🚀 Step 5: Crear y ejecutar pruebas

Use AskUserQuestion (AskQuestion) para elegir "Continuar / Solo revisar ejemplos / Omitir."

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "🚀 Step 5: Crear y ejecutar pruebas",
  "questions": [{
    "id": "step_action",
    "prompt": "¿Qué desea hacer con este paso?",
    "options": [
      {"id": "practice", "label": "Continuar tal cual"},
      {"id": "review", "label": "Solo revisar ejemplos"},
      {"id": "skip", "label": "Omitir"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
Entrada:
```
Cree el archivo skills/csv-analyzer/tests/test_analyzer.py con el siguiente contenido:

import pytest
import pandas as pd
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.analyzer import CSVAnalyzer

@pytest.fixture
def sample_csv():
    """Crear un archivo CSV de muestra para pruebas"""
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, None, 28],
        'score': [85.5, 90.0, 78.5, 82.0, 88.5]
    })
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.csv', delete=False, encoding='utf-8'
    ) as f:
        df.to_csv(f, index=False)
        return f.name

def test_analyze_basic(sample_csv):
    """Prueba de analisis basico"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    assert result['rows'] == 5
    assert result['columns'] == 4
    assert 'columns_info' in result

def test_column_types(sample_csv):
    """Prueba de analisis de tipos de columna"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    col_names = [col['name'] for col in result['columns_info']]
    assert 'id' in col_names
    assert 'name' in col_names

def test_null_detection(sample_csv):
    """Prueba de deteccion de valores faltantes"""
    analyzer = CSVAnalyzer(sample_csv)
    result = analyzer.analyze()

    age_col = next(col for col in result['columns_info'] if col['name'] == 'age')
    assert age_col['null_count'] == 1

def test_file_not_found():
    """Prueba de error de archivo no encontrado"""
    with pytest.raises(FileNotFoundError):
        CSVAnalyzer('nonexistent.csv')

Luego, ejecute las pruebas con el siguiente comando:
cd skills/csv-analyzer && pip install -r requirements.txt && pytest tests/ -v
```

**Resultado esperado**: Se crean pruebas y todas las pruebas pasan.

---

## ⚠️ Problemas comunes y soluciones

Use AskUserQuestion (AskQuestion) para seleccionar su problema y recibir asistencia guiada.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el problema",
  "questions": [{
    "id": "trouble",
    "prompt": "Seleccione la opción que corresponda",
    "options": [
      {"id": "trouble_1", "label": "No se puede importar el módulo"},
      {"id": "trouble_2", "label": "pandas no está instalado"},
      {"id": "trouble_3", "label": "Las pruebas fallan"},
      {"id": "trouble_4", "label": "La salida JSON tiene problemas de codificación"}
    ]
  }]
}
```


### Problema 1: "No se puede importar el modulo"
**Causa**: La ruta de Python no esta configurada
**Prompt de solucion**:
```
Agregue el directorio del script a sys.path:
sys.path.insert(0, str(Path(__file__).parent.parent))
O configure la variable de entorno PYTHONPATH.
```

### Problema 2: "pandas no esta instalado"
**Causa**: Paquetes de dependencia no instalados
**Prompt de solucion**:
```
Ejecute pip install -r requirements.txt.
Si usa un entorno virtual, verifique que el entorno correcto esté activo.
```

### Problema 3: "Las pruebas fallan"
**Causa**: La ruta del archivo de prueba es incorrecta
**Prompt de solucion**:
```
Verifique el directorio desde el cual está ejecutando pytest.
Verifique que los archivos de prueba estén en el directorio tests/.
```

### Problema 4: "La salida JSON tiene problemas de codificacion"
**Causa**: La codificacion no es UTF-8
**Prompt de solucion**:
```
Especifique ensure_ascii=False en json.dumps().
Especifique encoding='utf-8' al escribir en archivos.
```

---

## ✅ Punto de control
- [ ] La estructura del directorio esta creada
- [ ] Documentado con SKILL.md
- [ ] analyzer.py esta implementado
- [ ] requirements.txt esta creado
- [ ] Todas las pruebas pasan


---

## 📋 Vista previa de resultados

### Salida esperada
```
📁 output/
└── {nombre-del-proyecto}/  (artefactos de agente/código)
```

### Comandos de verificacion
```bash
# Verificar existencia y tamano del archivo
ls -lh output/{nombre-del-proyecto}/

# Verificar el inicio (primeras 30 lineas)
head -30 output/{nombre-del-proyecto}/
```

> 💡 Ver texto completo: `cat output/{nombre-del-proyecto}/` para mostrar el texto completo

---

## ✅ Verificacion de finalizacion
Pegue lo siguiente en el chat de Cursor para verificar la finalizacion:

```
# Verificacion de finalizacion: confirme que el directorio skills/csv-analyzer/ se haya creado correctamente y que todas las pruebas de pytest pasen.
```

**Resultado esperado**: Se muestra un juicio de aprobado/no aprobado y los elementos faltantes.

---

## ➡️ Siguientes pasos

Esta seccion esta completa. Inicie la siguiente seccion o abra una nueva ventana para comenzar una nueva seccion.

Use AskUserQuestion (AskQuestion) para elegir.

**Ejemplo de configuracion de AskQuestion:**
```json
{
  "title": "Seleccione el siguiente paso",
  "questions": [{
    "id": "next_step",
    "prompt": "Seleccione la siguiente acción",
    "options": [
      {"id": "next_auto", "label": "Iniciar la siguiente sección (/next_lesson)"},
      {"id": "next_window", "label": "Iniciar en nueva ventana (/start-6-3)"},
      {"id": "finish", "label": "Finalizar aquí"}
    ]
  }]
}
```

**Despues de la seleccion (ejemplo)**:
- next_auto → /next_lesson
- next_window → Abrir nueva ventana con /start-6-3
- finish → Finalizar
