#!/usr/bin/env python3
"""
clipper.py - YouTube Clipper メインCLI

動画 → DL → 字幕取得 → AIチャプター分析 → インタラクティブ選択 → クリップ抽出

Usage:
    python clipper.py --url "https://youtube.com/watch?v=xxxxx"
    python clipper.py --file /path/to/local.mp4
    python clipper.py --url "..." --auto-select "score>0.8"
    python clipper.py --url "..." --auto-select all
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# スクリプトディレクトリをパスに追加
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
ROOT_DIR = Path(__file__).resolve().parents[3]

from downloader import get_video_info, download_video, download_subtitles
from transcriber import transcribe_video
from chapter_analyzer import load_srt, analyze_chapters, display_chapters
from subtitle_translator import translate_srt, create_bilingual_srt
from clip_extractor import extract_chapters_as_clips


def create_session_dir(base_dir: Path, video_id: str) -> Path:
    """セッションディレクトリ作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = base_dir / f"{timestamp}_{video_id}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def select_chapters_interactive(chapters: list) -> list:
    """インタラクティブにチャプターを選択（Claude Code内で使用）

    Note: このスキルはClaude Code内で呼ばれるため、
    ユーザーの指示はClaudeが解釈して適切なチャプターを返す。
    スタンドアロン実行時はauto-selectを使用。
    """
    return chapters  # Claude Code内では全チャプター返して選択はClaude側で行う


def filter_chapters(chapters: list, criteria: str) -> list:
    """フィルタ条件でチャプターを選択

    criteria examples:
        "all" - 全チャプター
        "score>0.8" - スコア0.8以上
        "1,3,5" - 番号指定
        "1-3" - 範囲指定
    """
    criteria = criteria.strip()

    if criteria.lower() == "all":
        return chapters

    # スコアフィルタ: "score>0.8" or "score>=0.7"
    if criteria.startswith("score"):
        # >= を先にチェック（> は >= にもマッチするため）
        if ">=" in criteria:
            op = ">="
        elif ">" in criteria:
            op = ">"
        else:
            print(f"  警告: 認識できないスコア演算子 '{criteria}' → 全チャプター返却")
            return chapters
        try:
            threshold = float(criteria.split(op, 1)[1])
        except (ValueError, IndexError):
            print(f"  警告: スコアフィルタの解析失敗 '{criteria}' → 全チャプター返却")
            return chapters
        if op == ">":
            return [ch for ch in chapters if ch.get("highlight_score", 0) > threshold]
        return [ch for ch in chapters if ch.get("highlight_score", 0) >= threshold]

    # 範囲指定: "1-3"
    if "-" in criteria and "," not in criteria:
        try:
            start, end = criteria.split("-")
            ids = list(range(int(start), int(end) + 1))
        except ValueError:
            print(f"  警告: 範囲フィルタの解析失敗 '{criteria}' → 全チャプター返却")
            return chapters
        return [ch for ch in chapters if ch["id"] in ids]

    # 番号指定: "1,3,5"
    if "," in criteria or criteria.isdigit():
        ids = [int(x.strip()) for x in criteria.split(",")]
        return [ch for ch in chapters if ch["id"] in ids]

    # マッチしなければ全て
    print(f"  警告: 認識できないフィルタ条件 '{criteria}' → 全チャプターを選択")
    return chapters


def run_clipper(
    url: str = None,
    file_path: str = None,
    output_base: str = "output/clips",
    resolution: int = 1080,
    target_lang: str = "ja",
    burn_subtitles: bool = False,
    auto_select: str = None,
    chapters_only: bool = False,
) -> dict:
    """メインパイプライン実行"""
    output_base = Path(output_base).resolve()

    # === Step 1: 動画取得 ===
    print("=" * 60)
    print("Step 1: 動画取得")
    print("=" * 60)

    if url:
        # URL からメタ情報取得
        metadata = get_video_info(url)
        video_id = metadata["id"]
        print(f"  タイトル: {metadata['title']}")
        print(f"  チャンネル: {metadata['channel']}")
        print(f"  長さ: {metadata['duration']}秒")
        print(f"  プラットフォーム: {metadata['platform']}")

        # セッションディレクトリ作成
        session_dir = create_session_dir(output_base, video_id)

        # 動画ダウンロード
        print(f"\n  動画をダウンロード中（{resolution}p）...")
        video_path = download_video(url, session_dir, resolution)
        print(f"  完了: {video_path}")

    elif file_path:
        video_path = Path(file_path).resolve()
        if not video_path.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {video_path}")
        video_id = video_path.stem
        metadata = {
            "id": video_id,
            "title": video_path.stem,
            "channel": "local",
            "duration": 0,
            "url": str(video_path),
            "platform": "local",
        }
        session_dir = create_session_dir(output_base, video_id)
    else:
        raise ValueError("--url または --file を指定してください")

    # メタデータ保存
    metadata_path = session_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    # === Step 2: 字幕取得 ===
    print("\n" + "=" * 60)
    print("Step 2: 字幕取得")
    print("=" * 60)

    subtitles_dir = session_dir / "subtitles"
    original_srt = None
    source_lang = "unknown"

    if url:
        # URL動画: yt-dlpで字幕ダウンロード
        subs = download_subtitles(url, subtitles_dir)
        if subs:
            # 優先順位: en > ja > 最初に見つかったもの
            for lang in ["en", "ja"] + list(subs.keys()):
                if lang in subs:
                    original_srt = subs[lang]
                    source_lang = lang
                    break
            print(f"  字幕取得: {source_lang} ({original_srt.name})")
        else:
            print("  字幕なし → Gemini音声認識で文字起こし")

    if original_srt is None:
        # 字幕なし or ローカルファイル → Gemini文字起こし
        print("  Gemini音声認識を実行中...")
        result = transcribe_video(video_path, subtitles_dir)
        original_srt = result["srt_path"]
        source_lang = result["detected_lang"]
        print(f"  文字起こし完了: {result['segment_count']}セグメント, 言語: {source_lang}")

    # === Step 3: AIチャプター分析 ===
    print("\n" + "=" * 60)
    print("Step 3: AIチャプター分析")
    print("=" * 60)

    segments = load_srt(original_srt)
    print(f"  字幕セグメント数: {len(segments)}")
    print("  Gemini Flashでチャプター分析中...")

    chapters = analyze_chapters(
        segments,
        video_title=metadata.get("title", ""),
        video_duration=metadata.get("duration", 0),
    )

    # チャプター保存
    chapters_path = session_dir / "chapters.json"
    chapters_path.write_text(
        json.dumps(chapters, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n  {len(chapters)}チャプター検出:\n")
    print(display_chapters(chapters))

    if chapters_only:
        print("\n  --chapters-only: チャプター分析のみで終了")
        return {
            "session_dir": str(session_dir),
            "metadata": metadata,
            "chapters": chapters,
            "chapters_path": str(chapters_path),
        }

    # === Step 4: チャプター選択 ===
    print("\n" + "=" * 60)
    print("Step 4: チャプター選択")
    print("=" * 60)

    if auto_select:
        selected = filter_chapters(chapters, auto_select)
        print(f"  自動選択 ({auto_select}): {len(selected)}チャプター")
    else:
        selected = chapters
        print(f"  全{len(selected)}チャプターを選択（Claude Codeでフィルタ可能）")

    if not selected:
        print("  選択されたチャプターがありません")
        return {
            "session_dir": str(session_dir),
            "metadata": metadata,
            "chapters": chapters,
            "selected": [],
        }

    # === Step 5: 字幕翻訳 ===
    print("\n" + "=" * 60)
    print("Step 5: 字幕翻訳")
    print("=" * 60)

    translated_srt = subtitles_dir / f"translated_{target_lang}.srt"

    if source_lang == target_lang:
        print(f"  ソース言語と翻訳先が同じ（{target_lang}） → 翻訳スキップ")
        translated_srt = None  # 同一言語時はNoneにして字幕重複を防止
    else:
        print(f"  {source_lang} → {target_lang} 翻訳中...")
        translate_srt(original_srt, translated_srt, source_lang, target_lang)
        print(f"  翻訳完了: {translated_srt}")

    # バイリンガルSRT
    bilingual_srt = subtitles_dir / "bilingual.srt"
    if translated_srt is not None and source_lang != target_lang and translated_srt.exists():
        create_bilingual_srt(original_srt, translated_srt, bilingual_srt)

    # === Step 6: クリップ抽出 ===
    print("\n" + "=" * 60)
    print("Step 6: クリップ抽出")
    print("=" * 60)

    clips_dir = session_dir / "clips"
    clips = extract_chapters_as_clips(
        video_path=video_path,
        chapters=selected,
        original_srt=original_srt,
        translated_srt=translated_srt if translated_srt is not None else original_srt,
        output_dir=clips_dir,
        burn_subs=burn_subtitles,
        target_lang=target_lang,
        skip_bilingual=(source_lang == target_lang),
    )

    # === Remotion入力データ生成 ===
    remotion_input = {
        "metadata": metadata,
        "chapters": selected,
        "clips": clips,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "session_dir": str(session_dir),
    }
    remotion_path = session_dir / "remotion_input.json"
    remotion_path.write_text(
        json.dumps(remotion_input, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # === 完了 ===
    print("\n" + "=" * 60)
    print("完了!")
    print("=" * 60)
    print(f"  セッション: {session_dir}")
    print(f"  クリップ数: {len(clips)}")
    print(f"  チャプター: {chapters_path}")
    print(f"  Remotion入力: {remotion_path}")

    return {
        "session_dir": str(session_dir),
        "metadata": metadata,
        "chapters": chapters,
        "selected_chapters": selected,
        "clips": clips,
        "remotion_input_path": str(remotion_path),
        "original_srt": str(original_srt),
        "translated_srt": str(translated_srt) if translated_srt is not None else None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Clipper - 動画ハイライト抽出 & クリップ生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  # YouTube動画からクリップ抽出
  python clipper.py --url "https://youtube.com/watch?v=xxxxx"

  # ローカル動画
  python clipper.py --file /path/to/video.mp4

  # スコア0.8以上を自動選択
  python clipper.py --url "..." --auto-select "score>0.8"

  # チャプター分析のみ
  python clipper.py --url "..." --chapters-only

  # 全クリップ + 字幕焼き込み
  python clipper.py --url "..." --auto-select all --burn-subtitles
        """,
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--url", help="動画URL（YouTube/Vimeo/X等）")
    source.add_argument("--file", help="ローカル動画ファイル")

    parser.add_argument("-o", "--output", default="output/clips", help="出力ベースディレクトリ")
    parser.add_argument("-r", "--resolution", type=int, default=1080, help="動画品質 (720/1080)")
    parser.add_argument("--target-lang", default="ja", help="翻訳先言語 (default: ja)")
    parser.add_argument("--burn-subtitles", action="store_true", help="字幕焼き込み")
    parser.add_argument("--auto-select", default=None, help='自動選択 ("all", "score>0.8", "1,3,5")')
    parser.add_argument("--chapters-only", action="store_true", help="チャプター分析のみ")

    args = parser.parse_args()

    result = run_clipper(
        url=args.url,
        file_path=args.file,
        output_base=args.output,
        resolution=args.resolution,
        target_lang=args.target_lang,
        burn_subtitles=args.burn_subtitles,
        auto_select=args.auto_select,
        chapters_only=args.chapters_only,
    )

    # 結果をJSON出力
    print("\n--- Result JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
