#!/usr/bin/env python3
"""
Style Analyzer - 文体分析・プロファイル生成ツール

ユーザーが書いた複数の文章ファイルを読み込み、文体の特徴を定量的に抽出して
スタイルプロファイル（YAML形式）を生成する。
"""

import argparse
import math
import re
import statistics
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT_DIR / "output" / "style_profile.yaml"

# =============================================================================
# 定数
# =============================================================================

# 接続詞リスト（カテゴリ別）
CONJUNCTIONS: Dict[str, List[str]] = {
    "順接": ["だから", "したがって", "そのため", "それで", "ゆえに", "よって", "その結果"],
    "逆接": [
        "しかし", "だが", "ところが", "けれども", "けれど", "にもかかわらず",
        "一方で", "一方", "しかしながら", "とはいえ", "それでも", "ただし",
        "もっとも",
    ],
    "並列・累加": [
        "また", "さらに", "そして", "加えて", "それに", "そのうえ",
        "しかも", "おまけに", "なおかつ", "および", "ならびに",
    ],
    "説明・補足": [
        "つまり", "すなわち", "要するに", "なぜなら", "というのも",
        "なぜかというと", "言い換えると", "換言すれば",
    ],
    "転換": ["さて", "ところで", "では", "それでは", "ちなみに", "話は変わるが", "それはさておき"],
    "対比": ["むしろ", "逆に", "反対に", "それに対して", "他方", "かえって"],
    "例示": ["たとえば", "具体的には", "いわば", "例を挙げると"],
}

ALL_CONJUNCTIONS: List[str] = []
for words in CONJUNCTIONS.values():
    ALL_CONJUNCTIONS.extend(words)
# 長い接続詞を先にマッチさせるためソート
ALL_CONJUNCTIONS.sort(key=len, reverse=True)

# 口語的表現パターン
COLLOQUIAL_PATTERNS: List[str] = [
    r"ですよね",
    r"ですね",
    r"ですよ",
    r"ますよね",
    r"ますね",
    r"ますよ",
    r"じゃない",
    r"だよね",
    r"だよ",
    r"だね",
    r"かな[。？]",
    r"よね[。？]",
    r"んです",
    r"のです",
    r"ちゃう",
    r"ちゃった",
    r"っぽい",
    r"みたいな",
    r"とか[、。]",
    r"って[、。]",
    r"なんか",
    r"やっぱり",
    r"やっぱ",
    r"ちょっと",
    r"すごく",
    r"めっちゃ",
    r"けっこう",
    r"ぶっちゃけ",
]

# 文語的表現パターン
FORMAL_PATTERNS: List[str] = [
    r"である",
    r"において",
    r"における",
    r"に関して",
    r"に対して",
    r"によって",
    r"に基づき",
    r"に基づいて",
    r"を踏まえ",
    r"を鑑み",
    r"されたい",
    r"すべき",
    r"であろう",
    r"ものとする",
    r"とされる",
    r"と考えられる",
    r"と思われる",
    r"の観点から",
    r"前述の",
    r"後述の",
    r"上記の",
    r"下記の",
    r"当該",
    r"かかる",
    r"もって",
]

# 修飾語（副詞）リスト
COMMON_ADVERBS: List[str] = [
    "非常に", "特に", "実際に", "本当に", "とても", "かなり", "極めて",
    "やや", "少し", "多少", "若干", "大いに", "著しく", "圧倒的に",
    "明らかに", "確実に", "おそらく", "恐らく", "きっと", "たぶん",
    "必ず", "常に", "頻繁に", "しばしば", "時々", "たまに", "ほとんど",
    "まったく", "全く", "決して", "一切", "すでに", "既に", "もはや",
    "ようやく", "ついに", "結局", "最終的に", "基本的に", "一般的に",
    "具体的に", "積極的に", "徐々に", "急速に", "直接", "間接的に",
]


# =============================================================================
# テキスト前処理
# =============================================================================


def strip_markdown(text: str) -> str:
    """Markdown記法を除去してプレーンテキストに変換する。"""
    # YAML frontmatter を除去
    text = re.sub(r"^---\s*\n.*?\n---\s*\n", "", text, flags=re.DOTALL)
    # コードブロックを除去
    text = re.sub(r"```[\s\S]*?```", "", text)
    # インラインコードを除去
    text = re.sub(r"`[^`]+`", "", text)
    # 見出し記号を除去
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # リンクをテキスト部分だけ残す
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # 画像を除去
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", "", text)
    # 強調記号を除去
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", text)
    # リスト記号を除去
    text = re.sub(r"^[\s]*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)
    # 引用記号を除去
    text = re.sub(r"^>\s*", "", text, flags=re.MULTILINE)
    # 水平線を除去
    text = re.sub(r"^[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # HTMLタグを除去
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def split_sentences(text: str) -> List[str]:
    """テキストを文単位に分割する。"""
    # 。！？で文を分割（ただし括弧内は無視しない簡易版）
    # 句点・感嘆符・疑問符を文の区切りとして使用
    raw = re.split(r"(?<=[。！？!?])", text)
    sentences = []
    for s in raw:
        s = s.strip()
        # 空文や極端に短い断片は除外
        if len(s) >= 2:
            sentences.append(s)
    return sentences


def split_paragraphs(text: str) -> List[str]:
    """テキストを段落単位に分割する（空行区切り）。"""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


# =============================================================================
# 文字種分析
# =============================================================================


def classify_char(ch: str) -> str:
    """1文字をカテゴリに分類する。"""
    cp = ord(ch)
    # ひらがな
    if 0x3040 <= cp <= 0x309F:
        return "hiragana"
    # カタカナ
    if 0x30A0 <= cp <= 0x30FF:
        return "katakana"
    # 漢字（CJK統合漢字 + 拡張A）
    if (0x4E00 <= cp <= 0x9FFF) or (0x3400 <= cp <= 0x4DBF):
        return "kanji"
    # ASCII（スペース含む印字可能文字）
    if 0x0020 <= cp <= 0x007E:
        return "ascii"
    return "other"


def calc_char_ratios(text: str) -> Dict[str, float]:
    """文字種ごとの比率を計算する。空白・改行は除外。"""
    # 空白と改行を除去
    chars = [ch for ch in text if ch not in (" ", "\u3000", "\t", "\n", "\r")]
    if not chars:
        return {"kanji": 0, "hiragana": 0, "katakana": 0, "ascii": 0, "other": 0}
    counter: Counter = Counter()
    for ch in chars:
        counter[classify_char(ch)] += 1
    total = len(chars)
    return {
        "kanji": round(counter.get("kanji", 0) / total, 4),
        "hiragana": round(counter.get("hiragana", 0) / total, 4),
        "katakana": round(counter.get("katakana", 0) / total, 4),
        "ascii": round(counter.get("ascii", 0) / total, 4),
        "other": round(counter.get("other", 0) / total, 4),
    }


# =============================================================================
# 語尾パターン分析
# =============================================================================

DESU_MASU_ENDINGS = [
    r"です[。？！!?]?$",
    r"ます[。？！!?]?$",
    r"でした[。？！!?]?$",
    r"ました[。？！!?]?$",
    r"ません[。？！!?]?$",
    r"でしょう[。？！!?]?$",
    r"ましょう[。？！!?]?$",
    r"ください[。？！!?]?$",
]

DA_DEARU_ENDINGS = [
    r"である[。？！!?]?$",
    r"であった[。？！!?]?$",
    r"であろう[。？！!?]?$",
    r"ではない[。？！!?]?$",
    r"ではなかった[。？！!?]?$",
    r"(?<!し)(?<!ま)(?<!で)(?<!だっ)(?<!てい)た[。]$",  # 「〜た。」（だ/である系の過去）
    r"だ[。]$",
    r"だった[。？！!?]?$",
]


def classify_sentence_ending(sentence: str) -> str:
    """文の語尾パターンを分類する。"""
    s = sentence.strip()
    for pat in DESU_MASU_ENDINGS:
        if re.search(pat, s):
            return "desu_masu"
    for pat in DA_DEARU_ENDINGS:
        if re.search(pat, s):
            return "da_dearu"
    return "other"


def analyze_endings(sentences: List[str]) -> Dict[str, Any]:
    """語尾パターンの統計を計算する。"""
    if not sentences:
        return {
            "desu_masu": 0.0,
            "da_dearu": 0.0,
            "other": 0.0,
            "dominant_style": "unknown",
        }
    counter: Counter = Counter()
    for s in sentences:
        counter[classify_sentence_ending(s)] += 1
    total = len(sentences)
    dm = counter.get("desu_masu", 0)
    dd = counter.get("da_dearu", 0)
    ot = counter.get("other", 0)
    result = {
        "desu_masu": round(dm / total, 4),
        "da_dearu": round(dd / total, 4),
        "other": round(ot / total, 4),
    }
    if dm >= dd and dm >= ot:
        result["dominant_style"] = "desu_masu"
    elif dd >= dm and dd >= ot:
        result["dominant_style"] = "da_dearu"
    else:
        result["dominant_style"] = "mixed"
    return result


# =============================================================================
# 接続詞分析
# =============================================================================


def analyze_conjunctions(sentences: List[str]) -> Dict[str, Any]:
    """接続詞の使用頻度を分析する。"""
    counter: Counter = Counter()
    for s in sentences:
        s_stripped = s.strip()
        for conj in ALL_CONJUNCTIONS:
            # 文頭に接続詞が来るパターン（読点やスペースが続く場合）
            if re.match(rf"^{re.escape(conj)}[、,\s]", s_stripped):
                counter[conj] += 1
                break  # 1文につき1つだけカウント
    total_count = sum(counter.values())
    top_items = counter.most_common(5)
    top_5 = [{"word": word, "count": count} for word, count in top_items]
    return {
        "total_count": total_count,
        "per_sentence": round(total_count / max(len(sentences), 1), 4),
        "top_5": top_5,
    }


# =============================================================================
# 体言止め分析
# =============================================================================

# 体言止めの特徴: 文末が名詞的な語で終わる（助詞・助動詞・動詞活用語尾がない）
# 簡易判定: 文末文字が漢字・カタカナ、または「こと」「もの」「ところ」等で終わる
TAIGEN_DOME_PATTERNS = [
    # 文末が漢字で終わる（句点の直前）
    r"[\u4e00-\u9fff]。$",
    # 文末がカタカナで終わる
    r"[\u30a0-\u30ff]。$",
    # 「こと」「もの」「ところ」「わけ」「はず」で終わる
    r"(?:こと|もの|ところ|わけ|はず|とき|ため)。$",
]


def analyze_taigen_dome(sentences: List[str]) -> Dict[str, Any]:
    """体言止めの頻度を分析する。"""
    count = 0
    for s in sentences:
        s = s.strip()
        for pat in TAIGEN_DOME_PATTERNS:
            if re.search(pat, s):
                count += 1
                break
    total = max(len(sentences), 1)
    return {
        "frequency": round(count / total, 4),
        "count": count,
    }


# =============================================================================
# 句読点分析
# =============================================================================


def analyze_punctuation(text: str) -> Dict[str, str]:
    """句読点のパターンを判定する。"""
    # 句点
    maru_count = text.count("。")
    period_count = text.count("．") + text.count(".")  # 全角・半角ピリオド
    if maru_count > 0 and period_count == 0:
        period_style = "。"
    elif period_count > 0 and maru_count == 0:
        period_style = "．"
    elif maru_count > 0 and period_count > 0:
        period_style = "。" if maru_count >= period_count else "．"
    else:
        period_style = "。"

    # 読点
    touten_count = text.count("、")
    comma_count = text.count("，") + text.count(",")  # 全角・半角カンマ
    if touten_count > 0 and comma_count == 0:
        comma_style = "、"
    elif comma_count > 0 and touten_count == 0:
        comma_style = "，"
    elif touten_count > 0 and comma_count > 0:
        comma_style = "、" if touten_count >= comma_count else "，"
    else:
        comma_style = "、"

    # パターン判定
    if period_style == "。" and comma_style == "、":
        pattern = "standard"
    elif period_style == "．" and comma_style == "，":
        pattern = "academic"
    else:
        pattern = "mixed"

    return {
        "period_style": period_style,
        "comma_style": comma_style,
        "pattern": pattern,
    }


# =============================================================================
# 修飾語分析
# =============================================================================


def analyze_modifiers(text: str, sentences: List[str]) -> Dict[str, Any]:
    """修飾語（副詞）の出現密度を分析する。"""
    counter: Counter = Counter()
    for adv in COMMON_ADVERBS:
        c = len(re.findall(re.escape(adv), text))
        if c > 0:
            counter[adv] = c
    total_adverbs = sum(counter.values())
    total_sentences = max(len(sentences), 1)
    top_items = counter.most_common(10)
    return {
        "density": round(total_adverbs / total_sentences, 4),
        "common_adverbs": [word for word, _ in top_items[:10]],
    }


# =============================================================================
# 口語/文語バランス
# =============================================================================


def analyze_colloquial_formal(text: str) -> Dict[str, Any]:
    """口語的表現と文語的表現の比率を推定する。"""
    colloquial_count = 0
    for pat in COLLOQUIAL_PATTERNS:
        colloquial_count += len(re.findall(pat, text))

    formal_count = 0
    for pat in FORMAL_PATTERNS:
        formal_count += len(re.findall(re.escape(pat), text))

    total = max(colloquial_count + formal_count, 1)
    c_ratio = round(colloquial_count / total, 4)
    f_ratio = round(formal_count / total, 4)

    if c_ratio > 0.6:
        assessment = "口語寄り"
    elif c_ratio > 0.4:
        assessment = "やや口語寄り"
    elif f_ratio > 0.6:
        assessment = "文語寄り"
    elif f_ratio > 0.4:
        assessment = "やや文語寄り"
    else:
        assessment = "バランス型"

    return {
        "colloquial_ratio": c_ratio,
        "formal_ratio": f_ratio,
        "assessment": assessment,
    }


# =============================================================================
# 文長分析
# =============================================================================


def analyze_sentence_length(sentences: List[str]) -> Dict[str, Any]:
    """文の長さの統計を計算する。"""
    if not sentences:
        return {
            "average": 0.0,
            "median": 0.0,
            "min": 0,
            "max": 0,
            "std_dev": 0.0,
        }
    lengths = [len(s.strip()) for s in sentences]
    avg = statistics.mean(lengths)
    med = statistics.median(lengths)
    std = statistics.stdev(lengths) if len(lengths) > 1 else 0.0
    return {
        "average": round(avg, 1),
        "median": round(med, 1),
        "min": min(lengths),
        "max": max(lengths),
        "std_dev": round(std, 1),
    }


# =============================================================================
# YAML出力（標準ライブラリのみ）
# =============================================================================


def to_yaml(data: Any, indent: int = 0) -> str:
    """辞書/リストを簡易YAML文字列に変換する（外部ライブラリ不要）。"""
    prefix = "  " * indent
    lines: List[str] = []

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict,)):
                lines.append(f"{prefix}{key}:")
                lines.append(to_yaml(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                if value and isinstance(value[0], dict):
                    for item in value:
                        first = True
                        for k, v in item.items():
                            if first:
                                lines.append(f"{prefix}  - {k}: {_yaml_scalar(v)}")
                                first = False
                            else:
                                lines.append(f"{prefix}    {k}: {_yaml_scalar(v)}")
                elif value:
                    for item in value:
                        lines.append(f"{prefix}  - {_yaml_scalar(item)}")
                else:
                    lines.append(f"{prefix}  []")
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(value)}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                lines.append(to_yaml(item, indent))
            else:
                lines.append(f"{prefix}- {_yaml_scalar(item)}")
    else:
        lines.append(f"{prefix}{_yaml_scalar(data)}")

    return "\n".join(lines)


def _yaml_scalar(value: Any) -> str:
    """スカラー値をYAML表現に変換する。"""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return str(value)
    if value is None:
        return "null"
    s = str(value)
    # 特殊文字を含む場合はクオート
    if any(c in s for c in (":", "#", "[", "]", "{", "}", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "\\")):
        return f'"{s}"'
    if s in ("true", "false", "null", "yes", "no", "on", "off"):
        return f'"{s}"'
    if s == "":
        return '""'
    return f'"{s}"'


# =============================================================================
# メイン分析処理
# =============================================================================


def analyze_files(file_paths: List[str]) -> Dict[str, Any]:
    """複数ファイルを読み込み、統合的な文体分析を行う。"""
    all_text = ""
    source_files = []

    for fp in file_paths:
        path = Path(fp)
        if not path.exists():
            print(f"警告: ファイルが見つかりません: {fp}", file=sys.stderr)
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # UTF-8 で読めない場合は shift_jis を試行
            try:
                content = path.read_text(encoding="shift_jis")
            except Exception as e:
                print(f"警告: ファイル読み込みエラー: {fp} ({e})", file=sys.stderr)
                continue

        plain = strip_markdown(content)
        char_count = len(plain.replace("\n", "").replace(" ", "").replace("\u3000", ""))
        source_files.append({
            "path": str(path),
            "chars": char_count,
        })
        all_text += plain + "\n\n"

    if not all_text.strip():
        print("エラー: 分析対象のテキストが空です。", file=sys.stderr)
        sys.exit(1)

    # 基本統計
    sentences = split_sentences(all_text)
    paragraphs = split_paragraphs(all_text)
    total_chars = sum(f["chars"] for f in source_files)

    # 各分析を実行
    endings = analyze_endings(sentences)
    sent_length = analyze_sentence_length(sentences)
    char_ratios = calc_char_ratios(all_text)
    conjunctions = analyze_conjunctions(sentences)
    taigen = analyze_taigen_dome(sentences)
    punctuation = analyze_punctuation(all_text)
    modifiers = analyze_modifiers(all_text, sentences)
    coll_formal = analyze_colloquial_formal(all_text)

    # 段落あたりの文数
    para_sentences = []
    for p in paragraphs:
        p_sents = split_sentences(p)
        if p_sents:
            para_sentences.append(len(p_sents))
    avg_sents_per_para = round(statistics.mean(para_sentences), 1) if para_sentences else 0.0

    # タイムスタンプ（JST）
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst).strftime("%Y-%m-%dT%H:%M:%S+09:00")

    profile = {
        "style_profile": {
            "generated_at": now,
            "source_files": source_files,
            "total_chars": total_chars,
            "total_sentences": len(sentences),
            "total_paragraphs": len(paragraphs),
            "sentence_endings": endings,
            "sentence_length": sent_length,
            "char_ratios": char_ratios,
            "conjunctions": conjunctions,
            "paragraph_structure": {
                "avg_sentences_per_paragraph": avg_sents_per_para,
            },
            "taigen_dome": taigen,
            "punctuation": punctuation,
            "modifiers": modifiers,
            "colloquial_formal_balance": coll_formal,
        }
    }
    return profile


def generate_test_profile() -> Dict[str, Any]:
    """テスト用のサンプルプロファイルを生成する。"""
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    return {
        "style_profile": {
            "generated_at": now,
            "source_files": [
                {"path": "sample_article_1.md", "chars": 2450},
                {"path": "sample_article_2.md", "chars": 3120},
            ],
            "total_chars": 5570,
            "total_sentences": 142,
            "total_paragraphs": 28,
            "sentence_endings": {
                "desu_masu": 0.72,
                "da_dearu": 0.18,
                "other": 0.10,
                "dominant_style": "desu_masu",
            },
            "sentence_length": {
                "average": 39.2,
                "median": 35.0,
                "min": 8,
                "max": 98,
                "std_dev": 15.4,
            },
            "char_ratios": {
                "kanji": 0.31,
                "hiragana": 0.48,
                "katakana": 0.08,
                "ascii": 0.06,
                "other": 0.07,
            },
            "conjunctions": {
                "total_count": 34,
                "per_sentence": 0.24,
                "top_5": [
                    {"word": "また", "count": 8},
                    {"word": "しかし", "count": 6},
                    {"word": "そして", "count": 5},
                    {"word": "さらに", "count": 4},
                    {"word": "つまり", "count": 3},
                ],
            },
            "paragraph_structure": {
                "avg_sentences_per_paragraph": 5.1,
            },
            "taigen_dome": {
                "frequency": 0.07,
                "count": 10,
            },
            "punctuation": {
                "period_style": "。",
                "comma_style": "、",
                "pattern": "standard",
            },
            "modifiers": {
                "density": 0.12,
                "common_adverbs": ["非常に", "特に", "実際に"],
            },
            "colloquial_formal_balance": {
                "colloquial_ratio": 0.25,
                "formal_ratio": 0.75,
                "assessment": "やや文語寄り",
            },
        }
    }


def print_summary(profile: Dict[str, Any]) -> None:
    """分析結果のサマリーをstdoutに出力する。"""
    sp = profile["style_profile"]

    print("\n=== Style Analyzer - 文体分析レポート ===\n")
    print(f"分析ファイル数: {len(sp['source_files'])}")
    print(f"総文字数: {sp['total_chars']:,}")
    print(f"総文数: {sp['total_sentences']}")
    print(f"総段落数: {sp['total_paragraphs']}")

    # 語尾パターン
    endings = sp["sentence_endings"]
    print("\n--- 語尾パターン ---")
    print(f"  です/ます調: {endings['desu_masu'] * 100:.1f}%")
    print(f"  だ/である調: {endings['da_dearu'] * 100:.1f}%")
    print(f"  その他: {endings['other'] * 100:.1f}%")
    dominant_label = {
        "desu_masu": "です/ます調",
        "da_dearu": "だ/である調",
        "mixed": "混合型",
        "unknown": "不明",
    }
    print(f"  -> 主要スタイル: {dominant_label.get(endings['dominant_style'], endings['dominant_style'])}")

    # 文長
    sl = sp["sentence_length"]
    print("\n--- 文長 ---")
    print(f"  平均: {sl['average']}文字  中央値: {sl['median']}文字")
    print(f"  最短: {sl['min']}文字  最長: {sl['max']}文字")

    # 文字種比率
    cr = sp["char_ratios"]
    print("\n--- 文字種比率 ---")
    print(f"  漢字: {cr['kanji'] * 100:.1f}%  ひらがな: {cr['hiragana'] * 100:.1f}%  カタカナ: {cr['katakana'] * 100:.1f}%")

    # 接続詞
    conj = sp["conjunctions"]
    print("\n--- 接続詞 TOP5 ---")
    if conj["top_5"]:
        items = [f"{item['word']}({item['count']})" for item in conj["top_5"]]
        print(f"  {' '.join(items)}")
    else:
        print("  (接続詞の使用なし)")

    # 体言止め
    td = sp["taigen_dome"]
    print("\n--- 体言止め ---")
    total_sents = max(sp["total_sentences"], 1)
    print(f"  使用率: {td['frequency'] * 100:.1f}% ({td['count']}回/{total_sents}文)")

    # 句読点
    punc = sp["punctuation"]
    print("\n--- 句読点 ---")
    print(f"  句点: {punc['period_style']}  読点: {punc['comma_style']}  パターン: {punc['pattern']}")

    # 口語/文語
    cf = sp["colloquial_formal_balance"]
    print("\n--- 口語/文語バランス ---")
    print(f"  口語: {cf['colloquial_ratio'] * 100:.1f}%  文語: {cf['formal_ratio'] * 100:.1f}%")
    print(f"  判定: {cf['assessment']}")

    print()


# =============================================================================
# CLI
# =============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Style Analyzer - ユーザーの文章から文体プロファイルを生成",
    )
    parser.add_argument(
        "--input",
        action="append",
        dest="inputs",
        metavar="FILE",
        help="分析対象のテキスト/Markdownファイル（複数指定可）",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help=f"出力先YAMLファイルパス（デフォルト: {DEFAULT_OUTPUT}）",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="テストモード: サンプルプロファイルを生成して終了",
    )
    args = parser.parse_args()

    if args.test:
        profile = generate_test_profile()
        print_summary(profile)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        yaml_str = to_yaml(profile)
        output_path.write_text(yaml_str, encoding="utf-8")
        print(f"[テストモード] サンプルプロファイル保存先: {output_path}")
        return

    if not args.inputs:
        parser.error("--input を少なくとも1つ指定してください（または --test を使用）")

    profile = analyze_files(args.inputs)
    print_summary(profile)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = to_yaml(profile)
    output_path.write_text(yaml_str, encoding="utf-8")
    print(f"プロファイル保存先: {output_path}")


if __name__ == "__main__":
    main()
