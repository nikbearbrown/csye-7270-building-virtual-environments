# Components — walker-survival-shooting at f848d84

Film: *Walker Survival Shooting, Before the Slice* (godot-gamedev, walker mode).
Game folder checked: `walker-survival-shooting/godot/` exported from the course repository at commit `f848d84`.
The machine-readable version of this table is `gamedev-evidence.json`.

## What the project contains

The Godot project has **no scripts**, **no input map**, **no main scene**, **no audio files** and **no player**.
Everything runtime-relevant is one saved scene (`base.tscn`), one imported model, and the project file.

| Component | Files | What enters | Important lines / properties | What changes / what is visible | Beats |
|---|---|---|---|---|---|
| `greybox-room` (ENV-BASE-01) | `base.tscn` | nothing at runtime; a static saved scene | `room` CSGCombiner3D with `use_collision = true`; floor 16 × 0.5 × 10 m, walls 3 m high, ceiling | a closed 16 × 10 m room, 3 m interior height | B10, B14 |
| `stair-ramp` | `base.tscn` lines 12–13, 46–81 | nothing at runtime | 6 CSGBox3D steps (0.2 m rise, 0.3 m run, top at 1.45 m); `stairs_ramp` StaticBody3D + CollisionShape3D tilted by (0.8321, 0.5547) = 33.7°; BoxShape3D 1.5 × 0.1 × 2.163 m | visible steps; an invisible collision ramp across all six step edges (seen only with `--debug-collisions`) | B11 → B12 |
| `lighting` | `base.tscn` lines 5–10, 86–98 | nothing at runtime | Environment background (0.03, 0.035, 0.045), ambient (0.45, 0.5, 0.6) × 0.35; two OmniLight3D at x = ±3.5, y = 2.9, colour (0.78, 0.86, 1.0), energy 1.5, range 8 m, shadows on | two bright pools on the ceiling, blue-grey walls and floor | B13 → B14 |
| `project-config` | `project.godot` | — | Forward Plus, Jolt Physics, D3D12, `canvas_items` stretch; no `[input]` section, no `run/main_scene` | nothing can trigger a sound; F5 asks for a scene; window default 1152 × 648 | B10 |
| `test-seat` (ENV-SEAT-TEST-01) | `assets/furniture/test_chair.glb`, `.glb.import` | — | default import settings; instanced at (4, 0.25, −4) | the small dark chair against the back wall | B10, B14 |

Excluded (counted in the ledger, outside the film's scope): `.editorconfig`, `.gitattributes`, `.gitignore`
(template tooling, no runtime effect), `icon.svg`, `icon.svg.import` (default project icon, unused by the scene).

## Input → state → output trace

There is no player input in this build, so the only complete trace the source supports is a
**source change → engine state → visible output** trace:

1. **Source (input):** `base.tscn` line 80, the CollisionShape3D transform with rotation entries 0.8321 / 0.5547,
   and line 13, BoxShape3D size 2.163 m.
2. **Engine state:** Jolt creates a static box collider tilted 33.7° whose top surface passes through the front edge
   of each step. Measured by `capture/ramp_check.gd`: noses 1–5 hit `stairs/stairs_ramp` 0.7 mm above the step top;
   nose 6 hits the CSG landing edge at 0.0 mm (`evidence/ramp-check.log`).
3. **Output:** in a normal render nothing changes (no mesh); with `--debug-collisions` the ramp appears across every
   step edge (`figures/stairs_compare.png`).

What this trace does **not** show: that a character can walk the ramp (there is no character), or what happens if
the step height changes (stated in the film as an untested prediction).

## Assets outside the Godot project (shown, not in-engine)

| Asset | File | Model | Status |
|---|---|---|---|
| SFX-TERMINAL-POWER-ON | `design/sfx_sound/sfx_power_on.flac` (output 00042) | Stable Audio 3 Small SFX | accepted, unedited, not in the project |
| SFX-TERMINAL-POWER-OFF | `design/sfx_sound/sfx_power_off.flac` (00044) | Stable Audio 3 Small SFX | accepted, unedited, not in the project |
| SFX-TERMINAL-CURSOR | `design/sfx_sound/sfx_botton_press.flac` (00070) | Stable Audio 3 Small SFX | accepted, unedited, not in the project |
| SFX-TERMINAL-ERROR | — | Stable Audio 3 Small SFX | not final; not shown or played |
| CHAR-TURN | `design/character/turnaround.png` | ChatGPT image generation | accepted reference |
| Storyboard panel 3 | `design/storyboard/03-tablet-onehand.png` | the designer's hand sketch | design only |
