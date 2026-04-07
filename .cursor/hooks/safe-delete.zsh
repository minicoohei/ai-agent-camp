#!/bin/zsh
# =============================================================================
# Safe Delete Hooks for Zsh
# rm等の破壊的コマンドをgomiに変換する安全機構
# 
# 使用方法: ~/.zshrc に以下を追加
#   source /path/to/.cursor/hooks/safe-delete.zsh
# =============================================================================

# -----------------------------------------------------------------------------
# gomi インストールチェックと自動インストール
# -----------------------------------------------------------------------------
_safe_delete_ensure_gomi() {
    if command -v gomi &> /dev/null; then
        return 0  # インストール済み
    fi

    echo "⚠️  gomi がインストールされていません"
    echo ""
    
    # Homebrew でインストール（macOS）
    if command -v brew &> /dev/null; then
        echo "📦 Homebrew を使用して gomi をインストールしますか? [Y/n]"
        read -r response
        if [[ "$response" =~ ^[Yy]?$ ]]; then
            brew install gomi
            if command -v gomi &> /dev/null; then
                echo "✅ gomi のインストールが完了しました"
                return 0
            fi
        fi
    fi

    # Go でインストール
    if command -v go &> /dev/null; then
        echo "📦 Go を使用して gomi をインストールしますか? [Y/n]"
        read -r response
        if [[ "$response" =~ ^[Yy]?$ ]]; then
            go install github.com/b4b4r07/gomi@latest
            if command -v gomi &> /dev/null; then
                echo "✅ gomi のインストールが完了しました"
                return 0
            fi
        fi
    fi

    # 手動インストール案内
    echo ""
    echo "📋 手動インストール方法:"
    echo "   Homebrew: brew install gomi"
    echo "   Go:       go install github.com/b4b4r07/gomi@latest"
    echo ""
    echo "詳細: https://github.com/b4b4r07/gomi"
    return 1
}

# -----------------------------------------------------------------------------
# rm コマンドを gomi に置き換える関数
# -----------------------------------------------------------------------------
rm() {
    # gomi がなければインストールを促す
    if ! command -v gomi &> /dev/null; then
        _safe_delete_ensure_gomi || {
            echo "❌ gomi がインストールされていないため、削除を中止しました"
            return 1
        }
    fi

    local args=()
    local has_recursive=false
    local has_force=false
    local targets=()

    # 引数を解析
    for arg in "$@"; do
        case "$arg" in
            -r|-R|--recursive)
                has_recursive=true
                ;;
            -f|--force)
                has_force=true
                ;;
            -rf|-fr|-Rf|-fR)
                has_recursive=true
                has_force=true
                ;;
            -i|--interactive)
                # gomi では不要（常に安全）
                ;;
            -v|--verbose)
                # gomi では不要
                ;;
            -*)
                # その他のオプションは無視
                ;;
            *)
                targets+=("$arg")
                ;;
        esac
    done

    # 対象がなければエラー
    if [[ ${#targets[@]} -eq 0 ]]; then
        echo "❌ 削除対象が指定されていません"
        return 1
    fi

    # 警告メッセージ
    echo ""
    echo "🗑️  安全削除: rm → gomi に変換しました"
    echo ""
    echo "   対象: ${targets[*]}"
    if $has_recursive; then
        echo "   モード: 再帰的削除 (-r)"
    fi
    echo ""
    echo "📂 復元方法: gomi -b"
    echo ""

    # gomi を実行
    if $has_recursive; then
        gomi -r "${targets[@]}"
    else
        gomi "${targets[@]}"
    fi
}

# -----------------------------------------------------------------------------
# rmdir コマンドを gomi に置き換える関数
# -----------------------------------------------------------------------------
rmdir() {
    # gomi がなければインストールを促す
    if ! command -v gomi &> /dev/null; then
        _safe_delete_ensure_gomi || {
            echo "❌ gomi がインストールされていないため、削除を中止しました"
            return 1
        }
    fi

    echo ""
    echo "🗑️  安全削除: rmdir → gomi に変換しました"
    echo ""
    echo "   対象: $*"
    echo ""
    echo "📂 復元方法: gomi -b"
    echo ""

    gomi "$@"
}

# -----------------------------------------------------------------------------
# shred コマンドをブロック
# -----------------------------------------------------------------------------
shred() {
    echo ""
    echo "🚫 shred コマンドは使用できません"
    echo ""
    echo "   shred はファイルを復元不可能に削除するコマンドです。"
    echo "   代わりに gomi を使用してください。"
    echo ""
    echo "   使用方法: gomi $*"
    echo ""
    return 1
}

# -----------------------------------------------------------------------------
# 初期化時にgomiの存在確認（警告のみ、インストールは促さない）
# -----------------------------------------------------------------------------
if ! command -v gomi &> /dev/null; then
    echo ""
    echo "⚠️  [safe-delete] gomi がインストールされていません"
    echo "   rm/rmdir コマンド実行時にインストールを促します"
    echo ""
fi

# -----------------------------------------------------------------------------
# ヘルプ関数
# -----------------------------------------------------------------------------
safe_delete_help() {
    echo ""
    echo "🛡️  Safe Delete Hooks"
    echo ""
    echo "このスクリプトは rm, rmdir, shred コマンドを安全な gomi に変換します。"
    echo ""
    echo "変換ルール:"
    echo "   rm file.txt      → gomi file.txt"
    echo "   rm -rf dir/      → gomi -r dir/"
    echo "   rmdir dir/       → gomi dir/"
    echo "   shred file.txt   → ブロック（使用不可）"
    echo ""
    echo "gomi コマンド:"
    echo "   gomi file.txt    ファイルをゴミ箱へ移動"
    echo "   gomi -r dir/     ディレクトリを再帰的にゴミ箱へ移動"
    echo "   gomi -b          ゴミ箱の中身を表示（復元UI）"
    echo ""
}




