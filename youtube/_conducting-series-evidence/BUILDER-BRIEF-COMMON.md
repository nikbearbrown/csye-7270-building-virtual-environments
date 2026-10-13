# BUILDER BRIEF (common to all three films) — "CSYE 7270: Start Here"

You are one builder authoring ONE act of ONE whole-run lecture film (the `lecture` skill, channel claude-liam: Liam in for Bear, Kokoro am_onyx, free).
The three films: (1) **Conducting AI for Games**, (2) **Why Godot**, (3) **What Is Walker, and Why**. Narration is written and VOICED (never edit it).
Your job is the PICTURE for your act's beats. Each film is ~6.5 minutes, ~27–34 body beats, ~5–6 acts. The series is for the course CSYE 7270
(named only in BOPEN/BIDEA, which you do not build); in every picture YOU build, never write or show "this chapter", "the book", "the course", an
assignment or a module: the viewer has seen nothing else.

Paths. REEL = your film's folder under
`/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/`:
`claude-liam-lecture-csye-7270-conducting-ai-for-games/` · `claude-liam-lecture-csye-7270-why-godot/` · `claude-liam-lecture-csye-7270-what-is-walker/`.
EVID = `.../youtube/_conducting-series-evidence/` (all the real evidence; index below). TK = `/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/`.
Your film's `LANE-PLAN.md` (in REEL) lists your beats with the evidence for each and lane suggestions. A COMPLETE worked example of a finished film made with the
same kit (read, do not edit): `/Users/bear/Documents/CoWork/bear-textbooks/books/claude-mascot-3d/youtube/claude-liam-lecture-claude-mascot-blender-mcp/` — its
`scenes_act*.py`, `lanes/act*.json`, `factcheck/act*.md`, `BUILD-LOG.md` ("Mistakes worth not repeating"), and the same kit.

## What is different about these films (read twice)
- **Honesty first.** These are not sales pitches. Each film says where a premise is only partly true, shows failures with their real text, and never makes
  anything look more finished or more certain than the evidence. Film-specific honesty rules are in your LANE-PLAN.md.
- **Everything displayed is real or labelled.** Real captures of real runs (the Godot games, the real `publish.sh` output, the real Walker records, real web
  pages) are shown AS THEMSELVES; a drawing may show an idea; illustrative values are labelled "example". Never invent output, UI, numbers or quotes.
  Recorded runs are labelled "recorded run" (the Godot demo was a Claude Code subagent, not `claude -p`; its tool limits were stated in the prompt, not enforced).
- **Real game captures are the picture wherever the narration is about a game** (Bear: "use the actual projects they are going to build — Walker Jump Man has
  now become Claude Walker"). They are Godot's real output of the walker-claude project (Clawd as the player), Walker Pong, and Godot's own MIT demos.
  Captured in Godot 4.7.2 by script, silent MP4s/PNGs, 1920x1080. Show them as video (Remotion `OffthreadVideo`/Manim ImageMobject frames) or stills with
  camera moves; do not fake gameplay. Label scripted input: "scripted input, recorded 2026-10-09".
- **Bear's wording rule:** wherever you write on-screen text meaning a 3D model, write "3D model"; an AI model is "AI model"; never a bare "model" (the proper
  name "Model Context Protocol" is fine).
- **One look.** Claude palette: stage #F2F0E9 / cream #FAF9F5, ink #3D3929, terracotta #D97757 the ONE accent, EB Garamond. A real tool keeps its own look inside
  its window; the stage around it stays cream. The Clawd mascot's own colour #dd775b is the object's own, not an accent (it is a flat mascot: see GATE T trap).
- **The first beat of your act carries the act title** (Title Case serif, size 40, as the act's first picture's label). Titles are in REEL/narration.py `ACTS`.
- Beat ids are UPPER-CASE (`B09`); a Manim class name starts with its beat id: `class B09_Name(Scene):`.
- Where the narration says something the evidence does not support exactly, REPORT it (do not edit narration).

## EVID index (real evidence; read the README-style files first)
- `EVID/walker-evidence/ANALYSIS.md` — a REAL `publish.sh` run (what 54 files it installs, the 12-line manifest, C# vs GDScript, Claude vs Codex, committed vs working tree). Raw files: `walker-evidence/publish.log`, `installed-tree.txt`, `installed/claude/CLAUDE.md`, `installed/claude/godot.md`, `installed/codex/AGENTS.md`, `claude-vs-codex.diff`.
- `EVID/walker-evidence/conducting-records.md` — the real conducting records of walker-jumpman / walker-jumpman-clawd (change brief, 3 predictions, the failed 25-check run, rejected capture takes, narrower-than-worded checks, what is pending). Every quote has file:line. The repos themselves: `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-jumpman-clawd/` (C), `/Users/bear/Documents/CoWork/bear-textbooks/books/walker/games/walker-jumpman/` (S, the starter; `walker-jumpman/` at books/ root does NOT exist), `/Users/bear/Documents/CoWork/bear-textbooks/books/walker/` (W, framework), `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/` (the Claude Walker repo).
- `EVID/godot-evidence/DEMO.md` — a real "no bridge" demo: an agent added a Label to Walker Pong's `.tscn` by text edit; independent check, control run; plus Godot's size/CLI facts from this Mac. Files in `part1/` and `part2/` (`pong.tscn.before`, `pong.tscn.after`, `pong.tscn.diff`, `check_label.gd`, `independent-checks.txt`, `04-tool-calls-and-results.txt`).
- `EVID/godot-captures/` — real Godot renders: `walker-claude/` (Jumpman with Clawd: 7 stills + `walker-claude-jumpman-gameplay.mp4` 7.17 s + `walker-claude-clawd-gallery.mp4` 7.0 s + NOTES.md), `walker-pong/`, `walker-2d-dodge-the-creeps/`, `walker-2d-kinematic-character/`, `walker-3d-platformer/` (each with NOTES/raw-log, PNGs, a clip). Read each folder's NOTES.md or raw-log for what is on screen. (The capture agent may still be finishing `INDEX.md`.)
- `EVID/web-captures/*.png` + `receipts.json` — real full-page screenshots (1600x900 at 2.4x) of public pages: Godot home/license/download/contribution-policy/CLI docs/TSCN docs; GitHub: Coding-Solo godot-mcp, CoplayDev unity-mcp, nikbearbrown/walker, nikbearbrown/walker-jumpman-clawd; Unity MCP docs + changelog. NOT capturable (403): unity.com blog, unity.com/features/ai, Epic docs — for those, show a labelled text card quoting the page (<=15 words, attributed) and say it is quoted, not captured.
- `EVID/research/` — `conducting-brief.md`, `engines-brief.md`, `walker-brief.md`: researched, source-cited briefs (verbatim quotes with path:line, URLs and dates). Use them to fact-check every number and quote you show.
- Walker framework source for quoting rules verbatim: W/README.md, W/prompts/runtime.md (12 lines), W/engines/godot.md, W/gdd/persona.md, W/docs/zelda-gdd-workflow.md, W/godot-scripting-conventions-research-prompt.md.

## Lessons from earlier builds (they cost real rework; apply from the start)
- **GATE T at 4K reads dark UI, dark outlines, floor shadows, flat terracotta-ish objects (the Clawd mascot #dd775b) and dark game art as low-contrast "text blobs"** (any pixel within ~48 RGB of ink/mute is "text"). Real captures with dark areas fail unless cropped to avoid dark small shapes next to mid-tones, or landing AFTER the 50% mark. Check at REAL 4K: render your class once at 3840x2160 (24 fps, caching off) into a private scratch folder and run `TK/runtime/scripts/type_check.py`'s functions on its 50% and 85% frames. Take the shared 4K lock first: `until mkdir /private/tmp/claude-501/lecture-csye-4k.lock 2>/dev/null; do sleep 20; done`, and `rmdir` it right after (16 builders share the machine).
- **Ink-coloured rings/outlines around text fail §8.6b (overlap):** ring with grey (DIM), not ink. A ring around a real capture's pixels fails §8.3b.
- **Gate V** (50% and 85% frames): underfill < 55% of the safe area is a MAJOR unless the beat is declared `sparse` with a reason; low ink/background separation (< 0.3) fails: no pale fills. Never crop a capture past the frame edge at the 50%/85% samples.
- **`CCPlainShell` holds ~13 lines of ~66 columns**, spaces lines evenly, cannot highlight one line: for long lines or per-line cues use Manim Menlo text (`M(...)`, size ≥ 32, ≈ 0.25 units/char).
- Manim `done()`/`until()` can undercount on cache hits: verify clip length with a real `-ql --fps 24` render and ffprobe (target 0.05–0.1 s UNDER the audio); clear stale partial files after changing code.
- The `->` glyph in EB Garamond 32 is under the type floor; draw arrows as shapes. A Pango `Text()` can drop single spaces on this Mac: LOOK at the rendered still; double the space at the fused boundary.
- A real game video in a Manim scene: extract frames with ffmpeg into `pantry/` (prefix `a<N>_`) and use `ImageMobject`s stepped in time, or use the Remotion lane with a staticFile video. Real captures are 1920x1080; never upscale beyond the 4K stage with a visible blur — keep them in a framed window (≤ 70% of the stage) with the cream stage around it.

## 0. Read first (in this order, fully)
1. `TK/skills/make/lecture/SKILL.md` (BEST-BEAT LAW, SHOW-THE-THING LAW, PRIMARILY VISUAL, MOTION CARRIES THE CLAIM, ONE LOOK, ONE CAST PER ACT).
2. `TK/skills/make/show-tell/SKILL.md` DRAWING LAWS + the GATE B/T/V traps; `TK/skills/make/nopunt/SKILL.md`.
3. `REEL/narration.py` (every line in order), `REEL/beat_sheet.json` (`actual_duration_s` = the clock), `REEL/ACTS.md`, `REEL/LANE-PLAN.md`.
4. `REEL/kit.py` (palette, `T`, `M`, `Iso`, `until`, `done`, `guard`, `dim_arrow`), `REEL/preflight.sh`, and the mascot film's `scenes_act1.py` + `lanes/act1.json`.
5. If your beats show a terminal or code: `TK/skills/make/cc-explainer/SKILL.md` (CCPlainShell, ClaudeCodeBeat) and `TK/docs/EXECUTABLE-EVIDENCE.md`.

## 1. What you deliver (and only this)
- `REEL/scenes_act<N>.py` — your Manim beat classes + act-prefixed helpers (`a<N>_...`). NO imports of kit (it is pasted by `assemble_scenes.py`).
- `REEL/lanes/act<N>.json` — one entry per beat (schema below). Remotion beats are fully specified there (pattern + props); `"durationSeconds": "__AUDIO__"` is replaced with the measured audio by make_sheet.
- `REEL/factcheck/act<N>.md` — table ROWS ONLY, `| # | Beat | Claim (as spoken / shown) | Verdict | Source / derivation | Fix |`, verdicts PASS / CORRECTED / EXEMPT. One row per checkable claim in your beats' narration AND per number/text you put on screen, verified against EVID/research briefs, EVID real evidence, or a cited primary.
- Images you display go in `REEL/pantry/` (prefix `a<N>_`); frames extracted from captures too. New evidence you generate goes in `REEL/evidence/act<N>/`. Remotion beats that need `staticFile` use `TK/runtime/remotion/public/lecture-csye-<short>/` (create it; touch nothing else in TK), `<short>` = `games` / `godot` / `walker`.
- Final report (your last message): per beat → lane picked, runner-up, one-line why; anything you could not finish or verify; any narration problem (do not edit narration: report it); commands to re-run your evidence.

## 2. Hard laws for Manim scenes (the costly traps — already learned)
- Scene classes: literally `class B45_Name(Scene):`; the name starts with the beat id; never subclass a helper (run.sh scene discovery is textual and would slate it).
- End every scene with `done(self)`. Pace with `until(self, "exact phrase from the narration", lead=…)`. `[pace] ... OVER` in preflight output means the clip outruns its audio: shorten. Leave ≥0.1 s slack.
- MIDPOINT RULE: GATE T and Gate V sample each clip at 50%. `self.play` is guarded automatically (kit's ST), but `self.wait` is not: the 45–55% frame must be a still that already contains the label(s) that matter — nothing half-faded, mid-sweep, mid-draw, or a lone empty frame.
- Gate A (static stub): every scene must add ≥1 NEW non-text, non-Rectangle shape (Line/Dot/Arrow/Circle/Polygon/Create/GrowFromCenter…) AFTER its first frame, and the shape set must change; moves/fills/Transform of existing shapes do not count. Never do arithmetic on `c2p()/n2p()` results; never position with `Text.get_left()/get_right()` or `mob.get_right()`: write explicit coordinates; wrap group slices as `VGroup(*…)`; wrap `get_center()` in `np.array(...)` before subtracting.
- Forbidden: `rate_functions.ease_in_quad`, `ease_out_cubic` (use kit `ease_in`); `.animate(path_arc=…)` (use `MoveAlongPath(obj, ArcBetweenPoints(a,b))`); `MoveAlongPath` and `.animate` on one object in one `play`; `FadeOut` of a NEW copy of a label (keep references).
- Type: EB Garamond via `T(...)`, size ≥ 32 (titles/act titles 40, hero numbers bigger), Menlo via `M(...)` ≥ 32. Terracotta (`TERRA`) is NEVER text and never a thin/short stroke or underline: use a terracotta DOT or a small spark. Numerals and step markers are ink. No fill behind text (Gate B fails highlighter rectangles): outline-only cells with ≥0.25 padding. No line, outline, or arrow touching or crossing text; ≥0.3 unit gap between a leader line and its label. Labels sit BESIDE objects.
- Frame: stay inside ±6.2 × ±3.3.
- Dark ink-coloured shapes packed together fuse into one "text blob" under GATE T: draw bars/blocks in the greys (`BAR1/BAR2/BAR3`, `DIM`, `GHOST`); a large near-black field fails (use DIM).
- `Transform` of different polygons crumples mid-flight; morph like-for-like or fade/replace. `Indicate` the whole group.
- Manim caches partial movie files by animation hash: after replacing an image file behind the same path, change the name.
- Do not shrink the laws to fit a layout: split the beat's picture, or tighten the text.

## 3. Lane entry schema (`lanes/act<N>.json`, keys = beat ids)
```json
"B13": {"lane": "manim", "class": "B13_Name", "visual_intent": "what is on screen, concretely",
        "motion_claim": "the motion the voice can point at", "show": [{"at": 0.3, "event": "…"}],
        "runner_up": "the second lane you auditioned", "why": "why this one wins", "sparse": true}
"B15": {"lane": "remotion", "pattern": "CCPlainShell", "props": {"title": "…", "lines": [...], "durationSeconds": "__AUDIO__"},
        "visual_intent": "…", "motion_claim": "…", "show": [...], "runner_up": "…", "why": "…"}
```
`sparse: true` (default) waives only Gate V underfill/clustered; set `false` for beats that fill the frame on their own. A beat with no `runner_up` was not auditioned.

## 4. Preflight (run it constantly)
`REEL/preflight.sh <N> B45_ClassA B46_ClassB …` → assembles kit + your `scenes_act<N>.py` into a private scratch, runs Gate A, the layout audit (fix every WARN), and a low-res LAST-FRAME still per class at `/private/tmp/claude-501/lecture-csye-<short>-act<N>/stills/<Class>.png`. LOOK at every still (and a mid-frame for motion beats). A gate-clean scene that reads as a slide fails the still-frame test: the picture must MOVE to carry the claim. For Remotion beats: `REEL/still_remotion.py <BEAT_ID>` renders 25/50/95% stills from the sheet (run `make_sheet.py` is the lead's job; test props with `cd TK/runtime/remotion && npx remotion still src/index.ts <Pattern> <png> --frame=<n> --props='<json>'`; Remotion fps is 30; at 4K body text ≥ 48 design px, tracked headings ≥ 54, chips ≥ 32; any Remotion `at` cue stays out of the 45–55% window).

## 5. Do not
- edit `narration.py`, `make_sheet.py`, `kit.py` (report kit needs), other acts' files, `beat_sheet.json`, `mp3/`, `media/`, or anything in TK except your own `public/lecture-csye-<short>/` folder;
- run `art run/final/post`, `remotion_scenes.py`, `make_sheet.py`, anything paid, anything that publishes; run real 4K renders only for the GATE T/V checks, under the lock;
- invent facts, numbers, interface output, or quotes; run `claude -p` (its login is expired) or any model call;
- say "this chapter", "the book", "the course", "module", or an assignment in anything shown on screen.
