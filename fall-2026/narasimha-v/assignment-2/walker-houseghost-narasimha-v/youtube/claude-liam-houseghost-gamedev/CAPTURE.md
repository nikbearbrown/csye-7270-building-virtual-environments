# Capture record — HOUSEGHOST Night 1 slice

| | |
|---|---|
| Engine | Godot 4.7.2.stable.official.ed1daf0bf |
| Method | `scripted-input` — Godot Movie Maker, offline render |
| Command | `Godot --path <copy> --script capture_driver.gd --write-movie run-01.avi --fixed-fps 60 --quit-after 2100` |
| Rendered | 3840×2160, 60 fps, MJPEG + PCM 48 kHz stereo |
| Delivered | `capture/run-01.mp4` — H.264 CRF 18, AAC 192 kbps |
| Duration | 32.63 s, 1958 ticks (exactly 60 fps × 32.63 s) |
| Capture SHA-256 | `96fe1625d3de59ca32e821a6e72dfc4e4c81c3b5afa444abb31581a1496c2fdf` |
| Source snapshot (build_id) | `b7b0e7967fe3ba968ffa2ac864975600ecced69fcdea68c985f67bcbfc6ab49b` |
| Hash method | SHA-256 over the sorted SHA-256 list of every scene, script, sprite, effect and music file plus `project.godot` |

## How the run was driven

An isolated copy of the project, with its import cache rebuilt from scratch. The
driver instantiates the real main scene and sends real `InputEventKey` events. It
never teleports the player, never seeds meters, and never calls a game function to
force an outcome. Every step waits on a condition the game itself reports, and the
run **fails** rather than passes if the clock runs out — exhausting `--quit-after`
is not success.

Two things the driver had to learn, both measured from the project rather than
guessed:

- **The flip is event-driven.** `world.gd` handles it in `_unhandled_input`, so a
  synthesized action never reaches it; `Input.action_press` only sets the polled
  state. Every input here is a real key event.
- **A jump released in the same frame is not a jump.** `JUMP_CUT` takes 45 % of the
  rise, so a press-and-release inside one frame produces the shortest hop in the
  game. The floor gaps are 170 px wide and a full jump carries 275 px; a cut one
  does not clear them. The driver holds the key for 0.30 s.

## Resolution

The game's logical canvas is 1920×1080 with `canvas_items` stretch. The capture
window is overridden to 3840×2160, so the framing is identical and the render is
native 4K at an exact 2× scale — not a 1080p recording enlarged into a 4K container.
The display on this machine is 2560×1664; Godot rendered offscreen above it.

## Audio

Captured from the engine, not dubbed. Measured from the delivered file: continuous
programme between −17 and −23 dBFS, with the music ducking to −23.0 dB at the flip
(11 s) and the deliberate post-contact hush at 17–19 s. Both music loops and the
event sounds are present in the mix as the game played them.

## What the run plays

Opening read at 7.33 s · gap jumped at 8.92 s · flip at 11.80 s · the music box
answers at 13.03 s (recognition 1, calendar 7→5) · upright again at 16.08 s ·
**stopped at 19.38 s by his own shelf**, which is solid only in the remembered
room · flips past it along the ceiling · his shoes answer at 23.05 s
(recognition 2, calendar 4) · walks into a gap on purpose at 29.10 s, spending a
night to show what the floor costs · set down again, and walks away from it.

Two relics, both worlds, five of the nine sounds, and a real failure. Nothing is
staged: every outcome is the game's own response to a key.

## Known honesty note

This is a scripted-input capture and is labelled as such on screen wherever it
appears. It is not a recording of a person playing. The human playthrough is a
separate, unrecorded session reported in `TEST-REPORT.md`.
