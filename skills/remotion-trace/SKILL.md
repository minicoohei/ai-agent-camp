---
name: remotion-trace
description: |
  参考動画からプロ品質の Remotion 動画を再現するワークフロースキル。
  「参考動画から再現したい」「動画トレース」「PVを作りたい」「Remotion動画を参考動画ベースで作りたい」で使用。
---


# Remotion Video Trace

参考動画からプロ品質の Remotion 動画を再現するためのワークフロースキル。
企業PV制作の実プロジェクト（16イテレーション）で確立した手法を体系化。

## トリガーワード
「Remotion動画を作りたい」「PVを作りたい」「参考動画から再現」「動画トレース」

## 前提条件
- Node.js + Remotion (`mv-composer/` プロジェクト or 新規)
- ffmpeg (フレーム抽出・音声処理)
- yt-dlp (参考動画ダウンロード)

---

## Part 1: Reference Research（参考動画リサーチ）

### 1.1 参考動画ソース

目的に応じてソースを使い分ける:

| ソース | URL | 用途 |
|--------|-----|------|
| Vimeo Staff Picks | `vimeo.com/channels/staffpicks` | トランジション・カラーグレーディング |
| Art of the Title | `artofthetitle.com` | タイトルシーケンス・モーショングラフィックス |
| Stash Media | `stashmedia.tv` | CM・プロモ映像のトレンド |
| YouTube | 同業種・競合検索 | 企業PV・紹介動画の業界水準把握 |
| ゲームトレーラー | Brikk等 | ダイナミックなカット・エフェクト |

### 1.2 クリップ収集

「このシーンの表現が欲しい」単位で **5-10秒のクリップ** を収集する。動画全体ではなく、特定の演出・トランジションにフォーカス。

```bash
# YouTube/Vimeo からクリップ単位でダウンロード
yt-dlp --download-sections "*57-59" -o "data/video_refs/{project}/{id}_%(section_start)s-%(section_end)s.%(ext)s" "https://youtube.com/watch?v={id}"

# Vimeo の場合
yt-dlp --download-sections "*20-30" -o "data/video_refs/{project}/vimeo_{id}_0020-0030.%(ext)s" "https://vimeo.com/{id}"
```

### 1.3 ファイル管理

```
data/video_refs/{project_name}/
├── {videoId}_{startSec}-{endSec}.mp4   # 参考クリップ
├── frames/                              # 抽出フレーム（Part 2で生成）
└── README.md                           # 各クリップの出典・用途メモ
```

**必ず README.md に出典を記録**:
```markdown
## {videoId}_{start}-{end}.mp4
- 出典: {会社名} 公式PV (YouTube)
- 用途: 人物紹介のワイプ演出（暗背景→矩形飛散→写真露出）
```

---

## Part 2: Frame Analysis（フレーム分析）

### 2.1 フレーム抽出

```bash
# 参考動画からフレーム抽出（6-10fps推奨）
ffmpeg -i data/video_refs/{project}/clip.mp4 \
  -vf "fps=8" \
  data/video_refs/{project}/frames/clip_%04d.png

# 特定区間のみ抽出する場合
ffmpeg -i clip.mp4 -ss 2.0 -t 3.0 -vf "fps=10" frames/%04d.png
```

### 2.2 視覚分析チェックリスト

抽出フレームを Read ツールで開き、以下の観点で分析する:

- [ ] **トランジション手法**: ワイプ/フェード/スケール/clipPath/スライド
- [ ] **タイミング・イージング**: spring/ease-out/linear/ステップ
- [ ] **テキスト表現**: パンチイン/タイプライター/カスケード/スライドイン
- [ ] **背景処理**: 暗転/ブラー/パーティクル/グラデーション/画像overlay
- [ ] **色彩・コントラスト**: ブランドカラー/色温度/明暗バランス
- [ ] **レイアウト**: グリッド/フルブリード/分割/センタリング
- [ ] **BGM同期ポイント**: beat落ちでカット切り替え/テキスト出現

### 2.3 分析結果の記録

各クリップについて以下を記述:
```
## clip: {videoId}_{start}-{end}.mp4
### アニメーション分解
- 0.0s: 暗背景 + 白い矩形がランダム配置で飛散
- 0.5s: clipPath inset で左→右に写真がワイプイン
- 1.5s: 写真フル表示 + 左下に名前テロップ（白文字 shadow付き）
- 3.0s: 3ストリップに分割、各ストリップが別アングル
### Remotion実装メモ
- clipPath: `inset(0 ${100 - progress}% 0 0)` で実現可能
- 矩形飛散: position:absolute + ランダム top/left/rotation
```

### 2.4 draw.io PNG → React SVGアニメーション化ガイド

draw.io等で作成した図解PNGを、Remotion上のReact SVGアニメーションに変換する手順。

#### なぜ変換するか

| 観点 | PNG（そのまま） | React SVG |
|------|----------------|-----------|
| アニメーション | 不可（静止画） | 要素が `spring()` で順番に登場 |
| 解像度 | 拡大でぼやける | SVGはどんなサイズでもシャープ |
| 微調整 | draw.ioで再編集→再エクスポート | px値やタイミングをコードで即座に制御 |
| 2フェーズ遷移 | 不可 | 1シーンで前半/後半で異なる情報を表示可能 |

#### 変換手順

1. **構成要素の分解**: draw.ioの図をノード（ボックス）、矢印（コネクタ）、テキストラベルに分解。各要素の座標・サイズ・色をメモ
2. **Reactコンポーネント化**: 各要素をSVGプリミティブで再実装
   ```typescript
   // ノード → rect + text
   <rect x={node.x} y={node.y} width={node.w} height={node.h}
     rx={8} fill={node.color} opacity={nodeOpacity} />
   <text x={node.x + node.w/2} y={node.y + node.h/2}
     textAnchor="middle" dominantBaseline="central"
     fill="#FFF" fontSize={16}>{node.label}</text>

   // 矢印 → path or line
   <line x1={arrow.x1} y1={arrow.y1} x2={arrow.x2} y2={arrow.y2}
     stroke="#666" strokeWidth={2} markerEnd="url(#arrowhead)" />
   ```
3. **スタッガードアニメーション付与**: `spring()` で要素を順番に登場させる
   ```typescript
   const nodeOpacity = spring({
     frame: frame - index * STAGGER_DELAY,
     fps, config: { damping: 14, mass: 0.6, stiffness: 160 },
   });
   const nodeScale = spring({
     frame: frame - index * STAGGER_DELAY,
     fps, config: { damping: 14, mass: 0.6, stiffness: 160 },
   });
   // style: { opacity: nodeOpacity, transform: `scale(${nodeScale})` }
   ```
4. **座標管理**: 矢印のSVG path座標はTypeScript定数で管理し、ノード位置変更時に連動更新
   ```typescript
   const NODES = {
     input:   { x: 100, y: 200, w: 180, h: 60, color: '#3B82F6', label: 'Input' },
     process: { x: 400, y: 200, w: 180, h: 60, color: '#10B981', label: 'Process' },
     output:  { x: 700, y: 200, w: 180, h: 60, color: '#F59E0B', label: 'Output' },
   } as const;
   ```

#### チェック

静的PNGが `<Img>` で3秒以上表示されている場合 → 「アニメーション化を検討」フラグを出す。
motion-review スキルの **J3** チェック項目と連動。

---

## Part 3: BPM & Audio Analysis（音楽分析）

### 3.1 BPM解析

```bash
# 参考動画から音声抽出
ffmpeg -i reference.mp4 -vn -acodec pcm_s16le ref_audio.wav

# 手動カウント: 10秒間のbeat数を数えて × 6
# または ffmpeg のエネルギー検出で波形を可視化
ffmpeg -i ref_audio.wav -af "showinfo" -f null - 2>&1 | head -50
```

### 3.2 Beat-Aligned Duration 設計

```
BPM = 103 の場合:
1 beat = 60/103 = 0.5825s
5 beats = 2.91s
9 beats = 5.24s
```

**sectionDurations は必ず beat の整数倍にする**。これにより BGM の拍とシーン切り替えが自然に同期する。

### 3.3 BGM 生成（fal.ai Stable Audio）

**Stable Audio 2.5**（推奨）: 最大190秒を一発生成可能。ジョイント問題なし。

```javascript
// fal.ai Stable Audio 2.5（最大190秒）
const result = await fal.subscribe("fal-ai/stable-audio-25/text-to-audio", {
  input: { prompt: "...", seconds_total: 80 },
});
const url = result.data?.audio?.url;
```

```bash
# 末尾フェードアウト（4秒）を適用して mp3 に変換
ffmpeg -y -i raw.wav -af "afade=t=out:st=76:d=4" -q:a 2 bgm_final.mp3
```

**代替モデル（fal.ai）**:
| モデル | API ID | 最大尺 | 用途 |
|--------|--------|--------|------|
| Stable Audio 2.5 | `fal-ai/stable-audio-25/text-to-audio` | 190秒 | 汎用（推奨） |
| Beatoven maestro | `beatoven/music-generation` | 150秒 | ライセンス済み商用BGM |
| CassetteAI | `cassetteai/music-generator` | 180秒 | 低コスト高速 |
| Stable Audio (旧) | `fal-ai/stable-audio` | 47秒 | **非推奨**（分割+crossfadeが必要） |

**旧方式（47秒制限の場合のみ）**: 複数パートを crossfade で連結

```bash
ffmpeg -i part1.mp3 -i part2.mp3 \
  -filter_complex "[0][1]acrossfade=d=2:c1=tri:c2=tri" \
  -y bgm_full.mp3
```

### 3.4 ナレーション生成（ElevenLabs TTS）

TaxAccountantDemo v34-v40 で確立したワークフロー。

#### 3.4.1 音声生成
```bash
# ElevenLabs multilingual v2 + 日本語向け推奨設定
VOICE_ID="StTDrGrPSyfaHGmzwXbj"  # Masa（落ち着いた日本語男性）
SETTINGS='{"stability":0.70,"similarity_boost":0.80,"style":0.10,"use_speaker_boost":true}'

curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"text":"テキスト","model_id":"eleven_multilingual_v2","voice_settings":'"${SETTINGS}"'}' \
  --output "narration.mp3"
```

#### 3.4.2 中国語発音混入対策（重要）
ElevenLabs multilingual v2 は日本語の漢字を中国語読みすることがある。

**対策**: 問題が起きやすい漢字をひらがなに置換してから生成
```
税理士 → ぜいりし    記帳 → きちょう      仕訳 → しわけ
取引 → とりひき      損益 → そんえき      即時 → そくじ
即座 → そくざ        監視 → かんし        瞬時 → しゅんじ
24時間365日 → にじゅうよじかん さんびゃくろくじゅうごにち
12,800円 → いちまん にせん はっぴゃく えん
```


**stability を 0.55→0.70 に上げる**と中国語混入が減る。

#### 3.4.3 Gemini 発音評価（必須QA）
```python
import google.generativeai as genai
model = genai.GenerativeModel("gemini-2.0-flash")
audio = genai.upload_file("narration.mp3")
resp = model.generate_content([
    audio,
    "この日本語音声を正確に書き起こしてください。"
    "中国語の発音が混入していないか、読み間違いがあれば指摘。"
])
```
全クリップに対して実行し、問題があるクリップのみ再生成。

#### 3.4.4 atempo 速度調整
ナレーション尺がシーン尺を超える場合、ffmpeg atempo で調整:
```bash
# 例: 5.1秒のナレーションを3.6秒に収める（atempo 1.42）
ffmpeg -y -i raw.mp3 -af "atempo=1.42" adjusted.mp3
```
**限界**: atempo 1.35倍が上限。超えると早口で聞き取りづらい → テキストを短縮するか、シーン尺を延長。

#### 3.4.5 Remotion への組み込み
```typescript
// props にナレーションプレフィックスを定義
interface Props {
  narrationPrefix?: string;  // e.g. "tax/audio/narration/v4_s"
}

// 各シーンに Audio を配置
{p.narrationPrefix && starts.map((st, i) => {
  const padNum = String(i + 1).padStart(2, "0");
  return (
    <Sequence key={`narr-${i}`} from={st} durationInFrames={frames[i]}>
      <Audio src={staticFile(`${p.narrationPrefix}${padNum}.mp3`)} volume={1.2} />
    </Sequence>
  );
})}
```

**音量バランス**: ナレーション `volume={1.0-1.2}`, BGM `volume={0.18-0.25}`

### 3.5 音声ルール
- **SE なし・BGM 一本で駆け抜ける**のが基本スタイル
- 転調は動画が 45秒超の場合のみ検討
- ライブ映像等の直接挿入時は `muted` で BGM と干渉させない
- **ナレーション付き動画**: BGM volume を 0.20-0.25 に下げてナレーションを際立たせる
- **キャプションとナレーションの整合**: キャプションテキストはナレーション内容と一致させる（数値の%表記も統一）

---

## Part 4: Storyboard（絵コンテ作成）

### 4.1 シーン分割表

以下のテンプレートで全シーンを定義してから実装に入る:

| Scene | 秒数 | Beat数 | 参考クリップ | 演出概要 | コンポーネント名 |
|-------|------|--------|-------------|---------|----------------|
| 01 | 2.91 | 5 | {clip_id} | ロゴ blur→focus + パーティクル | LogoFocusIn |
| 02 | 2.91 | 5 | {clip_id} | バリュー訴求パンチイン | ValuePunch |
| 03 | 5.24 | 9 | {clip_id} | メンバー紹介ワイプ | MemberShowcase |
| ... | | | | | |

### 4.2 Props インターフェース設計

```typescript
interface CompositionProps {
  // 全シーン共通
  bgmSrc?: string;
  sectionDurations?: number[];  // Beat-aligned

  // シーン固有 props
  logoSrc?: string;
  // ...
}

export const DEFAULT_PROPS: CompositionProps = {
  sectionDurations: [2.91, 2.91, 5.24, 5.24, 12.23, 6.99, 8.74], // BPM倍数
  bgmSrc: '{project}/audio/bgm.mp3',
  // ...
};
```

### 4.3 sectionDurations 優先

**sectionDurations 配列を先に確定** → 各シーンコンポーネントはフレーム数を受け取って内部で配分。Root.tsx の `durationInFrames` は `Math.round(sum(sectionDurations) * FPS)` で自動計算。

---

## Part 5: Implementation Patterns（Remotion テクニック集）

企業PV制作で確立した 13 のテクニック。新プロジェクトでもそのまま適用可能。

### P1: Blur→Focus ロゴ
```typescript
const blurPx = interpolate(frame, [0, 20], [20, 0], { extrapolateRight: 'clamp' });
// style: { filter: `blur(${blurPx}px)` }
```
ロゴ画像を最初ぼかして徐々にシャープに。テキストでロゴを再現しない（フォント不一致リスク）。

### P2: パンチインテキスト
```typescript
const scale = spring({ frame: f, fps, config: { damping: 12, mass: 0.5, stiffness: 200 } });
// style: { transform: `scale(${scale})`, opacity: Math.min(1, f / 5) }
```
テキストが弾むように出現。`damping` を低くしすぎると振動が目立つので 10-15 が適正。

### P3: clipPath ワイプ
```typescript
const progress = interpolate(frame, [startF, endF], [0, 100], { extrapolateRight: 'clamp' });
// style: { clipPath: `inset(0 ${100 - progress}% 0 0)` }
```
右→左に写真がワイプイン。方向は `inset()` の値を変えるだけ。

### P4: 矩形飛散→写真ワイプ
暗背景にランダム配置の白/色付き矩形を散らし、clipPath で写真を露出させる二段階演出。
```typescript
// Phase A: 矩形飛散（テキストは入れない）
{rects.map((r, i) => (
  <div key={i} style={{
    position: 'absolute', top: r.y, left: r.x,
    width: r.w, height: r.h, background: r.color,
    transform: `rotate(${r.rot}deg)`,
    opacity: interpolate(f, [0, phaseAEnd], [1, 0])
  }} />
))}
// Phase B: clipPath で写真ワイプ
```

### P5: 3ストリップ分割
画面を縦3分割し、各ストリップに異なるアングルの写真を配置。ストリップごとに微妙にタイミングをずらすとリッチに見える。

### P6: Apple風カードグリッド
```typescript
const scrollY = interpolate(frame, [0, dur], [0, -totalHeight], { extrapolateRight: 'clamp' });
// グリッドを translateY でスクロール
// 特定カードでデセラレーション → カーソル追従 → クリック演出
```
カーソル位置はスクロールオフセットからカードの実画面座標を逆算して合わせる。

### P7: 4パネルスタガー
```typescript
const panelDelay = panelIndex * 4; // フレーム単位のずらし
const slideIn = interpolate(frame - panelDelay, [0, 15], [100, 0], { extrapolateRight: 'clamp' });
// 各パネルの baseOffset で異なる画像を表示
const imgIdx = (cycleIndex + pi * Math.ceil(images.length / 4)) % images.length;
```
4分割パネルの更新タイミングをずらす。**全パネル同じ画像にならないよう `baseOffset` 必須**。

### P8: カウントアップ
```typescript
// spring() は振動するので絶対使わない
const eased = 1 - Math.pow(1 - ratio, 3); // cubic ease-out
const displayNum = Math.round(eased * targetNumber);
```
**spring() でカウントアップすると数値が上がって下がって戻る。cubic ease-out を使うこと。**

### P9: CSS パーティクル
```typescript
// i2v の代替。position:absolute + CSS animation で浮遊ドット
{particles.map((p, i) => (
  <div key={i} style={{
    position: 'absolute', borderRadius: '50%',
    width: p.size, height: p.size, background: p.color,
    top: `${p.y}%`, left: `${p.x}%`, opacity: p.opacity,
    animation: `float ${p.duration}s ease-in-out infinite`,
  }} />
))}
```
**i2v（Kling等）は品質が微妙** → CSS パーティクルやRemotionアニメーションで代替する。

### P10: SceneWrap exit
```typescript
const exitProgress = interpolate(frame, [dur - exitFrames, dur], [0, 1], { extrapolateLeft: 'clamp' });
// style: { transform: `scale(${1 - 0.05 * exitProgress})`, opacity: 1 - exitProgress }
```
シーン終了時に `scale: 0.95` + `opacity: 0` で自然に次シーンへ遷移。`noExit` prop で無効化可能。

### P11: 顔保護
```typescript
// objectFit: "cover" は顔が切れる → "contain" + blurred background
<div style={{ position: 'relative', overflow: 'hidden' }}>
  {/* ブラー背景 */}
  <Img src={src} style={{ position: 'absolute', width: '120%', filter: 'blur(20px)', objectFit: 'cover' }} />
  {/* メイン画像 */}
  <Img src={src} style={{ position: 'relative', objectFit: 'contain', width: '100%', height: '100%' }} />
</div>
```

### P12: テキスト可読性
```typescript
// 黒帯はダサい → text-shadow で可読性確保
style: {
  textShadow: '0 2px 8px rgba(0,0,0,0.8), 0 0 20px rgba(0,0,0,0.5), 0 0 40px rgba(0,0,0,0.3)',
  // フォントサイズは大きめに（最低 48px）
}
```

### P13: 動画直挿入
```typescript
import { OffthreadVideo } from 'remotion';
// <OffthreadVideo src={staticFile('{project}/video/live_muted.mp4')} muted />
```
ライブ映像等は `muted` で挿入し、BGM トラックと干渉させない。サムネイルは ffmpeg で事前抽出:
```bash
ffmpeg -i video.mp4 -ss 5 -frames:v 1 thumb.jpg
```

---

## Part 6: Comparison Loop（比較改善ループ）

### 6.1 レンダリング

```bash
cd mv-composer
npx remotion render src/index.ts {CompositionId} out/{Name}_v{N}.mp4
```

### 6.2 出力動画のフレーム抽出

```bash
ffmpeg -i out/{Name}_v{N}.mp4 -vf "fps=8" data/video_refs/{project}/output_frames/v{N}_%04d.png
```

### 6.3 比較分析

参考動画フレームと出力フレームを並べて、**プロの映像クリエイター視点** で以下をチェック:

- [ ] タイミングのズレ（フレーム単位で比較）
- [ ] イージングの質（機械的 vs 有機的）
- [ ] 色温度・コントラストの差
- [ ] テキストの級数・配置・可読性
- [ ] 画像のクロップ・アスペクト比（顔切れ）
- [ ] BGM 同期ポイントのズレ
- [ ] 「死んでるフレーム」（動きのない静止区間 0.5秒以上）
- [ ] シーン間の黒フレーム（意図しない暗転）
- [ ] 重複表示（同じテキスト/画像が2回出る等）

### 6.4 修正→再レンダリング

指摘事項を修正 → `v{N+1}` としてレンダリング → 再度比較。
**v1→v18 のような反復は正常。5-10回のイテレーションで収束するのが標準。**

---

## Part 7: Lessons Learned（禁止事項・推奨事項）

### 禁止
| ルール | 理由 |
|--------|------|
| 絵文字をアイコンに使わない | レンダリング環境でフォント欠落 → SVG/画像を使う |
| i2v（Kling/fal.ai等）に頼らない | 品質が微妙、Remotion CSS で代替可能 |
| spring() でカウントアップしない | 振動して数値が上がって下がる |
| objectFit "cover" で人物写真 | 顔が切れる → "contain" + blurred bg |
| 黒帯テロップ | ダサい → text-shadow で可読性確保 |
| 7MB超の画像をそのまま使う | デコードエラー → `sips --resampleWidth 1200` |
| テキストでロゴを再現 | フォント不一致 → ロゴ画像を使う |

### 推奨
| ルール | 理由 |
|--------|------|
| SE なし・BGM 一本 | 駆け抜ける勢いが出る |
| sectionDurations を BPM 倍数に | 音ハメが自然になる |
| 画像は 1200px 幅以下にリサイズ | Remotion のデコード安定性 |
| シーン間を ±5フレーム オーバーラップ | 黒フレーム防止 |
| 名前テロップは1シーン1回 | 2回出ると違和感 |
| パネル画像は baseOffset で分散 | 全パネル同じ画像防止 |
| ライブ映像は muted 挿入 | BGM との干渉防止 |
| ブランドカラーは OGP/公式サイトから取得 | 目視推定は不正確 |

---

## ワークフロー全体像

```
[1. Reference Research]
  ↓ 参考クリップ収集（5-10秒単位）
[2. Frame Analysis]
  ↓ フレーム抽出 → 演出分解
[3. BPM & Audio]
  ↓ テンポ解析 → sectionDurations 確定 → BGM 生成
[4. Storyboard]
  ↓ シーン分割表 → Props設計
[5. Implementation]
  ↓ パターン集（P1-P13）を活用して実装
[6. Comparison Loop]  ←─── 5-10回反復
  ↓ レンダリング → フレーム比較 → 修正
[7. Final Check]
  ↓ Lessons Learned チェック → 完成
```
