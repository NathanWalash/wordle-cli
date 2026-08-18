```
 ██     ██  ██████  ██████  ██████  ██      ███████
 ██     ██ ██    ██ ██   ██ ██   ██ ██      ██
 ██  █  ██ ██    ██ ██████  ██   ██ ██      █████
 ██ ███ ██ ██    ██ ██   ██ ██   ██ ██      ██
  ███ ███   ██████  ██   ██ ██████  ███████ ███████
        p l a y   t h e   d a i l y   w o r d   i n   y o u r   s h e l l
```

<p align="center">
  <b>wordle-cli</b> — the New York Times Wordle, in your terminal.<br>
  No browser tab, no accounts, no dependencies. Just Python 3.
</p>

<p align="center">
  <a href="https://github.com/NathanWalash/wordle-cli/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NathanWalash/wordle-cli/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

---

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

*Guess tiles are green / yellow / grey; the keyboard uses two greys —
light = unused, dark = already tried.*

## Features

- 🎯 Plays **today's real Wordle** — the answer comes straight from NYT's public
  puzzle feed.
- 👥 **Practice mode with shareable codes** — race a friend on the same word.
- ⌨️ Live **QWERTY tracker** beside the board showing used vs unused letters.
- 📖 **Real-word validation** against a bundled ~15k word list.
- 🎨 Clean ANSI colours, no emoji tiles.
- 🪶 **Zero dependencies** — pure Python standard library.

## Install

With [pipx](https://pipx.pypa.io) (recommended — installs it as an isolated, global command):

```sh
pipx install git+https://github.com/NathanWalash/wordle-cli.git
```

Or from a clone:

```sh
git clone https://github.com/NathanWalash/wordle-cli.git
cd wordle-cli
pipx install .          # or: pip install .
```

Then just run:

```sh
wordle
```

## Usage

```sh
wordle                 # play today's puzzle (keyboard tracker shown by default)
wordle -n              # play without the keyboard tracker
wordle --hint          # print a small hint (first letter, vowel/unique counts) and exit
wordle --solve         # reveal today's answer and exit
```

You get 6 guesses at the 5-letter word. After each guess the board redraws with
your feedback and an updated tracker.

| Flag | Effect |
| --- | --- |
| `--practice [CODE]` | Play offline; share the printed code, or pass a friend's code |
| `-n`, `--no-keyboard` | Hide the letter tracker |
| `--hint` | First letter + vowel/unique-letter counts, then exit |
| `--solve` | Print the answer and exit |

## Play with a friend

Practice mode plays a word offline (no daily puzzle needed) and gives you a
short code. Anyone who runs the same code gets the **same word**, so you can
race each other:

```sh
wordle --practice            # prints e.g. "code K7Q2MX" and starts a game
wordle --practice K7Q2MX     # a friend runs your code -> same word
```

The code is deliberately **unrelated to the word** — it's mapped through a hash,
so seeing the code tells you nothing about the answer. Codes are case- and
dash-insensitive (`k7q2-mx` works too).

## How it works

The answer is read from NYT's public puzzle endpoint —
`https://www.nytimes.com/svc/wordle/v2/<date>.json` — which is the same JSON your
browser downloads *before* you type a guess. The CLI just reads the `solution`
field. No scraping, no auth.

## Development

```sh
git clone https://github.com/NathanWalash/wordle-cli.git
cd wordle-cli
pip install -e .
pip install pytest && pytest        # run the test suite
```

## License

MIT — see [LICENSE](LICENSE).
