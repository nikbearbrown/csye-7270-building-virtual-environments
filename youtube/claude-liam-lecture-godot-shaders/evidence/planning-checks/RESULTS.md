# Planning checks: results

**What this is.** The runs behind the numbers in `FACTCHECK.md`, in the order they were done, with the command, the result and what it means. All on Bear's Mac: Apple M4 Pro, Godot 4.7.2 stable (official), Forward+ unless stated, 2026-10-13.
**Why.** So any figure on screen can be re-run. Failed and inconclusive runs are kept and labelled.
**Found.** Seven scripts, one Lab batch, eleven findings. Two runs did not give the answer first time (the first `TIME` attempt; the tween on a never-set uniform) and both taught something.

The first runs of `verify.gd` and `verify2.gd` were read from the terminal and are transcribed in `run-0-first-runs-transcribed.txt`; the saved `run-1` and `run-2` logs are the re-runs.

Re-run the Lab batch: `./run-lab-checks.sh` (writes `lab-results.jsonl` and `png/`). Re-run a script: copy it into a scratch Godot project and `godot --path <project> --script res://<file>.gd`.

| Script / batch | Log | Finding |
|---|---|---|
| `verify.gd` A | `run-1-verify.log` | **Inconclusive, kept.** A node added after a 3 s timer read 1 stripe of `TIME` when engine ticks said 4.2 s (a second run read 3). Do not rely on it. |
| `verify.gd` B | `run-1-verify.log` | `UV.y` read 0.043 at the top and 0.965 at the bottom of a ColorRect; `discard` on the right half left the stage color (0.302 on the old stage) there. |
| `verify.gd` C | `run-1-verify.log` | A Sprite2D moved by `VERTEX.x += 50.0 * step(0.5, UV.y)`: left edge at rows 2, 25, 50, 75, 97 was x = 301, 313, 325, 338, 349 (even ramp 300 to 350). Only the four corners moved. |
| `verify.gd` D | `run-1-verify.log` | Naive `set_pixel` loop over 1920 × 1080: 53.8 ms (first run), 58.4 ms (re-run). A packed-array loop: 65 to 67 ms. Frame budget at 60 fps: 16.67 ms. |
| `verify2.gd` A2 | `run-2-verify2.log` | **TIME is one global clock.** Two nodes, one present from the start and one added at 3.0 s of process time, both read 12 quarter-seconds lit (3.0 s). |
| `verify2.gd` E | `run-2-verify2.log` | Same 1920 × 1080 gradient drawn by a shader: CPU submit time median 0.035 ms (first run) and 0.038 ms (re-run). The GPU time counter returned 0.0: unsupported here. |
| `verify3.gd` F, G, H | `run-3-verify3.log` | `hint_range(0,1)` does not clamp (7.0 stored). A wrong name (`rd`) is a silent no-op, stored as an unused parameter, no error. A tween on `shader_parameter/red` sweeps 0.0, 0.49, 1.0. |
| `verify4.gd` | `run-4-verify4.log`, `run-4b-verify4-darkcanvas.log` | The first run (white canvas) could not show light() at all because the base sprite was already white: **kept.** On a dark canvas: constant `light()` = 0.2 red reads 0.2, 0.4, 0.6 under one, two, three lights; an empty `light()` gives 0.0, no `light()` gives 1.0. |
| `verify5.gd` | `run-5a-verify5-FAILED-uniform-never-set.log`, `run-5b-verify5-fixed.log` | **5a failed:** a tween on a uniform never set from code errors "property does not exist". 5b: one `set_shader_parameter` in `_ready` fixes it; a pushed key event then opens the iris (centre stage color to sprite color). |
| `verify6.gd` | `run-6-verify6.log` | `get_shader_parameter` is null before any set (pixel still shows the default 0.2). Uniform names are case-sensitive: `"Red"` ignored, `"red"` works (0.898). |
| `run-lab-checks.sh` | `lab-results.jsonl`, `lab-summary.txt`, `png/` | 17 Lab renders of the film's 13 shader files; every probe as in `FACTCHECK.md`. Lean measured by `analyze-lean.py` → `lean-edge.txt` (50 px over 128 rows). |

**Side finding for the color film.** The Signal Garden pad shader at activation 0.5 reads (0.2588, 0.4392, 0.3059) in the Compatibility renderer and (0.2980, 0.5373, 0.3804) in Forward+: the same shader, two renderers, different pixels, because `source_color` uniforms are mixed in linear light in one and as raw values in the other.
