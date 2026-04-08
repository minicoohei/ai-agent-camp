"""
Video Scriptwriter - 企画・スクリプト自動生成
テーマ + フォーマット → scenes.json（storyboard/audio/editor互換）

フォーマット:
  - split_screen_teaching: 教育系（上半分テキスト+TTS / 下半分ゲーム映像）
  - ranking_list: ランキング/リスト型（TOP5等）
  - reddit_story: Reddit/2ch読み上げ型
  - dark_facts: ダークファクト/雑学型
  - standard_teaching: 標準教育型（フルスクリーン）
  - product_intro: 商品紹介型
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Playbook参照
PLAYBOOKS_DIR = Path(__file__).parents[2] / "video-playbook" / "playbooks"

# フォーマット定義
FORMATS = {
    "split_screen_teaching": {
        "name": "Split-Screen教育型",
        "description": "上半分にテキスト+ナレーション、下半分にゲーム映像（Minecraft/Subway Surfers等）",
        "typical_duration": 30,
        "scene_count": {"15s": 5, "30s": 8, "60s": 14},
        "structure": "hook → problem → explanation(multiple) → summary → cta",
        "layout": "split_screen",
        "split_ratio": "60:40",  # 上:下
    },
    "ranking_list": {
        "name": "ランキング/リスト型",
        "description": "「○○ランキングTOP5」等、カウントダウン形式",
        "typical_duration": 30,
        "scene_count": {"15s": 5, "30s": 7, "60s": 12},
        "structure": "hook → item5 → item4 → item3 → item2 → item1 → cta",
        "layout": "fullscreen",
    },
    "reddit_story": {
        "name": "Reddit/2ch読み上げ型",
        "description": "テキストスクロール + TTS + 背景動画",
        "typical_duration": 60,
        "scene_count": {"15s": 4, "30s": 7, "60s": 12},
        "structure": "hook → setup → conflict → twist → resolution → reaction",
        "layout": "text_scroll",
        "background": "gameplay",
    },
    "dark_facts": {
        "name": "ダークファクト/雑学型",
        "description": "「知ると怖い○○」系、AI画像+テロップ",
        "typical_duration": 30,
        "scene_count": {"15s": 5, "30s": 8, "60s": 14},
        "structure": "hook → fact1 → fact2 → fact3 → shocking_reveal → cta",
        "layout": "fullscreen",
    },
    "standard_teaching": {
        "name": "標準教育型",
        "description": "フルスクリーンの教育/解説動画",
        "typical_duration": 30,
        "scene_count": {"15s": 5, "30s": 8, "60s": 14},
        "structure": "hook → problem → core_concept → mechanism → solution → cta",
        "layout": "fullscreen",
    },
    "product_intro": {
        "name": "商品紹介型",
        "description": "商品/サービスの紹介・レビュー",
        "typical_duration": 30,
        "scene_count": {"15s": 5, "30s": 8, "60s": 12},
        "structure": "result_first → problem → product_intro → demo → benefit → cta",
        "layout": "fullscreen",
    },
}

# Hook テンプレート
HOOK_TEMPLATES = {
    "question": "「{topic}」について知っていますか？",
    "shocking": "99%の人が知らない{topic}の真実",
    "pov": "POV: {topic}を知った瞬間",
    "wait": "最後まで見て。{topic}がヤバすぎる",
    "ranking": "{topic}ランキングTOP{count}",
    "dark": "知ると怖い{topic}の事実",
    "nobody": "誰も教えてくれない{topic}の話",
    "comparison": "{topic}、あなたはどっち派？",
}


def load_playbook(video_type: str) -> Optional[Dict]:
    """Playbookの知見を読み込む"""
    playbook_path = PLAYBOOKS_DIR / f"{video_type}.json"
    if playbook_path.exists():
        with open(playbook_path) as f:
            return json.load(f)
    return None


def get_api_key() -> str:
    """Gemini API keyを取得"""
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        env_file = Path(__file__).parents[3] / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("GEMINI_API_KEY"):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def generate_with_gemini(prompt: str, api_key: str) -> str:
    """Gemini APIでテキスト生成"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }).encode()
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    return text


def build_prompt(
    topic: str,
    format_key: str,
    duration: str,
    language: str,
    hook_style: str,
    playbook: Optional[Dict],
    custom_instructions: str = ""
) -> str:
    """スクリプト生成用のプロンプトを構築"""
    fmt = FORMATS[format_key]
    num_scenes = fmt["scene_count"].get(duration, 8)
    
    # Playbook知見の組み込み
    playbook_context = ""
    if playbook and playbook.get("aggregated"):
        agg = playbook["aggregated"]
        playbook_context = f"""
## 参考: Playbook知見（{agg.get('sample_count', 0)}本の分析データ）
- 平均シーン長: {agg.get('avg_scene_duration', 3)}秒
- ペーシング: {agg.get('common_pacing', 'fast')}
- よく使われる構成: {', '.join(agg.get('common_structures', [])[:3])}
- テロップスタイル: {', '.join(agg.get('caption_styles', [])[:2])}
- テクニック: {', '.join(agg.get('all_techniques', [])[:5])}
"""

    # フォーマット別の追加指示
    format_instructions = ""
    if format_key == "split_screen_teaching":
        format_instructions = """
## Split-Screen特有の指示
- visual_promptは「上半分」に表示する内容のみ記述（下半分はゲーム映像で自動合成）
- テロップは画面上部60%の範囲内に収める
- ナレーションは簡潔に（1シーン15-25文字）
- 各シーンにsplit_screen: trueフラグを設定
"""
    elif format_key == "ranking_list":
        format_instructions = """
## ランキング型特有の指示
- 順位を大きく表示（テロップの一部として）
- 最後の1位は他より長めのシーン
- 各アイテムにrank番号を設定
- ナレーションで「第○位は...」と読み上げ
"""
    elif format_key == "reddit_story":
        format_instructions = """
## ストーリー読み上げ型特有の指示
- narrationにストーリーの全文を入れる（長文OK）
- visual_promptは雰囲気を伝える背景イメージ（テキストは後乗せ）
- テキストスクロール用にtext_overlay.scroll: trueを設定
- 感情の起伏を意識（淡々→緊張→驚き→感動）
"""

    prompt = f"""あなたはTikTok動画のプロ脚本家です。
以下の条件でscenes.jsonを生成してください。

## トピック
{topic}

## フォーマット
{fmt['name']}（{fmt['description']}）

## 構成パターン
{fmt['structure']}

## 条件
- 動画尺: {duration}
- シーン数: {num_scenes}
- 言語: {language}
- Hookスタイル: {hook_style}

{format_instructions}
{playbook_context}
{f"## 追加指示{chr(10)}{custom_instructions}" if custom_instructions else ""}

## 重要ルール
1. 冒頭3秒で視聴者を掴む（hook）
2. テロップは1行5-8文字（日本語の場合）
3. ナレーションは簡潔でパンチのある表現
4. visual_promptは英語で記述（AI画像生成用）
5. visual_promptに「NO text, NO letters, NO words, NO writing」を必ず含める
6. 最後にCTA（いいね、フォロー、コメント誘導）
7. motion_typeは全シーン"i2v"（静止画禁止）

## 出力形式（JSON）
```json
{{
  "title": "動画タイトル",
  "format": "{format_key}",
  "duration": "{duration}",
  "language": "{language}",
  "hook_style": "{hook_style}",
  "scenes": [
    {{
      "frame_number": 1,
      "timestamp": "0:00-0:03",
      "duration": 3.0,
      "scene_type": "hook",
      "description": "シーンの説明（日本語）",
      "visual_prompt": "English prompt for AI image generation. NO text, NO letters...",
      "camera_angle": "close_up / medium / wide",
      "narration": "ナレーション文（日本語）",
      "text_overlay": {{
        "main_text": "テロップ",
        "sub_text": "",
        "position": "center",
        "style": "bold"
      }},
      "motion_type": "i2v",
      "energy": "high / medium / low"
    }}
  ],
  "metadata": {{
    "target_audience": "ターゲット層",
    "key_message": "核心メッセージ",
    "cta_type": "like / follow / comment / share",
    "estimated_retention_hooks": ["使用した維持テクニック"]
  }}
}}
```

JSONのみ出力してください。"""
    
    return prompt


def generate_script(
    topic: str,
    format_key: str = "standard_teaching",
    duration: str = "30s",
    language: str = "ja",
    hook_style: str = "question",
    output_dir: Optional[Path] = None,
    custom_instructions: str = ""
) -> Path:
    """メイン: トピック → scenes.json生成"""
    
    print(f"\n{'='*60}")
    print(f"🎬 スクリプト生成: {topic}")
    print(f"   フォーマット: {FORMATS[format_key]['name']}")
    print(f"   尺: {duration} / Hook: {hook_style} / 言語: {language}")
    print(f"{'='*60}\n")
    
    # API Key
    api_key = get_api_key()
    if not api_key:
        print("❌ GEMINI_API_KEY未設定")
        sys.exit(1)
    
    # Playbook読み込み
    video_type_map = {
        "split_screen_teaching": "teaching",
        "ranking_list": "teaching",
        "reddit_story": "clip",
        "dark_facts": "teaching",
        "standard_teaching": "teaching",
        "product_intro": "intro",
    }
    playbook = load_playbook(video_type_map.get(format_key, "teaching"))
    if playbook:
        print(f"📚 Playbook参照: {playbook.get('type')} ({playbook.get('aggregated', {}).get('sample_count', 0)}本)")
    
    # プロンプト生成
    prompt = build_prompt(topic, format_key, duration, language, hook_style, playbook, custom_instructions)
    
    # Gemini API呼び出し
    print("🤖 Geminiでスクリプト生成中...")
    raw_output = generate_with_gemini(prompt, api_key)
    
    # JSON抽出
    if "```json" in raw_output:
        json_str = raw_output.split("```json")[1].split("```")[0]
    elif "```" in raw_output:
        json_str = raw_output.split("```")[1].split("```")[0]
    else:
        json_str = raw_output
    
    script = json.loads(json_str.strip())
    
    # 出力
    if output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic[:30].replace(" ", "_").replace("/", "_")
        output_dir = Path("output/scripts") / f"{timestamp}_{safe_topic}"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "scenes.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(script, f, ensure_ascii=False, indent=2)
    
    # サマリー表示
    scenes = script.get("scenes", [])
    print(f"\n✅ スクリプト生成完了: {output_path}")
    print(f"   タイトル: {script.get('title', '不明')}")
    print(f"   シーン数: {len(scenes)}")
    print(f"   フォーマット: {script.get('format', format_key)}")
    
    total_dur = sum(s.get("duration", 3) for s in scenes)
    print(f"   推定尺: {total_dur:.0f}秒")
    
    print(f"\n📋 シーン一覧:")
    for s in scenes:
        stype = s.get("scene_type", "?")
        narr = s.get("narration", "")[:30]
        text = s.get("text_overlay", {}).get("main_text", "")[:20]
        print(f"   {s.get('frame_number', '?'):2d}. [{stype:12s}] {narr}... | テロップ: {text}")
    
    if script.get("metadata"):
        meta = script["metadata"]
        print(f"\n🎯 メタデータ:")
        print(f"   ターゲット: {meta.get('target_audience', '?')}")
        print(f"   CTA: {meta.get('cta_type', '?')}")
        hooks = meta.get("estimated_retention_hooks", [])
        if hooks:
            print(f"   維持テクニック: {', '.join(hooks)}")
    
    return output_path


def list_formats():
    """利用可能なフォーマット一覧"""
    print("\n📺 利用可能なフォーマット:")
    print(f"{'='*60}")
    for key, fmt in FORMATS.items():
        print(f"\n  {key}")
        print(f"    {fmt['name']}")
        print(f"    {fmt['description']}")
        print(f"    構成: {fmt['structure']}")
        durations = ", ".join(f"{d}={n}scenes" for d, n in fmt["scene_count"].items())
        print(f"    尺: {durations}")


def main():
    parser = argparse.ArgumentParser(description="TikTok動画スクリプト自動生成")
    parser.add_argument("--topic", "-t", help="動画のトピック/テーマ")
    parser.add_argument("--format", "-f", default="standard_teaching",
                       choices=list(FORMATS.keys()), help="フォーマット")
    parser.add_argument("--duration", "-d", default="30s",
                       choices=["15s", "30s", "60s"], help="動画の尺")
    parser.add_argument("--language", "-l", default="ja", help="言語")
    parser.add_argument("--hook", default="question",
                       choices=list(HOOK_TEMPLATES.keys()), help="Hookスタイル")
    parser.add_argument("--output", "-o", help="出力ディレクトリ")
    parser.add_argument("--instructions", "-i", help="追加指示")
    parser.add_argument("--list-formats", action="store_true", help="フォーマット一覧")
    args = parser.parse_args()
    
    if args.list_formats:
        list_formats()
        return
    
    if not args.topic:
        print("❌ --topic を指定してください")
        print("   例: --topic '睡眠の質を上げる5つの方法'")
        parser.print_help()
        sys.exit(1)
    
    output_dir = Path(args.output) if args.output else None
    generate_script(
        topic=args.topic,
        format_key=args.format,
        duration=args.duration,
        language=args.language,
        hook_style=args.hook,
        output_dir=output_dir,
        custom_instructions=args.instructions or ""
    )


if __name__ == "__main__":
    main()
