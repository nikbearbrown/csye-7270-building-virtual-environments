# SUBMISSION — CSYE 7270 Assignment 3

| Field | Value |
|---|---|
| **Assignment** | Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender |
| **Student** | zhefan-z |
| **Project name** | walker-magic-zhefan |
| **GitHub repository URL** | https://github.com/nikbearbrown/csye-7270-building-virtual-environments · folder `fall-2026/zhefan-z/assignment-3/` · branch `zhefan-z/assignment-3` |
| **Git tag and submitted commit SHA** | No tag (instructor, 2026-10-09). The submitted commit SHA and PR link are in the Canvas note, since a commit cannot contain its own SHA. |
| **Game-source revision shown in the film** | `8d8895c` (its game files are identical to `1bacec8`; `8d8895c` added only documents outside the project folder). |
| **Godot version, Blender version, and operating system** | Godot 4.7.2.stable.official.ed1daf0bf (Vulkan 1.4.312, Forward+); Blender 5.2.2 LTS with its glTF exporter 5.2.40; Windows 11 Home, NVIDIA GeForce RTX 5060 Laptop GPU. |
| **The three assets and what each is for** | **Rock** (1.0 × 0.8 × 0.7 m, 60 triangles): a roadblock on the path that the player jumps over. **Crystal** (0.35 × 0.35 × 0.6 m, 30 triangles): decoration, a cold-blue glow in the cave scenery. **Treasure chest** (0.8 × 0.5 × 0.6 m, 76 triangles): the reward at the exit after a cleared level, warm on purpose. |
| **MCP project and version** | MCP for Blender: server 2.1.9 (pinned), add-on 1.8. MCP route for all three assets. `crystal.glb` was exported headlessly from its saved `crystal.blend` (`tools/blender/export_crystal.py`) after my Blender session had been reset (FRICTIONAL.md, 2026-10-14). |
| **My hand edit in Blender** | Crystal_Short_B rotation Z from −2.54° to 20°, typed into the sidebar and confirmed with Enter, on the fourth attempt (the first three never reached the scene). The cone was then lengthened ×1.2125 along its own axis to keep the brief's 0.35 m width. |
| **Checks run (command and result)** | See below. |
| **Final film URL and filename** | https://drive.google.com/file/d/1QBK1eDibqnIOKHVK9bmj2RE82UffqI7_/view?usp=drive_link · `csye7270-a3-zhefan-z-walker-magic-3d-assets.mp4` (the master `claude-liam-walker-magic-3d-assets-gamedev.mp4`, renamed only) · "Cold Stone, Warm Gold: Three 3D Props for a Cave Mage", 5:42, 3840×2160, 30 fps, 34,357,326 bytes |
| **Final film SHA-256** | `5d3d8a1ed0708f3763ba398f4f99d1c619e91b93a4bd169a5140ac4afcadc7f7` |
| **Changed games since Assignment 2** | No. Same game, walker-magic-zhefan; a planned HD-2D visual direction is recorded in FRICTIONAL.md (2026-10-08); its gameplay is unchanged so far. |

## Checks run (command and result)

Run in Git Bash from `walker-magic-zhefan/` (Windows equivalents of the assignment's macOS commands; Git Bash provides GNU `timeout`):

| Check | Command | Result |
|---|---|---|
| Headless import | `"E:/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe" --headless --path . --import` | exit 0, no errors or warnings; created the three `.glb.import` files |
| Headless asset check | `timeout 120 "E:/7270/godot/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe" --headless --path . --script res://tests/test_a3_assets.gd --fixed-fps 60` | `A3 ASSET CHECK: 22 checks / 0 failures`, exit 0 (sizes, upright, node scale, triangles, colours, crystal emission, chest front +Z, one light, props on the floor, 1.45 m mage). Recorded on a copy of `8d8895c`: `walker-magic-zhefan/youtube/claude-liam-walker-magic-3d-assets-gamedev/evidence/test_a3_assets-8d8895c.log` |
| The check can fail | the same script with the rock's brief width set to 1.1, in a scratch copy | `rock.size` FAIL, 22 checks / 1 failure, exit 1 |
| `.glb` files read outside Blender | `python -I scripts/read_glb.py <copy of 8d8895c>/assets/models` (in the film folder) | one node each with no transform; height on Y from 0; 60 / 30 / 76 triangles; the chest's gold lock reaches +Z 0.25 (`evidence/glb-read-8d8895c.log`) |
| Film checks (Brutalist) | `./art godot-gamedev --check REEL --game <snapshot of 8d8895c>` · `./art godot-waikthrough --check REEL` · `./art final REEL --height 2160 --fps 30` | PASS · PASS · exported; Gate V 46 frames, 0 BLOCKER, 0 MAJOR |
| HUMAN CHECK: look | Godot editor and F6, from the game camera, from above and from below | upright, closed undersides, no missing faces; the background, floor and billboard fixes (TEST-REPORT.md) |

A fresh-clone check of the submitted commit (import, the asset check, the scene loading, and that the game source matches `8d8895c`) is reported in the Canvas note.

## Summary of my changes

*(Drafted by Claude Code from FRICTIONAL.md and TEST-REPORT.md; the decisions listed are mine.)*

- I chose three assets my game can use (rock, crystal, treasure chest), set the 1.45 m mage scale and the ±0.02 m tolerance, and committed the brief with my own triangle measurements before building (`c75176a`).
- Claude Code built each asset through the Blender MCP from my approved plans; I asked for the rock's Revision 1 (fit factors 1.000), made the hand edit on the crystal, accepted the rock's 0.066 m floor gap, and lowered the chest's gold to metallic 0.3.
- The assets were exported as `.glb` (+Y Up), imported into a new Godot 3D prop room with my mage as a 1.45 m size reference, and checked headlessly; my look in the editor led to the background, floor and billboard fixes.
- The Brutalist film was built by Claude Code from my approved beat sheet with my screenshots; Claude in my claude.ai chat reviewed the script and suggested wording fixes; I watched and listened to the whole film before uploading it.

## Known limitations

From TEST-REPORT.md:
- The rock has a 0.066 m gap at the floor between its two base stones.
- The chest's lid is an 8-sided prism with a flat top, not a true curve.
- `build_rock.py`, `build_crystal.py` and `build_chest.py` record the code in run order but were not re-run on their own to rebuild the assets. The crystal's hand edit is recorded as a note, not as code.
- `crystal.glb` was exported headlessly from the saved `crystal.blend`.
- The crystal's emission comes through as #243E92 at energy 1.0; how strong the glow looks in the real cave lighting is unknown.
- The prop room is a separate 3D scene; it is not connected to the 2D game yet, as the assignment allows.

From the film: the running scene is a scripted camera on a capture copy with a 3840×2160 viewport, not a human look; the outro card is silent because the toolkit copy has no stock jingle; the Your Turn narration ends with the skill's sign-off "Liam, in for Bear.", which is not written in SCRIPT.md.
