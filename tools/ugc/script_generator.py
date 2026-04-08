"""
UGCスクリプト生成モジュール

Gemini Flashを使用してプラットフォーム別のUGCスクリプトを生成する。
"""

import json
import os
import sys
from pathlib import Path
from typing import Literal, Optional

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))
from runtime_env import load_runtime_env
from bootcamp_utils import get_client, get_flash_model

load_runtime_env(Path(__file__).resolve().parents[2])


# プロンプトテンプレートを読み込み
PROMPTS_PATH = Path(__file__).parent / "prompts.json"


def load_prompts() -> dict:
    """プロンプトテンプレートを読み込む"""
    if PROMPTS_PATH.exists():
        with open(PROMPTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def generate_ugc_script(
    topic: str,
    platform: Literal["tiktok", "youtube_shorts", "instagram"] = "tiktok",
    duration: Optional[int] = None,
    language: str = "ja",
    custom_prompt: Optional[str] = None,
) -> str:
    """
    UGCスクリプトを生成する
    
    Args:
        topic: 動画のトピック/テーマ
        platform: プラットフォーム (tiktok, youtube_shorts, instagram)
        duration: 動画の長さ（秒）、Noneの場合はプラットフォームのデフォルト
        language: 言語コード
        custom_prompt: カスタムプロンプト（指定時はテンプレートを上書き）
        
    Returns:
        生成されたスクリプト
    """
    client = get_client()
    if not client:
        raise EnvironmentError("GEMINI_API_KEY が設定されていません")
    
    prompts = load_prompts()
    script_templates = prompts.get("script_templates", {})
    
    # プラットフォームのテンプレートを取得
    template = script_templates.get(platform, script_templates.get("tiktok", {}))
    
    if duration is None:
        duration = template.get("duration", 30)
    
    # プロンプトを構築
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt_template = template.get("prompt", "")
        prompt = prompt_template.format(
            topic=topic,
            duration=duration,
            language=language,
        )
    
    print(f"🎬 スクリプト生成中... (platform={platform}, duration={duration}s)")
    
    try:
        response = client.models.generate_content(
            model=get_flash_model(),
            contents=[prompt],
        )
        
        script = response.text.strip()
        
        # 余分な装飾を除去
        script = _clean_script(script)
        
        print(f"✅ スクリプト生成完了 ({len(script)}文字)")
        return script
        
    except Exception as e:
        print(f"❌ スクリプト生成エラー: {e}")
        raise


def _clean_script(script: str) -> str:
    """スクリプトから余分な装飾を除去"""
    # Markdownコードブロックを除去
    if script.startswith("```"):
        lines = script.split("\n")
        # 最初と最後の```を除去
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        script = "\n".join(lines)
    
    # 引用符で囲まれている場合は除去
    script = script.strip('"\'')
    
    return script.strip()


def estimate_duration(script: str, wpm: int = 150) -> float:
    """
    スクリプトの読み上げ時間を推定する
    
    Args:
        script: スクリプトテキスト
        wpm: 1分あたりの単語数（日本語の場合は文字数/3で近似）
        
    Returns:
        推定秒数
    """
    # 日本語の場合は文字数で計算（約3文字/秒）
    char_count = len(script)
    # 英語の場合は単語数で計算
    word_count = len(script.split())
    
    # 日本語かどうかを判定（ひらがな・カタカナ・漢字が含まれるか）
    import re
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', script):
        # 日本語: 約3文字/秒
        return char_count / 3.0
    else:
        # 英語: 約2.5単語/秒
        return word_count / 2.5


if __name__ == "__main__":
    # テスト
    import argparse
    
    parser = argparse.ArgumentParser(description="UGCスクリプト生成")
    parser.add_argument("topic", help="動画のトピック")
    parser.add_argument("--platform", "-p", default="tiktok", 
                       choices=["tiktok", "youtube_shorts", "instagram"])
    parser.add_argument("--duration", "-d", type=int, default=None)
    parser.add_argument("--language", "-l", default="ja")
    
    args = parser.parse_args()
    
    script = generate_ugc_script(
        topic=args.topic,
        platform=args.platform,
        duration=args.duration,
        language=args.language,
    )
    
    print("\n" + "=" * 50)
    print("生成されたスクリプト:")
    print("=" * 50)
    print(script)
    print("=" * 50)
    print(f"推定読み上げ時間: {estimate_duration(script):.1f}秒")
