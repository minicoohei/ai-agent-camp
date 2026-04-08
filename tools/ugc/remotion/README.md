# Remotion - コードベース動画生成

React/TypeScriptで動画をプログラマブルに生成するツール。

## 特徴

- **コードベース**: React/TypeScriptで動画を記述
- **ローカル実行**: API不要、FFmpegでレンダリング
- **プログラマブル**: データ駆動の動画生成
- **無料**: オープンソース（Pro版もあり）

## セットアップ

### 1. 前提条件

```bash
# Node.js 18+
node --version

# FFmpeg
brew install ffmpeg
```

### 2. Remotionプロジェクト作成

```bash
cd ~/aiagent-base/tools/ugc/remotion/
npm init video my-video
cd my-video
```

### 3. 開発サーバー起動

```bash
npm start
```

ブラウザで http://localhost:3000 が開きます。

## 基本的な使い方

### テンプレートプロジェクト

```bash
# シンプルなテキスト動画
npm init video -- --template hello-world

# データ駆動動画
npm init video -- --template data-driven

# アニメーション豊富
npm init video -- --template spring-animations
```

### 動画レンダリング

```bash
# MP4出力
npm run build

# 特定のComposition
npx remotion render src/index.ts MyVideo output.mp4

# 解像度指定
npx remotion render src/index.ts MyVideo output.mp4 --width=1920 --height=1080
```

## サンプルコード

### 基本的なComposition

```typescript
// src/MyVideo.tsx
import {AbsoluteFill, useCurrentFrame} from 'remotion';

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  
  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#000',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <h1 style={{color: 'white', fontSize: 100}}>
        Frame: {frame}
      </h1>
    </AbsoluteFill>
  );
};
```

### アニメーション例

```typescript
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';

export const AnimatedVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  
  const scale = spring({
    frame,
    fps,
    config: {
      damping: 100,
    },
  });
  
  return (
    <AbsoluteFill style={{backgroundColor: 'white'}}>
      <div
        style={{
          transform: `scale(${scale})`,
          fontSize: 100,
        }}
      >
        Hello Remotion!
      </div>
    </AbsoluteFill>
  );
};
```

### データ駆動動画

```typescript
// src/DataVideo.tsx
import {Sequence} from 'remotion';

const data = [
  {title: 'Slide 1', duration: 90},
  {title: 'Slide 2', duration: 90},
  {title: 'Slide 3', duration: 90},
];

export const DataVideo: React.FC = () => {
  return (
    <>
      {data.map((item, index) => (
        <Sequence
          key={index}
          from={index * 90}
          durationInFrames={item.duration}
        >
          <AbsoluteFill style={{backgroundColor: '#000'}}>
            <h1 style={{color: 'white'}}>{item.title}</h1>
          </AbsoluteFill>
        </Sequence>
      ))}
    </>
  );
};
```

## 高度な機能

### 音声追加

```typescript
import {Audio} from 'remotion';

<Audio src="audio.mp3" />
```

### 画像表示

```typescript
import {Img} from 'remotion';

<Img src="image.png" />
```

### トランジション

```typescript
import {interpolate} from 'remotion';

const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

## ユースケース

1. **データ可視化動画**: グラフ、統計のアニメーション
2. **ソーシャルメディア投稿**: 定型フォーマットの量産
3. **プレゼン動画**: スライドから動画生成
4. **説明動画**: テキスト + 図解のアニメーション
5. **バッチ生成**: CSVデータから複数動画生成

## リンク

- 公式サイト: https://www.remotion.dev/
- ドキュメント: https://www.remotion.dev/docs/
- テンプレート: https://www.remotion.dev/templates
- コミュニティ: https://remotion.dev/discord

## トラブルシューティング

### FFmpegが見つからない

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Windows
# https://ffmpeg.org/download.html からダウンロード
```

### レンダリングが遅い

```bash
# 並列レンダリング
npx remotion render --concurrency=8

# 低解像度でテスト
npx remotion render --scale=0.5
```

### メモリ不足

```bash
# メモリ制限を増やす
NODE_OPTIONS=--max-old-space-size=8192 npm run build
```
