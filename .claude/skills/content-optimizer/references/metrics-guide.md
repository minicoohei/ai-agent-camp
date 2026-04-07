# チャネル別KPI定義・取得方法・判定基準

コンテンツパフォーマンスを測定・評価するための指標ガイド。
A/Bテストの勝敗判定や改善サイクルの基盤となる。

---

## 1. X (Twitter) メトリクス

### 1-1. 主要指標一覧

| メトリクス | 定義 | 取得方法 | アクセス制限 | ベンチマーク |
|-----------|------|---------|------------|------------|
| **Engagement Rate** | (likes + RT + replies + quotes) / impressions | X API v2 `public_metrics` + `non_public_metrics` | 自アカウントのみ full data | 1-3%: Good, 3-5%: Great, 5%+: Viral |
| **Impressions** | ツイートが表示された回数（ユニーク含まず） | X API v2 `non_public_metrics` | 自アカウントのみ | フォロワー数の1-3倍が目安 |
| **Reach（Unique Views）** | ユニークユーザーへの表示回数 | X API v2 `non_public_metrics` | 自アカウントのみ | - |
| **Likes** | いいね数 | X API v2 `public_metrics` | 公開 | - |
| **Retweets** | RT数（引用RTは別カウント） | X API v2 `public_metrics` | 公開 | - |
| **Quote Tweets** | 引用RT数 | X API v2 `public_metrics` | 公開 | - |
| **Replies** | 返信数 | X API v2 `public_metrics` | 公開 | - |
| **Bookmarks** | ブックマーク数 | X API v2 `non_public_metrics` | 自アカウントのみ | - |
| **Profile Clicks** | プロフィールクリック数 | X API v2 `non_public_metrics` | 自アカウントのみ | - |
| **URL Clicks** | リンククリック数 | X API v2 `non_public_metrics` | 自アカウントのみ | - |

### 1-2. X API v2 取得方法

```python
# X API v2 でツイートのメトリクスを取得する例
import requests

def get_tweet_metrics(tweet_id: str, bearer_token: str) -> dict:
    """
    自アカウントのツイートメトリクスを取得（non_public_metrics も含む）
    """
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    params = {
        "tweet.fields": "public_metrics,non_public_metrics,created_at"
    }
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    tweet = data["data"]
    public = tweet.get("public_metrics", {})
    non_public = tweet.get("non_public_metrics", {})

    return {
        "tweet_id": tweet_id,
        "created_at": tweet.get("created_at"),
        # public metrics（他アカウントでも取得可）
        "likes": public.get("like_count", 0),
        "retweets": public.get("retweet_count", 0),
        "replies": public.get("reply_count", 0),
        "quotes": public.get("quote_count", 0),
        "bookmarks": public.get("bookmark_count", 0),
        # non_public metrics（自アカウントのみ）
        "impressions": non_public.get("impression_count", 0),
        "url_clicks": non_public.get("url_link_clicks", 0),
        "profile_clicks": non_public.get("user_profile_clicks", 0),
    }

def calc_engagement_rate(metrics: dict) -> float:
    """エンゲージメント率を計算"""
    impressions = metrics.get("impressions", 0)
    if impressions == 0:
        return 0.0
    engagements = (
        metrics.get("likes", 0)
        + metrics.get("retweets", 0)
        + metrics.get("replies", 0)
        + metrics.get("quotes", 0)
    )
    return round(engagements / impressions * 100, 2)
```

### 1-3. 注意事項

- `non_public_metrics`（impressions等）は**自アカウントのツイートのみ**取得可能
- 他アカウントのツイートは `public_metrics` のみ取得可能
- `verified` フィールドは v2 API で廃止済み（`USER_FIELDS` に含めないこと）
- Basicプランの場合、レート制限: 450リクエスト/15分

---

## 2. メール メトリクス

### 2-1. 主要指標一覧（Resend API 基準）

| メトリクス | 定義 | 計算式 | ベンチマーク |
|-----------|------|--------|------------|
| **Open Rate** | メールを開封した割合 | 開封数 / 配信成功数 | 20-30%: 一般的, 30%+: 優良 |
| **Click Rate** | リンクをクリックした割合 | クリック数（ユニーク）/ 配信成功数 | 2-5%: 一般的, 5%+: 優良 |
| **CTR（Click-to-Open Rate）** | 開封者のうちクリックした割合 | クリック数 / 開封数 | 10-20%: 一般的 |
| **Bounce Rate** | 配信失敗率 | バウンス数 / 送信数 | 2%以下が目標 |
| **Unsubscribe Rate** | 配信停止率 | 配信停止数 / 配信成功数 | 0.5%以下を維持 |
| **Spam Report Rate** | スパム報告率 | スパム報告数 / 配信成功数 | 0.08%以下（Googleガイドライン） |

### 2-2. Resend API 取得方法

```python
# Resend API でメールメトリクスを取得する例
import requests

def get_email_metrics(email_id: str, api_key: str) -> dict:
    """Resend API でメール配信結果を取得"""
    url = f"https://api.resend.com/emails/{email_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    return response.json()

def calc_email_stats(campaign_data: dict) -> dict:
    """メールキャンペーン統計を計算"""
    sent = campaign_data.get("sent", 0)
    delivered = campaign_data.get("delivered", 0)
    opened = campaign_data.get("opened", 0)
    clicked = campaign_data.get("clicked", 0)
    bounced = campaign_data.get("bounced", 0)
    unsubscribed = campaign_data.get("unsubscribed", 0)
    spam = campaign_data.get("complained", 0)

    return {
        "open_rate": round(opened / delivered * 100, 2) if delivered > 0 else 0,
        "click_rate": round(clicked / delivered * 100, 2) if delivered > 0 else 0,
        "ctr": round(clicked / opened * 100, 2) if opened > 0 else 0,
        "bounce_rate": round(bounced / sent * 100, 2) if sent > 0 else 0,
        "unsubscribe_rate": round(unsubscribed / delivered * 100, 2) if delivered > 0 else 0,
        "spam_rate": round(spam / delivered * 100, 2) if delivered > 0 else 0,
    }
```

---

## 3. 統計的有意性の判定

### 3-1. 基本的な考え方

A/Bテストの結果が「偶然の差ではなく、本当に変数の効果によるものか」を判定する。

| 判定指標 | 説明 | 基準 |
|---------|------|------|
| **p値** | 帰無仮説（差がない）が真である確率 | p < 0.05 で有意（95%信頼水準） |
| **信頼区間** | 真の改善率がどの範囲に収まるか | 0を含まなければ有意 |
| **検出力** | 真の差を検出できる確率 | 80%以上を目標 |

### 3-2. 最低サンプルサイズの目安

**前提: 信頼水準95%、検出力80%、最低検出差異（MDE）10%**

| ベースライン指標 | 改善率10%を検出するための最低サンプル数（片方） |
|----------------|----------------------------------------------|
| Open Rate 25% | 約 3,200 通（A/B 各1,600通） |
| Click Rate 3% | 約 17,500 通（A/B 各8,750通） |
| Engagement Rate 2% | 約 26,500 インプレッション（各13,250） |
| Engagement Rate 5% | 約 10,000 インプレッション（各5,000） |

> **注意**: サンプルが少ない場合、大きな差（20%以上）でないと統計的に有意と言えない。
> SNS投稿のように1投稿=1バリアントの場合、複数回の実験結果を蓄積してトレンドで判断する。

### 3-3. 簡易有意性チェック

```python
from scipy import stats
import math

def check_significance(
    impressions_a: int, engagements_a: int,
    impressions_b: int, engagements_b: int,
    confidence_level: float = 0.95
) -> dict:
    """
    2比率のZ検定で有意差を判定
    （エンゲージメント率などの比率指標に使用）
    """
    rate_a = engagements_a / impressions_a
    rate_b = engagements_b / impressions_b

    # プールされた比率
    p_pool = (engagements_a + engagements_b) / (impressions_a + impressions_b)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/impressions_a + 1/impressions_b))

    z_score = (rate_b - rate_a) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # 両側検定

    relative_improvement = (rate_b - rate_a) / rate_a * 100 if rate_a > 0 else 0

    return {
        "rate_a": round(rate_a * 100, 2),
        "rate_b": round(rate_b * 100, 2),
        "relative_improvement_pct": round(relative_improvement, 1),
        "z_score": round(z_score, 3),
        "p_value": round(p_value, 4),
        "is_significant": p_value < (1 - confidence_level),
        "confidence_level": confidence_level,
        "winner": "B" if (p_value < (1 - confidence_level) and rate_b > rate_a)
                  else "A" if (p_value < (1 - confidence_level) and rate_a > rate_b)
                  else "no_significant_difference"
    }
```

### 3-4. SNS特有の注意点

SNS投稿では1投稿が1バリアントになるため、単一投稿での厳密な有意性判定は困難。

**推奨アプローチ:**

1. **同一コンテンツ・異なる日時**: 時間帯テストのみに有効（コンテンツ変数を固定）
2. **複数回実験の蓄積**: 同じ変数で5回以上テストし、勝率でトレンド判定
3. **経験則の活用**: インプレッションが1,000以上かつ相対差が20%以上なら参考値として採用
4. **ガードレール重視**: 主要指標が「大差ない」でも、フォロワー減などガードレールに引っかかれば却下

---

## 4. パフォーマンス評価フレームワーク

### 4-1. 勝敗判定フロー

```
実験終了
    ↓
1. ガードレール指標を確認（unfollow_rate, spam_reports）
    ↓ いずれかが悪化 → B は不採用（Aを維持）
    ↓ 問題なし
    ↓
2. primary_metric の相対差を確認
    ↓ 差が10%未満 → 「有意差なし」として記録、次の変数をテスト
    ↓ 差が10%以上
    ↓
3. サンプルサイズが十分か確認（上記テーブル参照）
    ↓ 不十分 → 「参考値」として記録し、同条件で再テスト推奨
    ↓ 十分
    ↓
4. 勝者（A or B）を採用し、学習を記録
```

### 4-2. 実験結果記録テンプレート

```yaml
# 実験完了後に記入

experiment_id: exp-2025-01-15-001
completed_at: "2025-01-18"

results:
  variant_a:
    label: "コントロール（質問型フック）"
    impressions: 1240
    engagements: 18
    rate_pct: 1.45

  variant_b:
    label: "テスト（数値引用型フック）"
    impressions: 1180
    engagements: 31
    rate_pct: 2.63

  relative_improvement_pct: +81.4
  is_significant: true  # サンプルが少ないため参考値
  winner: B

learnings:
  what_worked: "数値引用型フックは質問型に比べ約80%高いエンゲージメント率を示した"
  hypothesis_confirmed: true
  caveats: "サンプルサイズが小さく、再現性の確認が必要"
  next_experiment: "同じBのフック形式を使い、CTA変数をテストする"

action:
  adopted: true
  implementation: "今後の投稿では数値引用型フックを標準パターンとして採用"
```

### 4-3. KPIダッシュボード（チャネル別目標値）

**X (Twitter) 月次目標:**

| KPI | 現状 | 短期目標（3ヶ月） | 中期目標（6ヶ月） |
|-----|------|----------------|----------------|
| Engagement Rate | - | 2.0% | 3.5% |
| Impressions/投稿 | - | 1,000 | 3,000 |
| フォロワー増加数/月 | - | +100 | +300 |

**メール 月次目標:**

| KPI | 現状 | 短期目標（3ヶ月） | 中期目標（6ヶ月） |
|-----|------|----------------|----------------|
| Open Rate | - | 25% | 35% |
| Click Rate | - | 3% | 6% |
| Unsubscribe Rate | - | <0.5% | <0.3% |

---

## 5. データ収集スケジュール

### 5-1. 測定タイミング

| チャネル | 指標 | 収集タイミング | 理由 |
|---------|------|-------------|------|
| X / Twitter | Engagement Rate | 投稿後24時間・72時間 | 初動とロングテールを分けて把握 |
| X / Twitter | Impressions | 投稿後72時間（実験終了時） | アルゴリズムによる遅延拡散を含める |
| メール | Open Rate | 送信後48時間 | 開封の85%は48時間以内に発生 |
| メール | Click Rate | 送信後7日間 | クリックはオープンより遅延することがある |
| LinkedIn | Engagement Rate | 投稿後5日間 | LinkedInはエンゲージメント寿命が長い |

### 5-2. 収集自動化（推奨コマンド）

```bash
# X APIでツイートメトリクスを収集（A/Bバリアント比較）
python skills/content-optimizer/scripts/collect_metrics.py \
  --tweet-ids "tweet_id_A,tweet_id_B" \
  --experiment-id "exp-2025-01-15-001"

# ユーザーの直近投稿メトリクスを一括取得
python skills/content-optimizer/scripts/collect_metrics.py \
  --username minicoohei \
  --output ./output/content-optimizer/metrics/
```

> **Note:** 現在の `collect_metrics.py` は X (Twitter) API v2 専用です。
> メール・LinkedIn メトリクスは Phase 3 以降で対応予定。
