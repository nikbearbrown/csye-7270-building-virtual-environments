# SOURCES — Assignment 6, walker-rudy's particle effects

Credits, tools, versions, and who did what. The dated record is [FRICTIONAL.md](FRICTIONAL.md).

**How this file was made:** Claude Code (Claude Opus 5.5) drafted it on 2026-11-07 at my request, from FRICTIONAL.md, TUNING.md, TEST-REPORT.md, the sessions' transcripts and the commits. I reviewed it the same day, before it was committed ("看过了，没问题", "I've read it; no problems").

## Starting point

- **My Assignment 2 game**, `game/`:
  - a copy of [`../assignment-5/game/`](../assignment-5/game/) as committed at tag `a5`, copied unchanged with `git archive` (commit `e61e8025`). No change of game since Assignment 2;
  - its art, sound and music, with their models and terms, are credited in [../assignment-2/SOURCES.md](../assignment-2/SOURCES.md) and [../assignment-2/ASSET-LOG.md](../assignment-2/ASSET-LOG.md); Assignment 5's tint shader, which this assignment leaves alone, in [../assignment-5/SOURCES.md](../assignment-5/SOURCES.md).
- **The course's test wrapper**, `scripts/run-test.sh`:
  - from the assignment's "Build It" section, changed in four places for this folder (commit `47ce9e2d`);
  - the changes are listed at the top of the script.
- **The course's chapter and example**, read from the course repository (`upstream/main`), not copied into this folder:
  - Chapter 9, `chapters/09-particle-effects.md`: the trail made from an ordinary emitter with `local_coords` off, as its Dodge the Creeps example makes one; the headless price and the 6.9 ms frame sleep;
  - Example 09, `examples/09-particle-effects/tests/particle_cost.gd`, which `game/tests/cost_effects.gd` adapts (its header says so).
- **The F9 key** follows the code in the assignment's Use It section (`game/app/vsync_debug.gd`).
- **The film** was made with the course-provided Brutalist toolkit (`godot-gamedev` with the `walker` modifier); its tools, voice and versions are credited in [youtube/claude-liam-walker-rudy-particles/SOURCES.md](youtube/claude-liam-walker-rudy-particles/SOURCES.md).

## People

- **Shuai Zhang (me):** deciding the scope (the 2D game only); asking for Effect B to be a trail behind Rudy, and choosing both effects from the options Claude put to me; reviewing and approving the change brief, the prompts and the plans; judging every preview at real speed before Claude read a frame, approving every tuning change and giving every verdict, including the one that overruled Claude's reading of Effect B's round r2; finding that Effect B was missing from the game; generating the process shader in the editor and writing its reading; choosing what to measure for Use It and having Codex record it; playing the game myself; watching the film and uploading it; deciding when to commit.
- No other collaborators. No one else has looked at the work or played it.

## Tools

| Tool | Version | Used for |
|---|---|---|
| Claude Code (desktop app), model Claude Opus 5.5 | 2.1.310 | Explaining the assignment; the setup, the wrapper and the baselines; the Compatibility and headless probes; drafting CHANGE-BRIEF.md and its revisions; the prompts and commands for every scoped session, running them and checking their results; the review of CLAUDE.md; the strip captures, the real-speed plays, the strip readings, predictions and comparisons, and the tuning changes; the scene mutations; the F9 key and its check; checking the process shader's line references and Codex's evidence; the film; drafting TUNING.md, TEST-REPORT.md, FRICTIONAL.md, this file and the README |
| Claude Code (command line, `claude -p`), model `claude-opus-5-5` | 2.1.310 for all eight sessions | The scoped sessions, each with its prompt and full transcript in `sessions/`: the CLAUDE.md draft (`session-1`); Effect A, its configuration test and preview (`session-2`); the plan and the build of Effect A's trigger and state test (`session-3`, `session-3b`); Effect B, its configuration test and preview (`session-4`); the plan and the build of Effect B's wiring and state test (`session-5`, `session-5b`); the cost script (`session-6`) |
| Codex (OpenAI's coding agent) | not recorded in its evidence | Use It, at my request: a temporary editor plugin in a scratch copy of the game (`evidence/use-it-code/plugin.cfg` names Codex as its author) that started the real Visual Profiler, read its and the Monitors' cells, drove the real `Main` through the game's input actions and saved the screenshots and logs in `evidence/use-it-code/` |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build | The imports, the headless tests and probes, the Movie Maker strips, the editor (the process shader, the Visual Profiler), and the film's capture |
| GNU coreutils `timeout` (Homebrew) | 9.12 | The time limit in the wrapper |
| Python 3 with Pillow and NumPy | 3.13.5, Pillow 10.4.0, NumPy 2.1.3 | Sampling the background colours for the brief's luminance table from an Assignment 2 screenshot; reading the strips: crops, enlargements, and the pixel comparison of each dust frame with a no-dust render; the film's stills. All but the film's scripts were kept outside the repository |
| FFmpeg (Homebrew) | 9.0.2 | The film only |
| Git | 2.51.0 | Version control; `git archive` for the copy; `git show upstream/main:` to read the course's example |

`/opt/homebrew/bin/godot` is a two-line shim to the app's binary, installed by Claude on 2026-10-24 for Assignment 5; it is outside the repository.

## Textures

There is no texture file in this assignment, and so no separate credits file: this section is the provenance record. No texture was downloaded, and no generative model made one.

| Texture | Where it is defined | What it is |
|---|---|---|
| `Flash`'s texture | `game/effects/slash_sparks.tscn` lines 3–5 (the gradient) and 7–13 | A `GradientTexture2D`, 64 × 64, radial: white-cream to yellow, then a rim in the art's line colour `#290F0D`, fading out at the edge |
| `Sparks`' texture | the same gradient, and lines 15–21 | The same gradient as a 12 × 40 streak |
| `RunDust`'s texture | `game/effects/run_dust.tscn` lines 3–5 and 7–13 | A `GradientTexture2D`, 32 × 32, radial, white fading to transparent, so the colour ramp sets the colour |
| Colour ramps and scale curves | the same scene files | `GradientTexture1D` and `CurveTexture` sub-resources holding the brief's values |

The scoped build sessions wrote them from the settings in CHANGE-BRIEF.md (sections 2 and 3, and Revision 4 for the dust's ramp). The rim colour `#290F0D` is the outline colour of the game's art (`game/systems/art/outline.gdshader` line 12); the other colours were chosen by Claude in the brief and, for the dust, changed in tuning round r1 with my approval. The art the effects play over is Assignment 2's, credited there.

## Human / AI contributions

| Part | AI | Me |
|---|---|---|
| Reading the assignment and the scope | Claude explained the steps | Decided the scope: the 2D game only, without the Assignment 3 props scene |
| Setup | Claude branched from `a5`, copied the game, wrote the `.gitignore`, adapted the wrapper and ran the baselines. It also corrected a commit message of its own that said I had reviewed files I had only seen summarised | Asked for it; asked for CLAUDE.md to be committed empty; decided each commit |
| Choosing the effects | Claude found why its first ideas could not work (the goblins are too far apart for two defeats in one burst; Compatibility draws no particle trails), wrote and ran the Compatibility probe, and put options to me | Asked for Effect B to be a trail behind Rudy; chose the sword sparks and the world-space dust trail, and kept the renderer |
| CHANGE-BRIEF.md | Claude drafted all of it, including the intent, settings, rules, predictions, budgets and short answers, and later Revisions 2–4 from the probes and the tuning rounds | Read it and approved the commit; every revision records a change I approved |
| CLAUDE.md | The scoped session wrote the draft (`998fd175`). Claude wrote its prompt, ran it, checked it, and did the review with a headless probe (`a3242b9d`) | Read the summary and approved both commits |
| The effects, `slash_sparks.tscn` and `run_dust.tscn` | The scoped sessions wrote them from the brief (`ea4419ae`, `017e8a52`). Claude made each approved tuning change | Approved each commit of the sessions' files unedited, and each tuning change |
| The previews | The same sessions wrote them; Claude ran them headless to check the bursts' frames | Watched each one at real speed before Claude read its frames |
| The configuration tests and the scene mutations | The sessions wrote the tests. Claude made the four scene mutations, ran the tests and the mutated previews, and restored the files | Asked for them |
| The trigger code and the state tests | The scoped sessions planned the driver and the state tests, then wrote them and ran the four driver mutations (`ebe2d9d5`, `d0abc9dd`). Claude wrote the prompts, checked each plan against the code, translated `plan-3.md` from Chinese and checked every result | Approved both plans' steps; asked for the plan in English; found that Effect B was missing from the game, which led to its wiring; played the game after each effect was wired in |
| The strips and their readings | Claude ran every Movie Maker capture and every real-speed play, read the frames, predicted each round, measured the invisible dust against a no-dust render, and compared each new strip with its prediction. Its readings are claims, recorded as Claude's in TUNING.md | Gave my first look before Claude read any frame; approved one change per round; gave each verdict after watching the new strip at real speed. Overruled Claude on Effect B's r2: Claude read it as done; I said the dust stayed on the ground, and r3 followed |
| The process shader | Claude described the editor steps and checked every line reference | Generated `particles_generated.gdshader` from a copy of `Sparks`' material and wrote its reading in TEST-REPORT.md (`8b795772`) |
| The cost script | The scoped session wrote and ran `cost_effects.gd` (`fe303c70`); Claude reran it and drafted the report | Asked for it |
| The F9 key | Claude wrote `vsync_debug.gd` and checked it in a window (`d60fb037`) | Asked for it and approved the commit |
| Use It | Codex wrote and ran the instrument and recorded the GPU price and the captures. Claude described the checks, checked the evidence and drafted the report | Chose what to measure, had Codex record it and reviewed it; played the game myself and found the size and control feel fine; asked for the screenshots to be halved and the originals kept out of git |
| The film and its narration | Claude wrote the capture driver, the beat sheet and the narration (spoken by a local Kokoro voice), made the stills, and built and checked the film | Asked for it, watched it, found no problem, and uploaded it |
| Documents | Claude drafted TUNING.md, TEST-REPORT.md (except the process-shader section), FRICTIONAL.md, this file and the README from our conversation and the logs | Wrote TEST-REPORT.md's process-shader section; checked the others against what I did |
