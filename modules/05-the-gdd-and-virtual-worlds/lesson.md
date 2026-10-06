# Module 5 — The GDD and virtual worlds

CSYE 7270 · Fall 2026 · Week 5

## Executive summary

A game design document, or GDD, is a promise about what a game does, written so that people, and now agents, can build it and check it. You will recover a GDD from an existing 3D project, audit it against the source, write one measurable acceptance criterion for a small new 3D interaction, have an agent build it, and verify it with a test you run yourself. On 27 September 2026 the recovered GDD for Godot's 3D Platformer was mostly accurate, yet it stated at least nine wrong or unsupported things, including the key that fires the gun. Claude Code's build was cut off by a usage limit and Codex finished it. Walker's `/gdd` skill did the recovery and is not in public Walker `main` yet, so this page gives the public fallback. The build proves the interaction meets its written criterion in headless play, not that anyone can see the pad or enjoys it.

## The question

Walker's GDD skill read the Godot 3D Platformer demo and returned a sixteen-section document with 107 `[OBSERVED]` tags, each citing a file and line. Section M-06 says the player shoots with **F9**. The project binds shooting to the physical **Ctrl** key. Section M-03 reports jump heights of 1.53 m and 3.60 m and cites `evidence/baseline-probe.json`; the agent listed that file but never opened it. Section 09 says no skybox exists; the stage folder holds a skybox shader and texture.

None of this stops the document looking finished, and all of it travels: into a film script, into tests an agent writes from the GDD, into the next student's understanding. What makes a design statement trustworthy, and what must it say before an agent can build from it and you can prove the build matches it?

## The ideas

### What a GDD is for

The Spring 2026 course page said a GDD shares the owner's vision with the team and "often is made subject to a lot of changes." Its section list still works as a checklist of decisions: elevator pitch, game flow, assets, characters, story, gameplay (goal, mechanics, levels, losing or restarting, the skills a player needs), graphics, sound, technical description, and a production document that turns the design into tasks. The prototyping page's shorter list (world, interface, player, other characters, key objects, animations) suits a first sketch.

Walker's framing is sharper. A **game brief** says what the player does, what success looks like, what can go wrong, and what is out of scope. A **GDD** develops those decisions until an engineer can implement them and a tester can check them. Keep observation, proposal, approval, implementation and verification separate: a GDD is not a game, and a newer GDD does not validate an older build.

Three engine-neutral habits carry forward from the old documentation and pitch assignments: write numbers, not adjectives; make every feature justify itself and document non-goals as rigorously as goals; and explain your most distinctive mechanic twice, as a spec and in a sentence a non-player would follow. The old course asked for exact numbers but never ran them. This module does.

### Zelda, stable IDs, failure modes and gates

Walker's GDD skill speaks as **Zelda**, a senior-designer persona adapted from **Forge**, the GDD prompt set of Spring 2026. Forge's commands (`v1`–`v4` vision, `s1`–`s4` systems, `w1`–`w3` world, `p1`–`p5` scope, `g1`–`g4` compile and review) survive almost intact, and Walker added `reverse`, `draft`, `deck`, `film` and `status`. Three Forge ideas matter here.

- **Sixteen sections,** from pillars and mechanics to out of scope, risks and open questions.
- **Stable IDs** (`PX-01`, `M-01`, `F-01`, `T-01`), so a ticket, a test and a playtest note can point at the same thing.
- **Seven failure modes,** such as Priority Inflation (more than 40% of features tagged CORE) and the Implementation Void (mechanics with only a happy path).

Design runs in four phases, each followed by a gate (vision, systems, world, scope) recorded in `design/DESIGN-STATUS.json`. Zelda never signs a gate herself. The `silent` flag skips the questions and gates for one call and writes "gate — unsigned at time of writing." That suits a rough draft, not approval.

### Provenance tags

When `/gdd reverse` recovers a design from code, every claim gets a tag: `[OBSERVED path:line]` (the code does this), `[INFERRED]` (the code implies it; the evidence is stated) or `[MISSING]` (the code cannot tell you, such as the win condition). `/gdd draft` adds `[ASSUMPTION]` for a gap Zelda filled. A tag is a claim about evidence, not evidence: to know an `[OBSERVED]` tag is right, open the cited line.

### Acceptance criteria a machine can check

A requirement is testable when a stranger could write the test without asking you anything. Name:

- **The quantity and its unit.** Godot's 3D units are metres ([Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)).
- **A tolerance.** "Returns to the pad" is not checkable; "within 0.2 m of the respawn point" is.
- **A time box in the engine's clock,** such as "within 600 frames at `--fixed-fps 60`," not "quickly."
- **How the state is reached:** ordinary input through `Input.action_press`, or a constructed fixture that writes state directly. Both are legitimate but prove different things, so say which.
- **What must not change,** and **what is out of scope** because only a person can judge it.

### The 3D machinery for this interaction

**Coordinates and physics.** Godot 3D is right-handed with Y up, and a `Node3D`'s transform is relative to its parent, so a position in a `.tscn` is local. This project runs 120 physics ticks per second with Jolt, so at `--fixed-fps 60` each frame carries two ticks. The platformer's coins sit under a parent offset by (−16, −6, −12), so a coin written at (18.5, 2.35, 5.25) is near (2.5, −3.65, −6.75) in the world.

**Areas, signals and layers.** An `Area3D` detects bodies, and `body_entered` needs `monitoring` on ([Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)). The coin's handler `_on_coin_body_enter` is never connected in `coin.gd`; the connection is a `[connection]` line in `coin/coin.tscn`, so an agent that reads only `.gd` files will think the handler is dead code. Everything here uses layer 1 and mask 1, so a new `Area3D` sees the player. Layer *n* is the value 2^(n−1), as in Module 4.

**Instancing, markers and teleports.** An instance in a `.tscn` is an `ext_resource` line plus a `[node ... instance=ExtResource("id")]` line ([TSCN format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)); hand-editing these is the "dangerous middle," where references parse cleanly and point at the wrong thing. A `Marker3D` is the natural respawn point ([Marker3D](https://docs.godotengine.org/en/stable/classes/class_marker3d.html)). This project uses physics interpolation, so code that teleports an object must call `reset_physics_interpolation()` ([docs](https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/using_physics_interpolation.html)). `player.gd`'s reset code already does, so a checkpoint must reuse it.

### Scoping mobile, networked and XR worlds

The syllabus asks you to scope these in Week 5, not build them: say what each target needs, what you can verify with the hardware you have, and what stays unverified. Mobile touch arrives as `InputEventScreenTouch`, and mouse-emulated touch is not a phone ([input](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html)). Networking uses ENet over UDP, and client input is untrusted ([multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)). OpenXR needs an `XROrigin3D`, an `XRCamera3D` and usually two `XRController3D` nodes, and can fail to initialize ([XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html)).

A scoping paragraph is honest when every sentence is a requirement, a verified fact about your build, or a named unverified item. The Walker builds show the pattern. [`walker-mobile-multitouch-cubes`](https://github.com/nikbearbrown/walker-mobile-multitouch-cubes) verified pinch and rotate with synthetic touch events and lists any physical device as unverified. [`walker-networking-multiplayer-bomber`](https://github.com/nikbearbrown/walker-networking-multiplayer-bomber) ran two real ENet processes on loopback and lists anything beyond loopback as unverified. [`walker-xr-openxr-character-centric-movement`](https://github.com/nikbearbrown/walker-xr-openxr-character-centric-movement) is import only: OpenXR fails without a headset.

## The Walker example: /gdd, walker-jumpman-clawd/design, and walker-3d-platformer

**Do you have `/gdd`?** The skill lives in the Walker framework at `gdd/` and writes only into `design/`. As of 27 September 2026 the `gdd/` folder and the `publish.sh` that installs it existed only in the instructor's local Walker copy. Public [Walker](https://github.com/nikbearbrown/walker) `main` (commit `10fedb8`, 11 September) predates them, and a check on 6 October 2026 still found no `gdd/` folder. **You cannot clone the skill yet.** The public repository does carry the reusable prompt [`prompts/zelda-gdd.md`](https://github.com/nikbearbrown/walker/blob/main/prompts/zelda-gdd.md), which you can hand to an agent as plain instructions. It installs no `/gdd` command and has no `reverse` spec. If your instructor gives you a Walker copy containing `gdd/`, use Route 1; otherwise use Route 2. Read `publish.sh` before running it, because it overwrites an existing `CLAUDE.md` or `AGENTS.md`; install only the `gdd` skill.

**A recovered GDD with a confident error.** On 18 September 2026 the skill produced `design/` version 0.3.0-draft for `walker-jumpman-clawd`, separating the game that exists from `[ASSUMPTION]` proposals. Its decision D-02 says the layer names "4 Hazard, 5 Goal" do not match code (8, 16). They match: layer 4 is the value 8 and layer 5 is 16, so applying D-02 would break correct names. That folder was not public when the chapter was checked on 27 September; a check on 6 October 2026 found it in the public [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd) `design/` folder (version 0.3.0-draft, D-02 still unapplied).

**The 3D build.** [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer) is Godot's official 3D Platformer demo (`3d/platformer` in [`godot-demo-projects`](https://github.com/godotengine/godot-demo-projects), commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`); the public repository keeps the upstream MIT license. A blue robot jumps through a GridMap level, collects coins and shoots patrolling robots; the adaptation changed one line, `config/name`. Rerun on 27 September with `--fixed-fps 60`: `tests/input_probe.gd` drives 600 frames and passed four checks (movement, jump, projectile created, reset); `tests/feature_route.gd` runs 1,800 frames and reported `coins=2 enemy_hit=true`. Unverified: everything visual and audible, touch and gamepad, and every human judgment.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Answer before running anything, and keep the answers.

1. The reverse pass will tag most claims `[OBSERVED]`. Pick two it may get wrong and say why: integer input bindings in `project.godot`, line numbers, world versus local positions, or claims copied from Markdown rather than code.
2. `input_probe.gd` checks reset against the player's start position. If your pad sits on the path the probe walks, what happens to that check, and is it a bug in the pad or in the probe?
3. Criterion 5 below places the player below y = −12 directly. What does that prove that input alone cannot, and what does it fail to prove?
4. Where is the hard part: `player.gd`, the pad's placement, or the `game.tscn` edit?

### 2. Build It

**Get the project and a baseline.** Obtain your own copy of the public `walker-3d-platformer`, which has `godot/` and the two probes in `tests/`; do not edit the instructor's repository. Record the starting commit in `FRICTIONAL.md` as your baseline, and make sure `.gitignore` excludes `.godot/` and `evidence/`. Import once, then run both probes. They take a fresh report path after `--` and refuse to overwrite one; `timeout 120` stops a script error from hanging headless Godot.

```bash
godot --headless --path godot --import
```

```bash
mkdir -p evidence
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script $PWD/tests/input_probe.gd -- $PWD/evidence/baseline-probe.json
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script $PWD/tests/feature_route.gd -- $PWD/evidence/baseline-route.json
```

Expect `{"jump":true,"movement":true,"projectile_created":true,"reset_action":true}` and then `coins=2 enemy_hit=true`, both exiting 0. Leak warnings may print at exit.

**Route 1: you have a Walker copy containing `gdd/`.** Copy only that folder and fill in its tokens the way `publish.sh` would; `../walker` is your copy.

```bash
mkdir -p .claude/skills
```

```bash
cp -R ../walker/gdd .claude/skills/gdd
```

```bash
python3 ../walker/scripts/render_dir.py .claude/skills "AGENT_NAME=Claude" "GDD_SKILL_DIR=.claude/skills/gdd" "GDD_SKILL_COMMAND=/gdd" "ASSET_GEN_SKILL_DIR=.claude/skills/asset-gen" "ASSET_SKILL_COMMAND=/asset-gen" "RUNTIME_ASSET_DIR=assets"
```

```bash
grep -rn '\${' .claude/skills/gdd
```

That last command should print nothing: every token was replaced. Commit the skill separately.

```bash
git add .claude && git commit -m "Install Walker gdd skill"
```

For Codex the folder is `.agents/skills/gdd`, the command is `$gdd`, and metadata is generated as below (not run in the chapter).

```bash
python3 ../walker/scripts/generate_codex_metadata.py .agents/skills
```

**Prompt 1: recover the design.** In Claude Code the whole prompt is the slash command; `silent` skips Zelda's questions and gates for this call.

```text
/gdd reverse --path godot silent
```

Headless, with a transcript (make a `notes` folder first); it took twenty minutes in the chapter's run.

```bash
claude -p "/gdd reverse --path godot silent" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose < /dev/null > notes/session-1-reverse.jsonl
```

Under Codex it is `$gdd reverse --path godot silent` (not run in the chapter). Commit the result as agent output, unreviewed.

```bash
git add design && git commit -m "gdd reverse (silent): agent output, unreviewed"
```

**Route 2: you do not have the skill.** Do not paste Prompt 1; the command will not exist. The chapter's fallback is `prompts/zelda-gdd.md` as plain instructions, but it has no `reverse` spec and the chapter printed no tested prompt for it, so say in `FRICTIONAL.md` that you did not recover the design. To still practise the audit, use a GDD that exists: the repository's own `GDD.md`, or, as a course suggestion the chapter did not run, the `recovered-design/` folder of the [example record](../../examples/05-the-gdd-and-virtual-worlds/README.md) copied into `design/`, which has the section numbers Prompt 2 names. Commit it as unreviewed.

**Audit it.** This part is yours. Check at least these in the GDD and `IMPLEMENTATION-MAP.md`, and log each finding in `FRICTIONAL.md`.

1. Every input binding. `project.godot` stores keys as integers, so ask Godot: `OS.get_keycode_string(4194326)` in a one-line `SceneTree` script prints `Ctrl`.
2. Five `[OBSERVED path:line]` tags chosen at random. Open the line.
3. Every number attributed to a file under `evidence/`. Did the agent open it? The transcript tells you.
4. Every `[MISSING]` or "not found" claim. One `grep` often settles it.
5. Every "tested" or "verified." Which test, and does it exist?
6. That `DESIGN-STATUS.json` shows all four gates unsigned. Do not sign them to look finished.

**Write the acceptance criterion** before any agent touches the code. The chapter's interaction is a checkpoint pad: once the player walks onto it, the reset action and falling off the map return the player to the pad instead of the level start. You may build the pad or specify a small 3D interaction of your own, with your own Prompt 2 in the same structure (one concern, invariants, allowed edits, exact commands, a stop rule). The [full criterion](../../examples/05-the-gdd-and-virtual-worlds/AC-01-checkpoint-pad.md) is in the example record.

| # | Criterion | Reached by |
|---|---|---|
| 1 | `Area3D` pad, at least 1.5 m × 1.5 m, on walkable floor 3–6 m from the start, off `input_probe.gd`'s path | scene observation |
| 2 | Before activation, `reset_position` held 5 frames leaves the player within 0.2 m of the start | input only |
| 3 | Pad reached within 600 frames; it activates once, and re-entry does not re-activate it | input only |
| 4 | After activation, `reset_position` held 5 frames leaves the player within 0.2 m of the pad's respawn point | input only |
| 5 | After activation, a player placed below y = −12 is within 0.2 m of the respawn point within 2 frames | constructed fixture, labelled |
| 6 | Both existing probes still pass: all four checks true, a coin collected, exit 0 | existing probes |

The criterion also lists what is out of scope: whether a player can see and understand the pad, touch, gamepad and export.

```bash
git add design/AC-01-checkpoint-pad.md && git commit -m "AC-01 checkpoint pad: human-authored acceptance criterion"
```

**Prompt 2: build it and test it.** It refers to sections M-05 and 06b of the recovered GDD; use the section numbers from yours.

```text
Implement design/AC-01-checkpoint-pad.md in this Godot 4.7.2 GDScript project
(walker-3d-platformer). Read that file, design/GDD.md sections M-05 and
06b, and godot/player/player.gd first.

One concern: a checkpoint pad that moves the player's respawn point.
Invariants: do not change any movement, jump, camera, coin, enemy, or
bullet behaviour or constant; do not change godot/project.godot; keep
the existing reset and fall code path, only change where it sends the
player. Allowed edits: godot/player/player.gd (respawn point only),
godot/game.tscn (instance the pad), and new files under godot/checkpoint/
and tests/. The pad needs a visible mesh so a person can see it.

To place the pad you may run read-only Godot probe scripts to find
walkable floor near the start; delete nothing, and put any probe you keep
under tests/. Write tests/test_checkpoint.gd as a SceneTree script that
drives the player with Input.action_press/action_release only, except the
fall check in criterion 5, which must be labelled as a constructed fixture.
It prints one JSON line per criterion and exits 1 if any fails.

Run, from the project root, and read the real output of each:
godot --headless --path godot --import
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/test_checkpoint.gd
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/input_probe.gd -- $PWD/evidence/probe-after.json
godot --headless --path godot --fixed-fps 60 --script $PWD/tests/feature_route.gd -- $PWD/evidence/route-after.json
(The two probes refuse to overwrite an existing report; pick a new file
name if one exists.)

If a criterion cannot be met as written, stop and say which and why; do
not weaken the criterion or the test. Finish with git status, git diff
--stat, and a list of what still needs a person to check in the editor.
```

Headless, with the prompt saved as `notes/prompt-2-implement.txt`:

```bash
claude -p "$(cat notes/prompt-2-implement.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose < /dev/null > notes/session-2-implement.jsonl
```

Claude Code declines to auto-approve a command containing a shell expansion such as `$PWD`, so in your own prompt write the absolute path; the agent had to reword one command. If an agent stops partway, as the chapter's did at its usage limit, do not start over: hand the working tree to a fresh session or the other CLI with this preface, saved with the full Prompt 2 as `notes/prompt-3-continue.txt`.

```text
A previous agent session (Claude Code) was stopped by an account usage
limit partway through the task below, before it ran any test. Its partial
work is in the working tree: see git status and git diff. Review that
partial work critically against design/AC-01-checkpoint-pad.md, keep or
change it, and finish the task. The task, exactly as it was given:
```

```bash
codex exec --sandbox workspace-write --json -o notes/codex-continue.md "$(cat notes/prompt-3-continue.txt)" < /dev/null > notes/session-3-codex.jsonl
```

The allow list omits `python3`, `rm` and any general shell: the agent tried `python3` five times, was refused, and used its Read tool instead. Do not add `Bash(env *)` or a similar wrapper; a command that runs other commands allows everything.

### 3. Use It

The chapter's run had no display, so none of this was done. Open `godot/project.godot` in the regular Godot editor. Each item is a **HUMAN CHECK**.

1. **HUMAN CHECK.** Find the pad in `game.tscn`. Does its mesh sit on the floor, or float or sink? Where is the respawn point?
2. **HUMAN CHECK.** Run and walk onto the pad. Can you tell it activated? If nothing visible changes, that is a design gap your criterion missed: log it as an open question, not a build failure.
3. **HUMAN CHECK.** Press R, then walk off an edge. Does the camera snap cleanly on respawn, or sweep from the old position?
4. **HUMAN CHECK.** Play five minutes as someone who has never seen the pad. Would they notice it?

### 4. Ship It

Commit the implementation on its own, with the criterion ID in the message.

```bash
git add -A && git commit -m "AC-01 checkpoint pad: implementation and test_checkpoint.gd"
```

In Route 1, add a changelog entry with the skill rather than editing the GDD by hand.

```text
/gdd changelog
```

In Route 2, record the entry in `FRICTIONAL.md` and leave the GDD alone. Either way, log the audit findings and the build there: which tags were wrong, how you found out, what you changed. Do not sign any gate. The film skill that fits is `godot-gdd`, which keeps proposed, built, tested and human-reviewed claims separate. It comes from a course-provided checkout of [brutalist.art](https://github.com/nikbearbrown/brutalist.art); if your copy lacks it, request the update.

### 5. Verify

Run all three tests yourself; do not rely on the agent's report.

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script $PWD/tests/test_checkpoint.gd
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script $PWD/tests/input_probe.gd -- $PWD/evidence/verify-probe.json
```

```bash
timeout 120 godot --headless --path godot --fixed-fps 60 --script $PWD/tests/feature_route.gd -- $PWD/evidence/verify-route.json
```

Then read the test, not just its output. Criteria 2 to 4 should use only `Input.action_press` and `action_release`, criterion 5 should be labelled a fixture, and you should know what each distance is measured against. A distance measured against a value the implementation computed itself is a gap in your criterion.

A pass proves that, at Godot 4.7.2 with a pinned time step, ordinary input reaches the pad, the pad moves the respawn point, and the old probes still pass. It does not prove the pad is visible, understandable, fair, or worth having. Read stderr too: one verification run in the example record exited 0 while logging a Jolt warning.

## What the agents got wrong

Run on 27 September 2026 with Claude Code 2.1.150 and Codex CLI 0.153.4.

1. **A recovered GDD that looked checked.** Nine claims were wrong or unsupported. The shoot key is Ctrl, keycode 4194326, not F9. The jump numbers came from `FRICTIONAL.md`, not the file the tag cited. The skybox files exist. A chat summary called 11 CORE features "observed and test-verified" when only six had any headless check. A one-line script, the transcript and an `ls` caught these; the tags did not.
2. **A fix with the wrong reason.** Claude Code hit its account usage limit after 43 turns, before any test ran. Codex strengthened the test but said the old check had been "raycasting against the pad itself." A ray ignores areas by default: the same ray hit the GridMap floor at y = −6.0, and hit the pad only with `collide_with_areas = true`. The old check was weak, but not for that reason.
3. **A criterion with a gap.** The pad computed its own respawn point from the player's height at entry, and criterion 4 measured against that number. The value was sensible (y = −5.91), but the criterion never said where it must be. A better one names it: a `Marker3D` child of the pad, no more than 0.2 m above its top surface. Only reading the code revealed the gap.

## If you know Unity or Unreal

Unity and Unreal were not run; these comparisons come from official documentation, checked on 27 September 2026.

| Godot | Unity | Unreal Engine 5 |
|---|---|---|
| `Area3D` + `body_entered` | trigger collider + `OnTriggerEnter` | Trigger Volume + `OnActorBeginOverlap` |
| `Marker3D` respawn point | empty GameObject transform | Player Start actor |
| `.tscn` text scene | scene YAML, GUIDs in `.meta` files | `.umap` level, binary |
| scripted-input probe | Play Mode test with `WaitForFixedUpdate` | Functional test actor in a level |
| OpenXR in Project Settings | XR Plug-in Management + OpenXR | OpenXR plugin |

A GDD is engine-agnostic, so criteria, tags, gates and scoping read the same in all three. What changes is what an agent can recover. A Godot reverse pass reads `res://coin/coin.gd` straight from a text scene; Unity makes it resolve a GUID; a mechanic built as an Unreal Blueprint is binary, so most of a recovered GDD would be `[MISSING]` or `[INFERRED]` from names. The [chapter](../../chapters/05-the-gdd-and-virtual-worlds.md) has the full comparison.

## Practice assessment (ungraded)

Answer in your own words, from the source. An ungraded practice quiz on Canvas covers the same ground; retake it freely and read the feedback.

1. Where is the coin's `_on_coin_body_enter` connected, and what would an agent conclude if it read only `coin/coin.gd`?
2. Pick a coin in `game.tscn`, whose parent sits at (−16, −6, −12), and compute its world position.
3. Rewrite this so a stranger could test it: "The checkpoint should feel responsive and reset the player quickly."
4. Criterion 5 writes the player's position directly. What does that prove that an input-only test cannot, and what does it fail to prove?
5. Pick one scoping build above and write two sentences for a GDD's technical section: one verified fact, one named unverified item.

Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then check the source yourself.

## The next step

Next is **Assignment 4, "Specify It, Then Build One 3D Interaction."** It opens in Module 5 and is due about Day 40, with a `godot-gdd` film; this lesson is the practice for it, and the assignment's own text sets its requirements. Module 6 then turns to shader foundations. The long reading is the companion chapter, [Chapter 5 — The GDD and Virtual Worlds](../../chapters/05-the-gdd-and-virtual-worlds.md).
