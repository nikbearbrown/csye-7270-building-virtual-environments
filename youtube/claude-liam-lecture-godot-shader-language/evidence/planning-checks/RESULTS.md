# Planning checks: results

**What this is.** The runs behind the numbers and messages in `FACTCHECK.md`: what was run, the command, the output file, and what it showed. All on Bear's Mac: Apple M4 Pro, Godot 4.7.2 stable (official), Forward+ unless stated, 2026-10-13.
**Why.** So any figure or engine message in the film can be re-run, and so runs that were inconclusive, failed or interrupted are visible instead of silently dropped.
**Found.** 67 Shader Lab runs (43 files and variants that must compile, 24 that must fail, every one with the expected exit code), 26 full engine logs, one GDScript check, eleven built-in visibility checks and five boundary checks. Five results changed the script: the docs' own `vec3 + 2` does not compile; only TIME, PI, TAU and E are visible inside your own functions; the documentation does discuss branch cost; `0.1 + 0.2 == 0.3` came out true here; a missing semicolon is reported on the next line.

## How to re-run

Every script is run from this folder (`zsh ./<name>`); the Lab lock is shared with other sessions, so a batch can take 15 to 20 minutes. Never `pkill -f` a script name: kill by PID.

| Script | Output | What it does |
|---|---|---|
| `lab-batch.sh` | `lab-results.jsonl`, `lab-summary.txt` (via `summarize_lab.py`), `png/` | 67 runs of `../../lab/check_shader.sh` on the files in `../../lab-shaders/`: command, exit code, the Lab's output, date. `RESUME=1` skips labels already recorded |
| `run-error-logs.sh` | `logs/<shader>.log` | The engine's FULL log for each of the 24 failing files and two clean ones (source excerpt with the marked line, the message, the `at:` line). Uses a throwaway copy of the Lab so it does not take the shared lock |
| `png-analysis.py` | `png-analysis.txt` | Pixel comparisons between renders (identical or not), where the teal line lands, the stripe rows |
| `pulse-range.sh` | `pulse-range.txt` | The opening shader sampled at 18 moments over 3.4 s |
| `run-builtins.sh` | `builtins-results.txt` | Which built-ins a user function can see (eleven tiny shaders in `builtins/`), plus boundary cases |
| `verify1.gd` | `run-1-verify1.log` | What the Inspector gets for each kind of uniform, from `ShaderMaterial.get_property_list()` (run in a scratch copy of the Lab: `godot --path <dir> --script res://verify1.gd`) |

`lab-batch.sh` was called `run-lab-checks.sh` until another session's `pkill -f run-lab-checks.sh` ended a batch of that name part-way (about 29 rows of 65 recorded). It was renamed, made resumable and run again to completion; two of its own runs overlapped for a minute, one label (`19-float-equals-321`) was recorded twice and the later row was kept.

## Findings

| # | Finding | Evidence |
|---|---|---|
| 1 | Every working file compiles (exit 0) and every `err` file fails (exit 1) with the engine's message; no clean log carries a warning | `lab-results.jsonl`, `logs/19-float-equals.log`, `logs/05-pastel.log` |
| 2 | Three spellings of one shader (neat, squeezed, spread) and the literal single line render the same pixels: 0 of 230,400 differ | `png-analysis.txt` |
| 3 | A commented-out line changes every pixel (largest channel difference 102/255); the active version equals the plain pastel shader | `png-analysis.txt` |
| 4 | `vec3 * 2.0` reads (0.4, 0.6, 0.8); `vec3 * vec3(2.0, 1.0, 0.5)` reads (0.4, 0.302, 0.2) | `lab-summary.txt` 07b, 07 |
| 5 | **The documentation's operator table writes `vec3(4, 5, 6) + 2`; Godot 4.7.2 refuses it** ("Invalid arguments to operator '+': 'vec3, int'.") | run 58-err-docs-table-vec3-plus-int |
| 6 | Int and float do not mix in assignment or arithmetic ("Invalid assignment of 'int' to 'float'.", "Invalid arguments to operator '+': 'int, float'.", "'*': 'float, int'"). **But** built-in function calls and vector constructors accept an int where a float is expected (`sin(1)`, `mix(vec3, vec3, 1)`, `vec4(1, 0, 0, 1)` compile): inconclusive for any blanket statement, so the film does not make one | runs 42, 43, 52, 53; `builtins-results.txt` boundary rows |
| 7 | A vec3 into `COLOR` ("Invalid arguments to operator '=': 'vec4, vec3'."); `.a` on a vec3 ("Invalid member for 'vec3' expression: '.a'."); mixing swizzle sets ("Cannot combine symbols from different sets in expression '.xg'."); constructor sizes ("Invalid arguments for the built-in function") | runs 44, 57, 51, 59, 60 |
| 8 | **A missing semicolon is reported on the NEXT line** (the marked line is the closing brace) | `logs/40-err-semicolon.log` |
| 9 | Function rules: return type must match; a non-void function needs a return; a call to a function defined below finds "No matching function"; a wrong argument type names both types | runs 45, 46, 47, 49 |
| 10 | **Inside a user function UV, COLOR, TEXTURE, TEXTURE_PIXEL_SIZE, FRAGCOORD, SCREEN_UV and SCREEN_PIXEL_SIZE are unknown; TIME, PI, TAU and E work** | `builtins-results.txt` |
| 11 | `in` copies (assigning to it compiles and the caller's variable stays 0.25); `inout` changes the original (0.75); `out` writes back | runs 12, 13, 14 |
| 12 | Overloading picks by argument type: `get_color(1)` teal, `get_color(1.0)` sand | run 15-overload |
| 13 | A condition must be a bool; a variable made inside braces is unknown after them; a const cannot be changed; a global used above its declaration is unknown (uniform, const and varying alike) | runs 50, 54, 55, 56, 62, 63 |
| 14 | If/else and the ternary draw the same pixels; the stripes loop draws five stripes of 22 rows at 360 rows | `png-analysis.txt` |
| 15 | **`UV.x == 0.5` lights no pixel at 640, 1280 or 1920 wide; one column at some odd widths (641, 1001), none at 321. The range version lights 6, 12, 20 columns.** `0.1 + 0.2 == 0.3` (from two uniforms) came out TRUE here, so the documentation's example is not a counter-example on this Mac | `png-analysis.txt`, run 29-float-sum-equals |
| 16 | `gl_FragColor` is an unknown identifier in Godot; the documentation maps it to `COLOR` | run 61, `converting_glsl_to_godot_shaders.html` |
| 17 | An unset `vec4` uniform with `source_color` reads (0, 0, 0) (black) | run 27-unset-tint |
| 18 | `ShaderMaterial` property list: group "Shader Parameters" (prefix `shader_parameter/`); `tint` (`source_color`) is a Color property, a plain `vec4` is a Vector4, `hint_range` gives a range hint ("0.0,1.0,0.001") | `run-1-verify1.log` |
| 19 | The opening shader pulses between 0.898 gray and (0.3765, 0.6392, 0.5686) teal with a period of about 3.2 s (tint set to #5FA391) | `pulse-range.txt` |
| 20 | `render_mode blend_add` adds the shader color to the background: (0.5, 0, 0) draws as (0.502, 0, 0) with the default and as (1.0, 0.8353, 0.7922) over the Lab stage | runs 21, 22 |
| 21 | **Boundary, inconclusive by design:** assigned at run time through the Lab, a shader with no `shader_type`, or with `render_mode` first, prints NO error and is simply not applied. The Lab cannot show that error, so the film cites the documentation for "first line" | `builtins-results.txt` (boundary rows) |
| 22 | The documentation's only statements about branch cost are on the Shader preprocessor page ("static" branching is handled well; many branches can slow a shader). Found by a text search of nineteen shader tutorial pages | `FACTCHECK.md` rows for B33 |

## Not run, on purpose

An infinite loop (it would freeze the machine), any timing of `discard` or of branches (no GPU time was readable on this setup), and any editor interaction.
