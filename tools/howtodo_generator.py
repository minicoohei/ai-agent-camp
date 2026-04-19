#!/usr/bin/env python3
"""
HowToDo生成モジュール

タスクに対して、具体的で再現可能な実行手順（HowToDo）を生成します。
- タスク種別の自動判定
- Gemini 3.0 Flash によるHowToDo生成
- Claude Extension用ショートカットYAML生成
"""

import json
import os
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from runtime_env import load_runtime_env

load_runtime_env()

try:
    from google import genai
    from google.genai import types as genai_types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class TaskType(Enum):
    """タスク種別（シンプル化）"""
    WORK = "work"             # 作業系（デフォルト）
    MEETING = "meeting"       # 会議系（カレンダー予定）
    BROWSER = "browser"       # ブラウザ手作業系


@dataclass
class HowToDoStep:
    """手順ステップ"""
    order: int                           # 手順番号
    action: str                          # 具体的なアクション
    check_condition: str                 # 完了条件（結果ベース）
    tool_hint: Optional[str] = None      # 使用ツールのヒント


@dataclass
class HowToDoResult:
    """HowToDo生成結果"""
    task_type: TaskType
    title: str
    summary: str = ""                                               # タスク概要（1-2文）
    completion_criteria: str = ""                                   # 完了条件
    prerequisites: List[str] = field(default_factory=list)          # 前提条件
    steps: List[HowToDoStep] = field(default_factory=list)
    needs_reply: bool = False                                       # 返信が必要かどうか
    reply_examples: List[str] = field(default_factory=list)         # 返信が必要な場合の返信例
    cursor_prompt: Optional[str] = None                             # 作業系用
    browser_shortcut: Optional[Dict[str, str]] = None               # ブラウザ系用
    estimated_minutes: int = 5
    source_info: Dict[str, Any] = field(default_factory=dict)       # 推測根拠/リソース情報
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        result = {
            "task_type": self.task_type.value,
            "title": self.title,
            "summary": self.summary,
            "completion_criteria": self.completion_criteria,
            "prerequisites": self.prerequisites,
            "steps": [asdict(step) for step in self.steps],
            "needs_reply": self.needs_reply,
            "reply_examples": self.reply_examples,
            "cursor_prompt": self.cursor_prompt,
            "browser_shortcut": self.browser_shortcut,
            "estimated_minutes": self.estimated_minutes,
            "source_info": self.source_info
        }
        return result


# タスク種別判定用キーワード
TASK_TYPE_KEYWORDS = {
    TaskType.MEETING: [
        "会議", "ミーティング", "mtg", "定例", "打ち合わせ",
        "議事録", "アジェンダ", "meeting", "1on1", "kickoff"
    ],
    TaskType.BROWSER: [
        "freee", "cloudsign", "salesforce", "kintone", "システム",
        "管理画面", "portal", "ポータル"
    ],
}

# 返信が必要かどうかの判定キーワード
NEEDS_REPLY_KEYWORDS = [
    "返信", "reply", "リプライ", "確認して", "教えて", "質問",
    "お願いします", "ご確認ください", "回答", "連絡ください",
    "@", "メンション"
]

# LLMプロンプト
HOWTODO_SYSTEM_PROMPT = """あなたはタスク実行の専門家です。
与えられたタスクに対して、具体的で再現可能な手順を生成してください。

## 重要なルール

1. **抽象的な表現を避ける**
   - ❌「均一に塗る」
   - ✅「白いところがなくなるまで塗る」

2. **完了条件を明確にする**
   - 各ステップに「〜が表示されたら完了」「〜になっていれば成功」を含める

3. **具体的なUI操作を記述**
   - 「ボタンをクリック」ではなく「右上の青い『送信』ボタンをクリック」

4. **タスク種別に応じた出力**
   - 返信系: 3パターンの返信例を生成
   - 作業系: Cursorで使えるプロンプトを生成
   - ブラウザ系: 画面操作の具体的手順を生成
"""


def classify_task(task: Dict[str, Any]) -> Tuple[TaskType, bool]:
    """
    タスクの種別と返信要否を判定
    
    Returns:
        Tuple[TaskType, bool]: (タスク種別, 返信が必要かどうか)
    """
    source = task.get("source", "").lower()
    content = str(task.get("content", "")).lower()
    title = str(task.get("title", "")).lower()
    mentions = task.get("mentions", [])
    
    # 結合してキーワード検索
    search_text = f"{source} {content} {title}"
    
    # カレンダー/Outputソースは会議タイプ
    if source in ["calendar", "output"]:
        return (TaskType.MEETING, False)
    
    # タスク種別を判定
    task_type = TaskType.WORK  # デフォルト
    for t_type, keywords in TASK_TYPE_KEYWORDS.items():
        if any(kw.lower() in search_text for kw in keywords):
            task_type = t_type
            break
    
    # 返信が必要かどうかを判定
    needs_reply = False
    if source == "slack" and mentions:
        # メンションがある場合は返信が必要
        needs_reply = True
    elif any(kw.lower() in search_text for kw in NEEDS_REPLY_KEYWORDS):
        needs_reply = True
    
    return (task_type, needs_reply)


def _build_output_schema(task_type: TaskType, needs_reply: bool = False) -> str:
    """タスク種別に応じた出力スキーマを生成"""
    base_schema = {
        "summary": "このタスクは何をするタスクか、1-2文で簡潔に説明",
        "completion_criteria": "このタスクが完了したと言える条件（結果ベースで具体的に）",
        "prerequisites": [
            "このタスクを始める前に必要な前提条件1",
            "必要なアクセス権やツール等"
        ],
        "steps": [
            {
                "order": 1,
                "action": "具体的なアクション内容",
                "check_condition": "完了条件（結果ベース）",
                "tool_hint": "使用ツール（オプション）"
            }
        ],
        "estimated_minutes": 5
    }
    
    # 返信が必要な場合は返信例を追加
    if needs_reply:
        base_schema["reply_examples"] = [
            "返信例1（丁寧）",
            "返信例2（簡潔）",
            "返信例3（フォーマル）"
        ]
    
    if task_type == TaskType.WORK:
        base_schema["cursor_prompt"] = "Cursorで実行するためのプロンプト"
    elif task_type == TaskType.BROWSER:
        base_schema["browser_shortcut"] = {
            "name": "shortcut-name",
            "prompt": "ブラウザ操作のプロンプト",
            "start_url": "https://example.com"
        }
    
    return json.dumps(base_schema, ensure_ascii=False, indent=2)


def _parse_llm_response(response_text: str, task_type: TaskType, title: str, needs_reply: bool = False) -> HowToDoResult:
    """LLMレスポンスをパース"""
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        # JSON解析失敗時のフォールバック
        return HowToDoResult(
            task_type=task_type,
            title=title,
            summary="タスクを実行します",
            completion_criteria="タスクが完了していること",
            prerequisites=[],
            needs_reply=needs_reply,
            steps=[HowToDoStep(
                order=1,
                action="タスクを確認して実行",
                check_condition="タスクが完了していること"
            )],
            estimated_minutes=10
        )
    
    # ステップをパース
    steps = []
    for step_data in data.get("steps", []):
        steps.append(HowToDoStep(
            order=step_data.get("order", len(steps) + 1),
            action=step_data.get("action", ""),
            check_condition=step_data.get("check_condition", ""),
            tool_hint=step_data.get("tool_hint")
        ))
    
    # 前提条件をパース（文字列またはリスト対応）
    prerequisites = data.get("prerequisites", [])
    if isinstance(prerequisites, str):
        prerequisites = [prerequisites] if prerequisites else []
    
    return HowToDoResult(
        task_type=task_type,
        title=title,
        summary=data.get("summary", ""),
        completion_criteria=data.get("completion_criteria", ""),
        prerequisites=prerequisites,
        steps=steps,
        needs_reply=needs_reply,
        reply_examples=data.get("reply_examples", []) if needs_reply else [],
        cursor_prompt=data.get("cursor_prompt"),
        browser_shortcut=data.get("browser_shortcut"),
        estimated_minutes=data.get("estimated_minutes", 5)
    )


class HowToDoGenerator:
    """HowToDo生成クラス"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初期化
        
        Args:
            api_key: Gemini API キー（省略時は環境変数から取得）
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.client = None
        self._model_name = None
        
        if HAS_GENAI and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            self._model_name = "gemini-3-flash-preview"
    
    def summarize_title(self, task: Dict[str, Any]) -> str:
        """
        タスクタイトルを簡潔にサマリー（最大25文字）
        
        Args:
            task: タスク情報
        
        Returns:
            要約されたタイトル
        """
        title = task.get("title", "タスク")
        content = task.get("content", task.get("preview", ""))[:300]
        remaining_tasks = task.get("remaining_tasks", [])
        
        # 既に短い場合はそのまま返す
        if len(title) <= 25:
            return title
        
        # LLMが使えない場合は簡易サマリー
        if not self.client:
            return self._summarize_title_fallback(title, content)
        
        prompt = f"""以下のタスク情報から、何をするタスクか一目でわかる短いタイトルを日本語で生成してください。

**要件**:
- 最大25文字
- 動詞で終わる（〜する、〜対応、〜確認 など）
- 具体的な対象を含む

**元タイトル**: {title}
**内容**: {content[:200]}
**残タスク**: {', '.join(remaining_tasks[:3]) if remaining_tasks else 'なし'}

**出力形式（JSON）**:
{{"summary_title": "要約タイトル（25文字以内）"}}"""
        
        try:
            response = self.client.models.generate_content(
                model=self._model_name,
                contents=[prompt],
                config=genai_types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            data = json.loads(response.text)
            summary_title = data.get("summary_title", title[:25])
            return summary_title[:25]  # 念のため25文字に制限
        except Exception as e:
            print(f"⚠️ タイトルサマリーエラー: {e}")
            return self._summarize_title_fallback(title, content)
    
    def _summarize_title_fallback(self, title: str, content: str) -> str:
        """タイトルサマリーのフォールバック"""
        # 括弧内の日付を除去
        import re
        clean_title = re.sub(r'\s*\([^)]*\d{4}[^)]*\)\s*', '', title)
        clean_title = re.sub(r'\s*\d{4}-\d{2}-\d{2}.*$', '', clean_title)
        
        # 25文字に切り詰め
        if len(clean_title) > 25:
            clean_title = clean_title[:22] + "..."
        
        return clean_title.strip() or title[:25]
    
    def check_task_completion(self, file_content: str, title: str) -> Dict[str, Any]:
        """
        LLMでタスクの完了状態を判定
        
        Args:
            file_content: SpecStoryファイルの内容（先頭2000文字程度）
            title: タスクのタイトル
        
        Returns:
            {
                "is_in_progress": bool,  # 仕掛かりかどうか
                "reason": str,           # 判定理由
                "remaining_work": str,   # 残作業（仕掛かりの場合）
                "confidence": float      # 確信度（0-1）
            }
        """
        # LLMが使えない場合はNone（呼び出し側でフォールバック判定を使う）
        if not self.client:
            return None
        
        prompt = f"""以下のSpecStory（作業履歴）ファイルを分析し、このタスクが「仕掛かり中」か「完了済み」かを判定してください。

**タスクタイトル**: {title}

**ファイル内容**:
```
{file_content[:2500]}
```

**判定基準**:
1. 「仕掛かり中」の特徴:
   - [ ] のチェックボックスが残っている
   - 「TODO」「次のステップ」「残タスク」の記載がある
   - 「実装中」「対応中」「WIP」などのステータス
   - 最後のメッセージが作業依頼や質問で終わっている

2. 「完了済み」の特徴:
   - [x] で全てチェックされている
   - 「完了」「Done」「クローズ」「対応済み」の明示的な記載
   - 最終的な成果物やリリースの報告で終わっている
   - 作業の終了宣言がある

**出力形式（JSON）**:
{{
    "is_in_progress": true/false,
    "reason": "判定理由（1-2文）",
    "remaining_work": "残っている作業（仕掛かりの場合のみ、簡潔に）",
    "confidence": 0.0-1.0
}}"""

        try:
            response = self.client.models.generate_content(
                model=self._model_name,
                contents=[prompt],
                config=genai_types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            result = json.loads(response.text)
            return result
        except Exception as e:
            print(f"⚠️ 完了判定エラー: {e}")
            return None
    
    def infer_tasks_from_activity(self, activity_logs: List[Dict]) -> List[Dict[str, Any]]:
        """
        Activity LogからLLMでタスクを推測
        
        Args:
            activity_logs: Activity Logのリスト（extract_activity_logsの結果）
        
        Returns:
            推測されたタスクのリスト
        """
        if not self.client:
            print("⚠️ Activity LogからのLLM推測: APIキー未設定")
            return []
        
        # 直近のログをサンプリング（OCRテキストは重いので制限）
        sampled_logs = []
        for log in activity_logs[:3]:  # 直近3ファイル分
            log_entries = log.get("logs", [])
            # window_titleがあるエントリのみ、10件まで
            relevant_entries = [
                e for e in log_entries 
                if e.get("window_title") or any(d.get("ocr_text") for d in e.get("displays", []))
            ][:10]
            
            for entry in relevant_entries:
                simplified = {
                    "timestamp": entry.get("timestamp", ""),
                    "app": entry.get("active_app", ""),
                    "window": entry.get("window_title", "")[:100],
                    # OCRは先頭500文字のみ
                    "screen_text": " ".join([
                        d.get("ocr_text", "")[:500] 
                        for d in entry.get("displays", [])[:1]
                    ])[:800]
                }
                sampled_logs.append(simplified)
        
        if not sampled_logs:
            return []
        
        # ログを整形
        log_summary = "\n".join([
            f"[{e['timestamp'][:16]}] {e['app']} - {e['window']}\n  画面: {e['screen_text'][:200]}..."
            for e in sampled_logs[:15]  # 最大15エントリ
        ])
        
        prompt = f"""以下のActivity Log（PC操作履歴）を分析し、**ユーザー自身がアクションを取るべきタスク**のみを推測してください。

**Activity Log**:
{log_summary}

**重要なフィルタリング基準**:
- ✅ 抽出すべき: ユーザー自身が編集・作成・返信・実行すべき作業
- ✅ 抽出すべき: ユーザー宛のメンション、依頼、質問
- ❌ 除外すべき: 単なる情報収集・閲覧目的のブラウジング
- ❌ 除外すべき: 他人の作業を見ているだけ（参考資料の確認など）
- ❌ 除外すべき: 一般的なニュース・記事の閲覧
- ❌ 除外すべき: 検索結果の一覧を眺めているだけ

**推測のポイント**:
1. ファイル編集中（Cursor, VSCode, Notion等で特定ファイルを開いている）→ 作業タスク
2. Slackで自分宛のメンションがある → 返信タスク
3. 申請・承認画面を操作している → 処理タスク
4. カレンダーで特定の予定を確認している → 準備タスク

**出力形式（JSON配列）**:
[
    {{
        "title": "タスクの短いタイトル（20文字以内）",
        "content": "具体的な作業内容の説明",
        "task_type": "work/browser/meeting のいずれか",
        "priority": "high/medium/low",
        "reason": "なぜユーザー自身がアクションを取るべきと判断したか"
    }},
    ...
]

**ユーザー自身のアクションが必要なタスクのみ**を最大3件まで出力してください。
該当するタスクがなければ空配列 [] を返してください。
"""
        
        try:
            response = self.client.models.generate_content(
                model=self._model_name,
                contents=[prompt],
                config=genai_types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3,
                ),
            )
            tasks = json.loads(response.text)
            
            # 結果を整形
            result = []
            for i, task in enumerate(tasks[:5]):
                # priority変換: high/medium → B, low → C
                llm_priority = task.get("priority", "medium").lower()
                priority = "B" if llm_priority in ["high", "medium"] else "C"
                
                result.append({
                    "id": f"activity_inferred_{i}",
                    "title": task.get("title", "Activity推測タスク"),
                    "content": task.get("content", task.get("description", "")),  # descriptionもフォールバック
                    "source": "activity_logger_llm",
                    "task_type": task.get("task_type", "work"),
                    "priority": priority,
                    "llm_reason": task.get("reason", task.get("category", ""))  # categoryもフォールバック
                })
            
            print(f"🔍 Activity Logから{len(result)}件のタスクを推測")
            return result
            
        except Exception as e:
            print(f"⚠️ Activity Log推測エラー: {e}")
            return []
    
    def generate(self, task: Dict[str, Any]) -> HowToDoResult:
        """
        タスクに対するHowToDoを生成
        
        Args:
            task: タスク情報（title, content, source等を含む辞書）
        
        Returns:
            HowToDoResult: 生成されたHowToDo
        """
        task_type, needs_reply = classify_task(task)
        title = task.get("title", "タスク")
        short_title = title[:30] + "..." if len(title) > 30 else title
        
        # 推測根拠情報を抽出
        source_info = self._extract_source_info(task)
        
        # LLMが使えない場合はフォールバック
        if not self.client:
            print(f"🔧 フォールバック生成: {short_title} (APIキー未設定またはgenai未インストール)")
            result = self._generate_fallback(task, task_type, title, needs_reply)
            result.source_info = source_info
            return result
        
        try:
            reply_indicator = " 📧" if needs_reply else ""
            print(f"🤖 LLM生成中: {short_title}{reply_indicator}...")
            result = self._generate_with_llm(task, task_type, title, needs_reply)
            result.source_info = source_info
            print(f"✅ LLM生成完了: {short_title}")
            return result
        except Exception as e:
            print(f"⚠️ LLMエラー ({e}) → フォールバック: {short_title}")
            result = self._generate_fallback(task, task_type, title, needs_reply)
            result.source_info = source_info
            return result
    
    def _extract_source_info(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """タスクから推測根拠/リソース情報を抽出"""
        source = task.get("source", "unknown")
        source_info = {
            "source_type": source,
            "reason": "",
            "resource_path": "",
            "resource_url": ""
        }
        
        if source == "specstory":
            source_info["reason"] = "SpecStoryの仕掛かりタスクから検出"
            source_info["resource_path"] = task.get("file", "")
            remaining = task.get("remaining_tasks", [])
            if remaining:
                source_info["remaining_todos"] = remaining[:5]  # 最大5件
        
        elif source == "slack":
            workspace = task.get("workspace", "")
            channel = task.get("channel", "")
            source_info["reason"] = f"Slack ({workspace}) #{channel} のメッセージから検出"
            source_info["resource_url"] = task.get("slack_url", "")
            source_info["mentions"] = task.get("mentions", [])
        
        elif source == "activity_logger":
            source_info["reason"] = "Activity Logのアプリ使用履歴から検出"
        
        elif source == "activity_logger_llm":
            source_info["reason"] = task.get("llm_reason", "Activity LogからLLMが推測")
        
        elif source in ["calendar", "output"]:
            source_info["reason"] = "Googleカレンダーの予定から検出"
            source_info["resource_path"] = task.get("file", "")
        
        elif source == "gmail":
            source_info["reason"] = "Gmailのメールから検出"
        
        elif source == "voicememo":
            source_info["reason"] = "音声メモから検出"
        
        return source_info
    
    def _generate_with_llm(
        self, 
        task: Dict[str, Any], 
        task_type: TaskType, 
        title: str,
        needs_reply: bool = False
    ) -> HowToDoResult:
        """LLMでHowToDoを生成"""
        output_schema = _build_output_schema(task_type, needs_reply)
        
        reply_note = "\n- ※返信が必要なタスクです。適切な返信例を生成してください。" if needs_reply else ""
        
        user_prompt = f"""## タスク情報
- タイトル: {title}
- 種別: {task_type.value}
- ソース: {task.get('source', 'unknown')}
- 詳細: {task.get('content', task.get('preview', 'なし'))}
- 関連コンテキスト: {task.get('context', 'なし')}{reply_note}

## 出力形式
以下のJSON形式で出力してください：
{output_schema}
"""
        
        response = self.client.models.generate_content(
            model=self._model_name,
            contents=[
                genai_types.Content(role="user", parts=[genai_types.Part(text=HOWTODO_SYSTEM_PROMPT)]),
                genai_types.Content(role="model", parts=[genai_types.Part(text="了解しました。具体的で再現可能な手順を生成します。")]),
                genai_types.Content(role="user", parts=[genai_types.Part(text=user_prompt)]),
            ],
            config=genai_types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        
        return _parse_llm_response(response.text, task_type, title, needs_reply)
    
    def _generate_fallback(
        self, 
        task: Dict[str, Any], 
        task_type: TaskType, 
        title: str,
        needs_reply: bool = False
    ) -> HowToDoResult:
        """LLM不使用時のフォールバック生成（タスク詳細を反映）"""
        
        content = task.get("content", task.get("preview", ""))
        remaining_tasks = task.get("remaining_tasks", [])
        file_path = task.get("file", "")
        source = task.get("source", "")
        
        # タスク概要を生成
        summary = self._generate_summary(task, task_type)
        
        # 完了条件を生成
        completion_criteria = self._generate_completion_criteria(task, task_type)
        
        # 前提条件を生成
        prerequisites = self._generate_prerequisites(task, task_type)
        
        # 残タスクがある場合は、それを具体的な手順として使用
        if remaining_tasks:
            steps = self._build_steps_from_remaining_tasks(remaining_tasks, task_type)
        else:
            steps = self._build_default_steps(task_type, title, content)
        
        # 見積もり時間を計算
        estimated_minutes = max(5, len(steps) * 3)
        
        result = HowToDoResult(
            task_type=task_type,
            title=title,
            summary=summary,
            completion_criteria=completion_criteria,
            prerequisites=prerequisites,
            steps=steps,
            needs_reply=needs_reply,
            estimated_minutes=estimated_minutes
        )
        
        # 返信が必要な場合
        if needs_reply:
            result.reply_examples = self._generate_reply_examples(task)
        
        # 種別に応じた追加情報
        if task_type == TaskType.WORK:
            result.cursor_prompt = self._generate_cursor_prompt(task)
        elif task_type == TaskType.BROWSER:
            result.browser_shortcut = self._generate_browser_shortcut(task)
        
        return result
    
    def _build_steps_from_remaining_tasks(
        self, 
        remaining_tasks: List[str], 
        task_type: TaskType
    ) -> List[HowToDoStep]:
        """残タスクから手順を生成"""
        steps = []
        for i, rt in enumerate(remaining_tasks[:7], 1):  # 最大7ステップ
            tool_hint = self._guess_tool(rt)
            steps.append(HowToDoStep(
                order=i,
                action=rt,
                check_condition=f"「{rt[:30]}」が完了していること",
                tool_hint=tool_hint
            ))
        return steps
    
    def _build_default_steps(
        self, 
        task_type: TaskType, 
        title: str, 
        content: str
    ) -> List[HowToDoStep]:
        """タスク種別とコンテンツからデフォルト手順を生成"""
        
        # コンテンツから具体的なアクションを抽出
        action_keywords = self._extract_action_keywords(title + " " + content)
        
        if task_type == TaskType.REPLY:
            return [
                HowToDoStep(1, f"「{title[:40]}」のメッセージを開く", "メッセージ全文が表示されていること"),
                HowToDoStep(2, "依頼内容・質問の要点を把握", "何を求められているか理解できていること"),
                HowToDoStep(3, "返信文を作成（下記の返信例を参考に）", "返信文が完成していること"),
                HowToDoStep(4, "送信ボタンをクリック", "送信完了の通知が表示されること"),
            ]
        elif task_type == TaskType.APPROVAL:
            return [
                HowToDoStep(1, "承認システムにログイン", "承認一覧画面が表示されること"),
                HowToDoStep(2, f"「{title[:30]}」の申請を開く", "申請詳細が表示されること"),
                HowToDoStep(3, "申請内容・金額・添付資料を確認", "内容に問題がないこと"),
                HowToDoStep(4, "承認ボタンをクリック", "「承認完了」メッセージが表示されること"),
            ]
        elif task_type == TaskType.DOCUMENT:
            return [
                HowToDoStep(1, "対象システムにログイン", "ダッシュボードが表示されること"),
                HowToDoStep(2, f"「{title[:30]}」関連の書類を検索", "対象書類が見つかること"),
                HowToDoStep(3, "書類の内容を確認", "記載内容に誤りがないこと"),
                HowToDoStep(4, "ダウンロード/登録/送信を実行", "完了メッセージが表示されること"),
            ]
        elif task_type == TaskType.MEETING:
            return [
                HowToDoStep(1, "会議の目的・アジェンダを確認", "議題を把握していること"),
                HowToDoStep(2, "必要な資料・データを準備", "共有資料が揃っていること"),
                HowToDoStep(3, "会議ツール（Zoom/Meet等）を開く", "接続準備が完了していること"),
                HowToDoStep(4, "会議に参加・議事メモを取る", "議事録のドラフトが完成していること"),
            ]
        elif task_type == TaskType.BROWSER:
            return [
                HowToDoStep(1, "対象のシステム/サイトを開く", "ログイン画面またはダッシュボードが表示されること", "Browser"),
                HowToDoStep(2, f"「{title[:30]}」に関する画面に移動", "目的の画面が表示されること", "Browser"),
                HowToDoStep(3, "必要な入力・操作を実行", "入力/操作が完了すること", "Browser"),
                HowToDoStep(4, "結果を確認して完了", "期待通りの結果になっていること", "Browser"),
            ]
        else:  # WORK
            file_action = f"「{action_keywords}」関連のファイルを開く" if action_keywords else "対象ファイル/コードを開く"
            return [
                HowToDoStep(1, file_action, "ファイルが開かれていること", "Cursor"),
                HowToDoStep(2, f"「{title[:30]}」の実装/修正を行う", "コード変更が完了していること", "Cursor"),
                HowToDoStep(3, "変更内容を保存", "ファイルが保存されていること", "Cursor"),
                HowToDoStep(4, "動作確認・テスト実行", "エラーなく動作すること", "Terminal"),
            ]
    
    def _extract_action_keywords(self, text: str) -> str:
        """テキストからアクションキーワードを抽出"""
        keywords = []
        action_words = ["実装", "作成", "修正", "追加", "削除", "更新", "設定", "確認", "対応"]
        for word in action_words:
            if word in text:
                keywords.append(word)
        return "・".join(keywords[:2]) if keywords else ""
    
    def _guess_tool(self, action: str) -> Optional[str]:
        """アクションから使用ツールを推測"""
        action_lower = action.lower()
        if any(kw in action_lower for kw in ["コード", "実装", "ファイル", "関数", "クラス", "修正"]):
            return "Cursor"
        elif any(kw in action_lower for kw in ["コマンド", "実行", "テスト", "ビルド", "npm", "python"]):
            return "Terminal"
        elif any(kw in action_lower for kw in ["ブラウザ", "画面", "サイト", "url", "ログイン"]):
            return "Browser"
        elif any(kw in action_lower for kw in ["メール", "返信", "slack", "送信"]):
            return "Email/Slack"
        return None
    
    def _generate_reply_examples(self, task: Dict[str, Any]) -> List[str]:
        """タスク内容に応じた返信例を生成"""
        content = task.get("content", task.get("preview", ""))
        title = task.get("title", "")
        search_text = (content + " " + title).lower()
        
        # キーワードベースで返信パターンを選択
        if "確認" in search_text:
            return [
                f"確認いたしました。{title[:30]}について、以下の通りご報告いたします。",
                "ご確認依頼ありがとうございます。確認の上、ご連絡いたします。",
                f"お問い合わせの件、確認いたしました。{title[:30]}は問題ございません。"
            ]
        elif "お願い" in search_text or "依頼" in search_text:
            return [
                f"承知いたしました。「{title[:30]}」の件、対応いたします。",
                f"ご依頼ありがとうございます。{title[:30]}について、本日中に対応いたします。",
                "了解いたしました。完了次第、ご報告させていただきます。"
            ]
        elif "質問" in search_text or "教えて" in search_text:
            return [
                f"ご質問ありがとうございます。{title[:30]}についてお答えいたします。",
                "お問い合わせの件、以下の通りご回答いたします。",
                f"ご質問いただいた{title[:30]}について、ご説明いたします。"
            ]
        elif "報告" in search_text or "共有" in search_text:
            return [
                f"ご共有ありがとうございます。{title[:30]}について承知いたしました。",
                "ご報告ありがとうございます。内容確認いたしました。",
                f"{title[:30]}の件、了解いたしました。何かあればご連絡ください。"
            ]
        elif "相談" in search_text:
            return [
                f"{title[:30]}について、ご相談ありがとうございます。以下、私の考えをお伝えします。",
                "ご相談の件、拝見いたしました。いくつかご提案させていただきます。",
                f"お時間をいただければ、{title[:30]}について詳しくお話しできればと思います。"
            ]
        else:
            # デフォルトの汎用返信例
            return [
                f"お世話になっております。{title[:30]}の件、承知いたしました。",
                f"ご連絡ありがとうございます。{title[:30]}について対応いたします。",
                f"{title[:30]}の件、了解いたしました。進捗があればご報告いたします。"
            ]
    
    def _generate_cursor_prompt(self, task: Dict[str, Any]) -> str:
        """タスク詳細からCursorプロンプトを生成"""
        title = task.get("title", "タスク")
        content = task.get("content", task.get("preview", ""))
        remaining_tasks = task.get("remaining_tasks", [])
        file_path = task.get("file", "")
        
        prompt_parts = [f"## タスク: {title}"]
        
        if file_path:
            prompt_parts.append(f"\n### 対象ファイル\n`{file_path}`")
        
        if remaining_tasks:
            prompt_parts.append("\n### 残タスク（チェックリスト）")
            for rt in remaining_tasks:
                prompt_parts.append(f"- [ ] {rt}")
        
        if content and content != title:
            prompt_parts.append(f"\n### 詳細・コンテキスト\n{content[:500]}")
        
        prompt_parts.append("\n### 実行手順")
        prompt_parts.append("1. 上記の残タスクを順番に実装してください")
        prompt_parts.append("2. 各タスク完了後、動作確認を行ってください")
        prompt_parts.append("3. 完了したらチェックを入れてください")
        
        return "\n".join(prompt_parts)
    
    def _generate_browser_shortcut(self, task: Dict[str, Any]) -> Dict[str, str]:
        """ブラウザショートカット情報を生成"""
        title = task.get("title", "task")
        content = task.get("content", "")
        
        # URLを推測
        start_url = "https://example.com"
        if "freee" in (title + content).lower():
            start_url = "https://accounts.secure.freee.co.jp/"
        elif "slack" in (title + content).lower():
            start_url = "https://slack.com/"
        elif "github" in (title + content).lower():
            start_url = "https://github.com/"
        
        # ショートカット名を生成
        safe_name = title[:25].replace(" ", "-").replace("　", "-").lower()
        safe_name = "".join(c for c in safe_name if c.isalnum() or c == "-")
        
        return {
            "name": f"task-{safe_name}",
            "prompt": f"以下のタスクをブラウザで実行してください：\n\n{title}\n\n{content[:200]}",
            "start_url": start_url
        }
    
    def _generate_summary(self, task: Dict[str, Any], task_type: TaskType) -> str:
        """タスク概要を生成（1-2文）"""
        title = task.get("title", "タスク")
        content = task.get("content", task.get("preview", ""))
        remaining_tasks = task.get("remaining_tasks", [])
        
        # タスク種別に応じた概要テンプレート
        type_summaries = {
            TaskType.REPLY: f"「{title[:30]}」に対して返信を作成・送信するタスクです。",
            TaskType.APPROVAL: f"「{title[:30]}」の承認リクエストを確認・承認するタスクです。",
            TaskType.DOCUMENT: f"「{title[:30]}」に関する書類を処理（ダウンロード/登録/確認）するタスクです。",
            TaskType.MEETING: f"「{title[:30]}」に関する会議の準備・参加・議事録作成を行うタスクです。",
            TaskType.BROWSER: f"ブラウザで「{title[:30]}」に関するシステム操作を実行するタスクです。",
            TaskType.WORK: f"「{title[:30]}」に関するコード/ファイルの作成・編集を行うタスクです。"
        }
        
        summary = type_summaries.get(task_type, f"「{title[:30]}」を実行するタスクです。")
        
        # 残タスクがある場合は補足
        if remaining_tasks:
            summary += f" {len(remaining_tasks)}件の残タスクがあります。"
        
        return summary
    
    def _generate_completion_criteria(self, task: Dict[str, Any], task_type: TaskType) -> str:
        """完了条件を生成"""
        title = task.get("title", "タスク")
        remaining_tasks = task.get("remaining_tasks", [])
        
        # タスク種別に応じた完了条件
        type_criteria = {
            TaskType.REPLY: "返信が送信され、送信完了の通知が表示されていること",
            TaskType.APPROVAL: "承認/却下が完了し、ステータスが更新されていること",
            TaskType.DOCUMENT: "書類の処理が完了し、必要な場所に保存/送信されていること",
            TaskType.MEETING: "会議に参加し、議事録/メモが作成されていること",
            TaskType.BROWSER: "システムでの操作が完了し、期待する結果が確認できていること",
            TaskType.WORK: "コード/ファイルの編集が完了し、動作確認が取れていること"
        }
        
        base_criteria = type_criteria.get(task_type, "タスクが完了していること")
        
        # 残タスクがある場合は具体化
        if remaining_tasks:
            base_criteria += f"。残タスク{len(remaining_tasks)}件が全て完了していること"
        
        return base_criteria
    
    def _generate_prerequisites(self, task: Dict[str, Any], task_type: TaskType) -> List[str]:
        """前提条件を生成"""
        content = task.get("content", task.get("preview", "")).lower()
        title = task.get("title", "").lower()
        search_text = content + " " + title
        
        prerequisites = []
        
        # 共通の前提条件
        if task_type in [TaskType.BROWSER, TaskType.APPROVAL, TaskType.DOCUMENT]:
            prerequisites.append("対象システムへのログインアクセス権")
        
        if task_type == TaskType.REPLY:
            prerequisites.append("返信先の情報（メールアドレス/チャンネル）の確認")
            prerequisites.append("返信に必要な情報・資料の準備")
        
        if task_type == TaskType.MEETING:
            prerequisites.append("会議ツール（Zoom/Meet/Teams）のセットアップ")
            prerequisites.append("議題・アジェンダの確認")
        
        if task_type == TaskType.WORK:
            prerequisites.append("開発環境のセットアップ")
            if "api" in search_text:
                prerequisites.append("API仕様書の確認")
            if "test" in search_text or "テスト" in search_text:
                prerequisites.append("テスト環境へのアクセス")
        
        # キーワードベースの追加条件
        if "freee" in search_text:
            prerequisites.append("freeeへのログインアクセス")
        if "github" in search_text:
            prerequisites.append("GitHubリポジトリへのアクセス権")
        if "slack" in search_text:
            prerequisites.append("Slackワークスペースへのアクセス")
        
        # 最低1件は返す
        if not prerequisites:
            prerequisites.append("タスク実行に必要な権限・情報の確認")
        
        return prerequisites[:5]  # 最大5件
    
    def generate_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        複数タスクに対してHowToDoを一括生成
        
        Args:
            tasks: タスク情報のリスト
        
        Returns:
            HowToDo付きタスクのリスト
        """
        results = []
        for task in tasks:
            # タイトルをサマリー
            original_title = task.get("title", "タスク")
            summary_title = self.summarize_title(task)
            
            # HowToDo生成
            howtodo = self.generate(task)
            
            # 結果を構築
            task_with_howtodo = task.copy()
            task_with_howtodo["original_title"] = original_title
            task_with_howtodo["title"] = summary_title  # サマリータイトルに置換
            task_with_howtodo["howtodo"] = howtodo.to_dict()
            results.append(task_with_howtodo)
        return results


def generate_shortcuts_yaml(tasks: List[Dict[str, Any]]) -> str:
    """
    Claude Extension用ショートカットYAML生成
    
    Args:
        tasks: HowToDo付きタスクのリスト
    
    Returns:
        YAML形式の文字列
    """
    shortcuts = []
    
    for task in tasks:
        howtodo = task.get("howtodo", {})
        if howtodo.get("task_type") != TaskType.BROWSER.value:
            continue
        
        shortcut = howtodo.get("browser_shortcut")
        if shortcut:
            shortcuts.append({
                "名前": f"/{shortcut.get('name', 'unknown')}",
                "プロンプト": shortcut.get("prompt", ""),
                "開始URL": shortcut.get("start_url", ""),
                "スケジュール": "-"
            })
    
    if HAS_YAML:
        return yaml.dump(shortcuts, allow_unicode=True, default_flow_style=False)
    else:
        # YAML未インストール時はJSON形式で代替
        return json.dumps(shortcuts, ensure_ascii=False, indent=2)


# テスト用
if __name__ == "__main__":
    # サンプルタスク
    sample_tasks = [
        {
            "title": "Slackで田中さんに返信",
            "content": "プロジェクト進捗について確認して教えてください",
            "source": "slack"
        },
        {
            "title": "経費申請の承認",
            "content": "freeeで経費承認ワークフロー",
            "source": "email"
        },
        {
            "title": "API実装",
            "content": "ユーザー認証APIのエンドポイントを追加",
            "source": "specstory"
        },
    ]
    
    generator = HowToDoGenerator()
    
    for task in sample_tasks:
        print(f"\n{'='*50}")
        print(f"タスク: {task['title']}")
        
        task_type = classify_task(task)
        print(f"種別: {task_type.value}")
        
        result = generator.generate(task)
        print(f"HowToDo:")
        for step in result.steps:
            print(f"  {step.order}. {step.action}")
            print(f"     ✓ {step.check_condition}")
        
        if result.reply_examples:
            print(f"返信例: {result.reply_examples[0][:50]}...")
        if result.cursor_prompt:
            print(f"Cursorプロンプト: {result.cursor_prompt[:50]}...")
