---
description: Security settings verification and best practices check
---

# Security Settings Verification

## Usage
```
/check-security
```

## Process
Verify the project's security settings and detect potential risks.

## Check Items

### 1. Sensitive Information Leak Check
```bash
# Check if .env files are tracked by Git
git ls-files | grep -E "\.env$|\.env\." && echo "WARNING: .env files tracked!"

# Check .gitignore
cat .gitignore | grep -E "\.env|secret|credential|\.key"

# Scan for hardcoded credentials
grep -rn "password\s*=\s*['\"]" --include="*.py" --include="*.js" .
grep -rn "api_key\s*=\s*['\"]" --include="*.py" --include="*.js" .
grep -rn "secret\s*=\s*['\"]" --include="*.py" --include="*.js" .
```

### 2. Dependency Vulnerabilities
```bash
# Python
pip-audit 2>/dev/null || echo "pip-audit not installed"

# Node.js
npm audit 2>/dev/null || echo "No package.json"

# GitHub Dependabot
gh api repos/{owner}/{repo}/vulnerability-alerts 2>/dev/null
```

### 3. Authentication Settings
```bash
# Check SSH key permissions
ls -la ~/.ssh/*.pub 2>/dev/null
ls -la ~/.ssh/id_* 2>/dev/null | head -5

# GPG signing settings
git config --get user.signingkey

# 2FA status
gh auth status 2>/dev/null | grep -i "two-factor"
```

### 4. API Key Management
```bash
# Check environment variables (mask values)
env | grep -iE "(api_key|token|secret|password|credential)" | sed 's/=.*/=***/'

# Check .env file existence
ls -la .env* 2>/dev/null
```

### 5. GitHub Repository Settings
```bash
# Branch protection
gh api repos/{owner}/{repo}/branches/main/protection 2>/dev/null

# Secret scanning
gh api repos/{owner}/{repo}/secret-scanning/alerts 2>/dev/null
```

## Output Format

```markdown
## Security Check Report

### Summary
- Critical issues: X
- Warnings: X
- Informational: X

### Details

#### Sensitive Information Leak Risk
| Check Item | Status | Details |
|------------|--------|---------|
| .env Git tracking | OK/NG | ... |
| Hardcoded credentials | OK/NG | ... |
| .gitignore settings | OK/NG | ... |

#### Dependency Vulnerabilities
| Package | Severity | Action |
|---------|----------|--------|
| package-a | High | Update recommended |
| package-b | Medium | Update recommended |

#### Authentication Settings
| Item | Status | Recommendation |
|------|--------|----------------|
| SSH key permissions | OK/NG | Set to 600 |
| GPG signing | OK/NG | Enable recommended |
| 2FA | OK/NG | Enable recommended |

### Recommended Actions
1. [Critical] ...
2. [Warning] ...
3. [Info] ...
```

## Checklist

### Required
- [ ] .env file is included in .gitignore
- [ ] No hardcoded credentials
- [ ] SSH key permissions are appropriate (600)
- [ ] No dependency vulnerabilities

### Recommended
- [ ] GPG signing enabled
- [ ] 2FA enabled
- [ ] Branch protection configured
- [ ] Secret scanning enabled
- [ ] Dependabot enabled

### Periodic Checks
- [ ] Weekly: Dependency vulnerability scan
- [ ] Monthly: Credential rotation
- [ ] Quarterly: Security settings review

## Security Best Practices

### 1. Credential Management
```python
# Bad example
API_KEY = "sk-1234567890abcdef"

# Good example
import os
API_KEY = os.environ.get("API_KEY")
```

### 2. .gitignore Settings
```gitignore
# Environment variables
.env
.env.local
.env.*.local

# Credentials
*.pem
*.key
credentials.json
service-account.json

# IDE settings (may contain sensitive info)
.idea/
.vscode/settings.json
```

### 3. Environment Variable Management
```bash
# Development: .env + dotenv
# Production: environment variables or secret manager

# GitHub Actions: Secrets
# GCP: Secret Manager
# AWS: Secrets Manager / Parameter Store
```

### 4. Dependency Management
```bash
# Regular updates
pip install --upgrade pip
pip-audit
npm audit
npm update

# Use lock files
pip freeze > requirements.txt
npm ci  # Uses package-lock.json
```

## Troubleshooting

### If Sensitive Information Was Committed
```bash
# Remove from history (note: force push required)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner
bfg --delete-files "*.env"

# Invalidate and rotate credentials (mandatory)
```

### If Vulnerabilities Are Found
```bash
# 1. Assess impact scope
# 2. Apply patches
pip install package==X.X.X  # Fixed version
npm update package

# 3. Verify
pip-audit
npm audit
```

## Related Resources
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Anthropic Security Guidelines](https://docs.anthropic.com/en/docs/security)
