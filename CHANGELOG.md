# Changelog

All notable changes to this project are documented here. This project follows
[Semantic Versioning](https://semver.org).

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

[1.0.0]: https://github.com/NathanWalash/wordle-cli/releases/tag/v1.0.0
