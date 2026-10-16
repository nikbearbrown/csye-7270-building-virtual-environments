# COMPONENTS — what this film explains

Scope: the Assignment 3 layer of `godot/` at c0dba4c. The ledger (`gamedev-evidence.json`) hashes all 17 A3 files
and lists the 73 Assignment 2 files as exclusions with a reason (they are the 2D game, unchanged by A3 and explained
in the Assignment 2 film).

| Component | Files | Beats | What the film shows |
|---|---|---|---|
| Lantern Gate | `a3/lantern_gate.gd`, `.tscn`, `.glb`, `.glb.import` | B02, B12, B13 | the six-part gate; two `-convcolonly` boxes imported as collision-only bodies on layer 3; the stand-in stopping at the base in a real capture |
| Supply Stack | `a3/supply_stack.glb`, `.import` | B02, B05–B08, B11 | the MCP calls that build it (verbatim Blender Python), scale left after call 2, applied by call 5, measured in Godot |
| Lamp-oil Shrine | `a3/oil_shrine.glb`, `.import` | B02, B09, B11 | Bao's 20° OilGem hand edit (before/after, measured), the re-exported GLB measured in Godot |
| Prop room | `a3/lantern_gate_room.gd`, `.tscn`, `game/session.gd` (F4 only), `project.godot` | B13, B14, B15 | the A3-R3 orbit camera (code, then the real orbit capture front → behind → below) |
| A3 tests | `tests/harness.gd`, `test_a3_assets.gd`, `test_lantern_gate.gd`, `test_a3_camera.gd`, `capture_a3_orbit.gd` | B10, B11, B15 | the size/scale/budget check (code, then recorded headless output beside the brief) |

Code → result pairs (code-then-result-v1): B10 → B11, B12 → B13, B14 → B15. The Blender Python excerpts (B05, B07)
come from `tools/blender/`, outside `godot/`, so they are plain code panels with path and lines, each followed by
Blender's own window showing the result (B06, B08).

Not explained here: the Assignment 2 game (sprites, audio, weapons, progression, HUD, its 122 checks) — see the
Assignment 2 film, `youtube/claude-liam-walker-lanternfall-bao-x-gamedev/`. `tests/capture_lantern_gate.gd` is an
earlier still-capture tool, superseded for this film.
