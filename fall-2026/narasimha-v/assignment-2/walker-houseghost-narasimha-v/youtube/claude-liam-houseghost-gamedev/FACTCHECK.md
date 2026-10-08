# Fact check — every number spoken in the film

| Claim | Value | Where it comes from |
|---|---|---|
| Capture is native 4K | 3840×2160 | `ffprobe` on `capture/run-01.mp4` |
| Capture is deterministic | 1958 ticks at 60 fps = 32.63 s | driver log `PASS` record |
| Floor gaps | 170 px | `FloorSeg` shapes: 1180→1350, 2520→2690, 3860→4030 |
| Jump reach | 275 px at 300 px/s | `SPEED`, `JUMP_VELOCITY`, `GRAVITY` in `player.gd` |
| A cut jump is shorter | ×0.45 | `JUMP_CUT` in `player.gd` |
| Footsteps were louder than the flip | +5 dB RMS at matched peaks | measured on the source wavs |
| Audio size after conversion | 22 MB → 1.2 MB | `du` before and after |
| Ogg importer loop default | `false` | recorded probe output |
| Music ducking | −15 dB | `DUCK_DB` in `audio.gd` |
| Checks passing | 13, 0 failed | `tests/test_sound_triggers.gd` |
| Silhouette size | 33 × 96 px | `CHARACTER-SHEET.md` |
| Recognition reached | 2 of 3, calendar 7→3 | driver log |
| Blocked at | x = 2099 by `Memory0` at x = 2200 | scene file + driver log |

No number in the narration is estimated. Where a value could not be measured it is
not spoken.
