---
description: Obtener los materiales más recientes del repositorio de origen (upstream)
---

# Actualizar materiales del curso a la última versión

## Uso
```
/update-material
```

## Descripción general
Incorpora los últimos cambios de materiales del curso desde el repositorio original (minicoohei/ai-agent-camp) a su repositorio personal (ej.: su propio ai-agent-camp en GitHub) creado mediante Import o clone + push.

## Pasos de ejecución

Ejecute lo siguiente en orden.

### 1. Verificar el remote upstream
```bash
git remote -v
```
Si `upstream` no aparece, agréguelo en el siguiente paso.

### 2. Agregar upstream (solo si no está configurado)
```bash
git remote add upstream https://github.com/minicoohei/ai-agent-camp.git
```
Omita este paso si `upstream` ya existe.

### 3. Obtener lo más reciente
```bash
git fetch upstream
```

### 4. Fusionar en la rama actual
```bash
# Verificar la rama actual (generalmente main)
git branch --show-current

# Incorporar el main de upstream
git merge upstream/main
```
Si su rama se llama `master`, usar `git merge upstream/main` sigue siendo correcto (upstream utiliza main).

## Si ocurren conflictos
Los conflictos pueden ocurrir cuando los archivos que ha modificado también fueron actualizados en el repositorio original. En ese caso, proporcione la siguiente orientación.

- Abra los archivos en conflicto en su editor, revise los marcadores `<<<<<<<` / `=======` / `>>>>>>>` y resuelva manualmente
- Después de la resolución: `git add <archivo>` -> `git commit` para completar la fusión
- Si la resolución es difícil, puede respaldar el archivo y usar `git checkout --theirs -- <ruta>` para adoptar la versión de upstream

## Notas
- **Destinatario**: Esto es para repositorios que copió para uso personal (Import / clone+push). También funciona para forks.
- **Seguridad**: Nunca se ejecuta `git push --force`. Solo se realiza la fusión; envíe al remoto con `git push origin main` según sea necesario.
