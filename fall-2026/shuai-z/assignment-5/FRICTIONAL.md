# FRICTIONAL — Assignment 5, walker-rudy

What I tried, what I expected, what happened, how I checked it, what I did about it, and what I learned, with my work and Claude's kept apart.

**How this file is written.** Claude Code drafts each entry from our Claude Code conversation, and I check it against what I actually did. Where I recorded no expectation or lesson, the entry says so instead of inventing one. Each entry says when it was written; entries written after the event are labelled as retrospective.

**Tools.** Claude Opus 5.5 in Claude Code (desktop app), Claude Code 2.1.302; Godot 4.7.2; macOS.

---

## 2026-10-22 — Reading the assignment against my project

*Retrospective, written on 2026-10-24, from the conversation.*

- **Attempt (me):** I pasted the assignment and asked Claude, in Chinese, what to do step by step.
- **What Claude found, by reading my folders and the course repository's chapters:**
  - My game is 2D and uses GL Compatibility; my 3D scene is a separate Forward Plus project. So the shader from code goes in the game, and the textured shader goes in the props scene.
  - Two of the game's existing checks rule out a new material on the obvious objects. `checks.gd` lines 871–877 keep the outline on Rudy's sprite. Lines 1056–1061 allow a material only on the spikes and the goblin.
  - The props scene's check, `check_props.gd` lines 85–89, reads each `.glb`'s own material colours, so the importer's Use External would make it fail.
  - The course's wrapper cannot run as given, for three reasons:
    - `godot` is not on my PATH;
    - it hard-codes `--path godot`;
    - the game's checks are a scene (`checks.tscn`), which `--script` cannot run.
  - The new branch must start from `a3`, not from my Assignment 4 branch, whose GDD commit stays off GitHub.
  - The course repository's own `assignments/05-shader-and-material.md` is an older draft; I follow the Canvas text.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude read the files and wrote the plan; I asked for it.

## 2026-10-24 — Step 0: the folder, the wrapper and the baselines

*Written on 2026-10-24, from the conversation. Commits `84658acf` and `cca08046`.*

- **Attempt (Claude, at my request):**
  - Branched `shuai-z/assignment-5` from `a3`.
  - Copied `assignment-2/game` and `assignment-3/godot` into `assignment-5/` with `git archive`, so only committed files came across: 133 and 14 files, the same as in `a3`.
- **A problem found on the way (Claude):** the course repository's root `.gitignore` ignores `*.wav`. The game's six sound effects are tracked only because Assignment 2 force-added them. A plain `git add` of the copy would have left them out, and a fresh clone would then fail the game's check that every file it names exists. Claude added an exception for `game/systems/audio/sfx/*.wav` to this folder's `.gitignore`.
- **The wrapper (Claude):** the course's `scripts/run-test.sh`, changed in four places, which are listed at the top of the script:
  - the project is an argument;
  - a `.tscn` test runs as a scene;
  - Godot is found when it is not on PATH;
  - it runs from this folder wherever it is called from.
- **Checks (Claude):**
  - Both imports exited 0 in 3–4 s with no error line. Afterwards neither copy differed from its source (`diff -rq`, ignoring `.godot/`).
  - Baselines at 60 fps through the wrapper: the game's `checks.tscn`, 141 PASS and 0 FAIL; the props scene's `check_props.gd`, 44 ok and 0 FAIL. These are the counts Assignments 2 and 3 recorded. Logs: `logs/`.
  - The game's log ends with `WARNING: 41 ObjectDB instances were leaked at exit` and `ERROR: 8 resources still in use at exit`. Assignment 2's test report already explains these as the headless audio driver, not the game. The wrapper does not fail on them.
- **My decisions:**
  - I held the step 0 commits until the brief had been reviewed.
  - I asked for `godot` to be put on my PATH. Claude wrote a two-line shim at `/opt/homebrew/bin/godot`, and `godot --version` printed `4.7.2.stable.official.ed1daf0bf`.
- **Differs from the assignment:**
  - The wrapper's arguments are `<game|godot> <test> <fps>`.
  - The layout: this folder in the course repository plays the part of the `walker-` repository's root, as in Assignment 3.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude did all of step 0 and its checks; I asked for it and chose when to commit.

## 2026-10-24 — Step 1: the change brief

*Written on 2026-10-24, from the conversation. Commit `fc9cd523`.*

- **Attempt (me):** I asked Claude to draft a complete CHANGE-BRIEF.md for me to review.
- **First draft (Claude):** everything except the colour line, the predicted values and the short answers. It left those blank because the assignment asks for them from me.
- **Second draft (Claude):** I asked it to fill them in as well, since this course expects us to use AI and I would review the result. Claude filled them in and wrote at the top of the brief that it had drafted all of it.
- **Choices Claude made, with its reasons in the brief:**
  - The hearts (`Hud/Hearts`) carry the shader from code instead of Rudy, because of the two existing checks above.
  - The state is the invulnerable window after a hit or a respawn. The hearts take the lit waystone's blue, fading as the window runs out.
  - The timing comes from the game's code. The spikes and goblins hit Rudy before his own countdown in the same physics tick. So the first frame shows 71/72 = 0.986, and the tint is visible for 71 ticks, 1.183 s.
  - With `Engine.time_scale` at 0.5, the tint lasts 2.4 s, because 64-bit rounding adds one tick (checked in Python).
  - The textured shader uses Poly Haven's Rock 01, by Rob Tuytel, CC0; Claude checked it on the Poly Haven API and licence page. It goes on the waystone's Stone and the circle's DarkStone surfaces, attached as overrides rather than through Use External.
- **A design value changed by a computation (Claude):** at `tint_strength` 0.6, the heart's outline would fall to 2.1:1 contrast against the sky beside it at full tint. At 0.4 it stays at 3.5:1, above 3:1, so the brief uses 0.4.
- **Review (me):** I reviewed the brief and found no problems.
- **One change before the commit (Claude):** the note at the top said I had checked the predicted values by hand as part of my review. Claude replaced it with what is known: I reviewed the brief on 2026-10-24, and section 3 shows the arithmetic, so each value can be checked by hand. The brief was then committed, before either shader exists.
- **Hand check of the predicted values:** none recorded. The rubric asks for predictions "computed by hand". A hand check of two of them, made after the captures, is in the second entry of 2026-10-28.
- **Still to do:** type the colour line into the shader myself, and record it as Claude's suggestion.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude drafted the whole brief, including the colour line, the predicted values and the short answers. I asked for it, reviewed it and approved the commit.

## 2026-10-24 — Step 2: the first CLAUDE.md run could not log in

*Written on 2026-10-24, from the conversation. Transcript: `sessions/session-1-auth-failed.jsonl`.*

- **Attempt (Claude, at my request):** the course's scoped run, `claude -p` with `sessions/prompt-1.txt`, which is the course's prompt with paths for this folder's two projects.
  - It started at 22:19:16 EDT, from Claude's own shell.
  - `CLAUDECODE` was unset for the run, because the run was started from inside another Claude Code session.
- **What happened:** it stopped after 3 s with exit code 1. Its only reply was "Failed to authenticate: OAuth session expired and could not be refreshed".
- **What the transcript's last line says:** `"subtype":"success"`, but also `"is_error":true` and `"terminal_reason":"api_error"`, with 0 tokens used. Read alone, `subtype` would have reported a success; the check has to read `is_error` and the reply as well.
- **Check (Claude):** the run created only its transcript. There is no CLAUDE.md, and `game/shaders`, `godot/shaders` and the wrapper are unchanged.
- **Next:** I log the command-line `claude` in again, and Claude repeats the run.
- **Human / AI:** Claude started the run and read its transcript; logging in is mine to do.

## 2026-10-26 — Step 2: the CLAUDE.md draft

*Written on 2026-10-26, from the conversation. Transcript: `sessions/session-1.jsonl`.*

- **Attempt:** I logged the command-line `claude` in again, and Claude repeated the same run with the same prompt and permissions.
- **The run:**
  - It started at 22:06:38 EDT and ended at 22:08:05 EDT.
  - Its result event reads `"subtype":"success"`, `"is_error":false` and `"terminal_reason":"completed"`: 25 turns in 84 s.
  - It used model `claude-opus-5-5` in Claude Code 2.1.310, and reports a `total_cost_usd` of 1.11.
- **Permission denials: 2.** Both were Bash commands outside the allowed list. One read the logs with `tail` and the two `.glb` files' JSON with Python; the other read the `.glb` files again. The scoping held: instead of the answer, the draft lists the surface indices as unconfirmed.
- **Checks (Claude, in this conversation):**
  - The run created only `CLAUDE.md` (82 lines) and its transcript.
  - `game/shaders`, `godot/shaders` and the wrapper are unchanged.
  - The first line is a heading, which is right because there is no `AGENTS.md`. Line 56 is exactly `@CHANGE-BRIEF.md`.
  - The transcript holds no e-mail or account field.
  - Claude opened every file and line the draft cites, and each one says what the draft says it does.
- **Left for the review, after the unedited draft is committed:**
  - the surface indices and mesh node names the draft could not confirm;
  - a "Headless facts" block, confirmed on this machine;
  - the brief citations the draft did not open.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped `claude -p` session wrote `CLAUDE.md`. Claude, in this conversation, ran that session and checked its output. I logged the command line in.

## 2026-10-26 — Step 2: reviewing the CLAUDE.md draft

*Written on 2026-10-26, from the conversation. The unedited draft is commit `dfeca3fb`; the review is the commit that adds this entry.*

- **Attempt (Claude, at my request):** the review the assignment asks for. Check every reference, delete what is not a test, and add a "Headless facts" block confirmed on this machine.
- **References:** Claude opened every file and line the draft cites, and all were right. The draft already kept the two screenshot scripts out of the test commands and called them not tests, so nothing had to be deleted.
- **Probes**, in `evidence/headless-probe/`, with their logs in `logs/probe_*.log`, run headless with Godot 4.7.2:
  - **`probe_surfaces.gd`, run against `godot/`.** `Waystone/Waystone` has surfaces 0 Stone, 1 Moss and 2 Rune; `TeleportCircle/TeleportCircle` has 0 Gold, 1 DarkStone and 2 PaleGold. This settles the two items the draft left unconfirmed.
  - **`probe_headless.gd`, in a throwaway project:**
    - the run had the headless display server and the dummy renderer, with no video adapter;
    - a broken shader loaded without an error; the `SHADER ERROR` came when the shader was set on a `ShaderMaterial` (line 17 of the probe);
    - the broken shader's uniform list was empty;
    - the good shader listed `amount` with its type and range, but the renderer reported no default for it (null);
    - the frame could not be read back;
    - the probe still quit with exit code 0.
  - **A difference from Example 06.** Claude added `--rendering-driver metal` or `vulkan` to `--headless`, in either order, and all four runs stayed on the headless display server. Example 06 saw the fallback to a window with the long form, `--display-driver headless`. That was not repeated here, because it can open a window. The rule stays: use `--headless` exactly.
- **Changes to CLAUDE.md** (82 lines, now 91):
  - added the surface indices and mesh names, so the overrides go on surface 0 and surface 1;
  - added, with references, the facts behind the brief citations the draft had not opened: the order of hits, the pause rule, the defeat timing and the shared outline material;
  - added how `checks.gd` counts;
  - added the Headless facts block;
  - removed the settled items from Unconfirmed.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude did the review and the probes; I asked for it.

## 2026-10-27 — The shader from code

*Written on 2026-10-27, from the conversation. The shader is commit `ae0a3757`.*

- **Attempt (me):** I wrote `game/shaders/invulnerable_tint.gdshader` from the brief's section 2. I committed it on its own, with the `.uid` Godot made for it, as `ae0a3757`. Its nine lines follow the brief:
  - `shader_type canvas_item;`, with no `render_mode`;
  - the three uniforms, with the brief's names, types, hints and defaults;
  - the colour line, at line 8, exactly as the brief gives it.
- **What I adopted from Claude:** the colour line and the three uniforms come from the brief, which Claude drafted. I typed them in. SOURCES.md records this too.
- **Before I wrote it (Claude):** Claude listed what to prepare and how to check the result. It wrote `evidence/headless-probe/probe_shader.gd`. The probe sets a shader on a `ShaderMaterial`, which makes Godot compile it, then prints the uniforms the engine reports and the source's declaration lines.
- **Finding (Claude): a clean import says nothing about this shader yet.** The assignment's check is to reimport and confirm that no `SHADER ERROR` appears. `evidence/headless-probe/import_check.sh` imports two fresh copies of `game/` that contain broken shaders (`logs/probe_import_check.log`):
  - `outline.gdshader`, which the main scene uses, with a semicolon removed: one `SHADER ERROR`;
  - in the same copy, `unused_typo.gdshader`, which nothing uses, with `COLOR` misspelt: no error on import, though the probe then reports `Unknown identifier in expression: 'COLOUR'`;
  - the broken outline again, in a copy with no main scene: no error.

  So a headless import compiles only what the main scene uses. Nothing uses the new shader until the driver gives `Hud/Hearts` its material, so the probe is the check that compiles it.
- **Checks (Claude):**
  - The commit holds only the shader and its `.uid`.
  - The text matches the brief's section 2, with no `TIME`, sampler, `vertex()` or `light()`. It is 302 bytes of ASCII.
  - Reimport: exit 0, with no `SHADER ERROR` and no other `ERROR` or `WARNING` line (`logs/game_import_tint.log`).
  - Compile, with the probe: no `SHADER ERROR` or `SCRIPT ERROR` line (`logs/probe_invulnerable_tint.log`). The engine reports three uniforms: `tint_amount` and `tint_strength` as `float` with the range 0.0 to 1.0, and `tint_color` as `Color`. The declarations give the defaults 0.0, `vec4(0.6, 0.88, 1.0, 1.0)` and 0.4.
  - The existing tests, through the wrapper at 60 fps: the game's 141 PASS and 0 FAIL, and the props scene's 44 ok and 0 failed. The game's log differs from step 0's in two lines: the camera shake's random offset, and the ObjectDB instances leaked at exit, 30 instead of 41.
- **A false alarm (Claude's mistake):** the first compile check counted one `SHADER ERROR` line, but it was the probe's own marker, which contained those words. Claude reworded the marker. The rerun counted none, and on a broken copy the probe still caught Godot's real error.
- **Differs from the assignment:**
  - the shader is in `game/shaders/`, because the effect is in the 2D game (the brief, section 2);
  - the probe backs up the reimport check, for the reason above.
- **Expected / learned:** added on 2026-10-28, in my words: "一开始写色彩行之前，还不知道 COLOR 里已经乘了贴图和 modulate" ("Before I first wrote the colour line, I did not yet know that COLOR already has the texture and the modulate multiplied into it").
- **Human / AI:** I wrote the shader and committed it. Claude wrote the probe and the import check, ran every check, and drafted this entry.

## 2026-10-27 — The driver and its test: the plan

*Written on 2026-10-27, from the conversation. Prompt `sessions/prompt-2.txt`; transcript `sessions/session-2.jsonl`; the plan, extracted unchanged from its result event, `sessions/plan-2.md`.*

- **Before the run (Claude, approved by me):** CLAUDE.md was brought up to date, because the agent reads it first.
  - `game/shaders/` holds the shader now, so the two lines that said it did not exist were changed.
  - A Headless fact was added: a headless import compiles only the shaders the main scene uses.
- **The prompt (Claude, reviewed by me):** the course's prompt for this step, for the plan only.
  - It names `game/` and `Hud/Hearts`.
  - It asks for each *driven* uniform, because the brief says code never sets `tint_color` or `tint_strength`.
  - It asks for numbered steps, each with the files it changes.
- **The command was read-only.** `--permission-mode dontAsk` refuses anything not allowed. Only the read tools and read-only `git` and `ls` were allowed, and `Edit`, `Write` and `NotebookEdit` were disallowed. This CLI's `--help` (2.1.310) lists no `default` mode; its choices are `acceptEdits`, `auto`, `bypassPermissions`, `manual`, `dontAsk` and `plan`.
- **The run:** 19:15:48 to 19:19:21 EDT.
  - The result event: `success`, `is_error` false, `terminal_reason` completed, 8 turns, $1.30, no permission denials.
  - It read files with 7 Bash commands and changed nothing. Apart from its transcript, all 181 files matched a snapshot of their hashes taken before the run.
- **The plan:** 5 steps and 14 assertions, A1 to A14, each tied to a rule in the brief:
  - a material on `Hud/Hearts`, local to the scene;
  - a driver in `hud.gd` that sets only `tint_amount`;
  - a new headless test that plays through four hits with real input.
- **Claude's review, and the changes I accepted:**
  1. A13 reloaded by adding a second Main beside the first. It now frees the old one first, as `checks.gd` does at lines 1320–1323.
  2. A6 checks the first frame of every window, not only after hits 1 and 4.
  3. The two temporary `hud.gd` mutations the plan offered are approved, with a check that `hud.gd` is restored.
  4. As proposed, the material is local to the scene and stores no `tint_color` or `tint_strength`.
  5. The capture tool is left for later.
- **A correction (Claude):** Claude first told me that the course's command, which disallows `Edit(godot/shaders/**)`, would not stop the Write tool. The permissions documentation says the opposite: `Edit(path)` rules cover every tool that edits files, and `Write(path)` rules never match.
- **My e-mail address is in the transcript once**, in the output of a `git show` the agent ran. It is the address in every commit's author field. The transcript stays unedited.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude drafted the prompt and the CLAUDE.md changes, ran the session, checked it and reviewed the plan. I reviewed and approved each of them, and accepted the plan with Claude's changes.

## 2026-10-27 — The driver and its test: the first implementation run was refused

*Written on 2026-10-27, from the conversation. Prompt `sessions/prompt-2b.txt`; transcript `sessions/session-2b-refused.jsonl`.*

- **The command (Claude):** `--permission-mode dontAsk`, with `Edit` allowed only on the five files the plan names, plus the wrapper and read-only `git`, and with the shader folders disallowed. Unlike the course's `acceptEdits`, it allowed no other change.
- **The run:** 19:29:24 to 19:30:08 EDT: `success`, `is_error` false, 11 turns, $0.88, 2 permission denials.
- **What happened:**
  - The agent's second command was `cd .../game && cat ...`, and its current directory stayed `game/` from then on.
  - The rules were written relative to the current directory, so `Edit(game/ui/hearts_tint.tres)` no longer named the file.
  - Its Write of `game/ui/hearts_tint.tres` was refused, and so was a `git -C ..` command.
  - It stopped, as the prompt asks, and would not write the file through the shell instead.
- **Check (Claude):** apart from the transcript, all 184 files matched the snapshot taken before the run.
- **The mistake was in Claude's command.** By the same reading, the relative deny rules on the shader folders stopped covering them after the `cd`. The shader stayed safe because `dontAsk` refuses every write that is not allowed. With the course's `acceptEdits`, a `cd` could leave a relative deny rule covering nothing. That last point is an inference, not tested.
- **Fix:**
  - Every path rule is now absolute, `//Users/...`, written as `/$PWD/...`.
  - The wrapper is allowed under the other spellings an agent in `game/` would use.
  - The prompt is unchanged.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude wrote the command, ran it and found the cause. I approved the run and the rerun.

## 2026-10-27 — The driver and its test: the implementation

*Written on 2026-10-27, from the conversation. Prompt `sessions/prompt-2b.txt`; transcript `sessions/session-2b.jsonl`, in commit `bd797945`. Since 2026-10-28 this folder holds its labelled excerpt instead, `sessions/session-2b-excerpt.jsonl` (`sessions/README.md`).*

- **The run:** 19:38:29 to 19:51:56 EDT: `success`, `is_error` false, `terminal_reason` completed, $3.97. It took 96 turns, more than `--max-turns 80`, without being cut short, so the limit does not count turns the way the result event does.
- **Permission denials: 4,** none of which stopped the work:
  - a Python rewrite of the test file;
  - two wrapper commands joined by `; echo "exit $?"`;
  - a `git diff --no-index /dev/null` after a `cd`.

  It edited only the five planned files.
- **What it wrote:**
  - `game/ui/hearts_tint.tres`: the `ShaderMaterial`, local to the scene;
  - `game/ui/hud.tscn`: the material on `Hearts`;
  - `game/ui/hud.gd`: `_tint_hearts()`, which sets only `tint_amount`, from Rudy's `_invulnerable_left / invulnerable_time`. It runs before the debug line's early return;
  - `game/tests/invulnerable_tint_checks.gd`, 520 lines, and its `.tscn`: 15 checks.
- **Its results:**
  - The new test passed 15 of 15 at 30, 60 and 144 fps, `checks.tscn` 141 of 141, and `check_props.gd` 44 of 44.
  - The two `hud.gd` mutations each exited 1. A frame-counting driver failed A9, among others, at 30 and 144 fps. A driver that runs while paused, on its own clock, failed A12, among others, at 60.
  - `hud.gd` was restored to the same blob.
- **Deviations it reported:**
  - In the first frame-counting runs, a setup check of its own failed before A9 was reached. It changed how the test names the windows, then reran step 5 and both mutations. It says it loosened no assertion.
  - The reload, A13, ends hit 4's window early. So A12 checks that the tint fell by the unpaused game time only, 0.5333 s over 1.05 s of real time, and not a whole window's length across the pause.
- **Findings:**
  - At 144 fps, the respawn's first frame is exactly 1.0 (72/72), because the respawn falls in a frame with no physics tick after it. That meets rule 1's "at least 70/72"; the brief's reason for the value not being 1.0 covers hits only.
  - The leak count at exit in `logs/game_checks_60fps.log` rose to 42. It had already gone from 41 to 30 between two runs with no change to the game, so it says nothing by itself.
- **Checks (Claude):**
  - Against the snapshot, only the five files, the logs and the transcript changed. `rudy.gd`, `main.gd`, `checks.gd`, both shader folders, `godot/`, the wrapper, the brief, SOURCES and FRICTIONAL are unchanged.
  - The test calls none of `take_hit()`, `respawn_at()` or `set_shader_parameter()`, and assigns none of Rudy's state. It gives input through `Input.action_press()`.
  - Claude ran the new test again at 30, 60 and 144 fps, outside the wrapper's logs. Leak lines aside, each run matched the session's log.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped session wrote the material, the driver and the test, and ran them. Claude ran the session and checked it. I approved the run.

## 2026-10-27 — The shader mutations

*Written on 2026-10-27, from the conversation.*

- **Mutation 1 (me):** I deleted the semicolon after `shader_type canvas_item` on line 1. Through the wrapper at 60 fps, the new test exited 1 (`logs/game_invulnerable_tint_checks_60fps_no_semicolon.log`):
  - one `SHADER ERROR`, "Expected a ';' after 'shader_type canvas_item'";
  - A1 and A2 failed, and 13 checks passed.
- **Mutation 2 (me):** I put the semicolon back and renamed `tint_amount` to `tint_amt` on lines 3 and 8, so the shader still parsed. The test exited 1 with no `SHADER ERROR` (`logs/game_invulnerable_tint_checks_60fps_renamed.log`):
  - A1 and A2 failed;
  - the other 13 passed, including every check of the value on the material. `set_shader_parameter()` with the old name raises no error and reads back what it stored, so only the name checks catch this.
- **Restore (me), checked by Claude:** `git diff` on the shader is empty, and the file matches `ae0a3757` byte for byte. The clean test then passed 15 of 15 at 60 fps.
- **A false mismatch (Claude's mistake):** Claude's first check that the rename was the only change used `\b` with macOS `sed`, which does not support it, and so it reported a difference. Redone without `\b`, the renamed shader matched the commit once the name was changed back.
- **Expected / learned:** none recorded.
- **Human / AI:** I made both mutations and restored the shader. Claude ran the test after each and kept both logs.

## 2026-10-27 — The textured shader: Rock 01's textures

*Written on 2026-10-27, from the conversation. Commit `e0e14c17`.*

- **Attempt (Claude, after I approved the download):** the four 1k PNGs the brief names, from Poly Haven. Before asking me, Claude read their sizes and MD5 sums from Poly Haven's API.
- **The download:** into an empty staging folder first. All four match the API's size and MD5. Three are 8-bit RGB; the roughness map is 16-bit greyscale, which the brief did not say.
- **A mistake on the way (Claude):** the session's working directory had changed to the repository's root, and the copy used a relative path, so the PNGs landed in a new `godot/` folder there. The first import found no textures, which showed it. Claude moved the four files into `assignment-5/godot/assets/textures/rock_01/`, with their MD5 sums unchanged, and removed the empty folders. Nothing was left outside `assignment-5/`.
- **ATTRIBUTION.md** records the page and file URLs, Rob Tuytel with the role "All", 2018-08-09, 1500 mm, CC0, and `_nor_gl` as the convention used. The licence page, checked on 2026-10-27, says "Our assets are all licensed as CC0".
- **Import settings:**
  - Godot's first import gave lossless compression, normal-map detection, no mipmaps and `detect_3d/compress_to=1`. The editor would have switched the textures to VRAM compression the first time it drew them in 3D.
  - Claude wrote the brief's section 5 settings into the four `.import` files, removed their cached imports and reimported. Godot kept the settings.
  - `probe_textures.gd` reads the imported formats (`logs/probe_textures.log`). The colour and roughness maps are DXT1 and the OpenGL normal map is RGTC_RG, each with 10 mipmap levels; the DirectX map is RGB8 with none. `get_image().get_format()` works in a headless run.
- **Expected / learned:** none recorded.
- **Human / AI:** I approved the download. Claude did the rest and drafted this entry.

## 2026-10-27 — The textured shader: the normal-map check

*Written on 2026-10-27, from the conversation. Commit `14efd4ba`.*

- **The check:** `godot/tests/normal_map_check.gd` is the assignment's code, unchanged; a diff against the assignment's text is empty.
- **Calibration (Claude):** `calibrate_normal_map_check.gd` runs it on Rock 01's normal map in both conventions (`logs/godot_calibrate_normal_map_check_60fps.log`):

  | | `directx = false` | `directx = true` |
  |---|---|---|
  | `_nor_gl` | 0.1444 | 1.8556 |
  | `_nor_dx` | 1.8556 | 0.1444 |

  The OpenGL file is low with `directx = false`, so the sign convention is the right way round, and nothing needs to go in TEST-REPORT.md.
- **A property of the ratio (Claude):** a map's two ratios always sum to 2, because (t1 − t2)² + (t1 + t2)² = 2(t1² + t2²). The DirectX file is the OpenGL file with green inverted, so the pair gives one independent number, 0.1444.
- **The threshold** is not set yet. Claude proposed 0.5, between the known-good 0.1444 and the 1 of a map with no surface behind it.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude copied the check, wrote and ran the calibration, and drafted this entry. I approved the commit.

## 2026-10-27 — The textured shader: the shader and its materials

*Written on 2026-10-27, from the conversation. The shader is commit `a87a18be`; the materials, `6d71a4f4`.*

- **Attempt (me):** I wrote `godot/shaders/weathered_stone.gdshader` from the brief's section 5 and committed it on its own.
- **Check (Claude):** it compiles, and the engine lists nine entries: three samplers, the groups `surface` and `relief`, and four uniforms (`logs/probe_weathered_stone.log`). The engine reports a sampler only as a `Texture2D`, with no hints, so Claude checked the hints from the source lines. All ten declarations match the brief.
- **The materials (Claude):** `waystone_stone.tres` and `circle_darkstone.tres`, with the brief's values.
  - `godot/tools/add_stone_overrides.gd` set them as surface material overrides, on surface 0 of `Waystone/Waystone` and surface 1 of `TeleportCircle/TeleportCircle`, and saved `props_room.tscn` the way the editor does. That also dropped `type="Node3D"` from the three instance lines, which Assignment 3's builder had written; it changes nothing.
  - `probe_overrides.gd` shows each override on its surface and the other six surfaces unchanged (`logs/probe_overrides.log`). The materials' values read back as written.
  - `check_props.gd` still passes 44 of 44. The overrides leave alone the `.glb` materials it reads, as the brief planned.
- **The editor (me):** I looked at both materials in the editor. Neither of the two sessions changed any file. The import settings held, so the brief's predicted failure 8, that the editor rewrites them, did not happen.
- **The circle's tint:**
  - Claude averaged Rock 01's colour map in linear light: `#776C5E`. Times `#8F857D` it is `#40352A`, darker and browner than the brief's aim, `#4A4440`.
  - The tint that gives `#4A4440` is `#A4A7B4`. I chose it, and the brief's revision 2 records why. I looked at the circle in the editor again.
- **Expected / learned:** none recorded.
- **Human / AI:** I wrote the shader, chose the tint and checked the look. Claude checked the shader, wrote the materials, the tool and the probes, computed the tint, and drafted this entry.

## 2026-10-27 — The hint experiment

*Written on 2026-10-27, from the conversation. The shader is commit `9481663a`; the strip, the materials and the scene, `143e9055`.*

- **The strip (Claude):** `godot/tools/write_grey_strip.gd` writes `grey_strip_3x1.png`, three opaque texels of 64, 128 and 192, and Godot and Pillow both read those values back. It is imported lossless, with no mipmaps and with normal-map detection and 3D compression off. The imported texture is RGB8 with the same three values.
- **The shader (me):** `godot/shaders/hint_experiment.gdshader`, spatial and unshaded, with `source_color_tex` (`source_color, filter_nearest`), `plain_tex` (`filter_nearest`) and the bool `use_source_color`, which picks the one that writes `ALBEDO`. It compiles with those three uniforms (`logs/probe_hint_experiment.log`). I committed it on its own.
- **The materials and the scene (Claude):** `hint_source_color.tres` and `hint_plain.tres` bind the strip to both samplers and differ only in the bool. `godot/tools/build_hint_experiment.gd` builds `hint_experiment.tscn`: quad A above quad B, a camera facing them, and a WorldEnvironment.
  - The tonemap is Linear at exposure 1.0, with glow, fog and adjustments off. Those are the defaults, so the scene file leaves them out; `probe_hint_scene.gd` reads them back (`logs/probe_hint_scene.log`).
  - The labels "A  source_color" and "B  no hint" and the background `#202830` are Claude's choices; the brief names neither.
- **The editor (me):** each band of B is lighter than the band of A above it, and the bands have sharp edges. The session changed no file. The displayed values themselves, 64, 128 and 192 against 137, 188 and 225, still need a capture that reads them in the engine.
- **Expected / learned:** none recorded.
- **Human / AI:** I wrote the shader and checked the scene. Claude wrote the strip writer, the materials, the builder and the probes, and drafted this entry.

## 2026-10-27 — The materials audit and its review

*Written on 2026-10-27, from the conversation. Prompt `sessions/prompt-3.txt`; transcript `sessions/session-3.jsonl`. The audit, unedited, is commit `cd1e71a3`; the review is the commit that adds this entry.*

- **The prompt (Claude, reviewed by me):** the course's audit prompt, changed in five places:
  - this folder's paths and wrapper;
  - a sentence that the brief's dated revisions replace what they name;
  - the attribution sentence: the course's "which I checked myself" became "which were checked against Poly Haven's API and licence page", since Claude, not I, checked them;
  - two more assertions, from the brief's predicted failures 8 and 9: every import setting the brief sets, and the surface or quad each material is on.
- **The command:** `dontAsk`, with `Edit` allowed only on `godot/MATERIALS.md` and `godot/tests/test_materials.gd`, by absolute path, and the shader folders disallowed.
- **The run:** 21:04:16 to 21:08:35 EDT: `success`, `is_error` false, `terminal_reason` completed, 35 turns, $1.65.
  - Two permission denials: a `for` loop over `cat` in `godot/`, and a wrapper command joined with `; echo "exit $?"`. It then ran the wrapper alone.
  - It wrote only the two files; every other file's hash matched the snapshot taken before the run.
- **The test:** 125 PASS and 0 FAIL, in five parts: the shaders' uniform lists and sampler hints, the materials, the import settings, where each material is, and the normal maps' curl ratios, 0.1444 and 1.8556 again. Claude's own run outside the wrapper matched its log.
- **Its findings:** eight, none a mismatch with the brief. Among them: the roughness map loses its 16-bit precision as DXT1; `_nor_dx` is imported though nothing uses it; the brief's line numbers for the lighting are stale; and the `source_color` mutation is left to me.
- **The review (Claude):**
  - Every integer enum was looked up, the importer's in Godot 4.7.2's source and the scene's in `ClassDB`. The audit's names were all right; two unnamed values now have names.
  - The formats were checked with `get_image().get_format()`, and match.
  - One number nobody measured was wrong: "about 3 MB" for the DirectX map's import, which is 1,908,496 bytes on disk. "About 23°" is now 22.97°, computed from the camera's transform.
  - The stale line numbers are corrected in the brief's revision 3, and the test got a comment naming the importer enums it compares.
- **Expected / learned:** none recorded.
- **Human / AI:** the scoped session wrote `MATERIALS.md` and the test. Claude drafted the prompt, ran and checked the session, did the review and drafted this entry. I approved the prompt and the run.

## 2026-10-27 — The fresh cache and the `source_color` mutation

*Written on 2026-10-27, from the conversation. Logs: `logs/godot_import_fresh_cache.log` and `logs/godot_test_materials_60fps_no_source_color.log`.*

- **The fresh cache (Claude, at my request):** the assignment says to delete `godot/.godot`, reimport and run the test. Claude moved the cache into its scratchpad instead of deleting it, so it could be restored; for `godot/` the effect is the same. The cache was 8.6 MB, ignored by git, with no tracked files.
  - The import from empty took 3 s: exit 0, with no `SHADER ERROR` and no other error or warning. It made 16 imported files, as many as before (`logs/godot_import_fresh_cache.log`).
  - `test_materials.gd` passed 125 of 125, `check_props.gd` 44 of 44, and the calibration passed. Their logs matched the committed ones byte for byte, and no `.import` or `.uid` file changed.
- **The mutation (me):** I deleted `source_color` from `albedo_tex`, line 3 of `weathered_stone.gdshader`. `git diff` showed that one line and nothing else.
  - Through the wrapper at 60 fps, `test_materials.gd` exited 1 with no `SHADER ERROR`: 124 checks passed and one failed (`logs/godot_test_materials_60fps_no_source_color.log`). The failure was `weathered_stone.gdshader: albedo_tex hints are source_color, filter_linear_mipmap, repeat_enable`, which found `filter_linear_mipmap, repeat_enable`.
  - The shader still parses, and the engine does not report sampler hints, so only that check, which reads the hints from the source text, catches it. This is the brief's predicted failure 7.
- **The restore (me), checked by Claude:** the shader matches `a87a18be` byte for byte. The clean run passed 125 of 125 again, and its log matches the committed one.
- **Expected / learned:** none recorded.
- **Human / AI:** I made the mutation and restored the shader. Claude moved the cache, ran the import and the tests, kept the logs and drafted this entry.

## 2026-10-27 — The generated shader and LANGUAGE-NOTES

*Written on 2026-10-27, from the conversation. The generated shader is commit `fe795908`; LANGUAGE-NOTES.md, `5db11399`.*

- **The generated shader (me):** in the editor, I gave a unique StandardMaterial3D Rock 01's albedo, OpenGL normal and roughness textures, enabled Normal Map, and converted it to a ShaderMaterial from the Inspector's resource menu. I saved the code as `godot/shaders/standard_generated.gdshader` and annotated it. Its 34 code lines and Godot's two comments are unchanged; the other 25 comment lines are mine. Nothing uses it.
- **Checks (Claude):**
  - it compiles headlessly, and the engine reports 16 uniforms (`logs/probe_standard_generated.log`);
  - the annotations change no code;
  - the four uniforms the comments call unused, `albedo_texture_size`, `point_size`, `uv2_scale` and `uv2_offset`, are read by neither function, and no line writes `ALPHA`.
- **The editor session:** it drew Rock 01's three textures in a StandardMaterial3D, the case the brief's predicted failure 8 is about. Afterwards `git status` showed only the two new files, and no `.import` file had changed.
- **LANGUAGE-NOTES.md (me):** part A gives the generated shader's lines the assignment asks for; part B answers the eight questions, each with a line reference to one of my three shaders.
  - Claude checked every line reference, and all were right.
  - At my request, Claude changed the 12 links from local absolute paths to relative ones, with GitHub line anchors, and corrected line 16 to say the conversion used the Inspector's resource menu.
- **Expected / learned:** none recorded.
- **Human / AI:** I made and annotated the generated shader and wrote the notes. Claude checked both, made the two changes I asked for in the notes, and drafted this entry.

## 2026-10-27 — The windowed captures of the hearts and the hint experiment

*Written on 2026-10-27, from the conversation. Commit `1868dc08`; logs `logs/capture_tint.log` and `logs/capture_hint.log`.*

- **The tools (Claude):** `game/tests/capture_tint.tscn`, with its script, and `godot/tests/capture_hint.gd`. Each saves the frame as drawn, 1920 × 1080, never resized, and prints the sampled pixels beside the brief's predictions.
  - For the hearts, `move_right` walks Rudy into the first spikes. Once that window has run out, the tool stops the driver with `hud.set_process(false)` and sets `tint_amount` from code.
  - Claude's first dry runs used `--headless`, and both hung until the time limit ended them (exit 124), because `frame_post_draw` never comes without a renderer. Both tools now stop at once, with exit 1, when run headless.
- **The runs (Claude, with my approval),** in a window, each in its project's renderer:
  - the hearts, in GL Compatibility: P1 and P2 match the brief exactly at 0.0, 0.5 and 1.0. At 2.0, P1 is `#A3C1D7` against `#A2C0D7` and P2 is exact, so `hint_range` does not clamp a value set from code. P3 never changes;
  - at 0.0, against a capture with no material, one edge pixel of the 11,200 under the hearts differs, by one step;
  - the hint experiment, in Forward+: all six bands match, 64, 128 and 192 with `source_color`, and 137, 188 and 225 without.
- **Expected / learned:** none recorded.
- **Human / AI:** Claude wrote both tools, ran them and drafted this entry. I approved the runs.

## 2026-10-27 — My playtest

*Written on 2026-10-27, from the conversation.*

- **Attempt (me):** I played the game in the editor. At first Run Project opened the 3D scene, because I had the `godot/` project open. Claude explained that `game/` holds the game, gave me the controls, and listed what to look for.
- **What I saw, in my words:** "确实像你说的，受伤时红心颜色变淡，然后逐渐恢复。其他都没改变" ("It is as you said: when I'm hit, the hearts turn pale, then gradually recover. Nothing else changed.")
- **The three boundary cases:** Claude asked whether I had also tried walking back into the spikes in the window, losing all three hearts, and pausing in the window. I answered "都试过了" ("I tried them all."). I did not describe them one by one, so TEST-REPORT.md records them as behaving as the brief says.
- **Check (Claude):** after the session, `git status` showed no file changed.
- **Expected / learned:** none recorded.
- **Human / AI:** I played and said what I saw. Claude listed what to try, checked `git status`, and drafted this entry.

## 2026-10-27 — The sweep, the two materials and the OS screenshot, done by Claude

*Written on 2026-10-27, from the conversation. Logs `logs/capture_sweep.log` and `logs/capture_hint_vs_os.log`; the results are in TEST-REPORT.md, sections 7, 8 and 12.*

- **Why Claude:** the assignment marks the sweep and the two materials HUMAN CHECK, and asks me to compare a capture with an OS screenshot once. I asked Claude to do all three for me and to record that truthfully: "这几项我要求你帮我做，如实记录" ("I'm asking you to do these for me; record them truthfully"). So they rest on in-engine captures and Claude's reading of them.
- **The sweep tool (Claude):** `godot/tests/capture_sweep.gd`. It changes the loaded material and shader in memory and never saves them, so the Ownership rule holds. Afterwards `git status` showed every material, the shader and the scene unchanged.
- **The sweep:**
  - From the scene's Camera, `albedo_tint` and `uv_scale` changed the look plainly. `normal_strength` and `roughness_offset` changed it by 1 to 3 steps on average, and Claude could not see the difference.
  - So Claude added a close-up pass, with the camera moved in memory to about 2 m from the waystone. The two changed it by about 3 steps again.
  - Claude then measured why. The normal map's normals tilt 7.7° from flat on average. 90% of the roughness map's texels lie between 0.474 and 0.571. And the Sun's mirror direction off the waystone's sides points below the floor, so no camera can see a highlight there.
  - Claude's judgement: `uv_scale` breaks the look at both ends.
- **One shader, two materials:**
  - Line 18 with `ALBEDO` halved, in the loaded shader's code only, darkened both stones, by 22.54 and 10.52 steps.
  - The circle's `normal_strength` at 2.0 changed only the circle, by 0.76 steps, too little to see. So Claude added a second edit, the circle's `albedo_tint` at white: 19.97 steps on the circle, 0.00 on the waystone.
- **The OS screenshot:**
  - The first `screencapture` missed the window: I have two displays, and the region pointed at the wrong one. Claude moved that file out of the repository without opening it, since it held another part of my screen. It then changed the tool to put the window on the primary display first, and to delete any screenshot that does not show the window.
  - The second showed the window's client area only, at 1920 × 1080. Claude looked at it, and it shows only the hint scene.
  - The engine capture matched all six predictions; the screenshot was 4 to 11 steps darker. The screenshot embeds the display's colour profile, "Q27q-1L". Converted from it to sRGB with Pillow, all six bands came back to the engine's values exactly, so the engine capture is the one to trust.
- **The rerun (Claude):** before drafting TEST-REPORT.md, Claude ran every headless test again at `5db11399`. All passed with the same counts. Six logs came out byte for byte as committed. `logs/game_checks_60fps.log` differs in two lines that are not results: the random camera-shake offset, and a path count of 81 instead of 79, from the two `capture_tint` files.
- **My review:** I reviewed Claude's results and looked at the captures, and found no problems: "我审核了你的结果，截图也看过了，没有问题。" ("I reviewed your results and looked at the screenshots too; there is no problem.") TEST-REPORT.md records this too.
- **Expected / learned:** none recorded.
- **Human / AI:** I asked Claude to do these checks, then reviewed its results and the captures. Claude wrote both tools, ran them, judged the captures, made the measurements, and drafted this entry and TEST-REPORT.md.

## 2026-10-28 — Checking the work against the assignment, and closing the documentation gaps

*Written on 2026-10-28, from the conversation.*

- **Attempt (me):** I asked Claude, in Chinese, what is left of Assignment 5 and whether what is done meets the assignment.
- **The check (Claude):** it reread the Canvas text and checked each part, the "Done means" list and the rubric against the files.
  - Parts 1 to 3 are done. Ship It and Verify have not started.
  - Five things fell short of the text: no curl threshold is set; rule 8's fade-in has no check; `sessions/session-2b.jsonl`, at 1.6 MB, is over the "about 1 MB" allowed for a transcript; CLAUDE.md's Unconfirmed section was out of date, and its test commands left out the two new tests; and SOURCES.md still says of the documents, "Will check them against what I did".
  - Others could cost points. The interface sweep and the two-materials check, which the assignment marks HUMAN CHECK, were done by Claude. The predictions were computed by Claude's script, not by hand. And no entry here records what I expected or learned.
  - `rudy.gd`, `main.gd`, the existing tests, the outline material, both `project.godot` files, and the `.glb` files and their imports are byte for byte as in Assignments 2 and 3.
- **Found on the way (Claude):** the driver (`bd797945`) added a line to `hud.gd`'s top comment and two lines to `hud.tscn`. So three of CLAUDE.md's references were one line off, and it still said `Hearts` has no material. The brief cites the same lines; its revision 4 gives the new ones.
- **The changes (Claude, at my request), not committed:**
  - CLAUDE.md, from 103 lines to 109. The moved references and the hearts' material are corrected. Added: the driver; two facts the captures settled, that `hint_range` does not clamp and what the hint experiment displays; the sweep's finding; the generated shader; the two new tests' commands and counts; the four new capture tools, with a Headless fact about them. Unconfirmed now lists only what is still open.
  - The transcript: `sessions/session-2b-excerpt.jsonl`, 874,696 bytes, made by `scripts/excerpt_transcript.py`, replaces `sessions/session-2b.jsonl` in the folder; the full transcript stays in `bd797945`. The excerpt keeps all 664 events and cuts only two fields of the harness's copy of each tool result, which repeat what is kept. `sessions/README.md` labels it and lists every transcript.
  - The FRICTIONAL entry and the SOURCES rows that cite the transcript now name the excerpt.
- **Checks (Claude):** putting the 61 cut values back gives the original events exactly; the result event is byte for byte the original; and the script, run on the full transcript from `bd797945`, gives the excerpt byte for byte.
- **Still mine to do or decide:** the threshold; the fade-in check; the sweep and the two-materials check, by my own eyes; a hand check of some predictions; what I expected and learned; and checking SOURCES.md and this file against what I did.
- **Expected / learned:** none recorded.
- **Human / AI:** I asked for the check and the changes. Claude did the check, made the changes and their checks, and drafted this entry.

## 2026-10-28 — The curl threshold, the fade-in and the three edge cases

*Written on 2026-10-28, from the conversation.*

- **The threshold (me):** I chose 0.5, the value Claude had proposed. It lies between Rock 01's 0.1444 in its own convention and the 1 the assignment gives for a map with no surface behind it.
- **Its checks (Claude):** two more checks in `godot/tests/calibrate_normal_map_check.gd`: each Rock 01 file, read in its own convention, is under 0.5.
  - Through the wrapper at 60 fps: 4 PASS, exit 0 (`logs/godot_calibrate_normal_map_check_60fps.log`).
  - With the threshold set to 0.1, below 0.1444, the two new checks failed and the test exited 1 (`logs/godot_calibrate_normal_map_check_60fps_threshold_0.1.log`). Claude restored the script and checked it against its SHA-256 from before the change. The rerun passed 4 of 4.
- **The fade-in (me):** Claude asked me to run `game/` in the editor, press Enter on the title, and watch whether the hearts fade in as before and whether they look blue. I answered "看过了没问题" ("I looked; no problem").
- **The three edge cases (me):** asked for a sentence on each, I answered "都没问题" ("none of them had a problem").
- **What Claude did not write:** I asked Claude to write the remaining points for me to review. It left three as they were, because the assignment asks for them from me: the sweep and the two-materials check by my own eyes, predictions computed by hand, and what I expected and learned. The sweep and the two-materials check stay Claude's checks, as TEST-REPORT.md records.
- **The hand check (me), after the captures:** from the inputs and formulas Claude gave me, I recomputed two of the brief's predictions by hand: P1 at `tint_amount` 0.5, and quad B's left band in the hint experiment. I said "手算复核完了，没问题" ("I've done the hand check; no problem"). My numbers are not written down here.
- **My review:** I reviewed the day's changes, and SOURCES.md and this file against what I did: "审核完了，没问题" ("I've finished the review; no problems").
- **Updated (Claude):** TEST-REPORT.md (the summary, and sections 1, 4, 5, 10 and 14); CLAUDE.md, where the threshold and the fade-in are now facts and Unconfirmed lists two items; and SOURCES.md.
- **Expected / learned:** about the shader from code, in my words: "一开始写色彩行之前，还不知道 COLOR 里已经乘了贴图和 modulate" ("Before I first wrote the colour line, I did not yet know that COLOR already has the texture and the modulate multiplied into it"). It is in that entry too.
- **Human / AI:** I chose the threshold, checked the fade-in and the edge cases, did the hand check, said what I learned and reviewed the changes. Claude added the threshold's checks and their mutation, ran them, updated the documents and drafted this entry.
