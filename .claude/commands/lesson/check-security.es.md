---
description: "Lesson command"
nonInteractiveMode: compliant
---
# Verificación de configuración de seguridad

## Uso
```
/check-security
```

## Proceso
Verificar la configuración de seguridad del proyecto y detectar riesgos potenciales.

## Elementos de verificación

### 1. Verificación de filtración de información confidencial
```bash
# Verificar si los archivos .env estan rastreados por Git
git ls-files | grep -E "\.env$|\.env\." && echo "WARNING: .env files tracked!"

# Verificar .gitignore
cat .gitignore | grep -E "\.env|secret|credential|\.key"

# Escanear credenciales codificadas directamente
grep -rn "password\s*=\s*['\"]" --include="*.py" --include="*.js" .
grep -rn "api_key\s*=\s*['\"]" --include="*.py" --include="*.js" .
grep -rn "secret\s*=\s*['\"]" --include="*.py" --include="*.js" .
```

### 2. Vulnerabilidades de dependencias
```bash
# Python
pip-audit 2>/dev/null || echo "pip-audit no instalado"

# Node.js
npm audit 2>/dev/null || echo "Sin package.json"

# GitHub Dependabot
gh api repos/{owner}/{repo}/vulnerability-alerts 2>/dev/null
```

### 3. Configuración de autenticación
```bash
# Verificar permisos de claves SSH
ls -la ~/.ssh/*.pub 2>/dev/null
ls -la ~/.ssh/id_* 2>/dev/null | head -5

# Configuracion de firma GPG
git config --get user.signingkey

# Estado de 2FA
gh auth status 2>/dev/null | grep -i "two-factor"
```

### 4. Gestión de claves API
```bash
# Verificar variables de entorno (enmascarar valores)
env | grep -iE "(api_key|token|secret|password|credential)" | sed 's/=.*/=***/'

# Verificar existencia del archivo .env
ls -la .env* 2>/dev/null
```

### 5. Configuración del repositorio de GitHub
```bash
# Proteccion de ramas
gh api repos/{owner}/{repo}/branches/main/protection 2>/dev/null

# Escaneo de secretos
gh api repos/{owner}/{repo}/secret-scanning/alerts 2>/dev/null
```

## Formato de salida

```markdown
## Informe de verificacion de seguridad

### Resumen
- Problemas criticos: X
- Advertencias: X
- Informativos: X

### Detalles

#### Riesgo de filtracion de informacion confidencial
| Elemento de verificacion | Estado | Detalles |
|--------------------------|--------|----------|
| Rastreo de .env en Git | OK/NG | ... |
| Credenciales codificadas directamente | OK/NG | ... |
| Configuracion de .gitignore | OK/NG | ... |

#### Vulnerabilidades de dependencias
| Paquete | Gravedad | Accion |
|---------|----------|--------|
| package-a | Alta | Actualizacion recomendada |
| package-b | Media | Actualizacion recomendada |

#### Configuracion de autenticacion
| Elemento | Estado | Recomendacion |
|----------|--------|---------------|
| Permisos de clave SSH | OK/NG | Configurar a 600 |
| Firma GPG | OK/NG | Habilitar recomendado |
| 2FA | OK/NG | Habilitar recomendado |

### Acciones recomendadas
1. [Critico] ...
2. [Advertencia] ...
3. [Informativo] ...
```

## Lista de verificación

### Obligatorio
- [ ] El archivo .env está incluido en .gitignore
- [ ] No hay credenciales codificadas directamente
- [ ] Los permisos de clave SSH son apropiados (600)
- [ ] No hay vulnerabilidades en dependencias

### Recomendado
- [ ] Firma GPG habilitada
- [ ] 2FA habilitado
- [ ] Protección de ramas configurada
- [ ] Escaneo de secretos habilitado
- [ ] Dependabot habilitado

### Verificaciones periódicas
- [ ] Semanal: Escaneo de vulnerabilidades de dependencias
- [ ] Mensual: Rotación de credenciales
- [ ] Trimestral: Revisión de configuración de seguridad

## Mejores prácticas de seguridad

### 1. Gestión de credenciales
```python
# Mal ejemplo
API_KEY = "sk-1234567890abcdef"

# Buen ejemplo
import os
API_KEY = os.environ.get("API_KEY")
```

### 2. Configuración de .gitignore
```gitignore
# Variables de entorno
.env
.env.local
.env.*.local

# Credenciales
*.pem
*.key
credentials.json
service-account.json

# Configuracion de IDE (puede contener informacion confidencial)
.idea/
.vscode/settings.json
```

### 3. Gestión de variables de entorno
```bash
# Desarrollo: .env + dotenv
# Produccion: variables de entorno o gestor de secretos

# GitHub Actions: Secrets
# GCP: Secret Manager
# AWS: Secrets Manager / Parameter Store
```

### 4. Gestión de dependencias
```bash
# Actualizaciones regulares
uv sync
pip-audit
npm audit
npm update

# Usar archivos de bloqueo
uv lock
npm ci  # Usa package-lock.json
```

## Solución de problemas

### Si se hizo commit de información confidencial
```bash
# Eliminar del historial (nota: se requiere push forzado)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret" \
  --prune-empty --tag-name-filter cat -- --all

# O usar BFG Repo-Cleaner
bfg --delete-files "*.env"

# Invalidar y rotar credenciales (obligatorio)
```

### Si se encuentran vulnerabilidades
```bash
# 1. Evaluar el alcance del impacto
# 2. Aplicar parches
uv add package==X.X.X  # Version corregida
npm update package

# 3. Verificar
pip-audit
npm audit
```

## Recursos relacionados
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Anthropic Security Guidelines](https://docs.anthropic.com/en/docs/security)
