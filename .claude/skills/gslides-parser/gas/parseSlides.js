/**
 * Google Slides パーサー — プレゼンテーション構造をJSON出力
 *
 * SlidesApp でプレゼンテーションの全要素を解析し、
 * pptx-converter 互換の構造化データを返す。
 *
 * clasp run parsePresentation --params '["PRESENTATION_ID"]'
 */

// ─── メインエントリーポイント ──────────────────────────────

/**
 * プレゼンテーション全体をパースしてJSON構造を返す
 * @param {string} presentationId - Google Slides のプレゼンテーションID
 * @returns {Object} パース結果
 */
function parsePresentation(presentationId) {
  var pres = SlidesApp.openById(presentationId);
  var slides = pres.getSlides();

  var result = {
    source: "Google Slides: " + pres.getName(),
    presentation_id: presentationId,
    presentation_url: "https://docs.google.com/presentation/d/" + presentationId + "/edit",
    slide_width_pt: pres.getPageWidth(),
    slide_height_pt: pres.getPageHeight(),
    generated_at: new Date().toISOString(),
    slides: []
  };

  for (var i = 0; i < slides.length; i++) {
    result.slides.push(parseSlide_(slides[i], i + 1));
  }

  return result;
}

/**
 * パース結果をログに出力（デバッグ用）
 * @param {string} presentationId
 */
function parsePresentationLog(presentationId) {
  var result = parsePresentation(presentationId);
  Logger.log(JSON.stringify(result, null, 2));
  return result;
}

// ─── スライドパース ────────────────────────────────────────

/**
 * 1スライドの全要素をパース
 * @param {Slide} slide
 * @param {number} slideNumber (1-based)
 * @returns {Object}
 */
function parseSlide_(slide, slideNumber) {
  var layoutName = "";
  try {
    layoutName = slide.getLayout().getLayoutName();
  } catch (e) {
    layoutName = "Unknown";
  }

  var slideData = {
    slide_number: slideNumber,
    object_id: slide.getObjectId(),
    layout: layoutName,
    elements: []
  };

  var elements = slide.getPageElements();
  for (var i = 0; i < elements.length; i++) {
    try {
      var parsed = parseElement_(elements[i]);
      if (parsed) {
        slideData.elements.push(parsed);
      }
    } catch (e) {
      slideData.elements.push({
        id: elements[i].getObjectId(),
        type: "error",
        error: e.toString()
      });
    }
  }

  return slideData;
}

// ─── 要素パース（ディスパッチ） ────────────────────────────

/**
 * ページ要素を種類に応じてパース
 * @param {PageElement} elem
 * @returns {Object}
 */
function parseElement_(elem) {
  var type = elem.getPageElementType();

  var base = {
    id: elem.getObjectId(),
    position: getPosition_(elem)
  };

  try {
    base.title = elem.getTitle() || "";
    base.description = elem.getDescription() || "";
  } catch (e) {
    // title/description が取得できない要素もある
  }

  if (type === SlidesApp.PageElementType.SHAPE) {
    return parseShape_(elem.asShape(), base);
  }
  if (type === SlidesApp.PageElementType.IMAGE) {
    return parseImage_(elem.asImage(), base);
  }
  if (type === SlidesApp.PageElementType.TABLE) {
    return parseTable_(elem.asTable(), base);
  }
  if (type === SlidesApp.PageElementType.GROUP) {
    return parseGroup_(elem.asGroup(), base);
  }
  if (type === SlidesApp.PageElementType.SHEETS_CHART) {
    return parseSheetsChart_(elem.asSheetsChart(), base);
  }
  if (type === SlidesApp.PageElementType.LINE) {
    return parseLine_(elem.asLine(), base);
  }
  if (type === SlidesApp.PageElementType.WORD_ART) {
    return parseWordArt_(elem.asWordArt(), base);
  }
  if (type === SlidesApp.PageElementType.VIDEO) {
    return parseVideo_(elem.asVideo(), base);
  }

  // 不明な要素
  base.type = "other";
  base.element_type = type.toString();
  return base;
}

// ─── 位置情報取得 ──────────────────────────────────────────

/**
 * 要素の位置・サイズをポイント単位で取得
 * @param {PageElement} elem
 * @returns {Object}
 */
function getPosition_(elem) {
  var pos = {
    left: 0,
    top: 0,
    width: 0,
    height: 0,
    rotation: 0
  };

  try {
    var transform = elem.getTransform();
    pos.left = Math.round(transform.getTranslateX() * 100) / 100;
    pos.top = Math.round(transform.getTranslateY() * 100) / 100;
  } catch (e) {}

  try {
    pos.width = Math.round(elem.getWidth() * 100) / 100;
    pos.height = Math.round(elem.getHeight() * 100) / 100;
  } catch (e) {}

  try {
    pos.rotation = elem.getRotation() || 0;
  } catch (e) {}

  return pos;
}

// ─── Shape パース ──────────────────────────────────────────

/**
 * Shape 要素をパース（テキストボックス、矩形、楕円等）
 * @param {Shape} shape
 * @param {Object} base
 * @returns {Object}
 */
function parseShape_(shape, base) {
  base.type = "shape";

  try {
    base.shape_type = shape.getShapeType().toString();
  } catch (e) {
    base.shape_type = "UNKNOWN";
  }

  // プレースホルダー判定
  try {
    var phType = shape.getPlaceholderType();
    if (phType && phType !== SlidesApp.PlaceholderType.NONE) {
      base.is_placeholder = true;
      base.placeholder_type = phType.toString();
    }
  } catch (e) {}

  // テキスト抽出
  try {
    var textRange = shape.getText();
    if (textRange) {
      var text = textRange.asString();
      // 末尾の改行を除去
      if (text && text.endsWith("\n")) {
        text = text.substring(0, text.length - 1);
      }
      base.value = text;
      base.has_text = true;

      // テキストスタイル（最初のランから）
      base.style = extractTextStyle_(textRange);

      // 段落情報
      var paragraphs = textRange.getParagraphs();
      base.paragraph_count = paragraphs.length;
    }
  } catch (e) {
    base.has_text = false;
  }

  // 塗りつぶし色
  try {
    var fill = shape.getFill();
    if (fill.getType() === SlidesApp.FillType.SOLID) {
      base.fill_color = rgbToHex_(fill.getSolidFill().getColor().asRgbColor());
    }
  } catch (e) {}

  // 枠線
  try {
    var border = shape.getBorder();
    if (border && border.getWeight() > 0) {
      base.border = {
        weight: border.getWeight(),
        color: rgbToHex_(border.getLineFill().getSolidFill().getColor().asRgbColor())
      };
    }
  } catch (e) {}

  // テキストがある shape は "text" タイプとして扱う
  if (base.has_text && base.value && base.value.trim()) {
    base.type = "text";
  }

  return base;
}

// ─── Image パース ──────────────────────────────────────────

/**
 * Image 要素をパース
 * @param {Image} image
 * @param {Object} base
 * @returns {Object}
 */
function parseImage_(image, base) {
  base.type = "image";

  try {
    base.image_info = {
      content_type: image.getContentUrl() ? "url" : "embedded",
      source_url: image.getSourceUrl() || "",
      content_url: image.getContentUrl() || ""
    };
  } catch (e) {
    base.image_info = { error: e.toString() };
  }

  // リンク
  try {
    var link = image.getLink();
    if (link) {
      base.link_url = link.getUrl();
    }
  } catch (e) {}

  return base;
}

// ─── Table パース ──────────────────────────────────────────

/**
 * Table 要素をパース
 * @param {Table} table
 * @param {Object} base
 * @returns {Object}
 */
function parseTable_(table, base) {
  base.type = "table";

  var numRows = table.getNumRows();
  var numCols = table.getNumColumns();

  base.table_config = {
    rows: numRows,
    cols: numCols
  };

  // 全セルのテキストを抽出
  var value = [];
  for (var r = 0; r < numRows; r++) {
    var row = [];
    for (var c = 0; c < numCols; c++) {
      try {
        var cell = table.getCell(r, c);
        var cellText = cell.getText().asString();
        // 末尾改行除去
        if (cellText && cellText.endsWith("\n")) {
          cellText = cellText.substring(0, cellText.length - 1);
        }
        row.push(cellText);
      } catch (e) {
        row.push("");
      }
    }
    value.push(row);
  }
  base.value = value;

  // ヘッダー行検出（1行目のスタイルが太字か）
  try {
    if (numRows > 1) {
      var headerCell = table.getCell(0, 0);
      var headerStyle = headerCell.getText().getTextStyle();
      base.table_config.header_row = headerStyle.isBold() || false;
    }
  } catch (e) {}

  // セルスタイル（ヘッダー/ボディ）
  try {
    if (numRows > 0 && numCols > 0) {
      base.cell_styles = {
        header: extractCellStyle_(table.getCell(0, 0)),
        body: numRows > 1 ? extractCellStyle_(table.getCell(1, 0)) : {}
      };
    }
  } catch (e) {}

  return base;
}

/**
 * テーブルセルのスタイルを抽出
 * @param {TableCell} cell
 * @returns {Object}
 */
function extractCellStyle_(cell) {
  var style = {};
  try {
    var ts = cell.getText().getTextStyle();
    style.font = ts.getFontFamily() || "";
    style.size = ts.getFontSize() || 0;
    style.bold = ts.isBold() || false;
    style.color = "";
    try {
      var fg = ts.getForegroundColor();
      if (fg) style.color = rgbToHex_(fg.asRgbColor());
    } catch (e) {}
  } catch (e) {}

  try {
    var fill = cell.getFill();
    if (fill.getType() === SlidesApp.FillType.SOLID) {
      style.fill = rgbToHex_(fill.getSolidFill().getColor().asRgbColor());
    }
  } catch (e) {}

  return style;
}

// ─── Group パース ──────────────────────────────────────────

/**
 * Group 要素をパース（子要素を再帰的に処理）
 * @param {Group} group
 * @param {Object} base
 * @returns {Object}
 */
function parseGroup_(group, base) {
  base.type = "group";
  base.children = [];

  try {
    var children = group.getChildren();
    for (var i = 0; i < children.length; i++) {
      var child = parseElement_(children[i]);
      if (child) {
        base.children.push(child);
      }
    }
  } catch (e) {
    base._warning = "グループ子要素の抽出に失敗: " + e.toString();
  }

  return base;
}

// ─── SheetsChart パース ────────────────────────────────────

/**
 * Sheets連携チャートをパース
 * @param {SheetsChart} chart
 * @param {Object} base
 * @returns {Object}
 */
function parseSheetsChart_(chart, base) {
  base.type = "chart";

  try {
    base.chart_info = {
      spreadsheet_id: chart.getSpreadsheetId() || "",
      chart_id: chart.getChartId() || 0,
      embed_type: chart.getEmbedType().toString()
    };
  } catch (e) {
    base.chart_info = { error: e.toString() };
  }

  return base;
}

// ─── Line パース ───────────────────────────────────────────

/**
 * Line 要素をパース
 * @param {Line} line
 * @param {Object} base
 * @returns {Object}
 */
function parseLine_(line, base) {
  base.type = "line";

  try {
    base.line_type = line.getLineType().toString();
  } catch (e) {}

  try {
    base.line_style = {
      weight: line.getWeight() || 0
    };
    var lineFill = line.getLineFill();
    if (lineFill.getFillType() === SlidesApp.LineFillType.SOLID) {
      base.line_style.color = rgbToHex_(lineFill.getSolidFill().getColor().asRgbColor());
    }
  } catch (e) {}

  return base;
}

// ─── WordArt パース ────────────────────────────────────────

/**
 * WordArt 要素をパース
 * @param {WordArt} wordArt
 * @param {Object} base
 * @returns {Object}
 */
function parseWordArt_(wordArt, base) {
  base.type = "wordart";

  try {
    base.value = wordArt.getRenderedText() || "";
  } catch (e) {}

  return base;
}

// ─── Video パース ──────────────────────────────────────────

/**
 * Video 要素をパース
 * @param {Video} video
 * @param {Object} base
 * @returns {Object}
 */
function parseVideo_(video, base) {
  base.type = "video";

  try {
    base.video_info = {
      source: video.getSource().toString(),
      url: video.getUrl() || "",
      video_id: video.getVideoId() || ""
    };
  } catch (e) {
    base.video_info = { error: e.toString() };
  }

  return base;
}

// ─── テキストスタイル抽出 ──────────────────────────────────

/**
 * TextRange から最初のランのスタイルを抽出
 * @param {TextRange} textRange
 * @returns {Object}
 */
function extractTextStyle_(textRange) {
  var style = {
    font: "",
    size: 0,
    bold: false,
    italic: false,
    color: "",
    align: ""
  };

  try {
    var runs = textRange.getRuns();
    if (runs.length > 0) {
      var ts = runs[0].getTextStyle();
      style.font = ts.getFontFamily() || "";
      style.size = ts.getFontSize() || 0;
      style.bold = ts.isBold() || false;
      style.italic = ts.isItalic() || false;

      try {
        var fg = ts.getForegroundColor();
        if (fg) {
          style.color = rgbToHex_(fg.asRgbColor());
        }
      } catch (e) {}
    }
  } catch (e) {}

  // 段落アライメント
  try {
    var paragraphs = textRange.getParagraphs();
    if (paragraphs.length > 0) {
      var pStyle = paragraphs[0].getRange().getParagraphStyle();
      var alignment = pStyle.getParagraphAlignment();
      if (alignment) {
        var alignMap = {};
        alignMap[SlidesApp.ParagraphAlignment.START] = "left";
        alignMap[SlidesApp.ParagraphAlignment.CENTER] = "center";
        alignMap[SlidesApp.ParagraphAlignment.END] = "right";
        alignMap[SlidesApp.ParagraphAlignment.JUSTIFIED] = "justify";
        style.align = alignMap[alignment] || alignment.toString();
      }
    }
  } catch (e) {}

  return style;
}

// ─── ユーティリティ ────────────────────────────────────────

/**
 * RgbColor を "#RRGGBB" 形式に変換
 * @param {RgbColor} rgb
 * @returns {string}
 */
function rgbToHex_(rgb) {
  try {
    var r = Math.round(rgb.getRed() * 255);
    var g = Math.round(rgb.getGreen() * 255);
    var b = Math.round(rgb.getBlue() * 255);
    return "#" + ((r << 16) | (g << 8) | b).toString(16).padStart(6, "0").toUpperCase();
  } catch (e) {
    return "#000000";
  }
}
