# Prompts — Chapter 3 worked example

The exact prompts and command lines used on 2026-09-27, each run from the root of the scratch copy of `walker-3d-platformer` (`godot/` plus its Markdown files). Prompt text was passed with `"$(cat PROMPT-N.txt)"`.

## Run 1 — Claude Code 2.1.150 (model recorded: claude-sonnet-4-6)

```bash
claude -p "$(cat PROMPT-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(/Applications/Blender.app/Contents/MacOS/Blender:*)" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

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

## Run 2, first attempt — Claude Code (refused: "You've hit your session limit")

```bash
claude -p "$(cat PROMPT-2.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(/Applications/Blender.app/Contents/MacOS/Blender:*)" --max-turns 60 --strict-mcp-config --settings '{"autoMemoryEnabled":false}' --output-format stream-json --verbose > session-2.jsonl < /dev/null
```

```text
Your previous run stopped at the turn limit, resumed, and ended without running
its own test. Finish it as one bounded revision. Start by reading
godot/props/checkpoint_post.glb.import and git show HEAD --stat.

1. Using Godot's "Node type customization" documentation, find the one import
   setting that stopped the -convcolonly suffix from working, and fix only that.
   Remove the _subresources physics block you added, and give the collision mesh
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

## Run 2 — Codex CLI 0.153.4 (gpt-5.6-sol, reasoning low)

The same prompt with the first sentence and one phrase changed to say the previous run was Claude Code's.

```bash
codex exec --sandbox workspace-write --json "$(cat PROMPT-2-codex.txt)" < /dev/null > session-2-codex.jsonl
```

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

## Steps the operator ran (outside any agent sandbox)

Codex's sandbox crashed Blender at start-up (exit 139, four attempts), so after stopping the Codex run we ran the remaining step 5 ourselves:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/blender/build_checkpoint_post.py > tools/blender/build_checkpoint_post.log 2>&1
godot --headless --path godot --import
godot --headless --path godot --script res://tests/test_checkpoint_post.gd --fixed-fps 60
```
