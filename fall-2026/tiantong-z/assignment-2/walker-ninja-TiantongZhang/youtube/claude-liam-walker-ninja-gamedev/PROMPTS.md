# PROMPTS.md — the prompts this film shows, and their status

## B00 — the composer ask

**Status: RECONSTRUCTION.** Written to be illustrative. It is not a transcript,
there is no claim that it was ever sent, and no build receipt is shown. The
label is on screen for the whole beat and the narration says it within the
first ten seconds.

> Please use Walker to convert my game design document about a cyber-ninja in a
> torchlit dungeon — a second jump, one air dash, a sword on his back, spikes
> that pop out of the floor and enemies that patrol — into a playable Godot
> project, and then help me replace the code-drawn character with generated art
> without letting the blade and its hitbox come apart.

## B13 — Your Turn

**Status: USABLE.** This one is meant to be run, and it is bounded: one pose,
one prediction, one look.

> In walker-ninja, generate the ninth pose — attack recovery — from
> CHAR-REF-01, run it through `scripts/import_pose.py`, and wire `'recovery'`
> into `pose_key()` for `attack_phase() == 3`. Tell me whether you can see it
> before you change its length.

The prediction is the point: recovery is 3 ticks, 50 ms. The check
`pose-key-matches-the-state-it-claims` will pass whether or not the frame is
visible, so the instruction is to **look at the contact sheet**. That is the
film's lesson restated as homework.

## The prompts that made the assets

Not shown on screen — they belong to the asset log, not the film — but they are
one click away and recorded verbatim as the tools recorded them, not as they
were meant:

- the music prompt and all eight generations: `../../ASSET-LOG.md` → Music
- `CHAR-REF-01` and the eight poses: `../../ASSET-LOG.md` → Art
- the four Civitai failures, with the screenshots: `../../design/rejected/`
- everything still to be generated: `../../PROMPTS.md`
