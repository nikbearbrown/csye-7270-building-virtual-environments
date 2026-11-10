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
