#!/usr/bin/env python3
"""wordle-cli — play the day's NYT Wordle in your terminal.

No accounts, no browser tab. The daily answer is fetched from NYT's public
puzzle endpoint (the same JSON your browser downloads before you guess).
Practice mode plays offline from a bundled word list and can be shared with a
code so friends get the same word.
"""

import argparse
import datetime
import hashlib
import json
import random
import sys
import urllib.request
from collections import Counter
from importlib import resources

WORD_LEN = 5
MAX_GUESSES = 6
ENDPOINT = "https://www.nytimes.com/svc/wordle/v2/{date}.json"

# Share codes: unambiguous alphabet (no 0/O/1/I/L).
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
CODE_LEN = 6

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
# The one place emoji are used: the copy-paste result grid, so it matches the
# format everyone recognises when shared into a chat.
SQUARES = {"green": "\U0001f7e9", "yellow": "\U0001f7e8", "gray": "⬛"}

CLEAR = "\033[2J\033[3J\033[H"
KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")
KEYBOARD_INDENT = ("", " ", "   ")  # staggered like a real keyboard
ORDINALS = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th"}


def _load_list(filename):
    try:
        text = resources.files("wordle").joinpath(filename).read_text()
    except (FileNotFoundError, ModuleNotFoundError, OSError):
        return None
    words = {w.strip().lower() for w in text.split() if w.strip()}
    return words or None


def load_words():
    """Set of valid guess words (~15k), or None if unavailable."""
    return _load_list("words.txt")


def load_answers():
    """Sorted list of curated answer words for practice, or None."""
    answers = _load_list("answers.txt") or load_words()
    return sorted(answers) if answers else None


def normalize_code(code):
    """Uppercase and keep only alphabet chars, so 'k7q2-mx' == 'K7Q2MX'."""
    return "".join(c for c in code.upper() if c in CODE_ALPHABET)


def generate_code(length=CODE_LEN):
    return "".join(random.choice(CODE_ALPHABET) for _ in range(length))


def word_from_code(code, answers):
    """Deterministically map a share code to a word, unrelated to the code itself."""
    digest = hashlib.sha256(normalize_code(code).encode()).hexdigest()
    return answers[int(digest, 16) % len(answers)]


def fetch_puzzle(date):
    """Return (solution, puzzle_number) for the given date."""
    url = ENDPOINT.format(date=date)
    req = urllib.request.Request(url, headers={"User-Agent": "wordle-cli"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.load(resp)
    return data["solution"].lower(), data.get("days_since_launch")


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


def hard_mode_error(guess, history):
    """Return an error message if the guess ignores revealed hints, else None."""
    greens = {}       # position -> letter that must stay put
    required = set()  # letters revealed present that must be reused
    for past, marks in history:
        for i, (ch, m) in enumerate(zip(past, marks)):
            if m == "green":
                greens[i] = ch
                required.add(ch)
            elif m == "yellow":
                required.add(ch)

    for i, ch in sorted(greens.items()):
        if guess[i] != ch:
            return f"hard mode: {ORDINALS[i + 1]} letter must be {ch.upper()}."
    for ch in sorted(required):
        if ch not in guess:
            return f"hard mode: guess must use {ch.upper()}."
    return None


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


def draw(history, used, show_keyboard, header):
    """Redraw the whole board, with the keyboard panel to its right."""
    lines = [CLEAR, f"  {header}", ""]
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


def share_grid(history, solution, label):
    """Build the copy-paste emoji result grid, in the familiar Wordle format."""
    solved = bool(history) and history[-1][0] == solution
    count = len(history) if solved else "X"
    rows = "\n".join("".join(SQUARES[m] for m in marks) for _, marks in history)
    return f"Wordle {label} {count}/{MAX_GUESSES}\n\n{rows}"


def play(solution, header, show_keyboard, words, hard, share_label):
    history = []       # list of (guess, marks)
    used = set()       # letters guessed so far
    notice = ""
    solved = False

    while len(history) < MAX_GUESSES:
        draw(history, used, show_keyboard, header)
        if hard:
            print("  hard mode")
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
        if hard:
            err = hard_mode_error(guess, history)
            if err:
                notice = "..." + err
                continue

        marks = score(guess, solution)
        history.append((guess, marks))
        used.update(guess)
        if guess == solution:
            solved = True
            break

    draw(history, used, show_keyboard, header)
    if solved:
        print(f"  Got it in {len(history)}! ")
    else:
        print(f"  Out of guesses. The word was: {solution.upper()}")
    if history:
        print("\n" + share_grid(history, solution, share_label))
    return 0


def run_practice(code_arg, show_keyboard, words, hard):
    answers = load_answers()
    if not answers:
        print("No word list available for practice.", file=sys.stderr)
        return 1

    code = normalize_code(code_arg) if code_arg else ""
    if not code:
        code = generate_code()

    solution = word_from_code(code, answers)
    print(f"\n  Practice — share this code so others get the same word:  {code}\n")
    return play(
        solution, f"Practice · {code}", show_keyboard, words,
        hard=hard, share_label=f"Practice {code}",
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="wordle", description="Play the day's NYT Wordle in your terminal."
    )
    parser.add_argument(
        "--practice",
        nargs="?",
        const="",
        default=None,
        metavar="CODE",
        help="play an offline word; pass a shared CODE to match a friend, "
        "or omit it to get a new code to share",
    )
    parser.add_argument(
        "--hard",
        action="store_true",
        help="hard mode: revealed hints must be reused in later guesses",
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
    show_keyboard = not args.no_keyboard

    if args.practice is not None:
        return run_practice(args.practice, show_keyboard, load_words(), args.hard)

    date = datetime.date.today().isoformat()
    try:
        solution, number = fetch_puzzle(date)
    except Exception as exc:  # network / parsing issues
        print(f"Couldn't fetch today's word: {exc}", file=sys.stderr)
        return 1

    if args.solve:
        print(solution.upper())
        return 0
    if args.hint:
        print(make_hint(solution))
        return 0

    label = f"{number:,}" if number else date
    return play(
        solution, f"Wordle · {date}", show_keyboard, load_words(),
        hard=args.hard, share_label=label,
    )


if __name__ == "__main__":
    sys.exit(main())
