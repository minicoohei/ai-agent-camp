"""
UGC Storyboard Generator - 絵コンテ生成ツール

AI UGC動画制作のための絵コンテ作成ツール。
キャラクター参照画像＋詳細プロンプトで一貫性を保ちながら、
16コマの絵コンテを1枚の画像として生成します。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from dotenv import load_dotenv
from PIL import Image

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from bootcamp_utils import get_client, get_flash_model, get_image_model

try:
    from credential_manager import inject_to_environ
    inject_to_environ()
except ImportError:
    try:
        from tools.credential_manager import inject_to_environ
        inject_to_environ()
    except ImportError:
        pass
load_dotenv()


# デフォルト設定
DEFAULT_OUTPUT_DIR = Path("output/storyboard")
DEFAULT_NUM_FRAMES = 16

# アスペクト比とレイアウトの対応
ASPECT_RATIO_LAYOUTS = {
    "9:16": {"default": "2x8", "options": ["2x8", "4x4"]},
    "16:9": {"default": "8x2", "options": ["8x2", "4x4"]},
    "1:1": {"default": "4x4", "options": ["4x4"]},
    "4:3": {"default": "4x4", "options": ["4x4", "4x2"]},
    "3:4": {"default": "4x4", "options": ["4x4", "2x4"]},
}

# フレームサイズ（ピクセル）
FRAME_SIZES = {
    "9:16": (540, 960),
    "16:9": (960, 540),
    "1:1": (720, 720),
    "4:3": (800, 600),
    "3:4": (600, 800),
}

# デフォルト出力サイズ（リサイズ後）
DEFAULT_OUTPUT_WIDTH = 540  # 540px幅にリサイズ（TikTok 1080の半分）

# ビジュアルスタイル
VISUAL_STYLES = {
    "modern_clean": {
        "name": "モダン・クリーン",
        "base_prompt": "Modern minimalist aesthetic, clean lighting, professional quality, high detail",
        "setting": "minimalist room with clean lines, bright natural lighting"
    },
    "animal_crossing": {
        "name": "どうぶつの森風",
        "base_prompt": "Animal Crossing aesthetic, soft pastel colors, warm cozy atmosphere, cute rounded design",
        "setting": "cozy room with warm wood furniture, soft natural lighting, houseplants"
    },
    "vibrant_ugc": {
        "name": "ビビッドUGC",
        "base_prompt": "Vibrant energetic aesthetic, bold colors, dynamic composition, TikTok style",
        "setting": "colorful room with neon accents, ring light illumination"
    },
    "anime": {
        "name": "アニメ風",
        "base_prompt": "Anime illustration style, clean lines, vibrant colors, expressive",
        "setting": "stylized room with anime aesthetic"
    },
}

# カメラモーション
CAMERA_MOTIONS = {
    "zoom_in": "カメラがゆっくりズームイン",
    "zoom_out": "カメラがゆっくりズームアウト",
    "pan_left": "カメラが左にパン",
    "pan_right": "カメラが右にパン",
    "tilt_up": "カメラが上にティルト",
    "tilt_down": "カメラが下にティルト",
    "static": "カメラ固定",
}


def sanitize_filename(name: str) -> str:
    """ファイル名に使用できない文字を置換"""
    name = name.replace(" ", "_")
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name[:50]


def get_layout_dimensions(layout: str) -> Tuple[int, int]:
    """レイアウト文字列から行・列数を取得"""
    if "x" in layout:
        parts = layout.split("x")
        return int(parts[0]), int(parts[1])
    return 4, 4


def decompose_scenario_to_scenes(
    client,
    scenario: str,
    num_frames: int = 16,
    aspect_ratio: str = "9:16"
) -> List[Dict]:
    """
    シナリオから各フレームのシーン説明を生成
    
    Args:
        client: Gemini APIクライアント
        scenario: 動画のシナリオ・トピック
        num_frames: フレーム数
        aspect_ratio: アスペクト比
    
    Returns:
        シーン説明のリスト
    """
    orientation = "縦型（TikTok/Reels向け）" if aspect_ratio == "9:16" else "横型（YouTube向け）"
    
    prompt = f"""
あなたはUGC動画の絵コンテを作成するディレクターです。
以下のシナリオを{num_frames}コマの絵コンテに分解してください。

## シナリオ
{scenario}

## 形式
{orientation}

## 要件
1. 各コマは動画の流れを示す静止画として機能する
2. キャラクターのポーズ、表情、カメラアングルを具体的に指定
3. 動画のストーリーが自然に流れるように配置
4. 最初のフックから最後のCTAまで一貫した流れを作る

## 出力形式（JSON）
以下のJSON形式で出力してください：

```json
{{
  "title": "絵コンテタイトル",
  "scenes": [
    {{
      "frame_number": 1,
      "timestamp": "0:00-0:02",
      "scene_type": "hook",
      "description": "シーンの説明（日本語）",
      "visual_prompt": "English prompt for image generation describing character pose, expression, camera angle, and setting. NEVER include text/words/letters in the visual_prompt - text overlays will be added separately in post-production",
      "camera_angle": "medium shot / close-up / wide shot など",
      "character_action": "キャラクターのアクション",
      "emotion": "表情・感情",
      "narration": "このシーンのナレーション台本（日本語）。ナレーション不要の場合は空文字",
      "text_overlay": {{
        "main_text": "画面上に表示するメインテキスト（空なら表示なし）",
        "sub_text": "サブテキスト/キャプション（空なら表示なし）",
        "position": "top / center / bottom",
        "style": "bold / subtitle / minimal"
      }},
      "motion_type": "ken_burns / motion_graphics / i2v",
      "motion_note": "静止画で十分か、i2V動画変換が必要かの判定理由"
    }}
  ]
}}
```

## motion_type 判定基準
- "ken_burns": 風景や静的な構図。ズーム/パンで動きをつける（最低ライン）
- "motion_graphics": テキストアニメやUI遷移。Remotionで十分（i2V不要）
- "i2v": 人物の動き、表情変化、物理的なアクションがある場合（推奨：全フレーム）

⚠️ "static"は使わないでください。必ず ken_burns 以上の動きをつけてください。
静止画そのままだと安っぽくなるため、最低でも ken_burns を指定すること。

## テキスト配置ルール
- 画像内にテキストを描画しないでください（AIの日本語レンダリングは品質が低い）
- テロップ/キャプションはRemotionで後から合成します
- text_overlay で指定されたテキスト分のスペースを画面下部（55-65%の位置）に確保してください
- 具体的には、画面の下半分にテキストを被せても見やすいように、重要な被写体は画面上部〜中央に配置してください

JSONのみを出力してください。
"""
    
    print(f"📝 シナリオを{num_frames}コマに分解中...")
    
    response = client.models.generate_content(
        model=get_flash_model(),
        contents=[prompt]
    )
    
    response_text = response.text.strip()
    
    # JSONを抽出
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_str = response_text
    
    try:
        result = json.loads(json_str)
        scenes = result.get("scenes", [])
        print(f"✅ {len(scenes)}コマのシーン説明を生成しました")
        return scenes
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON解析エラー: {e}")
        print(f"Response: {response_text[:500]}...")
        return []


def generate_character_reference(
    client,
    character_prompt: str,
    aspect_ratio: str,
    style: str,
    output_path: Path
) -> Optional[Path]:
    """
    キャラクター参照画像を生成
    
    Args:
        client: Gemini APIクライアント
        character_prompt: キャラクター説明プロンプト
        aspect_ratio: アスペクト比
        style: ビジュアルスタイル
        output_path: 出力パス
    
    Returns:
        生成された画像のパス
    """
    from google.genai import types
    
    style_info = VISUAL_STYLES.get(style, VISUAL_STYLES["modern_clean"])
    
    full_prompt = f"""
Character reference sheet for UGC video storyboard.
{style_info['base_prompt']}

Character description: {character_prompt}

Create a clear, well-lit portrait showing the character from chest up.
The character should have a friendly, approachable expression.
Setting: {style_info['setting']}
High quality, detailed, consistent character design suitable for animation reference.
"""
    
    print(f"🎨 キャラクター参照画像を生成中...")
    
    try:
        response = client.models.generate_content(
            model=get_image_model(),
            contents=[full_prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",  # 参照画像は正方形
                    image_size="2K"
                )
            )
        )
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    print(f"✅ キャラクター参照画像: {output_path}")
                    return output_path
        
        print("⚠️ 画像データが見つかりませんでした")
        return None
        
    except Exception as e:
        print(f"❌ キャラクター参照画像生成エラー: {e}")
        return None


def generate_storyboard_sheet(
    client,
    scenes: List[Dict],
    character_image: Optional[Path],
    character_prompt: str,
    aspect_ratio: str,
    style: str,
    output_path: Path,
    num_frames: int = 8
) -> Optional[Path]:
    """
    全フレームを1枚の絵コンテシートとして一括生成。
    キャラクター一貫性を保つため、1回の生成で全フレームを含む画像を作る。
    
    Args:
        client: Gemini APIクライアント
        scenes: シーン情報リスト
        character_image: キャラクター参照画像パス
        character_prompt: キャラクター説明
        aspect_ratio: アスペクト比
        style: ビジュアルスタイル
        output_path: 出力パス
        num_frames: フレーム数
    
    Returns:
        生成された画像のパス
    """
    from google.genai import types
    
    style_info = VISUAL_STYLES.get(style, VISUAL_STYLES["modern_clean"])
    
    # グリッドレイアウト決定
    if num_frames <= 4:
        cols, rows = 2, 2
    elif num_frames <= 6:
        cols, rows = 2, 3
    elif num_frames <= 8:
        cols, rows = 2, 4
    else:
        cols, rows = 4, 4
    
    # 各フレームのシーン説明を組み立て
    scene_descriptions = []
    for i, scene in enumerate(scenes[:num_frames]):
        visual = scene.get("visual_prompt", scene.get("description", ""))
        camera = scene.get("camera_angle", "medium shot")
        emotion = scene.get("emotion", "neutral")
        scene_descriptions.append(
            f"Frame {i+1} (row {i//cols + 1}, col {i%cols + 1}): {visual}. Camera: {camera}. Expression: {emotion}"
        )
    
    scenes_text = "\n".join(scene_descriptions)
    
    full_prompt = f"""
Create a professional storyboard sheet with EXACTLY {num_frames} frames arranged in a {cols}x{rows} grid layout.
{style_info['base_prompt']}

CHARACTER (SAME person in EVERY frame - this is CRITICAL):
{character_prompt}

The SAME character must appear in ALL frames with IDENTICAL: face shape, eye color/shape, hair color/style, skin tone, body proportions, outfit (white blouse + light blue cardigan + gold necklace).

STORYBOARD FRAMES:
{scenes_text}

LAYOUT RULES:
- {cols} columns x {rows} rows grid, evenly spaced
- Each frame is a separate scene panel with thin border/divider between them
- Frames read left-to-right, top-to-bottom (like a manga/comic)
- Each frame should be roughly {aspect_ratio} aspect ratio within the grid
- Number each frame clearly in the corner (1, 2, 3...)

CRITICAL RULES:
- The character's appearance must be 100% consistent across ALL frames
- Do NOT include any text, words, captions, or dialogue in the frames (only frame numbers)
- Each frame shows a different scene/pose but the SAME character
- Professional storyboard quality with clear composition per frame

Generate ONE single image containing the complete {cols}x{rows} storyboard grid.
"""
    
    print(f"🎨 全{num_frames}フレームを1枚のシートとして生成中（{cols}x{rows}グリッド）...")
    
    try:
        contents = [full_prompt]
        
        # キャラクター参照画像がある場合は追加
        if character_image and character_image.exists():
            ref_image = Image.open(character_image)
            contents = [full_prompt, ref_image]
        
        response = client.models.generate_content(
            model=get_image_model(),
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="3:4" if num_frames <= 8 else "1:1",
                    image_size="2K"
                )
            )
        )
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    print(f"✅ 絵コンテシート生成: {output_path}")
                    return output_path
        
        print("⚠️ 画像データが見つかりませんでした")
        return None
        
    except Exception as e:
        print(f"❌ 絵コンテシート生成エラー: {e}")
        return None


def split_storyboard_sheet(
    sheet_path: Path,
    num_frames: int,
    output_dir: Path,
    output_width: int = DEFAULT_OUTPUT_WIDTH
) -> List[Path]:
    """
    1枚の絵コンテシートを個別フレームに切り出す。
    
    Args:
        sheet_path: シート画像パス
        num_frames: フレーム数
        output_dir: 出力ディレクトリ
        output_width: 出力幅（0で無制限）
    
    Returns:
        切り出したフレーム画像パスのリスト
    """
    if num_frames <= 4:
        cols, rows = 2, 2
    elif num_frames <= 6:
        cols, rows = 2, 3
    elif num_frames <= 8:
        cols, rows = 2, 4
    else:
        cols, rows = 4, 4
    
    img = Image.open(sheet_path)
    w, h = img.size
    
    cell_w = w // cols
    cell_h = h // rows
    
    # ボーダー/マージンを自動検出してトリミング
    margin_x = int(cell_w * 0.02)  # 2%マージン
    margin_y = int(cell_h * 0.02)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    
    print(f"✂️ シートを{cols}x{rows}に切り出し中... (元画像: {w}x{h})")
    
    for idx in range(min(num_frames, cols * rows)):
        row = idx // cols
        col = idx % cols
        
        left = col * cell_w + margin_x
        top = row * cell_h + margin_y
        right = (col + 1) * cell_w - margin_x
        bottom = (row + 1) * cell_h - margin_y
        
        frame = img.crop((left, top, right, bottom))
        
        # リサイズ
        if output_width > 0 and frame.width > output_width:
            ratio = output_width / frame.width
            new_size = (output_width, int(frame.height * ratio))
            frame = frame.resize(new_size, Image.Resampling.LANCZOS)
        
        frame_path = output_dir / f"frame_{idx+1:02d}.jpg"
        frame.save(frame_path, 'JPEG', quality=90)
        size_kb = frame_path.stat().st_size // 1024
        print(f"  📷 frame_{idx+1:02d}.jpg ({frame.width}x{frame.height}, {size_kb}KB)")
        frame_paths.append(frame_path)
    
    print(f"✅ {len(frame_paths)}フレーム切り出し完了")
    return frame_paths


def resize_frame(image_path: Path, max_width: int = DEFAULT_OUTPUT_WIDTH) -> Path:
    """
    フレーム画像をリサイズして上書き保存
    
    Args:
        image_path: 画像パス
        max_width: 最大幅（ピクセル）
    
    Returns:
        リサイズ後の画像パス
    """
    try:
        img = Image.open(image_path)
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            # JPEGで保存してファイルサイズも削減
            jpg_path = image_path.with_suffix('.jpg')
            img.save(jpg_path, 'JPEG', quality=90)
            # 元のPNGを削除
            if image_path.suffix == '.png' and jpg_path != image_path:
                image_path.unlink(missing_ok=True)
            print(f"    📐 リサイズ: {new_size[0]}x{new_size[1]} ({jpg_path.stat().st_size // 1024}KB)")
            return jpg_path
        return image_path
    except Exception as e:
        print(f"    ⚠️ リサイズエラー: {e}")
        return image_path


def generate_frame_image(
    client,
    scene: Dict,
    character_image: Optional[Path],
    character_prompt: str,
    aspect_ratio: str,
    style: str,
    output_path: Path,
    frame_index: int,
    output_width: int = DEFAULT_OUTPUT_WIDTH
) -> Optional[Path]:
    """
    1フレームの画像を生成
    
    Args:
        client: Gemini APIクライアント
        scene: シーン情報
        character_image: キャラクター参照画像パス
        character_prompt: キャラクター説明
        aspect_ratio: アスペクト比
        style: ビジュアルスタイル
        output_path: 出力パス
        frame_index: フレーム番号
        output_width: 出力幅（0で無制限）
    
    Returns:
        生成された画像のパス
    """
    from google.genai import types
    
    style_info = VISUAL_STYLES.get(style, VISUAL_STYLES["modern_clean"])
    
    visual_prompt = scene.get("visual_prompt", scene.get("description", ""))
    camera_angle = scene.get("camera_angle", "medium shot")
    emotion = scene.get("emotion", "neutral")
    
    # キャラクター一貫性を強化するプロンプト
    character_consistency = f"""
CHARACTER CONSISTENCY RULES (CRITICAL):
- This is frame {frame_index} of a continuous storyboard. The SAME character appears in every frame.
- Character identity: {character_prompt}
- You MUST maintain EXACTLY the same: face shape, eye color, eye shape, hair color, hair style, skin tone, body proportions, clothing/outfit across ALL frames.
- The character's outfit, accessories, and distinguishing features must NOT change between frames.
- Only the pose, expression, and camera angle should differ per scene.
- Think of this as keyframes from the SAME animated video — the character design is LOCKED.
"""
    
    full_prompt = f"""
Storyboard frame {frame_index} for UGC video.
{style_info['base_prompt']}

{character_consistency}

Scene: {visual_prompt}
Camera angle: {camera_angle}
Character emotion: {emotion}
Setting: {style_info['setting']}

Generate a single frame suitable for video storyboard.
High quality, detailed illustration.

CRITICAL: Do NOT include ANY text, words, letters, numbers, labels, watermarks, or written characters in the image. The image must be purely visual with ZERO text elements. No captions, no titles, no UI elements with text.
"""
    
    print(f"  🖼️ フレーム {frame_index} 生成中...")
    
    try:
        contents = [full_prompt]
        
        # キャラクター参照画像がある場合は追加
        if character_image and character_image.exists():
            ref_image = Image.open(character_image)
            contents = [full_prompt, ref_image]
        
        response = client.models.generate_content(
            model=get_image_model(),
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="2K"
                )
            )
        )
        
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.inline_data:
                    result_image = types.Part.as_image(part)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    result_image.save(output_path)
                    return output_path
        
        return None
        
    except Exception as e:
        print(f"    ❌ フレーム {frame_index} 生成エラー: {e}")
        return None


def compose_storyboard_grid(
    frame_paths: List[Path],
    layout: str,
    aspect_ratio: str,
    output_path: Path
) -> Optional[Path]:
    """
    フレーム画像をグリッドレイアウトで合成
    
    Args:
        frame_paths: フレーム画像パスのリスト
        layout: レイアウト（例: "4x4", "2x8"）
        aspect_ratio: 各フレームのアスペクト比
        output_path: 出力パス
    
    Returns:
        合成画像のパス
    """
    cols, rows = get_layout_dimensions(layout)
    frame_size = FRAME_SIZES.get(aspect_ratio, (720, 720))
    
    # グリッド画像のサイズ計算
    padding = 10
    grid_width = cols * frame_size[0] + (cols + 1) * padding
    grid_height = rows * frame_size[1] + (rows + 1) * padding
    
    # 白背景のグリッド画像を作成
    grid_image = Image.new('RGB', (grid_width, grid_height), color=(255, 255, 255))
    
    print(f"📐 グリッドレイアウト: {layout} ({cols}列 x {rows}行)")
    
    for idx, frame_path in enumerate(frame_paths):
        if idx >= cols * rows:
            break
        
        if frame_path and frame_path.exists():
            try:
                frame = Image.open(frame_path)
                frame = frame.resize(frame_size, Image.Resampling.LANCZOS)
                
                row = idx // cols
                col = idx % cols
                
                x = padding + col * (frame_size[0] + padding)
                y = padding + row * (frame_size[1] + padding)
                
                grid_image.paste(frame, (x, y))
            except Exception as e:
                print(f"  ⚠️ フレーム {idx+1} の貼り付けエラー: {e}")
    
    # 保存
    output_path.parent.mkdir(parents=True, exist_ok=True)
    grid_image.save(output_path, quality=95)
    print(f"✅ 絵コンテグリッド画像: {output_path}")
    
    return output_path


def generate_video_from_frames(
    start_frame_path: Path,
    end_frame_path: Optional[Path],
    output_dir: Path,
    duration: int = 5,
    camera_motion: Optional[str] = None,
    script: str = ""
) -> Optional[Path]:
    """
    フレーム画像からKlingで動画を生成
    
    Args:
        start_frame_path: 開始フレーム画像パス
        end_frame_path: 終了フレーム画像パス（オプション）
        output_dir: 出力ディレクトリ
        duration: 動画の長さ（秒）
        camera_motion: カメラモーション
        script: スクリプト（プロンプト用）
    
    Returns:
        生成された動画のパス
    """
    try:
        # Kling エンジンをインポート
        sys.path.insert(0, str(Path(__file__).parents[3] / "tools" / "ugc" / "engines"))
        from kling import KlingEngine
        
        engine = KlingEngine()
        engine.validate_api_key()
        
        # 出力パス
        video_dir = output_dir / "video"
        video_dir.mkdir(parents=True, exist_ok=True)
        output_path = video_dir / "output.mp4"
        
        # カメラモーションのプロンプト追加
        motion_prompt = ""
        if camera_motion and camera_motion in CAMERA_MOTIONS:
            motion_prompt = f"Camera motion: {camera_motion}. "
        
        # 動画生成
        print(f"🎬 Kling 2.6 Pro で動画生成中...")
        print(f"   開始フレーム: {start_frame_path}")
        if end_frame_path:
            print(f"   終了フレーム: {end_frame_path}")
        
        result = engine.generate(
            avatar_image=str(start_frame_path),
            script=motion_prompt + script,
            output_path=str(output_path),
            duration=duration,
            generate_audio=False
        )
        
        print(f"✅ 動画生成完了: {result.video_path}")
        print(f"   長さ: {result.duration}秒, コスト: ${result.cost:.2f}")
        
        return Path(result.video_path)
        
    except ImportError as e:
        print(f"❌ Kling エンジンのインポートエラー: {e}")
        return None
    except Exception as e:
        print(f"❌ 動画生成エラー: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="UGC Storyboard Generator - AI UGC用絵コンテ生成ツール"
    )
    
    # 基本パラメータ
    parser.add_argument(
        "--scenario", "-s",
        help="動画のシナリオ・トピック"
    )
    parser.add_argument(
        "--character", "-c",
        help="キャラクター詳細プロンプト"
    )
    parser.add_argument(
        "--character-image", "-ci",
        help="既存のキャラクター参照画像パス"
    )
    parser.add_argument(
        "--aspect-ratio", "-ar",
        default="9:16",
        choices=["9:16", "16:9", "1:1", "4:3", "3:4"],
        help="アスペクト比（デフォルト: 9:16）"
    )
    parser.add_argument(
        "--num-frames", "-n",
        type=int,
        default=16,
        choices=[4, 8, 16],
        help="フレーム数（デフォルト: 16）"
    )
    parser.add_argument(
        "--layout", "-l",
        help="グリッドレイアウト（例: 4x4, 2x8）"
    )
    parser.add_argument(
        "--style",
        default="modern_clean",
        choices=list(VISUAL_STYLES.keys()),
        help="ビジュアルスタイル"
    )
    parser.add_argument(
        "--session",
        help="セッション名（出力フォルダ名）"
    )
    parser.add_argument(
        "--output-width", "-ow",
        type=int,
        default=DEFAULT_OUTPUT_WIDTH,
        help=f"出力画像の最大幅（ピクセル、デフォルト: {DEFAULT_OUTPUT_WIDTH}、0で無制限）"
    )
    parser.add_argument(
        "--mode", "-m",
        default="sheet",
        choices=["sheet", "individual"],
        help="生成モード: sheet=1枚シート→切り出し（キャラ一貫性◎）、individual=1枚ずつ生成（デフォルト: sheet）"
    )
    
    # 動画生成パラメータ
    parser.add_argument(
        "--start-frame", "-sf",
        type=int,
        help="動画生成時の開始フレーム番号"
    )
    parser.add_argument(
        "--end-frame", "-ef",
        type=int,
        help="動画生成時の終了フレーム番号"
    )
    parser.add_argument(
        "--video-duration", "-vd",
        type=int,
        default=5,
        choices=[5, 10],
        help="動画の長さ（秒）"
    )
    parser.add_argument(
        "--camera-motion", "-cm",
        choices=list(CAMERA_MOTIONS.keys()),
        help="カメラモーション"
    )
    
    # 既存の絵コンテから動画生成
    parser.add_argument(
        "--storyboard-dir",
        help="既存の絵コンテディレクトリから動画を生成"
    )
    
    args = parser.parse_args()
    
    # クライアント初期化
    client = get_client()
    if not client:
        print("❌ GEMINI_API_KEY が設定されていません")
        sys.exit(1)
    
    # 出力ディレクトリの設定
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    if args.session:
        session_name = sanitize_filename(args.session)
        output_dir = DEFAULT_OUTPUT_DIR / f"{timestamp}_{session_name}"
    else:
        output_dir = DEFAULT_OUTPUT_DIR / timestamp
    
    # 既存の絵コンテから動画生成モード
    if args.storyboard_dir:
        storyboard_dir = Path(args.storyboard_dir)
        if not storyboard_dir.exists():
            print(f"❌ 絵コンテディレクトリが見つかりません: {storyboard_dir}")
            sys.exit(1)
        
        frames_dir = storyboard_dir / "frames"
        if not frames_dir.exists():
            print(f"❌ フレームディレクトリが見つかりません: {frames_dir}")
            sys.exit(1)
        
        if not args.start_frame:
            print("❌ --start-frame を指定してください")
            sys.exit(1)
        
        start_frame_path = frames_dir / f"frame_{args.start_frame:02d}.png"
        end_frame_path = None
        if args.end_frame:
            end_frame_path = frames_dir / f"frame_{args.end_frame:02d}.png"
        
        generate_video_from_frames(
            start_frame_path=start_frame_path,
            end_frame_path=end_frame_path,
            output_dir=storyboard_dir,
            duration=args.video_duration,
            camera_motion=args.camera_motion
        )
        return
    
    # 新規絵コンテ生成モード
    if not args.scenario:
        print("❌ --scenario を指定してください")
        parser.print_help()
        sys.exit(1)
    
    if not args.character and not args.character_image:
        print("❌ --character または --character-image を指定してください")
        parser.print_help()
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n📁 出力ディレクトリ: {output_dir}")
    
    # レイアウトの決定
    if args.layout:
        layout = args.layout
    else:
        layout = ASPECT_RATIO_LAYOUTS.get(args.aspect_ratio, {}).get("default", "4x4")
    
    # キャラクター参照画像
    character_image_path = None
    character_prompt = args.character or ""
    
    if args.character_image:
        character_image_path = Path(args.character_image)
        if not character_image_path.exists():
            print(f"⚠️ キャラクター画像が見つかりません: {args.character_image}")
            character_image_path = None
    
    if not character_image_path and args.character:
        character_image_path = generate_character_reference(
            client=client,
            character_prompt=args.character,
            aspect_ratio=args.aspect_ratio,
            style=args.style,
            output_path=output_dir / "character_reference.png"
        )
        # キャラ参照画像はリサイズしない（一貫性の参照元として高解像度を維持）
    
    # シナリオからシーン分解
    scenes = decompose_scenario_to_scenes(
        client=client,
        scenario=args.scenario,
        num_frames=args.num_frames,
        aspect_ratio=args.aspect_ratio
    )
    
    if not scenes:
        print("❌ シーン分解に失敗しました")
        sys.exit(1)
    
    # シーン情報を保存
    scenes_json_path = output_dir / "scenes.json"
    with open(scenes_json_path, "w", encoding="utf-8") as f:
        json.dump({"title": args.scenario, "scenes": scenes}, f, ensure_ascii=False, indent=2)
    print(f"📄 シーン情報: {scenes_json_path}")
    
    # フレーム画像生成
    frames_dir = output_dir / "frames"
    frame_paths = []
    
    if args.mode == "sheet":
        # === シートモード: 1枚生成→切り出し（キャラ一貫性◎） ===
        print(f"\n🎨 シートモード: 全{len(scenes)}フレームを1枚の画像として生成...")
        
        sheet_path = generate_storyboard_sheet(
            client=client,
            scenes=scenes,
            character_image=character_image_path,
            character_prompt=character_prompt,
            aspect_ratio=args.aspect_ratio,
            style=args.style,
            output_path=output_dir / "storyboard_sheet.png",
            num_frames=len(scenes)
        )
        
        if sheet_path:
            # シートを個別フレームに切り出し
            frame_paths = split_storyboard_sheet(
                sheet_path=sheet_path,
                num_frames=len(scenes),
                output_dir=frames_dir,
                output_width=args.output_width
            )
            
            # シート自体もリサイズしてグリッドとして保存
            grid_ext = "jpg" if args.output_width > 0 else "png"
            grid_path = output_dir / f"storyboard_grid.{grid_ext}"
            sheet_img = Image.open(sheet_path)
            grid_width = args.output_width * 2 if args.output_width > 0 else sheet_img.width
            if sheet_img.width > grid_width:
                ratio = grid_width / sheet_img.width
                sheet_img = sheet_img.resize(
                    (grid_width, int(sheet_img.height * ratio)),
                    Image.Resampling.LANCZOS
                )
            sheet_img.save(grid_path, 'JPEG' if grid_ext == 'jpg' else 'PNG', quality=90)
            print(f"📐 グリッド画像: {grid_path} ({grid_path.stat().st_size // 1024}KB)")
        else:
            print("⚠️ シート生成失敗。individualモードにフォールバック...")
            args.mode = "individual"
    
    if args.mode == "individual":
        # === 個別モード: 1フレームずつ生成 ===
        print(f"\n🎨 個別モード: {len(scenes)}フレームを1枚ずつ生成...")
        
        for idx, scene in enumerate(scenes):
            frame_path = frames_dir / f"frame_{idx+1:02d}.png"
            
            result_path = generate_frame_image(
                client=client,
                scene=scene,
                character_image=character_image_path,
                character_prompt=character_prompt,
                aspect_ratio=args.aspect_ratio,
                style=args.style,
                output_path=frame_path,
                frame_index=idx + 1,
                output_width=args.output_width
            )
            
            # リサイズ
            if result_path and args.output_width > 0:
                result_path = resize_frame(result_path, args.output_width)
            
            frame_paths.append(result_path)
        
        # グリッドレイアウトで合成
        successful_frames = [p for p in frame_paths if p is not None]
        if successful_frames:
            grid_ext = "jpg" if args.output_width > 0 else "png"
            grid_path = compose_storyboard_grid(
                frame_paths=frame_paths,
                layout=layout,
                aspect_ratio=args.aspect_ratio,
                output_path=output_dir / f"storyboard_grid.{grid_ext}"
            )
    
    # 動画生成（オプション）
    if args.start_frame and successful_frames:
        start_idx = args.start_frame - 1
        end_idx = (args.end_frame - 1) if args.end_frame else None
        
        if 0 <= start_idx < len(frame_paths) and frame_paths[start_idx]:
            start_frame_path = frame_paths[start_idx]
            end_frame_path = None
            if end_idx is not None and 0 <= end_idx < len(frame_paths) and frame_paths[end_idx]:
                end_frame_path = frame_paths[end_idx]
            
            generate_video_from_frames(
                start_frame_path=start_frame_path,
                end_frame_path=end_frame_path,
                output_dir=output_dir,
                duration=args.video_duration,
                camera_motion=args.camera_motion,
                script=args.scenario
            )
    
    # 完了メッセージ
    print("\n" + "=" * 60)
    print("✅ 絵コンテ生成完了!")
    print("=" * 60)
    print(f"\n📁 出力先: {output_dir}")
    print(f"   - キャラクター参照: character_reference.png")
    ext = "jpg" if args.output_width > 0 else "png"
    print(f"   - フレーム画像: frames/frame_01.{ext} ~ frame_{args.num_frames:02d}.{ext}")
    print(f"   - グリッド画像: storyboard_grid.png")
    print(f"   - シーン情報: scenes.json")
    
    if args.start_frame:
        print(f"   - 動画: video/output.mp4")
    
    print("\n動画生成のみ実行する場合:")
    print(f'  python {__file__} --storyboard-dir "{output_dir}" --start-frame 1 --end-frame 8 --video-duration 10')
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
