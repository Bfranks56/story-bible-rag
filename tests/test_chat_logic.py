"""
Unit tests for pure logic helpers in chat.py — no OpenAI or FAISS calls.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import chat  # noqa: E402


# ─── _has_triggers ─────────────────────────────────────────────────────────────

def test_has_triggers_matches_substring():
    assert chat._has_triggers("How does this compare to Wing Zero?", ["compare"])

def test_has_triggers_is_case_insensitive():
    assert chat._has_triggers("GUNDAM pilot style", ["gundam"])

def test_has_triggers_no_match():
    assert not chat._has_triggers("Tell me about Nerina's past", ["gundam", "evangelion"])

def test_has_triggers_empty_query():
    assert not chat._has_triggers("", ["gundam"])


# ─── should_search_web ────────────────────────────────────────────────────────

def test_should_search_web_triggers_on_vs():
    assert chat.should_search_web("Wing Zero vs Evangelion")

def test_should_search_web_triggers_on_gundam():
    assert chat.should_search_web("What gundam inspired Black Horizon?")

def test_should_search_web_no_trigger_for_story_query():
    assert not chat.should_search_web("What is Nerina's pilot style?")

def test_should_search_web_triggers_on_similar_to():
    assert chat.should_search_web("What shows are similar to Black Horizon?")


# ─── should_generate_content ──────────────────────────────────────────────────

def test_should_generate_content_plain_expand():
    assert chat.should_generate_content("Expand on Nerina's backstory")

def test_should_generate_content_plain_develop():
    assert chat.should_generate_content("Develop Tomas's relationship arc")

def test_should_generate_content_info_word_blocks_trigger():
    # "what" is an info word; "missing" is a generation trigger but NOT in the
    # explicit override list, so the info word wins → False
    assert not chat.should_generate_content("What is this story missing?")

def test_should_generate_content_info_word_with_explicit_expand():
    # "what" + "expand" = explicit override
    assert chat.should_generate_content("What would you expand on here?")

def test_should_generate_content_plain_story_query():
    assert not chat.should_generate_content("Who is Dashiel?")

def test_should_generate_content_create_blocked_by_how():
    # "how" is an info word; "create" is a generation trigger but NOT in the
    # explicit override list [expand, elaborate, develop, add to] → False
    assert not chat.should_generate_content("How should we create this character?")


# ─── detect_character_name ────────────────────────────────────────────────────

def test_detect_character_name_from_query():
    assert chat.detect_character_name("Tell me about Nerina", []) == "NERINA"

def test_detect_character_name_case_insensitive():
    assert chat.detect_character_name("what's tomas doing?", []) == "TOMAS"

def test_detect_character_name_from_search_result_file():
    results = [{"file": "Character_Bible_FRED_v1.10.md", "header": "Origins"}]
    assert chat.detect_character_name("describe this character", results) == "FRED"

def test_detect_character_name_query_takes_priority():
    results = [{"file": "Character_Bible_FRED_v1.10.md", "header": "Origins"}]
    assert chat.detect_character_name("What about Dashiel though?", results) == "DASHIEL"

def test_detect_character_name_falls_back_to_general():
    assert chat.detect_character_name("Tell me about the war", []) == "GENERAL"

def test_detect_character_name_no_results_no_match():
    assert chat.detect_character_name("interesting worldbuilding", []) == "GENERAL"


# ─── _build_context_sections ──────────────────────────────────────────────────

def test_build_context_sections_formats_correctly():
    results = [{"header": "Pilot Style", "content": "Nerina flies with grace."}]
    out = chat._build_context_sections(results, "STORY BIBLE", ("header", "content"))
    assert "[STORY BIBLE | Pilot Style]" in out
    assert "Nerina flies with grace." in out

def test_build_context_sections_skips_empty_header():
    results = [{"header": "", "content": "some content"}]
    out = chat._build_context_sections(results, "STORY BIBLE", ("header", "content"))
    assert out == ""

def test_build_context_sections_multiple_joined_by_separator():
    results = [
        {"header": "Origins", "content": "Born in the void."},
        {"header": "Personality", "content": "Quiet but fierce."},
    ]
    out = chat._build_context_sections(results, "STORY BIBLE", ("header", "content"))
    assert "---" in out
    assert "Origins" in out
    assert "Personality" in out

def test_build_context_sections_web_key_map():
    results = [{"title": "Gundam article", "snippet": "A classic mech series."}]
    out = chat._build_context_sections(results, "WEB", ("title", "snippet"))
    assert "[WEB | Gundam article]" in out
    assert "A classic mech series." in out


# ─── build_context_prompt ─────────────────────────────────────────────────────

def test_build_context_prompt_contains_question():
    results = [{"header": "Pilot Style", "content": "Grace in motion."}]
    prompt = chat.build_context_prompt("How does Nerina pilot?", results)
    assert "How does Nerina pilot?" in prompt

def test_build_context_prompt_includes_bible_context():
    results = [{"header": "Origins", "content": "Born in war."}]
    prompt = chat.build_context_prompt("Tell me about origins", results)
    assert "STORY BIBLE CONTEXT" in prompt

def test_build_context_prompt_no_web_results_excludes_external():
    results = [{"header": "Origins", "content": "Born in war."}]
    prompt = chat.build_context_prompt("Origins?", results, web_results=None)
    assert "EXTERNAL CONTEXT" not in prompt

def test_build_context_prompt_with_web_results_includes_external():
    bible_results = [{"header": "Origins", "content": "Born in war."}]
    web_results = [{"title": "Mech history", "snippet": "Mechs evolved over decades."}]
    prompt = chat.build_context_prompt("How did mechs start?", bible_results, web_results)
    assert "EXTERNAL CONTEXT" in prompt
    assert "Mech history" in prompt


# ─── build_expansion_prompt ───────────────────────────────────────────────────

def test_build_expansion_prompt_contains_request():
    results = [{"header": "Backstory", "content": "Lost her home."}]
    prompt = chat.build_expansion_prompt("Expand Nerina's backstory", results)
    assert "Expand Nerina's backstory" in prompt

def test_build_expansion_prompt_contains_existing_content():
    results = [{"header": "Backstory", "content": "Lost her home."}]
    prompt = chat.build_expansion_prompt("Expand on this", results)
    assert "Lost her home." in prompt

def test_build_expansion_prompt_requests_markdown_format():
    results = [{"header": "Arc", "content": "She grows."}]
    prompt = chat.build_expansion_prompt("Develop her arc", results)
    assert "markdown" in prompt.lower()
