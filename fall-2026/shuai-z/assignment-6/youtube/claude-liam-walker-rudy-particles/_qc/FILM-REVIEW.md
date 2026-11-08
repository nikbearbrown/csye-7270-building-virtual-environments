# FILM-REVIEW — Sparks and Dust for Walker Rudy.

Review of the actual master, `exports/landscape/claude-liam-walker-rudy-particles.mp4`
(SHA-256 `6bdc9809c6edd052f5a3ba99150cf553da3ceb6ecdb9bfeb7761e7407aeebbe9`, 742.4 s, 3840×2160 H.264 30 fps, AAC 48 kHz stereo), by Claude Code on 2026-11-07. On 2026-11-07 shuai-z watched it: "影片看过了，没问题，也已经上传了" ("I've watched the film; there is no problem, and it's uploaded too").

## Gates

| Gate | Result |
| --- | --- |
| `tools/check.sh` (the course's `./art godot-gamedev --check`, before render and at handoff) | PASS: 19 source files, 117 exclusions, 6 components, 7 exact excerpts, 7 code → result pairs |
| Gate T (type) | PASS (TYPECHECK.md), after one fix (below) |
| Gate V (frames) | 66 frames sampled, 0 BLOCKER, 0 MAJOR (REPORT.md) |
| Export receipt | `.verified.json`, status `ready`, SHA-256 matches the file |

## Corrections made before the final

1. **Gate T, B09, B19, B21:** the code panels' footers had 14, 15 and 14 words, over the 12-word limit; shortened, and those three beats re-rendered.
2. **My frame review, B13:** the two lines on how Claude measured the invisible dust overlapped the second row's captions on the card. No gate caught it. The lines moved down; the card's commit reference was also wrong (`017e8a52`, the build, instead of `c69523ca`, the r0 strip) and was corrected. The master was compiled again.
3. **Before the render** (SOURCES.md and FACTCHECK.md list them): the game card's whole frames became crops around Rudy; the gameplay holds of 6–10 s became 1.7–4.6 s by adding real footage; one enlargement moved to the level's left edge so the trail stays in it; Chinese quotations were rendered as boxes and now use a CJK font; three narration lines and one card were corrected against `TUNING.md`.

## What I looked at in the master

Frames at 20 / 60 / 90 % of every beat (99 frames, `_qc/review/`, reduced to 960 × 540):

- Code is readable at full size in every code beat, and the highlighted line follows the narration's cue (for example 73 → 77 → 80 in B05; 35 → 43 → 46 in B09; 54 → 56 → 58 in B21).
- Labels are present wherever they are needed: "Godot editor reconstruction" on every code beat; `FIXTURE CAPTURE(S)` on the six strip cards and on B28; `HEADLESS TEST OUTPUT` on B25 and B26; on the engine footage, the Movie Maker provenance chip and `SCRIPTED INPUT …` on every frame, `REPLAY …×` with `ENLARGED …×`, `ESC · THE GAME IS PAUSED`, and `HELD FINAL FRAME` on the five holds.
- The engine footage shows what the narration says: the flash on frame 214; overlapping bursts during the five cuts; the spray going left after the turn; the goblin squashed and gone while its sparks finish; the trail rising behind Rudy and stopping in the air; the paused frames with the "Paused" overlay.
- The hesitant writer completes the correction "Claude" → "eye" (B01).
- The outro card: exact title, @NikBearBrown, one mascot, no subline.

## Sound

Integrated loudness −24.5 LUFS, loudness range 6.1 LU, peak −3.0 dBFS. Every beat carries narration. The game's own music and effects play under the 1.0× gameplay at −11 dB; the replays carry narration only. The longest silence below −50 dB is 1.9 s, between beats.

## Limits of this review

Claude sampled frames rather than watching every frame, and measured the audio rather than listening to it. The sparks are small in the full 4K frames of the game, as they are in the game; the replays enlarge them. The full check is shuai-z's, recorded above in their words; they did not list what they looked at.
