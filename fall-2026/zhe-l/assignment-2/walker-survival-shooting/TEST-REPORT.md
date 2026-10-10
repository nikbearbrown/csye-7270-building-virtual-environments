# Test report — walker-survival-shooting

- **Source revision tested:** `f848d84` (the `godot/` folder has not changed since `69b0608`)
- **Engine:** Godot v4.7.2.stable.official.ed1daf0bf
- **Operating system:** Windows 11 Home 10.0.26200
- **Date:** 2026-10-09

There is no playable asset slice yet, so most of the required checks could not be run. Each row says what was actually done.

## Required checks
| Check | Result |
|---|---|
| Startup and controls | Partly checked. The project imports and `base.tscn` runs from a fresh copy (automated check 1). There are no controls yet. |
| Character against the sheet | Not done: there is no character in the scene. |
| Storyboard against the slice | Not done: no storyboard panel is playable yet. The greybox is the room that panels 1–4 take place in. |
| Sound events | Not done: the sound effects are not connected to any game event. |
| Music | Not done: no music has been generated. |
| Muted play | Not done: there is nothing to play yet. |
| Automated check | Done: see automated check 1. |
| Human playtest (sound on and muted) | Not done: there is no playable slice. |

## Automated check 1 — the project runs from a fresh copy
Exports the submitted revision into an empty folder, so nothing from my working copy (such as the `.godot/` cache) is used.

```bash
git archive f848d84 fall-2026/zhe-l/assignment-2/walker-survival-shooting/godot | tar -x -C <empty folder>
Godot_v4.7.2-stable_win64_console.exe --headless --path <folder>/.../godot --import
Godot_v4.7.2-stable_win64_console.exe --headless --path <folder>/.../godot --quit-after 120 res://base.tscn
```

Result: both commands exited with code 0. The import step imported `icon.svg` and `test_chair.glb`. Running `base.tscn` for 120 frames printed no errors or warnings (0 matches for "error", "warning", or "failed" in the log).

## Other checks already recorded
- **Stair ramp (2026-10-08):** a headless raycast check confirmed that the invisible collision ramp over the stairs matches the step edges (`FRICTIONAL.md`, 2026-10-08). The exact command was not saved, so it is not repeated here.
- **Sound reproducibility (2026-10-09):** re-running a sound with the same prompt and seed gave identical decoded audio (MD5 of the decoded audio; pairs listed in `SOURCES.md`).
- **Re-run while making the film (2026-10-09):** automated check 1 was run again on a fresh export of `f848d84` (both exit 0, 0 errors or warnings), and a new stair-ramp raycast check (`youtube/claude-liam-walker-survival-shooting-gamedev/capture/ramp_check.gd`) passed: the ramp surface meets step edges 1–5 within 0.7 mm and ends at step 6. Logs: `youtube/claude-liam-walker-survival-shooting-gamedev/evidence/`. These are headless checks run by Claude, not playtests.
- **Negative prompts (2026-10-09):** outputs that differed only in the negative prompt were identical, because every audio run used CFG 1.0 (`SOURCES.md`).

## Inspect-and-revise cycle
The sound effects went through observation-driven revisions, recorded in the `SOURCES.md` asset log and in `FRICTIONAL.md` (2026-10-09):
- Power on: the first versions (V01) sounded too sharp and explosive, so I changed the design to one clear single beep layered with short radio static; V03 output `00042` was accepted.
- Button press: the first version (around 1 kHz) was too sharp for a sound the player hears many times, so I lowered the target frequency step by step; the 100–200 Hz version `00070` was accepted.

## Known limitations
- No playable slice, so character, sound-event, music, and muted-play checks are missing.
- The error sound still has repeated or tremolo-like tones; I do not yet know how to get one clean tone from the model.
