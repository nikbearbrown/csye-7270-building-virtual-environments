# Downfall (walker-downfall) — Assignment 7: two animations

Downfall is the Assignment 2 game, unchanged as a game since then (no change
of game): an Arknights-inspired extraction roguelike built in **Godot 4.7.2,
Forward+, D3D12 on Windows**. This folder is the A7 upload, copied from the
game repository at `22651e36`: the game files a reviewer needs to open and run
the project (the export whitelist from `tools/export_manifest.py`, their
`.import`/`.uid` sidecars, every test and script; `scripts/a7_tracked_files.py`)
plus the A7 work. Art source files outside the A7 clips, reference sheets and
Blender files stay out.

## What A7 added

- **`npc_idle` — the cycle** (`animations/npc_idle.tscn`): every NPC figure
  (Closure at the base store; the squad, the trader and Closure at field set
  pieces) is a `Sprite3D` sliced 4×1 whose own `AnimationPlayer` plays a
  discrete frame track at 12 fps (keys 0/4/8/12, `LOOP_LINEAR`). It replaces
  `SpriteFrames` built in code; the old per-figure `frame` write is now a
  one-time seek, so each figure starts on its own cell.
- **`wave_release` — the committing action**
  (`animations/lappland_wave_rig.tscn`): Lappland's sword-wave release as a 2D
  cutout rig (`Node2D` pivots, `Sprite2D` parts cut from her combat sheet by
  `tools/a7_cut_rig_parts.py`) in a `SubViewport` drawn by a `Sprite3D`
  billboard at the player. Phase table at 30 fps: startup 6, active 4,
  recovery 10 frames; the wave leaves on frame 6.
- **The player's wave state machine** (`entities/player.gd`): READY /
  STARTUP / ACTIVE / RECOVERY. It is the one authority over the rig; the clip
  and its clock advance together on the physics tick (`advance(delta*r)`,
  r = attack-speed playback rate, ≥ 1). A dodge or loss of control in startup
  keeps the charge; a swing in recovery cuts it.
- Read-back tests, behaviour pins, a structure test, edge tests, four
  mutations in worktrees, a headless probe and Movie Maker previews.

Read `CHANGE-BRIEF.md` (the contract and its dated revisions r1–r7),
`TUNING.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, `SOURCES.md`,
`animations/ATTRIBUTION.md`, `CLAUDE.md`, `evidence/a7/human-checks.md`.

## Run

Open `project.godot` in Godot 4.7.2 (run `--import` once after cloning) and run
`game/main.tscn`. Controls: left mouse moves and attacks (no keyboard
movement), Space dodges, E interacts, Esc opens the menu, mouse wheel zooms,
Z/X rotate the camera. Lappland's release is every fourth landed hit (three
hits fill the charge).

Fixtures (not gameplay):

- `previews/wave_release_preview.tscn` — the Movie Maker strip source; writes
  `logs/wave_release_preview_<run>.log` with the first capture frame of each
  phase.
- `previews/wave_release_play.tscn` — a playable mine floor with two still
  dummies left and right of Lappland.
- `previews/npc_idle_in_game.tscn`, `previews/npc_idle_side_by_side.tscn`,
  `previews/wave_rig_turntable.tscn` — the NPC and rig review fixtures.

## Tests

Git Bash, from this folder (the wrapper finds Godot five folders up, in
`D:\CSYE 7370`, or set `GODOT`):

```bash
./scripts/run-test.sh test_npc_idle_readback.gd 60
./scripts/run-test.sh test_wave_rig_readback.gd 60
./scripts/run-test.sh test_a7_pins.gd 60 300
./scripts/run-test.sh test_wave_state_machine.gd 60 300
./scripts/run-test.sh test_wave_edges.gd 60 300
./scripts/a7_mutations.sh            # four worktrees, each imported from empty
./scripts/run-baseline.sh <label> 12
```

`run-test.sh <file> <fps|realtime> [timeout]` is the A7 course wrapper adapted
to this repository (`--path .`); a `Failed loading resource` line now fails
the run. Baseline before A7: 93/103; after: 99/108 (TEST-REPORT.md lists the
pre-existing and flaky failures).

## Known limitations

- No observation-driven tuning revision: the user kept the phase table as
  built (TUNING.md r0).
- Claude's strip reading flagged, and the user did not take up: the click's
  melee hit flash lands on the first startup frame; the rig may face away
  from a target on her screen-right.
- Death, loss of control, operator swap and leaving the floor mid-release are
  untested (they share the dodge's return-to-READY path); edges are tested at
  r = 1 only.
- The art is fan art generated with gpt sol 6.1; terms and prompts were not
  supplied (animations/ATTRIBUTION.md).
- The window-only input suites (`test_lappland_input` and others) fail
  headless, as before A7.

## Film

Brutalist godot-gamedev film, walker modifier, narrated by Liam (local Kokoro
`am_onyx`): `youtube/claude-liam-downfall-a7-animation-gamedev/`.

- **YouTube:** https://youtu.be/OdQSCe0ZvaQ
- **Master** (not committed; media is excluded):
  `exports/landscape/claude-liam-downfall-a7-animation-gamedev.mp4`, 7:47
  (466.8 s), 3840×2160, 30 fps, H.264 + AAC 48 kHz, SHA-256
  `fff554fd6910f4f7cfa4eff609870ee66307507fee587af67537d8fac18149fe`; its
  receipt `exports/landscape/claude-liam-downfall-a7-animation-gamedev.verified.json`
  is committed.
- **Filmed at** commit `299ef973`; the game source is unchanged since
  `45cf5845`.
- **Checks:** `./art godot-gamedev --check` PASS (9 code→result pairs,
  `CHECKS-REPORT.md`); final export gate 52 samples, 0 BLOCKER, 0 MAJOR.
- **The user watched and listened to the final export** (verbatim,
  translated from Chinese): "No problems."
