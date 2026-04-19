#!/usr/bin/env python3
"""
Slackログのサマリー生成＆アーカイブスクリプト

指定日より前の最終更新のファイルに対して：
1. AIでサマリーを生成
2. サマリーをsummary/フォルダに保存
3. 元ファイルをarchive/フォルダに移動
"""

import os
import re
import shutil
import time
from pathlib import Path
from datetime import datetime

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

# カットオフ日付
CUTOFF_DATE = "2025-12-01"


def get_latest_date_from_file(file_path: Path) -> str | None:
    """ファイル内の最新日付（## YYYY-MM-DD形式）を取得"""
    try:
        content = file_path.read_text(encoding="utf-8")
        dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", content, re.MULTILINE)
        if dates:
            return max(dates)  # 最新の日付を返す
    except Exception as e:
        print(f"  ⚠️ ファイル読み込みエラー: {e}")
    return None


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
        return f"# {channel_name} サマリー\n\n⚠️ サマリー生成に失敗しました\n"


def process_workspace(workspace_name: str):
    """ワークスペースのファイルを処理"""
    source_dir = DATA_DIR / workspace_name
    summary_dir = DATA_DIR / "summary" / workspace_name
    archive_dir = DATA_DIR / "archive" / workspace_name
    
    # ディレクトリ作成
    summary_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*50}")
    print(f"📁 {workspace_name} を処理中...")
    print(f"{'='*50}")
    
    # 対象ファイルを特定
    target_files = []
    for md_file in source_dir.glob("*.md"):
        latest_date = get_latest_date_from_file(md_file)
        if latest_date and latest_date < CUTOFF_DATE:
            target_files.append((md_file, latest_date))
    
    print(f"📊 対象ファイル: {len(target_files)} 件")
    
    # 処理
    processed = 0
    for md_file, latest_date in target_files:
        channel_name = md_file.stem
        print(f"\n  [{processed + 1}/{len(target_files)}] {channel_name} (最終: {latest_date})")
        
        try:
            # ファイル内容を読み込み
            content = md_file.read_text(encoding="utf-8")
            
            # サマリー生成
            print(f"    🤖 サマリー生成中...")
            summary = generate_summary(content, channel_name)
            
            # サマリーを保存
            summary_file = summary_dir / f"{channel_name}_summary.md"
            summary_file.write_text(summary, encoding="utf-8")
            print(f"    ✅ サマリー保存: {summary_file.name}")
            
            # 元ファイルをarchiveに移動
            archive_file = archive_dir / md_file.name
            shutil.move(str(md_file), str(archive_file))
            print(f"    📦 アーカイブ: {archive_file.name}")
            
            processed += 1
            
            # レート制限回避（1秒待機）
            time.sleep(1)
            
        except Exception as e:
            print(f"    ❌ エラー: {e}")
    
    print(f"\n✅ {workspace_name}: {processed}/{len(target_files)} 件を処理完了")
    return processed


def main():
    print("🚀 サマリー生成＆アーカイブ処理を開始...")
    print(f"📅 カットオフ日付: {CUTOFF_DATE} より前のファイルが対象")
    
    # 全ワークスペースを処理
    total = 0
    # 自分のワークスペースに合わせて変更してください
    for workspace in ["my-workspace"]:
        total += process_workspace(workspace)
    
    print(f"\n{'='*50}")
    print(f"🎉 全体完了: {total} 件のファイルを処理")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
