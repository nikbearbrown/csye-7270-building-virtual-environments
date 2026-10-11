# FACTCHECK.md — every number the film says out loud, and where it came from

One row per claim in the narration. "Where" is the thing a reviewer can re-run
or re-read, not a memory of having seen it.

---

## B00 — the ask

| claim | evidence |
|---|---|
| "The prompt on screen is a reconstruction … not a transcript of anything." | True by construction. `beat_sheet.json` B00 `runningText` says so on screen as well, and the narration says it in the first ten seconds. No build receipt is shown. |
| "a dungeon slice running in Godot four" | `godot/project.godot`: `config/features=PackedStringArray("4.7", "GL Compatibility")`. |
| "this time the character you are looking at was generated" | `godot/assets/poses/p1-idle.png` … `p8-death.png`, provenance in `../../SOURCES.md` §3 and `../../ASSET-LOG.md`. |

## B01 — what changed

| claim | evidence |
|---|---|
| "the same three thousand and seventy-two pixels" | `godot/levels/first_steps.json` → `"width": 3072`. |
| "the eight movement values are the same eight" | `godot/features/player/tuning.gd`, first eight `@export` values, with the comment saying they are the starter's and unchanged. |
| "nine generated images — one reference and eight poses" | `design/character/CHAR-REF-01.png` + `CHAR-P1…P8.png`; imported to `godot/assets/poses/`. |
| "one generated loop" | `godot/assets/music-loop.ogg`, Suno `v6-mini`, `ASSET-LOG.md` 2026-10-04. |
| "The four sound effects are not generated at all; they are synthesised by arithmetic" | `scripts/synth_placeholder_sfx.py`. `godot/assets/README.md` has a "Generated?" column reading **no** four times. |
| "one of those three is a placeholder, which I will say again" | Said again in B06's notes and in B12. |

## B02 / B03 — the pose mapping

| claim | evidence |
|---|---|
| The excerpt is `pose_key()` as written | `gamedev-evidence.json` → `excerpts[B02]`, lines 118–131 of `features/player/player.gd`, byte-identical to the file and to `shot.remotion.props.code`. The ledger refuses to build otherwise. |
| "Death is checked first" | Line 119 is the first branch. |
| "on death the body is disabled and is-on-floor keeps whatever it last returned" | `game/session.gd` sets `player.enabled = false` in `resolve_contacts()`; `death-pose-is-the-same-whatever-killed-you` asserts the pose is identical across spike, fall and enemy. |
| "those transitions are a logged event with the tick it happened on" | `capture/logs/take-p-inputs.jsonl`, `POSE <key>` entries with `tick` and `t_s`. |
| The sequence shown | From that log: idle 0.267, run 0.950, rise 1.433, fall 1.767, run 2.117, idle 2.200, rise 2.433, dash 2.617, fall 2.767, idle 3.067. |

**What B03 does not prove.** That the sprite is the *right* sprite for the
state. The footage shows the character moving and the log shows which key was
live; neither says the artwork is correct. `TEST-REPORT.md` §6 is explicit that
nothing in the suite asserts what the character looks like.

## B04 / B05 — the rim

| claim | evidence |
|---|---|
| The excerpt is `_mrect_o` / `_mpoly_o` as written | `excerpts[B04]`, lines 313–326. |
| "navy armour on a dark wall — one point six to one" | `CHARACTER-SHEET.md` §3b: plate `#1f3a6e` vs wall `#1b1620` = 1.60. WCAG relative luminance. |
| "a 3 px arm keeps one pixel of armour" | 3 − 2×1 = 1. The comment at lines 304–311 carries the same arithmetic. |
| "6.3% … 24.2% … 9.1%" | `scripts/import_pose.py` prints the first two on every run; the 9.1% baseline is measured on the code-drawn character and recorded in the script's own comment and in `ASSET-LOG.md`. |
| The strip shown | `media/B05-poses.png`, hashed in `code_result_pairs`. Built from the committed sprites in `godot/assets/poses/`. |

**Declared on screen:** the rim and the visor restoration are **edits to
generated assets**, not properties of the generation. B04's notes and
`ASSET-LOG.md` both say so.

## B06 / B07 — the trap warning

| claim | evidence |
|---|---|
| The excerpt is `advance_traps()` as written | `excerpts[B06]`, lines 276–288 of `game/session.gd`. |
| "rises over fifteen ticks" | `TRAP_RISE_TICKS = 15`, `game/session.gd`. |
| "Trigger at one thousand and sixty four, spike at one thousand one hundred and sixty" | `godot/levels/first_steps.json`: `{"spike": [1160, 304, 24, 16], "trigger_x": 1064}`. |
| "the warning fired thirty five ticks before the hit" | **Two independent paths.** `capture/logs/take-t-inputs.jsonl` → `WARNING LEAD warned=409 died=444 lead=35`. And `tests/test_game.gd` → `sfx-trap-fires-on-the-trigger-not-the-contact`, `lead_ticks: 35`. |
| "The driver read that out of the sound log" | `capture_gamedev.gd` `take_t()` walks `session.sfx_log` inside the attempt and asserts `lead >= 15`. |
| "the pose the storyboard asked for" | `design/storyboard/panel-06-death.jpg`, drawn 2026-10-03, before the pose was implemented. |

**Declared:** the sound heard in B07 is `godot/assets/sfx-trap.ogg`, which is
**synthesised, not generated**. B06's own notes say it and B12 says it again.

## B08 / B09 — the music guard

| claim | evidence |
|---|---|
| The excerpt is the guard as written | `excerpts[B08]`, lines 601–611 of `game/session.gd`. |
| "this function runs on every single death" | `resolve_contacts()` → `State.DYING` → `_physics_process` counts the retry down → `restart_attempt()`. |
| "a sixteen bar loop" | 16 bars × 1.9352 s = 30.9632 s, which is `music-loop.ogg`'s length as the engine reports it in `music-loop-is-flagged-to-loop`. |
| "playing reports false while a stream is paused" | Observed from the engine before the assertion was written; the regression check `retry-while-paused-resumes-rather-than-restarts` exists because of it. |
| "An ordinary retry moves the playhead forward" | `media/B09-suite-output.txt` / `.png`: `before 0.557 → after 0.651`. |
| "resumes at exactly the position it was paused at" | Same file: `at_pause` and `after_retry` are both `0.663999974727631`. |
| "99 checks / 0 failures" | Same file, last line. The **113** quoted in B12 is that 99 plus `test_keyboard.gd`'s 14. |

**What B09 is not.** It is not a live terminal and the film does not re-run the
suite on camera. The card is a monospace render of the recorded file and the
image is what the ledger hashes. **The two JSON payloads are wrapped one key
per line**; check names, values and their order are verbatim, and the label on
screen says so. The recorded lines are 91 characters wide, which renders at
29 px on a 3840-wide frame; the wrap buys 42 px.

## B10 / B11 — the blade

| claim | evidence |
|---|---|
| The excerpt is `_draw_swing()` as written | `excerpts[B10]`, lines 678–690. |
| "the same three numbers the kill hitbox is built from" | `ATTACK_PIVOT`, `attack_angle()`, `tuning.attack_reach` in both `_draw_swing()` and `_sync_attack_hitbox()`. |
| "the bright wedge only appears while the swing can actually kill" | Line 680: `if attack_phase() >= 2`. The hitbox is live for exactly the active window. |
| "the poses were prompted 'empty hand, NO weapon'" | `ASSET-LOG.md`, the `CHAR-P6` / `CHAR-P7` rows, verbatim. |
| "Nine active ticks, both facings" | `tuning.gd`: `attack_active_ticks = 9`. `attack-hitbox-on-the-blade-right` / `-left` sample 9 ticks each. |
| "four millionths of a pixel" | 3.8 × 10⁻⁶ px right, 3.9 × 10⁻⁶ px left, from those two checks. |

## B12 — the verdict

| claim | evidence |
|---|---|
| "measured at 124.018 BPM" | `ASSET-LOG.md` 2026-10-04: recovered from the audio by onset envelope + autocorrelation + a comb refinement, **not** taken from the prompt, which asked for 124. |
| "all four sound effects … synthesised placeholders" | `godot/assets/README.md`, `SOURCES.md` §4. |
| "No seed from either generator" | Suno exposes none (`ASSET-LOG.md` music section). The art model exposes none (`ASSET-LOG.md` `CHAR-REF-01` row). |
| "that broke a rule this project had written down for itself" | `CHARACTER-SHEET.md` §8, made binding by the correction dated 2026-10-04. |
| "113 automated checks, 0 failures" | 99 + 14. `TEST-REPORT.md` §1. |
| "it asserts nothing at all about what the character looks like" | `TEST-REPORT.md` §6. |
| "Two real art bugs passed all of them" | The air-pose sign error and the grey-pipework rim. `TEST-REPORT.md` §5, `FRICTIONAL.md` 2026-10-05. |

## B13 — your turn

| claim | evidence |
|---|---|
| "recovery is three ticks, fifty milliseconds" | 16 − 4 − 9 = 3 ticks; 3/60 s = 50 ms. `tuning.gd`. |
| "the suite will pass either way" | `pose_key()` already returns `"live"` for phase ≥ 2, so adding a `"recovery"` key is a change the existing check would follow rather than fail. Stated as the lesson, not as a defect. |

## B14 — the outro

Locked card. Exact title, `@NikBearBrown`, one slug-seeded mascot, no subline,
no narration, no game audio, existing stock jingle only. `OUTRO-LOCK.md`.

---

## Corrections made while building this film

Kept because a film about checking things should say what its own checks caught.

| | |
|---|---|
| Two component names were invented | `./art scenes --check` rejected `ClaudeHesitantWriter` and `ClaudeYourTurn`. The real ones are `BrutalistHesitantWriter` and `ClaudeComposerAsk` reused. |
| B09 carried numbers typed from memory | They disagreed with the recorded run. The card now quotes the file. |
| A path was in both `files[]` and `exclusions[]` | Checker caught it. |
| The ledger read a stale inventory | It was missing `tests/capture_gamedev.gd`, this film's own capture driver. The inventory is walked live now. |
| Recorded output was in `props.code` | It is not a source excerpt; the checker said so. |
| A `.txt` was offered as result evidence | "Result evidence must be visible media." It is a render of that text now. |
| The B02 pilot clipped | A 17-line excerpt showed 14, with the last cue pointing off-screen and a note cut mid-word. Excerpts are ≤ 14 lines and notes ≤ 100 characters. |
| Three takes stalled against walls | x 151.0, x 567.0 and x 567.0 again. The jump marks come from the level, not from my reading of it. |
| `sfx_log` came back empty | `restart_attempt()` clears it; the evidence has to be read inside the attempt that produced it. |
| B09's `tree` prop disagreed with the recorded file | It carried `at_pause: 0.744000017642975` where the file says `0.663999974727631` — a second, stale copy of a number the card already quotes. The prop is derived from the file now. The beat renders in `asset` mode and never displayed it, so nothing on screen was ever wrong. |
| The two evidence images did not fit the panel they render in | Composed to no particular aspect, they left up to 59 % of the workbench's image area unused. They are composed to its measured 1529 × 987 now. Found by sampling frames out of a finished master; Gate V does not check this. |
