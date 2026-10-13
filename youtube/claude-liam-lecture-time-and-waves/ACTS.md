# Acts and coverage map: Time and Waves

**What this is.** How this film is built from its brief and its source: which idea lands in which act and beat, what was left out and why, what was added that the brief did not ask for, the cast per act, the opening correction, the terms card, where every term is defined on screen, and the cut line.
**Why.** Bear split a long shader course into films of at most 15 minutes, preferably about 10 (2026-10-13). A split only works if every idea has a home. This file is the record that nothing was dropped silently.
**Found.** Five acts, 40 body beats, about 9.6 minutes. The film follows the brief's five acts and adds one idea the brief only hinted at: a single model that ties them together (`TIME` times `speed` counts cycles; a shape function turns the count into a look). Three things in it come from running, not reading: the tick counter and `TIME` have different zeros and drift apart (B05, B06), the roll-over jumps only the pulses that do not fit it (B04), and a tween on a uniform fails unless the uniform was set first (B40). One deviation from the brief is deliberate and listed under "Cut line".

## The source (third-party; nothing copied)

A long third-party shader course (the `TIME` node, the waves chapter and the flag; about 25 minutes of it) and the fade-in at the end of a short third-party introduction (`TIME / duration`, then a Tween). The creators are not named in the brief. No sentence, demo or variable name was reused: every demonstration was rebuilt and run. See `SOURCES.md`.

## The model the film teaches (this is the film's own framing)

- `TIME` is seconds on one clock. `TIME * speed` counts **cycles** (one cycle is one full swing).
- A **shape function** turns the count into a look: a sine (`sin(TAU * cycles)`), a sawtooth (`fract`), a triangle (a folded sawtooth) or a curve you draw (`CurveTexture`).
- Four numbers describe a sine wave: **amplitude** (how far from its middle), **speed** (how quickly the count runs), **offset** (where in its cycle it starts, counted in cycles) and **frequency** (how many cycles fit across a shape). Speed multiplies `TIME`; frequency multiplies position. The 0.5 lift that fits a sine into zero to one is a step, not a fifth number.
- Feed the count from position and the wave travels across a shape; for a one-time effect, drive a uniform instead.

## Coverage of the brief

| Brief item | Where it goes | Note |
|---|---|---|
| Act 1: `TIME` is global, since the engine started (docs) | **Act I**, B01 (a late node joins in step), B02 (docs row, why a shader needs a clock) | The pilot's bars demo is not repeated: this film's demo is a pulse, and the evidence is new (`verify1_clocks.gd` B) |
| Time scale affects it; pausing does not (verify both) | **Act I**, B03 | Measured: rate 0.504, 0.504, 0.506 at a time scale of 0.5; 1.002, 1.001, 1.000 paused; Movie Maker scene C03 shows both |
| Rollover: 3,600 s default; the setting's name | **Act I**, B04 | `rendering/limits/time/time_rollover_secs`, default read from the engine (3600). Added from running: only pulses that do not fit the limit jump (`verify5_rollover.gd`) |
| The standard fix for per-object timing: a uniform you set | **Act I**, B07 (an age counted from delta) and B08 (which clock for which job); **Act II**, B17 and B18 (a per-node offset as an instance uniform) | Two answers for two jobs: an age for "starts when the node does", an offset for "out of step with the others" |
| Why `Time.get_ticks_msec()` is not `TIME`'s origin (measure) | **Act I**, B05, B06 | Measured: the zeros differ by 0.26, 0.29, 0.26 s (a first cold launch read 0.75), and one second at half speed adds exactly 0.5 s to the gap |
| Act 2: `sin(TIME)` plotted; range -1 to 1 | **Act II**, B09, B10 | `TAU` is introduced here, because the number the sine wants is an angle (docs: radians) |
| Normalize with `0.5 + 0.5 * sin(x)` | **Act II**, B11 (why: negative colors clamp to zero), B12 (how: halve, then lift), B13 (as a shader with `mix`) | B11 is added: the failure that motivates the fix, measured |
| The four knobs on a plot, each moved in turn | **Act II**, B14 (amplitude), B15 (speed), B16 (offset); **Act IV**, B27 (frequency), B30 (all four) | Frequency waits until the wave has a shape to travel across: for a single pulse it would be the same number as speed |
| `amp * sin(freq * x + phase) + offset` and `x = u * freq - TIME * speed` | **Act IV**, B27, B28 as `(UV.x - TIME * speed) * frequency + offset` | Written so the knobs do not interact (the crest moves exactly `speed` shape-widths a second whatever the frequency: measured) |
| Act 3: `fract(TIME * speed)` is a restarting ramp | **Act III**, B19 | |
| `abs(fract(...) * 2.0 - 1.0)` ping-pongs | **Act III**, B20 | Written as `1.0 - abs(fract(c) * 2.0 - 1.0)` so the triangle starts at zero like the other two |
| `CurveTexture` sampled with `texture(curve, vec2(t, 0.0)).r` | **Act III**, B22 (the idea), B23 (the lookup, live) | Verified to about one percent; the resource is made in a script, so no editor frame is needed |
| Why a symmetric curve plays forward then backward | **Act III**, B24 (sine-fed against ramp-fed) | Verified: the sine-fed sequence is palindromic, the ramp-fed one is not |
| Act 4: the traveling wave added to a vertical offset or the sampling address | **Act IV**, B27, B28 (brightness), B31 (the sampling address) | |
| Multiplying by `UV.x` pins the left edge (a flag) | **Act IV**, B32 | Verified: the leftmost 12 columns move less than a tenth of the rightmost 60 |
| Water-style wobble by offsetting the address in the fragment stage | **Act IV**, B29 (rings from distance), B31 (the wobble), B34 (two waves added) | No new vertices needed; the limit is B33 (the outline does not bend, edge pixels smear) |
| Act 5: a logo that breathes (scale from a custom curve) and a banner whose wave travels | **Act V**, B35 to B40 | The scale is done in the fragment stage by looking the picture up from closer in (B37), so no geometry moves |
| Source: `sin(TIME)` added to `VERTEX.x` times 20 | **LEFT OUT** | Vertex-stage waves on a mesh are another film's subject (the brief's "Other films cover") |
| Source: normalized curve formula worked with three inputs by hand | Replaced | The plot (B09 to B12) and the cycle count do the same job without the hand arithmetic |
| Source: scaling the whole vertex by the normalized curve | Replaced | B36 to B38 scale in the fragment stage instead; the picture stays inside its rectangle |
| Source: a speed uniform | **Act II**, B15, B17 | |
| Source: the flag with cosine on x and an "incline" | Flag kept (B32, B39); cosine and incline **LEFT OUT** | They belong to the vertex-stage flag |
| Intro video: fade with `TIME / duration`, then with a Tween | **Act I**, B07 (an age replaces `TIME / duration`); **Act V**, B40 (a tween on a uniform) | |
| Facts to verify (docs; scratch runs; Lab) | `FACTCHECK.md` | All checked; none OPEN |
| Captures: pulse, breathing logo, traveling-wave banner, time-scale and pause scene | `CAPTURE-PLAN.md` | C13, C38, C39 and C03, plus fourteen more |
| "Other films cover": vertex waves, sin and cos on a circle, the pilot's clock | Not covered here | The film re-teaches `TIME` in four beats (B01 to B04) because it must stand alone |

## Corrections to the sources and the brief (detail in FACTCHECK.md)

- **`TIME` is not time since the node or scene was created.** It is one clock for the whole game (B01, B02).
- **Offset has one meaning.** The brief's formula used "offset" for a vertical shift and the text used it for "where it starts"; the film means the second, counted in cycles.
- **Terms card.** The brief listed Sine, Amplitude, Frequency and Offset; the lecture skill keeps the card to prerequisites, so amplitude, speed, offset and frequency are earned in their acts.
- **Cut line.** The brief suggested cutting the curve-texture beat and the second knob demo. Here the breathing logo of the payoff reads a curve, and speed is half the model, so both stay; a different set is named below.

## Added: in neither the brief nor the source (each checked in FACTCHECK.md)

1. A shader cannot store anything between frames, which is why it is handed a clock (B02; docs quote).
2. The roll-over only jumps pulses that do not fit it (B04), measured with the limit at two seconds.
3. The tick counter's zero and speed differ from `TIME`'s, with numbers (B05, B06).
4. A negative color is clamped to zero, so a raw sine would sit at its darkest for half of each swing (B11).
5. Per-node offsets with an instance uniform, so one material makes five pulses roll along a row (B17, B18).
6. Rings from the distance to the middle: the same four numbers fed a different count (B29).
7. The ripple's limit, edge smear, and the margin that avoids it (B33, B38).
8. Two waves added (B34).
9. A tween on a uniform fails if the uniform was never set from code (B40), found by a run.

## Cast per act (the same object is the same picture within an act)

| Act | Recurring objects |
|---|---|
| I One Clock | the pair of pulse squares (teal and cream); the marker on its track (B03); the two rulers, tick counter above and `TIME` below (B05, B06) |
| II The Wave | the plot (time along x, value up the side) with its terracotta dot; the 0 to 1 ramp strip with its marker (greys only); the pulse square; the row of five squares |
| III Loops and Curves | the ramp strip with its marker; the sawtooth and triangle on the same axes; the three bars; the breath curve and its strip |
| IV Waves on a Shape | the wide stripe banner and the checker picture; the address strip 0 to 1; the four sliders |
| V One Clock, Two Effects | the breathing logo (the teal test sprite) and the striped banner |

Colors: the Lab stage `#D9D5CA`; teal `#5FA391` (the test sprite's color), cream `#FAF9F5`; terracotta only as dots, rings and sparks, never as text; no large near-black fields.

## Opening correction and terms

- **BIDEA**: the writer types "TIME starts at zero when my node appears." and replaces "when my node appears" with "when the game starts". (The brief's `BIDEA_TEXT` put a line break inside the trigger phrase, so the correction could never fire; the break now sits before it.)
- **BDEFS** (prerequisites only, six): Shader, fragment(), Uniform, UV, Texture, Sine. The terms this film exists to teach are earned in their acts.

### Where each term is defined on screen (glossary wording where the glossary has one)

| Term | Beat | On-screen wording |
|---|---|---|
| TIME | B01 (caption), B02 (docs row) | "TIME · seconds on one clock shared by the whole game" (glossary) |
| time scale | B03 | "time scale: how fast the game's clock runs · 1 is normal" |
| roll-over | B04 | "wraps back to 0 · a project setting" |
| tick counter | B05 | "Time.get_ticks_msec(): milliseconds since the engine started" (docs) |
| delta, age | B07 | "delta: seconds since the last frame" (docs); "age: seconds since this node appeared" |
| tau | B09 | "TAU = 6.28 · one full turn" (docs: "the number of radians in a full turn") |
| mix, vec3, vec4 | B13 | caption "mix(a, b, t) blends from a to b: t of 0 gives a, 1 gives b" (glossary); cue labels "vec3: a bundle of three numbers: red, green, blue" and "vec4: red, green, blue, alpha (1 is solid)" |
| amplitude | B14 | "amplitude: how far the wave swings from its middle" |
| cycle, speed | B15 | "cycles = TIME × speed · one cycle = one full swing"; "speed: how quickly it repeats" |
| offset | B16 | "offset: added to slide the wave" with "here: where in its cycle it starts" (glossary: "a distance added to slide something") |
| hint_range, instance uniform | B17 | cue labels "hint_range: the editor limits it to 0 to 0.5" and "instance uniform: each node keeps its own value" (docs) |
| fract, ramp | B19 | "fract(x): the part after the point: x minus floor(x)" and "ramp: a smooth run of values from 0 up to 1" (glossary) |
| abs | B20 | "abs(x): drops the minus sign" (docs) |
| sawtooth | B21 | "sawtooth: a ramp that restarts" |
| CurveTexture | B22 | "CurveTexture: a curve baked into a strip of pixels" (docs) |
| frequency | B27 | "frequency: how many cycles fit across the shape" |
| distance | B29 | "distance(a, b): how far apart two points are" (docs) |
| TEXTURE | B31 | cue label "TEXTURE: the node's own picture; texture() reads it" (glossary, shortened to 60 characters) |
| scale about the middle | B37 | "bigger picture = look up closer in" |
| wind, tween | B39, B40 | "wind: 0 is still, 1 is full"; caption "tween: Godot's way to change a value smoothly over time from GDScript" (glossary) |

## Cut line

If the film runs long, cut in this order: the two-waves beat (B34), the roll-over beat (B04), the edge-smear beat (B33) and the sine-or-ramp beat (B24). Each extends an idea another beat already carries. The late-join demo (B01), the clock-mixing pair (B05, B06), the three knob beats (B14 to B16), the travel beat (B28) and the wind click (B40) stay: they are the proof and the payoff. The curve-texture pair (B22, B23) stays because the breathing logo reads one; if both must go, the logo breathes from a sine and B36 to B38 shrink to two beats. Current estimate: about 9.6 minutes, so no cut is needed.
