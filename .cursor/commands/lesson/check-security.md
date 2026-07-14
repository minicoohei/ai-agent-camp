---
description: "Lesson command"
nonInteractiveMode: compliant
---
# セキュリティ設定確認

## 使い方
```
/check-security
```

## 処理内容
プロジェクトのセキュリティ設定を確認し、潜在的なリスクを検出します。

## チェック項目

### 1. 機密情報の漏洩チェック
```bash
# .envファイルがGit管理されていないか確認
git ls-files | grep -E "\.env$|\.env\." && echo "WARNING: .env files tracked!"

# .gitignoreの確認
cat .gitignore | grep -E "\.env|secret|credential|\.key"

# ハードコードされた認証情報のスキャン
grep -rn "password\s*=\s*['\"]" --include="*.py" --include="*.js" .
grep -rn "api_key\s*=\s*['\"]" --include="*.py" --include="*.js" .
grep -rn "secret\s*=\s*['\"]" --include="*.py" --include="*.js" .
```

### 2. 依存関係の脆弱性
```bash
# Python
pip-audit 2>/dev/null || echo "pip-audit未インストール"

# Node.js
npm audit 2>/dev/null || echo "package.json なし"

# GitHub Dependabot
gh api repos/{owner}/{repo}/vulnerability-alerts 2>/dev/null
```

### 3. 認証設定
```bash
# SSH鍵の権限確認
ls -la ~/.ssh/*.pub 2>/dev/null
ls -la ~/.ssh/id_* 2>/dev/null | head -5

# GPG署名設定
git config --get user.signingkey

# 2FA状態
gh auth status 2>/dev/null | grep -i "two-factor"
```

### 4. API キー管理
```bash
# 環境変数の確認（値はマスク）
env | grep -iE "(api_key|token|secret|password|credential)" | sed 's/=.*/=***/'

# .envファイルの存在確認
ls -la .env* 2>/dev/null
```

### 5. GitHub リポジトリ設定
```bash
# ブランチ保護
gh api repos/{owner}/{repo}/branches/main/protection 2>/dev/null

# シークレットスキャン
gh api repos/{owner}/{repo}/secret-scanning/alerts 2>/dev/null
```

## 出力形式

```markdown
## セキュリティチェックレポート

### サマリー
- 重大な問題: X件
- 警告: X件
- 情報: X件

### 詳細

#### 機密情報の漏洩リスク
| チェック項目 | 状態 | 詳細 |
|-------------|------|------|
| .env Git管理 | OK/NG | ... |
| ハードコード認証情報 | OK/NG | ... |
| .gitignore設定 | OK/NG | ... |

#### 依存関係の脆弱性
| パッケージ | 重大度 | 対応 |
|-----------|--------|------|
| package-a | High | アップデート推奨 |
| package-b | Medium | アップデート推奨 |

#### 認証設定
| 項目 | 状態 | 推奨 |
|------|------|------|
| SSH鍵権限 | OK/NG | 600に設定 |
| GPG署名 | OK/NG | 有効化推奨 |
| 2FA | OK/NG | 有効化推奨 |

### 推奨アクション
1. [重大] ...
2. [警告] ...
3. [情報] ...
```

## チェックリスト

### 必須対応
- [ ] .env ファイルが .gitignore に含まれている
- [ ] 認証情報がハードコードされていない
- [ ] SSH鍵の権限が適切（600）
- [ ] 依存関係の脆弱性がない

### 推奨対応
- [ ] GPG署名の有効化
- [ ] 2FAの有効化
- [ ] ブランチ保護の設定
- [ ] シークレットスキャンの有効化
- [ ] Dependabotの有効化

### 定期チェック
- [ ] 週次: 依存関係の脆弱性スキャン
- [ ] 月次: 認証情報のローテーション
- [ ] 四半期: セキュリティ設定のレビュー

## セキュリティベストプラクティス

### 1. 認証情報の管理
```python
# 悪い例
API_KEY = "sk-1234567890abcdef"

# 良い例
import os
API_KEY = os.environ.get("API_KEY")
```

### 2. .gitignore 設定
```gitignore
# 環境変数
.env
.env.local
.env.*.local

# 認証情報
*.pem
*.key
credentials.json
service-account.json

# IDE設定（機密情報が含まれる可能性）
.idea/
.vscode/settings.json
```

### 3. 環境変数の管理
```bash
# 開発環境: .env + dotenv
# 本番環境: 環境変数 or シークレットマネージャー

# GitHub Actions: Secrets
# GCP: Secret Manager
# AWS: Secrets Manager / Parameter Store
```

### 4. 依存関係の管理
```bash
# 定期的な更新
uv sync
pip-audit
npm audit
npm update

# ロックファイルの使用
uv lock
npm ci  # package-lock.json を使用
```

## トラブルシューティング

### 機密情報がコミットされた場合
```bash
# 履歴から削除（注意: 強制プッシュが必要）
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/secret" \
  --prune-empty --tag-name-filter cat -- --all

# または BFG Repo-Cleaner を使用
bfg --delete-files "*.env"

# 認証情報の無効化・ローテーション（必須）
```

### 脆弱性が見つかった場合
```bash
# 1. 影響範囲の確認
# 2. パッチの適用
uv add package==X.X.X  # 修正バージョン
npm update package

# 3. 確認
pip-audit
npm audit
```

## 関連リソース
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Anthropic Security Guidelines](https://docs.anthropic.com/en/docs/security)
