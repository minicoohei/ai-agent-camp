# テスト Rules

## 方針
- 教材 repo では、学習者導線を壊さないことを優先する
- 実装変更時は、関連する既存テストや検証スクリプトを回す
- docs や skill を変えた時も、主要導線の整合性を確認する

## よく使う確認
```bash
pytest tests/test_check_agent_docs.py -v
pytest tests/test_check_command_paths.py -v
pytest tests/security/ -v
```

## 文書変更時の確認観点
- Codex / Claude Code / Cursor の説明が矛盾していないか
- lesson id や entry path の案内が壊れていないか
- 安全ルールが docs 間で食い違っていないか

## 命名の基本
- Python テストは `test_<subject>.py`
- テスト関数は `test_<behavior>`
