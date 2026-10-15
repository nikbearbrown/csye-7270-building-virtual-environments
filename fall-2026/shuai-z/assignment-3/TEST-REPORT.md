# TEST-REPORT — Assignment 3, walker-rudy's three 3D props

> 2026-10-13. Written by Claude Code from the runs below and from [FRICTIONAL.md](FRICTIONAL.md). My own check is given in my words, with Claude's translation; nothing in it is written for me.

| | |
|---|---|
| Source tested | Commit `c2e7fea`: the three `.glb` files, the scene and the headless check. The screenshot script `godot/tests/capture_props.gd` and this report were added in the next commit, which changes no asset, scene or check |
| Blender | 5.2.2 LTS, glTF add-on 5.2.40 |
| MCP | MCP for Blender (`ahujasid/mcp-for-blender`), server `mcp-for-blender` 2.1.9, add-on 1.8 |
| Godot | 4.7.2.stable.official.ed1daf0bf, the standard build, Forward Plus renderer (Metal 3.2) |
| Machine | macOS 15.1 (24B83), Apple M3 |
| Spec | [CHANGE-BRIEF.md](CHANGE-BRIEF.md), revision 1, with revision 2 (the waystone's rune and budget) and revision 3 (the teleport circle's undersides) |

## Summary

| Check (the assignment's) | Result | Evidence |
|---|---|---|
| Interface notes | Six parts of Blender's window in my own words, with my own screenshot | [BLENDER-NOTES.md](BLENDER-NOTES.md), [evidence/blender-notes-cube-selected.png](evidence/blender-notes-cube-selected.png) |
| Size | All three match the brief in Blender and in Godot, to 0.005 m | [Size](#size) |
| Upright and scale | All three stand along Godot's Y axis; every node's scale is 1, 1, 1 and its rotation 0 | [Upright and scale](#upright-and-scale) |
| Origin | Each origin is at the centre of the prop's underside; on the floor in the scene, each lowest point is level with the floor's top | [Origin](#origin) |
| Triangle count | 118 / 130, 280 / 300 and 82 / 100, all under the course limit of 500 | [Triangle count](#triangle-count) |
| Imports and appears | All three import with no errors and appear in `godot/scenes/props_room.tscn` | [Imports and appears](#imports-and-appears) |
| HUMAN CHECK: look | I looked at the scene in Godot: the sizes suit the 1.2 m post, nothing is wrong from behind or below, the gold is brighter in Godot than in Blender, and the spikes are closest to the 2D art and the teleport circle furthest from it | [Human check](#human-check-look) |
| What Claude got wrong | Three things, listed | [What Claude got wrong](#what-claude-got-wrong) |
| Inspect and revise | The waystone's rune, after looking at it: rectangle → my hand edit → an R (rejected) → an 8-sided ring → a thinner 12-sided ring | [Inspect and revise](#inspect-and-revise) |

## How to run the checks

From `fall-2026/shuai-z/assignment-3/` (on macOS; `timeout` is from Homebrew's coreutils):

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --import
timeout 120 /Applications/Godot.app/Contents/MacOS/Godot --headless --path godot --script res://tests/check_props.gd --fixed-fps 60
```

**Read the last line, not the exit code.** The check ends with `PASS: 0 failed check(s)` or `FAIL: n failed check(s)` and quits with 1 on a failure. But when the first version of the script had a parse error, Godot printed the error and still exited with **0**: a check that never ran looked like one that passed.

The run recorded here: [evidence/check_props-2026-10-13.txt](evidence/check_props-2026-10-13.txt), 44 checks, `PASS: 0 failed check(s)`.

**The check can fail.** With the waystone raised 0.3 m in the scene file, the same command reported `FAIL  Waystone sits on the floor (lowest point 0.3000 m above the floor's top)` and `FAIL: 1 failed check(s)`. The scene was then rebuilt with `godot/tools/build_props_room.gd`, the same as before apart from Godot's node ids.

**What the check shows.** Each imported prop's size, axis, origin, node scale and rotation, triangles and material colours, against numbers copied into the script from the brief. In the scene, it compares each prop's lowest point with the floor mesh's own top surface, not with the prop itself.

**What it does not show.** Whether the props look right, read as what they are, or suit the game; whether the colours look right under this light; anything about the 2D game, which this scene is not connected to. If the brief changes, the numbers in the script must be changed by hand.

## Size

Width × depth × height in metres. Blender is Z-up and Godot Y-up, so Blender's depth (Y) is Godot's Z and Blender's height (Z) is Godot's Y.

| Prop | Brief | Blender: the object's Dimensions | Godot: bounding box X × Z × Y |
|---|---|---|---|
| Waystone | 0.70 × 0.40 × 0.84 | 0.70 × 0.40 × 0.84 | 0.7000 × 0.4000 × 0.8400 |
| Teleport circle | 2.25 × 2.25 × 0.08 | 2.25 × 2.25 × 0.08 | 2.2500 × 2.2500 × 0.0800 |
| Spikes | 0.80 × 0.30 × 0.47 | 0.80 × 0.30 × 0.47 | 0.8000 × 0.3000 × 0.4700 |

The Blender column was read through the MCP from each joined object's `dimensions`, the same values the sidebar (N) shows under Item → Dimensions. It was read by code; I have no sidebar screenshot of the final objects. The Godot column is from the headless check.

## Upright and scale

| Prop | Height found on | Nodes in the imported scene | Node in `props_room.tscn` |
|---|---|---|---|
| Waystone | Y only | `waystone` and `Waystone`: scale (1, 1, 1), rotation (0, 0, 0) | scale (1, 1, 1) |
| Teleport circle | Y only | `teleport_circle` and `TeleportCircle`: scale (1, 1, 1), rotation (0, 0, 0) | scale (1, 1, 1) |
| Spikes | Y only | `spikes` and `Spikes`: scale (1, 1, 1), rotation (0, 0, 0) | scale (1, 1, 1) |

Before the import, Claude read the `.glb` files' JSON: each has a single node with no translation, rotation or scale, and its heights are on Y. Rotation and scale were applied in Blender after every step and again after joining.

## Origin

Each prop was built with its underside on Blender's floor and its origin set to the world origin after joining, so the origin is the centre of its underside. The headless check found the underside centre of each imported prop at (0.0000, 0.0000, 0.0000).

In the scene, all three stand at Y = 0. The check found each lowest point 0.0000 m above the floor's top surface (the floor's top is at Y = 0.0000, read from the floor mesh). In the screenshots, all three stand on the floor, with shadows that start at their bases: [evidence/godot/props_room-1-camera.png](evidence/godot/props_room-1-camera.png), [evidence/godot/props_room-3-low.png](evidence/godot/props_room-3-low.png).

## Triangle count

| Prop | Shapes | Triangles in Blender | Triangles in Godot | Budget |
|---|---|---|---|---|
| Waystone | 5 | 118 | 118 | 130 (revision 2; was 60) |
| Teleport circle | 6 | 280 | 280 | 300 |
| Spikes | 6 | 82 | 82 | 100 |

The Blender counts were read through the MCP (`calc_loop_triangles`) after joining, not from the Scene Statistics overlay. The counts include faces hidden inside the joined meshes, such as the bottom of the waystone's body inside its moss.

## Imports and appears

`godot --headless --path godot --import` imported the three `.glb` files and wrote their `.import` files with no import error. The only error in the log was `Cannot open file 'res://scenes/props_room.tscn'`, because the project's main scene had not been built yet. All three props appear in `godot/scenes/props_room.tscn`, side by side on an 8 × 5 m floor, with one directional light and a camera, and a 1.2 m post where Rudy would stand.

Screenshots of the running scene, rendered in a window by `godot/tests/capture_props.gd` (Claude's script; the images are real renders, not reconstructions):

| View | File |
|---|---|
| The scene's camera | [evidence/godot/props_room-1-camera.png](evidence/godot/props_room-1-camera.png) |
| From behind | [evidence/godot/props_room-2-behind.png](evidence/godot/props_room-2-behind.png) |
| Low, at the props' height | [evidence/godot/props_room-3-low.png](evidence/godot/props_room-3-low.png) |
| From above | [evidence/godot/props_room-4-above.png](evidence/godot/props_room-4-above.png) |
| From below the floor (the floor is one-sided) | [evidence/godot/props_room-5-below.png](evidence/godot/props_room-5-below.png) |

## Human check: look

**Mine.** I opened the scene in the Godot editor and looked at it. In my words: "看完了，没什么问题" (I have looked at it; there is no problem). Opening it in the editor created the two `.uid` files in `godot/tests/` and `godot/tools/`. Asked for more detail, I added (translated):

- Beside the 1.2 m post, all three props are a suitable size.
- From behind and from below there is no problem.
- Blender's gold is on the dark side; Godot's gold is brighter, and more golden.
- The spikes look most like the game's 2D art; the teleport circle looks least like it, because it lacks the circle's pattern of runes, the column of light and the glow.

**Claude's observations from the screenshots**, kept apart from mine:

- All three read as what they are beside the 1.2 m post: the spikes come up to below its middle, the waystone to about two thirds of it, and the teleport circle is almost twice as wide as the post is tall.
- Under Godot's light the gold is a saturated yellow gold, brighter than it looked in Blender's material preview, and the waystone's blue ring stands out on the grey stone.
- From behind, the waystone shows a plain back, as built; the ring is on the front only.
- From below the floor, all three undersides are closed (wood, moss green, gold), with no missing faces.
- Seen low and edge-on, the teleport circle is only a thin line; it reads from above.

No other person has looked at the scene.

## What Claude got wrong

1. **The brief missed the teleport circle's undersides.** Revision 1, drafted by Claude and approved by me, said no faces of the teleport circle overlap, but it had only checked the top faces. All three discs started at Z = 0, so their differently coloured undersides would have shared the floor plane and flickered from below. Claude found this while planning the build, before any of it was built. Fixed in CHANGE-BRIEF revision 3.
2. **The first headless check did not run.** It had two GDScript type-inference parse errors, and Godot still exited with 0. The parse errors were printed and no `PASS`/`FAIL` line followed; Claude fixed the types and confirmed separately that the 0 came from Godot itself.
3. **The first camera screenshot was wrong.** The capture script read the camera's global transform before the scene was in the tree, so it got the identity and photographed the scene from the origin. Fixed by waiting one frame before reading it; the image in `evidence/godot/` is the corrected one.

## Inspect and revise

The waystone, built exactly to revision 1, had a plain rectangular rune. Looking at it:

| Step | Who | What | Shapes / triangles |
|---|---|---|---|
| Built | Claude | the rectangle, Z 0.27–0.57 | 4 / 42 |
| Hand edit | me | moved the rune up 0.034 m, to Z 0.30–0.60 ([evidence/waystone-after-hand-edit.blend](evidence/waystone-after-hand-edit.blend)) | 4 / 42 |
| Tried | Claude, at my request | a capital R of three shapes; I rejected it: "现在不好看" (it does not look good) | 6 / 82 |
| Tried | Claude, at my request | a ring of two 8-sided cylinders | 5 / 86 |
| Kept | Claude, at my request | 12 sides and a thinner band (0.03 m instead of 0.05) | 5 / 118 |

The budget rose from 60 to 130 in CHANGE-BRIEF revision 2, with the reason; revision 1 is unchanged. Every code body is in [tools/blender/build_waystone.py](tools/blender/build_waystone.py).

## Predictions against results

| # | Prediction (CHANGE-BRIEF) | Result |
|---|---|---|
| 1 | Arrives lying on its side | Did not happen: the height is on Y for all three |
| 2 | Wrong size by a factor | Did not happen: the sizes match to 0.005 m, and every scale is 1 |
| 3 | Origin in the middle, so it floats or sinks | Did not happen: origins at the underside centre, on the floor |
| 4 | Over the triangle budget | The waystone went over revision 1's 60 when I changed its rune; the budget was revised to 130 with a reason. The other two stayed within budget |
| 5 | A colour does not survive the export | Did not happen: all eight colours match in the `.glb` and in Godot |
| 6 | Claude builds more detail than asked | Did not happen: shapes, segment counts and modifiers matched the brief at each step. The extra shapes came from my own requests |

## Known limitations

- The scene is a separate Godot project in `godot/`, not connected to the 2D game.
- Rudy is shown only as a 1.2 m post; the props are not seen beside his sprite.
- Flat colours only: the teleport circle's pattern of runes, its column of light and its glow are not modelled, nor the waystone's glow, and the waystone shows only its lit rune. These are why, in my judgement, the teleport circle is furthest from its 2D art; modelling them is the next step.
- The Blender sizes and triangle counts were read by code through the MCP, not from screenshots of Blender's sidebar or Scene Statistics.
- The check's expected numbers are copied into the script by hand from the brief.
- Godot's exit code does not show whether the check ran; only its last line does.
- Tested only on macOS 15.1 (Apple M3) with the Forward Plus renderer.
