# Chapter specification — CSYE 7270 companion book (Godot edition)

## Executive summary

**What this is.** The writing contract for every chapter of the CSYE 7270 companion book after the course moved from Unity/Unreal to Godot and Walker. Each writer (human or agent) reads it before drafting a chapter.

**Why it exists.** On 2026-09-27 Professor Bear asked for the course to be adapted for Godot: hands-on, with a chapter and a worked example for doing the work through a coding CLI (Claude Code or Codex), the Walker framework, and Godot; built from what the old Canvas export (`.imscc`) taught; using the existing `walker-*` Godot builds or adaptations of them; and ending every chapter with the similarities and differences of doing the same thing in **Unity** and in **Unreal Engine**.

**What it decides.** Chapter list and order (the revised Fall 2026 syllabus's 15 modules, plus a Chapter 0 for the CLI toolchain), the section skeleton, the evidence standard for the hands-on example, the voice, and the hard limits. It does not sign any AI+1 book gate.

---

## 1. Chapter list (one chapter per syllabus module)

The revised Word syllabus (`CSYE_7270_Virtual_Environments_and_Real-Time_3D.docx`) says each module maps one-to-one to a chapter. The sequence below follows it. Chapter 0 is the Week 1 toolchain setup the syllabus mentions ("setup and access checks are covered in Week 1").

| Ch | File | Syllabus week / focus | Old `.imscc` material it replaces | Primary Walker example(s) |
|---|---|---|---|---|
| 0 | `chapters/00-the-toolchain.md` | Week 1 setup — Claude Code, Codex, Walker, Godot at the command line | "Learning Unity" / "Unreal Engine" onboarding; `claude-code-guide` handout | `walker-pong` (public), `walker-jumpman` |
| 1 | `chapters/01-walker-and-godot.md` | Wk 1 Walker + Godot starter | How to Learn Unity 3D; Unreal Engine; Course Materials; Assignment 2 – Learning Unity | `walker-jumpman`, `walker-jumpman-clawd` |
| 2 | `chapters/02-prompting-game-art.md` | Wk 2 Prompting game art (+ sound and music, per Assignment 2) | Mini-Assignment 1 (GenAI art), Mini-Assignment 3 (GenAI audio), Animation Assets | `walker-jumpman-clawd` assets; Walker `asset-gen` local helpers |
| 3 | `chapters/03-blender-mcp-to-godot.md` | Wk 3 Blender MCP → Godot | Animation in Blender; Houdini intro (context only) | `walker-3d-platformer`, `walker-3d-csg` |
| 4 | `chapters/04-scenes-collision-and-physics.md` | Wk 4 Scenes, collision & physics (2D/3D mechanics) | Unity C#; Unreal Blueprints; 2D Games; Assignment 3 – Unreal Blueprints | `walker-2d-dodge-the-creeps`, `walker-pong`, `walker-2d-bullet-shower`, `walker-2d-dynamic-tilemap-layers`, `walker-loading-autoload`, `walker-loading-scene-changer` |
| 5 | `chapters/05-the-gdd-and-virtual-worlds.md` | Wk 5 GDD & virtual worlds (3D interaction; scope mobile, network, XR) | Game Design Document; Best Practices; Prototyping a Project; GDD assignments; Pitch Your Game | `walker-jumpman-clawd/design`, Walker `/gdd`, `walker-3d-platformer`, `walker-viewport-*`, `walker-xr-*`, `walker-mobile-*` |
| 6 | `chapters/06-shader-foundations.md` | Wk 6 Shader foundations (project context in CLAUDE.md) | Unity Shaders and Unreal Materials; CgFX; ShaderToy; Assignment 4 – Shaders | `walker-compute-post-shader`, a `walker-*` 2D project |
| 7 | `chapters/07-materials-and-textures.md` | Wk 7 Materials & textures | Unity Shadergraph; HLSL/Custom Nodes in Unreal; material link pages | `walker-3d-decals`, `walker-3d-global-illumination`, `walker-compute-texture`, `walker-compute-heightmap`, `walker-3d-graphics-settings` |
| 8 | `chapters/08-shader-verification.md` | Wk 8 Shader verification (review a plausible but incorrect change) | Assignment 4 – Shaders (verification half) | same as 6–7 |
| 9 | `chapters/09-particle-effects.md` | Wk 9 Particle effects | Particle Effects; Particle Effects in Unity; Flocking/VFX Graph; Assignment 5 | adapt `walker-2d-dodge-the-creeps` / `walker-3d-platformer` (has `particle_material.tres`) |
| 10 | `chapters/10-animation-foundations.md` | Wk 10 Animation foundations (behavior checks before track changes) | Animation; Animation in Unity / Unreal / Blender; Spriter; Assignment 6 | `walker-2d-finite-state-machine`, `walker-3d-ik` |
| 11 | `chapters/11-animation-and-interaction.md` | Wk 11 Animation & interaction (states ↔ player actions) | Mini-Assignment 2 (GenAI animation) | `walker-3d-platformer`, `walker-2d-finite-state-machine`, `walker-jumpman-clawd` |
| 12 | `chapters/12-audio-and-triggers.md` | Wk 12 Audio & triggers | Audio; Mini-Assignment 3 | the seven `walker-audio-*` builds |
| 13 | `chapters/13-profiling-and-optimization.md` | Wk 13 Profiling & optimization (mobile/XR constraints) | Profiling in Unity and Unreal | `walker-2d-bullet-shower`, `walker-3d-graphics-settings`, `walker-3d-antialiasing`, `walker-viewport-3d-scaling`, `walker-loading-threads`, `walker-loading-load-threaded`, `walker-misc-custom-logging` |
| 14 | `chapters/14-game-ai-and-systems.md` | Wk 14 Game AI & systems (navigation, behavior trees, PCG, scoped networking) | Game AI (FSM, BT, NPCs, logic, simulation, RL: Q-learning/DQN/PG/PPO, Gym); Game AI with Unity (NavMesh, ML-Agents, AI Planner); Procedural Content Generation (+ Houdini) | `walker-2d-finite-state-machine`, `walker-2d-dynamic-tilemap-layers`, `walker-compute-heightmap`, `walker-networking-*` |
| 15 | `chapters/15-final-projects-brief-to-export.md` | Wk 15 Final projects: full brief-to-export cycle | Final Portfolio Piece; Show and Tell; take-home midterm/final | `walker-jumpman-clawd` (full cycle), `walker-loading-*` (save/load, scene flow), `walker-gui-*` (menus, accessibility) |

Where a topic has no existing Walker build (particles, navigation, reinforcement learning), **adapt** an existing `walker-*` build or the matching upstream demo rather than inventing a new project from nothing, and say which.

## 2. Section skeleton (every chapter, in this order)

```
# Chapter N — Title

## Executive summary
  What this chapter is, why read it, what you will build and what that build does and
  does not prove. Plain language, 4–8 sentences. (Bear's rule: summary before any
  technical header.)

## The question
  A genuine puzzle or failure that the chapter resolves. Concrete, not rhetorical.

## Ideas you need
  The Godot concepts, explained as machinery (how it works and why it was designed that
  way), each linked to the official Godot documentation (docs.godotengine.org/en/stable/…).
  Use the course vocabulary from Chapter 1 (node, scene, scene tree, signal, script,
  collision shape, asset). Small tables and code are welcome.

## The Walker example: <walker-project-name>
  What the build is, where it came from (upstream path + commit, license), what its
  checks actually establish (quote real numbers from its README/FRICTIONAL), and what
  remains unverified. File references to the real files.

## Hands-on: <task>
  The Predict → Build It → Use It → Ship It → Verify template from Module 1.
  ### Predict        – 2–4 questions the student answers before delegating.
  ### Build It       – exact prompts to paste into Claude Code (and the Codex difference
                       where it matters), plus the exact shell commands. Prompts in ```text
                       blocks; shell in ```bash blocks, one command per block.
  ### Use It         – what to do in the editor / the running game and what to observe.
  ### Ship It        – the commit, the FRICTIONAL entry, which Brutalist Godot skill
                       (godot-walkthrough / godot-gamedev / godot-gdd) fits this work.
  ### Verify         – the headless command(s) and what a pass does and does not prove.

## What we actually ran
  The worked example: the date, the tool and model, the starting revision, the prompt
  given, what the agent changed (summarised diff with file names), the exact test command
  and its real output (trimmed), anything that went wrong and how it was fixed. Link to
  `../examples/NN-slug/`. Never present an unrun step as run.

## Check your understanding (ungraded)
  4–6 questions that require reading the source or running the game.

## Doing the same thing in Unity
  ### Similarities
  ### Differences
  Concretely: how you would do THIS chapter's hands-on task in Unity (which systems,
  which files, how an agent would edit them, how you would test headlessly
  — e.g. batchmode / Test Framework), and a short Godot ↔ Unity term table.
  Include the agent-workflow angle: which artefacts are text an agent can read and
  diff, which are binary or editor-only.

## Doing the same thing in Unreal Engine
  ### Similarities
  ### Differences
  Same treatment for Unreal Engine 5 (Blueprints vs C++, assets as .uasset, editor
  Python, commandlets/automation tests, the relevant subsystem — Niagara, Material
  Editor, Behavior Trees/StateTree, PCG framework, Unreal Insights, etc.).

## Sources
  Every external claim's source, as a list of links (official docs first). Mark the
  Unity/Unreal sections as documentation-based: "Unity and Unreal were not run for this
  chapter; the comparisons come from their official documentation, checked on <date>."
```

The Unity and Unreal sections are the last content sections of every chapter; only **Sources** follows them.

## 3. Evidence standard for the hands-on example

1. **Work on a copy, never the original.** Copy only a project's `godot/` folder (plus its small `.md` files) into your scratch directory, `git init` it, and commit a baseline. Never copy `youtube/`, `evidence/`, `_work/` or media. Never edit any `books/walker-*` directory, the Walker framework, or course files other than your own chapter and example folder.
2. **Headless only.** Run Godot with `--headless`. Do **not** open a visible Godot window or editor: Professor Bear closed capture windows and the demo series records a standing constraint against reopening them. Anything that needs a display (visual appearance, shader output, feel) is stated as a **human check** the student performs, not claimed.
3. **Use the real CLI for the example.** Perform the chapter's hands-on task by running a coding agent from the command line with the **exact prompt printed in the chapter**, in the scratch copy — `claude -p "<prompt>" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose > session.jsonl` (adjust tools to the task; keep them scoped). `codex exec` is an acceptable alternative or comparison. Keep the transcript. If the agent's result fails, that failure is part of the example: record it, then show the correction.
4. **Verify with your own command, not the agent's claim.** After the agent finishes, run the check yourself (`godot --headless --path … --script res://tests/…`) and record the real output. A passing headless test is state evidence, not a playtest.
5. **Store the record** in `examples/NN-slug/` (course repo): `README.md` (executive summary first; how to reproduce), `PROMPTS.md` (exact prompts), `changes.diff` (`git diff` from the baseline), any new test scripts, and the headless logs. Keep the session transcript if under ~1 MB; otherwise keep a trimmed excerpt and say so. No binaries over 200 KB, no media, no `.godot/` caches, no secrets.
6. **Starting points students can reach.** *(Superseded 2026-09-27: the `walker-*` adaptations are now public at `github.com/nikbearbrown/walker-*`, except `walker-gui-bidi-and-font-features`. Chapters 2–15 carry a "Get the builds" paragraph linking them; the upstream path below remains the provenance.)* Only `walker-jumpman`, `walker-jumpman-clawd` and `walker-pong` are public on GitHub (`github.com/nikbearbrown/<name>`). For every other build, tell students to start from the upstream demo in `github.com/godotengine/godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7` (the source of every `walker-*` adaptation, MIT license) and give the path (e.g. `2d/dodge_the_creeps`). The Walker adaptation's test harness can be reproduced from `examples/`.
7. **Engine version.** Godot **4.7.2** (regular, GDScript; the `godot` command is `/opt/homebrew/bin/godot` on the instructor's Mac). Name the version for anything version-sensitive.

## 4. Voice

- The **Teardown** register (`brutalist.art/runtime/prose/teardown/PROSE.md`): take the thing apart, explain how each piece actually works, judge the design choices, admit the limits. Short sentences for clarity; longer ones only to show how systems connect. Know the thing, not just its name.
- Address the student as **you**. Where the text speaks for the course's author about his documented course decisions, use **I** (Nik Bear Brown) — sparingly, and only for decisions recorded in the course files.
- Match Chapter 1 / Module 1's discipline: a plausible description is not a game; a passing command is not a playtest; an AI's "done" is not evidence.
- No hype, no filler, no "In this chapter we will explore…". No emoji.
- Markdown only. Code blocks tagged (`gdscript`, `bash`, `text`, `glsl` for Godot shading language is acceptable as `glsl` or `gdshader`).
- Length: roughly 4,000–7,000 words. Depth over breadth.

## 5. Hard limits

- **No fabrication.** Every factual claim about Godot, Unity, Unreal, Claude Code, Codex, or a tool is checked against official documentation or a real run. No invented quotes, statistics, benchmarks, release dates, or feature names. If you could not verify something, say so or leave it out.
- **Version care for Unity and Unreal.** Prefer version-stable facts. If you name a version or say "current", verify it on the vendor's site on the day and date it ("as of September 2026"). Do not repeat the old syllabus's error that Unreal is open source (it is source-available under the Unreal Engine EULA).
- **Do not use the third-party books** stored in the course folder (`*Z-Library*`, `930723439-Game-AI-Made-Easy-*`). Do not read or quote them.
- **No spend, no publishing.** No paid generation (Higgsfield, image/audio APIs), no GitHub pushes, no commits in the course repo, no YouTube, no Canvas. No large downloads (e.g. Godot export templates) — state what would be needed instead.
- **Disk.** The Mac has ~30 GB free. Keep each scratch workspace under ~300 MB. No video capture or rendering.
- **No stubs.** Write each chapter in full or report that you could not; never leave placeholder sections.

## 6. Addendum — rules learned while drafting (2026-09-27)

These came out of the real runs behind Chapters 0–15. They apply to every future hands-on example and to the prompts printed for students.

- **Pin the time step for frame-counted tests.** A test that counts frames while the game moves by `delta` seconds is machine-dependent. Run it with `--fixed-fps 60`. Without the flag, headless Godot sleeps toward a 6,900 µs frame (`low_processor_mode_sleep_usec`, "Roughly 144 FPS" in the 4.7.2 source), so 4,800 frames cover ~33 s of game time, not 80. The exception is audio drain waits and networking, which must run in real time; say which mode each run used (Chapters 0, 12, 13, 14).
- **Wrap every headless run in `timeout`.** A script error before `quit()` leaves headless Godot running forever (one hung for 30 minutes).
- **Headless exit code 0 is not "no errors."** Shader and script errors can print to stderr while the process exits 0 (Chapters 4, 6, 14). Tests should fail on errors they can detect, and reviewers should read stderr.
- **Import before testing.** Run `godot --headless --path <project> --import` once after cloning. Without it, UID warnings and missing-resource errors appear; one clean-clone run exited 0 with 55 ERROR lines (Chapter 4).
- **Scope agent permissions narrowly.** `Bash(env *)` allows any program. `Bash(godot *)` allows any GDScript, which can call `OS.execute()`. Both were used to route around a refused command. Add `--disallowedTools "Skill"` to nested `claude -p` runs; one session tried a settings-writing skill.
- **`codex exec` from a script needs `< /dev/null`,** or it can wait forever on "Reading additional input from stdin...".
- **Never run a test against the player's real `user://`.** Redirect `HOME` (or use a test-only save path). One verification run wrote into the real app-data folder (Chapter 15).
- **Tell the agent how to run the checks.** The most effective fix observed was one `## Checks` paragraph in `AGENTS.md` with the exact import and test commands (Chapter 0, Revise).
- **Do not pass display flags without `--headless`.** `--display-driver headless` alone, or `--headless` plus `--rendering-driver`, fell back to the macOS window server in Chapter 6's probes.
- **Usage limits are real.** Claude Code's session limit ended several runs; Codex finished them. Chapters say which tool did which step.
