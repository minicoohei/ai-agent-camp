# Generate Diagram with Nano Banana Pro

このコマンドは、`.cursor/tools/generate_diagram.py` を使用して、指定されたテーマに基づいた図解やインフォグラフィックを生成します。
長いテキストや段落全体を貼り付けて可視化することも可能です。

## 実行手順

1.  **パラメータの抽出**:
    ユーザーの入力から以下の情報を抽出してください。
    - **テーマ/内容**: 図解したい内容やテキスト（必須）
    - **スタイル**: `colorful_infographic` (default), `sketch`, `photorealistic`, `minimalist`, `claymation`, `pixel_art`
    - **アスペクト比**: `16:9` (default), `1:1`, `4:3`, `3:4`, `9:16`, `21:9`

2.  **ツールの実行**:
    以下の形式でコマンドを実行してください。長いテキストの場合は全体をクォートで囲むか、そのまま渡してください（ツール側で結合されます）。
    ```bash
    python .cursor/tools/generate_diagram.py "{テーマ/内容}" --style "{スタイル}" --aspect_ratio "{アスペクト比}"
    ```

3.  **結果の確認**:
    - 生成された画像のパスを確認し、ユーザーに報告してください。
    - エラーが発生した場合は、エラーメッセージを表示してください。

## 使用例

- 基本的な使用:
  `/generate-diagram 光合成の仕組み`

- 長文の可視化:
  `/generate-diagram "Gemini 3 Proは、推論機能を備えた新しいAIモデルです。思考プロセスを経て回答を生成するため、複雑なタスクにも対応できます。画像生成モデルであるNano Banana Proも提供されており..." --style minimalist`

- ファイルからの生成（Agentがファイルを読み込んで渡す場合など）:
  ※ Agentはファイル内容を読み取って引数として渡すか、直接 `python .cursor/tools/generate_diagram.py --file path/to/file.txt` を実行してください。
