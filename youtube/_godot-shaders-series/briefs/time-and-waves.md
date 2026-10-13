# Brief: Time and Waves

**What this is.** The content brief for the film on `TIME`, the sine wave and its four knobs, looping, custom easing curves and waves that travel across a shape. Slug `time-and-waves`, folder `claude-liam-lecture-time-and-waves`, group Fragment techniques, target about 10 minutes (ceiling 15). Title lines: `["Time and Waves"]`.
**Why.** Almost every shader animates. The pilot explains that `TIME` is one global clock; this film shows how to build per-object timing on top of it and how to describe any wave with four numbers.
**Found.** About 25 minutes of source across the TIME node, the waves chapter and the flag. The source repeats the "time since the scene was created" error. Measured: `TIME` is one global clock.

## The one idea

`TIME` counts seconds. Put it inside a sine and you get a smooth repeat. Four numbers describe the wave: how tall (amplitude), how fast it repeats (frequency), how quickly it moves (speed) and where it starts (offset). For a one-time effect, drive a uniform instead.

## The newcomer's assumption (BIDEA)

`BIDEA_TEXT = ("TIME starts\nwhen my node appears.", "when my node appears", "when the game starts")`.

## Prerequisites for the terms card

**Sine** (the smooth wave from a function), **Amplitude**, **Frequency**, **Offset**. Earn some in the acts; 17 characters or fewer.

## Suggested acts

1. **One Clock.** Recap in two beats: `TIME` is global since the engine started (docs). What affects it: time scale yes, pausing no (verify both in a scratch run). The rollover (docs: repeats every 3,600 seconds by default; check the project setting name). The standard fix for per-object timing: a uniform you set (and why `Time.get_ticks_msec()` is not the same origin as `TIME`: measure the offset in a scratch scene before claiming anything).
2. **The Wave.** `sin(TIME)` plotted; range −1 to 1; normalize to 0 to 1 with `0.5 + 0.5 * sin(x)`; the four knobs on a plot, each moved in turn (`amp * sin(freq * x + phase) + offset`; add `speed` as `x = u * freq - TIME * speed`).
3. **Loops and Curves.** `fract(TIME * speed)` is a ramp that restarts; `abs(fract(...) * 2.0 - 1.0)` ping-pongs; a `CurveTexture` sampled with `texture(curve, vec2(t, 0.0)).r` gives a custom easing; why a symmetric curve plays forward then backward (use the sawtooth, not the sine, to go one way).
4. **Waves on a Shape.** A traveling wave: `sin(UV.x * freq - TIME * speed) * amp` added to a vertical offset or to the sampling address; multiplying by `UV.x` pins the left edge (a flag); water-style wobble by offsetting the address in the fragment stage (no new vertices needed).
5. **Payoff.** One effect that uses all four: a logo that breathes (scale from a custom curve) and a banner whose wave travels.

## What the source does (my words)

- `sin(TIME)` added to `VERTEX.x` times 20; normalized curve formula worked with three input values; scaling the whole vertex by the normalized curve; a `sampler2D` curve texture (`CurveTexture`) sampled with `texture(curve, vec2(normalized, 0.0)).r`; the observation that the wave plays forward then back, and the fix with `fract(TIME)`; a speed uniform; the flag: `vertex.y += sin((UV.x - TIME * speed) * frequency) * amplitude * UV.x`, plus cosine on x and an "incline".
- The 8-minute intro fades with `TIME / duration` and then with a Tween.

## Source claims to check or correct

- **"TIME is the time since the scene (or shader) was created"**: wrong; docs and the pilot's run say one global clock. Correct it.
- "Time pauses/doesn't pause": docs say `TIME` is "affected by `time_scale` but not by pausing"; verify with a scratch scene (set `Engine.time_scale`, pause the tree) and report.
- Phase versus offset naming: say which is which and keep it consistent.

## Facts to verify

Docs: the `TIME` entry in every shader reference you cite; the rollover setting; `CurveTexture` usage. Scratch runs: `Engine.time_scale = 0.5` and `get_tree().paused = true` effects on `TIME`; whether a CurveTexture sampled at (t, 0) returns the curve value in `.r`. Lab: the wave plotted from a rect (probes across x at two `--wait` values), the pinned flag in a Polygon2D/mesh is the vertex film's job, so here use the fragment-stage wobble.

## Captures

Lab videos: pulse, breathing logo, traveling-wave banner (wobble in the fragment stage). Custom scene for the time-scale/pause demonstration.

## Cut line

The curve-texture beat; the second knob demo.

## Other films cover

Vertex-stage waves on a mesh: vertex shaders; `sin`/`cos` as position on a circle: trigonometry; the pilot already teaches the global clock (recap only).
