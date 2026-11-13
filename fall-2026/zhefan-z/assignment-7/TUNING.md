# TUNING — Assignment 7

Every revision records what I saw, Claude's reading, the change I approved, Claude's prediction, Claude's comparison and my verdict. Preview strips are fixture captures; in-game strips come from the pin scenarios (scripted input, real engine output). My observations are in my words *(translated from my Chinese)*.

## 2026-11-12 — first look at both clips, before Claude read anything

Previews at `72e8d21`, windowed, 1280×720.

- **Run cycle** (`previews/run_preview.tscn`, normal speed): the two-frame rhythm at 8 fps is right. The mage runs in place, as a preview should.
- **Wolf lunge** (`previews/lunge_preview.tscn`, `--time-scale 0.25`): the forward stretch is clear, but the wolf doesn't travel. That is expected here: the preview plays the clip only, and the 220 px/s dash comes from `wolf.gd`, so the full lunge is judged after wiring, in the game. No crack or step at the waist. The left-facing wolf moves correctly.

## 2026-11-12 — Wolf lunge and growl cancel, in the running game (wired, `33d78ae`, `72f37b8`)

What I saw (main scene, 1280×720): the stretch and the dash work together; the white flash reaches the rig; the mage's run, stop, jump and land switch clips correctly. A fireball cast during the growl only stopped the lunge when it killed the wolf; otherwise the wolf still lunged.

Claude's reading (`tests/probe_growl_cancel.gd`, real clicks): the cancel rule works, but from the distance where the wolf first sees the mage the fireball takes 20 ticks to arrive against a 31-tick growl, so only a cast in the first 12 growl ticks (0.2 s) lands in GROWL. Later casts land in LUNGE, which is committed by design; the lunges I saw stop were deaths.

My decision: keep the timings; the window is 0.2 s, recorded as a design finding.

## 2026-11-12 — Run cycle: r0, r1 (reverted), r2 (kept)

**r0, what I saw in the game:** the two-frame run looks like twitching while sliding sideways; on a closer look the problem isn't which leg is forward (the skirt hides that), it's that two pictures just swap.

**Claude's reading of `captures/run/game-r0/`** (windowed Movie Maker, `--fixed-fps 60`, `--debug-collisions`, frame n = tick n − 1): the only body movement is a 1 px hat hop between the two pictures; each pose is held 7–8 ticks while the body moves 1.83 px per tick, so the planted foot slides 13–15 px and then snaps back about 4 px at each pose change (slide, snap, slide).

**Attempts that failed:** mirroring the leg region (gives a kick, boots pointing back, a leg crossing the staff); Gemini contact B, twice (both kept the same foot forward: 103 px differ from contact A, all in the trailing leg); darkening the far leg (19 px differ; the A2 legs are already the darkest tones). Evidence: `captures/run/analysis/`, `26932e1`.

**r1:** four beats from the same two frames: discrete `Sprite2D.offset` and `scale` tracks for a 2 px sink and a 2 px lift with light squash and stretch, plus reset keys in the other eight clips. Claude's prediction: hat rows 268 / 270 / 267 / 265 across the four beats. Its comparison of `captures/run/game-r1/`: all four rows exactly as predicted, no shimmer within a held beat. **My verdict (game, 1280×720): reverted** — it still looks like the feet twitch (`fc096c9`, reverted in `338c8bf`).

**r2:** a new 4-frame run cycle drawn by Gemini in one image (prompt v3 in `design/IMAGE-PROMPTS-from-chat.md`), cleaned by `tools/clean_run_cycle.py` onto my A2 palette at the A2 size, torsos aligned to contact A, ground line kept. Claude's reading: the same character (hat 25–26 px, 13–14 A2 colours, ±4 % pixels); frame 1 is nearly contact A; frames 2–4 are new poses; frame 4 is airborne and doesn't reach for the next step; no single frame rate stops the foot sliding. Clip at 10 fps (6 ticks per frame at 60 Hz); measured per-frame ticks 6/6/6/7 on entry and 5/6/6/7 per loop after, because the clip wraps on the tick it reaches 0.4 s. **My verdict (game, 1280×720): kept — it looks much better** (`32eed66`).
