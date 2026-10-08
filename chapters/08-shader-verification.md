# Chapter 8 — Shader Verification

## Executive summary

This chapter is about reviewing a shader change that looks right, compiles, and passes the suite, but is wrong. The syllabus asks you to "compare controlled inputs and observed output" and to "show evidence, not just a successful compile".

You work on the failure flash from Chapter 6. A plausible commit changes two lines:

- the fade now counts frames instead of reading the game's clock;
- the shader now samples the texture instead of reading the incoming colour.

You ask Claude Code and Codex to review it. Then you build the evidence yourself: a timing check that sweeps frame rates, a CPU model of what the pixels should be, and a fixed test bench for the part only your eyes can check. Only then do you fix it.

The run for this book produced three results worth more than the fix:

- The frame-counting bug is invisible at 60 fps, the rate every existing command uses.
- The agent-written timing oracle rejected the correct code at 144 fps until its tolerance was reasoned out.
- The shader bug passes every headless check that exists and only a person looking at a screen can confirm it.

What the finished evidence proves, and what it leaves to you, is stated at the end of the hands-on.

## The question

Here is the change, as a reviewer would receive it:

```text
Flash: player owns its fade timer; sample the sprite texture explicitly

Presentation should not reach into session internals (retry_remaining).
The player now counts its own fade, and the shader reads TEXTURE directly
instead of relying on the incoming COLOR.
```

The motivation is respectable: decoupling presentation from session state is a real design value. Before any agent looked at it, it was run against every check the project had:

| Check | Result |
|---|---|
| `test_game.gd`, `test_keyboard.gd`, `test_clawd.gd` at `--fixed-fps 60` | all pass: 25, 9, 1,950 checks |
| `SHADER ERROR` lines in any log | 0 |
| Chapter 6's `verify_flash.gd` at `--fixed-fps 60` | **pass**: 12 of 12, largest gap 2.2 × 10⁻¹⁶ |
| `verify_flash.gd` at 30 fps and 144 fps | fail: gaps 0.515 and 0.606 |
| the agent's `test_flash.gd` | fail at every rate, for a reason that has nothing to do with the bug |

A reviewer who runs the usual commands sees green: a clean compile and a passing suite. The bug that shows only at other frame rates needs someone to try other frame rates. The other bug shows up nowhere in that table. So: **how do you review a shader change so that evidence, not a successful compile, decides whether it merges?**

## Ideas you need

### The ladder of evidence for a shader change

Each rung establishes something the rung below cannot. Know which rung a claim is standing on.

| Rung | Question it answers | Headless in Godot 4.7.2? |
|---|---|---|
| 1. Parse | Is it valid Godot shading language? | Yes: a `SHADER ERROR` line, and an empty uniform list, on first use (Chapter 6) |
| 2. Contract | Do the uniforms, types, hints and defaults match the spec? | Yes: `get_shader_uniform_list()`, plus the source text for defaults |
| 3. Driver | Does gameplay code set the uniforms to the right values at the right moments? | Yes: sample the uniform every frame, at several pinned frame rates, with real input |
| 4. Model | Given these inputs, what should each pixel be? | Yes, as arithmetic: a CPU model of the *spec*. It says what the GPU should do, not what it did. |
| 5. Observation | What did the GPU actually draw? | **No.** A fixed test scene, a screenshot and a colour picker, done by a person. |

"It compiles" is rung 1. Most plausible-but-wrong changes pass rungs 1 and 2 by construction; that is what makes them plausible. The seeded change passes 1 and 2, and passes 3 at 60 fps. Only rungs 3 at other rates, 4 and 5 catch it.

### Five families of plausible-but-incorrect change, and the input that exposes each

Each family has a controlled input: a value chosen so that the right answer and the wrong answer are far apart and easy to compute.

1. **Wrong input.** Reading `texture(TEXTURE, UV)` where the colour arrives in `COLOR`. Godot defines `COLOR` in a `canvas_item` fragment as "COLOR from the vertex() function multiplied by the TEXTURE color" ([CanvasItem shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html)). The exposing input is an untextured drawing whose parts have *different* vertex colours: Clawd's terracotta body and black eyes. At `flash_amount` 0 the right shader shows two colours; the wrong one cannot, because it never reads either.
2. **Colour space.** A normal map sampled with `source_color`, or a colour uniform without it. The exposing input is a flat normal texel (128, 128, 255). Read linearly, it points straight out. Decoded as sRGB, it tilts the surface 38.8° and lights it at 0.779 instead of 1.0 (Chapter 7).
3. **Alpha convention.** `blend_mix`, the `canvas_item` default ("alpha is transparency"), blends the output colour by its own alpha. A change that has already multiplied RGB by alpha, and keeps `blend_mix`, applies alpha twice. The exposing input is white at alpha 0.5 over black: the right blend gives 0.5, the double-applied one 0.25. Over the level's cream background, the red channel is 0.982 against 0.732. Godot's other mode, `blend_premul_alpha`, is the one that expects premultiplied colour.
4. **Coordinate flips.** Godot's GLSL-conversion guide warns that `FRAGCOORD` has a bottom-left origin like `gl_FragCoord`, while "when using UV coordinates in Godot, the y-coordinate will be flipped upside down" ([Converting GLSL to Godot shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html)). A ShaderToy port that mixes the two draws upside down. The exposing input is a texture that is red at the top and blue at the bottom.
5. **Time.** `TIME` is "global time since the engine has started … It repeats after every 3,600 seconds", so an effect keyed to `TIME` starts wherever the global clock happens to be. `abs(sin(TIME * 10.0))` is 0.46 at TIME = 12.30 and 0.996 at 12.40, so a "flash at the moment of failure" built that way has a random starting brightness. A counter of frames is a different time bug: 33 frames is 0.55 s at 60 fps, 1.1 s at 30, and 0.23 s at 144. The exposing input for both is the same: pin the clock and sweep it.

The seeded change contains families 1 and 5.

### Controlled inputs in a headless Godot run

Three facts from this course's runs make frame-rate evidence trustworthy:

1. **Pin the frame rate.** `--fixed-fps` is documented as "Force a fixed number of frames per second. This setting disables real-time synchronization." Without it, headless Godot runs as fast as the machine allows. Chapter 0 measured about 145 frames per second on the course Mac, enough to make an untouched frame-counted test fail 4 times in 6. With it, each frame is exactly 1/fps seconds of game time, and the run is repeatable.
2. **Physics has its own clock.** `walker-jumpman-clawd` ticks physics at 60 Hz whatever the frame rate. At 30 fps two physics ticks run per frame; at 144 fps most frames have none. Anything derived from a physics countdown moves in 1/60 s steps.
3. **Sample at a consistent point in the frame.** Godot emits `physics_frame` before physics processing and `process_frame` before `_process()`. A test that awaits `process_frame` and then reads a value that `_process()` sets is reading last frame's value against this frame's clock. Chapter 6's agent hit exactly that: a 0.0606 mismatch at 30 fps, one frame. The fix is a sampler node with a high `process_priority`, which runs after everything else in the frame.

### Test the spec, not the implementation, and then test the test

An **oracle** is whatever a test compares against. It can encode the spec or an implementation, and only the first survives a refactor.

- The Chapter 6 agent's `test_flash.gd` sets `retry_remaining` by hand and expects `flash_amount = retry_remaining / 0.55`. That is the implementation. It fails on the seeded change, but it would fail equally on a correct fade driven by its own clock. In the Claude Code review below, its failure was ranked the "CRITICAL" problem, above the player-visible regression.
- Chapter 6's own `verify_flash.gd` compares the flash with the session's countdown. That is milder, but still an implementation.
- A spec oracle compares the flash with the line the spec describes, 1 − t/0.55, where t is game time since the failure began. It allows a tolerance only for what the engine's clocks force.

Then **test the test**. A new check must fail on a known-bad version and pass on a known-good one. Running it only against the change under review tells you nothing about whether the check itself is right. In this chapter's run, that second half caught the agent's oracle rejecting correct code.

### The CPU model and the bench

A **CPU model** is the spec written as arithmetic, runnable headless. For the flash: output colour = `mix(vertex_rgb, flash_rgb, amount)`, with alpha unchanged. It gives the numbers the screen should show:

| | 0.0 | 0.5 | 1.0 |
|---|---|---|---|
| body `#dd775b` | `#dd775b` | `#815653` or `#815652` (blue is 82.5) | `#25354a` |
| eyes `#000000` | `#000000` | `#131b25` or `#121a25` (red 18.5, green 26.5) | `#25354a` |

Two conditions attach to that table. First, it models the *spec*, not the current shader: a model transcribed from the shader under review would repeat the shader's mistake. Second, the "mix happens on the values as written" assumption rests on a reading of the 4.7.2 source. The Compatibility renderer uploads canvas uniforms without colour conversion, and the RD renderers convert a `source_color` uniform in 2D only when the viewport uses HDR ([`Viewport.use_hdr_2d`](https://docs.godotengine.org/en/stable/classes/class_viewport.html) renders 2D "on linear values").

A **bench** is a scene that exists to be looked at. It holds fixed inputs: three copies of Clawd at `flash_amount` 0.0, 0.5 and 1.0, on the level's background, with no timers and no input. You open it in the editor, screenshot it, sample known pixels, and compare them with the model. A headless test can check that the bench is built right (three materials, three amounts, an intact uniform list). Only a person with a display can check what it shows.

### Compute shaders: compiled is not run

`walker-compute-post-shader` has the same ladder with different tools. Its grayscale pass is a GLSL compute kernel:

```glsl
float gray = color.r * 0.2125 + color.g * 0.7154 + color.b * 0.0721;
```

- **Rung 1 is stronger than for `.gdshader`.** Import runs a real GLSL-to-SPIR-V compile. Its `VERIFICATION.md` records "no compute compile error and 2112 SPIR-V bytes". This book's experiment showed a broken kernel importing to 0 bytes, with the error text visible only in `RDShaderFile.get_spirv().compile_error_compute`, never in the import log.
- **Rung 4 is easy.** The weights sum to 1.0, so white stays 1.0, mid-grey 0.5 stays 0.5, and pure red, green and blue become 0.2125, 0.7154 and 0.0721.
- **Rung 5 needs a GPU.** In its own words, "RenderingDevice is explicitly unavailable in this run. Compiled bytecode is not executed-shader evidence."

## The Walker example: walker-jumpman-clawd, as Chapter 6 left it

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-compute-post-shader`](https://github.com/nikbearbrown/walker-compute-post-shader). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

This chapter starts from the end state of Chapter 6's worked run:

- public `walker-jumpman-clawd` at `382f2ba`,
- plus the reviewed `CLAUDE.md` with its eight-rule effect spec,
- plus the agent's flash (`clawd_flash.gdshader` and 14 lines of `player.gd`),
- plus the agent's `test_flash.gd` and our `verify_flash.gd`.

Everything needed to rebuild it is in [`../examples/06-shader-foundations/changes.diff`](../examples/06-shader-foundations/changes.diff). The seeded change is [`../examples/08-shader-verification/seeded-change.diff`](../examples/08-shader-verification/seeded-change.diff).

What that starting point already establishes, from Chapter 6:

- the mechanics, keyboard and Clawd suites pass;
- the shader parses;
- the flash follows the countdown exactly at 30, 60 and 144 fps.

What it does not establish is anything about pixels. Chapter 6's human checks are the student's, and this book did not perform them. The spec in `CLAUDE.md` is the contract a reviewer holds the change to, and rule 4 ("At flash_amount 0.0 Clawd looks exactly as before") is the rule the shader change breaks.

`walker-compute-post-shader` (upstream `compute/post_shader` at `a3b5c11`, MIT) is the compute-shader companion: see *Compute shaders* above, and its `VERIFICATION.md`.

## Hands-on: review a plausible but incorrect shader change

### Predict

1. The seeded fade counts 33 frames. At `--fixed-fps` 30, 60 and 144, what is `flash_amount` on the last frame before the retry? At which rate will Chapter 6's check pass?
2. Clawd has no texture. After the seeded shader change, what will Clawd look like at `flash_amount` 0.0? Which check in the project could detect it?
3. You will write a timing oracle with a tolerance. What is the largest honest gap between a *correct* flash and the ideal line 1 − t/0.55 at 144 fps, given a 60 Hz physics countdown?
4. Two agents will review the change. Which bug do you expect each to find, and how will you know whether a finding is observed or assumed?

### Build It

Rebuild Chapter 6's end state, then apply the seeded change. From a clone of `walker-jumpman-clawd` at `382f2ba`, with this course's `examples/` folder beside it:

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

Both patches were checked to apply cleanly to a fresh copy of commit `382f2ba`. `git add -A` matters here: the first patch creates new files (`CLAUDE.md`, the shader, the tests), and `git commit -a` would leave them out.

If this is a fresh clone, run `godot --headless --path godot --import` once. Then run the whole suite yourself before any agent does, so you know what "green" looks like on a broken commit. As in Chapter 6, each test command is wrapped in `timeout 120` so that a script error cannot leave Godot running:

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/verify_flash.gd --fixed-fps 30
```

**Prompt 1 — the review (read-only).** Give the same prompt to both agents. It does not say what is wrong.

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

Read both reviews against the code, not against each other. For each claimed problem, ask: did the agent observe this, or assert it?

**Prompt 2 — the evidence, before any fix.**

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

**Test the test.** Before you trust `verify_flash_spec.gd`, run it against the known-good Chapter 6 shader and `player.gd` at all three rates, in a copy. It must pass there and fail on the seeded commit. If it fails on the known-good code, the oracle is wrong, not the code. Work out what tolerance the engine's clocks actually force, change it by hand, and commit that change separately with the reason.

**Prompt 3 — the fix.** Only now:

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

### Use It

This is where the shader bug is judged, and it is yours to do.

1. **The bench, broken and fixed.** Open `godot/project.godot` in Godot 4.7.2 and open `res://tests/flash_bench.tscn`; its script is a `@tool`, so it draws in the 2D view. Check out the seeded commit and take a screenshot. Then check out the fixed commit and take another. Use the same zoom, and no colour management in your screenshot tool.
2. **Sample and compare.** On each screenshot, sample one pixel well inside the body and one inside an eye on each of the three copies. Compare them with the model's table, allowing one step per channel at 0.5.
   - On the fixed commit you expect the table.
   - On the seeded commit, the documentation predicts that the body and eye colours are not preserved at 0.0. Claude Code's review predicted white; Codex's said only that the body and eyes would take "the default texture sample". Your screenshot decides.
3. **In the game.** Run the fixed build at a normal frame rate and fail a few times; the flash should look as it did in Chapter 6. If your display runs at 120 Hz or more, do the same with the seeded commit and watch the fade finish long before the retry. That is family 5, visible.

### Ship It

- **Commit order.** Commit the seeded change, the agents' evidence, your oracle correction, the fix, and your review edits separately, as the example repository's `git-log.txt` shows. A reviewer needs to see which line came from whom.
- **FRICTIONAL entry.** Record which reviewer found what, which claims were observed and which asserted, the oracle you corrected and the measured reason, and what the two bench screenshots showed. If an agent writes a FRICTIONAL entry for you, read who it says did the work. In this run Codex credited a named person, twice, with work that person did not do.
- **Brutalist skill.** `godot-gamedev`. The code excerpt is the two changed lines; the visible result is your pair of bench screenshots, broken and fixed, side by side.

### Verify

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

**What a pass proves:**

- The shader parses and keeps its contract.
- At three pinned frame rates, the value the shader receives follows the spec's line within the tolerance the engine's clocks force. That tolerance is justified by a check that fails the known-bad version and passes the known-good one.
- The bench is built with the three intended inputs.
- The model gives the pixel values to look for.

**What it does not prove:**

- That the fixed shader draws Clawd's colours, and the flash, as the model predicts.
- That the seeded shader was visibly wrong.

Both of those are your two screenshots.

## What we actually ran

**Date and tools.** 2026-09-27, Godot 4.7.2. Claude Code 2.1.150 ran with `claude-sonnet-4-6`. Codex CLI 0.153.4 ran with the account's configured `gpt-5.6-sol` at reasoning effort `low`. The starting point was the Chapter 6 end state (`b363a67`), plus the seeded commit `2473fd8`, which the book's author wrote. The full record is in [`../examples/08-shader-verification/`](../examples/08-shader-verification/).

**Before the agents.** The table in *The question* comes from `logs/seeded-*.log`. On the seeded commit, `verify_flash.gd` passed at 60 fps, failed at 30 (last frame before the retry 0.515) and failed at 144 (largest gap 0.606). `test_flash.gd` failed at every rate, with `expected 0.5 got 0.969697`.

**Review: Claude Code** (18 turns, about 4.5 minutes, read-only tools). Verdict "DO NOT MERGE". It found both bugs, and quoted `const FLASH_FRAMES := 33` and the `texture(TEXTURE, UV)` line as evidence. Things to notice:

- It ranked the implementation-coupled `test_flash.gd` failure first ("CRITICAL") and the visible regression fourth.
- It stated as fact that "Godot 4 provides a default 1×1 white texture" and that Clawd "becomes white". It observed neither, and no documentation it cited says so.
- It did not run 144 fps: "Not yet run; expected to fail".
- One command, `godot … ; echo "EXIT:$?"`, was refused by the permission rules, because the `echo` was outside the allowed prefix.

**Review: Codex** (5 shell commands; about 179,000 input tokens, 150,000 of them cached, and 4,700 output). Verdict "do not merge". It found both bugs, ran `verify_flash.gd` at 30 and 144, and quoted the results (0.5151515 and 0.6060606). It hedged the shader finding ("This can turn the body and eyes into the default texture sample") and gave a six-step human procedure. Both reviewers, given no hint, found both seeded bugs. That is one run each, on one change, so it is not a rate.

**Evidence: an interrupted start.** The Claude Code evidence session began at 14:47 and stopped at 14:48, after nine read-only tool calls, with no result record. It had been started with a shell `&` from a tool call that then exited, which may have ended the process. When we retried a few minutes later, the account had reached its limit: `You've hit your session limit · resets 6:40pm (America/New_York)`. Other agents were sharing the account. The evidence and fix sessions therefore ran on Codex, which the course allows as an alternative.

**Evidence: Codex** (about 349,000 input tokens, 314,000 cached; 10,000 output). It wrote `verify_flash_spec.gd`, `flash_model.gd`, the bench scene and script, `test_flash_bench.gd` and `BENCH.md`. Following the repository's `AGENTS.md`, it also added a `FRICTIONAL.md` entry. Against the seeded commit, its oracle failed at 30 fps (max error 0.515) and 144 fps (0.569) and passed at 60. The model printed `#815653` and `#131b25` for the midpoints, and the bench test passed 7 checks.

**Testing the test.** We ran the agent's `verify_flash_spec.gd` against the known-good Chapter 6 shader and driver in a separate copy. It passed at 30 and 60, and **failed at 144**: max error 0.0369 against a tolerance of 0.0303. From `logs/oracle-known-good-verify_flash_spec-144.log`:

```text
{"id":"time-linear flash stays within one frame or physics tick","observed":{"error":0.0368686868686869,"expected":0.569191919191919,"flash":0.606060606060606,"frame":37,"t":0.236944444444445,"tolerance":0.0303030303030303},"status":"FAIL"}
```

The prompt had said "one frame or one physics tick, whichever is longer", and that was our mistake as much as the agent's.

A correct flash that follows a 60 Hz countdown, sampled at the end of a 144 fps frame, can trail the ideal line by one physics tick *plus* the frame in which the failure was detected. We changed the tolerance to `(delta + physics_tick) / 0.55` by hand, in its own commit with that reasoning. The revised oracle:

| Oracle v2 | 30 fps | 60 fps | 144 fps |
|---|---|---|---|
| known-good Chapter 6 code | PASS (0.0303) | PASS (0.0303) | PASS (0.0369) |
| seeded change | FAIL (0.515) | PASS (0.0303) | FAIL (0.569) |

The 60 fps column cannot be fixed by any tolerance. At exactly 60 fps a 33-frame counter and a 0.55 s countdown are the same function, so the only evidence is at other rates.

The same review corrected the agent's `FRICTIONAL.md` entry. It said "Bear supplied two review findings" and "scoped this session". Nothing in the repository or the prompt said who the human was, and Bear did not do that work.

**Fix: Codex** (8 commands; about 373,000 input tokens, 327,000 cached; 4,500 output). It changed `vec4 col = texture(TEXTURE, UV);` back to `vec4 col = COLOR;` and replaced the counter with `clampf(game.retry_remaining / FLASH_SECONDS, 0.0, 1.0)`. It explained that "a second player timer could drift from the actual retry". It recorded its own tooling failure: a shell loop used zsh's read-only `status` variable and stopped after the first suite. Its new `FRICTIONAL.md` entry again credited Bear, one entry below our correction of the first, and we corrected it again.

**Our verification of the fix.** On the fixed commit, from `logs/fixed-*.log`:

| Check | Result |
|---|---|
| `test_game.gd`, `test_keyboard.gd`, `test_clawd.gd` @60 | pass |
| `test_flash.gd` @30 / 60 / 144 | pass |
| `verify_flash.gd` @30 / 60 / 144 | pass |
| `verify_flash_spec.gd` (v2) @30 / 60 / 144 | pass |
| `flash_model.gd`, `test_flash_bench.gd` @60 | pass |
| `SHADER ERROR` lines, all logs | 0 |

The fixed files are identical to the known-good Chapter 6 versions, apart from the constant's name.

**What we did not do.** No window was opened. We did not see the bench, the broken shader or the fixed one. The claim that the seeded shader loses Clawd's colours rests on Godot's definition of `COLOR` and the fact that Clawd has no texture. It was not observed. The two screenshots in *Use It* are the evidence for it, and they are yours to take.

## Check your understanding (ungraded)

1. Using the numbers in `logs/oracle-v2-*.log`, explain why the known-good code's worst error at 144 fps (0.0369) is larger than at 30 fps (0.0303), even though 144 fps samples more often.
2. Write the one-line change that would make the seeded frame counter frame-rate independent while the player still owns its fade. Which of the four timing checks would it pass, and which would it fail, and why?
3. `test_flash_bench.gd` passed on the seeded commit. List what it checks, and explain why none of those checks can see the shader bug.
4. Claude Code's review predicted that Clawd turns white (Codex said only that it takes the default texture sample). What would you see on the bench if `TEXTURE` defaulted to a different colour? Which part of your procedure would still catch the bug?
5. Add a "family 3" bug to a copy of the shader: multiply `col.rgb` by `col.a` and keep `blend_mix`. Which pixels of Clawd, if any, would change? Explain in terms of Clawd's alpha values, and say whether this bug matters for this drawing.
6. Write the controlled input, the predicted value and the headless or human check for a ShaderToy port that uses `UV` where the original used `fragCoord`.

## Doing the same thing in Unity

*Unity was not run for this chapter. This comparison comes from Unity's documentation (Unity 6.6 manual and scripting reference; Graphics Test Framework 8.3.3-exp.1), checked on 2026-09-27.*

### Similarities

- **Frame-rate independence is the driver's job.** A C# driver that counts frames has the same bug as the seeded GDScript; one that uses game time does not.
- **Game time can be pinned.** Unity's reference says that when `Time.captureDeltaTime` is non-zero, "Time.time increases at an interval of captureDeltaTime (scaled by Time.timeScale) regardless of real time and the duration of a frame". `Time.captureFramerate` is "the reciprocal of `Time.captureDeltaTime`". Together they serve the role `--fixed-fps` plays here. The documentation presents them as a way to capture movies, and warns that `captureDeltaTime` "does not have any affect on Time.unscaledTime" [sic].
- **The review workflow.** Everything in *Build It* carries over unchanged: agent review, controlled inputs, a spec oracle tested both ways, a bench.

### Differences

- **Image comparison exists as a package.** Unity's Graphics Test Framework "create[s] automated tests for rendering outputs — tests that render an image and compare it to a 'known good' reference image". Reference images are organised as ColorSpace/Platform/GraphicsAPI. The version documented, 8.3.3-exp.1, is experimental.
- **It still needs a GPU.** Batch runs with `-nographics` do not initialise the graphics device, so image tests are a different kind of run from the headless logic tests.
- **Reference images are per platform.** The folder hierarchy is itself a warning: the same shader's "correct" output differs by colour space, platform and graphics API. That is the same caution this book attaches to its predicted pixel values.

| Godot 4.7 | Unity 6.6 |
|---|---|
| `--fixed-fps 30` | `Time.captureFramerate = 30` |
| sampler node with high `process_priority` | a component in a late script-execution order, or `LateUpdate` |
| bench scene + screenshot + colour picker | Graphics Test Framework `ImageAssert` against reference images (GPU run) |
| uniform list + `SHADER ERROR` grep | `ShaderUtil.ShaderHasError()` in an EditMode test |

## Doing the same thing in Unreal Engine

*Unreal Engine was not run for this chapter. This comparison comes from Epic's documentation for Unreal Engine 5.8, checked on 2026-09-27.*

### Similarities

- **Pinning the clock.** The command line has `-UseFixedTimeStep` ("Use a fixed time step"), `-fps` ("Override fixed tick rate frames per second") and `-Deterministic` ("Shortcut for `-UseFixedTimeStep -FixedSeed`"). The frame-rate sweep in this chapter is a loop over `-fps` values.
- **The headless boundary.** `-nullrhi` runs "UE headless" with no rendering, so it is logic evidence only, as in Godot.
- **A human decides.** Screenshot tests end in a person's judgement. Epic's tool compares captures with a "Ground Truth" version "that you know is correct", and a reviewer decides whether a difference is a bug or a new ground truth.

### Differences

- **Screenshot tests are built in.** The Functional Screenshot Test Actor "can be placed in your level and used to capture a screenshot as part of the automation tests". You review the results in the Screenshot Comparison browser, opened from Window › Developer Tools › Session Frontend. Godot 4.7.2's command line, as used here, has no counterpart.
- **Off-screen rendering is documented.** `-RenderOffScreen` ("Render off screen") suggests a GPU run without a visible window. This book did not test whether it would satisfy a no-window rule like this course's.
- **The oracle is binary.** The material under test is a `.uasset`, so an agent reviews a Blueprint or material change through the editor's diff tool, or through generated text, rather than a two-line text diff.

| Godot 4.7 | Unreal Engine 5.8 |
|---|---|
| `--fixed-fps 144` | `-UseFixedTimeStep -fps=144` (or `-Deterministic`) |
| `--headless` | `-nullrhi` |
| bench + screenshot | Functional Screenshot Test Actor + Screenshot Comparison (Ground Truth) |
| `--script res://tests/…` | `-ExecCmds="Automation RunTest …;Quit"` |

## Sources

Godot (official documentation, 4.7, and source at the 4.7.2 commit):

- CanvasItem shaders (`COLOR`, `TIME`, render modes) — https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html
- Converting GLSL to Godot shaders (coordinate conventions) — https://docs.godotengine.org/en/stable/tutorials/shaders/converting_glsl_to_godot_shaders.html
- Shading language (hints) — https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
- Viewport `use_hdr_2d` — https://docs.godotengine.org/en/stable/classes/class_viewport.html
- Command line tutorial (`--fixed-fps`, `--headless`) — https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- Using compute shaders — https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html
- Godot source at `ed1daf0bf001b61586d9930840f2f1394092c079`: `drivers/gles3/storage/material_storage.cpp`, `servers/rendering/renderer_rd/renderer_canvas_render_rd.cpp` — https://github.com/godotengine/godot
- Godot demo projects, commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (`compute/post_shader`), MIT — https://github.com/godotengine/godot-demo-projects

Walker and this book:

- walker-jumpman-clawd — https://github.com/nikbearbrown/walker-jumpman-clawd (commit `382f2ba`)
- walker-compute-post-shader — https://github.com/nikbearbrown/walker-compute-post-shader (`VERIFICATION.md`)
- Chapter 6 record — `../examples/06-shader-foundations/` (including `HEADLESS-SHADER-FINDINGS.md`)
- Chapter 0, *The toolchain* (unpinned frame rates) — `00-the-toolchain.md`
- This chapter's record — `../examples/08-shader-verification/`

Agents:

- Claude Code memory and CLAUDE.md — https://code.claude.com/docs/en/memory
- Codex AGENTS.md — https://learn.chatgpt.com/docs/agent-configuration/agents-md

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 2026-09-27:

- Unity `Time.captureDeltaTime` — https://docs.unity3d.com/ScriptReference/Time-captureDeltaTime.html
- Unity `Time.captureFramerate` — https://docs.unity3d.com/ScriptReference/Time-captureFramerate.html
- Unity Graphics Test Framework — https://docs.unity3d.com/Packages/com.unity.testframework.graphics@8.3/manual/index.html
- Unity command line arguments (`-nographics`) — https://docs.unity3d.com/Manual/EditorCommandLineArguments.html
- `ShaderUtil.ShaderHasError` — https://docs.unity3d.com/ScriptReference/ShaderUtil.ShaderHasError.html
- Unreal command-line arguments reference — https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-command-line-arguments-reference
- Unreal Screenshot Comparison Tool — https://dev.epicgames.com/documentation/en-us/unreal-engine/screenshot-comparison-tool-in-unreal-engine
- Unreal automation tests — https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
