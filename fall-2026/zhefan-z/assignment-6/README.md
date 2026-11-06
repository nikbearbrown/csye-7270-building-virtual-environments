# walker-magic — Assignment 6: particle effects with Godot and Claude

Zhefan Zhang (zhefan-z), CSYE 7270 Fall 2026. Game: *walker-magic*, a 2D side-scroller in which a mage crosses a cave and casts fireballs at a wolf. Starting point: my Assignment 5 project, unchanged (see `SOURCES.md`).

**Engine:** Godot 4.7.2-stable, renderer Forward+ (the engine default). Windows, Git Bash.

## Run it

- Open `walker-magic-zhefan/project.godot` in Godot 4.7.2 and press F5.
- Tests, from this folder in Git Bash, after `godot --headless --path walker-magic-zhefan --import` once:
  - `./scripts/run-test.sh test_fireball_impact_config.gd 60`, `test_fireball_trail_config.gd 60`
  - `./scripts/run-test.sh test_fireball_impact.gd 30` (also 60 and 144), `test_fireball_trail.gd 30` (also 60 and 144)
  - `./scripts/run-test.sh cost_effects.gd 60 300` (headless price)
  - the nine earlier suites as listed in `CLAUDE.md`
- Previews (fixtures): `previews/fireball_impact_preview.tscn` (add `-- retrigger` for two impacts), `previews/fireball_trail_preview.tscn`. Strips: `godot --path walker-magic-zhefan --write-movie <abs path>/frame.png --fixed-fps 30 --quit-after 60 <preview>`.

**Controls:** A/D or arrows to walk, Space/W/Up to jump, left mouse to cast, Esc to pause, R to restart, M and N to mute music and sound effects.

**GPU price scene** (`previews/gpu_price.tscn`, run from the editor with F6 for the Visual Profiler): 1 effects off, 2 Effect A ×6, 3 Effect B heaviest, **F8 toggles vsync** (debug key; no project setting changes). In the editor F8 may stop the run; use the command line for the vsync comparison.

## What this assignment added

- **Effect A — fireball impact** (`effects/fireball_impact.tscn`): a one-shot GPUParticles2D burst of sparks and smoke on every fireball hit, alongside the unchanged A2 flash; overlapping instances on rapid hits.
- **Effect B — fireball trail** (`effects/fireball_trail.tscn`): a continuous GPUParticles2D trail with turbulence and a sphere emission shape; when the fireball ends, it is detached, stops emitting and fades where it was.
- Configuration and state tests for both, previews and frame strips, tuning records (`TUNING.md`), the headless price script, the GPU price scene, and the generated process shader with line references (`TEST-REPORT.md`).
- Spec `CHANGE-BRIEF.md`, context `CLAUDE.md`, evidence `TEST-REPORT.md`, log `FRICTIONAL.md`.

## Known limitations

- The `_spent` guard (two contacts in one frame) is not exercised by any test.
- The trail still shows 1–3 px gaps behind its head; the cause (a 30 fps particle simulation) is a guess.
- Effect B's GPU price is measured with 18 trails, above the brief's 6 + 6, so it is an upper bound.
- Whether the GPU keeps simulating a hidden emitter is not checked; nothing in the game hides one.

## Film

(Link, filename and SHA-256 added after the final render.)
