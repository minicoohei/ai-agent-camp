/**
 * convertSlides.js — テンプレートコピー＋プレースホルダー置換
 *
 * テンプレートプレゼンテーションをコピーし、
 * replaceAllText でプレースホルダーを一括置換する。
 * シンプルな書き換えに最適。
 *
 * clasp run convertPresentation --params '[
 *   "TEMPLATE_ID",
 *   "新しいタイトル",
 *   {"{{slide_1_title}}": "新タイトル", "{{slide_1_body}}": "新テキスト"}
 * ]'
 */

/**
 * テンプレートをコピーして replaceAllText で一括置換
 * @param {string} templateId - テンプレートのプレゼンテーションID
 * @param {string} newTitle - 新しいプレゼンテーション名
 * @param {Object} replacements - { "{{placeholder}}": "new value", ... }
 * @returns {Object} 結果 { presentation_id, url, replaced_count }
 */
function convertPresentation(templateId, newTitle, replacements) {
  // 1. テンプレートをコピー
  var templateFile = DriveApp.getFileById(templateId);
  var copy = templateFile.makeCopy(newTitle || "Copy of " + templateFile.getName());
  var newId = copy.getId();

  // 2. コピーを開く
  var pres = SlidesApp.openById(newId);

  // 3. プレースホルダー置換
  var replacedCount = 0;
  if (replacements) {
    var keys = Object.keys(replacements);
    for (var i = 0; i < keys.length; i++) {
      var placeholder = keys[i];
      var newValue = replacements[placeholder];
      if (newValue !== null && newValue !== undefined) {
        try {
          pres.replaceAllText(placeholder, String(newValue));
          replacedCount++;
        } catch (e) {
          // 置換失敗は無視（プレースホルダーが見つからない場合など）
        }
      }
    }
  }

  // 4. 保存
  pres.saveAndClose();

  return {
    presentation_id: newId,
    url: "https://docs.google.com/presentation/d/" + newId + "/edit",
    title: newTitle,
    replaced_count: replacedCount,
    total_placeholders: replacements ? Object.keys(replacements).length : 0
  };
}

/**
 * テンプレートのプレースホルダーを一覧取得（プレビュー用）
 * @param {string} templateId
 * @returns {Object} { placeholders: [...] }
 */
function listPlaceholders(templateId) {
  var pres = SlidesApp.openById(templateId);
  var slides = pres.getSlides();
  var placeholders = [];
  var pattern = /\{\{[^}]+\}\}/g;

  for (var i = 0; i < slides.length; i++) {
    var elements = slides[i].getPageElements();
    for (var j = 0; j < elements.length; j++) {
      try {
        if (elements[j].getPageElementType() === SlidesApp.PageElementType.SHAPE) {
          var text = elements[j].asShape().getText().asString();
          var matches = text.match(pattern);
          if (matches) {
            for (var k = 0; k < matches.length; k++) {
              placeholders.push({
                slide_number: i + 1,
                placeholder: matches[k],
                element_id: elements[j].getObjectId(),
                current_text: text.substring(0, 100)
              });
            }
          }
        }
      } catch (e) {}
    }
  }

  return {
    presentation_id: templateId,
    placeholder_count: placeholders.length,
    placeholders: placeholders
  };
}
