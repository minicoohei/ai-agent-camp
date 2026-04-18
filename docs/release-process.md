# Release Process

ai-agent-camp の多言語リリースフローと、AI エージェント向けの参照仕様をまとめる。

---

## バージョニング方針

[Semantic Versioning 2.0.0](https://semver.org/lang/ja/) に準拠。

| 段階 | バージョン帯 | 何を意味するか |
|------|-------------|---------------|
| 初期フェーズ | `v0.x.y` | 公開後の初期安定化期間。後方互換を壊す変更も含まれうる |
| 安定版 | `v1.0.0` 以降 | メジャー変更はマニフェスト構造・スキル I/F・hook の互換性を壊す変更のみ |
| マイナー | `v*.Y.0` | レッスン追加、スキル追加、後方互換のある改善 |
| パッチ | `v*.*.Z` | ドキュメント、バグ修正、軽微な調整 |

1 タグ = 3 言語（ja / en / es）の同時リリース。言語ごとにタグは切らない。

---

## リリース手順（メンテナ向け）

### 1. 事前確認

```bash
# main が最新で、テストが全て通っている
git checkout main && git pull
uv run pytest tests/security/ -q
bash scripts/lint-skills-sync.sh

# 完全性チェックが通る
uv run python tools/scripts/verify_integrity.py
```

### 2. タグを切る

```bash
# 例: v0.1.0 をリリース
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

`tags: ['v*']` にマッチするため `.github/workflows/release.yml` が発火し、`[ja, en, es]` の matrix ビルドが並列で走る（約 5 分）。

### 3. 生成される成果物

同じ GitHub Release に、3 言語 × 2 ファイル = 6 アセットが添付される:

```
ai-agent-camp-ja-v0.1.0.zip
ai-agent-camp-ja-v0.1.0.zip.sha256
ai-agent-camp-en-v0.1.0.zip
ai-agent-camp-en-v0.1.0.zip.sha256
ai-agent-camp-es-v0.1.0.zip
ai-agent-camp-es-v0.1.0.zip.sha256
```

Release notes は `generate_release_notes: true` により前回タグ以降の PR/コミットから自動生成される。必要に応じて編集。

### 4. アナウンス

- GitHub Release を publish（draft にしていれば）
- ai-agent.camp 側の Web に反映通知（範囲外）

---

## zip アーカイブの中身

`tools/build_release.py --lang {lang} --strict --output dist/{lang}` の出力をそのまま zip 化したもの。

| パス | 内容 |
|------|------|
| `courses/` | 対象言語のレッスン本文（言語 suffix 除去済み） |
| `skills/` | スキル群 |
| `.claude/` / `.cursor/` | ツール別の commands / hooks |
| `docs/` | ドキュメント |
| `CHECKSUMS.txt` | zip 内全ファイルの sha256 |

`build_release.py` の挙動:
- `lessons.manifest.{lang}.yaml` → `lessons.manifest.yaml` にリネーム
- `*.{lang}.md` → `*.md` にリネーム
- 対応翻訳のない `*.md` は `--strict` 時は欠落エラー、非 strict 時は skip

---

## <a id="agent-meta-v1"></a>AGENT-META v1 仕様

README 冒頭の HTML コメントブロックは、AI エージェントが対象リポジトリとダウンロード先を機械的に解決するための参照情報。`<!-- AGENT-META v1` で始まり `-->` で終わる。中身は YAML サブセット。

### フィールド定義

| フィールド | 型 | 意味 |
|-----------|----|------|
| `repo` | string | 一次公式リポジトリ (`owner/name`) |
| `mirror` | string | ミラーの公式リポ |
| `primary_branch` | string | デフォルトブランチ名 |
| `languages` | list[string] | 対応言語コード (`ja` / `en` / `es`) |
| `default_language` | string | 言語を指定されなかった時のフォールバック |
| `latest_tag_api` | URL | `GET` で `tag_name` を取得できる GitHub API |
| `release_asset_pattern` | URL template | `{tag}` `{lang}` を埋めると pinned な zip URL になる |
| `manifest_raw_pattern` | URL template | `{ref}` `{lang_suffix}` を埋めるとマニフェスト生 URL になる |
| `lang_suffix` | map | `languages` → `manifest_raw_pattern` の `{lang_suffix}` に埋める文字列 |
| `integrity_cli` | string | 完全性検証コマンド |

### 互換性ルール

- フィールドの**追加**: `v1` のまま行って良い（既存 parser は追加フィールドを無視）
- フィールドの**削除／意味変更**: `<!-- AGENT-META v2` に bump し、ハードフォーク扱い
- v1 で定義されたフィールド名は予約（互換理由のためのリネームも不可）

### parse サンプル

```python
import re
import urllib.request
import yaml

URL = "https://raw.githubusercontent.com/TokenPocket/ai-agent-camp/main/README.md"
readme = urllib.request.urlopen(URL).read().decode("utf-8")
m = re.search(r"<!--\s*AGENT-META\s+v1\n(.*?)\n-->", readme, re.DOTALL)
meta = yaml.safe_load(m.group(1))
print(meta["release_asset_pattern"].format(tag="v0.1.0", lang="ja"))
# → https://github.com/TokenPocket/ai-agent-camp/releases/download/v0.1.0/ai-agent-camp-ja-v0.1.0.zip
```

---

## AI エージェントからの参照パターン

### 特定バージョンを pinned で取得

```python
meta = parse_agent_meta(readme)
url = meta["release_asset_pattern"].format(tag="v0.1.0", lang="en")
# → 常に同じ内容を返す
```

### 常に最新を追う

```python
import json
tag = json.loads(urllib.request.urlopen(meta["latest_tag_api"]).read())["tag_name"]
url = meta["release_asset_pattern"].format(tag=tag, lang="ja")
```

### マニフェストだけ軽く参照

```python
# main の最新 manifest (en)
suffix = meta["lang_suffix"]["en"]  # ".en"
url = meta["manifest_raw_pattern"].format(ref="main", lang_suffix=suffix)
# → https://raw.githubusercontent.com/.../main/courses/lessons.manifest.en.yaml
```

---

## ロールバック

重大な不具合が含まれていた場合:

### 即時対応: Release を draft 化

```bash
gh release edit v0.1.0 --draft
```

アセット URL は 404 になり、AI エージェントがダウンロードできなくなる。タグ自体は残る。

### 次パッチを即発火

```bash
# 修正コミット後
git tag -a v0.1.1 -m "Hotfix: <内容>"
git push origin v0.1.1
```

### タグ自体を消すケース

**原則避ける**（AI エージェントが pinned URL をキャッシュしている可能性）。どうしても消す場合:

```bash
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0
gh release delete v0.1.0
```

消したタグを後から再作成するのは禁止（SHA が変わると信頼の連鎖が壊れる）。

---

## チェックサム

zip 自体の sha256 は同梱の `*.zip.sha256` に 1 行で入る。検証例:

```bash
# 方法1: sha256 ファイルと照合
curl -fsSLO https://github.com/TokenPocket/ai-agent-camp/releases/download/v0.1.0/ai-agent-camp-ja-v0.1.0.zip
curl -fsSLO https://github.com/TokenPocket/ai-agent-camp/releases/download/v0.1.0/ai-agent-camp-ja-v0.1.0.zip.sha256
sha256sum -c ai-agent-camp-ja-v0.1.0.zip.sha256

# 方法2: zip 展開後、同梱の CHECKSUMS.txt で個別ファイルを検証
unzip -q ai-agent-camp-ja-v0.1.0.zip
cd ja
sha256sum -c CHECKSUMS.txt
```

`CHECKSUMS.txt` は zip 内の全ファイル（自身を除く）の sha256。

---

## 参考

- [Semantic Versioning 2.0.0](https://semver.org/lang/ja/)
- [softprops/action-gh-release](https://github.com/softprops/action-gh-release) — zip 添付に使用している GitHub Action
- [`tools/build_release.py`](../tools/build_release.py) — 言語別ビルド本体
- [`tools/i18n_utils.py`](../tools/i18n_utils.py) — 言語 suffix / 対応言語の定義
- [`docs/security-guardrails.md`](security-guardrails.md) — 完全性検証の背景
