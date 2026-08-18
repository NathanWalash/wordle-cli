# Changelog

All notable changes to this project are documented here. This project follows
[Semantic Versioning](https://semver.org).

## [1.4.0] — 2026-08-18

### Added
- `--colorblind` flag: high-contrast blue/orange tiles instead of green/yellow.

## [1.3.0] — 2026-08-18

### Added
- `--no-color` flag, plus support for the `NO_COLOR` environment variable and
  automatic colour-off when output is not a terminal. A plain, ANSI-free board
  renders with `[x]` / `(x)` / `x` tile shapes.

## [1.2.0] — 2026-08-18

### Added
- `--version` flag to print the installed version.

## [1.1.0] — 2026-08-18

### Added
- **Hard mode** (`--hard`): revealed greens must stay in place and revealed
  yellows must be reused in later guesses.
- **Shareable result grid** printed after each game, in the familiar copy-paste
  format (`Wordle 1,234 4/6` plus the emoji squares).
- Published to PyPI as `nyt-wordle-cli` (`pip install nyt-wordle-cli`).

### Changed
- Professional README with a centred banner and expanded documentation.

## [1.0.0] — 2026-08-18

First release.

### Added
- Play the day's real NYT Wordle in the terminal, answer read from NYT's public
  puzzle feed.
- Colour-coded guess tiles and a live QWERTY letter tracker beside the board.
- Real-word validation against a bundled ~15k word list.
- **Practice mode** (`--practice`): play offline from a curated ~2.3k answer
  list, with a shareable code so friends get the same word. The code is
  unrelated to the word (derived by hashing), case- and separator-insensitive.
- `--hint` and `--solve` helpers, and `-n/--no-keyboard` to hide the tracker.
- Installable as a `wordle` command via `pipx` / `pip`.
- Test suite and GitHub Actions CI across Python 3.9–3.12.

[1.4.0]: https://github.com/NathanWalash/wordle-cli/releases/tag/v1.4.0
[1.3.0]: https://github.com/NathanWalash/wordle-cli/releases/tag/v1.3.0
[1.2.0]: https://github.com/NathanWalash/wordle-cli/releases/tag/v1.2.0
[1.1.0]: https://github.com/NathanWalash/wordle-cli/releases/tag/v1.1.0
[1.0.0]: https://github.com/NathanWalash/wordle-cli/releases/tag/v1.0.0
