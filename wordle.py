#!/usr/bin/env python3
"""wordle-cli — play the day's NYT Wordle in your terminal.

No dependencies, no browser tab. The answer is fetched from NYT's public
puzzle endpoint (the same JSON your browser downloads before you guess).
"""

import argparse
import datetime
import json
import sys
import urllib.request
from collections import Counter

WORD_LEN = 5
MAX_GUESSES = 6
ENDPOINT = "https://www.nytimes.com/svc/wordle/v2/{date}.json"

# ANSI colours (bright bg + black text, like the real tiles)
GREEN = "\033[42;30m"
YELLOW = "\033[43;30m"
GRAY = "\033[100;97m"
DIM = "\033[2m"
RESET = "\033[0m"
BG = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}

# For merging a letter's best-known status onto the keyboard.
RANK = {"gray": 1, "yellow": 2, "green": 3}
KEYBOARD_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")


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


def render(guess, marks):
    tiles = [f"{BG[m]} {ch.upper()} {RESET}" for ch, m in zip(guess, marks)]
    return "".join(tiles)


def update_keyboard(state, guess, marks):
    """Keep each letter's best-known status (green > yellow > gray)."""
    for ch, m in zip(guess, marks):
        if RANK[m] > RANK.get(state.get(ch, ""), 0):
            state[ch] = m


def render_keyboard(state):
    lines = []
    for indent, row in enumerate(KEYBOARD_ROWS):
        keys = []
        for ch in row:
            status = state.get(ch)
            if status:
                keys.append(f"{BG[status]} {ch.upper()} {RESET}")
            else:
                keys.append(f"{DIM} {ch.upper()} {RESET}")
        lines.append(("  " * indent) + "".join(keys))
    return "\n".join(lines)


def make_hint(solution):
    vowels = sum(1 for c in solution if c in "aeiou")
    uniq = len(set(solution))
    return (
        f"Hint: starts with '{solution[0].upper()}', "
        f"{vowels} vowel(s), {uniq} unique letter(s)."
    )


def play(solution, date, show_keyboard):
    print(f"Wordle — {date}.  {MAX_GUESSES} guesses, {WORD_LEN} letters.\n")
    keyboard = {}

    for attempt in range(1, MAX_GUESSES + 1):
        while True:
            try:
                guess = input(f"[{attempt}/{MAX_GUESSES}] > ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                return 0
            if len(guess) != WORD_LEN or not guess.isalpha():
                print(f"  ...enter a {WORD_LEN}-letter word.")
                continue
            break

        marks = score(guess, solution)
        print("  " + render(guess, marks))

        if show_keyboard:
            update_keyboard(keyboard, guess, marks)
            print(render_keyboard(keyboard) + "\n")

        if guess == solution:
            print(f"\n Got it in {attempt}! ")
            return 0

    print(f"\nOut of guesses. The word was: {solution.upper()}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Play the day's NYT Wordle.")
    parser.add_argument(
        "--solve", action="store_true", help="reveal today's answer and exit"
    )
    parser.add_argument(
        "--hint", action="store_true", help="print a small hint and exit"
    )
    parser.add_argument(
        "-k",
        "--keyboard",
        action="store_true",
        help="show a QWERTY tracker of used/unused letters after each guess",
    )
    args = parser.parse_args()

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

    return play(solution, date, show_keyboard=args.keyboard)


if __name__ == "__main__":
    sys.exit(main())
