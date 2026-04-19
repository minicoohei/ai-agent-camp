# Gmail Pending Replies - メール未返信抽出

Gmailで返信が必要なメールを抽出し、**返信案を自動生成**します。

## 対象カテゴリ

1. **未返信メール**: 自分宛メール（TO/CC）で、返信していないもの
2. **スレッド返信**: 自分が開始したスレッドで、最後の返信が他人からのもの

## データソース

### 方法1: 同期済みデータを使用（推奨）

`output/gmail/{アカウント名}/` に同期されたMarkdownファイルを解析します。

| アカウント | パス | 自分のアドレス |
|------------|------|----------------|
| default | `output/gmail/default/` | `user@example.com` |
| work | `output/gmail/work/` | 対応するアドレス |

### 方法2: API経由（GMAIL_ACCOUNTS_CONFIG設定時）

```bash
python src/get_gmail_pending_replies.py --days {日数}
```

## 実行手順

### Step 1: パラメータの抽出

ユーザーの入力から以下を抽出してください：
- **日数**: 対象日数（デフォルト: 7）
- **アカウント**: 特定アカウントのみ（デフォルト: all）
- **出力形式**: markdown / json（デフォルト: 画面表示）

### Step 2: メールのスキャン

同期データ `output/gmail/{アカウント}/YYYY-MM-DD/*.md` を解析し、以下を抽出：
- 自分以外からの受信メール
- 通知系メール（noreply, bank, peatix等）を除外
- 会議招待（.ics添付）を除外
- 同じ件名で自分が返信済みのものを除外

### Step 3: 結果の表示 + 返信案の自動生成

1. 未返信メール一覧を表示
2. **各メールの内容を分析し、メールタイプを判定**:
   - 📋 **依頼・タスク**: 具体的なアクションが求められているもの
   - ❓ **質問**: 回答が求められているもの
   - 📢 **情報共有**: 返信不要（CCで共有されたもの等）

3. **依頼・質問メールには返信案を自動生成**:
   - メール本文を読み込み
   - 関連するプロジェクト情報があれば参照
   - 適切な返信案を作成

## オプション

| オプション | 説明 | デフォルト |
|------------|------|-----------|
| `--days INT` / `-d` | 対象日数 | 7 |
| `--account TEXT` / `-a` | 特定アカウントのみ（ラベル名） | all |
| `--output PATH` / `-o` | 出力ファイルパス（.json / .md） | stdout |

## 使用例

### 基本実行

```
/gmail-pending-replies
```

→ デフォルト設定（7日分、全アカウント）で実行

### 日数指定

```
/gmail-pending-replies 3日分
```

→ `--days 3` で実行

### 特定アカウントのみ

```
/gmail-pending-replies personalアカウントだけ
```

→ `--account personal` で実行

### Markdownで保存

```
/gmail-pending-replies output/pending.md に保存
```

→ `--output output/pending.md` で実行

## 前提条件

### 同期データ使用時（推奨）

`output/gmail/{アカウント名}/` にメールが同期されていること。

```
output/gmail/
├── my-account/
│   ├── 2026-01-27/
│   │   ├── index.md          # 日別一覧
│   │   ├── 19bfd03adcbf0235.md  # 個別メール
│   │   └── ...
│   └── ...
└── work/
    └── ...
```

各メールファイルの形式：
```yaml
---
id: 19bfd03adcbf0235
subject: 件名
from: 送信者 <email@example.com>
date: 2026-01-27 10:13:51
attachments: file1.pdf, file2.xlsx  # オプション
---

# 件名

メール本文...
```

### API使用時（オプション）

`GMAIL_ACCOUNTS_CONFIG` 環境変数に複数アカウント設定が必要です：

```json
{
  "accounts": [
    {
      "label": "work",
      "type": "service_account",
      "subject": "user@company.com"
    },
    {
      "label": "personal",
      "type": "oauth",
      "client_id_env": "GMAIL_PERSONAL_CLIENT_ID",
      "client_secret_env": "GMAIL_PERSONAL_CLIENT_SECRET",
      "refresh_token_env": "GMAIL_PERSONAL_REFRESH_TOKEN"
    }
  ]
}
```

## 出力形式

### 1. 未返信メール一覧

```
📋 返信が必要なメール（default）: 2 件
📅 対象期間: 過去7日間

======================================================================

1. プロジェクト進捗レポートについて ⚠️ 要対応
   📅 2026-01-27 10:13
   👤 山田 太郎 <taro.yamada@example.com>
   📋 タイプ: 依頼・タスク
   💬 レポートの確認依頼
   🔗 https://mail.google.com/mail/u/0/#inbox/xxx

2. 月次ミーティングのアジェンダについて
   📅 2026-01-23 13:53
   👤 佐藤 花子 <hanako.sato@example.com>
   📢 タイプ: 情報共有（CC）
   💬 アジェンダ案の共有
   🔗 https://mail.google.com/mail/u/0/#inbox/yyy

======================================================================
```

### 2. 返信案の自動生成（依頼・質問メールのみ）

依頼や質問が含まれるメールには、自動的に返信案を生成します：

```
---
## 返信案: プロジェクト進捗レポートについて

件名: Re: プロジェクト進捗レポートについて

山田様

お世話になっております。
レポートのご依頼、承知いたしました。

以下のカテゴリでレポートをご用意できればと考えております。

【1. 情報収集・検索】
・Slack/Gmail/カレンダーの横断検索・サマリ生成

【2. 文章・資料作成】
・業務フロー図の自動生成

【3. 整形・転記】
・データクレンジング・フォーマット変換

今週中に資料をお送りします。
---
```

## 除外パターン

以下のメールは自動的に除外されます：

| カテゴリ | パターン例 |
|----------|------------|
| 通知系 | noreply, no-reply, notification |
| 銀行 | @bank.gmo-aozora.com |
| イベント | @peatix.com, @morningpitch.com |
| 自動送信 | spamdigest, Moderator |
| 会議招待 | .ics添付、teams.microsoft.com |

## 関連コマンド

- `/extract-tasks` - 複数ソースからのタスク抽出（Gmailも含む）
- `/slack-pending-replies` - Slack版の未返信抽出
