# Module 3 — Blender MCP to Godot

CSYE 7270 · Fall 2026 · Week 3

## Executive summary

This module gets a 3D asset from Blender into a Godot game by directing a coding agent, then proves the asset arrived intact. A model that looks right in Blender can arrive in Godot at the wrong size, lying on its side, carrying a scale that breaks its physics, or with a visible box where its collider should be. Each of those is a number a headless test can read. You will have an agent write a Blender Python script that builds a low-poly checkpoint post, run Blender with no window to export a `.glb` file, place it in a copy of a Walker 3D platformer, and test its size, axes, scale, materials, collision and footing. The finished test passes, and a check the agents did not write still found part of the pennant inside the collision hull. None of this shows that the post looks right under the game's lights or feels fair to bump into; those are human checks. The live Blender MCP route is described here but was not run.

## The question

Here is a column that should be 0.2 x 0.2 x 1.8 metres. The companion chapter built it in Blender three times, from the same script with one setting changed, and Godot received it three different ways. AABB is the axis-aligned bounding box Godot reports for a mesh.

```text
good:     node scale (1.0, 1.0, 1.0)  mesh AABB size (0.2, 1.8, 0.2)  AABB in scene (0.2, 1.8, 0.2)
no_yup:   node scale (1.0, 1.0, 1.0)  mesh AABB size (0.2, 0.2, 1.8)  AABB in scene (0.2, 0.2, 1.8)
no_apply: node scale (0.1, 0.9, 0.1)  mesh AABB size (2.0, 2.0, 2.0)  AABB in scene (0.2, 1.8, 0.2)
```

The second lies on its side. The third looks identical to the first in the running game, but its mesh is a two-metre cube wearing a scale of (0.1, 0.9, 0.1), and anything generated from that mesh inherits the scale. A fourth failure appears on none of these lines: a collision hull that Godot silently imports as a visible box with no collision at all. Which facts about an imported model can a test establish, which settings decide them, and what still needs your eyes?

## The ideas

### 1. Two ways for an agent to drive Blender

**The MCP route.** The Model Context Protocol lets a coding agent call tools that another program exposes. For Blender, an add-on opens a local socket inside a running Blender, and a small MCP server process launched by your agent relays tool calls to it. As of 27 September 2026 the chapter found two projects: the community **MCP for Blender** (`github.com/ahujasid/mcp-for-blender`, MIT, needs Blender 3.0+ and `uv`), which the syllabus names, and **Blender MCP** from Blender Lab (`projects.blender.org/lab/blender_mcp`, needs Blender 5.1+). Both run agent-written Python inside Blender without a guard. The community README says its socket has no authentication or encryption, and Blender Lab's page says its server executes LLM-generated code without guards. For this course that means two rules: keep the port on `localhost`, and leave the community add-on's generation services (Rodin, Hunyuan3D, Tripo) switched off unless you have approved the spend, because they call remote services.

**The script route.** Blender runs Python with no window:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_checkpoint_post.py
```

`-b` runs in the background, `--factory-startup` skips your own startup file, and `--python` runs a script that calls the same `bpy` API the MCP tools call. **Add `--python-exit-code 1`.** Without it Blender exits 0 when your script raises an exception: the chapter ran `raise ValueError` both ways and got exit codes 0 and 1.

| | MCP route | Script route |
|---|---|---|
| Blender window | open, add-on connected | none |
| You keep | a transcript of individual tool calls | a `.py` file you can diff, rerun and review |
| Good for | exploring a `.blend`, fixing one object, looking at the viewport | making an asset reproducibly |
| Failure mode | the scene changes and Git records nothing about how | the script encodes a wrong assumption and repeats it faithfully |

Neither route makes the model look right. Both hand you numbers. The worked example uses the script route because it runs headless.

### 2. Units and axes

A Blender unit is a metre in the factory scene (unit scale 1.0, read from `scene.unit_settings` in Blender 5.1.2). glTF measures linear distances in metres ([glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), section 3.4), and Godot's 3D units are metres too, with physics "tuned for this scale" ([Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)). So nothing converts while the Blender scene keeps unit scale 1.0. Size matters for physics, not only looks: the Walker 3D Platformer player is a `CharacterBody3D` with a 2.1 m capsule, 0.4 m radius, under gravity 22 at 120 physics ticks per second. A prop at the wrong scale is a wall the robot cannot climb or a step it does not notice.

Blender is Z-up. glTF and Godot are Y-up ([Model export considerations](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/model_export_considerations.html)). Blender's glTF exporter converts through its **+Y Up** option, on by default in 5.1.2, which puts Blender's Z extent on Godot's Y and Blender's Y extent on Godot's Z. That is a testable claim, and the `no_yup` line above is what breaking it looks like.

### 3. Apply transforms: the object's scale versus the mesh's size

A Blender object has a transform (location, rotation, scale) and mesh data (vertices). Build a pole by scaling a 2 m cube to (0.1, 0.1, 0.9) and the vertices still describe a 2 m cube. The exporter writes that scale onto the node, and Godot shows a `MeshInstance3D` with a non-unit scale: the `no_apply` line. Godot's physics documentation says to avoid translating, rotating or scaling `CollisionShape`s ([Collision shapes (3D)](https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html)), and its export guidance recommends applying the object transform before exporting. In Blender, **Object > Apply > Rotation & Scale** fixes it; in a script, `bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)`. A Godot test can then check both halves: unit scale on every node, and the right size in metres.

One trap for agent-written scripts: in Blender 5.1.2, `obj.dimensions` is not refreshed until the dependency graph is. A script that sets `scale` and prints `dimensions` straight away prints the old size, `(2.0, 2.0, 2.0)`, until `bpy.context.view_layer.update()` runs and it prints `(0.2, 0.2, 1.8)`. If an agent's log is its evidence, make sure the log is current.

### 4. glTF is the interchange format

Godot lists glTF 2.0 as recommended, as text (`.gltf` with a `.bin` and images) or binary (`.glb`) ([Available 3D formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)). Godot can import `.blend` files directly, but only by calling Blender's own exporter, so it needs Blender 3.0+ installed and its path set. Use `.glb` for a small prop: one file, no loose textures. Use `.gltf` when you want Git to show changes in the scene description. Either way the source of truth for how the asset was made is the script. Materials cross as glTF's metallic-roughness model: a Blender material named `PostMetal` arrives as a `StandardMaterial3D` whose `resource_name` is `PostMetal`. Blender-only shader nodes do not cross, and lights do not unless you ask (the exporter's Punctual Lights option defaults to off in 5.1.2).

### 5. The importer's settings, and collision decided at import time

An imported `.glb` gets a text `.import` file whose `[params]` decide what Godot builds. Two lines matter here, `nodes/use_name_suffixes` and `nodes/use_node_type_suffixes`. They are **false** in both of the Platformer demo's model imports, and a fresh import in Godot 4.7.2 sets both to **true**. Copy the demo's `.import` as a template and Godot ignores every naming hint in your model. With the second one on, Godot reads collision hints from node names ([Node type customization](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html)):

| Suffix | What Godot builds |
|---|---|
| `-col` | keeps the mesh and adds a child static collision node with the same geometry (concave) |
| `-convcol` | the same with a convex shape |
| `-colonly` | removes the mesh and creates a `StaticBody3D` collision instead (concave) |
| `-convcolonly` | removes the mesh and creates a `StaticBody3D` with a `ConvexPolygonShape3D` |
| `-noimp` | removes the node |

In glTF the collider must be a mesh; empties become `BoxShape3D` or `SphereShape3D` only with Collada files. For a prop, the usual pattern is a separate, simple mesh named `…-convcolonly`: invisible, convex, cheap, and shaped by you rather than by the visual mesh. You can also skip names and add a `CollisionShape3D` in a wrapper scene, as the demo does. Its enemy has a node named `Box` that holds a `SphereShape3D` and one named `Sphere4` that holds the `BoxShape3D`. Names are claims. The shape is the fact.

## The Walker example: walker-3d-platformer

**What it is.** [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer) is a Walker adaptation of Godot's official 3D Platformer demo: a robot that runs, jumps, shoots and collects coins on a tiled stage while enemies patrol. It copies `3d/platformer` from `github.com/godotengine/godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` and changes the project name only. The engine code is under the Godot contributors' MIT license (`LICENSE.md`), and its `SOURCES.md` warns not to infer that the root license replaces asset-specific notices. The repository is public (checked 6 October 2026), so you can clone it instead of copying from the upstream demo.

**What is in it that matters here.** `project.godot` sets Jolt Physics, 120 physics ticks per second and gravity 22. Two imported glTF models, `player/player.glb` (392 KB, skinned and animated) and `enemy/enemy.glb` (135 KB), both with both suffix settings off. Collision is authored in scenes, not in models: the player's 2.1 m capsule, the enemy's spheres and box, and a `GridMap` stage.

**What its checks establish.** The Walker record lists four normal-input assertions (movement, jump, projectile creation, reset) and a route that observes two coins collected and an enemy hit without writing gameplay state. Its `FRICTIONAL.md` is blunt about limits: exit 0 does not establish label readability. None of those checks touches an imported model's size, materials or collision, and the human playtest is still pending.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Write your answers down before you delegate, and keep them.

1. The post is 0.6 x 0.6 m at the base and 1.8 m tall in Blender. Which Godot axis should carry the 1.8? If you forget +Y Up, what does the test's AABB say?
2. You build the pole from a scaled cube and forget to apply the scale. The visual size is right. What will Godot report for the `MeshInstance3D`'s scale, and why would a collider built from it be a problem?
3. You copy `enemy/enemy.glb.import` as your new `.import` and name the collider `…-convcolonly`. What happens to the collider?
4. A box around "the base and the pole" is 0.6 m wide. The pole is 0.16 m wide. What will the robot bump into?

### 2. Build It

Start from the upstream demo at the commit Walker used:

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Copy `godot-demo-projects/3d/platformer` into a new project folder as `godot/`, run `git init` in the project folder, run `godot --headless --path godot --import` once, and commit that as your baseline. The prompt tells the agent to read `AGENTS.md` and `SOURCES.md`, and copies of those two and `GAME-BRIEF.md` are in [`examples/03-blender-mcp-to-godot/walker-context/`](../../examples/03-blender-mcp-to-godot/walker-context/). The public `walker-3d-platformer` repository already has `godot/`, `AGENTS.md` and `SOURCES.md` at its top level, so cloning it is a shorter start. The recorded run used Blender 5.1.2 at the path below; if your install differs, change only that line of the prompt and record your version.

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

The recorded headless run, on 27 September 2026 (the Blender path is on the allow list so the agent may launch it):

```bash
claude -p "$(cat PROMPT-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(/Applications/Blender.app/Contents/MacOS/Blender:*)" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

If you repeat it, add `--strict-mcp-config`, `--settings '{"autoMemoryEnabled":false}'` and `--disallowedTools "Skill"`, and ask for `--python-exit-code 1` in the prompt's Blender command.

**The Codex difference.** In the recorded run, Codex's `--sandbox workspace-write` could not run Blender at all: four attempts ended in a segmentation fault (exit 139), with a crash log pointing at Blender's Metal GPU check at start-up, which runs even in background mode. Run Blender yourself, outside the sandbox, and let Codex edit the script and the test. Close its standard input when scripting (`< /dev/null`).

**The MCP route (documented, not run).** These steps come from the MCP for Blender README as of 27 September 2026 (PyPI 2.1.1). They were not run, because they need the Blender window and `uv` was not installed on the instructor's Mac. Treat each line as a claim to check.

1. Install `uv` with its official installer (on macOS the README says `brew install uv`); it warns against `pip install uv`.
2. Register the server. `claude mcp add` takes `-e` for environment variables and `--` before the command:

```bash
claude mcp add -e DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender
```

   For Codex:

```bash
codex mcp add --env DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender
```

   `DISABLE_TELEMETRY=true` turns off the usage record the server otherwise sends. `BLENDER_MCP_SAFE_MODE=1` also exists: it blocks scripts that read or write files directly, run other programs or use the network, which would push your export through the server's `export_scene` tool.
3. Install the add-on with `uvx mcp-for-blender install-addon`, then in Blender enable **Interface: MCP for Blender** under **Edit > Preferences > Add-ons**.
4. In the 3D viewport press **N**, open the **MCP for Blender** tab and start the server. Leave the Poly Haven, Sketchfab, Hyper3D, Hunyuan3D and Tripo checkboxes off unless you mean to use them.
5. Give the agent the specification above, but ask for tool calls: `get_scene_info` first, one `execute_blender_code` call per object, `get_object_info` after each, `export_scene` to finish. Then copy every `execute_blender_code` body into `tools/blender/build_checkpoint_post.py`, or Git will not show how the post was built.

Blender Lab's server lists `execute_blender_code_for_cli`, which runs Python in a background Blender process, so an MCP client can also drive headless Blender. It requires Blender 5.1+ and was not tested.

### 3. Use It

Open the project in the Godot editor. Every judgment here is a **HUMAN CHECK**; write down what you observe.

1. Select `props/checkpoint_post.glb` and read the **Import** dock: are the suffix options on? Open **Advanced...**: `Collision` should be a `StaticBody3D`, not a mesh.
2. Open `game.tscn`, find `CheckpointPost`, and look at it beside the robot. **HUMAN CHECK:** does 1.8 m read as "checkpoint" beside a 2.1 m capsule? Is the pennant visible from both sides? It is a single face, and Godot imported its materials with culling disabled, so it should be, but only your eyes confirm it.
3. Turn on **Debug > Visible Collision Shapes** and run the game. Walk the robot into the pole, then into the air beside it. **HUMAN CHECK:** where does it stop? Jump at the pennant. Is what you feel what you see?
4. **HUMAN CHECK:** the agent placed the post 3.0 m from the spawn along +X. Is it in the robot's way at the start? Only play shows.

### 4. Ship It

Commit the Blender script, the `.glb`, its `.import`, the scene change and the test. Do not commit `.godot/`. The `.glb` is a build product of the script; committing both lets a grader run the game without Blender and lets you prove the file matches the script (in the recorded run, re-running the final script produced a byte-identical `.glb`).

Add a `FRICTIONAL.md` entry with the prompt, what the agent reported, what your commands showed, and what you decided about the collider. The fitting Brutalist skill for a film of this work is **godot-gamedev** with the `walker` modifier, from the course-provided checkout: a code excerpt (the script's export call, the `.import` line), then its visible result in the running scene.

### 5. Verify

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_checkpoint_post.py
```

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_checkpoint_post.gd --fixed-fps 60
```

`timeout` is GNU coreutils (on macOS, Homebrew's `coreutils`); it stops a test that errors before `quit()`. The first agent's debug script called a method that does not exist, never reached `quit()`, and ran for eight minutes until it was stopped by hand.

Then run the independent check, `verify_post_independent.gd`, copied from [`examples/03-blender-mcp-to-godot/scripts/independent/`](../../examples/03-blender-mcp-to-godot/scripts/independent/) into the folder you run from. It reads the post's placement from `game.tscn`, casts floor rays that exclude the post's own collider, and asks the physics server which points of the pennant lie inside the collider.

```bash
timeout 120 godot --headless --path godot --script "$PWD/verify_post_independent.gd" --fixed-fps 60
```

**What a pass proves:** the imported scene's size, axes, scale, materials and collision shape are what the test says, and the placed post's base touches the floor collision. **What it does not prove:** that the post looks right lit, that the materials read as metal and cloth, that the collider is fair where it is invisible, or that the placement suits the level.

## What the agents got wrong

Run on 27 September 2026 with Claude Code 2.1.150 and Codex CLI 0.153.4. An agent's "done" is a claim.

- **It pre-wrote the import file from the wrong template.** Before the first import, Claude Code wrote the `.import` file itself from `enemy.glb.import`, which has `use_node_type_suffixes=false`, so `-convcolonly` became a visible `MeshInstance3D` with no collision. It guessed at mesh names, hit its 60-turn limit, and later changed two things at once. A follow-up probe showed the suffix setting alone was enough.
- **Two checks proved less than they claimed.** The final floor ray started 2 m above the post and stopped on the post's own collider, so it proved the post was solid, not that it stood on anything. A ray that excluded the post's body found the floor at y = -4.0, gap 0.0 m. The agent also skipped unnamed materials to get a failing check green.
- **A check that looked at the wrong thing.** Codex's pennant check read only the hull's vertices and printed `overlap 0.0000`. Sampling the pennant on a 1 cm grid, 55 of 1,066 points were inside the collider, reaching x = 0.11 m. That is far better than the first box's 572, and still not zero.
- **A sandbox crash became a hunt for another route.** Blender crashed four times inside Codex's sandbox (exit 139). Codex then reached for a Computer Use tool to operate the Blender application, which refused. The prompt had not repeated "never open its window", and an agent will look for another way when its first one fails.

## If you know Unity or Unreal

| Godot 4.7 | Unity 6 | Unreal Engine 5.8 |
|---|---|---|
| 1 unit = 1 m, Y-up, right-handed | 1 unit = 1 m, Y-up, left-handed | 1 unit = 1 cm, Z-up, left-handed |
| glTF 2.0 built in (recommended) | FBX built in; glTF through the glTFast package | Interchange glTF importer, producing a Static Mesh `.uasset` |
| `.glb.import` (ConfigFile text) | model `.meta` (YAML) | import settings inside a binary `.uasset` |
| `-convcolonly` name suffix | Generate Colliders, or a collider in a prefab | `UCX_` prefix (documented for FBX) |
| `godot --headless --script` with `MeshInstance3D.get_aabb()` | `Unity -batchmode -runTests` with `Renderer.bounds` | Automation test, or editor Python through `-run=pythonscript` |

The Blender half does not change in any engine: the same `bpy` script, the same headless run, the same apply-transforms step. For an agent workflow, the biggest difference is what it can read. Godot's `.import` and `.tscn` files are text it can diff, and Unity's `.meta` and prefabs are diffable YAML under Force Text. Unreal's imported meshes and collision are binary `.uasset` files, inspected through editor Python. Unreal 5.8 also ships an Experimental MCP plugin that its documentation says has no authentication layer. Unity and Unreal were not run; the comparisons come from their documentation, checked on 27 September 2026. The [chapter](../../chapters/03-blender-mcp-to-godot.md) has the full comparison.

## Practice assessment (ungraded)

Answer these in writing, from the source and the running game.

1. You build the pole from a scaled cube and forget to apply the scale. Which of the test's checks catch it, and which still pass?
2. Why does a floor ray that stops on the post's own collider prove nothing about the floor? What must the ray exclude?
3. Write a pennant check that would have caught the 3 cm sliver. Why can a test that reads only the hull's vertices not see it?
4. In `enemy/enemy.tscn`, which shape does the node named `Box` hold? What does that say about a test that finds collision nodes by name?
5. Name two facts about the imported post a headless test can establish and two that only a person at the editor can.

The ungraded Canvas practice quiz has six questions with feedback. Do not paste Claude's explanation as proof of your understanding; ask it to question you, then answer and check the source yourself.

## The next step

Assignment 3, **"Build a Prop in Blender and Make It Work in Godot,"** opens in Module 3, covers Modules 3 and 4, and is due about Day 30. The Canvas assignment page holds its requirements; this lesson adds no graded deliverable. What you practised here, a reproducible script, the import settings, and measurements you can rerun, is what makes a prop of your own provably work in Godot. Module 4 turns to scenes, collision and physics in depth. For the long reading, see [Chapter 3 — Blender to Godot: MCP, Scripts, and a Prop You Can Measure](../../chapters/03-blender-mcp-to-godot.md).
