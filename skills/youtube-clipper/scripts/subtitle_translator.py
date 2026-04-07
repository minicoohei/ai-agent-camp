"""
subtitle_translator.py - バッチ字幕翻訳

多言語の字幕をバッチ20件ずつGemini Flashで日本語に翻訳。
バイリンガルSRT（原文+翻訳）も生成。
"""

import json
import os
import sys
from pathlib import Path

import pysrt

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from bootcamp_utils import get_client, get_flash_model

BATCH_SIZE = 20


def translate_batch(
    texts: list,
    source_lang: str,
    target_lang: str = "ja",
) -> list:
    """テキストのバッチをGemini Flashで翻訳"""
    client = get_client()
    if not client:
        raise RuntimeError("GEMINI_API_KEY が設定されていません")

    # ソースと翻訳先が同じ場合はそのまま返す
    if source_lang == target_lang:
        return texts

    numbered = "\n".join(f"[{i}] {t}" for i, t in enumerate(texts))

    prompt = f"""以下のテキストを{target_lang}に翻訳してください。
ソース言語: {source_lang}

ルール:
1. 各テキストの番号を維持すること
2. 自然な{target_lang}にすること（直訳ではなく意訳推奨）
3. 専門用語はそのまま残すか、適切な訳語を使うこと
4. JSON配列で返すこと（番号順に翻訳テキストのみ）

入力:
{numbered}

出力形式（JSON配列のみ、他のテキストは不要）:
["翻訳1", "翻訳2", ...]"""

    model = get_flash_model()
    try:
        response = client.models.generate_content(model=model, contents=prompt)
    except Exception as e:
        raise RuntimeError(f"Gemini API呼び出し失敗: {e}") from e

    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    try:
        translated = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Gemini応答のJSON解析失敗: {e}\n応答テキスト: {text[:500]}"
        ) from e

    # 数が合わない場合のフォールバック
    if len(translated) != len(texts):
        # 足りない分は原文で埋める
        while len(translated) < len(texts):
            translated.append(texts[len(translated)])
        translated = translated[: len(texts)]

    return translated


def translate_srt(
    srt_path: Path,
    output_path: Path,
    source_lang: str = "en",
    target_lang: str = "ja",
) -> Path:
    """SRTファイル全体を翻訳"""
    subs = pysrt.open(str(srt_path), encoding="utf-8")
    texts = [sub.text.replace("\n", " ") for sub in subs]

    translated_texts = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        translated_batch = translate_batch(batch, source_lang, target_lang)
        translated_texts.extend(translated_batch)
        print(f"  翻訳中: {min(i + BATCH_SIZE, len(texts))}/{len(texts)}")

    # 翻訳済みSRT作成
    translated_subs = subs.__class__()
    for i, sub in enumerate(subs):
        new_sub = pysrt.SubRipItem(
            index=sub.index,
            start=sub.start,
            end=sub.end,
            text=translated_texts[i] if i < len(translated_texts) else sub.text,
        )
        translated_subs.append(new_sub)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    translated_subs.save(str(output_path), encoding="utf-8")
    return output_path


def create_bilingual_srt(
    original_path: Path,
    translated_path: Path,
    output_path: Path,
) -> Path:
    """原文+翻訳のバイリンガルSRTを作成"""
    orig = pysrt.open(str(original_path), encoding="utf-8")
    trans = pysrt.open(str(translated_path), encoding="utf-8")

    if len(orig) != len(trans):
        print(f"  警告: 原文({len(orig)}件)と翻訳({len(trans)}件)の字幕数が一致しません。短い方に合わせます。")

    bilingual = pysrt.SubRipFile()
    for i, (o, t) in enumerate(zip(orig, trans)):
        text = f"{o.text}\n{t.text}"
        item = pysrt.SubRipItem(
            index=i + 1,
            start=o.start,
            end=o.end,
            text=text,
        )
        bilingual.append(item)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    bilingual.save(str(output_path), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="字幕翻訳")
    parser.add_argument("srt", help="SRTファイル")
    parser.add_argument("-o", "--output", required=True, help="翻訳SRT出力パス")
    parser.add_argument("--source-lang", default="en", help="ソース言語")
    parser.add_argument("--target-lang", default="ja", help="翻訳先言語")
    parser.add_argument("--bilingual", default=None, help="バイリンガルSRT出力パス")
    args = parser.parse_args()

    translated = translate_srt(
        Path(args.srt), Path(args.output), args.source_lang, args.target_lang
    )
    print(f"翻訳SRT: {translated}")

    if args.bilingual:
        bilingual = create_bilingual_srt(
            Path(args.srt), translated, Path(args.bilingual)
        )
        print(f"バイリンガルSRT: {bilingual}")
