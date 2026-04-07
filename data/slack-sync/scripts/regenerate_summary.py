#!/usr/bin/env python3
"""
archiveフォルダのファイルからサマリーを再生成
"""

import os
import re
import time
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

# パス設定
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_DIR = ROOT_DIR / "data"

# .envファイルを読み込み
load_dotenv(ROOT_DIR.parent / ".env")
load_dotenv(ROOT_DIR / ".env")

# Gemini API設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY が設定されていません")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_summary(content: str, channel_name: str) -> str:
    """Gemini APIでサマリーを生成"""
    prompt = f"""以下はSlackチャンネル「{channel_name}」の会話ログです。
このチャンネルの内容を日本語で要約してください。

要約には以下を含めてください：
1. チャンネルの主な目的/トピック
2. 重要な議論や決定事項
3. 主要な参加者（もしわかれば）
4. 期間中の主なイベントや進捗

フォーマット：
# {channel_name} サマリー

## 概要
（チャンネルの目的を1-2文で）

## 主なトピック
- トピック1
- トピック2
...

## 重要な議論・決定事項
（あれば箇条書きで）

## 備考
（その他特記事項）

---
会話ログ：
{content[:15000]}
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"  ⚠️ サマリー生成エラー: {e}")
        return f"# {channel_name} サマリー\n\n⚠️ サマリー生成に失敗しました: {e}\n"


def regenerate_summaries(workspace_name: str):
    """archiveフォルダからサマリーを再生成"""
    archive_dir = DATA_DIR / "archive" / workspace_name
    summary_dir = DATA_DIR / "summary" / workspace_name
    
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*50}")
    print(f"📁 {workspace_name} のサマリーを再生成中...")
    print(f"{'='*50}")
    
    # 失敗したサマリーを持つファイルを特定
    failed_files = []
    for summary_file in summary_dir.glob("*_summary.md"):
        content = summary_file.read_text(encoding="utf-8")
        if "サマリー生成に失敗しました" in content:
            # 対応するarchiveファイルを探す
            base_name = summary_file.stem.replace("_summary", "")
            archive_file = archive_dir / f"{base_name}.md"
            if archive_file.exists():
                failed_files.append((archive_file, summary_file))
    
    print(f"📊 再生成対象: {len(failed_files)} 件")
    
    # 再生成
    success = 0
    for i, (archive_file, summary_file) in enumerate(failed_files):
        channel_name = archive_file.stem
        print(f"\n  [{i + 1}/{len(failed_files)}] {channel_name}")
        
        try:
            content = archive_file.read_text(encoding="utf-8")
            
            print(f"    🤖 サマリー生成中...")
            summary = generate_summary(content, channel_name)
            
            # 成功したか確認
            if "サマリー生成に失敗しました" not in summary:
                summary_file.write_text(summary, encoding="utf-8")
                print(f"    ✅ 成功")
                success += 1
            else:
                print(f"    ⚠️ 失敗")
            
            # レート制限回避
            time.sleep(1.5)
            
        except Exception as e:
            print(f"    ❌ エラー: {e}")
    
    print(f"\n✅ {workspace_name}: {success}/{len(failed_files)} 件のサマリーを再生成")
    return success


def main():
    print("🚀 サマリー再生成を開始...")
    total = regenerate_summaries("infobox")
    print(f"\n🎉 完了: {total} 件のサマリーを再生成")


if __name__ == "__main__":
    main()
