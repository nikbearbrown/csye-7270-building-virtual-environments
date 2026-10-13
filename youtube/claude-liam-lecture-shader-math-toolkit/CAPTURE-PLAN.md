# Capture plan: The Shader Math Toolkit

**What this is.** Every Godot render and screenshot the build session must record for this film, with the exact shader file, target, values over time, duration, renderer, what must be visible at the 50 % and 85 % marks, and the result already verified. Nothing is recorded yet; every number below comes from planning runs in `evidence/planning-checks/`.
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment.
**Found.** 16 Godot renders (10 stills, 6 uniform sweeps), all one-shader Lab renders of tested files in `lab-shaders/`, plus one docs screenshot. No editor frames, no scene scripts, no scripted key presses: nothing here needs an interactive editor action. Every probe value below was read in a real Godot 4.7.2 window on Forward+ (Apple M4 Pro). The Compatibility renderer gives the same pixels for these shaders (`evidence/planning-checks/renderer-compare.json`), but the credit lines say Forward+.

## Conventions for every capture

- 30 fps; render at 3840 x 2160 using the Signal Garden SubViewport native-size route (see `../_godot-shaders-series/COMPONENT-SPECS.md`, "Capture harness"); the Lab stage color `#D9D5CA`; **Forward+**; offline fixed tick rate, so nothing here says anything about real-time frame rate. Stills are PNG at 3840 x 2160 (rendered, not upscaled); sweeps are MP4.
- **Strips** (`rect`): `--kind rect`, the shader fills the whole 16:9 frame, `UV` runs 0 to 1 across the full width.
- **Square pictures** (`square`): `--kind sprite --sprite-tex white --sprite-scale 5.625 --size 1280x720`, i.e. a 720 x 720 square centred in the 1280 x 720 logical canvas with the stage color either side. This is the Lab's own `sprite` kind; it gives the same pixels as a plain 720 x 720 rect render (`square-via-sprite.json`: largest difference one level, stage `217, 213, 202`), `UV` runs 0 to 1 across the square, and circles stay round. Readout and ring positions in the lanes use the square's frame (x from 0.219 to 0.781 of the width, y from 0 to 1) and are indicative: place them on the real frame.
- **Sweeps** use a piecewise-linear schedule on one uniform: time-in-seconds : value pairs (the harness option `--animate name:t0:v0,t1:v1,...` that `COMPONENT-SPECS.md` specifies; the exact option strings for the six sweeps are listed under the table; if the harness lacks the option, add it, or record segments whose end values meet and join them with ffmpeg). The values at the 50 % and 85 % marks are computed from the keyframes below. Sweeps finish by about 85 % of the estimated beat length and then hold, so a measured audio up to 10 % shorter or longer still lands; **if the measured beat is longer than the capture by more than half a second, re-record with the keyframes stretched** (the lane's `show` cues are fractions of the beat, so only the capture needs to change).
- No scripted input anywhere (no key events), so no "scripted input" label is needed; the sweeps are labelled "swept by script" in each lane's `videoLabel`.
- Output to `runtime/remotion/public/godot-shaders/math-toolkit/` with the file names in the table (the lanes use exactly these names).

## Godot renders

| ID | Beat | Shader (in `lab-shaders/`) | Target | Values over time | Length | File | At the 50 % mark | At the 85 % mark | Verified result to reproduce |
|---|---|---|---|---|---|---|---|---|---|
| C01 | B01 | `15-ring-final` | square (sprite route) | `radius`: 0 s = 0.12, 0.5 s = 0.12, 11 s = 0.38, 13 s = 0.38 (piecewise linear) | 13 s | `ring-grow.mp4` | radius = 0.269 | radius = 0.38 | radius 0.12: cream, teal, cream at d = 0.06, 0.16, 0.32; radius 0.38: cream at 0.32, teal at 0.42 (lab-summary.txt rows 15-ring-final-radius*) |
| C02 | B03 | `01-ramp` | rect, full frame | none (still) | still | `ramp.png` | the picture, unchanged | the picture, unchanged | x = 0.02 / 0.5 / 0.98 -> 0.0196 / 0.498 / 0.9804, red = green = blue |
| C03 | B08 | `02-step` | rect, full frame | `edge`: 0 s = 0.5, 4 s = 0.5, 6.5 s = 0.2, 10.5 s = 0.8, 12.5 s = 0.8 (piecewise linear) | 12.5 s | `step-sweep.mp4` | edge = 0.23 | edge = 0.8 | edge 0.5: 0 at x = 0.45, 1 at 0.55; edge 0.2: 0 at 0.15, 1 at 0.25; edge 0.8: 0 at 0.75, 1 at 0.85 |
| C04 | B13 | `03-smoothstep` | rect, full frame | `width`: 0 s = 0.4, 3.5 s = 0.4, 10 s = 0.03, 13 s = 0.03 (piecewise linear) | 13 s | `smoothstep-sweep.mp4` | width = 0.229 | width = 0.03 | width 0.45: 0.1255 / 0.498 / 0.8745 at x = 0.25 / 0.5 / 0.75; width 0.3: 0.0196 / 0.498 / 0.9804; width 0.03: 0 / 0.4824 / 1 |
| C05 | B15 | `04-mix-colors` | rect, full frame | none (still) | still | `mix-colors.png` | the picture, unchanged | the picture, unchanged | x = 0.02 -> (0.3804, 0.6431, 0.5686); 0.5 -> (0.6627, 0.7216, 0.5098); 0.98 -> (0.949, 0.7961, 0.451) |
| C06 | B20 | `05-fract` | rect, full frame | `count`: 0 s = 1, 4.5 s = 1, 10.5 s = 6, 12.5 s = 6 (piecewise linear) | 12.5 s | `fract-sweep.mp4` | count = 2.46 | count = 6 | count 1: 0.098 / 0.298 / 0.6 / 0.898 at x = 0.1 / 0.3 / 0.6 / 0.9; count 4: 0.3961 / 0.1961 / 0.3961 / 0.5961; count 6: 0.5961 / 0.7961 / 0.5961 / 0.3961 |
| C07 | B23 | `06-stripes` | rect, full frame | none (still) | still | `stripes.png` | the picture, unchanged | the picture, unchanged | x = 0.05 -> 0; 0.1 -> 1; 0.15 -> 0; 0.2 -> 1 (sixteen bands: eight ramps, each cut in half) |
| C08 | B29 | `08-distance` | square (sprite route) | none (still) | still | `distance.png` | the picture, unchanged | the picture, unchanged | middle 0.0039; (0.75, 0.5) 0.2471; middle of the right edge 0.4941; corner 0.7059 (exact 0.7071) |
| C09 | B31 | `09-glow` | square (sprite route) | none (still) | still | `glow.png` | the picture, unchanged | the picture, unchanged | middle 1.0; (0.75, 0.5) 0.5059; middle of the right edge 0.0; corner 0.0 |
| C10 | B33 | `07-pow` | rect, full frame | `power`: 0 s = 1, 3 s = 1, 11 s = 6, 15.5 s = 6 (piecewise linear) | 15.5 s | `pow-sweep.mp4` | power = 3.97 | power = 6 | power 1: 0.498 / 0.898 at x = 0.5 / 0.9; power 3: 0.1255 / 0.7255; power 6: 0.0157 / 0.5294 |
| C11 | B35 | `10-disk` | square (sprite route) | none (still) | still | `disk.png` | the picture, unchanged | the picture, unchanged | middle 0; d = 0.2 -> 0; d = 0.4 -> 1; corner 1; the disk spans 0.6 of the square (216 of 360 px) |
| C12 | B36 | `11-disk-flip` | square (sprite route) | none (still) | still | `disk-flip.png` | the picture, unchanged | the picture, unchanged | middle 1; d = 0.2 -> 1; d = 0.4 -> 0; corner 0 |
| C13 | B38 | `12-ring-hard` | square (sprite route) | none (still) | still | `ring-hard.png` | the picture, unchanged | the picture, unchanged | d = 0.2 -> 0; 0.34 -> 1; 0.45 -> 0 |
| C14 | B39 | `13-ring-color` | square (sprite route) | none (still) | still | `ring-color.png` | the picture, unchanged | the picture, unchanged | d = 0.2 and 0.45 -> cream (0.9804, 0.9608, 0.9216); d = 0.34 -> teal (0.3686, 0.6392, 0.5686) |
| C15 | B40 | `14-ring-soft` | square (sprite route) | none (still) | still | `ring-soft.png` | the picture, unchanged | the picture, unchanged | d = 0.2 -> cream; 0.28 -> (0.6941, 0.8118, 0.7569); 0.34 -> teal; 0.40 -> (0.6431, 0.7843, 0.7255); 0.45 -> cream |
| C16 | B41 | `15-ring-final` | square (sprite route) | `radius`: 0 s = 0.3, 6 s = 0.3, 8.5 s = 0.12, 11.5 s = 0.38, 12.5 s = 0.38 (piecewise linear) | 12.5 s | `ring-dial.mp4` | radius = 0.282 | radius = 0.304 | as C01 for the three radii; the radius 0.30 picture is identical to C15 |

Exact `--animate` options for the six sweeps:

```
C01  --animate radius:0:0.12,0.5:0.12,11:0.38,13:0.38
C03  --animate edge:0:0.5,4:0.5,6.5:0.2,10.5:0.8,12.5:0.8
C04  --animate width:0:0.4,3.5:0.4,10:0.03,13:0.03
C06  --animate count:0:1,4.5:1,10.5:6,12.5:6
C10  --animate power:0:1,3:1,11:6,15.5:6
C16  --animate radius:0:0.3,6:0.3,8.5:0.12,11.5:0.38,12.5:0.38
```

For the videos the voice and the capture are independent clocks: cues in the lane (code highlights, read-outs, rings, the ramp marker) are fractions of the measured beat; the capture just plays from its first frame.

## Screenshot

| ID | Beat | What | How |
|---|---|---|---|
| D1 | B12 | The Godot 4.7 "Built-in shader functions" page at the `smoothstep` entry, 1600 x 900 at device scale 2.4 (a 3840-wide PNG): the section heading near the top of the viewport, the two formula lines `t = clamp((c - a) / (b - a), 0.0, 1.0);` and `return t * t * (3.0 - 2.0 * t);`, and the sentence `Results are undefined if a >= b.` all visible | Playwright (BrowserCapture convention), address `https://docs.godotengine.org/en/4.7/tutorials/shaders/shader_reference/shader_functions.html#shader-func-smoothstep`; scroll the heading into view with a small top margin; caption with the capture date. Re-read the three quoted lines in the captured image: if the page wording has changed, stop and tell Bear (FACTCHECK rows 23 and 24 quote it as read on 2026-10-13) |

## Manim data (not a capture)

Every plot is drawn from `evidence/planning-checks/plot_data.py` (numpy, the same formulas the shaders compute; `dense-compare.md` proves them identical to Godot's pixels: 21 curves, largest difference 0 levels). The plots are drawings of math, not Godot captures, and the film says so once, on screen, in B04 ("curves drawn from the formulas · checked against Godot 4.7.2 renders"); the one measured number drawn (0.028, B11) also carries the credit "checked in Godot 4.7.2 · Forward+".

## Not captured on purpose

No editor frames (no Inspector is shown). No GPU or frame timing. No real-time frame-rate claim anywhere. No key events.
