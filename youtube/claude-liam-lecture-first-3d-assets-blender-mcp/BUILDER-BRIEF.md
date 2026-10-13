# BUILDER BRIEF — lecture: "Your First 3D Game Assets with Claude and Blender"

You are one of seven builders, each authoring ONE act of a whole-document lecture film (the `lecture` skill, channel claude-liam: Liam in for Bear,
Kokoro am_onyx, free). Narration is written and VOICED (do not edit it); your job is the PICTURE for your beats. The film is 79 beats / about 13 min.
It explains a university assignment: students make three simple 3D game assets with Claude, the Blender MCP and Blender, export them as .glb and
check them in Godot. The source is the assignment text itself (REEL/ACTS.md maps it to acts).

Reel folder (call it REEL):
`/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-3d-assets-blender-mcp/`
Toolkit (TK): `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/`
Source: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/assignments/03-first-3d-assets-with-blender-mcp.md`
Your act's beats and lane suggestions: `REEL/LANE-PLAN.md`. The real evidence you display: `REEL/EVIDENCE-INDEX.md` (images in `REEL/pantry/ev_*.png`, logs and scripts in `REEL/evidence/`).
A COMPLETE worked example from a sibling film built with the same kit: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-blender-to-godot/` (its `scenes_act1.py`, `lanes/act1.json`, `lanes/act2.json`, `factcheck/act1.md`). Read, do not edit.

## What is different about THIS film (read twice)
- **Honesty first.** The course has NEVER run the Blender MCP route. No beat may show an MCP session, an MCP tool call's output, a Claude Code session working in Blender, or the MCP add-on's panel as if it ran. Commands the assignment tells students to type (`brew install uv`, `claude mcp add ...`, `uvx mcp-for-blender install-addon`) are shown on `CCPlainShell` WITHOUT output, and the shell/card says on screen "documented, not run". The script route (`Blender -b ... --python-exit-code 1 --python ...`) WAS run for real: show its real log. README text is shown as the project's own words (document skin, 15 words or fewer per quote, attributed, with the version and date from REEL/evidence/mcp/).
- **Everything displayed is real or labelled.** Real Blender windows and renders, real Godot output, real numbers from REEL/evidence/. A drawing may show an idea (a Manim diagram of an origin); it may not show a tool's interface. Illustrative values are labelled "example".
- **One look.** Claude palette: stage #F2F0E9 / cream #FAF9F5, ink #3D3929, terracotta #D97757 the ONE accent, EB Garamond. A real tool keeps its own look inside its window; the stage around it stays cream.
- **The first beat of your act carries the act title** (Title Case serif, size 40, as the act's first picture's label), so the viewer always knows where they are. The act titles are in REEL/narration.py `ACTS`.
- **Self-contained.** Never write or show "this chapter", "the book", a module number, or the course name. The assignment's tag `a3` and Day numbers: do not show dates.
- Beat ids are UPPER-CASE (`B09A`); a Manim class name starts with its beat id: `class B09A_Name(Scene):`.

## 0. Read first (in this order, fully)
1. `TK/skills/make/lecture/SKILL.md` (BEST-BEAT LAW, SHOW-THE-THING LAW, PRIMARILY VISUAL, MOTION CARRIES THE CLAIM, ONE LOOK, ONE CAST PER ACT).
2. `TK/skills/make/show-tell/SKILL.md` DRAWING LAWS + the GATE B/T/V traps; `TK/skills/make/nopunt/SKILL.md`.
3. `REEL/narration.py` (every line, in order, so you know what comes before and after your beats), `REEL/beat_sheet.json` (`actual_duration_s` = the clock), `REEL/ACTS.md`, `REEL/LANE-PLAN.md`, `REEL/EVIDENCE-INDEX.md`.
4. `REEL/kit.py` (palette, `T`, `M`, `Iso`, `until`, `done`, `guard`, `dim_arrow`), `REEL/preflight.sh`, and the sibling's `scenes_act1.py` + `lanes/act1.json`.
5. If your beats show a terminal or code: `TK/skills/make/cc-explainer/SKILL.md` (CC kit: CCPlainShell, ClaudeCodeBeat) and `TK/docs/EXECUTABLE-EVIDENCE.md`.

## 1. What you deliver (and only this)
- `REEL/scenes_act<N>.py` — your Manim beat classes + act-prefixed helpers (`a<N>_...`). NO imports of kit (it is pasted by `assemble_scenes.py`).
- `REEL/lanes/act<N>.json` — one entry per beat (schema in section 4). Remotion beats are fully specified there (pattern + props); `"durationSeconds": "__AUDIO__"` is replaced with the measured audio by make_sheet.
- `REEL/factcheck/act<N>.md` — table ROWS ONLY, `| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |`, verdicts PASS / CORRECTED / EXEMPT. One row per checkable claim in your beats' narration AND per number/text you put on screen; verify each against the assignment, REEL/evidence/ (real runs), or a cited primary (the Blender manual https://docs.blender.org/manual/en/5.1/, Godot docs https://docs.godotengine.org/en/stable/, the MCP README copies in REEL/evidence/mcp/).
- New real evidence you generate goes in `REEL/evidence/act<N>/` (scripts + output); images you display go in `REEL/pantry/` (prefix `a<N>_`). Remotion captures that need `staticFile` go in `TK/runtime/remotion/public/lecture-a3assets/` (create it; touch nothing else in TK).
- Final report (your last message): per beat → lane picked, runner-up, one-line why; anything you could not finish or verify; any narration problem (do not edit narration: report it); commands to re-run your evidence.

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
- A tool or website you want to capture in a browser: only public pages, no sign-in, 1600×900 at device scale 2.4 (3840-wide PNG) → `TK/runtime/remotion/public/lecture-a3assets/…` → `BrowserCapture` with the real URL, a dated caption, camera moves that push in to what the sentence names (see `TK/skills/make/medhavy-walkthrough/` for the capture gotchas). Check what is installed (Playwright / Chrome headless) before planning on it; fall back honestly if it is not worth it.

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
`REEL/preflight.sh <N> B45_ClassA B46_ClassB …` → assembles kit + your `scenes_act<N>.py` into a private scratch, runs the Gate A static check (from a folder holding only scenes.py), the layout audit (fix every WARN), and a low-res LAST-FRAME still per class at `/private/tmp/claude-501/lecture-a3assets-act<N>/stills/<Class>.png`. LOOK at every still (and, for motion beats, render a mid-frame too: `manim -ql --save_last_frame` shows only the end; `manim -ql -s` + a sleep of `self.wait` early in a scratch copy, or `manim -ql scenes.py Class` then grab frames with ffmpeg from the mp4 at 25/50/95%). A gate-clean scene that reads as a slide fails the still-frame test: the picture must MOVE to carry the claim.

## 6. Do not
- edit `narration.py`, `make_sheet.py`, `kit.py` (report kit needs), other acts' files, `beat_sheet.json`, `mp3/`, or anything in TK;
- run 4K renders, `art run/final/post`, anything paid, anything that publishes;
- invent facts, numbers, interface output, or quotes;
- say "this chapter", "the book", "module", or name the course in anything shown on screen or spoken (the course is named once, in BIDEA, by the film's opening).
