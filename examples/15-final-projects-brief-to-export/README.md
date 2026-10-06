# Worked example — Chapter 15: a persistent best time, reproduced and exported

## Executive summary

**What this is.** The complete record behind Chapter 15's hands-on. On 27 September 2026 Claude Code (2.1.150, `claude-sonnet-4-6`) implemented FEAT-10, a persistent personal best, in a scratch copy of `walker-jumpman-clawd`. The copy's `godot/` folder was byte-identical to published commit `382f2ba`, with baseline `48bd764`. The work followed save rules written from the game's own production-plan note WJ-D02. The reviewer then checked the result, sent one correction back to the same session, reproduced the final commit from a clean clone, and attempted a Web export on a machine with no export templates.

**Why look at it.** The first pass passed every test and said, in its own summary, that no test touched the player's real save. That was false. The unchanged `test_game.gd` and `test_keyboard.gd` wrote `user://best_time.json`, the second with a "best" of 0.0667 s from a 4-tick fixture. The version rule also broke whenever a newer file changed another field as well. The logs here show the failure, the fix and the reproduction.

**What it found.** Final state: 25/25 mechanics, 9/9 keyboard, 1,950/0 animation parity, 38/38 best-time checks, and 13/13 on the reviewer's own rule check. The original suites leave `user://` alone. A clean clone passes everything after one import. The project's own invariant script rejects the change (`Invariant changed: godot/ui/hud.gd`), a design decision still open. `--export-release "Web"` fails because the 4.7.2 Web templates are missing, as expected. `--export-pack` works without templates and shows exactly what would ship.

**What it does not show.** A played Web export, a screen reader, crash safety of the save, or whether a best time is worth showing.

**Side effect to note.** The first pass's test runs wrote `best_time.json` (0.0667 s) into the real `~/Library/Application Support/Godot/app_userdata/walker-jumpman-clawd/` folder, which the scratch copy shares by project name. The published game never reads it. It was left in place for the owner to delete.

---

## Contents

| Path | What it is |
|---|---|
| `PROMPTS.md` | Both prompts, word for word, and the exact command lines |
| `claude/changes-first-pass.diff` | The first pass against baseline `48bd764`, reconstructed by replaying the six Write/Edit calls in `session.jsonl` onto the baseline; the reviewer re-ran the failing checks on it |
| `claude/changes.diff` | The final change after the correction, taken from the working tree before commit `ef72546` |
| `claude/test_best_time.gd` | The agent's final test (38 checks) |
| `claude/session.jsonl`, `session.md` | First pass: raw transcript (514 KB) and readable excerpt |
| `claude/session-fix.jsonl`, `session-fix.md` | The correction, resumed with `--resume` (161 KB) |
| `reviewer/verify_best_time_rules.gd` | The human-written 13-check rule test (cases A–E) |
| `reviewer/normal_play_save_probe.gd` | A 20-line probe: normal play completes the route and saves |
| `export/export_presets.cfg` | The agent's Web preset |
| `export/pack-listing.txt`, `pack-sha256.txt` | What `--export-pack` wrote: 20 entries, sizes and hashes |
| `logs/` | Numbered runs: `0x` baseline, `1x` first pass, `2x` final, `30-` clean clone of the published repo, `40-` clean clone of the final commit (and its export pack), `5x` export attempts on the first pass |

## Reproduce

From a clone of the public repository at `382f2ba`, apply the final change:

```bash
git apply --exclude=godot/tests/test_clawd.gd.uid path/to/claude/changes.diff
```

The exclusion is only needed if an earlier import already created that `.uid` file. Copy `reviewer/verify_best_time_rules.gd` to `godot/tests/`. On macOS, keep every run out of your real user data:

```bash
mkdir -p ../scratch-home
```

```bash
HOME="$PWD/../scratch-home" godot --headless --path godot --import
```

```bash
HOME="$PWD/../scratch-home" godot --headless --path godot --script res://tests/test_best_time.gd --fixed-fps 60
```

```bash
HOME="$PWD/../scratch-home" godot --headless --path godot --script res://tests/verify_best_time_rules.gd --fixed-fps 60
```

Run `test_game.gd`, `test_keyboard.gd` and `test_clawd.gd` the same way. Then:

```bash
godot --headless --path godot --export-release "Web" ../build/web/index.html
```

Expected without templates: exit 1 and `No export template found at the expected path: …/export_templates/4.7.2.stable/web_nothreads_release.zip`.

## Results at a glance

| Check | First pass | Final |
|---|---|---|
| original three suites | pass, **but write `user://best_time.json`** | pass; no file |
| agent's `test_best_time.gd` | 31/31 | 38/38 |
| reviewer's `verify_best_time_rules.gd` | 2 failures (version-2 files with a renamed level or format overwritten) | 13/13 |
| clean clone of the final commit | — | import exit 0; one untracked `.uid` (the reviewer forgot to commit it); all suites pass |
| `node scripts/clawd-build.cjs` on the published repo + change | — | `Error: Invariant changed: godot/ui/hud.gd` |
| `--export-release "Web"` | exit 1, templates missing | exit 1, templates missing |
| `--export-pack` (.zip / .pck) | exit 0 (logs `51`–`53`) | exit 0; 24,926 / 25,396 bytes; `tests/` excluded, gallery included; the PCK runs 120 frames with `--main-pack` (logs `41`–`43`) |
