# TEST-REPORT.md — Downfall (Assignment 2 summary)

**Revision:** `111bf6e` (committed 2026-10-07). This is the source revision the film shows. Later commits change documents and film files only.

**Engine:** Godot 4.7.2-stable, Windows 11.

**Command:** `& 'D:\CSYE 7370\downfall-godot\tests\run_all.ps1' -Visual`. That runs 25 headless suites (now including `test_audio`), plus `test_audio` again with real playback, the windowed UI and input suites and the capture scripts (`--audio-driver Dummy`).

## Result: all automated tests pass

On 2026-10-07, `tests/run_all.ps1 -Visual` was run on the exact file set submitted in `downfall-godot/`, after a fresh `--import`, on Godot 4.7.2 and Windows 11. **Every suite passed, with 0 failures.** The log is `design/evidence/fresh-copy-course-subset.log`.

`run_all.ps1` stops on the first `FAIL` or `SCRIPT ERROR`, and it ran to the end.

| Suite | Result |
|---|---|
| test_v1 (core rules, saves) | 73 checks, 0 failures |
| test_base_state, test_warehouse, test_orders, test_medical, test_progression, test_base_scene | passed (no failure lines) |
| test_layout (60 seeds) | 10 checks, 0 failures |
| test_terrain | 21 checks, 0 failures |
| test_scene_dressing | 15 checks, 0 failures |
| test_guards | 43 checks, 0 failures |
| test_movement | 9 checks, 0 failures |
| test_combat | 14 checks, 0 failures |
| test_enemy_attacks | 109 checks, 0 failures |
| test_lappland | 59 checks, 0 failures |
| test_relics | 12 checks, 0 failures |
| test_builds | 117 checks, 0 failures |
| test_inventory | 48 checks, 0 failures |
| test_loot | 57/57 passed |
| test_item_icons | 152/152 passed |
| test_relic_icons | 12/12 passed |
| test_gear | 41/41 passed |
| test_ai_driver | 4 checks, 0 failures |
| test_revisions | 86 checks, 0 failures |
| **test_audio**, headless (sound-trigger counts, loop points, pause, stings, mute) | 26 checks, 0 failures |
| **test_audio**, windowed (real playback) | 26 checks, 0 failures |
| test_ui_v1 (real mouse and key events) | 12 checks, 0 failures |
| test_lappland_input (real input events) | 7 checks, 0 failures |
| capture_enemy_attacks, capture_lappland, capture_v1, capture_terrain, capture_guards | 0 failures |

The same ZIP that goes to Canvas was also unpacked into an empty folder. There, `test_v1` (73/73), `test_audio` and `test_relic_icons` (12/12) passed again.

**Not covered by this result:** the human playtest with sound on and muted (see *Human playtest* below).

## Automated results (latest evidence files, all 2026-10-07 unless noted)

| Suite | Result | File |
|---|---|---|
| v1 core | 73/73 | `../evidence/downfall-v1-tests.json` |
| UI (real mouse/key events) | 12/12 | `downfall-v1-ui-tests.json` |
| Lappland combat | 59/59 | `lappland-tests.json` |
| Lappland input (real events) | 7/7 | `lappland-input-tests.json` |
| Enemy attacks | 109/109 | `enemy-attacks-tests.json` |
| Guards | 43/43 | `downfall-guard-tests.json` |
| Layout (20 seeds per region) | 10/10 | `downfall-layout-tests.json` |
| Terrain (2026-10-06) | 21/21 | `downfall-terrain-tests.json` |
| Movement, combat, relics | 9, 14, 12 pass; 0 fail | `downfall-test-*-1791*.json` |
| Audio, headless (state) | 26/26 | `downfall-audio-tests-headless.json` |
| Audio, windowed (real playback, Dummy driver) | 26/26 | `downfall-audio-tests.json` |

The builds, loot, inventory, gear, revisions, medical and orders suites print only to
the console; **no saved result exists for them.**

## Against the assignment checks

| Check | Status |
|---|---|
| Startup and controls | Covered by automated UI/input suites. Fresh-copy run done on 2026-10-07 (see *Fresh-copy run* below). |
| Character vs. sheet | Captures `design/character/in-engine/lappland-{region}-{ready,combo-1..3,wave,dash}.png` exist. No side-by-side against a sheet. |
| Storyboard vs. game | See [STORYBOARD.md](STORYBOARD.md); its panels *are* the captures. The recovery-ward moment has no capture. |
| Sound events, exactly once per event | `tests/test_audio.gd` counts every `FieldAudio.play()` call (counted before the headless early return). One walk into the warehouse: lights-on 4 (one per bank), hatch 4 and shelf 4 (one per built rack); one walk out: lights-off 1; standing in the room or leaving adds none. Two settles give one sting. **Hatch and shelf files are not generated yet**, so those two are counted but silent. HIT, LOOT and BUILD still have no guard. |
| Music loop | Loop points in code equal `audio/asset_log.json` (checked by the test). Seam measured on the decoded OGGs (`SOURCES.md`, *Generated audio*). Pause, death, extraction, next-floor and boot-settle behavior match CHANGE-BRIEF's predictions (`test_audio.gd`); field pause holds the position (0.000 s moved over 30 frames). **The seam has not been listened to by a person yet** (`audio/_check/*_x3.ogg`). |
| Muted play | Settings → 静音 mutes the Master bus; the test checks mute and unmute. Every audio event has a visual equivalent (CHANGE-BRIEF, *Mute*). **No muted human play-through yet.** |
| Automated check added | `tests/test_audio.gd` (26 checks), in `run_all.ps1` headless and `-Visual`. |
| Human playtest, sound on and muted | **No record for this assignment.** Nothing is invented here. |

## Inspect-and-revise cycles

These already exist in the record:

- Combat atlas re-slice after the shrink and clipped swords (2026-09-29).
- Background v1 → v2 (before/after captures).
- Enemy floating-weapon variant removed.
- Equipment v1 → v5.

## Honest limitations

- Two of the four warehouse event sounds (hatch, shelf) are not generated yet.
- Loop seams checked by measurement only, not yet by ear.
- Fewer than 10 poses.
- No silhouette or collision overlay images.
- No human playtest notes.
- No film.
- Uses copyrighted IP.


## Fresh-copy run (2026-10-07, live)

The whole project was cloned into an empty folder with `git clone`. The Godot executables were copied beside the clone, then `--import` and `run_all.ps1 -Visual` were run there. The logs are in `youtube/claude-liam-downfall-gamedev/evidence/`.

| Revision | Result |
|---|---|
| `6014c89` | Crashed in the first suite: `store_string` on a null file. Every suite writes to `res://../evidence`, which a clone does not have. Fixed in `f770e26`: `run_all.ps1` now creates the folder. |
| `f770e26` | All suites passed up to `test_revisions`. Then `test_audio` stopped with `Invalid access to property or key 'base'`: the music streams were missing. Cause: the `.gitignore` rule `music/` also matched `audio/music/`. Fixed in `111bf6e`. |
| `111bf6e` | **Every test suite passed**, headless and windowed (`test_audio` 26/26 in both passes, `test_ui_v1` 12/12, `test_lappland_input` 7/7). One screenshot script, `capture_v1`, failed once with `Out of bounds get index '0'` on a random map, then passed on two reruns. `capture_terrain` and `capture_guards` passed. **`capture_v1` is flaky, not fixed.** |
| Course-repo copy (code plus used assets, 949 files, 2026-10-07) | **Every suite passed**, headless and windowed, including all capture scripts (`design/evidence/fresh-copy-course-subset.log`). The first try failed `test_builds`: that test reads the research table `局内构筑调研_集成战略藏品.md`, which the game-only history did not track. The table is now included. |

## Film captures as evidence (2026-10-07)

Five real 4K Movie Maker captures were made from an isolated clone of `111bf6e` (`youtube/claude-liam-downfall-gamedev/CAPTURE.md`). They confirm with real playback:

- base music;
- the light cues;
- the field loop;
- pause freezing the field;
- one fail sting at a real death on floor 31;
- one extract sting after a real click on the camp's 撤离 button.

These are scripted input, **not** a human playtest.

## Human playtest

**Still not recorded.** The author needs to play with sound on and then muted, and write down what they actually saw and heard. Nothing here stands in for that.
