# Evidence notes, part A: Assignment 5 runs in Godot 4.7.2

## What this is, why it exists, what it found

**What.** Real runs, on Bear's Mac (Apple M4 Pro, Godot 4.7.2.stable.official.ed1daf0bf, run on 2026-10-16), of the instructor example for CSYE 7270 Assignment 5, done the way a student would do them: the assignment's wrapper script, the three mutations, the hint experiment, the pad values. Nothing here is invented; every number comes from a log or JSON file in `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/evidence/runs/` or a capture in `.../captures/forward-plus/`.

**Why.** The film walks students through the assignment. A narrator may only quote numbers that were measured. The shaders, materials and tests are an INSTRUCTOR EXAMPLE written by an AI (Codex) in `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot/course-series/`. They are not a student's hand-written work and the film must never call them that.

**What it found (the short version).**
1. The baseline is green and reproducible: 53 checks / 0 failures; the driver test passes at 30, 60 and 144 fps with 0.6 s of game time each; the curl calibration reproduces the example's earlier file byte for byte.
2. All three mutations fail the way the assignment says (parse: 4 failures + a SHADER ERROR line; rename: exactly 1 failure; missing `source_color`: 2 failures). Every shader file was restored byte-identical (sha256 checked) and the baseline went green again.
3. **Exit code 0 is not "no errors", proven twice.** (a) A script that feeds Godot a shader with a missing semicolon prints SHADER ERROR and exits 0; the wrapper turns that into exit 1. (b) The driver test run against a shader whose driven uniform was renamed PASSES (10/10, exit 0, log byte-identical to the baseline) because `set_shader_parameter` with an undeclared name raises no error. Only the uniform-list assertion in the contract test catches it.
4. **The hint experiment gives opposite pictures in the two renderers.** Forward+ matches the assignment's prediction (source_color quad unchanged 64/128/192; data quad brighter 137/188/225). Compatibility shows both quads unchanged (64/128/192).
5. **The pad's colours depend on the renderer, and the example's predictions only fit Compatibility.** Compatibility reproduces the example's recorded numbers exactly (re-run, zero difference). Forward+ differs from those predictions by up to 69 in one channel, and agrees byte for byte with a recomputation that decodes the sRGB colours to linear first, does the arithmetic, and encodes at the end.
6. The example's unexplained 3 to 5 byte Compatibility difference reproduces with a plain constant `ALBEDO = vec3(0.0585)`: no `mix()`, no stripe, no uniform, no hint. It is not caused by `mix()`. I did not find its mechanism and do not claim one.
7. A surprise in Forward+: for a colour uniform set from GDScript, the `source_color` hint made no measurable difference; the value's type did (a `Color` is converted, a `Vector4`/`Vector3` is not). Details in R9c.

Sections below: the table of every quotable number, then each run in order (command, exit code, elapsed, one-line result), deviations from the assignment text, surprises, and the file list.

---

## Table of numbers a narrator may quote

All numbers below are measured unless a row says "computed".

### Baseline and driver

| Quantity | Value | Source |
|---|---|---|
| Material contract baseline | **53 checks / 0 failures**, exit 0 (I counted 53 PASS lines, 0 FAIL lines) | `evidence/runs/R1-baseline-60fps.log` |
| Warnings in the baseline log | 1 `WARNING` line in the log ("Loaded resource as image file, this will not work on export") that the wrapper's grep does not match | same log |
| Driver test | **10 checks / 0 failures** at 30, 60 and 144 fps, exit 0 each | `R2-driver-{30,60,144}fps.log` |
| Game seconds (scale 1.0) | 0.599999999999999 at 30 fps, 0.599999999999999 at 60 fps, 0.6 at 144 fps. Say "0.6 seconds" | the DURATION lines |
| Game seconds (time scale 0.5) | 0.599999999999998 at all three rates | same |
| Render samples while charging (scale 1.0 / 0.5) | 16 / 34 at 30 fps; 34 / 70 at 60 fps; 83 / 169 at 144 fps | same |
| Tolerance in the test | 0.0166766666666667 s (that is 1/60 + 0.00001: one physics tick, not one frame at that rate) | same |
| Sample count in the TRACE | 294 at 30 fps, 409 at 60 fps, 726 at 144 fps | RESULT lines |
| Largest gap between uniform and charge/0.6 over all samples | 1.2e-15 at every rate (computed from the TRACE) | TRACE lines |
| Wall-clock cost | each headless test took 0.3 to 0.5 s, even the 144 fps run that simulates 726 frames; `--fixed-fps` does not run in real time. Do not say "the test ran for five seconds" | `journal-commands-exit-codes-elapsed.tsv` |

### Mutations (real file edits in the scratch copy, wrapper exit codes)

| Mutation | Wrapper exit | Checks / failures | Failing lines | Other |
|---|---|---|---|---|
| M1 parse: delete `;` after `shader_type spatial` (signal.gdshader line 1) | **1** | 53 / **4** | declared activation is float; declared quiet_color is vec4; declared active_color is vec4; declared stripe_count is float | `SHADER ERROR: Expected a ';' after 'shader_type spatial'.` and `UNIFORM_TYPES {}`. "texture-free signal" still passes. Raw `godot` without the wrapper also exits 1 here, because the test itself quits with 1 on failures |
| M2 rename: `activation` to `renamed_activation` in signal.gdshader only (2 occurrences: line 3 and line 10) | **1** | 53 / **1** | exactly: declared activation is float | `UNIFORM_TYPES` lists `renamed_activation`; no SHADER ERROR, the shader still compiles |
| M2b driver test against the renamed shader | **0** | 10 / **0** | none | log byte-identical to the baseline 60 fps driver log, TRACE included. `set_shader_parameter("activation", 0.7)` then `get_shader_parameter("activation")` printed `0.7`; `renamed_activation` read back `<null>`; no error line |
| M3 hint: delete `source_color` from the color_map line (surface.gdshader line 3) | **1** | 53 / **2** | matte color hint; coated color hint | no SHADER ERROR: the shader still compiles and still looks plausible |
| After restoring all three | **0** | 53 / **0** | none | sha256 of all four shader files equal the pre-mutation hashes, and `cmp` says identical to the files in `walker-claude` |

### Exit code 0 is not "no errors" (R5)

| Run | What printed | Exit |
|---|---|---|
| `shader-error-demo.gd` raw | `SHADER ERROR: Expected a ';' after 'shader_type spatial'.`, `ERROR: Shader compilation failed.`, `UNIFORMS 0` | **0** |
| same script through `scripts/run-test.sh` | the same lines | **1** |
| `git diff --stat godot/shaders/` clean | nothing printed | 0 |
| after a one-character edit | ` godot/shaders/signal.gdshader \| 2 +-` / ` 1 file changed, 1 insertion(+), 1 deletion(-)` | **0** (plain `git diff` exits 0 either way: the guard is "prints nothing", not the exit code) |
| after `git checkout -- godot/shaders/` | nothing printed | 0 |

### Curl ratios (normal maps)

| Image (size) | Read as GL | Read as DX | Stride |
|---|---|---|---|
| Poly Haven stone_floor `_nor_gl` (1024 x 1024) | **0.48445** | **1.51555** | 2 (the wrapper test; same as the example's file) |
| Poly Haven stone_floor `_nor_dx` (1024 x 1024) | **1.51555** | **0.48445** | 2 |
| `_nor_gl` | 0.48816 | 1.51184 | 4 (the assignment's default) |
| `_nor_gl` | 0.49841 | 1.50159 | 8 (the assignment's value for 4K; this pair is 1k, not 4K) |
| `_nor_dx` | 1.51183 | 0.48817 | 4 |
| `_nor_dx` | 1.50156 | 0.49844 | 8 |
| analytic-normal-gl.png (256 x 256, generated by code) | **0.05447** | **1.94553** | 2 (the example's default; also printed in the baseline log) |
| analytic-normal-gl.png | 0.05560 | 1.94440 | 4 |
| analytic-normal-gl.png | 0.05178 | 1.94822 | 8 |

The expected example values (0.48445 / 1.51555 / 1.51555 / 0.48445) are reproduced exactly; the JSON file is byte-identical to `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/evidence/course-assignment-series/shaders/normal-calibration.json`. The assignment's own listing, pasted verbatim into my script, and the example's helper return identical numbers at every stride. Note for honesty: the assignment says the GL file should come out "low" as GL and "near 2" as DX. The real Poly Haven pair gives 0.48 and 1.52: the order is right and the gap between conventions is 1.03, but 0.48 is not near 0 and 1.52 is not near 2. The analytic map does land near 0.05 and 1.95. I did not investigate why the photo-derived map sits mid-range.

### Hint experiment (3x1 PNG of greys 64, 128, 192; 3840 x 2160; unshaded; Linear tonemap; exposure 1.0)

Predicted (computed, the assignment's encode function: `encode(x) = 12.92x` for `x <= 0.0031308`, else `1.055 * x^(1/2.4) - 0.055`):

| Band | x = byte / 255 | encode(x) | x 255 | 8-bit |
|---|---|---|---|---|
| 64 | 0.25098 | 0.53807 | 137.21 | **137** |
| 128 | 0.50196 | 0.73665 | 187.84 | **188** |
| 192 | 0.75294 | 0.88235 | 224.9999 | **225** |

Measured (centre pixel of each band, RGB8 = round(c x 255); R = G = B everywhere; also cross-checked by reading the saved PNGs with PIL):

| Quad | Band | **Forward+** (Metal) | **Compatibility** (OpenGL on Metal) |
|---|---|---|---|
| source_color sampler | 64 / 128 / 192 | **64 / 128 / 192** | **64 / 128 / 192** |
| no hint (data) sampler | 64 / 128 / 192 | **137 / 188 / 225** | **64 / 128 / 192** |

Forward+ matches the assignment's prediction exactly (source_color quad unchanged, data quad brighter by the computed amounts). Compatibility shows both quads unchanged, i.e. no brightening of the data quad, so the assignment's prediction does not hold there. The assignment already says its predictions assume Forward+ or Mobile and tells students on Compatibility to measure first; this is why. The example's own earlier fixture ran in Compatibility and recorded 64/128/192 on both quads (`hint-samples.json`); that is reproduced.

Renderer read from the engine in the same run: Forward+ run reported `forward_plus`, `Apple M4 Pro (Apple9)`, driver `metal`; Compatibility run reported `gl_compatibility`, `Apple M4 Pro`, driver `opengl3`.

### Pad shader, signal.gdshader, per-channel RGB8 (fixed camera, Linear tonemap, exposure 1.0, directional light, ambient 0.35)

Pixels: UV.x 0.15625 is the dark stripe, 0.21875 the light stripe. "pred" is the example's recorded prediction (`controlled-predictions.json`, arithmetic on the colours as written, labelled "compatibility"). "diff" is measured minus pred.

| activation | stripe | pred | example recorded (Compat) | **re-run Compat** | diff Compat | **re-run Forward+** | diff Forward+ |
|---|---|---|---|---|---|---|---|
| 0.0 | dark | 66, 27, 15 | 66, 24, 10 | **66, 24, 10** | 0, -3, -5 | **83, 32, 17** | +17, +5, +2 |
| 0.0 | light | 102, 41, 23 | 102, 39, 19 | **102, 39, 19** | 0, -2, -4 | **102, 41, 23** | 0, 0, 0 |
| 0.5 | dark | 48, 105, 74 | 47, 105, 74 | **47, 105, 74** | -1, 0, 0 | **63, 136, 97** | +15, +31, +23 |
| 0.5 | light | 66, 112, 78 | 66, 112, 78 | **66, 112, 78** | 0, 0, 0 | **76, 137, 97** | +10, +25, +19 |
| 1.0 | dark | 31, 184, 133 | 28, 184, 133 | **28, 184, 133** | -3, 0, 0 | **31, 184, 133** | 0, 0, 0 |
| 1.0 | light | 31, 184, 133 | 28, 184, 133 | **28, 184, 133** | -3, 0, 0 | **31, 184, 133** | 0, 0, 0 |
| 2.0 | dark | 0, 255, 250 | 0, 255, 251 | **0, 255, 251** | 0, 0, +1 | **0, 248, 181** | 0, -7, -69 |
| 2.0 | light | 0, 255, 242 | 0, 255, 243 | **0, 255, 243** | 0, 0, +1 | **0, 247, 180** | 0, -8, -62 |

- The Compatibility re-run equals the example's recorded numbers in all 24 channel values (same-day run, difference 0 everywhere; the task allowed up to 1).
- Forward+ equals a **recomputation** (script `evidence/runs/scripts/analyze.py`: decode the shader's `source_color` colours from sRGB to linear, do `mix()` and the 0.65 stripe scale in linear, encode with the assignment's function, clamp) in all 24 channel values, difference 0. That is an agreement of numbers, shown here as a fit, not a statement about engine internals.
- Forward+ and the prediction agree where the arithmetic does not mix or scale (activation 1.0, and the light stripe at 0.0, where the stripe factor is 1.0) and disagree most where it does (activation 0.5, the dark stripe at 0.0).
- Activation 2.0 was set from code, outside `hint_range(0.0, 1.0)`. It was not clamped in either renderer: the colours at 2.0 are not the colours at 1.0 (Compat green 255, blue 251/243 vs 133; Forward+ 248/247 and 181/180). So `hint_range` did not clamp a value set from GDScript (the assignment's question 5), in both renderers.

### R9 probe: constant `ALBEDO`, unshaded, same camera and tonemap

Values per channel (R = G = B in every patch). "As written" is value x 255, rounded.

| value | as written | **Compat** (all 4 kinds) | Compat minus as written | **Forward+ float / literal** | Forward+ Color uniform |
|---|---|---|---|---|---|
| 0.0585 | 15 | **10** | -5 | 68 | 15 |
| 0.09 | 23 | **19** | -4 | 85 | 23 |
| 0.104 | 27 | **24** | -3 | 91 | 27 |
| 0.12 | 31 | **28** | -3 | 97 | 31 |
| 0.16 | 41 | **39** | -2 | 111 | 41 |
| 0.19 | 48 | **47** | -1 | 121 | 48 |
| 0.26 | 66 | **66** | 0 | 139 | 66 |
| 0.40 | 102 | **102** | 0 | 170 | 102 |
| 0.52 | 133 | **133** | 0 | 191 | 133 |
| 0.72 | 184 | **184** | 0 | 221 | 184 |

What the probe shows, and nothing more:
- **The Compatibility deviation is present for a constant output.** `ALBEDO = vec3(0.0585)` as a literal in the shader gives 10, not 15. So it does not come from `mix()`, from the stripe factor, from a uniform, or from `source_color`.
- **It looks like a function of the value alone.** Every Compatibility pad channel whose pre-output value is also a patch in this probe equals that patch's response: activation 0, dark stripe (0.26, 0.104, 0.0585) gave (66, 24, 10), the same as the patches; light stripe (0.4, 0.16, 0.09) gave (102, 39, 19), the same; activation 1.0 red (0.12) gave 28, the same; activation 0.5 dark red (0.19) gave 47, the same. Pad values that are not patches in the probe (for example 0.412) were not cross-checked this way. The size of the shortfall shrinks from -5 at 0.0585 to 0 from 0.26 up.
- **It is not an artefact of the SubViewport.** The same row read from the main window's own viewport (what the assignment's `capture()` snippet reads), a 1280 x 720 SubViewport and a 3840 x 2160 SubViewport gave identical numbers in both renderers (R9d).
- **Forward+ differs by renderer, not by a hidden deviation:** a literal or float uniform written to `ALBEDO` comes out as the sRGB encoding of the value (68 for 0.0585; I checked all ten against the assignment's `encode`: exact), and a `Color` uniform round-trips to the value as written (15). No 3 to 5 byte droop appears in Forward+.
- **Not shown:** the mechanism. I tried four closed-form guesses on paper (power-law decode and encode pairs with exponents 2.0, 2.2, 2.4, exact sRGB): none matched the ten Compatibility values within 3. I make no claim about the cause.

### R9c, a surprise worth one sentence in the film or none at all

For a colour uniform set from GDScript with `set_shader_parameter`, in Forward+ the **hint made no difference**: `uniform vec4 q : source_color` and `uniform vec4 q` both gave 15 for a `Color(0.0585, ...)` and both gave 68 for a `Vector4(0.0585, ...)`; the same held for `vec3` with `Vector3` (68) and `Color` (15). So the value's Variant type decided whether it was converted, not the hint. In Compatibility all eight cases gave 10 (no conversion either way). I tested only values passed from GDScript, not values stored in a `.tres` or typed in the Inspector, so do not extend this to "the hint does nothing for uniforms". The hint on a **texture sampler** does matter in Forward+ (R7).

---

## Runs, in order

Working copy: `/private/tmp/claude-501/a5-evidence/godot/` (an `rsync -a --exclude .godot` copy of `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-claude/godot/`). Nothing under `walker-claude` was touched. Every command ran from `/private/tmp/claude-501/a5-evidence`. The full command list with exit codes and elapsed times is `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/evidence/runs/journal-commands-exit-codes-elapsed.tsv`. For windowed runs the elapsed figure includes any wait for the Lab lock (R9b-types-fp shows 77.7 s because another session held the lock; the run itself took about 4 s).

The wrapper is `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/evidence/runs/scripts/run-test.sh`, written verbatim from the assignment text (diffed against it: identical). `set -o pipefail` is on, so `$?` is the exit status of `godot`, not `tee`.

| Run | Command (from scratch dir) | Exit | Elapsed | One-line result |
|---|---|---|---|---|
| R0 fresh cache | `godot --headless --path godot --import` | 0 | 3.0 s | No `.godot` existed; import finished, 4.4 MB cache built, no WARNING/ERROR/fail in the log. `evidence/runs/R0-import.log` (ANSI codes stripped; raw copy `R0-import.ansi.log`) |
| R1 baseline | `./scripts/run-test.sh test-material-contract.gd 60` | 0 | 0.5 s | `RESULT 53 checks / 0 failures / baseline`; 53 PASS, 0 FAIL; one engine WARNING about `Image.load_from_file` at test line 50 |
| R2 driver 30 | `./scripts/run-test.sh test-signal-driver.gd 30` | 0 | 0.4 s | `RESULT 10 checks / 0 failures; sample count 294`; game_seconds 0.599999999999999, render_samples 16 |
| R2 driver 60 | `... test-signal-driver.gd 60` | 0 | 0.4 s | 10 / 0; sample count 409; game_seconds 0.599999999999999, render_samples 34 |
| R2 driver 144 | `... test-signal-driver.gd 144` | 0 | 0.4 s | 10 / 0; sample count 726; game_seconds 0.6, render_samples 83 |
| R3 calibration | `./scripts/run-test.sh test-normal-calibration.gd 60` | 0 | 1.3 s | `PASS known GL/DX convention`; 0.48445 / 1.51555 / 1.51555 / 0.48445; JSON byte-identical to the example's. Two engine WARNINGs (`load_from_file`), not caught by the wrapper |
| R3b strides | `godot --headless --path godot --script res://tests/ev-curl-strides.gd -- <json>` | 0 | 3.2 s | Nine rows (3 images x strides 2, 4, 8), assignment listing and example helper agree exactly |
| R4 M1 parse | edit signal.gdshader line 1, then `./scripts/run-test.sh test-material-contract.gd 60` | **1** | 0.3 s | 4 failures + SHADER ERROR; restored |
| R4 M2 rename | rename in signal.gdshader only, same wrapper command | **1** | 0.3 s | exactly 1 failure, "declared activation is float" |
| R4 M2b driver | `./scripts/run-test.sh test-signal-driver.gd 60` against the renamed shader | **0** | 0.4 s | passes 10 / 0; log byte-identical to R2's 60 fps log. Honest finding: it neither fails nor hangs |
| R4 M2c probe | `godot --headless ... --script res://tests/ev-undeclared-param.gd` | 0 | 0.2 s | declared list lacks `activation`; `get_shader_parameter("activation")` returns 0.7 |
| R4 M3 hint | edit surface.gdshader line 3, same wrapper command | **1** | 0.3 s | 2 failures (matte, coated color hint); no SHADER ERROR; restored |
| R4 final | `./scripts/run-test.sh test-material-contract.gd 60` | 0 | 0.3 s | 53 / 0 after restore; all four sha256 match the originals |
| R5 raw | `godot --headless --path godot --script res://tests/shader-error-demo.gd` | **0** | 0.2 s | SHADER ERROR printed; exit 0 |
| R5 wrapper | `./scripts/run-test.sh shader-error-demo.gd 60` | **1** | 0.2 s | same output; wrapper turns it into exit 1 |
| R6 diff guard | `git diff --stat godot/shaders/` before, after, and after checkout | 0, 0, 0 | instant | silent / one stat line / silent. `evidence/runs/git-diff-guard.log` |
| R7 hint, Forward+ | `with_lab_lock.sh godot --path godot --rendering-method forward_plus --script res://course-series/tests/ev-hint-fixture.gd -- <outdir> forward_plus` | 0 | 2.6 s | window opened, Metal; 64/128/192 and 137/188/225 |
| R7 hint, Compat | same with `--rendering-method gl_compatibility` and tag `compatibility` | 0 | 1.4 s | window opened, OpenGL; 64/128/192 on both quads |
| R8 pad, Forward+ | `with_lab_lock.sh godot ... forward_plus --script res://course-series/tests/ev-signal-values.gd -- <outdir> forward_plus signal_fp` | 0 | 2.0 s | table above |
| R8 pad, Compat | same, `gl_compatibility` | 0 | 1.3 s | equals the example's recorded numbers exactly |
| R9 constant ALBEDO | `with_lab_lock.sh godot ... --script res://course-series/tests/ev-constant-albedo.gd -- <outdir> <tag>` in both renderers | 0, 0 | 4.3 s, 4.0 s | 4 rows x 10 values; table above |
| R9b types | `ev-constant-albedo-b.gd`, both renderers | 0, 0 | 77.7 s (lock wait), 3.9 s | Color vs Vector4 vs Vector3, no hint |
| R9c hint x type | `ev-constant-albedo-c.gd`, both renderers | 0, 0 | 0.8 s, 3.9 s | same with `source_color`; hint changed nothing |
| R9d render target | `ev-constant-albedo-d.gd` with `root`, `sub1280`, `sub3840`, both renderers (6 runs) | all 0 | 0.6 to 1.5 s each | same numbers from all three targets |

R9 was time-boxed to 30 minutes and finished well inside it (the R9 to R9d runs span about 4 minutes of wall time, plus writing the probe scripts). The windowed runs opened a real window every time (nothing needed to be skipped).

`runs/failed/` is empty: no run failed or needed repeating. The only slip was a shell typo (`echo =====` is a zsh error) while reading files, which ran no Godot.

---

## Deviations from the assignment text

1. **Names and paths.** The assignment's baseline test is `godot/tests/test_materials.gd`; the example's equivalent is `test-material-contract.gd` (and `test-signal-driver.gd`, `test-normal-calibration.gd`). The wrapper runs `res://tests/<file>`, so I copied those three scripts from `walker-claude/godot/course-series/tests/` into `godot/tests/` of the scratch copy, names unchanged. The example keeps its shaders in `godot/course-series/shaders/`; the assignment says `godot/shaders/`. The R6 scratch repo (`/private/tmp/claude-501/a5-evidence/repo`) uses `godot/shaders/` as the assignment says.
2. **Mutations by real file edit.** The example's own mutation evidence used an in-memory switch (`-- parse`, `-- rename`, `-- color-hint` user args). I did not use it: I edited the actual files, as the assignment tells a student, and got the same counts the example recorded (4 / 1 / 2 failures, 53 checks).
3. **The example's test already exits 1 on failures**, so the wrapper's grep for SHADER ERROR / SCRIPT ERROR was not what produced exit 1 in M1/M2/M3 (raw `godot` also exited 1 in M1). The grep matters for the R5 script, which has no failure counter.
4. **Hint fixture edited, not copied.** `ev-hint-fixture.gd` is a copy of `render-hint-fixture.gd` with: an explicit `WorldEnvironment` (Linear tonemap, exposure 1.0, glow, fog and adjustments off; flat background colour (0.965, 0.953, 0.925), which reads as 246, 243, 236 in the PNG). **The example's fixture has no WorldEnvironment node**, so the engine default applied there. Also the true renderer is read from the engine (the example's JSON hard-codes `"rendering_method": "gl_compatibility"`), samples are RGB8 integers, and a second user argument names the output files. The output directory is still the first user argument.
5. **Pad script.** `ev-signal-values.gd` is the `signal` part of `render-material-evidence.gd` plus the engine-reported renderer and file tags; the camera, environment, light, quad and sample pixels are unchanged.
6. **Poly Haven pair is 1k.** The assignment says stride 8 for 4K textures; I ran stride 8 on the 1024 x 1024 pair as the task asked and report it as such.
7. **Image format of the capture differs by renderer** (RGB8 in Forward+, RGBA8 in Compatibility, from `Image.get_format()`: 4 and 5). Pixel values were read through `get_pixel`, so it did not matter, but a narrator should not quote the format as a property of the shader.
8. **R5 script length.** The script that ran is exactly 6 lines. The saved copy `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/evidence/runs/shader-error-demo.gd` has 2 comment lines on top saying it was written for the film.
9. **R6 edit.** The one-character edit was on line 9 of signal.gdshader (`mix(0.65, 1.0, stripe)` to `mix(0.60, 1.0, stripe)`), labelled in the log as "a hand edit standing in for an agent edit, made for this film". The git identity was set only inside the scratch repo.

## Surprises, for the narrator's care

- **The example's predictions are for Compatibility, and the example's project is Compatibility.** A student on Forward+ or Mobile who follows the same arithmetic ("mix the colours as written") will be off by up to 31 in a channel at activation 0.5 and by 69 at activation 2.0. The film should not say "the prediction was right" without naming the renderer.
- **The example's earlier note about an unexplained 3 to 5 byte difference is real and reproduces on a constant colour.** What we can say: it is in the Compatibility output path for any value written to `ALBEDO`, it is gone in Forward+ (where the numbers follow the sRGB encode exactly), it is independent of `mix()`, the hint, and the render target. What we cannot say: why.
- **Rename mutation and the driver test.** The assignment says only the uniform-list assertion catches a rename. Confirmed in a real run: with `renamed_activation` in the shader the driver test passed all 10 checks, and its log was byte-identical to the unmutated run, including the 409-sample TRACE. The pad would simply not change colour.
- **Headless tests are fast.** 144 fps x 5 s of game time ran in 0.4 s of wall time. The wrapper's 120 s timeout is for hangs, not for normal runtime.
- **Only the exit code of the test is not the story.** The SHADER ERROR in R5 was printed with exit 0. A narrator should show the printed line and the two exit codes side by side.
- **`WARNING: Loaded resource as image file`** appears in the baseline and calibration logs (from `Image.load_from_file` on a `res://` PNG). It is a warning, not an error; the wrapper does not look for it.
- **Lab lock.** Another session (an editor-capture probe) held `/private/tmp/claude-501/shaderlab.lock` at the start; my windowed runs went through `with_lab_lock.sh` and one waited about 74 s. The lock was free when I finished.

## What I could not do or did not do

- No audio, no video, no publishing, nothing under `walker-claude` modified, no GPU timing, no Inspector or editor-session evidence (that is another agent's lane).
- I did not test values stored in `.tres` files or set through the Inspector for the R9c question, only values passed from GDScript.
- I did not find the cause of the Compatibility deviation.
- I did not run the assignment's other tests (`test_materials.gd` as the assignment names it does not exist in the example), the editor conversion of a `StandardMaterial3D`, or the `curl` check against a live URL.

---

## Files written (absolute paths)

Notes: `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/evidence/EVIDENCE-NOTES.md`

Under `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/evidence/runs/`:
- logs: `R0-import.log`, `R0-import.ansi.log`, `R1-baseline-60fps.log`, `R2-driver-30fps.log`, `R2-driver-60fps.log`, `R2-driver-144fps.log`, `R3-normal-calibration-60fps.log`, `R3-normal-calibration.json`, `R3b-curl-strides.log`, `R3b-curl-strides.json`, `R4-M1-parse-60fps.log`, `R4-M1-parse-raw-no-wrapper.log`, `R4-M2-rename-contract-60fps.log`, `R4-M2-rename-driver-60fps.log`, `R4-M2-undeclared-probe.log`, `R4-M3-hint-60fps.log`, `R4-final-baseline-60fps.log`, `R5-shader-error-raw.log`, `R5-shader-error-wrapper.log`, `git-diff-guard.log`, `R7-hint-forward_plus.log`, `R7-hint-compatibility.log`, `R8-signal-forward_plus.log`, `R8-signal-compatibility.log`, `R9-constant-albedo-{forward_plus,compatibility}.{log,json}`, `R9b-types-{forward_plus,compatibility}.{log,json}`, `R9c-hint-types-{forward_plus,compatibility}.{log,json}`, `R9d-{forward_plus,compatibility}-{root,sub1280,sub3840}.{log,json}`
- `shader-error-demo.gd`, `journal-commands-exit-codes-elapsed.tsv`, `sha256-shaders-before-and-after-mutations.txt`
- `scripts/`: `run-test.sh`, `rec.sh`, `ev-curl-strides.gd`, `ev-undeclared-param.gd`, `ev-hint-fixture.gd`, `ev-signal-values.gd`, `ev-constant-albedo.gd`, `ev-constant-albedo-b.gd`, `ev-constant-albedo-c.gd`, `ev-constant-albedo-d.gd`, `analyze.py`, `analysis.json`

Under `/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-first-shaders-materials-godot/captures/forward-plus/` (all PNGs are 3840 x 2160; both renderers' hint and pad JSON live here as the task asked):
- `hint_forward_plus.png`, `hint_forward_plus.json`, `hint_compatibility.png`, `hint_compatibility.json`, `gray-three-band.png`
- `signal_fp_0.0.png`, `signal_fp_0.5.png`, `signal_fp_1.0.png`, `signal_fp_2.0.png`, `signal_values_forward_plus.json`, `signal_values_compatibility.json`
- `constant_albedo_forward_plus.png`, `constant_albedo_compatibility.png`

Scratch (not part of the deliverable, 19 MB): `/private/tmp/claude-501/a5-evidence/`.
