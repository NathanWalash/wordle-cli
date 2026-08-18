# wordle-cli

Play the day's [NYT Wordle](https://www.nytimes.com/games/wordle) right in your
terminal — no browser tab, no dependencies, just Python 3 (which ships with
macOS).

```
  Wordle · 2026-08-18

   S  T  A  R  E
   P  L  U  C  K      Q  W [E][R][T] Y [U] I  O [P]
   ·  ·  ·  ·  ·      [A][S] D  F  G  H  J [K][L]
   ·  ·  ·  ·  ·        Z  X [C] V  B  N  M
   ·  ·  ·  ·  ·
   ·  ·  ·  ·  ·

  [2/6] >
```

*(Guess tiles are green / yellow / grey; the keyboard uses two greys —
light = unused, dark = already tried.)*

## How it works

The answer is fetched from NYT's public puzzle endpoint —
`https://www.nytimes.com/svc/wordle/v2/<date>.json` — which is the same JSON
your browser downloads *before* you type a guess. So the CLI just reads the
`solution` field. No auth, no scraping, no solving required.

## Usage

```sh
./wordle.py                 # play today's puzzle (keyboard tracker shown by default)
./wordle.py -n              # play without the keyboard tracker
./wordle.py --hint          # print a small hint (first letter, vowel/unique counts) and exit
./wordle.py --solve         # reveal today's answer and exit
```

You get 6 guesses at the 5-letter word. After each guess the board redraws with
your feedback and an updated QWERTY tracker showing which letters you've used.

| Flag | Effect |
| --- | --- |
| `-n`, `--no-keyboard` | Hide the letter tracker |
| `--hint` | First letter + vowel/unique-letter counts, then exit |
| `--solve` | Print the answer and exit |

## Notes

- Any 5-letter alphabetic input is accepted (no dictionary check).
- Requires Python 3 and a terminal that supports ANSI colours.

## Project

A small for-fun project. Commits are kept small and focused; see `git log`.
