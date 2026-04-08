# データ分析のヒント

## pandas 基本操作

```python
import pandas as pd

# CSV読み込み
df = pd.read_csv("data/sales-data.csv")

# 基本情報確認
df.info()           # カラム型、欠損値
df.describe()       # 基本統計量
df.head(10)         # 先頭10行

# 日付型変換
df["date"] = pd.to_datetime(df["date"])

# グループ集計
monthly = df.groupby(df["date"].dt.month)["amount"].sum()
category = df.groupby("category")["amount"].agg(["sum", "mean", "count"])

# データ結合
customers = pd.read_csv("data/customer-data.csv")
merged = df.merge(customers, on="customer_id", how="left")
```

## matplotlib 可視化

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.family"] = "Hiragino Sans"  # macOS日本語フォント

# 折れ線グラフ
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly.index, monthly.values, marker="o")
ax.set_xlabel("月")
ax.set_ylabel("売上金額（円）")
ax.set_title("月別売上推移")
plt.tight_layout()
plt.savefig("output/charts/monthly-sales.png", dpi=150)

# 棒グラフ
fig, ax = plt.subplots(figsize=(10, 6))
category_sales.plot(kind="bar", ax=ax)
ax.set_title("カテゴリ別売上")
plt.tight_layout()
plt.savefig("output/charts/category-sales.png", dpi=150)

# 円グラフ
fig, ax = plt.subplots(figsize=(8, 8))
category_sales.plot(kind="pie", ax=ax, autopct="%1.1f%%")
ax.set_title("カテゴリ別売上比率")
plt.savefig("output/charts/category-pie.png", dpi=150)
```

## seaborn 活用

```python
import seaborn as sns

# ヒートマップ
pivot = df.pivot_table(values="amount", index="region", columns="category", aggfunc="sum")
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(pivot, annot=True, fmt=",.0f", cmap="Blues", ax=ax)
plt.tight_layout()
plt.savefig("output/charts/region-category-heatmap.png", dpi=150)

# ボックスプロット
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=merged, x="member_rank", y="amount", ax=ax)
ax.set_title("会員ランク別購入金額分布")
plt.savefig("output/charts/rank-boxplot.png", dpi=150)
```

## ABC分析のコード例

```python
product_sales = df.groupby("product_id")["amount"].sum().sort_values(ascending=False)
cumsum = product_sales.cumsum()
cumsum_pct = cumsum / product_sales.sum() * 100

def classify_abc(pct):
    if pct <= 80:
        return "A"
    elif pct <= 95:
        return "B"
    else:
        return "C"

abc_rank = cumsum_pct.apply(classify_abc)
```
