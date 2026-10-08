# Chapter 6 — Shader Foundations

## Executive summary

This chapter covers what a shader is in Godot 4.7.2, how Godot turns the text you write into something the GPU runs, and what "done" can honestly mean for a visual effect that an agent built. You read it because a shader is the part of a game where the gap between "it compiles" and "it looks right" is widest, and where a coding agent's confident summary is least connected to anything it could observe.

The hands-on task has two steps:

1. **Write the spec.** Before any code exists, you write a specification of one visible effect and its boundaries into the project's `CLAUDE.md`.
2. **Build it.** You then direct Claude Code to build that effect in `walker-jumpman-clawd`: a failure flash that tints Clawd toward the level's ink colour when a run fails, and fades back before the retry.

The build proves four things with machine evidence:

- The shader passes Godot's shader parser.
- The uniforms exist with the right types.
- The gameplay code drives the flash correctly at 30, 60 and 144 frames per second.
- The retry key cancels the flash.

It does not prove that the flash looks right. Nothing in a headless run can, and the chapter shows why by experiment. The look is a check you perform in the editor, against colours predicted in advance.

## The question

In the worked run for this chapter, Claude Code wrote the shader, a driver in GDScript, and a new test. It ran the test at 30 and 144 frames per second, reported "11 checks, 0 failures, no `SHADER ERROR` lines", and listed what the test could not prove. It was a careful, well-organised piece of work.

Then the shader was broken on purpose: one semicolon deleted. The agent's test still passed, all 11 checks, exit code 0. So did the project's 25 mechanics checks. The only sign of trouble was one line in the log, `SHADER ERROR: Expected a ';'.`, which nothing was reading.

That is this chapter's question. **When an agent says a shader effect is done, what could it possibly have checked, and what would you have to check yourself?**

Answering it takes two pieces of machinery: how Godot compiles and runs a shader, and what a headless run actually contains. It also takes a discipline the syllabus names for this week: write down the visible effect and its boundaries *before* the agent writes code. Once that is written, "done" means "meets these rules". You know in advance which rules a machine can check and which only your eyes can.

## Ideas you need

### A shader is a small program the GPU runs many times at once

A **shader** is a program that runs on the graphics processor, not the CPU. The CPU hands the GPU a batch of geometry and some settings, and the GPU runs your program over and over in parallel:

- once per vertex (to decide where each corner of the geometry lands),
- once per pixel the geometry covers (to decide that pixel's colour),
- and, optionally, once per pixel per light.

Godot's own introduction describes its language as "based on the popular OpenGL Shading Language (GLSL) but simplified" ([Introduction to shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html)). The old version of this course taught shaders through CgFX and HLSL in NVIDIA's shader library and through ShaderToy. The ideas carry over; the dialect changes.

Three consequences of "runs many times at once" shape everything else:

1. **A pixel cannot ask its neighbour what colour it became.** Each invocation runs independently. Effects that need other pixels (blur, outlines of the whole screen) read a texture that was *already drawn*.
2. **Values arrive in only three ways.** They come from the geometry (per vertex), from textures, or from **uniforms**: values the CPU sets once for a whole draw and that every invocation sees the same. A uniform is the contract between your GDScript and your shader.
3. **There is no `print`.** A shader cannot log. The only output is the colour it writes, and seeing that output means rendering it.

### Shader types and processor functions

Every Godot shader starts with a `shader_type` line that says what the program draws. Godot 4.7 has six types. The documentation lists them, and the Godot 4.7.2 binary used for this book accepted all six in a headless run (modes 0–5).

| `shader_type` | Draws | Processor functions you can write |
|---|---|---|
| `spatial` | 3D meshes | `vertex()`, `fragment()`, `light()` |
| `canvas_item` | 2D: sprites, shapes, UI | `vertex()`, `fragment()`, `light()` |
| `particles` | computes per-particle data (does not draw) | `start()`, `process()` |
| `sky` | the sky's radiance cubemap | `sky()` |
| `fog` | volumetric fog froxels | `fog()` |
| `texture_blit` | blits into a `DrawableTexture2D` | (new in 4.7; see its reference page) |

The processor functions, in Godot's words ([Introduction to shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html)):

- `vertex()` "runs over all the vertices in the mesh and sets their positions".
- `fragment()` "runs for every pixel covered by the mesh".
- `light()` "runs for every pixel and for every light".

Chapter 9 uses `particles`, and Chapter 7 sits on top of `spatial`. This chapter stays in `canvas_item`, because the Walker example is 2D.

### Inside a `canvas_item` shader

The [CanvasItem shader reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) defines the built-ins you will actually touch:

- **`VERTEX`** in `vertex()` is "presented in local space (pixel coordinates, relative to the Node2D's origin)". Move it and the drawing moves.
- **`UV`** is the texture coordinate from the vertex function.
- **`TEXTURE`** is the "Default 2D texture" the item was drawn with.
- **`COLOR`** in `fragment()` is the one that matters most here. The reference defines it as "COLOR from the vertex() function multiplied by the TEXTURE color. Also output color value." It arrives holding the combined colour of the drawing, and whatever you leave in it is what gets drawn.
- **`TIME`** is "Global time since the engine has started, in seconds. It repeats after every 3,600 seconds." It is not the time since *your* event. Chapter 8 returns to that.
- **`SCREEN_UV`** is the screen coordinate of the current pixel.

The `COLOR` definition decides a real bug. Clawd in `walker-jumpman-clawd` is not a sprite. `clawd_art.gd` paints him with `draw_rect()` calls, one colour per rectangle (`BODY := Color("dd775b")`, `EYE := Color.BLACK`), so his colours live in the *vertex colour*. A shader that starts from `texture(TEXTURE, UV)`, the line in most sprite tutorials, throws the vertex colour away. A shader that starts from `COLOR` keeps it. The two lines look equally reasonable, and both parse.

Two built-ins from older tutorials no longer exist. Godot 4 removed `SCREEN_TEXTURE`. You now declare a sampler uniform with `hint_screen_texture`, and the screen-reading guide gives the form `uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;` ([Screen-reading shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html)). The screen texture holds "the already rendered contents of the screen". In 2D, "if shaders that use hint_screen_texture overlap, the second one will not use the result of the first one." An agent trained on Godot 3 code will write `SCREEN_TEXTURE`. Godot 4.7.2 rejects it with a helpful message: `SCREEN_TEXTURE has been removed in favor of using hint_screen_texture with a uniform.`

`light()` has a trap too: "If you define a light() function it will replace the built-in light function, even if your light function is empty." An empty `light()` is not neutral. It replaces Godot's lighting for that item with nothing.

Render modes go on the line after `shader_type` and change how Godot applies the result. For `canvas_item`, `blend_mix` ("alpha is transparency") is the default. `blend_premul_alpha`, `unshaded` and `light_only` are the others you are likely to meet.

### Uniforms and hints: the contract with GDScript

A **uniform** declares a value the CPU supplies. The [shading language reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html) shows the pattern: a type, an optional hint after a colon, an optional default.

```glsl
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 flash_color : source_color = vec4(0.14510, 0.20784, 0.29020, 1.0);
```

- **Hints** tell the editor, and sometimes the renderer, what the value means.
  - `hint_range(min, max)` gives the Inspector a slider. In a headless run on 4.7.2, setting `flash_amount` to `7.0` from code stored `7.0`. The hint shapes the editor; it does not clamp your code.
  - `source_color` marks a colour. The reference says any texture "which contains sRGB color data requires a `source_color` hint in order to be correctly sampled", because "Godot renders in linear color space, but some textures contain sRGB color data." Chapter 7 is about that sentence.
  - `hint_normal` marks a normal map.
- **Defaults** are what the shader uses until someone sets a value.
- **Setting a value** happens on a material, not on the shader. A `Shader` is the program. A `ShaderMaterial` is "a material that uses a custom Shader program", and it holds the parameter values. `set_shader_parameter()` "changes the value set for this material". The [ShaderMaterial reference](https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html) warns that the change affects every node sharing that material, and points to per-instance uniforms or a duplicated material when you need per-node values. In GDScript:

```gdscript
var mat := ShaderMaterial.new()
mat.shader = preload("res://features/player/clawd_flash.gdshader")
material = mat
mat.set_shader_parameter("flash_amount", 1.0)
```

The parameter name is a string, case-sensitive, and nothing checks it at parse time. A typo is a silent no-op: the uniform keeps its default and the effect never appears.

### VisualShader: the node graph is the same language underneath

Godot's node-graph editor, **VisualShader**, is the equivalent of Unity's Shader Graph and Unreal's Material Editor. The [VisualShader guide](https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html) says the graph "is converted to a script shader behind the scene, and you can see this code by pressing the last button in the toolbar". It also warns that visual shaders "do not expose all features of the shader script".

That conversion matters for agent work. In a headless run on 4.7.2, a VisualShader built in code (a float parameter mixed into a colour constant) returned readable shader text from its `.code` property. The generated code declared `uniform float flash_amount;` and ended with `COLOR.rgb = n_out4p0;`. An agent cannot look at your graph, but it can read, diff and test the code the graph becomes. The graph itself is stored as a resource of nodes and connections, and reviewing that is harder than reviewing ten lines of shader text.

### How Godot compiles your shader, and what a headless run can see

Here is the chain from text to pixels. Godot's own shader compiler reads the `.gdshader` text, checks it (syntax, types, which built-ins exist in which function), and generates code for the active renderer. That code is compiled again for the GPU and then runs. Errors can happen at the first stage or the later ones. The look can be wrong even when both succeed.

The course runs Godot only with `--headless`, and Godot's command-line reference defines that flag as headless mode "(`--display-driver headless --audio-driver Dummy`). Useful for servers and with `--script`" ([Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)). What does such a run know about shaders? The documentation does not say, so this book measured it before any chapter was written. The full record, with real outputs, is in [`../examples/06-shader-foundations/HEADLESS-SHADER-FINDINGS.md`](../examples/06-shader-foundations/HEADLESS-SHADER-FINDINGS.md). What it found:

| What you want to know | Can headless show it? | How it appears |
|---|---|---|
| Does the shader parse and type-check? | **Yes.** The dummy renderer calls Godot's `ShaderCompiler` (`servers/rendering/dummy/storage/material_storage.cpp` at the 4.7.2 commit). | `SHADER ERROR: …` then `ERROR: Shader compilation failed.` on stderr |
| When does the error appear? | On **first use**, not on `load()` | `load()` of a broken shader succeeds. The error fires at `mat.shader = sh` or at `get_shader_uniform_list()`. |
| Does a broken shader fail the run? | **No** | Exit code 0, including a scene run with `--quit-after 10` |
| Which uniforms exist, with which types and hints? | **Yes** | `Shader.get_shader_uniform_list()`. A shader that failed to parse returns `[]`. |
| What are the uniforms' defaults? | Not through the engine | `get_shader_parameter()` and `RenderingServer.shader_get_parameter_default()` both returned `null`. Read the source text. |
| Does the renderer-specific GPU compile succeed? | No | There is no GPU driver in a headless run. |
| What colour does a pixel become? | **No** | No RenderingDevice, no local RenderingDevice; a viewport texture reads back `null` |

Two traps came out of the same experiment. First, under `--headless`, `RenderingServer.get_current_rendering_method()` still returned `forward_plus` and the driver name still returned `metal`: they report configuration, not what is running. Second, and worse, `--display-driver headless` on its own, and `--headless --rendering-driver metal`, both reported `DisplayServer` "macOS" and a real Metal GPU. The engine fell back to the windowed display server. Use `--headless` exactly as written and never add `--rendering-driver` to it.

So the honest split is:

- **Machine evidence** (headless):
  - The shader parses: a correct, non-empty uniform list, *and* no `SHADER ERROR` line in the log.
  - The uniforms have the right names, types and hints.
  - The gameplay code sets them to the right values at the right moments.
- **Human evidence** (a display):
  - What the pixels look like.

A good spec says which is which for every rule.

### CLAUDE.md: project context the agent reads every time

Claude Code reads `CLAUDE.md` at the start of every session. Its documentation says CLAUDE.md files in the directory hierarchy above the working directory "are loaded at launch", that files can import others with `@path` syntax "with a maximum depth of four hops", and that you should "target under 200 lines per CLAUDE.md file". It also says "the more specific and concise your instructions, the more consistently Claude follows them" ([How Claude remembers your project](https://code.claude.com/docs/en/memory)).

That page also describes an interaction that matters for Walker projects, which already carry an `AGENTS.md`. Claude Code v2.1.277 and later can read `AGENTS.md` directly. But by default, once any `CLAUDE.md` exists in your directory or above, Claude reads "your `CLAUDE.md` files only", unless the `CLAUDE.md` imports `AGENTS.md`. The Claude Code used for this chapter was 2.1.150, older than that feature. Either way the fix is the same: make the first line of `CLAUDE.md` read `@AGENTS.md`, so adding project context never silently drops the project's existing rules.

Codex works the other way round. It builds its instructions from `~/.codex/AGENTS.md` and then every `AGENTS.md` from the Git root down to the working directory, "joining them with blank lines". Alternative filenames are consulted only as configured fallbacks ([Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)). A Codex session does not read your `CLAUDE.md` unless you tell it to in the prompt, or put the spec in `AGENTS.md`.

What belongs in `CLAUDE.md` for shader work is what the agent cannot discover quickly or will get wrong:

- the renderer,
- how the thing you are shading is drawn,
- where the state that drives the effect lives,
- the exact test commands,
- what a headless run on your machine can and cannot see,
- and the effect specification itself.

### Specifying a visible effect before any code exists

The syllabus asks you to "specify a visible effect and its boundaries before coding". A useful effect spec has three parts:

1. **Observable rules**, stated so they can be measured. Write "the flash is 1.0 on the first frame of the failure and 0.0 when the retry starts, and lasts the same wall-clock time at 30, 60 and 144 fps". Do not write "a nice quick flash".
2. **Boundaries**: what must not change. Write "only Clawd changes; collision, movement, input and the 0.55 s retry are untouched", not "keep it simple".
3. **The evidence split**: which rules a headless test proves, and which you will check with your eyes, and how.

Writing rule 1 with frame rates in it is not pedantry. The game ticks physics 60 times a second (`common/physics_ticks_per_second=60` in `project.godot`), but it draws as fast as the display allows. An effect counted in frames lasts twice as long at 30 fps as at 60. Chapter 8 is built on that fact.

## The Walker example: walker-jumpman-clawd

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman), [`walker-compute-post-shader`](https://github.com/nikbearbrown/walker-compute-post-shader). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

`walker-jumpman-clawd` is Professor Bear's semester-long CSYE 7270 example. It is public at [github.com/nikbearbrown/walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd). Its `SOURCES.md` records that it forks the starter `walker-jumpman` at commit `9387542ca473b0a252c43bfe6d4fd39b61f8d439` and ports Clawd's 18 animations from Brutalist's `ClaudeMascotScene.tsx` as drawing-only GDScript. The same file notes that the repository "does not add a blanket license to inherited work whose license has not been established. Public availability is not itself a license grant." Clone it to learn from; do not redistribute it as your own.

This chapter starts from commit `382f2baa5ee5e90a5afc083d82a5337845157f34`. The files that matter for a shader:

| File | What it tells you |
|---|---|
| `godot/project.godot` | `renderer/rendering_method="gl_compatibility"` (line 27): the Compatibility renderer, not Forward+. Physics ticks at 60 Hz. |
| `godot/features/player/clawd_art.gd` | Clawd is drawn by `canvas.draw_rect(…, EYE if i >= 7 else BODY)`, with `BODY := Color("dd775b")` and `EYE := Color.BLACK`. No texture anywhere. |
| `godot/features/player/player.gd` | `_draw()` calls `ClawdArt.paint(self, …)`. The collider is a separate 18 × 28 `RectangleShape2D`. |
| `godot/game/session.gd` | The state machine (`enum State { MENU, PLAYING, PAUSED, DYING, COMPLETE }`). A failure sets `retry_remaining = 0.55`; `_physics_process` counts it down and calls `restart_attempt()`. R calls `restart_attempt()` directly. |
| `godot/tests/` | `test_game.gd` (mechanics), `test_keyboard.gd` (real key events), `test_clawd.gd` (animation parity) |

What its checks establish, from a baseline run on 2026-09-27 with `--fixed-fps 60`:

- 25 mechanics checks pass.
- 9 keyboard checks pass.
- `test_clawd.gd` reports `"checks":1950,"failures":0` over 162 animation samples.

That matches the repository's own `FRICTIONAL.md`, which records the same 25 and 9 and "1,944 scalar comparisons and six staged presentation checks" and adds: "This establishes sampled parity, not that every possible frame is right."

What remains unverified is also in its own words. The wide Clawd art "extends beyond the original 18 × 28 collision box; that tradeoff needs human inspection," and "human play-feel and film approval remain pending." None of its existing tests draws a pixel. That is the environment your shader lands in: well-tested mechanics, and no automated check of appearance at all.

The spec for this chapter also names **`walker-compute-post-shader`**, a Walker adaptation of Godot's `compute/post_shader` demo, public at [github.com/nikbearbrown/walker-compute-post-shader](https://github.com/nikbearbrown/walker-compute-post-shader). Its upstream source is [github.com/godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects), commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, path `compute/post_shader`, MIT license. It is the other kind of shader: a GLSL compute shader (`post_process_grayscale.glsl`, marked `#[compute]`) run as a `CompositorEffect` after the 3D scene renders. Its `VERIFICATION.md` is a model of stating the boundary:

- Ten headless checks pass: real G/S key events toggle the two effects, and the labels update.
- The imported grayscale shader reports "no compute compile error and 2112 SPIR-V bytes".
- But "RenderingDevice is explicitly unavailable in this run. Compiled bytecode is not executed-shader evidence," and "compute dispatch, depth reconstruction, per-view operation, GPU RID cleanup and actual image changes remain unverified."

Godot's [compute shader tutorial](https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html) adds that compute shaders "can only be used from RenderingDevice-based renderers (the Forward+ or Mobile renderer)". `walker-jumpman-clawd` uses Compatibility, so a compute effect is not an option there. Look at `walker-compute-post-shader` for the shape of an honest shader verification record, then do the 2D task below.

## Hands-on: specify, then build a failure flash

### Predict

Answer these in writing before you open Claude Code.

1. Clawd is drawn with `draw_rect()` calls and has no texture. In a `canvas_item` `fragment()`, which built-in carries his terracotta body colour: `COLOR` or `texture(TEXTURE, UV)`? What would the other one give you?
2. The level background is `#f6f3ec`. Using the WCAG contrast formula, white against it is about 1.11:1 and the level ink `#25354a` is about 11.23:1. What happens to a *white* flash at full strength?
3. If the fade is driven by counting 33 frames, how long does it last at 30 fps, at 60 and at 144? The retry always comes 0.55 s after the failure.
4. Of the spec's eight rules below, which can a headless test prove, and which need your eyes?

### Build It

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

Run the baseline so you know what "unchanged" looks like. Every frame-counted test gets a pinned `--fixed-fps`. Every test command is also wrapped in `timeout 120`, because a GDScript error before the script calls `quit()` leaves headless Godot running. In this book's probe, a null-method call in `_initialize()` was still running when `timeout` stopped it 20 seconds later, with exit status 124. `timeout` comes from GNU coreutils; on macOS, `brew install coreutils` provides it.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_clawd.gd --fixed-fps 60
```

**Step 1 — project context and the spec.** The spec block is yours: you write it, the agent copies it. The agent's job is to fill in project facts from the files, each with a reference. Paste this into Claude Code:

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

**Review what it wrote before you build on it.** This is a human step, and in the worked run it found real errors (see *What we actually ran*):

- Check every file reference against the file.
- Delete anything listed as a test that is not a test.
- Correct any "Unconfirmed" item that claims a headless test can verify a look.
- Add the headless facts for your machine. The worked run's corrected `CLAUDE.md` is in the example folder; its "Headless facts" block is four lines you can reuse.

Commit the reviewed file on its own, so the diff of the next step contains only the effect.

**Codex difference.** This repository already has an `AGENTS.md`, which Codex reads automatically; it will not read `CLAUDE.md` unless told to. Either append your spec block to `AGENTS.md`, or start the build prompt with "Read CLAUDE.md first". Run Codex non-interactively with a writable sandbox and closed stdin:

```bash
codex exec -s workspace-write "$(cat prompt-2.txt)" < /dev/null
```

**Step 2 — the build.** Paste this into Claude Code:

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

The Godot permission is `Bash(godot --headless:*)`, not `Bash(godot:*)`. If your Claude Code has user-level skills installed, also pass `--disallowedTools "Skill"` so the session cannot hand the task to one. None of this chapter's sessions invoked a skill; their transcripts show only Read, Write, Edit and Bash calls. The agent can run tests but cannot open a window. In the Chapter 7 run the same scoping refused a plain `godot --version`, which shows the rule is enforced.

### Use It

Now look, because nothing else can. Open `godot/project.godot` in the Godot 4.7.2 editor and press F5.

1. **Before any failure.** Clawd should look exactly as in the baseline: terracotta body, black eyes, no box around him. If he is white, or a solid block, the shader is reading the wrong input.
2. **A failure.** Walk into the red spikes on the first ground segment, or fall into a gap. Clawd should turn dark ink at once and fade back over about half a second, and the retry should put him back at the start in his normal colours. Do it several times; the look should be the same every time.
3. **R mid-failure.** Fail, then press R immediately. The tint should vanish on the retry, not linger.
4. **Boundaries.** Watch the platforms, the spikes, the "01 / GET MOVING" labels and the HUD during a flash. Nothing but Clawd should change. Open the gallery (`res://gallery/clawd_gallery.tscn`): it calls `Art.paint(self, …)` on its own node, not on the Player, so it should be unaffected.
5. **Controlled inputs.** Godot's debugging guide says that "while using **Remote** you can inspect or change the nodes' parameters in the running project." Pause the running game and select the Player node in the Remote scene tree. In the Inspector, open its material and set `flash_amount` to 0.0, 0.5 and 1.0 in turn. Take a screenshot at each value, and sample Clawd's body and one eye with a colour picker. The spec and the arithmetic of `mix()` predict:

| `flash_amount` | Body (from `#dd775b`) | Eye (from `#000000`) |
|---|---|---|
| 0.0 | `#dd775b` (221, 119, 91) | `#000000` |
| 0.5 | about (129, 86, 82–83) | about (18–19, 26–27, 37) |
| 1.0 | `#25354a` (37, 53, 74) | `#25354a` |

These predictions assume the mix happens on the colour values exactly as written. That assumption comes from reading the 4.7.2 source, not from observing a pixel. The Compatibility renderer's canvas uniform upload does no sRGB-to-linear conversion, and the Forward+ and Mobile renderers convert a `source_color` uniform in 2D only when the viewport renders in HDR. If your screenshot disagrees by more than a step or two per channel, that is a finding. Write it down, with the screenshot.

### Ship It

- **Commit.** Commit the effect separately from the reviewed `CLAUDE.md`, with a message that says what was checked, for example `Failure flash (shader + driver + test); headless checks at 30/60/144 fps; look checked by hand in the editor`. Keep your verification script in its own commit, so a reviewer can see which checks you wrote.
- **FRICTIONAL entry.** Record, in your own words and with the real date:
  - who did what (you wrote the spec and reviewed `CLAUDE.md`; the agent wrote the shader, driver and test),
  - what went wrong (in the worked run: wrong citations, a test that stopped measuring frame rate),
  - what you checked by eye and what you saw.
  Never record a human check you did not perform.
- **Brutalist skill.** This is development work, so the fit is `godot-gamedev`, "a Liam-narrated Godot development film pairing each focused code excerpt with the visible game result it produces". For a shader, the visible result has to be real engine output that you capture on a display. A headless log is not a visible result. `godot-walkthrough` (on disk as `godot-waikthrough`, which also accepts the other spelling) plays features and does not explain code. `godot-gdd` is for the design document.

### Verify

Run the project's suites and confirm they are unchanged: 25, 9, and 1,950 checks, and no `SHADER ERROR` lines.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

Then run your own check, not the agent's, at three frame rates. The worked run's `verify_flash.gd` is in the example folder: copy it to `godot/tests/`.

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

**What a pass proves:**

- Godot's shader compiler accepted the shader: the uniform list is intact and no `SHADER ERROR` line appears.
- The uniforms have the types, hint and default the spec names.
- In the real game loop, with a real fall and a real R key event, the value the shader receives follows the spec at three frame rates.

**What it does not prove:**

- That Clawd is tinted at all in the Compatibility renderer.
- That his colours at 0.0 are unchanged.
- That the level is untouched.
- That the flash reads well.

Those are the human checks in *Use It*, and nothing headless replaces them.

## What we actually ran

**Date and tools.** 2026-09-27, on the instructor's Mac: Godot 4.7.2.stable.official.ed1daf0bf, Claude Code 2.1.150 (its default model in this account was `claude-sonnet-4-6`). Both sessions ran non-interactively with the commands above, with `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` set so the agent kept no notes between runs. The starting revision was `walker-jumpman-clawd` `382f2ba`, with only `godot/` and the root `.md` files copied into a scratch Git repository. The full record is in [`../examples/06-shader-foundations/`](../examples/06-shader-foundations/).

**Before any agent ran: the headless experiment.** Summarised above and recorded in `HEADLESS-SHADER-FINDINGS.md`. One part of it broke the no-window rule. Four probe runs of about one second each, using `--display-driver headless` or `--headless --rendering-driver …`, fell back to the macOS display server, so a window may have appeared briefly. They are reported there, and were not repeated.

**Session 1 (`CLAUDE.md`).** 11 turns, about 100 seconds. The agent copied the spec block word for word and put `@AGENTS.md` on line 1. Its project context had these errors, found by checking each reference:

- It cited `project.godot` "lines 5–6" for the renderer and "line 4" for the main scene. The real lines are 7, 27 and 6.
- It attributed "Godot 4.7.2" to `project.godot`, which only says `"4.7"`. The patch version comes from the README.
- It listed `node scripts/clawd-build.cjs` as a headless test command. That script writes a build manifest, and `scripts/` was not in the copy.
- Under "Unconfirmed" it wrote that whether the `ShaderMaterial` tints the `draw_rect()` output would be settled by "the new headless test". A headless test cannot settle that at all.

All four were corrected by hand, and the headless facts were added, in a separate commit (`ea760cd`).

**Session 2 (the build).** 25 turns, about 22 minutes. About 15 of those minutes were a single reasoning step, between the failing 30 fps run and the agent's next action. The agent wrote:

- `godot/features/player/clawd_flash.gdshader`, starting from `vec4 col = COLOR;`: the right input, mixed toward `flash_color`, alpha untouched;
- 14 lines in `player.gd` that create the `ShaderMaterial` in `_ready()` and set `flash_amount = clampf(retry_remaining / 0.55, 0.0, 1.0)` during the failure and 0.0 otherwise, from `_process()`;
- `godot/tests/test_flash.gd`.

Its first test failed at `--fixed-fps 30`: `expected 0.6970 got 0.7576, remaining 0.3833`. The gap, 0.0606, is exactly one 30 fps frame (1/30 ÷ 0.55). The test read the material in the middle of a frame, after physics had advanced the countdown but before `_process()` updated the flash.

The agent's fix was to stop running frames. The final test calls `_update_flash()` directly after setting `retry_remaining` by hand to 0.55, 0.275 and 0.0. That makes it pass, and it also makes the `--fixed-fps` value irrelevant: spec rule 8's "at 30 and 144 fps" is no longer measured, even though the summary still reports runs at both rates.

**Our own verification.**

- The three original suites, at `--fixed-fps 60`, were unchanged: 25 PASS, 9 PASS, `"checks":1950,"failures":0`, no `SHADER ERROR`.
- The agent's `test_flash.gd` passed at 30, 60 and 144.
- The mutation: with one semicolon removed from the shader, `test_flash.gd` still exited 0 with 11 passing checks, and `test_game.gd` still passed 25 of 25. The log said `SHADER ERROR: Expected a ';'.` The agent's uniform "type" checks are set-then-get round trips, and a `ShaderMaterial` round-trips a parameter whether or not the shader parsed.

The mutation run, trimmed from `logs/mutation-missing-semicolon-test_flash.log`:

```text
SHADER ERROR: Expected a ';'.
FLASH TESTS: {"checks":11,"engine":"4.7.2-stable (official)","failures":0,"scope":"Shader parse + uniform types + flash_amount rules 1 and 2; visual result is a human check"}
```

We then wrote `verify_flash.gd`. It checks the uniform list (empty means the parse failed), reads the default colour from the source text, triggers a real failure by dropping Clawd below the level's fall line, samples the flash with a node that runs after every other `_process()` in the same frame, and sends a real R key event.

Results, from `logs/verify_flash-*.log`:

| `--fixed-fps` | Frames in the failure | Game time | First frame | Last frame before retry | Result |
|---|---|---|---|---|---|
| 30 | 17 | 0.567 s | 0.970 | ≈ 0 | 12 PASS |
| 60 | 34 | 0.567 s | 1.0 | ≈ 0 | 12 PASS |
| 144 | 82 | 0.571 s | 1.0 | ≈ 0 | 12 PASS |

The 144 fps run, trimmed from `logs/verify_flash-144.log`:

```text
{"average_frame_rate":143.7,"first_flash":1.0,"frames_in_failure":82,"last_flash_before_retry":0.0000000000000000883131951406374,"max_gap_vs_countdown":0.0,"seconds_in_failure":0.570555555555554}
VERIFY_FLASH failures=0
```

With the semicolon removed again, `verify_flash.gd` exited 1 with three failures, starting with `uniform list has both uniforms (parse succeeded)`.

Two small facts fell out of that table. First, the failure lasts 34 physics ticks, not 33. `0.55 − 33 × (1/60)` in floating point leaves about 5 × 10⁻¹⁷, which is not ≤ 0, so the retry waits one more tick. Second, at 30 fps the first visible flash value is 0.970, not 1.0, because two physics ticks run per frame and the countdown has already moved. The spec said "1.0 on the first frame"; the physics loop says "within one tick of it". The check allows 0.96, and the spec should have said so.

**What we did not do.** No window was opened, so none of the *Use It* checks was performed for this book. We do not know from observation that the tint appears, that the colours at 0.0 are unchanged, or that the predicted values in the table are what the screen shows. They are your checks.

## Check your understanding (ungraded)

1. Open `godot/tests/test_flash.gd` from the example folder. Find the line that makes its result independent of `--fixed-fps`, and explain in two sentences why the agent's change made the test pass without making it better.
2. Change `vec4 col = COLOR;` to `vec4 col = texture(TEXTURE, UV);`. Which of the project's headless checks fail? Run them. Then run the game and describe what you see. Which spec rule is violated, and why could no headless run tell you?
3. Add a third uniform to the shader but misspell its name in the `set_shader_parameter()` call. What does Godot report, headless and in the editor? What would a test have to assert to catch it?
4. `hint_range(0.0, 1.0)` is on `flash_amount`. Set it to 1.5 from GDScript and run the game. What happens to Clawd's colour, and what does that tell you about where to enforce a range?
5. `project.godot` uses the Compatibility renderer. Read the compute shader tutorial's renderer requirement and explain why the `walker-compute-post-shader` approach could not be dropped into this project.
6. Write the spec rule you would add so that the next agent cannot satisfy rule 8 by calling `_update_flash()` directly.

## Doing the same thing in Unity

*Unity was not run for this chapter. This comparison comes from Unity's documentation (the manual documents Unity 6.6 as of September 2026).*

### Similarities

- **Code or graph.** A shader can be written as code, in ShaderLab with HLSL program blocks (`HLSLPROGRAM … ENDHLSL`), or built as a node graph. For 2D sprites under URP, Shader Graph provides *Sprite Unlit*, *Sprite Lit* and *Sprite Custom Lit* targets.
- **Material properties are the contract.** You declare a property, set it on a `Material` from C#, and the shader reads it. For per-object values without duplicating materials, Unity has `MaterialPropertyBlock`, applied with `Renderer.SetPropertyBlock()`. That is the counterpart of Godot's per-instance uniforms or a duplicated `ShaderMaterial`.
- **Time is global.** The built-in `_Time` is "(t/20, t, t*2, t*3)". It is engine time, not the time since your event, exactly like Godot's `TIME`. A failure flash still needs a driver in C# that knows when the failure started.
- **The agent workflow.** An agent edits text (shader code, C# driver, tests), runs a headless test runner, and cannot see the result.

### Differences

- **Which pipeline.** Unity's shaders are written for a render pipeline (Built-in, URP or HDRP), and code for one is not automatically valid in another. Godot's `canvas_item` shader is one language across its renderers.
- **Batching caveat.** Unity's own `MaterialPropertyBlock` reference warns it "is not compatible with SRP Batcher" and that using it in URP or HDRP "will likely result in a drop in performance". Chapter 13's profiling is where you would check the cost of per-instance values in Godot.
- **Headless tests and graphics.** Unity's command line runs tests with `-batchmode -runTests -testPlatform EditMode` (or `PlayMode`) through the Unity Test Framework. `-nographics` means Unity "doesn't initialize the graphics device", which is the same boundary this chapter hit. An EditMode test can call the editor API `ShaderUtil.ShaderHasError(shader)`, which "checks if a shader has any compilation errors". That is a direct boolean, where Godot needs the uniform-list test plus a log grep. Whether it reports errors under `-nographics` was not checked for this book.
- **Text an agent can diff.** Unity's default Asset Serialization Mode is "Force Text", so scenes and materials are text an agent can read and diff. A Shader Graph is still best reviewed through the code it generates, just as with VisualShader.

| Godot 4.7 | Unity 6.6 |
|---|---|
| `shader_type canvas_item` | URP Sprite Unlit / Sprite Lit shader, or a ShaderLab shader |
| `uniform float x : hint_range(0, 1)` | `_X ("X", Range(0.0, 1.0)) = 0.5` in `Properties`, plus the HLSL variable |
| `ShaderMaterial.set_shader_parameter()` | `Material.SetFloat()`, or `MaterialPropertyBlock` |
| VisualShader | Shader Graph |
| `TIME` | `_Time` |
| `godot --headless --script …` | `-batchmode -runTests …`, with `-nographics` for no GPU |
| uniform list + `SHADER ERROR` grep | `ShaderUtil.ShaderHasError()` in an EditMode test |

## Doing the same thing in Unreal Engine

*Unreal Engine was not run for this chapter. This comparison comes from Epic's documentation for Unreal Engine 5.8, checked on 2026-09-27. Unreal's source code is available to licensees on GitHub under the Unreal Engine EULA. It is source-available, not open source.*

### Similarities

- **Parameters are the contract.** A material is built in the node-based Material Editor with named parameters. At runtime you create a Material Instance Dynamic and set a scalar parameter from Blueprint or C++ (*Create Dynamic Material Instance*, *Set Scalar Parameter Value*), which is the same move as `set_shader_parameter()`.
- **Hand-written code in a node.** The Custom material expression lets you "write custom HLSL shader code" inside the graph, the counterpart of VisualShader's Expression node.
- **The same headless boundary.** Unreal's `-nullrhi` flag uses a "null rendering hardware interface to run UE headless". A headless automation run checks logic, not pixels, as in Godot.

### Differences

- **Assets are not text.** Unreal stores assets "on disk as `.uasset` files, which is a file format specific to Unreal Engine". Epic's Diff Tool page says that with assets and Blueprints "a textual representation would not be constructive". An agent cannot read or diff your material graph the way it reads a `.gdshader`. It needs the editor's Python API, or C++ that builds the material.
- **The Custom node costs something.** Epic's page says it "prevents constant folding and may use significantly more instructions than an equivalent version done with built in nodes", and advises using it only for functionality the built-in nodes cannot provide.
- **Running tests.** Automation tests run from the command line, for example `-ExecCmds="Automation RunTest MySet.MySubSet;Quit"`, with `-unattended` to suppress dialogs and `-ReportExportPath` for JSON and HTML results.
- **Off-screen rendering is documented.** Unreal documents `-RenderOffScreen` ("Render off screen"), which the Godot 4.7.2 command line used here has no counterpart for. Whether it would let an agent capture pixels without a window was not tested.

| Godot 4.7 | Unreal Engine 5.8 |
|---|---|
| `.gdshader` text | Material asset (`.uasset`) built in the Material Editor |
| uniform | Material parameter (Scalar, Vector, Texture) |
| `ShaderMaterial` + `set_shader_parameter()` | Material Instance Dynamic + Set Scalar Parameter Value |
| VisualShader Expression node | Custom material expression (HLSL) |
| `--headless` | `-nullrhi` (no rendering), `-RenderOffScreen` |
| `--script res://tests/…` | `-ExecCmds="Automation RunTest …;Quit"` |

## Sources

Godot (official documentation, 4.7, and source at the 4.7.2 commit):

- Introduction to shaders — https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html
- Shading language reference — https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
- CanvasItem shaders — https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html
- Screen-reading shaders — https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html
- Visual shaders — https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html
- Converting GLSL to Godot shaders (ShaderToy mapping) — https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html
- Using compute shaders — https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html
- Shader class — https://docs.godotengine.org/en/stable/classes/class_shader.html
- ShaderMaterial class — https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html
- Viewport `use_hdr_2d` — https://docs.godotengine.org/en/stable/classes/class_viewport.html
- Command line tutorial — https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Overview of debugging tools (Remote scene tree) — https://docs.godotengine.org/en/stable/tutorials/scripting/debug/overview_of_debugging_tools.html
- Godot source at `ed1daf0bf001b61586d9930840f2f1394092c079`: `servers/rendering/dummy/storage/material_storage.cpp`, `drivers/gles3/storage/material_storage.cpp`, `servers/rendering/renderer_rd/renderer_canvas_render_rd.cpp` — https://github.com/godotengine/godot
- Godot demo projects, commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (`compute/post_shader`), MIT — https://github.com/godotengine/godot-demo-projects

Agents:

- Claude Code, "How Claude remembers your project" — https://code.claude.com/docs/en/memory
- Codex, "Custom instructions with AGENTS.md" — https://learn.chatgpt.com/docs/agent-configuration/agents-md
- `claude --help` (2.1.150) and `codex exec --help` (0.153.4), run on 2026-09-27

Walker:

- walker-jumpman-clawd — https://github.com/nikbearbrown/walker-jumpman-clawd (commit `382f2ba`; `README.md`, `FRICTIONAL.md`, `SOURCES.md`)
- walker-compute-post-shader — https://github.com/nikbearbrown/walker-compute-post-shader (`README.md`, `VERIFICATION.md`, `FRICTIONAL.md`)
- This chapter's record — `../examples/06-shader-foundations/`

Contrast arithmetic: WCAG 2 relative luminance and contrast ratio — https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 2026-09-27:

- Unity command line arguments — https://docs.unity3d.com/Manual/EditorCommandLineArguments.html
- Unity Test Framework command line — https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html
- `ShaderUtil.ShaderHasError` — https://docs.unity3d.com/ScriptReference/ShaderUtil.ShaderHasError.html
- `MaterialPropertyBlock` — https://docs.unity3d.com/ScriptReference/MaterialPropertyBlock.html
- Built-in shader variables (`_Time`) — https://docs.unity3d.com/Manual/SL-UnityShaderVariables.html
- ShaderLab Properties — https://docs.unity3d.com/Manual/SL-Properties.html
- `Material.SetFloat` — https://docs.unity3d.com/ScriptReference/Material.SetFloat.html
- Shader code blocks in ShaderLab — https://docs.unity3d.com/Manual/shader-shaderlab-code-blocks.html
- URP Sprite Unlit / Sprite Lit shader graphs — https://docs.unity3d.com/6000.4/Documentation/Manual/urp/prebuilt-shader-graphs-urp-sprite-unlit.html
- Asset serialization mode — https://docs.unity3d.com/Manual/class-EditorManager.html
- Unreal command-line arguments reference — https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference
- Run automation tests — https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- Custom material expressions — https://dev.epicgames.com/documentation/en-us/unreal-engine/custom-material-expressions-in-unreal-engine
- Instanced materials — https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-materials-in-unreal-engine
- Set Scalar Parameter Value — https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Rendering/Material/SetScalarParameterValue
- Working with assets (`.uasset`) — https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-assets-in-unreal-engine
- UE Diff Tool — https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine
- Unreal Engine on GitHub (EULA-governed source access) — https://www.unrealengine.com/ue-on-github
