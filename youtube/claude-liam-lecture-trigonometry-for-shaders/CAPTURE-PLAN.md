# Capture plan: Trigonometry for Shaders

**What this is.** Every Godot render and Godot-docs screenshot the build session must record for this film, with the exact shader file, target, values over time, duration, renderer, what must be on screen at the 50 % and 85 % marks, and the result already verified. Nothing is recorded yet; every number below comes from planning runs in `evidence/planning-checks/`.
**Why.** Films show only what was really done and recorded. This is the list of things to really do, written so a medium-effort session can do them without further judgment.
**Found.** 13 Godot renders (all one-shader Shader Lab renders: 4 stills and 9 clips; 3 clips use a scripted uniform schedule), 2 docs screenshots, **no editor frames and no editor actions**, no scripted key or mouse input. All 12 shaders shown on screen compile and run in the Lab; every probe value below was read in a real Godot 4.7.2 window on Forward+ (and the plain-colour ones also on Compatibility with identical pixels).

Conventions for all captures:

- 30 fps, offline at a fixed tick rate, so nothing here says anything about real-time frame rate. Live `TIME` clips start at `TIME = 0` on the first captured frame (the moon starts at the right, angle 0) and advance 1/30 s per frame.
- Renderer: Forward+ (say so in `videoLabel`; the lanes already do).
- Square renders: a **480 × 480** logical canvas captured at **1920 × 1920** (the SubViewport native-size route in `../_godot-shaders-series/COMPONENT-SPECS.md`, so the shader is evaluated per output pixel and nothing is upscaled). Wide render (C06): a **640 × 360** logical canvas captured at **1920 × 1080**. The shaders' discs have hard edges on purpose; do not blur them.
- Stage: the rect shaders paint their own warm grey (0.85, 0.84, 0.79); the sprite renders (C11, C12) show the Lab clear colour `#D9D5CA`.
- Every clip is captured at least one second longer than its beat's measured audio (the lane's `durationSeconds` is filled from the audio at build time). Where a value is scripted it is given as a fraction of the beat; compute seconds from the measured audio. A scripted value is labelled "scripted" in the clip's `videoLabel` (the lanes already do).
- **Sprite renders (C11, C12).** The Lab's test sprite is 128 px drawn with nearest-neighbour filtering; at 1920 px that is 15 captured pixels per texel and the blob's edge would look blocky. Have the harness draw the same teal blob with its two cream eyes at 512 px with linear filtering (the sprite is made by code in `lab/runner.gd`, so this is a parameter, not a new asset). The shader reads `texture(TEXTURE, UV)`, so nothing in the file changes; check that the verified probe pairs below still read teal inside the blob and stage outside.
- Output goes to `runtime/remotion/public/godot-shaders/` with the file names the lanes use.
- Probe positions are fractions of the captured frame (u across, v down), so every probe below also works on the 1920-pixel capture.

## Godot renders

| ID | Beat | Shader (in `lab-shaders/`) | Target and setup | Values over time | Length | Verified result to reproduce | On screen at the 50 % and 85 % marks |
|---|---|---|---|---|---|---|---|
| C01 | B01 | `06-meteor-orbit` | rect, square; layout `video` | live `TIME`, no input | 14 s | Planet (0.369, 0.639, 0.569) in the middle; moon (0.502, 0.600, 0.749) on a ring at 0.600 of the half-width, +1.00 rad/s clockwise; meteor (0.902, 0.651, 0.251) at 0.2 from the moon, +3.00 rad/s around it; stage (0.851, 0.839, 0.788) | All three bodies visible and never overlapping (the meteor stays 0.2 from the moon, more than the sum of their radii) |
| C02 | B19 | `01-moon-fixed` | rect, square, still PNG | none | still | Moon (0.502, 0.600, 0.749) at uv (0.7598, 0.65); the y-up mirror spot (0.7598, 0.35) is empty stage; planet at (0.5, 0.5) | Same still |
| C03 | B21 | `02-orbit` | rect, square | live `TIME` | 14 s | Moon +0.99 to +1.00 rad/s clockwise at a constant 0.600 of the half-width; a lap takes 6.28 s | Moon anywhere on its ring, planet in the middle |
| C04 | B22 | `03-orbit-fast` | rect, square | live `TIME` | 12 s | Moon +2.00 rad/s clockwise (lap 3.14 s) | Same |
| C05 | B23 | `05-moons-evenly` | rect, square | live `TIME` | 12 s | Three moons, gaps 120.0, 120.0, 120.0 degrees, +1.00 rad/s clockwise | Three moons and the planet |
| C06 | B24 | `04-orbit-aspect` | rect, **wide** (640 × 360 logical, 1920 × 1080 captured); layout `stack` | scripted `aspect`: 1.0 until 0.58 of the beat, linear to 1.7778 by 0.82, then held; live `TIME` | 16 s | Planet 160 × 90 px on the 640 × 360 view at aspect 1.0 (an oval, ratio 1.778) and 90 × 90 px at 1.7778 (round); at 1920 × 1080 that is 480 × 270 then 270 × 270 | 50 %: oval planet and a sideways-stretched orbit; 85 %: round planet and round orbit, readout "aspect 1.78" |
| C07 | B28 | `06-meteor-orbit` | rect, square; layout `video` | live `TIME` | 14 s | As C01 (the same file: the clip may reuse C01's frames cut to length) | Same as C01 |
| C08 | B29 | `07-meteor-reverse` | rect, square | live `TIME` | 14 s | Moon +1.00 rad/s clockwise; meteor around the moon -3.00 rad/s (counterclockwise) | Moon and meteor visible |
| C09 | B35 | `08-atan-colors` | rect, square, still PNG | none | still | Right (0.635, 0.643, 0.412), down (0.769, 0.647, 0.329), up (0.502, 0.643, 0.490); seam: just above the left axis teal (0.373, 0.639, 0.569), just below amber (0.898, 0.651, 0.251) | Same still: the conic picture with its hard edge along the left half of the horizontal axis |
| C10 | B36 | `09-atan-one-argument` | rect, square, still PNG | none | still | Lower right and upper left both (0.769, 0.647, 0.329); upper right and lower left both (0.502, 0.643, 0.490) | Same still: the butterfly |
| C11 | B38 | `10-sweep` | sprite (the Lab's teal test sprite, 128 px scaled to 0.8 of the canvas), square | scripted `sweep`: 0.30 until 0.68 of the beat, then 0.0, then linear to 1.0 by 0.97, then held | 16 s | At sweep 0.5 the upper half of the blob is shown (upper-left and upper-right probes teal (0.373, 0.639, 0.569)) and the lower half hidden (stage (0.851, 0.835, 0.792)); at sweep 0.3 only the upper-left probe is shown; the pixel p = (-0.3, -0.3) is hidden at 0.12 and shown at 0.13 | 50 %: sweep 0.30 held, a wedge of the blob from the left to about 10:48 o'clock shown; 85 %: sweep about 0.59 |
| C12 | B39 | `11-sweep-top` | as C11 | scripted `sweep`: 0.30 until 0.60 of the beat, then 0.0, then linear to 1.0 by 0.97, then held | 16 s | At sweep 0.5 the right half is shown (upper-right and lower-right probes teal) and the left half hidden; at 0.3 only the upper-right probe is shown | 50 %: sweep 0.30 held, a wedge from twelve o'clock clockwise (about 108 degrees); 85 %: sweep about 0.68 |
| C13 | B40 | `12-flower` | rect, square | live `TIME` | 14 s | Eight petals; edge radius between 0.398 and 0.700 of the half-width; the pattern turns +1.00 rad/s clockwise | The flower, petals clearly separate |

Upper-left, upper-right, lower-right and lower-left probes for C11 and C12 are the four points at uv (0.36, 0.36), (0.64, 0.36), (0.64, 0.64), (0.36, 0.64) of the sprite, inside the blob and away from its eyes. Harness features this list needs (all in `../_godot-shaders-series/COMPONENT-SPECS.md`): `--size` for the square and wide canvases, live `TIME`, a piecewise `--animate` schedule (C06, C11, C12), still PNG output, PNG sequence then ffmpeg to MP4.

## Editor frames and editor actions

None. This film shows no editor window; every Godot picture is a one-shader Lab render. (So nothing from this film goes into the series' editor recording script.)

## Screenshots

| ID | Beat | What | How |
|---|---|---|---|
| D1 | B08 | The Godot 4.7 `Vector2` class page at `from_angle()`: `https://docs.godotengine.org/en/stable/classes/class_vector2.html#class-vector2-method-from-angle` (anchor id verified to exist). The camera pushes in on "This is equivalent to doing Vector2(cos(angle), sin(angle)) or Vector2.RIGHT.rotated(angle)." | Playwright (BrowserCapture convention): 1600 × 900 at device scale 2.4, scrolled so the `from_angle()` entry sits in the upper third and its description is legible; caption with the capture date; set the lane's `moves` and `ring` from the real screenshot |
| D2 | B33 | The Godot 4.7 built-in functions page at the two-argument `atan(y, x)` entry: `https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_functions.html#shader-func-atan2` (the anchor id `shader-func-atan2` is the `atan(vec_type y, vec_type x)` entry; `shader-func-atan` is the one-argument entry just above it). The camera pushes in on "Calculates the arc tangent given a numerator and denominator. The signs of y and x are used to determine the quadrant that the angle lies in." and the return line "in the range [-PI, PI]" | As D1. Read the entry in the capture and change nothing the page says; if the 4.7 page has been reworded since 2026-10-13, say what it says now in `BUILD-LOG.md` and re-check FACTCHECK rows 11 and 49 |

## Not captured on purpose

No GPU timing and no real-time frame-rate claim anywhere (the Lab's captures are offline). No editor frames, no live editor session and no keyboard or mouse input. No Compatibility-renderer capture (the pixels match Forward+ for these shaders: FACTCHECK row 64).
