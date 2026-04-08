#!/usr/bin/env python3
"""
Video Playbook Manager - 動画分析結果からタイプ別Playbookに知見を蓄積・活用

使い方:
  --add -t template.json   分析結果からPlaybookに知見を追加
  --show TYPE              タイプ別Playbookを表示
  --list                   全Playbookの一覧（サンプル数付き）
  --export TYPE            Playbookをマークダウンでエクスポート
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Playbookディレクトリ
PLAYBOOKS_DIR = Path(__file__).parents[1] / "playbooks"

# 動画タイプ定義
VIDEO_TYPES = {
    "intro": "紹介・レビュー（商品紹介、サービス紹介、人物紹介）",
    "teaching": "ティーチング・解説（ハウツー、知識共有、tips、ノウハウ）",
    "template": "テンプレート・トレンド（流行りのフォーマット、音源同期、チャレンジ）",
    "meme": "Meme・ネタ（オチ重視、ユーモア、パロディ）",
    "dance": "ダンス・パフォーマンス（振付、BPM同期、カバー）",
    "mv": "MV・シネマティック（音楽映像、エフェクト重視、映画的演出）",
    "clip": "切り抜き・ハイライト（長尺→短尺、名場面、配信切り抜き）",
}


def classify_video_type(template: Dict) -> str:
    """テンプレートのsummaryから動画タイプを判定"""
    summary = template.get("summary", {})
    category = summary.get("category", "").lower()
    structure = summary.get("structure", "").lower()
    transcript = summary.get("full_transcript", "").lower()

    # ルールベース判定（summaryのcategoryから）
    if any(w in category for w in ["tutorial", "howto", "education", "tips"]):
        return "teaching"
    if any(w in category for w in ["product", "review", "intro", "unbox"]):
        return "intro"
    if any(w in category for w in ["meme", "comedy", "funny", "parody"]):
        return "meme"
    if any(w in category for w in ["dance", "choreography", "performance"]):
        return "dance"
    if any(w in category for w in ["music", "mv", "cinematic", "lyric"]):
        return "mv"
    if any(w in category for w in ["clip", "highlight", "compilation", "切り抜き"]):
        return "clip"
    if any(w in category for w in ["trend", "template", "challenge"]):
        return "template"

    # トランスクリプトベース
    if any(w in transcript for w in ["方法", "やり方", "コツ", "解説", "教え", "ポイント", "特徴"]):
        return "teaching"
    if any(w in transcript for w in ["紹介", "レビュー", "おすすめ", "買って"]):
        return "intro"

    return "teaching"  # デフォルト


def extract_playbook_insights(video_type: str, template: Dict) -> Dict:
    """テンプレートからタイプ別の制作知見を抽出"""
    summary = template.get("summary", {})
    scenes = template.get("scenes", [])

    # シーン長の統計
    durations = [s.get("duration", 0) for s in scenes if s.get("duration")]
    avg_dur = sum(durations) / len(durations) if durations else 3.0
    min_dur = min(durations) if durations else 1.0
    max_dur = max(durations) if durations else 5.0

    # テロップ分析
    captions = [s.get("text_overlay", {}) for s in scenes if s.get("text_overlay", {}).get("text")]
    caption_positions = [c.get("position", "center") for c in captions]
    caption_colors = [c.get("color", "#FFFFFF") for c in captions]

    # ショットタイプ分析
    shot_types = [s.get("visual", {}).get("shot_type", "medium") for s in scenes]

    # ナレーション情報
    narrations = [s.get("narration", "") for s in scenes if s.get("narration")]
    full_transcript = summary.get("full_transcript", "")

    # STTセグメント数の推定（ナレーション有りシーン数で代用）
    duration = template.get("duration", 0)

    insight = {
        "source_url": template.get("source_url", ""),
        "analyzed_at": datetime.now().isoformat(),
        "duration": duration,
        "total_scenes": len(scenes),

        # タイミング
        "timing": {
            "avg_scene_duration": round(avg_dur, 1),
            "min_scene_duration": round(min_dur, 1),
            "max_scene_duration": round(max_dur, 1),
            "pacing": summary.get("pacing", "medium"),
        },

        # 構成
        "structure": {
            "pattern": summary.get("structure", ""),
            "hook_duration": durations[0] if durations else 2.0,
            "key_techniques": summary.get("key_techniques", []),
        },

        # テロップ
        "captions": {
            "style": summary.get("caption_style", ""),
            "dominant_position": max(set(caption_positions), key=caption_positions.count) if caption_positions else "center",
            "colors_used": list(set(caption_colors))[:5],
            "density": len(captions) / len(scenes) if scenes else 0,
        },

        # ビジュアル
        "visual": {
            "dominant_shot_type": max(set(shot_types), key=shot_types.count) if shot_types else "medium",
            "shot_variety": len(set(shot_types)),
            "resolution": template.get("resolution", "不明"),
        },

        # 音声
        "audio": {
            "has_narration": bool(full_transcript),
            "narration_density": len(narrations) / (duration / 10) if duration > 0 else 0,
            "words_per_scene": len(full_transcript) / max(1, len(scenes)),
        },
    }

    return insight


def update_playbook(video_type: str, insight: Dict) -> Dict:
    """タイプ別playbookに知見を追加"""
    PLAYBOOKS_DIR.mkdir(parents=True, exist_ok=True)
    playbook_path = PLAYBOOKS_DIR / f"{video_type}.json"

    if playbook_path.exists():
        with open(playbook_path) as f:
            playbook = json.load(f)
    else:
        playbook = {
            "type": video_type,
            "description": VIDEO_TYPES.get(video_type, ""),
            "insights": [],
            "aggregated": {},
        }

    # 知見追加
    playbook["insights"].append(insight)

    # 集計更新
    insights = playbook["insights"]
    n = len(insights)

    playbook["aggregated"] = {
        "sample_count": n,
        "avg_duration": round(sum(i["duration"] for i in insights) / n, 1),
        "avg_scenes": round(sum(i["total_scenes"] for i in insights) / n, 1),
        "avg_scene_duration": round(sum(i["timing"]["avg_scene_duration"] for i in insights) / n, 1),
        "common_pacing": max(
            set(i["timing"]["pacing"] for i in insights),
            key=lambda x: sum(1 for i in insights if i["timing"]["pacing"] == x)
        ),
        "common_structures": [i["structure"]["pattern"] for i in insights if i["structure"]["pattern"]],
        "all_techniques": list(set(t for i in insights for t in i["structure"].get("key_techniques", []))),
        "caption_styles": [i["captions"]["style"] for i in insights if i["captions"]["style"]],
        "common_caption_position": max(
            set(i["captions"]["dominant_position"] for i in insights),
            key=lambda x: sum(1 for i in insights if i["captions"]["dominant_position"] == x)
        ),
    }

    with open(playbook_path, "w", encoding="utf-8") as f:
        json.dump(playbook, f, ensure_ascii=False, indent=2)

    print(f"📚 Playbook更新: {playbook_path} ({n}本の分析データ)")
    return playbook


def cmd_add(template_path: str):
    """テンプレートからPlaybookに知見を追加"""
    path = Path(template_path)
    if not path.exists():
        print(f"❌ ファイルが見つかりません: {template_path}")
        sys.exit(1)

    with open(path) as f:
        template = json.load(f)

    # 動画タイプ判定
    video_type = classify_video_type(template)
    print(f"🏷️ 動画タイプ判定: {video_type} ({VIDEO_TYPES.get(video_type, '')})")

    # 知見抽出
    insight = extract_playbook_insights(video_type, template)

    # Playbook更新
    playbook = update_playbook(video_type, insight)

    print(f"\n✅ Playbook蓄積完了")
    print(f"   タイプ: {video_type}")
    print(f"   サンプル数: {playbook['aggregated']['sample_count']}")
    print(f"   ソース: {template.get('source_url', '不明')}")


def cmd_show(video_type: str):
    """タイプ別Playbookを表示"""
    if video_type not in VIDEO_TYPES:
        print(f"❌ 未知のタイプ: {video_type}")
        print(f"   有効なタイプ: {', '.join(VIDEO_TYPES.keys())}")
        sys.exit(1)

    playbook_path = PLAYBOOKS_DIR / f"{video_type}.json"
    if not playbook_path.exists():
        print(f"⚠️ Playbookが見つかりません: {video_type}")
        print(f"   まだ分析データがありません。--add で追加してください。")
        return

    with open(playbook_path) as f:
        playbook = json.load(f)

    agg = playbook.get("aggregated", {})
    print(f"\n{'='*60}")
    print(f"📚 Playbook: {video_type}")
    print(f"   {VIDEO_TYPES[video_type]}")
    print(f"{'='*60}\n")

    print(f"📊 サンプル数: {agg.get('sample_count', 0)}")
    print(f"⏱️ 平均動画長: {agg.get('avg_duration', 0)}秒")
    print(f"🎬 平均シーン数: {agg.get('avg_scenes', 0)}")
    print(f"⚡ 平均シーン長: {agg.get('avg_scene_duration', 0)}秒")
    print(f"🏃 ペーシング: {agg.get('common_pacing', '不明')}")
    print(f"📍 テロップ位置: {agg.get('common_caption_position', '不明')}")

    structures = agg.get("common_structures", [])
    if structures:
        print(f"\n📐 構成パターン:")
        for s in structures:
            print(f"   • {s}")

    techniques = agg.get("all_techniques", [])
    if techniques:
        print(f"\n🛠️ 使用テクニック:")
        for t in techniques:
            print(f"   • {t}")

    styles = agg.get("caption_styles", [])
    if styles:
        print(f"\n🔤 テロップスタイル:")
        for s in styles:
            print(f"   • {s}")


def cmd_list():
    """全Playbookの一覧"""
    PLAYBOOKS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n📚 Playbook一覧")
    print(f"{'='*60}")

    found = False
    for type_key, type_desc in VIDEO_TYPES.items():
        playbook_path = PLAYBOOKS_DIR / f"{type_key}.json"
        if playbook_path.exists():
            with open(playbook_path) as f:
                playbook = json.load(f)
            count = playbook.get("aggregated", {}).get("sample_count", 0)
            avg_dur = playbook.get("aggregated", {}).get("avg_duration", 0)
            print(f"  📖 {type_key:12s} | {count:3d}本 | 平均{avg_dur:.0f}秒 | {type_desc}")
            found = True
        else:
            print(f"  📄 {type_key:12s} |   0本 |          | {type_desc}")

    if not found:
        print(f"\n  ⚠️ まだPlaybookがありません。")
        print(f"     video-analyzerで分析後、--add で追加してください。")

    print(f"\n💡 詳細: --show TYPE  |  エクスポート: --export TYPE")


def cmd_export(video_type: str):
    """PlaybookをMarkdown形式でエクスポート"""
    if video_type not in VIDEO_TYPES:
        print(f"❌ 未知のタイプ: {video_type}")
        print(f"   有効なタイプ: {', '.join(VIDEO_TYPES.keys())}")
        sys.exit(1)

    playbook_path = PLAYBOOKS_DIR / f"{video_type}.json"
    if not playbook_path.exists():
        print(f"⚠️ Playbookが見つかりません: {video_type}")
        return

    with open(playbook_path) as f:
        playbook = json.load(f)

    agg = playbook.get("aggregated", {})
    insights = playbook.get("insights", [])

    # Markdown生成
    md = []
    md.append(f"# 📚 Playbook: {video_type}")
    md.append(f"")
    md.append(f"**{VIDEO_TYPES[video_type]}**")
    md.append(f"")
    md.append(f"## 概要")
    md.append(f"")
    md.append(f"- サンプル数: **{agg.get('sample_count', 0)}本**")
    md.append(f"- 平均動画長: **{agg.get('avg_duration', 0)}秒**")
    md.append(f"- 平均シーン数: **{agg.get('avg_scenes', 0)}**")
    md.append(f"- 平均シーン長: **{agg.get('avg_scene_duration', 0)}秒**")
    md.append(f"- ペーシング: **{agg.get('common_pacing', '不明')}**")
    md.append(f"- テロップ位置: **{agg.get('common_caption_position', '不明')}**")
    md.append(f"")

    structures = agg.get("common_structures", [])
    if structures:
        md.append(f"## 構成パターン")
        md.append(f"")
        for s in structures:
            md.append(f"- {s}")
        md.append(f"")

    techniques = agg.get("all_techniques", [])
    if techniques:
        md.append(f"## 使用テクニック")
        md.append(f"")
        for t in techniques:
            md.append(f"- {t}")
        md.append(f"")

    styles = agg.get("caption_styles", [])
    if styles:
        md.append(f"## テロップスタイル")
        md.append(f"")
        for s in styles:
            md.append(f"- {s}")
        md.append(f"")

    # 個別分析サマリー
    if insights:
        md.append(f"## 分析済み動画")
        md.append(f"")
        for i, ins in enumerate(insights, 1):
            md.append(f"### {i}. {ins.get('source_url', '不明')}")
            md.append(f"")
            md.append(f"- 分析日: {ins.get('analyzed_at', '不明')}")
            md.append(f"- 動画長: {ins.get('duration', 0)}秒 / {ins.get('total_scenes', 0)}シーン")
            md.append(f"- ペーシング: {ins.get('timing', {}).get('pacing', '不明')}")
            pattern = ins.get("structure", {}).get("pattern", "")
            if pattern:
                md.append(f"- 構成: {pattern}")
            md.append(f"")

    output = "\n".join(md)
    print(output)

    # ファイルにも保存
    export_path = PLAYBOOKS_DIR / f"{video_type}_playbook.md"
    with open(export_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"\n📄 エクスポート保存: {export_path}")


def main():
    parser = argparse.ArgumentParser(
        description="動画Playbook管理 - タイプ別知見の蓄積・活用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 分析結果をPlaybookに追加
  python manage_playbook.py --add -t output/templates/video_001/template.json
  
  # Playbook一覧
  python manage_playbook.py --list
  
  # 特定タイプのPlaybook表示
  python manage_playbook.py --show teaching
  
  # Markdownエクスポート
  python manage_playbook.py --export teaching

動画タイプ:
  intro     紹介・レビュー
  teaching  ティーチング・解説
  template  テンプレート・トレンド
  meme      Meme・ネタ
  dance     ダンス・パフォーマンス
  mv        MV・シネマティック
  clip      切り抜き・ハイライト
"""
    )
    parser.add_argument("--add", action="store_true", help="テンプレートからPlaybookに知見を追加")
    parser.add_argument("-t", "--template", help="テンプレートJSONファイルパス（--add時に必須）")
    parser.add_argument("--show", metavar="TYPE", help="タイプ別Playbookを表示")
    parser.add_argument("--list", action="store_true", help="全Playbookの一覧")
    parser.add_argument("--export", metavar="TYPE", help="PlaybookをMarkdown形式でエクスポート")
    args = parser.parse_args()

    if args.add:
        if not args.template:
            print("❌ --add には -t/--template が必要です")
            sys.exit(1)
        cmd_add(args.template)
    elif args.show:
        cmd_show(args.show)
    elif args.list:
        cmd_list()
    elif args.export:
        cmd_export(args.export)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
