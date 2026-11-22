# Assignment 7 — Submission

- **Assignment:** Assignment 7 - Doing Animation with Claude and Godot
- **Student:** Jingyao Yuan (course folder `jingyao-y`)
- **Project name:** Downfall (`walker-downfall`)
- **GitHub repository URL:** https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/Jingyao_Y/fall-2026/jingyao-y/assignment-7/walker-downfall/
- **Git tag and submitted commit SHA:** tag `a7`; the commit SHA is given in
  the Canvas note (a commit cannot contain its own SHA).
- **Game-source revision shown in the film:** the film was built at commit
  `299ef973`; the game source is unchanged since `45cf5845`. Later commits
  change only tests' support files, documents and film records.
- **Godot version, renderer, and operating system:** Godot 4.7.2-stable
  (official), Forward+, D3D12 on Windows 11 (NVIDIA GeForce RTX 4060 Laptop
  GPU).
- **Sprite clip: route, node, scene, frame rate:** `npc_idle` — Sprite3D with
  an AnimationPlayer frame track; node `NpcIdle` (Sprite3D, hframes 4 ×
  vframes 1) and its `AnimationPlayer`; scene `res://animations/npc_idle.tscn`,
  instanced by `FieldArt.npc_idle` for every NPC figure; 12 fps, keys at
  frames 0/4/8/12, `step` 1/12.
- **Rig clip: route, rig source, node, scene, frame rate:** `wave_release` —
  2D cutout rig keyed as resource text; parts cut from
  `godot_assets/lappland_combat_64.png` (row west, column 10) by
  `tools/a7_cut_rig_parts.py`; node `WaveRig` (`Billboard` Sprite3D +
  `Viewport` SubViewport → `Rig` Node2D pivots + `AnimationPlayer`); scene
  `res://animations/lappland_wave_rig.tscn`, instanced on the Player; 30 fps,
  `step` 1/30, keys at frames 0/6/10/20.
- **Which clip loops and which commits:** `npc_idle` loops
  (`LOOP_LINEAR`); `wave_release` commits (`LOOP_NONE`; startup 6, active 4,
  recovery 10 frames; the wave leaves on frame 6).
- **The one authority over each animated node:** `NpcIdle.frame` — its own
  AnimationPlayer (autoplay; callers only set the texture and seek once). The
  rig parts — the rig's AnimationPlayer, called only by the Player's wave
  state machine (`entities/player.gd`), which also alone writes
  `Billboard.visible` and `Rig.scale.x` (GmCamera writes the unkeyed
  `Billboard.offset.y`). The operator sprite — `LapplandAnimator3D` for its
  frames; `Player` alone for its `visible`.
- **Sprite sheet source and licence (or model, version, and terms):** the
  game's own art, fan art of Arknights characters generated with
  **gpt sol 6.1** (as the user stated it); terms of use, date checked and
  prompt log not supplied by the user. Originals as delivered and the code
  that derives the sheets are committed (`animations/ATTRIBUTION.md`).
- **Final film URL and filename:** https://youtu.be/OdQSCe0ZvaQ —
  `claude-liam-downfall-a7-animation-gamedev.mp4` (7:47, 3840×2160, 30 fps;
  kept locally, not on GitHub; receipt
  `youtube/claude-liam-downfall-a7-animation-gamedev/exports/landscape/claude-liam-downfall-a7-animation-gamedev.verified.json`).
- **Final film SHA-256:**
  `fff554fd6910f4f7cfa4eff609870ee66307507fee587af67537d8fac18149fe`
- **Summary of human and agent contributions (written by the agent from the
  actual record):** The agent (Claude Code, Claude Opus 5.5) wrote the brief
  and its revisions r1–r6, the pins, the probe, every review, the previews,
  the mutation runner, the reports and every commit; delegated agent sessions
  (in place of `claude -p`, which is not installed here) drafted CLAUDE.md,
  built both clips and their read-backs, wired the clips, the state machine,
  the structure and edge tests and the re-pin; a fork of the agent built the
  film. The user chose the location, the art source, the rig route and the
  attack-speed rule (r4); approved or declined every revision and plan step;
  watched every preview and gave every verdict ("same", "All fine", "Reads
  well", the background and interrupt checks, "everything is nice", "Keep r0,
  no revision", and "No problems" on the final film); ran the Movie Maker
  capture; supplied the model name (r7). FRICTIONAL.md has the full record.
- **Known limitations:** no observation-driven tuning revision (the user kept
  r0); Claude's strip notes (an early hit flash, facing) not taken up; death,
  loss of control, operator swap and leaving the floor mid-release untested,
  edges tested at rate 1 only; the window-only input suites fail headless as
  before A7; `test_combat` and `test_recruit_kits` flake under parallel load
  (pre-existing; TEST-REPORT.md).
- **Changed games since Assignment 2:** no.

## Run and verify

Open `project.godot` with Godot 4.7.2 and run `--import` once, then
`game/main.tscn`. Tests, from this folder in Git Bash (the wrapper finds Godot
five folders up, or set `GODOT`):
`./scripts/run-test.sh test_npc_idle_readback.gd 60`,
`./scripts/run-test.sh test_wave_rig_readback.gd 60`,
`./scripts/run-test.sh test_a7_pins.gd 60 300`,
`./scripts/run-test.sh test_wave_state_machine.gd 60 300`,
`./scripts/run-test.sh test_wave_edges.gd 60 300`. A fresh sparse clone of
this folder was checked before tagging (TEST-REPORT.md "Fresh-clone check").
On Windows, clone to a short path or set `git config core.longpaths true`.
