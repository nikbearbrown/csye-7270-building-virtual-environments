# Example 03 — Blender to Godot: a scripted prop, measured in the game

## Executive summary

**What this is.** The record behind Chapter 3's worked example, run on 2026-09-27. A coding agent wrote a Blender Python script that builds a low-poly checkpoint post (0.6 x 0.6 m base, 1.8 m eight-sided pole, 0.4 x 0.25 m pennant, materials `PostMetal` and `FlagCloth`, a separate collision hull named with Godot's `-convcolonly` suffix), ran Blender headless to export `checkpoint_post.glb`, placed it in a scratch copy of `walker-3d-platformer`, and wrote a headless Godot test.

**Why it matters.** The first agent (Claude Code) pre-wrote the model's `.import` file from the demo's enemy import, which disables name suffixes, then spent its turns guessing at the missing collider and hit its turn limit. It resumed when a hung debug process was stopped, changed two things at once, lost track of the Godot binary after its context was compacted, and never ran its finished test. Claude Code then refused a revision run (account usage limit), so Codex did the revision, but Blender crashed inside Codex's sandbox and Codex tried to reach the Blender application through a Computer Use tool, which refused. We stopped it and ran Blender, the import and the test ourselves. The final test passes 17 of 17. An independent check still finds 55 of 1,066 pennant sample points inside the collision hull, which the agent's check (vertices only) could not see.

**What it does not show.** Anything visual: lighting, materials, whether the post reads as a checkpoint, whether its collider feels fair. No Blender or Godot window was opened. The MCP route was documented, not run.

---

## Results

| Step | Who | What our own commands showed |
|---|---|---|
| Baseline | — | `godot --headless --path godot --import` clean (`logs/baseline-import.log`) |
| Run 1 | Claude Code | Final test (run by us): 16/16 PASS (`logs/verify1-test_checkpoint_post.log`). Independent: floor at y = -4.0 under the post, gap 0.0 m; 572 of 1,066 pennant sample points inside the 0.6 x 1.8 x 0.6 m box collider (`logs/verify1-independent.log`) |
| Suffix probe | us | Fresh import of the same `.glb`: `use_node_type_suffixes=true` by default, `StaticBody3D [Collision]` + `ConvexPolygonShape3D`. With it `false`: the collider becomes a visible `MeshInstance3D [Collision-convcolonly]` (`logs/probe-suffix-setting.log`) |
| Run 2 | Codex (edits) + us (Blender, import, test) | 17/17 PASS (`logs/verify2-test_checkpoint_post.log`). Independent: floor gap 0.0 m; 55 of 1,066 pennant points inside the tapered hull, furthest at local x = 0.11 m (`logs/verify2-independent.log`) |
| Codex sandbox | Codex | Blender 5.1.2 exit 139 four times; crash in the Metal GPU backend check at start-up (`logs/blender-crash-in-codex-sandbox.txt`) |

Other probes behind the chapter's claims: axis and apply-scale mistakes end to end (`logs/probe-mutations-*.log`), stale `obj.dimensions` before a depsgraph update (`logs/probe-stale-dimensions.log`), Blender exiting 0 on a Python exception unless `--python-exit-code` is set (`logs/probe-blender-exit-code.log`), Blender 5.1.2 exporter and unit defaults (`logs/probe-blender-defaults.log`), imported material classes and culling (`logs/probe-materials.log`). Rebuilding with the final script produced a byte-identical `.glb` (Git showed no change).

## Files

| Path | What it is |
|---|---|
| `PROMPTS.md` | Prompts and command lines exactly as run, plus the commands we ran ourselves |
| `checkpoint_post.glb` | The final exported asset (6,288 bytes) |
| `changes.diff` | `git diff` baseline → final. The committed Blender log inside it had absolute paths replaced with `<scratch>`; everything else is verbatim |
| `diffs/` | The same split into run 1 and run 2, plus the scratch `git log` |
| `scripts/agent/` | Agent-written files, final versions, plus run-1 versions (`*.run1*`) and the debug script that hung (`debug_options.run1-hung.gd`) |
| `scripts/independent/` | Our checks and probes: `verify_post_independent.gd`, `print_import_tree.gd`, `print_materials.gd`, `measure_player_enemy.gd`, `make_mutations.py` + `measure_mutations.gd`, `stale_dimensions.py` |
| `walker-context/` | The three Walker Markdown files the prompt asks the agent to read |
| `logs/` | Every run's output, with local paths replaced and colour codes stripped; `run-times.txt` has start and stop times |
| `transcripts/` | Sanitized agent transcripts: `run1-claude.jsonl`, `run2-claude-refused.jsonl`, `run2-codex.jsonl` |

**Transcripts are trimmed, and say so.** Only these changes: absolute home and scratch paths replaced; session-start hook events dropped; Claude Code's `init` event reduced to cwd, model, tools, permission mode and version; Claude Code's duplicate `tool_use_result` fields dropped. Codex's own temporary paths (`/tmp/blender-*`) are left as they were, because they are part of what it did.

## Reproduce

Tools: Godot 4.7.2 (regular) as `godot`; Blender 5.1+ (5.1.2 used); Git; Claude Code or Codex. GNU `timeout` is recommended (macOS: Homebrew `coreutils`).

```bash
git clone https://github.com/godotengine/godot-demo-projects.git
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
mkdir walker-3d-platformer-asset && cp -R godot-demo-projects/3d/platformer walker-3d-platformer-asset/godot
cp walker-context/*.md walker-3d-platformer-asset/
cd walker-3d-platformer-asset && git init && git add -A && git commit -m "Baseline"
godot --headless --path godot --import
```

Then run `PROMPTS.md` run 1. To check the result, or to rebuild from our final files instead: copy `scripts/agent/build_checkpoint_post.py` to `tools/blender/`, `scripts/agent/test_checkpoint_post.gd` to `godot/tests/`, add the `CheckpointPost` node from `changes.diff` to `godot/game.tscn`, then:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_checkpoint_post.py
godot --headless --path godot --import
timeout 120 godot --headless --path godot --script res://tests/test_checkpoint_post.gd --fixed-fps 60
timeout 120 godot --headless --path godot --script "$PWD/verify_post_independent.gd" --fixed-fps 60
```

(`verify_post_independent.gd` must be copied to the folder you run from; Godot accepts its absolute path.) Do not copy `scripts/agent/checkpoint_post.glb.import.run1`: it is the file that disabled the suffix. Let Godot write a fresh `.import`.

## Human checks still open

- Does the post read as a checkpoint beside the robot, under the stage's lighting? Is the pennant visible from both sides?
- Is the invisible collision around the pole (up to 11 cm each side at mid-height) and along the pennant's lower edge (3 cm) acceptable to a player?
- Is 3.0 m from the spawn along +X in the robot's opening path?
