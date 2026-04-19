/**
 * deckSlides.js — ゼロから Google Slides デッキを生成
 *
 * テンプレートなしで新しいプレゼンテーションを作成し、
 * スライド仕様に基づいて要素を配置する。
 * Gemini で生成したアウトラインから直接スライドを構築する。
 *
 * clasp run createDeck --params '[
 *   "プレゼンタイトル",
 *   [{"layout":"TITLE","elements":[{"type":"textbox","value":"タイトル","position":{...},"style":{...}}]}]
 * ]'
 */

/**
 * ゼロからデッキを生成
 * @param {string} title - プレゼンテーションタイトル
 * @param {Array} slideSpecs - [{layout, elements: [{type, value, position, style, ...}]}]
 * @returns {Object} 結果
 */
function createDeck(title, slideSpecs) {
  // 1. 新しいプレゼンテーション作成
  var pres = SlidesApp.create(title || "New Presentation");

  // 2. デフォルトのスライドを削除
  var defaultSlides = pres.getSlides();
  if (defaultSlides.length > 0) {
    defaultSlides[0].remove();
  }

  var slideLog = [];

  // 3. スライドを順次追加
  if (slideSpecs) {
    for (var i = 0; i < slideSpecs.length; i++) {
      var spec = slideSpecs[i];
      var layout = getLayout_(pres, spec.layout || "BLANK");
      var slide = pres.appendSlide(layout);

      var elemResults = [];

      if (spec.elements) {
        for (var j = 0; j < spec.elements.length; j++) {
          var elemSpec = spec.elements[j];
          var result = addElement_(slide, elemSpec);
          elemResults.push(result);
        }
      }

      slideLog.push({
        slide_number: i + 1,
        layout: spec.layout || "BLANK",
        elements_added: elemResults.length
      });
    }
  }

  // 4. 保存
  pres.saveAndClose();

  return {
    presentation_id: pres.getId(),
    url: "https://docs.google.com/presentation/d/" + pres.getId() + "/edit",
    title: title,
    slides_count: slideSpecs ? slideSpecs.length : 0,
    log: slideLog
  };
}

/**
 * テンプレートベースのデッキ生成（テンプレートコピー + スライド追加/削除）
 * @param {string} templateId - テンプレートプレゼンテーションID
 * @param {string} title - 新タイトル
 * @param {Array} slideSpecs - スライド仕様
 * @returns {Object}
 */
function createDeckFromTemplate(templateId, title, slideSpecs) {
  // テンプレートをコピー
  var templateFile = DriveApp.getFileById(templateId);
  var copy = templateFile.makeCopy(title || "Deck: " + templateFile.getName());
  var pres = SlidesApp.openById(copy.getId());

  // 既存スライドを全削除（テーマだけ残す）
  var existingSlides = pres.getSlides();
  for (var i = existingSlides.length - 1; i >= 0; i--) {
    existingSlides[i].remove();
  }

  var slideLog = [];

  // スライドを追加
  if (slideSpecs) {
    for (var i = 0; i < slideSpecs.length; i++) {
      var spec = slideSpecs[i];
      var layout = getLayout_(pres, spec.layout || "BLANK");
      var slide = pres.appendSlide(layout);

      if (spec.elements) {
        for (var j = 0; j < spec.elements.length; j++) {
          addElement_(slide, spec.elements[j]);
        }
      }

      slideLog.push({
        slide_number: i + 1,
        layout: spec.layout || "BLANK",
        elements_added: spec.elements ? spec.elements.length : 0
      });
    }
  }

  pres.saveAndClose();

  return {
    presentation_id: copy.getId(),
    url: "https://docs.google.com/presentation/d/" + copy.getId() + "/edit",
    title: title,
    template_id: templateId,
    slides_count: slideSpecs ? slideSpecs.length : 0,
    log: slideLog
  };
}

/**
 * スライドに要素を追加
 * @param {Slide} slide
 * @param {Object} spec - { type, value, position, style, ... }
 * @returns {Object}
 */
function addElement_(slide, spec) {
  var elemType = spec.type || "textbox";

  try {
    switch (elemType) {
      case "textbox":
        insertTextBox_(slide, spec);
        return { type: "textbox", status: "added" };

      case "shape":
        insertShape_(slide, spec);
        return { type: "shape", status: "added" };

      case "table":
        insertTable_(slide, spec);
        return { type: "table", status: "added" };

      case "image":
        if (spec.image_url) {
          var pos = spec.position || {};
          slide.insertImage(
            spec.image_url,
            pos.left || 50,
            pos.top || 50,
            pos.width || 400,
            pos.height || 300
          );
          return { type: "image", status: "added" };
        }
        return { type: "image", status: "skipped", reason: "no image_url" };

      default:
        return { type: elemType, status: "unsupported" };
    }
  } catch (e) {
    return { type: elemType, status: "error", error: e.toString() };
  }
}
