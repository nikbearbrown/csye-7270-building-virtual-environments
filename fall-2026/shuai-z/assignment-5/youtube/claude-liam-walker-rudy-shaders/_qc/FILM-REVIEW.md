# FILM-REVIEW — Two Shaders for Walker Rudy.

Review of the actual master, `exports/landscape/claude-liam-walker-rudy-shaders.mp4`
(SHA-256 `a1bd8a3c5c20f4ab63d14884f6cf0ab5ca977fc59ff1c030d50dd238ba6d42fa`, 759.2 s, 3840×2160 H.264 30 fps, AAC 48 kHz stereo), by Claude Code on 2026-10-28. On 2026-10-29 shuai-z checked it: "影片我核对过了，没问题，已经上传到Google drive" ("I've checked the film; there is no problem, and I've uploaded it to Google Drive").

## Gates

| Gate | Result |
| --- | --- |
| `tools/check.sh` (the course's `./art godot-gamedev --check`, once per project, before render and at handoff) | PASS for `game/`: 15 source files, 105 exclusions, 3 components, 3 exact excerpts, 3 code → result pairs. PASS for `godot/`: 38 source files, 2 exclusions, 6 components, 4 exact excerpts, 4 code → result pairs |
| Gate T (type) | PASS (TYPECHECK.md) |
| Gate V (frames) | 56 frames sampled, 0 BLOCKER, 0 MAJOR (REPORT.md) |
| Export receipt | `.verified.json`, status `ready`, SHA-256 matches the file |

## Corrections made before the final

1. **Code cut off in the editor view.** A pilot frame of B11 showed lines 12–14 below the panel and the third source note clipped. The excerpts became `weathered_stone.gdshader` 3–13, `hint_experiment.gdshader` 2–13 and `invulnerable_tint_checks.gd` 347–354, and the source notes were shortened on every code beat.
2. **The highlighted line skipped a cue in B11.** The scene picks the last cue whose time has passed in list order, so a cue listed out of time order hid the next one. `build_reel.py` now sorts cues by time.
3. **The roughness map rendered white** in B10: PIL clipped its 16-bit values. It is now scaled to 8 bits, and the card says so.
4. **Gate T, B11 and B15:** the panel footers had 16 and 17 words, over the 12-word limit; shortened.
5. **Gate V, ten stills:** the source lines at the bottom crossed the 5 % title-safe inset; moved up, with the sweep and two-materials grids tightened to make room. B02 and B18 failed the whole-frame contrast measure because engine images fill most of the card; their titles are now declared as the measured text regions, as Assignment 3 did for engine footage.
6. **Gate V, B14:** the provenance chip over the pale sky measured 0.28; the chips' backing was made more opaque (alpha 190 → 235). The first rebuild reused cached gameplay media, so the change did not reach the video until the cache was cleared.
7. **My frame review, B08, B09, B14:** the long left-hand chip (`SCRIPTED INPUT …`, `CAMERA MOVED …`) ran into the right-hand provenance chip on the same row, so both were partly unreadable. The provenance chip now sits one row higher. No gate caught this.

## What I looked at in the master

Frames at 20 / 60 / 90 % of every beat (84 frames, `_qc/review/`):

- Code is readable at full size in every code beat; the highlighted line follows the narration's cue (for example 1 → 3 → 7 → 8 in B05; 3 → 5 → 9 in B11; 349 → 350 in B20).
- Labels are present wherever they are needed: "Godot editor reconstruction" on every code beat; `ENGINE CAPTURE · WINDOW` on the stills from Use It; `HEADLESS TEST OUTPUT` on B21 and B22; on the engine footage, the Movie Maker provenance chip and `SCRIPTED INPUT …` or `CAMERA MOVED BY A FILM-ONLY SCRIPT …` on every frame, `REPLAY 0.5×` / `REPLAY ⅓×`, `CUT · …`, and `HELD FINAL FRAME` on the two holds (3.4 s in B08, 3.1 s in B09).
- The inset in B08 and B09 shows the hearts tinted after each hit, the value falling, three empty hearts after the last hit, and three full hearts after the respawn.
- The hesitant writer completes the correction "Claude" → "hand" (B01).
- The outro card: exact title, @NikBearBrown, one mascot, no subline.

## Sound

Integrated loudness −24.5 LUFS, loudness range 6.1 LU, peak −2.9 dBFS, no clipping. Every beat carries narration. The game's own music and effects play under the 1.0× gameplay at −11 dB; the replays and the props scene carry narration only (the props scene has no sound). The longest stretch without narration is near the end of B14, where 39 s of footage outlasts its narration and is shown at full speed rather than retimed.

## Limits of this review

Claude sampled frames rather than watching every frame, and measured the audio rather than listening to it. The full check is shuai-z's, recorded above in their words; they did not list what they looked at.
