# Assignment 5 - A Shader and a Material That Say Something About Your Game

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 50 after the first class day.

**Covers:** [Module 6 — Shader foundations](../modules/06-shader-foundations/lesson.md) and [Module 7 — Materials and textures](../modules/07-materials-and-textures/lesson.md), and their chapters, [Shader Foundations](../chapters/06-shader-foundations.md) and [Materials and Textures](../chapters/07-materials-and-textures.md).

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

You add two visual layers to the game you have been building since Assignment 2. First you write `CLAUDE.md`, the context file Claude Code reads at the start of every session, with a specification of one visible effect and its boundaries, before any shader exists. Then you direct Claude Code to build that effect: a shader that tells the player about one game state, driven by game code and tested at three pinned frame rates. Last, you give one 3D object a material pass with sourced or generated textures, audited, attributed, and judged under lighting you control. You hand in the repository tagged `a5`, your evidence, and one `godot-gamedev` film. A passing headless run proves that the shader parses, its uniforms are driven as specified, and the material is wired as audited. It proves nothing about what the screen shows, so every visual rule ends in a human check you perform and record.

## Your task

1. **Project context.** Write `CLAUDE.md`: the facts an agent cannot discover quickly or will get wrong, and your effect specification.
2. **A shader that communicates a game state.** Pick one state the player must notice. Damage, danger, selection, a dissolve, water, an outline: these are examples of the kind of thing, not a menu. The effect has stated boundaries and controlled-input tests.
3. **A material pass on a 3D object**, with sourced or generated textures, audited, attributed, and judged under controlled lighting.

**Your game, one more layer.** From Assignment 2 on, you build one game, the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. Assignments 3–10 each add one layer and are submitted as a git tag; this one is **`a5`**. If your game is 2D, do part 3 in the 3D scene you added in Assignment 3 or 4. The one change of game the course allows had to happen before Assignment 4; if you made it, your submission note says so. This is an individual assignment.

Claude Code assistance is expected; use your Northeastern access. Nothing paid is required, and paid output earns no bonus. You remain responsible for the specification, for reviewing everything the agent writes, and for every human check.

### What counts

| Part | Minimum |
|---|---|
| `CLAUDE.md` | At the repository root, under 120 lines, every fact with a file reference. If the repository has an `AGENTS.md`, the first line is exactly `@AGENTS.md`, so new context never silently drops the existing rules. |
| Shader effect | One `canvas_item` or `spatial` shader on a `ShaderMaterial`, changing how something looks while one named game state holds, with at least one uniform set by game code from that state. `TIME` may animate the effect but cannot link it to the state: it is global engine time, not time since your event. |
| Material pass | One 3D object whose material uses at least two textures in different roles, at least one of them data rather than colour (a normal, roughness, metallic or ambient-occlusion map, or a packed ORM texture). |

### Rights and provenance

- **Sourced textures:** record the source URL, authors and roles, licence, and date checked in a credits file next to the asset (for example `ATTRIBUTION.md`). [Poly Haven's licence](https://polyhaven.com/license) requires no credit; the course requires provenance anyway.
- **Generated textures:** follow Assignment 2's rules (free or local model, name, version and terms in `SOURCES.md`, prompt logged, no named living artist, brand or copyrighted character). A generated "normal map" is only a picture of one until it passes the pixel check below. Textures written by code are fine; show the code.
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd)'s `SOURCES.md` says public availability is not a licence grant for its inherited work: study it, do not copy its art. Never commit credentials.

## 1. Predict

Commit `CHANGE-BRIEF.md` before your first prompt. Keep the original; add dated revisions below it.

### `CHANGE-BRIEF.md` — the state, the rules, the predictions

- **The state:** what the effect communicates, why the player needs it, and the script and variable that hold it.
- **The effect specification**, in a block you will paste into `CLAUDE.md`. Chapter 6's failure-flash specification is a model of the form, not the content:
  - *Observable rules* that can be measured: the uniform's value when the state begins and ends, how long any change takes in seconds, and that it takes the same game time at 30, 60 and 144 frames per second.
  - *Boundaries:* collision, movement, input, the state machine and its timings, existing test expectations, and every other object stay unchanged. Presentation code may read game state; it never writes it.
  - *The evidence split:* for each rule, a headless test or your eyes, and how.
- **Controlled inputs and predicted values.** Three uniform values (for example 0.0, 0.5 and 1.0) and at least two named pixels of the shaded object. Compute by hand what each pixel becomes at each value on your real background, as Chapter 6 does for `mix()`. This only works for output you can model: an unshaded, or fixed-lighting, result. If your effect is lit by the scene, either fix the lighting for these three screenshots and say how, or make the effect's colour independent of light. If the effect changes contrast against a background, compute the ratio.
- **The material plan:** the object; each texture's role, source, and whether it holds colour (sRGB) or data (linear); the import settings you expect; the lighting you will judge under; how visible you expect the change to be.
- **At least three predicted failure cases**, each with the check that would catch it.

Then answer briefly:

1. Which renderer does `project.godot` name, and what does it rule out? (Decals and compute shaders need Forward+ or Mobile; VoxelGI, SDFGI and SSIL are unavailable in Mobile and Compatibility.)
2. What colour arrives in your fragment function, and what would the tempting alternative give you? (For `canvas_item`: `texture(TEXTURE, UV)` instead of `COLOR`.)
3. How long would a frame-counting version of your effect last at 30, 60 and 144 frames per second?
4. An agent wires a texture into a material by editing text and never opens the editor. What happens to that texture's import settings?

## 2. Build It

Read the module lessons and both chapters first; [Example 06](../examples/06-shader-foundations/) and [Example 07](../examples/07-materials-and-textures/) hold their real prompts, diffs, tests and logs. Public Walker projects that demonstrate the techniques: [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) (the failure flash), [walker-compute-post-shader](https://github.com/nikbearbrown/walker-compute-post-shader) (a verification record that states its boundary), [walker-3d-graphics-settings](https://github.com/nikbearbrown/walker-3d-graphics-settings) (the ship Chapter 7 audits) and [walker-3d-decals](https://github.com/nikbearbrown/walker-3d-decals) (four texture licences in one project).

Commands assume your project lives in `godot/`; change `--path` if not. Run `--import` once after cloning. Wrap every test in `timeout`, because a script error before `quit()` leaves headless Godot running (`brew install coreutils` provides it on macOS). Pin frame-counted tests with `--fixed-fps`. Exit code 0 does not mean no errors: read stderr for `SHADER ERROR`.

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/<existing_test>.gd --fixed-fps 60
```

Run each existing test that way and record the counts: your baseline.

### Step 1 — `CLAUDE.md`

The specification block is yours; the agent copies it and fills in project facts, each with a reference.

```text
You are working in my game repository (Godot 4, GDScript, project in
godot/). Do not change any file except the one you create: CLAUDE.md at
the repository root.

Read AGENTS.md if it exists, README.md, CHANGE-BRIEF.md,
godot/project.godot, the scripts that own the game state named in
CHANGE-BRIEF.md, the script and scene that draw the object my effect will
change, the 3D scene and object named for the material pass, and the
test scripts in godot/tests/.

Write CLAUDE.md, under 120 lines, in this order:
1. If AGENTS.md exists, the first line is exactly: @AGENTS.md
2. "Project context": engine version, renderer, main scene, how the
   shaded object is drawn, which script owns the game state that drives
   the effect, the 3D object for the material pass and where its
   material comes from, and the exact headless test commands. Give a
   file reference for every fact. Do not guess.
3. "Effect specification": copy the block between SPEC BEGIN and
   SPEC END below word for word.
4. "Out of scope": what this change must not touch, in your own words,
   consistent with the spec.
5. "Unconfirmed": anything you could not confirm from the files.

Do not write a shader and do not edit any script. Stop after CLAUDE.md.

SPEC BEGIN
(paste your effect specification from CHANGE-BRIEF.md here)
SPEC END
```

To run it non-interactively with scoped tools and a kept transcript, save it as `prompt-1.txt`:

```bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Glob,Grep,Bash(git:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > session-1.jsonl
```

Commit the draft unedited, then review it. In Chapter 6's run the draft cited wrong lines, listed a build script as a test, and claimed a headless test would settle the look. Check every reference, delete non-tests, and add a "Headless facts" block; the [reviewed `CLAUDE.md`](../examples/06-shader-foundations/files/CLAUDE.md) has four lines to adapt once confirmed on your machine. Commit your review separately. Codex reads `AGENTS.md`, not `CLAUDE.md`; if you use it, begin each prompt with "Read CLAUDE.md first".

### Step 2 — the shader effect

Ask for a plan first; you decide whether to accept it.

```text
Read CLAUDE.md first. Its effect specification is the contract for this
change; its headless facts describe what a test on this machine can
observe.

First propose the smallest plan that meets the spec: the shader file, the
code that gives the object a ShaderMaterial, the code that sets each
uniform from game state, and a new headless test in godot/tests/. Say
which spec rule each test assertion covers, and which rules only a human
can check. Do not edit yet.

After I approve a step, implement only that step and show the diff.
Rules:
- Do not edit the existing tests or change their expectations.
- The new test must drive the state through the real game loop and real
  input, not by calling the update function directly.
- Run the existing test commands from CLAUDE.md, then your new test at
  --fixed-fps 30, 60 and 144. Show the real output, including any
  SHADER ERROR lines.
- Say exactly what your test proves and what it cannot prove in a
  headless run, and list the human checks needed to judge the look.
- Do not commit.
```

This prompt asks for a plan and then waits for your approval, which a one-shot `claude -p` run cannot do. Run it interactively in `claude`, or in two invocations: one that stops after the plan, and a second, written by you after reading the plan, that implements the steps you approved. For a non-interactive step, Chapter 6 scoped the session like this; `Bash(godot --headless:*)` lets the agent run tests but not open a window.

```bash
claude -p "$(cat prompt-2.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose > session-2.jsonl
```

Then write your own check, modelled on Example 06's [`verify_flash.gd`](../examples/06-shader-foundations/tests/verify_flash.gd): assert the uniform list from `get_shader_uniform_list()` (a shader that failed to parse returns an empty list), read defaults from the source text (a headless engine does not report them), trigger the state with a real event and real input, and sample from a node with a high `process_priority`, so it reads after every other `_process()` in the frame. Run it at `--fixed-fps` 30, 60 and 144. Delete one semicolon from the shader, confirm the check exits 1, and restore the file. Commit the check on its own.

### Step 3 — the material pass

Get the textures first. Then audit, with no changes, using this adaptation of Chapter 7's prompt:

```text
Inspect before editing. Always run Godot with --headless; never add
--rendering-driver. A headless run uses a dummy renderer: it draws
nothing.

Task: audit the material of the 3D object named in CHANGE-BRIEF.md, then
write a headless test that pins what you found. Do not change any
material, scene or .import file in this task.

1. Read the object's scene and material resources (or the imported
   scene's materials), the .import file of every texture it uses, and
   the lights and environment that light it.
2. Write godot/MATERIALS.md with:
   - one table row per material slot actually used: slot, texture file,
     channel, whether the data is color (sRGB) or non-color (linear),
     and the texture's import settings (compress/mode,
     compress/normal_map, mipmaps/generate, detect_3d/compress_to);
   - the material flags and scalars that change the look;
   - the lights and environment effects that light the object;
   - findings: anything that looks wrong, wasteful or unused, each with
     the evidence line;
   - attribution, using exactly the facts in CHANGE-BRIEF.md, which I
     checked myself.
3. Write godot/tests/test_materials.gd (extends SceneTree) that loads the
   scene headlessly and asserts the table: every slot's texture path and
   channel, the flags and scalars, and the import settings read from the
   .import files with ConfigFile. Add a pixel check that each normal map
   is a plausible tangent-space normal map (decode with
   Image.load_from_file; blue above 0.5 on at least 95% of sampled
   texels), and report the same statistic for each color texture. Print
   one PASS/FAIL line per check and exit 1 on any failure.
4. Run it with --headless --fixed-fps 60 and show the real output. Say
   what the test cannot establish headlessly.
Do not commit.
```

Commit the audit unedited, then review it: look up every integer enum, check format claims with `get_image().get_format()`, and delete numbers nobody measured. Commit your corrections separately. Then the change, plan first:

```text
Read godot/MATERIALS.md and godot/tests/test_materials.gd first.

Change one thing: give the object the material described in
CHANGE-BRIEF.md. First propose the plan, without editing: the resource
you will create or change, how it is wired so a reimport keeps it, every
property that changes and why, and the assertions you will add. Do not
edit the source model or any existing texture.

After I approve, implement it, reimport with
godot --headless --path godot --import, update test_materials.gd so it
proves the new material is in place with the properties the change
exists to set and that everything else matches the audit, run it with
--fixed-fps 60, and show the real output. List the human checks needed
to judge the material under the lighting in MATERIALS.md.
Do not commit.
```

For an imported 3D scene, the material belongs behind the importer's per-material **Use External** setting, so a reimport keeps it ([advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html)). Verify from an empty cache: delete `godot/.godot`, reimport, and run the test.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_materials.gd --fixed-fps 60
```

Then mutate the one property your change exists to set (Chapter 7's was `ao_enabled`), confirm the test exits 1, and restore it.

### What the agent is likely to get wrong

Each row happened in the runs behind Chapters 6 and 7.

| Recorded mistake | How it was caught |
|---|---|
| After a 30 fps failure, the agent rewrote its test to call the update function directly; the frame rate stopped mattering, and the summary still reported 30 and 144. | Reading the test, not the summary. |
| Uniform "type" checks were set-then-get round trips; with a semicolon deleted from the shader, all 11 still passed. | The mutation, plus a uniform-list assertion. |
| The audit misnamed an enum (`4` is `TONE_MAPPER_AGX`, not ACES), invented memory figures, and proposed a "fix" that would have mislabelled a menu. | Looking each value up. |
| An import setting written as a flat key the importer ignores; a UID typed by hand. | A failing test; a headless probe. |
| An `ORMMaterial3D` with `ao_enabled` left off passed a 100-check test that never asserted the flag. | A probe, then one assertion on the flag. |

### What must not change, and what counts as done

Must not change: collision, movement, input, game-state logic and timings, existing tests, objects outside your boundary, and the source model and texture files. Done means every specification rule has a recorded machine or human check, both mutations fail their tests, every texture is credited, and the earlier suites give their baseline counts. "Claude said it works" is not on the list.

## 3. Use It

Open the project in the Godot editor and run it. Record actual results in `TEST-REPORT.md`, with the source revision, Godot version and renderer:

| Check | Evidence to collect |
|---|---|
| Baseline | Every earlier test, before and after, with pinned frame rate and counts. |
| Shader parses | Uniform-list assertion, no `SHADER ERROR` line, and the mutation exiting 1. |
| Driver | The uniform sampled every frame at 30, 60 and 144 fps through a real event: first value, last value, game-time duration. |
| Controlled values (HUMAN CHECK) | A screenshot per controlled value; sampled pixels beside your predicted table. |
| In play (HUMAN CHECK) | The state triggered by normal play several times; boundaries hold. |
| Material wiring | The material test after a fresh import, and its mutation exiting 1. |
| Texture data | The normal-map statistic for every normal map and colour texture. |
| Material look (HUMAN CHECK) | Change-on and change-off screenshots from one camera under the stated lighting. |
| Import settings | The diff of any `.import` file the editor rewrote, explained. |

For controlled values, use the [Remote scene tree](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) to change the uniform in the running, paused game. Screenshot each value with no colour management in your screenshot tool, and sample your named pixels. Your prediction assumes the arithmetic happens on the values as written, which Chapter 6 reports as a reading of the source, not an observation. A difference of more than a step or two per channel is a finding: record it with the screenshot, then find out why.

For the material, light the object as `CHANGE-BRIEF.md` says and switch off effects you could confuse with your change, such as SSAO when you judge an AO texture. Do not write "looks better" unless you compared two images. Texture detection runs only when a real editor draws the texture, so run `git status` after your first editor session.

Include at least one inspect-and-revise cycle driven by an observation. Do not delete a failing assertion or weaken an expected result to obtain a green report. If another person looks at your effect, record their actual words; do not invent a playtester. Your own playtest is required, and no headless run replaces it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier. It pairs each code excerpt with the visible result it produces; for a shader, that result is real engine output captured on your display, never a headless log. Ask Claude Code to read the installed skill instructions and follow them. If your checkout lacks the skill, request the course-provided version.

Make **one** landscape film that:

1. Identifies your game, the state your effect communicates, and the object given the material pass.
2. Shows your specification: which rules a machine checks and which you checked by eye.
3. Shows the shader and driver lines, each followed by your controlled-value screenshots and the effect in play.
4. Shows the material change, followed by your change-on and change-off screenshots.
5. Shows what the tests proved, the mutations that failed them, and what no headless run can show.
6. States the agent mistakes you caught, what remains uncertain, one next step, the human and AI contributions, the texture sources, and the revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed editor views, scripted-input captures and held frames; never present a reconstruction as a screenshot. Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. There is no minimum runtime. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**. The film is part of the 60-point category below, not a substitute for working source.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with the shader, driver, material resources, and used textures with their `.import` files; no `.godot` cache or credentials.
- `README.md`: project name, starting point, engine version and renderer, run instructions, controls, what this assignment added, known limitations, and the film link.
- `CLAUDE.md` as reviewed, `CHANGE-BRIEF.md`, `MATERIALS.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`, and the texture credits file.
- Your tests, cited logs, screenshots, prompts, and any `claude -p` transcript under about 1 MB (otherwise a labelled excerpt).
- The film's beat sheet, script/prompts, and evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit in the order the work happened, so a reviewer can see which lines an agent wrote: agent draft, your review, agent change, your check or fix. Use messages that say what was checked, for example `Danger tint (shader + driver + test); headless checks at 30/60/144 fps; look checked by hand in the editor`. Tag the final submission commit **`a5`**.

## 5. Verify and submit to Canvas

Clone the `a5` tag into a fresh folder. Run `--import` once, then every test at its pinned frame rates; confirm the counts match `TEST-REPORT.md` and no log contains `SHADER ERROR`. A working local folder is not proof that everything was posted.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 5 - A Shader and a Material That Say Something About Your Game
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Game-source revision shown in the film:
Godot version, renderer, and operating system:
Game state the shader communicates:
3D object and scene given the material pass:
Texture sources and licences (or model, version, and terms):
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
Changed games since Assignment 2 (yes/no; if yes, FRICTIONAL.md entry):
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and the film must refer to the same submitted work; identify later changes as a new revision.

## Rubric — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| Frictional — honest log | 10 |
| GitHub version posting matching Canvas | 10 |
| Relative Quartile | 20 |
| **Total** | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|---|---:|
| Context and specification: `CLAUDE.md` with a file reference for every fact, headless facts, and your corrections committed apart from the agent's draft (5); a specification with measurable rules, boundaries and an evidence split, committed before any shader (5). | 10 |
| Shader effect: communicates the named state in the running game and meets its specification (6); driven from game state, frame-rate independent, boundaries kept (3); works in the project's renderer with the specified uniforms, types, hints and defaults (3). | 12 |
| Material pass: an audit of slots, channels, colour and data roles, import settings and lighting, with your corrections (4); a change that survives a fresh import, with recorded provenance and attribution (4); an A/B judgment under stated, controlled lighting (4). | 12 |
| Verification: a shader check that detects a parse failure, shown failing on a mutation (4); the driver sampled at three pinned frame rates through real events (3); a material test that passes after a fresh import and fails on a mutation (3); human checks at controlled values against your predictions (3); an evidence-based revision and an honest limitation (3). | 16 |
| Brutalist explainer: accurate explanation of effect and material (4); excerpts followed by real captured engine output (3); test limits, contributions and texture sources stated (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing headless suite establishes that the shader parses, its uniforms are driven as specified, and the material is wired as audited; it does not establish that anything looks right, so a missing human check loses that check's points whatever the logs say.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source and documentation are actually posted.
- **3 points:** Canvas identifies the exact submitted commit and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit your starting point, every texture source and generative model with its terms, collaborators, and tools. Describe what AI contributed to the code, tests, audit, script, and narration, and what you personally specified, checked, changed, or rejected.

The instructor or a TA may ask you to set your uniform in the running game and predict a named pixel's colour before you look, or to explain why a texture is imported as data. Inability to explain reduces points under the relevant criteria. Recording a human check you did not perform misrepresents verification; misrepresenting authorship, provenance, or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.
