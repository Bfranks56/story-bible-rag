"""
Tests covering Phase 0 fixes:
  0.1 - ingest.py embeddings scope bug
  0.2 - MODEL constant in chat.py
  0.3 - tokens wired from API response
  0.4 - search.py raises NotImplementedError
  0.5 - FAISS index module-level cache
"""

import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import chat    # noqa: E402
import ingest  # noqa: E402
import search  # noqa: E402


# ─── 0.1  ingest.py embeddings scope bug ──────────────────────────────────────

def test_parse_markdown_no_embeds_does_not_raise(tmp_path, monkeypatch):
    """get_embeds=False must not raise NameError for undefined `embeddings`."""
    monkeypatch.setattr("time.sleep", lambda _: None)
    md = tmp_path / "test.md"
    md.write_text("# Header One\nSome content here.\n\n# Header Two\nMore content.\n")
    sections = ingest.parse_markdown_file(str(md), get_embeds=False)
    assert isinstance(sections, list)
    assert len(sections) > 0
    assert "embedding" not in sections[0]


def test_parse_markdown_embeds_stored_when_api_returns_data(tmp_path, monkeypatch):
    """Embeddings are attached to sections when batch API call succeeds."""
    monkeypatch.setattr("time.sleep", lambda _: None)
    fake_vector = [0.1] * 10
    monkeypatch.setattr(ingest, "get_embeddings_batch", lambda texts, **kw: [fake_vector] * len(texts))

    md = tmp_path / "test.md"
    md.write_text("# Pilot Style\nFlying fast.\n")
    sections = ingest.parse_markdown_file(str(md), get_embeds=True)
    assert sections[0]["embedding"] == fake_vector


def test_parse_markdown_embeds_skipped_when_api_returns_none(tmp_path, monkeypatch):
    """If the batch API call returns None, sections are returned without embeddings."""
    monkeypatch.setattr("time.sleep", lambda _: None)
    monkeypatch.setattr(ingest, "get_embeddings_batch", lambda texts, **kw: None)

    md = tmp_path / "test.md"
    md.write_text("# Origins\nBorn in war.\n")
    sections = ingest.parse_markdown_file(str(md), get_embeds=True)
    assert isinstance(sections, list)
    assert "embedding" not in sections[0]


# ─── 0.2  MODEL constant ──────────────────────────────────────────────────────

def test_model_constant_exists():
    assert hasattr(chat, "MODEL")

def test_model_constant_is_string():
    assert isinstance(chat.MODEL, str)

def test_model_constant_value():
    assert chat.MODEL == "gpt-4o-mini"


# ─── 0.3  tokens wired from API response ─────────────────────────────────────

def test_call_openai_chat_returns_tuple(monkeypatch):
    """`_call_openai_chat` must return (content, tokens) not just content."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Test response"
    mock_response.usage.total_tokens = 55

    monkeypatch.setattr(chat.client.chat.completions, "create", lambda **kw: mock_response)

    result = chat._call_openai_chat("some prompt")
    assert isinstance(result, tuple), "_call_openai_chat should return a tuple"
    content, tokens = result
    assert content == "Test response"
    assert tokens == 55


def test_call_openai_chat_tokens_zero_when_usage_missing(monkeypatch):
    """If usage is None/falsy, tokens defaults to 0."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello"
    mock_response.usage = None

    monkeypatch.setattr(chat.client.chat.completions, "create", lambda **kw: mock_response)

    _, tokens = chat._call_openai_chat("prompt")
    assert tokens == 0


def test_make_turn_tokens_populated():
    """_make_turn correctly stores the token count passed in."""
    turn = chat._make_turn("assistant", "some content", tokens=123)
    assert turn["tokens"] == 123


# ─── 0.4  search.py raises NotImplementedError ────────────────────────────────

def test_search_content_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        search.search_content("Nerina core values")


# ─── 0.5  FAISS index module-level cache ─────────────────────────────────────

def test_load_index_returns_cached_values(monkeypatch):
    """When _INDEX and _METADATA are already set, faiss.read_index is not called."""
    sentinel_index = object()
    sentinel_meta = [{"header": "cached", "content": "data"}]

    monkeypatch.setattr(chat, "_INDEX", sentinel_index)
    monkeypatch.setattr(chat, "_METADATA", sentinel_meta)

    disk_reads = {"n": 0}
    def mock_read_index(path):
        disk_reads["n"] += 1
        return sentinel_index

    monkeypatch.setattr(chat.faiss, "read_index", mock_read_index)

    idx, meta = chat.load_index_and_metadata()
    assert idx is sentinel_index
    assert meta is sentinel_meta
    assert disk_reads["n"] == 0, "faiss.read_index should not be called when cache is warm"


def test_load_index_populates_cache_on_first_call(monkeypatch, tmp_path):
    """First call with empty cache should read from disk and populate _INDEX/_METADATA."""
    import pickle

    monkeypatch.setattr(chat, "_INDEX", None)
    monkeypatch.setattr(chat, "_METADATA", None)

    mock_index = MagicMock()
    mock_meta = [{"header": "test"}]

    # Write real pickle so open() works without patching builtins
    pkl_path = tmp_path / "metadata.pkl"
    with open(pkl_path, "wb") as f:
        pickle.dump(mock_meta, f)

    # Mock faiss so it doesn't need a real index file
    monkeypatch.setattr(chat.faiss, "read_index", lambda path: mock_index)

    idx, meta = chat.load_index_and_metadata(base_path=str(tmp_path) + "/")

    assert idx is mock_index
    assert meta == mock_meta
    assert chat._INDEX is mock_index
    assert chat._METADATA == mock_meta
