# Module 15 — Final projects: from brief to export

CSYE 7270 · Fall 2026 · Week 15

## Executive summary

This capstone module turns Walker's cycle, Game brief → Build → Playtest → Inspect → Revise → Export, into a procedure someone else can repeat from a clean copy of your repository. You will add a persistent personal best to the public `walker-jumpman-clawd` game, reproduce it from a fresh clone, and attempt a Web export. On 27 September 2026 Claude Code built that feature, passed all 31 of its new checks, and reported that no test touched the player's real saved data. That was false: two of the game's unchanged test suites had written a personal best into the real save folder. The final commit passes all five test scripts from a clean clone, and the export fails exactly where it should, because the Godot 4.7.2 export templates (the prebuilt engine files an export needs) are not installed. None of that plays an exported game, tests a screen reader, or shows that a best-time line is fun. The module prepares Assignment 10, the final project.

## The question

Your project passes every check in your working folder. You push it. A TA clones it and runs the same commands. What differs about their folder, and which of your passing checks depended on it? The chapter found three answers on the course Mac on 27 September 2026.

1. **The import cache.** Your folder has `godot/.godot/`; a clone does not. In Chapter 4's project, a fresh-clone run before importing printed seven `PASS` lines, exited 0, and logged 55 `ERROR` lines for assets it could not load. `walker-jumpman-clawd` draws everything in code, so it needs no import.
2. **Generated files you never committed.** Importing a clean clone of `walker-jumpman-clawd` created an untracked `godot/tests/test_clawd.gd.uid`.
3. **The user data folder.** `user://` is not in your project. It is named after `application/config/name`, so every copy with that name shares it, including your real game.

## The ideas

### 1. The cycle is a procedure, and its last stage has three levels

Every stage leaves evidence a stranger can open, and `walker-jumpman-clawd` carries the whole cycle as files:

| Stage | Evidence it leaves in `walker-jumpman-clawd` |
|---|---|
| Game brief | `GAME-BRIEF.md`; `GDD.md` (12 features, 22 acceptance cases) |
| Build | `PRODUCTION-PLAN.md` (22 tickets); `BUILD-REPORT.md` (its first 25-check run found 4 failures) |
| Playtest | `PLAYTEST-PLAN.md`, a no-coaching human protocol |
| Inspect | `DESIGN-REVIEW.md`, which says what each check establishes |
| Revise | `CHANGE-BRIEF.md` and `FRICTIONAL.md`: dated predictions, failures, fixes |
| Export | Not yet: tickets WJ-020 to WJ-022 are planned |

A stage is finished when its evidence exists, not when an agent says so. "Export" also hides three different claims, and your final project should name the one it makes.

| Claim | Evidence that establishes it | What it does not establish |
|---|---|---|
| **Source-ready** | A clean clone of a named commit imports and passes its documented checks on a named engine version, with the logs, hash and version string | That anyone can run it without Godot |
| **Export-ready** | A committed `export_presets.cfg`, matching templates, a successful `--export-release`, and notes from playing the exported package | That it is published |
| **Released** | A human decided to publish a specific package to a specific place | Quality |

`walker-jumpman-clawd` is source-ready for its first iteration. Its build report records that export templates are absent and nothing was exported or published.

### 2. Reproducing from a clean clone

A clean clone has no import cache, no untracked files, no leftover user data and no editor state, so it is the only honest test of "source-ready". Clone the committed revision into an empty folder, import once, and run `git status --short`: anything listed is something the import generated that you never committed. Run every documented check with its documented flags, reading the log and not only the exit code, and record the commit hash and engine version string.

This project also fingerprints itself. `scripts/clawd-build.cjs` hashes every file under `godot/` into a combined `build_id` and refuses to run if a file the iteration promised to preserve has changed. On a clean clone of the published commit it reproduced the committed `build_id`, `91580b18…`: identical source, byte for byte. [Chapter 0](../../chapters/00-the-toolchain.md#the-time-trap-frames-are-not-seconds) explains the clock trap behind `--fixed-fps 60`.

### 3. Export presets, templates and what `--export-pack` shows

An **export preset** is a named recipe for one platform, saved in `export_presets.cfg` at the project root and safe to commit; signing keys and passwords go in `.godot/export_credentials.cfg`, which generally should not be ([Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)). An **export template** is a prebuilt engine binary for one platform, without the editor or debugger, to which your project's data is attached. Templates are a separate download, installed through **Editor → Manage Export Templates**, and Godot looks for them in a folder named for the exact engine version.

**Your decision.** The templates are a large download (about 1.3 GB, per Assignment 10), and this module does not require them. A Web export needs the Godot 4.7.2 templates, matching your editor's exact version, and whether to download them is up to you. The instructor's run did not; its failure is the evidence used here. Assignment 10 asks for an export preset, an inspected `--export-pack` listing and an export attempt, with the claimed state matching your evidence. An attempt that fails for lack of templates, with the error kept, supports a source-ready claim.

| Command | Produces | Needs templates? |
|---|---|---|
| `--export-release "<preset>" <path>` (and `--export-debug`) | A runnable package for the preset's platform | Yes |
| `--export-pack "<preset>" <file.pck or .zip>` | The project data only | No, on 4.7.2 (run on 27 September 2026) |

`--export-pack` lists exactly which files a preset would ship, but it is not a game anyone can double-click. The level is a `.json` file and a separate filter governs non-resource files, so the instructor listed a pack rather than guess. The Web target needs the Compatibility rendering method and cannot export C# projects ([Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html)); `walker-jumpman-clawd` uses `gl_compatibility` and GDScript.

### 4. Save data: where it lives and how it ages

`res://` is your project folder. `user://` is a per-project folder, writable even in an exported project; on macOS it is `~/Library/Application Support/Godot/app_userdata/[project_name]` ([File paths](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html)). The name comes from `application/config/name` unless `application/config/use_custom_user_dir` overrides it.

Godot's [saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html) tutorial offers JSON, binary through `store_var` and `get_var`, or `ConfigFile`. JSON is diffable but cannot hold a `Vector2`, and [FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html) warns that deserialized objects can carry code, so never allow them from untrusted data. `FileAccess.open()` returns `null` on failure, and a file is flushed when closed, not if the process is killed. `DirAccess.rename()` overwrites an existing destination ([DirAccess](https://docs.godotengine.org/en/stable/classes/class_diraccess.html)), so writing a temporary file and renaming it should survive a crash mid-write. The instructor did not test a crash.

A save file outlives the code that wrote it. Four rules:

1. Put a `version` in the file and read it first.
2. A newer version came from a newer build. Never repair or overwrite it.
3. Validate the whole snapshot before changing live state. `walker-loading-serialization` failed 9 of 28 negative checks while its loaders applied part of a snapshot and leaked nodes; a shared validator fixed all 28.
4. Tests never touch the player's real save. On macOS, pointing `HOME` at a scratch folder moves `user://` there (confirmed with Godot 4.7.2; Windows and Linux untested).

### 5. Menus, focus and what a screen reader would find

Godot's [navigation guide](https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html) says to focus a node from code when the scene starts, and `walker-gui-accessibility` tests 8 Tab transitions through every control. A `Control` has `accessibility_name` and `accessibility_live` ([Control](https://docs.godotengine.org/en/stable/classes/class_control.html)), and Godot 4.5 added AccessKit screen reader support, which its release notes call experimental. But `walker-jumpman-clawd` paints its HUD with `draw_string`, so none of its text is a `Label` or has an accessible name, and the best-time line inherits that. No screen reader was tested, and headless tests cannot verify VoiceOver speech.

### 6. Defending the project: what the old final asked, and what still holds

The Spring 2026 course graded a Final Portfolio Piece on five criteria, and its Show and Tell video had to name the student and the game. Four expectations still hold. The old weights do not; Assignment 10 uses the course's 60 / 10 / 10 / 20 framework.

| Old criterion | Where it lives now |
|---|---|
| Professionalism: can someone else run it, are things named well | The clean-clone check, the `walker-` name, run instructions in the README |
| Scope: shaders, animation, UX/UI and the rest | Every layer added since Assignment 2 in one repository, tagged `a3` to `a10`; Assignment 10 sets the criteria |
| Video: must discuss what you did | Two films, the labor-separation disclosure in `SOURCES.md`, `FRICTIONAL.md` |
| License: MIT or your own copyright | `SOURCES.md` or the README names licenses and sources for code, art, audio and film assets |

"What you did" has a shape in this module's example. Claude Code wrote the feature. The human wrote the save rules, ran the independent check, found the false claim and decided the correction. Catching the claim was plausibility auditing, and turning WJ-D02 into rules was problem formulation. The syllabus's Week 15 row lists all five supervisory capacities.

The [explainer policy](../../prerequisites/brutalist-godot-explainers.md) offers three film skills; pick by the claim. `godot-walkthrough` shows what the game does when played. `godot-gdd` shows why it is specified that way, keeping proposals, implemented features, tests and pending decisions separate. `godot-gamedev` shows how it is built. Assignment 10 requires the first two, with the `walker` modifier. The film is code: the beat sheet and script live in GitHub, the rendered file in designated media storage, linked from the README by filename and SHA-256. State the game and the revision shown.

## The Walker example: walker-jumpman-clawd

**Get the builds.** All are public: [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman), [`walker-loading-serialization`](https://github.com/nikbearbrown/walker-loading-serialization), [`walker-gui-accessibility`](https://github.com/nikbearbrown/walker-gui-accessibility), [`walker-gui-custom-splash-screen`](https://github.com/nikbearbrown/walker-gui-custom-splash-screen), [`walker-gui-control-gallery`](https://github.com/nikbearbrown/walker-gui-control-gallery) and [`walker-loading-runtime-save-load`](https://github.com/nikbearbrown/walker-loading-runtime-save-load). The adaptations of Godot's demo projects keep the upstream MIT license. The two Jumpman repositories carry no license file (checked on GitHub, 6 October 2026), so credit them in `SOURCES.md`.

**What it is.** Professor Bear's evolving Assignment 1 example: the First Steps level with the Clawd mascot as the player, forked from `walker-jumpman` at commit `9387542`. Its `SOURCES.md` credits the mascot's 18 animations as a GDScript port of Brutalist's `ClaudeMascotScene.tsx`, "not an Anthropic product or endorsement". The chapter's run used commit `382f2ba`. Public `main` is one commit ahead and changes only `README.md`, `design/` and `youtube/` (checked through the GitHub API, 6 October 2026), so cloning it gives the same `godot/` folder and `scripts/`.

**What its checks establish.** Run with `--fixed-fps 60`: 25 mechanics checks, 9 keyboard checks and a 1,950-comparison animation-parity check, and the deterministic route reaches the flag with zero deaths. `CLAWD-STATUS.json` says what is not done: `"human_playtest": "pending"`.

## Predict → Build It → Use It → Ship It → Verify

### 1. Predict

Answer in writing before you delegate, and keep your answers.

1. The game's existing tests create the session with default settings, and you may not edit them. Once the game saves a best time on completion, where will those tests' "completions" be saved? Which test "completes" a run in a few physics ticks?
2. A save file says `"version": 2` and also uses a different `"level"` name. Your code checks `level` before `version`. What happens on the next completion?
3. You clone your own repository into an empty folder and import. Which files will Godot create that are not in the commit? Should they be committed?
4. `export_presets.cfg` is committed and valid. What will `--export-release "Web"` do on a machine with no templates? What will `--export-pack` do?

### 2. Build It

Get your own copy of the public repository. Do not edit the instructor's.

```bash
git clone https://github.com/nikbearbrown/walker-jumpman-clawd.git
```

At the clone's root, the folder that contains `godot/`, record the baseline with the README's three checks. The instructor's runs were not wrapped in `timeout`; these add it, because a script error before `quit()` leaves headless Godot running forever.

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_clawd.gd --fixed-fps 60
```

Expect `WALKER TESTS: 25 checks / 0 failures`, nine `PASS` lines, and `"checks":1950,"failures":0`.

This prompt turns WJ-D02's "write migration/corruption/reset rules before implementation" into rules; writing them is the design work. Paste it into Claude Code from the clone's root:

```text
This is walker-jumpman-clawd (Godot 4.7.2, GDScript), Professor Bear's Walker
example. Read README.md, GDD.md (FEAT-10), PRODUCTION-PLAN.md (WJ-D02),
godot/project.godot, godot/game/session.gd, godot/ui/hud.gd and every script
in godot/tests/ before editing anything.

Implement FEAT-10, a persistent personal best, as ONE bounded change.
Save rules (these are the WJ-D02 rules; follow them exactly):
- One JSON file, default path user://best_time.json, holding
  {"format": "walker-jumpman-clawd.best", "version": 1,
   "level": "first-steps", "best_seconds": <float>}.
- Load it once when the session starts. Missing file: no best, no error.
- Ignore, with push_warning and without crashing, a file that is not valid
  JSON, is not a dictionary, has the wrong format or level, or whose
  best_seconds is not a finite number greater than 0.
- A file whose version is greater than 1 was written by a newer build: ignore
  it and never overwrite it.
- On COMPLETE, if there is no best or last_finish_time is lower, update the
  best and save it: write a temporary file, then rename it over the old one.
  A failed write is reported with push_warning and changes no game state.
- The HUD's complete panel shows the best time. Nothing else in the HUD moves.
- The save path must be settable before the session enters the tree, so a
  test never reads or writes the player's real user:// file.

Do not change movement, tuning, the level JSON, collision, the camera or any
existing test. The 25 mechanics checks, 9 keyboard checks and test_clawd.gd
must still pass.

Write godot/tests/test_best_time.gd (extends SceneTree, same report style as
test_game.gd). Give every case its own fresh directory under
res://../evidence/. Complete the real route with tests/route_driver.gd and
prove: the file is written with the schema above; a NEW session instance
loads the same best; a slower completion does not replace it; each rejected
file leaves the game playable and is replaced only when a valid best is
saved; a version-2 file survives a completion byte for byte.

Then add godot/export_presets.cfg with one preset named "Web" (platform
"Web", export path ../build/web/index.html, tests/* excluded from the
export). Do not install or download export templates.

Run all four test scripts with
`godot --headless --path godot --script <res:// path> --fixed-fps 60`
and report the real output. Do not commit. End with a short list of what
these tests cannot tell us.
```

The instructor ran it headless, with the prompt saved one folder above the project. The settings string was meant to keep the session out of Claude Code's automatic memory; its effect was not verified, and you need neither it nor `--strict-mcp-config`.

```bash
claude -p "$(cat ../prompt-best-time.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > ../session.jsonl
```

Verify the result yourself (below) before correcting anything. The instructor's correction went into the same session with `--resume`, using the ID from the first transcript's `init` event; use your own ID, not the one shown.

```bash
claude -p "$(cat ../prompt-best-time-fix.txt)" --resume ae769ccf-812c-460e-896e-fd82e64b77c2 --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > ../session-fix.jsonl
```

This correction states observed facts, the rule each broke and the smallest fix, without describing the code. Send it only if your checks find the same failures; otherwise write one from what you observed.

```text
I verified your change with my own commands. Two save rules are broken and
one claim in your summary is false.

1. You wrote that no test writes the player's real user:// file. With HOME
   pointed at a scratch folder, the unchanged tests/test_game.gd saved
   best_seconds 5.4667 to user://best_time.json, and tests/test_keyboard.gd
   saved 0.0667 (its resolve_contacts fixture "finishes" after 4 ticks).
   Those tests create the session with the default path.
2. My check wrote {"format":"walker-jumpman-clawd.best","version":2,
   "level":"first-steps-remix","best_seconds":4.0}, completed the route, and
   the file was overwritten. The same happens when a version-2 file renames
   "format". The rule is: a version greater than 1 is never overwritten,
   whatever else in the file changed.

Fix both in godot/game/session.gd only:
- A session with test_mode = true persists nothing unless the test set
  best_time_path explicitly. Normal play keeps user://best_time.json.
- Read "version" before any other field. If it is a number greater than 1,
  never write that path in this session.
Do not edit test_game.gd, test_keyboard.gd or test_clawd.gd.

In tests/test_best_time.gd: give each run its own new directory (for example
a timestamped folder), so a file left by an earlier run cannot make case 01
pass; add the two version-2 cases above; delete the "hud-best-field-set"
check, because it does not test the HUD.

Run all four test scripts the same way as before and report the real output.
Do not commit.
```

**The Codex difference.** Codex was not run for this chapter. In Chapter 4, its `workspace-write` sandbox could not write under `user://`, so it may block accidental saves and make normal saving fail. Neither is tested; if you use Codex, check where your saves landed.

### 3. Use It

Play before you read any report.

1. Open `godot/project.godot` in Godot 4.7.2, play with F5, and finish the course. **HUMAN CHECK:** does the complete panel show your time and a best, and is the line readable at 640 × 360 scaled to your window? Nothing checks whether the longer detail line fits.
2. Quit, relaunch and finish more slowly. **HUMAN CHECK:** the best must not change. Finish faster, and it must. Normal play writes your real `user://` on purpose; only test runs must stay out of it.
3. Open `best_time.json` in the user data folder ([File paths](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html) lists it for each system). **HUMAN CHECK:** does it match the schema in the prompt?
4. Use the menu with the keyboard only, then with a screen reader if you have one: VoiceOver on macOS, Narrator or NVDA on Windows. **HUMAN CHECK:** write down what it announces. Expect little.
5. Read `export_presets.cfg`. **HUMAN CHECK:** is `tests/*` really excluded, and is the gallery scene meant to ship? The pack listing below says it does.

### 4. Ship It

Commit the change and your own check separately. Read `git status` first: the instructor's final test wrote a fresh `evidence/` folder on every run, so decide what you keep.

```bash
git add -A
```

```bash
git commit -m "FEAT-10: persistent personal best under WJ-D02 save rules"
```

Your own check is the evidence the agent did not write. The instructor's, [`verify_best_time_rules.gd`](../../examples/15-final-projects-brief-to-export/reviewer/verify_best_time_rules.gd), has 13 checks in five cases; read it, then copy it to `godot/tests/` or write one that attacks the rules differently. A script's `.uid` file exists only after an `--import` that follows its creation, so import before you commit. The instructor forgot, and a clean clone re-created the file as untracked.

```bash
git add godot/tests/verify_best_time_rules.gd godot/tests/verify_best_time_rules.gd.uid
```

```bash
git commit -m "Add reviewer's save-rule check (human-written)"
```

Then run the project's invariant script from the full repository. It needs Node (the instructor's run used v24.17.0).

```bash
node scripts/clawd-build.cjs
```

It will fail, as it should: the first Clawd iteration promised `godot/ui/hud.gd` stays byte-identical, and FEAT-10 changes it. Whether to update that invariant is a design decision with an owner. Record it in `CHANGE-BRIEF.md`; do not delete the complaining line.

Your `FRICTIONAL.md` entry records which predictions were right, any false claim and how you found it, any stray file, the fix, any failure you cannot explain, and what is still unverified. For films, `godot-gdd` defends FEAT-10's rules against evidence (planned, built, tested, pending), and `godot-walkthrough` shows the best time surviving a restart. Use the course-provided checkout of [Brutalist](https://github.com/nikbearbrown/brutalist.art) and request the update if it lacks a skill. This practice adds no graded film.

### 5. Verify

On macOS, point `HOME` at a scratch folder for every test run, moving `user://` out of your real data.

```bash
mkdir -p ../scratch-home
```

Run the three original suites, then list the scratch user folder. There should be no `best_time.json`.

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/test_clawd.gd --fixed-fps 60
```

```bash
ls "../scratch-home/Library/Application Support/Godot/app_userdata/walker-jumpman-clawd/"
```

Then the two save-rule tests. Afterward there should be a `best_time.json`, because the instructor's case E plays in normal mode on purpose.

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/test_best_time.gd --fixed-fps 60
```

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/verify_best_time_rules.gd --fixed-fps 60
```

Reproduce from a clean clone, replacing the placeholder with your repository's path or URL.

```bash
git clone <your-repository> ../repro-check
```

Inside `../repro-check`, import, then look for files the import created:

```bash
godot --headless --path godot --import
```

```bash
git status --short
```

Run every test as above. Then attempt the export. The target folders must exist first.

```bash
mkdir -p build/web build/pack
```

```bash
godot --headless --path godot --export-release "Web" ../build/web/index.html
```

```bash
godot --headless --path godot --export-pack "Web" ../build/pack/game.zip
```

With no templates, the first export exits 1 with this error, which is the evidence for "not export-ready here":

```text
ERROR: Cannot export project with preset "Web" due to configuration errors:
No export template found at the expected path:
~/Library/Application Support/Godot/export_templates/4.7.2.stable/web_nothreads_debug.zip
No export template found at the expected path:
~/Library/Application Support/Godot/export_templates/4.7.2.stable/web_nothreads_release.zip
ERROR: Project export for preset "Web" failed.
```

If you install the templates, build again, serve the output and play it in browsers you name; the instructor did not. On the instructor's clean clone, `--export-pack` exited 0 and wrote a 24,926-byte ZIP of 20 entries: scripts compiled to `.gdc`, `levels/first_steps.json`, nothing from `tests/`, and the diagnostic `gallery/clawd_gallery` scene.

**What a pass proves:** a named commit is source-ready on Godot 4.7.2 on that Mac, the save rules hold for the cases tested, the unchanged suites no longer touch `user://`, and the preset is valid enough for Godot to look for templates. **What it does not prove:** that a Web export runs in any browser, that a crash between write and rename is safe, that a screen reader can read the result, or that anyone wants a best time.

## What the agents got wrong

Run on 27 September 2026 with Claude Code 2.1.150 (`claude-sonnet-4-6`). Every check the agent wrote passed; the instructor's own checks found these.

- **A false claim in the report.** The summary said no test touches the player's real `user://best_time.json`, yet that file existed. With `HOME` redirected, the unchanged `test_game.gd` saved 5.4667 seconds and `test_keyboard.gd` saved 0.0667, because its fixture "finishes" the course four physics ticks after its last restart. The prompt asked only for a settable path and forbade editing the old tests, so the gap was the prompt's as much as the agent's.
- **The version rule broke when another field changed.** `_load_best()` checked `format` and `level` before `version`, so a version-2 file with a renamed level or format was overwritten. The agent's own version-2 case changed only the version, so it passed; a human-written combined case failed twice.
- **A test proved less than its labels said.** Case 01 reused a fixed directory, so on a second run "file exists" passed while the file kept its first-run timestamp and nothing was written. A check named `hud-best-field-set` tested nothing about the HUD.

## If you know Unity or Unreal

| Godot | Unity | Unreal Engine 5 |
|---|---|---|
| `user://` | `Application.persistentDataPath` | `Saved/SaveGames` on development platforms |
| `export_presets.cfg` | Build profile asset (Unity 6) | Project packaging settings, launch profiles |
| Export templates | Platform build-support modules, added through the Hub | Platform SDKs, for some targets |
| `--export-release` | `-batchmode -executeMethod` into `BuildPipeline.BuildPlayer` | `RunUAT BuildCookRun` |
| `ConfigFile`, JSON | `PlayerPrefs`, JSON | `USaveGame` through `SaveGameToSlot` |
| `accessibility_name`, AccessKit | Accessibility module | UMG accessibility settings, `Accessibility.Enable=1` |
| `godot --headless --script` test | Play Mode test through `-runTests` | `-ExecCmds="Automation RunTest …;Quit"` |

The biggest difference for an agent workflow is how much of the pipeline is text it can read and diff. In Godot the preset, scenes and a JSON save are text, and the export is one flag on the editor binary. Unity's build profile is an asset file and its scenes are YAML by default, but installed modules are not in the project. Unreal packages through a separate tool and a cook step, and a Blueprint save graph is a binary `.uasset`. Unity and Unreal were not run for this course; the comparisons come from their documentation, checked on 27 September 2026. [Chapter 15](../../chapters/15-final-projects-brief-to-export.md) has the full comparison.

## Practice assessment (ungraded)

Answer in writing, from the source and the running game, before the practice quiz.

1. Open `godot/tests/test_keyboard.gd`. Which line "completes" the course, after how many physics ticks, and why is that harmless before FEAT-10 and data-corrupting after it?
2. Reorder `_load_best()`'s checks so `level` comes before `version`. Which case in `test_best_time.gd`, and which in your own check, fails? Why didn't the agent's original version-2 case fail?
3. List the files an `--import` of a fresh clone of your project creates, and say which belong in Git. Run `--export-pack`, list the ZIP, and name one file that should not ship and one that must.
4. Write three sentences for your final film about your own project: something you decided, something the agent did, and something no check established.

The ungraded Canvas practice quiz for this module has six multiple-choice questions with feedback. Do not paste Claude's explanation as proof of your understanding. Ask it to question you, then check the source yourself.

## The next step

Assignment 10, **"Final Project: From Brief to Export,"** opens in Module 14 and is due about Day 100; the Canvas page governs the date. It covers Modules 14 and 15 and the whole semester, with two films, `godot-walkthrough` and `godot-gdd`, both with the `walker` modifier. Carry this module's habits into it: a clean-clone run of your tagged repository, the state you can honestly claim, and a record of what you decided and what the agent did. The syllabus gives Week 15 to final Brutalist films and class discussion, so be ready to explain any part of yours. This lesson adds no graded deliverable. The long reading is [Chapter 15 — Final Projects: From Brief to Export](../../chapters/15-final-projects-brief-to-export.md).
