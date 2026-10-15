# Three Props for Walker Rudy. — Assignment 3 film

The required Brutalist Godot explainer for Assignment 3, built with the course-provided **`godot-gamedev`** skill and its **`walker`** modifier: Claude prompt opening → what was actually built → the game and the brief → the real Blender session (screenshots, one prompt and the code it ran, what it built, the hand edit, the revision cycle) → Godot source, each excerpt followed by its visible result → Verdict → Your Turn → the regular spoken outro. Liam, in for Bear (local Kokoro `am_onyx`). No captions.

**Source shown:** `fall-2026/shuai-z/assignment-3/` at `f6f8acf` (the Godot project in `godot/` is unchanged since). The commit that adds this folder changes no game source.

**Master:** `exports/landscape/claude-liam-walker-rudy-3d-props.mp4` · 6:31 · 3840×2160 · SHA-256 `e5372f47fd683d2bd3765ab3006afe9b1bbe520f1c96c16cc4cf001a13fe7276` (not in git; `.gitignore` and the repository's rules keep MP4/WAV out). Gates and the frame review: [`_qc/REPORT.md`](_qc/REPORT.md). Course media copy: [claude-liam-walker-rudy-3d-props.mp4 on Google Drive](https://drive.google.com/file/d/1Kwu9iYwfaDHa3HdD_G-FQ89Ik9Yynv0c/view?usp=drive_link); it is not published on YouTube or elsewhere.

## The assignment's film requirements, and where they are

| Requirement (Assignment 3, §4) | Beats |
| --- | --- |
| Identifies the game, the three assets and why the game needs each | B00, B01, B02 (the 2D art at one scale, with each prop's role), B03 (the brief) |
| Shows the real Blender session, labelled: own screenshots; reconstructions labelled | B04 (shuai-z's own screenshots); B06–B09 (Blender viewport images from the MCP `look` tool, labelled as Claude's captures) |
| At least one prompt to Claude and what it built | B05 (the 20:14 prompt, verbatim, and the code Claude ran) → B06 (what it built) |
| The hand edit | B07: before/after comparison stills (option b — no recording exists; labelled), B08 (in the revision cycle) |
| The three assets in the running Godot scene | B11: native 4K Movie Maker capture of the real main scene, one camera orbit added for the film (labelled) |
| The headless numbers beside the brief, labelled as headless | B12 → B13 (`HEADLESS CHECK OUTPUT`: brief, Blender, Godot), B14 → B15 (the check can fail; diagnostic, labelled) |
| What was checked, what remains uncertain, what Claude got wrong, one next step, human and AI contributions, the source revision | BVD1, BVD2 (revision `f6f8acf` also on every code beat and in B00) |
| Walker opening/summary; Verdict → Your Turn → regular outro | B00, B01 · BVD1, BVD2, BHTF, BOUT |

## The evidence chain

| File | What it is |
| --- | --- |
| [`capture/`](capture) | the orbit driver and the copy's `project.godot` diff, the run log, the two check logs and the diagnostic diff (the MP4 is not in git) |
| [`blender-looks/`](blender-looks) | the MCP `look` images used, with times in CAPTURE.md |
| [`CAPTURE.md`](CAPTURE.md) | how each piece of evidence was recorded, and its hash |
| [`gamedev-evidence.json`](gamedev-evidence.json) | all 11 authored files in `godot/` with SHA-256 → 4 components; 3 verbatim excerpts; 3 code → result pairs with hashed media |
| [`COMPONENTS.md`](COMPONENTS.md) · [`SHOTLIST.md`](SHOTLIST.md) · [`RIFF.md`](RIFF.md) | readable views of the same, generated from the sheet |
| [`FACTCHECK.md`](FACTCHECK.md) · [`SOURCES.md`](SOURCES.md) · [`PROMPTS.md`](PROMPTS.md) | every spoken number with its source; provenance and corrections; every prompt shown |
| [`tools/`](tools) | the scripts that build the stills, the sheet, the media and mix, the ledger and the docs |
| [`BUILD-PROMPT.md`](BUILD-PROMPT.md) | the paste-ready rebuild |

```bash
./art godot-gamedev --check ../course-fork/fall-2026/shuai-z/assignment-3/youtube/claude-liam-walker-rudy-3d-props --game ../course-fork/fall-2026/shuai-z/assignment-3/godot
```

## Honesty boundary

- **No recording of the Blender session exists.** The Blender images are shuai-z's own two screenshots (B04) or the MCP `look` tool's images, which Claude captured (B06–B09); each is labelled. The hand edit is shown as before/after stills, not a recording; the after still was captured for the film from the saved file.
- Godot editor views are **reconstructions** with verbatim source and line numbers, labelled as such.
- The Godot footage is the real main scene; only the camera moves, driven by a film-only autoload on an isolated copy. No frame was sped up, slowed or cropped.
- The raised-waystone run is a **diagnostic** on an isolated copy, labelled; the project's scene was not changed.
- The human check in the verdict is shuai-z's, reported from TEST-REPORT.md; nobody else has looked at the scene.
