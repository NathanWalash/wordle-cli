<div align="center">

<pre>
╭───┬───┬───┬───┬───┬───╮
│ W │ O │ R │ D │ L │ E │
╰───┴───┴───┴───┴───┴───╯
</pre>

<h1>wordle-cli</h1>

<p><strong>Play the New York Times Wordle in your terminal.</strong><br>
No browser tab, no accounts, no dependencies — just Python 3.</p>

<p>
  <a href="https://github.com/NathanWalash/wordle-cli/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/NathanWalash/wordle-cli/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://pypi.org/project/nyt-wordle-cli/"><img alt="PyPI" src="https://img.shields.io/pypi/v/nyt-wordle-cli"></a>
  <img alt="Python" src="https://img.shields.io/pypi/pyversions/nyt-wordle-cli">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green">
</p>

</div>

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

Guess tiles are green / yellow / grey; the on-screen keyboard uses two greys —
light for unused letters, dark for ones you've tried.

## Features

- Plays **today's real Wordle** — the answer is read from NYT's public puzzle feed.
- **Practice mode with shareable codes** so friends can race on the same word.
- **Hard mode** — revealed hints must be reused in later guesses.
- Live **QWERTY tracker** beside the board.
- **Real-word validation** against a bundled list of ~15,000 words.
- **Shareable result grid** in the familiar copy-paste format.
- Clean ANSI colours, and **zero dependencies** — pure Python standard library.

## Installation

From PyPI (recommended):

```sh
pip install nyt-wordle-cli
```

Or with [pipx](https://pipx.pypa.io) to keep it isolated as a global command:

```sh
pipx install nyt-wordle-cli
```

Then run:

```sh
wordle
```

## Usage

```sh
wordle                       # play today's puzzle
wordle --hard                # hard mode
wordle --practice            # offline game; prints a code you can share
wordle --practice K7Q2MX     # play a friend's code (same word)
wordle -n                    # hide the keyboard tracker
wordle --hint                # print a small hint, then exit
wordle --solve               # reveal today's answer, then exit
```

| Flag | Effect |
| --- | --- |
| `--practice [CODE]` | Play offline; share the printed code, or pass a friend's code |
| `--hard` | Revealed greens must stay in place and yellows must be reused |
| `-n`, `--no-keyboard` | Hide the letter tracker |
| `--hint` | First letter plus vowel and unique-letter counts, then exit |
| `--solve` | Print the answer and exit |

## Play with a friend

Practice mode plays a word offline and prints a short code. Anyone who runs the
same code gets the **same word**, so you can compete:

```sh
wordle --practice            # you: prints e.g. "K7Q2MX" and starts a game
wordle --practice K7Q2MX     # a friend: same code, same word
```

The code is deliberately **unrelated to the word** — it is mapped through a hash,
so the code reveals nothing about the answer. Codes are case- and
dash-insensitive (`k7q2-mx` works too).

## Sharing your result

After each game, wordle-cli prints a result grid you can paste anywhere:

```
Wordle 1,234 4/6

⬛🟨⬛⬛🟩
⬛⬛🟨🟩🟩
🟨⬛🟩🟩🟩
🟩🟩🟩🟩🟩
```

## How it works

The daily answer is read from NYT's public puzzle endpoint —
`https://www.nytimes.com/svc/wordle/v2/<date>.json` — which is the same JSON your
browser downloads before you type a guess. wordle-cli just reads the `solution`
field. Practice mode never touches the network: it draws from a bundled,
curated answer list and derives the word from your share code.

## Development

```sh
git clone https://github.com/NathanWalash/wordle-cli.git
cd wordle-cli
pip install -e ".[dev]"      # or: pip install -e . pytest
pytest
```

The test suite covers scoring (including duplicate-letter rules), guess and
hard-mode validation, the share grid, and the deterministic share-code mapping.
CI runs it on Python 3.9 through 3.12.

## Contributing

Issues and pull requests are welcome. Please keep changes focused and make sure
`pytest` passes before opening a PR.

## License

[MIT](LICENSE)
