# ACTS.md — coverage map

Source read in full on 2026-10-06: `csye-7270-building-virtual-environments/chapters/03-blender-mcp-to-godot.md` (436 lines) and its evidence record
`examples/03-blender-mcp-to-godot/` (README, PROMPTS, logs, transcripts, scripts). One film, no length cap; the estimated runtime is logged in BUILD-LOG.md.
Every source section is in an act or under LEFT OUT with its reason.

## Opening pair (fixed)
- **BIDEA** (hesitant writer): "My model looks right in Blender, so it must be right in the game?" → corrected to "…but what did the game receive?". Greeting: **Bonjour**.
- **BDEFS** (Terms In This Lecture, 6): mesh · collider · bounding box · glTF · headless · MCP. ("coding agent" is defined in-line at B08, where it first matters.)

## Acts (source order)
| Act | Title | Beats | Source sections |
|---|---|---|---|
| I | One Column, Three Arrivals | B01–B07 | Executive summary (the question), "The question" (three-way probe table, the fourth failure) |
| II | Two Ways to Let an Agent Drive Blender | B08–B18 | Idea 1 (MCP route: community vs Blender Lab, no-auth warning, two rules; script route: `-b`, `--factory-startup`, `--python`, `--python-exit-code 1`; the MCP-vs-script table) |
| III | Metres, Axes and Applied Scale | B19–B32 | Idea 2 (units), Idea 3 (axes, +Y Up), Idea 4 (apply transforms; stale `obj.dimensions`), the Walker example's physics numbers (capsule 2.1 m, gravity 22, 120 ticks) |
| IV | What Godot Builds From a File | B33A–B44 | Idea 5 (glTF as interchange; materials crossing), Idea 6 (the `.import` file; the two suffix settings), Idea 7 (collision decided at import; the suffix table; empties; concave-only-in-static; the enemy's five shapes) |
| V | Building the Post, Then Checking the Builder | B45–B71B | Hands-on Predict + Build It (the task, the prompt), "What we actually ran" (Run 1 Claude Code; our checks; Run 2 Codex; the 17/17 and the sliver), Verify (what a pass proves and does not) |

## Closing three (fixed)
- **BVDT** (recap, six lines) → **BHTF** (Your Turn: paste-able prompt that makes the viewer use the idea; two checks) → **BOUT** (`ClaudeTitleOutro`, exact title, @NikBearBrown, no jingle, 1.0 s tail).

## LEFT OUT (with reasons)
- **Executive summary "What it proves and what it does not"** — folded into Act V's closing beats (B71A/B71B); not a separate beat.
- **"The Walker example" paragraphs** (the Walker framework, "Get the builds", the demo's own tests "Four normal-input assertions pass…"): Walker is Bear's framework and the demo's own checks touch no imported model; the viewer does not need it. The demo's physics numbers and the enemy's shapes are used (B21, B43) as facts about Godot's official demo.
- **MCP route, numbered install steps 1–5** (`uv`, `claude mcp add`, add-on install, `Start MCP Server`, telemetry/safe-mode switches): documented, NOT run in the source ("Treat each line as a claim to check"). The film teaches the route's architecture and its security rules (B09–B12) and says it was not run; it does not teach unrun steps as a procedure.
- **"Use It" (four human checks in the editor)** — their substance (looks, pennant visibility, felt collision, placement) is the "still needs your eyes" list in B71B.
- **"Ship It"** (commit the script, the `.glb` and its import; do not commit `.godot/`; a re-run is byte-identical) — repository workflow, not the lecture's subject; "the script is the source of truth" is made in B35.
- **"Check your understanding" (6 questions)** — course exercises; their substance feeds the Your Turn prompt (BHTF).
- **"Doing the same thing in Unity" and "…in Unreal Engine"** — documentation-only comparisons of other engines ("not run for this chapter"); the lecture teaches Godot. 
- **Sources list** — citations are carried in SOURCES.md and FACTCHECK.md.

## Swaps and splits
- No act swapped. Beats split for length (>15 s): B33→B33A/B33B, B47→B47A/B47B, B67→B67A/B67B, B71→B71A/B71B (IDs must be upper-case: build_safety rejects lower-case suffixes).

## Cast per act (recurring objects keep the same picture)
- **I** the column: isometric (B01), then the Godot side view (Y up, Z across) with the 0.2 × 1.8 rectangle, the 2 m outline cube, X/Y/Z cells and the real probe lines.
- **II** two routes: the live window with socket and server (the real Blender window screenshot) vs a script file that runs and exits (real terminal text).
- **III** the same column and cube as Act I; Blender's Z-up world and Godot's Y-up world as two sets of axes.
- **IV** one mesh and one `.import` file (the real enemy import) recurring; the post's collider render.
- **V** the checkpoint post (real Blender render), its collider (ghost overlay), Godot's floor line at y = -4.0, the pennant.
