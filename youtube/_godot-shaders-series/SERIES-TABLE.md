# Series table (generated)

**What this is.** One row per film, read from the films' own files by `series_table.py`: beats, words, estimated minutes at Liam's measured pace, lanes, open fact-check rows, and the first line of each film's cut line.
**Why.** So the plan's numbers are the layouts' numbers.
**Found.** See the totals line at the bottom. Minutes are an estimate from word count (0.34 s per word plus the fixed opening and closing); the real length is known after the voice is generated.

| Film | Beats | Words | Est. min | Lanes (manim / capture / remotion / editor) | OPEN rows | Lint |
|---|---|---|---|---|---|---|
| **Foundations** | | | | | | |
| Godot Shaders | 49 | 1868 | 10.7 | 18 / 17 / 6 / 2 | 0 | clean |
| Godot Shader Language | 47 | 1918 | 10.9 | 22 / 8 / 6 / 0 | 0 | clean |
| The Shader Math Toolkit | 47 | 1815 | 10.4 | 23 / 16 / 2 / 0 | 0 | clean |
| Textures and Color | 47 | 1918 | 10.9 | 7 / 27 / 4 / 3 | 0 | clean |
| Shaders in 3D | 50 | 1814 | 10.3 | 14 / 24 / 5 / 1 | 0 | clean |
| **Fragment techniques** | | | | | | |
| UV Space | 48 | 1812 | 10.3 | 17 / 19 / 6 / 0 | 0 | clean |
| Patterns and Pixelation | 49 | 1790 | 10.2 | 18 / 22 / 3 / 0 | 0 | clean |
| Drawing Shapes with Math | 50 | 1900 | 10.8 | 15 / 25 / 3 / 1 | 0 | clean |
| Soft Edges, Glow and Noise | 48 | 1791 | 10.2 | 15 / 23 / 2 / 2 | 0 | clean |
| Time and Waves | 46 | 1690 | 9.6 | 18 / 18 / 4 / 0 | 0 | clean |
| Trigonometry for Shaders | 46 | 1752 | 10.0 | 23 / 13 / 4 / 0 | 0 | clean |
| Lines and Shine | 41 | 1587 | 9.1 | 14 / 21 / 0 / 0 | 0 | clean |
| Outlines | 47 | 1868 | 10.7 | 11 / 27 / 3 / 0 | 0 | clean |
| **Vertex and space** | | | | | | |
| Vertex Shaders | 46 | 1730 | 9.9 | 12 / 27 / 0 / 0 | 0 | clean |
| Matrices and Fake 3D | 47 | 1791 | 10.2 | 22 / 15 / 4 / 0 | 0 | clean |
| Local, World and Screen Space | 46 | 1779 | 10.1 | 24 / 12 / 2 / 1 | 0 | clean |
| **Screen, textures and light** | | | | | | |
| Reading the Screen | 44 | 1685 | 9.6 | 11 / 25 / 2 / 0 | 0 | clean |
| Reflections | 43 | 1557 | 8.9 | 12 / 19 / 4 / 2 | 0 | clean |
| SubViewports | 46 | 1840 | 10.5 | 16 / 22 / 0 / 2 | 0 | clean |
| Light Shaders | 46 | 1808 | 10.3 | 12 / 25 / 3 / 0 | 0 | clean |

**Totals.** 20 films, 933 beats, 35,713 words, about 204 minutes (3.4 hours) of film; 0 OPEN fact-check rows in all.

## Cut lines (what moves out if a film runs long)

- **Godot Shaders.** Cut, in this order: the budget-bars beat (B05), then the typo beat (B32), the editor-slider beat (B27) and the tween beat (B33): each repeats an idea another beat already carries. The vertex-lean pair (B16, B17), the discard beat (B20) and the iris build (B42, B43) stay: they are the proof and the payoff.
- **Godot Shader Language.** Cut, in this order: the overloading beat (B27), the two-performance-notes beat (B33), the global-built-ins half of B24 (keep the pass-it-in half), and the ternary beat (B29): each repeats an idea another beat already carries or is an extra. The vectors-and-swizzles beats (B12 to B17), the signature and built-in beats (B20, B23), and the whole reading act (B34 to B41) stay: they are the film.
- **The Shader Math Toolkit.** Cut, in this order: the toolkit map (B06), the sine beat (B34), the normalize beat (B27), the soft-spot beat (B31), the smooth step docs beat (B12) and the floor-only beat (B21). Each repeats or previews an idea carried elsewhere. The plot-reading pair (B04, B05), the smooth step correction (B11), the whole-and-leftover split (B22), the mod trap (B25) and the whole ring build (Act V) stay: they are the method, the two corrections and the payoff. A cut beat also leaves its name in the recap line (BVDT_LINES[3] for normalize and sine), so trim that line and its spoken twin too.
- **Textures and Color.** Cut, in this order: the tween beat (B26), the brighten beat (B13), the alpha-hole beat (B12), the gray pair (B14, B15), then the from-code beat (B36): each extends an idea another beat already carries. The dissolve build (B19 to B25), the two-renderer reveal (B27 to B31) and the hint rules (B33 to B39) stay: they are the film.
- **Shaders in 3D.** Cut, in this order: the tween beat (B28), the cull beat (B17), the two-questions beat (B18), the output-is-s R G B beat (B42) and the missing-functions beat (B35): each repeats an idea another beat carries. The lit sphere (B11), the unshaded pair (B14), the box reveal (B36) and the two-renderer comparison (B37 to B41) stay: they are the film's proof.
- **UV Space.** Cut, in this order: the node-setting beat (B16, a second route to the same repeat switch), the transparent-border beat (B37), the stretched-pixel beat (B31), the fold drawing (B26) and the gate drawing (B39: the mask then takes one beat, B38). Each repeats or decorates an idea another beat already carries. The reversal beats (B09 to B11), the centered zoom (B19 to B21), the oval and its fix (B28, B29, B32, B33) and the mask result (B40) stay: they are the proof and the payoff.
- **Patterns and Pixelation.** Cut, in this order: the scale beat (B24), the worked example (B16) and the diagonal-step beat (B28), then merge the moving stripes (B33) into the stripes beat (B32). Each repeats an idea another beat already carries. The drift pair (B13, B14), the rounding pair (B17, B18), the wide-shape trap (B39, B40) and the dot screen with its edge check (B41, B42) stay: they are the proof and the payoff.
- **Drawing Shapes with Math.** Cut, in this order: the ring-in-numbers table (B13), the hard-edge beat (B34), the second numbers table (B16), then one of the three dial-sweep beats (B42: arm width and arm gap move into B41). The min and max act shrinks to the sum bug and its fix (B14, B15, B17) plus one beat for the negative case (B18 and B19 merge). The circle by hand (B04, B08), the cross by max (B23), and the crosshair build (B35 to B38) stay: they are the idea and the payoff.
- **Soft Edges, Glow and Noise.** Cut, in this order: the reveal-pace beat (B32), the beat on what else H D R two D changes (B40), the swapped-lines beat (B10) and the beat on glow without H D R two D (B41). Each is a true caveat that another beat or the docs already carry. The S-curve pair (B05, B06), the parentheses pair (B21, B22), the seam pair (B29, B30), the two glow runs (B36, B37) and the finale (B42) stay: they are the proof and the payoff.
- **Time and Waves.** Cut, in this order: the two-waves beat (B34), the roll-over beat (B04), the edge-smear beat (B33) and the sine-or-ramp beat (B24): each extends an idea another beat already carries. The late-join demo (B01), the clock-mixing pair (B05, B06), the three knob beats (B14 to B16), the travel beat (B28) and the wind click (B40) stay: they are the proof and the payoff. The curve-texture pair (B22, B23) stays because the breathing logo reads one; if both must go, the logo breathes from a sine and B36 to B38 shrink to two beats.
- **Trigonometry for Shaders.** Cut, in this order: the flower beat (B40), the three-moons beat (B23), the arm beat (B30) and the oval-limit beat (B24): each is a bonus that repeats an idea another beat already carries. Then the start-at-the-top beat (B39). The triangle-to-circle beats (B06, B07), the orbit (B19 to B21), the meteor (B26 to B29) and the worked pixel with the sweep (B37, B38) stay: they are the proof and the payoff.
- **Lines and Shine.** Cut, in this order: Act V (B31 to B35), and with it the last sentence of B14, which promises it; then the center-shift beat (B23); then fold B16 and B17 into one beat (the band, then the tilt). The wide-shape limit (B30) stays unless the film is far over: it is the honest edge of the whole method. The shine itself (B01, B22, B24 to B29) never goes.
- **Outlines.** Cut, in this order: the line-color beat (B14), the loop-cost beat (B22), the branch beat (B24), the modulate beat (B40), then the thin-part beat (B37) and the brush-number beat (B35). The corner beat (B17), the padding beats (B29 to B31) and the checks table (B41) stay: they are the proof and the payoff.
- **Vertex Shaders.** Cut, in this order: the color-shortcut beat (B33), the flat beat (B30), the wind beat (B25), the polygon-needs-a-texture beat (B38) and the upside-down beat (B35): each repeats a lesson another beat already carries or is a trap rather than the main line. The four-corner tilt (B12), the pair (B17), the travelling and pinned flag (B21, B22) and the lit flag (B32) stay: they are the proof and the payoff.
- **Matrices and Fake 3D.** Cut, in this order: the order-swap pair (B22, B23), the corner spin (B38), the two-turns beat (B31) and the card-versus-box beat (B33): each repeats an idea another beat already carries. The columns trio (B04 to B06), the product-order beat (B21), the flip itself (B28, B29) and the door (B35, B41) stay: they are the stumbling blocks and the payoff.
- **Local, World and Screen Space.** Cut, in this order: the hole beat (B24), the wrong-order beat (B29), the turn-and-stretch beat (B22) and the parents warning (B11): each repeats an idea another beat carries, and none leans on its neighbours. Only if that is not enough, drop the frag coord beat (B31) and its tile in capture C10, and change 'four' to 'three' in B26 and B33 and the counting words in B30 to B32 (re-voice those beats). The sky window (B21), the world colors (B16), the four-tile agreement (B33) and the two-move test (B36, B37) stay: they are the proof and the payoff.
- **Reading the Screen.** Cut, in this order: the symptom table (B38), the finale (B37), the mouse-filter beat (B13), the edge-and-filter beat (B36) and the frosted-glass beat (B25): each repeats an idea another beat already carries, or adds a habit rather than the idea. The window (B03 to B09), the spotlight with its oval fix (B16 to B20), the pool (B27 to B29) and the overlap with its fix (B32, B33) stay: they carry the idea.
- **Reflections.** Cut, in this order: the renderer-table beat (B31), the color-distance picture (B32), then the polish pair (B34 coast, B35 tint), then the canvas-layer beat (B15). Each repeats an idea another beat carries or covers a rarer case. The hidden-map idea (B03 to B09), the copy positions (B12, B13), the rect trap (B17), the lookup and its code (B22, B23), the map toggle (B24) and the equals failure (B28, B29, B30) stay: they are the proof and the payoff.
- **SubViewports.** Cut, in this order: the input beat (B39), the update-mode beat (B38), the three-in-a-row beat (B37), the per-pixel beat (B20), then the hue beats (B26 to B29), keeping the stripes at one color. The origin and cut-off pair (B07, B08), the dark-edges beat (B10), the predict-and-reveal pair (B16, B17) and the wobble beats (B33 to B35) stay: they are the proof and the payoff.
- **Light Shaders.** Cut, in this order: the grid beat (B39), the stripes beat (B38), the pulse beat (B16), then the limits beat (B18). Each repeats an idea another beat already carries, or sits outside the film's one idea. The rebuild (B13), the lighthouse (B26) and the expanding ring (B36) stay: they are the proof and the two payoffs.
