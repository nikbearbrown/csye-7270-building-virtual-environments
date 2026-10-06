# Module 2 — Prompting game art (and sound)

CSYE 7270 · Fall 2026 · Week 2

## Executive summary

This module teaches you to prompt image, sound and music models for your own game, then judge what comes back where it counts: inside Godot, at game size, on real events. A generated picture that looks finished in a folder has not met a single engine constraint; its size, background, frame layout and collider are still open, and an unimported music file has no loop point. You will practise on a scratch copy of a public Walker project: a coding agent turns one AI-generated reference image into a checked sprite asset and wires placeholder sounds to game events, and you check its work with commands the agent did not write. A pass shows that import settings, frame regions, collider size and trigger counts are what the files say. It does not show that the sprite reads at game size or that a sound feels right; those are human checks. The module feeds Assignment 2.

## The question

Professor Bear's Assignment 2 log records a Gemini image he accepted as "closer to a game sprite" than his first try: three big-headed termite soldiers in pixel-art style, asset TERM-REF-02.

Looks like game art. Now ask the engine's questions. The file is a 1,024 x 873 JPEG. The Clawd game renders 640 x 360, and its player collides as an 18 x 28 pixel box. The picture's "pixels" are about four source pixels wide and JPEG-smoothed, so they sit on no exact grid. The background is white, not transparent. The three soldiers are three different creatures, not three frames of one, seen from above in a game seen from the side.

What has to happen between "the model gave me a nice picture" and "this is an asset in my game", and which of those steps can a machine check for you?

## The ideas

### 1. A prompt is a specification, and the engine reads the result

An image model responds to mood words such as "menacing" and "crisp". Godot responds to numbers: pixel dimensions, an alpha channel, a frame grid, a loop point counted in samples. A prompt of mood words produces a picture; a prompt that carries the engine's numbers produces something you can check. Decide before you generate how you will check each constraint.

| Constraint | Put it in the prompt as | Check it in Godot as |
|---|---|---|
| Size | "reads as a 32-pixel-tall sprite in a 640 x 360 game" | Beside the player, at 1:1 viewport scale |
| Background | "a solid medium-gray background" (never "transparent") | The imported texture has alpha; corners are alpha 0 |
| Silhouette | "bold, flat, readable outline" | Fill it black at game size: does it still read? |
| Frames | "4 frames in one row, equal cells, same baseline" | `SpriteFrames.get_frame_count()` and each region |
| Orientation | "side view, facing right" | `flip_h` makes the left-facing version |
| Loop (audio) | "120 BPM, 8 bars, no fade-out" | Import loop points; listen across the seam three times |

Two rules come from Walker's `asset-gen` skill: the generator bakes a checkerboard into "transparent" backgrounds, and "facing left" and "facing right" often come out identical, so generate one direction and flip it. The tools change every term; these constraints do not.

### 2. Provenance is part of the asset

A generated file without its record is an unlabelled bottle. Assignment 2's asset log asks for the model and version, its license or terms, the exact prompt and settings, the outcome, the edits and where the file is used. It does three jobs.

- **Reproduction.** A TA may ask you to regenerate an asset from your log.
- **Rights.** The U.S. Copyright Office's January 2025 report concluded that AI output is protected only where a human author contributed sufficient expressive elements; prompts alone do not count. Your selection and edits are the parts that are yours, and the log shows them.
- **Contamination.** TERM-REF-02 was made with Gemini from TERM-REF-01, which was made from three web photos whose source and license were not recorded, so it may still count as derived from them. The same log records a rejection: Gemini heard "those termites" as "Kratos termites" and drew a copyrighted game character's face.

The course rules are narrower than the law: no named living artist's style, copyrighted character, brand, existing music or recordings as reference, and no cloned voices. Open models are allowed, and some carry non-commercial terms: Meta's AudioCraft code is MIT, but its weights are CC-BY-NC 4.0. That is acceptable for coursework if `SOURCES.md` says so.

### 3. The import pipeline and the texture settings

Godot never uses your PNG or WAV directly at runtime. The **importer** converts it into `res://.godot/imported/` and writes a plain-text sidecar beside the source, such as `termite_soldiers.png.import`. Commit the `.import` files, not `.godot/` ([Import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)). Because the sidecar is text, an agent can read it, a diff can show it and a test can assert on it.

| Setting | Lives in | For a 2D sprite |
|---|---|---|
| `compress/mode` | `.import` | 0 Lossless (the default); the docs recommend it for pixel art |
| `mipmaps/generate` | `.import` | Off unless the camera zooms far out; costs about 33% more memory |
| `texture_filter` | the **node** (`CanvasItem`) | Nearest (1) for pixel art. The project default is Linear in 4.7.2 |

The last row catches Unity users. Since Godot 4.0, texture filter and repeat modes are set on the `CanvasItem` in 2D, not in the importer ([Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)). Setting it on the sprite keeps the change bounded; the project default changes every textured node.

### 4. Frames, and the collider that is not the art

An `AnimatedSprite2D` plays a `SpriteFrames` resource: named animations, each a list of frames with a speed and a loop flag. Frames cut from one sheet are usually `AtlasTexture` resources, the sheet plus a `region` rectangle, all in a `.tres` text file ([2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)). Frame count is a fact a test can check. A new pose and a different creature look identical to that test; only you can tell them apart.

The collider is not the art. In `walker-jumpman-clawd`, `features/player/player.gd` builds an 18 x 28 `RectangleShape2D`, and Clawd's arms are drawn outside that box; the README calls the trade-off a human judgment. For generated sprites, keep the `CollisionShape2D` a **sibling** of the sprite so scaling or flipping the art never changes it. Size it from what the player believes is solid, not from the image rectangle with its antennae and margin, and write down why. Art beyond the collider is fair when thin or decorative, unfair when it looks like the part that hurts you.

### 5. Sound: import, loop, trigger

Godot's documentation recommends WAV for short, repetitive effects and Ogg Vorbis for music and long sounds ([Importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html)). The course keeps MP3 out of GitHub. The two importers handle loops differently; these are Godot 4.7.2's defaults from a probe import:

```text
# sound.wav.import (importer "wav")        # music.ogg.import (importer "oggvorbisstr")
edit/trim=false                            loop=false
edit/normalize=false                       loop_offset=0
edit/loop_mode=0                           bpm=0
edit/loop_begin=0                          beat_count=0
edit/loop_end=-1                           bar_beats=4
compress/mode=2
```

For WAV, `edit/loop_mode` is 0 Detect from WAV, 1 Disabled, 2 Forward, 3 Ping-Pong, 4 Backward; `loop_begin` and `loop_end` count **samples**, and `-1` means the last sample. Detect is not Disabled: an effect imported with Detect did not loop only because its file carried no loop chunk. In the loaded `AudioStreamWAV` the numbering shifts by one, so importer mode 2 (Forward) loads as `loop_mode` 1. Ogg has only a loop *offset*, so cut generated music at a bar boundary before you import it.

For Ogg, `loop_offset` is in seconds and is where the stream starts again after it loops; the end of the loop is the end of the file, or the end of the last beat if `beat_count` is set ([AudioStreamOggVorbis](https://docs.godotengine.org/en/stable/classes/class_audiostreamoggvorbis.html)). Godot cannot end the loop earlier than the file does, so cut the file at a bar boundary before you import it.

Playback happens through a node. `AudioStreamPlayer` is non-positional; the 2D and 3D versions pan and attenuate by position. `max_polyphony` defaults to 1, and calling `play()` past that limit cuts off the oldest sound ([AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html)). That is the engine-level cause of the double-trigger bug, and the fix is in the event, not the file: play on the *transition* into a state, not every frame the state is true. Assignment 2's rule that sound must never decide game state has a test: remove the audio node, send the same inputs, and the game must end in the same state.

### 6. Procedural audio is not generative audio

`walker-audio-generator` fills an audio buffer every frame with a 440 Hz sine. That is procedural synthesis, a formula evaluated sample by sample, not a generative model. It does not satisfy Assignment 2's generative-model requirement, any more than code-drawn or SVG art written by Claude does. Its 15 headless assertions pass on the Dummy driver, and its own log calls them state checks, not heard audio.

## The Walker example: walker-jumpman-clawd, and Walker's asset helpers

**Get the builds.** [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman) and [`walker-audio-generator`](https://github.com/nikbearbrown/walker-audio-generator) are public. The audio generator adapts Godot's `audio/generator` demo and keeps the upstream MIT license. The two Jumpman repositories carry no license file (checked 6 October 2026); credit them in `SOURCES.md` as your starting point.

**What it is.** `walker-jumpman-clawd` is Professor Bear's semester-long example, forked from the starter `walker-jumpman`; the chapter's run used commit `382f2ba`. It replaced the player's drawing with Clawd and added 18 animations, keeping the starter's physics, level and tests. Godot 4.7.2, GDScript.

**What its checks establish.** `CLAWD-STATUS.json` records 25 mechanics checks, 9 keyboard checks, and 162 animation samples with 1,944 scalar comparisons plus 6 presentation cases, all passing, with `"human_playtest": "pending"`. A rerun of all three in a scratch copy for the chapter gave 25 PASS, 9 PASS, `{"checks":1950,"failures":0}`. They show that physics and tuning did not change and that the drawing code matches its reference numbers. They do not show that Clawd reads well, that the wide art is fair against the collider, or that anyone enjoys the jump.

**Why it teaches this module.** It has no image or audio files: every pixel is drawn by `_draw()`, and `ASSET-PLAN.md` is a specification only. So you can watch the first generated file arrive and see which settings appear, which files Git keeps, and which of the project's rules (collider unchanged, presentation never writes game state) the asset must obey.

**The trap it carries.** Both starters keep audio out of Git: `walker-jumpman`'s `.gitignore` contains `*.wav`, and `walker-jumpman-clawd`'s contains `*.wav` and `audio/` (checked on GitHub, 27 September and 6 October 2026). Assignment 2 asks you to commit the audio your slice uses. Save a WAV in either starter and `git status` will not show it.

**Walker's asset helpers.** Walker's `asset-gen` skill wraps paid generators (its text: every call costs real money). This course does not use them, and paid output earns no bonus. Three local helpers are free: `grid_slice.py` (Pillow) cuts an image into equal cells; `find_loop_frame.py` needs a frame sequence; `rembg_matting.py` loads a 972,666,916-byte model, so it was not run.

Watch the grid assumption fail. `grid_slice.py TERM-REF-02.jpg -o gridslice --grid 2x2` reported `{"ok": true, "cells": 4, "cell_size": "512x436"}`, but "ok" only means it wrote four files. Counting pixels shows the black soldier cut into four pieces. A generator that lays out creatures freely has not made a grid, and a tool that assumes one reports success anyway.

## Predict → Build It → Use It → Ship It → Verify

The exercise uses TERM-REF-02 because its provenance is on record, gaps included. If you already have a first generated reference of your own for Assignment 2, with its asset-log row, use that instead. Either way this is practice in a scratch copy, not your Assignment 2 slice.

### 1. Predict

Write your answers down before you delegate, and keep them.

1. The black soldier is about 436 source pixels long and must fit a 48-pixel cell. How many source pixels become one sprite pixel? The legs and antennae are about 4 source pixels wide. What happens to them?
2. One image of three different soldiers gives you how many frames of a walk cycle?
3. One `RectangleShape2D` sits on an enemy scene that can show any of the three soldiers, two of them drawn on a diagonal. Where will the box and the drawn body disagree?
4. The starter's `.gitignore` contains `*.wav` and `audio/`. You ask for new sound files in `godot/audio/`. What will `git status` show?

### 2. Build It

Get the project and the reference (public in the course repository). Cloning `main` is fine: commits after `382f2ba` touch only `youtube/`, `design/` and `README.md` (checked 6 October 2026).

```bash
git clone https://github.com/nikbearbrown/walker-jumpman-clawd.git
```

```bash
cd walker-jumpman-clawd
```

```bash
mkdir -p source-art
```

```bash
curl -L -o source-art/TERM-REF-02.jpg https://raw.githubusercontent.com/nikbearbrown/csye-7270-building-virtual-environments/main/fall-2026/nik-bear-brown/assignment-2/reference/termite-soldiers-pixel-02.jpg
```

Write `source-art/PROVENANCE.md` yourself before the agent sees the file. [The version used in the recorded run](../../examples/02-prompting-game-art/PROVENANCE.md) records Gemini (prompted by voice); version, prompt and settings not recorded; derived from web photos of unrecorded source; reference only. Then take a baseline and commit it (ask Claude Code, or run `git add -A` then `git commit -m "Baseline"`):

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

`--fixed-fps 60` pins the game clock. Without it, a frame-counting test measures your machine's speed.

**Prompt 1, the art.** Paste into Claude Code, or save as `PROMPT-1.txt` for a headless run:

```text
This repository is a scratch copy of walker-jumpman-clawd (Godot 4.7.2, GDScript).
Read AGENTS.md and source-art/PROVENANCE.md first.

Task: turn the AI-generated reference source-art/TERM-REF-02.jpg into an
inspectable 2D enemy asset, and prove its import settings, frames and collider
with a headless test. One bounded change: do not edit anything under
godot/features/player/, godot/game/, godot/levels/, godot/ui/, or the existing
tests, and do not change project.godot.

1. Write tools/cut_termites.py (Python 3 with Pillow and NumPy only). Find the
   three soldiers from their non-white pixels, not from a fixed grid. Crop each,
   turn the white background transparent, and scale all three by one shared
   factor so the largest fits a 48 x 48 px cell. Do not rotate, redraw or
   recolour them. Write one horizontal strip,
   godot/features/termite/termite_soldiers.png (144 x 48), and print each
   soldier's source bounding box and the scale factor.
2. Import the strip for crisp 2D use: lossless compression, no mipmaps.
   Nearest filtering is a property of the node, not the import.
3. Make godot/features/termite/termite_frames.tres, a SpriteFrames with one
   animation per soldier (named by head colour), one frame each, each frame an
   AtlasTexture region of the strip.
4. Make godot/features/termite/termite.tscn: an Area2D root on the existing
   Hazard layer, an AnimatedSprite2D child using those frames, and a sibling
   CollisionShape2D whose RectangleShape2D covers the black soldier's head and
   body only, not its legs, antennae or jaws. Write down the size you chose
   and how you measured it.
5. Make godot/art_lab/termite_lab.tscn showing all three soldiers beside the
   real Clawd player at the game's 640 x 360 scale, for a human to judge.
6. Write godot/tests/test_termite_art.gd (extends SceneTree). Print one
   PASS/FAIL line per check and exit non-zero on any failure. Check the
   strip's .import parameters, the texture size, three animations with exactly
   one 48 x 48 frame each, texture_filter NEAREST on the sprite, the collider
   size, that the collider is not a child of the sprite, and the Hazard layer bit.
7. Run godot --headless --path godot --import, then your test, then the three
   existing test commands in README.md. Report the real output. Do not claim
   the termite is readable at game size; that is a human check.
```

The recorded headless run, on 27 September 2026:

```bash
claude -p "$(cat PROMPT-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*)" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

For later runs, add `--strict-mcp-config` (loads only MCP servers you name, so none), `--settings '{"autoMemoryEnabled":false}'` (no auto memory) and `--disallowedTools "Skill"` (a nested session cannot invoke a settings-writing skill). Check Prompt 1's result yourself and commit it before continuing.

**Prompt 2, the sound.** Same repository:

```text
Same repository, next bounded change: audio plumbing, before any generated
sound exists. Read godot/game/session.gd and godot/features/player/player.gd,
but do not edit them, the level, the tuning, project.godot, or any existing
test.

1. Write tools/make_test_tones.py (Python standard library only). It writes
   16-bit mono 44.1 kHz WAV files to godot/audio/placeholder/: jump.wav (80 ms),
   fail.wav (250 ms) and music_loop.wav (exactly 4.000 s, two bars at 120 BPM,
   starting and ending on a zero crossing). Add a README.md in that folder
   saying these are synthesized test tones, not generated or final assets.
2. Import music_loop.wav with loop mode Forward from the first to the last
   sample, and the two effects with looping disabled.
3. Add godot/audio/audio_cues.gd as a child node of the main scene. It only
   observes existing state: one jump cue for each increase of player.jumps,
   one fail cue for each entry into the DYING state, music while PLAYING,
   paused while PAUSED, stopped on COMPLETE. It must never write game state.
   Count every play() call per cue.
4. Write godot/tests/test_audio_cues.gd (extends SceneTree). Drive the real
   game through the player's existing test inputs, never by setting state:
   three jumps, one death on the spikes, one pause and resume. Check exactly
   one jump cue per jump, exactly one fail cue per death, the music's imported
   loop settings, and that the same inputs without the audio node end in the
   same game state. One PASS/FAIL line per check; exit non-zero on failure.
5. Every file the game loads must be committable. Run git status and
   git check-ignore -v on each new file and report which are ignored and by
   which rule. Do not edit .gitignore; that decision is mine.
6. Run the import, then your test, test_termite_art.gd and the three existing
   tests, each with --fixed-fps 60, and report the real output. Hearing the
   loop seam is a human check.
```

The tones are synthesized by a formula. They prove the plumbing (import settings, event wiring, trigger counts) and are not generated audio. Your real sounds replace them under the same names, and the test keeps checking the wiring.

**The Codex difference.** The same prompts run with `codex exec`. Codex reads `AGENTS.md` automatically; Claude Code reads it directly only from version 2.1.277 on, and only when there is no `CLAUDE.md` (Module 0), hence the prompt's instruction. Claude Code's `--allowedTools` decides which commands may run; Codex's `--sandbox workspace-write` confines writes to the working folder. Close standard input when you script Codex, or it can wait for input:

```bash
codex exec --sandbox workspace-write --json "$(cat PROMPT-1.txt)" < /dev/null > session-codex.jsonl
```

### 3. Use It

Open the project in the Godot editor and do what no test did. Every judgment here is a **HUMAN CHECK**; write down what you observe.

1. Open `res://art_lab/termite_lab.tscn` and use **Run Current Scene**. **HUMAN CHECK:** each sprite pixel is two screen pixels. Can you tell the black soldier's head from its jaws? Are the legs legs, or a scatter of dots? Does a top-down creature belong beside a side-view Clawd?
2. Set a soldier's **CanvasItem > Texture > Filter** to **Inherit**. The project default is Linear, so the sprite goes soft. Set it back to Nearest.
3. Open `res://features/termite/termite.tscn`, turn on **Debug > Visible Collision Shapes**, and switch the `AnimatedSprite2D` between black, red and yellow. **HUMAN CHECK:** the rectangle stays put while the art changes under it. Is it fair for each one?
4. Read the **Import** dock for `termite_soldiers.png` (Lossless, no mipmaps) and `music_loop.wav` (Loop Mode Forward, Loop Begin 0, Loop End 176399).
5. Run the game with sound on. Jump, die on the spikes, pause with Escape. **HUMAN CHECK:** does each cue happen once, when you expect it? Listen to at least three repetitions of the loop. A 100 Hz test tone tells you little about a musical seam; your generated loop will tell you a lot.

A screenshot of the lab beside the collider overlay from Verify is good evidence for `TEST-REPORT.md`.

### 4. Ship It

Commit the scripts, scenes, resources, tests, the PNG and every `.import` file, but not `.godot/`. Before you commit anything audio, look at what Git will actually take:

```bash
git status --short --ignored
```

```bash
git check-ignore -v godot/audio/audio_cues.gd
```

If the second command prints a rule, that file will not reach GitHub or a grader's clone. Changing the rule is your decision. The worked example made one narrow change, re-including `godot/audio/` after the `audio/` rule, and proved it with `git check-ignore -v --no-index`.

Add a `FRICTIONAL.md` entry in the Assignment 2 format: what you wanted, what you asked for, what came back, what you decided, and who did what (you, the coding agent, the generative model). Add the reference's asset-log row with its "not recorded" fields left visible. If you film the work, use **godot-gamedev** with the `walker` modifier from the course-provided checkout of [Brutalist](https://github.com/nikbearbrown/brutalist.art); request the update if your copy lacks it. It pairs each code excerpt with its visible result, the import-to-screen trace this exercise produces.

### 5. Verify

Run the agent's tests yourself. `timeout` (GNU coreutils; on macOS, Homebrew's `coreutils`) stops a script that errors before `quit()`, which otherwise leaves headless Godot running forever:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_termite_art.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_audio_cues.gd --fixed-fps 60
```

Then run checks the agent did not write. Copy `verify_collider_vs_alpha.py` and `verify_audio_real_scene.gd` from [`examples/02-prompting-game-art/scripts/independent/`](../../examples/02-prompting-game-art/scripts/independent/) into your repository root. The first compares the collider with every frame's opaque pixels and writes an 8x overlay. The second loads the real `main.tscn`, drives Clawd only through test inputs, and logs the physics frame of each event and cue.

```bash
python3 verify_collider_vs_alpha.py . --overlay overlay-8x.png
```

```bash
timeout 120 godot --headless --path godot --script "$PWD/verify_audio_real_scene.gd" --fixed-fps 60
```

Finally, clone your own commit and run the tests there, reading the errors and not only the exit code:

```bash
git clone . ../fresh-clone
```

```bash
godot --headless --path ../fresh-clone/godot --import
```

**What a pass proves:** import parameters, texture size, frame regions, node filter, collider size and layer are what the files say, and cue counters rose once per event in a scripted run. **What it does not prove:** that the sprite reads at game size, that the collider is fair for every variant, that a sound is audible or the loop has no click, or that a grader's clone contains the files. Headless Godot uses the Dummy audio driver, so a cue counter is a state change, not a sound.

## What the agents got wrong

Run on 27 September 2026 with Claude Code 2.1.150 and Codex CLI 0.153.4. Every test the agents wrote passed; checks run outside them still found these. An agent's "done" is a claim.

- **The collider test checked the agent's own number.** The agent chose a 20 x 34 box, and its test asserted `size == Vector2(20, 34)`. An independent check against each frame's opaque pixels found the box covers 77% of the black soldier's pixels and cuts off seven rows of its abdomen; for the yellow soldier, 458 of the collider's 680 pixels are empty.
- **The sound test broke its own rule.** The prompt said "never by setting state". The test set `game.player.position`, called `game.set_paused(true)`, and built its own `AudioCues` node instead of loading `main.tscn`.
- **The effects were imported as "detect loop".** Both had `edit/loop_mode=0`, not Disabled, and did not loop only because the tone files carry no loop chunk.
- **A fresh clone was broken while every test stayed green.** The `audio/` rule on `.gitignore` line 23 kept `godot/audio/` out of Git, which the agent reported honestly. In a clone, `main.tscn` printed a parse error, `test_audio_cues.gd` failed to parse, and `godot` still exited 0, while the other 62 checks passed.

## If you know Unity or Unreal

| Godot 4.7 | Unity 6 | Unreal Engine 5 |
|---|---|---|
| `.import` file (ConfigFile text) | `.meta` file (YAML under Force Text) | `.uasset`, binary |
| `texture_filter` = Nearest, on the node | Filter Mode: Point, on the importer | Filter Nearest, on the texture |
| `SpriteFrames` + `AtlasTexture` regions | Sprite Mode: Multiple + Sprite Editor slices | Paper 2D Sprites and a Flipbook |
| `CollisionShape2D` + `RectangleShape2D` | `BoxCollider2D` | Sprite collision (Fully Custom) |
| WAV import loop mode and sample points | `AudioSource.loop`; no clip loop points | Sound Wave `Looping` flag |
| `AudioStreamPlayer` | `AudioSource` | A Sound Wave played directly, or a Sound Cue or MetaSound |
| `godot --headless --script res://tests/…` | `Unity -batchmode -runTests …` | `UnrealEditor-Cmd … -ExecCmds="Automation RunTest …"` |

For an agent workflow, the biggest difference is what it can read. Godot's `.import`, `.tres` and `.tscn` files are plain text it can diff. Unity's `.meta`, scenes and prefabs are diffable YAML under Force Text, the manual's default. Unreal's textures, sprites and flipbooks are binary `.uasset` files, so an agent works through editor Python. Unity and Unreal were not run; the comparisons come from their documentation, checked on 27 September 2026. The [chapter](../../chapters/02-prompting-game-art.md) has the full comparison.

## Practice assessment (ungraded)

Answer these in writing, from the source and the running game.

1. Write the check that would have caught the yellow soldier's empty collider. Where should each soldier's collider data live so that switching the animation cannot leave the wrong box behind?
2. Why did `godot` exit 0 when `test_audio_cues.gd` could not be parsed in the fresh clone? What would you add to a script so that case fails?
3. Name one thing a headless audio test can establish and one thing only your ears can.
4. For one asset you will generate for Assignment 2, write the prompt constraint, Godot check and human check for size, background and loop.

The ungraded Canvas practice quiz has six questions with feedback. Do not paste Claude's explanation as proof of your understanding; ask it to question you, then answer and check the source yourself.

## The next step

Assignment 2, **"Generate Art, Sound, and Music for Your Game,"** opens in Module 2 and is due about Day 20; the Canvas page governs the date. Your constraint table feeds the prompts and predicted failures in `CHANGE-BRIEF.md`, your collider reasoning feeds the collision overlay in `CHARACTER-SHEET.md`, and the asset log and rights rules go into `SOURCES.md`. The one-cue-per-event test and the `git check-ignore` habit become your automated check and your fresh-copy run. This lesson adds no graded deliverable. For the long reading, see [Chapter 2 — Prompting Game Art (and Sound) Against the Engine](../../chapters/02-prompting-game-art.md).
