# TUNING.md — Assignment 7: wave_release feel

The Assignment 6 tuning record (hit_spark, fire_pit_flames) is at tag `a6`.
This file replaces it. Written by the agent (Claude Code) from the user's own
words; the observer for every human entry is the user (the student). Claude's
readings of a strip are labelled as claims and kept apart from the user's
verdicts. Frames in `captures/` are **fixture captures** from
`res://previews/wave_release_preview.tscn` (CHANGE-BRIEF.md r6).

## r0 — the phase table as built (6 / 4 / 10 at 30 fps, rate 1)

- **Code:** commit e51a4563 (state machine f965840e, rig 1722fbbd, RESET at
  build 45cf5845).
- **Capture (run by the user):** `captures/wave_release/r0/frame*.png`,
  241 frames, `--fixed-fps 30 --quit-after 240`, written 2026-11-22 12:12.
- **The user's look in the running game (before Claude read the strip):**
  the user ran the preview windowed at the project's window size, at normal
  speed and at `--time-scale 0.25`.
  - **Observation and decision (verbatim, human-provided, observer: the
    user):** "I saw the record. everything is nice, we did a good job."
  - **Decision:** keep r0 as it is.
- **Log note (agent):** the user's later windowed runs overwrote
  `logs/wave_release_preview.log` (its header now reads ACTIVE 143, the
  `--time-scale 0.25` run), so the per-frame log that matches the r0 frames
  was lost. The preview now writes one log per run (see FRICTIONAL.md).
- **Claude's reading of the r0 strip (a claim, not a check; read after the
  user's verdict above was recorded):**
  - Boundaries, read from the frames (charge mark, sprite/rig swap, the wave):
    click at capture 27; rig replaces the sprite at **29** (STARTUP, of which
    the first 2 frames are the click's hitstop); the yellow charge mark is
    gone at **37** (ACTIVE: the wave leaves; its crescent and the 215 hit on
    the enemy show by 40); recovery from **41**; the sprite is back and the
    next swing starts at **50** (READY). These match the agent's earlier
    smoke run header exactly (29 / 37 / 41 / 50), so the capture is
    deterministic, and the phase table holds: 6 + 2 hitstop / 4 / 9–10 frames.
  - **Possible issue 1 — the hit lands at the start of the wind-up.** The
    click's melee hit (the white "129", the large slash arc and the impact
    flash on the enemy) all show at capture 29, the first startup frame, as
    brief r3 (4) keeps them on the click. The biggest flash of the action
    therefore comes before the wind-up, and the wave leaves 8 frames later
    with a smaller purple crescent. Claude's reading: the startup may read as
    "already hit", not as a wind-up.
  - **Possible issue 2 — facing.** The enemy stands to her screen-right in
    this capture (not west as the preview intended), and the rig's pose seems
    to face screen-left (face and the leading blade on the left) through
    29–49; the next ordinary swing at 50 looks similar, so this may be how the
    sheet's facing reads rather than a mirror bug. Uncertain at this scale.
  - Not seen in the strip: no blank or stale frame at the swaps (29, 50); the
    feet stay on the same line.
- **The user's decision after Claude's reading (verbatim):** "Keep r0, no
  revision". The user did not take up either possible issue. r0 is the
  kept phase table (6 / 4 / 10 at 30 fps). The rubric item "at least one
  observation-driven revision with a prediction, two strips and the user's
  verdict" is therefore **not met**, and is recorded as not met rather than
  filled with an invented revision.
- **Committed fixture frames (labelled fixture captures):** capture 27
  (click), 29 (first STARTUP), 36 (last STARTUP, f5), 37 (first ACTIVE, f6,
  the wave leaves), 40 (last ACTIVE, f9), 41 (first RECOVERY, f10), 49 (last
  RECOVERY), 50 (READY, sprite back). The rest of the sequence stays local
  and untracked.
