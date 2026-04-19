#!/usr/bin/env python3
"""
export_to_images.py — PPTX → PNG 画像エクスポート

LibreOffice headless で高品質変換。未インストール時は python-pptx + Pillow フォールバック。

Usage:
  python export_to_images.py input.pptx -o output_dir/
  python export_to_images.py input.pptx --dpi 150
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _find_libreoffice():
    """LibreOffice の実行パスを探す"""
    cmd = shutil.which("libreoffice") or shutil.which("soffice")
    if cmd:
        return cmd
    # Windows のデフォルトインストールパスを確認
    if platform.system() == "Windows":
        for candidate in [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ]:
            if Path(candidate).exists():
                return candidate
    return None


def export_libreoffice(pptx_path, output_dir, dpi=150):
    """LibreOffice headless で PPTX → PNG 変換"""
    pptx_path = Path(pptx_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    libreoffice_cmd = _find_libreoffice()
    if not libreoffice_cmd:
        raise RuntimeError(
            "LibreOffice not found. Please install it and add to PATH.\n"
            "  Linux: sudo apt install libreoffice\n"
            "  macOS: brew install --cask libreoffice\n"
            "  Windows: https://www.libreoffice.org/download/"
        )

    # LibreOffice で PDF に変換してから各ページをPNG化
    with tempfile.TemporaryDirectory() as tmpdir:
        # Step 1: PPTX → PDF
        cmd = [
            libreoffice_cmd, "--headless", "--convert-to", "pdf",
            "--outdir", tmpdir,
            str(pptx_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")

        pdf_name = pptx_path.stem + ".pdf"
        pdf_path = Path(tmpdir) / pdf_name

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not generated: {pdf_path}")

        # Step 2: PDF → PNG (using pdftoppm or Pillow)
        images = _pdf_to_png(pdf_path, output_dir, dpi)

    return images


def _pdf_to_png(pdf_path, output_dir, dpi=150):
    """PDF → PNG 変換 (pdftoppm or Pillow)"""
    images = []

    # Try pdftoppm first (poppler-utils)
    if shutil.which("pdftoppm"):
        prefix = str(output_dir / "slide")
        cmd = [
            "pdftoppm", "-png", "-r", str(dpi),
            str(pdf_path), prefix,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            for f in sorted(output_dir.glob("slide-*.png")):
                images.append(f)
            return images

    # Fallback: Pillow + pdf2image
    try:
        from pdf2image import convert_from_path
        pil_images = convert_from_path(str(pdf_path), dpi=dpi)
        for i, img in enumerate(pil_images):
            out_path = output_dir / f"slide-{i+1:03d}.png"
            img.save(str(out_path), "PNG")
            images.append(out_path)
        return images
    except ImportError:
        pass

    raise RuntimeError("PNG変換に必要なツールが見つかりません。"
                       "libreoffice, pdftoppm, または pdf2image をインストールしてください。")


def export_pptx_to_images(pptx_path, output_dir=None, dpi=150):
    """メインエクスポート関数"""
    pptx_path = Path(pptx_path)
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    if output_dir is None:
        output_dir = pptx_path.parent / f"{pptx_path.stem}_images"

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[export] Exporting: {pptx_path}")
    print(f"[export] Output dir: {output_dir}")
    print(f"[export] DPI: {dpi}")

    images = export_libreoffice(pptx_path, output_dir, dpi)

    print(f"[export] Generated {len(images)} images:")
    for img in images:
        print(f"  {img}")

    return images


def main():
    parser = argparse.ArgumentParser(description="PPTX → PNG 画像エクスポート")
    parser.add_argument("pptx", type=str, help="入力PPTXファイルパス")
    parser.add_argument("--output", "-o", type=str, default=None, help="出力ディレクトリ")
    parser.add_argument("--dpi", type=int, default=150, help="出力解像度 (default: 150)")
    args = parser.parse_args()

    try:
        images = export_pptx_to_images(args.pptx, args.output, args.dpi)
        print(f"\n完了: {len(images)} 枚の画像を生成しました")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
