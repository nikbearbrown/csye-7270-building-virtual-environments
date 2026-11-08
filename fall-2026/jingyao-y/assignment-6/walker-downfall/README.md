# Downfall (walker-downfall) — Assignment 6: particle effects

Downfall is the Assignment 2 game, unchanged as a game since then (no change of
game): an Arknights-inspired extraction roguelike built in **Godot 4.7.2,
Forward+, D3D12 on Windows**. This folder is the A6 upload: the game files a
reviewer needs to open and run the project (the export whitelist from
`tools/export_manifest.py`, their `.import`/`.uid` sidecars, every test and
script) plus the A6 work. Art source files, reference sheets and Blender files
stay out (`scripts/a6_tracked_files.py`, `.gitignore`).

## What A6 added

- **Effect A `hit_spark`** (`effects/hit_spark.tscn`): a one-shot burst when an
  operator's melee hit lands (`entities/player.gd`, `_hit_spark()` at the three
  landed-hit sites). Three `GPUParticles3D` (Flash, Sparks, Puff); overlap rule:
  a new instance per hit under the GameManager, freed by its own 0.55 s timer.
- **Effect B `fire_pit_flames`** (`effects/fire_pit_flames.tscn`): the 萨米 fire
  pit's flames and embers as two `GPUParticles3D` with turbulence and
  preprocess, replacing the old code-made CPU particles. A feedback loop:
  `entities/fire_pit.gd` sets `amount_ratio = 0.3 + 0.7·clamp(burn_left/120,0,1)`
  and `emitting = burn_left > 0`.
- Configuration and state tests for both, frame-strip previews (fixtures), the
  generated process shader `shaders/particles_generated.gdshader` (reference
  only), a headless cost script and a GPU-price fixture.

Read `CHANGE-BRIEF.md` (contract, predictions, dated revisions), `TUNING.md`
(every tuning step with prediction, strips and the user's verdict),
`TEST-REPORT.md` (all results), `FRICTIONAL.md`, `SOURCES.md`, `CLAUDE.md`.

## Run

Open `project.godot` in Godot 4.7.2 (run `--import` once after cloning) and run
`game/main.tscn`. Controls: left mouse moves and attacks (no keyboard
movement), E interacts (feeds a fire), Esc opens the menu, mouse wheel zooms,
Z/X rotate the camera.

Fixtures (labelled FIXTURE on screen; not gameplay):

- `previews/hit_spark_preview.tscn` (`-- --snow`, `-- --loop`) and
  `previews/fire_pit_flames_preview.tscn` (`-- --loop`, `-- --pit=N`): the
  strip sources.
- `previews/play_check.tscn` (`-- --city`, `-- --lit`): a real field floor for
  in-play checks; **Y** pauses the whole tree, **H** hides the pit effects.
- `previews/gpu_price.tscn`, run from the editor with Visual Profiler:
  **U** Effect A at its peak, **I** all pits full, **O** toggles vsync (the
  vsync debug key; no project setting changes). F7/F8 are not used because the
  editor uses them to pause/stop a running scene.

## Tests

Git Bash, from this folder (the wrapper finds Godot three folders up, or set
`GODOT`):

```bash
./scripts/run-test.sh test_hit_spark_config.gd 60
./scripts/run-test.sh test_hit_spark_state.gd 60 600
./scripts/run-test.sh test_fire_pit_flames_config.gd 60
./scripts/run-test.sh test_fire_pit_flames_state.gd 60 600
./scripts/run-test.sh cost_effects.gd 60 300
./scripts/run-baseline.sh <label> 8
```

`run-test.sh <file> <fps|realtime> [timeout]` is the A6 course wrapper adapted
to this repository (`--path .`). Baseline before A6: 78/89 at 60 fps in
parallel; after A6: 82/93 (TEST-REPORT.md lists the pre-existing and
load-sensitive failures).

## Known limitations

- Effect A has no completed tuning revision: the one observation-driven
  proposal (a larger Puff for snow) was declined by the user (TUNING.md).
- Effect B's embers (0.05-unit quads) are barely visible at the default zoom.
- 赫拉格, 星熊, 林, 罗莎 and 桑塔拉 hit through `entities/kits/*.gd` and get no
  HitSpark (brief r2).
- The GPU price is single-frame Visual Profiler readings of the particle
  process step; the draw step was not isolated (TEST-REPORT.md).
- Level dressing (boulders without colliders) can hide a fire pit; found during
  A6, outside its scope, to be fixed after A6.

## Film

Pending (Brutalist godot-gamedev, walker modifier). Link and SHA-256 will be
added here and in SUBMISSION.md.
