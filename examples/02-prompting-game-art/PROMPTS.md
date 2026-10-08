# Prompts — Chapter 2 worked example

The exact prompts and command lines used on 2026-09-27. Each ran from the root of the scratch copy of `walker-jumpman-clawd` (commit `382f2ba` plus `source-art/`). The prompt text was passed with `"$(cat PROMPT-N.txt)"`.

## Run 1 — Claude Code 2.1.150 (model recorded: claude-sonnet-4-6), the art

```bash
claude -p "$(cat PROMPT-1.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*)" --max-turns 60 --output-format stream-json --verbose > session-1.jsonl
```

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

## Run 2 — Claude Code 2.1.150 (claude-sonnet-4-6), the sound

```bash
claude -p "$(cat PROMPT-2.txt)" --permission-mode acceptEdits --allowedTools "Read,Edit,Write,Glob,Grep,Bash(godot:*),Bash(git:*),Bash(ls:*),Bash(mkdir:*),Bash(python3:*)" --max-turns 60 --strict-mcp-config --settings '{"autoMemoryEnabled":false}' --output-format stream-json --verbose > session-2.jsonl
```

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

## Run 3 — Codex CLI 0.153.4 (gpt-5.6-sol, reasoning low), the revision

Claude Code had reached the account's usage limit for the day, so the revision ran in Codex.

```bash
codex exec --sandbox workspace-write --json "$(cat PROMPT-3.txt)" < /dev/null > session-3-codex.jsonl
```

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
