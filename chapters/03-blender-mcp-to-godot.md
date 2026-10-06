# Chapter 3 — Blender to Godot: MCP, Scripts, and a Prop You Can Measure

CSYE 7270 · Fall 2026 · Week 3

## Executive summary

**What this chapter is.** The Week 3 module: getting a 3D asset from Blender into a Godot game, driven by a coding agent, and proving the asset arrived intact. It covers the two ways an agent can drive Blender (a live MCP connection to the Blender window, and a Python script run by Blender without a window), the units, axes and transforms that decide whether a model arrives at the right size and the right way up, glTF as the interchange format, and the Godot import settings that turn a specially named mesh into collision.

**Why read it.** A model that looks right in Blender can arrive in Godot at the wrong size, lying on its side, carrying a scale that breaks its physics, with a collider missing or a visible box where the collider should be. Every one of those is a number you can check without opening a window. The chapter shows which numbers, and which command reads them.

**What you will build.** In a scratch copy of `walker-3d-platformer`, a coding agent writes a Blender Python script that builds a low-poly checkpoint post (a base, an eight-sided pole and a pennant, with two named materials and a separate collision hull), runs Blender headless to export it as `.glb`, places it in the level, and writes a headless Godot test for its size in metres, its axes, its scale, its materials, its collision and its footing on the floor.

**What it proves and what it does not.** In the worked example the first agent hit its turn limit chasing a missing collider. The cause was one line it had copied from the demo's own import file, and it was fixed only after the session resumed. The second agent's sandbox crashed Blender on start-up. The finished test passes 17 of 17, and a check the agents did not write still found part of the pennant inside the collision hull. None of this shows that the post looks right under the game's lights, reads as a checkpoint, or feels fair to run into. Those are human checks. The MCP route is documented step by step but was not run: it needs the Blender window, which this book's worked examples never open.

---

## The question

Here is a column that should be 0.2 x 0.2 x 1.8 metres. For this chapter we built it in Blender three times, from the same script with one setting changed, and Godot received it three different ways:

```text
good:     node scale (1.0, 1.0, 1.0)  mesh AABB size (0.2, 1.8, 0.2)  AABB in scene (0.2, 1.8, 0.2)
no_yup:   node scale (1.0, 1.0, 1.0)  mesh AABB size (0.2, 0.2, 1.8)  AABB in scene (0.2, 0.2, 1.8)
no_apply: node scale (0.1, 0.9, 0.1)  mesh AABB size (2.0, 2.0, 2.0)  AABB in scene (0.2, 1.8, 0.2)
```

The second lies on its side. The third *looks* identical to the first in the running game: its drawn size is right. But its mesh is a two-metre cube wearing a scale of (0.1, 0.9, 0.1), and anything generated from that mesh inherits the scale. And a fourth failure appears on none of these lines: a collision hull that Godot silently imports as a visible box with no collision at all.

So which facts about an imported model can a test establish, which settings decide them, and what still needs your eyes?

---

## Ideas you need

### 1. Two ways for an agent to drive Blender

**The MCP route.** The Model Context Protocol lets a coding agent call tools that another program exposes. For Blender, a Blender add-on opens a local socket inside a running Blender, and a small MCP server process, launched by your agent, relays tool calls to it. As of 27 September 2026 there are two projects:

| | MCP for Blender (community) | Blender MCP (Blender Lab) |
|---|---|---|
| Where | `github.com/ahujasid/mcp-for-blender` (the old `ahujasid/blender-mcp` address redirects there) | `projects.blender.org/lab/blender_mcp`, documented at `blender.org/lab/mcp-server` |
| Package | PyPI `mcp-for-blender` 2.1.1 ("formerly `blender-mcp`"; existing setups "keep working") | an add-on plus an MCP server named `blender-mcp`; release v1.0.3, 2026-09-11 |
| Needs | Blender 3.0+, Python 3.10+, `uv` | Blender 5.1+ |
| Example tools | `get_scene_info`, `get_object_info`, `get_viewport_screenshot`, `execute_blender_code`, `export_scene`; Poly Haven, Sketchfab and Poly Pizza downloads; Hyper3D Rodin, Hunyuan3D and Tripo generation | `execute_blender_code`, `execute_blender_code_for_cli` ("in a background Blender process"), blend-file summaries, window screenshots, Python API look-ups |
| License | MIT | not stated on the documentation page |

The syllabus names the community project. Both run agent-written Python inside Blender without a guard. The community README: the socket "has no authentication or encryption, so anyone who can reach that port can run Python inside Blender." The Blender Lab page: the server "will execute LLM generated code in Blender without any guards in place to protect your data from removal or being sent to a remote location." For this course that means two rules: keep the port on `localhost`, and leave the community add-on's generation services (Rodin, Hunyuan3D, Tripo) switched off unless you have approved the spend, because they call remote services.

**The script route.** Blender runs Python with no window:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_checkpoint_post.py
```

`-b` runs "in background (often used for UI-less rendering)", `--factory-startup` skips "reading the 'startup.blend' in the user's home directory", and `--python` runs a script (`Blender --help`, 5.1.2). The script calls the same `bpy` API the MCP tools call. **Add `--python-exit-code 1`.** Without it Blender exits 0 when your script raises an exception: we ran `raise ValueError` both ways and got exit codes 0 and 1.

| | MCP route | Script route |
|---|---|---|
| Blender window | open, add-on connected | none |
| The agent sees | tool results, viewport screenshots | the script's stdout, the exported file |
| You keep | a transcript of individual tool calls | a `.py` file you can diff, rerun and review |
| Good for | exploring an existing `.blend`, fixing one object in conversation, looking at the viewport | making an asset reproducibly; anything you must regenerate |
| Failure mode | the scene changes and Git records nothing about how | the script encodes a wrong assumption and repeats it faithfully |

Neither route makes the model look right. Both hand you numbers. The worked example uses the script route because it runs headless.

### 2. Units: a metre is a metre, until it is not

- Blender's factory scene uses the metric system with a unit scale of 1.0, so one Blender unit is one metre (read from `scene.unit_settings` in Blender 5.1.2 with `--factory-startup`).
- glTF: "The units for all linear distances are meters" ([glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), section 3.4).
- Godot: "Godot uses the metric system for everything in 3D, with 1 unit being equal to 1 meter", and "Physics and other areas are tuned for this scale" ([Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)).

So Blender → glTF → Godot needs no conversion while the Blender scene keeps unit scale 1.0. Size matters because of physics, not only looks. Walker 3D Platformer's player is a `CharacterBody3D` whose `CollisionCapsule` is 2.1 m tall with a 0.4 m radius (`godot/player/player.tscn`, confirmed by instantiating it headless), under gravity 22 at 120 physics ticks per second (`project.godot`). A prop at the wrong scale is a wall the robot cannot climb or a step it does not notice.

### 3. Axes: Blender is Z-up; glTF and Godot are Y-up

Blender is right-handed with +Z up. glTF is right-handed with "+Y as up, +Z as forward, and -X as right". Godot is right-handed and Y-up, with "the -Z axis as the camera's forward direction" ([Model export considerations](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html)). Blender's glTF exporter converts on export through its **+Y Up** option ("Export using glTF convention, +Y up"), on by default in Blender 5.1.2's bundled exporter (`io_scene_gltf2` 5.1.20). The conversion puts Blender's Z extent on Godot's Y, and Blender's Y extent on Godot's Z. That is a testable claim; the `no_yup` line above is what breaking it looks like.

### 4. Apply transforms: the object's scale versus the mesh's size

A Blender object has a transform (location, rotation, scale) and mesh data (vertices). Make a pole by adding a 2 m cube and scaling it to (0.1, 0.1, 0.9), and the vertices still describe a 2 m cube; only the object's scale makes it look like a pole. The glTF exporter writes that scale onto the node, and Godot shows a `MeshInstance3D` with a non-unit scale (the `no_apply` line). Godot's physics documentation says to "avoid translating, rotating, or scaling CollisionShapes to benefit from the physics engine's internal optimizations" ([Collision shapes (3D)](https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html)), and its export guidance recommends applying "the object transform in the 3D modeling software before exporting".

In Blender this is **Object > Apply > Rotation & Scale**; in a script, `bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)`, whose operator description reads "Apply the object's transformation to its data." Afterwards the scale is (1, 1, 1) and the vertices carry the real size. A Godot test can check both halves: unit scale on every node, and the right size in metres.

One more trap for agent-written scripts: in Blender 5.1.2, `obj.dimensions` is not refreshed until the scene's dependency graph is. A script that sets `scale` and prints `dimensions` straight away prints the old size: `(2.0, 2.0, 2.0)` before `bpy.context.view_layer.update()`, `(0.2, 0.2, 1.8)` after. If your agent's log is its evidence, make sure the log is current.

### 5. glTF is the interchange format

Godot's documentation lists glTF 2.0 as "**(recommended)**", in text (`.gltf` with a `.bin` and images) and binary (`.glb`) forms ([Available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)). Godot can import `.blend` files directly, but only by calling Blender's own glTF exporter, so it needs Blender 3.0 or later installed and its path set under **Filesystem > Import > Blender > Blender Path**. FBX goes through `ufbx` by default since Godot 4.3. OBJ "doesn't support skinning, animation, UV2 or PBR materials."

Use `.glb` for a small prop: one file, no loose textures. Use `.gltf` when you want Git to show changes in the scene description. Either way the source of truth for *how* the asset was made is the script. Materials cross as glTF's metallic-roughness model: a Blender material named `PostMetal` arrives as a `StandardMaterial3D` whose `resource_name` is `PostMetal`, which the worked example's test checks. Blender-only shader nodes do not cross, and lights do not unless you ask (the exporter's **Punctual Lights** option defaults to off in 5.1.2).

### 6. The scene importer's own settings

An imported `.glb` gets a text `.import` file whose `[params]` decide what Godot builds. Walker 3D Platformer's enemy shows the lines that matter here:

```text
nodes/root_type=""
nodes/root_scale=1.0
nodes/apply_root_scale=false
nodes/use_name_suffixes=false
nodes/use_node_type_suffixes=false
meshes/generate_lods=true
meshes/create_shadow_meshes=true
materials/extract=0
_subresources={}
gltf/naming_version=2
```

`_subresources` stores per-node and per-material choices from the Advanced Import Settings dialog (the player's `.import` is 348,820 bytes because it stores settings for every animation slice). The two `use_*_suffixes` lines are **false** in both of the demo's model imports. A fresh import in Godot 4.7.2 sets both to **true**. Copy the demo's `.import` as a template and Godot ignores every naming hint in your model.

### 7. Collision decided at import time

With node-type suffixes on, Godot reads hints from node names ([Node type customization](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html)):

| Suffix | What Godot builds |
|---|---|
| `-col` | keeps the mesh and adds "a child static collision node ... using the same geometry as the mesh" (concave) |
| `-convcol` | the same with a convex shape |
| `-colonly` | removes the mesh and creates a `StaticBody3D` collision instead (concave) |
| `-convcolonly` | removes the mesh and creates a `StaticBody3D` with a `ConvexPolygonShape3D` |
| `-noimp` | removes the node |

Blender *empties* drawn as a cube or sphere become `BoxShape3D` or `SphereShape3D`, but only "with Collada files"; in glTF the collider must be a mesh. For a prop, the usual pattern is a separate, simple mesh named `…-convcolonly`: invisible, convex, cheap, and shaped by you rather than by the visual mesh. Godot's collision-shapes page says "You can only use concave shapes within StaticBodies", and primitive shapes are faster than convex ones, which are faster than concave ones. You can also skip names and add a `CollisionShape3D` in a wrapper scene, as the demo does. Its player has a capsule; its enemy has five `CollisionShape3D` nodes in `enemy/enemy.tscn`, and the one named `Box` holds a `SphereShape3D` while the one named `Sphere4` holds the `BoxShape3D`. Names are claims. The shape is the fact.

---

## The Walker example: walker-3d-platformer

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** A Walker adaptation of Godot's official 3D Platformer demo: a robot that runs, jumps, shoots and collects coins on a tiled stage while enemies patrol. It copies `3d/platformer` from `github.com/godotengine/godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` and "changes the project name only; gameplay and original assets are retained" (`walker-3d-platformer/README.md`). A `diff` against that upstream folder confirms it: only `project.godot` differs. The engine code is under the Godot contributors' MIT license (`LICENSE.md`), and `SOURCES.md` warns not to "infer that the root software license replaces asset-specific notices". The Walker build is public at [github.com/nikbearbrown/walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer); the upstream path at that commit is its provenance, and it remains a valid starting point.

**What is in it that matters here.** `project.godot` sets `3d/physics_engine="Jolt Physics"`, 120 physics ticks per second and gravity 22. Two imported glTF models, `player/player.glb` (392 KB, skinned and animated) and `enemy/enemy.glb` (135 KB), both with both suffix settings off. Collision authored in scenes, not in models: the player's 2.1 m capsule, the enemy's spheres and box, and a `GridMap` stage whose mesh library pairs tile meshes with collision resources in `stage/collision/`. WAV effects with their own `.import` files.

**What its checks establish.** The Walker record lists "Four normal-input assertions pass: movement, jump, projectile creation, reset", and a feature route that "observes two coins collected and an enemy hit without writing gameplay state" (`GDD.md`). Its `FRICTIONAL.md` records a secret area reached through ordinary inputs on the ninth bounded headless play, and is blunt about limits: "Exit0 does not establish label readability." None of those checks touches an imported model's size, materials or collision. Human playtest, listening and visual review are still pending in the series ledger (`walker-demo-series/queue.json`, `"human_review": "pending"`).

---

## Hands-on: build a checkpoint post in Blender, headless, and verify it in the platformer

### Predict

1. The post is 0.6 x 0.6 m at the base and 1.8 m tall in Blender. Which Godot axis should carry the 1.8? If you forget +Y Up, what does the test's AABB say?
2. You build the pole from a scaled cube and forget to apply the scale. The visual size is right. What will Godot report for the `MeshInstance3D`'s scale, and why would a collider built from it be a problem?
3. Copy `enemy/enemy.glb.import` as your new `.import` and name the collider `…-convcolonly`. What happens to the collider?
4. A box around "the base and the pole" is 0.6 m wide. The pole is 0.16 m wide. What will the robot bump into?

### Build It

Start from the upstream demo at the commit Walker used:

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `godot-demo-projects/3d/platformer` into a new folder as `godot/`, `git init` it, run `godot --headless --path godot --import` once, and commit that as your baseline. The worked example also had Walker's Markdown files beside `godot/`; the prompt tells the agent to read `AGENTS.md` and `SOURCES.md`, and copies of those two and `GAME-BRIEF.md` are in `examples/03-blender-mcp-to-godot/walker-context/` if you want the same context.

**Prompt 1, the script route.** Paste into Claude Code, or save as `PROMPT-1.txt`:

```text
This repository is a scratch copy of walker-3d-platformer (Godot 4.7.2, GDScript,
Jolt physics). Read AGENTS.md, SOURCES.md and godot/player/player.tscn first.

Task: build one small low-poly prop in Blender from a script, export it as
binary glTF, place it in the game, and prove its size, materials and collision
with a headless test. One bounded change: do not edit any existing script, the
player, the enemies, the stage, or project.godot.

Blender 5.1.2 is at /Applications/Blender.app/Contents/MacOS/Blender. Run it only
in background mode (-b --factory-startup --python <script>). Never open its window.

1. Write tools/blender/build_checkpoint_post.py (bpy). Start from an empty scene
   with metric units. Build a checkpoint post with Blender's +Z up and the origin
   at the centre of the base's underside: a 0.6 x 0.6 x 0.1 m base, an 8-sided
   pole 0.08 m in radius whose top is 1.8 m above the floor, and a flat pennant
   0.4 m long and 0.25 m tall hanging from the top of the pole along +X.
   Use two named materials: PostMetal (base and pole) and FlagCloth (pennant).
   Add a separate box collider around the base and pole only, not the pennant,
   named with Godot's convex-collision-only import suffix. Apply rotation and
   scale on every object. Print each object's name, dimensions, scale and
   material names, then export godot/props/checkpoint_post.glb (binary glTF,
   +Y up, apply modifiers).
2. Run Blender headless on the script and save its output to
   tools/blender/build_checkpoint_post.log.
3. Run godot --headless --path godot --import. Read the new .import file and
   tell me which of its settings decide whether the suffix is honoured.
4. Place one instance of the imported scene in game.tscn, standing on the floor
   about 3 m from the player's start and clear of the player's first steps.
5. Write godot/tests/test_checkpoint_post.gd (extends SceneTree). Print one
   PASS/FAIL line per check and exit non-zero on any failure. Load the imported
   scene and check: the merged visual AABB matches the Blender dimensions from
   step 1 within 1 cm, with Blender's Z extent appearing on Godot's Y; every
   MeshInstance3D has unit scale; the only materials are PostMetal and FlagCloth;
   a StaticBody3D holds a ConvexPolygonShape3D whose bounds cover the base and
   pole but not the pennant; the prop is shorter than the player's collision
   capsule. Then load game.tscn, step a few physics frames, and use a downward
   ray to show that the placed post stands on the floor.
6. Run the test and the import again and report the real output. List what
   still needs a person to look at in the running game.
```

Our headless run (the Blender path is on the allow list so the agent may launch it):

```bash
claude -p "$(cat PROMPT-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(/Applications/Blender.app/Contents/MacOS/Blender:*)" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

If you repeat it, add `--strict-mcp-config`, `--settings '{"autoMemoryEnabled":false}'` and `--disallowedTools "Skill"`, and ask for `--python-exit-code 1` in the prompt's Blender command.

**The Codex difference.** In our run, Codex's `--sandbox workspace-write` could not run Blender at all: four attempts ended in a segmentation fault (exit 139), with a crash log pointing at Blender's Metal GPU check during start-up, which runs even in background mode. Run Blender yourself, outside the sandbox, and let Codex edit the script and the test. Close its standard input when scripting (`< /dev/null`).

**The MCP route (documented, not run for this chapter).** These steps are from the MCP for Blender README as of 27 September 2026 (PyPI 2.1.1). They were not run: they need the Blender window, and `uv` was not installed on the instructor's Mac. Treat each line as a claim to check.

1. Install `uv` with its official installer (on macOS the README says `brew install uv`); it warns against `pip install uv`.
2. Register the server. For Claude Code (`claude mcp add` takes `-e` for environment variables and `--` before the command):

```bash
claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender
```

   For Codex:

```bash
codex mcp add --env DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender
```

   `DISABLE_TELEMETRY=true` turns off the "minimal anonymous usage record" the server otherwise sends; per the README, prompts, code and screenshots are collected only if you opt in. `BLENDER_MCP_SAFE_MODE=1` also exists: it blocks scripts that read or write files directly, run other programs or use the network, which would push your export through the server's `export_scene` tool (it takes an absolute path and `glb` or `fbx`).
3. Install the add-on with `uvx mcp-for-blender install-addon`; in Blender, **Edit > Preferences > Add-ons**, enable **Interface: MCP for Blender**.
4. In the 3D viewport press **N**, open the **MCP for Blender** tab and start the server. The README's quick start calls the button **Start MCP Server**; its Usage section calls it **Connect to Claude**. Leave the Poly Haven, Sketchfab, Hyper3D, Hunyuan3D and Tripo checkboxes off unless you mean to use them.
5. Give the agent the specification above, but ask for tool calls: `get_scene_info` first, one `execute_blender_code` call per object, `get_object_info` after each, `export_scene` to finish. Then copy every `execute_blender_code` body into `tools/blender/build_checkpoint_post.py`, or Git will not show how the post was built.

Blender Lab's server lists `execute_blender_code_for_cli`, which runs Python "in a background Blender process", so an MCP client can also drive headless Blender. It requires Blender 5.1+ and was not tested here.

### Use It

1. Open the project in the Godot editor. Select `props/checkpoint_post.glb` and read the **Import** dock: are the suffix options on? Open **Advanced...** and look at the scene tree: `Collision` should be a `StaticBody3D`, not a mesh.
2. Open `game.tscn`, find `CheckpointPost`, and look at it next to the robot. Does 1.8 m read as "checkpoint" beside a 2.1 m capsule? Is the pennant visible from both sides? It is a single face; glTF marks both materials double-sided, and Godot imported them as `StandardMaterial3D` with `cull_mode = 2` (culling disabled), so it should be, but only your eyes confirm it.
3. Turn on **Debug > Visible Collision Shapes** and run the game. Walk the robot into the pole, then into the air beside it. Where does it stop? Jump at the pennant. Is what you feel what you see?
4. Check that the post is not in the robot's way at the start. The agent placed it 3.0 m from the spawn along +X; whether that blocks the opening route is something only play shows.

### Ship It

Commit the Blender script, the `.glb`, its `.import`, the scene change and the test. Do not commit `.godot/`. The `.glb` is a build product of the script; committing both lets a grader run the game without Blender and lets you prove the file matches the script (in our run, re-running the final script produced a byte-identical `.glb`: `git status` showed no change).

Add a `FRICTIONAL.md` entry with the prompt, what the agent reported, what your commands showed, and what you decided about the collider. The fitting Brutalist skill for a film of this work is **godot-gamedev** with the `walker` modifier: a code excerpt (the Blender script's export call, the `.import` line), then its visible result in the running scene.

### Verify

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_checkpoint_post.py
```

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_checkpoint_post.gd --fixed-fps 60
```

`timeout` is GNU coreutils (on macOS, Homebrew's `coreutils`); it stops a test that errors before `quit()`. The worked example needed it: the first agent's debug script called a method that does not exist, never reached `quit()`, and ran for eight minutes until we stopped it.

Then the independent check, `examples/03-blender-mcp-to-godot/scripts/independent/verify_post_independent.gd`, run the same way with an absolute `--script` path. It reads the post's placement from `game.tscn`, casts floor rays that exclude the post's own collider, and asks the physics server which points of the pennant lie inside the collider.

What a pass proves: the imported scene's size, axes, scale, materials and collision shape are what the test says, and the placed post's base touches the floor collision. What it does not prove: that the post looks right lit, that the materials read as metal and cloth, that the collider is fair where it is invisible, or that the placement suits the level.

---

## What we actually ran

**When and with what.** 27 September 2026, macOS on an Apple M4 Pro. Godot `4.7.2.stable.official.ed1daf0bf`, Blender 5.1.2 (glTF exporter 5.1.20), Claude Code 2.1.150 (transcripts record `claude-sonnet-4-6`), Codex CLI 0.153.4 (`gpt-5.6-sol`, reasoning low). Baseline: the `godot/` folder and Markdown files of the local `walker-3d-platformer` (identical to upstream `3d/platformer` at `a3b5c11` except the project name), committed in a scratch repository; the import ran clean. Full record: [`../examples/03-blender-mcp-to-godot/`](../examples/03-blender-mcp-to-godot/).

**Run 1, Claude Code, Prompt 1.** The agent read the project, then did something the prompt did not ask for: before the first import it *wrote* the `.import` file itself, using `enemy.glb.import` as its template. It switched `use_name_suffixes` to true and left `use_node_type_suffixes=false`, exactly the setting that disables `-convcolonly`. Its first Blender run failed with `ValueError: faces.new(...): face already exists` (it had added the pennant's back face as a second face over the same four vertices); it fixed that, and Blender printed the objects:

```text
Base                   dims=(0.6000, 0.6000, 0.1000)  scale=(1.000, 1.000, 1.000)  materials=['PostMetal']
Collision-convcolonly  dims=(0.6000, 0.6000, 1.8000)  scale=(1.000, 1.000, 1.000)  materials=[]
Pennant                dims=(0.4000, 0.0000, 0.2500)  scale=(1.000, 1.000, 1.000)  materials=['FlagCloth']
Pole                   dims=(0.1600, 0.1600, 1.7000)  scale=(1.000, 1.000, 1.000)  materials=['PostMetal']
```

It built every vertex at its real coordinates, so "apply rotation and scale" was a no-op, which its own comment said. It placed the post in `game.tscn` with a node ID it made up (`unique_id=987654321`). Its test then failed: no `StaticBody3D`. Now the transcript shows the difference between a diagnosis and a guess. The agent decided that "Godot 4.7 seems to check the **mesh name** too", renamed the mesh data, rebuilt and reimported: no change. It wrote a debug script that called a method that does not exist on a nil object; the script never reached `quit()`, and headless Godot kept running. At 61 turns the session hit `--max-turns` (`error_max_turns`, 21 minutes). Nine commands had been refused by the allow list along the way: `tee`, `sed -n`, `python3`, and compound commands.

The session was not over. When we stopped the hung Godot process, the background task's completion woke the agent in the same `-p` session, and it carried on for 24 more turns. It changed *two* things at once: it set `use_node_type_suffixes=true` **and** added a `_subresources` block asking Godot to generate physics for the collision node. The collider appeared, so the fix could not tell you which change mattered. Then the context was compacted, and the agent forgot that `godot` was on the path: it tried `/Applications/Godot.app/Contents/MacOS/Godot` seven times (nine refusals in this phase), and ended by asking a human to approve the command. It never ran its own finished test.

We ran it: 16 of 16 checks passed. We then checked what the agent had not.

- **Which fix mattered.** A fresh import of the same `.glb` in an empty project uses Godot's defaults (`use_name_suffixes=true`, `use_node_type_suffixes=true`) and produces `StaticBody3D [Collision]` with a `ConvexPolygonShape3D`. Set only `use_node_type_suffixes=false`, reimport, and the collider comes back as `MeshInstance3D [Collision-convcolonly]`: a visible box with no collision at all. The suffix alone was enough; `_subresources` was redundant.
- **The floor check was not a floor check.** The agent first placed the post at the player's spawn height, y = -3.84189. Its first test run, while the collider was still missing, sent a ray straight through the post to the floor at y = -4.0, so the post had been floating 16 cm up; the agent moved it to -4.0. But the finished test's ray starts 2 m above the post and stops on the post's own collider at y = -2.2: it proves the post is solid, not that it stands on anything. Only a header comment remembers the earlier ray. Our ray, excluding the post's body, found the `GridMap` floor at y = -4.0 under the post and at three offsets around it: gap 0.0 m. The placement was right; the finished test could not have told you.
- **A check was weakened to get green.** The first run failed "no unexpected materials" because the imported collision box carried an unnamed default material. The agent's later version skips unnamed materials. Assignment 2's rule applies here too: do not weaken an expected result merely to obtain a green report.
- **The pennant was inside the collider.** The box ran to x = 0.3; the pennant runs from 0.08 to 0.48. Sampling the pennant on a 1 cm grid and asking the physics server, 572 of its 1,066 points were inside the collider. The agent's check (`X_max <= 0.35`) passed anyway.
- **Two constants posing as facts.** The capsule height (2.10) and the post's position were constants in the test, not read from the scenes.

**Run 2: the revision.** Claude Code refused a new session ("You've hit your session limit"; many parallel sessions had used the day's allowance), so the revision went to Codex:

```text
The previous agent run (Claude Code) stopped at the turn limit, resumed, and
ended without running its own test. Finish it as one bounded revision. Start by reading
godot/props/checkpoint_post.glb.import and git show HEAD --stat.

1. Using Godot's "Node type customization" documentation, find the one import
   setting that stopped the -convcolonly suffix from working, and fix only that.
   Remove the _subresources physics block the previous run added, and give the collision mesh
   data its plain name again, so we can see whether the suffix alone does the job.
   Delete godot/tests/debug_tree.gd, godot/tests/debug_options.gd and
   tools/blender/inspect_glb.py, with their .uid files.
2. Make the floor check honest: read the post's transform from game.tscn instead
   of a constant, cast the downward ray with the post's own StaticBody3D
   excluded, and require the floor to be within 2 cm of the post's base.
3. Read the capsule height from player/player.tscn instead of a constant.
4. Replace the "collision X_max <= 0.35" check with one that measures how much
   of the pennant's length lies inside the collider, and fails if any does. Then
   change the collider in the Blender script so that check passes while the base
   and the pole stay fully covered.
5. Rebuild with Blender headless, reimport, and run
   godot --headless --path godot --script res://tests/test_checkpoint_post.gd --fixed-fps 60
   Report the real output and git diff --stat. Do not commit.
```

```bash
codex exec --sandbox workspace-write --json "$(cat PROMPT-2-codex.txt)" < /dev/null > session-2-codex.jsonl
```

Codex identified `nodes/use_node_type_suffixes` from the documentation (it ran a web search), found it already corrected, removed `_subresources`, deleted the debug files, restored the mesh name, and rewrote the three checks as asked. For the collider it replaced the box with a tapered convex hull: ±0.3 m at the base, narrowing to ±0.08 m at the top of the pole. Then it tried to rebuild. Blender crashed in its sandbox four times (exit 139), with and without a private temporary folder, a separate config folder, and a `--gpu-backend` flag. Next, Codex reached for a Computer Use tool to operate the Blender *application* ("Initialize Blender so its headless build can access the graphics backend"). That tool refused: "Computer Use was not approved to use Blender". We stopped the run there, five and a half minutes in. The prompt had not repeated Chapter 3's "never open its window" rule, and an agent will look for another way when its first one fails.

We ran the rest ourselves, outside the sandbox: Blender (exit 0), import, test. **17 of 17 passed**: AABB 0.78 x 1.8 x 0.6 m with the 1.8 on Y; unit scale on all three meshes; materials exactly PostMetal and FlagCloth; one `StaticBody3D` with a `ConvexPolygonShape3D`; the capsule height read from `player.tscn` (2.1); a floor ray with the post excluded hitting y = -4.0, 0.0000 m from the base; and "no pennant length lies inside collider [overlap 0.0000 m]".

That last line is wrong. Codex's check looked only at the hull's *vertices* at the pennant's height, and the vertices there are the pole's corners at x = 0.08. The hull's slanted faces are not vertices. Our physics sampling: **55 of 1,066 pennant points are inside the collider, reaching x = 0.11 m**, a 3 cm sliver along the pennant's lower edge. Far better than the box's 572, still not zero. We left it unfixed: it is question 4 below. The tapered hull also leaves invisible collision around the pole, 11 cm on each side at mid-height, which is a design judgment, not a test result.

## Check your understanding (ungraded)

1. Set `export_yup=False` in the Blender script, rebuild and rerun the test. Which checks fail, and what AABB does Godot report? Compare with the `no_yup` probe line.
2. Build the pole as `primitive_cylinder_add` scaled to size, without applying scale. Which check fails? Does any check still pass that should not?
3. Copy `enemy/enemy.glb.import`'s `[params]` over the post's and reimport. Predict the scene tree, then print it with the probe script in `examples/03-blender-mcp-to-godot/scripts/independent/`.
4. Replace the tapered hull with two convex pieces, a box for the base and a box for the pole, so that no pennant point is inside. What does Godot build from two `-convcolonly` meshes? Then rewrite Codex's pennant check so it would have caught the 3 cm sliver.
5. In `enemy/enemy.tscn`, which shape does the node named `Box` hold? What does that tell you about a test that finds collision nodes by name?
6. Why did the first Blender failure (`face already exists`) not stop the agent's `Blender -b` command with a non-zero exit? What flag fixes that, and what similar trap did Chapter 2 find in Godot?

---

## Doing the same thing in Unity

### Similarities

The Blender half does not change: the same `bpy` script, the same headless run, the same apply-transforms step. Unity also expects metres: "Unity's physics system expects 1 m in the game world to be 1 unit in the imported file" ([Model import settings](https://docs.unity3d.com/Manual/FBXImporter-Model.html)). Unity is Y-up, so Blender's Z-up still gets converted somewhere. And the verification idea carries over: load the imported model in a test, measure its renderer bounds, list its materials, inspect its colliders.

### Differences

- **Format.** Unity's built-in model pipeline is FBX-first. Its Model tab offers **Scale Factor**, **Convert Units**, **Bake Axis Conversion** (for "a model that uses a different axis system than Unity") and **Generate Colliders** ("Import the mesh with mesh colliders automatically attached") ([Model import settings](https://docs.unity3d.com/Manual/FBXImporter-Model.html)). glTF comes through the **glTFast** package, which "uses Unity's ScriptedImporter interface and will register itself as the default importer for the .gltf and .glb extensions" ([glTFast editor import](https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.15/manual/ImportEditor.html)). In Godot, glTF is the default path; in Unity it is a package.
- **Handedness.** "Unity uses a left-handed coordinate system: the positive x-axis points to the right, the positive y-axis points up, and the positive z-axis points forward" ([Rotation and orientation](https://docs.unity3d.com/6000.3/Documentation/Manual/QuaternionAndEulerRotationsInUnity.html)). Blender, glTF and Godot are right-handed. The importer converts; a script that places things by coordinates has to know which way is forward.
- **Collision.** Unity has no name-suffix convention like `-convcolonly`. You choose the importer's Generate Colliders (a mesh collider on every mesh, the cousin of `-col`) or add a `BoxCollider` or convex `MeshCollider` in a prefab, often from an `AssetPostprocessor` script so the rule is code rather than a checkbox.
- **What an agent can read.** Import settings live in the model's `.meta` file and the wrapper prefab is YAML under Force Text serialization; both are diffable text, like Godot's `.import` and `.tscn`.
- **Headless verification.** An Edit Mode test can load the model through `AssetDatabase`, instantiate it and assert on `Renderer.bounds`, `sharedMaterials` names and `Collider` components, run with `-runTests -batchmode -testPlatform EditMode` ([Test Framework command line](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)).
- **Agent bridge on the Unity side.** Unity's AI Assistant package documents a Unity MCP server for clients such as Claude Code; the current package documentation (2.20.0-pre.1) marks it deprecated: "Use the Unity command-line interface (CLI) instead" ([AI client integration with Unity](https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.20/manual/integration/unity-mcp-overview.html)). That bridges an agent to Unity, not to Blender.

| Godot 4.7 | Unity 6 |
|---|---|
| glTF 2.0 built in (recommended) | FBX built in; glTF through glTFast |
| Right-handed, Y-up, 1 unit = 1 m | Left-handed, Y-up, 1 unit = 1 m |
| `.glb.import` (ConfigFile) | model `.meta` (YAML) |
| `-convcolonly` name suffix | Generate Colliders, or a `BoxCollider` / `MeshCollider` in a prefab |
| `MeshInstance3D.get_aabb()` | `Renderer.bounds` |
| `godot --headless --script` | `Unity -batchmode -runTests` |

## Doing the same thing in Unreal Engine

### Similarities

Unreal imports glTF through its **Interchange** framework, "file format agnostic, asynchronous, customizable, and can be used at runtime", with the Interchange Editor and Interchange Framework plugins enabled by default ([Importing assets using Interchange](https://dev.epicgames.com/documentation/unreal-engine/importing-assets-using-interchange-in-unreal-engine?lang=en-US)). Like Godot, Unreal reads collision intent from names: the documented FBX pipeline treats a mesh named `UCX_<RenderMeshName>` as custom convex collision, removes it from the render mesh and turns it "into the collision model" ([FBX static mesh pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine)). Same idea as `-convcolonly`: a simple invisible hull you shaped yourself. Whether the glTF path through Interchange honours `UCX_` names is not stated on the pages we checked; test it before relying on it.

### Differences

- **Units and axes.** "1 Unreal Unit is 1 centimeter", and the editor's coordinate system is left-handed and Z-up ([Coordinate system and spaces](https://dev.epicgames.com/documentation/en-us/unreal-engine/coordinate-system-and-spaces-in-unreal-engine)). A 1.8 m post is 180 units. The importer converts; a test's expected numbers change by a factor of 100, and "up" is Z again.
- **Binary assets.** The imported Static Mesh, its materials and its collision are `.uasset` files that an agent cannot diff; it inspects them through editor Python or C++. Headless: `UnrealEditor-Cmd.exe <project>.uproject -run=pythonscript -script=<file>` runs Python without the editor UI ([Scripting the editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)), and automation tests run with `-ExecCmds="Automation RunTest <name>;Quit"` ([Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)).
- **Agent bridge on the Unreal side.** UE 5.8 ships an **Experimental** Unreal MCP plugin that "embeds an MCP server inside the Unreal Editor process" at `http://127.0.0.1:8000/mcp`, over HTTP, and "has no authentication layer" ([Unreal MCP in Unreal Editor](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US)). With it the MCP pattern runs at both ends: one server drives Blender, another drives the engine. Each end is unauthenticated local code execution, and neither measures the result for you.

| Godot 4.7 | Unreal Engine 5.8 |
|---|---|
| 1 unit = 1 m, Y-up, right-handed | 1 unit = 1 cm, Z-up, left-handed |
| glTF importer → `PackedScene` | Interchange glTF importer → Static Mesh `.uasset` |
| `-convcolonly` suffix | `UCX_` prefix (documented for FBX) |
| `.glb.import`, text | import settings inside a binary `.uasset` |
| GDScript `SceneTree` test | Automation test, or editor Python through `-run=pythonscript` |
| MCP for Blender drives Blender only | Unreal MCP (Experimental) drives the editor |

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 27 September 2026 (Unity manual pages served for Unity 6.x, Unreal pages for UE 5.8). The MCP route was not run; its steps come from the projects' own pages on the same date.

**Godot (documentation, stable branch, and the 4.7.2 binary)**
- Available 3D formats: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html
- Model export considerations: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html
- Node type customization: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html
- Introduction to 3D: https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html
- Collision shapes (3D): https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html
- Import process: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html
- Probed in Godot 4.7.2 (`examples/03-blender-mcp-to-godot/scripts/`): fresh-import suffix defaults, the effect of `use_node_type_suffixes=false`, the axis and apply-scale probes, the player capsule, the floor rays and pennant sampling.

**Blender and glTF**
- `Blender --help` (5.1.2): `-b`, `--factory-startup`, `--python`, `--python-exit-code`; bundled `io_scene_gltf2` 5.1.20 operator properties (`export_yup`, `export_apply`, `export_lights`) read with `bpy`; `bpy.ops.object.transform_apply` description.
- glTF 2.0 specification, section 3.4: https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html

**Blender MCP projects**
- MCP for Blender (community), README and `src/blender_mcp/server.py`: https://github.com/ahujasid/mcp-for-blender ; PyPI: https://pypi.org/project/mcp-for-blender/
- Blender MCP (Blender Lab): https://projects.blender.org/lab/blender_mcp (readme, `readme_tools.rst`, releases API) and https://www.blender.org/lab/mcp-server/

**Walker files**
- `walker-3d-platformer`: `README.md`, `SOURCES.md`, `GDD.md`, `FRICTIONAL.md`, `godot/project.godot`, `godot/player/player.tscn`, `godot/enemy/enemy.tscn`, `godot/enemy/enemy.glb.import`, `godot/player/player.glb.import`
- `walker-demo-series/queue.json`
- Upstream: https://github.com/godotengine/godot-demo-projects (commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, `3d/platformer`)
- Old course: Canvas export pages "Animation in Blender", "Introduction to Houdini", "SideFX Houdini" (context only)

**Coding CLIs**
- `claude --help` and `claude mcp add --help` (2.1.150); `codex exec --help` and `codex mcp add --help` (0.153.4)

**Unity (documentation only)**
- Model import settings: https://docs.unity3d.com/Manual/FBXImporter-Model.html
- glTFast editor import: https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.15/manual/ImportEditor.html
- Rotation and orientation: https://docs.unity3d.com/6000.3/Documentation/Manual/QuaternionAndEulerRotationsInUnity.html
- Test Framework command line: https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html
- AI client integration with Unity (MCP): https://docs.unity3d.com/Packages/com.unity.ai.assistant@2.20/manual/integration/unity-mcp-overview.html

**Unreal Engine (documentation only)**
- Importing assets using Interchange: https://dev.epicgames.com/documentation/unreal-engine/importing-assets-using-interchange-in-unreal-engine?lang=en-US
- FBX static mesh pipeline: https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine
- Coordinate system and spaces: https://dev.epicgames.com/documentation/en-us/unreal-engine/coordinate-system-and-spaces-in-unreal-engine
- Scripting the editor using Python: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python
- Run automation tests: https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- Unreal MCP in Unreal Editor: https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor?lang=en-US
