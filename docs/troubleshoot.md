# トラブルシューティング完全ガイド

**更新日**: 2026年3月20日

このガイドは、ai-agent-camp の使用中に発生する一般的な問題の解決方法をまとめています。

> **ターミナル初心者の方へ**: このガイドでは「ターミナルで実行」という手順が多く登場します。ターミナルの開き方や基本操作がわからない場合は、先に [ターミナル入門ガイド](terminal-guide.md) をお読みください。

---

## 目次

1. [セットアップ関連の問題](#セットアップ関連の問題)
2. [API・認証関連の問題](#api認証関連の問題)
3. [ツール・スキル実行エラー](#ツールスキル実行エラー)
4. [パフォーマンス・リソース問題](#パフォーマンスリソース問題)
5. [コマンド・スキル固有の問題](#コマンドスキル固有の問題)
6. [データ処理関連の問題](#データ処理関連の問題)
7. [ネットワーク・通信関連の問題](#ネットワーク通信関連の問題)
8. [一般的な質問 (FAQ)](#一般的な質問-faq)
9. [サポート・リソース](#サポートリソース)

---

## セットアップ関連の問題

### 問題 1: "コマンドが見つかりません" エラー

```
Error: Command 'コマンド名' not found
zsh: command not found: claude
zsh: command not found: codex
```

**原因**:
- 使っているツール本体がインストールされていない
- PATH 環境変数が正しく設定されていない
- ツールに合わない入口を使っている
- コマンド名にタイプミスがある

**解決方法**:

#### Step 1: インストール状態確認

```bash
# Claude Code / Codex / Cursor の確認
which claude || true
claude --version || true
which codex || true
codex --version || true
which cursor || true

# 参照ディレクトリの確認
ls -la .cursor/commands/
ls -la skills/
```

#### Step 2: 使うツールを再インストール

```bash
# Claude Code
npm install -g @anthropic-ai/claude-code

# Codex
npm install -g @openai/codex
```

#### Step 3: PATH の確認・設定

```bash
# 現在の PATH を確認
echo $PATH

# ツール本体の場所を確認
which claude || true
which codex || true

# 必要に応じて PATH に追加
export PATH="${PATH}:/usr/local/bin"
export PATH="${PATH}:$(npm config get prefix)/bin"

# .bashrc または .zshrc に追加（永続化）
echo 'export PATH="${PATH}:$(npm config get prefix)/bin"' >> ~/.zshrc
source ~/.zshrc
```

#### Step 4: コマンドが存在するか確認

```bash
# Cursor command の一覧
ls .cursor/commands/lesson/ | grep コマンド名 || true
ls .cursor/commands/utility/ | grep コマンド名 || true

# スキルリストを表示
ls skills/ | grep スキル名
```

**チェックリスト**:
- [ ] `claude --version` または `codex --version` でバージョンが表示される
- [ ] `which claude` または `which codex` でパスが表示される
- [ ] `.cursor/commands/` ディレクトリが存在する
- [ ] `skills/` ディレクトリが存在する

> **ターミナル操作がはじめての方**: 上記のコマンドをどこで実行すればよいかわからない場合は [ターミナル入門ガイド](terminal-guide.md) を参照してください。

---

### 問題 2: Python・Node.js がない

```
Error: python: command not found
Error: node: command not found
```

**原因**: 環境に必要なランタイムがインストールされていない

**解決方法**:

#### macOS の場合

```bash
# Homebrew で Python インストール
brew install python@3.11

# Homebrew で Node.js インストール
brew install node@18

# バージョン確認
python3 --version
node --version
```

#### Linux の場合

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip nodejs npm

# CentOS/RHEL
sudo yum install python3 python3-pip nodejs npm
```

#### 代替方法: nvm・pyenv を使用

```bash
# Node Version Manager インストール
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Python Version Manager インストール
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

---

### 問題 3: Git がインストールされていない

```
Error: git: command not found
```

**解決方法**:

```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt-get install git

# 確認
git --version
```

---

### 問題 4: 権限不足エラー

```
Error: Permission denied
zsh: permission denied: ./script.sh
```

**原因**: ファイルに実行権限がない

**解決方法**:

```bash
# ファイルの権限を確認
ls -la .claude/hooks/ || true
ls -la tools/

# 実行権限を付与
chmod +x .claude/hooks/*.sh
chmod +x tools/*.py
chmod +x skills/*/scripts/*.py
```

---

## API・認証関連の問題

### 問題 5: "API キー未設定" エラー

```
Error: GEMINI_API_KEY or GOOGLE_API_KEY not found
Error: ANTHROPIC_API_KEY not set
```

**原因**: 環境変数に API キーが設定されていない

**解決方法**:

#### Step 1: 環境変数を確認

```bash
# 設定済みの環境変数をリスト表示
env | grep API_KEY
env | grep TOKEN

# 特定の変数を確認
echo $GEMINI_API_KEY
echo $GOOGLE_API_KEY
echo $ANTHROPIC_API_KEY
```

#### Step 2: API キーを取得

```bash
# Gemini API キー取得
# https://aistudio.google.com/app/apikey にアクセス

# Google Cloud API キー取得
# https://console.cloud.google.com/
```

#### Step 3: 環境変数を設定

```bash
# 一時的な設定（現在のセッションのみ）
export GEMINI_API_KEY="your-api-key"
export GOOGLE_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"

# 確認
echo $GEMINI_API_KEY
```

#### Step 4: 環境変数を永続化

```bash
# .env ファイルを作成
cat > .env << EOF
GEMINI_API_KEY=your-api-key
GOOGLE_API_KEY=your-api-key
ANTHROPIC_API_KEY=your-api-key
SLACK_BOT_TOKEN=xoxb-...
EOF

# .bashrc または .zshrc に追加
cat >> ~/.zshrc << EOF
if [ -f .env ]; then
  export \$(cat .env | grep -v '#' | xargs)
fi
EOF

source ~/.zshrc
```

#### Step 5: .env ファイルをセキュアに管理

```bash
# .env を .gitignore に追加
echo ".env" >> .gitignore

# .env のパーミッション設定
chmod 600 .env
```

**チェックリスト**:
- [ ] API キーを取得した
- [ ] 環境変数に設定した
- [ ] `.env` ファイルに記載した
- [ ] `.env` は `.gitignore` に含まれている
- [ ] `.env` のパーミッションが 600

---

### 問題 6: "認証に失敗しました" エラー

```
Error: Authentication failed
Error: Invalid credentials
Error: 401 Unauthorized
```

**原因**: API キーが無効、期限切れ、または権限不足

**解決方法**:

#### Google API の場合

```bash
# 認証状態を確認
gcloud auth list

# 認証を再実行
gcloud auth application-default login

# トークンを確認
gcloud auth application-default print-access-token

# トークン情報を確認
curl -H "Authorization: Bearer $(gcloud auth application-default print-access-token)" \
  https://www.googleapis.com/oauth2/v1/tokeninfo
```

#### Clasp（GAS）の場合

```bash
# ログイン状態を確認
clasp login --status

# 再ログイン
clasp login

# ログアウト
clasp logout
```

#### GitHub API の場合

```bash
# 認証状態を確認
gh auth status

# 再認証
gh auth login

# トークンの確認
gh api user
```

---

### 問題 7: "レート制限エラー" (429 Too Many Requests)

```
Error 429: Too Many Requests
Error: Rate limit exceeded
```

**原因**: API の使用制限に達した

**解決方法**:

#### Step 1: 実行を一時停止

```bash
# 数分～数時間待機
sleep 300  # 5分待機

# その後、再実行
/コマンド名
```

#### Step 2: リトライ設定を追加

```bash
# リトライロジック付きで実行
/コマンド名 --retry-delay 5 --max-retries 3

# または
python script.py --backoff-factor 2 --max-retries 5
```

#### Step 3: キューイングで並列実行を避ける

```bash
# コマンドをキューに入れて順次実行
/コマンド1 --queue
/コマンド2 --queue
/コマンド3 --queue

# キューを実行
python scripts/run_queue.py
```

#### Step 4: バッチサイズを削減

```bash
# 一度に処理するデータ量を削減
/コマンド名 --batch-size 10

# または
/コマンド名 --batch-size 5 --delay 2
```

**予防策**:
- API 使用量を監視
- リクエスト間に遅延を設定
- キャッシュを活用して重複リクエストを避ける

---

## ツール・スキル実行エラー

### 問題 8: "ModuleNotFoundError" - Python モジュール不足

```
ModuleNotFoundError: No module named 'pillow'
ModuleNotFoundError: No module named 'google'
ImportError: No module named 'requests'
```

**原因**: 必要な Python パッケージがインストールされていない

**解決方法**:

#### Step 1: 不足しているモジュールをインストール

```bash
# 単一パッケージのインストール
uv add pillow
uv add google-genai
uv add requests
```

#### Step 2: プロジェクト全体の依存関係を一括インストール

```bash
# pyproject.toml の依存関係をすべてインストール
uv sync
```

#### Step 3: 特定のバージョンで問題がないか確認

```bash
# インストール済みパッケージを確認
uv pip list | grep module名

# 特定バージョンをインストール
uv add pillow==10.0.0

# 互換性確認
uv pip check
```

**よくあるモジュール**:
```
google-genai          # Gemini API
google-cloud-bigquery # BigQuery
python-pptx           # PowerPoint
openpyxl              # Excel
pillow                # 画像処理
requests              # HTTP 通信
beautifulsoup4        # HTML パース
playwright            # ブラウザ自動操作
```

---

### 問題 9: "Playwright ブラウザ未インストール"

```
Error: Chromium not found
Error: Browser executable not found
```

**原因**: Playwright のブラウザがインストールされていない

**解決方法**:

```bash
# Playwright ブラウザをインストール
playwright install chromium

# または
playwright install

# Firefox も必要な場合
playwright install firefox

# すべてのブラウザをインストール
playwright install
```

---

### 問題 10: スキルが実行されない

```
Error: Skill not found
Error: Cannot import skill
```

**原因**: スキルがインストールされていない、またはパスが正しくない

**解決方法**:

#### Step 1: スキルがインストールされているか確認

```bash
# スキルディレクトリを確認
ls -la skills/

# 特定のスキルを確認
ls -la skills/banner-creator/

# スキルのメインファイルを確認
ls -la skills/banner-creator/scripts/
```

#### Step 2: スキルをインストール

```bash
# 単一スキルのインストール
python skills/banner-creator/scripts/install.py

# または
cd skills/banner-creator && uv sync

# すべてのスキルをインストール
python scripts/setup.py --install skills
```

#### Step 3: 実行パスを確認

```bash
# スキルのメインファイルパスを確認
which banner-creator

# または直接実行
python skills/banner-creator/scripts/main.py --help
```

---

## パフォーマンス・リソース問題

### 問題 11: "メモリ不足" エラー

```
MemoryError: Unable to allocate X bytes
OSError: [Errno 12] Cannot allocate memory
```

**原因**: メモリ使用量が限界に達した

**解決方法**:

#### Step 1: 現在のメモリ使用状況を確認

```bash
# macOS
top -l 1 | head -20
vm_stat

# Linux
free -h
top

# 特定のプロセスのメモリ使用量
ps aux | grep python
ps aux | grep node
```

#### Step 2: 不要なプロセスを終了

```bash
# Python プロセスを終了
killall python
killall python3

# Node.js プロセスを終了
killall node

# 特定のプロセスを終了
kill -9 PID
```

#### Step 3: バッチサイズを削減

```bash
# 一度に処理するデータ量を削減
/コマンド名 --batch-size 5

# ストリーミング処理に変更
/コマンド名 --stream

# ジェネレータを使用
/コマンド名 --lazy
```

#### Step 4: 出力ファイルを削除

```bash
# 古い生成ファイルを削除
rm -rf docs/generated/banners/2026-01-*

# キャッシュをクリア
rm -rf .cache/

# ログファイルをクリア
rm -rf logs/*.old
```

---

### 問題 12: コマンド実行が遅い

```
実行時間が長い
タイムアウトエラー
```

**原因**:
- ネットワーク遅延
- API レスポンス遅延
- リソース不足
- 不適切な設定

**解決方法**:

#### Step 1: ネットワーク接続を確認

```bash
# インターネット接続確認
ping google.com
ping 8.8.8.8

# DNS 確認
nslookup google.com
dig google.com

# 遅延を測定
curl -w "@curl-format.txt" https://api.example.com
```

#### Step 2: CPU・メモリ使用状況を確認

```bash
# macOS
top -l 1 | head -20

# Linux
htop
vmstat 1 5
```

#### Step 3: 並列処理を有効化

```bash
# ワーカー数を指定
/コマンド名 --workers 4

# または
/コマンド名 --parallel --processes 4
```

#### Step 4: キャッシュを有効化

```bash
# キャッシュを使用
/コマンド名 --cache

# キャッシュをリセット
/コマンド名 --cache --clear
```

#### Step 5: タイムアウト値を増やす

```bash
# タイムアウトを延長
/コマンド名 --timeout 300

# リトライ設定
/コマンド名 --retry-delay 5 --max-retries 3
```

---

### 問題 13: ディスク容量不足

```
Error: No space left on device
DiskFull Exception
```

**原因**: ディスク容量が満杯

**解決方法**:

#### Step 1: ディスク容量を確認

```bash
# ディスク容量確認
df -h

# パーティション別
df -T

# ディレクトリサイズを確認
du -sh *
du -sh .
du -sh docs/
```

#### Step 2: 不要なファイルを削除

```bash
# 古い生成ファイルを削除
find docs/generated/ -mtime +30 -delete

# ログファイルを削除
find logs/ -mtime +7 -delete

# キャッシュをクリア
rm -rf .cache/
rm -rf ~/.cache/

# 一時ファイルを削除
rm -rf /tmp/*
```

#### Step 3: 大きなファイルを確認

```bash
# 大容量ファイルを検索
find . -size +100M -type f -exec ls -lh {} \;

# または
du -sh * | sort -h | tail -10
```

---

## コマンド・スキル固有の問題

### 問題 14: バナー生成が失敗する

```
Error: Failed to generate banner
Error: Image generation failed
```

**原因**:
- API キー未設定
- プロンプトが不適切
- サイズ指定エラー

**解決方法**:

```bash
# API キー確認
echo $GEMINI_API_KEY

# プロンプト検証
/create-banner --message "テキスト" --debug

# サイズを確認
/create-banner --platform x_post --list-sizes

# デフォルト設定で試す
/create-banner --platform x_post --message "テスト"
```

---

### 問題 15: BigQuery 接続失敗

```
Error: Failed to authenticate with BigQuery
Error: Project not found
```

**原因**:
- GCP 認証未完了
- プロジェクト ID 誤り
- 権限不足

**解決方法**:

```bash
# GCP 認証を確認
gcloud auth list
gcloud config list

# プロジェクト ID を確認
gcloud projects list

# プロジェクト を設定
gcloud config set project PROJECT_ID

# BigQuery へのアクセス権限を確認
gcloud projects get-iam-policy PROJECT_ID

# BigQuery 接続テスト
bq ls
bq show dataset_id
```

---

### 問題 16: PowerPoint 処理エラー

```
Error: Failed to read PPTX file
Error: Invalid PPTX format
```

**原因**:
- ファイルが破損している
- フォーマットが古い
- 権限不足

**解決方法**:

```bash
# ファイルが存在するか確認
file presentation.pptx

# ファイルサイズを確認
ls -lh presentation.pptx

# 別のツールで開いて保存
# PowerPoint または LibreOffice で開き直す

# 古いバージョンを確認
file -i presentation.pptx

# python-pptx のバージョン確認
pip show python-pptx
```

---

## データ処理関連の問題

### 問題 17: CSVファイル読み込みエラー

```
Error: Failed to parse CSV
Error: Encoding error
```

**原因**:
- ファイルエンコーディング不一致
- 区切り文字が異なる
- ファイル形式エラー

**解決方法**:

```bash
# ファイルエンコーディング確認
file -i data.csv

# エンコーディング変換
iconv -f SHIFT_JIS -t UTF-8 data.csv > data_utf8.csv

# 区切り文字を確認
head -1 data.csv | od -c

# 行末を確認
file -i data.csv
```

---

### 問題 18: JSON パースエラー

```
Error: Failed to parse JSON
json.decoder.JSONDecodeError
```

**原因**:
- JSON フォーマットが不正
- エスケープ文字の誤り
- BOM が付いている

**解決方法**:

```bash
# JSON ファイルを検証
python -m json.tool data.json

# または
jq . data.json

# BOM を削除
sed '1s/^\xEF\xBB\xBF//' data.json > data_clean.json

# 整形
jq '.' data.json > data_formatted.json
```

---

## ネットワーク・通信関連の問題

### 問題 19: インターネット接続エラー

```
Error: Connection refused
Error: Network unreachable
Error: Name or service not known
```

**原因**:
- インターネット接続が切れている
- ファイアウォール設定
- DNS 問題

**解決方法**:

#### Step 1: インターネット接続を確認

```bash
# インターネット接続確認
ping 8.8.8.8
ping google.com

# DNS 確認
nslookup google.com
dig google.com

# ネットワークインターフェース確認
ifconfig

# 接続状態確認
networkQuality
```

#### Step 2: ファイアウォール設定を確認

```bash
# macOS ファイアウォール確認
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# ファイアウォール無効化
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# Linux ファイアウォール確認
sudo iptables -L
```

#### Step 3: DNS を変更

```bash
# Google Public DNS を使用
# /etc/resolv.conf に追加
nameserver 8.8.8.8
nameserver 8.8.4.4

# または macOS
networksetup -setdnsservers Wi-Fi 8.8.8.8 8.8.4.4
```

---

### 問題 20: Slack 接続エラー

```
Error: Failed to connect to Slack
Error: Invalid token
```

**原因**:
- Slack Bot Token が無効
- チャネル ID が誤っている
- 権限不足

**解決方法**:

```bash
# Slack Bot Token 確認
echo $SLACK_BOT_TOKEN

# トークンを検証
curl -s -X auth.test \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/auth.test | jq .

# チャネル ID を確認
curl -s -X conversations.list \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/conversations.list | jq .

# トークンの権限を確認
curl -s -X auth.test \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  https://slack.com/api/auth.test | jq '.auth_test_data'
```

---

## 一般的な質問 (FAQ)

### Q1: コマンドの出力をファイルに保存したい

**A**: リダイレクトまたは `--output` パラメータを使用

```bash
# 標準出力をリダイレクト
/コマンド名 > output.txt

# 標準エラーも含める
/コマンド名 > output.txt 2>&1

# パラメータで指定
/コマンド名 --output result.json

# JSON 形式で出力
/コマンド名 --output-format json > result.json
```

---

### Q2: 複数ファイルをバッチ処理したい

**A**: ループやスクリプトで処理

```bash
# Bash ループ
for file in *.csv; do
  /コマンド名 --input "$file"
done

# jq でバッチ処理
jq -r '.[] | @base64d' input.json | while read line; do
  /コマンド名 --config "$line"
done

# GNU Parallel
cat files.txt | parallel /コマンド名 --input {}
```

---

### Q3: 実行内容をログに記録したい

**A**: ログレベルを設定

```bash
# ログをファイルに記録
/コマンド名 --log-file execution.log

# ログレベルを指定
/コマンド名 --log-level DEBUG

# 詳細ログを表示
/コマンド名 -vvv

# ログをリアルタイムで監視
tail -f execution.log
```

---

### Q4: 環境によって設定を変えたい

**A**: 環境変数またはコンフィグファイルを使用

```bash
# 環境別 .env ファイル
.env.development
.env.production
.env.staging

# 環境を指定して実行
ENV=production /コマンド名

# または
/コマンド名 --env production

# .env ファイルを読み込む
set -a
source .env.${ENV}
set +a
```

---

### Q5: デバッグモードで詳細情報を表示したい

**A**: デバッグフラグを使用

```bash
# デバッグモード有効化
/コマンド名 --debug

# トレース出力
/コマンド名 --trace

# Dry-run（実行しない）
/コマンド名 --dry-run

# 実行前に確認
/コマンド名 --confirm

# 詳細ログ
/コマンド名 --verbose --verbose --verbose
```

---

### Q6: コマンドをスケジュール実行したい

**A**: cron または GitHub Actions

```bash
# cron ジョブ登録
crontab -e

# 毎日 9:00 に実行
0 9 * * * /path/to/コマンド名 >> /var/log/cron.log

# GitHub Actions ワークフロー
name: Scheduled Task
on:
  schedule:
    - cron: '0 9 * * *'
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: /コマンド名
```

---

### Q7: キャッシュをクリアしたい

**A**: キャッシュディレクトリを削除

```bash
# 全キャッシュ削除
rm -rf .cache/
rm -rf ~/.cache/

# 特定のキャッシュ削除
/コマンド名 --cache --clear

# または
/コマンド名 --no-cache
```

---

### Q8: エラーメッセージの意味がわかりません

**A**: ログを詳しく確認

```bash
# 詳細ログを出力
/コマンド名 --debug 2>&1 | tee error.log

# ログの最後を確認
tail -50 error.log

# エラー部分のみを抽出
grep -i error error.log

# スタックトレースを確認
tail -100 error.log | grep -A 50 "Traceback"
```

---

### Q9: 古いコマンドから新しいコマンドに移行したい

**A**: 互換性を確認してマイグレーション

```bash
# 古いコマンドの確認
/old-command --help

# 新しいコマンドの確認
/new-command --help

# パラメータマッピング
# old: --input file.csv → new: --file file.csv
/new-command --file file.csv

# 同時に実行して出力を比較
/old-command --output old.json
/new-command --output new.json
diff old.json new.json
```

---

### Q10: ベストプラクティスは何ですか？

**A**: 推奨実行方法

```text
1. 使っているツールの入口からセットアップ確認をする
   - Codex: aiagent-check-setup
   - Cursor: /check-setup

2. API キーは chat に貼らず、.env.local に保存する

3. lesson や command を小さく試す

4. ログや出力ファイルを確認する
```

---

## サポート・リソース

### 公式ドキュメント

- [Claude Code 公式](https://claude.com/claude-code)
- [Gemini API ドキュメント](https://ai.google.dev/gemini-api)
- [Google Cloud ドキュメント](https://cloud.google.com/docs)
- [Slack API ドキュメント](https://api.slack.com)

### コミュニティ

- GitHub Issues: バグ報告・質問
- Discussions: 機能リクエスト・ベストプラクティス
- Stack Overflow: `claude-code` タグで質問

### 自分でデバッグするコツ

1. **エラーメッセージを読む** - 最初の行が原因を示していることが多い
2. **ログレベルを上げる** - `--debug` または `--log-level DEBUG` で詳細を確認
3. **ステップバイステップで実行** - 各処理を個別に確認
4. **最小限の入力でテスト** - 小さなデータセットで確認
5. **既知の問題を検索** - GitHub Issues を確認

### よくある解決ステップ

```text
1. 状態確認
   - Codex: aiagent-check-setup
   - Cursor: /check-setup

2. ログを増やして再実行

3. エラー箇所と関連ファイルを確認

4. 秘密情報や権限設定を再確認

5. 最小構成で再実行
```

---

**ドキュメント更新履歴**

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2026-03-20 | 1.1.0 | 3ツール対応の入口と安全導線に更新 |
| 2026-02-02 | 1.0.0 | 初版作成（20カテゴリ、90+の問題解決例） |

**フィードバック**: このドキュメントに追加すべき内容や改善提案がある場合は、Issues でお知らせください。
