"""
TTS（Text-to-Speech）モジュール

Eleven Labs APIを使用してテキストを音声に変換する。
"""

import os
import tempfile
from pathlib import Path
from typing import Optional

import sys

TOOLS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS_DIR))
from runtime_env import load_runtime_env

load_runtime_env(TOOLS_DIR.parent)


# Eleven Labs 日本語対応の声
VOICE_PRESETS = {
    "japanese_female": "EXAVITQu4vr4xnSDxMaL",  # Sarah
    "japanese_male": "pNInz6obpgDQGcFmaJgB",    # Adam
    "energetic": "21m00Tcm4TlvDq8ikWAM",        # Rachel
    "calm": "AZnzlk1XvdvUeBnXmlld",             # Domi
    "default": "EXAVITQu4vr4xnSDxMaL",
}


def get_api_key() -> str:
    """Eleven Labs APIキーを取得"""
    api_key = os.environ.get("ELEVEN_API_KEY") or os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ELEVEN_API_KEY または ELEVENLABS_API_KEY が設定されていません。\n"
            "https://elevenlabs.io で取得してください。"
        )
    return api_key


def generate_speech(
    text: str,
    output_path: Optional[str] = None,
    voice: str = "default",
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> str:
    """
    テキストを音声に変換する
    
    Args:
        text: 変換するテキスト
        output_path: 出力ファイルパス（Noneの場合は一時ファイル）
        voice: 声のプリセット名 (japanese_female, japanese_male, energetic, calm)
        voice_id: Eleven LabsのボイスID（指定時はvoiceを上書き）
        model_id: モデルID
        stability: 安定性（0-1）
        similarity_boost: 類似性ブースト（0-1）
        
    Returns:
        生成された音声ファイルのパス
    """
    try:
        from elevenlabs import ElevenLabs
    except ImportError:
        raise ImportError("elevenlabs パッケージがインストールされていません: pip install elevenlabs")
    
    api_key = get_api_key()
    
    # ボイスIDを決定
    if voice_id is None:
        voice_id = VOICE_PRESETS.get(voice, VOICE_PRESETS["default"])
    
    # 出力パスを決定
    if output_path is None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            output_path = tmp.name
    else:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    print(f"🎤 音声生成中... (voice={voice}, {len(text)}文字)")
    
    try:
        client = ElevenLabs(api_key=api_key)
        
        # 音声を生成
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=model_id,
            voice_settings={
                "stability": stability,
                "similarity_boost": similarity_boost,
            }
        )
        
        # ファイルに保存
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        print(f"✅ 音声生成完了: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ 音声生成エラー: {e}")
        raise


def get_audio_duration(audio_path: str) -> float:
    """
    音声ファイルの長さを取得する（秒）
    
    Args:
        audio_path: 音声ファイルのパス
        
    Returns:
        長さ（秒）
    """
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0
    except Exception:
        # pydubが使えない場合は0を返す
        return 0.0


def list_voices() -> list:
    """
    利用可能な声の一覧を取得
    
    Returns:
        声の情報リスト
    """
    try:
        from elevenlabs import ElevenLabs
        api_key = get_api_key()
        client = ElevenLabs(api_key=api_key)
        
        voices = client.voices.get_all()
        return [
            {
                "voice_id": v.voice_id,
                "name": v.name,
                "labels": v.labels,
            }
            for v in voices.voices
        ]
    except Exception as e:
        print(f"声一覧の取得に失敗: {e}")
        return []


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="テキストを音声に変換")
    parser.add_argument("text", nargs="?", help="変換するテキスト")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument("--voice", "-v", default="default",
                       choices=list(VOICE_PRESETS.keys()))
    parser.add_argument("--list-voices", action="store_true", help="利用可能な声を一覧表示")
    
    args = parser.parse_args()
    
    if args.list_voices:
        print("利用可能な声:")
        print("-" * 50)
        for voice in list_voices():
            print(f"  {voice['name']}: {voice['voice_id']}")
        print("-" * 50)
        print("\nプリセット:")
        for name, vid in VOICE_PRESETS.items():
            print(f"  {name}: {vid}")
    elif args.text:
        output = generate_speech(
            text=args.text,
            output_path=args.output,
            voice=args.voice,
        )
        
        duration = get_audio_duration(output)
        print(f"音声の長さ: {duration:.1f}秒")
    else:
        parser.print_help()
