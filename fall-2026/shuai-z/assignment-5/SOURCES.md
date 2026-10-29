# SOURCES — Assignment 5, walker-rudy's shaders and materials

Credits, tools, versions, and who did what. The dated record is [FRICTIONAL.md](FRICTIONAL.md). This file is updated as the work goes on.

## Starting point

- **My Assignment 2 game**, `game/`:
  - a copy of [`../assignment-2/game/`](../assignment-2/game/) as committed at tag `a3`, copied unchanged (commit `84658acf`);
  - its art, sound and music, with their models and terms, are credited in [../assignment-2/SOURCES.md](../assignment-2/SOURCES.md) and [../assignment-2/ASSET-LOG.md](../assignment-2/ASSET-LOG.md).
- **My Assignment 3 props scene**, `godot/`:
  - a copy of [`../assignment-3/godot/`](../assignment-3/godot/) as committed at `a3`, copied unchanged in the same commit;
  - its props and colours are credited in [../assignment-3/SOURCES.md](../assignment-3/SOURCES.md).
- **The course's test wrapper**, `scripts/run-test.sh`:
  - from the assignment's "Build It" section, changed in four places for this folder's two projects (commit `cca08046`);
  - the changes are listed at the top of the script.

## People

- **Shuai Zhang (me):** asking for each step; reviewing and approving the change brief, the prompts and the plan; writing the three shaders and making the three mutations; checking the materials and the hint scene in the editor; making and annotating the generated shader, and writing LANGUAGE-NOTES.md; playing the game for Use It and checking the hearts' fade-in, and reviewing the checks Claude did for me; choosing the curl threshold; recomputing two predictions by hand; deciding when to commit.
- No other collaborators. No one else has looked at the work or played it.

## Tools

| Tool | Version | Used for |
|---|---|---|
| Claude Code (desktop app), model Claude Opus 5.5 | 2.1.302 | Reading the assignment against my project; step 0 (the copy, the `.gitignore` exception, the wrapper, the imports and the baselines); drafting CHANGE-BRIEF.md, including the colour line, the predicted values and the short answers; running the scoped CLAUDE.md session, then checking and reviewing its draft; the guide and the checks for the shader from code; the probes in `evidence/headless-probe/`; the prompts, commands and checks for the driver's sessions, and the review of its plan; running the test after each shader mutation; downloading and checking Rock 01, its import settings and the normal-map check's calibration; the stone and hint materials, the scene tools and their probes, and the circle's tint; the audit's prompt, command and checks, and its review; checking the generated shader and LANGUAGE-NOTES.md; the windowed capture tools and their runs; at my request, the interface sweep, the two-materials check and the OS-screenshot comparison; drafting this file, FRICTIONAL.md and TEST-REPORT.md |
| Claude Code (command line, `claude -p`), model `claude-opus-5-5` | 2.1.302 for the CLAUDE.md run that could not log in, 2.1.310 for every later session | The scoped sessions: the CLAUDE.md draft (`sessions/session-1.jsonl`), the driver's plan (`sessions/session-2.jsonl`) and its implementation (`sessions/session-2b-refused.jsonl`, and `sessions/session-2b-excerpt.jsonl`, a labelled excerpt of the full transcript in `bd797945`), and the materials audit (`sessions/session-3.jsonl`) |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build | The imports, the headless tests, the probes, the scene tools and the windowed captures |
| GNU coreutils `timeout` (Homebrew) | 9.12 | The time limit in the wrapper and the probe runs |
| Python 3 with Pillow | 3.13.5, Pillow 10.4.0 | Reading the heart textures' texels, the `.glb` headers and an Assignment 2 screenshot; computing the brief's predicted values and contrast ratios, with a short script kept outside the repository; reading the grey strip back, and averaging Rock 01's colour map for the circle's tint, also with scripts kept outside it; for TEST-REPORT.md, the hearts' outline contrast, viewing sheets and difference images of the sweep, the normal and roughness maps' ranges, and converting the OS screenshot from its colour profile, with scripts kept outside it too; making the labelled excerpt of the driver's transcript, with `scripts/excerpt_transcript.py`, which is in the repository and uses only Python's standard library |
| macOS `screencapture` | built into macOS 15.1 | The one OS screenshot of the hint scene's window, compared with the engine's capture |
| curl | 8.12.1 | Downloading Rock 01 and reading Poly Haven's API |
| jq | 1.7.1 | Reading the result event of a `claude -p` transcript |
| Git | 2.51.0 | Version control; `git archive` for the copy, and for the temporary copies in `evidence/headless-probe/import_check.sh` |

`/opt/homebrew/bin/godot` is a two-line shim to the app's binary, so that `godot` is on my PATH. Claude installed it on 2026-10-24; it is outside the repository.

## Textures

- **Rock 01** (`rock_01`) from Poly Haven, by Rob Tuytel, CC0 (https://polyhaven.com/a/rock_01), downloaded on 2026-10-27.
  - Files: the 1k diffuse, `_nor_gl`, `_nor_dx` (calibration only) and roughness PNGs, in `godot/assets/textures/rock_01/`. Each matches the size and MD5 that Poly Haven's API lists.
  - `godot/assets/textures/rock_01/ATTRIBUTION.md` records the URLs, the author and role, the licence, the date checked, and the normal-map convention used, `_nor_gl`.
- **The grey strip**, `godot/assets/hint_experiment/grey_strip_3x1.png`, is written by code: `godot/tools/write_grey_strip.gd`.

## Colour sources

| Colour | Value | Source |
|---|---|---|
| The hearts' tint, `tint_color` | `Color(0.6, 0.88, 1.0)`, `#99E0FF` | `game/content/level_1/waystone.gd` line 19, `GLOW`, the lit waystone's glow. It is the uniform's default in `game/shaders/invulnerable_tint.gdshader` line 4 |
| The waystone's Stone and the circle's DarkStone, as imported | `#8C8A80`, `#4A4440` | Assignment 3's brief, checked by `godot/tests/check_props.gd` |
| `albedo_tint` in `circle_darkstone.tres` | `#A4A7B4` | Computed by Claude so that Rock 01's average colour, times the tint, is Assignment 3's DarkStone `#4A4440`. It replaced the brief's starting value `#8F857D`, which averaged `#40352A`; I chose the change (CHANGE-BRIEF.md, revision 2) |

## Human / AI contributions

| Part | Claude | Me |
|---|---|---|
| Reading the assignment | Read it against my two projects and the course's chapters. Found the existing checks that rule out a new material on Rudy and the props; the check that rules out Use External; the wrapper's three problems; and that the Assignment 4 branch must not be the base | Asked for the step-by-step plan |
| Step 0 | Branched from `a3`; copied both projects; found and fixed the `*.wav` ignore; adapted the wrapper; imported both projects; ran the baselines; installed the `godot` shim | Asked for it; held the commits until the brief was reviewed; asked for the shim |
| CHANGE-BRIEF.md | Drafted all of it: the design (the hearts, the invulnerable window, Rock 01, overrides rather than Use External), the rules, the colour line, the predicted values, the contrast check that moved `tint_strength` from 0.6 to 0.4, and the short answers | Asked for the full draft; reviewed it and found no problems; approved the commit; on 2026-10-28, after the captures, recomputed two of its predictions by hand |
| CLAUDE.md | The scoped `claude -p` session drafted it: 82 lines, committed unedited (`dfeca3fb`). Claude, in our conversation, ran that session twice (the first could not log in), checked the draft, and reviewed it with two probes; the reviewed version has 91 lines (`c095e9de`). Before the driver's session, Claude updated it: the shader now exists, and a headless import compiles only what the main scene uses | Logged the command-line `claude` in; asked for the run and the review; approved both commits and the update |
| The shader from code, `game/shaders/invulnerable_tint.gdshader` | Specified it in the brief: the file, the three uniforms' names, types, hints and defaults, and the colour line. Listed what to prepare and how to check it; wrote `probe_shader.gd` and `import_check.sh`; ran the checks | Wrote it from the brief and committed it on its own (`ae0a3757`) |
| The colour line | Suggested `COLOR.rgb = mix(COLOR.rgb, tint_color.rgb, tint_amount * tint_strength);` in the brief | Typed it into the shader, line 8 |
| The driver and its test: `game/ui/hearts_tint.tres`, `hud.tscn`, `hud.gd`, `game/tests/invulnerable_tint_checks.gd` and `.tscn` | The scoped sessions planned them (`session-2.jsonl`), then wrote and ran them (`session-2b-excerpt.jsonl`). Claude, in our conversation, drafted both prompts, reviewed the plan and proposed five changes, wrote the scoped commands, ran the sessions and checked every result | Reviewed and approved both prompts and each run; accepted the plan with Claude's changes |
| The shader mutations | Ran the new test through the wrapper after each, and kept both logs | Made both mutations and restored the shader |
| Rock 01's textures and their import settings | Downloaded and checked them, wrote ATTRIBUTION.md, wrote the brief's import settings and checked the imported formats | Approved the download |
| The normal-map check | Copied the assignment's check unchanged, and wrote and ran its calibration; on 2026-10-28, added the threshold's two checks and showed that they fail at 0.1 | Approved the commit; chose the threshold, 0.5 |
| The textured shader, `godot/shaders/weathered_stone.gdshader` | Specified it in the brief; listed what to prepare and how to check it; ran the checks | Wrote it from the brief and committed it on its own (`a87a18be`) |
| The stone materials and their overrides | Wrote both materials and `godot/tools/add_stone_overrides.gd`, checked each surface, and computed the circle's tint | Chose the tint `#A4A7B4`; checked the look in the editor, twice |
| The hint experiment | Wrote the strip's writer, both materials, `godot/tools/build_hint_experiment.gd` and the probes | Wrote `godot/shaders/hint_experiment.gdshader` and committed it on its own (`9481663a`); checked the scene in the editor |
| The materials audit: `godot/MATERIALS.md` and `godot/tests/test_materials.gd` | The scoped session wrote them (`session-3.jsonl`), committed unedited (`cd1e71a3`). Claude, in our conversation, adapted the course's prompt, ran the session, checked it, and reviewed the audit: enums, formats and one wrong number | Approved the prompt and the run |
| The fresh-cache run and the `source_color` mutation | Moved the cache aside, reimported, ran the tests, and kept both logs | Made the mutation and restored the shader |
| The generated shader, `godot/shaders/standard_generated.gdshader` | Checked that the annotations change no code and that the uniforms they call unused are unused; ran its probe | Converted a StandardMaterial3D in the editor, annotated the code, and committed it (`fe795908`) |
| LANGUAGE-NOTES.md | Checked every line reference; at my request, made the links relative and corrected line 16 | Wrote it (`5db11399`) |
| The captures of the hearts and the hint experiment | Wrote `game/tests/capture_tint.tscn` and `godot/tests/capture_hint.gd`, and ran them in a window | Approved the runs |
| The playtest | Listed what to try; recorded my words; checked `git status` afterwards | Played the game and said what I saw; on 2026-10-28, watched the hearts' fade-in |
| The interface sweep, the two-materials check and the OS-screenshot comparison | Did all three at my request: wrote `godot/tests/capture_sweep.gd` and `godot/tests/capture_hint_vs_os.gd`, ran them, judged the captures and made the measurements | Asked Claude to do them, and to record that it did; reviewed the results and looked at the captures |
| Checking the work against the assignment, and closing the documentation gaps (2026-10-28) | Checked each part against the Canvas text; updated CLAUDE.md (references the driver moved, the hearts' material, the new tests and capture tools, Unconfirmed); wrote `scripts/excerpt_transcript.py` and `sessions/README.md`, and replaced the 1.6 MB transcript with its excerpt; added the brief's revision 4 | Asked for the check and the changes |
| Documents | Drafted this file, FRICTIONAL.md and TEST-REPORT.md from our conversation and the logs; ran every headless test again for TEST-REPORT.md | Checked them against what I did, and reviewed the changes of 2026-10-28: "审核完了，没问题" ("I've finished the review; no problems") |
