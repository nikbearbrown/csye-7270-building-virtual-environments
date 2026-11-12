# TUNING — Assignment 6

One section per round (r0, r1, …), newest last. I write my own verdict first; only then does Claude read the frame strips.
The preview scenes are test fixtures, so every capture from them is labelled a **fixture capture**.

---

## Effect A: landing dust

### r0 — 2026-11-10 — the version the agent built, untuned

- **What I looked at:** `godot/previews/landing_dust_preview.tscn`, run windowed at the project's window size (2048 × 1152). I first watched it without Movie Maker, then ran all four captures (bright / dark background × full fade / retrigger) and watched them slowed down. Which background my first windowed look used is not recorded.
- **Random seed:** the preview's instance of the effect has `use_fixed_seed` on (seed 7270, commit 1df1db72); the effect scene itself does not.
- **Fixture captures:** `captures/landing_dust/r0/`
  - `bright-fade/` and `dark-fade/`: frames 10, 11, 12, 15, 20, 30, 50, 58, 60;
  - `bright-retrigger/` and `dark-retrigger/`: frames 24, 25, 26, 27, 30, 35;
  - command (from this folder, in Git Bash; `$(pwd -W)` gives the absolute Windows path Godot needs):

```bash
godot_console --path godot res://previews/landing_dust_preview.tscn --write-movie "$(pwd -W)/captures/landing_dust/r0/bright-fade/frame.png" --fixed-fps 30 --quit-after 80 -- bright
```

  The other three runs change the folder and the words after `--` (`bright retrigger`, `dark`, `dark retrigger`). The rest of each 80-frame sequence and Movie Maker's `frame.wav` were deleted.

#### My first verdict (written before Claude read anything)
(2026-11-10, my own words to Claude)

The camera looks down at an angle at the floor, the area by the desks, and a ripple ring on the floor appears the moment the capsule spawns (or the moment the game starts). But the rising dust is not noticeable.

(Added after capturing r0 and watching it slowed down)

I ran them all and I saw it; slowed down it really is clearer. But the dust effect I mean is a number of grey cloud-like puffs, not a number of dots.

Frame-by-frame comparison with my predictions in CHANGE-BRIEF: not written yet.

#### Claude's reading (after my verdict above)
(Claude Code / Claude Opus 5.5, 2026-11-10, reading the four fixture captures in `captures/landing_dust/r0/`)

- **When it appears:** triggered at frame 10. By pixel comparison, the picture first changes on frame 11, one frame late, so frames are read from 11.
- **The whole effect is small:** in the 2048 × 1152 frame, the area that changes is only about 200 × 130 pixels, at the bottom of the capsule.
- **Dust:** small light specks, about 5–8 pixels, slightly warm, and fewer than 24 can be seen.
  - Clearest on frames 12–20; one or two left on frame 30; nothing visible on frames 50, 58 and 60.
  - The brief predicts a slow fade over 1.6 s; in the picture it can no longer be seen after about 0.7 s (frame 30).
  - Many specks are hidden by the capsule: the emission ring's radius is 0.2 m, smaller than the capsule's 0.3 m, so the dust is born inside the capsule, and the camera is behind the character.
- **Ground ring:** a thin beige ring is visible on frames 15 and 20 and gone by frame 30, matching its 0.45 s lifetime. It is more noticeable than the dust.
- **Contrast:** under both backgrounds the floor is a light grey-blue. The "dark" background is not dark; it is only at the edge of a desk's shadow, so the two sets look almost the same. The dust colour (0.48, 0.45, 0.40) is unshaded and close to the floor's brightness; only its slight warmth sets it apart.
- **Retrigger:**
  - frame 24 still has a few old specks; on frame 25 the old ones have all gone and the character has moved to the new spot 0.5 m away;
  - no new dust yet on frame 26; the new ring starts on frame 27; frames 30 and 35 show the new ring and a few specks;
  - the old effect is cleared and replays at the new position, as the brief's retrigger rule says.
- **Why it reads as dots rather than clouds:**
  - each speck's quad is only 0.08 m; with the 0.6–1.2 scale it is 5–10 cm, which is a few pixels from about 2.5 m away;
  - the texture is a round gradient, solid in the middle and fading at the edge, so each speck is a small soft dot;
  - the 24 specks spread far apart and do not overlap, so they never join into a puff.

#### What to change next round (my decision)
Not decided yet. Claude pointed out that the cloud-like look I want conflicts with the brief's "no higher than the ankle (0.10 m)" rule, so it would be a change of intent, not only of values, recorded as a dated revision of CHANGE-BRIEF; Claude suggested making it in Step 4 (tuning).

Decided (2026-11-11): change the intent first, then tune. The new intent is 6–8 neutral-grey puffs, each 0.18–0.25 m across, visible top edge no higher than 0.30 m, with a few faint grey puffs still visible at 0.7 s. It is in CHANGE-BRIEF's revision history (commit e121aede).

---

## 2026-11-12 — Effect A, revision r1
- **What I saw (running game, editor F5, window 2048 × 1152):** on landing there is dust and the ring, and nothing fires at the start. The dust I want is puffs that look like grey clouds, not a scatter of dots.
- **Claude's reading of r0:** (interactive `claude` session, Claude Code / Opus 5.5, 2026-11-12)
  - Frames 12–20: only scattered warm specks of 5–8 pixels that never overlap; at frame 15 the ground ring is more visible than the dust.
  - Frame 30: only 2–3 barely visible specks, against the revised intent's "a few faint grey puffs still visible at 0.7 s".
  - Frame 50: nothing left.
  - The colour is a warm beige, not neutral grey. The "dark" background is only the edge of the desk's shadow, so the two sets differ little.
  - Retrigger: the timing and the clearing of the old dust are right, but it looks just as dotty.
  - Cause: the quads are only 0.08 m, a few pixels after scaling at that distance, and the particles do not overlap; the emission ring radius of 0.2 m is smaller than the capsule radius of 0.3 m, so many are hidden by the capsule.
- **Change:** `Dust` `draw_pass_1` QuadMesh `size` (0.08, 0.08) → (0.32, 0.32). **Approved by me after the fact:** the prompt said to give the proposal and the prediction and wait for my approval before editing, but the agent took my "start" (meant as "start reading the frames and proposing") as permission for everything. It edited the scene file and the test's expected value and ran the configuration test first, and only then sent the reading, the proposal and the prediction together (in the session transcript the edit is at 07:56:36 UTC, the prediction at 07:57:19 UTC). I read the proposal, agreed to keep the change, and went on to capture r1. Also, this time the agent read the prompt from the file `prompt-4-r1.txt` instead of my pasting it; the text is the same.
- **Configuration test:** 156 passed, 1 failed. The failure was "Dust top including quads = 0.232 m <= 0.10 m". Following the brief revision, the agent did not change that check: it changes to 0.30 m only once this round is kept.
- **Claude's prediction for r1:** (written before r1 was rendered, but after the edit, see above)
  - 10 / 11: frame 10 invisible; frame 11 may show a very faint haze.
  - 12: a few very faint, soft-edged grey-beige puffs at the feet, clearly bigger than r0's specks; the small ring just appearing.
  - 15: the most visible frame, a low patch of overlapping puffs at the feet reaching out on both sides of the capsule; the ring less visible than the dust.
  - 20: the cloud spreads out and thins; the ring at full size, very faint.
  - 30: the ring gone; a few faint grey puffs still visible, about 25% bigger than at birth.
  - 50: perhaps a last, very faint haze.
  - 58 / 60: nothing.
  - Retrigger 25 / 27 / 30 / 35: the same timing as r0; at 25 the old cloud is cleared, at 27 it appears at the new spot, at 30 it is most visible, at 35 it spreads and fades; the old cloud does not come back.
  - Problems it expected to remain (one per later round): the lower half of each billboard going into the floor, leaving a hard straight line at the bottom of the puffs; 24 overlapping puffs joining into one patch instead of 6–8 separate puffs; the colour still warm; the overall diameter reaching 1.0–1.2 m, over 0.9 m; `visibility_aabb` possibly too small horizontally (±0.68 m against ±0.6 m).
- **Claude's comparison of r1 with its prediction:** (same interactive session, `prompt-4-r1-compare.txt`, no files changed)
  - Achieved: bigger and longer-lasting. Changed pixels at frame 15 went from 2988 to 5271, at frame 20 from 5078 to 10557. At frame 30 (0.7 s), r0 is almost invisible and r1 is still clear (bright background 301 → 5143, dark 44 → 1861).
  - Frame by frame: 10, 11, 12, 30, 58, 60 and the retrigger set match the prediction. 15 matches in part: "most visible" is right, but the dust sits at the capsule's left, right and front instead of spreading into one patch, and the ring is about as visible as the dust. 20 shows five or six separate soft patches in a ring around the feet, the far side hidden by the capsule. 50 does not match: the predicted faint haze is not visible (largest difference 3).
  - The five risks: the floor cut is **confirmed** (the lower half of every patch is cut off by the floor in a horizontal line, because the billboard centre is only 0.04 m up and its radius is 0.13–0.19 m); joining into one patch is half right (it is a broken ring of patches, and 6–8 puffs cannot be told apart); the warm colour is **confirmed** (it reads as orange-beige, and it is seen through that warmth rather than through a difference in brightness); the diameter over 0.9 m was **wrong** (about 0.9 m, as in r0; the soft outer edges cannot be seen); `visibility_aabb` shows no problem in these frames.
  - Its explanation: the floor cut, the capsule hiding the far side and 24 patches spread evenly on a ring together make it read as "a ring of smudges" rather than cloud puffs. At frame 50 the opacity is about 0.05, so each pixel changes by less than 3/255. The height is only about 15 pixels above r0's, far below 0.30 m, but it could not convert that to metres from the picture.
- **My verdict (running game, window 2048 × 1152):** kept, because I think Effect 1 is good enough now; I can no longer find anything wrong with it. After all, what lands from a jump is a human, not a mech, so I don't think the dust needs to be big.
- **Tuning of Effect A stops here (my decision, 2026-11-12).** What Claude pointed out and I did not tune further: in r1 the colour is still warm (the brief's intent says neutral grey); 24 patches go round the feet in a ring and 6–8 puffs cannot be told apart; the lower half of each puff is cut off in a straight line by the floor; the far side is hidden by the capsule. In the running game I do not see these as problems, so I stop on my in-game judgement. This differs from Claude's reading of the strips and is recorded here.
  - My view on two of these points (2026-11-12): **the capsule hiding the dust** does not matter. First, it is smoke, and smoke being hidden by a solid object is normal; my design document also says there is no special demand for technical perfection, so in practice the hiding is fine. **The colour:** I really cannot see much difference between the beige and a neutral grey. So the colour intent goes back to "low-saturation, slightly warm grey"; see the 2026-11-12 revision in CHANGE-BRIEF.
- **Strips:** `captures/landing_dust/r0/`, `captures/landing_dust/r1/`
- **Commits:** 9799850d (r1 strips), c1ef8d69 (the kept change: scene, test limit 0.10 → 0.30 m, brief revision, the two prompts). Configuration test 157 passed, state test 27 passed.
