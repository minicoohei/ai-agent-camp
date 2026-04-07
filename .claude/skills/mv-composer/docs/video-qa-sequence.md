# Video QA パイプライン — シーケンス図

## 全体フロー

```mermaid
sequenceDiagram
    participant CLI
    participant QA as video_qa.py
    participant FF as ffprobe / ffmpeg
    participant W as fal.ai Whisper
    participant G as Gemini 2.0 Flash
    participant P as PIL / numpy

    CLI->>QA: video.mp4, mv_id, --stages

    rect rgb(240, 248, 255)
        Note over QA,FF: Stage 1: metadata (ffprobe ×1)
        QA->>FF: ffprobe -show_format -show_streams
        FF-->>QA: 解像度, 尺, コーデック, 音声有無
    end

    rect rgb(240, 248, 255)
        Note over QA,FF: Stage 2: black_frames (ffmpeg ×1)
        QA->>FF: ffmpeg -vf blackdetect
        FF-->>QA: black_start / black_duration 一覧
        QA->>QA: トランジション時刻と照合 → 有意判定
    end

    rect rgb(240, 248, 255)
        Note over QA,FF: Stage 3: silence (ffmpeg ×1)
        QA->>FF: ffmpeg -af silencedetect
        FF-->>QA: silence_start / silence_end 一覧
        QA->>QA: 1.5s超の無音を抽出
    end

    rect rgb(240, 248, 255)
        Note over QA,FF: Stage 4: narration_sync (ffprobe ×8)
        loop 8シーン
            QA->>FF: ffprobe narration_mvXX_fast/frame_XX.mp3
            FF-->>QA: duration
            QA->>QA: ナレーション尺 vs シーン尺+0.5s
        end
    end

    rect rgb(255, 248, 230)
        Note over QA,G: Stage 5: audio_accuracy (Whisper ×8 + Gemini text ×8)
        loop 8シーン
            QA->>W: whisper_transcribe(frame_XX.mp3)
            W-->>QA: transcribed text
            QA->>G: compare_pronunciation(expected, transcribed)
            G-->>QA: {pass, issues[], summary}
            QA->>QA: high severity ≥1 → FAIL
        end
    end

    rect rgb(255, 243, 230)
        Note over QA,G: Stage 6+7: visual + terop (ffmpeg ×16 + Gemini Vision ×8)
        loop 8シーン
            QA->>FF: extract_frame(30%) + extract_frame(70%)
            FF-->>QA: 2枚 JPG
            QA->>G: Gemini Vision(2画像 + プロンプト)
            G-->>QA: {design_score, text_content_detected, issues[]}
            QA->>QA: pass = high==0 AND design_score≥40
            opt テロップあり
                QA->>QA: to_hiragana → sliding window → similarity≥50%
            end
        end
    end

    rect rgb(245, 240, 255)
        Note over QA,G: Stage 8: i2v_quality (ffmpeg ×6-9 + PIL ×2-3 + Gemini Vision ×2-3)
        loop 2-3 i2vシーン (motion_type=="i2v")
            QA->>FF: extract_frame(0.5s, 2.5s, 4.5s)
            FF-->>QA: 3枚 JPG
            QA->>P: compute_frame_diff(3 frames)
            P-->>QA: motion_diff (0.0-1.0)
            QA->>G: Gemini Vision(3画像 + i2vプロンプト)
            G-->>QA: {artifacts[], motion_quality}
            QA->>QA: high artifact≥1 OR diff<0.005 → FAIL
        end
    end

    QA->>QA: 全ステージ集計 → overall_pass
    QA-->>CLI: QA Summary + Report JSON
    Note over CLI: Cost: ~$0.002/MV (Gemini ×18, Whisper ×8)
```

## 呼出回数サマリー

| 外部サービス | Stage | 呼出/MV | 備考 |
|-------------|-------|---------|------|
| ffprobe | 1, 4 | 9 | metadata ×1 + narration ×8 |
| ffmpeg | 2, 3, 6-7, 8 | 19-22 | blackdetect ×1 + silencedetect ×1 + frame抽出 ×16 + i2v frame抽出 ×6-9 |
| fal.ai Whisper | 5 | 8 | シーンごとに1回 |
| Gemini text | 5 | 8 | 発音比較（pykakasi + Gemini Flash） |
| Gemini Vision | 6-7, 8 | 10-11 | 映像品質 ×8 + i2v ×2-3 |
| PIL/numpy | 8 | 2-3 | フレーム差分計算 |
| **合計API** | | **26-27** | **~$0.002/MV** |

## pass/fail 判定ルール（Python側で一元管理）

| チェック | FAIL条件 |
|---------|---------|
| metadata | 尺差 ≥ 2.0s or 音声なし |
| black_frames | トランジション外の1.0s超黒フレーム ≥ 1 |
| silence | 1.5s超の無音 ≥ 1 |
| narration_sync | ナレーション超過 > 0.5s |
| audio_accuracy | high severity 発音エラー ≥ 1 |
| terop_verify | テロップ一致率 < 50%（スライディングウィンドウ部分一致） |
| visual | design_score < 40 or high issue ≥ 1 |
| i2v_quality | high severity artifact ≥ 1 or モーション量 < 0.005 |
