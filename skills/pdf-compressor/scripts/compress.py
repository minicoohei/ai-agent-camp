#!/usr/bin/env python3
"""
PDF Compressor - PDFファイルを圧縮してファイルサイズを削減
"""

import argparse
import sys
import tempfile
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image
import img2pdf

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.utils.path_validator import validate_path

def compress_pdf(
    pdf_path: Path,
    output_path: Path,
    width: int = 1920,
    quality: int = 85,
    dpi: int = 150,
) -> bool:
    """PDFを圧縮する"""
    
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return False

    orig_size = pdf_path.stat().st_size / 1024 / 1024
    print(f"📄 PDF圧縮処理を開始...")
    print(f"   入力: {pdf_path.name}")
    print(f"   元のサイズ: {orig_size:.2f} MB")

    # PDFをページ画像に変換
    print(f"\n🔄 PDFをページ画像に変換中 (DPI: {dpi})...")
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
    except Exception as e:
        print(f"Error: PDF変換に失敗しました: {e}")
        return False
    
    print(f"   {len(images)} ページを変換しました")

    # 一時ディレクトリで画像を処理
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        image_paths = []

        print(f"\n🗜️ 画像を圧縮中 (幅: {width}px, 品質: {quality}%)...")
        for i, img in enumerate(images, 1):
            # アスペクト比を維持してリサイズ
            aspect = img.height / img.width
            target_height = int(width * aspect)

            # リサイズ
            img_resized = img.resize((width, target_height), Image.Resampling.LANCZOS)

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
                print(f"   リサイズ: {img.width}x{img.height} → {width}x{target_height}")

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
        description="PDF Compressor - PDFファイルを圧縮してファイルサイズを削減",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python compress.py large_document.pdf
  python compress.py slides.pdf --width 1280 --quality 75
  python compress.py report.pdf -o report_small.pdf
""",
    )

    parser.add_argument("pdf", help="圧縮するPDFファイルのパス")
    parser.add_argument(
        "--output", "-o",
        help="出力PDFのパス（省略時: {元ファイル名}_compressed.pdf）"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1920,
        help="ページ幅（ピクセル）(default: 1920)"
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=85,
        help="JPEG品質 1-100 (default: 85)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=150,
        help="変換時のDPI (default: 150)"
    )

    args = parser.parse_args()

    pdf_path = validate_path(args.pdf, must_exist=True, must_be_file=True)
    
    if args.output:
        output_path = validate_path(args.output, must_exist=False)
    else:
        output_path = validate_path(pdf_path.parent / f"{pdf_path.stem}_compressed.pdf", must_exist=False)

    success = compress_pdf(
        pdf_path=pdf_path,
        output_path=output_path,
        width=args.width,
        quality=args.quality,
        dpi=args.dpi,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
