"""
サンプルデータの決定論的テスト。

外部ファイルに依存せず、インラインのフィクスチャデータで構造を検証する。
"""
import pytest
import json


@pytest.fixture
def inline_slack_data():
    """Slackサンプルデータ（インライン）"""
    return {
        "channel": "general",
        "messages": [
            {"user": "U001", "text": "こんにちは", "ts": "1700000000.000001"},
            {"user": "U002", "text": "お疲れさまです", "ts": "1700000001.000002"},
        ],
    }


@pytest.fixture
def inline_gmail_data():
    """Gmailサンプルデータ（インライン）"""
    return {
        "emails": [
            {"from": "alice@example.com", "subject": "テスト", "body": "本文"},
            {"from": "bob@example.com", "subject": "確認", "body": "よろしく"},
        ],
    }


def test_slack_sample_structure(inline_slack_data):
    """Slackサンプルデータの構造確認"""
    assert "channel" in inline_slack_data
    assert "messages" in inline_slack_data
    assert isinstance(inline_slack_data["messages"], list)
    assert len(inline_slack_data["messages"]) > 0


def test_gmail_sample_structure(inline_gmail_data):
    """Gmailサンプルデータの構造確認"""
    assert "emails" in inline_gmail_data
    assert isinstance(inline_gmail_data["emails"], list)
    assert len(inline_gmail_data["emails"]) > 0
