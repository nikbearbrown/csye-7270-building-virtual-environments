# FRICTIONAL — Assignment 3, walker-rudy

What I tried, what I expected, what happened, how I checked it, what I did about it, and what I learned, with my work and Claude's kept apart.

**How this file is written.** Claude Code drafts each entry from our Claude Code conversations and their timestamps, and I check it against what I actually did. Where I recorded no expectation or lesson, the entry says so instead of inventing one. Each entry says when it was written; entries written after the event are labelled as retrospective.

**Tools.** Claude Opus 5.5 in Claude Code (desktop app), Claude Code 2.1.296; Blender 5.2.2 LTS; Godot 4.7.2; MCP for Blender (`mcp-for-blender` 2.1.9, add-on 1.8); macOS.

---

## 2026-10-12 — Learning Blender's window

*Retrospective, written on 2026-10-13.*

- **Attempt (me):** before any prompting, I opened Blender 5.2.2 and looked at the window with the default scene.
- **Result:** [BLENDER-NOTES.md](BLENDER-NOTES.md), the six parts in my own words, and a screenshot of my session with the Cube selected and the sidebar on the Item tab.
- **Human / AI:** the text and the screenshot are mine. Claude converted the screenshot from WebP to PNG and added it to the file; it did not change my text.

## 2026-10-12 — The connector I already had was a different MCP

*Retrospective, written on 2026-10-13.*

- **Expected:** that I had already connected Claude to Blender through a connector in the Claude app.
- **Check (Claude):** read the connector's manifest, `~/Library/Application Support/Claude/Claude Extensions/ant.dir.gh.blender.blender-mcp/manifest.json`.
- **What happened:** it is Blender Lab's MCP server (1.0.1, `projects.blender.org/lab/blender_mcp`), not the community project the assignment names (`ahujasid/mcp-for-blender`). Its tools differ: no `get_scene_info` and no `look`. No Blender extension for it was found in my Blender 5.2 user folder, so there is no evidence it ever reached my Blender.
- **Response (me):** I installed the assignment's MCP instead, and turned the Blender Lab connector off by hand in the Claude app so that only one Blender server is offered to Claude.
- **Human / AI:** Claude found and read the manifest; I chose to switch and turned the connector off.

## 2026-10-12 — Installing MCP for Blender

*Retrospective, written on 2026-10-13. Every command and its full output: [evidence/mcp-setup-log.md](evidence/mcp-setup-log.md).*

- **Attempt:** the assignment's manual steps. Claude ran all the terminal commands in my Claude Code session, from 22:55 EDT.
- **Checks before installing (Claude):** `mcp-for-blender` on PyPI (2.1.9) points to ahujasid's repository, and the README's manual steps, fetched that evening, match the assignment's.
- **Install uv — skipped.** uv 0.10.2 was already installed with uv's official standalone installer (`~/.local/bin`), not Homebrew (`brew list uv`: `No such keg`). The README accepts that installer, so Claude did not install a second copy. Differs from the assignment.
- **Register the server — failed once.**
  - The assignment's line `claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender` returned `Invalid environment variable format: blender, environment variables should be added as: -e KEY1=value1 -e KEY2=value2` and exit code 1.
  - Diagnosis (Claude): `claude mcp add --help` shows `-e, --env <env...>`, which takes several values, so it swallowed the server name. The help's own example puts the name first.
  - Response: `claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender`, which succeeded. The server is in **local** scope: only Claude Code sessions started in `~/csye7270/course-fork` see it.
  - `claude mcp get blender` then said `✔ Connected` although Blender was closed: that only means Claude Code could start the server process.
- **Install the add-on — worked first time.** `uvx mcp-for-blender install-addon` copied `blender_mcp.py` (add-on 1.8, SHA-256 `eb0facf6…297fa5`) into `~/Library/Application Support/Blender/5.2/scripts/addons/` at 22:56 EDT.
- **Defaults, read from the add-on's code (Claude):** the socket listens on `localhost:9876` and starts automatically whenever Blender opens with the add-on enabled; Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D and Tripo are off; content telemetry is off.
- **In Blender (me):** I enabled **Interface: MCP for Blender** in Preferences. The sidebar's MCP for Blender tab showed "Connected on port 9876" and "Addon 1.8 · up to date", with every library and generator checkbox off ([evidence/mcp-panel-connected.png](evidence/mcp-panel-connected.png)).
- **Check that it worked:** in a new Claude Code session at 23:08 EDT, I asked whether Claude could see the Blender MCP; its `get_addon_status` call returned Blender 5.2.2 LTS, protocol 13 of 13 expected, every library and generator off. Claude repeated the call on 2026-10-13 with the same result.
- **Time:** about 15 minutes, from the first command at 22:55 to the working check at 23:08 EDT, well inside the two-hour time box.
- **Unresolved:** I cannot verify that `DISABLE_TELEMETRY=true` stops the anonymous usage record; I have no network check of what the server sends.
- **Human / AI:** Claude ran every terminal command, diagnosed the `-e` order from the help text, and read the add-on's code. I did the steps in Blender's window and checked the panel.

## 2026-10-13 — The server needs Blender open

*Written on 2026-10-13, from the conversation.*

- **Attempt (me):** asked Claude, in that Claude Code session, to call `get_scene_info`.
- **What happened:** at 18:09 EDT it returned `Error getting scene info: Could not connect to Blender. Make sure the Blender addon is running.`
- **Question I asked:** whether Blender must be open, with the MCP server connected, whenever I want to use it.
- **Response (me):** I opened Blender, and at 18:10 EDT the same call returned my scene: `1 camera, 1 light, 1 mesh`, the Cube at `(0.0, 0.0, 0.0)`, `size 2.0x2.0x2.0`, `unit scale 1.0`.
- **What this shows:** the Claude Code side starts on its own, but every tool call needs Blender running with the add-on's server listening.
- **To do:** disable the add-on in Preferences when I am not working on this assignment, because its socket opens every time Blender starts.

## 2026-10-13 — Building the waystone through the MCP

*Written on 2026-10-13, from the conversation. The code of every call, in order: [tools/blender/build_waystone.py](tools/blender/build_waystone.py).*

- **Attempt:** the assignment's workflow for one asset. Claude first called `get_scene_info` (the default scene: a 2 m Cube, a light and a camera, unsaved, unit scale 1.0) and proposed eight steps without building. I approved them, including deleting the camera and light and joining the parts at the end.
- **Built (Claude, one `execute_blender_code` call per object):** an empty scene in metric metres; then the body, the pyramid top, the rectangular rune and the moss, exactly to [CHANGE-BRIEF.md](CHANGE-BRIEF.md) revision 1. After each call, `get_scene_info` reported location, size, rotation, scale and ground.
- **Check (Claude):** 0.70 × 0.40 × 0.84 m, Z from 0 to 0.84; 4 objects, no modifiers, rotation 0 and scale 1 on each; 42 triangles against a budget of 60. The base colours read back from the shader nodes as `#8C8A80`, `#6E7F3C` and `#99E0FF`, the brief's values. Claude converted each hex colour from sRGB to linear before writing it to the node's Base Color, and also set the viewport colour.
- **Claude's own observation, from `look`:** the stone reads as a box with a low gable rather than a weathered standing stone, the rune as a plain rectangle, and the rune's blue looks greyer in Blender's material preview than its value. Claude said these were for me to judge.
- **My hand edit, in Blender's window:** I moved the rune up. Claude read it back: from Z = 0.42 to Z = 0.4537 (+0.034 m), with X, Y and size unchanged, and the file saved at 20:05 EDT. That file is kept as [evidence/waystone-after-hand-edit.blend](evidence/waystone-after-hand-edit.blend).
  - **What it taught me about the interface:** I found that pressing G and Z moved the rune only up and down. When I asked Claude what shortcut that was, it explained that the keys are a sequence, not a chord: G starts a move (Grab), and pressing Z during the move constrains it to the Z axis (twice for the object's local Z). A number typed after them moves by exactly that distance, for example G, Z, 0.03, Enter; R and S take the same axis keys.
- **Revision, from an observation (mine):**
  1. I asked Claude to try a capital R. The waystone in my Assignment 2 art has a rune that looks like an R. Claude built it from three shapes (6 shapes in all, the course limit) and reported 82 triangles, over my budget of 60. I looked at it and rejected it: "现在不好看" (it does not look good).
  2. I asked for a ring. A torus is not one of the course's basic shapes, so Claude made it from two 8-sided cylinders, a blue ring and a stone-coloured disc in front of its middle: 86 triangles.
  3. I asked for 12 sides and a thinner band. Claude rebuilt both cylinders: band 0.03 m (was 0.05), 118 triangles.
  4. I accepted it. Claude added [CHANGE-BRIEF.md](CHANGE-BRIEF.md) revision 2 (the rune and a budget of 130); revision 1 is unchanged.
- **Joined (Claude, approved by me):** the five parts became one object, `Waystone`, with its origin at the world origin, the centre of its underside. Check after joining: location (0, 0, 0), rotation 0, scale 1, 0.70 × 0.40 × 0.84 m, on the ground, 118 triangles, 3 materials (Stone, Moss, Rune), 0 non-manifold edges. Claude looked at it from the front, back, right, three-quarter and from below.
- **A small surprise:** right after the save, the check printed `dirty True`. Claude read it again in a separate call: `dirty False`, with the file's time at 20:43:06 EDT, so the save had taken.
- **Not checked yet:** how it looks in Godot, beside the other two assets; whether the colours survive the export (prediction 5).
- **Human / AI:** Claude proposed the plan, wrote and ran all the code, and measured each step. I approved the plan, did the hand edit, rejected the R, chose the ring, its 12 sides and its thinner band, and accepted the result.

## 2026-10-13 — Building the teleport circle through the MCP

*Written on 2026-10-13, from the conversation. The code of every call, in order: [tools/blender/build_teleport_circle.py](tools/blender/build_teleport_circle.py).*

- **A new file without touching the old one (Claude, at my request):** Blender still had `waystone.blend` open. Rather than reload Blender's start-up file from inside the add-on, Claude saved the session under the new name first, `blender/teleport_circle.blend`, and only then emptied it. Check: `waystone.blend` kept its time (20:43:06) and git showed no change to it.
- **A gap in my brief, found while planning (Claude):** revision 1 said every top face of the circle is at a different height, so no faces overlap. But all three discs started at Z = 0, so their undersides would have shared the floor plane in three colours and flickered when seen from below. Claude proposed raising the inner disc's and the centre disc's undersides to Z = 0.01 and 0.02, inside the rim disc, without changing any top face or the outer size. I agreed; it is [CHANGE-BRIEF.md](CHANGE-BRIEF.md) revision 3. The brief was drafted by Claude and approved by me, so this is a miss by both of us.
- **Built (Claude, one call per object):** the rim, the inner disc, the centre disc and three rune blocks at 90°, 210° and 330°.
- **Check (Claude):** 2.25 × 2.25 × 0.08 m, Z from 0; 6 objects, no modifiers, rotation 0 and scale 1; 280 triangles against a budget of 300; base colours read back as `#F0A830`, `#4A4440`, `#FFD76E`. From below, `look` showed one plain gold face, with no flicker.
- **Claude's observations, from `look`:** in Blender's material preview the gold looks tan rather than glowing gold; the rune blocks read as short dashes; seen edge-on, the 0.08 m disc is almost a line, so the Godot camera will need to look down on it.
- **My request, and the limit it ran into:** I asked for more rune blocks. The circle already had six shapes, the course limit. Claude offered three options: drop the centre disc for a fourth rune (232 triangles), make the three runes larger, or keep it as it is. It also said that an Array modifier would only hide extra cubes, not stay within the limit. I chose to keep it as it is.
- **Joined (Claude):** one object, `TeleportCircle`. Check after joining: origin (0, 0, 0) at the centre of the underside, rotation 0, scale 1, 2.25 × 2.25 × 0.08 m, on the ground, 280 triangles, 3 materials, 0 non-manifold edges. Saved at 21:15:05 EDT.
- **Not checked yet:** how it looks in Godot under the scene's light; whether the colours survive the export (prediction 5).
- **Human / AI:** Claude planned the build, found the undersides gap, wrote and ran all the code, and measured each step. I approved the plan and the revision, asked for more runes, and chose to keep three when the shape limit came up.

## 2026-10-13 — Building the spikes through the MCP

*Written on 2026-10-13, from the conversation. The code of every call, in order: [tools/blender/build_spikes.py](tools/blender/build_spikes.py).*

- **New file (Claude):** saved the session as `blender/spikes.blend` first, then emptied it; `teleport_circle.blend` was left unchanged.
- **Plan (Claude, approved by me):** the wooden base and five 8-sided cones, exactly to [CHANGE-BRIEF.md](CHANGE-BRIEF.md) revision 1. Before building, Claude checked whether the cones' undersides at Z = 0.12 would share a plane with the base's top in a visible way. They do share it, but the cone hides it from above and the base from below, so the brief needed no revision.
- **Built (Claude, one call per object):** the base, then the cones at X = −0.32, −0.16, 0, 0.16 and 0.32.
- **Check (Claude):** 0.80 × 0.30 × 0.47 m, Z from 0; 6 objects, no modifiers, rotation 0 and scale 1; 82 triangles against a budget of 100; a 0.02 m gap between neighbouring cones; colours read back as `#7A5838` and `#5C6168`.
- **Claude's observations, from `look`:** the most recognisable of the three; the base is 0.30 m deep but the cones only 0.14 m across, so a strip of bare wood shows in front of and behind the row; the eight sides of each cone show on close view.
- **My decision:** I looked and changed nothing.
- **Joined (Claude):** one object, `Spikes`. Check after joining: origin (0, 0, 0) at the centre of the underside, rotation 0, scale 1, 0.80 × 0.30 × 0.47 m, on the ground, 82 triangles, 2 materials, 0 non-manifold edges. Saved at 21:31:51 EDT.
- **Not checked yet:** how it looks in Godot; whether the colours survive the export (prediction 5).
- **Human / AI:** Claude planned, wrote and ran all the code and measured each step. I approved the plan and accepted the result unchanged.

## 2026-10-13 — Export, the Godot scene and the headless check

*Written on 2026-10-13, from the conversation.*

- **Where the scene lives (my decision):** a new, separate Godot project in `assignment-3/godot/` that holds only the 3D prop scene. I chose not to copy my Assignment 2 game into it. The assignment says a 2D game's prop scene does not need to be connected to the game yet.
- **Export (Claude, through the MCP):** [tools/blender/export_glb.py](tools/blender/export_glb.py). Claude first read the glTF exporter's option names in Blender 5.2.2 (glTF add-on 5.2.40): `export_yup` is on by default, as the assignment says. Blender had `spikes.blend` open, so Claude exported the spikes from it. For the other two, rather than reloading files from inside the add-on, it appended each object from its own `.blend` into the session, exported it alone and removed it again, so no `.blend` was saved or changed.
- **Check of the files themselves (Claude):** Claude read each `.glb`'s JSON header. Heights are on Y, every node has no translation, rotation or scale, the waystone's ring is on +Z (Blender's −Y front, as the brief predicted), and the eight base colours convert back to the brief's hex values.
- **Godot project (Claude):** `project.godot` (Godot 4.7, Forward Plus) and an import (`godot --headless --path godot --import`). The import created the three `.import` files, then logged `Cannot open file 'res://scenes/props_room.tscn'`, because the main scene did not exist yet.
- **The scene (Claude):** [godot/tools/build_props_room.gd](godot/tools/build_props_room.gd) builds [godot/scenes/props_room.tscn](godot/scenes/props_room.tscn) headless: an 8 × 5 m floor, one directional light with shadows, a camera, the spikes, waystone and teleport circle side by side at Y = 0, and a 1.2 m post marking Rudy's height. Claude used a script rather than writing the `.tscn` by hand, so that the camera is aimed with `look_at`.
- **The headless check (Claude):** [godot/tests/check_props.gd](godot/tests/check_props.gd), run with `timeout 120 … --script res://tests/check_props.gd --fixed-fps 60`.
  - The first run hit two GDScript type-inference parse errors. Godot still exited with code **0**; Claude ran it again without a pipe to confirm that the 0 came from Godot itself. So the exit code alone proves nothing, and the check's last line, `PASS` or `FAIL`, is what to read.
  - After the fix, 44 checks passed ([evidence/check_props-2026-10-13.txt](evidence/check_props-2026-10-13.txt)). Each prop's size matches the brief to 0.005 m, its height is on Y, its origin is at the centre of its underside, every node's scale is 1, its triangles are within budget, and its colours match. In the scene, each prop's lowest point is level with the floor's own top surface.
- **Does the check catch anything? (Claude)** Claude raised the waystone 0.3 m in the scene file and ran the check again. It reported `FAIL  Waystone sits on the floor (lowest point 0.3000 m above the floor's top)`. Claude then rebuilt the scene with the builder script; the result was the same as before apart from Godot's node ids.
- **What the check does not show:** whether the props look right, read as what they are, or suit the game under this light. That is my human check, not done yet.
- **Human / AI:** Claude wrote and ran the export, the project, the scene builder and the check, and tested that the check can fail. I chose a separate project for the scene.

## 2026-10-13 — My look at the scene, screenshots, and TEST-REPORT

*Written on 2026-10-13, from the conversation.*

- **My human check:** I opened the scene in the Godot editor and looked at it: "看完了，没什么问题" (I have looked at it; there is no problem). When Claude asked for specifics, I added (translated): beside the 1.2 m post all three are a suitable size; from behind and below there is no problem; Blender's gold is on the dark side and Godot's is brighter and more golden; the spikes look most like the 2D art and the teleport circle least.
- **Why the teleport circle looks least like its 2D art (mine, translated):** it lacks the circle's pattern of runes and lines, the column of light, and the glow. With three rune blocks, the six-shape limit and flat colours, none of these fits this assignment; they are a next step.
- **Screenshots (Claude):** [godot/tests/capture_props.gd](godot/tests/capture_props.gd) renders the scene in a real window, because the headless renderer draws nothing. It saves five views to [evidence/godot/](evidence/godot/): the camera, behind, low, above, and below the floor.
- **A bug in it, found by looking at the output (Claude):** the first "camera" image showed only sky and an edge of gold. The script had read the camera's global transform before the scene was in the tree, so it got the identity. Waiting one frame fixed it. Claude added the below-the-floor view afterwards, for the assignment's "from behind and below".
- **TEST-REPORT (Claude):** drafted from the runs, the screenshots and this log. My check is quoted as I said it; Claude's observations from the screenshots are listed separately as Claude's.
- **Human / AI:** I did the look in Godot. Claude wrote the screenshot script, found and fixed its bug, and drafted the report.

## 2026-10-13 to 10-14 — Making the film

*Written on 2026-10-14, from the conversation. The film's own records are in [youtube/claude-liam-walker-rudy-3d-props/](youtube/claude-liam-walker-rudy-3d-props/) (CAPTURE.md, FACTCHECK.md, `_qc/FILM-REVIEW.md`).*

- **Attempt:** the required Brutalist explainer. Claude read the `godot-gamedev` skill, its evidence reference and the walker modifier's bookends in `brutalist.art`, and the assignment's film requirements, before building anything.
- **My choice: how to show the hand edit.** There was no screen recording of it. Claude offered (a) re-enact it and record the screen, labelled as a re-enactment, or (b) before/after stills from the two files. I chose (b). No image had been taken between my edit and the R trial, so Claude opened a byte-identical copy of `evidence/waystone-after-hand-edit.blend` in my Blender and called `look` with the same settings as the 19:58 "before" image. The film labels both as comparison stills, not a recording.
- **New evidence (Claude):** a native 4K Movie Maker take of the real scene on an isolated copy of `godot/`, with an autoload that only moves the camera; the headless check re-run (PASS), and run again with the waystone raised 0.3 m on a copy (FAIL, exit 1). The project's files were not changed.
- **Found while making it (Claude):** TEST-REPORT.md and this file said the check run had 46 checks; the log has 44 `ok` lines. I asked Claude to correct both to 44, and the film says 44.
- **Problems the film's own checks found, and the fixes (Claude):** a code panel cut off the lines the narration pointed to (shorter excerpt, narration redone for that beat); two note boxes clipped; the type check read the teleport circle's 2D runes as overlapping labels (that card became a still; the art and the checker were not changed); my stills crossed the title-safe edge by about 20 px (moved). Then the evidence check, the type check and the frame check passed.
- **Not checked by the tools:** whether the explanation is right and the film is good to watch; the frame check samples 40 frames and does not listen.
- **Media:** I uploaded the MP4 to the course Google Drive and gave Claude the link; Claude checked that it opens without signing in and shows the file name, and added it to the README. The MP4 is not in git.
- **Human / AI:** Claude wrote the beat sheet, the narration, the stills, the capture driver and the scripts, rendered the film and wrote its records. I chose option (b), asked for the 46 → 44 correction, and uploaded the film.
