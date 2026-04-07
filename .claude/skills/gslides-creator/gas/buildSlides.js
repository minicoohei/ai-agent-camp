/**
 * buildSlides.js — テンプレートコピー＋要素単位の詳細書き換え
 *
 * テンプレートをコピーし、スライド/要素単位で
 * テキスト・スタイル・位置を詳細に書き換える。
 * マッピング YAML + データに基づく精密制御用。
 *
 * clasp run buildPresentation --params '[
 *   "TEMPLATE_ID",
 *   "新しいタイトル",
 *   [{"slide_number":1, "elements":[{"id":"g123","value":"新テキスト"}]}]
 * ]'
 */

/**
 * テンプレートをコピーして要素単位で書き換え
 * @param {string} templateId - テンプレートのプレゼンテーションID
 * @param {string} newTitle - 新しいプレゼンテーション名
 * @param {Array} slideUpdates - [{slide_number, elements: [{id, value, style, position}]}]
 * @returns {Object} 結果
 */
function buildPresentation(templateId, newTitle, slideUpdates) {
  // 1. テンプレートをコピー
  var templateFile = DriveApp.getFileById(templateId);
  var copy = templateFile.makeCopy(newTitle || "Built: " + templateFile.getName());
  var newId = copy.getId();

  // 2. コピーを開く
  var pres = SlidesApp.openById(newId);
  var slides = pres.getSlides();

  var updateLog = [];

  // 3. スライドごとに更新
  if (slideUpdates) {
    for (var i = 0; i < slideUpdates.length; i++) {
      var update = slideUpdates[i];
      var slideIdx = (update.slide_number || 1) - 1;

      if (slideIdx < 0 || slideIdx >= slides.length) {
        updateLog.push({
          slide_number: update.slide_number,
          status: "skipped",
          reason: "slide not found"
        });
        continue;
      }

      var slide = slides[slideIdx];
      var elemResults = [];

      if (update.elements) {
        for (var j = 0; j < update.elements.length; j++) {
          var elemUpdate = update.elements[j];
          var result = updateElement_(slide, elemUpdate);
          elemResults.push(result);
        }
      }

      updateLog.push({
        slide_number: update.slide_number,
        status: "updated",
        elements: elemResults
      });
    }
  }

  // 4. 保存
  pres.saveAndClose();

  return {
    presentation_id: newId,
    url: "https://docs.google.com/presentation/d/" + newId + "/edit",
    title: newTitle,
    slides_updated: updateLog.length,
    log: updateLog
  };
}

/**
 * 個別要素を更新
 * @param {Slide} slide
 * @param {Object} elemUpdate - { id, value, style, position }
 * @returns {Object} 更新結果
 */
function updateElement_(slide, elemUpdate) {
  var elemId = elemUpdate.id;
  if (!elemId) {
    return { id: null, status: "skipped", reason: "no id" };
  }

  // 要素を ID で検索
  var elem = null;
  var pageElements = slide.getPageElements();
  for (var i = 0; i < pageElements.length; i++) {
    if (pageElements[i].getObjectId() === elemId) {
      elem = pageElements[i];
      break;
    }
  }

  if (!elem) {
    return { id: elemId, status: "not_found" };
  }

  var type = elem.getPageElementType();

  try {
    // テキスト書き換え
    if (elemUpdate.value !== undefined) {
      if (type === SlidesApp.PageElementType.SHAPE) {
        updateShapeText_(elem.asShape(), elemUpdate);
      } else if (type === SlidesApp.PageElementType.TABLE) {
        updateTableData_(elem.asTable(), elemUpdate);
      }
    }

    // 位置調整
    if (elemUpdate.position) {
      updatePosition_(elem, elemUpdate.position);
    }

    return { id: elemId, status: "updated" };
  } catch (e) {
    return { id: elemId, status: "error", error: e.toString() };
  }
}

/**
 * Shape のテキストを更新
 * @param {Shape} shape
 * @param {Object} update - { value, style }
 */
function updateShapeText_(shape, update) {
  var textRange = shape.getText();
  if (!textRange) return;

  // テキスト設定
  textRange.setText(String(update.value));

  // スタイル適用
  if (update.style) {
    applyTextStyle_(textRange, update.style);
  }
}

/**
 * テーブルのデータを更新
 * @param {Table} table
 * @param {Object} update - { value: [[row data]] }
 */
function updateTableData_(table, update) {
  var data = update.value;
  if (!Array.isArray(data)) return;

  var numRows = table.getNumRows();
  var numCols = table.getNumColumns();

  for (var r = 0; r < Math.min(data.length, numRows); r++) {
    if (!Array.isArray(data[r])) continue;
    for (var c = 0; c < Math.min(data[r].length, numCols); c++) {
      try {
        table.getCell(r, c).getText().setText(String(data[r][c]));
      } catch (e) {}
    }
  }
}

/**
 * 要素の位置・サイズを更新
 * @param {PageElement} elem
 * @param {Object} pos - { left, top, width, height }
 */
function updatePosition_(elem, pos) {
  try {
    if (pos.left !== undefined) elem.setLeft(pos.left);
    if (pos.top !== undefined) elem.setTop(pos.top);
    if (pos.width !== undefined) elem.setWidth(pos.width);
    if (pos.height !== undefined) elem.setHeight(pos.height);
  } catch (e) {}
}
