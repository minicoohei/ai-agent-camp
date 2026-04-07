"""
Viral Short Video Script Generator

TikTok/YouTube Shorts向けのバイラル動画スクリプトを生成。
バイラルテクニック（3秒フック、モジュラー構造、ループブリッジ、
フラッシュテキスト等）を自動的に組み込んだスクリプトを出力する。

機能:
  1. スクリプト生成: viral_script.json, scenes.json, hook_variants.json
  2. ピークフック抽出: --analyze-video でバズ動画の最強フックを特定

出力:
  - viral_script.json: バイラル構造化スクリプト
  - scenes.json: storyboard-generator互換形式
  - hook_variants.json: フックバリエーション
  - hook_analysis.json: ピークフック分析結果（--analyze-video時）
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from bootcamp_utils import get_client, get_flash_model

load_dotenv()

DEFAULT_OUTPUT_DIR = Path("output/viral-scripts")

# フックコンピレーション素材プリセット
HOOK_ASSETS_DIR = Path(__file__).parent.parent / "assets" / "hooks"
HOOK_PRESETS = {
    "hook_viral_10": HOOK_ASSETS_DIR / "hook_viral_10.mp4",
    "hook_trifecta": HOOK_ASSETS_DIR / "hook_trifecta.mp4",
    "hook_600k_gmv": HOOK_ASSETS_DIR / "hook_600k_gmv.mp4",
}

# video-frame-reader のパス
VIDEO_FRAME_READER = Path(__file__).parents[2] / "video-frame-reader" / "extract_keyframes.py"

# --- バイラルテクニック知識ベース ---

HOOK_TRIGGERS = {
    "curiosity_gap": {
        "ja": [
            "99%の人がこれ知らないんだけど...",
            "正直これ教えたくなかったんだけど...",
            "これ知ってる？ほとんどの人が間違えてる",
            "誰も教えてくれなかった{topic}の真実",
        ],
        "en": [
            "Nobody tells you this about {topic}...",
            "I wasn't going to share this but...",
            "99% of people get this wrong about {topic}",
            "The truth about {topic} nobody talks about",
        ],
    },
    "fomo": {
        "ja": [
            "これ見逃したらマジで損する",
            "今だけの方法、すぐ使えなくなるかも",
            "知らないと損する{topic}の裏技",
            "まだこれ使ってないの？",
        ],
        "en": [
            "You're missing out if you don't know this",
            "This won't work forever, use it now",
            "Stop scrolling — you need to see this",
            "Still not using this? You're leaving money on the table",
        ],
    },
    "social_proof": {
        "ja": [
            "100万人が使ってるのに誰も教えてくれない",
            "TikTokでバズった{topic}の方法",
            "プロが実はやってる{topic}のコツ",
            "みんなこっそり使ってる",
        ],
        "en": [
            "1M people already use this and nobody told you",
            "This went viral for a reason",
            "Pros secretly do this with {topic}",
            "Everyone's using this but nobody talks about it",
        ],
    },
    "pattern_interrupt": {
        "ja": [
            "ちょっと待って、これ見て",
            "え、マジで？これ試してみて",
            "ストップ。これだけは知っておいて",
            "3秒だけ時間ちょうだい",
        ],
        "en": [
            "Wait — look at this",
            "STOP scrolling. You need to see this",
            "Give me 3 seconds",
            "I just found something insane",
        ],
    },
    "contrarian": {
        "ja": [
            "{topic}は全部ウソだった",
            "みんなが信じてる{topic}、実は間違い",
            "{topic}をやめたら人生変わった",
            "あの有名な{topic}のアドバイス、逆効果です",
        ],
        "en": [
            "Everything you know about {topic} is wrong",
            "I stopped {topic} and here's what happened",
            "The {topic} advice everyone gives is actually harmful",
            "Unpopular opinion: {topic} doesn't work",
        ],
    },
}

TONE_INSTRUCTIONS = {
    "casual": "フレンドリーで親しみやすいトーン。友達に話すように。「〜だよね」「マジで」「ヤバい」等のカジュアルな表現OK",
    "professional": "信頼感のあるプロフェッショナルなトーン。データや実績を交えて。敬語ベース",
    "energetic": "ハイテンションでエネルギッシュ。感嘆符多め、テンポ速く。「すごい！」「最高！」",
    "storytelling": "ストーリー形式。「実は先日...」「最初は〇〇だったんだけど...」のように物語で引き込む",
}

DURATION_CONFIGS = {
    15: {"hook": 3, "body_segments": 1, "cta": 2, "body_per_segment": 10},
    30: {"hook": 3, "body_segments": 2, "cta": 3, "body_per_segment": 12},
    60: {"hook": 3, "body_segments": 4, "cta": 4, "body_per_segment": 13},
}


def build_script_prompt(
    topic: str,
    product: Optional[str],
    duration: int,
    target: Optional[str],
    tone: str,
    hook_style: str,
    lang: str,
    enable_loop: bool,
    enable_flash: bool,
    enable_split_screen: bool,
) -> str:
    """Gemini用のスクリプト生成プロンプトを組み立てる"""

    dur_config = DURATION_CONFIGS.get(duration, DURATION_CONFIGS[30])
    tone_desc = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["casual"])

    # フック例を取得
    if hook_style == "auto":
        hook_examples = []
        for style, examples in HOOK_TRIGGERS.items():
            ex = examples[lang][0].replace("{topic}", topic)
            hook_examples.append(f"  - [{style}] {ex}")
        hook_section = "フックスタイルは最適なものを自動選択してください:\n" + "\n".join(hook_examples)
    else:
        examples = HOOK_TRIGGERS.get(hook_style, HOOK_TRIGGERS["curiosity_gap"])
        hook_examples = [ex.replace("{topic}", topic) for ex in examples[lang][:3]]
        hook_section = f"フックスタイル: {hook_style}\n参考例:\n" + "\n".join(f"  - {ex}" for ex in hook_examples)

    product_section = f"\n商材/サービス: {product}" if product else ""
    target_section = f"\nターゲット層: {target}" if target else ""

    loop_instruction = ""
    if enable_loop:
        loop_instruction = """
## ループブリッジ(リウォッチ誘導)
動画の最後のセリフが冒頭のフックに自然に繋がるようにしてください。
例: 「さっき言った一番ヤバいやつだけど...」→ 冒頭に戻る
loop_bridge フィールドに、末尾のセリフと冒頭への繋がりを記述してください。
"""

    flash_instruction = ""
    if enable_flash:
        flash_instruction = """
## フラッシュテキスト(リウォッチトリガー)
動画の最後に一瞬だけ表示するテキストを指定してください。
0.1秒未満で表示され、意識的に読めない速度で「もう一回見よう」と思わせます。
flash_text フィールドに、テキスト内容と色（red, white, yellow, black のいずれか）を指定してください。
テキスト例: 「もう一回見て」「隠しメッセージ」「気づいた？」「答えは最初に」
"""

    split_screen_note = ""
    if enable_split_screen:
        split_screen_note = """
## スプリットスクリーン
この動画はスプリットスクリーン（上: メインコンテンツ / 下: ゲームプレイ背景）で
使用される想定です。各シーンの visual_note にはメインコンテンツの描写のみ記述してください。
"""

    script_lang = "日本語" if lang == "ja" else "English"

    prompt = f"""あなたはTikTok/YouTube Shortsのバイラル動画スクリプトライターです。
以下の条件でバイラル動画のスクリプトを生成してください。

## 基本情報
- トピック: {topic}{product_section}{target_section}
- 動画の長さ: {duration}秒
- トーン: {tone_desc}
- スクリプト言語: {script_lang}

## 構造(モジュラー方式)
- Hook（冒頭フック）: {dur_config['hook']}秒 — 最重要。スクロール停止を狙う
- Body: {dur_config['body_segments']}セグメント x 約{dur_config['body_per_segment']}秒
- CTA: {dur_config['cta']}秒

## フック設計
{hook_section}

### フック設計の必須要件:
1. 最初の1秒でスクロールを止める「パターンインタラプト」を入れる
2. 心理トリガーを必ず1つ以上使う（curiosity_gap, fomo, social_proof, pattern_interrupt, contrarian）
3. 冒頭の表情/動きを具体的に指示する（目を見開く、手を振る等）
{loop_instruction}
{flash_instruction}
{split_screen_note}
## 出力形式(JSON)

以下のJSON形式で出力してください。JSON以外の文字は含めないでください:

```json
{{
  "meta": {{
    "topic": "{topic}",
    "product": "{product or ''}",
    "duration": {duration},
    "target": "{target or ''}",
    "tone": "{tone}"
  }},
  "hook": {{
    "text": "フックのセリフ（{script_lang}）",
    "duration": {dur_config['hook']},
    "trigger_type": "curiosity_gap|fomo|social_proof|pattern_interrupt|contrarian",
    "visual_note": "映像の具体的な指示",
    "emotion": "surprise|excitement|concern|friendly|serious"
  }},
  "body": [
    {{
      "text": "ボディのセリフ",
      "duration": {dur_config['body_per_segment']},
      "visual_note": "映像の具体的な指示",
      "motion_type": "i2v|ken_burns|static|motion_graphics"
    }}
  ],
  "cta": {{
    "text": "CTAのセリフ",
    "duration": {dur_config['cta']},
    "visual_note": "映像の具体的な指示",
    "emotion": "friendly|urgent|excited"
  }},
  "loop_bridge": {{
    "enabled": {"true" if enable_loop else "false"},
    "end_text": "動画末尾のセリフ（冒頭に繋がるもの）",
    "connects_to": "hook",
    "visual_note": "冒頭と同じカメラアングルに戻る"
  }},
  "flash_text": {{
    "enabled": {"true" if enable_flash else "false"},
    "text": "一瞬表示するテキスト",
    "color": "red",  # Options: red, white, yellow, black
    "duration_frames": 3,
    "position": "center"
  }},
  "viral_techniques": {{
    "split_screen": {"true" if enable_split_screen else "false"},
    "captions": true,
    "lofi_aesthetic": true,
    "fast_pace": true,
    "speech_speed": 1.2
  }}
}}
```

bodyの要素数は{dur_config['body_segments']}個にしてください。
JSONのみを出力してください。"""

    return prompt


def build_variants_prompt(
    topic: str,
    original_hook: Dict,
    num_variants: int,
    lang: str,
) -> str:
    """フックバリエーション生成プロンプト"""
    script_lang = "日本語" if lang == "ja" else "English"
    trigger_types = list(HOOK_TRIGGERS.keys())

    return f"""以下のオリジナルフックに対して、{num_variants}つの異なるバリエーションを生成してください。
各バリエーションは異なる心理トリガーを使ってください。

## オリジナルフック
- テキスト: {original_hook.get('text', '')}
- トリガー: {original_hook.get('trigger_type', '')}
- トピック: {topic}

## 使用可能なトリガータイプ
{', '.join(trigger_types)}

## 出力形式(JSON配列のみ)
```json
[
  {{
    "text": "バリエーション1のテキスト（{script_lang}）",
    "trigger_type": "トリガータイプ",
    "visual_note": "映像指示",
    "emotion": "表情"
  }}
]
```

オリジナルとは異なるトリガータイプを使い、{num_variants}個のバリエーションを生成してください。
JSONのみを出力してください。"""


def convert_to_scenes_json(viral_script: Dict) -> Dict:
    """viral_script.json → storyboard-generator互換 scenes.json に変換"""
    def format_timestamp(seconds: int) -> str:
        """Convert seconds to MM:SS format"""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}:{secs:02d}"

    scenes = []
    current_time = 0

    # Hook
    hook = viral_script.get("hook", {})
    hook_dur = hook.get("duration", 3)
    scenes.append({
        "frame_number": 1,
        "timestamp": f"{format_timestamp(current_time)}-{format_timestamp(current_time + hook_dur)}",
        "scene_type": "hook",
        "description": hook.get("visual_note", ""),
        "visual_prompt": _build_visual_prompt(hook),
        "camera_angle": "close-up",
        "character_action": hook.get("visual_note", "カメラに向かって話す"),
        "emotion": hook.get("emotion", "surprise"),
        "narration": hook.get("text", ""),
        "text_overlay": {
            "main_text": "",
            "sub_text": "",
            "position": "center",
            "style": "bold",
        },
        "motion_type": "i2v",
        "motion_note": "冒頭フック: 表情変化が重要なためi2V推奨",
    })
    current_time += hook_dur

    # Body segments
    body = viral_script.get("body", [])
    for i, segment in enumerate(body):
        seg_dur = segment.get("duration", 10)
        motion = segment.get("motion_type", "ken_burns")
        scenes.append({
            "frame_number": len(scenes) + 1,
            "timestamp": f"{format_timestamp(current_time)}-{format_timestamp(current_time + seg_dur)}",
            "scene_type": "body",
            "description": segment.get("visual_note", ""),
            "visual_prompt": _build_visual_prompt(segment),
            "camera_angle": "medium shot" if i % 2 == 0 else "over-the-shoulder",
            "character_action": segment.get("visual_note", "説明している"),
            "emotion": "neutral",
            "narration": segment.get("text", ""),
            "text_overlay": {
                "main_text": "",
                "sub_text": "",
                "position": "center",
                "style": "subtitle",
            },
            "motion_type": motion,
            "motion_note": f"Body segment {i+1}",
        })
        current_time += seg_dur

    # CTA
    cta = viral_script.get("cta", {})
    cta_dur = cta.get("duration", 3)
    scenes.append({
        "frame_number": len(scenes) + 1,
        "timestamp": f"{format_timestamp(current_time)}-{format_timestamp(current_time + cta_dur)}",
        "scene_type": "cta",
        "description": cta.get("visual_note", ""),
        "visual_prompt": _build_visual_prompt(cta),
        "camera_angle": "medium shot",
        "character_action": cta.get("visual_note", "画面下を指差す"),
        "emotion": cta.get("emotion", "friendly"),
        "narration": cta.get("text", ""),
        "text_overlay": {
            "main_text": "",
            "sub_text": "",
            "position": "bottom",
            "style": "bold",
        },
        "motion_type": "i2v",
        "motion_note": "CTA: アクション促進のためi2V推奨",
    })
    current_time += cta_dur

    # Loop bridge (optional extra scene)
    loop_bridge = viral_script.get("loop_bridge", {})
    if loop_bridge.get("enabled"):
        scenes.append({
            "frame_number": len(scenes) + 1,
            "timestamp": f"{format_timestamp(current_time)}-{format_timestamp(current_time + 2)}",
            "scene_type": "loop_bridge",
            "description": loop_bridge.get("visual_note", "冒頭に繋がるシーン"),
            "visual_prompt": "Same camera angle and setting as frame 1, character turning back to camera with curious expression",
            "camera_angle": "close-up",
            "character_action": loop_bridge.get("visual_note", "冒頭と同じアングルに戻る"),
            "emotion": "curiosity",
            "narration": loop_bridge.get("end_text", ""),
            "text_overlay": {
                "main_text": "",
                "sub_text": "",
                "position": "center",
                "style": "bold",
            },
            "motion_type": "i2v",
            "motion_note": "ループブリッジ: 冒頭に繋がるため表情変化が必要",
        })

    # Flash text metadata (scenes.json拡張フィールド)
    flash_text = viral_script.get("flash_text", {})

    title = viral_script.get("meta", {}).get("topic", "Viral Short Video")

    return {
        "title": title,
        "scenes": scenes,
        "_viral_meta": {
            "flash_text": flash_text,
            "viral_techniques": viral_script.get("viral_techniques", {}),
            "loop_bridge": loop_bridge,
        },
    }


def _build_visual_prompt(segment: Dict) -> str:
    """セグメント情報から英語のビジュアルプロンプトを組み立てる"""
    visual_note = segment.get("visual_note", "")
    emotion = segment.get("emotion", "neutral")
    return (
        f"UGC-style talking head video frame. {visual_note}. "
        f"Expression: {emotion}. "
        f"Natural lighting, casual setting, iPhone-shot aesthetic. "
        f"Do NOT include any text or words in the image."
    )


def generate_viral_script(
    client,
    topic: str,
    product: Optional[str] = None,
    duration: int = 30,
    target: Optional[str] = None,
    tone: str = "casual",
    hook_style: str = "auto",
    lang: str = "ja",
    enable_loop: bool = True,
    enable_flash: bool = True,
    enable_split_screen: bool = False,
    num_variants: int = 3,
) -> Dict:
    """
    バイラル動画スクリプトを生成する。

    Returns:
        {
            "viral_script": {...},
            "scenes": {...},
            "hook_variants": [...]
        }
    """
    from google.genai import types

    # Step 1: メインスクリプト生成
    print("📝 バイラルスクリプト生成中...")
    prompt = build_script_prompt(
        topic=topic,
        product=product,
        duration=duration,
        target=target,
        tone=tone,
        hook_style=hook_style,
        lang=lang,
        enable_loop=enable_loop,
        enable_flash=enable_flash,
        enable_split_screen=enable_split_screen,
    )

    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[prompt],
        config=types.GenerateContentConfig(
            temperature=0.8,
            max_output_tokens=4000,
        ),
    )

    response_text = response.text.strip()
    viral_script = _parse_json_response(response_text)

    if not viral_script:
        print("❌ スクリプト生成に失敗しました")
        return {}

    hook = viral_script.get("hook", {})
    print("✅ メインスクリプト生成完了")
    print(f"   Hook: [{hook.get('trigger_type', '?')}] {hook.get('text', '')[:50]}...")

    # Step 2: フックバリエーション生成
    print(f"\n🔄 フックバリエーション x{num_variants} 生成中...")
    variants_prompt = build_variants_prompt(
        topic=topic,
        original_hook=hook,
        num_variants=num_variants,
        lang=lang,
    )

    variants_response = client.models.generate_content(
        model=get_flash_model(),
        contents=[variants_prompt],
        config=types.GenerateContentConfig(
            temperature=0.9,
            max_output_tokens=2000,
        ),
    )

    hook_variants = _parse_json_response(variants_response.text.strip())
    if not isinstance(hook_variants, list):
        hook_variants = []
    print(f"✅ {len(hook_variants)}個のフックバリエーション生成完了")

    # Step 3: scenes.json 変換
    print("\n🔧 scenes.json 形式に変換中...")
    scenes_data = convert_to_scenes_json(viral_script)
    print(f"✅ {len(scenes_data['scenes'])}シーンに変換完了")

    return {
        "viral_script": viral_script,
        "scenes": scenes_data,
        "hook_variants": hook_variants,
    }


def _parse_json_response(text: str):
    """LLMレスポンスからJSONを抽出"""
    # ```json ... ``` ブロックを探す
    json_match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_str = text

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # フォールバック1: バッククォートを除去して再試行
    json_str = json_str.strip()
    if json_str.startswith("```"):
        json_str = re.sub(r"^```\w*\s*", "", json_str)
    if json_str.endswith("```"):
        json_str = json_str[: json_str.rfind("```")].rstrip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # フォールバック2: 最初の [ or { から最後の ] or } までを抽出
    start_array = text.find("[")
    start_obj = text.find("{")

    if start_array >= 0 and (start_obj < 0 or start_array < start_obj):
        # 配列を探す
        end = text.rfind("]")
        if end > start_array:
            json_str = text[start_array : end + 1]
    elif start_obj >= 0:
        # オブジェクトを探す
        end = text.rfind("}")
        if end > start_obj:
            json_str = text[start_obj : end + 1]
    else:
        print("⚠️ JSON解析エラー: JSONの開始文字が見つかりません")
        print(f"   Response (先頭300字): {text[:300]}...")
        return None

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON解析エラー: {e}")
        print(f"   Response (先頭300字): {text[:300]}...")
        return None


# =============================================================================
# ピークフック抽出機能
# =============================================================================


def resolve_analyze_video_path(value: str) -> Optional[Path]:
    """
    --analyze-video の値をファイルパスに解決する。
    プリセット名（hook_viral_10, hook_trifecta, hook_600k_gmv）またはファイルパスを受け付ける。
    """
    if value in HOOK_PRESETS:
        preset_path = HOOK_PRESETS[value]
        if preset_path.exists():
            return preset_path
        print(f"⚠️ プリセット '{value}' のファイルが見つかりません: {preset_path}")
        print("   初回セットアップ: bash skills/viral-short-video/scripts/download_assets.sh")
        return None
    p = Path(value)
    if p.exists():
        return p
    print(f"⚠️ ファイルが見つかりません: {value}")
    print(f"   利用可能なプリセット: {', '.join(HOOK_PRESETS.keys())}")
    return None


def extract_keyframes_from_video(video_path: Path, output_dir: Path) -> Optional[Dict]:
    """
    video-frame-reader を使ってキーフレームを抽出する。
    """
    cmd = [
        sys.executable,
        str(VIDEO_FRAME_READER),
        str(video_path),
        "-o", str(output_dir),
        "--threshold", "0.80",   # フック動画は場面転換が多いので低めの閾値
        "--quality", "50",       # Vision API用に少し高めの品質
        "--scale", "0.4",        # 分析用にやや大きめ
        "--fps", "1.0",          # 1秒に1フレーム
    ]

    print(f"🎬 キーフレーム抽出中: {video_path.name}")
    print(f"   コマンド: {' '.join(cmd[:4])}...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"❌ キーフレーム抽出失敗: {result.stderr[-300:]}")
            return None

        extraction_result = json.loads(result.stdout)
        print(f"✅ {extraction_result.get('keyframe_count', 0)}フレーム抽出 "
              f"({extraction_result.get('reduction_rate', 0)}% 削減)")
        return extraction_result

    except subprocess.TimeoutExpired:
        print("❌ キーフレーム抽出タイムアウト (120秒)")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 出力のJSON解析エラー: {e}")
        return None


def score_frames_with_gemini(
    client,
    frame_files: List[str],
    video_name: str,
) -> List[Dict]:
    """
    Gemini Flash Vision で各フレームの「フック度」をスコアリングする。
    バッチ処理で全フレームを一度に送信。
    """
    from google.genai import types
    from PIL import Image

    print(f"\n🔍 Gemini Vision でフック度スコアリング中... ({len(frame_files)}フレーム)")

    # フレーム画像をbase64で添付(最大12枚に制限 — トークン節約)
    max_frames = min(len(frame_files), 12)
    step = max(1, len(frame_files) // max_frames)
    selected_indices = list(range(0, len(frame_files), step))[:max_frames]

    # フレームを画像として読み込み
    contents = []
    contents.append(f"""以下は動画「{video_name}」のキーフレーム画像です。
各フレームについて「フック度（視聴者のスクロールを止める力）」をスコアリングしてください。

## スコアリング基準
- **10点**: 絶対にスクロールを止める。強烈な感情表現/衝撃的なビジュアル/テキストオーバーレイの組み合わせ
- **8-9点**: 非常に強いフック。好奇心を強く刺激する
- **6-7点**: 中程度のフック力。一定の注意を引く
- **4-5点**: 弱いフック。通常のコンテンツ
- **1-3点**: フック力なし。スクロールされる可能性大

## フックタイプ分類
- curiosity_gap: 「知りたい」と思わせる
- pattern_interrupt: 予想外の動き/ビジュアルでスクロール停止
- social_proof: 数字/実績で信頼を示す
- fomo: 見逃し恐怖を煽る
- contrarian: 常識を覆す主張
- emotional: 強い感情を引き出す
- visual_shock: 衝撃的なビジュアル

## 出力形式(JSON配列のみ)
```json
[
  {{
    "frame_index": 1,
    "score": 8.5,
    "hook_type": "pattern_interrupt",
    "reason": "フレームの分析理由",
    "transcript_hint": "画面に表示されているテキストや推定セリフ",
    "visual_elements": "注目すべきビジュアル要素"
  }}
]
```

全{len(selected_indices)}フレームについて必ず回答してください。
各フィールドは簡潔に（reason/transcript_hint/visual_elementsは各20文字以内）。
JSONのみ出力してください。マークダウンのコードブロックで囲まないでください。
""")

    for idx in selected_indices:
        frame_path = frame_files[idx]
        try:
            img = Image.open(frame_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            contents.append(img)
            contents.append(f"↑ フレーム #{idx + 1} (index {idx})")
        except Exception as e:
            print(f"  ⚠️ フレーム {idx+1} の読み込みエラー: {e}")

    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=8192,
            ),
        )

        scores = _parse_json_response(response.text.strip())
        if isinstance(scores, list):
            print(f"✅ {len(scores)}フレームのスコアリング完了")
            return scores
        else:
            print("⚠️ スコアリング結果のJSONパースに失敗")
            return []

    except Exception as e:
        print(f"❌ Gemini Vision エラー: {e}")
        return []


def analyze_video_for_peak_hooks(
    client,
    video_path: Path,
    topic: Optional[str] = None,
    duration: int = 30,
) -> Dict:
    """
    動画を分析してピークフック（最もフックの強い瞬間）を特定する。

    Returns:
        hook_analysis.json の内容
    """
    from google.genai import types

    video_name = video_path.stem

    # Step 1: キーフレーム抽出
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "keyframes"
        extraction_result = extract_keyframes_from_video(video_path, temp_path)

        if not extraction_result:
            return {"error": "キーフレーム抽出に失敗"}
        if isinstance(extraction_result, dict) and "error" in extraction_result:
            return {"error": extraction_result.get("error", "キーフレーム抽出に失敗")}

        frame_files = extraction_result.get("files", [])
        if not frame_files:
            return {"error": "キーフレームが見つかりませんでした"}

        # Step 2: Gemini Vision でスコアリング
        scores = score_frames_with_gemini(client, frame_files, video_name)

        if not scores:
            return {"error": "フレームスコアリングに失敗"}

        # Step 3: ピークフック特定
        sorted_scores = sorted(scores, key=lambda x: x.get("score", 0), reverse=True)
        peak_hooks = sorted_scores[:5]  # 上位5つ

        # Step 4: スクリプト再構成案を生成
        top_hook = peak_hooks[0] if peak_hooks else {}
        recommended_structure = ""

        if top_hook and topic:
            print("\n📝 ピークフックに基づくスクリプト再構成案を生成中...")

            structure_prompt = f"""以下のフック分析結果に基づいて、TikTok/YouTube Shorts動画のスクリプト構成案を作成してください。

## ピークフック情報
- フックタイプ: {top_hook.get('hook_type', '?')}
- 理由: {top_hook.get('reason', '?')}
- 推定セリフ/テキスト: {top_hook.get('transcript_hint', '?')}
- ビジュアル要素: {top_hook.get('visual_elements', '?')}

## 動画パラメータ
- トピック: {topic}
- 目標の長さ: {duration}秒

## 構成案
このフックパターンを冒頭に使い、{duration}秒の動画スクリプト構成案を日本語で簡潔に記述してください。
3行以内で:
1. 冒頭（0-3秒）: フックの具体的な実装方法
2. 本編（3-{duration-3}秒）: 展開の流れ
3. 締め（最後3秒）: CTA

テキストのみで出力してください。"""

            try:
                response = client.models.generate_content(
                    model=get_flash_model(),
                    contents=[structure_prompt],
                    config=types.GenerateContentConfig(
                        temperature=0.5,
                        max_output_tokens=500,
                    ),
                )
                recommended_structure = response.text.strip()
                print("✅ 再構成案生成完了")
            except Exception as e:
                print(f"⚠️ 再構成案生成エラー: {e}")
                recommended_structure = "（生成に失敗しました）"

        # Step 5: 結果をまとめる
        analysis = {
            "source_video": video_name,
            "source_path": str(video_path),
            "total_keyframes_analyzed": len(frame_files),
            "frames_scored": len(scores),
            "peak_hooks": [
                {
                    "rank": i + 1,
                    "frame_index": h.get("frame_index", 0),
                    "timestamp_sec": h.get("frame_index", 0),  # 1fpsで抽出しているのでindex≈秒
                    "score": h.get("score", 0),
                    "hook_type": h.get("hook_type", "unknown"),
                    "reason": h.get("reason", ""),
                    "transcript_hint": h.get("transcript_hint", ""),
                    "visual_elements": h.get("visual_elements", ""),
                }
                for i, h in enumerate(peak_hooks)
            ],
            "all_scores_summary": {
                "avg_score": round(sum(s.get("score", 0) for s in scores) / max(len(scores), 1), 2),
                "max_score": max((s.get("score", 0) for s in scores), default=0),
                "min_score": min((s.get("score", 0) for s in scores), default=0),
            },
            "recommended_structure": recommended_structure,
        }

        return analysis


def print_hook_analysis(analysis: Dict) -> None:
    """フック分析結果のサマリーを表示"""
    print("\n" + "=" * 60)
    print("🎯 ピークフック分析結果")
    print("=" * 60)

    print(f"\nソース動画: {analysis.get('source_video', '?')}")
    print(f"分析フレーム数: {analysis.get('frames_scored', 0)}")

    summary = analysis.get("all_scores_summary", {})
    print(f"平均スコア: {summary.get('avg_score', 0)} / "
          f"最高: {summary.get('max_score', 0)} / "
          f"最低: {summary.get('min_score', 0)}")

    print(f"\n--- ピークフック TOP {len(analysis.get('peak_hooks', []))} ---")
    for hook in analysis.get("peak_hooks", []):
        print(f"\n  #{hook.get('rank', '?')} [スコア {hook.get('score', 0)}/10] "
              f"@ ~{hook.get('timestamp_sec', 0)}秒")
        print(f"     タイプ: {hook.get('hook_type', '?')}")
        print(f"     理由: {hook.get('reason', '')[:80]}")
        if hook.get("transcript_hint"):
            print(f"     テキスト: {hook.get('transcript_hint', '')[:60]}")
        if hook.get("visual_elements"):
            print(f"     ビジュアル: {hook.get('visual_elements', '')[:60]}")

    if analysis.get("recommended_structure"):
        print("\n--- スクリプト再構成案 ---")
        print(f"  {analysis['recommended_structure']}")

    print("=" * 60)


def save_outputs(result: Dict, output_dir: Path) -> None:
    """生成結果をファイルに保存"""
    output_dir.mkdir(parents=True, exist_ok=True)

    # viral_script.json
    viral_path = output_dir / "viral_script.json"
    with open(viral_path, "w", encoding="utf-8") as f:
        json.dump(result["viral_script"], f, ensure_ascii=False, indent=2)
    print(f"📄 {viral_path}")

    # scenes.json
    scenes_path = output_dir / "scenes.json"
    with open(scenes_path, "w", encoding="utf-8") as f:
        json.dump(result["scenes"], f, ensure_ascii=False, indent=2)
    print(f"📄 {scenes_path}")

    # hook_variants.json
    variants_path = output_dir / "hook_variants.json"
    with open(variants_path, "w", encoding="utf-8") as f:
        json.dump(result["hook_variants"], f, ensure_ascii=False, indent=2)
    print(f"📄 {variants_path}")


def run_storyboard_generator(
    scenes_json_path: Path,
    character: str,
    session: str,
) -> None:
    """storyboard-generatorを呼び出す"""
    storyboard_script = (
        Path(__file__).parents[2] / "storyboard-generator" / "scripts" / "generate_storyboard.py"
    )
    if not storyboard_script.exists():
        print(f"⚠️ storyboard-generator が見つかりません: {storyboard_script}")
        return

    # scenes.jsonからシナリオテキストを構築
    with open(scenes_json_path) as f:
        scenes_data = json.load(f)

    scenario_parts = []
    for scene in scenes_data.get("scenes", []):
        narration = scene.get("narration", "")
        if narration:
            scenario_parts.append(narration)
    scenario = " → ".join(scenario_parts)

    num_frames = len(scenes_data.get("scenes", []))
    # clamp to supported values
    if num_frames <= 4:
        num_frames = 4
    elif num_frames <= 8:
        num_frames = 8
    else:
        num_frames = 16

    cmd = [
        sys.executable,
        str(storyboard_script),
        "--scenario", scenario,
        "--character", character,
        "--aspect-ratio", "9:16",
        "--num-frames", str(num_frames),
        "--mode", "sheet",
        "--session", session,
    ]

    print("\n🎨 storyboard-generator を呼び出し中...")
    print(f"   コマンド: {' '.join(cmd[:6])}...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ ストーリーボード生成完了")
            if result.stdout:
                # 出力の最後の数行を表示
                lines = result.stdout.strip().split("\n")
                for line in lines[-10:]:
                    print(f"   {line}")
        else:
            print("❌ storyboard-generator エラー:")
            if result.stderr:
                print(result.stderr[-500:])
    except subprocess.TimeoutExpired:
        print("❌ storyboard-generator タイムアウト (300秒)")


def print_script_summary(result: Dict) -> None:
    """スクリプトのサマリーを表示"""
    vs = result.get("viral_script", {})
    scenes = result.get("scenes", {}).get("scenes", [])
    variants = result.get("hook_variants", [])

    hook = vs.get("hook", {})
    cta = vs.get("cta", {})
    loop = vs.get("loop_bridge", {})
    flash = vs.get("flash_text", {})
    tech = vs.get("viral_techniques", {})

    print("\n" + "=" * 60)
    print("📊 バイラルスクリプト サマリー")
    print("=" * 60)

    meta = vs.get("meta", {})
    print(f"\nトピック: {meta.get('topic', '?')}")
    if meta.get("product"):
        print(f"商材: {meta['product']}")
    print(f"長さ: {meta.get('duration', '?')}秒 / シーン数: {len(scenes)}")
    print(f"トーン: {meta.get('tone', '?')}")

    print("\n--- Hook ---")
    print(f"  [{hook.get('trigger_type', '?')}] {hook.get('text', '')}")
    print(f"  表情: {hook.get('emotion', '?')} / 映像: {hook.get('visual_note', '')[:60]}")

    print(f"\n--- Body ({len(vs.get('body', []))}セグメント) ---")
    for i, seg in enumerate(vs.get("body", [])):
        print(f"  [{i+1}] {seg.get('text', '')[:60]}...")

    print("\n--- CTA ---")
    print(f"  {cta.get('text', '')}")

    print("\n--- バイラルテクニック ---")
    print(f"  ループブリッジ: {'✅' if loop.get('enabled') else '❌'}", end="")
    if loop.get("enabled"):
        print(f" → {loop.get('end_text', '')[:40]}")
    else:
        print()
    print(f"  フラッシュテキスト: {'✅' if flash.get('enabled') else '❌'}", end="")
    if flash.get("enabled"):
        print(f" → [{flash.get('color', 'red')}] {flash.get('text', '')}")
    else:
        print()
    print(f"  スプリットスクリーン: {'✅' if tech.get('split_screen') else '❌'}")
    print(f"  字幕: {'✅' if tech.get('captions') else '❌'}")
    print(f"  ロファイ感: {'✅' if tech.get('lofi_aesthetic') else '❌'}")
    print(f"  音声速度: {tech.get('speech_speed', 1.0)}x")

    print(f"\n--- フックバリエーション ({len(variants)}個) ---")
    for i, v in enumerate(variants):
        print(f"  [{i+1}] [{v.get('trigger_type', '?')}] {v.get('text', '')}")

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Viral Short Video Script Generator - TikTok/YouTube Shorts向けバイラルスクリプト生成"
    )

    parser.add_argument("--topic", "-t", required=True, help="動画のトピック/テーマ")
    parser.add_argument("--product", "-p", help="商材/サービス名")
    parser.add_argument(
        "--duration", "-d", type=int, default=30, choices=[15, 30, 60],
        help="動画の長さ（秒）"
    )
    parser.add_argument("--target", help="ターゲット層の説明")
    parser.add_argument(
        "--tone", default="casual",
        choices=["casual", "professional", "energetic", "storytelling"],
        help="トーン"
    )
    parser.add_argument(
        "--hook-style", default="auto",
        choices=["auto", "curiosity", "fomo", "social_proof", "pattern_interrupt", "contrarian"],
        help="フックスタイル"
    )
    parser.add_argument("--no-loop", action="store_true", help="ループブリッジを無効化")
    parser.add_argument("--no-flash", action="store_true", help="フラッシュテキストを無効化")
    parser.add_argument("--split-screen", action="store_true", help="スプリットスクリーン用指示を含める")
    parser.add_argument(
        "--variants", type=int, default=3, help="フックバリエーション数"
    )
    parser.add_argument(
        "--lang", default="ja", choices=["ja", "en"], help="スクリプト言語"
    )
    parser.add_argument("--session", "-s", help="セッション名（出力フォルダ名）")
    parser.add_argument("--dry-run", action="store_true", help="結果を表示のみ（保存しない）")

    # ピークフック抽出
    parser.add_argument(
        "--analyze-video",
        help="バズ動画を分析してピークフックを抽出。"
             "プリセット名(hook_viral_10, hook_trifecta, hook_600k_gmv)またはファイルパスを指定"
    )

    # ストーリーボード連携
    parser.add_argument(
        "--generate-storyboard", action="store_true",
        help="storyboard-generatorを呼び出して絵コンテも生成"
    )
    parser.add_argument(
        "--character", help="ストーリーボード用キャラクター説明"
    )

    args = parser.parse_args()

    # hook_style の短縮名を正式名に
    hook_map = {
        "curiosity": "curiosity_gap",
        "fomo": "fomo",
        "social_proof": "social_proof",
        "pattern_interrupt": "pattern_interrupt",
        "contrarian": "contrarian",
        "auto": "auto",
    }
    hook_style = hook_map.get(args.hook_style, "auto")

    # クライアント初期化
    client = get_client()
    if not client:
        print("❌ GEMINI_API_KEY が設定されていません")
        sys.exit(1)

    # --- ピークフック抽出モード ---
    if args.analyze_video:
        video_path = resolve_analyze_video_path(args.analyze_video)
        if not video_path:
            sys.exit(1)

        print(f"\n🎯 ピークフック抽出モード: {video_path.name}")
        analysis = analyze_video_for_peak_hooks(
            client=client,
            video_path=video_path,
            topic=args.topic,
            duration=args.duration,
        )

        if "error" in analysis:
            print(f"❌ エラー: {analysis['error']}")
            sys.exit(1)

        print_hook_analysis(analysis)

        if not args.dry_run:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_name = args.session or f"hook_analysis_{video_path.stem}"
            output_dir = DEFAULT_OUTPUT_DIR / f"{timestamp}_{session_name}"
            output_dir.mkdir(parents=True, exist_ok=True)

            analysis_path = output_dir / "hook_analysis.json"
            with open(analysis_path, "w", encoding="utf-8") as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            print(f"\n📄 分析結果: {analysis_path}")

            # スクリプト生成も続けるかどうか
            print("\n💡 この分析結果を元にスクリプトを生成するには:")
            print(f"   python {__file__} --topic \"{args.topic}\" --duration {args.duration}")
        else:
            print("\n(dry-run: ファイル保存をスキップ)")
        return

    # --- 通常のスクリプト生成モード ---
    result = generate_viral_script(
        client=client,
        topic=args.topic,
        product=args.product,
        duration=args.duration,
        target=args.target,
        tone=args.tone,
        hook_style=hook_style,
        lang=args.lang,
        enable_loop=not args.no_loop,
        enable_flash=not args.no_flash,
        enable_split_screen=args.split_screen,
        num_variants=args.variants,
    )

    if not result:
        print("❌ スクリプト生成に失敗しました")
        sys.exit(1)

    # サマリー表示
    print_script_summary(result)

    if args.dry_run:
        print("\n(dry-run: ファイル保存をスキップ)")
        return

    # ファイル保存
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_name = args.session or args.topic[:30].replace(" ", "_")
    output_dir = DEFAULT_OUTPUT_DIR / f"{timestamp}_{session_name}"

    print(f"\n📁 出力ディレクトリ: {output_dir}")
    save_outputs(result, output_dir)

    # ストーリーボード生成
    if args.generate_storyboard:
        if not args.character:
            print("⚠️ --character が未指定です。デフォルトキャラクターを使用します")
            args.character = "20代の日本人、カジュアルな服装、明るい表情、自然な室内背景"

        run_storyboard_generator(
            scenes_json_path=output_dir / "scenes.json",
            character=args.character,
            session=session_name,
        )

    # 次のステップを案内
    print("\n" + "=" * 60)
    print("📌 次のステップ")
    print("=" * 60)
    print("\n1. ストーリーボード生成:")
    print("   python skills/storyboard-generator/scripts/generate_storyboard.py \\")
    print(f'     --scenario "$(cat {output_dir / "scenes.json"} | python -c "import sys,json; print(json.load(sys.stdin)[\'title\'])")" \\')
    print(f'     --character "20代の日本人、カジュアルな服装" \\')
    print(f"     --num-frames {min(len(result['scenes']['scenes']), 8)} --mode sheet")
    print("\n2. 動画合成（ストーリーボード生成後）:")
    print("   python skills/video-editor/scripts/compose_video.py \\")
    print("     --storyboard-dir <storyboard_output_dir> --captions")

    flash = result.get("viral_script", {}).get("flash_text", {})
    if flash.get("enabled"):
        print(f'     --flash-text "{flash.get("text", "")}" --flash-color {flash.get("color", "red")}')

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
