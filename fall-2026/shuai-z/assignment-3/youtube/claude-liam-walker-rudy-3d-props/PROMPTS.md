# PROMPTS — Three Props for Walker Rudy.

Every prompt shown or read in the film.

## B00 — Jambo, Liam

**Status:** reconstructed prompt — illustrative, not a transcript

```text
Please use Walker to convert my game design document about Walker Rudy — a chibi boy who crosses the Harvest Fields past spikes and a waystone checkpoint to a teleport circle — into three simple 3D props built in Blender through the Blender MCP, exported as .glb, and shown side by side at game scale in a small Godot 3D scene.
```

On-screen result lines (each checked in FACTCHECK.md):

- Repo walker-rudy · assignment-3/ at f6f8acf · Blender 5.2.2 · MCP for Blender 2.1.9 · Godot 4.7.2.
- Built: waystone, teleport circle, spikes — basic shapes, flat colours, 82 to 280 triangles each.
- Brief, approvals and the hand edit: shuai-z · every Blender call and the Godot scripts: Claude Code.

## BHTF — Your turn.

**Status:** suggested prompt for the viewer

```text
Read my CHANGE-BRIEF.md and godot/tests/check_props.gd. Before you change anything, predict what the check will print if spikes.glb is exported with its origin at the centre of the wooden block instead of the centre of its underside. Then make that change on a copy, re-export, and show me the check's output before and after.
```

## B05, B07, B08 — shuai-z's prompts quoted from the build session

Verbatim from the Claude Code session of 2026-10-13 (times EDT), with Claude's translation:

- 20:07: “我把符文往上移了点，你看一下；但是我觉得符文变成大写字母R会好看点，你改一下试试，看下三角面数会不会超” [I moved the rune up a little, take a look; but I think the rune would look better as a capital R — try it, and see whether the triangle count goes over.]
- 20:14 (shown in B05): “现在不好看，不用R，把符文换成一个圆环试试” [It does not look good now. No R — try turning the rune into a ring.]
- 20:18: “改成12边，加Revision 2，然后圆环再细一点” [Make it 12 sides, add Revision 2, and make the ring a bit thinner.]

These are shuai-z's own prompts, shown as such. The code Claude ran for each is in `assignment-3/tools/blender/build_waystone.py`.
