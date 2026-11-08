# Sparks and Dust for Walker Rudy. — Assignment 6 film

The required Brutalist Godot explainer for Assignment 6, built with the course-provided **`godot-gamedev`** skill and its **`walker`** modifier: Claude prompt opening → what was actually built → the game, both effects, their jobs, event and condition → the three parts of a particle system and why the headless price is near zero → Effect A: the intent, the process settings and the first strip, the emission settings and tuning round r1, the trigger and the effect in play with rapid repeats → Effect B: the intent, the first strip and rounds r1–r3, the process settings with damping and the effect in play, the world-space trail, the condition with start, stop and pause → two annotated lines of the generated process shader → what the tests proved, the mutations, both prices against the budget, what no headless run shows → Verdict → Your Turn → the regular spoken outro. Liam, in for Bear (local Kokoro `am_onyx`). No captions.

Claude Code (Claude Opus 5.5) built the film on 2026-11-07 at shuai-z's request ("接下来按照作业要求做影片", "next, make the film as the assignment asks"), from the work and records already committed. On 2026-11-07 shuai-z watched the film and uploaded it: "影片看过了，没问题，也已经上传了" ("I've watched the film; there is no problem, and it's uploaded too").

**Source shown:** `fall-2026/shuai-z/assignment-6/` at `d0ed415` (`d0ed4152ba4c5dc88ac2d712dbdb5889b07c9f54`). The game source is unchanged since `d60fb037`. The commit that adds this folder changes no game source.

**Master:** `exports/landscape/claude-liam-walker-rudy-particles.mp4` · 12:22 · 3840×2160 H.264 30 fps, AAC 48 kHz stereo · SHA-256 `6bdc9809c6edd052f5a3ba99150cf553da3ceb6ecdb9bfeb7761e7407aeebbe9` (not in git; `.gitignore` and the repository's rules keep MP4/WAV out). Gates and the frame review: [`_qc/FILM-REVIEW.md`](_qc/FILM-REVIEW.md). Course media copy, uploaded by shuai-z: [claude-liam-walker-rudy-particles.mp4 on Google Drive](https://drive.google.com/file/d/1qAWW-L9Z0K5cUQ3Nql18tFhFgYpp4KuR/view?usp=sharing); it is not published on YouTube or elsewhere. On 2026-11-07 Claude opened the link in a signed-out browser: the file name shows, and the page offers playback. Claude did not download it, so the SHA-256 above is the local master's; the Drive copy is identified by its file name.

## The assignment's film requirements, and where they are

| Requirement (Assignment 6, §4) | Beats |
| --- | --- |
| Identifies the game, both effects, their jobs, and the event and condition that drive them | B02 (crops of the film's own engine capture), B00 |
| The three parts of a particle system, a line from the scene file or the generated shader for each; why a GPU effect's headless price is near zero | B03 (`slash_sparks.tscn` 108, 79, 109; `particles_generated.gdshader` 311); B27 with the numbers |
| Effect A: the intent block, the first strip, each tuning revision (prediction, before and after, verdict), the effect in play with rapid repeats | B04 → B05 → B06 (r0) → B07 → B08 (r1) → B09 → B10 (five cuts, two bursts alive), B11 (the sky, the goblin, the pause) |
| Effect B the same way, plus the feature A doesn't use and its start, stop and pause behaviour | B12 → B13 (r0) → B14, B15, B16 (r1–r3) → B17 (damping) → B18 → B19 (`local_coords` off, `trail_enabled` off) → B20 → B21 → B22 (start, stop, Esc) |
| Two annotated lines of the generated process shader beside the brief's settings | B23 (lines 139 and 311 beside the velocity and gravity rows) |
| What the tests proved, the mutations that failed them, both prices against the budget, what no headless run can show | B24 → B25; B26; B27; B28 |
| Agent mistakes caught, strip readings overruled, what remains uncertain, one next step, human and AI contributions, texture sources, revision shown | BVD1, BVD2 (revision also on every code beat and in B00) |
| Walker opening and summary; Verdict → Your Turn → regular outro | B00, B01 · BVD1, BVD2, BHTF, BOUT |
| Labels: preview captures as fixtures, scripted input, held frames; no reconstruction as a screenshot | `FIXTURE CAPTURE(S)` on every strip card; `SCRIPTED INPUT`, the Movie Maker provenance chip, `REPLAY …×`, `ENLARGED …×`, `ESC · THE GAME IS PAUSED` and `HELD FINAL FRAME` on the engine footage; "Godot editor reconstruction" on every code beat; `HEADLESS TEST OUTPUT` on the logs |

## The evidence chain

| File | What it is |
| --- | --- |
| [`capture/`](capture) | the film-only driver, the harness diff and the run log (the MP4 and the WAV are not in git) |
| [`CAPTURE.md`](CAPTURE.md) | how the take was recorded, the frame/log alignment check, and the hashes |
| [`checks/game/`](checks/game) | `gamedev-evidence.json`: 19 files in 6 components, 117 excluded with a reason, 7 excerpts, 7 code → result pairs with hashed media |
| [`COMPONENTS.md`](COMPONENTS.md) · [`SHOTLIST.md`](SHOTLIST.md) · [`RIFF.md`](RIFF.md) | readable views of the same, generated from the sheet and the ledger |
| [`FACTCHECK.md`](FACTCHECK.md) · [`SOURCES.md`](SOURCES.md) · [`PROMPTS.md`](PROMPTS.md) | every spoken number with its source; provenance, textures and corrections; every prompt shown |
| [`beat_sheet.json`](beat_sheet.json) · [`tools/`](tools) | the beat sheet, and the scripts that build the stills, the sheet, the media and mix, the ledger and the docs |
| [`stills/`](stills) | every evidence card and figure the film shows |
| [`BUILD-PROMPT.md`](BUILD-PROMPT.md) | the paste-ready rebuild |
| [`_qc/FILM-REVIEW.md`](_qc/FILM-REVIEW.md) | the gates and Claude's review of the master |

```bash
tools/check.sh
```

## Honesty boundary

- Godot editor views are **reconstructions** with verbatim source and line numbers, labelled as such. No live editing session was recorded.
- The gameplay is the real main scene rendered by Movie Maker, with **scripted input** from a film-only driver on an isolated copy, labelled on every frame. Replays are labelled with their speed; enlarged replays say so; held frames are labelled.
- The frame strips are **fixture captures** of the preview scenes, labelled on every card. Claude's readings and predictions on them are quoted from `TUNING.md` and called claims; the verdicts are shuai-z's.
- The Visual Profiler crop and the paused frames are **Codex's** captures from Use It, and the film says so.
- Headless results are shown as recorded logs, labelled, and the film says what they cannot show.
- The human checks in the verdict are shuai-z's, reported from `TUNING.md` and `TEST-REPORT.md`; nobody else has played the game.
