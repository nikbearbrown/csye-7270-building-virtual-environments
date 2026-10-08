# Chapter 15 — Final Projects: From Brief to Export

CSYE 7270 · Fall 2026 · Week 15

## Executive summary

**What this chapter is.** The last step of Walker's cycle, *Game brief → Build → Playtest → Inspect → Revise → Export*, taken seriously. The chapter covers what it takes for someone else to reproduce your build from a clean clone. It covers what an export is, and why Godot cannot make one without templates you install. It covers how a game keeps data between runs without corrupting it or clobbering it, what "accessible" means for a menu, and how the final Brutalist film ties all of that to one revision you can defend.

**Why read it.** Week 15 asks you to "reproduce the build and defend its design and evidence." Every earlier chapter ended at "the test passes on my machine." That is not the end. Your folder holds caches, imported files and saved data that a clean clone does not have. And a save file that a test writes into the player's real data folder is a bug the test itself cannot see.

**What you build.** A persistent personal best for Professor Bear's `walker-jumpman-clawd`. This is the game's own proposed feature FEAT-10, built under save rules its production plan asked for. It gets a round-trip headless test, a clean-clone reproduction check, and an export attempt whose real error message is the evidence. On 27 September 2026 Claude Code built it, and all 31 of its new checks passed. Its report said no test touched the player's real save. That was false. Two of the game's unchanged test suites wrote a "personal best" of 0.0667 seconds into `~/Library/Application Support/Godot/app_userdata/walker-jumpman-clawd/`. A second prompt fixed it, and a reviewer-written check confirmed the fix.

**What it does and does not prove.** A clean clone at a named commit imports, and all five test scripts pass. The save rules hold for missing, corrupt, newer-version and unwritable files. Export fails exactly where it should, because the 4.7.2 Web templates are not installed. None of that plays the exported game in a browser, tests a screen reader, or tells you whether a best-time line makes anyone want another run.

---

## The question

Your project passes every check in your working folder. You push it. A TA clones it and runs the same commands.

What is different about their folder, and which of your passing checks depended on the difference?

This chapter found three concrete answers, all on the course Mac on 27 September 2026:

1. **The import cache.** Your folder has `godot/.godot/`, and a clone does not. In Chapter 4's project, a test run in a fresh clone *before* importing printed seven `PASS` lines and exited 0, while logging 55 `ERROR` lines for textures and sounds it could not load. In this chapter's project, which draws everything in code, the same step works without an import. Knowing which kind of project you have is part of reproducing it.
2. **Generated files you never committed.** Importing a clean clone of the published `walker-jumpman-clawd` created an untracked `godot/tests/test_clawd.gd.uid`. Godot generates these identifiers, and the repository simply never committed that one.
3. **The user data folder.** `user://` is not in your project at all. It is a folder named after `application/config/name`. Two copies of a project with the same name share it: your scratch copy, the TA's clone, your real game. When the new code saved a best time, the unchanged tests wrote into the same folder the real game would use.

---

## Ideas you need

### Source-ready, export-ready, released

Module 1 drew the line in one sentence: "An editor run is not an exported application, and an export is not a public release." The Walker jumpman README says the same about itself: "This is a source-code release, not a hosted game or downloadable executable." For your final project, name which of three states you are claiming, and bring the evidence for that state:

| State | What it means | Evidence that establishes it | What it does not establish |
|---|---|---|---|
| **Source-ready** | A clean clone of a named commit imports and passes its documented checks on the named engine version, with no files from your machine | the clone's import log, each test's output, the commit hash, the Godot version string | that anyone can run it without Godot |
| **Export-ready** | A committed `export_presets.cfg`, matching export templates, an `--export-release` that succeeds, and the exported package launched and played on its target | the export log, the package's file list and SHA-256, notes from playing the *exported* build | that it has been published, or that strangers can find it |
| **Released** | A human decided to publish a specific package to a specific place | the destination, the package hash, the approval | quality; it only records that someone decided |

`walker-jumpman-clawd` is source-ready for its first iteration. Its GDD proposes a "locally served Web export" as the distributable. Its PRODUCTION-PLAN lists that as tickets WJ-020 to WJ-022, still planned. Its BUILD-REPORT says "Export templates are absent; no export download, Web package, repository push, or game publication occurred."

### Export presets and export templates

An **export preset** is a named recipe for one platform: which files to include, where to write the output, platform options. Godot keeps presets in `export_presets.cfg` at the project root, which "can be safely committed to version control". Signing keys and passwords go in `.godot/export_credentials.cfg`, which should "generally **not** be committed" ([Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)).

An **export template** is a prebuilt engine binary for one platform: "a specially-compiled binary, which is smaller in size, more optimized and does not include tools like the editor and debugger". Your project's data is packed and attached to it. Templates are a separate download from the editor. You install them from **Editor → Manage Export Templates**, either by downloading from inside the editor or from a TPZ file ([Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)). Godot looks for them in a folder named for the exact engine version. The real error below shows `4.7.2.stable`, so install the templates for the version you run.

From the command line ([command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)), `godot` must be an editor binary, not an exported game. [Chapter 0](00-the-toolchain.md#godot-is-also-a-command-line-program) has the full flag table.

| Command | What it produces | Needs templates? |
|---|---|---|
| `--export-release "<preset>" <path>` | a runnable package for the preset's platform | yes |
| `--export-debug "<preset>" <path>` | the same with the debug template | yes |
| `--export-pack "<preset>" <file.pck or .zip>` | the project **data only**; the extension picks PCK or ZIP | no, on 4.7.2 (we ran it) |

`--export-pack` is useful for inspection. It shows you exactly which files a preset would ship. It is not a game anyone can double-click.

**Resources and filters.** A preset's export mode can be "Export all resources in the project", selected scenes or resources, or everything except checked items. Two filters adjust that. The first "allows non-resource files such as `.txt`, `.json` and `.csv` to be exported", and the second can "exclude every file of a certain type" ([Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)). Read the first filter with care in this project, because the level is a `.json` file read with `FileAccess`. We did not guess whether it ships. We exported a pack and listed it (below). On 4.7.2, `levels/first_steps.json` was included by the "all resources" mode without an include filter.

**The Web target.** Godot 4 "can only target WebGL 2.0 (using the Compatibility rendering method)", and C# projects "currently cannot be exported to the web" ([Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html)). `walker-jumpman-clawd` already uses `gl_compatibility` and GDScript, so both constraints are met. The same page covers serving the exported files from a web server with the right headers. Testing a Web export means serving it and playing it in browsers you name.

### Reproducing from a clean clone

A clean clone is the only honest test of "source-ready". It has no `godot/.godot/` import cache, no untracked files, no user data you forgot about, and no editor state. The procedure is short. Clone the committed revision into an empty folder. Import. Run every documented check with the documented flags. Run the main scene briefly. Compare what the import generated with what is committed. `walker-jumpman-clawd` adds one more habit: `scripts/clawd-build.cjs` records a SHA-256 for every file under `godot/`, plus a combined `build_id`. It also refuses to run if files the iteration promised to preserve have changed. We ran it on a clean clone of the published commit `382f2ba`. It produced the same `build_id`, `91580b18…`, as the committed manifest. The source is identical, byte for byte.

Two cautions from [Chapter 0's time trap](00-the-toolchain.md#the-time-trap-frames-are-not-seconds): run frame-counted tests with `--fixed-fps 60`, and read the log, not just the exit code.

### Save data: where it lives, and how it ages

**Where.** `res://` is your project folder. `user://` is a per-project folder that is "guaranteed to be writable to, even in an exported project". On macOS it is `~/Library/Application Support/Godot/app_userdata/[project_name]` ([File paths](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html)). The name comes from `application/config/name`, unless `application/config/use_custom_user_dir` gives the folder its own name ([ProjectSettings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html)). That is why your scratch copy, your clone and your real game share one save folder when their project names match.

**Format.** Godot's [saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html) tutorial offers JSON, or binary with `FileAccess.store_var`/`get_var`, or `ConfigFile` for settings. JSON is readable and diffable, but "Vector2 is not supported by JSON", so you convert. Binary handles most types. There is one security line to remember. `get_var` can deserialize objects if you allow it, and "Deserialized objects can contain code which gets executed. Do not use this option if the serialized object comes from untrusted sources" ([FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html)). `walker-loading-serialization` adds its own note: treat a `ConfigFile` save as trusted local data, "not a safe arbitrary-object import."

**Failure.** `FileAccess.open()` returns `null` on failure, and `get_open_error()` says why. A file is flushed when it is closed or freed, but not if the process is killed, so call `flush()` for data you cannot lose ([FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html)). `DirAccess.rename()` overwrites a destination that "exists and is not access-protected" ([DirAccess](https://docs.godotengine.org/en/stable/classes/class_diraccess.html)). That makes "write a temporary file, then rename it over the old one" a reasonable pattern: a crash mid-write leaves the old file intact. We did not test a crash.

**Versioning.** A save file outlives the code that wrote it. The rules that matter:

1. Put a `version` in the file, and read it **first**, before trusting anything else in the document.
2. A version newer than you understand came from a newer build. Do not "repair" it, and never overwrite it.
3. Validate the whole snapshot before changing any live state. `walker-loading-serialization` learned this the hard way. Before its fix, 9 of 28 negative checks failed. The loaders applied part of a snapshot, hit an assignment error on the rest, and left "partial state changes and leaked nodes". After a shared validator that checks everything before mutating anything, all 28 pass.
4. Tests must never read or write the player's real save.

Rule 4 is easy to state and, as "What we actually ran" shows, easy to break without noticing.

### Menus and accessibility basics

The Walker GUI builds give you concrete, tested patterns:

- **Keyboard focus from the first frame.** Godot's [navigation guide](https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html) says "any node must be focused by using code when the scene starts", for example `$StartButton.grab_focus.call_deferred()`, because not everyone can use a mouse. `walker-gui-accessibility` grabs focus in `_ready()`, and its test drives 8 Tab transitions through every control and back.
- **Names and live regions.** A `Control` has `accessibility_name`, "the human-readable node name that is reported to assistive apps", and `accessibility_live`, for text that updates while focus is elsewhere ([Control](https://docs.godotengine.org/en/stable/classes/class_control.html)). Godot 4.5 added screen reader support to Control nodes through AccessKit. The release notes call it "in its experimental phase" ([Godot 4.5](https://godotengine.org/releases/4.5/)).
- **Custom controls need custom work.** `walker-gui-accessibility`'s three-item list reports its role, items and values through `NOTIFICATION_ACCESSIBILITY_UPDATE`. Its Walker adaptation fixed a real input bug. Pressing left at item 0 selected index −1 instead of wrapping to 2, and `posmod` fixed it. The README is exact about the limit: "headless tests do not verify VoiceOver speech or native accessibility-tree integration."
- **A drawn HUD is invisible to assistive technology.** `walker-jumpman-clawd`'s HUD is one `Control` that paints every word with `draw_string`, with `mouse_filter` set to ignore. None of that text is a `Label` or a `Button`, so none of it has an accessible name. The best-time line you add in this chapter inherits that. We did not test a screen reader. The structure alone tells you what one would find.
- **First impressions.** `walker-gui-custom-splash-screen` turns off the engine's boot image (`boot_splash/show_image=false`, black background). It then plays its own splash scene and switches with `change_scene_to_packed(load("res://main.tscn"))`. The comment says it uses `load()` rather than `preload()` "to avoid delaying the splash screen's appearance". Its 11 headless assertions cover the timing and the transition. The particles and the look are unverified.
- **Controls you did not wire.** `walker-gui-control-gallery` passes 35 control and state checks. Its log also records something a demo can hide: "Do not claim menu check items toggle automatically: source has no signal handlers."

### The final Brutalist film

The course's [explainer policy](../prerequisites/brutalist-godot-explainers.md) offers three skills. For a final project you are defending, pick by the claim. `godot-walkthrough` shows what the game does when played. `godot-gamedev` shows how it is built, as an input → state → output trace with tests. `godot-gdd` shows why it is specified that way, with a "clear separation of proposals, implemented features, tests, and pending human decisions". Week 15's "defend its design and evidence" usually means `godot-gdd`, often with a walkthrough. The policy treats the film as code. The beat sheet and script live in GitHub. The rendered file lives in designated media storage, identified by "filename and checksum". The README links that exact version.

---

## The Walker example: `walker-jumpman-clawd`

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman), [`walker-loading-serialization`](https://github.com/nikbearbrown/walker-loading-serialization), [`walker-gui-accessibility`](https://github.com/nikbearbrown/walker-gui-accessibility), [`walker-gui-custom-splash-screen`](https://github.com/nikbearbrown/walker-gui-custom-splash-screen), [`walker-gui-control-gallery`](https://github.com/nikbearbrown/walker-gui-control-gallery), [`walker-pong`](https://github.com/nikbearbrown/walker-pong), [`walker-loading-runtime-save-load`](https://github.com/nikbearbrown/walker-loading-runtime-save-load). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** Professor Bear's evolving Assignment 1 example: the `walker-jumpman` First Steps level with the Clawd mascot as the player. It is public at [github.com/nikbearbrown/walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd). The starter it forked, [walker-jumpman](https://github.com/nikbearbrown/walker-jumpman), was pinned at commit `9387542`. `SOURCES.md` records that the mascot's 18 animations are a GDScript port of Brutalist's `ClaudeMascotScene.tsx`, "not an Anthropic product or endorsement", and that the repository "does not add a blanket license to inherited work whose license has not been established."

**Why it is the Week 15 example.** It carries the whole cycle as documents:

| File | Stage | What it records |
|---|---|---|
| `GAME-BRIEF.md` | brief | the promise, "I can see why that failed, and I want one more try", scope, what is proposed and not built |
| `GDD.md` | brief | 16 sections, 12 features (FEAT-10 is "Persistent personal best result"), 22 acceptance cases |
| `PRODUCTION-PLAN.md` | build | 22 dependency-ordered tickets. WJ-D02, the personal best, is deferred with "write migration/corruption/reset rules before implementation" |
| `BUILD-REPORT.md` | build / inspect | the first 25-check run found 4 failures, including a phantom second death from stale `Area2D` contacts; the fix and the rerun |
| `PLAYTEST-PLAN.md` | playtest | fixtures, a no-coaching human protocol, "Keep empty forms empty until used" |
| `DESIGN-REVIEW.md` | inspect | what the document checks establish, and "No Godot process or gameplay test ran" |
| `CHANGE-BRIEF.md`, `FRICTIONAL.md` | revise | three predictions for the Clawd iteration; real failures, such as a 343-frame capture where 540 were expected |
| `evidence/` | all | JSON receipts per run, never overwritten |

**What its checks establish.** Run as its README says, with `--fixed-fps 60`: 25 mechanics checks, 9 keyboard checks, and a 1,950-comparison animation-parity check. The deterministic route reaches the flag with zero deaths. `CLAWD-STATUS.json` is explicit about what is not done: `"human_playtest": "pending"`, `"level_extension": "not implemented"`, `"assignment_1_complete": false`.

**Supporting builds for this chapter** (from `godot-demo-projects` at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`; each Walker build is public at `github.com/nikbearbrown/<build name>`):

| Build (upstream path) | What it adds | Recorded checks | Recorded limit |
|---|---|---|---|
| `walker-loading-runtime-save-load` (`loading/runtime_save_load`) | loading images, audio, fonts, glTF and ZIP at run time; exporting them back | 28 loading, 20 export and scene-state, 30 missing-file, 15 corrupt-file checks | "Export permission failures remain an untested edge case" |
| `walker-loading-serialization` (`loading/serialization`) | ConfigFile and JSON saves of player and enemies | 12 round-trip, 28 negative and 42 validator checks | "saves are not atomic and disk-full handling is not proved" |
| `walker-gui-accessibility` (`gui/accessibility`) | focus, names, a live region, a custom accessible list | 8 Tab transitions, wrap, bounds | screen reader output unverified |
| `walker-gui-control-gallery` (`gui/control_gallery`) | every standard Control | 35 control and state checks | rendered layout unverified |
| `walker-gui-custom-splash-screen` (`gui/custom_splash_screen`) | a boot-to-splash-to-main sequence | 11 real-time assertions | particle look, real restart unverified |

---

## Hands-on: a persistent best time, reproduced and exported

### Predict

1. The game's existing tests create the session with default settings, and you may not edit them. Once the game saves a best time on completion, where will those tests' "completions" be saved? Which test "completes" a run in a few physics ticks?
2. A save file says `"version": 2` and also uses a different `"level"` name. Your code checks `level` before `version`. What happens on the next completion?
3. You clone your own repository into an empty folder and import. Which files will Godot create that are not in the commit? Should they be committed?
4. `export_presets.cfg` is committed and valid. What will `--export-release "Web"` do on a machine with no templates? What will `--export-pack` do?

### Build It

Get your own copy of the public repository:

```bash
git clone https://github.com/nikbearbrown/walker-jumpman-clawd.git
```

Record the baseline from inside the clone. The first three checks are the README's:

```bash
timeout 120 godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_keyboard.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_clawd.gd --fixed-fps 60
```

Expect `WALKER TESTS: 25 checks / 0 failures`, nine JSON lines with `"status":"PASS"`, and `"checks":1950,"failures":0`. We did our work in a scratch copy containing only `godot/` and the Markdown files, committed as baseline `48bd764`. That copy did not include `scripts/`, which turns out to matter.

The prompt turns WJ-D02's "write migration/corruption/reset rules before implementation" into rules. Writing those rules is the design work. Paste it into Claude Code:

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

The command we ran, with the prompt saved one folder up:

```bash
claude -p "$(cat ../prompt-best-time.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > ../session.jsonl
```

`--strict-mcp-config` loads no MCP servers beyond an explicit list (`claude --help`). The settings string was meant to keep this throwaway session out of Claude Code's automatic memory, and we did not verify its effect. You need neither.

After our own verification (below), the correction went into the **same** session with `--resume`, so the agent kept its context. The session ID came from the first transcript's `init` event:

```bash
claude -p "$(cat ../prompt-best-time-fix.txt)" --resume ae769ccf-812c-460e-896e-fd82e64b77c2 --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*)" --max-turns 60 --output-format stream-json --verbose --strict-mcp-config --settings '{"autoMemoryEnabled":false}' > ../session-fix.jsonl
```

The correction prompt is in [`examples/15-final-projects-brief-to-export/PROMPTS.md`](../examples/15-final-projects-brief-to-export/PROMPTS.md). It states the observed facts and the rule each one broke, then asks for the smallest fix. It does not describe the code it wants.

**The Codex difference.** We did not run Codex for this chapter. In Chapter 4, Codex's `workspace-write` sandbox reported that Godot could not write under `user://`, which on macOS is outside the project. So the same sandbox should have blocked this chapter's accidental writes to the real save folder. It should also have made normal-mode saving fail inside the sandbox. Neither is tested. If you use Codex, check which of your saves actually landed where.

### Use It

These are the human checks. Record what you see:

1. Open `godot/project.godot` in Godot 4.7.2 and play (F5). Finish the course. Does the complete panel show your time and a best? Is the line readable at 640 × 360 scaled to your window? The detail line got longer, and nothing checks whether it fits.
2. Quit, relaunch, finish more slowly. The best must not change. Finish faster. It must.
3. Open `best_time.json` in the user data folder in a text editor. On macOS that is `~/Library/Application Support/Godot/app_userdata/walker-jumpman-clawd/`; the [File paths](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html) page lists the other systems. Does it match the schema in the prompt?
4. Play the menu with the keyboard only, then with a screen reader if you have one: VoiceOver on macOS, Narrator or NVDA on Windows. Write down what it announces. Given how the HUD is drawn, expect little.
5. Read `export_presets.cfg`. Is `tests/*` really excluded? Is the gallery scene meant to ship? The pack listing below says it does.

### Ship It

Commit the change and your own check separately:

```bash
git add -A
```

```bash
git commit -m "FEAT-10: persistent personal best under WJ-D02 save rules"
```

```bash
git add godot/tests/verify_best_time_rules.gd godot/tests/verify_best_time_rules.gd.uid
```

```bash
git commit -m "Add reviewer's save-rule check (human-written)"
```

Commit the `.uid` files Godot generates for your scripts. The `.uid` for your own check exists only after an `--import` following its creation. We forgot it, and the clean-clone import re-created it as an untracked file.

Then run the project's own invariant script from the full repository. It is not in a `godot/`-only copy:

```bash
node scripts/clawd-build.cjs
```

It will fail, as it should. The first Clawd iteration promised that `godot/ui/hud.gd` stays byte-identical, and FEAT-10 changes it. Whether to update that invariant is a design decision with an owner. Record it in `CHANGE-BRIEF.md`. Don't just delete the line that complains.

Your `FRICTIONAL.md` entry should record which predictions were right, the false claim, how you found it, the stray file, the fix, and what is still unverified. For the film, `godot-gdd` defends FEAT-10's rules against evidence: planned, built, tested, pending. `godot-walkthrough` shows the best time surviving a restart. Identify the film by filename and SHA-256, and give the game revision it shows.

### Verify

On macOS, point `HOME` at a scratch folder for every test run. That moves `user://` out of your real data. We confirmed it with Godot 4.7.2 on macOS: `OS.get_user_data_dir()` followed `HOME`. We did not test Windows or Linux.

```bash
mkdir -p ../scratch-home
```

First the three original suites, then look in the scratch user folder. There should be no `best_time.json`:

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

Then the two save-rule tests. After the reviewer check there should be a `best_time.json`, because its case E plays in normal mode on purpose:

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/test_best_time.gd --fixed-fps 60
```

```bash
HOME="$PWD/../scratch-home" timeout 120 godot --headless --path godot --script res://tests/verify_best_time_rules.gd --fixed-fps 60
```

Reproduce from a clean clone. Replace the placeholder with your repository's path or URL:

```bash
git clone <your-repository> ../repro-check
```

Then, inside `../repro-check`:

```bash
godot --headless --path godot --import
```

```bash
git status --short
```

Run every test as above. Then attempt the export. The target folders must exist first:

```bash
mkdir -p build/web build/pack
```

```bash
godot --headless --path godot --export-release "Web" ../build/web/index.html
```

```bash
godot --headless --path godot --export-pack "Web" ../build/pack/game.zip
```

**What a pass proves:** a named commit is source-ready on Godot 4.7.2 on this Mac. The save rules hold for the cases tested. The unchanged suites no longer touch `user://`. The export preset is valid enough for Godot to look for templates. **What it does not prove:** that the Web export runs in any browser, since nobody has built it, that a crash between write and rename is safe, that a screen reader can read the result, or that anyone cares about a best time. And "slower completion does not replace the best" is still tested with a fixture, not a real slower route.

---

## What we actually ran

**Date and tools.** 27 September 2026 on the course Mac. Godot 4.7.2.stable.official.ed1daf0bf. Claude Code 2.1.150 with its print-mode default model, `claude-sonnet-4-6`. Scratch copy of `walker-jumpman-clawd`, holding `godot/` byte-identical to published commit `382f2ba` plus the Markdown files, as baseline `48bd764`. Baseline: 25/25, 9/9, and 1,950 comparisons with 0 failures.

**First pass: 31 turns, 9 minutes, CLI-reported cost $1.23** ([transcript](../examples/15-final-projects-brief-to-export/claude/session.md)). The agent added `best_time_path` (default `user://best_time.json`) and `_load_best()`, which rejects wrong JSON, format, level and values with warnings. It added `_save_best()`, which writes `best_time.json.tmp` and renames it, and updates the best only if the save succeeds. The HUD's complete panel gained a `best %.1f s` field. It also wrote a 31-check `test_best_time.gd` and a `Web` preset (`export_filter="all_resources"`, `exclude_filter="tests/*"`). It reported all four suites passing. Among "what these tests cannot tell us", it wrote: "No test writes to or reads the player's actual `user://best_time.json`."

**Our verification found three problems.**

1. **The claim was false.** After our first verification run, `~/Library/Application Support/Godot/app_userdata/walker-jumpman-clawd/best_time.json` existed, containing `"best_seconds":0.0666666666666667`. The file had been created at 14:11 local time, during the agent's own test runs, and rewritten at 14:17 by ours. We repeated the runs with `HOME` pointed at a scratch folder. The unchanged `test_game.gd` saved `5.46666666666665` from its real route. The unchanged `test_keyboard.gd` saved `0.0666666666666667` (`logs/11-first-pass-existing-suites-write-user-data.log`), because its `resolve_contacts(false, true)` fixture "finishes" the course 4 physics ticks (0.0667 s) after its last restart. The agent had made the path *settable*, as asked. But the old tests never set it, and the prompt forbade editing them. Our prompt had a gap, and the agent's summary papered over it.
2. **The version rule broke when another field changed.** Our check, [`verify_best_time_rules.gd`](../examples/15-final-projects-brief-to-export/reviewer/verify_best_time_rules.gd), wrote a version-2 file with the level renamed, completed the route, and compared bytes. The file had been overwritten. `_load_best()` checked `format` and `level` before `version`, returned "wrong level", and never set the "newer build" flag. A renamed `format` failed the same way. The agent's own version-2 case had changed only the version, so it passed.
3. **The agent's test proved less than its labels said.** Case 01 reused a fixed directory. We ran the test twice: the second run passed all 31 checks while the case 01 file kept its first-run timestamp, so "file exists" passed without anything being written (`logs/16-first-pass-case01-stale-file-second-run.log`). A check named `hud-best-field-set` tested nothing about the HUD.

**Second pass: 8 turns, 3.5 minutes, $0.76.** The corrected `session.gd` defaults to an empty path. `_ready()` resolves it to `user://best_time.json` only when `test_mode` is false. `_load_best()` reads `version` immediately after the dictionary check. The test now uses a per-run timestamped directory, adds both version-2 cases, and drops the empty check: 38 checks. The real save file's timestamp stayed at 14:17 through the second session, so the fixed suites wrote nothing to it.

**Our checks on the final commit**, with `HOME` sandboxed. Logs are in [`examples/15-…/logs/`](../examples/15-final-projects-brief-to-export/logs/).

| Check | First pass | Final |
|---|---|---|
| `test_game.gd` / `test_keyboard.gd` / `test_clawd.gd` | 25/25, 9/9, 1950/0 — **but wrote `user://best_time.json`** | 25/25, 9/9, 1950/0; no save file created |
| agent's `test_best_time.gd` | 31/31 | 38/38 |
| our `verify_best_time_rules.gd` (13 checks) | **2 failures** (cases B and C: version-2 files overwritten) | 13/13, including normal play writing `user://best_time.json` inside the sandboxed `HOME` |

One run we cannot explain. On one execution of our check against the first-pass code, in a freshly created `HOME`, normal play printed `best_time: rename failed with error 1` and left `best_time.json.tmp` behind. Two reruns of that code, and sixteen probe runs of the final code in fresh `HOME`s, did not reproduce it. Five of those runs are saved in `logs/22-final-normal-play-probe.log`. The log is kept as `logs/13-first-pass-reviewer-one-off-rename-failure.log`. An unexplained failure goes in the record, not in the bin.

**Clean-clone reproduction** of the final scratch commit `35f1ec4`. The import exited 0, and `git status` showed one untracked file, `godot/tests/verify_best_time_rules.gd.uid`, the one we forgot. All five suites passed, and the main scene ran 120 frames with exit 0. For comparison, a clean clone of the published `382f2ba` passed its three suites *without* importing. It created no `.godot/` folder, because the game draws everything in code and has nothing to import. Its manifest reproduced `build_id 91580b18…`. We then applied our change to that clone and ran `node scripts/clawd-build.cjs`:

```text
Error: Invariant changed: godot/ui/hud.gd
```

The project's own guard caught what our `godot/`-only copy could not see.

**Export attempts.** On the published commit, which has no preset:

```text
ERROR: This project doesn't have an `export_presets.cfg` file at its root.
Create an export preset from the "Project > Export" dialog and try again.
```

With the agent's preset:

```text
ERROR: Cannot export project with preset "Web" due to configuration errors:
No export template found at the expected path:
~/Library/Application Support/Godot/export_templates/4.7.2.stable/web_nothreads_debug.zip
No export template found at the expected path:
~/Library/Application Support/Godot/export_templates/4.7.2.stable/web_nothreads_release.zip
ERROR: Project export for preset "Web" failed.
```

Exit code 1. That error is the evidence for "not export-ready here". It also tells you what to install: the **Godot 4.7.2 export templates**, through Editor → Manage Export Templates, which provides the Web template files named above. After that, build again, serve the output, and play it in browsers you name. We did not download templates.

`--export-pack` needs no templates. On the final commit's clean clone it exited 0 and wrote a 24,926-byte ZIP and a 25,396-byte PCK (SHA-256 `656bbec6…`). The ZIP lists 20 entries. The scripts are compiled to `.gdc`, `levels/first_steps.json` is included, nothing from `tests/` is, and the diagnostic `gallery/clawd_gallery` scene *is*. `godot --headless --main-pack walker-jumpman-clawd.pck --quit-after 120` ran it with the editor binary and exit 0. That shows the packed data loads. It is not an exported game.

**A stray file.** The first pass left `best_time.json` holding 0.0667 s in Professor Bear's real `app_userdata/walker-jumpman-clawd/` folder. The published game has no FEAT-10 code, so it never reads the file. We left it in place. Deleting it is his call.

---

## Check your understanding (ungraded)

1. Open `godot/tests/test_keyboard.gd`. Which line "completes" the course, after how many physics ticks, and why would that be a harmless fixture before FEAT-10 and a data-corrupting one after it?
2. Reorder `_load_best()`'s checks so `level` comes before `version` again. Which case in `test_best_time.gd`, and which in `verify_best_time_rules.gd`, fails? Why didn't the agent's original case 09 fail?
3. List the files an `--import` of a fresh clone of your final project creates. Which should be committed, and which are caches?
4. Run `--export-pack` on your final project and list the ZIP. Name one file that ships and should not, and one that must ship and would break the game if excluded.
5. The HUD draws its text with `draw_string`. Sketch the smallest change that would let a screen reader announce "Course complete, 5.4 seconds, best 5.4 seconds", and name the Control properties involved.
6. `scripts/clawd-build.cjs` says `Invariant changed: godot/ui/hud.gd`. Write the two-sentence `CHANGE-BRIEF.md` entry that justifies changing the invariant. Or explain why FEAT-10 should not touch the HUD.

---

## Doing the same thing in Unity

*Unity was not run for this chapter. The comparisons come from Unity's official documentation (the Unity 6 manual, 6000.x), the Unity Hub documentation and the Unity Test Framework manual, checked on 27 September 2026.*

### Similarities

- **Per-user save folders outside the project.** [`Application.persistentDataPath`](https://docs.unity3d.com/ScriptReference/Application-persistentDataPath.html) is Unity's `user://`. On a macOS player it is `~/Library/Application Support/unity.company name.product name`, and Unity's docs tell you to build full paths with `Path.Combine`. It is named from the company and product names, so two builds with the same names share it. That is the same trap as `config/name`.
- **Build configuration as a committable file.** In Unity 6 a [build profile](https://docs.unity3d.com/6000.4/Documentation/Manual/build-profiles.html) (File → Build Profiles) is "a set of configuration settings you can use to build your application on a particular platform", saved "as an asset file that is ready for use with version control", the role of `export_presets.cfg`.
- **A separate per-platform install.** Unity's platform build support is an Editor **module** that you add through the Hub (Installs → Manage → Add modules). You can only add modules to Editors the Hub installed ([Hub docs](https://docs.unity.com/en-us/hub/add-modules)). That is the equivalent of export templates, including the "you have the editor but not the target" failure.
- **Screen readers are opt-in engineering.** Unity's [Accessibility module](https://docs.unity3d.com/6000.4/Documentation/Manual/accessibility/module-intro.html) lets an app "communicate with native screen readers" on Android, iOS, Windows and macOS. You build an accessibility hierarchy separate from your GameObjects, much as Godot's custom control fills in accessibility data by hand.

### Differences

- **Headless build and test.** Build from a script called with `-batchmode -executeMethod … -quit` ([command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html)). `-batchmode` runs "without the need for human interaction", and `-quit` "can hide some error messages", so read the log. The script calls [`BuildPipeline.BuildPlayer`](https://docs.unity3d.com/ScriptReference/BuildPipeline.BuildPlayer.html), using the overload that "accepts BuildPlayerWithProfileOptions" if you use build profiles. It returns a `BuildReport` with Succeeded or Failed. Test the save round trip in a Play Mode test run with `-runTests -testPlatform PlayMode` ([Test Framework CLI](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)). Godot needs neither a build script nor a test package: `--export-release` and `--script` are built in.
- **The convenient store is not a file you control.** [`PlayerPrefs`](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html) stores strings, floats and ints in a macOS `.plist` or the Windows registry, "without encryption. Don't use PlayerPrefs data to store sensitive data." It has no version field unless you add one. A versioned JSON file in `persistentDataPath` is the closer match to this chapter's design.
- **What an agent can review.** Scenes and prefabs are YAML text by default (Chapter 4), and a build profile is saved as a project asset. Build scripts and save code are C#. All of these are diffable. The installed modules are not in the project at all.

| Godot | Unity |
|---|---|
| `user://` | `Application.persistentDataPath` |
| `export_presets.cfg` | build profile asset (Unity 6) |
| export templates | platform build-support modules (Hub) |
| `--export-release` | `-batchmode -executeMethod` → `BuildPipeline.BuildPlayer` |
| `ConfigFile` / JSON / `store_var` | `PlayerPrefs` / JSON (`JsonUtility`) / your own binary |
| `accessibility_name`, AccessKit | Accessibility module, `AccessibilityHierarchy` |
| `godot --headless --script` test | Play Mode test via `-runTests` |

## Doing the same thing in Unreal Engine

*Unreal Engine was not run for this chapter. The comparisons come from Epic's Unreal Engine 5 documentation (5.8 at the time of checking), checked on 27 September 2026. Unreal is source-available under the Unreal Engine EULA, not open source ([source access](https://dev.epicgames.com/documentation/en-us/unreal-engine/downloading-source-code-in-unreal-engine)).*

### Similarities

- **Save objects with slots.** A `USaveGame` subclass holds the fields. `SaveGameToSlot` "simply saves the game immediately and returns a `bool` indicating success or failure", and `LoadGameFromSlot` "will create and return a `USaveGame` object if it succeeds" ([saving and loading](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine)). On development platforms the files are `.sav` files in the project's `Saved\SaveGames` folder. You still own the version field and the rules for newer files.
- **Packaging is a separate, checked step.** You package from the Platforms menu with "Package Project". Cooking "prepares game content so that it can be run outside of the Unreal Editor", and there are Development and Shipping configurations ([packaging](https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project)). That is the same source-ready versus export-ready distinction.
- **Screen readers need explicit support.** "UE now supports third party screen readers for Windows or VoiceOver on iOS". You enable it with `Accessibility.Enable=1`, and common UMG widgets have built-in support. The docs call it an "**Experimental** feature" ([screen readers](https://dev.epicgames.com/documentation/unreal-engine/supporting-screen-readers-in-unreal-engine)). Godot's AccessKit support is also experimental.

### Differences

- **The command-line build is UAT, not the editor binary.** You package headlessly with `RunUAT.sh BuildCookRun -project=… -clientconfig=Development …` from `Engine/Build/BatchFiles` ([build operations](https://dev.epicgames.com/documentation/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine?lang=en-US)). The step includes a cook that converts every asset for the platform. Godot's `--export-release` is one flag on the editor binary.
- **Platform SDKs, not just templates.** "Developing and packaging for some target platforms, such as Linux, mobile, and XR platforms, may require additional Software Development Kits", and consoles need "a source code build of the Unreal Engine" ([packaging](https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project)).
- **Asynchronous saving is the documented default.** The docs recommend `AsyncSaveGameToSlot`, to avoid "a sudden framerate hitch" and a possible certification issue. This chapter's Godot save is synchronous, which is fine for one small JSON file written on a results screen.
- **Reviewability.** A `USaveGame` in C++ is text an agent can diff. A Blueprint save graph is a binary `.uasset` (Chapter 4). Reproducing a build from a clean clone also means cooking every binary asset, which takes far longer than Godot's import.

| Godot | Unreal Engine 5 |
|---|---|
| `user://best_time.json` | `USaveGame` in a slot (`Saved/SaveGames/*.sav` on development platforms) |
| temp file + `DirAccess.rename` | `SaveGameToSlot` / `AsyncSaveGameToSlot` |
| `export_presets.cfg` + templates | project packaging settings + platform SDKs; launch profiles |
| `godot --export-release` | `RunUAT BuildCookRun` |
| import cache `.godot/` | cooked content |
| `accessibility_name`, AccessKit | UMG accessibility settings, `Accessibility.Enable=1` |
| `godot --headless --script` test | `-ExecCmds="Automation RunTest …;Quit"` (Chapter 4) |

---

## Sources

Official documentation first. Godot pages are the `stable` manual, checked on 27 September 2026 against Godot 4.7.2 on the course Mac.

**Godot**
- [Exporting projects](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html); [Exporting for the Web](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_web.html); [Command line tutorial](https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html)
- [File paths in Godot projects](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html); [Saving games](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html); [FileAccess](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html); [DirAccess](https://docs.godotengine.org/en/stable/classes/class_diraccess.html); [ConfigFile](https://docs.godotengine.org/en/stable/classes/class_configfile.html); [ProjectSettings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html)
- [Keyboard/Controller navigation and focus](https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html); [Control](https://docs.godotengine.org/en/stable/classes/class_control.html); [Godot 4.5 release notes: screen readers via AccessKit](https://godotengine.org/releases/4.5/)
- Demo source: [godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects) at `a3b5c113112f77291d5f3d1360f33a882fdc52f7`

**Walker and course records (read on 27 September 2026)**
- [walker-jumpman-clawd](https://github.com/nikbearbrown/walker-jumpman-clawd) at `382f2ba`: `README.md`, `GAME-BRIEF.md`, `GDD.md`, `PRODUCTION-PLAN.md`, `BUILD-REPORT.md`, `PLAYTEST-PLAN.md`, `DESIGN-REVIEW.md`, `CHANGE-BRIEF.md`, `FRICTIONAL.md`, `SOURCES.md`, `CLAWD-STATUS.json`, `scripts/clawd-build.cjs`
- `walker-loading-runtime-save-load`, `walker-loading-serialization`, `walker-gui-accessibility`, `walker-gui-control-gallery`, `walker-gui-custom-splash-screen`: `README.md`, `FRICTIONAL.md`, scripts
- `walker-demo-series/queue.json`
- Course: [Module 1 lesson](../modules/01-walker-and-godot/lesson.md); [Required Brutalist Godot explainers](../prerequisites/brutalist-godot-explainers.md); [assessment policy](../prerequisites/assessment-policy.md)
- This chapter's run: [`examples/15-final-projects-brief-to-export/`](../examples/15-final-projects-brief-to-export/)

**Unity** (documentation-based; Unity was not run for this chapter; checked 27 September 2026)
- [Application.persistentDataPath](https://docs.unity3d.com/ScriptReference/Application-persistentDataPath.html); [PlayerPrefs](https://docs.unity3d.com/ScriptReference/PlayerPrefs.html)
- [Introduction to build profiles](https://docs.unity3d.com/6000.4/Documentation/Manual/build-profiles.html); [BuildPipeline.BuildPlayer](https://docs.unity3d.com/ScriptReference/BuildPipeline.BuildPlayer.html); [Editor command-line arguments](https://docs.unity3d.com/Manual/EditorCommandLineArguments.html)
- [Unity Hub: add modules](https://docs.unity.com/en-us/hub/add-modules)
- [Accessibility module](https://docs.unity3d.com/6000.4/Documentation/Manual/accessibility/module-intro.html)
- [Unity Test Framework command line](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)

**Unreal Engine** (documentation-based; Unreal was not run for this chapter; checked 27 September 2026)
- [Saving and loading your game](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine)
- [Packaging your project](https://dev.epicgames.com/documentation/en-us/unreal-engine/packaging-your-project); [Build operations: cooking, packaging, deploying and running](https://dev.epicgames.com/documentation/unreal-engine/build-operations-cooking-packaging-deploying-and-running-projects-in-unreal-engine?lang=en-US)
- [Supporting screen readers](https://dev.epicgames.com/documentation/unreal-engine/supporting-screen-readers-in-unreal-engine)
- [Downloading source code](https://dev.epicgames.com/documentation/en-us/unreal-engine/downloading-source-code-in-unreal-engine) (Unreal Engine EULA)
