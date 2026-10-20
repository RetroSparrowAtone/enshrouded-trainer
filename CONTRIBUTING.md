# Contributing to enshrouded-trainer

Thanks for wanting to help. This is a hobbyist / educational modding
project for Enshrouded — nothing here is affiliated with Keen Games.

## Ground rules
- Every feature lives in a plugin under `plugins/`. The host must stay
  generic: no cheat logic inside `trainer_host/`.
- Plugins communicate through `contracts/` only. Do not import another
  plugin directly.
- Memory offsets belong in `offsets/en_shrouded_2026.json` and are
  versioned per game patch. PRs bumping offsets must state the game
  build number.
- Run `pytest tests/` before opening a PR.

## Plugin checklist
1. Subclass `contracts.plugin.PluginBase`.
2. Declare `NAME`, `VERSION`, `REQUIRES_OFFSETS`.
3. Register hotkeys via `ctx.hotkeys.bind(...)` — never raw `keyboard`.
4. Handle `ctx.process` being `None` (game closed) gracefully.

## Style
- Black, 100 cols. Type hints on public functions.
- No `eval` of user config. Use `pydantic` schemas in `config/schema.py`.

Use at your own risk — see SECURITY.md.