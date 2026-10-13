# BUILDER BRIEF (common to every Godot shader film): the layout stage

**What this is.** The instructions for whoever lays out ONE film of the Godot shader lecture series: the script, the beat sheet, the picture for every beat, the fact-check and the handoff for the build session.
**Why.** Bear's two-stage rule (2026-10-11, restated 2026-10-13): a higher-effort session lays the film out completely; a medium-effort Claude Code session then builds it (scenes, voice, render). This file makes twenty layouts consistent.
**Found.** A pilot film is already laid out: `claude-liam-lecture-godot-shaders/`. It is the model for file shapes, tone and depth. The checker `lint_series.py` enforces the mechanical rules, so a clean lint is part of "done".

You lay out; you do **not** voice, render, record, publish, or write Manim or Remotion scene code. The build session does those from your layout.

## 0. Paths

All under `/Users/bear/Documents/CoWork/bear-textbooks/books/`.

- `SER` = `csye-7270-building-virtual-environments/youtube/_godot-shaders-series/` (this folder): `GLOSSARY.md`, `COMPONENT-SPECS.md`, `series_config.py`, `make_sheet_shared.py`, `lint_series.py`, `lab/`, `briefs/<slug>.md`.
- `FILM` = `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-<slug>/` (yours; create it).
- `TK` = `brutalist.art/` (the toolkit: read only; never edit it).
- The pilot (the model, read first, do not edit): `csye-7270-building-virtual-environments/youtube/claude-liam-lecture-godot-shaders/`.
- Governing skill: `TK/skills/make/lecture/SKILL.md`. Read it fully. Also `TK/skills/make/nopunt/SKILL.md` (SHOW / HOLD / CARD) and the traps in section 6 below.

## 1. Series facts (do not relitigate)

- **Channel `claude-liam`**: Liam, in for Bear, Kokoro `am_onyx`, free. Outro `ClaudeTitleOutro`, handle `@NikBearBrown`, spoken "<Title>. At Nik Bear Brown." Teardown register (Feynman × MKBHD).
- **Standalone films.** The viewer has watched no other film and read no book. Never say "the book", "the course", "this chapter", "last time", "next time"; never name a course or school; **never number a film or use "part", "episode", "series"** (Bear, 2026-10-11, twice). If another film's idea is needed, teach it in one or two sentences where it is needed (or put it in the terms card).
- **Length (Bear, 2026-10-13): no more than 15 minutes, preferably about 10.** Target 40 to 46 body beats, about 1,400 to 1,700 words in the body, 9 to 11.5 minutes total. `lint_series.py` estimates minutes as (every spoken word, bookend beats included, × 0.34 s + 4 s) ÷ 60. That errs long on purpose: the measured bookend time is about 78 s, which is less than the same words at body pace. The real length is known only after the voice is generated, so treat the lint figure as the ceiling. Every film names a **cut line** in `ACTS.md`: what moves out if it runs long.
- **Engine.** Godot **4.7.2** is installed; the docs are **4.7** (`docs.godotengine.org/en/stable`). The renderer is stated whenever a film shows a pixel value (see GLOSSARY and the color film: Forward+ and Compatibility give different pixels for the same shader).
- **Playlist** is not named yet: use `series_config.bopen(TITLE, SUMMARY)` and never type a playlist name.
- **Palette**: stage `#F2F0E9`, cream `#FAF9F5`, ink `#3D3929`, **one** accent terracotta `#D97757` (never text, never a thin stroke), EB Garamond; a real tool keeps its own look inside its window.

## 2. What you deliver (and nothing else)

```
FILM/
  narration.py            every spoken line and all bookend content (schema in section 3)
  lanes/act1.json …       one lane entry per body beat (schema in section 4)
  make_sheet.py           the 4-line shim (copy the pilot's) — then RUN it: it writes beat_sheet.json and SCRIPT.md
  ACTS.md                 coverage map of your brief: every item assigned to an act or to LEFT OUT with a reason; cast per act; cut line
  SHOTLIST.md             one table row per body beat (section 5)
  FACTCHECK.md            Gate F rows (section 7)
  CHECKS-REPORT.md        SHOW / HOLD / CARD counts, lane histogram, teaching-arc checklist (pilot shows the shape)
  SOURCES.md              what the film is built from, with URLs and dates; what was NOT stored (see section 7)
  PROMPTS.md              "No generation prompts: free build." (one line is fine)
  CAPTURE-PLAN.md         every Godot capture the build session must record (section 8)
  BUILD-PROMPT.md         the handoff (section 9)
  lab-shaders/NN-name.gdshader   every shader shown on screen, each passing lab/check_shader.sh
  evidence/planning-checks/      the logs of every run you did (command line, output, date)
```

Every human-facing `.md` opens with three bold lines before any header-level detail: `**What this is.**` `**Why.**` `**Found.**` (Bear's executive-summary-first rule). Report every file by **absolute path**.

## 3. `narration.py` schema (copy the pilot's file and replace its content)

```python
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_godot-shaders-series"))
import series_config as S
SLUG = "claude-liam-lecture-<slug>"            # must equal the folder name
TITLE = "…"                                    # exact film title; spoken in BOPEN and BOUT
TITLE_LINES = ["…", "…"]                       # <= 3 lines, each <= 28 characters
OPENING_DESCRIPTION = "…"                      # <= 52 characters, what the viewer learns, no digits
SUMMARY = "…"                                  # one or two sentences, spoken after the title in BOPEN (what it covers and why it is useful)
BOPEN = S.bopen(TITLE, SUMMARY)
GREETING = "Hallo"
TOPIC = "GODOT SHADERS · …"
TAGS = [...]
ACTS = [("I", "Title Case Title"), ...]        # 3 to 5 acts; numerals I..V
BODY = [("B01", 0, "narration…"), ("B02", 0, "…"), ...]   # (id, act index, text); ids run B01.. with no gaps
BIDEA = "Hallo. This is Liam, in for Bear. …"  # greeting + the topic's framing; does NOT repeat the title/summary
BIDEA_TEXT = ("A shader decides the color of\nthe whole screen.", "the whole screen", "one pixel")   # (text, trigger, replacement)
BDEFS = "Five terms. …"                        # spoken; 3 to 6 prerequisite terms only
BDEFS_TERMS = [("GPU", "the graphics chip: many small workers at once"), ...]   # term <= 17 chars; meaning <= ~70
BVDT_HEADING = "…"; BVDT_LINES = [4 or 6 bare sentences, one per act]
BVDT_NARRATION = "Let's recap with Claude. " + the lines spoken
BHTF_PROMPT = "…a prompt the viewer can paste that makes them USE the main idea…"
BHTF_CHECKS = ["Check: …", "Check: …"]         # exactly two, the viewer's own checks on the result
BHTF_NARRATION = "Your turn. Paste this into Claude: " + BHTF_PROMPT + " Then check two things yourself. …"
BHTF_SEGMENT = "…"                             # short card label
CUT_LINE = "…"                                 # what moves out if the film runs long
SOURCE_DOC = "…"
```

Narration rules (the "script" Bear will read):

- **Teardown register**: plain, concrete, second person allowed, one idea per beat, **20 to 40 words per beat (never over 48)**, sentences short enough to say in one breath (under 25 words). A beat that needs more is two beats. No "just/simply/easy/obviously", no hype, no filler.
- **Concrete before abstract; show the effect before the code.** Predict-then-reveal where it fits. Every earned term is defined *in the beat that first speaks it* using the GLOSSARY wording; a prerequisite goes in the terms card.
- **Numbers as words, acronyms with spaced letters** (see the GLOSSARY spoken-forms table), identifiers in their spoken forms. The screen keeps the real figures.
- **BIDEA** corrects ONE phrase of the misconception a newcomer arrives with. The trigger must appear verbatim in the text; neither trigger nor replacement ends in punctuation (the correction would never fire).
- **BDEFS** is prerequisites only. A concept the film exists to teach arrives in its act.
- **BVDT** recaps (asserts nothing new): one bare sentence per act, four or six lines.
- **BHTF** is a prompt to paste into Claude (Code or chat) that makes the viewer use the film's idea on their own shader, with two checks that put the human in the loop (a shader is where "it compiles" and "it looks right" are furthest apart). Read in full.
- Honesty: say what a demonstration does **not** show. Label scripted input. Quote only measured numbers (from your runs) and say what machine and renderer.

## 4. Lane entries (`lanes/act<N>.json`, keys are beat ids)

```json
"B07": {"lane": "manim", "class": "B07_FourCorners", "visual_intent": "what is on screen, concretely (40+ chars)",
        "motion_claim": "the motion the voice can point at", "show": [{"at": 0.2, "event": "…"}],
        "runner_up": "the second lane you auditioned", "why": "why this one wins", "sparse": true}
"B09": {"lane": "capture", "pattern": "ShaderLab", "props": {"layout": "side", "code": "…", "codeFile": "lab-shaders/02-dial.gdshader",
        "cues": [{"at": 0.2, "lines": [3]}], "video": "godot-shaders/dial.mp4", "videoLabel": "Godot 4.7.2 · scripted run", "durationSeconds": "__AUDIO__"},
        "capture_spec": "scene, shader file, uniforms and their values over time, seconds, renderer, inputs (details in CAPTURE-PLAN.md)",
        "visual_intent": "…", "motion_claim": "…", "show": [...], "runner_up": "…", "why": "…", "sparse": false}
```

- Lanes: `manim`, `remotion` (any registered pattern), `capture` (a Godot render shown in `ShaderLab`), `card`, `terminal`, `editor` (a real editor capture or a labelled `GodotDevWorkbench`). Patterns must exist (`TK/runtime/remotion/src/scenes.json`; check with `./brutalist.art/art scenes --check <Name>` from `books/`) or be a `### Name (NEW)` in `COMPONENT-SPECS.md`.
- A Manim class name starts with its beat id (`B07_…`); the run script finds scenes by text.
- Registered patterns you will use most: `LectureCodeTrace` (props `title, code, note, durationSeconds, cues[] fractions`: paced line focus; **holds at most 10 lines**, one cue fraction per line), `LectureEvidenceTable` (`title, headers[2–4], rows[1–4][], note, cues`), `CCPlainShell` (`title, lines, startCue, lineGap, lineCues`, about 13 lines of 66 columns), `ClaudeCodeBeat` (`title, code, language, largeText`), `GodotDevWorkbench` (`mode code|tree|asset|trace, title, project, source, code, cues, image…`: a *reconstruction*, labelled), `BrowserCapture` (a still of a real page: Godot docs pages are good evidence), `DesignPipelineClaim` (flows: set `diagramStyle: "show-tell-isometric"`, `objectKinds`), `LibraryIconRow`, `FormACard` (act title or one breath only; a card whose narration names a visual is a PUNT).
- **BEST-BEAT LAW**: for every body beat ask what single picture the sentence is about, audition at least two lanes, and pick the one whose *motion is the claim*. Router for this series: a function or quantity reshaping a 0→1 ramp, a coordinate system, a triangle of corners, a pixel grid, a flow of work → **Manim** (use `shader_kit.py` objects); shader code with its live result → **ShaderLab**; code alone → `LectureCodeTrace`; a table of kinds → `LectureEvidenceTable`; Godot's docs → `BrowserCapture`; the editor → real capture first, `GodotDevWorkbench` last. No lane has a quota and none is the default.
- **MOTION CARRIES THE CLAIM** (still-frame test): if a beat reads the same as a still, it fails. **PRIMARILY VISUAL**: labels of one to three words; never narration set as type; text-only cards only for an act title or one breath.
- **ONE CAST PER ACT**: the same object is the same picture throughout an act. Cast for the series: the **ramp strip** (0→1), the **test rectangle** (four terracotta corner dots), the **pixel grid**, the **test sprite** (a teal blob with two cream eyes and transparent padding, same as `lab/runner.gd`'s "sprite"; teal, not terracotta, so GATE T does not read it as text), on the Lab's warm light-grey stage (`#D9D5CA`). Pick shader colors that keep a mid-tone floor: avoid large near-black fields and flat terracotta.
- The first beat of each act carries the act title (Title Case, serif) as its label.

## 5. SHOTLIST.md

One row per body beat, exactly this header and the beat id first in the row (the checker reads it):

`| beat | about | lane picked | runner-up | why this one wins | evidence / capture |`

List every component the build must create (`ShaderLab`, `shader_kit` objects) and every capture and where it comes from. A beat with no runner-up was not auditioned.

## 6. Traps already paid for (the build session will hit them; design around them)

- **GATE T (type) at 4K** reads dark UI, dark outlines, flat terracotta objects and dark game art as low-contrast "text blobs" (any pixel within about 48 RGB of ink or mute counts as text). Real captures with dark areas fail unless they land after the 50 % mark or are cropped to avoid small dark shapes next to mid-tones. Ink rings around text fail the overlap rule: ring with grey. Terracotta is never text.
- **Gate V** samples the 50 % and 85 % frames: underfill below about 55 % of the safe area is a major unless the beat is declared `sparse` with a reason; pale fills fail the ink/background separation test. Never crop a capture past the frame edge at those samples.
- **Gate A** (Manim): every scene must add at least one new non-text, non-Rectangle shape after its first frame. **Midpoint rule**: the 45–55 % frame must be a settled still containing the labels that matter (nothing half-faded or mid-sweep). Forbidden: `ease_in_quad`/`ease_out_cubic` (use the kit's `ease_in`), `.animate(path_arc=…)`, `MoveAlongPath` plus `.animate` on one object in one `play`. Stay inside ±6.2 × ±3.3. Type ≥ 32 (act titles 40). No fill behind text (outline cells with padding). Dark ink shapes packed together fuse into a "text blob": draw bars and ramps as separate narrow tiles with gaps (the Math Toolkit layout measured it: a continuous strip of mid-dark grays, 27 to 113 of 255, is one text-like run to GATE T; pure black or white is not).
- A Pango `Text()` can drop single spaces on this Mac: double the space at the fused boundary and LOOK at the still. The `->` glyph is under the type floor: draw arrows as shapes.
- Kokoro: spell numbers and acronyms as in the GLOSSARY; "play-test" not "playtest"; `Godot`, `AI`, `pi` are covered by the dictionary.
- Captures: a Godot render is **offline at a fixed tick rate** and says nothing about real-time frame rate; label scripted input; label the renderer; a 4K SubViewport capture of a 1280×720 canvas is the proven route **for shaders that work in fractions (`UV`, ratios)**; shaders that read window pixels or mip levels are captured natively at the size shown (GLOSSARY "Series conventions"); do not upscale a small capture with visible blur.
- Never edit `beat_sheet.json` by hand and never re-run `make_sheet.py` after `art final` (it clears build stamps).
- **BHTF narration reads the prompt and then the two checks aloud; `props.command` holds only the prompt and `output` holds the checks.** That is settled: the shipped Why Godot film (2026-10-09) does exactly this and passed `bookend_check`. Do not "fix" it so that `narration_text == props.command`.
- **Lab batches are slow because the lock is shared.** About 95 renders took 15 to 20 minutes while other sessions held the lock. Batch the renders, run `check_shader.sh` once per shader, and never write a render loop that retakes the lock per frame.
- **The Lab renders a failing shader as white**, so a "white" probe (for example for `vec4(1.0)`) is ambiguous: probe a non-white color. `check_shader.sh` prints only the `SHADER ERROR` line; for the engine's full log (a missing semicolon is reported on the NEXT line) run a throwaway copy of the Lab, never the shared one. It flags nothing for a shader with no `shader_type`, or `render_mode` before it, at run time: the shader is simply not applied.
- **A covered, hidden or minimized Godot window stops drawing, and `TIME` stops with it** (this explains the pilot's inconclusive first TIME run). Any windowed, real-time (not Movie Maker) run that reads `TIME` must keep its window on top: `DisplayServer.window_set_flag(DisplayServer.WINDOW_FLAG_ALWAYS_ON_TOP, true)`.
- **`check_shader.sh` silently ignores options it does not parse**, and zsh does not split an unquoted `$S`: a batch lost its `--size` and `--kind` this way. Check that the RESULT line echoes what you asked for. The Lab has no camera or parent mode: films that need one use a scene script (the Local, World and Screen Space film's `scenes_lib.gd`, `probe_lib.gd`, `capture_scenes.gd` are reusable).
- **Godot prints a shader's source window with its comments stripped**, so a compile-error log cannot carry a teaching comment; a line printed by the launching script can. `CCPlainShell`'s `# ` comment lines are ghost ink (#6B6760 on #252422, about 2.8:1): fine for flavor, too weak for a definition.
- **`BrowserCapture`: provenance is the real address in the browser bar; its caption may carry a one-line definition** (80 characters at most). Labels on `ShaderLab` are 60 characters at most, so a longer GLOSSARY wording uses its short form (see the row) or goes in a Manim label.
- **The Lab `--wait` picture of a `TIME` shader freezes silently if the Godot window is covered, and the Lab binds only a plain image, not a `NoiseTexture2D`**: use `RenderingServer.force_draw(false, step)` in a scene script for those.
- **Scratch check scripts that name shader files silently run with NO shader if a file is renamed** ("shader not found" is only a log line): three logs in the Outlines layout measured the wrong thing until every log was scanned for `ERROR`. End any batch with that scan.
- **A Godot window can stop drawing mid-run even with always-on-top** (two of seven stress-test runs in the Outlines layout: every frame read the idle 6.9 ms). Reject such runs (an analysis script that checks frame times), and quote absolute timings as whole milliseconds and "about" (they drift about 2 percent run to run).
- **Never `pkill -f` a script name.** It killed other films' batches (met once). Kill by PID, and keep batch scripts resumable (`RESUME=1`, one result row per run).
- **zsh: never name a shell variable `path`.** It is tied to `PATH`; assigning it breaks every command that follows (met during the Patterns film's batch script). Use `shader_path`, `png_path`, and the like.
- **Define the small math words where they are first used.** The GLOSSARY now carries `floor`, `fract`, `mod`, `mix`, `step`, `length` and `TEXTURE` with the docs' own wording; put that wording in a cue `label` on the code line or in a Manim label, not only in narration.

## 7. Truth: FACTCHECK.md (Gate F) and evidence

`| # | Beat | Claim (as spoken or shown) | Verdict | Source / derivation | Fix |` with verdict **PASS**, **CORRECTED**, **EXEMPT** (a definition or an opinion, stated as one) or **OPEN** (not verifiable now: say why; the checker warns on OPEN). At least 12 rows; one row per checkable claim in the narration and per number or text put on screen.

- **Godot behavior**: verify against the 4.7 docs (fetch the page; quote closely; give the URL) **or** by running it. Run it with the Lab:
  `lab/check_shader.sh <shader> --kind rect|sprite|quad3d [--set name=value] [--tex sampler=gradient|checker|noise|sprite] [--probe x,y] [--png path] [--renderer forward_plus|gl_compatibility]` → one `RESULT {json}` line (pixels as 0..1 floats), non-zero exit and the compiler's message on a shader error. Write the command and the result into `evidence/planning-checks/` (a `RESULTS.md` is fine).
  For anything the Lab cannot do (GDScript-side timing, node behavior, input) write a small `--script` file and run it in a scratch project, as `claude-liam-lecture-godot-shaders/evidence/planning-checks/verify.gd` does. Scratch work goes under the session scratchpad, finished scripts and logs into `evidence/planning-checks/`.
- **The source material is third-party.** The brief tells you what its author says. Treat it as a claim to check, not a fact. Where it is loose or wrong, the row is CORRECTED and the film says the corrected thing. Do **not** store the source's text or copy its sentences; teach the idea in new words with new demos. Record in `SOURCES.md` that the source course/video is a third-party work whose creator Bear has not yet named, that nothing was copied, and which of its ideas the film follows.
- **Strip the datable** (versions other than the engine's, prices, counts). Attribute thin numbers aloud and on screen. A measured number says what machine, which renderer.
- **Never invent** UI, output, numbers, quotes or approvals. Anything shown as a Godot result must be a Lab or editor capture of a file in `lab-shaders/`.

## 8. CAPTURE-PLAN.md

For each capture: id, the beat(s) it serves, the shader file(s), the target (`rect|sprite|quad3d|scene`), uniform values or sweeps over time, scripted input if any, duration, frame rate (30), renderer (state it), what must be visible at the 50 % and 85 % marks, and whether it is a Lab render, a static editor frame, or needs an interactive editor action (editor states are recorded by the series editor driver, see `editor-capture/README.md`; no human recording is needed, so list the state script steps instead). Add the expected result you already verified (probe values). Mark anything you could not verify.

## 9. BUILD-PROMPT.md (the handoff to the medium-effort Claude Code session)

Copy the pilot's `BUILD-PROMPT.md` and edit the film-specific parts. It must be enough for a session with no other context: what is done, absolute paths, the commands in order (all run from `books/`: ensure the shared components exist, record captures, write the Manim scenes from `SHOTLIST.md`, `make_sheet.py`, `generate_audio_kokoro.py`, stills, `art run`, `art final --height 2160 --out`, `bookend_check.py`), the gates that must pass (F, A, B, V, T, bookend, PROOF), the traps, hard stops (**do not publish or stage, no paid generation, do not change the narration or beat sheet**), and the final-report format.

## 10. Order of work

1. Read the pilot completely, then your brief, then `GLOSSARY.md` and the lecture skill.
2. Fetch the docs pages your brief names; write the shaders and run them in the Lab; log everything.
3. Write `narration.py` and the lanes; run `make_sheet.py`; read `SCRIPT.md` aloud in your head (does Liam sound like a person?).
4. Write the paperwork and `CAPTURE-PLAN.md`, `BUILD-PROMPT.md`.
5. Run `python3 SER/lint_series.py <slug>` until it prints no errors; read every warning and fix or justify it in `CHECKS-REPORT.md`.
6. Final report (your last message, concise): the absolute path of `SCRIPT.md`; beats, words, estimated minutes; lane histogram; the cut line; the five most important facts you verified or corrected (with sources); anything OPEN; anything the brief got wrong or that the GLOSSARY should change (do not edit shared files: report); the editor actions your film needs.

## 11. Do not

- edit anything outside `FILM/` (and your Scratchpad): not `SER/`, not the pilot, not other films, not `TK/`, not any game or course repo, not `liam.json`;
- voice, render, record, stage or publish anything; spend anything; run `claude -p` or any model call;
- number a film, name a course, copy third-party text, or claim a run you did not do.
