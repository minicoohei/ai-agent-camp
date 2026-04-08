# A/Bテスト実験テンプレート集

チャネル別A/Bテストを標準化するためのテンプレート集。
実験の再現性・比較可能性を高めるため、必ず共通フォーマットを使用すること。

---

## 1. 実験定義 YAML テンプレート（共通フォーマット）

```yaml
# 実験ID: exp-{日付}-{連番3桁}
id: exp-YYYY-MM-DD-NNN

# チャネル: x_twitter | email | linkedin
channel: x_twitter

# 仮説（必須）: "Because [observation], we believe [change] will cause [outcome]"
hypothesis: "Because [observation], we believe [change] will cause [outcome]"

# テスト変数（1実験につき1変数のみ）
# x_twitter: hook | cta | format | tone | timing | hashtag | length
# email:     subject_line | preheader | send_time | cta_text | body_length
# linkedin:  hook | format | tone | cta
test_variable: hook

# バリアント定義
variants:
  - id: A
    label: "コントロール（現行）"
    content: "..."
    notes: ""
  - id: B
    label: "テスト（変更案）"
    content: "..."
    notes: ""

# 主要KPI（1つのみ）
# x_twitter: engagement_rate | impression_count | reply_rate | retweet_rate
# email:     open_rate | click_rate | ctr | unsubscribe_rate
# linkedin:  engagement_rate | comment_rate | share_rate
primary_metric: engagement_rate

# 副次KPI
secondary_metrics:
  - likes
  - retweets
  - replies

# ガードレール指標（悪化してはいけない指標）
guardrail_metrics:
  - unfollow_rate
  - spam_reports

# 実験期間（日数）
duration_days: 3

# 勝敗判定基準（primary_metric の相対改善率）
success_threshold_pct: 10

# ステータス: planned | running | completed | cancelled
status: planned

# 結果（completed になったら記入）
results:
  winner: null        # A | B | no_significant_difference
  a_value: null
  b_value: null
  relative_improvement_pct: null
  sample_size_a: null
  sample_size_b: null
  notes: ""
  learnings: ""
```

---

## 2. X (Twitter) テスト変数テンプレート（7種）

### 2-1. フック形式

```yaml
id: exp-YYYY-MM-DD-001
channel: x_twitter
hypothesis: "Because users engage more with questions, we believe switching from statement hooks to question hooks will increase reply rate"
test_variable: hook
variants:
  - id: A
    label: "ステートメント型フック"
    content: |
      AIで週10時間の作業が自動化できる。
      [本文続き...]
  - id: B
    label: "質問型フック"
    content: |
      週10時間、同じ作業を繰り返していませんか？
      [本文続き...]
primary_metric: reply_rate
secondary_metrics: [likes, retweets, impressions]
guardrail_metrics: [unfollow_rate]
duration_days: 3
```

**フック形式バリエーション:**

| タイプ | パターン | 例 |
|--------|---------|-----|
| 質問形 | 「〇〇していますか？」 | 「毎日同じミスを繰り返していませんか？」 |
| ステートメント形 | 断言から始める | 「AIは既にあなたの仕事を変えている」 |
| 数値引用形 | 具体的数字から始める | 「73%の企業が2025年までにAIを導入済み」 |
| ストーリー形 | 個人体験から始める | 「3ヶ月前、私はこの問題で1日3時間を無駄にしていた」 |

### 2-2. CTA（Call to Action）

```yaml
id: exp-YYYY-MM-DD-002
channel: x_twitter
hypothesis: "Because direct questions generate replies, we believe reply-oriented CTAs will outperform RT-oriented CTAs for engagement"
test_variable: cta
variants:
  - id: A
    label: "RT誘導CTA"
    content: |
      [本文...]
      参考になったらRTしていただけると嬉しいです。
  - id: B
    label: "リプライ誘導CTA"
    content: |
      [本文...]
      あなたはどちら派ですか？リプライで教えてください。
primary_metric: engagement_rate
secondary_metrics: [replies, retweets]
guardrail_metrics: [unfollow_rate]
duration_days: 3
```

**CTAバリエーション:**

| タイプ | 例文 | 期待効果 |
|--------|------|---------|
| リプライ誘導 | 「あなたはどう思いますか？」 | 返信数増加 |
| RT誘導 | 「参考になったらRTお願いします」 | 拡散増加 |
| リンク誘導 | 「詳細はプロフのリンクから」 | クリック増加 |
| 保存誘導 | 「後で見返したいならブックマーク」 | ブックマーク増加 |

### 2-3. フォーマット

```yaml
id: exp-YYYY-MM-DD-003
channel: x_twitter
hypothesis: "Because threads allow deeper content, we believe thread format will increase engagement rate vs single tweet"
test_variable: format
variants:
  - id: A
    label: "単体ツイート"
    content: |
      [140文字以内にまとめたコンテンツ]
  - id: B
    label: "スレッド形式（1/5）"
    content: |
      1/5: [フック]
      2/5: [詳細1]
      3/5: [詳細2]
      4/5: [詳細3]
      5/5: [まとめ・CTA]
primary_metric: engagement_rate
secondary_metrics: [impressions, profile_clicks]
guardrail_metrics: [unfollow_rate]
duration_days: 3
```

**フォーマットバリエーション:**

| タイプ | 特徴 | 適したコンテンツ |
|--------|------|--------------|
| 単体ツイート | シンプル・高速 | 格言・速報・問いかけ |
| スレッド | 深掘り可能 | How-to・事例紹介 |
| 画像付き | 視覚的訴求 | インフォグラフィック・結果共有 |
| 動画付き | 最高のリーチ | デモ・チュートリアル |

### 2-4. トーン

```yaml
id: exp-YYYY-MM-DD-004
channel: x_twitter
hypothesis: "Because our audience is practitioners, we believe casual/honest tone will outperform formal tone"
test_variable: tone
variants:
  - id: A
    label: "専門的トーン"
    content: |
      生成AIの業務適用において、プロンプト設計の最適化が
      ROI最大化の鍵となる。[続き...]
  - id: B
    label: "カジュアルトーン"
    content: |
      正直に言います。AIに仕事を任せるとき、
      一番ハマったのはプロンプトの書き方でした。[続き...]
primary_metric: engagement_rate
secondary_metrics: [replies, likes]
guardrail_metrics: [unfollow_rate]
duration_days: 3
```

**トーンバリエーション:**

| タイプ | 特徴 | 例 |
|--------|------|-----|
| 専門的 | 権威・信頼感 | 「研究によると〜」「データが示す〜」 |
| カジュアル | 親近感・共感 | 「正直に言うと〜」「これ、驚きませんか？」 |
| 逆張り | 注目・議論喚起 | 「〇〇は間違いだった」「実は〜ではない」 |
| 教育的 | 学習促進 | 「今日学んだこと：〜」「〇〇について解説します」 |

### 2-5. 投稿時間

```yaml
id: exp-YYYY-MM-DD-005
channel: x_twitter
hypothesis: "Because morning commuters check Twitter, we believe 7-9am posts will outperform lunch-time posts for a B2B audience"
test_variable: timing
variants:
  - id: A
    label: "朝投稿（7:00-9:00）"
    content: "[同一コンテンツ]"
    scheduled_time: "07:30"
  - id: B
    label: "昼投稿（12:00-13:00）"
    content: "[同一コンテンツ]"
    scheduled_time: "12:30"
primary_metric: engagement_rate
secondary_metrics: [impressions, likes]
guardrail_metrics: []
duration_days: 7  # 複数サイクル必要
notes: "同一コンテンツを異なる日/時間に投稿。アルゴリズムの差異に注意"
```

**投稿時間帯ガイド（日本時間）:**

| 時間帯 | 対象 | 特徴 |
|--------|------|------|
| 7:00-9:00 | 通勤時間帯 | BtoB向け・ニュース消費 |
| 12:00-13:00 | 昼休み | 全般・エンタメ消費 |
| 19:00-22:00 | 帰宅後 | BtoC向け・深掘りコンテンツ |
| 土曜 10:00-12:00 | 週末午前 | 学習コンテンツ向け |

### 2-6. ハッシュタグ

```yaml
id: exp-YYYY-MM-DD-006
channel: x_twitter
hypothesis: "Because hashtags can feel spammy, we believe posts without hashtags will have higher engagement rate per impression"
test_variable: hashtag
variants:
  - id: A
    label: "ハッシュタグあり"
    content: |
      [本文] #AI #ChatGPT #業務効率化
  - id: B
    label: "ハッシュタグなし"
    content: |
      [本文（同一）]
primary_metric: engagement_rate
secondary_metrics: [impressions, reach]
guardrail_metrics: []
duration_days: 3
```

### 2-7. ツイート長さ

```yaml
id: exp-YYYY-MM-DD-007
channel: x_twitter
hypothesis: "Because shorter content is easier to consume, we believe posts under 100 characters will have higher engagement rate than posts over 200 characters"
test_variable: length
variants:
  - id: A
    label: "短文（100文字以下）"
    content: |
      AIに奪われる仕事より、AIで生まれる仕事の方が多い。
      あなたはその準備ができていますか？
  - id: B
    label: "長文（200文字以上）"
    content: |
      「AIに仕事を奪われる」という話をよく聞きます。
      でも実際のデータを見ると、逆のことが起きています。
      [詳細な説明を200文字以上で記述...]
primary_metric: engagement_rate
secondary_metrics: [likes, replies, retweets]
guardrail_metrics: []
duration_days: 3
```

---

## 3. メール テスト変数テンプレート（5種）

### 3-1. 件名（Subject Line）

```yaml
id: exp-YYYY-MM-DD-010
channel: email
hypothesis: "Because personalized subjects feel relevant, we believe name-personalized subjects will increase open rate"
test_variable: subject_line
variants:
  - id: A
    label: "ジェネリック件名"
    content:
      subject: "AIツール活用の最新ガイド"
      body: "[共通本文]"
  - id: B
    label: "パーソナライズ件名"
    content:
      subject: "{{first_name}}さんへ：AIツール活用の最新ガイド"
      body: "[共通本文]"
primary_metric: open_rate
secondary_metrics: [click_rate, unsubscribe_rate]
guardrail_metrics: [spam_reports, unsubscribe_rate]
duration_days: 7
```

**件名バリエーション:**

| タイプ | パターン | 例 |
|--------|---------|-----|
| パーソナライズ | 氏名・会社名挿入 | 「{{name}}さんへ」 |
| 数値使用 | 具体的数字 | 「5分で読める〇〇ガイド」 |
| 質問形 | 疑問文 | 「〇〇で困っていませんか？」 |
| 緊急性 | 期限・限定 | 「本日限り：〇〇無料」 |
| 利益提示 | ベネフィット直球 | 「週3時間を節約する方法」 |

### 3-2. プレヘッダー

```yaml
id: exp-YYYY-MM-DD-011
channel: email
hypothesis: "Because preheaders serve as a secondary subject line, we believe benefit-focused preheaders will increase open rate"
test_variable: preheader
variants:
  - id: A
    label: "情報型プレヘッダー"
    content:
      subject: "[共通件名]"
      preheader: "最新のAIツール活用事例をまとめました"
      body: "[共通本文]"
  - id: B
    label: "ベネフィット型プレヘッダー"
    content:
      subject: "[共通件名]"
      preheader: "読了後、今日から使える3つのテクニックが身につきます"
      body: "[共通本文]"
primary_metric: open_rate
secondary_metrics: [click_rate]
guardrail_metrics: [unsubscribe_rate]
duration_days: 7
```

### 3-3. 送信時間

```yaml
id: exp-YYYY-MM-DD-012
channel: email
hypothesis: "Because Tuesday mornings have high email engagement, we believe Tuesday 9am will outperform Thursday 2pm"
test_variable: send_time
variants:
  - id: A
    label: "火曜午前（9:00）"
    content: "[共通コンテンツ]"
    scheduled_time: "Tuesday 09:00 JST"
  - id: B
    label: "木曜午後（14:00）"
    content: "[共通コンテンツ]"
    scheduled_time: "Thursday 14:00 JST"
primary_metric: open_rate
secondary_metrics: [click_rate]
guardrail_metrics: [unsubscribe_rate]
duration_days: 14  # 2週間で1サイクル
notes: "リストをランダム2分割してA/Bに割り当て"
```

### 3-4. CTAボタンテキスト

```yaml
id: exp-YYYY-MM-DD-013
channel: email
hypothesis: "Because action-oriented CTAs reduce friction, we believe 'Start Now' will outperform 'Learn More' for click rate"
test_variable: cta_text
variants:
  - id: A
    label: "情報型CTA"
    content:
      subject: "[共通件名]"
      body: "[共通本文]"
      cta_button: "詳細を見る"
      cta_url: "https://example.com/detail"
  - id: B
    label: "行動型CTA"
    content:
      subject: "[共通件名]"
      body: "[共通本文]"
      cta_button: "今すぐ試す"
      cta_url: "https://example.com/detail"
primary_metric: click_rate
secondary_metrics: [conversion_rate]
guardrail_metrics: [unsubscribe_rate]
duration_days: 7
```

### 3-5. 本文長さ

```yaml
id: exp-YYYY-MM-DD-014
channel: email
hypothesis: "Because busy readers prefer concise emails, we believe shorter emails (under 300 words) will have higher click rate"
test_variable: body_length
variants:
  - id: A
    label: "短文メール（300文字以下）"
    content:
      subject: "[共通件名]"
      body: |
        [要点のみ・3文以内のメール本文]
        [CTA]
  - id: B
    label: "長文メール（800文字以上）"
    content:
      subject: "[共通件名]"
      body: |
        [詳細な説明・背景・事例を含むメール本文]
        [CTA]
primary_metric: click_rate
secondary_metrics: [open_rate, read_rate]
guardrail_metrics: [unsubscribe_rate]
duration_days: 7
```

---

## 4. LinkedIn テスト変数テンプレート（4種）

### 4-1. フック形式

```yaml
id: exp-YYYY-MM-DD-020
channel: linkedin
hypothesis: "Because LinkedIn users scroll quickly, we believe data-driven hooks will stop more scrollers than question hooks"
test_variable: hook
variants:
  - id: A
    label: "質問型フック"
    content: |
      AIを業務に導入しようとして失敗したことはありますか？
      [続き...]
  - id: B
    label: "数値引用型フック"
    content: |
      AI導入プロジェクトの67%が最初の3ヶ月で失敗する。
      [続き...]
primary_metric: engagement_rate
secondary_metrics: [comments, shares, impressions]
guardrail_metrics: []
duration_days: 5
```

### 4-2. フォーマット

```yaml
id: exp-YYYY-MM-DD-021
channel: linkedin
hypothesis: "Because visual content stands out in feed, we believe carousel posts will outperform text-only posts"
test_variable: format
variants:
  - id: A
    label: "テキストのみ"
    content: |
      [テキスト投稿（1200文字程度）]
  - id: B
    label: "カルーセル（PDF）"
    content:
      text: "[キャプション]"
      attachment: "carousel.pdf"
      slides_count: 8
primary_metric: engagement_rate
secondary_metrics: [impressions, shares]
guardrail_metrics: []
duration_days: 5
```

### 4-3. トーン

```yaml
id: exp-YYYY-MM-DD-022
channel: linkedin
hypothesis: "Because LinkedIn users value authentic stories, we believe personal story posts will outperform industry insight posts"
test_variable: tone
variants:
  - id: A
    label: "業界インサイト型"
    content: |
      2025年のAI活用トレンド分析：
      [客観的データ・業界視点で記述]
  - id: B
    label: "個人ストーリー型"
    content: |
      先月、私のチームで起きた話をシェアします。
      [個人体験・具体的エピソードで記述]
primary_metric: engagement_rate
secondary_metrics: [comments, profile_views]
guardrail_metrics: []
duration_days: 5
```

### 4-4. CTA

```yaml
id: exp-YYYY-MM-DD-023
channel: linkedin
hypothesis: "Because specific questions get more responses, we believe specific opinion questions will outperform generic CTAs"
test_variable: cta
variants:
  - id: A
    label: "汎用CTA"
    content: |
      [本文]
      皆さんのご意見をお聞かせください。
  - id: B
    label: "具体的質問CTA"
    content: |
      [本文]
      あなたの組織でAI導入の最大の障壁は何ですか？
      A) 予算  B) スキル不足  C) 文化的抵抗  D) その他
      コメントで教えてください。
primary_metric: comment_rate
secondary_metrics: [engagement_rate, shares]
guardrail_metrics: []
duration_days: 5
```

---

## 5. 実験管理ログ（記録用テンプレート）

```yaml
# experiment-log.yaml
experiments:
  - id: exp-2025-01-15-001
    channel: x_twitter
    test_variable: hook
    status: completed
    results:
      winner: B
      relative_improvement_pct: 23.5
      learnings: "質問型フックはリプライ率を23%向上させた。特にYes/No形式の質問が効果的だった"
  # 以降に追加していく
```
