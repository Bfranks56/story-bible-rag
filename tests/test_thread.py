"""
Unit tests for thread persistence functions.
"""

import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import chat  # noqa: E402 — must come after sys.path insert


# ─── generate_thread_id ────────────────────────────────────────────────────────

def test_generate_thread_id_is_12_chars():
    tid = chat.generate_thread_id()
    assert len(tid) == 12

def test_generate_thread_id_is_hex():
    tid = chat.generate_thread_id()
    int(tid, 16)  # raises ValueError if not valid hex

def test_generate_thread_id_is_unique():
    ids = {chat.generate_thread_id() for _ in range(100)}
    assert len(ids) == 100


# ─── initialize_thread ─────────────────────────────────────────────────────────

def test_initialize_thread_has_required_keys():
    thread = chat.initialize_thread("abc123")
    assert "thread_id" in thread
    assert "created_at" in thread
    assert "turns" in thread

def test_initialize_thread_stores_id():
    thread = chat.initialize_thread("myid")
    assert thread["thread_id"] == "myid"

def test_initialize_thread_starts_with_empty_turns():
    thread = chat.initialize_thread("myid")
    assert thread["turns"] == []

def test_initialize_thread_created_at_is_iso_string():
    import datetime
    thread = chat.initialize_thread("myid")
    # Should parse without error
    datetime.datetime.fromisoformat(thread["created_at"])


# ─── _make_turn ────────────────────────────────────────────────────────────────

def test_make_turn_has_contract_fields():
    turn = chat._make_turn("user", "Who is Nerina?")
    for field in ("timestamp", "role", "content", "type", "characters", "tokens"):
        assert field in turn

def test_make_turn_defaults():
    turn = chat._make_turn("user", "Hello")
    assert turn["type"] == "story_query"
    assert turn["characters"] == []
    assert turn["tokens"] == 0

def test_make_turn_custom_values():
    turn = chat._make_turn("assistant", "She is a pilot.", "expansion", ["NERINA"], 42)
    assert turn["role"] == "assistant"
    assert turn["type"] == "expansion"
    assert turn["characters"] == ["NERINA"]
    assert turn["tokens"] == 42

def test_make_turn_characters_default_does_not_share_state():
    # Mutable default argument guard
    t1 = chat._make_turn("user", "A")
    t2 = chat._make_turn("user", "B")
    t1["characters"].append("NERINA")
    assert t2["characters"] == []


# ─── save_thread / load_thread ─────────────────────────────────────────────────

def test_save_and_load_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(chat, "THREADS_DIR", str(tmp_path))

    thread = chat.initialize_thread("test001")
    thread["turns"].append(chat._make_turn("user", "Who is Tomas?"))
    chat.save_thread(thread)

    loaded = chat.load_thread("test001")
    assert loaded["thread_id"] == "test001"
    assert len(loaded["turns"]) == 1
    assert loaded["turns"][0]["content"] == "Who is Tomas?"

def test_save_thread_creates_valid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(chat, "THREADS_DIR", str(tmp_path))

    thread = chat.initialize_thread("jsoncheck")
    chat.save_thread(thread)

    path = tmp_path / "jsoncheck.json"
    assert path.exists()
    with open(path) as f:
        data = json.load(f)
    assert data["thread_id"] == "jsoncheck"

def test_load_thread_returns_none_for_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(chat, "THREADS_DIR", str(tmp_path))
    result = chat.load_thread("doesnotexist")
    assert result is None

def test_save_thread_overwrites_on_second_save(tmp_path, monkeypatch):
    monkeypatch.setattr(chat, "THREADS_DIR", str(tmp_path))

    thread = chat.initialize_thread("overwrite")
    thread["turns"].append(chat._make_turn("user", "First question"))
    chat.save_thread(thread)

    thread["turns"].append(chat._make_turn("assistant", "First answer"))
    chat.save_thread(thread)

    loaded = chat.load_thread("overwrite")
    assert len(loaded["turns"]) == 2

def test_save_thread_creates_directory_if_missing(tmp_path, monkeypatch):
    nested = tmp_path / "deeply" / "nested"
    monkeypatch.setattr(chat, "THREADS_DIR", str(nested))

    thread = chat.initialize_thread("newdir")
    chat.save_thread(thread)  # should not raise

    assert (nested / "newdir.json").exists()
