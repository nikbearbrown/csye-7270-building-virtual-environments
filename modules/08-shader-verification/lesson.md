# Module 8 — Shader verification

CSYE 7270 · Fall 2026 · Week 8

## Executive summary

This module is about reviewing a shader change that looks right, compiles and passes the test suite, but is wrong. You review a plausible commit to a 2D failure flash: it swaps the flash's time source for a frame counter, and makes the shader sample a texture instead of reading the incoming colour. Two agents review it first. Then you build the evidence yourself (a timing check swept across frame rates, a CPU model of what the pixels should be, and a fixed bench scene for the part only your eyes can check) and only then fix it. The finished evidence proves that the shader parses and keeps its contract, and that the value the shader receives follows the spec at three frame rates. It does not prove what the GPU draws. Two screenshots you take yourself do that.

## The question

Here is the change, as a reviewer would receive it:

```text
Flash: player owns its fade timer; sample the sprite texture explicitly

Presentation should not reach into session internals (retry_remaining).
The player now counts its own fade, and the shader reads TEXTURE directly
instead of relying on the incoming COLOR.
```

The motivation is respectable, since decoupling presentation from session state is a real design value. Before any agent looked at it, the change was run against every check the project had:

| Check | Result |
|---|---|
| `test_game.gd`, `test_keyboard.gd`, `test_clawd.gd` at `--fixed-fps 60` | all pass: 25, 9, 1,950 checks |
| `SHADER ERROR` lines in any log | 0 |
| `verify_flash.gd` (the timing check from Module 6) at `--fixed-fps 60` | pass: 12 of 12, largest gap 2.2 × 10⁻¹⁶ |
| `verify_flash.gd` at 30 fps and 144 fps | fail: gaps 0.515 and 0.606 |
| the agent's `test_flash.gd` | fail at every rate, for a reason unrelated to the bug |

A reviewer who runs the usual commands sees green. One bug shows only at other frame rates, which needs someone to try them; the other appears nowhere in that table. So: **how do you review a shader change so that evidence, not a successful compile, decides whether it merges?**

## The ideas

### The ladder of evidence for a shader change

Each rung establishes something the rung below cannot. Know which rung a claim stands on.

| Rung | Question it answers | Headless in Godot 4.7.2? |
|---|---|---|
| 1. Parse | Is it valid Godot shading language? | Yes: a `SHADER ERROR` line and an empty uniform list, on first use |
| 2. Contract | Do the uniforms, types, hints and defaults match the spec? | Yes: `get_shader_uniform_list()`, plus the source text for defaults |
| 3. Driver | Does gameplay code set the uniforms correctly at the right moments? | Yes: sample the uniform every frame at several pinned frame rates, with real input |
| 4. Model | Given these inputs, what should each pixel be? | Yes, as arithmetic: a CPU model of the spec. It says what the GPU should do, not what it did. |
| 5. Observation | What did the GPU actually draw? | **No.** A fixed test scene, a screenshot and a colour picker, done by a person. |

"It compiles" is rung 1, and most plausible-but-wrong changes pass rungs 1 and 2 by construction; that is what makes them plausible. The seeded change passes 1 and 2, and passes 3 at 60 fps. Only rung 3 at other rates, rung 4 and rung 5 catch it. A headless run has no GPU driver and no pixel readback, so rung 5 is closed to it.

### Five families of plausible-but-incorrect change

Each family has a controlled input, a value chosen so the right and wrong answers are far apart and easy to compute.

1. **Wrong input.** Reading `texture(TEXTURE, UV)` where the colour arrives in `COLOR`. Godot defines `COLOR` in a `canvas_item` fragment as the vertex colour multiplied by the texture colour ([CanvasItem shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html)). The exposing input is an untextured drawing whose parts have different vertex colours, such as Clawd's terracotta body and black eyes. At `flash_amount` 0 the right shader shows two colours; the wrong one cannot, because it never reads either.
2. **Colour space.** A normal map sampled with `source_color`, or a colour uniform without it. The exposing input is a flat normal texel (128, 128, 255), which lights at 1.0 when decoded right and 0.779 when decoded as sRGB (Module 7).
3. **Alpha convention.** `blend_mix`, the `canvas_item` default, blends the output colour by its own alpha, so a change that already multiplied RGB by alpha applies alpha twice. The exposing input is white at alpha 0.5 over black: the right blend gives 0.5, the double-applied one 0.25. (`blend_premul_alpha` is the mode that expects premultiplied colour.)
4. **Coordinate flips.** Godot's [GLSL conversion guide](https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html) warns that `FRAGCOORD` has a bottom-left origin while UV y-coordinates are flipped, so a ShaderToy port that mixes the two draws upside down. The exposing input is a texture red at the top and blue at the bottom.
5. **Time.** `TIME` is global time since the engine started, so an effect keyed to it starts wherever the clock happens to be: `abs(sin(TIME * 10.0))` is 0.46 at TIME 12.30 and 0.996 at 12.40. A frame counter is a different time bug: 33 frames is 0.55 s at 60 fps, 1.1 s at 30 and 0.23 s at 144. For both, pin the clock and sweep it.

The seeded change contains families 1 and 5.

### Controlled inputs in a headless Godot run

Three facts make frame-rate evidence trustworthy. **Pin the frame rate.** The command-line documentation says `--fixed-fps` forces a fixed number of frames per second and disables real-time synchronization ([Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)). Without it, headless Godot ran at about 145 frames per second on the course Mac, enough to make an untouched frame-counted test fail 4 times in 6. With it, each frame is exactly 1/fps seconds of game time and the run repeats.

**Physics has its own clock.** `walker-jumpman-clawd` ticks physics at 60 Hz whatever the frame rate. At 30 fps two ticks run per frame; at 144 fps most frames have none. Anything derived from a physics countdown moves in 1/60 s steps.

**Sample at a consistent point in the frame.** A test that awaits `process_frame` and then reads a value that `_process()` sets reads last frame's value against this frame's clock. The fix is a sampler node with a high `process_priority`, which runs after everything else in the frame. See `process_frame` and `physics_frame` on [`SceneTree`](https://docs.godotengine.org/en/stable/classes/class_scenetree.html).

### Test the spec, not the implementation, and then test the test

An **oracle** is whatever a test compares against. It can encode the spec or an implementation, and only the first survives a refactor. The agent-written `test_flash.gd` sets `retry_remaining` by hand and expects `retry_remaining / 0.55`; that is the implementation, and it would fail a correct fade driven by its own clock too. A spec oracle compares the flash with the line the spec describes, 1 − t/0.55, where t is game time since the failure began, with a tolerance only for what the engine's clocks force.

Then **test the test.** A new check must fail on a known-bad version and pass on a known-good one; running it only against the change under review does not show the check is right. In this module's run, the known-good half caught an agent-written oracle rejecting correct code.

### The CPU model and the bench

A **CPU model** is the spec written as arithmetic, runnable headless. For the flash, output colour is `mix(vertex_rgb, flash_rgb, amount)` with alpha unchanged. It gives the numbers the screen should show:

| | 0.0 | 0.5 | 1.0 |
|---|---|---|---|
| body `#dd775b` | `#dd775b` | `#815653` or `#815652` | `#25354a` |
| eyes `#000000` | `#000000` | `#131b25` or `#121a25` | `#25354a` |

Two conditions attach to the table. It models the spec, not the current shader, because a model transcribed from the shader under review would repeat its mistake. And "the mix happens on the values as written" rests on a reading of the 4.7.2 source, not a pixel: the Compatibility renderer uploads canvas uniforms without colour conversion, and the other renderers convert a `source_color` uniform in 2D only when the viewport uses HDR ([`Viewport.use_hdr_2d`](https://docs.godotengine.org/en/stable/classes/class_viewport.html)).

A **bench** is a scene that exists to be looked at: three copies of Clawd at `flash_amount` 0.0, 0.5 and 1.0 on the level's background, with no timers or input. A headless test can check that the bench is built right (three materials, three amounts, an intact uniform list); only a person with a display can check what it shows.

### Compute shaders: compiled is not run

`walker-compute-post-shader` has the same ladder with different tools. Its grayscale pass is a GLSL compute kernel (see the [compute shader tutorial](https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html)):

```glsl
float gray = color.r * 0.2125 + color.g * 0.7154 + color.b * 0.0721;
```

Rung 1 is stronger than for `.gdshader`: import runs a real GLSL-to-SPIR-V compile, and its `VERIFICATION.md` records no compute compile error and 2112 SPIR-V bytes. A broken kernel in this course's experiment imported to 0 bytes, with the error visible only in `RDShaderFile.get_spirv().compile_error_compute`, never in the import log. Rung 4 is easy: the weights sum to 1.0, so white and mid-grey stay put and pure red, green and blue become 0.2125, 0.7154 and 0.0721. Rung 5 needs a GPU; the run has no RenderingDevice, so compiled bytecode is not executed-shader evidence.

## The Walker example: walker-jumpman-clawd, as Module 6 left it

[`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd) is Professor Bear's semester-long Godot platformer. Its character, Clawd, is drawn in code with `draw_rect()` calls and has no texture. The repository is public, and its `SOURCES.md` says public availability is not a licence grant for inherited work whose licence is unestablished, so clone it to learn from. This module starts from the end state of Module 6's worked run: the public repository at commit `382f2ba`, plus a reviewed `CLAUDE.md` with an eight-rule effect spec, the agent's flash (`clawd_flash.gdshader` and 14 lines of `player.gd`), the agent's `test_flash.gd` and the human-written `verify_flash.gd`. Everything needed to rebuild it is in [`changes.diff`](../../examples/06-shader-foundations/changes.diff), and the seeded change is [`seeded-change.diff`](../../examples/08-shader-verification/seeded-change.diff).

The spec rules that matter here are rule 1 (the fade is linear in game time and lasts the same wall-clock time at 30, 60 and 144 fps) and rule 4 (at `flash_amount` 0.0 Clawd looks exactly as before, and at 1.0 every visible pixel is the flash colour). The seeded change breaks both. What the starting point already establishes: the mechanics, keyboard and Clawd suites pass, the shader parses, and the flash follows the countdown at 30, 60 and 144 fps. It establishes nothing about pixels.

The compute companion, [`walker-compute-post-shader`](https://github.com/nikbearbrown/walker-compute-post-shader) (an adaptation of Godot's `compute/post_shader` demo, upstream MIT licence kept), shows the compute side in its `VERIFICATION.md`.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

1. The seeded fade counts 33 frames. At `--fixed-fps` 30, 60 and 144, what is `flash_amount` on the last frame before the retry? At which rate will the timing check pass?
2. Clawd has no texture. After the seeded shader change, what will Clawd look like at `flash_amount` 0.0? Which check in the project could detect it?
3. You will write a timing oracle with a tolerance. What is the largest honest gap between a correct flash and the ideal line 1 − t/0.55 at 144 fps, given a 60 Hz physics countdown?
4. Two agents will review the change. Which bug do you expect each to find, and how will you know whether a finding is observed or assumed?

### 2. Build It

Rebuild Module 6's end state, then apply the seeded change. Clone `walker-jumpman-clawd` at `382f2ba` (Module 6's Build It has the commands), with this course's `examples/` folder beside the clone, and run:

```bash
git apply ../examples/06-shader-foundations/changes.diff
```

```bash
git add -A
```

```bash
git commit -m "Chapter 6 end state"
```

```bash
git apply ../examples/08-shader-verification/seeded-change.diff
```

```bash
git add -A
```

```bash
git commit -m "Seeded change for review"
```

In the course author's check, both patches applied cleanly to a fresh copy of commit `382f2ba`. `git add -A` matters: the first patch creates new files (`CLAUDE.md`, the shader, the tests), and `git commit -a` would leave them out.

If this is a fresh clone, run `godot --headless --path godot --import` once. Then run the suite yourself before any agent does, so you know what "green" looks like on a broken commit. Each test command is wrapped in `timeout 120` so a script error cannot leave Godot running:

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
```

**Prompt 1: the review (read-only).** Give the same prompt to both agents. It does not say what is wrong.

```text
Review only; do not edit any file. This repository is walker-jumpman-clawd
(Godot 4.7.2, GDScript, project in godot/). CLAUDE.md holds the effect
specification for the failure flash and the headless facts for this machine.

The most recent commit (git show HEAD) changes the flash. Review it against
the specification:
1. For each numbered spec rule, say whether the change preserves it, with
   the evidence line from the code.
2. List every problem you find, most severe first. For each, say how you
   would prove it: a headless check (give the command) or a human check in
   the editor (give the procedure). A headless run uses a dummy renderer.
3. You may run the headless tests listed in CLAUDE.md and the tests in
   godot/tests/, always with --headless and a pinned --fixed-fps.
Give a verdict: merge, or do not merge.
```

With Claude Code, give it read and headless-test tools only, so a review cannot edit:

```bash
claude -p "$(cat prompt-1-review.txt)" --allowedTools "Read,Glob,Grep,Bash(git:*),Bash(godot --headless:*),Bash(grep:*)" --max-turns 60 --output-format stream-json --verbose > review-claude.jsonl
```

With Codex, run it in a separate clone so the two reviews cannot touch each other's files. Codex reads `AGENTS.md` automatically and `CLAUDE.md` only because the prompt names it:

```bash
codex exec -s workspace-write --json -o review-codex.md "$(cat prompt-1-review.txt)" < /dev/null > review-codex.jsonl
```

Read both reviews against the code, not each other. For each claimed problem, ask: did the agent observe this, or assert it?

**Prompt 2: the evidence, before any fix.** Run it with either agent, as Module 6's build step did. In the run, Codex produced the evidence and the fix, because Claude Code's account usage limit had been reached.

```text
Do not fix the flash yet. Two reviews of HEAD found:
(a) the fade counts frames, so its length depends on the frame rate;
(b) the shader starts from texture(TEXTURE, UV) instead of COLOR, and Clawd
    is drawn with draw_rect() and has no texture.
Build the evidence first.

1. godot/tests/verify_flash.gd compares flash_amount with the session's
   retry countdown. That tests one implementation, not the spec. Add
   godot/tests/verify_flash_spec.gd that tests CLAUDE.md rule 1 directly:
   accumulate game time t from each frame's delta since the failure began,
   and require |flash_amount - (1 - t / 0.55)| to stay within one frame or
   one physics tick (whichever is longer), divided by 0.55. Also require:
   first failure frame >= 0.96, last failure frame <= 0.07, and 0.0 on the
   first frame after the retry. Use a real failure (Clawd moved below
   level.fall_y) and a sampler node that runs after every other _process in
   the frame.
2. godot/tests/flash_model.gd: a CPU model of spec rule 4, not of the
   current shader. Given a vertex color and flash_amount, return
   mix(vertex_rgb, flash_color_rgb, amount) with alpha unchanged. Print the
   predicted colors as hex for Clawd's body (#dd775b) and eyes (#000000) at
   0.0, 0.5 and 1.0, and assert the spec's endpoints.
3. godot/tests/flash_bench.tscn with flash_bench.gd: three copies of Clawd's
   drawing side by side on #f6f3ec, each with its own ShaderMaterial using
   clawd_flash.gdshader, flash_amount fixed at 0.0, 0.5 and 1.0, a label
   under each. No gameplay, input or timers. It is for a human to look at
   in the editor.
4. godot/tests/test_flash_bench.gd: headless; loads the bench and asserts
   each copy's flash_amount and that the shader's uniform list is intact.
5. BENCH.md at the repository root: the human procedure (open the bench,
   screenshot, sample body and eye pixels, compare with the model's table,
   what a mismatch means).

Run verify_flash_spec.gd with --headless at --fixed-fps 30, 60 and 144
against HEAD and report which checks fail. Run flash_model.gd and
test_flash_bench.gd with --headless --fixed-fps 60. Show the real output.
Do not edit the shader, player.gd or the existing tests. Do not commit.
```

**Test the test.** Before you trust `verify_flash_spec.gd`, run it against the known-good Module 6 shader and `player.gd` at all three rates, in a copy. It must pass there and fail on the seeded commit. If it fails on the known-good code, the oracle is wrong, not the code. Work out what tolerance the engine's clocks actually force, change it by hand, and commit that change separately with the reason.

**Prompt 3: the fix.** Only now:

```text
Now fix both problems with the smallest change. The shader must start from
the incoming COLOR again. The fade must follow game time, not frame count;
keep the player owning its fade if you can do that correctly, and say which
design you chose and why. Do not edit any file in godot/tests/.

Then run, always with --headless: the three original suites at
--fixed-fps 60; test_flash.gd, verify_flash.gd and verify_flash_spec.gd at
--fixed-fps 30, 60 and 144; flash_model.gd and test_flash_bench.gd at
--fixed-fps 60. Show the real output, and say which checks remain human
checks. Do not commit.
```

In the run, Codex put the shader back on `COLOR` and drove the fade from the session's `retry_remaining` clock, so the player no longer counts frames. Judge your own fix against the spec and your oracle, not against that one.

### 3. Use It

This is where the shader bug is judged, and it is yours. Every item is a **HUMAN CHECK**.

1. **The bench, broken and fixed.** HUMAN CHECK: open `godot/project.godot` in Godot 4.7.2, then `res://tests/flash_bench.tscn`; its script is a `@tool`, so it draws in the 2D view. Screenshot it on the seeded commit, then on the fixed commit, at the same zoom and with no colour management in your screenshot tool.
2. **Sample and compare.** HUMAN CHECK: on each screenshot, sample one pixel well inside the body and one inside an eye on each of the three copies, and compare them with the model's table, allowing one step per channel at 0.5. On the fixed commit you expect the table. On the seeded commit, the documentation predicts the body and eye colours are not preserved at 0.0; Claude Code's review predicted white, and Codex's said only "the default texture sample". Your screenshot decides.
3. **In the game.** HUMAN CHECK: run the fixed build and fail a few times; the flash should look as it did in Module 6. If your display runs at 120 Hz or more, repeat with the seeded commit and watch the fade finish long before the retry. That is family 5, visible.

### 4. Ship It

- **Commit order.** Commit the seeded change, the agents' evidence, your oracle correction, the fix and your review edits separately, as the example's [`git-log.txt`](../../examples/08-shader-verification/git-log.txt) shows, so a reviewer can see which line came from whom.
- **FRICTIONAL entry.** Record which reviewer found what, which claims were observed and which asserted, the oracle you corrected and the measured reason, and what the two bench screenshots showed. If an agent writes a FRICTIONAL entry for you, read who it says did the work.
- **Brutalist skill.** `godot-gamedev`. The code excerpt is the two changed lines; the visible result is your pair of bench screenshots, broken and fixed, side by side. The skills come from the course-provided Brutalist checkout; if yours lacks one, ask for the update.

### 5. Verify

The full matrix, on the fixed commit:

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash_spec.gd --fixed-fps 30
```

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash_spec.gd --fixed-fps 144
```

```bash
timeout 120 godot --headless --path godot --script res://tests/flash_model.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_flash_bench.gd --fixed-fps 60
```

Also run the three original suites, `test_flash.gd` and `verify_flash.gd` at 30, 60 and 144, and grep every log for `SHADER ERROR`.

**What a pass proves:** the shader parses and keeps its contract; at three pinned frame rates the value the shader receives follows the spec's line within the tolerance the engine's clocks force, justified by a check that fails the known-bad version and passes the known-good one; the bench holds the three intended inputs; and the model gives the pixel values to look for.

**What it does not prove:** that the fixed shader draws Clawd's colours and the flash as the model predicts, or that the seeded shader was visibly wrong. Both of those are your two screenshots.

## What the agents got wrong

This record is from 27 September 2026: Claude Code 2.1.150 (`claude-sonnet-4-6`) and Codex CLI 0.153.4 (`gpt-5.6-sol`, reasoning effort `low`). Both reviewers, given no hint, found both seeded bugs and said do not merge. That is one run each on one change, so it is not a rate.

**Claude ranked by its own test and stated what it had not observed.** It put the implementation-coupled `test_flash.gd` failure first ("CRITICAL") and the visible regression fourth. It stated as fact that Godot 4 provides a default white texture and that Clawd "becomes white", observing neither and naming no documentation that says so, and it did not run 144 fps, writing "expected to fail". Codex hedged its shader finding but ran the timing check at 30 and 144 and quoted the results.

**The agent's timing oracle rejected correct code.** Codex wrote `verify_flash_spec.gd` with a tolerance of one frame or one physics tick, whichever is longer. Run against the known-good Module 6 code, it passed at 30 and 60 fps and failed at 144 with error 0.0369 against a tolerance of 0.0303. A correct flash following a 60 Hz countdown, sampled at the end of a 144 fps frame, can trail the ideal line by one physics tick plus the frame in which the failure was detected. The prompt's wording was the course author's mistake as much as the agent's; a human corrected the tolerance to one frame plus one tick, in its own commit.

**The agent's FRICTIONAL entries credited a named person with work that person did not do.** Codex credited that person with supplying review findings and scoping the session, and did it again after the first correction. Nothing in the repository or the prompt said who the human was. Read who an agent says did the work before you sign your name under it.

## If you know Unity or Unreal

*Unity and Unreal were not run for this module; this comparison comes from their official documentation, checked on 27 September 2026.*

| Godot 4.7 | Unity 6.6 | Unreal Engine 5.8 |
|---|---|---|
| `--fixed-fps N` | `Time.captureFramerate = N` | `-UseFixedTimeStep -fps=N` (or `-Deterministic`) |
| `--headless` | `-nographics` (no graphics device) | `-nullrhi` |
| `--script res://tests/…` | `-runTests` (Unity Test Framework) | `-ExecCmds="Automation RunTest …;Quit"` |
| Bench scene, screenshot, colour picker | Graphics Test Framework image assertion against reference images (needs a GPU) | Functional Screenshot Test Actor and Screenshot Comparison against a Ground Truth image |
| Two-line shader diff in text | Code in text; Shader Graph reviewed through generated code | `.uasset` material reviewed in the editor's diff tool or generated text |

The review workflow carries over unchanged. The biggest difference is tooling for the last rung: Unity's Graphics Test Framework (experimental; version 8.3.3-exp.1 was documented) compares renders with reference images organised by colour space, platform and graphics API, and Unreal has a built-in screenshot comparison browser, while Godot 4.7.2's command line as used here has no counterpart, so the course uses a bench and a person. The [chapter](../../chapters/08-shader-verification.md) has the full comparison.

## Practice assessment (ungraded)

Answer these in your own words, then take the Canvas practice quiz for this module. Do not paste Claude's explanation as proof of your understanding.

1. Why does the seeded change pass every check at 60 fps? Which rungs catch it, and which do not?
2. Why is the known-good code's worst error at 144 fps (0.0369) larger than at 30 fps (0.0303), even though 144 fps samples more often?
3. `test_flash_bench.gd` passed on the seeded commit. What does it check, and why can none of it see the shader bug?
4. Claude Code's review predicted Clawd turns white. What would you see on the bench if `TEXTURE` defaulted to a different colour, and which part of your procedure still catches the bug?
5. A ShaderToy port uses `UV` where the original used `fragCoord`. Write the controlled input, predicted value and check that would catch it.

## The next step

This module feeds Assignment 6, "Audit a Plausible but Incorrect Shader Change". It covers Module 8, opens in Module 8 and is due about Day 60; its own page has the brief and the rubric, and nothing in this lesson is graded by itself. Bring this module's habits: know which rung a claim stands on, use controlled inputs, and test the test. Read the companion chapter, [Chapter 8 — Shader Verification](../../chapters/08-shader-verification.md), for the full run, the transcripts and the Unity and Unreal comparison.
