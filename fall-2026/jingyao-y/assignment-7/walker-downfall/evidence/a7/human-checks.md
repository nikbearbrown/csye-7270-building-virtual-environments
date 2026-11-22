# A7 human checks — running record

Written by the agent from the user's own words. The observer for every entry
is the user (the student). Claude's own readings are labelled as claims and
kept apart. TEST-REPORT.md cites this file.

## 2026-11-22 — npc_idle, side-by-side preview (before wiring)

- **What was shown:** `res://previews/npc_idle_side_by_side.tscn`, run
  windowed at the project's window size: the base store with today's
  Closure (AnimatedSprite3D from `FieldArt.npc_idle`) on the left and the new
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
  (Closure, dark metal floor), then the seed-1729 Chernobog mine floor next to
  the Rhodes Island squad set piece (three figures, dark rock ground).
- **Asked:** same breathing as before (rate, feet, scale, crispness); no
  stutter, repeated frame or jump at the wrap over 5+ wraps; the three squad
  figures out of step; no drift in the cell; readable on both grounds.
- **User's observation (verbatim):** "All fine"
- **Headless support (agent, measured):** the three squad figures sat at
  clip positions 0.88 / 1.22 / 0.22 s (cells 2 / 3 / 0) on that floor
  (scratch probe, not committed); pins N1–N3 unchanged after wiring.
- **Still to do:** the lightest ground an NPC appears on (snow camp) for the
  "against the background" check, unless the user counts this one.

## 2026-11-22 — wave_release wired (plan step 3), first play

- **What was shown:** `res://previews/wave_release_play.tscn`, windowed: the
  real game on the seed-1729 Chernobog mine floor, field cleared, Lappland
  with two still, very-high-health dummies left and right of her. Every 4th
  swing is a release; Space dodges. Code at commit f965840e (phase table
  6/4/10 at 30 fps, rate 1).
- **Asked:** whether startup, active and recovery read as distinct; whether
  the wave leaves on the downward sweep; any foot pop, flash or blank frame
  at the sprite↔rig swaps; mirroring on both sides; whether 6/4/10 feels
  too fast, too slow or right; a dodge tried in each phase.
- **User's verdict (verbatim):** "Reads well"
- **Not stated by the user, so not recorded as checked:** which phases were
  dodged in, the mirror on each side, the swap artefacts. The rubric's
  "action in play, interrupt in each phase" human check stays open until the
  user confirms those, after the edge tests.

## 2026-11-22 — remaining human checks (the user's report, translated)

The user wrote these in Chinese; the agent translated them into English at
the user's request (all documents in English). Observer: the user.

- **Against the background (both clips over the darkest and lightest ground
  they appear on):** "The light/dark contrast is clear; pass."
- **The action in play, an interrupt in each phase:** "I tried interrupting
  it during all combat states, during item searching, and while standing
  still; pass."
- **Provenance:** the image model is "gpt sol 6.1"; the user asked to record
  only that ("mark just this, nothing else needed").
