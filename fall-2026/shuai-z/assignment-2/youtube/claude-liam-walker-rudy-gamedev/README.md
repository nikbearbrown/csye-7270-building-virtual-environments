# Walker Rudy, Wired In. — walker-rudy game-development film

The required Brutalist Godot explainer for [walker-rudy](../../), built with the course-provided
**`godot-gamedev`** skill and its **`walker`** modifier: Claude prompt opening → what was actually built →
component-by-component source, each excerpt followed by its visible result in the running slice → Verdict →
Your Turn → the regular spoken outro. Liam, in for Bear (local Kokoro `am_onyx`). No captions.

**Commit IDs in this folder** are the local `walker-rudy` repository's, as the film shows them; the project moved into the
course repository with its history, which gave each commit a new ID with the same files: `3b7aa1c` is `9871718` there,
and `c0e8055` is `440a8f7`.

**Master:** `exports/landscape/claude-liam-walker-rudy-gamedev.mp4` · 9:56 · SHA-256 `cb2f01dbe7f0788b5a8c9196b8168e2f2151e4be09aee4febee018a1165528a0` (not in git; `.gitignore` keeps MP4/WAV out). Gates and the frame review: [`_qc/FILM-REVIEW.md`](_qc/FILM-REVIEW.md).

## The assignment's six film requirements, and where they are

| Requirement (assignment 02, §4) | Beats |
| --- | --- |
| 1. Concept and pillars in plain terms | B01, B02 |
| 2. One asset traced design → prompt → raw output → edits → in-engine | B14 (sheet pose #7) → B15 (prompt, rejected HURT-01, edit, accepted HURT-02) → B16 (frames.json edit record) → B16R (the matted frame the game loads) → B17 (CHAR-HURT in play) |
| 3. Character in two+ states in the running slice; the four sound events in real play | states: B07–B13, B17, B21–B29, B35; jump B03/B11, stomp B03/B21, hurt B17/B25/B27, portal B03/B35 (each with a `SOUND` chip from the log) |
| 4. A clearly labelled segment with the slice's own audio and no narration | **B03**: 17.5 s, `SLICE AUDIO ONLY · NO NARRATION` |
| 5. A source change → what the player sees or hears | B18 → B19: the outline shader's width, 8 vs 0 (diagnostic), hair against wheat |
| 6. Tested, uncertain, next step, human/AI contributions, which model made which asset, source revision | BVD1, BVD2 (revision `3b7aa1c` also on every code beat) |

## The evidence chain

| File | What it is |
| --- | --- |
| [`capture/`](capture) | four native-4K Movie Maker takes (`run-0N.mp4` + `.wav` + `-inputs.jsonl`), the input-only driver, the copy's `project.godot` diff, the checks' and import's recorded output |
| [`CAPTURE.md`](CAPTURE.md) | how the takes were recorded, what the driver may and may not do, the labels |
| [`gamedev-evidence.json`](gamedev-evidence.json) | all 114 authored files with SHA-256 → 10 components; 15 verbatim excerpts; 15 code → result pairs with hashed media |
| [`COMPONENTS.md`](COMPONENTS.md) · [`SHOTLIST.md`](SHOTLIST.md) · [`RIFF.md`](RIFF.md) | readable views of the same, generated from the sheet |
| [`FACTCHECK.md`](FACTCHECK.md) · [`SOURCES.md`](SOURCES.md) · [`PROMPTS.md`](PROMPTS.md) | every spoken number with its source; provenance, corrections and asset terms; every prompt shown |
| [`tools/`](tools) | the scripts that cut excerpts, build stills, media and mix, and write the ledger |
| [`BUILD-PROMPT.md`](BUILD-PROMPT.md) | the paste-ready rebuild |

```bash
./art godot-gamedev --check ../walker-rudy/youtube/claude-liam-walker-rudy-gamedev --game ../walker-rudy/game
```

## Honesty boundary

- All gameplay is **scripted keyboard input through the real engine**, labelled on every frame; it is not a human
  playtest. shuai-z's playtest is reported from TEST-REPORT.md, not shown.
- Godot editor views are **reconstructions** with verbatim source and line numbers, labelled as such.
- Raw generations (B15) are labelled raw and not in-engine; the in-engine result follows in B17.
- The outline-off frame is a **diagnostic** runtime change on an isolated copy, labelled.
- No gameplay was sped up or centre-cut; replays and held frames are labelled. Every sound heard in gameplay
  is the engine's own recorded mix.
- Media (MP4, WAV) stay out of git per the repository's `.gitignore`. The final MP4 is on Google Drive as the course media copy (linked from the project README.md); it is not published on YouTube or elsewhere.
