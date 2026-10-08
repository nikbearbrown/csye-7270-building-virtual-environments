# Module 6 — Shader foundations

CSYE 7270 · Fall 2026 · Week 6

## Executive summary

A shader is a small program that the graphics processor runs for every corner or pixel of whatever you draw. This module explains how Godot 4.7.2 turns shader text into something the GPU runs, how a game script hands the shader its values, and what a headless run (Godot with no window, the only kind an agent can do here) can and cannot see. You write a specification of one visible effect first, then direct Claude Code to build it: a failure flash that tints the character Clawd toward a dark ink colour when a run fails and fades back before the retry. The build's checks prove that the shader parses, that its two settings exist with the right types, and that the game's code drives the flash correctly at 30, 60 and 144 frames per second. They do not prove that the flash looks right. That is a set of human checks you perform in the editor, against colours you predicted in advance.

## The question

In the run behind this module, Claude Code wrote a shader, a GDScript driver and a new test. It ran the test at 30 and 144 frames per second, reported "11 checks, 0 failures, no `SHADER ERROR` lines", and listed what the test could not prove.

Then the shader was broken on purpose: one semicolon deleted. The agent's test still passed all 11 checks with exit code 0. So did the project's 25 mechanics checks. The only sign of trouble was one log line, `SHADER ERROR: Expected a ';'.`, which nothing was reading.

So: **when an agent says a shader effect is done, what could it possibly have checked, and what would you have to check yourself?** Answering takes two pieces of machinery (how Godot compiles a shader, and what a headless run contains) and one habit: write down the visible effect and its boundaries before the agent writes code.

## The ideas

### A shader runs many times at once

A **shader** runs on the graphics processor, not the CPU, once per vertex, once per pixel the geometry covers, and optionally once per pixel per light, all in parallel. Godot's shading language is based on GLSL but simplified; see [Introduction to shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html). Godot 4.7 has six shader types; this module uses `canvas_item` (2D), Module 7 builds on `spatial` (3D), and Module 9 uses `particles`.

Three consequences shape everything else. **A pixel cannot ask its neighbour what colour it became**, so effects that need other pixels read a texture that was already drawn. **Values arrive in three ways:** from the geometry, from textures, and from **uniforms**, which the CPU sets once per draw and every invocation sees identically; a uniform is the contract between your GDScript and your shader. And **there is no `print`**: a shader's only output is the colour it writes, so seeing that output means rendering it.

### Inside a canvas_item shader

The [CanvasItem shader reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) defines the built-ins you will touch. `vertex()` moves geometry, `fragment()` colours each covered pixel, and `light()` runs per pixel per light. In `fragment()`, `COLOR` arrives holding the vertex colour multiplied by the texture colour, and whatever you leave in it is drawn. `TIME` is global engine time, not time since your event.

The `COLOR` definition decides a real bug. Clawd is not a sprite: `clawd_art.gd` paints him with `draw_rect()` calls, one colour per rectangle, so his colours live in the vertex colour. A shader that starts from `texture(TEXTURE, UV)`, the line in most sprite tutorials, throws that colour away; one that starts from `COLOR` keeps it. Both lines parse, and both look reasonable.

Two more traps from older tutorials. Godot 4 removed `SCREEN_TEXTURE`; you declare a sampler uniform with `hint_screen_texture` instead, as the [screen-reading guide](https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html) shows, and an agent trained on Godot 3 code will write the old name. And a `light()` function replaces Godot's built-in lighting for that item even when it is empty, so an empty `light()` is not neutral.

### Uniforms: the contract with GDScript

A uniform declares a value the CPU supplies: a type, an optional hint after a colon, an optional default. This is the shader the agent wrote for this module's task.

```glsl
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 flash_color : source_color = vec4(0.14510, 0.20784, 0.29020, 1.0);
```

Hints describe a value; they do not enforce it. `hint_range` gives the Inspector a slider, but in a headless run on 4.7.2, setting `flash_amount` to `7.0` from code stored `7.0`. `source_color` marks a colour for correct decoding; Module 7 explains why that matters.

A `Shader` is the program. A `ShaderMaterial` holds the values, and `set_shader_parameter()` sets one; the [ShaderMaterial reference](https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html) warns that a change affects every node sharing that material.

```gdscript
var mat := ShaderMaterial.new()
mat.shader = preload("res://features/player/clawd_flash.gdshader")
material = mat
mat.set_shader_parameter("flash_amount", 1.0)
```

The parameter name is a case-sensitive string and nothing checks it at parse time. A typo is a silent no-op: the uniform keeps its default and the effect never appears.

### VisualShader is the same language underneath

Godot's node-graph editor, [VisualShader](https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html), converts the graph to shader text behind the scenes, and it does not expose every feature of the script language. In a headless run on 4.7.2, a VisualShader built in code returned readable shader text from its `.code` property. An agent cannot look at your graph, but it can read, diff and test the code the graph becomes, which is easier to review than a web of nodes and connections.

### What Godot checks, and what a headless run can see

Godot's own shader compiler reads the `.gdshader` text, checks syntax, types and which built-ins exist where, and generates code for the active renderer. The GPU driver compiles that code again, and then it runs. The experiment in [`HEADLESS-SHADER-FINDINGS.md`](../../examples/06-shader-foundations/HEADLESS-SHADER-FINDINGS.md) measured what a `--headless` run does with it:

| Question | Headless answer |
|---|---|
| Does the shader parse and type-check? | Yes. A `SHADER ERROR` line, then `Shader compilation failed`, goes to stderr. |
| When does the error appear? | On first use, such as assigning the shader to a material, not on `load()`. |
| Does a broken shader fail the run? | No. Exit code 0. |
| Which uniforms exist, with which types and hints? | Yes, from `Shader.get_shader_uniform_list()`; a shader that failed to parse returns an empty list. |
| What are the uniform defaults? | Not through the engine. Read the source text. |
| Does the GPU compile succeed, and what colour does a pixel become? | No. No GPU driver, no pixel readback. |

Two traps came out of the same experiment. `RenderingServer.get_current_rendering_method()` still says `forward_plus` under `--headless`, because it reports configuration, not what is running. And `--display-driver headless` alone, or `--headless` plus `--rendering-driver`, fell back to the windowed macOS display server. Use `--headless` exactly as written and never add `--rendering-driver`.

So the honest split is this. **Machine evidence:** the shader parses (a non-empty uniform list and no `SHADER ERROR` line), the uniforms have the right names and types, and the game code sets them correctly at the right moments. **Human evidence:** what the pixels look like.

### CLAUDE.md and the effect spec

Claude Code reads `CLAUDE.md` at the start of every session, and its documentation advises keeping it specific and short ([How Claude remembers your project](https://code.claude.com/docs/en/memory)). Walker projects already carry an `AGENTS.md`, and by default a `CLAUDE.md` in the directory means Claude reads that file only unless it imports `AGENTS.md`, so make its first line `@AGENTS.md`. For shader work, `CLAUDE.md` should hold what the agent cannot discover quickly or will get wrong: the renderer, how the thing is drawn, where the driving state lives, the exact test commands, what a headless run can see, and the effect specification.

A useful effect spec has three parts. **Observable rules** that can be measured: write that the flash is 1.0 on the first frame of the failure and lasts the same wall-clock time at 30, 60 and 144 fps, not "a nice quick flash". **Boundaries**: what must not change, such as collision, movement, input and the 0.55 s retry. And **the evidence split**: which rules a headless test proves, and which you will check by eye, and how.

Frame rates belong in rule 1 because the game ticks physics 60 times a second but draws as fast as the display allows, so an effect counted in frames lasts twice as long at 30 fps as at 60. Module 8 is built on that fact.

## The Walker example: walker-jumpman-clawd

[`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd) is Professor Bear's semester-long example for this course, and it is public. Its `SOURCES.md` records that it forks the starter [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman) and ports Clawd's 18 animations as drawing-only GDScript, and it says public availability is not a licence grant for inherited work whose licence is unestablished. Clone it to learn from; do not redistribute it as your own. This module starts from commit `382f2baa5ee5e90a5afc083d82a5337845157f34`.

| File | What it tells you |
|---|---|
| `godot/project.godot` | The Compatibility renderer (`gl_compatibility`), not Forward+. Physics ticks at 60 Hz. |
| `godot/features/player/clawd_art.gd` | Clawd is drawn by `draw_rect()` calls with `BODY := Color("dd775b")` and `EYE := Color.BLACK`. No texture anywhere. |
| `godot/features/player/player.gd` | `_draw()` calls `ClawdArt.paint()`. The collider is a separate 18 × 28 rectangle. |
| `godot/game/session.gd` | The state machine. A failure sets `retry_remaining = 0.55`; `_physics_process` counts it down and restarts. R restarts directly. |
| `godot/tests/` | `test_game.gd` (mechanics), `test_keyboard.gd` (real key events), `test_clawd.gd` (animation parity) |

A baseline run on 27 September 2026 with `--fixed-fps 60` passed 25 mechanics checks and 9 keyboard checks, and `test_clawd.gd` reported 1,950 checks and 0 failures over 162 animation samples. The repository's own `FRICTIONAL.md` says this establishes sampled parity, not that every frame is right, and that the wide Clawd art needs human inspection against the collision box. None of its tests draws a pixel.

The other Walker build for this week, [`walker-compute-post-shader`](https://github.com/nikbearbrown/walker-compute-post-shader) (an adaptation of Godot's `compute/post_shader` demo, upstream MIT licence kept), is a GLSL compute shader run as a `CompositorEffect` after the 3D scene renders. Its `VERIFICATION.md` models how to state a boundary: ten headless checks pass and the shader imports to 2112 SPIR-V bytes, but compute dispatch and actual image changes remain unverified because the run has no RenderingDevice. Godot's [compute shader tutorial](https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html) says such shaders need the Forward+ or Mobile renderer, so Clawd's Compatibility project cannot use one.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Answer these in writing before you open Claude Code, and keep the answers.

1. Clawd is drawn with `draw_rect()` and has no texture. In a `canvas_item` `fragment()`, which built-in carries his terracotta body colour: `COLOR` or `texture(TEXTURE, UV)`? What would the other one give you?
2. The level background is `#f6f3ec`. White against it has a contrast ratio of about 1.11 to 1; the level ink `#25354a` has about 11.23 to 1. What happens to a white flash at full strength?
3. If the fade is driven by counting 33 frames, how long does it last at 30, 60 and 144 fps? The retry always comes 0.55 s after the failure.
4. Of the eight rules in the spec below, which can a headless test prove, and which need your eyes?

### 2. Build It

Get the exact starting point.

```bash
git clone https://github.com/nikbearbrown/walker-jumpman-clawd.git
```

```bash
cd walker-jumpman-clawd
```

```bash
git checkout -b ch06-failure-flash 382f2baa5ee5e90a5afc083d82a5337845157f34
```

```bash
godot --headless --path godot --import
```

Run the baseline so you know what "unchanged" looks like. Every frame-counted test gets a pinned `--fixed-fps`, and every test command is wrapped in `timeout 120`, because a GDScript error before `quit()` leaves headless Godot running. On macOS, `brew install coreutils` provides `timeout`.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_clawd.gd --fixed-fps 60
```

**Step 1: project context and the spec.** The spec block is yours; the agent copies it. The agent's job is to fill in project facts from the files, each with a reference. Paste this into Claude Code:

```text
You are working in a scratch copy of walker-jumpman-clawd (Godot 4.7.2,
GDScript, project in godot/). Do not change any file except the one you
create: CLAUDE.md at the repository root.

Read AGENTS.md, README.md, CHANGE-BRIEF.md, godot/project.godot,
godot/game/session.gd, godot/features/player/player.gd,
godot/features/player/clawd_art.gd and the test scripts in godot/tests/.

Write CLAUDE.md, under 120 lines, in this order:
1. The first line is exactly: @AGENTS.md
2. "Project context": engine version, renderer, main scene, how Clawd is
   drawn, which script owns the session state machine and the retry
   countdown, Clawd's collision shape, and the exact headless test commands.
   Give a file reference for every fact. Do not guess.
3. "Effect specification": copy the block between SPEC BEGIN and SPEC END
   below word for word.
4. "Out of scope": what this change must not touch, in your own words,
   consistent with the spec.
5. "Unconfirmed": anything you could not confirm from the files.

Do not write a shader and do not edit any script. Stop after CLAUDE.md.

SPEC BEGIN
Failure flash (Chapter 6)
Visible effect: when a run fails (spikes or a fall), Clawd is tinted toward a
flash color, then fades back to normal by the moment the retry happens.
1. One float uniform, flash_amount, 0.0 to 1.0, drives the effect. It is 1.0
   on the first frame of the failure and reaches 0.0 when the retry starts.
   The fade is linear in time and lasts the same wall-clock time at 30, 60
   and 144 frames per second.
2. Pressing R during the failure ends the flash at once. In every state
   except the failure, flash_amount is 0.0.
3. A second uniform, flash_color, is a color with default #25354a (the
   level's ink). Not white: the background is #f6f3ec, and white against it
   has a contrast ratio of about 1.1 to 1.
4. At flash_amount 0.0 Clawd looks exactly as before: same body color, same
   black eyes, same transparent surroundings. At 1.0 every visible pixel of
   Clawd is flash_color; transparent pixels stay transparent.
5. Only Clawd changes. The level, background, HUD and gallery do not.
6. No change to collision, movement, input, the session state machine, the
   0.55 s retry delay, or any existing test's expectations. Presentation
   code may read session state; it never writes it.
7. It must work in this project's renderer.
8. Evidence: a new headless test proves the shader is accepted by Godot's
   shader parser in a headless run, the two uniforms exist with the right
   types, and flash_amount obeys rules 1 and 2 at 30 and 144 fps. How it
   looks is a human check.
SPEC END
```

To run it non-interactively with scoped tools and a kept transcript, save the prompt as `prompt-1.txt` and run:

```bash
claude -p "$(cat prompt-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Glob,Grep,Bash(git:*),Bash(ls:*)" --max-turns 40 --output-format stream-json --verbose > session-1.jsonl
```

**Review what it wrote before you build on it.** This is a human step, and in the run it found real errors. Check every file reference against the file, delete anything listed as a test that is not a test, correct any "Unconfirmed" item that claims a headless test can verify a look, and add the headless facts for your machine. The corrected `CLAUDE.md` is in [the example folder](../../examples/06-shader-foundations/files/CLAUDE.md); its "Headless facts" block is four lines you can reuse. Commit the reviewed file on its own, so the next diff contains only the effect.

**Step 2: the build.** Paste this into Claude Code:

```text
Read CLAUDE.md first. Its effect specification is the contract for this
change; its headless facts describe what a test on this machine can observe.

Implement the failure flash with the smallest change that meets the spec:
- a canvas_item shader file for Clawd,
- the code that gives Clawd a ShaderMaterial with that shader,
- the code that sets flash_amount from session state each frame,
- a new headless test, godot/tests/test_flash.gd.

Rules:
- Do not edit the existing tests or change their expectations.
- Run the three existing test commands from CLAUDE.md, then your new test at
  --fixed-fps 30 and at --fixed-fps 144. Show the real output, including any
  SHADER ERROR lines.
- Say exactly what your test proves and what it cannot prove in a headless
  run, and list the human checks needed to judge the look.
- Do not commit.
```

```bash
claude -p "$(cat prompt-2.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot --headless:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose > session-2.jsonl
```

The Godot permission is `Bash(godot --headless:*)`, not `Bash(godot:*)`. If your Claude Code has user-level skills installed, also pass `--disallowedTools "Skill"` so the session cannot hand the task to one. The agent can run tests but cannot open a window.

**Codex difference** (documented, not run for this module). Codex reads this repository's `AGENTS.md` automatically but not `CLAUDE.md`. Either append your spec block to `AGENTS.md`, or start the build prompt with "Read CLAUDE.md first". Run Codex non-interactively with a writable sandbox and closed stdin:

```bash
codex exec -s workspace-write "$(cat prompt-2.txt)" < /dev/null
```

### 3. Use It

Now look, because nothing else can. Open `godot/project.godot` in the Godot 4.7.2 editor and press F5. Every item below is a **HUMAN CHECK**.

1. **Before any failure.** HUMAN CHECK: Clawd should look as in the baseline, with a terracotta body, black eyes and no box around him. If he is white or a solid block, the shader is reading the wrong input.
2. **A failure.** HUMAN CHECK: walk into the red spikes or fall into a gap. Clawd should turn dark ink at once and fade back over about half a second, and the retry should restore his colours. Repeat; the look should not vary.
3. **R mid-failure.** HUMAN CHECK: fail, then press R at once. The tint should vanish on the retry, not linger.
4. **Boundaries.** HUMAN CHECK: during a flash, watch the platforms, spikes, labels and HUD. Nothing but Clawd should change. The gallery scene paints on its own node, not the Player, so it should be unaffected.
5. **Controlled inputs.** HUMAN CHECK: Godot's [debugging overview](https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html) says the Remote scene tree lets you inspect and change a running project's nodes. Pause the game, select the Player node there, and set `flash_amount` to 0.0, 0.5 and 1.0 in its material. Screenshot each value and sample the body and one eye with a colour picker.

| `flash_amount` | Body (from `#dd775b`) | Eye (from `#000000`) |
|---|---|---|
| 0.0 | `#dd775b` (221, 119, 91) | `#000000` |
| 0.5 | about (129, 86, 82 to 83) | about (18 to 19, 26 to 27, 37) |
| 1.0 | `#25354a` (37, 53, 74) | `#25354a` |

These predictions assume the mix happens on the colour values as written. That comes from reading the 4.7.2 source (the Compatibility renderer does no sRGB-to-linear conversion on canvas uniforms), not from observing a pixel. If your screenshot disagrees by more than a step or two per channel, that is a finding; record it with the screenshot.

### 4. Ship It

- **Commit.** Commit the effect separately from the reviewed `CLAUDE.md`, with a message that says what was checked, for example `Failure flash (shader + driver + test); headless checks at 30/60/144 fps; look checked by hand in the editor`. Keep your verification script in its own commit.
- **FRICTIONAL entry.** Record, in your own words and with the real date, who did what (you wrote the spec and reviewed `CLAUDE.md`; the agent wrote the shader, driver and test), what went wrong, and what you checked by eye and saw. Never record a human check you did not perform.
- **Brutalist skill.** This is development work, so the fit is `godot-gamedev`, a film that pairs each code excerpt with the visible result it produces. The Brutalist Godot skills come from the course-provided checkout; if your copy lacks one, ask for the update. For a shader, the visible result must be real engine output captured on a display, and a headless log is not one.

### 5. Verify

Run the project's suite and confirm it is unchanged: 25, 9 and 1,950 checks, and no `SHADER ERROR` lines. One command is shown; run the other two baseline commands from Build It the same way.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

Then run your own check, not the agent's, at three frame rates. The run's [`verify_flash.gd`](../../examples/06-shader-foundations/tests/verify_flash.gd) is in the example folder; copy it to `godot/tests/`.

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
```

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 144
```

Then prove your check can fail. Delete one semicolon from the shader, rerun, and confirm it exits 1. Restore the file.

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 60
```

**What a pass proves:** Godot's shader compiler accepted the shader (intact uniform list, no `SHADER ERROR` line); the uniforms have the types, hint and default the spec names; and in the real game loop, with a real fall and a real R key event, the value the shader receives follows the spec at three frame rates.

**What it does not prove:** that Clawd is tinted at all in the Compatibility renderer, that his colours at 0.0 are unchanged, that the level is untouched, or that the flash reads well. Those are the human checks in step 3.

## What the agents got wrong

This record is from 27 September 2026, run with Claude Code 2.1.150 (default model `claude-sonnet-4-6`). Its shader was right: it started from `COLOR`, mixed toward `flash_color` and left alpha alone. The mistakes were around it.

**The `CLAUDE.md` draft cited the wrong lines and made a false claim.** It gave wrong `project.godot` line numbers, credited the patch version to a file that only says `"4.7"`, and listed a script that writes a build manifest as a headless test command. Under "Unconfirmed" it said the new test would settle whether the material tints a `draw_rect()` drawing, which no headless test can do. Checking each reference against the file caught all four.

**The test stopped measuring frame rate.** Its first version failed at 30 fps by exactly one frame (0.0606). The agent's fix was to stop running frames: the final test calls `_update_flash()` directly after setting the countdown by hand. That passes at any rate and makes `--fixed-fps` irrelevant, so rule 8's "at 30 and 144 fps" is no longer measured, though the summary still reports both runs. Reading the test, not the summary, caught it.

**The shader tests could not see a broken shader.** With the semicolon removed, the agent's test still reported 11 passing checks. Its uniform "type" checks were set-then-get round trips, and a `ShaderMaterial` round-trips a parameter whether or not the shader parsed. A mutation (break it on purpose, rerun) caught this, and so did the uniform-list check in `verify_flash.gd`, which exited 1 with three failures.

## If you know Unity or Unreal

*Unity and Unreal were not run for this module; this comparison comes from their official documentation, checked on 27 September 2026.*

| Godot 4.7 | Unity 6.6 | Unreal Engine 5.8 |
|---|---|---|
| `.gdshader` text, `shader_type canvas_item` | ShaderLab with HLSL blocks, or Shader Graph | Material asset (`.uasset`) in the Material Editor |
| `uniform` with a hint | `Properties` entry such as `Range(0.0, 1.0)` | Material parameter (Scalar, Vector, Texture) |
| `ShaderMaterial.set_shader_parameter()` | `Material.SetFloat()`, or `MaterialPropertyBlock` | Material Instance Dynamic, Set Scalar Parameter Value |
| VisualShader | Shader Graph | Material Editor graph; the Custom node holds hand-written HLSL |
| `--headless` | `-batchmode`, with `-nographics` for no GPU | `-nullrhi` |
| `--script res://tests/…` | `-runTests` (Unity Test Framework) | `-ExecCmds="Automation RunTest …;Quit"` |

The biggest difference for an agent workflow is what it can read. An agent can diff a `.gdshader` and Unity's default text-serialized assets, but not an Unreal `.uasset` material graph, which needs the editor's Python API or C++. All three share the headless boundary: no-GPU runs check logic, not pixels. The [chapter](../../chapters/06-shader-foundations.md) has the full comparison.

## Practice assessment (ungraded)

Answer these in your own words, then take the Canvas practice quiz for this module. Do not paste Claude's explanation as proof of your understanding.

1. Use the semicolon experiment to explain why exit code 0 and a passing test do not show that a shader compiled. Name two signals that do.
2. Clawd is drawn with `draw_rect()`. Which built-in carries his colour, what would `texture(TEXTURE, UV)` give instead, and why could no headless check tell you?
3. Sort the spec's eight rules into "a headless test can prove this" and "only a person can check this", and defend one rule that could go either way.
4. A call to `set_shader_parameter()` misspells the uniform name. What does Godot report, and what would a test assert to catch it?
5. Write the spec rule that stops the next agent satisfying rule 8 by calling `_update_flash()` directly.

## The next step

This module feeds Assignment 5, "A Shader and a Material That Say Something About Your Game". It covers Modules 6 and 7, opens in Module 6 and is due about Day 50, and nothing in this lesson is graded by itself. Module 7 moves from a 2D shader you write to the textures and materials a 3D model arrives with. Read the companion chapter, [Chapter 6 — Shader Foundations](../../chapters/06-shader-foundations.md), for the full run, the agent's transcripts and the Unity and Unreal comparison in detail.
