# Layout report: the 13 remaining Godot shader films (2026-10-14)

**What this is.** The result of the request to lay out the 13 shader films that were thought to have no layout folders yet.
**Why.** So Bear knows what state the folders are in before anything is built from them.
**Found.** **All 13 folders already existed, complete and lint clean, since the 2026-10-13 layout pass (files dated Oct 13 20:11).** The seven films described as "existing" are the seven that were later *built* overnight (godot-shaders, godot-shader-language, shader-math-toolkit, shaders-in-3d, trigonometry-for-shaders, vertex-shaders, light-shaders; see MORNING-REPORT.md); the other 13 are the laid-out-but-unbuilt ones. Re-laying them out would have overwritten finished, fact-checked work, so I did not. Instead I audited and re-verified them. Result: every one of the 13 has the full file set; the lint is 20 of 20 clean; the regenerated SERIES-TABLE.md, LINT-REPORT.md and CLAUDE-CODE-PROMPTS.md came out byte-identical to the existing ones (so the layouts and the tables agree); a fresh run of all 195 lab shaders in Godot 4.7.2 gave 192 clean compiles and exactly 3 compile errors, all three being the deliberately broken teaching shaders. One fix was made: SubViewports' PROMPTS.md was a 35-byte stub and now matches the other films' wording. Nothing was generated, captured, rendered, published, staged or committed, and the seven built films, godot-shading-language and pronunciation/liam.json were not touched.

## Per film (counts from the generated SERIES-TABLE.md; fact-check verdicts counted from each FACTCHECK.md)

| Film | Beats | Words | Est. min | Lanes (manim / capture / remotion / editor) | Lint | OPEN fact-check rows | Fact-check rows (PASS / EXEMPT / CORRECTED) |
|---|---|---|---|---|---|---|---|
| textures-and-color | 47 | 1918 | 10.9 | 7 / 27 / 4 / 3 | clean | 0 | 102 / 13 / 4 |
| uv-space | 48 | 1812 | 10.3 | 17 / 19 / 6 / 0 | clean | 0 | 61 / 5 / 3 |
| patterns-and-pixelation | 49 | 1790 | 10.2 | 18 / 22 / 3 / 0 | clean | 0 | 66 / 3 / 1 |
| drawing-shapes-with-math | 50 | 1900 | 10.8 | 15 / 25 / 3 / 1 | clean | 0 | 68 / 14 / 2 |
| soft-edges-glow-and-noise | 48 | 1791 | 10.2 | 15 / 23 / 2 / 2 | clean | 0 | 78 / 16 / 4 |
| time-and-waves | 46 | 1690 | 9.6 | 18 / 18 / 4 / 0 | clean | 0 | 78 / 4 / 3 |
| lines-and-shine | 41 | 1587 | 9.1 | 14 / 21 / 0 / 0 | clean | 0 | 62 / 6 / 3 |
| outlines | 47 | 1868 | 10.7 | 11 / 27 / 3 / 0 | clean | 0 | 68 / 7 / 6 (rows are F01..; different table style) |
| matrices-and-fake-3d | 47 | 1791 | 10.2 | 22 / 15 / 4 / 0 | clean | 0 | 66 / 7 / 4 |
| local-world-and-screen-space | 46 | 1779 | 10.1 | 24 / 12 / 2 / 1 | clean | 0 | 76 / 6 / 3 |
| reading-the-screen | 44 | 1685 | 9.6 | 11 / 25 / 2 / 0 | clean | 0 | 60 / 10 / 7 |
| reflections | 43 | 1557 | 8.9 | 12 / 19 / 4 / 2 | clean | 0 | 60 / 8 / 3 |
| subviewports | 46 | 1840 | 10.5 | 16 / 22 / 0 / 2 | clean | 0 | 68 / 2 / 4 |

Beat counts, words, minutes and lanes match SERIES-TABLE.md; each film's cut lines are in that file ("Cut lines" section) and in its own ACTS.md.

## What was checked, and how

- **File set.** Each of the 13 folders has SCRIPT.md, narration.py, beat_sheet.json, lanes/ (4 or 5 act files; reading-the-screen and subviewports have four acts), ACTS.md, SHOTLIST.md, FACTCHECK.md, CHECKS-REPORT.md, SOURCES.md, CAPTURE-PLAN.md, PROMPTS.md, BUILD-PROMPT.md, lab-shaders/ and evidence/planning-checks/ (13 to 88 files each, with RESULTS.md or summaries, scripts and numbered run logs, failed and inconclusive runs kept).
- **Lint.** `lint_series.py`: 20 of 20 films, 0 errors, 0 warnings.
- **Generators.** `series_table.py`, `lint_series.py --report` and `make_claude_code_prompts.py` re-run; outputs identical to the previous files.
- **Godot 4.7.2 re-run.** Installed Godot is 4.7.2.stable.official. Every .gdshader in the 13 films' lab-shaders/ folders (195 files) was compiled through `lab/check_shader.sh` (sprite or quad3d stage by shader type, output to scratch, not into the film folders). 192 compile. The 3 errors are the intentional failures: drawing-shapes-with-math/16-uv-inside-function-FAILS.gdshader, local-world-and-screen-space/04-broken-matrix-in-fragment.gdshader, reading-the-screen/04-godot3-screen-texture.gdshader. This is a compile smoke test only; the numeric claims were run and logged when the films were laid out (run logs in each evidence/planning-checks/) and I did not re-run those experiments.
- **Claims corrected.** The CORRECTED counts above are the claims where the brief or its third-party source was loose or wrong and the film says the corrected thing; each is logged with the fix in that film's FACTCHECK.md (for example, in uv-space a texture's own repeat setting does apply to a shader's reads on a TextureRect; in subviewports a fade written as COLOR.a = UV.x leaves a dark haze on transparent pictures; in outlines the brief's subtraction form of the line color, "ifs are slow", and the deprecated way to build the padded image).

## Open items and caveats

- 0 OPEN fact-check rows anywhere in the 13, but this is layout-stage: nothing has been voiced, captured in the editor, rendered or watched. The captures and editor frames described in CAPTURE-PLAN.md do not exist yet for these 13.
- The documentation site put a bot-check page in front of the headless browser during the overnight builds (MORNING-REPORT.md); the 13 films' docs quotes were read 2026-10-13 and any docs-screenshot beats may need the same quote-card fallback at build time.
- The playlist name is still empty in series_config.py (Bear has not named it).
- reflections has only 5 lab shaders and relies mostly on scripted-scene experiments (exp_*.gd) in its evidence folder; its numbers come from those logs, not the Lab.
- Not done, by design of the request: audio, editor-frame capture, render, publish, git add/commit/push.

## Paths

- Films: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/../claude-liam-lecture-<slug>/ for the 13 slugs above.
- Series folder: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/../_godot-shaders-series/ (SERIES-TABLE.md, LINT-REPORT.md, CLAUDE-CODE-PROMPTS.md regenerated, unchanged in content).
- Changed in this pass: /Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/_godot-shaders-series/../claude-liam-lecture-subviewports/PROMPTS.md and this report.
