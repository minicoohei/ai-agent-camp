#!/usr/bin/env python3
"""
PDF Page Editor - PDFのテキスト編集ツール
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path

import yaml
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env

load_runtime_env()


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
GEMINI_VISION_MODEL = "gemini-3-flash-preview"
GEMINI_IMAGE_MODEL = "gemini-3-pro-preview"

EXTRACTION_PROMPT = """このスライド/ページ画像を詳細に解析し、すべてのテキスト要素を抽出してください。

以下のJSON形式で出力してください：

```json
{
  "layout": "title_slide | content | section_header | two_column | image_heavy | document",
  "elements": [
    {
      "type": "title | heading | subheading | text | bullet_list | numbered_list | code_block | caption | footer | header",
      "content": "テキスト内容",
      "items": ["箇条書き項目1", "箇条書き項目2"],
      "position": {
        "region": "top | center | bottom | left | right | top-left | top-right | bottom-left | bottom-right"
      }
    }
  ],
  "diagrams": [
    {
      "type": "flowchart | diagram | chart | image | icon",
      "description": "図の説明",
      "labels": ["図内のテキストラベル1", "ラベル2"]
    }
  ],
  "notes": "ページ全体に関する補足情報"
}
```

重要な指示：
1. すべてのテキスト要素を正確に抽出してください
2. 図やダイアグラム内のテキストラベルも抽出してください
3. 日本語と英語の両方を正確に抽出してください
4. JSON形式のみを出力してください（説明文不要）
"""


def get_client():
    from google import genai
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is not set.")
        sys.exit(1)
    return genai.Client(api_key=GEMINI_API_KEY)


def get_workspace_path(pdf_path: Path) -> Path:
    return pdf_path.parent / f"{pdf_path.stem}_workspace"


def image_to_bytes(image: Image.Image) -> bytes:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def parse_json_response(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        return {"layout": "unknown", "elements": [], "raw_response": text}


def cmd_analyze(args):
    from google.genai import types
    from pdf2image import convert_from_path
    from tqdm import tqdm

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    workspace = get_workspace_path(pdf_path)
    pages_dir = workspace / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    print(f"📄 PDF解析を開始: {pdf_path.name}")
    print(f"📁 ワークスペース: {workspace}")

    print("\n🔄 PDFをページ画像に変換中...")
    images = convert_from_path(pdf_path, dpi=args.dpi)
    print(f"   {len(images)} ページを変換しました")

    print("\n💾 ページ画像を保存中...")
    for i, image in enumerate(images, start=1):
        page_path = pages_dir / f"page_{i:03d}.png"
        image.save(page_path, "PNG")

    client = get_client()
    print("\n🔍 各ページを解析中...")

    pages_data = []
    for i, image in tqdm(enumerate(images, start=1), total=len(images), desc="解析中"):
        image_bytes = image_to_bytes(image)
        try:
            response = client.models.generate_content(
                model=GEMINI_VISION_MODEL,
                contents=[
                    EXTRACTION_PROMPT,
                    types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                ],
                config=types.GenerateContentConfig(temperature=0.1),
            )
            page_data = parse_json_response(response.text)
        except Exception as e:
            tqdm.write(f"⚠️ ページ {i} の解析エラー: {e}")
            page_data = {"layout": "unknown", "elements": [], "error": str(e)}

        page_data["page_number"] = i
        page_data["image_path"] = str(pages_dir / f"page_{i:03d}.png")
        pages_data.append(page_data)

    result = {
        "document": {
            "source": pdf_path.name,
            "total_pages": len(pages_data),
            "workspace": str(workspace),
            "analyzed_at": datetime.now().isoformat(),
        },
        "pages": pages_data,
    }

    yaml_path = workspace / "analysis.yaml"

    class CustomDumper(yaml.SafeDumper):
        pass

    def str_representer(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    CustomDumper.add_representer(str, str_representer)

    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(result, f, Dumper=CustomDumper, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

    print(f"\n✅ 解析完了: {yaml_path}")
    print("\n📊 解析サマリー:")
    print(f"   - 総ページ数: {len(pages_data)}")
    print(f"   - ワークスペース: {workspace}")

    print("\n📑 ページ一覧:")
    for page in pages_data:
        layout = page.get("layout", "unknown")
        text_preview = ""
        for elem in page.get("elements", []):
            if elem.get("type") == "title" and elem.get("content"):
                c = elem["content"]
                text_preview = f' - "{c[:40]}..."' if len(c) > 40 else f' - "{c}"'
                break
        print(f"   Page {page['page_number']:3d}: {layout}{text_preview}")

    return result


def cmd_edit(args):
    from google.genai import types

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}")
        print("ヒント: 先に 'analyze' コマンドでPDFを解析してください")
        sys.exit(1)

    yaml_path = workspace / "analysis.yaml"
    if not yaml_path.exists():
        print(f"Error: Analysis file not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        analysis = yaml.safe_load(f)

    page_number = args.page
    total_pages = analysis["document"]["total_pages"]

    if page_number < 1 or page_number > total_pages:
        print(f"Error: Page number must be between 1 and {total_pages}")
        sys.exit(1)

    page_data = analysis["pages"][page_number - 1]
    
    # 編集済み画像が存在する場合はそれを使用（連鎖編集対応）
    if page_data.get("edited_path") and Path(page_data["edited_path"]).exists():
        image_path = Path(page_data["edited_path"])
        print(f"   既存の編集済み画像を使用: {image_path}")
    else:
        image_path = Path(page_data["image_path"])

    if not image_path.exists():
        print(f"Error: Page image not found: {image_path}")
        sys.exit(1)

    if args.replace:
        old_text, new_text = args.replace
        prompt = f"""この画像内のテキスト「{old_text}」を「{new_text}」に置き換えてください。
それ以外の部分は一切変更しないでください。背景、レイアウト、他のテキストはそのまま保持してください。"""
    elif args.delete:
        prompt = f"""この画像内のテキスト「{args.delete}」を削除してください。
削除した部分は周囲の背景色で自然に埋めてください。
それ以外の部分は一切変更しないでください。"""
    elif args.prompt:
        prompt = args.prompt
    else:
        print("Error: 編集指示を指定してください (--replace, --delete, or --prompt)")
        sys.exit(1)

    print(f"📝 ページ {page_number} を編集中...")
    print(f"   画像: {image_path}")
    print(f"   指示: {prompt[:100]}...")

    client = get_client()
    input_image = Image.open(image_path)

    # オーバーレイ画像（ロゴなど）の読み込み
    overlay_image = None
    if args.overlay:
        overlay_path = Path(args.overlay)
        if overlay_path.exists():
            overlay_image = Image.open(overlay_path)
            print(f"   オーバーレイ: {overlay_path}")
        else:
            print(f"Warning: Overlay image not found: {overlay_path}")

    width, height = input_image.size
    aspect_ratio = width / height
    if aspect_ratio > 1.9:
        ar_str = "21:9"
    elif aspect_ratio > 1.5:
        ar_str = "16:9"
    elif aspect_ratio > 1.2:
        ar_str = "4:3"
    elif aspect_ratio > 0.9:
        ar_str = "1:1"
    elif aspect_ratio > 0.7:
        ar_str = "3:4"
    else:
        ar_str = "9:16"

    try:
        # コンテンツを構築（オーバーレイ画像がある場合は追加）
        contents = [prompt, input_image]
        if overlay_image:
            contents.append(overlay_image)

        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=ar_str, image_size="2K"),
            ),
        )

        edited_dir = workspace / "edited"
        edited_dir.mkdir(parents=True, exist_ok=True)

        for part in response.parts:
            if part.inline_data:
                result_image = types.Part.as_image(part)
                output_path = edited_dir / f"page_{page_number:03d}_edited.png"
                result_image.save(output_path)
                print(f"\n✅ 編集完了: {output_path}")

                page_data["edited_path"] = str(output_path)
                page_data["edit_history"] = page_data.get("edit_history", [])
                page_data["edit_history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "prompt": prompt,
                })

                with open(yaml_path, "w", encoding="utf-8") as f:
                    yaml.dump(analysis, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

                return True

        print("Error: No image data in response")
        return False

    except Exception as e:
        print(f"Error: 画像編集に失敗しました: {e}")
        return False


def cmd_rebuild(args):
    import img2pdf

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}")
        sys.exit(1)

    yaml_path = workspace / "analysis.yaml"
    if not yaml_path.exists():
        print(f"Error: Analysis file not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        analysis = yaml.safe_load(f)

    pages_dir = workspace / "pages"
    edited_dir = workspace / "edited"

    image_paths = []
    edited_count = 0

    for page_data in analysis["pages"]:
        page_num = page_data["page_number"]
        edited_path = edited_dir / f"page_{page_num:03d}_edited.png"
        original_path = pages_dir / f"page_{page_num:03d}.png"

        if edited_path.exists():
            image_paths.append(str(edited_path))
            edited_count += 1
        elif original_path.exists():
            image_paths.append(str(original_path))
        else:
            print(f"Warning: Page {page_num} image not found, skipping")

    if not image_paths:
        print("Error: No page images found")
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
    else:
        source_name = analysis["document"]["source"]
        output_path = workspace / f"{Path(source_name).stem}_edited.pdf"

    print(f"📄 PDFを再構成中...")
    print(f"   総ページ数: {len(image_paths)}")
    print(f"   編集済みページ: {edited_count}")
    print(f"   出力先: {output_path}")

    try:
        converted_paths = []
        temp_dir = workspace / "temp"
        temp_dir.mkdir(exist_ok=True)

        for i, img_path in enumerate(image_paths):
            img = Image.open(img_path)
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                img = background
            temp_path = temp_dir / f"temp_{i:03d}.png"
            img.save(temp_path, "PNG")
            converted_paths.append(str(temp_path))

        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(converted_paths))

        for temp_path in converted_paths:
            Path(temp_path).unlink()
        temp_dir.rmdir()

        print(f"\n✅ PDF生成完了: {output_path}")

        analysis["document"]["output_pdf"] = str(output_path)
        analysis["document"]["rebuilt_at"] = datetime.now().isoformat()

        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(analysis, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        return True

    except Exception as e:
        print(f"Error: PDF生成に失敗しました: {e}")
        return False


def cmd_show(args):
    workspace = Path(args.workspace)
    yaml_path = workspace / "analysis.yaml"

    if not yaml_path.exists():
        print(f"Error: Analysis file not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        analysis = yaml.safe_load(f)

    page_number = args.page
    total_pages = analysis["document"]["total_pages"]

    if page_number < 1 or page_number > total_pages:
        print(f"Error: Page number must be between 1 and {total_pages}")
        sys.exit(1)

    page_data = analysis["pages"][page_number - 1]

    print(f"\n📄 ページ {page_number} の詳細:")
    print(f"   レイアウト: {page_data.get('layout', 'unknown')}")
    print(f"   画像: {page_data.get('image_path', 'N/A')}")

    if page_data.get("edited_path"):
        print(f"   編集済み: {page_data['edited_path']}")

    print("\n📝 テキスト要素:")
    for i, elem in enumerate(page_data.get("elements", []), start=1):
        elem_type = elem.get("type", "unknown")
        content = elem.get("content", "")
        items = elem.get("items", [])

        if content:
            print(f"   {i}. [{elem_type}] {content[:80]}{'...' if len(content) > 80 else ''}")
        elif items:
            print(f"   {i}. [{elem_type}]")
            for item in items[:5]:
                print(f"      - {item[:60]}{'...' if len(item) > 60 else ''}")
            if len(items) > 5:
                print(f"      ... ({len(items) - 5} more items)")

    if page_data.get("diagrams"):
        print("\n📊 図・ダイアグラム:")
        for i, diag in enumerate(page_data["diagrams"], start=1):
            print(f"   {i}. [{diag.get('type', 'unknown')}] {diag.get('description', 'N/A')}")
            if diag.get("labels"):
                print(f"      ラベル: {', '.join(diag['labels'][:5])}")


def cmd_insert(args):
    """新しいページを指定位置に挿入"""
    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}")
        sys.exit(1)

    yaml_path = workspace / "analysis.yaml"
    if not yaml_path.exists():
        print(f"Error: Analysis file not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        analysis = yaml.safe_load(f)

    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    after_page = args.after_page
    total_pages = analysis["document"]["total_pages"]

    if after_page < 0 or after_page > total_pages:
        print(f"Error: after_page must be between 0 and {total_pages}")
        sys.exit(1)

    # 新しいページ番号（挿入位置の次）
    new_page_num = after_page + 1
    print(f"📄 ページ {new_page_num} として挿入中...")
    print(f"   画像: {image_path}")

    pages_dir = workspace / "pages"
    pages_dir.mkdir(exist_ok=True)

    # 挿入位置以降のページ番号を+1ずつリネーム（逆順で処理）
    for i in range(total_pages, after_page, -1):
        old_path = pages_dir / f"page_{i:03d}.png"
        new_path = pages_dir / f"page_{i+1:03d}.png"
        if old_path.exists():
            old_path.rename(new_path)
            print(f"   リネーム: page_{i:03d}.png → page_{i+1:03d}.png")

    # 編集済みフォルダも同様にリネーム
    edited_dir = workspace / "edited"
    if edited_dir.exists():
        for i in range(total_pages, after_page, -1):
            old_edited = edited_dir / f"page_{i:03d}_edited.png"
            new_edited = edited_dir / f"page_{i+1:03d}_edited.png"
            if old_edited.exists():
                old_edited.rename(new_edited)

    # 新しい画像をコピー
    new_image_path = pages_dir / f"page_{new_page_num:03d}.png"
    img = Image.open(image_path)
    img.save(new_image_path, "PNG")
    print(f"   保存: {new_image_path}")

    # analysis.yamlの更新
    # 既存ページのpage_numberを更新
    for page_data in analysis["pages"]:
        if page_data["page_number"] > after_page:
            old_num = page_data["page_number"]
            new_num = old_num + 1
            page_data["page_number"] = new_num
            page_data["image_path"] = str(pages_dir / f"page_{new_num:03d}.png")
            if page_data.get("edited_path"):
                page_data["edited_path"] = str(edited_dir / f"page_{new_num:03d}_edited.png")

    # 新しいページデータを作成
    new_page_data = {
        "page_number": new_page_num,
        "image_path": str(new_image_path),
        "layout": "content",
        "elements": [
            {
                "type": "title",
                "content": args.title if args.title else "新規ページ",
                "position": {"region": "top"}
            }
        ],
        "inserted_at": datetime.now().isoformat(),
    }

    # 正しい位置に挿入
    analysis["pages"].insert(after_page, new_page_data)
    analysis["document"]["total_pages"] = total_pages + 1

    # 保存
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(analysis, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\n✅ ページ挿入完了")
    print(f"   新しいページ番号: {new_page_num}")
    print(f"   総ページ数: {total_pages + 1}")

    return True


def cmd_overlay(args):
    """Pillowでロゴ/画像を直接合成（AIを使わない）"""
    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}")
        sys.exit(1)

    yaml_path = workspace / "analysis.yaml"
    if not yaml_path.exists():
        print(f"Error: Analysis file not found: {yaml_path}")
        sys.exit(1)

    with open(yaml_path, "r", encoding="utf-8") as f:
        analysis = yaml.safe_load(f)

    overlay_path = Path(args.image)
    if not overlay_path.exists():
        print(f"Error: Overlay image not found: {overlay_path}")
        sys.exit(1)

    # オーバーレイ画像を読み込み
    overlay_img = Image.open(overlay_path).convert("RGBA")
    
    # サイズ指定がある場合はリサイズ
    if args.width:
        aspect = overlay_img.height / overlay_img.width
        new_size = (args.width, int(args.width * aspect))
        overlay_img = overlay_img.resize(new_size, Image.Resampling.LANCZOS)
    
    # 対象ページを決定
    if args.pages:
        pages = [int(p) for p in args.pages.split(",")]
    else:
        pages = list(range(1, analysis["document"]["total_pages"] + 1))
    
    # 出力ディレクトリ
    edited_dir = workspace / "edited"
    edited_dir.mkdir(exist_ok=True)
    
    # マージン設定
    margin_x = args.margin_x if args.margin_x else 30
    margin_y = args.margin_y if args.margin_y else 20
    
    # 背景塗りつぶし設定
    clear_bg = args.clear_background
    clear_padding = args.clear_padding if args.clear_padding else 10
    
    for page_num in pages:
        if page_num < 1 or page_num > analysis["document"]["total_pages"]:
            print(f"⚠️ ページ {page_num} はスキップ（範囲外）")
            continue
        
        page_data = analysis["pages"][page_num - 1]
        
        # 編集済み画像があればそれを使用、なければ元画像
        if page_data.get("edited_path") and Path(page_data["edited_path"]).exists():
            base_path = Path(page_data["edited_path"])
        else:
            base_path = Path(page_data["image_path"])
        
        if not base_path.exists():
            print(f"⚠️ ページ {page_num} の画像が見つかりません: {base_path}")
            continue
        
        # ベース画像を読み込み
        base_img = Image.open(base_path).convert("RGBA")
        
        # 位置を計算（デフォルト: 右下）
        position = args.position if args.position else "bottom-right"
        
        if position == "bottom-right":
            x = base_img.width - overlay_img.width - margin_x
            y = base_img.height - overlay_img.height - margin_y
        elif position == "bottom-left":
            x = margin_x
            y = base_img.height - overlay_img.height - margin_y
        elif position == "top-right":
            x = base_img.width - overlay_img.width - margin_x
            y = margin_y
        elif position == "top-left":
            x = margin_x
            y = margin_y
        elif position == "center":
            x = (base_img.width - overlay_img.width) // 2
            y = (base_img.height - overlay_img.height) // 2
        else:
            # カスタム位置 "x,y" 形式
            try:
                x, y = map(int, position.split(","))
            except ValueError:
                print(f"Error: Invalid position format: {position}")
                sys.exit(1)
        
        # 合成
        result = base_img.copy()
        
        # 背景塗りつぶし（元のロゴを覆い隠す）
        if clear_bg:
            from PIL import ImageDraw
            draw = ImageDraw.Draw(result)
            clear_x1 = x - clear_padding
            clear_y1 = y - clear_padding
            clear_x2 = x + overlay_img.width + clear_padding
            clear_y2 = y + overlay_img.height + clear_padding
            # 背景色を取得（右下の角から少し内側のピクセル）
            try:
                bg_color = base_img.getpixel((base_img.width - 5, base_img.height - 5))[:3]
            except:
                bg_color = (255, 255, 255)  # フォールバック: 白
            draw.rectangle([clear_x1, clear_y1, clear_x2, clear_y2], fill=bg_color + (255,))
        
        result.paste(overlay_img, (x, y), overlay_img)
        
        # RGB変換して保存
        output_path = edited_dir / f"page_{page_num:03d}_edited.png"
        result.convert("RGB").save(output_path, "PNG")
        
        # analysis.yamlを更新
        analysis["pages"][page_num - 1]["edited_path"] = str(output_path)
        
        print(f"✅ ページ {page_num}: {output_path}")
    
    # analysis.yamlを保存
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(analysis, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"\n🎉 {len(pages)} ページにロゴを合成しました")


def cmd_compress(args):
    """PDFを圧縮してファイルサイズを削減"""
    import img2pdf
    from pdf2image import convert_from_path
    import tempfile

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    # 出力パスを決定
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = pdf_path.parent / f"{pdf_path.stem}_compressed.pdf"

    orig_size = pdf_path.stat().st_size / 1024 / 1024
    print(f"📄 PDF圧縮処理を開始...")
    print(f"   入力: {pdf_path.name}")
    print(f"   元のサイズ: {orig_size:.2f} MB")

    # 設定
    target_width = args.width if args.width else 1920
    quality = args.quality if args.quality else 85
    dpi = args.dpi if args.dpi else 150

    # PDFをページ画像に変換
    print(f"\n🔄 PDFをページ画像に変換中 (DPI: {dpi})...")
    images = convert_from_path(pdf_path, dpi=dpi)
    print(f"   {len(images)} ページを変換しました")

    # 一時ディレクトリで画像を処理
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        image_paths = []

        print(f"\n🗜️ 画像を圧縮中 (幅: {target_width}px, 品質: {quality}%)...")
        for i, img in enumerate(images, 1):
            # アスペクト比を維持してリサイズ
            aspect = img.height / img.width
            target_height = int(target_width * aspect)

            # リサイズ
            img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

            # RGB変換（透過を白背景に）
            if img_resized.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img_resized.size, (255, 255, 255))
                if img_resized.mode == "P":
                    img_resized = img_resized.convert("RGBA")
                if img_resized.mode == "RGBA":
                    background.paste(img_resized, mask=img_resized.split()[-1])
                img_resized = background

            # JPEG形式で保存
            temp_path = temp_dir / f"page_{i:03d}.jpg"
            img_resized.save(temp_path, "JPEG", quality=quality, optimize=True)
            image_paths.append(str(temp_path))

            if i == 1:
                print(f"   リサイズ: {img.width}x{img.height} → {target_width}x{target_height}")

        # PDFに再構成
        print("\n📄 PDFを再構成中...")
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))

    # 結果を表示
    new_size = output_path.stat().st_size / 1024 / 1024
    reduction = (1 - new_size / orig_size) * 100

    print(f"\n✅ 完了: {output_path}")
    print(f"\n📊 結果:")
    print(f"   元のサイズ: {orig_size:.2f} MB")
    print(f"   圧縮後: {new_size:.2f} MB")
    print(f"   削減率: {reduction:.1f}%")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="PDF Page Editor - PDFのテキスト編集ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python pdf_page_editor.py analyze document.pdf
  python pdf_page_editor.py edit document_workspace 3 --replace "旧テキスト" "新テキスト"
  python pdf_page_editor.py edit document_workspace 5 --delete "削除するテキスト"
  python pdf_page_editor.py edit document_workspace 7 --prompt "右上のロゴを削除"
  python pdf_page_editor.py rebuild document_workspace
  python pdf_page_editor.py compress large_document.pdf --width 1920 --quality 85
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="利用可能なコマンド")

    analyze_parser = subparsers.add_parser("analyze", help="PDFを解析")
    analyze_parser.add_argument("pdf", help="解析するPDFファイルのパス")
    analyze_parser.add_argument("--dpi", type=int, default=150, help="ページ画像のDPI (default: 150)")

    edit_parser = subparsers.add_parser("edit", help="ページを編集")
    edit_parser.add_argument("workspace", help="ワークスペースディレクトリのパス")
    edit_parser.add_argument("page", type=int, help="編集するページ番号")
    edit_group = edit_parser.add_mutually_exclusive_group(required=True)
    edit_group.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"), help="テキストを置換")
    edit_group.add_argument("--delete", metavar="TEXT", help="テキストを削除")
    edit_group.add_argument("--prompt", metavar="INSTRUCTION", help="自由記述の編集指示")
    edit_parser.add_argument("--overlay", metavar="IMAGE_PATH", help="埋め込むロゴ/画像のパス（プロンプトと併用可）")

    rebuild_parser = subparsers.add_parser("rebuild", help="PDFを再構成")
    rebuild_parser.add_argument("workspace", help="ワークスペースディレクトリのパス")
    rebuild_parser.add_argument("--output", "-o", help="出力PDFのパス")

    show_parser = subparsers.add_parser("show", help="ページの詳細を表示")
    show_parser.add_argument("workspace", help="ワークスペースディレクトリのパス")
    show_parser.add_argument("page", type=int, help="表示するページ番号")

    overlay_parser = subparsers.add_parser("overlay", help="ロゴ/画像を直接合成（Pillow使用）")
    overlay_parser.add_argument("workspace", help="ワークスペースディレクトリのパス")
    overlay_parser.add_argument("image", help="合成する画像のパス")
    overlay_parser.add_argument("--pages", help="対象ページ（カンマ区切り、例: 1,2,3）。省略時は全ページ")
    overlay_parser.add_argument("--width", type=int, help="ロゴの幅（ピクセル）。省略時は元のサイズ")
    overlay_parser.add_argument("--position", default="bottom-right", 
                               help="位置: bottom-right, bottom-left, top-right, top-left, center, または x,y")
    overlay_parser.add_argument("--margin-x", type=int, default=30, help="X方向マージン (default: 30)")
    overlay_parser.add_argument("--margin-y", type=int, default=20, help="Y方向マージン (default: 20)")
    overlay_parser.add_argument("--clear-background", action="store_true", help="ロゴ配置前に背景を塗りつぶす（元のロゴを覆い隠す）")
    overlay_parser.add_argument("--clear-padding", type=int, default=10, help="塗りつぶし領域のパディング (default: 10)")

    insert_parser = subparsers.add_parser("insert", help="新しいページを指定位置に挿入")
    insert_parser.add_argument("workspace", help="ワークスペースディレクトリのパス")
    insert_parser.add_argument("--after-page", type=int, required=True, help="この番号の後に挿入（0で先頭）")
    insert_parser.add_argument("--image", required=True, help="挿入する画像のパス")
    insert_parser.add_argument("--title", help="ページのタイトル（オプション）")

    compress_parser = subparsers.add_parser("compress", help="PDFを圧縮してファイルサイズを削減")
    compress_parser.add_argument("pdf", help="圧縮するPDFファイルのパス")
    compress_parser.add_argument("--output", "-o", help="出力PDFのパス（省略時: {元ファイル名}_compressed.pdf）")
    compress_parser.add_argument("--width", type=int, default=1920, help="ページ幅（ピクセル）(default: 1920)")
    compress_parser.add_argument("--quality", type=int, default=85, help="JPEG品質 1-100 (default: 85)")
    compress_parser.add_argument("--dpi", type=int, default=150, help="変換時のDPI (default: 150)")

    args = parser.parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "edit":
        cmd_edit(args)
    elif args.command == "rebuild":
        cmd_rebuild(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "overlay":
        cmd_overlay(args)
    elif args.command == "insert":
        cmd_insert(args)
    elif args.command == "compress":
        cmd_compress(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
