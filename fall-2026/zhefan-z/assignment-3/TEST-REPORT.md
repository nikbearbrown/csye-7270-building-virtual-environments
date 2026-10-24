# TEST-REPORT — Assignment 3: three 3D assets

> Drafted by Claude (claude.ai chat) from the Claude Code reports and commits of this assignment; reviewed by me. The human-check judgments are mine, translated from my Chinese answers.

## Environment
- Windows, NVIDIA GeForce RTX 5060 Laptop GPU
- Blender 5.2.2 LTS (the course chapter ran 5.1.2); glTF exporter 5.2.40
- MCP for Blender server 2.1.9 (pinned), add-on 1.8, protocol 13
- Godot 4.7.2.stable.official.ed1daf0bf, Vulkan 1.4.312, Forward+

## Commands (Windows equivalents of the assignment's macOS commands)
Run in Git Bash from `walker-magic-zhefan/` (Git Bash provides GNU `timeout`):

```
"E:/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe" --headless --path . --import
timeout 120 "E:/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe" --headless --path . --script res://tests/test_a3_assets.gd --fixed-fps 60
```

Import: exit 0, no errors or warnings; it created the three `.glb.import` files and changed no committed `.import` or `.uid` file.
Check: `A3 ASSET CHECK: 22 checks / 0 failures`, exit 0, no Godot process left running.

## Results against the brief

| Check | Rock | Crystal | Chest |
|---|---|---|---|
| Brief W × D × H (m) | 1.0 × 0.8 × 0.7 | 0.35 × 0.35 × 0.6 | 0.8 × 0.5 × 0.6 |
| Blender dimensions (obj.dimensions, read by Claude Code's code; the same value the sidebar shows) (m) | 1.000 × 0.800 × 0.700 | 0.350 × 0.350 × 0.600 | 0.800 × 0.500 × 0.600 |
| Godot bounding box X × Y × Z (headless) | 1.0 × 0.7 × 0.8 | 0.35 × 0.6 × 0.35 | 0.8 × 0.6 × 0.5 |
| Stands along / lowest point (headless) | Y / 0.0 | Y / 0.0 | Y / 0.0 |
| Node scale in Godot | 1, 1, 1, no rotation | 1, 1, 1 | 1, 1, 1 |
| Rotation / scale in Blender after apply | 0 / 1 | 0 / 1 | 0 / 1 |
| Triangles (counted by Claude Code's code and get_scene_info; budget) | 60 (200) | 30 (100) | 76 (150) |
| Triangles predicted in the brief | 3 × 20 = 60 | 3 × 10 = 30 | 12 + 28 + 12 + 12 + 12 = 76 |
| Colours imported vs brief | #343539, #797069 exact | #3558C8 exact; emission on | #8A5A2B, #D4A73A exact |

Godot's axis order is X × Y × Z with Y up, so Godot's Y is the brief's height and Z is the brief's depth.

Extra checks:
- **Front:** the chest's lock (Blender −Y) reaches glTF/Godot +Z = 0.25 while the wood stops at 0.21, so the front faces +Z, as the brief predicted.
- **The .glb files read outside Blender:** each has one node with identity transform, height on Y from 0, the expected triangle count and the expected material values.
- **One light:** the scene check confirms exactly one light in `prop_room.tscn`.
- **Mage size reference:** a Sprite3D of `mage_idle.png` with pixel size 0.0226563 gives a visible height of 1.45 m with her feet at y 0 (worked out from the pixel size, not measured from a render).
- **The check can fail:** Claude Code ran a scratch copy with the rock's brief width changed to 1.1. It reported `rock.size FAIL`, 22 checks / 1 failure, exit 1. So a passing run is not just a script that always passes.

## What the headless check does not show
- Whether the assets read as what they are, or suit the cave. That is the human check below.
- How the colours look under the light, with shadows, or how bright the crystal's glow appears: it compares stored values only.
- The brief's numbers themselves: they were copied by hand into the script, so it would agree with a wrong copy.
- Flat contact with the floor: a lowest point at y = 0 does not show that a stone rests on a face. The rock's 0.066 m floor gap is not tested, and there is no physics.
- The mage's 1.45 m from a render, or the camera framing on screen.

## HUMAN CHECK: look
I opened `res://showcase3d/prop_room.tscn` in the Godot editor and ran it with F6. I looked from the game camera, from above at an angle, and from below through the floor.
- All three assets stand upright on the floor, have closed undersides and show no missing faces.
- The undersides are dark because the only light comes from above.
- The background showed Godot's default grey, and the camera saw the floor's left and front edges. Fixed (see the revision cycles).
- From the side, the mage Sprite3D became a thin line. Fixed by setting it to Y-billboard.
- Beside the 1.45 m mage, the rock, crystal and chest read as what they are, and I am fairly satisfied with them.

No other person looked at the scene.

Screenshots (my own):
- `../blender-session.png` — my Blender session with an 8-vertex cylinder selected (BLENDER-NOTES.md), taken before any asset was built.
- `evidence/prop-room-f6-before-fixes.png` — the F6 run from the game camera, **before the scene fixes** (grey default background, floor edges visible).
- `evidence/prop-room-editor-above-before-fixes.png` — the editor viewport from above at an angle, **before the scene fixes**.
- `evidence/prop-room-editor-below-before-fixes.png` — the editor viewport from below through the floor, **before the scene fixes**.

There is no screenshot from after the scene fixes (background #0F1119, larger floor, Y-billboard mage) in `evidence/` yet.

## Inspect-and-revise cycles
1. **Rock, Revision 1.** Observation: the first build read as three separate stones with a notch between the base stones, and the final fit had stretched it by X 1.19 and Y 1.12, which made the stones look like dice. Cause, found by Claude Code: it had sized the parts from `get_scene_info`'s box, which overstates rotated parts. Revision: the parts were rebuilt to overlap and sized from their real mesh vertex bounds. Result: fit factors 1.000, 1.000, 1.000; the top notch is gone. A 0.066 m gap remained at the floor under the joint; I accepted it as a known limitation.
2. **Chest gold.** Observation in Blender's preview: fully metallic gold (metallic 1.0, roughness 0.35) read dark olive, because a metal shows mostly reflections and the cave scene has only one light. Revision: metallic 0.3, roughness 0.5. Result: In my F6 screenshot (evidence/prop-room-f6-before-fixes.png), the gold bands and lock show as yellow-gold.
3. **Prop room scene.** Observation from my F6 run and editor look: grey default background, visible floor edges, and a mage that turns into a line from the side. Revision: a WorldEnvironment with background #0F1119, a larger floor, and Y-billboard on the mage. The headless check still passes 22 of 22.

## What Claude got wrong
- **The first rock fit** stretched the rock 19% wide, because Claude Code sized parts from an overstated bounding box (cycle 1).
- **Its diagnosis of my hand edit:** after my first attempts did not register, Claude Code concluded my edits were going to a different Blender. My screenshot showed the same Blender; the real cause was probably that my rotation had been cancelled. It corrected itself.
- **Overwriting a moved file:** while organising the Assignment 2 docs, Claude Code wrote a new note over the README it had just moved, because it did not check the path first. It noticed before committing and restored the original from git (blob fc1c4fe).
- **The registration command:** Claude (claude.ai chat) gave me the assignment's `claude mcp add -e DISABLE_TELEMETRY=true blender -- …` order, which fails on my Claude Code because `-e` takes several values and swallowed `blender`. Claude Code found the working order.
- **FRICTIONAL.md:** Claude Code once said the file did not exist; it had been created in bac0f4c.
- **The first test run:** `test_a3_assets.gd` failed to load on its first run (a GDScript typing error); Claude Code typed the variables and re-ran it.
- **`build_rock.py`'s header** numbered the calls wrong (it called the second Rock_A run call 3; the markers say call 4) until Claude Code corrected it before the first commit.

## Known limitations
- The rock has a 0.066 m gap at the floor between its two base stones.
- The chest's lid is an 8-sided prism with a flat top, not a true curve.
- `build_rock.py`, `build_crystal.py` and `build_chest.py` record the code in run order but were not re-run on their own to rebuild the assets. The crystal's hand edit is recorded as a note, not as code.
- `crystal.glb` was exported headlessly from the saved `crystal.blend` (see FRICTIONAL.md, 2026-10-14).
- The crystal's emission comes through as a darker emission colour (#243E92) at energy 1.0, which is how the exporter wrote strength 0.5; how strong the glow looks in the real cave lighting is unknown.
- The prop room is a separate 3D scene; it is not connected to the 2D game yet, as the assignment allows.
