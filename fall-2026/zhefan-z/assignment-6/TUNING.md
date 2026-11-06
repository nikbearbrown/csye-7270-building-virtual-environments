# TUNING — Assignment 6

Every revision records what I saw, Claude's reading, the change I approved, Claude's prediction, Claude's comparison and my verdict. Strips are fixture captures from the preview scenes (Movie Maker, 30 fps), not gameplay. My observations are in my words *(translated from my Chinese)*.

## 2026-11-05 — Effect A, r0: first look, before Claude read anything

What I saw (preview `previews/fireball_impact_preview.tscn`, windowed, 1280×720; once single, once with `retrigger`): sparks spray out in all directions to about one mage height; a white puff of smoke in the middle. The smoke's strength felt right and the whole burst's duration felt right. I did not notice whether the two impacts in the retrigger run looked different from each other.

Effect scene at this point: `c82d338`.

## 2026-11-05 — Effect A, r0b: the preview, not the effect (fixture fix, no effect change)

What I saw (preview with `retrigger`, windowed, 1280×720, `--time-scale 0.25`): the two impacts looked almost the same, as if stamped.

Claude's reading of r0 and r0-retrigger (`prompt-4a.txt`): frames 10–15 match the intent; at frame 20 the sparks are already faint dark-red specks, behind the brief's "orange-red"; 30 faint smoke only; 50 empty. On the sameness, it measured the spark positions instead of judging by eye: the second impact (r0-retrigger frame 20, 4 frames old) matches the first (r0 frame 15, 5 frames old) scaled by 0.83 with a mean error of 1.6 px, against 4.1 px for a 15°-rotated control. Its explanation: the preview gave the second impact seed + 1, which drew almost the same random values. It recommended fixing the preview, not the effect, and said a `lifetime_randomness` change would not remove what I saw.

Change: `previews/fireball_impact_preview.gd`, seeds `first_seed + 1000 × spawn index` (1 and 1001), approved by me. The effect scene is unchanged (`0069149`).

Claude's prediction for r0b: frames 10–15 identical to r0-retrigger (the first impact keeps seed 1); from frame 20 the second impact no longer lines up with the first.

My verdict (preview with `retrigger`, 1280×720, `--time-scale 0.25`): the two impacts now look different. Kept. The sameness was the fixture's.

Claude against me: Claude read frame 20 as behind the intent (sparks too dark too soon). Watching in slow motion, I judged the darkening rhythm right. My verdict stands; no change made for it.

Strips: `captures/fireball_impact/r0/`, `r0-retrigger/`, `r0b-retrigger/`. Commits: `0069149`.

## 2026-11-05 — Effect A, revision r1 (observation-driven)

What I saw (running game, main scene, 1280×720, Effect A wired in since `f5743f5`): impacts on the ground, on the walls at the screen edges and on the wolf all read well; the smoke is clearly visible over the pit; a hit on the wolf is unmistakable; rapid casting looks fine. The one thing I wanted to try: the moment of impact should look brighter, or last a little longer.

Claude's reading of r0 (`prompt-4b.txt`), measured against the empty frame 50: at frame 10 the centre's brightest pixel was 144/255 and none above 200 within 3 px; the 86 pixels above 200 sat in a ring 4–8 px out. A grey disc with a white rim, not a white-yellow flash: `Smoke` draws on top of `Sparks` and starts at full opacity at age 0, although the brief's intent puts the puff at 0.1–0.8 s.

Change: Smoke colour ramp (`Grad_smoke`), offsets `(0, 1)`, grey alpha 0.55 → 0, to offsets `(0, 0.125, 1)`, grey alpha 0 → 0.55 → 0 (a 0.1 s fade-in of its 0.8 s life); colour and peak unchanged. Approved by me. The burst and sparks untouched.

Claude's prediction for r1: frame 10 no grey disc, sparks at full brightness, most of the 86 bright pixels back; frame 12 smoke at about 0.37, a darker grey centre; frame 15 smoke slightly stronger (about 0.50 vs 0.44); frame 20 about 0.37 vs 0.32; frame 30 about the same; frame 50 empty. It said the change makes the impact brighter, not longer.

Claude's comparison of r1 with its prediction: frame 10 matched and more: pixels above 200 within 12 px 86 → 175, centre brightest 144 → 230, a white disc with a faint grey tint (its caveat that the cave might show through was wrong). Frame 12 did not match: the centre changed about −5%, not the predicted −33%. Frames 15–30 moved in the predicted direction but less; frame 50 identical. Its explanation: each captured frame is one 1/30 s step older than it assumed (frame n shows about (n − 9)/30 s, backed by the spark distances), plus staggered puff starts and overlapping puffs damping the change. So the change brightens about one frame of the strip.

My verdict (running game, main scene, 1280×720): the moment of impact is brighter. Kept.

Strips: `captures/fireball_impact/r0/`, `captures/fireball_impact/r1/`. Commits: `35a1f70` (change), this entry with the r1 strip.

## 2026-11-06 — Effect B, r0: first look, before Claude read anything

What I saw (preview `previews/fireball_trail_preview.tscn`, windowed, 1280×720): the trail is longer than the fireball; it flickers; after the fireball stops, the rest of the trail fades away slowly where it is.

Effect scene at this point: `8484040`.
