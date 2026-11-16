# Assignment 10 - Final Project: From Brief to Export

CSYE 7270 · Fall 2026 · **250 points**
Planned due date: Sunday, December 20, 2026, at 11:59 pm America/New_York. See the [Fall 2026 assignment schedule](fall-2026-assignment-schedule.md); Canvas remains the official deadline. The 10% daily late penalty applies.
Required viewing: [AI Policy for Professor Bear's Courses | Using AI Responsibly in Class](https://youtu.be/8Ut0Cdl6vMw).
## Executive summary

This is the final project, worth 250 points. It covers Module 15 and draws on the whole course, including Module 14 through the game-AI technique you built and taught in Assignment 9. You finish the game you have built since Assignment 2 in four steps:
1. Bring your Assignment 9 technique into the finished game, and audit it for a case its tests miss.
2. Add one piece of data that survives a restart, under save rules written first.
3. Add a front door: a start or pause menu.
4. Take Walker's cycle to its last step, so that anyone can reproduce your build from a clean clone of tag a10 and you can say honestly whether it is source-ready or export-ready.
You also hold the finished game to your Assignment 8 pitch. Every item you said would exist is marked delivered, changed or dropped.
You defend the project in two films with the walker modifier:
- godot-walkthrough shows what the finished game does;
- godot-gdd shows why it is specified that way, and names the five Supervisory Capacities with evidence.
It is individual work, graded in the same proportions as every assignment: 150 points for implementation and explanation, 25 for Frictional, 25 for GitHub posting, and 50 (20%) for Relative Quartile. Passing every check shows the build reproduces and its rules hold for the cases tested. It does not show the game is fun, that an export runs where you did not run it, or that a screen reader can use it.
## Your task

Start this project early. It is worth two and a half assignments, and most of it cannot be done in the last week. Read this brief and the Module 15 material with the October 19 GDD milestone. Then work to these targets:

| Preparation target | Work toward the final |
|---|---|
| Assignment 4 GDD — October 19 | Read the final brief; name the core loop, scope, export target and largest uncertainty. |
| Assignment 5 shaders — October 29 | Keep the shaders/materials and their evidence; identify renderer-dependent features. |
| Assignment 6 particles — November 3 | Preserve visual and cost checks; write save rules and attempt an early export. |
| Assignment 7 animation — November 15 | Keep a small playable loop with documented transitions and earlier layers working. |
| Assignment 8 pitch — November 22 | Save the “exists today” and “will exist” lists that the final must reconcile. |
| Assignment 9 teaching technique — December 12 | Preserve the technique, tests and teach/ projects; plan its integration and the audit gap. |
| Assignment 10 final — December 20 | Complete integration, persistence, menu, clean-clone/export evidence, pitch ledger and both films. |

These are preparation targets in the existing project log, not extra graded submissions. See the [release and preparation plan](fall-2026-assignment-schedule.md#release-and-preparation-plan).
Work from these sources, which include their run records:
- the [Module 15 lesson](../modules/15-final-projects-brief-to-export/lesson.md) and the chapter Final Projects: From Brief to Export, with [examples/15-final-projects-brief-to-export](../examples/15-final-projects-brief-to-export/);
- for your game-AI technique, the [Module 14 lesson](../modules/14-game-ai-and-systems/lesson.md), its [labs page](../modules/14-game-ai-and-systems/labs.md), and the chapter Game AI and Systems, with [examples/14-game-ai-and-systems](../examples/14-game-ai-and-systems/).
The sum of the semester. Since Assignment 2 you have built one game in one repository whose name begins walker-, tagged a3 through a9. This assignment adds the last layers to that repository and is submitted as the tag a10. Do not restart.
The finished build must still contain, working together, what earlier assignments added:
- generated art and sound;
- Blender assets from Assignment 3;
- a GDD, and a 3D interaction with the collision or physics behaviour specified in Assignment 4;
- a shader and a material;
- particle effects;
- animation wired to player actions;
- the game-AI technique from Assignment 9.
Assignment 9's teach/ projects stay in the repository and must still pass their checks. If a layer had to be removed or replaced, the README says what and why.
The pitch is a promise. Your Assignment 8 PROJECT-BRIEF.md ends with two lists, exists today and will exist. The finished project is where those lists meet the truth: every "will exist" item is marked delivered, changed or dropped, with its evidence or its reason.
Individual work. This is an individual project. Credit anyone who playtested or gave feedback in SOURCES.md.
Tools and cost. Claude Code through your Northeastern access is expected; no purchase of any kind is required. If a usage limit ends a session, HANDOFF.md lets a later session continue: in Module 14, Codex finished a task from the handoff file Claude Code left. Name every tool in SOURCES.md.
License. License your own contributions under the [MIT License](https://opensource.org/license/mit), or with a copyright statement of your own, in a LICENSE file and the README.
Keep every upstream license. Godot's demos and their Walker adaptations are MIT. walker-jumpman and walker-jumpman-clawd carry no license file, and the latter's SOURCES.md notes that public availability is not a license grant. If you started from either, license only your own additions and say so. Name any asset whose license is unresolved, and do not publish a film that uses it.
### Integrate your Assignment 9 technique

Bring your Assignment 9 technique from its scenario scenes into the finished game, where it does its job in real play.
If you change technique, choose from the table below, justify the choice in CHANGE-BRIEF.md (including why not the others), and meet that row's minimum in the finished game. Either way, the table's last column is what your audit and your own play must look past.
| Option (Module 14) | Minimum in your game | What its tests cannot show |
|---|---|---|
| State-machine or behavior-tree character | At least three behaviors with explicit transitions (or tree priorities), hysteresis where a boundary could flicker, and a read-only state property that tests read instead of internals. | Whether it is fun, fair or readable to play against. |
| Navigation | A character that reaches a far target around obstacles and stops at the closest point for an unreachable one (`NavigationAgent2D`/`3D`, or `AStarGrid2D` on a grid), with no test depending on the frame the first path arrives. | Behavior with other agents, moving obstacles, other maps. |
| Procedural content with a validator | A seeded generator whose output enters your real scene; a validator built from the player's measured limits minus a stated margin; hand-made impossible cases rejected; the same output for a seed on Godot 4.7.2. | That an accepted output can be crossed, or is any good. |
| A learning agent | One decision in your game learned from reward, seeded and repeatable, with its learning curve and its greedy policy evaluated separately from the exploring training rate. | Anything about deep reinforcement learning or continuous state. |
| Scoped two-process networking | Two processes on `127.0.0.1` only, one synchronized state change, one rejected unauthorized change, and a written check of every `any_peer` RPC you declare. | Latency, packet loss, NAT, or a modified client. |

A behaviour-tree addon (LimboAI or Beehave, both MIT) is allowed if you pin its version, credit it, and can explain what it does for you that Module 14's plain GDScript tree did by hand. Godot RL Agents was not run for this course; if you use it, its setup and claims are yours to verify.
### Take the cycle to export

- GDD. Update your Assignment 4 GDD so every feature is labelled proposed, implemented, tested or human decision pending. Use the reusable prompt prompts/zelda-gdd.md from public [Walker](https://github.com/nikbearbrown/walker).
- Persistence. One piece of data survives a restart: a best time, settings, progress. Module 15 saved a personal best in [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) under rules written before any code.
- A front door. A start or pause menu usable by keyboard alone, with focus set when the scene starts.
- Reproduction. A clean clone of tag a10 imports and passes every documented check, including Assignment 9's teach/ projects.
- Export. The export target and its renderer are decided in your brief. A committed export_presets.cfg, an inspected --export-pack, and an export attempt, with the state you claim matching the evidence. A public release is not required.
## 1. Predict

Replace the contents of CHANGE-BRIEF.md with this assignment's brief, and commit it before the first agent run. CLAUDE.md imports the file. Earlier briefs stay at their tags, and you can read any of them back, for example git show a7:CHANGE-BRIEF.md, when you write the GDD defence. Add dated revisions below the original rather than rewriting it.
- The element: your Assignment 9 technique, and what finishing it means in the full game. Name the scenes it now works in and what changes when other systems are live around it. If you changed technique, give the design reason and the options you rejected.
- The test contract: what tests will read and never read. Module 14's guard tests read only the guard's mode and positions, and moved the player only as a printed fixture.
- Save rules, before implementation: path, format and version field, and what happens for missing, corrupt, newer-version and unwritable files. Module 15's plan deferred its save feature with "write migration/corruption/reset rules before implementation"; writing them is the design work.
- The export target and its renderer. Name the renderer the target requires; the Web target needs Compatibility and GDScript. List every earlier feature that renderer puts at risk: decals, compute shaders, particle trails, particle SDF collision, and any shader that relies on them. Name the state you expect to claim.
- The pitch ledger: copy the "will exist" list from your Assignment 8 PROJECT-BRIEF.md, and predict which items you will deliver, change or drop.
- Predictions, in writing:
  - one gap your Assignment 9 tests do not cover, which your audit will probe;
  - where your existing tests' runs will be saved once persistence exists;
  - which files an import of a fresh clone will create that are not committed;
  - what --export-release and --export-pack will each do without templates.
- At least three predicted failure cases, and how you will check them.
What must not change: the earlier layers and their tests, unless your brief first says why. Done means every row of the Use It table has evidence.
## 2. Build It

Split the work into separate agent runs, each ending by writing HANDOFF.md: files changed, exact test commands and real results, what the next task may rely on, and what is unverified. Each later run starts by reading it and rerunning every test it lists, and CLAUDE.md points at it. Sequencing the runs is Tool Orchestration.
A sensible order:
1. the renderer switch, if your export target needs one, with every earlier suite and look check rerun;
2. integrating your game-AI technique, in two or three runs if it has parts, as Module 14's guard did;
3. persistence;
4. the menu;
5. the export preset.
Start each run with a plan:
```text
Read CLAUDE.md first, then README.md, GDD.md, CHANGE-BRIEF.md,
HANDOFF.md if it exists, project.godot, and every script and test this
task touches. Run every test HANDOFF.md lists through
./scripts/run-test.sh; if any fails, stop and report.

Task: <one task from my brief>. Propose the smallest plan: the files and
nodes to add or change, what must not change, and the checks that will
prove it, reading only the observable state my test contract names.
Do not edit yet. After I approve, implement only that task, run every
listed test through ./scripts/run-test.sh (60 for frame-counted tests,
realtime for audio and networking), paste the real output, and update
HANDOFF.md. A run is clean only if every test exits 0 and its log has
no "SCRIPT ERROR", "SHADER ERROR" or "Failed loading resource" lines;
list any other "ERROR:" line and say what it means. Use Godot 4.7.2
API; if you are unsure something exists, say so instead of guessing.
Do not open a Godot window. Do not commit.
```
This is a prompt to Claude Code, not an installed shell command. For a non-interactive run, scope it the way earlier assignments did, with read-only git and Skills disabled:
```bash
claude -p "$(cat prompt-run.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(./scripts/run-test.sh:*),Bash(godot --headless --path godot --import:*),Bash(git status:*),Bash(git diff:*),Bash(git log:*),Bash(ls:*),Bash(mkdir:*)" --disallowedTools "Skill" --max-turns 60 --output-format stream-json --verbose > session-N.jsonl
```
Scoping prevents accidents; it contains nothing. Allowing godot --script allows anything GDScript can do, and Module 14 has the proof (below).
Your gate between runs:
1. Read the session's final result event, which records a --max-turns stop and any permission denials.
2. Read the diff and the new HANDOFF.md.
3. Run godot --headless --path godot --import once.
4. Rerun every test yourself through scripts/run-test.sh (the Assignment 9 version, which takes GODOT_PROJECT) and read the whole log. A script error does not change Godot's exit code; the wrapper fails on it, but read anything else marked ERROR: too.
5. Commit. That commit is the baseline for the next diff.
Persistence. Module 15's rules held once corrected:
- read version before any other field, and never overwrite a newer version whatever else changed;
- validate the whole file before changing live state;
- warn and stay playable on any failure;
- write a temporary file, then rename it over the old one.
Tests never touch the player's real user://. The primary rule is in your code: the save path is injectable, a test-mode session saves nothing unless the test sets a path, and a test asserts the real save folder is unchanged.
As a backstop for older suites that save through game code (exactly what Module 15's agent got wrong), point the user-data location at a scratch folder for every test run. On macOS, and probably on Linux, that means HOME; Module 15 verified it on macOS only. On Windows, user:// lives under %APPDATA%, so HOME does nothing there and the equivalent is APPDATA. Verify the override on your own operating system before you rely on it, and record how.
Create the scratch folder first, once:
```bash
mkdir -p ../scratch-home
```
Then run each save-touching test against it, for example on macOS:
```bash
HOME="$PWD/../scratch-home" ./scripts/run-test.sh test_best_time.gd 60
```
The menu. Grab focus in code when the scene starts, for example $StartButton.grab_focus.call_deferred(). Text drawn with draw_string has no accessible name; a Label or Button can carry accessibility_name. Godot's screen reader support is experimental, and testing one is optional.
Export. Add one preset for your target, exclude your tests, and commit export_presets.cfg. Never commit .godot/export_credentials.cfg.
If your target needs a different renderer from the one you built on, switch early. Then rerun every earlier suite, and redo every earlier human look check (Assignment 5's controlled values, Assignment 6's on-screen verdicts), because a headless run draws nothing and will pass on a game whose effects no longer render.
The output folders must exist, and --export-pack needs no templates, so first look at what would ship:
```bash
mkdir -p build/web build/pack
```
```bash
godot --headless --path godot --export-pack "Web" ../build/pack/game.zip
```
--export-release needs export templates for the exact engine version (a folder named 4.7.2.stable), installed from Editor → Manage Export Templates. They are a large download: the 4.7.2 template file on [Godot's 4.7.2 release page](https://github.com/godotengine/godot/releases/tag/4.7.2-stable) is about 1.3 GB (1,281,349,702 bytes, checked 6 October 2026). Downloading them is your decision; check your disk first.
Without templates, run the export anyway and keep the error: it is the evidence for "source-ready, not export-ready." With them, export, launch the exported build, play it, and record the package's SHA-256. Replace Web with your preset's name:
```bash
godot --headless --path godot --export-release "Web" ../build/web/index.html
```
A Web build must be served over HTTP; opening index.html from the file system does not work. As far as we know, threaded builds also need cross-origin isolation headers from the server. The editor's Run in Browser handles both. If you serve it yourself, record how.
### What the recorded runs got wrong

What agents got wrong in Modules 14 and 15, each while their own tests passed:
- A guard's "never inside the obstacle" check could not fail, because physics stopped the body at the surface. The audit measured clearance instead.
- "Movement begins on the next physics tick" held in 8 of 20 trials; the first path arrived anywhere from frame 2 to frame 9.
- A behaviour-tree guard passed 12 of 12 checks on top of 626 lines of SCRIPT ERROR.
- Denied kill and lsof, an agent put OS.execute("/bin/kill", …) inside a Godot test. Allowing godot --script allows anything GDScript can do.
- The level-generator agent measured the jump under a ceiling (128.3 px; 163.3 px on a flat floor) and tested landing on a hand-built row, not a generated level.
- Module 15's agent wrote that no test touched the player's real save; two unchanged suites wrote to it, leaving a "best" of 0.0667 s. It also checked level before version, so a newer file was overwritten.
Write at least one audit of your own, in the style of Module 14's audit/ scripts, for a case your Assignment 9 tests and the agent's tests do not cover in the finished game. Both of Module 14's guard brains ignored a player standing in plain sight for about 165 physics frames, because nobody had specified what Search should do. Look for that kind of gap, especially where your technique now meets systems it never met in its scenario scenes.
## 3. Use It

Record actual results in TEST-REPORT.md, with revision, engine version, renderer, operating system and date:

| Check | Evidence to collect |
|---|---|
| Clean clone of a10 | Import log, git status, generated-file inventory, engine/renderer/OS, short main-scene run and every documented test result. |
| Assignment 9 technique in the finished game | The technique's checks, scenario-to-game integration evidence, the new audit of a missed case, and your own play against it. |
| Assignment 9 teach/ projects | The documented starter and solution checks with the correct GODOT_PROJECT, preserving the tested revision. |
| Persistence | Round trip, missing/corrupt/newer-version/unwritable cases, real save folder unchanged by tests, and a human restart check. |
| Menu | Start or pause menu operated by keyboard, with initial focus; screen-reader testing only if actually attempted. |
| Semester layers | Generated art/sound, Blender assets, GDD/interaction, shaders/materials, particles, animation and game AI working together, or a documented removal/replacement. |
| Pitch ledger | Each Assignment 8 “will exist” item marked delivered, changed or dropped, with evidence or reason. |
| Export state | Committed preset, target/renderer, inspected pack contents, export attempt, exact blockers or played exported build, and checksum if built. |
| Human playtest and revision | A real full play session and at least one observation-driven inspect-and-revise cycle; honest remaining limits. |

For the clean clone's short main-scene run, use the --quit-after flag from Chapter 0's table:
```bash
timeout 120 godot --headless --path godot --quit-after 120
```
A scripted route is not a playtest, and your own playtest is required. Never delete a failing assertion or weaken an expected value to get green. Document at least one inspect-and-revise cycle driven by an observation.
### The two defense films

Use the course-provided [Brutalist](https://github.com/nikbearbrown/brutalist.art) workflows, both with the walker modifier and both showing the submitted revision. Ask Claude Code to read each installed skill and follow it. If your checkout lacks one, request the course-provided version. The films discuss what you did.
Film 1, godot-walkthrough: what the finished game does. Real play from launch:
- the core loop;
- the earlier layers in context;
- your game-AI technique doing its job in real play;
- a failure and recovery;
- completion;
- the persisted data surviving a restart.
Label scripted-input captures; they are not playtests.
Film 2, godot-gdd: why it is specified that way. Walk the GDD with game evidence, keeping proposed, implemented, tested and human-decision-pending apart. Then:
- walk the pitch ledger: what your Assignment 8 pitch said would exist, and what happened to each item;
- explain your technique as it now works in the finished game, your save rules, and the export state you claim, with its evidence.
Film 2's Verdict names the five Supervisory Capacities. Each gets one concrete moment from anywhere in this game's history since Assignment 2, cited by tag or commit:
- PA, Plausibility Auditing: a wrong note you caught that seemed fine until you played it.
- PF, Problem Formulation: a task you defined before the agent saw it.
- TO, Tool Orchestration: an order of tasks, and the context each run got.
- IJ, Interpretive Judgment: meaning you supplied that no check could detect.
- EI, Executive Integration: how you held the semester's layers toward one game.
The syllabus makes the final week the week of all five. The same five, with those moments in more detail, go in FRICTIONAL.md. If you tagged earlier Frictional entries with PA, PF, TO, IJ or EI, start there.
For both films:
- Walker opening/summary and Verdict → Your Turn → regular outro.
- AI narration, including Liam, is allowed.
- Reconstructed views and held frames are labelled.
- Use the skill's native 4K landscape rendering and checks, and watch each final export.
- There is no minimum runtime. A Short, paid media and public YouTube publication are not required.
## 4. Ship It

- The game source and used assets, with export_presets.cfg, and Assignment 9's teach/ projects. No caches, credentials or export output.
- README.md: name, starting point and credits, engine version and renderer, run instructions, controls, every test command with its time mode, the state claimed and its evidence, the pitch ledger, the license, and both film links.
- LICENSE, GDD.md, CLAUDE.md, CHANGE-BRIEF.md, HANDOFF.md, TEST-REPORT.md, PERFORMANCE.md, and FRICTIONAL.md with the five capacities.
- SOURCES.md: every asset, model, addon and tool, and the syllabus's labor-separation disclosure with the stage you actually reached and all five capacities.
- Both films' beat sheets, scripts/prompts, and evidence/coverage records.
Keep MP3, MP4, export packages and files over 25 MB out of GitHub. Store them in the designated course media storage and link them from the README. Identify each film, and any export package, by filename and SHA-256 checksum. Test reviewer access. Tag the final submitted commit a10.
## 5. Verify

Clone tag a10 into an empty folder, replacing the placeholder, and run every documented check there:
```bash
git clone --branch a10 <your-repository> ../a10-check
```
Then, inside ../a10-check:
```bash
godot --headless --path godot --import
```
```bash
git status --short
```
Run every game test through scripts/run-test.sh, then Assignment 9's checks with GODOT_PROJECT=teach/solution and GODOT_PROJECT=teach/starter.
Submit a source ZIP of that revision, without caches, credentials or large media, with SUBMISSION.md:
```text
Assignment: Assignment 10 - Final Project: From Brief to Export
Student:
Project name:
GitHub repository URL:
Tag a10 commit SHA:
Game-source revision shown in both films:
Godot version, renderer, and operating system:
Renderer changed for export (yes/no; if yes, from what):
Game-AI or systems element (from Assignment 9, or changed and why), in one sentence:
Persisted data and save rules (one line):
State claimed (source-ready or export-ready) and its evidence:
Export target; templates installed (yes/no):
Export package filename and SHA-256 (if built):
Pitch ledger (delivered / changed / dropped counts):
License for my contributions:
Walkthrough film URL, filename, SHA-256:
GDD film URL, filename, SHA-256:
Summary of my work:
Known limitations:
```
It is fine to render from a game-source commit and then make a final submission commit adding the film documentation. Identify both revisions, and verify that the final commit does not change the demonstrated game source. Put the final submitted SHA in the Canvas note; do not try to embed a commit's own SHA into that same commit. Canvas, GitHub, and both films must refer to the same submitted work.
## Rubric — 250 points

| Component | Points |
|---|---:|
| Implementation and explanation | 150 |
| Frictional — honest log | 25 |
| GitHub version posting matching Canvas | 25 |
| Relative Quartile | 50 |
| **Total** | **250** |

### Implementation and explanation — 150 points


| Criterion | Points |
|---|---:|
| Assignment 9 technique integrated into real play, justified if changed, behind the specified observable-state test contract; an audit of a case the tests miss and human play against it. | 32.5 |
| Persistence and reproduction: save rules written first and enforced, version/corruption handling, isolated save tests, and a clean a10 clone passing every documented game and teach/ check. | 25 |
| Export: committed preset, target/renderer decision, inspected pack contents and an attempted release export; source-ready/export-ready claims match actual evidence. | 15 |
| Finished game: the semester's layers working together, a keyboard-usable front door, a reconciled pitch ledger, clear run instructions, names, licenses and professional presentation. | 30 |
| Verification: actual full playtesting, an observation-driven revision, appropriate checks and honest limitations. | 12.5 |
| Both required Brutalist films: real-play coverage and GDD defense, pitch/save/export evidence, all five capacities with concrete tagged moments, readable/audible films showing the submitted game revision. | 35 |
| **Subtotal** | **150** |

Award partial credit for demonstrated work within each criterion. Claims must be defensible; attractive presentation does not repair an incorrect explanation. A clean-clone pass shows the build reproduces on your machine and engine version. It does not show that an exported game runs elsewhere or that anyone enjoys it.
### Frictional — honest log — 25 points

In FRICTIONAL.md, record actual attempts, expectations, difficulties or checks, responses, and learning. Distinguish your work from the AI's work.
- 7 points: Specific, honest accounts of what you tried and what happened.
- 7 points: What you checked, changed, or learned in response, including unresolved questions.
- 5 points: Explicit human/AI contributions, including what you accepted, modified, or rejected.
- 4 points: Traceability to relevant commits, prompts, tests, or observations.
- 2 points: The five Supervisory Capacities, each with a concrete moment in more detail than the film gives.
An unsuccessful attempt can earn full Frictional credit. More hours, more entries, or invented struggle do not earn extra credit. If something worked immediately, say so and explain how you checked it. Label retrospective notes honestly. AI may organize your notes; it must not manufacture experience or understanding.
### GitHub version posting matching Canvas — 25 points

- 10 points: Required, accessible game source, teaching projects and documentation are actually posted.
- 8 points: Canvas identifies the exact submitted commit (tag a10) and supplies the matching source files and clear run instructions.
- 7 points: Accessible film links, identified media versions, and film source/evidence correspond to the submitted game.
### Relative Quartile — 50 points

Assigned after the instructor and TAs review the full comparison group. It compares specificity, substantive improvement, demonstrated understanding, evidence, honesty about verification, usability, and professional communication. These are comparative considerations, not extra point categories.
Meeting the stated criteria can earn the other 200 points; it does not guarantee these 50 points. The course's announced comparison-group and tie/late-work rules govern placement. Production polish matters only as professional communication. A plain, precise explanation outranks a beautiful one that misrepresents the work. Paid-tool access and simply using Brutalist earn no automatic comparative bonus.
## Academic integrity

Use SOURCES.md to credit every starter, asset, model, addon, collaborator and tool. Describe what AI contributed to the game, tests, GDD, scripts, beat sheets and narration, and what you personally decided, played, checked, changed or rejected.
The instructor or a TA may ask you to:
- rebuild from your tag;
- run any test;
- defend a save rule;
- explain how your game-AI technique decides what to do;
- account for any pitch-ledger entry.
Inability to explain reduces points under the relevant criteria. Misrepresenting authorship, provenance, playtesting or verification is an academic-integrity matter under the [course AI policy video](https://youtu.be/8Ut0Cdl6vMw) and the course/university policies.
