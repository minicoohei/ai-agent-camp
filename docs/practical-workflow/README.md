# 実務演習：変更を残し、手順を再利用し、確かめて直す

架空の「青空商事」の見積確認を題材に、GitHub・Skills・反復ループ・デザインシステムをつなげます。会社名、金額、案件はすべて演習用です。実際の顧客資料やアカウント画面は使いません。

## 何ができるようになるか

| 順番 | 演習 | 時間の目安 | 提出物・合格条件 |
| --- | --- | --- | --- |
| 1 | [GitHubで変更をレビューする](01-github.md) | 45分 | 作業ブランチ、差分、PR本文。オンライン実施時は自分のPrivateリポジトリのPRとChecks |
| 2 | [Skillsを別の入力へ再利用する](02-skills.md) | 30分 | 同じSkillによる2件の確認結果と、根拠の照合記録 |
| 3 | [測って直すループを回す](03-iteration.md) | 30分 | 固定4テストの結果、最大3回の修正記録、停止理由 |
| 4 | [デザインシステムを作る](04-design-system.md) | 45分 | 色・文字・余白のルール、共通部品、4状態、見た目と機能を分けた確認表 |

150分は演習部分の目安です。初回のGit・Python・GitHub認証の準備時間と休憩は別に取ります。講師が1回実演し、受講者が同じ操作を行い、各節のチェックリストで止まって確認します。

## 開始前の準備

1. Campのセットアップを終え、[安全ガイド](../codex-safety.md)を読みます。Git、Python 3.10以上、ファイルを読めるAIの作業環境を用意します。GitHub実習では自分のアカウントも必要です。
2. 教材は読む場所、演習は書く場所に分けます。Campの隣に新しい `camp-practice` フォルダを作り、[starter](starter/) の中身だけをコピーします。隠しファイルの `.gitignore` も含めます。`.git` や教材全体はコピーしません。同名フォルダがあれば上書きせず、別名を選びます。
3. AIで `camp-practice` を開き直します。ターミナルの `pwd`（Windows PowerShellでは `Get-Location`）と、AI画面の作業フォルダを照合します。以後のコマンドは、このフォルダを起点に実行します。
4. `python3 --version`、`git --version` を確認します。Windowsで `python3` がなければ、以後の `python3` を `py -3` に読み替えます。

AIへの依頼文（チャット欄へ貼る）：

```text
この教材の docs/practical-workflow/starter の中身（隠しファイルの .gitignore を含む）を、教材フォルダの隣の新規 camp-practice へコピーしてください。
同名フォルダがあれば止まってください。教材原本は変更せず、.git、個人設定、認証情報を持ち込まないでください。
コピー元とコピー先、コピーしたファイル一覧を報告してください。GitHubへの送信はまだ行いません。
```

### ツールごとの入口

| ツール | 依頼する場所 | この演習でのSkillの読み方 |
| --- | --- | --- |
| Codex | `camp-practice` を開いたタスク | `skills/quote-review/SKILL.md` をパスで指定して読む |
| Claude Code | `camp-practice` を開いたチャット／Codeタブ | 同じパスを指定して読む。自動検出に依存しない |
| Cursor | `camp-practice` を開いたAgentチャット | 同じパスを指定して読む。Markdownをシェルで実行しない |

この共通手順ではMCP、APIキー、追加プラグインを必要としません。接続設定の有無を学習達成条件にしません。

## 元の章との使い分け

| 既存の章 | 既存内容をそのまま使う部分 | この演習で補う部分 |
| --- | --- | --- |
| [基礎・エージェント](../../courses/aiagent/lesson01-foundation/ch03-agents/practice/reference.md) | 観察→判断→行動の概念 | 実行結果を次の修正へ渡し、数値と回数で止める |
| [Module 6](../../courses/aiagent/lesson03-core/module06-agent-development/practice/exercise.md) | Command・Skill・Agentの作成 | Skillの手順と案件入力を分離し、2件目で再利用を検証する |
| [Module 11](../../courses/aiagent/lesson03-core/module11-github-actions/practice/exercise.md) | CI/CD、定期実行、Secrets | 保存・commit・push・PR・mergeの違いと最初のPR、run→job→logの確認 |
| [Module 18](../../courses/aiagent/lesson03-core/module18-pm-sysdef/practice/exercise.md) | PRD・設計・プロトタイプ・テスト | デザインルールを部品と状態へ落とし、AIに渡して照合する |

新しい章番号やスラッシュコマンドは追加しません。Module 11の前提が難しい場合は演習1から、Module 6の作成後には演習2、Module 18の画面設計では演習4を使います。公開サイトのページ内容とは別に、このリポジトリのMarkdownを開いて進めてください。

## 講師の進行と提出

各演習で「操作場所→入力→見える結果→成功条件」の順に説明します。待ち時間は2分までとし、止まった受講者には再開する節と残るエラーを記録してもらいます。講師の成功を受講者本人の成功として記録しません。

最後に `evidence/summary.md` を作り、各演習の合否、成果物の相対パス、実行コマンドと結果、未完了箇所、次の一手を記載します。オンライン未実施なら「ローカル完了・GitHub未実施」、AI未実行なら「手順の確認のみ」と区別します。

- [ ] 作業フォルダを自分で示せる
- [ ] GitHubへの送信とローカル保存の違いを説明できる
- [ ] 同じSkillを別入力に使った根拠がある
- [ ] 失敗時も上限で止まり、再開位置が残る
- [ ] 画面の見た目と機能の確認結果を分けている
- [ ] 顧客名、メール、秘密値、内部URL、原本の画像を含めていない
