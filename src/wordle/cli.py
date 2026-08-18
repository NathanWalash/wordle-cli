#!/usr/bin/env python3
"""wordle-cli — play the day's NYT Wordle in your terminal.

No accounts, no browser tab. The answer is fetched from NYT's public puzzle
endpoint (the same JSON your browser downloads before you guess).
"""

import argparse
import datetime
import json
import sys
import urllib.request
from collections import Counter
from importlib import resources

WORD_LEN = 5
MAX_GUESSES = 6
ENDPOINT = "https://www.nytimes.com/svc/wordle/v2/{date}.json"

# ANSI styling.
RESET = "\033[0m"
DIM = "\033[2m"
# Guess-tile feedback colours (bright bg + dark text), like the real tiles.
GREEN = "\033[42;30m"
YELLOW = "\033[43;30m"
GRAY = "\033[100;97m"
BG = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}
# Keyboard keys: two greys only — used (dark) vs unused (light).
KEY_USED = "\033[100;97m"
KEY_UNUSED = "\033[47;30m"

CLEAR = "\033[2J\033[3J\033[H"
KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")
KEYBOARD_INDENT = ("", " ", "   ")  # staggered like a real keyboard


def load_words():
    """Return the set of valid guess words, or None if unavailable."""
    try:
        text = resources.files("wordle").joinpath("words.txt").read_text()
    except (FileNotFoundError, ModuleNotFoundError, OSError):
        return None
    words = {w.strip().lower() for w in text.split() if w.strip()}
    return words or None


def fetch_solution(date):
    """Return the day's five-letter solution, lowercased."""
    url = ENDPOINT.format(date=date)
    req = urllib.request.Request(url, headers={"User-Agent": "wordle-cli"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.load(resp)
    return data["solution"].lower()


def score(guess, solution):
    """Return a list of 'green' / 'yellow' / 'gray' per letter (Wordle rules)."""
    result = ["gray"] * WORD_LEN
    remaining = Counter(solution)

    # First pass: exact matches.
    for i, ch in enumerate(guess):
        if ch == solution[i]:
            result[i] = "green"
            remaining[ch] -= 1

    # Second pass: present-but-misplaced, respecting remaining counts.
    for i, ch in enumerate(guess):
        if result[i] == "green":
            continue
        if remaining[ch] > 0:
            result[i] = "yellow"
            remaining[ch] -= 1

    return result


def is_valid_guess(guess, words, solution):
    """A guess is valid if it's the right shape and a known word (or the answer)."""
    if len(guess) != WORD_LEN or not guess.isalpha():
        return False
    if words is None:
        return True  # no word list available -> accept any 5-letter word
    return guess in words or guess == solution


def render_guess(guess, marks):
    return "".join(f"{BG[m]} {ch.upper()} {RESET}" for ch, m in zip(guess, marks))


def empty_row():
    return "".join(f"{DIM} · {RESET}" for _ in range(WORD_LEN))


def keyboard_lines(used):
    """Three staggered rows; used letters dark grey, unused light grey."""
    lines = []
    for indent, row in zip(KEYBOARD_INDENT, KEYBOARD_ROWS):
        keys = "".join(
            f"{KEY_USED if ch in used else KEY_UNUSED} {ch.upper()} {RESET}"
            for ch in row
        )
        lines.append(indent + keys)
    return lines


def draw(history, used, show_keyboard, date):
    """Redraw the whole board, with the keyboard panel to its right."""
    lines = [CLEAR, f"  Wordle · {date}", ""]
    kb = keyboard_lines(used) if show_keyboard else []
    kb_start = (MAX_GUESSES - len(KEYBOARD_ROWS)) // 2  # vertically centre it

    for r in range(MAX_GUESSES):
        left = render_guess(*history[r]) if r < len(history) else empty_row()
        right = ""
        if show_keyboard and 0 <= r - kb_start < len(kb):
            right = "    " + kb[r - kb_start]
        lines.append(("  " + left + right).rstrip())

    print("\n".join(lines) + "\n")


def make_hint(solution):
    vowels = sum(1 for c in solution if c in "aeiou")
    uniq = len(set(solution))
    return (
        f"Hint: starts with '{solution[0].upper()}', "
        f"{vowels} vowel(s), {uniq} unique letter(s)."
    )


def play(solution, date, show_keyboard, words):
    history = []       # list of (guess, marks)
    used = set()       # letters guessed so far
    notice = ""

    while len(history) < MAX_GUESSES:
        draw(history, used, show_keyboard, date)
        if notice:
            print(f"  {notice}")
            notice = ""

        attempt = len(history) + 1
        try:
            guess = input(f"  [{attempt}/{MAX_GUESSES}] > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            return 0

        if len(guess) != WORD_LEN or not guess.isalpha():
            notice = f"...enter a {WORD_LEN}-letter word."
            continue
        if not is_valid_guess(guess, words, solution):
            notice = f"...'{guess}' is not in the word list."
            continue

        marks = score(guess, solution)
        history.append((guess, marks))
        used.update(guess)

        if guess == solution:
            draw(history, used, show_keyboard, date)
            print(f"  Got it in {len(history)}! ")
            return 0

    draw(history, used, show_keyboard, date)
    print(f"  Out of guesses. The word was: {solution.upper()}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="wordle", description="Play the day's NYT Wordle in your terminal."
    )
    parser.add_argument(
        "--solve", action="store_true", help="reveal today's answer and exit"
    )
    parser.add_argument(
        "--hint", action="store_true", help="print a small hint and exit"
    )
    parser.add_argument(
        "-n",
        "--no-keyboard",
        action="store_true",
        help="hide the QWERTY letter tracker (shown by default)",
    )
    args = parser.parse_args(argv)

    date = datetime.date.today().isoformat()
    try:
        solution = fetch_solution(date)
    except Exception as exc:  # network / parsing issues
        print(f"Couldn't fetch today's word: {exc}", file=sys.stderr)
        return 1

    if args.solve:
        print(solution.upper())
        return 0
    if args.hint:
        print(make_hint(solution))
        return 0

    return play(solution, date, show_keyboard=not args.no_keyboard, words=load_words())


if __name__ == "__main__":
    sys.exit(main())
