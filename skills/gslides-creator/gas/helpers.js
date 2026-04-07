/**
 * helpers.js — gslides-creator 共通ヘルパー関数
 *
 * convertSlides.js / buildSlides.js / deckSlides.js で共有する
 * テキストスタイル適用、レイアウト取得、色変換などのユーティリティ。
 */

// ─── テキストスタイル適用 ──────────────────────────────────────

/**
 * TextRange にスタイルを適用
 * @param {TextRange} textRange
 * @param {Object} style - { font, size, bold, italic, color, align }
 */
function applyTextStyle_(textRange, style) {
  if (!textRange || !style) return;

  try {
    var ts = textRange.getTextStyle();
    if (style.font) ts.setFontFamily(style.font);
    if (style.size) ts.setFontSize(style.size);
    if (style.bold !== undefined) ts.setBold(style.bold);
    if (style.italic !== undefined) ts.setItalic(style.italic);
    if (style.color) {
      ts.setForegroundColor(style.color);
    }
  } catch (e) {
    // スタイル適用エラーは無視
  }

  // 段落アライメント
  if (style.align) {
    try {
      var alignMap = {
        "left": SlidesApp.ParagraphAlignment.START,
        "center": SlidesApp.ParagraphAlignment.CENTER,
        "right": SlidesApp.ParagraphAlignment.END,
        "justify": SlidesApp.ParagraphAlignment.JUSTIFIED
      };
      var paragraphs = textRange.getParagraphs();
      for (var i = 0; i < paragraphs.length; i++) {
        paragraphs[i].getRange().getParagraphStyle()
          .setParagraphAlignment(alignMap[style.align] || SlidesApp.ParagraphAlignment.START);
      }
    } catch (e) {}
  }
}

// ─── レイアウト取得 ───────────────────────────────────────────

/**
 * プレゼンテーションからレイアウトを名前で取得
 * @param {Presentation} pres
 * @param {string} layoutName - レイアウト名
 * @returns {Layout}
 */
function getLayout_(pres, layoutName) {
  var layouts = pres.getLayouts();

  // 完全一致
  for (var i = 0; i < layouts.length; i++) {
    if (layouts[i].getLayoutName() === layoutName) {
      return layouts[i];
    }
  }

  // 部分一致
  var upper = layoutName.toUpperCase();
  for (var i = 0; i < layouts.length; i++) {
    if (layouts[i].getLayoutName().toUpperCase().indexOf(upper) >= 0) {
      return layouts[i];
    }
  }

  // フォールバック: BLANK
  for (var i = 0; i < layouts.length; i++) {
    if (layouts[i].getLayoutName().toUpperCase() === "BLANK") {
      return layouts[i];
    }
  }

  return layouts[0];
}

// ─── 要素挿入 ─────────────────────────────────────────────────

/**
 * スライドにテキストボックスを挿入
 * @param {Slide} slide
 * @param {Object} spec - { value, position: {left, top, width, height}, style }
 * @returns {Shape}
 */
function insertTextBox_(slide, spec) {
  var pos = spec.position || {};
  var shape = slide.insertTextBox(
    spec.value || "",
    pos.left || 50,
    pos.top || 50,
    pos.width || 600,
    pos.height || 50
  );

  if (spec.style) {
    applyTextStyle_(shape.getText(), spec.style);
  }

  return shape;
}

/**
 * スライドにシェイプを挿入
 * @param {Slide} slide
 * @param {Object} spec - { shape_type, value, position, style, fill_color }
 * @returns {Shape}
 */
function insertShape_(slide, spec) {
  var pos = spec.position || {};
  var shapeType = SlidesApp.ShapeType[spec.shape_type || "RECTANGLE"]
    || SlidesApp.ShapeType.RECTANGLE;

  var shape = slide.insertShape(
    shapeType,
    pos.left || 50,
    pos.top || 50,
    pos.width || 200,
    pos.height || 100
  );

  if (spec.fill_color) {
    try {
      shape.getFill().setSolidFill(spec.fill_color);
    } catch (e) {}
  }

  if (spec.value) {
    shape.getText().setText(spec.value);
    if (spec.style) {
      applyTextStyle_(shape.getText(), spec.style);
    }
  }

  return shape;
}

/**
 * スライドにテーブルを挿入
 * @param {Slide} slide
 * @param {Object} spec - { value: [[row]], position, header_style, body_style }
 * @returns {Table}
 */
function insertTable_(slide, spec) {
  var data = spec.value || [];
  if (data.length === 0) return null;

  var rows = data.length;
  var cols = data[0].length;
  var pos = spec.position || {};

  var table = slide.insertTable(
    rows, cols,
    pos.left || 50,
    pos.top || 150,
    pos.width || 620,
    pos.height || Math.min(rows * 30, 300)
  );

  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      if (r < data.length && c < data[r].length) {
        try {
          table.getCell(r, c).getText().setText(String(data[r][c]));

          // ヘッダー行にスタイル適用
          if (r === 0 && spec.header_style) {
            applyTextStyle_(table.getCell(r, c).getText(), spec.header_style);
          }
        } catch (e) {}
      }
    }
  }

  return table;
}

// ─── 色変換 ───────────────────────────────────────────────────

/**
 * HEX カラーコード "#RRGGBB" を検証
 * @param {string} hex
 * @returns {boolean}
 */
function isValidHexColor_(hex) {
  if (!hex) return false;
  return /^#?[0-9A-Fa-f]{6}$/.test(hex);
}

/**
 * HEX を "#RRGGBB" 形式に正規化
 * @param {string} hex
 * @returns {string}
 */
function normalizeHexColor_(hex) {
  if (!hex) return "#000000";
  hex = hex.replace(/^#/, "");
  if (hex.length === 3) {
    hex = hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2];
  }
  if (!/^[0-9A-Fa-f]{6}$/.test(hex)) return "#000000";
  return "#" + hex.toUpperCase();
}
