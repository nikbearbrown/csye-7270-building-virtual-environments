# walker-2d-finite-state-machine: capture notes

**What this is.** A real windowed Godot 4.7.2 Movie Maker run of the Hierarchical Finite State Machine demo, recorded 2026-10-09 at a fixed 30 fps from a scratch copy. The source at `/Users/bear/Documents/CoWork/bear-textbooks/books/walker-2d-finite-state-machine/godot` was not touched. The copy got only the capture autoload and a 1920x1080 window.

Three things are drawn on screen:
- The player's current state, as a label above the green body.
- The "STATESTACK" panel at top left: the pushdown stack.
- The controls panel at top right.

## Scripted input (InputEventAction, frames at 30 fps)
| Frames | Input |
|---|---|
| f30–42 | move_right (walk) |
| f50–60 | run + move_right (sprint) |
| f70–90 | move_left |
| f95–105 | move_up |
| f110–120 | move_down |
| f130 | jump |
| f170, f177, f185 | attack, three taps (combo) |
| f225, f235, f245 | fire, three taps |
| f265–280 | run + move_left |
| f295 | simulate_damage (X) |

## Files (all 1920x1080)
| File | What is on screen |
|---|---|
| `01-idle-state.png` | IDLE label; STATESTACK "0 Idle". |
| `02-move-state.png` | MOVE label; stack "0 Move"; the player has moved right. |
| `03-run-sprint.png` | MOVE label (sprint is part of the Move state); the player further right. |
| `04-jump-state-stack.png` | The player raised above its shadow; stack "0 Jump / 1 Idle". This is the pushdown: Jump is pushed on top of Idle. |
| `05-attack-combo.png` | ATTACK label with the sword mid-swing; stack "0 Attack / 1 Idle". |
| `06-firing-bullets.png` | IDLE label; a bullet (white dot) leaving the player. |
| `07-stagger-after-simulated-damage.png` | STAGGER label, the player tinted orange; stack "0 Stagger / 1 Idle". |
| `walker-2d-finite-state-machine-clip.mp4` | 8.0 s, H.264, 30 fps, no audio. Movie frames 25–265: walk, sprint, move left/up/down, jump, three-hit sword combo, three bullets. The state label and STATESTACK update live. |

**Problems:**
- A first attempt held move_right plus run for 2.7 s, and the player left the screen; the demo has no walls. Moves were shortened to keep the player in view. That take was discarded.
- The demo's "Explanations" text is not visible in these frames.
- Only 113 of 340 movie frames are distinct, because the idle stretches are truly static.
