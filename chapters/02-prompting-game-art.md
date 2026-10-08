# Chapter 2 — Prompting Game Art (and Sound) Against the Engine

CSYE 7270 · Fall 2026 · Week 2

## Executive summary

**What this chapter is.** The teaching chapter behind Assignment 2. You will prompt image, sound and music models for your game, and then judge what comes back where it counts: inside Godot, at game size, on real events. It covers prompting against technical constraints (on-screen size, palette, silhouette, frame count, tileability, loopability), recording provenance and rights, and the Godot machinery that decides whether a generated file becomes a usable asset: the import pipeline, texture filtering, `SpriteFrames`, collision shapes, audio import and loop points, and `AudioStreamPlayer` wired to real game events.

**Why read it.** A generated image that looks finished in a folder has not yet met a single engine constraint. Its size, background, frame layout, perspective and collider are all still open. So is the loop point of a music file nobody has imported.

**What you will build.** In a scratch copy of `walker-jumpman-clawd`, you direct a coding agent to turn one AI-generated reference image, Professor Bear's pixel-art termite soldiers, into a checked Godot asset: a transparent sprite strip, correct import settings, a `SpriteFrames` resource, an enemy scene with a separate collider, and a headless test. Then you have it wire placeholder sounds to real game events and count the triggers.

**What it proves and what it does not.** In the worked example, every test the agents wrote passed. Checks run outside the agents still found four real defects. The collider fit one of the three soldiers. The sound test broke its own "never set state" rule. The effects were imported as "detect loop", not "no loop". And the starter's `.gitignore` kept the new audio folder out of Git, so a fresh clone could not load the main scene while every existing test stayed green. A second agent fixed the last three; the first is yours. None of this shows that the termite reads well at 48 pixels or that a sound feels right. Those are human checks, and the assignment grades them.

---

## The question

Professor Bear's Assignment 2 log records a Gemini image he accepted as "closer to a game sprite" than his first try: three big-headed termite soldiers in a pixel-art style, asset TERM-REF-02. In an image viewer it looks like game art.

Now ask the engine's questions. The file is a 1,024 x 873 JPEG. The Clawd game renders a 640 x 360 viewport, and its player collides as an 18 x 28 pixel box. The picture's "pixels" are drawn roughly four source pixels wide, then smoothed and JPEG-compressed, so they sit on no exact grid. The background is white, not transparent. The three soldiers are three different creatures, not three frames of one. They are seen from above, and the game is seen from the side.

The image viewer shows you none of that. So what has to happen between "the model gave me a nice picture" and "this is an asset in my game", and which of those steps can a machine check for you?

---

## Ideas you need

### 1. A prompt is a specification, and the engine reads the result

An image model reads your prompt. Godot reads the file the model gives back, and the two readers want different things. The model responds to mood words: "menacing", "retro", "crisp". Godot responds to numbers: pixel dimensions, an alpha channel, a frame grid, a loop point in samples. A prompt made only of mood words produces a picture. A prompt that carries the engine's numbers produces something you can check.

Put each constraint in the prompt, and decide before you generate how you will check it once the file is in Godot:

| Constraint | Put it in the prompt as | Check it in Godot as |
|---|---|---|
| On-screen size | "reads as a 32-pixel-tall sprite in a 640 x 360 game" | Beside the player in the running scene, at 1:1 viewport scale |
| Background | "centred on a solid medium-gray background" (never "transparent") | The imported texture has alpha; its corners are alpha 0 |
| Palette | three to six hex values from your character sheet | Sample imported pixels against the environment behind them |
| Silhouette | "bold, flat, readable outline" | Fill it black at game size: does the shape still say what it is? |
| Frame count and layout | "4 frames in one row, equal cells, same scale and baseline" | `SpriteFrames.get_frame_count()` and each frame's region |
| Orientation | "side view, facing right" | `flip_h` makes the left-facing version; the right-facing one must exist |
| Tileability | "seamless, edges wrap" | Tile it 3 x 3 and look at the seams |
| Loopability (audio) | "120 BPM, 8 bars, no fade-out" | Import loop points; listen across the seam three times |

Two of these rules come from Walker's own `asset-gen` skill: "never prompt for a 'transparent background' (the generator bakes a checkerboard)", and generate one facing direction and flip it at runtime, because "'facing left' vs 'right' often comes out identical" (`walker/asset-gen/rembg.md`, `walker/asset-gen/SKILL.md`).

The old Unity/Unreal course named a tool per week: Midjourney and DALL-E 3 for sprites, Stable Diffusion with ControlNet for textures, Suno and Audacity for audio (old syllabus, weeks 3, 5 and 13). The revised syllabus names no single tool ("Gemini, ChatGPT, Midjourney, or available alternatives"). The tools change every term. The constraints above do not.

### 2. Provenance is part of the asset

A generated file without its record is an unlabelled bottle. Assignment 2's asset log asks for the model and version, where it ran, its license or terms, the exact prompt and settings, the outcome, the edits, and where the file is used. That record does three jobs.

- **Reproduction.** A TA may ask you to regenerate an asset from your log.
- **Rights.** The U.S. Copyright Office's January 2025 report on copyrightability concluded that AI output is protected only where "a human author has determined sufficient expressive elements", and not for "the mere provision of prompts". Your selection, edits and arrangement are the parts that are yours; the log is how you show them.
- **Contamination.** A reference carries its history. Bear's log records this problem precisely: TERM-REF-02 was made with Gemini from TERM-REF-01, which was made from three web photos whose source and license were not recorded, and Claude noted that "an image made from them may still count as derived from those photos." The same log records a rejection: Gemini heard "those termites" as "Kratos termites" and drew termites with a copyrighted game character's face. Bear kept those off GitHub.

The course's rules are narrower than the law: no named living artist's style, no copyrighted character, no brand, no existing music or recordings as reference, no cloned voices (Assignment 2). Open models are allowed, and some carry non-commercial terms: Meta's AudioCraft repository releases its code under MIT but its model weights (MusicGen, AudioGen) under CC-BY-NC 4.0. That is acceptable for coursework if `SOURCES.md` says so.

### 3. The import pipeline: source file, `.import` file, cache

Godot never uses your PNG or WAV directly at runtime. When the editor finds a new source file it runs an **importer**, writes the converted resource into `res://.godot/imported/`, and writes a sidecar next to the source, such as `termite_soldiers.png.import`. The documentation is explicit: commit the `.import` files; do not commit `.godot/` ([Import process](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html)).

The `.import` file is plain text in Godot's `ConfigFile` format, which is what makes the course's workflow possible: an agent can read it, a diff can show it, a test can assert on it. These are the `[params]` Godot 4.7.2 wrote for a fresh PNG in a probe project (nine lines about normal maps, channel remapping and Basis Universal omitted):

```text
compress/mode=0
compress/high_quality=false
compress/lossy_quality=0.7
mipmaps/generate=false
mipmaps/limit=-1
process/fix_alpha_border=true
process/premult_alpha=false
process/hdr_as_srgb=false
process/size_limit=0
detect_3d/compress_to=1
```

You can run the importer without opening the editor: `godot --import` "starts the editor, waits for any resources to be imported, and then quits" (`godot --help`, 4.7.2).

### 4. Texture settings that decide whether a sprite survives

| Setting | Lives in | What it does | For a 2D sprite |
|---|---|---|---|
| `compress/mode` | `.import` | 0 Lossless (the default), then, in the order the docs list them, 1 Lossy, 2 VRAM Compressed, 3 VRAM Uncompressed, 4 Basis Universal | 0. The docs recommend Lossless for pixel art; VRAM compression should be "avoided for 2D as it exhibits noticeable artifacts" |
| `mipmaps/generate` | `.import` | Pre-shrunk copies for zoomed-out drawing, about 33% more memory | Off unless the camera zooms far out |
| `process/fix_alpha_border` | `.import` | Fills transparent pixels next to the art with the neighbouring colour, so filtering does not pull in a halo | On (the default) |
| `detect_3d/compress_to` | `.import` | If the texture is later used in 3D, Godot switches it to VRAM compression with mipmaps and reimports | Leave it, but know that putting your sprite on a 3D quad changes its import |
| `texture_filter` | the **node** (`CanvasItem`) | 1 Nearest reads one texel; 2 Linear blends four; 0 inherits from the parent | Nearest for pixel art. The project default (`rendering/textures/canvas_textures/default_texture_filter`) is Linear in 4.7.2 |

The last row catches Unity users. Since Godot 4.0, "texture filter and repeat modes are set in the CanvasItem properties in 2D... and in a per-material configuration in 3D", not in the importer ([Importing images](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)). Setting it on the sprite node keeps the change bounded; setting the project default changes every textured node in the game.

**sRGB.** Godot treats colour textures as sRGB data and renders in linear space. In 2D there is no sRGB checkbox to get wrong. It becomes your problem in two places: HDR images, where `process/hdr_as_srgb` corrects files that store sRGB data, and shaders, where a colour sampler needs the `source_color` hint so it is converted before lighting ([shading language](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html)). Chapter 6 returns to this.

### 5. Frames: `SpriteFrames` and `AnimatedSprite2D`

Godot animates a sheet in two ways ([2D sprite animation](https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html)):

- **`AnimatedSprite2D` + `SpriteFrames`.** A `SpriteFrames` resource holds named animations, each a list of frame textures with a speed in frames per second and a loop flag. A new `SpriteFrames` in 4.7.2 contains one animation, `default`, at 5 FPS, looping. Frames cut from one sheet are usually `AtlasTexture` resources: the sheet plus a `region` rectangle. All of it lives in a `.tres` text file.
- **`Sprite2D` + `AnimationPlayer`.** `Sprite2D` has `hframes`, `vframes` and `frame`; an `AnimationPlayer` track keys `frame`. Use it when the frame change must line up with other tracks, such as a hitbox or a sound.

Frame count is a fact a test can check. A frame that is a new pose and a frame that is a different *creature* look identical to that test. Only you can tell them apart.

### 6. The collider is not the art

Chapter 1's rule holds for generated art. Walker Jumpman Clawd shows it in source: `features/player/player.gd` builds an 18 x 28 `RectangleShape2D` in `_ready()`, and `clawd_art.gd` promises "Drawing only: never writes a body's position, velocity, input, or collision shape." Clawd's arms are drawn outside that box, and the README calls the trade-off a human judgment: "The wide art extends beyond the original 18 x 28 collision box; that tradeoff needs human inspection."

For generated sprites: keep the `CollisionShape2D` a **sibling** of the sprite, not its child, so scaling or flipping the art never changes the collider; size it from what the player *believes* is solid (the body), not from the image rectangle with its antennae, legs and margin; and write down why. Art beyond the collider is fair when it is thin or decorative. It is unfair when it looks like the part that hurts you.

### 7. Sound: import, loop, trigger

Godot's documentation recommends "WAV for short and repetitive sound effects, and Ogg Vorbis for music, speech, and long sound effects": WAV is cheap on the CPU, Ogg small on disk ([Importing audio samples](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html)). The course keeps MP3 files out of GitHub, so deliver Ogg or WAV. The two importers handle loops differently. These are 4.7.2's defaults from a probe import:

```text
# sound.wav.import (importer "wav")        # music.ogg.import (importer "oggvorbisstr")
edit/trim=false                            loop=false
edit/normalize=false                       loop_offset=0
edit/loop_mode=0                           bpm=0
edit/loop_begin=0                          beat_count=0
edit/loop_end=-1                           bar_beats=4
compress/mode=2
```

For WAV, `edit/loop_mode` is 0 Detect from WAV, 1 Disabled, 2 Forward, 3 Ping-Pong, 4 Backward, and `loop_begin`/`loop_end` count **samples**; `-1` means the last sample. `compress/mode=2` is Quite OK Audio, the default; 0 is uncompressed PCM. Careful: in the loaded `AudioStreamWAV` resource the numbering shifts by one, because the resource has no "detect" option. We imported the same file with each mode: importer 2 (Forward) loads as `loop_mode` 1, `LOOP_FORWARD`. Ogg and MP3 have only a loop *offset*, where playback restarts, and no loop end: "Ogg Vorbis and MP3 only support a 'loop begin' loop point". Cut a generated music track at a bar boundary *before* you import it as Ogg; Godot cannot end the loop early for you.

Playback happens through a node. `AudioStreamPlayer` is non-positional; `AudioStreamPlayer2D` and `AudioStreamPlayer3D` pan and attenuate by position. `max_polyphony` defaults to 1, and "Calling play() after this value is reached will cut off the oldest sounds" ([AudioStreamPlayer](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html)). That is the engine-level cause of the double-trigger bug students meet most often. Two calls in one frame sound like one clipped sound; two calls a few frames apart sound like a stutter. The fix is not in the audio file. It is in the event: play on the *transition* into a state, not on every frame the state is true.

Assignment 2's rule that "sound must never decide game state" comes with a test: remove the audio node, send the same inputs, and the game must end in the same state.

### 8. Procedural audio is not generative audio

`walker-audio-generator`, a Walker adaptation of Godot's `audio/generator` demo, makes sound with no file at all: `generator_demo.gd` fills an `AudioStreamGeneratorPlayback` buffer every frame with `push_frame(Vector2.ONE * sin(phase * TAU))`, a 440 Hz sine at a 22,050 Hz mix rate. That is **procedural synthesis**, a formula evaluated sample by sample. It is **not a generative model**, and it does not satisfy Assignment 2's generative-model requirement, any more than "code-drawn or SVG art written by Claude" does. Its record also shows what a headless audio test can prove: 15 assertions pass on the Dummy driver, and "these are synthetic GUI input and headless/Dummy-driver state checks, NOT heard audio or waveform verification" (`walker-audio-generator/FRICTIONAL.md`).

---

## The Walker example: walker-jumpman-clawd, and Walker's asset helpers

<!-- public-walker-repos -->
**Get the builds.** Every Walker project this chapter names is a public repository: [`walker-jumpman-clawd`](https://github.com/nikbearbrown/walker-jumpman-clawd), [`walker-jumpman`](https://github.com/nikbearbrown/walker-jumpman), [`walker-audio-generator`](https://github.com/nikbearbrown/walker-audio-generator). The adaptations of Godot's demo projects were published on 27 September 2026, each keeping the upstream MIT license and adding a Walker brief, a recovered GDD and its headless tests. Cloning the Walker repository is the quickest start. Where this chapter also gives an upstream `godot-demo-projects` path and commit, that records where the build came from, and it remains a valid starting point.

**What it is.** `walker-jumpman-clawd` is Professor Bear's semester-long example, forked from the course starter `walker-jumpman` (commit `9387542`) and public at `github.com/nikbearbrown/walker-jumpman-clawd`. This chapter used commit `382f2ba`. Its first iteration replaced the player drawing with Clawd and added a gallery of 18 animations, keeping the starter's physics, level and tests. Godot 4.7.2, GDScript, Compatibility renderer, a 640 x 360 viewport stretched to 1280 x 720 (`godot/project.godot`).

**What its checks establish.** `CLAWD-STATUS.json` records 25 mechanics checks and 9 keyboard checks passing, and 162 animation samples with 1,944 scalar comparisons plus 6 presentation cases, all passing, with `"human_playtest": "pending"`. We reran all three in a scratch copy: 25 PASS, 9 PASS, `{"checks":1950,"failures":0}`. They establish that the physics and tuning did not change and that the drawing code matches its reference numbers. They do not establish that Clawd reads well, that the wide art is fair against the collider, or that anyone enjoys the jump.

**Why it teaches this chapter.** It has *no* image or audio files. Every pixel is drawn by `_draw()`, and `ASSET-PLAN.md` opens: "Specification only; no runtime art/audio created or selected." Its sound entries are plans: SND-001 effects "Optional; omit in first greybox", SND-002 music "Absent". So it is a clean place to watch the first generated file arrive: which settings appear, which files Git keeps, and which of the project's own rules (collider unchanged, presentation never writes game state) the new asset must obey.

**One trap it carries for Assignment 2.** Both public starters keep audio out of Git. `walker-jumpman`'s `.gitignore` contains `*.wav`; `walker-jumpman-clawd`'s contains `*.wav` and `audio/` (checked on GitHub, 27 September 2026). Assignment 2 asks you to commit the WAV or Ogg files your slice uses. Start from either starter, save WAVs, and `git status` will not show them.

**The Walker asset helpers.** Walker's `asset-gen` skill wraps paid generators: Gemini images at 5 to 15 cents, Grok at 2 cents, Tripo3D models from 30 cents ("These are paid APIs — every call costs real money"). This course does not use them. Its three local helpers are free, and they differ in what they need:

| Helper | Needs | Does | Run here? |
|---|---|---|---|
| `grid_slice.py` | Pillow | Cuts an image into equal cells (`--grid 2x2 --names a,b,c,d`) | Yes, below |
| `find_loop_frame.py` | Pillow, NumPy | Finds the video frame most like the first (32 x 32 embeddings, cosine similarity, threshold 0.90) so a walk or idle cycle can be trimmed to loop | No: it needs a frame sequence |
| `rembg_matting.py` | `rembg`, `pymatting`, ONNX Runtime and the BiRefNet model | Mattes out a solid background with colour matting plus a BiRefNet soft mask | No: it loads BiRefNet in every mode, and the model file `rembg` downloads on first use is 972,666,916 bytes |

The grid assumption is worth seeing fail. `grid_slice.py TERM-REF-02.jpg -o gridslice --grid 2x2` reported `{"ok": true, "cells": 4, "cell_size": "512x436"}`. "ok" means it wrote four files. A pixel count of those files shows that every cell has foreground touching an inside edge. The black soldier is cut into four pieces: the tips of its jaws land in the two upper cells, and its body is split down the middle, with 370 foreground rows on each side of x = 512. A generator that lays out creatures freely has not made a grid, and a tool that assumes one reports success anyway.

---

## Hands-on: turn one generated image into a checked Godot asset, then wire sound to real events

The exercise uses TERM-REF-02 because its provenance is on record, gaps included. If you already have a first generated reference of your own for Assignment 2, with its asset-log row, use that instead. Either way this is practice, not your Assignment 2 slice: the image is a reference, and the sounds are test tones.

### Predict

Write your answers down before you delegate.

1. The black soldier is about 436 source pixels long and must fit a 48-pixel cell. How many source pixels become one sprite pixel? The legs and antennae are about 4 source pixels wide. What happens to them?
2. One image of three different soldiers gives you how many frames of a walk cycle?
3. One `RectangleShape2D` sits on an enemy scene that can show any of the three soldiers, two of them drawn on a diagonal. Where will the box and the drawn body disagree?
4. The starter's `.gitignore` contains `*.wav` and `audio/`. You ask for new sound files in `godot/audio/`. What will `git status` show?

### Build It

Get the project and the reference. The image is public in the course repository.

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

Write `source-art/PROVENANCE.md` yourself before the agent sees the file; `examples/02-prompting-game-art/PROVENANCE.md` is the version we used (model Gemini by voice; version, prompt and settings not recorded; derived from web photos of unrecorded source; reference only). Then take a baseline and commit it:

```bash
godot --headless --path godot --import
```

```bash
godot --headless --path godot --script res://tests/test_game.gd --fixed-fps 60
```

`--fixed-fps 60` pins the game clock; without it, a frame-counting test measures your machine's speed (Chapter 0, "The time trap").

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

The prompt names what may not change, forbids the grid assumption, separates the import from the node filter, asks for the collider to be measured and justified, and reserves the readability judgment for you. Our headless run:

```bash
claude -p "$(cat PROMPT-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*)" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

For later runs we added `--strict-mcp-config`, which loads only MCP servers named with `--mcp-config` (none, so no remote tools), and `--settings '{"autoMemoryEnabled":false}'`, which turns off auto memory for the run. Other chapters' runs also found it wise to add `--disallowedTools "Skill"` so a nested session cannot invoke a settings-writing skill.

**Prompt 2, the sound.** After you have checked Prompt 1's result yourself and committed it:

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

The tones are synthesized by a formula, like `walker-audio-generator`'s sine. They prove the plumbing: import settings, event wiring, trigger counts. They are not generated audio and do not count for Assignment 2. When your real sounds arrive, they replace these files under the same names, and the test keeps checking the wiring.

**The Codex difference.** The same prompts run with `codex exec`. Codex reads `AGENTS.md` automatically; Claude Code reads `CLAUDE.md` and, from version 2.1.277, falls back to `AGENTS.md` only when there is no `CLAUDE.md` (Chapter 0). The 2.1.150 used for these runs did not, which is why the prompt says "Read AGENTS.md first". The permission models differ in kind: Claude Code's `--allowedTools` decides *which commands* may run, while Codex's `--sandbox workspace-write` lets the model run the commands it chooses but confines writes to the working folder. Close standard input when you script Codex, or it can wait on "Reading additional input from stdin":

```bash
codex exec --sandbox workspace-write --json "$(cat PROMPT-1.txt)" < /dev/null > session-codex.jsonl
```

### Use It

Open the project in the Godot editor and do what no test did.

1. Open `res://art_lab/termite_lab.tscn` and use **Run Current Scene**. Each sprite pixel is two screen pixels in the 1280 x 720 window. Can you tell the black soldier's head from its jaws? Are the legs legs, or a scatter of dots? Does a top-down creature belong beside a side-view Clawd?
2. Select a soldier and set **CanvasItem > Texture > Filter** to **Inherit**. The project default is Linear, and the sprite goes soft. Set it back to Nearest.
3. Open `res://features/termite/termite.tscn`, turn on **Debug > Visible Collision Shapes**, and switch the `AnimatedSprite2D` between black, red and yellow. Watch the rectangle stay put while the art changes shape under it.
4. Select `termite_soldiers.png` and read the **Import** dock (Lossless, no mipmaps). Select `music_loop.wav` (Loop Mode Forward, Loop Begin 0, Loop End 176399).
5. Run the game with sound on. Jump, die on the spikes, pause with Escape. Does each cue happen once, when you expect it? Listen to at least three repetitions of the loop. A 100 Hz test tone tells you little about a musical seam; your generated loop will tell you a lot.

A screenshot of the lab next to the collider overlay from Verify is good evidence for your `TEST-REPORT.md`.

### Ship It

Commit the scripts, scenes, resources, tests, the PNG and every `.import` file, but not `.godot/`. Before you commit anything audio, look at what Git will actually take:

```bash
git status --short --ignored
```

```bash
git check-ignore -v godot/audio/audio_cues.gd
```

If the second command prints a rule, that file will not reach GitHub and a grader's fresh clone will not have it. Changing the rule is your decision; the worked example shows one narrow change and how to prove it.

Add a `FRICTIONAL.md` entry in the Assignment 2 format: what you wanted the player to see or hear, what you asked for, what came back, what you decided, and who did what (you, the coding agent, the generative model). Add the reference's asset-log row with its "not recorded" fields left visible. If you explain the work in a film, the Brutalist skill Assignment 2 requires is **godot-gamedev** with the `walker` modifier; it pairs each code excerpt with its visible result, which is the import-setting-to-screen trace this exercise produces.

### Verify

Run the agent's tests yourself. `timeout` (GNU coreutils; on macOS it comes with Homebrew's `coreutils`) stops a test script that errors before it reaches `quit()`, which otherwise leaves headless Godot running forever:

```bash
godot --headless --path godot --import
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_termite_art.gd --fixed-fps 60
```

```bash
timeout 120 godot --headless --path godot --script res://tests/test_audio_cues.gd --fixed-fps 60
```

Then run checks the agent did not write. Copy `verify_collider_vs_alpha.py` and `verify_audio_real_scene.gd` from `examples/02-prompting-game-art/scripts/independent/` into your repository root. The first compares the collider with every frame's opaque pixels and writes an 8x overlay for your eyes. The second loads the real `main.tscn`, drives Clawd only through its test inputs, and logs the physics frame of each event and each cue.

```bash
python3 verify_collider_vs_alpha.py . --overlay overlay-8x.png
```

```bash
timeout 120 godot --headless --path godot --script "$PWD/verify_audio_real_scene.gd" --fixed-fps 60
```

(Godot accepts an absolute path for `--script`, so the check can live outside the project; that keeps it out of your game.)

Finally, clone your own commit and run the tests there, reading the errors and not only the exit code:

```bash
git clone . ../fresh-clone
```

```bash
godot --headless --path ../fresh-clone/godot --import
```

What a pass proves: the import parameters, texture size, frame regions, node filter, collider size and layer are what the files say, and the cue counters rose once per observed event in a scripted run. What it does not prove: that the sprite reads at game size, that the collider is fair for every variant, that a sound is audible or pleasant, that the loop has no click, or that the repository a grader clones contains the files. Headless Godot uses the Dummy audio driver; a cue counter is a state change, not a sound.

---

## What we actually ran

**When and with what.** 27 September 2026, macOS on an Apple M4 Pro. Godot `4.7.2.stable.official.ed1daf0bf`. Claude Code 2.1.150; its transcripts record `claude-sonnet-4-6`, the account default (we did not pass `--model`). Codex CLI 0.153.4 with the model in the local configuration (`gpt-5.6-sol`, reasoning effort low). Starting revision: `walker-jumpman-clawd` `382f2ba`, its `godot/` folder, top-level Markdown and `.gitignore` copied to a scratch folder, plus `source-art/TERM-REF-02.jpg` (SHA-256 `69f812f0…4718`) and its provenance note, committed as a local baseline. The full record (scripts, logs, diffs, sanitized transcripts) is in [`../examples/02-prompting-game-art/`](../examples/02-prompting-game-art/).

**Baseline.** Import clean; 25/25 mechanics, 9/9 keyboard, and `{"checks":1950,"failures":0}`, all with `--fixed-fps 60`.

**Run 1, Claude Code, Prompt 1.** 53 turns, 19 minutes. The agent looked at the image, wrote `tools/cut_termites.py`, and caught its first failure itself: it tried to name the soldiers by head colour, and the red soldier's dark maroon head read as "black". Its fix was to classify by *position* in this image ("layout-specific to TERM-REF-02's triangular arrangement", in its words), which makes the script right for this file and wrong for any other. It printed a shared scale factor of 0.110092 (the black soldier, 308 x 436 source pixels, becomes 34 x 48) and resampled with `Image.NEAREST`, so each sprite pixel keeps one source pixel out of about nine. It built the strip, a `SpriteFrames` with three one-frame animations (black, red, yellow; 48 x 48 `AtlasTexture` regions; 5 FPS), the `Area2D` scene on layer value 8 with `texture_filter = 1` on the sprite and a sibling 20 x 34 collider, an art-lab scene (it paints Clawd with the player's drawing code at game scale instead of instancing the player, whose script expects the game session as its parent), and a 28-check test. Its measured "body core" was 19 x 43; it chose 20 x 34 "to exclude the antennae at the top and jaw/leg extremities". It reported 28/28 and the original tests passing, and made no readability claim.

We reran everything: 28/28, 25/25, 9/9, 1,950/0. We broke the test on purpose, setting the sprite's filter to Linear: it printed `FAIL sprite texture_filter == NEAREST` and exited 1, so it can fail. Then the check the agent did not write:

```text
collider 20x34 -> cell cols 14..33, rows 7..40
black  art bbox 33x48; opaque inside collider 77%; collider area that is transparent 237 of 680 px
red    art bbox 32x40; opaque inside collider 73%; collider area that is transparent 353 of 680 px
yellow art bbox 33x30; opaque inside collider 86%; collider area that is transparent 458 of 680 px;
       collider rows with no art [7, 8, 12, 39, 40]
```

The rectangle is centred on the black soldier, whose body runs all 48 rows, so it cuts off the last seven rows of the abdomen (73 opaque pixels). The diagonal soldiers get the same upright box; for yellow, two-thirds of the collider is empty and it sticks out above and below the art. The 8x overlay also showed every soldier's legs and antennae reduced to broken dots, the nearest-neighbour loss we predicted. The agent's test checked `size == Vector2(20, 34)`, a number the same agent chose, so it could see none of this. Its `.import` checks also match raw text (`contains("compress/mode=0")`) rather than parsing the file.

**Run 2, Claude Code, Prompt 2.** 63 turns, 22 minutes; six commands refused by the permission rules (pipes into `grep`, `xxd`, `which … ||`), each retried in an allowed form. It wrote a standard-library tone script (a 900 Hz jump, a 300 Hz fail, and a 100 Hz music loop whose 176,400 samples hold exactly 400 cycles), `audio_cues.gd` as a child of `main.tscn`, and a 13-check test; music imported with `edit/loop_mode=2`, `loop_end=176399`. It reported 13/13, and answered step 5 honestly: every file under `godot/audio/`, including the script `main.tscn` now loads, is ignored by `.gitignore:23: audio/`.

Our checks found three problems behind that pass:

1. **The test broke its own rule.** The prompt said "never by setting state". The test reached the spikes with `game.player.position = Vector2(330.0, 310.0)`, paused with `game.set_paused(true)`, and built its own `AudioCues` node instead of loading `main.tscn`, so the real scene wiring was never exercised.
2. **The effects were not "disabled".** Both effect imports said `edit/loop_mode=0`, Detect from WAV. They did not loop only because the tone files carry no loop chunk. A WAV exported from an audio editor with loop markers would.
3. **A fresh clone was broken, and the tests stayed green.** We committed and cloned. In the clone, loading `main.tscn` printed `Parse Error: [ext_resource] referenced non-existent resource at: res://audio/audio_cues.gd`, and `test_audio_cues.gd` failed to parse, yet `godot` **exited 0**. The other 62 checks passed, because no original test loads `main.tscn`.

Our real-scene driver loaded `main.tscn`, held right, jumped once and walked into the spikes, never touching position or state:

```text
frame 34: player.jumps -> 1
frame 35: jump cue #1
frame 99: state -> DYING
frame 100: fail cue #1
deaths=1 jump_plays=1 fail_plays=1 music_plays=1
```

One cue per event, each one physics tick late. `AudioCues` is the first child in `main.tscn`, the player is added later by `session.gd`, and the session sets `process_physics_priority = 10`, so in every physics step the observer runs before the things it observes. At 1/60 s it is inaudible, and it is a real property of the design.

**Run 3, Codex, a revision prompt.** Claude Code had reached the account's usage limit for the day (its next run returned "You've hit your session limit"), so the revision went to Codex:

```text
Revise the previous agent run (Claude Code). Checks run outside that session found
three problems. Fix only these; do not change session.gd, player.gd, the level,
the tuning, project.godot or the three original tests.

1. godot/tests/test_audio_cues.gd breaks its own rule: it sets
   game.player.position to reach the spikes, calls game.set_paused() directly,
   and builds its own AudioCues node instead of loading res://game/main.tscn.
   Rewrite it to instantiate res://game/main.tscn and to drive play only through
   the player's test inputs (test_control, test_axis, test_jump_pressed,
   test_jump_held) and Input.action_press / action_release for "pause". No writes
   to position, velocity or game state. Keep every existing check, and add one
   that prints the physics frame of each jump and death and of its cue.
2. jump.wav and fail.wav are imported with edit/loop_mode=0 (Detect from WAV),
   not Disabled. Set them to Disabled, reimport, and make the test read all three
   .import files with ConfigFile and check the loop numbers there.
3. .gitignore ignores godot/audio/ (the "audio/" and "*.wav" rules), so a fresh
   clone cannot load main.tscn. My decision: track everything under godot/audio/.
   Add the narrowest rules that do that, and prove it with git check-ignore -v.
Run godot --headless --path godot --import, then the new test and the other four
tests, each with --fixed-fps 60, and report the real output. Do not commit.
```

```bash
codex exec --sandbox workspace-write --json "$(cat PROMPT-3.txt)" < /dev/null > session-3-codex.jsonl
```

It took four and a half minutes. Its first two test runs failed and it reported both: the cues arrived a frame after their events, and walking right alone stopped at the raised step. Its final test loads `main.tscn`, drives Clawd with test inputs and a real `pause` input event, reads the three `.import` files with `ConfigFile`, and prints `FRAME jump 1: physics=6` beside `FRAME jump cue 1: physics=7`. It set the effects to `edit/loop_mode=1` and added `!godot/audio/` and `!godot/audio/**` after `audio/` in `.gitignore`. Inside the sandbox, Godot printed `ERROR: Cannot save file '…/Library/Application Support/Godot/editor_settings-4.7.tres'` and could not open its `user://logs` files; the commands still succeeded.

We verified: 17/17 audio checks, 28/28, 25/25, 9/9, 1,950/0. `git check-ignore -v --no-index` names the new `!godot/audio/**` rule for the script, the WAVs and their `.import` files. A new fresh clone imports cleanly, loads `main.tscn` with no errors and passes every test. One judgment to notice: Codex's timing check *requires* each cue to arrive exactly one frame after its event. It pins the observer latency as expected behaviour; if you fix the ordering later, change that check on purpose.

**Not verified by anyone.** Whether the termite reads at game size, which collider is fair for which soldier, whether a top-down creature belongs in a side-view level, and how any of it sounds. The lab scene and overlay exist for the first two. Your ears are the only instrument for the last.

## Check your understanding (ungraded)

1. Open `termite_soldiers.png.import`. If this were a 1920 x 1080 painted background that the camera zooms out from, which two lines would you change, and to what?
2. In `cut_termites.py`, replace `Image.NEAREST` with `Image.BOX`, then rerun the script, the import and `verify_collider_vs_alpha.py`. What happens to the legs? Is it still pixel art?
3. The strip has three animations of one frame each. From the Assignment 2 pose menu, list the frames you would generate next for a walking enemy, and how many cells the strip then needs.
4. Give each soldier its own collider. Where should that data live so that switching the animation cannot leave the wrong box behind? Write the check that would have caught the yellow soldier's empty box.
5. Make `AudioCues` observe *after* the session in each physics step. Which property decides the order? Which of Codex's checks fails, and what should it say instead?
6. Why did `godot` exit 0 when `test_audio_cues.gd` could not be parsed? What would you add to a CI script so that case fails?

---

## Doing the same thing in Unity

### Similarities

The shape of the task is the same. A source image goes through an importer whose settings live in a sidecar file; a sprite asset is cut from the texture; an animation plays the frames; a collider separate from the art decides contact. So is the judgment: a frame-count test cannot tell a pose from a different creature, and no batch test says whether a player can read the sprite.

Unity's sidecar is the `.meta` file, created "for each folder and file in the `Assets` folder", holding "the unique ID assigned to the asset, and values for all the asset's import settings" ([Asset metadata](https://docs.unity3d.com/Manual/AssetMetadata.html)). With Asset Serialization Mode at Force Text, which the manual gives as the default ([Editor settings](https://docs.unity3d.com/Manual/class-EditorManager.html)), `.meta` files, scenes and prefabs are YAML an agent can read and diff. Losing a `.meta` file breaks every reference to the asset, as losing a Godot `.import` file's `uid` does.

### Differences

- **Where the filter lives.** Unity keeps **Filter Mode** (Point, Bilinear, Trilinear) on the texture importer, beside **sRGB (Color Texture)**, **Generate Mipmap**, **Alpha is Transparency** and **Pixels Per Unit** ([Sprite texture settings](https://docs.unity3d.com/Manual/texture-type-sprite.html)). Godot 4 moved the filter to the node. "Fix the import" does nothing for a blurry sprite in Godot.
- **Slicing.** Unity sets **Sprite Mode: Multiple** and cuts the sheet in the Sprite Editor; the slices are recorded in the texture's `.meta`. Godot keeps the cut in a `SpriteFrames` or `AtlasTexture` resource and leaves the texture's import alone.
- **Collider from art.** Unity can generate a physics outline from the sprite's alpha (**Generate Physics Outline**, and the Sprite Editor's Custom Physics Shape, used by a `PolygonCollider2D`). That is convenient and it is this chapter's trap: an alpha outline includes the legs. You would still set a `BoxCollider2D` for the body by hand.
- **Audio looping.** A Unity AudioClip's import settings cover Load Type, Compression Format (PCM, ADPCM, Vorbis/MP3), quality and sample rate ([Audio Clip](https://docs.unity3d.com/Manual/class-AudioClip.html)); looping is a property of the playing component, `AudioSource.loop` ([AudioSource.loop](https://docs.unity3d.com/ScriptReference/AudioSource-loop.html)). Godot puts loop points, in samples, in the import.
- **Headless verification.** An agent would enforce import settings from an `AssetPostprocessor`, or check them in an Edit Mode test through `TextureImporter` (`filterMode`, `mipmapEnabled`, `sRGBTexture`, `textureCompression`, `spriteImportMode`, `spritePixelsPerUnit`; [TextureImporter](https://docs.unity3d.com/ScriptReference/TextureImporter.html)), then run `-runTests -batchmode -projectPath <path> -testPlatform EditMode -testResults <file>` ([Test Framework command line](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html)).

| Godot 4.7 | Unity 6 |
|---|---|
| `.import` file (ConfigFile text) | `.meta` file (YAML under Force Text) |
| `compress/mode=0` (Lossless) | Compression: None |
| `CanvasItem.texture_filter` = Nearest, on the node | Filter Mode: Point, on the importer |
| `SpriteFrames` + `AtlasTexture` regions | Sprite Mode: Multiple + Sprite Editor slices |
| `AnimatedSprite2D` | `SpriteRenderer` + Animator / Animation Clip |
| `CollisionShape2D` + `RectangleShape2D` | `BoxCollider2D` |
| WAV `edit/loop_mode`, `loop_begin`, `loop_end` | `AudioSource.loop` (no clip loop points) |
| `AudioStreamPlayer` | `AudioSource` |
| `godot --headless --script res://tests/…` | `Unity -batchmode -runTests …` |

## Doing the same thing in Unreal Engine

### Similarities

Unreal also separates the imported asset from what draws it, and what draws it from its collision. Its 2D system, **Paper 2D**, turns a texture into **Sprites** and plays sprites in sequence as a **Flipbook** ([Paper 2D overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-overview-in-unreal-engine)). Sprite extraction offers an **Auto** mode that "groups pixels separated by transparency" and a **Grid** mode with cell sizes and spacing, the two strategies this chapter compared ([Paper 2D sprites](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-import-and-use-paper-2d-sprites-in-unreal-engine)). A sprite's collision has a **Sprite Collision Domain** (None, 2D or 3D physics) and geometry types including **Tight Bounding Box**, which "excludes any fully transparent areas", **Shrink Wrapped**, and **Fully Custom** ([Paper 2D sprite collision](https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-sprite-collision-in-unreal-engine)). The alpha-based types carry the same trap as Unity's outline; Fully Custom is the body-only box.

### Differences

- **Pixel-art settings are a menu action on the texture.** Unreal's documented shortcut "removes Mipmaps, sets the Filter to Nearest, and uses the Editor Icon as the Compression Setting" ([Paper 2D sprites](https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-import-and-use-paper-2d-sprites-in-unreal-engine)), and the texture groups include `TEXTUREGROUP_Pixels2D` for point-filtered pixels ([Texture format support](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-format-support-and-settings-in-unreal-engine)). As in Unity, the filter belongs to the texture asset.
- **Binary assets.** Textures, sprites and flipbooks are `.uasset` files, which an agent cannot read or diff as it reads a Godot `.tres` or `.import`. Agents work through editor Python instead, including headless through the commandlet `UnrealEditor-Cmd.exe <project>.uproject -run=pythonscript -script=<file>`; "the Python environment is only available in the Unreal Editor", not in a running game ([Scripting the editor using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python)).
- **Audio.** Unreal imports `.wav, .ogg, .flac, .aif, .opus, .mp3`, converts everything to 16-bit WAV internally, and recommends 16-bit sources because 24-bit files are not dithered ([Importing audio files](https://dev.epicgames.com/documentation/unreal-engine/importing-audio-files?lang=en-US)). Looping is a flag on the Sound Wave: "If set, when played directly (not through a sound cue) the wave will be played looping" ([unreal.SoundWave](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/SoundWave)). Event logic grows into Sound Cues or MetaSounds, also binary assets.
- **Headless verification.** Automation tests run from the command line with `-ExecCmds="Automation RunTest <name>;Quit"`, with `-ReportExportPath` for JSON results ([Run automation tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine)).

| Godot 4.7 | Unreal Engine 5 |
|---|---|
| `.import` + `.godot/imported/` cache | `.uasset`, binary, holding imported data and settings |
| `texture_filter` = Nearest on the node | Filter Nearest / `TEXTUREGROUP_Pixels2D` on the texture |
| `SpriteFrames` animation | Paper 2D Flipbook |
| `AtlasTexture` region | Paper 2D Sprite extracted from a texture |
| `CollisionShape2D` | Sprite collision (Collision Domain, Fully Custom) |
| WAV import loop points | Sound Wave `Looping` flag; Sound Cue or MetaSound for logic |
| `godot --headless --script` | `UnrealEditor-Cmd … -ExecCmds="Automation RunTest …"` |

Unreal Engine is source-available under its EULA, not open source: the source repository on GitHub requires linking an Epic account and accepting the Unreal Engine EULA ([Downloading source code](https://dev.epicgames.com/documentation/unreal-engine/downloading-source-code-in-unreal-engine?lang=en-US)).

## Sources

Unity and Unreal were not run for this chapter; the comparisons come from their official documentation, checked on 27 September 2026 (the Unity manual pages served were for Unity 6.6, the Unreal pages for UE 5.8).

**Godot (documentation, stable branch, and the 4.7.2 binary)**
- Import process: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/import_process.html
- Importing images: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
- ResourceImporterTexture: https://docs.godotengine.org/en/stable/classes/class_resourceimportertexture.html
- Importing audio samples: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
- 2D sprite animation: https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html
- CanvasItem (`texture_filter`): https://docs.godotengine.org/en/stable/classes/class_canvasitem.html
- AudioStreamPlayer: https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html
- Shading language (`source_color`): https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
- Probed directly in Godot 4.7.2 (scripts in `examples/02-prompting-game-art/scripts/probe/`): default texture and audio import parameters, `default_texture_filter` = Linear, the WAV importer-to-resource loop-mode mapping, `SpriteFrames` defaults.

**Walker and course files**
- `walker/asset-gen/SKILL.md`, `walker/asset-gen/rembg.md`, `walker/asset-gen/tools/{grid_slice,find_loop_frame,rembg_matting}.py`
- `walker-jumpman-clawd` at `382f2ba`: `README.md`, `CLAWD-STATUS.json`, `ASSET-PLAN.md`, `godot/features/player/{player,clawd_art}.gd`, `godot/game/session.gd`, `.gitignore`; https://github.com/nikbearbrown/walker-jumpman-clawd
- `walker-jumpman` `.gitignore`: https://github.com/nikbearbrown/walker-jumpman
- `walker-audio-generator/godot/generator_demo.gd`, `walker-audio-generator/FRICTIONAL.md`
- `assignments/02-generate-art-sound-music-for-your-game.md`; `fall-2026/nik-bear-brown/assignment-2/FRICTIONAL.md` and `reference/`
- Old course: Canvas export pages "Mini-Assignment 1: Generative AI for Game Art", "Mini-Assignment 3: Generative AI for Game Audio", "Animation Assets", and the old syllabus's weekly GenAI tool list

**Rights and models**
- U.S. Copyright Office, *Copyright and Artificial Intelligence, Part 2: Copyrightability* (January 2025): https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf ; summary in NewsNet 1060: https://www.copyright.gov/newsnet/2025/1060.html
- AudioCraft license statement (code MIT, weights CC-BY-NC 4.0): https://github.com/facebookresearch/audiocraft
- `rembg` BiRefNet model URL and size: `rembg/sessions/birefnet_general.py` in the installed `rembg` 2.0.77; HTTP headers of the release file

**Coding CLIs**
- `claude --help` (2.1.150); Claude Code memory settings (`autoMemoryEnabled`): https://code.claude.com/docs/en/memory
- `codex exec --help` (0.153.4)

**Unity (documentation only)**
- Asset metadata: https://docs.unity3d.com/Manual/AssetMetadata.html
- Editor settings, Asset Serialization Mode: https://docs.unity3d.com/Manual/class-EditorManager.html
- Sprite (2D and UI) texture settings: https://docs.unity3d.com/Manual/texture-type-sprite.html
- TextureImporter: https://docs.unity3d.com/ScriptReference/TextureImporter.html
- Audio Clip import settings: https://docs.unity3d.com/Manual/class-AudioClip.html
- AudioSource.loop: https://docs.unity3d.com/ScriptReference/AudioSource-loop.html
- Test Framework command line: https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html

**Unreal Engine (documentation only)**
- Paper 2D overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-overview-in-unreal-engine
- Importing and using Paper 2D sprites: https://dev.epicgames.com/documentation/en-us/unreal-engine/how-to-import-and-use-paper-2d-sprites-in-unreal-engine
- Paper 2D sprite collision: https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-sprite-collision-in-unreal-engine
- Texture format support and settings: https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-format-support-and-settings-in-unreal-engine
- Importing audio files: https://dev.epicgames.com/documentation/unreal-engine/importing-audio-files?lang=en-US
- unreal.SoundWave: https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/SoundWave
- Scripting the editor using Python: https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python
- Run automation tests: https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine
- Downloading source code: https://dev.epicgames.com/documentation/unreal-engine/downloading-source-code-in-unreal-engine?lang=en-US
