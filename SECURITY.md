# セキュリティポリシー

## 脆弱性の報告

セキュリティに関する問題を発見した場合、**GitHub Issues には投稿しないでください**。

以下の方法で非公開にご報告ください:

- **GitHub Security Advisories**: [このリポジトリの Security Advisories](../../security/advisories/new) から報告
- **連絡先**: リポジトリオーナー [@minicoohei](https://github.com/minicoohei) へ直接ご連絡ください

### 報告に含めていただきたい情報

- 脆弱性の概要と影響範囲
- 再現手順
- 該当するファイル・コンポーネント
- 可能であれば修正案

## 対応ポリシー

| 段階 | 目安 |
|------|------|
| 受領確認 | 3 営業日以内 |
| 初期評価・トリアージ | 7 営業日以内 |
| 修正リリース（重大度による） | 30 日以内 |

重大な脆弱性については優先的に対応します。報告者には進捗を随時共有します。

## セキュリティアーキテクチャ

本プロジェクトは **3 層防御** の構造を採用しています:

| 層 | 機構 | 役割 |
|----|------|------|
| 第 1 層 | `settings.json` deny リスト | 危険コマンドの即時拒否 |
| 第 2 層 | `bash_guard.py` / `write_guard.py` | rm→ゴミ箱ツール置換・秘密情報ファイル保護・Prompt Injection 対策・認証ヘッダ exfil 検知 |
| 第 3 層 | `pre-commit` フック | 機密ファイルのコミット防止 |

加えて以下の観点で防御を入れています:

- **Indirect Prompt Injection 対策**: `skills/check-inbox/` 等、外部メッセージを LLM に渡すスキルでは境界タグで囲み、既知の PI フレーズを除去
- **Fork Supply Chain 検知**: `tools/scripts/verify_integrity.py` で origin URL と追跡ファイルのハッシュを公式と照合
- **Guardrail Bypass 警告**: `CLAUDE_GUARDRAILS_SKIP=1` 使用時は stderr に明示警告を表示

詳細は [`docs/security-guardrails.md`](docs/security-guardrails.md) を参照してください。

## スコープ

### 対象

- `tools/` 配下の Python スクリプト
- `.claude/hooks/` 配下のセキュリティフック
- `.claude/settings.json` の deny リスト設定
- `scripts/` 配下のセットアップ・ヘルパースクリプト
- `.claude/skills/` 配下のスキルスクリプト
- pre-commit フックの設定

### 対象外

- 外部 API サービス（Google Cloud、Slack、Gemini 等）の脆弱性
- サードパーティ製パッケージ自体の脆弱性（該当パッケージの管理元へ報告してください）
- Cursor IDE / Claude Code 本体の脆弱性

## クレデンシャル管理

- API キー・認証情報は **`.env` ファイル** で管理し、Git にはコミットしません
- `.gitignore` により `.env`、`credentials.json` 等を除外しています
- `pre-commit` フックが機密ファイルの誤コミットを自動検出・防止します
- リポジトリには `.env.example` をテンプレートとして提供しています

万が一クレデンシャルがコミットされた場合は、直ちに該当キーを無効化し、履歴からの除去を行ってください。
