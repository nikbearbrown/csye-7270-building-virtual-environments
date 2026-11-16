# Assignment 5 - Shaders, Materials, and the Godot Shading Language

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies.

**Covers:** Module 6 — Shader foundations and Module 7 — Materials and textures, and their chapters, Shader Foundations and Materials and Textures.

**Required viewing:** [AI Policy for Professor Bear's Courses \| Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw).

## Executive summary

You add two hand-written shaders, and the materials that use them, to the game you have been building since Assignment 2.

First you write `CHANGE-BRIEF.md`, a specification for a colour effect that names the one line of shading language that produces it, before any shader exists. Then you write `CLAUDE.md`, the context file Claude Code reads at the start of every session, which imports that specification.

Then you hand-write the effect's shader from code alone: no textures, only uniforms, built-ins and arithmetic. One uniform is driven by game state through a driver and tests that Claude Code writes.

Next you hand-write a `spatial` shader that reads textures as information and exposes its parameters as Inspector controls. Two materials use it and look different. You also run one experiment that reads the same texture as colour and as data.

Last, you read the shader Godot generates for a `StandardMaterial3D` and answer questions about the Godot shading language, with line references to your own code.

You hand in the repository tagged `a5`, your evidence, and one `godot-gamedev` film. A passing headless run proves that your shaders parse, their uniforms are declared and driven as specified, and your materials are wired as audited. It proves nothing about what the screen shows, so every visual rule ends in a human check you perform and record.

## Your task

1.  **Project context.** Write `CLAUDE.md`. It holds the facts an agent cannot discover quickly or will get wrong, and a line importing your specification.
2.  **A shader from code alone.**
    - *What a shader is:* a small program the GPU runs for every vertex and every pixel of whatever it draws, all in parallel. Each run sees only built-in values, uniforms that game code sets, and textures. It writes its outputs and remembers nothing, which is why game state must reach it as a uniform.
    - *Your shader:* hand-write one that adds colour to one object while one game state holds. It uses no textures of its own, so every value on screen comes from a uniform, a built-in or arithmetic. Damage, danger, selection, a power-up glow: these are examples of the kind of thing, not a menu.
3.  **A shader that reads textures, and the materials that use it.**
    - *What a material is:* a resource that pairs one shader with values for that shader's uniforms, including the textures that fill its samplers. Many materials can share one shader.
    - *What a texture is:* a grid of numbers whose meaning is decided by the shader that samples it. Colour stored in sRGB must be decoded before arithmetic. Data such as a mask, noise, roughness or a normal map must be read as stored.
    - *Your shader:* hand-write a `spatial` shader that samples both kinds and exposes its parameters as Inspector controls. Two materials use it and look different.
4.  **The language.**
    - *What the Godot shading language is:* a language close to GLSL ES 3.0. You choose a `shader_type` instead of writing `main()`, and the type decides which processor functions and built-ins exist. Uniform hints shape the Inspector, and some hints also change the value the shader receives.
    - *Your task:* read the shader Godot writes for a `StandardMaterial3D`, and answer questions about the language with line references to your own shaders.

By the end you should be able to explain four things in your own words, each with a line of your own code:

- what a shader does;
- how a material differs from a shader;
- why a texture is information rather than a picture;
- what the Godot shading language is.

**Your game, one more layer.** From Assignment 2 on, you build one game, the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. Assignments 3–10 each add one layer and are submitted as a git tag; this one is **`a5`**. If your game is 2D, do parts 3 and 4 in the 3D scene you added in Assignment 3 or 4. The one change of game the course allows had to happen before Assignment 4; if you made it, your submission note says so. This is an individual assignment.

**Who writes what.** You write every line of both shaders, the hint-experiment shader, and the language notes yourself. Claude Code assistance is expected for everything else: it drafts `CLAUDE.md`, writes the driver and the tests, audits the materials, and reviews your shaders when you ask. It does not edit them.

If you adopt one of its suggestions, type it in yourself, record it in `SOURCES.md` and `FRICTIONAL.md`, and be ready to explain it. Use your Northeastern access. Nothing paid is required, and paid output earns no bonus. You remain responsible for the specification, for reviewing everything the agent writes, and for every human check.

### What counts

| Part | Minimum |
|----|----|
| `CLAUDE.md` | At the repository root, under 120 lines, with a file reference for every project-context fact. If the repository has an `AGENTS.md`, the first line is exactly `@AGENTS.md`, so new context never silently drops the existing rules. The specification is imported with a line reading `@CHANGE-BRIEF.md`, not pasted, so it can be replaced at the next assignment without the old contract lingering. |
| Shader from code | One `canvas_item` or `spatial` shader that you wrote, on a `ShaderMaterial`, that changes the colour of one object while one named game state holds. It has no sampler uniforms of its own; the object's sprite texture arriving in `COLOR` is fine. It has at least two uniforms, each with a type, a hint and a default, and one of them is a float set by game code from that state. The colour change is the colour line from your specification. `TIME` may animate the effect but cannot link it to the state: it is global engine time, not time since your event. |
| Textured shader and materials | One `spatial` shader that you wrote, on a 3D object, sampling at least two textures: at least one colour texture with `source_color`, and at least one data texture without it (a mask, noise, height or roughness map, or a normal map with `hint_normal`). It has at least four non-texture uniforms with hints and defaults, organized into at least two `group_uniforms` groups. Two `ShaderMaterial` resources use this one shader and differ in at least two values or one texture. The part also includes the hint experiment. |
| The language | The shader generated from one converted `StandardMaterial3D`, annotated, and `LANGUAGE-NOTES.md` answering the questions in Step 4, each with a line reference. |

### Rights and provenance

- **Sourced textures:** record the source URL, authors and roles, licence, and date checked in a credits file next to the asset (for example `ATTRIBUTION.md`). [Poly Haven's licence](https://polyhaven.com/license) requires no credit; the course requires provenance anyway. Poly Haven ships normal maps in two conventions, `_nor_gl` and `_nor_dx`. Godot expects OpenGL, so record which one you used.
- **Generated textures:** follow Assignment 2's rules (free or local model, name, version and terms in `SOURCES.md`, prompt logged, no named living artist, brand or copyrighted character). A generated "normal map" is only a picture of one until it passes the curl check in Step 3. Textures written by code are fine; show the code.
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd)'s `SOURCES.md` says public availability is not a licence grant for its inherited work: study it, do not copy its art. Never commit credentials.

## 1. Predict

Commit `CHANGE-BRIEF.md` before you write either shader or send your first prompt. Keep the original; add dated revisions below it. `CLAUDE.md` imports this file, so it is the contract the agent works to.

### `CHANGE-BRIEF.md` — the state, the rules, the predictions

- **The state:** what the effect communicates, why the player needs it, and the script and variable that hold it.
- **The effect specification**, in its own section. Chapter 6's failure-flash specification is a model of the form, not the content:
  - *The shader:* its path in `godot/shaders/`, its `shader_type` and any `render_mode`, and each uniform's name, type, hint, default, and what sets it.
  - *The colour line:* the one line of Godot shading language, inside `fragment()`, that changes the colour. You write the shader from it, and your predictions are computed from it.
  - *Observable rules* that can be measured:
    - the uniform's value when the state begins and when it ends;
    - how long any change takes in seconds, with a tolerance of one frame period, and that it takes the same game time at 30, 60 and 144 frames per second;
    - what happens when the state begins again mid-transition: restart, extend or ignore;
    - whether the duration is measured in scaled or unscaled time under `Engine.time_scale`, and what the effect does while the tree is paused;
    - the uniform's value if the state ends before a transition finishes;
    - if the object has several instances, how each gets its own value.
  - *Boundaries:* collision, movement, input, the state machine and its timings, existing test expectations, and every other object stay unchanged. Presentation code may read game state; it never writes it.
  - *The evidence split:* for each rule, a headless test or your eyes, and how.
- **Controlled inputs and predicted values.** Choose three uniform values (for example 0.0, 0.5 and 1.0) and at least two named pixels of the shaded object. Using your colour line, compute by hand what each pixel becomes at each value on your real background, as Chapter 6 does for `mix()`.
  - This only works for output you can model: an unshaded or fixed-lighting result. If your effect is lit by the scene, either fix the lighting for these captures and say how, or make the effect's colour independent of light.
  - If your project enables HDR 2D (`rendering/viewport/hdr_2d`), 2D blending happens in linear space and your arithmetic must account for it.
  - If the effect changes contrast against a background, compute the ratio.
- **The hint experiment.** Take a 3×1 PNG whose texels are the greys 64, 128 and 192, sampled once with `source_color` and once without, on unshaded quads under a Linear tonemap at exposure 1.0.
  - Predict the displayed 8-bit value of each band on each quad. The sRGB encoding function is `encode(x) = 12.92x` for `x ≤ 0.0031308`, and `1.055·x^(1/2.4) − 0.055` otherwise.
  - Say which quad you expect to show the file's values unchanged, and why.
  - These predictions assume Forward+ or Mobile. If you use Compatibility, say so and measure before you explain.
- **The material plan:**
  - the object, and the lighting you will judge under;
  - for each texture: its role and source, what its numbers mean, whether the shader samples it as colour (with `source_color`) or as data (without it), and the import settings you will set explicitly (`compress/mode`, `compress/normal_map`, `mipmaps/generate`). Set them rather than leaving them on Detect, so the editor has nothing to change later;
  - for each uniform: its name, type, hint, range, default and group, and what you expect to change on screen across its range;
  - what differs between the two materials, and why.
- **At least three predicted failure cases**, each with the check that would catch it. The rules above are good sources: an effect that restarts when it should ignore, one enemy's flash appearing on every enemy, a duration that changes under time scale, a data texture sampled with `source_color`.

Then answer briefly:

1.  Which renderer does `project.godot` name, and what does it rule out? (Decals and compute shaders need Forward+ or Mobile; VoxelGI, SDFGI and SSIL are unavailable in Mobile and Compatibility.)
2.  What colour arrives in your fragment function before you change it, and what would the tempting alternative give you?
    - For `canvas_item`: what would `texture(TEXTURE, UV)` give you instead of `COLOR`?
    - For `spatial`: what does `ALBEDO` hold if you never write it, and what does `COLOR` hold?
3.  How long would a frame-counting version of your effect last at 30, 60 and 144 frames per second?
4.  Which resource holds your uniform's default, which holds its current value, and what happens if two objects share the material?
5.  Does `hint_range` clamp a value your driver sets from code? Predict now; you will check in Use It.

## 2. Build It

Read the module lessons and both chapters first; Example 06 and Example 07 hold their real prompts, diffs, tests and logs. In those examples an agent writes the shader. In this assignment you write it, and the agent works on the driver, the tests and the review.

Public Walker projects that demonstrate the techniques:

- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd): the failure flash;
- [walker-compute-post-shader](https://github.com/nikbearbrown/walker-compute-post-shader): a verification record that states its boundary;
- [walker-3d-graphics-settings](https://github.com/nikbearbrown/walker-3d-graphics-settings): the ship Chapter 7 audits;
- [walker-3d-decals](https://github.com/nikbearbrown/walker-3d-decals): four texture licences in one project.

Commands assume your project lives in `godot/`; change `--path` if not. Run `--import` once after cloning.

bash

``` bash
godot --headless --path godot --import
```

Commit this wrapper before Step 1 and run every test through it. It does four things:

- wraps the test in `timeout`, because a script error before `quit()` leaves headless Godot running (`brew install coreutils` provides it on macOS);
- pins the frame rate with `--fixed-fps`;
- keeps a log;
- fails on `SHADER ERROR` and `SCRIPT ERROR` lines, because exit code 0 does not mean no errors.

An exit status of 124 means the test hung.

bash

``` bash
#!/usr/bin/env bash
# scripts/run-test.sh <test-file.gd> <fps>
set -o pipefail
mkdir -p logs
log="logs/$(basename "$1" .gd)_${2}fps.log"
timeout 120 godot --headless --path godot --script "res://tests/$1" --fixed-fps "$2" 2>&1 | tee "$log"
status=$?
if grep -qE "SHADER ERROR|SCRIPT ERROR" "$log"; then status=1; fi
exit $status
```

bash

``` bash
./scripts/run-test.sh <existing_test>.gd 60
```

Run each existing test that way and record the counts: your baseline.

After every agent session, do two checks:

1.  **Read the final result event** in the session's `.jsonl` file. It records whether the run stopped at `--max-turns`, and current versions list permission denials. A run that hit the turn limit ends with the same apparent calm as one that finished.
2.  **Run `git diff --stat godot/shaders/`**, which must print nothing. Tool permissions prevent accidents but contain nothing: an agent that can write a `.gd` file and run Godot can execute anything. The diff is your guarantee. Diff `scripts/run-test.sh` in every review too, since the agent can edit it.

### Step 1 — `CLAUDE.md`

The specification is yours, in `CHANGE-BRIEF.md`. The agent imports it and fills in project facts, each with a reference.

text

``` text
You are working in my game repository (Godot 4, GDScript, project in
godot/). Do not change any file except the one you create: CLAUDE.md at
the repository root.

Read AGENTS.md if it exists, README.md, CHANGE-BRIEF.md,
godot/project.godot, scripts/run-test.sh, the scripts that own the game
state named in CHANGE-BRIEF.md, the script and scene that draw the
object my effect will change, the 3D scene and object named for the
textured shader, and the test scripts in godot/tests/.

Write CLAUDE.md, under 120 lines, in this order:
1. If AGENTS.md exists, the first line is exactly: @AGENTS.md
2. "Project context": engine version, renderer, main scene, how the
   shaded object is drawn, which script owns the game state that drives
   the effect, the 3D object for the textured shader and where its
   material comes from, and the exact test commands, all through
   scripts/run-test.sh. Give a file reference for every fact. Do not
   guess.
3. "Current change": a heading followed by exactly this line:
   @CHANGE-BRIEF.md
4. "Ownership": files in godot/shaders/ are hand-written by the human
   and are never edited by an agent.
5. "Out of scope": what this change must not touch, in your own words,
   consistent with the spec.
6. "Unconfirmed": anything you could not confirm from the files.

Do not write a shader and do not edit any script. Stop after CLAUDE.md.
```

To run it non-interactively with scoped tools and a kept transcript, save it as `prompt-1.txt`:

bash

``` bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Glob,Grep,Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > session-1.jsonl
```

The git permissions are read-only on purpose. An agent allowed `git:*` can commit its own draft, which erases the record a reviewer uses to tell who wrote which lines.

Commit the draft unedited, then review it. In Chapter 6's run, the draft cited wrong lines, listed a build script as a test, and claimed a headless test would settle the look. Check every reference, delete non-tests, and add a "Headless facts" block. The reviewed `CLAUDE.md` has four lines to adapt once confirmed on your machine. Commit your review separately. Codex reads `AGENTS.md`, not `CLAUDE.md`; if you use it, begin each prompt with "Read CLAUDE.md first".

### Step 2 — the shader from code

Write `godot/shaders/<name>.gdshader` by hand from your specification, using the colour line exactly as specified. If the line has to change, revise the specification first, with a date. Reimport, and confirm no `SHADER ERROR` appears. Commit the shader on its own, for example `Danger tint shader, hand-written`.

Then direct the driver and its test, plan first; you decide whether to accept the plan.

text

``` text
Read CLAUDE.md first. The specification in CHANGE-BRIEF.md is the
contract for this change; its headless facts describe what a test on
this machine can observe. The shader in godot/shaders/ is hand-written
by me and is not yours to edit: do not edit any .gdshader file. If you
believe it is wrong or cannot meet the spec, say so and stop.

First propose the smallest plan that meets the spec: the code that gives
the object a ShaderMaterial using my shader, the code that sets each
uniform from game state, and a new headless test in godot/tests/. Say
which spec rule each test assertion covers, and which rules only a human
can check. Do not edit yet.

After I approve a step, implement only that step and show the diff.
Rules:
- Do not edit the existing tests or change their expectations.
- The test asserts the shader's uniform names and types with
  get_shader_uniform_list(), and reads defaults from the shader source
  text, because a headless engine does not report them.
- The test drives the state through the real game loop and real input,
  not by calling the update function directly, and checks the retrigger
  rule.
- Sample the uniform from a node with a high process_priority, so it
  reads after every other _process() in the frame.
- Run every test with ./scripts/run-test.sh: the existing ones at 60,
  and the new one at 30, 60 and 144. Show the real output, including any
  SHADER ERROR lines.
- Say exactly what your test proves and what it cannot prove in a
  headless run, and list the human checks needed to judge the look.
- Do not commit.
```

This prompt asks for a plan and then waits for your approval, which a one-shot `claude -p` run cannot do. Run it interactively in `claude`, or in two invocations: one that stops after the plan, and a second, written by you after reading the plan, that implements the steps you approved. For a non-interactive step, scope the session like this:

bash

``` bash
claude -p "$(cat prompt-2.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(./scripts/run-test.sh:*),Bash(godot --headless --path godot --import:*),Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Edit(godot/shaders/**)" --max-turns 60 --output-format stream-json --verbose > session-2.jsonl
```

Then mutate the shader twice. Each time, confirm the test exits 1, then restore the file.

1.  **Delete one semicolon.** This proves the test detects a parse failure; a shader that failed to parse returns an empty uniform list.
2.  **Rename the driven uniform in the shader only.** This proves the test checks the name contract the driver depends on. `set_shader_parameter` with a name the shader doesn't declare raises no error, and reading it back returns the stored value, so only the uniform-list assertion catches it.

Record both results.

### Step 3 — the textured shader and its materials

**Textures and import settings.** Get the textures first, following the provenance rules above. Set their import settings explicitly, as your plan says, and reimport.

**The shader and its two materials.** Write the shader by hand. Make two `ShaderMaterial` resources as `.tres` files that both reference it, and place them in your 3D scene. For an imported 3D scene, the material belongs behind the importer's per-material **Use External** setting, so a reimport keeps it ([advanced import settings](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/advanced_import_settings.html)).

**The hint experiment**, in its own scene:

- A GDScript you commit writes the 3×1 PNG. Import it lossless, with no mipmaps.
- A `spatial` shader with `render_mode unshaded` has two samplers bound to that same file: one with `source_color, filter_nearest`, one with `filter_nearest` only. A `bool` uniform picks which sampler writes `ALBEDO`.
- Two materials from that shader, one per `bool` value, go on two quads facing the camera.
- A `WorldEnvironment` sets a Linear tonemap at exposure 1.0, with glow, fog and adjustments off.

**The normal-map check.** If a material uses a normal map, commit this check as `godot/tests/normal_map_check.gd` before the audit. A real tangent-space normal map encodes the slopes of a height surface, so its slope field is curl-free: its two mixed partial derivatives agree. A generated imitation has no surface behind it, so its two terms are unrelated. A map in the wrong green convention, DirectX in Godot, is curl-free only under the other convention, so its terms cancel the wrong way. The ratio lands near 0 for a real map in the right convention, near 1 when there is no surface behind it, and near 2 when the surface is real but the convention is wrong.

gdscript

``` gdscript
# ~0: slope field of a real surface in this convention.
# ~1: no surface behind it.
# ~2: real surface, other green convention.
static func curl_ratio(source: Image, directx := false, stride := 4) -> float:
    var img := source.duplicate() as Image
    if img.is_compressed():
        img.decompress()
    var s: float = -1.0 if directx else 1.0
    var curl_sq := 0.0
    var terms_sq := 0.0
    for v in range(1, img.get_height() - 1, stride):
        for u in range(1, img.get_width() - 1, stride):
            var t1 := (_dh_du(img, u, v + 1) - _dh_du(img, u, v - 1)) * 0.5
            var t2 := (_dh_dv(img, u + 1, v, s) - _dh_dv(img, u - 1, v, s)) * 0.5
            curl_sq += (t1 - t2) * (t1 - t2)
            terms_sq += t1 * t1 + t2 * t2
    return curl_sq / maxf(terms_sq, 1e-12)


static func _normal(img: Image, u: int, v: int) -> Vector3:
    var c := img.get_pixel(u, v)
    return Vector3(c.r, c.g, c.b) * 2.0 - Vector3.ONE


static func _dh_du(img: Image, u: int, v: int) -> float:
    var n := _normal(img, u, v)
    return -n.x / maxf(n.z, 0.05)


static func _dh_dv(img: Image, u: int, v: int, s: float) -> float:
    var n := _normal(img, u, v)
    return s * n.y / maxf(n.z, 0.05)
```

Calibrate it before you trust it. Run it on a Poly Haven `_nor_gl` and `_nor_dx` pair of the same material: the GL file should come out low with `directx = false` and near 2 with `directx = true`. If the results come out reversed, the sign convention is backwards; flip `s` and say so in `TEST-REPORT.md`. Very flat or heavily compressed maps drift toward 1, because 8-bit quantization noise swamps the real slopes. Set your threshold from the known-good pair, not by feel. Use a stride of 8 on 4K textures.

Know what the check cannot tell you. A normal map computed from an albedo with a Sobel filter passes, because it really is the slope field of a surface, just not one anyone modelled. Curl-free means a surface exists behind the map, not that it is the right surface.

**The audit.** Commit your hand-written work, then audit it with no changes:

text

``` text
Inspect before editing. Always run Godot through ./scripts/run-test.sh
or godot --headless --path godot --import; never add
--rendering-driver. A headless run uses a dummy renderer: it draws
nothing.

Task: audit the materials named in CHANGE-BRIEF.md, then write a
headless test that pins what you found. Do not change any .gdshader
file, material, scene or .import file in this task.

1. Read the textured shader, both ShaderMaterial resources that use it,
   the hint-experiment shader and its two materials, the .import file
   of every texture they use, and the lights and environment of the
   scenes they appear in.
2. Write godot/MATERIALS.md with:
   - one row per material: resource path, shader path, every uniform
     value it sets, and every texture it binds;
   - one row per sampler in each shader: name, hints as written in the
     source, the texture each material binds to it, and that texture's
     import settings (compress/mode, compress/normal_map,
     mipmaps/generate);
   - the lights and environment settings that change the look,
     including tonemap and exposure;
   - findings: anything that looks wrong, wasteful, unused or
     inconsistent with CHANGE-BRIEF.md, each with the evidence line;
   - attribution, using exactly the facts in CHANGE-BRIEF.md, which I
     checked myself.
3. Write godot/tests/test_materials.gd (extends SceneTree) that loads the
   scenes headlessly and asserts the tables: both materials for the
   textured shader reference the same shader path; each sampler's hints,
   read from the source text; each material's uniform values and texture
   paths; the import settings read from the .import files with
   ConfigFile; and the uniform list from get_shader_uniform_list(). For
   each normal map, preload godot/tests/normal_map_check.gd, decode the
   source file with Image.load_from_file, and print curl_ratio under
   both conventions. Print one PASS/FAIL line per check and exit 1 on
   any failure.
4. Run it with ./scripts/run-test.sh test_materials.gd 60 and show the
   real output. Say what the test cannot establish headlessly.
Do not commit.
```

Commit the audit unedited, then review it. Look up every integer enum, check format claims with `get_image().get_format()`, and delete numbers nobody measured. Commit your corrections separately.

**Fresh cache and mutation.** Verify from an empty cache: delete `godot/.godot`, reimport, and run the test.

bash

``` bash
./scripts/run-test.sh test_materials.gd 60
```

Then delete `source_color` from your colour sampler, the one property this part exists to get right. Confirm the test exits 1, then restore it.

### Step 4 — reading the language

In a scratch scene, make a `StandardMaterial3D` with an albedo texture, a normal map and a roughness texture enabled; your Step 3 textures will do. Make it unique, then use the Inspector's resource menu to convert it to a `ShaderMaterial`. Save the generated code as `godot/shaders/standard_generated.gdshader`; nothing in the game uses it. In `LANGUAGE-NOTES.md`, give the line numbers in that file for:

- `shader_type` and `render_mode`;
- the uniforms that correspond to the Inspector's albedo colour and normal-map strength;
- the albedo sampler and the normal-map sampler, with their hints;
- the lines that write `ALBEDO`, `ROUGHNESS` and `NORMAL_MAP`.

Then answer these in `LANGUAGE-NOTES.md`, in your own words, each with a line reference to one of your three shaders:

1.  What does `shader_type` decide? Answer for each type you used, citing the first line of each shader.
2.  Which processor functions did you write, and when does each run? What would change if you moved your colour line into `vertex()`, and why?
3.  Name three built-ins you read and two you wrote. Which of the ones you read are read-only?
4.  For each hint you used, does it change only the Inspector, or also the value the shader receives? Cite your hint experiment.
5.  Does `hint_range` clamp a value set from code? Cite what you observed.
6.  Which line of the generated shader makes the albedo sample as colour and the normal map as data, and what is the equivalent line in your textured shader?
7.  Your `fragment()` runs for every pixel at once. Why can't it read what the neighbouring pixel's `fragment()` is computing, and how does game state reach it instead?
8.  Name two things the Godot shading language provides that plain GLSL does not, or makes you write yourself.

The agent may check that your line references point where you say. It does not write the answers.

### What the agent is likely to get wrong

Each row happened in the runs behind Chapters 6 and 7.

| Recorded mistake | How it was caught |
|----|----|
| After a 30 fps failure, the agent rewrote its test to call the update function directly; the frame rate stopped mattering, and the summary still reported 30 and 144. | Reading the test, not the summary. |
| Uniform "type" checks were set-then-get round trips; with a semicolon deleted from the shader, all 11 still passed. | The mutation, plus a uniform-list assertion. |
| The audit misnamed an enum (`4` is `TONE_MAPPER_AGX`, not ACES), invented memory figures, and proposed a "fix" that would have mislabelled a menu. | Looking each value up. |
| An import setting written as a flat key the importer ignores; a UID typed by hand. | A failing test; a headless probe. |
| An `ORMMaterial3D` with `ao_enabled` left off passed a 100-check test that never asserted the flag. | A probe, then one assertion on the flag. |

### What must not change, and what counts as done

**Must not change:** collision, movement, input, game-state logic and timings, existing tests, objects outside your boundary, and the source model and texture files.

**Done means all of the following:**

- every specification rule has a recorded machine or human check;
- all three mutations fail their tests;
- no agent session changed `godot/shaders/`;
- every texture is credited;
- every language question has an answer with a line reference;
- the earlier suites give their baseline counts.

"Claude said it works" is not on the list.

## 3. Use It

Open the project in the Godot editor and run it. Record actual results in `TEST-REPORT.md`, with the source revision, Godot version and renderer:

| Check | Evidence to collect |
|----|----|
| Baseline | Every earlier test, before and after, with pinned frame rate and counts. |
| Shaders parse | Uniform-list assertions for both shaders, no `SHADER ERROR` line, and both shader mutations exiting 1. |
| Driver | The uniform sampled every frame at 30, 60 and 144 fps through a real event, including a retrigger: first value, last value, game-time duration. |
| Controlled values (HUMAN CHECK) | A capture per controlled value, with sampled pixels beside your predicted table; a capture with the uniform set to 2.0 from code, answering the `hint_range` question. |
| In play (HUMAN CHECK) | The state triggered by normal play several times; boundaries hold. |
| Hint experiment (HUMAN CHECK) | A capture of both quads, with sampled band values beside your predictions. |
| Interface sweep (HUMAN CHECK) | Each uniform of the textured shader at its minimum, default and maximum: what changed, and any setting that breaks the look. |
| One shader, two materials (HUMAN CHECK) | Side-by-side captures under the stated lighting. Edit one line of the shader and record that both objects change; edit one value in one material and record that only one changes. |
| Material wiring | The material test after a fresh import, and the `source_color` mutation exiting 1. |
| Texture data | The curl ratio under both conventions for every normal map and for the calibration pair. |
| Import settings | The diff of any `.import` file the editor rewrote, explained. |

For controlled values, capture in-engine rather than with your screenshot tool. OS screenshots apply display colour profiles and scaling, so the pixel at the coordinates you predicted may not be the one you measure. Bind this to a debug key in a real windowed run. It reads the rendered frame at viewport resolution, and it is real engine output, not a headless log:

gdscript

``` gdscript
func capture(driver: Node, mat: ShaderMaterial, param: StringName, value: float, path: String) -> void:
    driver.set_process(false)  # also set_physics_process(false) if the driver writes there
    mat.set_shader_parameter(param, value)
    await RenderingServer.frame_post_draw
    get_viewport().get_texture().get_image().save_png(path)
    driver.set_process(true)
```

Without `set_process(false)`, the driver overwrites your value before the frame draws. Compare one capture against an OS screenshot once, and record which you trust and why. Your prediction assumes the arithmetic happens on the values as written, which Chapter 6 reports as a reading of the source, not an observation. A difference of more than a step or two per channel is a finding: record it with the capture, then find out why.

For the textured shader, light the object as `CHANGE-BRIEF.md` says, and switch off effects you could confuse with your change, such as SSAO when you judge a roughness or normal map. Do not write "looks better" unless you compared two images. Texture detection runs only when a real editor draws the texture, so run `git status` after your first editor session.

If the editor rewrites an import setting and a test fails, updating the expectation to the value the editor wrote is a legitimate revision when it is its own commit, with the `.import` diff and the reason. Deleting the assertion is not.

Include at least one inspect-and-revise cycle driven by an observation. Do not delete a failing assertion or weaken an expected result to obtain a green report. If another person looks at your work, record their actual words; do not invent a playtester. Your own playtest is required, and no headless run replaces it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier. It pairs each code excerpt with the visible result it produces; for a shader, that result is real engine output captured on your display, never a headless log. Ask Claude Code to read the installed skill instructions and follow them. If your checkout lacks the skill, request the course-provided version.

Make **one** landscape film that:

1.  Identifies your game, the state your effect communicates, and the object given the textured shader.
2.  Answers the four questions from Your task: what a shader does, how a material differs from a shader, why a texture is information, and what the Godot shading language is. Each answer points at a line of your code.
3.  Shows the colour line in your specification, the shader and driver lines, your controlled-value captures, and the effect in play.
4.  Shows the hint experiment predicted and measured, the interface sweep, and two materials from one shader.
5.  Shows two annotated lines of the generated shader beside their equivalents in yours.
6.  Shows what the tests proved, the mutations that failed them, and what no headless run can show.
7.  States the agent mistakes you caught, what remains uncertain, one next step, the human and AI contributions, the texture sources, and the revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed editor views, scripted-input captures and held frames; never present a reconstruction as a screenshot. Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. There is no minimum runtime. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**. The film is part of the 60-point category below, not a substitute for working source.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with both shaders, the hint-experiment shader and scene, the driver, all material resources, and the used textures with their `.import` files; no `.godot` cache or credentials.
- `README.md`: project name, starting point, engine version and renderer, run instructions, controls, what this assignment added, known limitations, and the film link.
- `CLAUDE.md` as reviewed, `CHANGE-BRIEF.md`, `MATERIALS.md`, `LANGUAGE-NOTES.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`, and the texture credits file.
- Your tests, `scripts/run-test.sh`, the texture-writing script, cited logs, captures, prompts, and any `claude -p` transcript under about 1 MB (otherwise a labelled excerpt).
- The film's beat sheet, script/prompts, and evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Commit in the order the work happened, so a reviewer can see who wrote which lines: your shader, agent draft, your review, agent change, your check or fix. Use messages that say what was checked, for example `Danger tint driver + test (agent); headless checks at 30/60/144 fps; shader untouched; look checked by hand in the editor`. Tag the final submission commit **`a5`**.

## 5. Verify and submit to Canvas

Clone the `a5` tag into a fresh folder. Run `--import` once, then every test at its pinned frame rates through `scripts/run-test.sh`. Confirm the counts match `TEST-REPORT.md` and no log contains `SHADER ERROR`. A working local folder is not proof that everything was posted.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

text

``` text
Assignment: Assignment 5 - Shaders, Materials, and the Godot Shading Language
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Game-source revision shown in the film:
Godot version, renderer, and operating system:
Game state the shader from code communicates:
3D object and scene given the textured shader:
Texture sources and licences (or model, version, and terms):
Final film URL and filename:
Final film SHA-256:
Summary of my work:
Known limitations:
Changed games since Assignment 2 (yes/no; if yes, FRICTIONAL.md entry):
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and the film must refer to the same submitted work; identify later changes as a new revision.

## Rubric — 100 points

| Component                              | Points  |
|----------------------------------------|---------|
| Implementation and explanation         | 60      |
| Frictional — honest log                | 10      |
| GitHub version posting matching Canvas | 10      |
| Relative Quartile                      | 20      |
| **Total**                              | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|----|----|
| Specification and context: a specification with the colour line, the uniform table, measurable rules (including retrigger, tolerance and time scale), boundaries and an evidence split, committed before any shader (4); pixel predictions and hint-experiment predictions computed by hand (2); `CLAUDE.md` with a file reference for every fact, the specification imported, and your corrections committed apart from the agent's draft (2). | 8 |
| Shader from code: a hand-written shader that meets its specification, with a colour line that matches the spec (5); driven from game state, frame-rate independent, retriggering as specified, boundaries kept (4); controlled-value captures against your predictions, with differences explained (3). | 12 |
| Textured shader and materials: colour and data textures with correct hints, explicit import settings, and recorded provenance and attribution (4); a parameter interface with types, hints, defaults and groups, and the sweep recorded (4); one shader and two materials demonstrated, including the shader-edit and material-edit observation (3); the hint experiment predicted, measured and explained (3). | 14 |
| The language: the generated shader annotated accurately (4); language notes that are accurate, in your own words, and line-referenced (6). | 10 |
| Verification: the parse and rename mutations both fail the shader check (3); the driver sampled at three pinned frame rates through real events (2); a material test that passes after a fresh import and fails when `source_color` is removed (3). | 8 |
| Brutalist explainer: accurate explanation of the four ideas and both shaders (3); excerpts followed by real captured engine output (3); test limits, contributions and texture sources stated, in a readable, audible final film using the required workflow (2). | 8 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing headless suite establishes that the shaders parse, their uniforms are declared and driven as specified, and the materials are wired as audited. It does not establish that anything looks right, so a missing human check loses that check's points whatever the logs say.

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

Use `SOURCES.md` to credit your starting point, every texture source and generative model with its terms, collaborators, and tools. Describe what AI contributed to the driver, tests, audit, script, and narration. Describe what you personally wrote, specified, checked, changed, or rejected.

You should be able to say, in your own words and pointing at a line of your own code, what a shader does, how a material differs from a shader, why a texture is information rather than a picture, and what the Godot shading language is. The instructor or a TA may ask you to:

- change one line of your shader and predict the result before you look;
- set your uniform in the running game and predict a named pixel's colour;
- explain why a texture is sampled as data, and point to the line that makes it so.

Inability to explain reduces points under the relevant criteria. Presenting agent-written shader code as hand-written misrepresents authorship. Recording a human check you did not perform misrepresents verification. Misrepresenting authorship, provenance, or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw) and the course/university policies.
