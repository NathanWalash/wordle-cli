"""Tests for wordle-cli scoring and guess validation (no network needed)."""

from wordle.cli import (
    score,
    is_valid_guess,
    load_words,
    load_answers,
    normalize_code,
    generate_code,
    word_from_code,
    CODE_ALPHABET,
    CODE_LEN,
)


def test_all_correct():
    assert score("crane", "crane") == ["green"] * 5


def test_all_absent():
    assert score("fizzy", "crane") == ["gray"] * 5


def test_present_but_misplaced():
    # brick vs crane: r is exact (green); c is present but misplaced (yellow).
    assert score("brick", "crane") == ["gray", "green", "gray", "yellow", "gray"]


def test_duplicate_letters_limited_to_count():
    # "stars" has two s's; the extra s in "sassy" beyond those must go gray.
    assert score("sassy", "stars") == ["green", "yellow", "yellow", "gray", "gray"]


def test_bundled_word_list_loads():
    words = load_words()
    assert words is not None
    assert "crane" in words
    assert len(words) > 10000


def test_valid_guess_accepts_real_word():
    words = {"crane", "stare"}
    assert is_valid_guess("crane", words, "pluck") is True


def test_valid_guess_rejects_nonword():
    words = {"crane", "stare"}
    assert is_valid_guess("zzzzz", words, "pluck") is False


def test_valid_guess_always_allows_solution():
    words = {"crane"}
    assert is_valid_guess("pluck", words, "pluck") is True


def test_valid_guess_accepts_anything_without_list():
    assert is_valid_guess("zzzzz", None, "pluck") is True


def test_valid_guess_rejects_wrong_shape():
    assert is_valid_guess("cat", {"cat12"}, "pluck") is False
    assert is_valid_guess("cr4ne", None, "pluck") is False


# --- practice / share-code logic ---

SAMPLE = ["apple", "brave", "crane", "dwell", "eagle", "flint"]


def test_same_code_gives_same_word():
    assert word_from_code("K7Q2MX", SAMPLE) == word_from_code("K7Q2MX", SAMPLE)


def test_code_is_case_and_separator_insensitive():
    assert word_from_code("k7q2mx", SAMPLE) == word_from_code("K7Q2-MX", SAMPLE)


def test_word_from_code_is_in_pool():
    for code in ("ABC234", "ZZZZZZ", "Q9R8T7"):
        assert word_from_code(code, SAMPLE) in SAMPLE


def test_different_codes_usually_differ():
    words = {word_from_code(c, SAMPLE) for c in ("AAAAAA", "BBBBBB", "CCCCCC", "DDDDDD")}
    assert len(words) > 1  # not all collapsing to one word


def test_normalize_strips_ambiguous_and_symbols():
    assert normalize_code("k7-q2 mx!") == "K7Q2MX"


def test_generate_code_shape():
    code = generate_code()
    assert len(code) == CODE_LEN
    assert all(c in CODE_ALPHABET for c in code)


def test_answers_list_loads():
    answers = load_answers()
    assert answers is not None
    assert "crane" in answers
    assert answers == sorted(answers)  # stable order for deterministic codes
