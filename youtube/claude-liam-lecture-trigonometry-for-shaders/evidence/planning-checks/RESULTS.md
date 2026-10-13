# Planning checks: results

**What this is.** The runs behind every number and every Godot claim in `FACTCHECK.md`, in the order they were done, with the command, the result and what it means. All on Bear's Mac: Apple M4 Pro, macOS 26.5.1, Godot 4.7.2 stable (official), Forward+ unless a label says Compatibility, 2026-10-13.
**Why.** So any figure on screen can be re-run, and so the checks that did not go as planned are visible instead of tidied away.
**Found.** Every prediction held. 25 runs through the series' Shader Lab (71 probe readings, every one inside tolerance), 1 batch process rendering 51 cases (303 probe readings compared with predictions, every one inside tolerance, plus 5 readings kept as readings, and measurements on 36 saved frames), 1 GDScript math script (12 checks), and the 4.7 documentation quoted from the live pages. Nothing failed. Three things did not go straight: the first Lab runner was stopped while it queued (see Honest notes), the first flower shape was redrawn after looking at it, and two shader behaviours are only "undefined by the docs, finite on this Mac" (the arc tangent exactly on an axis).

## How the checks were built

Every probe has a **prediction computed from the maths** (`p = UV * 2 - 1`, `UV = (p + 1) / 2`, angles growing clockwise because y counts down) before the Godot reading is compared with it. Colours are plain constants, so a reading is the constant to 8-bit rounding (0.002); tolerance is 0.008, or 0.004 where the reading is a number encoded in a colour channel.

Re-run:

| What | Command (from this folder) |
|---|---|
| Math script | `godot --headless --path <scratch project with project.godot> --script <abs path>/verify-math.gd` |
| Essential Lab runs | `python3 run_lab_checks.py` (writes `lab-results.jsonl`, `lab-summary.txt`, `png/<label>.png`) |
| Many-variant batch | `python3 run_batch.py` (writes `batch-cases.json`, `batch-results.json`, `batch-summary.txt`; needs the scratch project at `/private/tmp/claude-501/godot-shaders-trigonometry-for-shaders/proj`, which holds a copy of `project.godot`) |
| Re-do the comparison only | `python3 run_batch.py --no-godot` |

| Script / batch | Log | Finding |
|---|---|---|
| `verify-math.gd` A | `run-1-verify-math.log` | `Vector2.from_angle(a)` equals `Vector2(cos a, sin a)`: largest difference 1.06e-7 (float32) over 12 angles, including 30.0 and negatives. |
| `verify-math.gd` B, C, D | `run-1-verify-math.log` | `Vector2.DOWN.angle()` is 1.5708 (PI/2), `RIGHT` 0, `UP` -1.5708, `LEFT` 3.1416; `Vector2(1, -1).angle()` is -0.7854; `RIGHT.rotated(PI/2)` is (0, 1): a positive rotation goes DOWN, which is clockwise on screen. `angle()` equals `atan2(y, x)`. |
| `verify-math.gd` E, F | `run-1-verify-math.log` | The by-hand example: 0.6 cos 30 degrees = 0.519615, 0.6 sin 30 degrees = 0.3 exactly (uv 0.7598, 0.65). Thirty read as radians: 4.7746 turns, ends at 278.9 degrees, `sin` -0.98803, `cos` 0.15425; thirty degrees gives 0.5 and 0.866025. |
| `verify-math.gd` G, H, I, J, K, L | `run-1-verify-math.log` | Ratios do not depend on size (error 1e-16 for hypotenuses 1 to 1000); `sin` 50 degrees 0.766044; `cos x = sin(x + PI/2)`; six whole radii and a leftover 0.2832 make a full turn; sine landmarks 0, 1, 0, -1, 0; tau / 3 = 120 degrees; `atan2` just below the left axis +3.14059, just above -3.14059; the one-argument `atan(1/1)` and `atan(-1/-1)` are both 0.7854 while the two-argument forms differ (0.7854 and -2.3562). |
| Lab `20-constants` | `lab-summary.txt` | `PI`, `TAU`, `E` compile **undeclared** and match their values; `TAU == 2 PI`; `radians(45.0) == PI / 4.0`; `degrees(PI) == 180.0`. |
| Lab `21-trig-values` | `lab-summary.txt` | `sin(radians(30))` 0.502, `cos(radians(30))` 0.8667, `0.5 tan(radians(45))` 0.502. With 30 read as radians: `0.5 + 0.5 sin(30)` reads 0.0078 (a sine of about -0.98, within one 8-bit step of -0.988), `0.5 + 0.5 cos(30)` 0.5765, turns / 8 0.5961 (4.77 turns). The shader compiled and ran with no error: skipping the conversion is silent. |
| Lab `27-pixel-p` | `lab-summary.txt` | `UV * 2.0 - 1.0` echoes UV at the corners and middle (0.0196, 0.498, 0.9765) and is inside the unit circle at the middle only. |
| Lab `01-moon-fixed`, `22-angle-90`, `22-angle-30-compat` | `lab-summary.txt` | Moon at 30 degrees at uv (0.7598, 0.65): right of the middle and BELOW it; the y-up mirror spot is empty. At 90 degrees the moon is straight down. Compatibility renderer: identical pixels (plain constants). |
| Lab `02`, `03`, `04`, `05`, `06`, `07`, `12` (one run each) | `lab-summary.txt`, `png/` | All seven TIME-driven shaders compile and run; pictures in `png/`. |
| Lab `23-meteor-*` | `lab-summary.txt` | The meteor lands at `moon + 0.2 (cos b, sin b)` for (a, b) = (0.8, 2.0) and (0.8, -2.0); the spot for the opposite sign is empty. |
| Lab `24-atan`, `24-atan-odd-view-481` | `lab-summary.txt` | The pixel's angle number `t = atan(p.y, p.x) / TAU + 0.5`: right 0.498, down 0.749, up 0.251; the four diagonals match the maths; **the seam**: 0.000 just above the left axis, 1.000 just below. The top-start number reads 1.0 just left of twelve and 0.0 just right of it. On an odd-sized view (pixels exactly on the axes, where the docs call the result undefined) this Mac returned finite values: -PI/2 and +PI/2 on the vertical axis, -PI on the left axis, 0 on the right, and an arbitrary -3PI/4 at the exact middle. |
| Lab `25-atan-one-argument`, `09-atan-one-argument` | `lab-summary.txt` | With `atan(p.y / p.x)`, opposite quadrants read the same number (0.749 and 0.749; 0.247 and 0.251), and the colour picture is identical in opposite quadrants. |
| Lab `08-atan-colors`, `-compat` | `lab-summary.txt` | Colours equal `mix(teal, amber, t)` at four points; teal just above the left axis, amber just below; Compatibility renderer: same pixels. |
| Lab `10-sweep-0.5`, `11-sweep-top-0.5`, `10-sweep-0.5-compat` | `lab-summary.txt` | At sweep 0.5 the upper half of the blob is shown (reveal starts at the left, over the top); with the `fract` start the right half is shown (reveal starts at twelve). Compatibility renderer: same pixels. |
| Lab `26-flower-static-8` | `lab-summary.txt` | Edge radius `0.55 + 0.15 cos(8 a)` probed inside and outside at eight angles, including either side of the left axis. |
| Batch: 15 angles | `batch-summary.txt` | The moon lands at `0.6 (cos a, sin a)` for 0, 30, 60, ... 330, -30, -90 and 390 degrees, every time below the middle for positive sines (y down). |
| Batch: TIME series | `batch-summary.txt`, `png/batch-*` | `a = TIME`: the moon turns clockwise at +0.992, +1.002, +0.998, +1.002 rad/s at a constant 0.600 of the half-width. `a = TIME * 2.0`: +1.971, +1.999, +2.000 rad/s. Meteor: moon +1.00 rad/s around the planet; meteor around the MOON +2.99, +2.98, +3.02, +3.00 rad/s; reversed meteor -3.01, -2.99, -3.00, -3.00 with the moon unchanged. Three moons: gaps 120.0, 120.0, 120.0 degrees at two times. |
| Batch: the wide view | `batch-summary.txt`, `png/batch-wide*` | On 640 x 360 the planet is 160 x 90 px (oval, ratio 1.778); with `p.x *= aspect` and aspect 1.7778 it is 90 x 90 px. On 480 x 480 it is 120 x 120. |
| Batch: sweeps and the worked pixel | `batch-summary.txt` | Sweep 0, 0.25, 0.3, 0.5, 0.75, 1.0 for both reveals: each of four probe points is shown exactly when its t is below sweep. The pixel p = (-0.3, -0.3) (t = 0.125) is hidden at sweep 0.12 and shown at 0.13. |
| Batch: atan rings | `batch-summary.txt` | 24 directions at radius 0.7: R and B (the TAU and PI forms) equal the predicted t, G equals the top-seam t. 16 opposite pairs agree for the one-argument form (32 probes). |
| Batch: the flower | `batch-summary.txt`, `png/batch-flower12*` | 64 edge probes for 8 petals and 64 for 6 petals all inside/outside as predicted; edge radius 0.398 to 0.700; the pattern turns +0.99 and +1.01 rad/s clockwise; 8 petals counted on the saved frame. |
| Docs | `docs-quotes.txt` | Exact quotes with URLs, anchors and the read date. |
| All captures | `contact-sheet.png` | The planning-run frames of every capture (C01 to C13) on one sheet, so the pictures can be looked at before anything is built. |

## Honest notes (what did not go straight)

- **The first Lab runner was stopped.** A first version tried 65 runs through `check_shader.sh`; with several films laid out at once the shared Lab queued every run, so it was stopped after its first run and split in two: the essential runs through the Lab (above) and the many-variant sweeps in one Godot process (`verify-batch.gd` in a scratch project, which mimics `lab/runner.gd`: same clear colour, same stage kinds, same probe rule). No reading from the stopped run was used.
- **The flower was redrawn.** The first version of the shape (`0.6 + 0.1 cos(8 a)`, called a gear in the first draft) looked like a wavy disc, not a gear and not a flower. It was changed to `0.55 + 0.15 cos(8 a)` and renamed `12-flower`; all its checks were re-run on the final file. FACTCHECK row 60 records the wording fix.
- **8-bit readings.** A Lab probe is read from an 8-bit frame, so `sin(30.0)` shows as -0.984 (one step from -0.988). The film puts the math value (-0.99) on screen and says the shader reading agrees to 8-bit precision.
- **The arc tangent on an axis is undefined by the docs.** Godot's page says "The result is undefined if x == 0", and Khronos' page says the same. The film never relies on it. A pixel exactly on an axis only occurs in odd-sized views; here it returned finite values. Other graphics cards may differ.
- **No GPU timing, no frame-rate claim.** Nothing in this film depends on either; captures are offline at a fixed tick rate.
- **Third-party material.** The source course and intro video are known to this layout only through the series brief's description; no transcript was stored or copied (see `SOURCES.md`).

## Side findings for the series (read, not rendered)

- **`LectureCodeTrace` holds about ten lines.** From `LectureCodeTrace.tsx`: the code box is 700 px high with 36 px padding and a 3 px border at the 1920 x 1080 design, and each line is 42 px type at line height 1.45 (about 61 px), so about 10 lines fit. The pilot's `B14` puts a 13-line file in one; look at its still. This film's longer files use `ShaderLab` with `layout: code` instead. (Read from the source only; not rendered here.)
- **`PI`, `TAU` and `E` live in each shader type's reference** (Global built-ins), not in the Shading language page: the `GLOSSARY.md` could say where to cite them.
- **The voice dictionary reads all-caps `PI` as the letters P, I** (the principal investigator rule) and lowercase `pi` as "pie": narration should write `pi`, never `PI`.
