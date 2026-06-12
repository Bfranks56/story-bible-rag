"""
Unit tests for file I/O helpers — save_draft_content and search_web.
External dependencies (OpenAI, DDGS) are mocked.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import chat       # noqa: E402
import web_search  # noqa: E402


# ─── save_draft_content ───────────────────────────────────────────────────────

def test_save_draft_content_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    filename = chat.save_draft_content("## New Scene\nSomething happens.", "NERINA")
    assert os.path.exists(filename)

def test_save_draft_content_correct_content(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    content = "## Battle Scene\nNerina wins."
    filename = chat.save_draft_content(content, "NERINA")
    with open(filename) as f:
        assert f.read() == content

def test_save_draft_content_filename_contains_character(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    filename = chat.save_draft_content("stuff", "TOMAS")
    assert "TOMAS" in filename

def test_save_draft_content_filename_contains_timestamp(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    filename = chat.save_draft_content("stuff", "GENERAL")
    # Timestamp format: YYYYMMDD_HHMMSS
    import re
    assert re.search(r"\d{8}_\d{6}", filename)

def test_save_draft_content_general_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    filename = chat.save_draft_content("stuff")
    assert "GENERAL" in filename


# ─── web_search.search_web ────────────────────────────────────────────────────

def test_search_web_returns_list_of_dicts():
    mock_result = [{"title": "Gundam", "body": "A mech show.", "href": "http://example.com"}]
    with patch("web_search.DDGS") as MockDDGS:
        instance = MockDDGS.return_value
        instance.text.return_value = mock_result
        results = web_search.search_web("gundam history", max_results=1)

    assert isinstance(results, list)
    assert results[0]["title"] == "Gundam"
    assert results[0]["snippet"] == "A mech show."
    assert results[0]["url"] == "http://example.com"

def test_search_web_respects_max_results():
    mock_results = [
        {"title": f"Result {i}", "body": "body", "href": "http://example.com"}
        for i in range(5)
    ]
    with patch("web_search.DDGS") as MockDDGS:
        instance = MockDDGS.return_value
        instance.text.return_value = mock_results[:2]
        results = web_search.search_web("anything", max_results=2)

    assert len(results) == 2

def test_search_web_returns_empty_list_on_exception():
    with patch("web_search.DDGS") as MockDDGS:
        instance = MockDDGS.return_value
        instance.text.side_effect = Exception("network error")
        results = web_search.search_web("anything")

    assert results == []
