# Two Shaders for Walker Rudy. — Assignment 5 film

The required Brutalist Godot explainer for Assignment 5, built with the course-provided **`godot-gamedev`** skill and its **`walker`** modifier: Claude prompt opening → what was actually built → the game, the state and the object → the four questions → the brief's colour line → the shader from code, each excerpt followed by its visible result (controlled-value captures, the effect in play) → the textured shader (the textures, the interface sweep, the running scene) → the hint experiment predicted and measured → two materials from one shader → the generated shader beside mine → what the tests proved, the mutations, what no headless run shows → Verdict → Your Turn → the regular spoken outro. Liam, in for Bear (local Kokoro `am_onyx`). No captions.

Claude Code (Claude Opus 5.5) built the film on 2026-10-28 at shuai-z's request, from the work and records already committed. On 2026-10-29 shuai-z checked the film and uploaded it: "影片我核对过了，没问题，已经上传到Google drive" ("I've checked the film; there is no problem, and I've uploaded it to Google Drive").

**Source shown:** `fall-2026/shuai-z/assignment-5/` at `a2a3a77` (`a2a3a77d50c5c9d8a65663d21898b7de54096604`). The runtime source is unchanged since `bd797945` in `game/` and `fe795908` in `godot/`. The commit that adds this folder changes no game source.

**Master:** `exports/landscape/claude-liam-walker-rudy-shaders.mp4` · 12:39 · 3840×2160 H.264 30 fps, AAC 48 kHz stereo · SHA-256 `a1bd8a3c5c20f4ab63d14884f6cf0ab5ca977fc59ff1c030d50dd238ba6d42fa` (not in git; `.gitignore` and the repository's rules keep MP4/WAV out). Gates and the frame review: [`_qc/FILM-REVIEW.md`](_qc/FILM-REVIEW.md). Course media copy, uploaded by shuai-z: [claude-liam-walker-rudy-shaders.mp4 on Google Drive](https://drive.google.com/file/d/1Cx9urHkUlUhYBZ6EGtCq6PX-BPRnuqhX/view?usp=drive_link); it is not published on YouTube or elsewhere. On 2026-10-29 Claude opened the link in a signed-out browser: the file name shows, and Drive was still processing the video for playback. Claude did not download it, so the SHA-256 above is the local master's; the Drive copy is identified by its file name.

## The assignment's film requirements, and where they are

| Requirement (Assignment 5, §4) | Beats |
| --- | --- |
| Identifies the game, the state the effect communicates, and the object given the textured shader | B02 (two frames from the film's own engine captures), B00 |
| Answers the four questions, each pointing at a line of code | B03 (the four lines); what a shader does B05 (`invulnerable_tint.gdshader:8`); material vs shader B07, B17 (`circle_darkstone.tres:9`); a texture is information B10, B11 (`weathered_stone.gdshader:3–5`); the shading language B11, B13 (`:7`, `:9`, `:18–21`) |
| The colour line in the specification, the shader and driver lines, the controlled-value captures, the effect in play | B04 → B05 → B06 (captures at 0.0/0.5/1.0/2.0) → B07 → B08, B09 (Movie Maker, scripted input, labelled) |
| The hint experiment predicted and measured, the interface sweep, two materials from one shader | B15 → B16; B11 → B12; B17 → B18 |
| Two annotated lines of the generated shader beside their equivalents | B19 (`standard_generated.gdshader` 11, 70/72 against `weathered_stone.gdshader` 3, 19/20) |
| What the tests proved, the mutations that failed them, what no headless run can show | B20 → B21; B22; B23 |
| Agent mistakes caught, what remains uncertain, one next step, human and AI contributions, texture sources, revision shown | BVD1, BVD2 (revision also on every code beat and in B00) |
| Walker opening/summary; Verdict → Your Turn → regular outro | B00, B01 · BVD1, BVD2, BHTF, BOUT |
| Labels: reconstructed editor views, scripted-input captures, held frames | "Godot editor reconstruction" on every code beat; `SCRIPTED INPUT`, `REPLAY 0.5×`/`⅓×`, `CUT ·`, `HELD FINAL FRAME` and the Movie Maker provenance chip on the engine footage; `ENGINE CAPTURE · WINDOW` and `HEADLESS TEST OUTPUT` on the stills |

## The evidence chain

| File | What it is |
| --- | --- |
| [`capture/`](capture) | the two film-only drivers, the harness diffs and the run logs (the MP4s and the WAV are not in git) |
| [`CAPTURE.md`](CAPTURE.md) | how each piece of evidence was recorded, the frame/log alignment check, and the hashes |
| [`checks/game/`](checks/game), [`checks/godot/`](checks/godot) | one `gamedev-evidence.json` per Godot project (the checker takes one `project.godot`): `game/` 15 files in 3 components, 105 excluded with a reason, 3 excerpts; `godot/` 38 files in 6 components, 2 excluded, 4 excerpts; 7 code → result pairs with hashed media |
| [`COMPONENTS.md`](COMPONENTS.md) · [`SHOTLIST.md`](SHOTLIST.md) · [`RIFF.md`](RIFF.md) | readable views of the same, generated from the sheet and the ledgers |
| [`FACTCHECK.md`](FACTCHECK.md) · [`SOURCES.md`](SOURCES.md) · [`PROMPTS.md`](PROMPTS.md) | every spoken number with its source; provenance and corrections; every prompt shown |
| [`beat_sheet.json`](beat_sheet.json) · [`tools/`](tools) | the beat sheet, and the scripts that build the inset, the stills, the sheet, the media and mix, the ledgers and the docs |
| [`BUILD-PROMPT.md`](BUILD-PROMPT.md) | the paste-ready rebuild |

```bash
tools/check.sh
```

## Honesty boundary

- Godot editor views are **reconstructions** with verbatim source and line numbers, labelled as such. No live editing session was recorded.
- The gameplay is the real main scene rendered by Movie Maker, with **scripted input** from a film-only driver on an isolated copy, labelled on every frame. The inset is the same frame's hearts, enlarged; the value beside it is what the driver read from the material on that frame. Replays are labelled with their speed; held frames are labelled.
- The props scene is the real main scene; only the camera moves, driven by a film-only script on an isolated copy.
- The stills of the hearts, the sweep, the hint experiment, the two materials and the OS screenshot are the windowed engine captures from Use It. The sweep, the two-materials check and the OS comparison were judged by Claude at shuai-z's request and reviewed by shuai-z; the film says so.
- Headless results are shown as recorded logs, labelled `HEADLESS TEST OUTPUT`, and the film says what they cannot show.
- The human checks in the verdict are shuai-z's, reported from TEST-REPORT.md; nobody else has played the game or looked at the scenes.
