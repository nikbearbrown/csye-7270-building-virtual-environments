# walker-rudy — three 3D props (Assignment 3)

CSYE 7270, Assignment 3: *Your First 3D Game Assets with Claude, the Blender MCP, and Blender*. By Shuai Zhang.

walker-rudy is my 2D side-scroller from Assignment 2 ([`../assignment-2/`](../assignment-2/)): Rudy crosses Level 1, Harvest Fields, past spikes and a waystone checkpoint to the teleport circle. This assignment adds 3D versions of those three props, built in Blender by directing Claude through the Blender MCP, exported as `.glb`, and shown side by side at game scale in a small, separate Godot 3D scene.

| | |
|---|---|
| Props | **Waystone** (the checkpoint; 0.70 × 0.40 × 0.84 m, 118 triangles), **teleport circle** (the end of the level; 2.25 × 2.25 × 0.08 m, 280 triangles), **spikes** (a hazard; 0.80 × 0.30 × 0.47 m, 82 triangles). Scale: Rudy = 1.2 m |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build; the project is [`godot/`](godot/), Forward Plus |
| Blender | 5.2.2 LTS; sources in [`blender/`](blender/) |
| MCP | MCP for Blender ([`ahujasid/mcp-for-blender`](https://github.com/ahujasid/mcp-for-blender)), server 2.1.9, add-on 1.8. All three props were built through the MCP; no asset library or generator was used |
| Machine | macOS 15.1, Apple M3 |
| Assistance | Claude Code, Claude Opus 5.5. The human/AI split is in [SOURCES.md](SOURCES.md) and [FRICTIONAL.md](FRICTIONAL.md) |
| Final film | *Three Props for Walker Rudy.* (Brutalist `godot-gamedev`, `walker` modifier; 6:31, 3840×2160), file `claude-liam-walker-rudy-3d-props.mp4`, SHA-256 `e5372f47fd683d2bd3765ab3006afe9b1bbe520f1c96c16cc4cf001a13fe7276`. It shows the source at `f6f8acf`. The MP4 is not in git; its beat sheet, prompts, evidence and checks are in [youtube/claude-liam-walker-rudy-3d-props/](youtube/claude-liam-walker-rudy-3d-props/). Course media: [claude-liam-walker-rudy-3d-props.mp4 on Google Drive](https://drive.google.com/file/d/1Kwu9iYwfaDHa3HdD_G-FQ89Ik9Yynv0c/view?usp=drive_link) |

## Open the scene

Open `godot/project.godot` in Godot 4.7.2; the main scene is `scenes/props_room.tscn` (F5 runs it). Or, from this folder (in a fresh clone, import first):

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import
/Applications/Godot.app/Contents/MacOS/Godot --path godot
```

The scene: an 8 × 5 m floor, one directional light, a camera, and from left to right a 1.2 m post marking Rudy's height, the spikes, the waystone and the teleport circle.

## Run the check

From this folder (`timeout` is from Homebrew's coreutils):

```bash
timeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/check_props.gd --fixed-fps 60
```

It loads each `.glb` and checks its size, its up axis, its origin, every node's scale and rotation, its triangles and its colours against [CHANGE-BRIEF.md](CHANGE-BRIEF.md). It then checks in the scene that each prop's lowest point is on the floor's top. **Read the last line**, `PASS: 0 failed check(s)` or `FAIL: n failed check(s)`. Godot exits with 0 even when the script fails to parse, so the exit code alone proves nothing. The check does not show whether the props look right; that was my own look, in [TEST-REPORT.md](TEST-REPORT.md).

Screenshots of the running scene, from five views, are made in a window by:

```bash
timeout 120 /Applications/Godot.app/Contents/MacOS/Godot --path godot --script res://tests/capture_props.gd -- ../evidence/godot
```

The scene itself is built by `godot/tools/build_props_room.gd` (run it the same way, headless, to rebuild `scenes/props_room.tscn`).

## What this assignment added

- **The brief, before building:** [CHANGE-BRIEF.md](CHANGE-BRIEF.md), revision 1, committed before any prop was built, with six predicted failures and their checks. Revision 2 records the waystone's new rune; revision 3 records the teleport circle's undersides.
- **Blender:** [BLENDER-NOTES.md](BLENDER-NOTES.md), my notes on the window; the MCP setup ([evidence/mcp-setup-log.md](evidence/mcp-setup-log.md)); three `.blend` sources; every code body Claude ran, in [`tools/blender/`](tools/blender/) (`build_waystone.py`, `build_teleport_circle.py`, `build_spikes.py`, `export_glb.py`); my hand edit, kept as [evidence/waystone-after-hand-edit.blend](evidence/waystone-after-hand-edit.blend).
- **Godot:** the new project in `godot/` with the three `.glb` files and their `.import` files, the scene, the scene builder, the headless check and the screenshot script.
- **Records:** [TEST-REPORT.md](TEST-REPORT.md), [FRICTIONAL.md](FRICTIONAL.md), [SOURCES.md](SOURCES.md).
- **The film:** *Three Props for Walker Rudy.* (6:31, 4K), made with the Brutalist `godot-gamedev` skill and its `walker` modifier; its beat sheet, prompts, fact check, capture logs, stills and build tools are in [youtube/claude-liam-walker-rudy-3d-props/](youtube/claude-liam-walker-rudy-3d-props/), and the MP4 is linked above.

## Known limitations

In full in [TEST-REPORT.md](TEST-REPORT.md#known-limitations):

- the scene is a separate Godot project, not connected to the 2D game, and Rudy is shown only as a 1.2 m post;
- flat colours only: of the three, the teleport circle looks least like its 2D art, because it lacks the circle's pattern of runes, the column of light and the glow (my own judgement); adding them is the next step;
- the Blender sizes and triangle counts were read by code through the MCP, not from screenshots of Blender's sidebar;
- the check's expected numbers are copied by hand from the brief;
- tested only on macOS.

## Files

| Path | What |
|---|---|
| `blender/` | `waystone.blend`, `teleport_circle.blend`, `spikes.blend` (`.blend1` backups are ignored) |
| `tools/blender/` | The MCP code for each prop and for the export |
| `godot/assets/props/` | `waystone.glb`, `teleport_circle.glb`, `spikes.glb` and their `.import` files |
| `godot/scenes/props_room.tscn` | The 3D scene |
| `godot/tests/` | `check_props.gd` (headless check), `capture_props.gd` (screenshots) |
| `godot/tools/build_props_room.gd` | Builds the scene |
| `evidence/` | Screenshots, the MCP setup log, the check's output, the hand-edited waystone |
| `youtube/claude-liam-walker-rudy-3d-props/` | The film's beat sheet, prompts, fact check, captures' logs, stills and build tools (the MP4 is not in git) |
