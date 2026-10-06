# Chapter 5 — The GDD and Virtual Worlds

## Executive summary

A game design document is a promise about what a game does, written so that other people, and now agents, can build it and check it. This chapter makes that promise concrete in three steps. You recover a GDD from an existing 3D project with Walker's `/gdd reverse` skill, audit what it claims against the source, and then write one measurable acceptance criterion for a small new 3D interaction (a checkpoint pad), have a coding agent build it, and verify it with a scripted-input test you run yourself. We did all three on September 27, 2026 with the `walker-3d-platformer` example. The recovered GDD was 4,777 words and mostly accurate, and it stated at least nine things that were wrong or unsupported, including the key that fires the gun. The build was started by Claude Code, cut off by an account usage limit, and finished by Codex, which strengthened the test and gave a wrong reason for one of its changes. The chapter also shows how to scope mobile, networked, and XR versions of a world honestly, using the course's Walker builds, most of whose hardware-dependent behavior is still unverified. What the build proves: the new interaction meets its written criterion in headless play, and the old checks still pass. What it does not prove: that a player can see the pad, understands it, or enjoys the game more with it.

## The question

We asked Walker's GDD skill to read the Godot 3D Platformer demo and write down what the game is. It worked silently for twenty minutes and returned a sixteen-section document with 107 `[OBSERVED]` tags, each pointing at a file and a line. Section M-06 says the player shoots with **F9**. The project binds shooting to the physical **Ctrl** key. Section M-03 reports measured jump heights of 1.53 m and 3.60 m and cites `evidence/baseline-probe.json`; the agent listed that file but never opened it, and the numbers came from somewhere else. Section 09 says no skybox exists; the stage folder contains a skybox shader and texture.

None of these errors would stop the document from looking finished. All of them would travel: into a film script, into a test an agent writes from the GDD, into the next student's understanding. So what makes a design statement trustworthy? And the harder half of the question: what must a design statement say before an agent can build from it and you can prove the build matches? The old version of this course asked for GDDs with "exact numbers" and never ran them. This chapter runs them.

## Ideas you need

### What a GDD is for

The old course page put it simply: a GDD shares the owner's vision with the team, and it "often is made subject to a lot of changes." Walker's framing is sharper. A **game brief** says what the player does, what success looks like, what can go wrong, and what is out of scope. A **GDD** develops those decisions until an engineer can implement them and a tester can check them (Walker, `docs/zelda-gdd-workflow.md`). Two rules from the Walker skill's persona matter more than any section heading: separate "source observation, proposed design, approved design, implemented behavior, and verified behavior," and remember that "producing a GDD is not producing a game, and a newer GDD does not validate an older build."

### Where Zelda came from

Walker's GDD skill speaks as **Zelda**, a senior-designer persona. It is an adaptation of **Forge**, the GDD prompt set this course used in Spring 2026 (`forge_gdd_prompt_set.md` in the old Canvas export). Forge's command table survives almost intact: `v1`–`v4` for vision, `s1`–`s4` for systems, `w1`–`w3` for world, `p1`–`p5` for scope, `g1`–`g4` to compile and review. Walker added five commands: `reverse`, `draft`, `deck`, `film`, and `status`. Three Forge ideas are worth carrying in your head.

**Sixteen sections.** Metadata, vision summary, pillars, core loop, player-experience (PX) goals, mechanics, systems, progression, world, narrative, characters, feature list, out of scope, technical requirements, risks, and open questions.

**Stable IDs.** Every PX goal, mechanic, system, feature, risk, and test gets an ID (`PX-01`, `M-01`, `S-01`, `F-01`, `R-01`, `T-01`) so a ticket, a test, and a playtest note can point at the same thing.

**Seven failure modes.** Forge's critique command audits a GDD for the Ghost Center (no locked vision), the Mechanic Mirage (PX goals that are feature descriptions in disguise), the Implementation Void (mechanics with only a happy path), Priority Inflation (more than 40% of features tagged CORE), the Novelist's Trap (story written for a reader, not an engineer), the Completeness Fallacy (decisions with no recorded reasoning), and the Stagnant Artifact (no version history, never revised after a prototype).

### Gates, and who signs them

The skill divides design into four phases and puts a gate after each: vision, systems, world, scope. The gates live in `design/DESIGN-STATUS.json` with a name, date, and revision for each. The persona is explicit: "Zelda asks the question; a human answers; Zelda records the answer. Zelda never signs a gate herself." The `silent` flag skips the questions and the gates for one call and records "gate — unsigned at time of writing" in the output. That is useful for a rough draft. It is not approval.

### Provenance tags

When `/gdd reverse` recovers a design from code, every claim gets one of three tags (Walker, `gdd/commands/reverse.md`):

| Tag | Meaning | Example from the 3D platformer |
|---|---|---|
| `[OBSERVED path:line]` | The code does this | Falling below y = −12 resets the player (`player.gd:36`) |
| `[INFERRED]` | The code strongly implies this; state the evidence | Coin clusters suggest intended routes |
| `[MISSING]` | The code cannot tell you this | The target player; the win condition |

`/gdd draft` adds a fourth, `[ASSUMPTION]`, for a gap Zelda filled to make the draft whole. The spec's own warnings are the ones to remember: "Sprites do not prove a mechanic; a script without a scene does not prove a working feature; a TODO is not a design decision." Numbers found in code are observed tuning, "not approved design." A tag is a claim about evidence. It is not evidence. The only way to know an `[OBSERVED]` tag is right is to open the cited line.

### Acceptance criteria that a machine can check

A requirement is testable when a stranger could write the test without asking you anything. For a 3D interaction, that means naming:

- **The quantity and its unit.** Godot's 3D units are metres: "1 unit being equal to 1 meter," and physics is calibrated for that ([Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)).
- **A tolerance.** "Returns to the pad" is not checkable; "within 0.2 m of the respawn point" is.
- **A time box in the engine's clock.** "Within 600 frames at `--fixed-fps 60`," not "quickly." Read Chapter 0's "The time trap: frames are not seconds" before you write any frame count.
- **How the state is reached.** By ordinary input (`Input.action_press`), or by a constructed fixture that writes game state directly. Both are legitimate. They prove different things, and the criterion must say which.
- **What must not change.** The existing checks that must still pass.
- **What is out of scope.** The judgments only a person can make.

The clawd GDD's proposed tests show the same idea as a table: an ID, a setup, an action, an expected result, and the mechanic it links to (`T-20 | level with tasks A,B | touch B first | ledger unchanged, HUD "Do A first" | M-05`).

### The 3D machinery you need for this interaction

**Coordinates.** Godot 3D is right-handed with Y up ([Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)). A `Node3D` stores its transform relative to its parent, so a position inside a `.tscn` is local; you add the parent's offset to get world space. The platformer's coins and enemies sit under parents offset by (−16, −6, −12), which is how a coin written at (18.5, 2.35, 5.25) ends up near (2.5, −3.65, −6.75) in the world.

**The player body.** A `CharacterBody3D`, moved in `_physics_process` with `move_and_slide()`, exactly like the 2D body in Chapter 1 ([Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)). This project runs physics at **120 ticks per second**, uses **Jolt** as its 3D physics engine, and sets gravity to 22 m/s² (`project.godot` lines 149–151). Jolt became the default 3D engine for new projects in Godot 4.6 ([Godot 4.6 release](https://godotengine.org/releases/4.6/)); this project selects it explicitly. At `--fixed-fps 60`, each rendered frame therefore carries two physics ticks.

**Areas and signals.** An `Area3D` detects bodies. Its `body_entered` signal is "emitted when the received body enters this area," and it requires `monitoring` to be on ([Area3D](https://docs.godotengine.org/en/stable/classes/class_area3d.html)). Signals are Godot's observer pattern: a script declares `signal activated`, calls `activated.emit()`, and anything connected to it runs ([Using signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html)). Connections can be made in code with `connect()` or saved in the scene file. The coin in this project is the second kind: `coin.gd` defines `_on_coin_body_enter` and never connects it; the connection is line 266 of `coin/coin.tscn`, `[connection signal="body_entered" from="." to="." method="_on_coin_body_enter"]`. An agent that reads only `.gd` files will think that handler is dead code.

**Layers.** Every body and area in this project uses the defaults, collision layer 1 and mask 1, so a new `Area3D` with default settings will see the player. Remember Chapter 1's rule: in code, layer *n* is the bitmask value 2^(n−1).

**Instancing.** A scene can contain instances of other scenes. In the text file that is an `ext_resource` line pointing at the `.tscn` (by path and, when the editor saves it, by `uid`) and a `[node ... instance=ExtResource("id")]` line ([TSCN format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)). Scenes saved by Godot 4.7 also carry a `unique_id` on every node. Hand-editing these lines is what the syllabus calls the "dangerous middle": resource paths, UIDs, and scene references that parse cleanly and point at the wrong thing.

**Markers.** A `Marker3D` is "a generic 3D position hint for editing," just a `Node3D` drawn as a cross in the editor ([Marker3D](https://docs.godotengine.org/en/stable/classes/class_marker3d.html)). It is the natural way to mark a respawn point.

**Teleporting under interpolation.** This project turns on physics interpolation, which smooths rendering between physics ticks. When code moves an object to a new place, the docs say it is "the responsibility of the user to call `reset_physics_interpolation()`" to avoid a streak ([Physics interpolation](https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/using_physics_interpolation.html)). The existing reset code in `player.gd` already does this; a checkpoint must reuse that path, not write a second teleport.

### Scoping mobile, networked, and XR versions of a world

The syllabus asks you to scope these in Week 5, not build them. Scoping means the GDD's technical section says what each target needs, what you can verify with the hardware you have, and what stays unverified. Godot's documentation sets the floor:

- **Mobile.** Touch arrives as `InputEventScreenTouch` and `InputEventScreenDrag`; Project Settings can emulate touch from the mouse for desktop testing ([Input examples](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html)). An Android export needs OpenJDK 17 and specific Android SDK components ([Exporting for Android](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)), and any command-line export needs export templates installed ([Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)). Mouse-emulated touch is not a phone.
- **Networked.** Godot's high-level multiplayer runs through the `MultiplayerAPI`, with ENet as the default peer; it "only uses UDP," so internet play needs port forwarding, and the docs advise treating all client input as untrusted ([High-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)). WebRTC is built into web exports but needs a separate GDExtension on native platforms ([WebRTC](https://docs.godotengine.org/en/stable/tutorials/networking/webrtc.html)).
- **XR.** OpenXR is "a core interface", enabled in Project Settings; a scene needs an `XROrigin3D` with an `XRCamera3D` and usually two `XRController3D` nodes; the Mobile renderer is recommended for both desktop VR and standalone headsets; and initialization can fail for reasons that "differ from platform to platform" ([Setting up XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html)).

A scoping paragraph in a GDD is honest when every sentence in it is either a requirement, a verified fact about your build, or a named unverified item. The next section shows what that looks like in real builds.

## The Walker example: /gdd, walker-jumpman-clawd/design, and walker-3d-platformer

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-3d-platformer`](https://github.com/nikbearbrown/walker-3d-platformer), [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-mobile-multitouch-cubes`](https://github.com/nikbearbrown/walker-mobile-multitouch-cubes), [`walker-mobile-sensors`](https://github.com/nikbearbrown/walker-mobile-sensors), [`walker-networking-multiplayer-bomber`](https://github.com/nikbearbrown/walker-networking-multiplayer-bomber), [`walker-networking-webrtc-minimal`](https://github.com/nikbearbrown/walker-networking-webrtc-minimal), [`walker-xr-mobile-vr-interface-demo`](https://github.com/nikbearbrown/walker-xr-mobile-vr-interface-demo), [`walker-xr-openxr-character-centric-movement`](https://github.com/nikbearbrown/walker-xr-openxr-character-centric-movement), [`walker-viewport-3d-scaling`](https://github.com/nikbearbrown/walker-viewport-3d-scaling). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

### The `/gdd` skill

The skill lives in the Walker framework at `gdd/`: a `SKILL.md` entry point, `persona.md` (Zelda), `commands.yaml` (the registry: 30 design commands, 5 Walker additions, 3 navigation commands; the 30 are Forge's 20 numbered commands above and its 8 refinement tools such as `logline` and `uiux`, plus `tasks` and `edu`, which the Forge prompt set does not contain), one spec per command in `commands/`, and `templates/` for a fresh `design/` folder. `SKILL.md` contains tokens such as `${GDD_SKILL_COMMAND}` and `${GDD_SKILL_DIR}` that are filled in at install time. When it runs, the skill writes only into `design/`: `GAME-BRIEF.md`, `sections/`, `GDD.md`, `IMPLEMENTATION-MAP.md`, `decisions.md`, `DESIGN-STATUS.json`, `CHANGELOG.md`, `reviews/`, `DECK.html`, and `diagrams/*.svg`. Gate enforcement is, in the workflow document's words, "a convention the skill follows, not code that enforces it."

**Where to get it.** As of September 27, 2026, the `gdd/` folder and the `publish.sh` that installs it exist only in the instructor's local Walker working copy (dated September 18). The public repository's `main` (commit `10fedb8`, September 11) predates them: its `publish.sh` installs only `asset-gen`, and its workflow document still calls `/gdd` a specification. Until the skill is published you cannot clone it; the example record lists SHA-256 hashes of the exact files we ran. The public version's `prompts/zelda-gdd.md` can be handed to an agent as plain instructions in the meantime, but it installs no `/gdd` command and has no `reverse` spec.

**How it gets into a project.** The working-copy `publish.sh --engine godot --agent claude --out <dir>` copies both skills into `<dir>/.claude/skills/`, fills the tokens with `scripts/render_dir.py`, writes `<dir>/CLAUDE.md` and `<dir>/godot.md`, writes a `.gitignore` if none exists, and runs `git init`; with `--agent codex` it uses `.agents/skills/` and `AGENTS.md` and generates each skill's `agents/openai.yaml`. Read it before running it on an existing project: it overwrites an existing `CLAUDE.md` or `AGENTS.md` without asking, its engine guide is the C#/.NET one, and its default `.gitignore` excludes `assets` and `*.import`, where Godot only asks you to exclude `.godot/` ([Version control](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html)). For an existing GDScript game, installing only the `gdd` skill, as the hands-on does, is the smaller and safer change.

**One mismatch to know about.** The skill's frontmatter says `allow_implicit_invocation: false`. That is a Codex setting: in `agents/openai.yaml`, "when false, Codex won't implicitly invoke the skill" ([Codex skills](https://learn.chatgpt.com/docs/build-skills)). Claude Code does not know the field, and its docs say "unknown frontmatter fields are silently ignored" ([Claude Code skills](https://code.claude.com/docs/en/skills)). In Claude Code, therefore, the model may load `/gdd` on its own when your request sounds like design work. The Claude Code equivalent is `disable-model-invocation: true`.

### A recovered GDD in the course's own example: walker-jumpman-clawd/design

On September 18, 2026, I gave the GDD skill a new concept for my semester example: Clawd, a coding agent, runs every level as an agentic loop of tasks, and the obstacles are bugs, malware, and vague instructions. The skill ran `reverse` and then a `draft` overlay, silently, producing `design/` version 0.3.0-draft. Its brief separates an `[OBSERVED]` account of the game that exists (25 mechanics checks, 9 keyboard checks, 162 animation samples, zero human playtests) from an `[ASSUMPTION]` section for everything proposed. It tags 8 of 15 features CORE (53%), fails to re-prioritize under 40% without removing the loop, and logs the choice as open question Q-04 for me rather than deciding. Its proposed tests (`T-20` to `T-25`) each name a setup, an action, and an expected result.

It also contains a confident error. Decision D-02 says the layer names in `project.godot` ("4 Hazard, 5 Goal") "do not match code (8, 16)" and marks the fix "Decided, not applied." They do match: layer 4 is the bitmask value 8 and layer 5 is 16 ([Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html)). Applying D-02 would break correct names. The same map lists layer 4 as "unused in code." A recovered GDD can be wrong in exactly the places that look most technical.

I pushed this `design/` folder to the public `walker-jumpman-clawd` on September 27, 2026 (commit `ce011ca`), after the chapter's runs at `382f2ba`, which carried only the starter GDD.

### The 3D build: walker-3d-platformer

**What it is.** Godot's official 3D Platformer demo, adapted for Walker. A blue robot moves through a GridMap level, jumps, collects coins, and shoots patrolling robots. The camera follows and swings away from walls. The adaptation changed exactly one line, `config/name` in `project.godot` (we diffed it against the upstream checkout). The source is `3d/platformer` in `github.com/godotengine/godot-demo-projects` at commit `a3b5c113112f77291d5f3d1360f33a882fdc52f7`, under the Godot contributors' MIT license; the upstream README credits the virtual joystick add-on to Marco F. The Walker adaptation is public at [github.com/nikbearbrown/walker-3d-platformer](https://github.com/nikbearbrown/walker-3d-platformer); the upstream folder is where it came from and remains a valid starting point.

**What its checks establish.** Two scripted-input probes, both of which we reran on September 27 with `--fixed-fps 60`:

- `tests/input_probe.gd` drives the game for 600 frames with ordinary actions and reports four checks: movement, jump, projectile created, and reset. All four passed (exit code 0).
- `tests/feature_route.gd` steers toward the nearest coin using the camera's axes, jumps and shoots on a schedule, and records coins and enemy states for 1,800 frames. It reported `coins=2 enemy_hit=true` (exit code 0).

The project's `FRICTIONAL.md` also records a normal-input route to a secret area and measured jump rises of 1.53 m and 3.60 m from a separate comparison test.

**What remains unverified.** Everything visual and audible, physical touch and gamepad input, and any human judgment. The project's GDD says so directly: "There is no inspected top-level game script establishing a scored win/ending; do not invent one."

### The mobile, network, XR, and viewport builds: what is verified

The demo-series ledger (`walker-demo-series/queue.json`) tracks these adaptations. Their READMEs are models of honest scoping:

| Build | Verified headless | Explicitly unverified |
|---|---|---|
| `walker-mobile-multitouch-cubes` | Synthetic screen-touch events drive pinch and rotate; 24 numeric checks | Any physical device; rendered output |
| `walker-mobile-sensors` | 17 assertions that the game falls back cleanly when sensors are absent | "Desktop zero readings are not proof that mobile sensors work" |
| `walker-networking-multiplayer-bomber` | Two real ENet processes on loopback: registration, movement, replicated bombs, scoring, disconnects | A full played victory, packet loss, anything beyond loopback |
| `walker-networking-webrtc-minimal` | Import only | Runtime blocked: no WebRTC GDExtension installed |
| `walker-xr-mobile-vr-interface-demo` | Native mobile XR interface initializes; arrow keys move the origin | Stereo pixels, lens distortion, head tracking; the mobile main scene it names does not exist |
| `walker-xr-openxr-character-centric-movement` | Import only | OpenXR initialization fails: "HMD not detected or required feature unsupported" |
| `walker-viewport-3d-scaling` | 37 input and state checks of scaling settings | GPU quality and performance |

The pattern is the lesson. Each build says what a headless run established, names the hardware it lacked, and refuses to simulate it. When your GDD's technical section scopes an XR or mobile version, write it this way.

## Hands-on: recover the design, then specify and build one 3D interaction

Three steps: recover and audit a GDD, write one acceptance criterion, and have the agent build and test it. You will work in your own copy with Git, one commit per step.

### Predict

Answer before you run anything, and keep the answers.

1. The reverse pass will tag most claims `[OBSERVED]`. Pick two it is likely to get wrong and say why: input bindings stored as integers in `project.godot`, line numbers, positions in world versus local space, or claims copied from Markdown files rather than code.
2. `input_probe.gd` checks reset by comparing the player's position with where it started. If your checkpoint pad sits on the path the probe walks, what happens to that check, and is that a bug in the pad or in the probe?
3. Criterion 5 below places the player below y = −12 directly. What does that prove that an input-only test cannot, and what does it fail to prove?
4. Where will the hard part of this task be: the code in `player.gd`, the placement of the pad, or the edit to `game.tscn`?

### Build It

**Get the project.** The upstream repository is large (the full checkout with history is close to 900 MB on disk). A partial clone of just the folder you need keeps it small. We did not run these three commands for this chapter; we used an existing checkout at the same commit.

```bash
git clone --filter=blob:none --sparse https://github.com/godotengine/godot-demo-projects.git
```

```bash
git -C godot-demo-projects sparse-checkout set 3d/platformer
```

```bash
git -C godot-demo-projects checkout a3b5c113112f77291d5f3d1360f33a882fdc52f7
```

Make your own project from it, with the Godot project in `godot/` and room for tests beside it.

```bash
mkdir -p walker-3d-platformer/tests
```

```bash
cp -R godot-demo-projects/3d/platformer walker-3d-platformer/godot
```

```bash
cd walker-3d-platformer
```

Copy the two probes from this book's example record (`examples/05-the-gdd-and-virtual-worlds/tests/input_probe.gd` and `feature_route.gd`) into `tests/`. Keep Godot's cache and the test reports out of Git, then commit a baseline.

```bash
git init
```

```bash
printf '.godot/\nevidence/\n' > .gitignore
```

```bash
git add -A
```

```bash
git commit -m "Baseline: godot-demo-projects 3d/platformer at a3b5c11"
```

Import the assets headless (this project has models, textures, and sounds, so it must be imported once before scripts can load them), then run both probes. The probes take a fresh report path after `--` and refuse to overwrite one. `timeout 120` stops a test that hits a script error before `quit()`, which would otherwise leave headless Godot running (Chapter 1 explains).

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

Expect `{"jump":true,"movement":true,"projectile_created":true,"reset_action":true}` from the first and `coins=2 enemy_hit=true` from the second. Leak warnings may print at exit; they do not change the exit code, which should be 0 for both.

**Install the GDD skill.** Copy only the `gdd` folder from the Walker framework and fill in its tokens the way `publish.sh` would. Here `../walker` is a Walker copy that contains `gdd/` (see "Where to get it" above; the September 11 public version does not).

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

The last command should print nothing: every token was replaced. Commit the skill on its own so the design work diffs cleanly.

```bash
git add .claude && git commit -m "Install Walker gdd skill"
```

For Codex, the folder is `.agents/skills/gdd`, the command token is `$gdd`, and Codex also wants the generated metadata. We did not run the Codex install for this chapter.

```bash
python3 ../walker/scripts/generate_codex_metadata.py .agents/skills
```

**Prompt 1: recover the design.** Make a folder for prompts and transcripts first (`mkdir -p notes`). In Claude Code, the whole prompt is the slash command. `silent` skips Zelda's questions and gates for this one call.

```text
/gdd reverse --path godot silent
```

Headless, with a transcript:

```bash
claude -p "/gdd reverse --path godot silent" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose < /dev/null > notes/session-1-reverse.jsonl
```

In Codex the command is `$gdd reverse --path godot silent`, run with `--sandbox workspace-write` (we did not run the reverse pass under Codex). Expect this to take a while; ours took twenty minutes. Commit the result as agent output, unreviewed.

```bash
git add design && git commit -m "gdd reverse (silent): agent output, unreviewed"
```

**Audit it.** This is the part that is yours. Open `design/GDD.md` and `design/IMPLEMENTATION-MAP.md` and check at least these, writing each finding in your FRICTIONAL log:

1. Every input binding. `project.godot` stores keys as integers; ask Godot what they are rather than guessing (`OS.get_keycode_string(4194326)` in a one-line `SceneTree` script prints `Ctrl`).
2. Five `[OBSERVED path:line]` tags chosen at random. Open the line.
3. Every number attributed to a file under `evidence/`. Did the agent open that file? The transcript tells you.
4. Every "not found" or `[MISSING]` claim about an asset or feature. One `grep` often settles it.
5. Every place the document says "tested" or "verified." Which test, and does it exist?
6. Whether `DESIGN-STATUS.json` shows all four gates unsigned. It should. Do not sign them to make the document look finished.

**Write the acceptance criterion.** Now write one criterion for a small new interaction, in your own words, before any agent touches the code. Ours is a checkpoint pad: when the player walks onto it, the reset action and falling off the map both return the player to the pad instead of the level start. The full text is `examples/05-the-gdd-and-virtual-worlds/AC-01-checkpoint-pad.md`; its six checks, in metres and in frames at `--fixed-fps 60` (two physics ticks each here), are:

| # | Criterion | How it is reached |
|---|---|---|
| 1 | An `Area3D` pad with a footprint of at least 1.5 m × 1.5 m rests on walkable floor 3–6 m from the start, off the straight path `input_probe.gd` walks | Observation of the scene |
| 2 | Before activation, holding `reset_position` for 5 frames leaves the player within 0.2 m of the start | Input only |
| 3 | The player reaches the pad within 600 frames; it activates exactly once, and re-entering does not activate it again | Input only (`Input.action_press`/`action_release`) |
| 4 | After activation, holding `reset_position` for 5 frames leaves the player within 0.2 m of the pad's respawn point | Input only |
| 5 | After activation, placing the player below y = −12 returns it within 0.2 m of the respawn point within 2 frames | Constructed fixture, labelled: a direct state write that tests the fall branch, not a fall a player makes |
| 6 | `input_probe.gd` still reports all four checks true and `feature_route.gd` still collects a coin; both exit 0 | The existing probes |

Out of scope, and said so in the file: whether a player can see the pad and understands it, its look and sound, touch, gamepad, and any export.

```bash
git add design/AC-01-checkpoint-pad.md && git commit -m "AC-01 checkpoint pad: human-authored acceptance criterion"
```

**Prompt 2: build it and test it.** This prompt names the one concern, the invariants, the files the agent may touch, and the exact commands, and it tells the agent what to do if the criterion cannot be met. It refers to sections M-05 and 06b of our recovered GDD; use the section numbers from yours.

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

Headless, saved as `notes/prompt-2-implement.txt`:

```bash
claude -p "$(cat notes/prompt-2-implement.txt)" --permission-mode acceptEdits --allowedTools "Read,Write,Edit,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 80 --output-format stream-json --verbose < /dev/null > notes/session-2-implement.jsonl
```

Two practical notes. First, Claude Code declines to auto-approve an allowed command that contains a shell expansion such as `$PWD`; in a prompt for Claude Code, write the absolute path instead (the prompt above is printed exactly as we ran it, `$PWD` included, and the agent had to reword one command). Second, an agent can stop partway: ours did, when the shared account hit its usage limit. Do not start over. Hand the working tree to a fresh session, or the other CLI, with the same task and a preface that tells it to review the partial work before continuing:

```text
A previous agent session (Claude Code) was stopped by an account usage
limit partway through the task below, before it ran any test. Its partial
work is in the working tree: see git status and git diff. Review that
partial work critically against design/AC-01-checkpoint-pad.md, keep or
change it, and finish the task. The task, exactly as it was given:
```

followed by the full Prompt 2. We ran that under Codex:

```bash
codex exec --sandbox workspace-write --json -o notes/codex-continue.md "$(cat notes/prompt-3-continue.txt)" < /dev/null > notes/session-3-codex.jsonl
```

Notice what the allow-list leaves out: no `python3`, no `rm`, no general shell. In our run the agent tried `python3` five times to read a JSON report, was refused each time, and switched to reading the file with its Read tool. The allow-list shaped the method without blocking the task. Do not add `Bash(env *)` or similar wrappers to an allow-list: a command that runs other commands allows everything.

### Use It

This needs the editor and a display; we did not do it. Open `godot/project.godot` in the regular Godot editor.

1. Open `game.tscn` and find the pad in the Scene dock. Does its mesh sit on the floor, or float or sink? Where does the respawn point end up, and can you see it anywhere in the editor?
2. Press Run. Walk onto the pad. Can you tell it activated? If nothing visible changes, that is a design gap your criterion did not cover; write it down as an open question, not a failure of the build.
3. Press R. Then walk off an edge. Watch the camera when you respawn: does it snap cleanly, or sweep from the old position?
4. Play for five minutes as someone who has never seen the pad. Would they notice it?

### Ship It

Commit the implementation on its own, with the criterion ID in the message, and record the evidence files. Then add a changelog entry with the skill, rather than editing the GDD by hand.

```bash
git add -A && git commit -m "AC-01 checkpoint pad: implementation and test_checkpoint.gd"
```

```text
/gdd changelog
```

In `FRICTIONAL.md`, record the audit findings from Prompt 1 as well as the build: which tags were wrong, how you found out, and what you changed. Do not sign any gate in `DESIGN-STATUS.json`; you have not reviewed the vision, and a recovered document "is not an approval of any of it." If you make a film, the matching Brutalist skill is **godot-gdd**, which explains the design using game evidence and keeps proposed, built, tested, and human-reviewed claims separate.

### Verify

Run all three tests yourself. Do not rely on the agent's report.

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

Then read the test, not just its output. Check that criteria 2 to 4 really use only `Input.action_press` and `action_release`, that criterion 5 is labelled as a fixture, and what each distance is measured against. If it is measured against a value the implementation computed for itself, your criterion has a gap (ours did; see below).

A pass proves that, at Godot 4.7.2 with a pinned time step, ordinary input reaches the pad, the pad moves the respawn point, and the old probes still pass. It does not prove the pad is visible, understandable, fair, or worth having.

## What we actually ran

**When and with what.** September 27, 2026, macOS on an Apple M4 Pro. Godot `4.7.2.stable.official.ed1daf0bf`. Claude Code 2.1.150 (the transcripts record `claude-sonnet-4-6`, the account default). Codex CLI 0.153.4 with the local config's model (`gpt-5.6-sol`, reasoning effort low). The project was a scratch copy of `walker-3d-platformer` (its `godot/` folder, Markdown files, and the two probes), committed as a local baseline. The full record, with trimmed transcripts, is in [`../examples/05-the-gdd-and-virtual-worlds/`](../examples/05-the-gdd-and-virtual-worlds/).

**Baseline.** Import exited 0; `input_probe.gd` reported all four checks true; `feature_route.gd` reported `coins=2 enemy_hit=true`. Both exited 0 after printing shutdown leak warnings.

**Skill install.** We copied `walker/gdd` into `.claude/skills/gdd` and ran `render_dir.py` with `publish.sh`'s values for Claude; no `${...}` token remained. A one-turn `/gdd status` confirmed that Claude Code loaded the skill in `-p` mode.

**Prompt 1, `/gdd reverse --path godot silent`.** 48 turns, 20 min 10 s. The agent read the skill files, all eight scripts, `game.tscn`, `project.godot`, and the Markdown files; one command (`find ... -exec grep`) was refused as not read-only. It wrote `design/GDD.md` (4,777 words; 107 `[OBSERVED]`, 29 `[INFERRED]`, 30 `[MISSING]` tags), `IMPLEMENTATION-MAP.md`, `decisions.md` (10 open questions), `DESIGN-STATUS.json` (mode `recovered`, all gates unsigned), a 16-slide `DECK.html`, and four SVG diagrams. Much of it is right: the 73 coins, the eight scripts and scenes, the fall threshold, the sharp-turn rule, the missing win condition, the unverified touch hardware, and the observation that enemies cannot hurt the player.

**Our audit.** Nine claims were wrong or unsupported:

| Claim in the recovered GDD | What is true | How we checked |
|---|---|---|
| Shoot is bound to F9 | Physical keycode 4194326 is **Ctrl** | `OS.get_keycode_string(4194326)` printed `Ctrl`; `KEY_F9` is 4194340 |
| Shoot also on "Gamepad L3" | Joypad button 10 is the **right shoulder** | `JOY_BUTTON_RIGHT_SHOULDER` = 10; the left stick is 7 |
| Jump rises 1.53 m and 3.60 m, `[OBSERVED evidence/baseline-probe.json]` | The agent listed that file but never opened it; the numbers are in `FRICTIONAL.md`, from another test | The transcript's tool calls |
| "No skybox ... observed in source" | `stage/skybox.gdshader` and `stage/skybox.webp` exist | `ls godot/stage` |
| `SoundWalkLoop` is an enemy animation clip | It is an `AudioStreamPlayer` | `enemy.gd`, `enemy.tscn` |
| Gravity at `project.godot:153` | Line 151 | `grep -n` |
| `particle_material.tres` usage "untraced" | `enemy.tscn` references it | One `grep` |
| CORE percentage 69% tagged `[OBSERVED]` | Priority is Zelda's judgment, not an observation | The `reverse` spec's definition of the tag |
| "11 CORE features observed and test-verified" (chat summary) | Only movement, jump, projectile, reset, coins, and one enemy hit have any headless check | The two probes |

The GDD also links `design/diagrams/level-flow.svg`, which was never written. Integers in a config file, a file cited but never opened, a folder not listed: an agent writing fluently in the right format produces exactly these, and a tag makes them look checked.

**The criterion and a prediction.** We wrote AC-01 (the agent drafting this chapter, standing in for a student) and committed it before any implementation, with a timestamped prediction (`author-prediction.md`): the code would be easy and placement hard, 50% that the first test would fail to reach the pad, 30% that the pad would land on the probe's path.

**Prompt 2 under Claude Code: interrupted.** The agent read the criterion, the GDD, `player.gd`, the probes, and `game.tscn`. It tried five times to parse the baseline report with `python3`, was refused each time by the allow-list, and read the file with its Read tool instead, learning that the probe walks +X from x = −9.50 to −4.72; it placed the pad 4 m in +Z. Our `$PWD` caused one more refusal and a reworded command. It wrote a floor probe, the pad scene and script, the two-line `player.gd` change, the `game.tscn` edit, and a 297-line test; imported; found the floor under the pad at y = −6.0 rather than the −5.0 it had guessed; and moved the pad. Then, after 43 turns and 23 min 26 s, it stopped: "You've hit your session limit." The shared course account had run out, with several agents working on this book at once. No test had run.

**Prompt 3 under Codex: review and finish.** Codex (2 min 51 s, `workspace-write` sandbox) read the partial work, imported (Godot could not save its editor settings outside the sandbox, which did not change the exit code), ran the partial test, which passed, and made three changes: it cut the trigger box from 0.6 m to 0.2 m tall to match the visible mesh, rewrote criterion 1 to confirm that the pad's bottom meets the floor, and strengthened criterion 3 to prove the player really leaves and re-enters the pad. That stronger check failed once, because its own route stopped two metres short of leaving the pad; it fixed the route and reran. Both probes passed.

Codex described its criterion-1 change as fixing a false positive: the partial test's ray, it said, "was raycasting against the pad itself." We checked. A `PhysicsRayQueryParameters3D` ignores areas by default; the same ray against the finished scene hit the GridMap at y = −6.0, and hit the pad only with `collide_with_areas = true` (`audit/ray_default.gd`). The old check was weaker than it should have been, but not for that reason. The second agent improved the test and misdescribed the bug.

**Our verification.** We ran all four commands ourselves:

```text
{"criterion":1,"dist_from_start_m":4.0,"floor_y":-6.0,"footprint_xz":[1.5,1.5],"off_probe_path":true,"pad_bottom_y":-6.0,"pass":true, ...}
{"criterion":2,"dist_from_start_m":0.0015,"pass":true,"threshold_m":0.2}
{"activation_count_after_reentry":1,"criterion":3,"exited_pad":true,"reached_in_frames":64,"reentered_pad":true,"pass":true, ...}
{"criterion":4,"dist_from_pad_respawn_m":0.0882,"pad_respawn_point":[-9.498,-5.91,7.933],"pass":true,"threshold_m":0.2}
{"criterion":5,"dist_from_pad_respawn_m":0.0898,"label":"constructed_fixture_fall_branch","pass":true, ...}
{"criterion":6,"dist_from_start_after_reset_m":0.0015,"label":"regression_reset_before_pad_activation","pass":true, ...}
{"jump":true,"movement":true,"projectile_created":true,"reset_action":true}
coins=2 enemy_hit=true
```

All three scripts exited 0 (our runs were not wrapped in `timeout`; none hung). In the final test, every check but criterion 5 moves the player only with `Input.action_press` and `action_release`; the one direct state write is line 270, inside the labelled fixture. Neither predicted failure happened: the first real run reached the pad in 64 frames, off the probe's path. The prediction that placement would be the hard part held; the agent needed a floor probe and had guessed the floor height wrong.

**What our criterion missed.** Criterion 4 says "within 0.2 m of the pad's respawn point," and the pad computes that point itself, from the player's height at the moment of entry, instead of a marker anyone could inspect. The test compares the player with a number the implementation chose. The value is sensible here (y = −5.91, just above the floor), but the criterion never said where the point must be. A better one names it: "a `Marker3D` child of the pad, no more than 0.2 m above its top surface." That gap was found only by reading the implementation.

**What we did not do.** Open the editor, look at the pad, or play. The pad is a 0.2 m green box that the player walks through, since an `Area3D` is not solid; whether that reads as a pad or as a glitch is a human call.

## Check your understanding (ungraded)

1. Open `coin/coin.gd` and `coin/coin.tscn`. Where is `_on_coin_body_enter` connected, and what would an agent conclude about it if it read only the `.gd` file?
2. In `game.tscn`, the coins' parent node is at (−16, −6, −12). Compute the world position of `Coin4`. Then find one place in our recovered GDD that gives a position, and say whether it is local or world.
3. The clawd GDD's decision D-02 says layer names do not match the code. Using the physics documentation, show why they do. What would have happened if an agent had applied D-02?
4. Rewrite this requirement so a stranger could test it: "The checkpoint should feel responsive and reset the player quickly."
5. Pick one of the XR builds in the scoping table. Write the two sentences you would put in a GDD's technical section about it: one verified fact, one named unverified item.
6. Our recovered GDD tagged its CORE percentage `[OBSERVED]`. Why is that the wrong tag, and which Forge failure mode does a CORE list above 40% signal?

## Doing the same thing in Unity

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation.

### Similarities

A GDD is engine-agnostic, and so is most of this chapter. The acceptance criterion, the provenance tags, the gates, and the scoping table would read the same for a Unity project. The checkpoint itself has a direct Unity form: a collider with `isTrigger` set, whose `OnTriggerEnter` callback fires when a body with a `Rigidbody` enters it, invoked during physics simulation after the `FixedUpdate` calls ([OnTriggerEnter](https://docs.unity3d.com/ScriptReference/Collider.OnTriggerEnter.html)). The respawn point would be an empty GameObject's transform, the counterpart of a `Marker3D` (which, as our run showed, is worth asking for by name). The test would be a Play Mode test in the Unity Test Framework that steps physics with `yield return new WaitForFixedUpdate()` ([UnityTest attribute](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html)) and drives input through the Input System's `InputTestFixture` ([Input testing](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.4/manual/Testing.html)), run headless with `-batchmode -runTests -testPlatform PlayMode` ([Command-line arguments](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)).

The scoping targets have named Unity equivalents: XR Plug-in Management with the OpenXR plug-in ([OpenXR Plugin](https://docs.unity3d.com/Manual/com.unity.xr.openxr.html)), the Device Simulator for previewing mobile layouts and behavior in the Editor ([Device Simulator](https://docs.unity3d.com/Manual/device-simulator.html)), and Netcode for GameObjects for networking GameObject and MonoBehaviour workflows ([Netcode for GameObjects](https://docs.unity3d.com/Manual/com.unity.netcode.gameobjects.html)). The same honesty rule applies: a simulator is not a device.

### Differences

A reverse pass over a Unity project would read C# scripts easily and scenes with more difficulty. Scenes and prefabs are YAML under the default Force Text serialization, with each object as a separate YAML document ([YAML scene example](https://docs.unity3d.com/Manual/YAMLSceneExample.html)), but components refer to scripts and assets through GUIDs stored in `.meta` files ([Asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html)). An agent that wants to know "which script handles the coin" has to resolve a GUID to a file; in Godot it reads `path="res://coin/coin.gd"` directly. Signal-style wiring made in the Inspector (a `UnityEvent`) lives in that YAML too, which is the Unity version of our coin's `[connection]` line: invisible to anyone who reads only the scripts.

Placing the pad is also different work. In Godot the agent added two lines to a `.tscn`. In Unity it would either edit scene YAML by hand, with `fileID` and GUID references to get right, or write an Editor script that places the object through the API and run it with `-executeMethod`. The second is safer and is the pattern to ask an agent for.

| This chapter (Godot) | Unity |
|---|---|
| `Area3D` + `body_entered` | Trigger collider + `OnTriggerEnter` |
| `Marker3D` respawn point | Empty GameObject transform |
| Signal connection in `.tscn` | `UnityEvent` wiring in scene YAML |
| Instance of `checkpoint_pad.tscn` | Prefab instance |
| `--fixed-fps 60` scripted-input probe | Play Mode test with `WaitForFixedUpdate` and `InputTestFixture` |
| OpenXR in Project Settings | XR Plug-in Management + OpenXR plug-in |
| High-level multiplayer (ENet) | Netcode for GameObjects |
| Emulate touch from mouse | Device Simulator |

## Doing the same thing in Unreal Engine

### Similarities

Unreal has the same building blocks under Epic's names. A Trigger Volume "can cause events when a Player or other object enters or exits them," and `OnActorBeginOverlap` fires when another actor begins to overlap, provided both sides have overlap events enabled ([Trigger volumes](https://dev.epicgames.com/documentation/en-us/unreal-engine/trigger-volume-actors-in-unreal-engine), [On Actor Begin Overlap](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Collision/OnActorBeginOverlap)). Respawning belongs to the Game Mode: `RestartPlayer` spawns the player's pawn at the location `FindPlayerStart` returns, and Player Start actors mark those locations ([Player Start](https://dev.epicgames.com/documentation/en-us/unreal-engine/player-start-actor-in-unreal-engine), [Respawning a player character](https://dev.epicgames.com/documentation/en-us/unreal-engine/respawning-a-player-character)). A checkpoint is therefore a trigger that tells the Game Mode which start to use next. The test would be a functional test placed in a level ([Functional testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine)), run unattended through the automation system ([Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)).

For scoping, Unreal documents the same three targets: OpenXR on Windows and Android, for head-mounted devices ([OpenXR in Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-head-mounted-experiences-with-openxr-in-unreal-engine)), and a server-authoritative client-server replication model for multiplayer ([Networking overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine)).

### Differences

A reverse-GDD pass hits a wall in Unreal that it does not hit in Godot. Levels and Blueprint assets are `.umap` and `.uasset` files, which "are binary, so cannot be opened as text or merged in a text-based merge tool" ([Perforce and Unreal](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine?lang=en-US)). An agent can read the C++ classes and the `.ini` configuration, but a mechanic built in Blueprint is invisible to it as text, so most of a recovered GDD for a Blueprint-heavy project would be `[MISSING]` or `[INFERRED]` from names. To recover more, the agent would have to run editor Python inside Unreal (the Python Editor Script Plugin must be enabled) to dump asset properties ([Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)). The implementation has the same shape: a checkpoint written in C++ is agent-editable text, while one built as a Blueprint needs the editor, and its diff is viewed in the editor's diff tool ([UE Diff Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine)). And the functional test itself lives in a level, which is binary.

Unreal's networking is also built in at a different level. Replication is the engine's core model for multiplayer, where Godot's high-level API is something a project opts into with nodes and `@rpc` annotations. Scope accordingly: an Unreal multiplayer GDD section describes what replicates and who has authority from the first draft.

| This chapter (Godot) | Unreal Engine 5 |
|---|---|
| `Area3D` + `body_entered` | Trigger Volume + `OnActorBeginOverlap` |
| `Marker3D` respawn point | Player Start actor |
| Reset code in `player.gd` | Game Mode `RestartPlayer` / `FindPlayerStart` |
| `.tscn` text scene | `.umap` level, binary |
| GDScript | Blueprint graph (binary asset) or C++ |
| Scripted-input probe | Functional test actor in a level |
| OpenXR in Project Settings | OpenXR plugin (Windows and Android) |
| High-level multiplayer | Replication, server-authoritative |

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on September 27, 2026 (Unity manual pages for Unity 6.x; Epic documentation pages for Unreal Engine 5.8).

**Godot (official documentation, stable branch, Godot 4.7)**

- [Introduction to 3D](https://docs.godotengine.org/en/stable/tutorials/3d/introduction_to_3d.html)
- [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.html)
- [Physics introduction (layers and masks)](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html)
- [Area3D class](https://docs.godotengine.org/en/stable/classes/class_area3d.html)
- [Using signals](https://docs.godotengine.org/en/stable/getting_started/step_by_step/signals.html)
- [Marker3D class](https://docs.godotengine.org/en/stable/classes/class_marker3d.html)
- [TSCN file format](https://docs.godotengine.org/en/stable/engine_details/file_formats/tscn.html)
- [Using physics interpolation](https://docs.godotengine.org/en/stable/tutorials/physics/interpolation/using_physics_interpolation.html)
- [Godot 4.6 release notes (Jolt default for new 3D projects)](https://godotengine.org/releases/4.6/)
- [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [Input examples (touch, emulate touch from mouse)](https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html)
- [Exporting for Android](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)
- [High-level multiplayer](https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html)
- [WebRTC](https://docs.godotengine.org/en/stable/tutorials/networking/webrtc.html)
- [Setting up XR](https://docs.godotengine.org/en/stable/tutorials/xr/setting_up_xr.html)
- [Version control systems](https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html)

**Coding agents**

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Codex skills (`.agents/skills`, `$skill`, `openai.yaml`)](https://learn.chatgpt.com/docs/build-skills)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode.md)

**Walker and the example projects**

- [Walker framework](https://github.com/nikbearbrown/walker), public `main` at `10fedb8` (September 11, 2026), and the instructor's local working copy of September 18 (not yet published as of September 27), which adds `gdd/SKILL.md`, `gdd/persona.md`, `gdd/commands.yaml`, `gdd/commands/reverse.md`, `gdd/commands/draft.md`, the updated `publish.sh`, and the updated `docs/zelda-gdd-workflow.md`; `scripts/render_dir.py` and `scripts/generate_codex_metadata.py` are in both
- Forge GDD prompt set (Spring 2026 course export, `forge_gdd_prompt_set.md`): the sixteen sections and seven failure modes
- `walker-jumpman-clawd/design/` (version 0.3.0-draft, 2026-09-18; pushed to the public repository on 2026-09-27, commit `ce011ca`)
- [godot-demo-projects `3d/platformer` at `a3b5c11`](https://github.com/godotengine/godot-demo-projects/tree/a3b5c113112f77291d5f3d1360f33a882fdc52f7/3d/platformer) (MIT)
- `walker-3d-platformer` (public adaptation: `GDD.md`, `FRICTIONAL.md`, `tests/input_probe.gd`, `tests/feature_route.gd`)
- READMEs and verification notes of `walker-mobile-*`, `walker-networking-*`, `walker-xr-*`, `walker-viewport-*`, and the ledger `walker-demo-series/queue.json`
- This chapter's run: [`examples/05-the-gdd-and-virtual-worlds/`](../examples/05-the-gdd-and-virtual-worlds/)

**Unity (official documentation)**

- [Collider.OnTriggerEnter](https://docs.unity3d.com/ScriptReference/Collider.OnTriggerEnter.html)
- [Test Framework: UnityTest attribute](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-attribute-unitytest.html)
- [Test Framework: command-line arguments](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)
- [Input System: input testing](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.4/manual/Testing.html)
- [An example of a YAML scene file](https://docs.unity3d.com/Manual/YAMLSceneExample.html)
- [Asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html)
- [OpenXR Plugin](https://docs.unity3d.com/Manual/com.unity.xr.openxr.html)
- [Device Simulator](https://docs.unity3d.com/Manual/device-simulator.html)
- [Netcode for GameObjects](https://docs.unity3d.com/Manual/com.unity.netcode.gameobjects.html)
- [UnityEvents](https://docs.unity3d.com/Manual/unity-events.html)

**Unreal Engine (official documentation)**

- [Trigger Volume actors](https://dev.epicgames.com/documentation/en-us/unreal-engine/trigger-volume-actors-in-unreal-engine)
- [On Actor Begin Overlap](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/Collision/OnActorBeginOverlap)
- [Player Start actor](https://dev.epicgames.com/documentation/en-us/unreal-engine/player-start-actor-in-unreal-engine)
- [Respawning a player character](https://dev.epicgames.com/documentation/en-us/unreal-engine/respawning-a-player-character)
- [Functional testing](https://dev.epicgames.com/documentation/en-us/unreal-engine/functional-testing-in-unreal-engine)
- [Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)
- [Developing for head-mounted experiences with OpenXR](https://dev.epicgames.com/documentation/en-us/unreal-engine/developing-for-head-mounted-experiences-with-openxr-in-unreal-engine)
- [Networking overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine)
- [Scripting the Unreal Editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)
- [UE Diff Tool](https://dev.epicgames.com/documentation/en-us/unreal-engine/ue-diff-tool-in-unreal-engine)
- [Using Perforce as source control (binary `.uasset`/`.umap`)](https://dev.epicgames.com/documentation/unreal-engine/using-perforce-as-source-control-for-unreal-engine?lang=en-US)
