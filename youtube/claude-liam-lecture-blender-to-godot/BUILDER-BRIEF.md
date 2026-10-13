# BUILDER BRIEF — lecture: "Proving a 3D Model Arrived in Godot"

You are one of several builders authoring ONE act of a whole-chapter lecture film (the `lecture` skill, channel
claude-liam: Liam in for Bear, Kokoro am_onyx, free). Narration is written and voiced; your job is the PICTURE for
your beats. The film is 80 beats / ~15 min. Act I (B01–B07) is built and is your working exemplar.

Reel folder (call it REEL):
`/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-blender-to-godot/`
Toolkit (TK): `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/`
Source chapter: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/chapters/03-blender-mcp-to-godot.md`
Chapter's evidence record (real runs): `.../csye-7270-building-virtual-environments/examples/03-blender-mcp-to-godot/` (logs/, transcripts/, scripts/, README.md, PROMPTS.md)

## 0. Read first (in this order, fully)
1. `TK/skills/make/lecture/SKILL.md` — esp. BEST-BEAT LAW (audition ≥2 lanes per beat, pick the one whose MOTION is the claim), SHOW-THE-THING LAW (a tool is shown as itself: capture → library skin → built card; nothing invented on a tool's screen), PRIMARILY VISUAL, MOTION CARRIES THE CLAIM, ONE LOOK, ONE CAST PER ACT.
2. `TK/skills/make/show-tell/SKILL.md` DRAWING LAWS + the long list of GATE B/T/V traps (they apply to every Manim scene here).
3. `TK/skills/make/nopunt/SKILL.md` (catalog), `REEL/narration.py` (every line, in order — know what comes before and after your beats), `REEL/beat_sheet.json` (`actual_duration_s` per beat = the clock).
4. `REEL/kit.py` (palette, `T`, `M`, `Iso`, `until`, `done`, `guard`, `dim_arrow`), `REEL/scenes_act1.py` + `REEL/lanes/act1.json` (the exemplar: how a scene is paced, how a lane entry reads), `REEL/preflight.sh`.
5. If your beats show Claude Code / Codex: `TK/skills/make/cc-explainer/SKILL.md` (CC kit: CCSession, CCToolCall, CCPromptBar, CCPlainShell, REAL-SESSION and TYPES-NOT-NARRATES laws).

## 1. What you deliver (and only this)
- `REEL/scenes_act<N>.py` — your beat classes + act-prefixed helpers (`a<N>_...`). NO imports of kit (it is pasted by `assemble_scenes.py`), no `from manim import *` needed (the kit has it). Do not define anything that collides with kit names.
- `REEL/lanes/act<N>.json` — one entry per beat (schema in section 4). Remotion beats (CCPlainShell, ClaudeCodeBeat, CCSession…, BrowserCapture, LibraryIconRow) are fully specified here (pattern + props); `"durationSeconds": "__AUDIO__"` is replaced with the measured audio by make_sheet.
- `REEL/factcheck/act<N>.md` — table ROWS ONLY, format `| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |`, verdicts PASS / CORRECTED / EXEMPT. One row per checkable claim in your beats' narration AND per number/text you put on screen. VERIFY each against the chapter, the examples' logs/transcripts/scripts, or the cited primary doc — do not copy the chapter's own assertion as proof. If a spoken claim is wrong or unverifiable, say so in the row (CORRECTED + the fix) and in your final report; DO NOT edit narration.py.
- New real evidence you generate goes in `REEL/evidence/act<N>/` (scripts + their output, so it is reproducible); images you display go in `REEL/pantry/` (prefix `a<N>_`). Remotion captures that need `staticFile` go in `TK/runtime/remotion/public/lecture-blender-to-godot/` (create it; touch nothing else in TK).
- Final report (your last message): per beat → lane picked, runner-up, one-line why; anything you could not finish or verify; any narration problem; commands to re-run your evidence.

## 2. Hard laws for Manim scenes (the costly traps — already learned)
- Scene classes: literally `class B45_Name(Scene):`; the name starts with the beat id (`B33A_Formats`); never subclass a helper (run.sh scene discovery is textual and would slate it).
- End every scene with `done(self)`. Pace with `until(self, "exact phrase from the narration", lead=…)`. `[pace] ... OVER` in preflight output means the clip outruns its audio and compile will centre-cut it: shorten. Leave ≥0.1 s slack.
- MIDPOINT RULE: GATE T and Gate V sample each clip at 50%. `self.play` is guarded automatically (kit's ST), but `self.wait` is not: the 45–55% frame must be a still that already contains the label(s) that matter — nothing half-faded, mid-sweep, mid-draw, or a lone empty frame.
- Gate A (static stub): every scene must add ≥1 NEW non-text, non-Rectangle shape (Line/Dot/Arrow/Circle/Polygon/Create/GrowFromCenter…) AFTER its first frame, and the shape set must change; moves/fills/Transform of existing shapes do not count. Never do arithmetic on `c2p()/n2p()` results; never position with `Text.get_left()/get_right()` or `mob.get_right()` (the stub returns off-frame values): write explicit coordinates; wrap group slices as `VGroup(*…)`; wrap `get_center()` in `np.array(...)` before subtracting.
- Forbidden: `rate_functions.ease_in_quad`, `ease_out_cubic` (use kit `ease_in`); `.animate(path_arc=…)` (use `MoveAlongPath(obj, ArcBetweenPoints(a,b))`); `MoveAlongPath` and `.animate` on one object in one `play`; `FadeOut` of a NEW copy of a label (keep references).
- Type: EB Garamond via `T(...)`, size ≥ 32 (titles/act titles 40, hero numbers bigger), Menlo via `M(...)` ≥ 32. Terracotta (`TERRA`) is NEVER text and never a thin/short stroke or underline: use a terracotta DOT or a small spark beside the thing. Numerals and step markers are ink. No fill behind text (Gate B fails highlighter rectangles): outline-only cells with ≥0.25 padding. No line, outline, or arrow touching or crossing text; ≥0.3 unit gap between a leader line and its label. Labels sit BESIDE objects.
- Frame: stay inside ±6.2 × ±3.3 (the audit warns past ±6.3 × ±3.4, measured on text edges). Long mono lines: at size 32, Menlo ≈ 0.25 units per character.
- Dark ink-coloured shapes packed together fuse into one "text blob" under GATE T: draw bars/blocks in the greys (`BAR1/BAR2/BAR3`, `DIM`, `GHOST`), outline small objects in ink only if they are large; a large near-black field fails (use DIM). Chart/table lines in `DIM`; only the ONE row that matters is ringed/in ink.
- Pango drops some single spaces in `Text()` on this Mac (words fuse: "fingerprintsin"): LOOK at the rendered still; if words fuse, double the space at that boundary. A `Paragraph` line must not START with a lowercase `w`.
- `Transform` of different polygons crumples mid-flight; morph like-for-like (Rectangle→Rectangle, same vertex count) or fade/replace. `Indicate` the whole group, not one part.
- Manim caches partial movie files by animation hash: after replacing an image file behind the same path, change the name, or the old pixels replay.
- Do not shrink the laws to fit a layout: split the beat's picture, or tighten the text.

## 3. Real things, shown as themselves
- Tools named in narration are SHOWN: Blender → its real icon (`pantry/icon_blender.png`), its real window (`pantry/blender_window.png`, 3456×2006 — a REAL screenshot of Blender 5.1.2 with the post loaded; crop/zoom with camera moves, not shrunk), real Blender renders (`pantry/post_visual.png`, `post_collider_only.png`, `post_front*.png`; transparent PNGs, 2400×1350, the post is centred and small in frame — crop with `ImageMobject` then `.scale/.shift` or crop in PIL into a new pantry file). Godot → `pantry/icon_godot.png`. Claude Code / Codex → the CC kit / Codex templates (read the skills; `./art scenes "<tool>"` then `./art scenes --check <Name>`: only RENDERABLE names; `FlowDiagram` is NOT renderable even though older docs name it).
- Real command lines and their output are replayed VERBATIM (`CCPlainShell`, or Menlo text in Manim for a few short lines) from `examples/03-.../logs/*` or from output you re-run (EXECUTABLE-EVIDENCE: run it, keep stdout, label it recorded output). Never invent output, error text, UI labels or numbers. Quotes: paraphrase or keep under ~15 words with attribution.
- If the real thing cannot be captured (e.g., MCP route was not run in the chapter), say so honestly on screen ("documented, not run") and show only what is true (architecture diagram, the real README sentence).
- Remotion beats: test with `cd TK/runtime/remotion && npx remotion still src/index.ts <Pattern> /private/tmp/claude-501/<yourscratch>/<name>.png --frame=<n> --props='<json>'` at ~25%, 50%, 95% of the beat (Remotion fps is 30; frames = duration × 30) and LOOK at the PNGs. At 4K, body text ≥ 48 design px, tracked headings ≥ 54, chips ≥ 32; headings ink. Any Remotion `at` cue must stay out of the 45–55% window. Do NOT use `art run`, `art final`, `remotion_scenes.py` or `make_sheet.py` on the reel, and do not edit TK components (a genuinely needed new component is a REPORT to the lead, not a build).
- A tool or website you want to capture in a browser: only public pages, no sign-in, 1600×900 at device scale 2.4 (3840-wide PNG) → `TK/runtime/remotion/public/lecture-blender-to-godot/…` → `BrowserCapture` with the real URL, a dated caption, camera moves that push in to what the sentence names (see `TK/skills/make/medhavy-walkthrough/` for the capture gotchas). Check what is installed (Playwright / Chrome headless) before planning on it; fall back honestly if it is not worth it.

## 4. Lane entry schema (`lanes/act<N>.json`, keys = beat ids)
```json
"B13": {"lane": "manim", "class": "B13_Name", "visual_intent": "what is on screen, concretely",
        "motion_claim": "the motion the voice can point at", "show": [{"at": 0.3, "event": "…"}],
        "runner_up": "the second lane you auditioned", "why": "why this one wins", "sparse": true}
"B15": {"lane": "remotion", "pattern": "CCPlainShell", "props": {"title": "…", "lines": [...], "durationSeconds": "__AUDIO__"},
        "visual_intent": "…", "motion_claim": "…", "show": [...], "runner_up": "…", "why": "…"}
```
`sparse: true` (default) waives only Gate V underfill/clustered for beats that are deliberately one-object-on-cream; set `false` for beats that fill the frame on their own. A beat with no `runner_up` was not auditioned.

## 5. Preflight (run it constantly)
`REEL/preflight.sh <N> B45_ClassA B46_ClassB …` → assembles kit + your `scenes_act<N>.py` into a private scratch, runs the Gate A static check (from a folder holding only scenes.py), the layout audit (fix every WARN), and a low-res LAST-FRAME still per class at `/private/tmp/claude-501/lecture-blender-act<N>/stills/<Class>.png`. LOOK at every still (and, for motion beats, render a mid-frame too: `manim -ql --save_last_frame` shows only the end; `manim -ql -s` + a sleep of `self.wait` early in a scratch copy, or `manim -ql scenes.py Class` then grab frames with ffmpeg from the mp4 at 25/50/95%). A gate-clean scene that reads as a slide fails the still-frame test: the picture must MOVE to carry the claim.

## 6. Do not
- edit `narration.py`, `make_sheet.py`, `kit.py` (report kit needs), other acts' files, `beat_sheet.json`, `mp3/`, or anything in TK;
- run 4K renders, `art run/final/post`, anything paid, anything that publishes;
- invent facts, numbers, interface output, or quotes;
- say "this chapter", "the book", or name a course in anything shown on screen.
