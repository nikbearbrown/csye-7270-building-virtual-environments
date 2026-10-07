# CHANGE-BRIEF.md — Downfall (Assignment 2 summary)

> **Retrospective.** This describes the current build. These are not predictions
> made before generation.

## Asset list

| ID | File (runtime) | Panel |
|---|---|---|
| CHAR-IDLE / CHAR-WALK | `godot_assets/lappland_8dir_walk_32.png` via `Lappland8DirWalk32.tres` | 1, 4, 5 |
| CHAR-ATK1..3, CHAR-WAVE, CHAR-HURT | `godot_assets/lappland_combat_64.png` | 4, 6, 8 |
| VFX-SLASH, VFX-WAVE | `godot_assets/lappland_vfx_slash_{1,2,3}.png`, `lappland_vfx_wave.png` | 4, 6 |
| ENEMY-WALK / ENEMY-ATK | `art/field/enemy_walk_*_64.png`, `enemy_dir_*_64.png`, `enemy_attacks_64.png` | 5 |
| ENV-SURF-MINE/CITY/SNOW | `art/field/surface_{mine,city,snow}_v2.png` | 3, 4, 5 |
| ENV-PROPS | `art/field/scene_groups_v2.png`, `props_v1.png` | 3 |
| ENV-RHODES | `art/rhodes_runtime/` | 1, 9 |
| ITEM-ICONS / RELIC-ICONS | `art/items/runtime/`, `art/relics/runtime/` | 6, 8, 10 |
| SFX-* (13 cues) | synthesized in memory by `game/field_audio.gd`; no files | 4–10 |
| SFX-LIGHTS-ON / SFX-LIGHTS-OFF | `audio/sfx/lights_on.wav`, `lights_off.wav` (Gemini, generated) | 9 |
| SFX-HATCH / SFX-SHELF | `audio/sfx/hatch.wav`, `shelf.wav` — **not generated yet**; the cue is wired and counted, silent until the file exists | 9 |
| MUS-BASE | `audio/music/base_loop.ogg` (Gemini, generated) | 1, 2, 9 |
| MUS-MINE | `audio/music/mine_loop.ogg` (Gemini, generated) | 3–7 |
| STING-EXTRACT / STING-FAIL | `audio/music/sting_extract.ogg`, `sting_fail.ogg` (Gemini, generated) | 10, 8 |

## Event-to-sound map

Each cue is listed with the code that triggers it and its double-trigger guard.

| Cue | Trigger | Double-trigger guard |
|---|---|---|
| SFX-HIT | each swing, `entities/player.gd:491` | Attack cooldown only. It plays even on air swings, and there is no hit/miss distinction. |
| SFX-CHARGE | charge reaches 3, `player.gd:439` | Edge-triggered (`before < sword_charge`). |
| SFX-HURT | `take_damage`, `player.gd:633` | None beyond the shield and dash early returns. |
| SFX-LOOT | pickup / crate open, `game/game_manager.gd:1344-1356, 1437, 1937` | None. |
| SFX-BUILD | relic chosen (`game_manager.gd:644`), notable-drop beam (`entities/loot.gd:98`) | None. |
| SFX-EXIT | ~~`settle()`~~ — **replaced 2026-10-07** by STING-EXTRACT / STING-FAIL via `GameMusic.end_run()` | `if _settled: return`. |
| SFX-LIGHTS-ON / HATCH / SHELF / LIGHTS-OFF | `room_reveal.gd` signals, connected in `GameManager._ready()` | see *Generated audio — predictions* |
| SFX-ENEMY-<type> ×7 | 0.1 s before wind-up ends, `entities/enemy.gd:429-431` | `_cue_played` flag, reset per attack. |

There is a global cap of 16 simultaneous voices. Sound never decides game state.
`play()` returns early when run headless, and the tests pass the same way.

## Generated audio — predictions

> **Written 2026-10-07, after the files were cut (`audio/tools/cut_audio.py`) and
> before any of them were wired into the game.** Later corrections go under
> *Audio revisions* below; these lines are not edited.

### Event sounds: one per event

All four are warehouse events from `world/room_reveal.gd`, whose signals were
added for exactly this and already fire on an edge, not per frame.

| Cue | Signal | Predicted count | Guard already in the code |
|---|---|---|---|
| SFX-LIGHTS-ON | `bank_lit(index)` | 4 per walk-in: banks 0, 1, 2, 3 in order, after each bank's flicker | `_announced` only rises; resets when the room is dark |
| SFX-HATCH | `hatch_opening(shelf)` | once per **built** rack per walk-in (4 on a fresh save) | emitted when the shelf clock crosses `HATCH_DELAY` upward only |
| SFX-SHELF | `shelf_rising(shelf)` | once per built rack, when it is on screen (4 after walking the room) | emitted when the clock crosses `hold` upward only |
| SFX-LIGHTS-OFF | `lights_out` | once per walk-out, after the last hatch shuts | `t > 0.0` check, then `t = 0` |

Standing in the doorway does not repeat any of them (the room edge has 0.3
units of hysteresis). Leaving and coming back plays the whole set again; that is
a new event. Hatches stacking (up to 4 inside 0.3 s) will be quieter than the
lights (-14 dB against -8 dB) and get ±5% random pitch.

### Music

| Situation | Predicted behavior |
|---|---|
| Boot, title, walking the base | MUS-BASE from 0:00. 0–40.17 s plays once, then 40.17–115.47 s loops (`loop_offset`). |
| A contract starts | MUS-BASE fades out over 1.0 s; MUS-MINE starts from 0:00: the 13.3 s intro once, then 13.30–45.30 s loops (10 bars of 3.2 s). Every region uses this track. |
| Next floor, camp | MUS-MINE carries on; it does not restart. |
| **Pause** (Esc pause menu, `modal == "pause"`) | In the field, the loop is paused (`stream_paused`) and resumes from the same sample on close, because the pause menu freezes the field. In the base, which does not freeze, the music is ducked by 10 dB instead and comes back on close. Other panels (bag, map) change nothing. |
| **Death** | MUS-MINE fades out over 0.3 s, then STING-FAIL plays once (12.0 s). |
| **Extraction** | MUS-MINE fades out over 1.0 s, then STING-EXTRACT plays once (5.7 s). |
| **After either sting** | MUS-BASE starts from 0:00 only once the sting has finished, so the two never overlap. |
| Interrupted contract found on boot | `load_base()` settles it as a death. **No sting**: the field music never started. |

The synthesized SFX-EXIT is no longer played by `settle()`; the stings replace it.

### Mute

Settings gets a 静音 toggle that mutes the Master bus and is saved in
`user://settings.cfg` with the other settings. Music and SFX go through their own
buses (`Music`, `SFX`) under Master. Muted, every audio event still has a visible
equivalent: the bank-by-bank light bands, the hatch frames, the rising shelf
sprites, the dimmed hall after lights out, and the settlement screen
(撤离带回 / 阵亡) instead of the stings.

### Predicted failure cases

1. **A click at the loop seam** if Godot's import settings override the runtime
   `loop_offset`. The seam was measured on the decoded OGGs (step 0.005 / 0.003
   against a typical 0.017 / 0.011), so a click would come from the engine side.
2. **The fail sting on boot**, from the interrupted-contract path above.
3. **Hatch pile-up**: four hatch sounds inside 0.3 s too loud or phasey.
4. **Base music starting under the sting** if the sting's `finished` signal is
   missed; the base track must wait on it.

### Audio revisions (observed while wiring, 2026-10-07)

What `tests/test_audio.gd` found against the predictions above:

- **Event counts: as predicted.** One walk-in on the default save: lights 4, hatch 4,
  shelf 4; one walk-out: lights-off 1; standing in the room or leaving adds nothing.
- **Pause: as predicted.** In the field the loop holds its position (0.000 s moved
  over 30 frames with the pause menu open) and resumes from there; in the base it
  ducks to -16 dB and returns to -6 dB.
- **Death / extraction / boot settle: as predicted.** One sting per settle (calling
  `settle()` twice still gives one), the base track waits for it, and the
  interrupted-contract settle on boot plays nothing (failure case 2 did not happen).
- **Not predicted: music still playing at quit is reported as leaked**
  (`ERROR: … resources still in use`), which fails `run_all.ps1`. Fixed the way
  `FieldAudio` already does it: headless runs switch tracks and streams but never
  start playback, and the windowed test frees the game and waits 0.3 s before
  quitting (as `test_ui_v1` does). The pause and resume checks therefore only test
  real playback in the windowed `-Visual` pass.
- **Not predicted: two engine details.** A paused `AudioStreamPlayer` reports
  `playing == false`, and `get_playback_position()` trails the mixer by one block
  (about 12 ms) right after pausing. The position helper and the test allow for
  both.
- Failure cases 1 (seam click) and 3 (hatch pile-up) **cannot be checked yet**: the
  first needs listening, the second needs the hatch file.

## Failure cases

These are **observed**, not predicted.

1. **Generated poses drift from the reference.** SE walk row faced the wrong way (fixed by mirroring); SW and N combat rows are near-duplicates (open).
2. **Sprites shrink or clip after slicing.** The uniform-grid slicing of the combat atlas shrank the sprite to 80% and clipped the swords. It was replaced by per-cell alignment on 2026-09-29.
3. **Character lost against the background.** Ground surfaces were deliberately prompted as low-contrast, and three-region captures exist. There is no numeric contrast check.
4. **A sound fires twice per event.** This is only guarded for EXIT, CHARGE and the enemy cues. HIT, LOOT and BUILD have no guard, and no automated count exists (see TEST-REPORT).


### Audio revisions (observed while recording the film from a fresh clone, 2026-10-07)

- **Not predicted: a fresh clone had no music at all.** A 720p trial capture of a camp
  start, recorded from a clean `git clone`, came out at −91 dB. A debug run showed
  `GameMusic._streams` was empty. Cause: the new `.gitignore` line `music/` (meant for
  the raw MP3 downloads in `/music/`) also matched `audio/music/`, so all five OGGs had
  never been committed. Fixed in `111bf6e` by anchoring the rule as `/music/`.
  `test_audio` catches this. On the fresh clone of `f770e26` it fails at the missing
  `base` stream. It just runs last, so the gap showed up in the capture first.
- **Confirmed by the same captures (real playback at 4K, Movie Maker):**
  - base music in the hall;
  - the four light banks and lights-off in the warehouse;
  - the field loop during a contract;
  - pause freezes the field;
  - one STING-FAIL at a real death on floor 31;
  - one STING-EXTRACT after a real click on the camp's 撤离 button.
