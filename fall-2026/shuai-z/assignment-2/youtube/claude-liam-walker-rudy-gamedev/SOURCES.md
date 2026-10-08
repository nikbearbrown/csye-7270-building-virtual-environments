# SOURCES — claude-liam-walker-rudy-gamedev

## What the film shows

| Evidence | Source | Identity |
| --- | --- | --- |
| Game source, every code excerpt | `walker-rudy/game/` at `3b7aa1c51663c614af1997720223622979ddcfbf` | per-file SHA-256 in `gamedev-evidence.json`; snapshot `316c7dca…` (CAPTURE.md) |
| Gameplay footage and the game's own audio | `capture/run-01.mp4` … `run-04.mp4` (+ `.wav`), Godot Movie Maker on an isolated copy | hashes below; method and driver in CAPTURE.md |
| Outline on/off frames | `stills/outline-on.png`, `outline-off.png` (engine renders at 3840×2160), composed into `stills/outline-pair.png` | diagnostic, labelled |
| Test output | `capture/checks-run.log`, the headless checks re-run on the isolated copy, 2026-10-04 (exit 0, 141 PASS) → `stills/checks-output.png` | |
| Concept text and pillars | `CONCEPT.md` draft v4 | quoted verbatim in B02 |
| Character-sheet pose #7 | `design/character/poses.png` (a code-drawn blockout, `design/tools/make_blockouts.py`), `CHARACTER-SHEET.md` pose table | crop in `stills/trace-1-sheet.png` |
| Prompt, raw outputs | `design/generation-prompts.md` (pose template and the CHAR-HURT line), `ASSET-LOG.md` rows CHAR-HURT-01/-02, `generated/rejected/CHAR-HURT-RUN-B-01.png`, `generated/accepted/CHAR-HURT-02.jpg` | composed in `stills/trace-2-raw.png` |
| Matted frame | `game/content/rudy/frames/CHAR-HURT.png` and its `frames.json` entry | |
| Contrast numbers (1.71, 11.13) | `TEST-REPORT.md`, predicted failure 2 (measured by `design/tools/check_readability.py`) | not re-measured for the film |
| Models, terms, contributions | `SOURCES.md` and `ASSET-LOG.md` of the project | |

Capture hashes (SHA-256): see `gamedev-evidence.json` (result media) and run
`shasum -a 256 capture/*` — the takes are not re-encoded after this record.

## Corrections made while writing (DOUBLE-CHECK LAW)

- "Six sound effects": the slice plays six (`sfx.gd` STREAMS); four planned sounds were never made (SFX-FALL,
  SFX-CHECKPOINT, SFX-SPORE, SFX-BLOCK). The film says a fall plays the hurt cry, as `main.gd:121` does.
- "141 checks": counted from the film's own re-run (`capture/checks-run.log`), not copied from TEST-REPORT.md.
- The apex/rise/fall figures (294 px, 0.38 s, 0.32 s) are the comment on `rudy.gd:60`, which states them for 60 ticks/s.
  They were not re-measured for the film; they are spoken as the source's figures.
- The test re-run is on the film's snapshot, not on the course-repository commit `9871718` named in TEST-REPORT.md;
  TEST-REPORT.md says that commit has the same files as the local one.
- The student is named `shuai-z`, the course folder's name, not the full name.

## Tools used to make the film

| Tool | Version | Use |
| --- | --- | --- |
| Brutalist toolkit (`brutalist.art`), skill `godot-gamedev` + `walker` | checkout `22264a3` | beat sheet contract, Remotion scenes, Kokoro wrapper, compiler, gates |
| Kokoro-82M via kokoro-onnx, voice `am_onyx` ("Liam, in for Bear") | local model `kokoro-v1.0.onnx` | all narration, free and local; not a clone of anyone |
| Remotion | the toolkit's `runtime/remotion` | bookends, editor reconstructions, design boards, verdict, outro |
| Godot | 4.7.2.stable.official.ed1daf0bf | the captures (Movie Maker) and the checks |
| FFmpeg, Pillow, NumPy | local | cutting the captures, chips, stills, the per-beat mix (`tools/build_reel.py`) |
| Claude Code, Claude Opus 5.5 | — | wrote the driver, the tools, the beat sheet and the narration; ran everything |

`GodotDevWorkbench` views are **reconstructions** of Godot's editor layout, labelled on screen. They are
not recordings of an editing session; the code, paths and line numbers in them are verbatim.

## Terms that travel with this film (not acted on: the film is not being published)

The film carries the slice's own audio, as the assignment requires (§4, item 4). shuai-z said on 2026-10-04
that the film will not be published online. If that changes:

- **ElevenLabs** (SFX-STOMP, -HURT, -PORTAL, -SLASH, -PICKUP), free plan: non-commercial use only, and anything
  published with these sounds must have "elevenlabs.io" or "11.ai" in its title (project SOURCES.md / ASSET-LOG.md).
- **Suno** (MUS-LOOP), free plan: personal, non-commercial use only; Suno keeps the rights.
- **Adobe Firefly** (SFX-JUMP): commercial use allowed; keep the Content Credentials.
- **Gemini** images: Google's Generative AI terms (project SOURCES.md).

## Not used

No paid generation for the film (the game's Gemini images, and ChatGPT's rejected frames, came from paid plans; project
SOURCES.md), no ElevenLabs or other paid TTS for narration, no stock footage, no Higgsfield beats, no captions. The
final MP4 was put on Google Drive as the course media copy by shuai-z; it is not published on YouTube or elsewhere.
