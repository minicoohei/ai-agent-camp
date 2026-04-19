#!/usr/bin/env python3
"""
シンプルAIエージェント実装（Final Example）

ReActパターンを使用したシンプルなエージェントの実装例です。

必要条件:
- Gemini API キー（環境変数 GEMINI_API_KEY）
- Python 3.9以上
- google-genai

使用方法:
    python simple_agent.py "東京の天気を調べて、傘が必要か教えて"
    python simple_agent.py --interactive
"""

import os
import sys
import argparse
import json
import re
from datetime import datetime
from typing import Optional, Dict, List, Any, Callable

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    print("Warning: google-genai がインストールされていません")


# ========================================
# ツール定義
# ========================================

class Tool:
    """ツールの基底クラス"""
    
    def __init__(self, name: str, description: str, parameters: Dict):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def execute(self, **kwargs) -> str:
        raise NotImplementedError


class WeatherTool(Tool):
    """天気取得ツール"""
    
    def __init__(self):
        super().__init__(
            name="get_weather",
            description="指定した都市の天気情報を取得します",
            parameters={
                "city": {"type": "string", "description": "都市名（例：東京、大阪）", "required": True}
            }
        )
    
    def execute(self, city: str) -> str:
        # 実際のAPIの代わりにモックデータを返す
        weather_data = {
            "東京": {"weather": "晴れ時々曇り", "temp": 12, "humidity": 45, "rain_prob": 10},
            "大阪": {"weather": "曇り", "temp": 14, "humidity": 55, "rain_prob": 30},
            "名古屋": {"weather": "晴れ", "temp": 13, "humidity": 40, "rain_prob": 5},
            "福岡": {"weather": "雨", "temp": 16, "humidity": 80, "rain_prob": 90},
            "札幌": {"weather": "雪", "temp": -2, "humidity": 70, "rain_prob": 60}
        }
        
        if city in weather_data:
            data = weather_data[city]
            return f"{city}の天気: {data['weather']}, 気温: {data['temp']}°C, 湿度: {data['humidity']}%, 降水確率: {data['rain_prob']}%"
        else:
            return f"{city}の天気情報が見つかりませんでした。対応都市: {', '.join(weather_data.keys())}"


class CalculatorTool(Tool):
    """計算ツール"""
    
    def __init__(self):
        super().__init__(
            name="calculate",
            description="数学的な計算を実行します",
            parameters={
                "expression": {"type": "string", "description": "計算式（例：2+2, 100*0.08）", "required": True}
            }
        )
    
    def execute(self, expression: str) -> str:
        try:
            import ast
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "エラー: 無効な文字が含まれています"

            tree = ast.parse(expression, mode="eval")
            for node in ast.walk(tree):
                if not isinstance(node, (
                    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
                    ast.Mod, ast.Pow, ast.USub, ast.UAdd,
                )):
                    return "エラー: 許可されていない式です"

            result = self._eval_ast(tree.body)
            return f"計算結果: {expression} = {result}"
        except Exception as e:
            return f"計算エラー: {e}"

    @staticmethod
    def _eval_ast(node):
        """ASTノードを再帰的に評価する。eval()を使わず安全に数式を計算する。"""
        import ast
        import operator

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("数値以外は許可されていません")

        if isinstance(node, ast.UnaryOp):
            val = CalculatorTool._eval_ast(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            if isinstance(node.op, ast.USub):
                return -val
            raise ValueError("許可されていない演算子です")

        if isinstance(node, ast.BinOp):
            ops = {
                ast.Add: operator.add, ast.Sub: operator.sub,
                ast.Mult: operator.mul, ast.Div: operator.truediv,
                ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
                ast.Pow: operator.pow,
            }
            fn = ops.get(type(node.op))
            if fn is None:
                raise ValueError("許可されていない演算子です")
            return fn(CalculatorTool._eval_ast(node.left), CalculatorTool._eval_ast(node.right))

        raise ValueError("許可されていない式です")


class DateTimeTool(Tool):
    """日時取得ツール"""
    
    def __init__(self):
        super().__init__(
            name="get_datetime",
            description="現在の日時を取得します",
            parameters={
                "format": {"type": "string", "description": "日時フォーマット（省略可）", "required": False}
            }
        )
    
    def execute(self, format: str = None) -> str:
        now = datetime.now()
        
        if format:
            try:
                return f"現在日時: {now.strftime(format)}"
            except:
                pass
        
        return f"現在日時: {now.strftime('%Y年%m月%d日 %H:%M:%S')} ({['月','火','水','木','金','土','日'][now.weekday()]}曜日)"


class SearchTool(Tool):
    """検索ツール（モック）"""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Webを検索して情報を取得します",
            parameters={
                "query": {"type": "string", "description": "検索クエリ", "required": True}
            }
        )
    
    def execute(self, query: str) -> str:
        # モック検索結果
        mock_results = {
            "AIエージェント": "AIエージェントとは、自律的にタスクを実行できるAIシステムです。環境を認識し、判断し、行動するサイクルを繰り返します。",
            "ReActパターン": "ReActは、Reasoning（推論）とActing（行動）を組み合わせたLLMエージェントの設計パターンです。",
            "MCP": "Model Context Protocol (MCP)は、AIとツールを接続するための標準プロトコルです。Anthropicが開発しました。"
        }
        
        for key, value in mock_results.items():
            if key.lower() in query.lower():
                return f"検索結果 ({key}): {value}"
        
        return f"'{query}'の検索結果: 関連情報が見つかりました。詳細は実際の検索APIで取得してください。"


# ========================================
# エージェント実装
# ========================================

class SimpleAgent:
    """シンプルなReActエージェント"""
    
    def __init__(self, tools: List[Tool] = None):
        self.tools = {tool.name: tool for tool in (tools or [])}
        self.model = None
        self.conversation_history = []
        
        if HAS_GENAI:
            api_key = os.environ.get("GEMINI_API_KEY")
            if api_key:
                self.model = genai.Client(api_key=api_key)
    
    def _get_system_prompt(self) -> str:
        """システムプロンプトを生成"""
        tool_descriptions = "\n".join([
            f"- {name}: {tool.description}\n  パラメータ: {json.dumps(tool.parameters, ensure_ascii=False)}"
            for name, tool in self.tools.items()
        ])
        
        return f"""あなたはタスクを実行するAIエージェントです。
ユーザーの要求に対して、必要に応じてツールを使用して情報を取得し、回答してください。

## 利用可能なツール
{tool_descriptions}

## 回答フォーマット
1. まず、タスクを分析し、必要なステップを考えます。
2. ツールが必要な場合は、以下の形式で呼び出しを指定します：
   TOOL_CALL: {{"tool": "ツール名", "params": {{"パラメータ名": "値"}}}}
3. ツールの結果を受け取ったら、その情報を使って回答を作成します。
4. 最終回答は明確で分かりやすく記述してください。

## 注意事項
- ツールを使う必要がない場合は、直接回答してください。
- 複数のツールが必要な場合は、一つずつ呼び出してください。
- 推測で回答せず、ツールで確認できることは確認してください。
"""
    
    def _parse_tool_call(self, text: str) -> Optional[Dict]:
        """ツール呼び出しをパース"""
        pattern = r'TOOL_CALL:\s*(\{.*?\})'
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None
    
    def _execute_tool(self, tool_call: Dict) -> str:
        """ツールを実行"""
        tool_name = tool_call.get("tool")
        params = tool_call.get("params", {})
        
        if tool_name not in self.tools:
            return f"エラー: ツール '{tool_name}' は利用できません"
        
        try:
            tool = self.tools[tool_name]
            result = tool.execute(**params)
            return result
        except Exception as e:
            return f"ツール実行エラー: {e}"
    
    def run(self, user_input: str, max_iterations: int = 5) -> str:
        """エージェントを実行"""
        if not self.model:
            return self._mock_run(user_input)
        
        # 会話履歴にユーザー入力を追加
        self.conversation_history.append({"role": "user", "content": user_input})
        
        system_prompt = self._get_system_prompt()
        messages = [system_prompt] + [
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history
        ]
        
        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            
            # LLMに問い合わせ
            response = self.model.models.generate_content(
                model='gemini-3-flash-preview',
                contents=["\n".join(messages)]
            )
            assistant_response = response.text
            
            print(f"\n[思考 {iteration}] {assistant_response[:200]}...")
            
            # ツール呼び出しをチェック
            tool_call = self._parse_tool_call(assistant_response)
            
            if tool_call:
                print(f"[ツール呼び出し] {tool_call}")
                tool_result = self._execute_tool(tool_call)
                print(f"[ツール結果] {tool_result}")
                
                # 結果を会話に追加
                messages.append(f"assistant: {assistant_response}")
                messages.append(f"tool_result: {tool_result}")
            else:
                # ツール呼び出しがなければ最終回答
                self.conversation_history.append({"role": "assistant", "content": assistant_response})
                return assistant_response
        
        return "最大反復回数に達しました。タスクを完了できませんでした。"
    
    def _mock_run(self, user_input: str) -> str:
        """API未接続時のモック実行"""
        print("\n[モックモード] Gemini API が利用できないため、デモ動作を行います")
        
        # 天気に関する質問
        if "天気" in user_input:
            # 都市を抽出
            cities = ["東京", "大阪", "名古屋", "福岡", "札幌"]
            city = next((c for c in cities if c in user_input), "東京")
            
            print(f"\n[思考] ユーザーは{city}の天気を知りたいようです。天気ツールを使用します。")
            print(f"[ツール呼び出し] get_weather(city='{city}')")
            
            weather_tool = WeatherTool()
            weather_result = weather_tool.execute(city=city)
            print(f"[ツール結果] {weather_result}")
            
            if "雨" in weather_result or "降水確率" in weather_result and "50" not in weather_result:
                rain_prob = int(re.search(r'降水確率: (\d+)', weather_result).group(1))
                umbrella = "傘を持っていくことをお勧めします" if rain_prob >= 50 else "傘は必要なさそうです"
            else:
                umbrella = "傘は必要なさそうです"
            
            return f"""
{weather_result}

{umbrella}。
"""
        
        # 計算に関する質問
        if any(op in user_input for op in ["+", "-", "*", "/", "計算"]):
            print("\n[思考] 計算が必要なようです。計算ツールを使用します。")
            
            # 簡単な数式抽出
            expr = re.search(r'[\d\s+\-*/().]+', user_input)
            if expr:
                calc_tool = CalculatorTool()
                result = calc_tool.execute(expression=expr.group().strip())
                print(f"[ツール呼び出し] calculate(expression='{expr.group().strip()}')")
                print(f"[ツール結果] {result}")
                return result
        
        # 日時に関する質問
        if any(word in user_input for word in ["今日", "日付", "時間", "何曜日"]):
            print("\n[思考] 日時情報が必要なようです。")
            dt_tool = DateTimeTool()
            result = dt_tool.execute()
            print(f"[ツール呼び出し] get_datetime()")
            print(f"[ツール結果] {result}")
            return result
        
        return f"""
ご質問ありがとうございます。

「{user_input}」についてですが、現在モックモードで動作しているため、
限定的な回答しかできません。

以下のような質問に対応できます：
- 天気に関する質問（例：東京の天気を教えて）
- 計算（例：100 * 1.1 を計算して）
- 日時（例：今日は何曜日？）

Gemini API キーを設定すると、より高度な回答が可能になります。
"""


class AgentWithMemory(SimpleAgent):
    """記憶機能付きエージェント"""
    
    def __init__(self, tools: List[Tool] = None):
        super().__init__(tools)
        self.short_term_memory = []  # 短期記憶（現在の会話）
        self.long_term_memory = {}   # 長期記憶（永続的な情報）
    
    def remember(self, key: str, value: Any):
        """長期記憶に保存"""
        self.long_term_memory[key] = value
        print(f"[記憶] '{key}' を記憶しました")
    
    def recall(self, key: str) -> Optional[Any]:
        """長期記憶から取得"""
        return self.long_term_memory.get(key)
    
    def get_context(self) -> str:
        """コンテキストを取得"""
        context = []
        
        if self.long_term_memory:
            context.append("## 記憶している情報")
            for key, value in self.long_term_memory.items():
                context.append(f"- {key}: {value}")
        
        if self.short_term_memory:
            context.append("\n## 最近の会話")
            for msg in self.short_term_memory[-5:]:
                context.append(f"- {msg['role']}: {msg['content'][:50]}...")
        
        return "\n".join(context)


# ========================================
# メイン
# ========================================

def create_default_agent() -> SimpleAgent:
    """デフォルトのエージェントを作成"""
    tools = [
        WeatherTool(),
        CalculatorTool(),
        DateTimeTool(),
        SearchTool()
    ]
    return SimpleAgent(tools)


def interactive_mode(agent: SimpleAgent):
    """対話モード"""
    print("\n" + "="*50)
    print("AIエージェント 対話モード")
    print("終了するには 'quit' または 'exit' と入力してください")
    print("="*50 + "\n")
    
    while True:
        try:
            user_input = input("\nあなた: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', '終了']:
                print("\nさようなら！")
                break
            
            response = agent.run(user_input)
            print(f"\nエージェント: {response}")
            
        except KeyboardInterrupt:
            print("\n\n中断されました。")
            break


def main():
    parser = argparse.ArgumentParser(description="シンプルAIエージェント")
    parser.add_argument("query", nargs="?", help="質問・タスク")
    parser.add_argument("--interactive", "-i", action="store_true", help="対話モード")
    parser.add_argument("--tools", action="store_true", help="利用可能なツール一覧")
    
    args = parser.parse_args()
    
    agent = create_default_agent()
    
    if args.tools:
        print("\n利用可能なツール:")
        for name, tool in agent.tools.items():
            print(f"\n  {name}")
            print(f"    説明: {tool.description}")
            print(f"    パラメータ: {json.dumps(tool.parameters, ensure_ascii=False)}")
        return
    
    if args.interactive:
        interactive_mode(agent)
        return
    
    if args.query:
        print(f"\n質問: {args.query}")
        response = agent.run(args.query)
        print(f"\n回答:\n{response}")
        return
    
    # 引数なしの場合はサンプル実行
    print("\n=== サンプル実行 ===")
    
    samples = [
        "東京の天気を教えて。傘は必要？",
        "100 * 1.08 を計算して",
        "今日は何曜日？"
    ]
    
    for query in samples:
        print(f"\n{'='*40}")
        print(f"質問: {query}")
        response = agent.run(query)
        print(f"\n回答: {response}")


if __name__ == "__main__":
    main()
