"""Tests for wordle-cli scoring and guess validation (no network needed)."""

import pytest

from wordle import __version__
from wordle.cli import (
    main,
    score,
    is_valid_guess,
    hard_mode_error,
    share_grid,
    load_words,
    load_answers,
    normalize_code,
    generate_code,
    word_from_code,
    CODE_ALPHABET,
    CODE_LEN,
)


def test_version_flag_prints_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


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


# --- hard mode ---

# After guessing "brick" vs "crane": r is green at index 1, c is present.
HARD_HISTORY = [("brick", ["gray", "green", "gray", "yellow", "gray"])]


def test_hard_mode_no_history_is_ok():
    assert hard_mode_error("crane", []) is None


def test_hard_mode_enforces_green_position():
    assert "2nd letter must be R" in hard_mode_error("plumb", HARD_HISTORY)


def test_hard_mode_enforces_present_letter():
    # 'r' is in place but the required 'c' is missing.
    assert "must use C" in hard_mode_error("trade", HARD_HISTORY)


def test_hard_mode_accepts_conforming_guess():
    assert hard_mode_error("crane", HARD_HISTORY) is None


# --- shareable result grid ---

def test_share_grid_win_shows_count_and_squares():
    grid = share_grid([("crane", ["green"] * 5)], "crane", "1,234")
    assert grid.startswith("Wordle 1,234 1/6")
    assert "\U0001f7e9\U0001f7e9\U0001f7e9\U0001f7e9\U0001f7e9" in grid


def test_share_grid_loss_uses_x():
    history = [("brick", ["gray", "green", "gray", "yellow", "gray"])] * 6
    grid = share_grid(history, "crane", "Practice ABC234")
    assert "X/6" in grid
