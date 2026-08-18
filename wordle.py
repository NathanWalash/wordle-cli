#!/usr/bin/env python3
"""wordle-cli — play the day's NYT Wordle in your terminal.

No dependencies, no browser tab. The answer is fetched from NYT's public
puzzle endpoint (the same JSON your browser downloads before you guess).
"""

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
RESET = "\033[0m"


def fetch_solution(date):
    """Return today's five-letter solution, lowercased."""
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
    colors = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}
    tiles = [f"{colors[m]} {ch.upper()} {RESET}" for ch, m in zip(guess, marks)]
    return "".join(tiles)


def main():
    date = datetime.date.today().isoformat()
    try:
        solution = fetch_solution(date)
    except Exception as exc:  # network / parsing issues
        print(f"Couldn't fetch today's word: {exc}", file=sys.stderr)
        return 1

    print(f"Wordle — {date}.  {MAX_GUESSES} guesses, {WORD_LEN} letters.\n")

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

        if guess == solution:
            print(f"\n Got it in {attempt}! ")
            return 0

    print(f"\nOut of guesses. The word was: {solution.upper()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
