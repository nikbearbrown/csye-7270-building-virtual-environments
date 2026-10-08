# Capture record — HOUSEGHOST Night 1 slice

| | |
|---|---|
| Engine | Godot 4.7.2.stable.official.ed1daf0bf |
| Method | `scripted-input` — Godot Movie Maker, offline render |
| Command | `Godot --path <copy> --script capture_driver.gd --write-movie run-01.avi --fixed-fps 60 --quit-after 2100` |
| Rendered | 3840×2160, 60 fps, MJPEG + PCM 48 kHz stereo |
| Delivered | `capture/run-01.mp4` — H.264 CRF 18, AAC 192 kbps |
| Duration | 19.97 s, 1198 ticks (exactly 60 fps × 19.97 s) |
| Capture SHA-256 | `ef7840f41a1aecb14063d2b0e384c57a5a945a3551994999e6837323d28b4a85` |
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

## Known honesty note

This is a scripted-input capture and is labelled as such on screen wherever it
appears. It is not a recording of a person playing. The human playthrough is a
separate, unrecorded session reported in `TEST-REPORT.md`.
