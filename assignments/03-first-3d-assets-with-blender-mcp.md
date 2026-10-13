# Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender

CSYE 7270 · Fall 2026 · **100 points**

**Due: Thursday, October 15, 2026, at 11:59 pm America/New_York.** Confirmed in Canvas. The **10% daily late penalty** applies.

**Covers:** [Module 3 — Blender MCP to Godot](../modules/03-blender-mcp-to-godot/lesson.md). Module 4 runs alongside it, and you do not need it here.

**Required viewing:** [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz).

## Executive summary

This is a gentle first assignment in 3D. You make **three simple 3D assets for your own game** by directing Claude through the Blender MCP in a running copy of Blender, do at least one edit yourself with the mouse, export each asset as a `.glb` file, and show all three together in a Godot 3D scene. The point is familiarity: what Blender's window shows, what Claude can and cannot do through the MCP, and what a game asset needs before an engine can use it (the right size, the right way up, a sensible origin, transforms applied). The assets are meant to be simple, built from basic shapes, so that the learning is in the workflow and not in the modelling. Grading is the usual 60 points for the work and its explanation, 10 for your Frictional log, 10 for matching versions on GitHub and Canvas, and 20 relative. One thing to know before you start: the course has **not** run the MCP route itself, so part of your job is to record honestly what happens on your machine. A passing check shows your assets arrived at the size you intended; it does not show they look right in your game, and that judgment is yours.

## Your task

Choose **three simple assets** that your game could use: for example a prop (a crate, a lantern), a piece of the environment (a platform, a tree, a rock), or something the player collects (a coin, a gem). Prefer things you actually want in your game. Build each in Blender with Claude, export it, and show the three together in Godot.

**What "simple" means here.** Each asset is built mainly from Blender's basic shapes (cube, cylinder, cone, sphere, plane), moved, scaled and combined, with a flat-colour material. No sculpting, no painted textures, no rigging, no animation. Keep each asset low-poly, with **no more than six basic shapes and no more than 500 triangles**. A Blender sphere or cylinder at its default settings can use a large share of that budget, so ask Claude to lower the segment counts. State your own triangle number in your brief, at or under 500. These are course limits for this assignment, so that everyone's work can be compared fairly; they are not engine limits.

**The cumulative game.** From Assignment 2 on, you build one game: the one you chose in Assignment 2, in a repository whose name begins **`walker-`**. Assignments 3–10 each add one layer to that same repository and are submitted as a git tag on it (`a3` here), so the final project is the sum of the semester rather than a restart. You may change games once, before Assignment 4, with a short written justification in `FRICTIONAL.md`; the tags then continue on the new repository, and your submission note says so. This is an individual assignment.

**Your game does not have to be 3D.** If it is 2D, you still make three assets that suit it (a 3D prop room, a diorama or a 2.5D stage would give them a place), and you show them in a small Godot 3D scene that you add to your repository: a floor, one light, a camera, and your three assets side by side at game scale. Assignments 4 and 5 reuse that scene. You do not need to connect it to your 2D game yet.

**Tools and cost.** Claude Code assistance is expected; use your Northeastern access. Blender is free and required from Week 3 ([Blender download](https://www.blender.org/download/)). The chapter ran Godot 4.7.2 and Blender 5.1.2; record your versions. The Blender MCP used here is the community project the syllabus names, [MCP for Blender](https://github.com/ahujasid/mcp-for-blender). Nothing paid is needed, and nothing paid earns credit.

**Rights and provenance.** You build the geometry yourself, with Claude, in Blender. A downloaded model or an AI-generated mesh does not count. The community add-on can also fetch models (Poly Haven, Sketchfab, Poly Pizza) and call generation services (Hyper3D Rodin, Hunyuan3D, Tripo): **leave all of those switched off.** They call remote services and may cost money. Record every tool and its version in `SOURCES.md`. Never commit credentials.

**A safety note.** By default the MCP runs Python that Claude writes *inside* your Blender, without a guard. The project's own README says its socket has no authentication or encryption, so anyone who can reach that port can run Python inside Blender. The add-on opens that socket whenever Blender starts while the add-on is enabled, not only while you work on this assignment, so turn the add-on off in Preferences when you are not using it. Keep the port on `localhost`, save your work before you start, and do not open `.blend` files from people you do not trust while the server is running.

## 1. Predict

First do the short "Learn the window" session in Build It below, so your sizes and budget are informed guesses and not blind ones. Then, before you ask Claude to build anything, commit `CHANGE-BRIEF.md`. Retain the original; add later revisions rather than rewriting it to make every prediction look right.

- **The three assets.** For each: its name, what it is in your game, and where it appears.
- **Size, in metres.** Width, depth and height, justified against something in your game (the player's height, a tile, a door). In Blender 1 unit is 1 metre, and Godot's 3D units are metres too, so nothing converts if you keep it that way.
- **Origin.** Where its origin point sits (for a prop that stands on the floor, the centre of the underside is usual), and why. Build each asset around Blender's world origin, the point where the three axes meet, with its base on the floor there, and keep each asset in its own file: that point is where Godot will place it.
- **Look.** What shape makes it recognisable, and its material colours.
- **Budget.** Your triangle budget, and why that number.
- **At least three predicted failure cases and how you will check each.** For example: an asset arrives lying on its side; it is the wrong size by a factor of ten; its origin is in the middle so it floats; Claude builds something far more detailed than you asked; the MCP server will not connect; a colour does not survive the export.

## 2. Build It

### Read first

Read the [Module 3 lesson](../modules/03-blender-mcp-to-godot/lesson.md), especially "Two ways for an agent to drive Blender", "Units and axes" and "Apply transforms". For the long reading, see [Chapter 3](../chapters/03-blender-mcp-to-godot.md).

### Learn the window

Open Blender and spend a short session just looking, before any prompting. Orbit, pan and zoom the 3D viewport. In `BLENDER-NOTES.md`, in your own words, name and describe six parts of the interface: the **3D viewport**, the **toolbar**, the **Outliner**, the **Properties editor**, the **sidebar** (press **N**; it shows the active object's location, rotation, scale and dimensions), and the **mode selector** in the viewport's header, which switches between Object Mode and Edit Mode. Add one screenshot of your own Blender session with an object selected. The Blender manual's [interface chapter](https://docs.blender.org/manual/en/5.1/interface/index.html) and [3D Viewport pages](https://docs.blender.org/manual/en/5.1/editors/3dview/index.html) are the reference.

### Connect Claude to Blender

The course ran the script route in Module 3 and has **not run the MCP route**. The steps below are the manual setup the chapter recorded from the project's README on 27 September 2026 (version 2.1.1). The project changes quickly: by 6 October 2026 (version 2.1.9) the README led with a one-line installer (`curl … | sh`) and `uvx mcp-for-blender setup`, which find the MCP clients on your machine and let you pick which to set up, and kept these manual steps as the fallback. The course has run neither. **Use the manual steps below**, because the one-line installer reaches every MCP client it finds on your machine, not only Claude Code. Treat each line as a claim to check, and write down what differs on your machine. On macOS the README installs `uv` with Homebrew (it gives other installers for Windows and Linux), and warns against `pip install uv`:

```bash
brew install uv
```

Register the server with Claude Code. The README's own line is `claude mcp add blender uvx mcp-for-blender`; the chapter's version below adds the README's `DISABLE_TELEMETRY=true` setting through Claude Code's `-e` option, which turns off the server's anonymous usage record. That combination is the chapter's adaptation, not a README line:

```bash
claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender
```

Put the server's name first. `-e` takes one or more values, so `claude mcp add -e DISABLE_TELEMETRY=true blender -- ...` reads `blender` as another variable and fails with `Invalid environment variable format: blender` (found in a real run on 2026-10-06; the same command with `--scope project` added in a scratch folder printed exactly that error).

Install the add-on:

```bash
uvx mcp-for-blender install-addon
```

In Blender, open **Edit > Preferences > Add-ons** and enable **Interface: MCP for Blender**. The add-on starts its server when Blender opens. To check, press **N** in the 3D viewport and open the **MCP for Blender** tab; if the server is not running, start it there. The README calls that button **Start MCP Server** in one place and **Connect to Claude** in another; the add-on's own code labels it **Connect to MCP server**. Leave every service and download checkbox off (they start off). Then start a new Claude Code session so it sees the server.

If it does not work, that is data. Try honestly, for about two hours (a course rule for this assignment), and record each step you tried and its exact error in `FRICTIONAL.md`. If the MCP has not connected by then, you may build the assets with the **script route** from Module 3 instead (Claude writes a Blender Python script, and you run Blender with no window). State that clearly in your submission. An honest, specific account of a failed attempt, with a working script-route fallback, earns up to 6 of the 8 MCP points in the rubric, not all 8.

### Build the assets, one at a time

Ask Claude for a plan first, then build one asset per request. Adapt this prompt for each asset; it is an adaptation, not a prompt the course has run, so read what Claude does before approving it:

```text
We are using Walker's Game brief → Build → Playtest → Inspect → Revise → Export
workflow. Use the Blender MCP tools in my open Blender session. Read
CHANGE-BRIEF.md first.

Task: build only this asset: <asset name>, exactly as the brief specifies (size
in metres, origin, materials, triangle budget). Start from an empty scene with
metric units; Blender is Z-up.

First call get_scene_info and tell me what is in the scene, then propose the
steps. Do not build yet.

After I approve: one execute_blender_code call per object. After each, call
get_scene_info with the location, size, rotation and scale fields and report
them. Apply rotation and scale before you finish. Then show me the result
with the look tool.

Do not use Poly Haven, Sketchfab, Poly Pizza, Hyper3D, Hunyuan3D or Tripo,
and do not call generate_3d, search_assets or import_asset. Do not export
yet. Say what you could not verify.
```

The chapter listed tools from version 2.1.1 (27 September 2026), among them `get_object_info`, `get_viewport_screenshot` and `export_scene`. Version 2.1.9 (6 October 2026) removed those three; its README lists nine tools: `execute_blender_code`, `look`, `get_scene_info`, `generate_3d`, `search_assets`, `import_asset`, `get_addon_status`, `disable_telemetry` and `record_trajectory_feedback`. The prompt above uses the 2.1.9 names. If your install names them differently, use what it has.

- **Look at it yourself** in Blender's viewport after each step. Claude cannot tell you whether it looks right.
- **Make at least one change by hand** in Blender's window: move a part, scale it, or change a colour. Note what you changed and what the experience taught you about the interface.
- **Save the code Claude ran.** Copy every `execute_blender_code` body into `tools/blender/build_<asset>.py`, or Git will not show how the asset was built.
- **Save your `.blend` source** for each asset. Blender keeps older saved versions next to your file, named `.blend1` and so on ([Save Versions](https://docs.blender.org/manual/en/5.1/editors/preferences/save_load.html)); do not commit those.

If you use the script route for an asset, run it with no window, and add `--python-exit-code 1`: without it Blender exits 0 when your script raises an exception. Replace the path with your Blender's:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1 --python tools/blender/build_<asset>.py
```

### Export and place them in Godot

Export each asset as binary glTF (`.glb`), with the exporter's **+Y Up** option on, which is its default in Blender 5.1.2 ([glTF 2.0 add-on](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_gltf2.html)). Version 2.1.9 has no export tool (2.1.1's `export_scene` took an absolute path and `glb` or `fbx`), so use Blender's own **File > Export > glTF 2.0**, or have Claude run Blender's glTF exporter through `execute_blender_code` and save that code with the rest. Put the three files inside your Godot project folder, then import:

```bash
godot --headless --path godot --import
```

Open the project, build the small 3D scene (floor, one light, a camera), and place the three assets side by side. Ask Claude Code to write one short headless script that loads each asset and prints its bounding-box size, its node scale and the axis it stands along, so you can compare the numbers with your brief. Run it as in Module 3:

```bash
timeout 120 godot --headless --path godot --script res://tests/<your_check>.gd --fixed-fps 60
```

These commands are written for macOS; on another system, use your equivalents and say so. On macOS `timeout` comes from Homebrew's `coreutils`, and it stops a script that errors before it quits. The check is Claude's, so read it: a check can prove less than it claims. In Module 3, an agent's floor check stopped on the object's own collider and proved nothing about the floor.

## 3. Use It

Record the actual result of each check in `TEST-REPORT.md`, with your Blender and Godot versions:

| Check | Evidence to collect |
|---|---|
| Interface notes | The six parts named in your own words, and one screenshot of your own session. |
| Size | For each asset, the dimensions Blender shows (in the sidebar) beside your brief, and the Godot bounding-box numbers beside both. |
| Upright and scale | Each asset stands the right way up in Godot, and its node scale is 1, 1, 1 after export. |
| Origin | Each origin is where the brief says: place each asset on the floor in Godot and see whether it sits on it or floats. |
| Triangle count | Within your budget. Blender shows scene statistics (right-click the status bar and enable **Scene Statistics**). |
| Imports and appears | All three import without errors and appear in your 3D scene. |
| HUMAN CHECK: look | Walk the camera around each asset, including from behind and below. Do the shapes read as what they are at game size, beside your character if it is 3D? Any missing faces, wrong colours? |
| What Claude got wrong | At least one thing, or an honest "nothing, and here is how I checked". |

Include at least one documented inspect-and-revise cycle based on an observation: a size you corrected, an origin you moved, a part you rebuilt. If you can have another person look at your scene, record what they actually say; do not invent a viewer. Do not delete a failing assertion to turn a report green.

## 4. Ship It — source and explainer

### Make one required Brutalist Godot explainer

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) **`godot-gamedev`** workflow with the **`walker`** modifier ([Required Brutalist Godot explainers](../prerequisites/brutalist-godot-explainers.md)). Ask Claude Code to read the installed skill instructions and follow them; the skill name is not a standalone executable. If your checkout lacks the skill, request the course-provided version before proceeding.

Make **one** landscape film. A short, plain film is fine. It:

1. Identifies your game, your three assets and why your game needs each.
2. Shows your real Blender session. Use screen recordings or screenshots you made yourself, labelled as such; a reconstruction must be labelled a reconstruction. Show at least one prompt to Claude and what it built, and show your own hand edit. If the skill has no way to take your footage, say so and use your own screenshots as stills, or ask the instructor before inventing a workaround.
3. Shows the three assets in the running Godot scene, and the headless numbers beside your brief, labelled as headless.
4. States what you checked, what remains uncertain, what Claude got wrong, one next step, the human and AI contributions, and the source revision shown.

Use the Walker opening/summary and Verdict → Your Turn → regular outro. AI narration, including Liam, is allowed. Follow the skill's native **4K landscape** rendering and quality checks, then watch the final export. Duration follows the explanation, with no minimum. A second film, a vertical Short, paid media generation, and public YouTube publication are **not required**.

### Post the version on GitHub

Your submitted source includes:

- The Godot project with the 3D scene, the three `.glb` files and their `.import` files, and your check script; for each asset, the `.blend` source and `tools/blender/build_<asset>.py`. Exclude `.godot/`, `.blend1` backups, caches and credentials.
- `README.md`: project name, Godot, Blender and MCP versions, how to run the check and open the scene, what this assignment added, known limitations, and the final-film link.
- `CHANGE-BRIEF.md`, `BLENDER-NOTES.md`, `TEST-REPORT.md`, `FRICTIONAL.md`, and `SOURCES.md`.
- The film's beat sheet, script/prompts, and relevant evidence/coverage records.

Keep MP3, MP4, and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify the exact film by filename and SHA-256 checksum. Test reviewer access to the source and media.

Use commit messages that describe a meaningful change and its purpose or check, for example `Fix lantern height to 0.9 m; origin to base`. Tag the submitted commit `a3` and push the tag.

## 5. Verify and submit to Canvas

Clone the tagged revision into an empty folder and run it there. A working local folder is not proof that everything was posted.

```bash
git clone <your-repository> ../a3-check
```

```bash
git -C ../a3-check checkout a3
```

In the clone, import once, run your check, and open the scene. Confirm that the film depicts that source.

Submit a source ZIP of that same GitHub revision, excluding caches, credentials, and large media, together with `SUBMISSION.md`:

```text
Assignment: Assignment 3 - Your First 3D Game Assets with Claude, the Blender MCP, and Blender
Student:
Project name:
GitHub repository URL:
Git tag and submitted commit SHA:
Game-source revision shown in the film:
Godot version, Blender version, and operating system:
The three assets and what each is for:
MCP project and version, or "script route" (and which assets used which):
My hand edit in Blender:
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
| Brief and predictions, committed before building: three assets chosen for your game and specified in numbers (6); at least three predicted failure cases, each with its check (4). | 10 |
| Process with Claude, the MCP and Blender: the MCP route working for at least two assets, with the code Claude ran kept in `tools/blender/` (8), or, if it would not connect within the time box, an honest, specific account of the attempt plus a working script-route fallback (up to 6); interface notes in your own words with your own screenshot (3); at least one hand edit in Blender and what it taught you (3). | 14 |
| The three assets, 6 points each: recognisably what the brief says (2); correct size, upright, origin sensible, transforms applied (3); a clean material (1). | 18 |
| Godot import and checks: all three import and appear in your 3D scene at game scale (4); your numbers match the brief and you can say what the check does and does not show (3); an evidence-based revision and an honest limitation (3). | 10 |
| Brutalist explainer: accurate explanation of your workflow and assets (3); your real Blender session and the Godot scene shown (3); traceable evidence and stated limits (1); readable, audible final film using the required workflow (1). | 8 |
| **Subtotal** | **60** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A passing check shows your assets arrived at the size, orientation and scale you measured; it does not show they look right under your game's lighting, read as what they are, or suit your game's style. Those are your human checks, and the rubric counts them.

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

Use `SOURCES.md` to credit your starting point, Blender and its version, the MCP project and its version, any colour or material sources, collaborators, and tools. Describe what AI contributed to the Blender code, the Godot scene and check, and the film's script, beat sheet, visuals, and narration, and what you personally decided, checked, changed, or rejected.

The instructor or a TA may ask you to open one of your assets in Blender and show where its size, origin and applied transforms are, to explain why a scale that is not applied causes trouble in Godot, or to show which part you edited by hand. Inability to explain reduces points under the relevant criteria. Misrepresenting authorship or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz) and the course/university policies.
