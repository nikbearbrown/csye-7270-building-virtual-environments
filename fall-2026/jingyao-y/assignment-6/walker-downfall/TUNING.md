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
**declined** — "Don't change." [不改] (2026-11-07). Nothing was edited; no r1
strips were captured. The prediction below is kept as written.
**Later the same day the user approved it:** "Change effect A's puff."
[把effect A的烟团改了] The change and the prediction are exactly those recorded
here before the decline (commit `cc9ebfaf`); results below.

Claude's prediction for r1 (same seeds, same fixture, 30 fps):
- r1-snow: puff 18→42 px across, extending past the body onto the snow. The
  "below" patch darkens by at least 8 levels (≤ 150) on frames 15 and 20,
  returns to 158 ± 1 by frame 30. Frame 10 and 12 change little (puff alpha is
  0.55 at birth but it is still small and mostly over the body). Flash and
  sparks unchanged.
- r1 (city): no visible difference (dark puff on dark street); the "below"
  patch changes by ≤ 3 levels.

(Superseded by the later approval above.)

## 2026-11-07 — Effect B, revision r1

User runtime observation (running preview `previews/fire_pit_flames_preview.tscn -- --loop`,
1280×720, 萨米 snow, real `snow_fire_pit.glb` model under the effect):
"Blocked by the stones, can't see it." [被石头挡上了看不到]

Claude's reading of r0 (`captures/fire_pit_flames/r0/`, 4× crop of 580–700 × 290–410):
lit and full on frame 11 (preprocess works; frame 10 is the one-frame GPU lag
the brief allowed); 12–54 a small orange tuft ~8–10 px tall on the logs; 70
and 99 visibly thinner with no gap or pop after the ratio change at 55; 105 a
few dying specks; 130, 175 empty. Embers (0.05-unit quads, ~1.5 px) not
visible. A faint warm ground glow is visible on the snow while lit.
Measured warm pixels (r − b > 40 and r ≥ unlit frame + 20) in the crop:
10: 0 · 12: 61 · 40: 53 · 54: 63 · 70: 24 · 99: 4 · 105: 14 · 130: 0 · 175: 0;
topmost warm pixel at y ≈ 344–347.
Cause: the pit model is 1.14 units tall and 1.5 wide (mesh AABB); flames are
emitted at local y 0.2 ± 0.18, among the logs and stones, so with normal depth
testing most of each flame quad is behind the model.

Change: `Flames` `position` (local y) 0.2 → 0.5 (one setting), reviewed
against the brief by the agent (intent: "flames lick up 0.6–0.9 units" above
the pit; nothing else changes); user approval: not asked to a decision —
**withdrawn by the agent** after the user's clarification below. Nothing was
edited.

Claude's prediction for r1 (same seed 7370, same fixture, 30 fps):
- Frames 12, 40, 54: warm pixels at least 1.5× r0 (≥ 90 each), topmost warm
  pixel at least 4 px higher (y ≤ 341). Same colours.
- Frames 70, 99: still thinner than 54 (ratio 0.44), but more visible than r0
  (frame 70 ≥ 35 warm px).
- Frames 10, 130, 175: unchanged (0 warm px). Frame 105: dying specks, ≥ r0.
- Embers unchanged (still not visible at this size).

**Clarification and withdrawal (same day).** The user sent a screenshot
(`evidence/a6/user/fire_pit_preview_occluded_by_boulders.png`) and said:
"It's covered by the rocks in the scene." [是被场景里的石头挡上了] The pit
was hidden under a cluster of the level's free-standing boulders, not by its
own stone ring, so Claude's diagnosis (emitter too low inside the pit model)
was wrong and the proposal was withdrawn.

Two fixture faults explained it:
1. The preview set only `fixed_map_seed`; the fire count and places still
   changed run to run (3 or 4 pits, different positions), so the user's
   window and strip r0 showed different pits. Both previews now also call
   `game.seed_rng(map_seed)`; two rounds over every pit index gave identical
   positions.
2. With that, seed 2026 gives 3 pits: 0 has the player standing on it,
   2 sits in a crowd, 1 is in open snow. The fixture now uses pit 1
   (`pit_index`, overridable with `-- --pit=N`).

Fixture change only; no effect setting changed. The level bug itself
(decorative boulders have no collider and can cover fires and other objects)
is outside A6's boundary; the user asked for it to be fixed after A6.

New baseline strip `captures/fire_pit_flames/r0b/` (pit 1, open snow), warm
pixels in the 580–700 × 290–410 crop: 10: 0 · 12: 72 · 40: 58 · 54: 76 ·
70: 36 · 99: 2 · 105: 7 · 130: 0 · 175: 0; top at y ≈ 346–349. Claude's
reading: a small orange tuft (~10 px) in the middle of the stone ring from
frame 12; thinner at 70; gone by 130; embers not visible; faint pink ground
glow while lit.

User runtime observation of r0b: see revision r2.

## 2026-11-07 — Effect B, revision r2

User runtime observation (running preview `-- --loop`, 1280×720, 萨米 snow,
open-snow pit 1): "Looks smothered in the wood; the fire should be bigger."
[像是闷在木头里，火应该更大]

Claude's reading of r0b: agrees. The tuft is ~10 px across and sits inside the
log pile; each flame quad is 0.30 units (9 px) and scale 0.6→1.0→0.2, so most
flames are 5–9 px and their upper half barely clears the logs.

Change: `Flames` `draw_pass_1` QuadMesh size 0.30×0.30 → 0.55×0.55 (one
setting), reviewed against the brief by the agent (intent: flames 0.6–0.9
units tall, about half an operator); user approval: **"Approved, change it."**
[批准，改吧] (2026-11-07). Edited `effects/fire_pit_flames.tscn` (QuadMesh_flames
size) and the config test's expected value; `test_fire_pit_flames_config.gd`
at 60 fps: 123 checks, 0 failed.

Claude's prediction for r1 (`captures/fire_pit_flames/r1/`, same seed and
fixture, 30 fps; crop 580–700 × 290–410, warm px as in r0b):
- Frames 12, 40, 54: at least 2× r0b (≥ 140 each); top at least 5 px higher
  (y ≤ 342); the core brighter and yellower where more additive quads overlap.
- Frame 70: still visibly thinner than 54 (≥ 70 warm px, < frame 54).
- Frames 99, 105: a few larger specks (≥ r0b).
- Frames 10, 130, 175: 0. Embers unchanged.

Claude's comparison of r1 with its prediction (warm px / top y, crop as above):
r0b 12: 72/348 · 40: 58/349 · 54: 76/347 · 70: 36/347 · 99: 2 · 105: 7 · 10/130/175: 0;
r1  12: 170/345 · 40: 164/346 · 54: 162/345 · 70: 108/345 · 99: 33 · 105: 27 · 10/130/175: 0.
- Matches: full-fire frames ≥ 140 (2.2–2.8×); core brighter and yellower;
  frame 70 thinner than 54 and ≥ 70; 99/105 above r0b; 10/130/175 empty.
- Misses: the top rose only 2–3 px, not ≥ 5. Explanation: flame height is set
  by how far particles travel (0.5–1.1 u/s for 0.8 s) and the scale curve's
  shrink to 0.2 at the end; a bigger quad mostly widens and thickens the core.
  The soft radial texture's faint upper edge also falls below the warm-pixel
  threshold, so the measured top understates the visible one.

User runtime verdict (running preview, 1280×720): **kept** — "Keep." [保留] (2026-11-07).
Strips: `captures/fire_pit_flames/r0b/`, `captures/fire_pit_flames/r1/`

### Effect A r1 — results (after the user's approval)

Edited `effects/hit_spark.tscn` (QuadMesh_puff size 0.5 → 1.0) and the config
test's expected value; `test_hit_spark_config.gd` at 60 fps: 165 checks, 0
failed. Strips `captures/hit_spark/r1/` (city) and `r1-snow/`, same seeds and
the same stand-ins (brawler / ice_warrior at (−1.5, 0.65, −14)) as r0.

Claude's comparison with the prediction:
- **Miss:** the "below" snow patch (630–650 × 378–386) reads 158.3 on every
  frame in both r0-snow and r1-snow; predicted ≤ 150 on frames 15 and 20.
- What did change: pixels differing by > 3 levels between r0 and r1 lie only
  in 621–661 × 340–376 (≈ 34 px, about the stand-in's body), 446–513 px per
  frame on snow and 622–808 on the city street, frames 10–20; mostly darker on
  frames 10–12 (428 / 344 px on snow); none at frame 30. On screen: a slightly
  larger, darker brown haze over the torso; the snow around the body looks the
  same.
- Explanation: the puff starts at alpha 0.55 and fades linearly to 0 while it
  grows 0.6 → 1.4, through a soft radial texture, so by the time it is large it
  is nearly transparent; doubling the quad widened the visible part only to
  the body's edges. The city prediction (≤ 3 levels in the patch) held.

User runtime verdict (running preview `-- --loop --snow`, 1280×720): **kept** —
"Keep." [保留] (2026-11-07).
Strips: `captures/hit_spark/r0/`, `r0-snow/`, `r1/`, `r1-snow/`.
