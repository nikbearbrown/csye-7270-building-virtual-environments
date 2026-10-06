# AC-01 — Checkpoint pad (proposed feature, human-authored)

Author: written for this example on 2026-09-27 by the AI agent that drafted Chapter 5, standing in for a student. Not reviewed by Professor Bear.
Status: proposed. Not in the recovered GDD; not approved by any gate.

## The interaction

A checkpoint pad on the ground near the start. When the player walks onto it,
it becomes the player's respawn point: the reset action and falling off the
map both return the player to the pad instead of the level start.

## Acceptance criteria (each one is measurable headless)

Units are Godot 3D units (metres). "Frame" means one iteration at
`--fixed-fps 60`; this project runs 120 physics ticks per second.

1. **Placement.** The pad is an Area3D whose collision footprint is at least
   1.5 m x 1.5 m, resting on walkable floor between 3 m and 6 m (horizontal
   distance) from the player's start position. It is not on the straight path
   that `tests/input_probe.gd` walks (move_forward, frames 120-179), so that
   probe's reset check still means "reset to the level start".
2. **Before activation.** Holding `reset_position` for 5 frames leaves the
   player within 0.2 m of the level start.
3. **Activation by input.** Using only movement actions (Input.action_press /
   action_release; no writes to the player's position or velocity), the player
   reaches the pad within 600 frames. The pad reports activation exactly once:
   re-entering it does not activate it again.
4. **Reset to pad.** After activation, holding `reset_position` for 5 frames
   leaves the player within 0.2 m of the pad's respawn point.
5. **Fall to pad (constructed fixture, labelled as such).** After activation,
   setting the player's position below y = -12 results in the player being
   within 0.2 m of the respawn point within 2 frames. This check writes game
   state directly; it tests the fall branch of the same code, not a fall a
   player would make.
6. **No regressions.** `tests/input_probe.gd` still reports all four checks
   true and exits 0; `tests/feature_route.gd` still collects at least one coin
   and exits 0. Both run with `--fixed-fps 60`.

## Out of scope for this criterion (human checks)

- Whether a player can see the pad and understands what it does.
- Its look, any sound, and whether it feels fair.
- Touch, gamepad, and any exported build.
