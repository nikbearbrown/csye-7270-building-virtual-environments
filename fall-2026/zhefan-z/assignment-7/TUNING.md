# TUNING — Assignment 7

Every revision records what I saw, Claude's reading, the change I approved, Claude's prediction, Claude's comparison and my verdict. Preview strips are fixture captures; in-game strips come from the pin scenarios (scripted input, real engine output). My observations are in my words *(translated from my Chinese)*.

## 2026-11-12 — first look at both clips, before Claude read anything

Previews at `72e8d21`, windowed, 1280×720.

- **Run cycle** (`previews/run_preview.tscn`, normal speed): the two-frame rhythm at 8 fps is right. The mage runs in place, as a preview should.
- **Wolf lunge** (`previews/lunge_preview.tscn`, `--time-scale 0.25`): the forward stretch is clear, but the wolf doesn't travel. That is expected here: the preview plays the clip only, and the 220 px/s dash comes from `wolf.gd`, so the full lunge is judged after wiring, in the game. No crack or step at the waist. The left-facing wolf moves correctly.
