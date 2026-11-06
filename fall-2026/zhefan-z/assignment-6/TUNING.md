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
