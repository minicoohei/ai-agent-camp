"""
ナレーション品質管理モジュール

narration-qa スキルの Step 0 + Step 3 を Python モジュール化。
TTS 入力テキストの前処理、生成後の Gemini 書き起こし検証、
自動リトライを提供する。
"""

import json
import os
import re
import time
from pathlib import Path
from typing import Optional


# ============================================================
# Step 0: TTS 入力テキストの前処理ルール
# ============================================================

# 既知の誤読漢字 → ひらがな/平易表現への変換テーブル
KANJI_FIXES = {
    "返信": "へんしん",
    "受信": "届いた",
    "議事録": "ぎじろく",
    "各": "それぞれの",
    "即座に": "すぐに",
    "承認": "しょうにん",
    "税理士": "ぜいりし",
    "成果": "せいか",
    "閉める": "しめる",
}

# 英語 → カタカナ変換テーブル（定着した外来語）
ENGLISH_TO_KATAKANA = {
    "GitHub": "ギットハブ",
    "Slack": "スラック",
    "Gmail": "ジーメール",
    "Google Drive": "グーグルドライブ",
    "Claude Code": "クロードコード",
    "LINE": "ライン",
    "TODO": "タスク",
    "workflow": "ワークフロー",
    "AI": "えーあい",
    "PMO": "ぴーえむおー",
    "PPTX": "パワーポイント",
    "GitHub Actions": "自動ワークフロー",
    "MCP": "エムシーピー",
    "API": "エーピーアイ",
    "Cursor": "カーソル",
    "Codex": "コーデックス",
    "Remotion": "リモーション",
    "FFmpeg": "エフエフエムペグ",
}

# 数字 → ひらがな変換パターン
_NUMBER_READINGS = {
    "0": "ゼロ", "1": "いち", "2": "に", "3": "さん", "4": "よん",
    "5": "ご", "6": "ろく", "7": "なな", "8": "はち", "9": "きゅう",
}

_COUNTER_READINGS = {
    "つ": {1: "ひとつ", 2: "ふたつ", 3: "みっつ", 4: "よっつ", 5: "いつつ",
           6: "むっつ", 7: "ななつ", 8: "やっつ", 9: "ここのつ"},
}


def _expand_number_yen(match: re.Match) -> str:
    """金額パターン (e.g. 12,800円) をひらがなに展開"""
    num_str = match.group(1).replace(",", "")
    num = int(num_str)
    parts = []
    if num >= 10000:
        man = num // 10000
        if man == 1:
            parts.append("いちまん")
        else:
            parts.append(f"{_NUMBER_READINGS.get(str(man), str(man))}まん")
        num %= 10000
    if num >= 1000:
        sen = num // 1000
        if sen == 1:
            parts.append("せん")
        elif sen == 3:
            parts.append("さんぜん")
        elif sen == 8:
            parts.append("はっせん")
        else:
            parts.append(f"{_NUMBER_READINGS.get(str(sen), str(sen))}せん")
        num %= 1000
    if num >= 100:
        hyaku = num // 100
        if hyaku == 1:
            parts.append("ひゃく")
        elif hyaku == 3:
            parts.append("さんびゃく")
        elif hyaku == 6:
            parts.append("ろっぴゃく")
        elif hyaku == 8:
            parts.append("はっぴゃく")
        else:
            parts.append(f"{_NUMBER_READINGS.get(str(hyaku), str(hyaku))}ひゃく")
        num %= 100
    if num >= 10:
        juu = num // 10
        if juu == 1:
            parts.append("じゅう")
        else:
            parts.append(f"{_NUMBER_READINGS.get(str(juu), str(juu))}じゅう")
        num %= 10
    if num > 0:
        parts.append(_NUMBER_READINGS.get(str(num), str(num)))
    parts.append("えん")
    return "".join(parts)


def _expand_number_percent(match: re.Match) -> str:
    """パーセントパターン (e.g. 95%) をひらがなに展開"""
    num_str = match.group(1).replace(",", "")
    num = int(num_str)
    parts = []
    if num >= 100:
        parts.append("ひゃく")
        num %= 100
    if num >= 10:
        juu = num // 10
        if juu == 1:
            parts.append("じゅう")
        else:
            parts.append(f"{_NUMBER_READINGS.get(str(juu), str(juu))}じゅう")
        num %= 10
    if num > 0:
        parts.append(_NUMBER_READINGS.get(str(num), str(num)))
    parts.append("パーセント")
    return "".join(parts)


def preprocess_narration_text(text: str) -> str:
    """TTS 入力テキストを前処理する (narration-qa Step 0)

    1. 英語 → カタカナ変換
    2. 既知の誤読漢字 → ひらがな/平易表現
    3. 数字展開 (金額・パーセント)

    ※全文ひらがな化はしない（TTS モデルが壊れるため）
    """
    # 英語 → カタカナ（長い語句から先に置換）
    for eng, kata in sorted(ENGLISH_TO_KATAKANA.items(), key=lambda x: -len(x[0])):
        text = text.replace(eng, kata)

    # 既知の誤読漢字 → ひらがな/平易表現
    for kanji, reading in KANJI_FIXES.items():
        text = text.replace(kanji, reading)

    # 金額展開: 12,800円 → ひらがな
    text = re.sub(r"([\d,]+)円", _expand_number_yen, text)

    # パーセント展開: 95% → ひらがな
    text = re.sub(r"([\d,]+)%", _expand_number_percent, text)

    # N つの → ひらがな (1-9)
    def _expand_tsu(m: re.Match) -> str:
        n = int(m.group(1))
        return _COUNTER_READINGS["つ"].get(n, f"{n}つ")
    text = re.sub(r"(\d)つ", _expand_tsu, text)

    return text


# ============================================================
# Step 3: Gemini 書き起こし検証
# ============================================================

def verify_narration(
    audio_path: str,
    original_text: str,
    model: str = "gemini-2.5-flash",
) -> dict:
    """TTS 生成音声を Gemini で書き起こし、原稿と照合する

    Args:
        audio_path: 生成された音声ファイルのパス
        original_text: 元の原稿テキスト
        model: 使用する Gemini モデル

    Returns:
        {status: "PASS"|"CRITICAL"|"MAJOR"|"MINOR",
         transcript: str, original: str, issues: list}
    """
    try:
        from google import genai
    except ImportError:
        print("  警告: google-genai パッケージ未インストール。検証をスキップします。")
        return {"status": "SKIP", "transcript": "", "original": original_text, "issues": []}

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("  警告: GEMINI_API_KEY 未設定。検証をスキップします。")
        return {"status": "SKIP", "transcript": "", "original": original_text, "issues": []}

    client = genai.Client(api_key=api_key)

    try:
        audio_file = client.files.upload(file=audio_path)
        response = client.models.generate_content(
            model=model,
            contents=[
                "この日本語音声を正確に書き起こしてください。句読点も含めて。テキストのみ返してください。",
                audio_file,
            ],
        )
        transcript = response.text.strip()
    except Exception as e:
        print(f"  Gemini 書き起こし失敗: {e}")
        return {"status": "ERROR", "transcript": "", "original": original_text, "issues": [str(e)]}

    # 照合
    issues = []
    status = "PASS"

    # 簡易照合: 意味の大きな乖離を検出
    orig_clean = re.sub(r"[\s、。,.\n]", "", original_text)
    trans_clean = re.sub(r"[\s、。,.\n]", "", transcript)

    # 文字レベルの一致率
    common = sum(1 for a, b in zip(orig_clean, trans_clean) if a == b)
    max_len = max(len(orig_clean), len(trans_clean), 1)
    similarity = common / max_len

    if similarity < 0.5:
        status = "CRITICAL"
        issues.append(f"一致率 {similarity:.0%} — 意味が大きく異なる可能性")
    elif similarity < 0.7:
        status = "MAJOR"
        issues.append(f"一致率 {similarity:.0%} — 一部の語句が異なる")
    elif similarity < 0.9:
        status = "MINOR"
        issues.append(f"一致率 {similarity:.0%} — 表記の違い（Gemini STT の限界の可能性）")

    result = {
        "status": status,
        "transcript": transcript,
        "original": original_text,
        "similarity": round(similarity, 3),
        "issues": issues,
    }

    icon = {"PASS": "OK", "MINOR": "MINOR", "MAJOR": "NG", "CRITICAL": "NG"}.get(status, "?")
    print(f"  narration-qa [{icon}]: similarity={similarity:.0%} | {original_text[:30]}...")

    return result


# ============================================================
# 統合: 生成 → 検証 → リトライ
# ============================================================

def qa_and_retry(
    text: str,
    output_path: str,
    voice: str = "default",
    max_retries: int = 3,
    stability: float = 0.70,
    similarity_boost: float = 0.80,
) -> str:
    """ナレーション生成 → 検証 → NG なら修正 → 再生成のループ

    narration-qa スキルの全フローを1関数で実行する。

    Args:
        text: 原稿テキスト
        output_path: 最終音声ファイルの出力先
        voice: TTS ボイスプリセット
        max_retries: 最大リトライ回数
        stability: ElevenLabs stability 設定
        similarity_boost: ElevenLabs similarity_boost 設定

    Returns:
        最終音声ファイルのパス
    """
    from ugc.tts import generate_speech

    # Step 0: テキスト前処理
    processed_text = preprocess_narration_text(text)
    if processed_text != text:
        print(f"  narration-qa: テキスト前処理適用")

    current_text = processed_text

    for attempt in range(max_retries):
        # Step 2: 音声生成
        audio_path = generate_speech(
            text=current_text,
            output_path=output_path,
            voice=voice,
            stability=stability,
            similarity_boost=similarity_boost,
        )

        # Step 3: Gemini 検証
        qa_result = verify_narration(audio_path, current_text)

        if qa_result["status"] in ("PASS", "MINOR", "SKIP"):
            return audio_path

        if attempt < max_retries - 1:
            print(f"  narration-qa: リトライ {attempt + 2}/{max_retries} — {qa_result['status']}")
            # CRITICAL/MAJOR: さらにテキストを平易化
            for issue_text in qa_result.get("issues", []):
                print(f"    {issue_text}")
            # 追加のひらがな化を試みる（漢字を含む部分をさらに変換）
            current_text = _further_simplify(current_text)
            time.sleep(1)

    print(f"  narration-qa: {max_retries}回リトライ後も改善なし。最後の生成結果を使用。")
    return audio_path


def _further_simplify(text: str) -> str:
    """リトライ時に追加のテキスト簡略化を試みる"""
    # 追加の誤読しやすい漢字をひらがな化
    extra_fixes = {
        "確認": "かくにん",
        "作成": "さくせい",
        "自動": "じどう",
        "削減": "さくげん",
        "分析": "ぶんせき",
        "実現": "じつげん",
        "処理": "しょり",
        "管理": "かんり",
        "完了": "かんりょう",
    }
    for kanji, reading in extra_fixes.items():
        text = text.replace(kanji, reading)
    return text
