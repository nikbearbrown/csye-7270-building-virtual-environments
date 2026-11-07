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
