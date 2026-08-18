# wordle-cli

Play the day's NYT Wordle in your terminal. No dependencies, no browser tab.

The answer is fetched from NYT's public puzzle endpoint — the same JSON your
browser downloads before you type a guess.

## Usage

```sh
./wordle.py
```

or

```sh
python3 wordle.py
```

You get 6 guesses at the 5-letter word. Tiles are coloured like the real game:
🟩 right letter, right spot · 🟨 right letter, wrong spot · ⬛ not in the word.

## Notes

- Any 5-letter alphabetic input is accepted (no dictionary check).
- Requires Python 3 (ships with macOS).
