# Case 2: The sprite that was "crisp"

Chapter 2, Game art and sound assets. Seeded flaw: pixel art imported with linear filtering (and mipmaps) and scaled by a non-whole factor, then reported as "crisp" from the file's resolution alone. Key terms: nearest vs linear filtering, integer scaling, import settings, mipmaps, texel.

---

# STUDENT PAGE

## Scenario
Priya is the art lead on a retro platformer. Artists made a 16 by 16 pixel hero in a pixel-art tool. She wants the hero to look like sharp, hard-edged squares at game size, 3.5 times larger on screen, because the blurry version in the build looked "muddy". She asks a coding agent to fix the hero's sprite.

## The instruction given to the agent
"The hero sprite looks blurry in the game. Make it crisp pixel art at 3.5x size and confirm it is correct."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Checked hero.png: 16x16, PNG, alpha present, no compression artefacts. Source is clean.
Set Sprite2D.scale = Vector2(3.5, 3.5).  (16 px -> 56 px)
Import settings: Filter left at the project default (Linear), Mipmaps: On,
because those are the engine's recommended defaults for textures.
Result: the sprite is sharp because the source file is pixel-perfect
and its resolution is only 16x16.
Status: confirmed crisp at 3.5x.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in this report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "confirmed crisp" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Priya why her hero is still blurry.

---

# TA RUBRIC PAGE (not for students)

## The fixed rubric
| Row | Pts | Awarded for |
|---|---|---|
| Catches the flaw | 3 | Q1 |
| Exact term | 2 | Q1 |
| Asks for evidence | 2 | Q2 |
| Fix or next step | 2 | Q3 |
| Scope and plain language | 1 | Q4 |

## The flaw in one sentence
The sprite is sampled with linear filtering (and mipmaps) at a non-integer scale (3.5), which blends neighbouring texels and blurs hard pixel edges; a clean source file says nothing about how the engine samples it.

## Terms
- **Full credit (2):** nearest filtering (vs linear); integer scaling (a whole-number factor such as 3 or 4); import settings (the filter/mipmap import options).
- **Half credit (1):** "anti-aliasing is on", "resolution is the problem", "texture quality setting", "compression" with no mention of filtering.
- **No credit:** "needs a higher-resolution image", "convert to JPEG", "turn on smoothing".

## Acceptable evidence requests
1. "Render one frame at game size, crop the hero and enlarge it; show that each source pixel appears as a solid square (zoom screenshot) with Filter = Nearest."
2. "Report the sprite's filter setting and the scale factor from the project, and show a screenshot at scale 3 or 4."

**Unacceptable:** "Confirm the PNG has no compression", "check the file is 16x16" (that is already claimed), "ask the artist".

## Traps
- Two causes are seeded: filter and 3.5 scale. A student who names only one still catches the flaw; naming both is the strongest Term.
- "Mipmaps" belong in 3D distance; naming them as a cause is not wrong but is secondary.
- Do not credit "make it look crisp" as a correction; it must name the setting or the whole-number scale.

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The agent proved the file is clean but never looked at how Godot samples it. The filter is Linear, which blends texels, and 3.5 is a non-integer scale. Pixel art needs Nearest filtering and integer scaling." Q2: "Zoom screenshot at game size: each source pixel must be a solid square with Nearest set." Q3: "Set the sprite's texture filter to Nearest, turn mipmaps off, and use a scale of 3 or 4. Show a cropped screenshot." Q4: "The game is smoothing the edges between the pixels, so the picture looks soft; we need it to keep them hard and use a whole-number size." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 never says which whole number to use.*

**Typical (6/10).** Q1: "The filter should be Nearest. The agent did not change it." Q2: "Look at it in the game." Q3: "Change the filter to Nearest." Q4: "The picture is being smoothed, so it looks blurry." *Catches 3; Term 1 (Nearest, no scaling or why); Evidence 0 ("look at it" is not a check); Fix 1 (filter only, scale still 3.5); Scope 1.* Total 6. *Reason: right main fix, no evidence request, scale missed.*

**Fluent but wrong (3/10).** Q1: "The resolution is insufficient for 3.5x; the pipeline should upsample to 56 by 56 with Lanczos and enable anti-aliasing on the sprite for sharper edges." Q2: "Compare PSNR between the source and the rendered sprite." Q3: "Upscale hero.png to 56 px with Lanczos and turn on MSAA." Q4: "It needs more pixels." *Catches 0 (anti-aliasing and upsampling are the opposite of the fix); Term 0; Evidence 1 (a measurement exists but would reward blur); Fix 1 (specific but wrong); Scope 1 (plain).* Total 3. *Reason: technical vocabulary pointing the wrong way.*
