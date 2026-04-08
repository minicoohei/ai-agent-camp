#!/usr/bin/env python3
"""
API 疎通確認スクリプト

設定済みの API キーで各サービスへの接続をテストします。

使い方:
    python test-script.py
"""

import json
import os
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Error: requests パッケージが必要です。")
    print("  pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv がなくても環境変数から直接読める


def test_gemini():
    """Google Gemini API のテスト"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {"status": "not_configured", "note": "GEMINI_API_KEY が未設定"}

    start = time.time()
    try:
        response = requests.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
            timeout=10
        )
        elapsed = int((time.time() - start) * 1000)

        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m["name"] for m in models[:3]]
            return {
                "status": "ok",
                "response_time_ms": elapsed,
                "model": model_names[0] if model_names else "unknown",
                "note": f"モデル一覧取得成功（{len(models)}件）"
            }
        else:
            return {
                "status": "error",
                "response_time_ms": elapsed,
                "note": f"HTTP {response.status_code}: {response.text[:100]}"
            }
    except Exception as e:
        return {"status": "error", "note": str(e)[:100]}


def test_anthropic():
    """Anthropic Claude API のテスト"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {"status": "not_configured", "note": "ANTHROPIC_API_KEY が未設定"}

    start = time.time()
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "ping"}],
            },
            timeout=15
        )
        elapsed = int((time.time() - start) * 1000)

        if response.status_code == 200:
            model = response.json().get("model", "unknown")
            return {
                "status": "ok",
                "response_time_ms": elapsed,
                "model": model,
                "note": "メッセージAPI応答成功"
            }
        else:
            return {
                "status": "error",
                "response_time_ms": elapsed,
                "note": f"HTTP {response.status_code}: {response.text[:100]}"
            }
    except Exception as e:
        return {"status": "error", "note": str(e)[:100]}


def test_openai():
    """OpenAI API のテスト"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return {"status": "not_configured", "note": "OPENAI_API_KEY が未設定"}

    start = time.time()
    try:
        response = requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        elapsed = int((time.time() - start) * 1000)

        if response.status_code == 200:
            models = response.json().get("data", [])
            return {
                "status": "ok",
                "response_time_ms": elapsed,
                "note": f"モデル一覧取得成功（{len(models)}件）"
            }
        else:
            return {
                "status": "error",
                "response_time_ms": elapsed,
                "note": f"HTTP {response.status_code}"
            }
    except Exception as e:
        return {"status": "error", "note": str(e)[:100]}


def test_fal():
    """fal.ai API のテスト"""
    api_key = os.environ.get("FAL_KEY")
    if not api_key:
        return {"status": "not_configured", "note": "FAL_KEY が未設定"}

    return {"status": "ok", "note": "キー設定済み（接続テストはスキップ）"}


def main():
    print("=" * 50)
    print("API 疎通確認テスト")
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()

    tests = [
        ("Google Gemini", test_gemini),
        ("Anthropic Claude", test_anthropic),
        ("OpenAI", test_openai),
        ("fal.ai", test_fal),
    ]

    results = []
    for name, test_func in tests:
        print(f"テスト中: {name}...", end=" ", flush=True)
        result = test_func()
        result["service"] = name

        status_icon = {
            "ok": "[OK]",
            "not_configured": "[SKIP]",
            "error": "[FAIL]",
        }.get(result["status"], "[?]")

        print(f"{status_icon} {result.get('note', '')}")
        results.append(result)

    # サマリー
    ok_count = sum(1 for r in results if r["status"] == "ok")
    skip_count = sum(1 for r in results if r["status"] == "not_configured")
    error_count = sum(1 for r in results if r["status"] == "error")

    print()
    print("-" * 50)
    print(f"結果: OK={ok_count}, スキップ={skip_count}, エラー={error_count}")
    print("-" * 50)

    if error_count > 0:
        print("\nエラーのあるサービスの API キーを確認してください。")
        sys.exit(1)
    elif ok_count == 0:
        print("\n設定済みの API キーがありません。.env ファイルを確認してください。")
    else:
        print("\n必須 API の接続テスト完了。")


if __name__ == "__main__":
    main()
