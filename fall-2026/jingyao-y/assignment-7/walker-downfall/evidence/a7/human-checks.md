# A7 human checks — running record

Written by the agent from the user's own words. The observer for every entry
is the user (the student). Claude's own readings are labelled as claims and
kept apart. TEST-REPORT.md cites this file.

## 2026-11-22 — npc_idle, side-by-side preview (before wiring)

- **What was shown:** `res://previews/npc_idle_side_by_side.tscn`, run
  windowed at the project's window size: the base store with today's
  可露希尔 (AnimatedSprite3D from `FieldArt.npc_idle`) on the left and the new
  `animations/npc_idle.tscn` clip on the right, started one cell ahead. This
  is a fixture; the clip is not wired into the game yet.
- **Asked:** whether the two breathe at the same rate, whether the right one
  stutters, repeats a frame or jumps at the wrap over five or more wraps, and
  whether the figure drifts in its cell.
- **User's observation (verbatim):** "same"
- **Claude's reading of the fixture strip (a claim, not a check):** same
  scale, position and pixels; cells change every 10 capture frames at 30 fps.
  Strip: scratchpad capture, not committed (the committed cycle strip comes
  from the student's Movie Maker run of the brief's preview).
- **What this does not cover:** the seam and registration checks in the
  running game after wiring (Step 5), and the background check.

## 2026-11-22 — npc_idle wired into the game (plan step 1)

- **What was shown:** `res://previews/npc_idle_in_game.tscn`, windowed at the
  project's window size: the real game with `FieldArt.npc_idle` now
  instancing `animations/npc_idle.tscn`. About 12 s at the base store
  (可露希尔, dark metal floor), then the seed-1729 Chernobog mine floor next to
  the 罗德岛小队 set piece (three figures, dark rock ground).
- **Asked:** same breathing as before (rate, feet, scale, crispness); no
  stutter, repeated frame or jump at the wrap over 5+ wraps; the three squad
  figures out of step; no drift in the cell; readable on both grounds.
- **User's observation (verbatim):** "All fine"
- **Headless support (agent, measured):** the three squad figures sat at
  clip positions 0.88 / 1.22 / 0.22 s (cells 2 / 3 / 0) on that floor
  (scratch probe, not committed); pins N1–N3 unchanged after wiring.
- **Still to do:** the lightest ground an NPC appears on (snow camp) for the
  "against the background" check, unless the user counts this one.
