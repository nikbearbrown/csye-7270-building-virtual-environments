# TUNING.md — Assignment 6

Every strip here is a **fixture capture**: a preview scene (`previews/`) rendered
by Godot's Movie Maker at a fixed 30 fps, not gameplay footage. The user's
runtime observations are quoted as given (translated from Chinese, with the
original in brackets). Claude's readings are claims, not checks.

## 2026-11-07 — Effect A, initial look (r0)

Strip: `captures/hit_spark/r0/` (frames 10, 12, 15, 20, 30, 50; city street,
fixed seed 7370/7371, bursts fired at frames 10 and 16). Capture log names the
GPU: NVIDIA GeForce RTX 4060 Laptop GPU, D3D12, Forward+.

User runtime observation (running preview `previews/hit_spark_preview.tscn -- --loop`,
1280×720 window, city background):
"Splashing outward." [向外迸溅] Asked to clarify, the user chose: "I can see it
splashing outward" [看得出向外迸溅], i.e. the outward throw reads as intended.

Claude's reading of r0 (4× nearest-neighbour crop of 560–720 × 300–420):
- 10: a soft white flash about 25 px across on the stand-in's torso, a few tiny
  white specks inside it. Burst appears on the trigger frame (no one-frame lag).
- 12: flash dimmer; sparks are specks bunched within ~10 px; no ring is visible.
- 15: flash gone; scattered yellow-orange specks up to ~25 px from the centre;
  the dark puff is practically invisible on the dark street.
- 20: the second burst's specks plus a faint grey haze.
- 30, 50: empty; the log shows 0 `HitSpark` nodes at frame 50.
- Claude's conclusion: timing and position match the brief; the sparks look too
  small and travel too little to read as an outward throw.

**Discrepancy:** Claude's strip reading said the outward throw does not read;
the user, watching it move in the running preview, says it does. Single still
frames at 30 fps lose the motion that makes the throw legible. The user's
verdict stands; no change is made on the strength of Claude's r0 reading.
The puff was not judged on the city street: it is meant for light ground, which
the snow check covers next.

## 2026-11-07 — Effect A, revision r1

User runtime observation (running preview `-- --loop --snow`, 1280×720, 萨米 snow):
"I can see it." [能看到] Asked specifically about the dark puff behind the
sparks: "Barely see a little." [勉强看到一点]

Claude's reading of r0-snow: flash and sparks read mainly where they overlap the
stand-in's dark body; specks that leave the body are faint on snow; the puff is
not visible. Measured 8-bit luminance of a snow patch just below the body
(x 630–650, y 378–386): 158.3 on every strip frame (10–50), so the puff never
reaches the snow. Cause, by arithmetic: Puff quad 0.5 units × scale 0.6→1.4 =
0.3→0.7 units = 9→21 px at 30 px/unit, soft radial texture, centred on a body
about 30 px wide, so almost all of it lies over the dark body.

Change: `Puff` `draw_pass_1` QuadMesh size 0.5×0.5 → 1.0×1.0 (one setting),
reviewed against the brief by the agent (the brief's intent: "a third,
alpha-blended dark layer that reads as a smudge on white"); user approval:
pending.

Claude's prediction for r1 (same seeds, same fixture, 30 fps):
- r1-snow: puff 18→42 px across, extending past the body onto the snow. The
  "below" patch darkens by at least 8 levels (≤ 150) on frames 15 and 20,
  returns to 158 ± 1 by frame 30. Frame 10 and 12 change little (puff alpha is
  0.55 at birth but it is still small and mostly over the body). Flash and
  sparks unchanged.
- r1 (city): no visible difference (dark puff on dark street); the "below"
  patch changes by ≤ 3 levels.
