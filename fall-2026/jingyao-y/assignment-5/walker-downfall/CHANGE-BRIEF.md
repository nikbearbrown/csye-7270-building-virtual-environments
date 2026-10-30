# CHANGE-BRIEF.md — Assignment 5: burning-bottle fire shader

> Skeleton laid out by Claude Code (2026-10-30): headings, and the facts in
> "What the code does today", each with its file reference. Every `TODO(你)`
> is the student's to write. The colour line, the rules and every predicted
> number are the student's. Commit this file before either shader exists.
> Later changes go in "Revisions" at the bottom, dated; the original stays.

## What the code does today (facts, checked 2026-10-30)

- 燃烧瓶投掷者 (`thrower`) lobs a bottle; its fire lasts `fire_time` 3.0 s
  (`game/enemy_attacks.gd:34`), 0 when the thrower is silenced
  (`entities/enemy.gd:1200`). Throwers spawn in the city region
  (`game/enemy_attacks.gd:163`).
- The bottle lands after 0.6 s (`entities/molotov.gd:8`) and calls
  `game.spawn_hazard(at, radius, 0.0, fire_time, …)` (`entities/molotov.gd:67`,
  `game/game_manager.gd:794`): a `GroundHazard` with `fuse` 0 and `lasting` 3.0.
- `GroundHazard` counts `lasting` down by the physics delta in
  `_physics_process`, only while `game.simulation_active()` is true
  (`entities/ground_hazard.gd:62`, `game/game_manager.gd:386`), hits every
  0.5 s, and frees itself when `lasting` reaches 0.
- The fire on the ground today is a `Decal` with a code-made circle texture
  (`entities/ground_hazard.gd:31`). A Decal takes textures, not a shader, so
  it stays as the scorch, and the new flames go on a new mesh.
- The same class also draws the slug burst and a boss's last rite (`fuse` > 0,
  `lasting` 0: `entities/enemy.gd:1443`, `entities/boss.gd:347`). Those are
  not burning fires.
- Renderer: `project.godot` sets no `rendering_method`; the Windows driver is
  D3D12 (`project.godot:27`). The field's `Environment` is made in
  `game/game_manager.gd:6501` and sets no tonemap or glow there. Confirm in a
  running game before predicting pixels.

## The state

- What it communicates, and why the player needs it: TODO(你)
- Name of the state: TODO(你) (e.g. "a fire patch is burning")
- Script and variable that hold it: TODO(你)

## Effect specification

### The shader

- Path: `res://shaders/TODO(你).gdshader`
- `shader_type`: TODO(你)
- `render_mode`: TODO(你)

| Uniform | Type | Hint | Default | Set by |
|---|---|---|---|---|
| TODO(你) | float | TODO | TODO | driver, from the state |
| TODO(你) | | | | |

### The colour line

```glsl
TODO(你): the one line inside fragment() that changes the colour
```

### Observable rules

| # | Rule | Value / answer |
|---|---|---|
| R1 | Uniform value when the state begins | TODO(你) |
| R2 | Uniform value when the state ends | TODO(你) |
| R3 | Duration of any change, in seconds (tolerance: one frame period); same game time at 30, 60, 144 fps | TODO(你) |
| R4 | State begins again mid-transition: restart, extend or ignore | TODO(你) |
| R5 | Scaled or unscaled time under `Engine.time_scale`; behaviour while paused | TODO(你) |
| R6 | Uniform value if the state ends before a transition finishes | TODO(你) |
| R7 | Several instances: how each gets its own value | TODO(你) |

### Boundaries

TODO(你): collision, movement, input, the state machine and its timings,
existing test expectations and every other object stay unchanged.
Presentation code may read game state; it never writes it. Name anything
specific to this change (the Decal, damage ticks, the slug burst …).

### Evidence split

| Rule | Headless test or eyes | How |
|---|---|---|
| R1 | TODO(你) | |
| R2 | | |
| R3 | | |
| R4 | | |
| R5 | | |
| R6 | | |
| R7 | | |

## Controlled inputs and predicted values

- Lighting/tonemap for these captures, and how it is fixed: TODO(你)
- Background colour(s) behind the flame: TODO(你)
- Uniform values: TODO(你) (three values)

| Pixel | Value 1 | Value 2 | Value 3 |
|---|---|---|---|
| TODO(你) pixel A (where, and why) | | | |
| TODO(你) pixel B | | | |

Working (by hand): TODO(你)

Contrast ratio against the background, if the effect changes it: TODO(你)

## Hint experiment predictions

3×1 PNG, greys 64, 128, 192; unshaded quads; Linear tonemap, exposure 1.0.

| Band | Stored | Quad with `source_color` | Quad without |
|---|---|---|---|
| 1 | 64 | TODO(你) | TODO(你) |
| 2 | 128 | TODO(你) | TODO(你) |
| 3 | 192 | TODO(你) | TODO(你) |

Working: TODO(你)

Which quad shows the file's values unchanged, and why: TODO(你)

## Material plan (textured shader)

- Object, scene, and the lighting it is judged under: TODO(你)

| Texture | Role | Source | What its numbers mean | Colour or data | compress/mode | compress/normal_map | mipmaps/generate |
|---|---|---|---|---|---|---|---|
| TODO(你) | | | | | | | |

| Uniform | Type | Hint | Range | Default | Group | Expected change across its range |
|---|---|---|---|---|---|---|
| TODO(你) | | | | | | |

- What differs between the two materials, and why: TODO(你)

## Predicted failure cases

| # | Failure | Check that catches it |
|---|---|---|
| F1 | TODO(你) | |
| F2 | TODO(你) | |
| F3 | TODO(你) | |

## Questions

1. Which renderer does `project.godot` name, and what does it rule out? TODO(你)
2. What colour arrives in `fragment()` before you change it, and what would the tempting alternative give you? TODO(你)
3. Spatial: what does `ALBEDO` hold if you never write it, and what does `COLOR` hold? TODO(你)
4. How long would a frame-counting version last at 30, 60 and 144 fps? TODO(你)
5. Which resource holds the uniform's default, which its current value, and what happens if two objects share the material? TODO(你)
6. Does `hint_range` clamp a value the driver sets from code? (Predict now.) TODO(你)

## Revisions

(none yet)
