"""Tests for wordle-cli scoring and guess validation (no network needed)."""

from wordle.cli import score, is_valid_guess, load_words


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
