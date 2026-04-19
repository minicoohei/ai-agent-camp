---
name: motion-review
description: "Remotionコンポジションを20項目チェックリストで品質レビューする。 「動画レビュー」「motion review」「Remotion品質チェック」等のリクエストで発動。"
triggers:
  - 動画レビュー
  - 動画の品質チェック
  - motion review
  - motion-review
  - Remotion品質チェック
  - PVレビュー
  - video review
---

# Motion Review Skill

Remotion コンポジションをプロの動画クリエイター視点でレビューし、品質改善指示を出すスキル。
GTM Manager / Campaign Orchestrator の Quality Review ステップで自動的に呼び出される。

## トリガーワード

`motion review`, `video review`, `動画レビュー`, `PVレビュー`, `Remotion品質チェック`

## 入力

- Remotion コンポジションファイルのパス（`.tsx`）
- （任意）レンダリング済み mp4 のパス

## 実行フロー

```
1. Read composition .tsx
2. Run 26-point checklist (A-I categories below)
3. Output structured review with P1/P2/P3 ratings
4. If any P1 exists → VERDICT: FIX_REQUIRED
5. If P2 only → VERDICT: FIX_RECOMMENDED
6. If P3 only → VERDICT: PASS
```

## Tone（レビュー出力の文体）

- 「プロの映像ディレクターが納品前に最終チェックする」トーン
- 各チェック項目は「OK — 理由」「P1/P2/P3 — 現状 → 修正指示」の形式。感想や曖昧な形容詞は使わない
- 良い点を1-2行で認めてから問題点に入る（例: 「A1 OK — OVERLAPが12f確保されており黒フレームなし。B1 P1 — spring configが全要素 damping:12 のみ → snappy/balanced/weighty/liquid の4段階に分離」）
- 修正指示は「ファイル名:行番号 + 現状コード + 修正後コード」の3点セットで出す

## トレードオフ判断基準

- P1を全て潰す > P2を多数潰す（P1が1つでもあればFIX_REQUIRED）
- interpolateで確実に静止 > springで見栄え良くするが振れるリスク
- シーン分割して情報密度を下げる > 1シーンに詰め込んで尺を節約する
- OVERLAPを大きめ(12f)にして安全マージン > 最小(4f)にしてシーンを長く取る

---

## 26-Point Pro Review Checklist

### Category A: シーン遷移（Transitions）

#### A1. シーン間の黒フレーム [P1]

**チェック**: Sequence が OVERLAP フレーム分重なっているか？
- NG: 非オーバーラップの Sequence（`from={starts[i]}` が前シーンの終了と一致）
- OK: `from={starts[i] - OVERLAP}`, `durationInFrames={frames[i] + OVERLAP * 2}`
- **判定基準**: 2フレーム以上の黒が入ったら P1

```typescript
// NG
<Sequence from={starts[1]} durationInFrames={frames[1]}>
// OK
<Sequence from={starts[1] - OVERLAP} durationInFrames={frames[1] + OVERLAP * 2}>
```

#### A1.5. クロスフェード＋ズームトランジション [P1]

**チェック**: フェーズ間が CrossFadeWrap（opacity fade + subtle scale）で滑らかに繋がっているか？
- NG: 白フラッシュ(opacity 0.85)のハードカットのみ → ぶつ切り感
- OK: XFADE=10フレーム(0.33秒)のオーバーラップ + 退場時 `scale(1.0→1.03)` で奥行き感 + 補助的な薄いフラッシュ(opacity 0.2)
- **判定基準**: Sequence 間に opacity crossfade がなければ P1
- **実装パターン**:
```typescript
const XFADE = 10;
const CrossFadeWrap: React.FC<{children; isFirst?; isLast?}> = ({children, isFirst, isLast}) => {
  const frame = useCurrentFrame();
  const { durationInFrames: dur } = useVideoConfig();
  const fadeIn = isFirst ? 1 : interpolate(frame, [0, XFADE], [0, 1], {extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const fadeOut = isLast ? 1 : interpolate(frame, [dur-XFADE, dur], [1, 0], {extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  const scaleOut = isLast ? 1 : interpolate(frame, [dur-XFADE, dur], [1, 1.03], {extrapolateLeft:"clamp",extrapolateRight:"clamp"});
  return <AbsoluteFill style={{opacity: fadeIn*fadeOut, transform:`scale(${scaleOut})`}}>{children}</AbsoluteFill>;
};
// Offsets with overlap
for (let i = 0; i < frameDurations.length; i++) {
  offsets.push(acc);
  acc += frameDurations[i] - (i < frameDurations.length - 1 ? XFADE : 0);
}
```
- **フラッシュは補助のみ**: opacity 0.2以下。0.5超の白フラッシュは P1（目が痛い＋ぶつ切り感）

#### A2. トランジション手法の多様性 [P2]

**チェック**: 全シーンが同じ exit/entrance パターンになっていないか？
- NG: すべて `opacity fade` のみ
- OK: Direction Blur, clipPath wipe, scale zoom, flash wipe を混在
- **判定基準**: 3種類以上のトランジション手法があれば OK

#### A3. clipPath の連続性 [P2]

**チェック**: Before→After 等の対比シーンで clipPath wipe が連動しているか？
- NG: S03 exit と S04 entrance が別タイミングで黒が入る
- OK: Sequence overlap + 方向一致（S03 右ワイプ退場 → S04 左ワイプ入場）

---

### Category B: モーション品質（Motion Quality）

#### B1. Spring Profile の差別化 [P1]

**チェック**: 要素の重さに応じた異なる spring config が使われているか？
- NG: 全要素が同じ `{ damping: 12, mass: 0.5, stiffness: 200 }`
- OK: 最低4段階（snappy / balanced / weighty / liquid）を使い分け
- **判定基準**: 2種類以下なら P1

```typescript
// 最低限のプロファイル
const SP = {
  snappy:   { damping: 8,  mass: 0.2, stiffness: 250 }, // アクセント線、バッジ
  balanced: { damping: 12, mass: 0.4, stiffness: 180 }, // テキスト
  weighty:  { damping: 16, mass: 0.8, stiffness: 120 }, // ロゴ、ウィンドウ
  liquid:   { damping: 20, mass: 1.2, stiffness: 60 },  // 背景装飾
};
```

#### B2. セカンダリ・モーション [P2]

**チェック**: 以下のうち2つ以上が実装されているか？
- [ ] Post-landing breathing（着地後の sin 波微動 ±1-2%）
- [ ] Follow-through rotation（入場時の微小回転 ±2-3deg）
- [ ] Scale bounce（scale 0.9→1.0 を opacity と同時）
- [ ] Post-count pulse（数字カウントアップ完了後の脈動）
- [ ] Drift（全文字入場後の上方ドリフト + 微拡大）

#### B3. BPM 同期 [P2]

**チェック**: sectionDurations とアニメーション delay がビートグリッドに乗っているか？
- NG: `sectionDurations: [3, 3, 2.5, 3]`（非整数ビート）、`delay={14}`（任意フレーム数）
- OK: `sectionDurations: [3, 3, 2.4, 3]`（beat 倍数）、`delay={beat(1)}`（18フレーム単位）
- **判定基準**: BGM の BPM を確認 → `60 / BPM * fps` = 1 beat のフレーム数

```typescript
const BEAT = 18; // 140 BPM @30fps
const beat = (n: number) => n * BEAT;
```

---

### Category C: 映像品質（Visual Polish）

#### C1. Film Grain のアニメーション [P1]

**チェック**: Film Grain が毎フレーム変化するか？
- NG: 固定 seed（`seed='2'`）→ フリーズテクスチャ = ないほうがマシ
- OK: `seed={frame % 5}` でフレームごとにローテーション
- **判定基準**: 固定 seed で Film Grain があったら P1（削除 or 修正）

#### C2. 背景の Ken Burns [P2]

**チェック**: i2v / 画像背景に微ズーム（Ken Burns）があるか？
- NG: `<OffthreadVideo>` がそのまま（壁紙貼り付け感）
- OK: 親 div に `scale(1.0 → 1.05-1.08)` を `interpolate` で適用
- **判定基準**: 背景が完全に静止していたら P2

#### C3. Vignette + Grain + ScanLines [P3]

**チェック**: 以下の映像フィルターが適用されているか？
- [ ] Vignette（radial-gradient, intensity 0.3-0.4）
- [ ] Film Grain（animated, opacity 0.03-0.05, mix-blend-mode: overlay）
- [ ] Scan Lines（repeating-linear-gradient, opacity 0.01-0.02）
- **判定基準**: 1つもなければ P2、1つあれば P3

---

### Category D: タイポグラフィ（Typography）

#### D1. フォントサイズの視認性 [P1]

**チェック**: 1080p 動画で最小テキストが読めるか？
- NG: 結果行 14px、ラベル 12px（動画再生時に判読不能）
- OK: 本文 18px 以上、ラベル 14px 以上
- **判定基準**: 18px 未満の本文テキストがあったら P1

| 用途 | 最小サイズ | 推奨サイズ |
|------|----------|----------|
| メインタイトル | 52px | 58-72px |
| サブタイトル | 36px | 42-48px |
| 本文 | 18px | 20-24px |
| ラベル・キャプション | 14px | 16-18px |
| 数字（カウントアップ） | 80px | 100-120px |

#### D2. タイポ基本設定 [P3]

**チェック**: 以下が設定されているか？
- [ ] `WebkitFontSmoothing: "antialiased"`
- [ ] `textRendering: "optimizeLegibility"`
- [ ] `lineHeight` が明示的に指定されている
- [ ] `letterSpacing` が体系的（tight / normal / wide / label の4段階程度）
- [ ] 数字フォントと日本語フォントの baseline が `alignItems: "baseline"` で揃っている

---

### Category E: 色彩・レイアウト（Color & Layout）

#### E1. 色温度のシフト [P3]

**チェック**: 全シーンが同じ色調でないか？
- NG: 全シーン `rgba(0,0,0,${overlay})` で同じ黒オーバーレイ
- OK: Before=暖色寄り `rgba(20,5,0,...)`, After=寒色寄り `rgba(0,0,20,...)`, CTA=ゴールド `rgba(10,5,0,...)`
- **判定基準**: 3シーン以上で色温度が変わっていれば OK

#### E2. レイアウトの非対称性 [P2]

**チェック**: 全シーンが中央揃えになっていないか？
- NG: 全シーン `alignItems: "center"`, `textAlign: "center"`
- OK: 左寄せ → 右寄せ → 中央 と視線がジグザグ移動
- **判定基準**: 3シーン以上が完全中央揃えなら P2

---

### Category F: コンテンツ＆タイミング整合性（Content & Timing Integrity）

v30-v36 の実制作イテレーションで発見された実践的バグを体系化。

#### F1. タイピングアニメーションのフレーム計算 [P1]

**チェック**: TYPING_END が PAUSE_AT のフレーム数を含んでいるか？
- NG: `TYPING_END = TYPING_START + text.length * TYPING_SPEED`（ポーズフレーム未計上 → タイプ途中で切れる）
- OK: `TYPING_END = TYPING_START + Math.ceil(text.length * TYPING_SPEED) + PAUSE_AT.length * PAUSE_FRAMES`
- **検出方法**: `TYPING_END` の計算式に `PAUSE_AT` / `PAUSE_FRAMES` が含まれているか grep で確認
- **修正パターン**: LPCreationDemo.tsx 参照（33f 不足していた実例）

#### F2. サブピクセルレンダリングのぼやけ [P1]

**チェック**: `interpolate()` の結果を translateY/X に直接使っていないか？
- NG: `transform: translateY(${interpolate(frame, [0, 100], [200, -400])}px)` → 小数値でテキスト/チャートがぼやける
- OK: `transform: translateY(${Math.round(interpolate(frame, [0, 100], [200, -400]))}px)`
- **検出方法**: `interpolate(` を含む行で `translateY|translateX|scrollY|top|left` を検索 → `Math.round()` 未ラップなら NG
- **例外**: `opacity`, `scale`, `rotate` は小数値が必要なので対象外
- **修正パターン**: CompetitorAnalysisDemo.tsx のレーダーチャートぼやけ修正を参照

#### F3. 背景上のテキスト可読性 [P1]

**チェック**: テキスト色と背景色のコントラスト比が WCAG AA (4.5:1) 以上か？
- NG: 明るいグラデーション背景に白テキスト `color: "#FFF"` → 読めない
- NG: 暗い背景に暗いテキスト `color: "#1E293B"` → 同様に読めない
- OK: 背景の明度に応じたテキスト色 + `textShadow` でコントラスト確保
- **検出方法**: 各シーンの `backgroundColor` / `background` と `color` プロパティの組み合わせを目視チェック
- **修正パターン**: MeshGradientTransition.tsx で白→ダークネイビーに変更した実例。画像背景上のテキストには `textShadow: "0 4px 40px rgba(0,0,0,0.9)"` を追加

#### F4. ロゴ/画像の透明度と背景干渉 [P2]

**チェック**: アルファチャンネル付き PNG が暗い背景で消えていないか？
- NG: 黒ロゴテキストの透明 PNG を `backgroundColor: "#000"` の上に直接配置 → ロゴが見えない
- OK: 白い半透明バッキングパネル `background: "rgba(255,255,255,0.95)"` を挿入
- **検出方法**: `<Img>` / `staticFile()` で `.png` を読み込んでいるシーンの親要素の `backgroundColor` を確認
- **修正パターン**: ShowcaseClosing.tsx で logo_aia.png の背後に白パネルを追加した実例

#### F5. スクロール範囲とコンテンツ量の整合 [P2]

**チェック**: parallax スクロールの `interpolate` 出力範囲がコンテンツ量に対して十分か？
- NG: 3列×5枚=15画像に対して 3列×3枚用のスクロール範囲 `[150, -350]` → 下の画像が表示されない
- OK: `scrollRange = rows * (IMG_HEIGHT + IMG_GAP)` を基準に設定
- **検出方法**: `columns` 配列の行数 × `(IMG_HEIGHT + IMG_GAP)` の合計と `interpolate` の `[start, end]` 範囲を比較
- **修正パターン**: CourseShowcase.tsx で 9枚→15枚増加時にスクロール範囲を `[250, -650]` に拡大した実例

#### F6. カードスタッガーのセクション超過 [P1]

**チェック**: `index * staggerDelay` の最大値がセクションの `durationInFrames` を超えていないか？
- NG: 6枚カード × 120f = 最大 cardStart 615f、しかしセクション 360f → カード 4-6 が表示されない
- OK: `(items.length - 1) * staggerDelay + springSettleFrames < durationInFrames`
- **検出方法**: `.map((item, index)` を含むコンポーネントで `index *` を検索。`(length - 1) * delay + 30f(settle)` が親 Sequence duration 以下か計算
- **修正パターン**: VoiceRush.tsx で `cardStart = 10 + index * 55` に変更（6枚 × 55f = max 285f < 360f）

#### F7. BGM 尺とビデオ尺の不整合 [P2]

**チェック**: BGM の再生時間がビデオの総尺以上か？
- NG: 50秒 BGM + 60秒ビデオ = 最後10秒が無音
- OK: BGM 尺 ≥ ビデオ総尺、または `<Audio loop />` でループ
- **検出方法**: `bgmSrc` のファイルを `ffprobe` で尺確認 → `durationInFrames / fps` と比較
- **修正パターン**: ProductShowcase.tsx で 60秒ビデオに `showcase_bgm_60s.mp3`（62秒）を使用

#### F8. ラベル/ヘッダーの一貫性 [P2]

**チェック**: 連続するデモセクションに統一されたラベルパターンがあるか？
- NG: 「LP制作デモ」「競合分析」「議事録AI」（命名規則バラバラ）
- OK: 「USE CASE 01」「USE CASE 02」「USE CASE 03」「USE CASE 04」（統一プレフィックス + 連番）
- **検出方法**: 各シーンコンポーネントのヘッダーテキストを収集し、命名パターンの一貫性を確認
- **修正パターン**: 4デモ全てに `USE CASE {NN}` + サブタイトルの2段構成を追加した実例

---

### Category G: プロダクション実装品質（Production Implementation Quality）

v26-v29 の TWIN PLANET PV制作（12シーン73秒）で発見された実践的な品質問題を体系化。

#### G1. --props によるデフォルト値オーバーライド不可 [P1]

**チェック**: Remotion 4 の `--props` CLI オプションで defaultProps を上書きしようとしていないか？
- NG: `npx remotion render Comp --props='{"bgmParts":["new.mp3"]}'` → defaultProps が優先され無視される
- OK: DEFAULT_PROPS の値を直接変更、または bgm.mp3 ファイル自体を差し替えてレンダリング
- **回避策**: 複数パターンをテストする場合は、ソースファイルを直接差し替えるか、ffmpeg で映像維持＋音声差替 `ffmpeg -y -i video.mp4 -i new_bgm.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mp4`
- **検出方法**: CI/スクリプトで `--props` を使っている箇所を grep

#### G2. Linter/外部ツールによるファイル巻き戻し [P1]

**チェック**: IDE の linter/formatter が Root.tsx や Composition ファイルを自動的に古い状態に書き戻していないか？
- NG: 編集したファイルが保存時に別のバージョンに上書きされる（import 削除、duration 変更等）
- OK: 編集後に `git diff` でファイル状態を確認、コミットされていない変更は定期的に stash/commit
- **対策**: 大きな変更は必ず feature branch で早めにコミット。レンダリング前に `grep sectionDurations` で値が期待通りか確認
- **検出方法**: レンダリング出力のファイルサイズが大幅に変わった場合（例: 77MB→29MB）は巻き戻しを疑う

#### G3. フォーカスズームの画面見切れ [P1]

**チェック**: `interpolate` で scale を 1.0 以上にする要素が画面端からはみ出していないか？
- NG: `focusScale = interpolate(prog, [0,1], [1, 1.25])` → 右端/下端のボックスが見切れる
- OK: `focusScale = 1.15` + `translateX(-40px)` で端のボックスを中央に寄せる
- **判定基準**: scale > 1.1 の要素が画面端（左10%/右10%）に配置されていたら P1
- **修正パターン**: StructureReveal で focusScale 1.25→1.15 + Marketing ボックスに translateX(-40px) を追加

#### G4. テロップ表示時間の不足 [P2]

**チェック**: テロップ（字幕テキスト）の表示時間が読み取りに十分か？
- NG: 3行テロップが各1秒以内で切り替わる → 読めない
- OK: 1行テロップ: 最低1.5秒、2行テロップ: 最低2秒、3行テロップ: 最低2.5秒
- **計算式**: `TELOP_DUR = Math.max(45, textLength * 3)` フレーム（30fps基準）
- **修正パターン**: TalentGridScroll で TELOP_DUR=75（2.5秒）に統一

#### G5. テロップ級数の不統一 [P2]

**チェック**: 同一シーン内のテロップで fontSize がバラバラでないか？
- NG: テロップ1=80px, テロップ2=56px, テロップ3=40px（視覚的にチグハグ）
- OK: 同カテゴリのテロップは同一 fontSize（80px統一等）。タイトルだけ別サイズは許容
- **検出方法**: 同一コンポーネント内の `fontSize` を一覧し、2種類以上のサイズが理由なく混在していないか確認

#### G6. シーン境界でのテキスト残留 [P2]

**チェック**: 前フェーズのテロップが次フェーズの冒頭で一瞬表示されていないか？
- NG: post-split フェーズ開始直後に前フェーズのテキストが 1-2 フレーム残る
- OK: フェーズ遷移時に開始フレームからの delay + fade-in を追加（`sf > 8 && opacity: interpolate(sf, [8, 18], [0, 1])`）
- **修正パターン**: PanDorobo の小テキストに 8フレーム delay + 10フレーム fade-in を追加

#### G7. 写真枚数とレイアウトの不整合 [P2]

**チェック**: 4-grid レイアウトに4枚しか画像がない場合、後半フェーズが1枚表示になっていないか？
- NG: images 配列が4枚で hero フェーズが images[0] 固定 → 変化がない
- OK: 8枚以上用意し、前半4-grid は先頭4枚、後半 hero スライドショーは残り4枚
- **実装**: `heroImages = images.slice(4)`, `heroDur = remainingFrames / heroImages.length`

#### G8. BGM生成のプロンプト差別化 [P3]

**チェック**: AI BGM 生成で複数パターンを作る際、プロンプトが十分に差別化されているか？
- NG: 全パターンが「pop music with clap, no vocals」の微妙な変形 → 似た曲が生成される
- OK: テンポ（115-132bpm）、楽器（ukulele/brass/808/marimba）、ジャンル（trap-pop/acoustic/anthemic）を明確に変える
- **Stable Audio 2.5**: `fal-ai/stable-audio-25/text-to-audio` で最大190秒一発生成（旧stable-audioの47秒制限は解消）
- **BGMテスト方法**: ffmpeg で映像の音声を完全差替 `ffmpeg -y -i video.mp4 -i bgm.mp3 -map 0:v -map 1:a -c:v copy -af "afade=t=out:st=70:d=3" -shortest out.mp4`

#### G9. 常時表示 vs 順序表示の選択 [P3]

**チェック**: テロップの表示方式が内容に適しているか？
- 順序表示が適切: 長いテキスト、ストーリー性のある情報、3行以上
- 常時表示が適切: ブランド名+サブタイトル（2-3行）、インパクト重視のキャッチコピー
- **実装（常時表示）**: spring fade-in + scale(0.8→1.0) で一括表示、left-align でインパクト
- **修正パターン**: ImDonutShowcase のテロップを順序表示→常時表示+左揃えに変更

---

### Category H: コンテンツ品質（Content Quality）

TaxAccountantDemo v15→v20、PersonalPMODemo v3 の制作で確立。GTM動画制作時に必ず適用。

#### H9. Claude Code UI色の統一 [P1]

**チェック**: Claude Code の UI表現が紫（Cursor風）ではなく黒（公式）になっているか？
- NG: `rgba(99,102,241,...)` (紫/インディゴ系)、`#A5B4FC` (薄紫テキスト)
- OK: 背景 `rgba(15,15,15,0.8)` / `rgba(20,20,20,0.9)`、アクセント `#D97757` (Claude orange)、スピナー stroke `#D97757`
- **検出方法**: `rgba(99,102,241` や `#A5B4FC` を grep で検索
- **判定基準**: Claude Code のUI表現に紫系の色が1箇所でもあったら P1

#### H10. ブランドアイコンの統一性 [P2]

**チェック**: 同一ブランドの派生アイコンが親ブランドのアイコンと統一されているか？
- NG: `github-actions.svg` が GitHub octocat と異なるカスタムデザイン
- OK: `github-actions.svg` = `github-issues.svg` = `github.svg` (同一の octocat)
- **判定基準**: 同一ブランドで見た目が異なるアイコンファイルがあったら P2

#### H11. SVG図の中央配置 [P2]

**チェック**: フルスクリーンのSVG図（アーキテクチャ図、フロー図）が画面中央に配置されているか？
- NG: 1920px幅の画面でSVG図の視覚的中心がx=840（画面中心960から120pxずれ）
- OK: SVG図の視覚的中心がx=960（画面中央）付近
- **検出方法**: QAフレームで目視確認。左右の余白が明らかに非対称なら NG
- **修正パターン**: PMOSelfImprove.tsx で全座標を +120px シフトした実例

#### H12. モックUIの垂直中央化 [P2]

**チェック**: Slack/Gmail等のモックUIでコンテンツが上寄せになっていないか？
- NG: メッセージが画面上部に固まり、下半分が空白
- OK: `justifyContent: "center"` で垂直中央に配置。サイドバー幅240-260px、本文フォント18px以上
- **修正パターン**: PMOSlackThread/PMOGmailAutoDraft でメインエリアに vertical centering を追加した実例

#### H1. ロゴ・ブランド表現 [P1]

**チェック**: サービス名がテキストだけで表示されていないか？
- NG: `<span>Claude Code</span>` のみ
- OK: `<Img src={staticFile("logo.svg")} />` + テキスト
- **判定基準**: 主要サービス名がロゴ画像なしで表示されていたら P1

#### H2. springアニメーションのぶれ [P1]

**チェック**: 静止すべき要素（ロゴ、タイトル、価格）に低damping springが使われていないか？
- NG: ロゴ表示に `spring({ config: { damping: 12 } })` → 微振動が目立つ
- OK: `interpolate(frame, [5, 18], [0, 1])` で滑らかフェードイン
- **判定基準**: ロゴ・タイトル・価格にdamping<16のspringがあったら P1

#### H3. ダミーデータのリアリティ [P2]

**チェック**: レシート・取引名・企業名が実在しそうか？
- NG: 「ABC ステーキ」「テスト商店」
- OK: 「JR東海 新幹線」「東横INN 品川」「個室ダイニング雅」
- 金額も現実的範囲（新幹線¥12,400、ホテル¥7,600-8,200、接待¥18,000-28,000）
- **判定基準**: 業界関係者が見て違和感あるデータがあったら P2

#### H4. 情報密度と分離 [P2]

**チェック**: 1シーンにチャート/テーブル/テキストが3つ以上詰め込まれていないか？
- NG: テーブル + 棒グラフ + ドーナツチャートが1シーン
- OK: テーブルシーン → チャートシーン に分離
- scale()拡大要素が重なっていないか（position:absoluteで明示配置）
- **判定基準**: scale>1.5の要素が2つ以上flexで配置されていたら P2

#### H5. キャプションと画面テキストの重複 [P2]

**チェック**: 画面に大きくテキストが表示されるシーンで、同内容のキャプションが出ていないか？
- NG: Hook画面「全部手動でやってますか？」+ キャプション「全部手動でやってますか？」
- OK: テキスト表示シーンはキャプション空、デモ画面シーンはキャプションで補足

#### H6. 「大量感」の演出 [P2]

**チェック**: AI自動処理シーンの項目数が少なすぎないか？
- NG: 2カテゴリ×4アイテム（スカスカ）
- OK: 6カテゴリ×10アイテム + STAGGER短縮（18f→10f）で高速処理感
- **判定基準**: 自動処理デモで5カテゴリ未満 or 8アイテム未満なら P2

#### H7. インタラクティブ感（チャットUI） [P3]

**チェック**: プロダクトデモ動画にユーザー操作/チャットアニメーションがあるか？
- タイプライター入力 → AI回答テーブルのチャットシーンがあるとベター
- 質問は具体的に（「交際費をうちわけで」「住所も参照して」等）
- **必須ではない** — あれば訴求力が上がるが、なくてもPASSする

#### H8. 訴求ストーリー構成 [P3]

**チェック**: 動画のストーリーが以下の流れになっているか？
- 前半: 痛み訴求 → 解決策提示 → 機能デモ
- 後半: 成果数値 → 教育/コース（実画面） → 価格（含まれるもの→金額→安心感） → CTA
- NG: 教育シーンがテキストonly
- OK: 実際のUI画面スクロール + テキストオーバーレイ

---

### Category I: 音声・ナレーション品質（Audio & Narration Quality）

TaxAccountantDemo v34-v40 で確立。ナレーション付き動画の必須チェック。

#### I1. ナレーション発音の正確性 [P1]

**チェック**: ElevenLabs TTS の日本語ナレーションが正しく聞き取れるか？
- NG: 「税理士」→「推理師」、「返信」→「阪神」、「議事録」→「石立」、「受信メール」→「閉める」
- OK: Gemini 2.0 Flash で全クリップを書き起こし → 期待テキストと意味が一致
- **検出方法**: `genai.upload_file(mp3)` + 書き起こし比較。全クリップ必須
- **修正パターン**: narration-qa スキルの Step 0 ルールに従い、漢字をひらがな化 or 平易な表現に言い換え
- **主な誤読パターン**: 返信→阪神、議事録→石立、各→夫は、即座に→危機座に、承認→チョンキン、マッキンゼー→松銀瀬
- **英語残留禁止**: TODO, GitHub, AI 等の英語をそのまま残すとElevenLabsが誤読する。全てカタカナ/ひらがな化必須
- **数字展開必須**: 7つの→ななつの、8種類→はっしゅるい、12,800円→いちまんにせんはっぴゃくえん

#### I2. ナレーションとキャプションの整合性 [P1]

**チェック**: 音声の内容と画面キャプションが一致しているか？
- NG: 音声「69%削減」、キャプション「70%削減」
- NG: 音声は価格のみ、キャプションにコース数・モジュール数も含む
- OK: キャプションはナレーションの要約 or 同一内容
- **検出方法**: NARRATION 配列のcaptionテキストとナレーション生成スクリプトのテキストを対照

#### I3. ナレーション尺とシーン尺の整合 [P1]

**チェック**: ナレーション音声の長さがシーンの durationInFrames 以内か？
- NG: 5.1秒のナレーションを3.6秒のシーンに atempo 1.42 で詰め込む → 早口で聞き取れない
- OK: atempo 1.3以下、または テキストを短縮してシーン尺に自然に収まる
- **判定基準**: atempo > 1.35 なら P1（テキスト短縮 or シーン尺延長を推奨）
- **検出方法**: `ffprobe` で各ナレーション mp3 の尺を取得 → sectionDurations と比較

#### I4. BGMとナレーションの音量バランス [P1]

**チェック**: ナレーションがBGMに埋もれていないか？
- NG: BGM `volume={0.35}`, ナレーション `volume={0.85}` → BGMが勝つ
- NG: BGM `volume={0.12}`, ナレーション `volume={0.85}` → amixで相殺されナレーションが小さくなる
- OK: BGM `volume={0.18-0.25}`, ナレーション `volume={1.0-1.2}`
- **判定基準**: ナレーション volume ÷ BGM volume ≥ 4.0 であること
- **注意**: ffmpeg amix は入力を正規化するため、volume値の見た目以上にBGMが大きくなることがある。実際に再生して確認必須
- **P2→P1に昇格**: 音量バランスの問題は視聴体験を根本的に損なうため

#### I5. BGMのジョイント音 [P2]

**チェック**: 複数パートをcrossfade結合したBGMで、結合点が不自然でないか？
- NG: 24秒目で急にテンポ/楽器が変わる（分割生成+crossfadeの典型問題）
- OK: Stable Audio 2.5 で一発生成（190秒まで対応）
- **修正パターン**: `fal-ai/stable-audio` → `fal-ai/stable-audio-25/text-to-audio` に移行

#### I6. 数字・専門用語の読み [P2]

**チェック**: TTS が数字や専門用語を正しく読めているか？
- NG: 「12,800円」→「12人100円」、「69%」→聞き取れない
- OK: 数字をひらがなに展開して生成（いちまん にせん はっぴゃく えん）
- **問題が起きやすい語**: 金額、パーセンテージ、「24時間365日」、英語混在（MCP、freee）

---

### Category J: 背景・ビジュアル素材の活用（Background & Visual Assets）

静的なシーンを動的に進化させるためのチェック項目。

#### J1. テキストのみシーンの背景不足 [P2]

**チェック**: テキストだけが表示されるシーンが3秒以上続いていないか？
- NG: 単色背景 + テキストのみで3秒以上（視覚的に退屈）
- OK: i2v背景、MeshGradient、パーティクル、または微動アニメーション付き背景を追加
- **検出方法**: シーンコンポーネントの JSX を確認し、`<Img>` / `<OffthreadVideo>` / SVG / Canvas 要素がなく `durationInFrames / fps >= 3` のシーンを特定
- **修正パターン**: i2v動画背景を `<OffthreadVideo>` で配置し、上にテキストをオーバーレイ

#### J2. i2v背景のオーバーレイ opacity [P2]

**チェック**: i2v背景使用時にオーバーレイの opacity が適切か？
- NG: `opacity: 0.3`（テキストが背景に埋もれる）、`opacity: 0.9`（背景が見えずi2vの意味なし）
- OK: `opacity: 0.5-0.7` の半透明オーバーレイで背景とテキストのバランスを確保
- **実装例**: `<div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.6)' }} />`
- **検出方法**: `OffthreadVideo` を含むシーンで、兄弟/子要素の `rgba(` や `opacity` 値を確認
- **判定基準**: overlay opacity が 0.5 未満 or 0.7 超の場合は P2

#### J3. 静的PNG画像の長時間表示 [P2]

**チェック**: 静的なPNG/JPG画像が3秒以上アニメーションなしで表示されていないか？
- NG: draw.io のスクリーンショットPNGを `<Img>` でそのまま3秒以上表示（紙芝居感）
- OK: React SVGアニメーション化し、要素が `spring()` でスタッガード登場する
- **変換指針**: draw.io等の図解PNGがある場合 → 構成要素（ノード、矢印、テキスト）を分解 → 各要素を `<rect>`, `<circle>`, `<text>`, `<line>` で再実装 → `spring()` でスタッガードアニメーション
- **検出方法**: `<Img src={staticFile("...png")}` を含むシーンで、親 Sequence の `durationInFrames / fps >= 3` かつ `interpolate` / `spring` が画像に適用されていない場合
- **判定基準**: 3秒以上の静的PNG表示があったら P2（アニメーション化を推奨）

---

## 出力フォーマット

```markdown
## Motion Review Report

**対象**: {composition_file_path}
**評価**: {A+ / A / B+ / B / C+ / C / D}
**VERDICT**: {PASS / FIX_RECOMMENDED / FIX_REQUIRED}

### P1 Issues (Must Fix)
| # | Check | Issue | Fix |
|---|-------|-------|-----|
| 1 | A1 | シーン間に黒フレーム | Sequence を OVERLAP フレーム重ねる |

### P2 Issues (Should Fix)
| # | Check | Issue | Fix |
|---|-------|-------|-----|

### P3 Issues (Nice to Have)
| # | Check | Issue | Fix |
|---|-------|-------|-----|

### Passed Checks
A1 ✓, B1 ✓, B2 ✓, ..., F1 ✓, F2 ✓, F6 ✓, ...

### 総評
{1-2行のサマリー}
```

## 評価基準

| Grade | 条件 |
|-------|------|
| A+ | P1=0, P2=0, P3≤1 |
| A  | P1=0, P2=0, P3≤3 |
| B+ | P1=0, P2≤1 |
| B  | P1=0, P2≤3 |
| C+ | P1≤1, P2≤3 |
| C  | P1≤2 |
| D  | P1≥3 |

## 使用例

### 単体実行
```
motion review mv-composer/src/compositions/AgentCampBrandPV.tsx
```

### Campaign Orchestrator からの呼び出し
Quality Review ステップで `channel = TikTok | YouTube` の場合、
成果物の Remotion ソースファイルに対してこのスキルを自動実行する。

VERDICT が FIX_REQUIRED の場合、Auto-fix Loop に入る（max 3回）。

---

## Render & Review Loop（自己改善ワークフロー）

レンダリング後に自動で品質チェックし、問題を検出したら修正→再レンダリングを繰り返す。
max 3イテレーションで収束させる。

### トリガーワード
`render and review`, `レンダリング＆レビュー`, `自己改善ループ`

### フロー

```
[1] Render
    npx remotion render src/index.ts {CompositionId} out/{Name}_v{N}.mp4
        ↓
[2] QA Frame Extraction
    bash scripts/qa_frames.sh out/{Name}_v{N}.mp4
    → data/qa_{Name}_v{N}/ に12フレーム出力
        ↓
[3] Visual Review（QAフレーム目視）
    Read ツールで各フレームを確認:
    - 黒フレーム検出（opacity=0の遷移境界）
    - テキスト見切れ・改行崩れ
    - 要素重なり・余白不足
    - 色彩・視認性の問題
        ↓
[4] Code Review（20項目チェックリスト）
    対象 .tsx ファイルを Read → 本スキルの A1-H8 をチェック
        ↓
[5] VERDICT 判定
    ├─ PASS (P1=0) → 完了。ユーザーに結果報告
    ├─ FIX_RECOMMENDED (P2のみ) → 修正提案をユーザーに提示
    └─ FIX_REQUIRED (P1あり) → 自動修正 → Step 1 に戻る（max 3回）
        ↓
[6] Auto-fix（P1の場合のみ自動実行）
    - P1 の修正を .tsx に適用
    - v{N+1} としてレンダリング
    - 再度 Step 2-5
```

### 実行方法

会話内で以下のように指示:

```
CCTrend-All をレンダリングしてレビューして
```

Claude Code が以下を自動実行:
1. `npx remotion render src/index.ts CCTrend-All out/CCTrend-All_v1.mp4`
2. `bash scripts/qa_frames.sh out/CCTrend-All_v1.mp4`
3. QAフレームを Read で目視確認
4. .tsx を Read → 20項目チェック
5. レビューレポート出力
6. P1があれば自動修正 → v2 レンダリング → 再レビュー

### 注意事項

- **max 3回**のイテレーションで止める。3回で解決しない場合はユーザーに報告
- P2/P3 は自動修正しない。提案のみ
- レンダリング前に `npx tsc --noEmit` で型チェック
- QAフレームは `data/qa_{Name}_v{N}/` に世代管理（上書きしない）
- 各イテレーションでバージョン番号をインクリメント（v1→v2→v3）

## TwinPlanetIntro 品質水準（参考: A グレード）

以下は A グレードの実装で確認された技法一覧。新規コンポジションはこれらを参考にすること:

| 技法 | 実装パターン |
|------|------------|
| 文字単位スタッガー | `chars.map((c, i) => spring({ delay: i * 4 }))` + translateY(30→0) |
| 着地後呼吸 | `p > 0.9 ? Math.sin(frame * 0.08) * 0.015 : 0` |
| clipPath ワイプ | `clipPath: inset(0 ${x}% 0 0)` で右→左に開示 |
| 確定的パンの多様性 | `(i * 7 + 3) % 11` で seeded random motion |
| Ken Burns 微ズーム | `scale(1.0 → 1.08)` over 120 frames |
| Pulsing accent line | 着地後に `sin(frame * 0.12) * 3` で幅パルス |
| 全画面フラッシュ | `[0,3,8] → [1,0.9,0]` で 8 フレームフェード |
| Count-up + pulse | cubic ease-out → 完了後 sin 波 ±3% |
| Blur 背景フォールバック | `blur(30px) brightness(1.1)` で背景穴埋め |
| 統一退場アニメーション | SceneWrap: zoom-out 6% + fade |
