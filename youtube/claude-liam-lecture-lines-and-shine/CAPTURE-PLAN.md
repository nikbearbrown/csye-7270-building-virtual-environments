# Capture plan: Lines and Shine

**What this is.** Every Godot render the build session must record for this film, with the exact shader file, target, values over time, length, renderer and the result already verified. Nothing is recorded yet; every number below comes from planning runs in `evidence/planning-checks/` (`run_lab_checks.py`, `verify1.gd`, `two_panels.gd`).
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment.
**Found.** 19 distinct captures (C01 to C20; C15 is C01 reused): 5 single-card clips, 3 stills, 7 two-panel scenes, 3 blob-sprite clips, 1 tween scene. **No editor frames and no docs screenshots are needed**, so there are no interactive editor actions for this film. All shaders compile in Godot 4.7.2 and every probe below was read in a real window on Forward+ and re-read in Compatibility (identical, or one level of 255 apart on the smooth maps).

## Conventions for all captures

- **Frame.** A 640 × 360 logical canvas, rendered at 3840 × 2160 by the Signal Garden SubViewport native-size route (`../_godot-shaders-series/COMPONENT-SPECS.md`, "Capture harness"). 30 fps, Forward+, offline fixed tick, so nothing here says anything about real-time frame rate. The Lab stage colour `#D9D5CA`.
- **The card.** Lab `sprite` kind with a plain white 128 px texture at scale 2.25: a **square card of 288 × 288 logical px centred at (320, 180)**, whose corners are (176, 36) and (464, 324). Every card shader assigns `COLOR` itself, so the whole square shows the shader. Readout positions in the lanes are fractions of the frame: `x = 0.275 + 0.45 u`, `y = 0.10 + 0.80 v` for a card address (u, v).
- **The blob.** The Lab's default teal test sprite (teal blob, two cream eyes, transparent padding), same scale 2.25, same square. Where a shine is shown the sprite's empty padding is what lets the leak show.
- **Two-panel scenes** use `evidence/planning-checks/two_panels.gd` (a verified still renderer; the build's harness animates the same scene): cards 256 × 256 logical px (scale 2.0) centred at (170, 190) and (470, 190); wide panels 304 × 171 centred at (160, 180) and (480, 180). Each panel has its own material. Left panel is always the "old" or "wrong" one.
- **Timing.** Every sweep is given as **fractions of the clip**, and the clip is cut to the beat's measured audio length (`actual_duration_s` in `beat_sheet.json`, after the audio step). The nominal length in the table is only for the first test render. Overlay cues in the lanes are fractions of the same length.
- **Labels.** A scripted run is labelled "scripted" in `videoLabel`; no capture claims real input. Every `videoLabel` names the engine and renderer.
- **Do not upscale a small capture**; record at the target size. The raw band at 89 degrees is 2 px wide on a 1728 px card: it must stay a crisp hairline, never a blur.
- Output to `brutalist.art/runtime/remotion/public/lines-and-shine/` with the file names the lanes use.

## Renders

| ID | Beat | Shader (in `lab-shaders/`) | Target and setup | Values over time (fractions of the clip) | Nominal length | At the 50 % and 85 % marks | Verified result to reproduce |
|---|---|---|---|---|---|---|---|
| C01 | B01, B27 | `11-shine-clock` | blob; angle 35, thickness 0.1 (file defaults) | driven by `TIME`; the sweep period is 2 s, so the clip is a whole number of 2 s cycles and loops seamlessly | 12 s | set the clock origin so the band is over the sprite at 50 % (`fract(TIME * 0.5)` = 0.5 there); at 85 % any phase | the clock version moves (4,780 pixels differ between two waits); the band is off the sprite at offsets ±1.5 |
| C02 | B08 | `01-signed-test` | card, still PNG | slope 0.5 | still | identical: warm upper left, cool lower right, grey strip | p = (0.40, 0.80) reads +0.593; (0.40, 0.20) reads +0.005; (0.40, -0.40) reads -0.603 (exact +0.602, -0.002, -0.599) |
| C03 | B09 | `01-signed-test` | card | slope 0 to 1.5 linearly over 0 to 100 % | 6 s | 50 %: slope 0.75; 85 %: slope 1.28 | slope 1 at 67 %: the zero strip is the diagonal |
| C04 | B11 | `02-angle-line` | card | angle 0 to 60 linearly over 0 to 100 % | 6 s | 50 %: 30 degrees; 85 %: 51 degrees | GPU slopes 0.57735 (30), 1.0 (45, at 75 %), 1.73205 (60); the strip climbs to the right |
| C05 | B12 | two panels: left `02-angle-line`, right `03-no-radians` | cards | both angle 0 to 30 over 0 to 67 %, then hold | 6 s | 50 %: 22 degrees; 85 %: 30 degrees held (left gentle and climbing, right steep and leaning the other way) | left m = 0.5774, right m = tan(30.0) = -6.40533 on the GPU; still `png/I-radians-30.png` |
| C06 | B14 | `02-angle-line` | card | angle held at 89.9 (0 to 33 %), 90.0 (33 to 67 %), 91.0 (67 to 100 %) | 6 s | 50 %: 90.0 (halves swapped); 85 %: 91.0 (still swapped) | GPU tan: +572.967, -22,877,334, -57.2901; left probe warm at 89.9, cool at 90, 90.1, 91, 100; same in Compatibility |
| C07 | B16 | `04-band-raw` | card, still PNG | angle 45, thickness 0.1 | still | identical: white band corner to corner, climbing to the right | probes at p = (0.6, 0.6), (-0.6, -0.6) and the centre read white (1.0); p = (0.5, -0.5) and (-0.5, 0.5) read grey (0.502) |
| C08 | B17 | `04-band-raw` | card | thickness 0.1; angle 0 until 28 %, 45 at 62 %, 75 at 78 %, 85 at 95 % (linear between) | 8 s | 50 %: about 30 degrees (clear band); 85 %: about 79 degrees (thin line) | widths as a percent of the card: 9.7 (0), 6.9 (45), 2.7 (75), 0.7 (85), 0.0 (89, 90); at 4K size 7.04, 2.64, 0.93, 0.12, 0.0 |
| C09 | B20 | `05-band-true` | card, still PNG | angle 45, thickness 0.1 | still | identical: the same band, 10 percent wide | measured width 9.8 percent (theory 10.0) |
| C10 | B21 | two panels: left `04-band-raw`, right `05-band-true` | cards, thickness 0.1 | both angle 0 until 20 %, 15 at 30 %, 45 at 35 %, 75 at 40 %, 85 at 44 %, hold to 100 % | 8 s | 50 % and 85 %: 85 degrees held (reached at 44 %): left a hairline (0.9 %), right the full band (10 %) | raw 9.7 / 6.6 / 2.4 / 0.8 percent, true 9.7 / 10.0 / 9.7 / 10.2 percent at 15 / 45 / 75 / 85 degrees (256 px cards) |
| C11 | B22 | `07-slide` | card | thickness 0.1; angle 35 with offset -0.8 to 0.8 over 5 to 40 %; hold to 55 %; angle 70 with offset -0.8 to 0.5 over 55 to 80 %; hold | 8 s | 50 %: first sweep finished (band at the lower right, 35 degrees); 85 %: 70 degrees, offset 0.5 held | offset ±0.5 moves the band ±72.0 px = 0.250 of the card at 0, 35 and 70 degrees (measured ±72.01, ±72.10, ±71.83) |
| C12 | B23 | two panels: left `08-center-shift`, right `07-slide` | cards, angle 0, thickness 0.1 | left `center.x` -0.6 to 0.6, right `offset` -0.6 to 0.6, both over 30 to 78 % | 8 s | 50 %: sweeps part-way (left band centred, right band just above centre); 85 %: right band at the bottom, left still centred | left centre moves 0.0 px; right moves 77.0 px at 0.6 (card 256 px) |
| C13 | B24, B25 | `09-shine-leak` | blob; angle 35, thickness 0.1 | offset -1.5 to 1.5 linearly over 0 to 100 % | 6 s | 50 %: offset 0, band through the middle and out to both edges of the square (the leak is visible); 85 %: offset 1.05, band in the lower right crossing empty padding | an empty pixel on the band line reads (1.0, 1.0, 1.0); the blob centre reads white where the band is |
| C14 | B26 | two panels (blobs): left `09-shine-leak`, right `10-shine` | blobs, angle 35, thickness 0.1 | both offset -1.5 to 1.5 over 5 to 95 % | 6 s | 50 %: both bands mid-sprite (left extends past the blob, right stays on it); 85 %: offset about 1.2 | the fixed panel's empty pixel on the band line equals the stage colour (0.851, 0.8353, 0.7922) |
| C15 | B27 | (C01 again) | (C01) | (C01) | | | |
| C16 | B28 | `10-shine` + scene script | blob named `Sprite`; root script is exactly the four lines shown on screen; the harness calls `shine()` at 1.0, 4.0, 7.0 and 10.0 s | the call sets offset -1.5 and tweens to 1.5 over 0.8 s; resting offset is the shader default -2.0 | 12 s | 50 %: at rest (the 4.0 s sweep ended at 4.8 s); 85 %: 0.2 s into a sweep | band covers the blob centre about 0.39 to 0.43 s after each call (0.388 to 0.429 in the final run); offset ends at 1.5; label "scripted call" always on screen |
| C17 | B29 | `10-shine` | blob; angle 35, thickness 0.1 | offset -1.5 to 1.5 over 10 to 90 % | 8 s | 50 %: offset 0, band mid-sprite; 85 %: offset about 1.3, the band past the blob (resting) | band on the blob at offset 0; off the sprite at ±1.5 |
| C18 | B30 | two wide panels: left `05-band-true`, right `06-wide-fix` (aspect 1.7778) | 304 × 171 panels, thickness 0.1 | both angle 0 to 45 over 5 to 38 %, then hold | 8 s | 50 % and 85 %: 45 degrees held: left shallow (29 degrees on screen), right a true diagonal | 29.2 degrees without the fix, 44.7 with it; thickness drifts 17.8 (20 degrees), 20.8 (45), 27.1 (70) px without the fix and stays 17.1 (16.9 to 17.1) with it (panel scale) |
| C19 | B34 | two panels: left `05-band-true`, right `12-direction` | cards, thickness 0.1 | both angle 0 to 89 over 5 to 95 % | 8 s | 50 %: about 45 degrees; 85 %: about 80: the two bands identical at both marks | 0 of 230,400 pixels differ at 30, 60 and 89 degrees; the direction form draws a centred 10 percent band at exactly 90 |
| C20 | B35 | two panels: left `02-angle-line`, right `13-direction-signed` | cards | both angle held at 89.9 (0 to 33 %), 90.0 (33 to 67 %), 91.0 (67 to 100 %) | 6 s | 50 %: 90.0, left halves swapped, right unchanged; 85 %: 91.0 | left swaps between 89.9 and 90 in both renderers; right keeps the same sides from 80 to 100 degrees |

Harness features this list needs. The spec already has `--animate name:t0:v0,t1:v1,...` (piecewise linear), `--material-at`, `--set-at` and PNG-sequence output then ffmpeg to MP4; this film adds: keyframes given as fractions of the clip (convert with the beat's measured length), `--animate` per panel, a scene option that loads `two_panels.gd`, a scripted call at given times (C16) and a clock-origin option for `TIME` (C01). Stills are PNG (C02, C07, C09).

## Stills already rendered and checked (planning runs)

`evidence/planning-checks/png/` holds the 640 × 360 Lab renders the table refers to (`A1-signed-slope-0.5.png`, `C-02-angle-30.png`, `D-raw-45.png`, `D-true-45.png`, `E-slide-*.png`, `F-fixed-*.png`, `F-leak-*.png`, `H-wide-*.png`, `I-*.png` for the two-panel scenes). A captured frame can be compared against them directly.

## Editor frames and docs screenshots

None. No claim in this film rests on the Inspector or on a captured web page.

## Not captured on purpose

No GPU timing, no frame-rate claim, no performance claim. No shader here is shown running on a device other than this Mac (Apple M4 Pro); the one hardware-dependent number (the tangent at exactly 90 degrees) is spoken and labelled as this Mac's.
