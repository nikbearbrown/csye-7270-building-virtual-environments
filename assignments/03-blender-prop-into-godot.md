# Assignment 3 - Build a Prop in Blender and Make It Work in Godot

CSYE 7270 · Fall 2026 · **100 points**

Assignments follow a **10-day cadence**. Use this assignment's due date in Canvas. The syllabus's **10% daily late penalty** applies. Suggested Canvas due date: Day 30 after the first class day.

**Covers:** [Module 3 — Blender MCP to Godot](../modules/03-blender-mcp-to-godot/lesson.md) and [Module 4 — Scenes, collision and physics](../modules/04-scenes-collision-and-physics/lesson.md).

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

You build one 3D prop for your own game in Blender, from a Python script that Blender runs without a window, and export it as glTF. In Godot you give it a collider you shaped, a named physics layer, and one physics role (static blocker, rigid body, or area trigger), and make it do that job in a scene of your game. A headless test proves the numbers: size, axes, scale, origin, triangle count, materials, collider fit, layers and masks, and behaviour. You hand in the repository tagged `a3`, the brief you wrote first, a test report, an honest log, and one `godot-gamedev` film. Grading is 60 points for the work and its explanation, 10 for the log, 10 for matching versions, and 20 relative. None of this proves the prop looks right under your game's lighting, reads as what it is, or feels fair to run into. Those are your human checks, and the rubric counts them.

## Your task

Design a prop your game needs (cover, a landmark, an obstacle, a crate, a switch) and specify it in numbers. Build it in Blender from a committed script, import it into Godot, and make it block, settle, or detect, as your brief says. Prove each property with a check you run yourself, and play the result.

**The cumulative game.** From Assignment 2 on, you build one game: the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. Assignments 3–10 each add one layer to that same repository and are submitted as a git tag on it (`a3` here), so the final project is the sum of the semester rather than a restart. You may change games once, before Assignment 4, with a short written justification in `FRICTIONAL.md`; the tags then continue on the new repository, and your submission note says so. This is an individual assignment.

**If your game is 2D,** add a 3D scene to it: a 3D prop room, a 3D diorama, or a 2.5D stage. A project may mix 2D and 3D scenes. The 3D scene measures in metres, not pixels: Godot uses "1 unit being equal to 1 meter" in 3D ([Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)). It needs a floor with collision, a camera, and a light. Connect it to the game by a scene change (`change_scene_to_file()`, Module 4), or name the gap as a known limitation.

**Tools and cost.** Claude Code assistance is expected; use your Northeastern access. Blender is free and required from Week 3 ([Blender download](https://www.blender.org/download/)). The chapters ran Godot 4.7.2 and Blender 5.1.2; record your versions. Nothing paid is needed, and nothing paid earns credit.

**Rights and provenance.** Build the geometry in Blender; a downloaded or AI-generated mesh does not satisfy this assignment. Materials and textures may come from your Assignment 2 asset log or the script; record each source and its terms in `SOURCES.md`. Never commit credentials.

### What the prop must have

| Property | Minimum |
|---|---|
| Purpose | A design reason, tied to an Assignment 2 pillar or storyboard panel. |
| Build | A committed Blender Python script that rebuilds it headless. |
| Format | `.glb`, or `.gltf` with a stated reason. |
| Scale and axes | Stated dimensions in metres, within 1 cm in Godot; Blender's Z on Godot's Y; unit scale on every imported `MeshInstance3D`. |
| Origin | Where your brief puts it (for a floor prop, usually the centre of its underside), within 1 cm. |
| Triangle budget | A number you state and justify; the imported visual meshes stay within it. |
| Materials | Named in Blender; exactly those names arrive in Godot. |
| Collider | A separate, simple shape you shaped. It covers what should block or detect, and nothing else. |
| Physics role | One: static blocker, rigid body, or area trigger. |
| Layers and masks | The prop on a named 3D physics layer; masks changed only where detection needs it. |
| Behaviour | The prop does its job in a scene of your game, exercised by the player or a labelled stand-in body. |

## 1. Predict

Commit `CHANGE-BRIEF.md` before the first Blender run. Retain the original; add dated revisions below it rather than rewriting it.

- **The specification:** every row of the table above, in numbers. The chapter gives no triangle budget, so justify yours from something you can measure: copies on screen, what your other models cost (counted the same way), the hardware you target.
- **The collider:** shape type, what it must cover and leave out, and how much invisible collision beside the visible surface you will accept.
- **The behaviour:** what should happen, and within how many frames at `--fixed-fps 60`.
- **The layer plan:** a table (Object | Layer number and bit value | Mask | What it should detect). Layer *n* is the bit value 2^(n−1).
- **Ownership and invariants:** who instances and frees the prop; what must not change (player tuning, other layers and masks, existing tests).
- **Answers, before you delegate:** which Godot axis carries the height; what Godot reports for a `MeshInstance3D` with unapplied scale; what a copied `.import` does to a `-convcolonly` collider; which object's mask must change for your detection; whether `body_entered` fires again for an overlap that began earlier.
- **At least three predicted failures** and how you will check each.

## 2. Build It

### Read first

The [Module 3 lesson](../modules/03-blender-mcp-to-godot/lesson.md) and [Chapter 3](../chapters/03-blender-mcp-to-godot.md), which built and measured a checkpoint post in [walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer) ([record](../examples/03-blender-mcp-to-godot/)). The [Module 4 lesson](../modules/04-scenes-collision-and-physics/lesson.md) and [Chapter 4](../chapters/04-scenes-collision-and-physics.md), whose shield pickup in [walker-2d-dodge-the-creeps](https://github.com/nikbearbrown/walker-2d-dodge-the-creeps) shows layers, masks and mutation testing ([record](../examples/04-scenes-collision-and-physics/)). Both Walker projects keep the upstream MIT license.

### Choose the route

**Script route (required record).** The agent writes `tools/blender/build_<prop>.py` with Blender's `bpy` API, and Blender runs it with no window. The path is the chapter's macOS one; use your own Blender executable elsewhere:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_<prop>.py
```

Keep `--python-exit-code 1`. Without it, Blender exits 0 when the script raises an exception.

**MCP route (optional, for exploring).** Chapter 3 documents the community MCP for Blender setup but did not run it; treat each step as a claim to check, and log what happened in `FRICTIONAL.md`. Keep its port on `localhost` and its generation and download services off. Copy every `execute_blender_code` body into the script and rebuild the submitted `.glb` from it, because Git records nothing about an MCP session.

### Choose the collider route

| Role | Godot body | Collider route | What your test should show |
|---|---|---|---|
| Static blocker | `StaticBody3D` | A separate mesh with the `-convcolonly` suffix, which the importer turns into a `StaticBody3D` with a `ConvexPolygonShape3D` ([node type customization](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/node_type_customization.html)), or a wrapper scene | A body driven into it stops at the collider. |
| Rigid body | `RigidBody3D` | A wrapper scene: `RigidBody3D` root, the imported model, and a `CollisionShape3D` you author | It falls, rests on the floor within your frame budget, and responds to a push. |
| Area trigger | `Area3D` | A wrapper scene: `Area3D` root, the model, and a `CollisionShape3D` | `body_entered` fires once per entry, only for bodies on layers in its mask, and the effect happens. |

For a wrapper, leave no `-convcolonly` mesh in the model, or the importer still builds a static body inside it. Concave shapes work only "within StaticBodies"; avoid scaling collision shapes ([Collision shapes (3D)](https://docs.godotengine.org/en/stable/tutorials/physics/collision_shapes_3d.html)). A `RigidBody3D` "cannot be controlled directly"; you apply forces ([RigidBody3D](https://docs.godotengine.org/en/stable/classes/class_rigidbody3d.html)). An area detects a body only when that body's layer is in the area's mask ([Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)). Name your layer under `[layer_names]` in `project.godot` (a `3d_physics/layer_N` key); in code, `set_collision_layer_value()` and `set_collision_mask_value()` take layer numbers, not bit values ([CollisionObject3D](https://docs.godotengine.org/en/stable/classes/class_collisionobject3d.html)). Test the layer on the running node.

### Work in inspectable increments

One step at a time, each committed separately:

1. **Blender script and log.** Done when Blender exits 0 with `--python-exit-code 1` and the log's names, dimensions, scales, materials and triangle counts match your brief. In Blender 5.1.2, `obj.dimensions` showed the old size until `bpy.context.view_layer.update()` ran, so make sure the log is current.
2. **Import.** Done when a fresh `--import` prints no `ERROR` lines and the scene tree holds the body type you expect. Let Godot write the `.import` file; for the suffix route, `nodes/use_node_type_suffixes` must be `true`.
3. **Role, layers and masks**, then **placement** on the floor of a scene in your game.
4. **Test.** One headless `SceneTree` test that prints a `PASS` or `FAIL` line per check and exits non-zero on any failure.

Put the exact Blender, import and test commands in a `## Checks` paragraph of your `AGENTS.md` (or `CLAUDE.md`). In Chapter 0, that one paragraph fixed an agent running checks the wrong way.

Ask Claude to propose a plan before editing:

```text
Read my CHANGE-BRIEF.md, README.md, AGENTS.md and the scene the prop will
go into. This is my Godot 4.7.2 GDScript game. Use Walker's brief → build →
playtest → inspect → revise workflow.

Task: build the prop in my brief in Blender from a Python script, export it
as binary glTF, import it, give it the collider, physics role and collision
layer my brief specifies, place it, and prove its size, axes, origin,
triangle count, materials, collider fit, layers and masks, and behaviour
with a headless test. Do not edit yet. First list the files you would
create or change and the order of the steps.

Rules for every step after I approve the plan:
- Run Blender only as <my Blender path> -b --factory-startup
  --python-exit-code 1 --python tools/blender/<script>.py. Never open its
  window or any other application.
- Never write or copy a .import file. Let Godot write it, then tell me
  which of its settings decide how my collider is imported.
- Never invent uid:// values or unique_id numbers in a .tscn file.
- Read expected values from my brief or from the scenes, not from
  constants you choose. A floor ray must exclude the prop's own collider.
- Run tests as timeout 120 godot --headless --path godot --script
  res://tests/<test>.gd --fixed-fps 60 and report the real output.
- Implement one step, show the diff, run its check, and stop. Tell me what
  still needs a person to look at in the running game.
- Do not change existing scripts, player tuning, other objects' layers or
  masks, or my existing tests. If a check fails, do not weaken it.
```

This is a prompt to Claude Code, not an installed shell command. You decide whether to accept the plan.

### What the agent is likely to get wrong

Each of these happened in the chapters' recorded runs.

- **It writes the `.import` file itself.** Claude Code copied the demo enemy's, which sets `use_node_type_suffixes=false`. The collider arrived as a visible box with no collision.
- **It guesses, then changes two things at once**, so nobody can tell which change fixed the collider.
- **Its floor check finds the prop.** A downward ray stopped on the post's own collider: proof the post was solid, not that it stood on anything.
- **It weakens a failing check**, here by skipping unnamed materials.
- **It measures vertices, not surfaces.** Codex's check passed "no pennant length lies inside collider" while 55 of 1,066 sampled pennant points were inside.
- **It invents engine identifiers** (`unique_id=987654321`), and writes tests that cannot fail: in Chapter 4, a shield cut from 3.0 s to 0.5 s still passed Claude Code's test 7 of 7.
- **It looks for another way.** When Blender crashed in Codex's sandbox, Codex reached for a tool to operate the Blender application. Repeat "never open its window", and run Blender yourself outside a sandbox.

## 3. Use It

Run every check yourself; the agent's pasted output is a claim. Record actual results in `TEST-REPORT.md` with the source revision, versions, and operating system.

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_<prop>.gd --fixed-fps 60
```

`timeout` (GNU coreutils; Homebrew's `coreutils` on macOS) stops a test that errors before `quit()`; one in Chapter 3 ran for eight minutes. At 120 physics ticks per second, `--fixed-fps 60` gives two ticks per frame; state yours.

| Check | Evidence to collect |
|---|---|
| Rebuild | The script reruns with exit 0, log values match the brief, and the `.glb` is unchanged (the chapter's rebuild was byte-identical in Git); otherwise say what differs and why. |
| Import | The `.import` settings that decide your collider; an import log with no `ERROR` lines. Exit code 0 is not "no errors". |
| Size, axes, scale | Merged visual AABB within 1 cm of the brief, height on Y, unit scale on every `MeshInstance3D`. |
| Origin | The geometry's position relative to the prop's origin, within 1 cm of the brief. |
| Triangle budget | Imported visual triangle count against your budget; in `Mesh.get_faces()`, "each three vertices represent one triangle" ([Mesh](https://docs.godotengine.org/en/stable/classes/class_mesh.html)). |
| Materials | Exactly the named materials, none skipped. |
| Collider fit | Sample what must not collide, and what must, on a grid fine enough to catch the gap you care about (the chapter used 1 cm), and ask the physics server which points are inside, as the chapter's [independent check](../examples/03-blender-mcp-to-godot/scripts/independent/verify_post_independent.gd) does. Report counts. |
| Layers and masks | Values read from the running nodes and compared with your table, as Chapter 4's [reviewer check](../examples/04-scenes-collision-and-physics/reviewer/verify_shield_timing.gd) does. |
| Behaviour | The role's assertion in frames under `--fixed-fps 60`, reached by ordinary input or by a fixture labelled as one. |
| Placement | A floor ray excluding the prop's collider finds the floor within 2 cm of the base. |
| Mutations | Two deliberate breaks, each caught and then restored: one in the asset pipeline (no +Y Up, unapplied scale, suffix setting off) and one in collision (a wrong mask bit, an oversized collider). |
| Regression | Every earlier test in your repository still passes. |

Do not delete a failing assertion or weaken an expected result merely to obtain a green report. A check that passes when the mechanism is broken is not measuring what its label claims.

**HUMAN CHECKs.** Play the scene with normal controls and record what you saw.

- Under your game's lighting, does the prop read as what it is? Do the materials read as intended? Is any single-faced part (a flag, a sign) visible from both sides?
- With **Debug > Visible Collision Shapes** on, walk or push into the prop, then beside it. Is the invisible margin your sampling measured fair to the player?
- Is the prop where the level needs it, and out of the way of anything it should not block?

Include at least one documented inspect-and-revise cycle driven by an observation, such as a reshaped collider or a moved origin. If another person plays, record their actual feedback; do not invent a playtester. Your own playtest is required; a headless test does not replace it.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier ([Required Brutalist Godot explainers](../prerequisites/brutalist-godot-explainers.md)). Ask Claude Code to read the installed skill instructions and follow them; the skill name is not a standalone executable. If your checkout lacks the skill, request the course-provided version before proceeding.

Make **one** landscape film that:

1. Identifies your game, the prop's purpose, and what this assignment added.
2. Traces the prop from source to scene, pairing each code excerpt with its result: the script's export call, the `.import` line that decides the collider, the imported scene tree, the prop in the running game.
3. Shows the physics role in real play, with at least one labelled segment with Visible Collision Shapes on.
4. Shows the headless test output, labelled as headless, and a mutation it caught.
5. States what you tested, what your human checks found under the game's lighting, what remains uncertain, one next step, the human and AI contributions, and the source revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Label reconstructed editor views, scripted-input captures, and held frames accurately. A Blender render or a fixture is not gameplay.

Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. Duration follows the explanation. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with the prop, its `.glb` and `.import`, any wrapper scene, and the tests; `tools/blender/build_<prop>.py` and its log. Exclude `.godot/`, caches and credentials.
- `README.md`: project name, starting point, Godot and Blender versions, how to rebuild the prop and run the game and checks, controls, what this assignment added, known limitations, and the final-film link.
- `CHANGE-BRIEF.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md`.
- The film's beat sheet, script/prompts, and relevant evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Use commit messages that describe a meaningful change and its purpose or check, for example `Reshape prop collider to clear the sign; rerun sampling check`. Tag the submitted commit `a3` and push the tag.

## 5. Verify and submit to Canvas

Clone the tagged revision into an empty folder and run it there. A working local folder is not proof that everything was posted.

```bash
git clone <your-repository> ../a3-check
```

```bash
git -C ../a3-check checkout a3
```

In the clone, rebuild the prop, import once, run every check, and play the scene briefly. Confirm that the film depicts that source.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 3 - Build a Prop in Blender and Make It Work in Godot
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Game-source revision shown in the film:
Godot version, Blender version, and operating system:
Prop, physics role, and collision layer:
Blender route (script only, or MCP then script):
Checks run (command and result):
Final film URL and filename:
Final film SHA-256:
Summary of my changes:
Known limitations:
Changed games since Assignment 2 (yes/no; if yes, FRICTIONAL.md entry):
```

It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit.

Canvas, GitHub, and the film must refer to the same submitted work. Do not move the `a3` tag after you submit; identify later changes as a new revision rather than silently replacing the submitted evidence.

## Rubric — 100 points

| Component | Points |
|---|---:|
| Implementation and explanation | 60 |
| Frictional — honest log | 10 |
| GitHub version posting matching Canvas | 10 |
| Relative Quartile | 20 |
| **Total** | **100** |

### Implementation and explanation — 60 points

| Criterion | Points |
|---|---:|
| Specification and Blender build: a brief with dimensions, origin, materials, a justified triangle budget, collider and layer plans, committed first (4); a committed script that rebuilds the prop headless, with its log (5); rebuild result and provenance recorded (3). | 12 |
| Import and measurement: import settings correct for your collider route (4); headless checks of size, axes, unit scale, origin, triangle count and materials against the brief (8). | 12 |
| Collision and physics role: collider fit measured by sampling, invisible margin stated (6); named layer and masks asserted on running nodes (4); the role working in a scene of your game under the pinned clock (6). | 16 |
| Verification: two mutations your tests catch (3); human playtest with Visible Collision Shapes and HUMAN CHECKs recorded (4); an evidence-based revision and an honest limitation (3). | 10 |
| Brutalist explainer: accurate explanation from script to running scene (4); actual mechanism and gameplay shown (3); traceable evidence and stated limits (2); readable, audible final film using the required workflow (1). | 10 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing headless test establishes the prop's measured size, collider, layers and behaviour in a pinned simulation; it does not establish that the prop looks right under your game's lighting, reads as what it is, or feels fair to collide with.

### Frictional — honest log — 10 points

In `FRICTIONAL.md`, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.

- **3 points:** Specific, honest accounts of what you tried and what happened.
- **3 points:** What you checked, changed, or learned in response, including unresolved questions.
- **2 points:** Explicit human/AI contributions, including what you accepted, modified, or rejected.
- **2 points:** Traceability to relevant commits, prompts, tests, or observations.

An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.

### GitHub version posting matching Canvas — 10 points

- **4 points:** Required, accessible game source and documentation are actually posted.
- **3 points:** Canvas identifies the `a3` tag and the exact submitted commit, and supplies the matching source files and clear run instructions.
- **3 points:** Accessible film link, identified media version, and film source/evidence correspond to the submitted game.

### Relative Quartile — 20 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.

Meeting the stated criteria can earn the other **80 points**; it does not guarantee these **20 points**. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.

## You must be able to explain it

Use `SOURCES.md` to credit your starting point, Blender and its version, any MCP server, texture or material sources, collaborators, and tools. Describe what AI contributed to the Blender script, the Godot scenes and code, the tests, and the film's script, beat sheet, visuals, and narration, and what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to rebuild the prop from your script, explain a layer or mask value, or show where the collider is wider than the art and why that is fair. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.
