# Compatibility particles probe (2026-11-04, before the brief)

A throwaway Godot project, not part of the game. Claude Code wrote and ran it
on 2026-11-04, before CHANGE-BRIEF.md was written, to check three things the
brief depends on, on this machine (Apple M3, macOS, Godot 4.7.2):

1. Does a `GPUParticles2D` with `trail_enabled` draw under GL Compatibility,
   the renderer the game uses (`game/project.godot`)?
2. Do damping and a box emission shape work under GL Compatibility?
3. Can a GPU render time be read with
   `RenderingServer.viewport_get_measured_render_time_gpu()`?

`probe.gd` builds three emitters with a code-written radial texture: on the
left, `trail_enabled` with the emitter moving in a circle; in the middle, a box
emission shape with damping 300 px/s², which should stop particles moving at
150 px/s within 0.5 s; on the right, a plain emitter as the reference.

## How it was run

From `assignment-6/`, once per renderer (`--rendering-method` overrides the
project setting for that run only). The full Movie Maker sequences went to the
scratchpad, and only frames 5 and 30 were kept here.

```bash
godot --headless --path evidence/compat-probe --import
godot --path evidence/compat-probe --always-on-top --write-movie <dir>/frame.png --fixed-fps 30 --quit-after 45
godot --path evidence/compat-probe --rendering-method forward_plus --always-on-top --write-movie <dir>/frame.png --fixed-fps 30 --quit-after 45
```

## What it found

| Question | GL Compatibility (OpenGL 4.1 on Metal) | Forward+ (Metal 3.2), for comparison |
|---|---|---|
| Trails | The engine warns `The Compatibility renderer does not support particle trails.` (`compatibility.log`), and the left emitter draws nothing (`compatibility_frame30.png`) | The left emitter draws stretched trails (`forward_plus_frame30.png`) |
| Damping and box emission | Work: the middle particles stop near the box by frame 30, while the reference spreads across its third | The same |
| GPU render time | 0.0 ms on every frame from 11 to 40, and Movie Maker's summary reads `GPU render time: 0.00` | Also 0.0 ms |

The trail result matches Chapter 9, which cites Godot's renderer comparison:
trails and SDF collision are not supported in Compatibility. The two GPU-time
zeros say only that this API returned 0 here, under both renderers. They do
not show what the editor's Visual Profiler reads; that is checked by a person
in the editor (CHANGE-BRIEF.md, section 5).

An earlier version of this probe, kept only in the scratchpad, also had a
turbulence emitter. It stayed at its origin under both renderers, so its
settings were wrong, not the renderer. That proves nothing about turbulence,
and it was dropped from this version.
