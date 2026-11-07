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

Note added 2026-11-06: this first look ran the preview windowed without `--fixed-fps`, at my display's rate (144 Hz or more), and the preview stops its carrier on frame 40 by frame count. So the fireball flew only about 0.28 s (stopped at x ≈ 232, not 410) in what I watched. My three observations stand; the flight was shorter than in the game and in the 30 fps strip.

## 2026-11-06 — Effect B in the running game, before tuning

What I saw (main scene, 1280×720, Effect B wired in since `e174c96`): casts to the right and to the left both trail behind the fireball; a shot straight up that times out leaves its trail fading where it was; Esc mid-flight freezes the trail and Esc again resumes it; no trail appears in the first frames after the scene loads; the trail reads over the pit and over the lighter ground. All normal. The one thing I want to try: the trail a little thicker or brighter.

## 2026-11-06 — Effect B, revision r1 (observation-driven)

What I saw (running game, main scene, 1280×720): see the entry above; everything behaved as the brief says, and the one thing I wanted to try was the trail a little thicker or brighter.

Claude's reading of r0 (`prompt-4c.txt`), measured against frame 50: the length is on target (about 71 px at frame 30, against 60–80), but the trail is 4–6 px tall, about a third of the intended 15–21 px, and reads as a row of separate dots with 3–5 px dark gaps, repeating every 8.7 px. It noted that 8.7 px is one 1/30 s step at 260 px/s, and guessed this comes from `GPUParticles2D` simulating at its default fixed 30 fps (not confirmed). The head is saturated (peak lum 240–255); dots older than about 0.15 s fall below lum 100.

Change: `ParticleProcessMaterial.scale_curve`, linear (0, 1) → (1, 0), to linear (0, 2) → (1, 0) with `max_value = 2.0`. Approved by me. It left the colour ramp alone because the brief ties it to the Sparks ramp.

Claude's prediction for r1: dots at the head 8–12 px, overlapping into a continuous strip; about 2.5–3× as many pixels lit; brighter only where dots overlap; length, fade, colours, turbulence and direction unchanged.

Claude's comparison of r1 with its prediction: every pixel lit in r0 is also lit in r1 (same fixed seed, bigger particles), frame 50 identical. Frames 10, 12, 45 and 50 match; frame 40 matches except for a 1 px gap; the head is 11–13 px (about 1.1–1.3 fireballs, was 0.5–0.7). Where it missed: the strip closes only right behind the fireball; from about the second dot back, 1–3 px gaps remain (r0: 3–5 px), because each dot shrinks as it ages and it had used the head size for the whole trail. Frame 30's changed pixels 208 → 421, under its 450–550, because about 150 of them are the unchanged fireball sprite; at frame 40 (no sprite) the count rose ×3.1. Length unchanged, not "a few px longer".

My verdict (running game, main scene, 1280×720): thicker and brighter. Kept.

Strips: `captures/fireball_trail/r0/`, `captures/fireball_trail/r1/`. Commits: `cc1f2f2` (change), this entry with the r1 strip.
