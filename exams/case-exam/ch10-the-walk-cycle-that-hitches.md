# Case 10: The walk cycle with a hitch

Chapter 10, Animation foundations. Seeded flaw: a looping walk clip whose last key repeats the first pose, so the pose is held for two frames at the loop point (a loop seam). The agent's check only counts keys. Key terms: loop seam, keyframe, loop mode, track, frame index.

---

# STUDENT PAGE

## Scenario
Kenji is the animator on a 2D action game. The hero's walk cycle has six poses. In the game the walk looks fine except for a tiny stall once per cycle, "like a limp". He asks the agent to check the clip and fix it if needed.

## The instruction given to the agent
"The walk animation stalls once per cycle. Inspect the clip and fix it. Report what you checked."

## Agent output
*(Author-written for illustration. This is not a sampled run.)*

```
Clip "walk": length 0.6 s, loop mode: Linear, 1 track (Sprite2D:frame), step 0.1 s
  keys: t=0.0 frame 0 | 0.1 f1 | 0.2 f2 | 0.3 f3 | 0.4 f4 | 0.5 f5 | 0.6 f0
Checks: clip has 7 keys; length 0.6 s is a whole number of 0.1 s steps; loop mode is set.
Change: set update mode to Discrete for the frame track.
Result: the clip is well-formed and loops correctly. The stall was an
interpolation artefact and is fixed.
```

## Questions (10 points)
1. **(5 pts)** What is the flaw in the agent's report, and what is the exact term (or terms) for it?
2. **(2 pts)** Write the one check or instruction that turns "loops correctly" into evidence.
3. **(2 pts)** Write the corrected instruction to the agent.
4. **(1 pt)** In two sentences and no jargon, tell Kenji why the walk stalls.

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
The last key (t = 0.6, frame 0) repeats the first pose, and the loop wraps at 0.6 s back to frame 0, so frame 0 is shown for two steps in a row at the loop point: a loop seam; the agent's checks (key count, length, loop mode set) cannot detect it.

## Terms
- **Full credit (2):** loop seam; duplicate first/last keyframe; the clip length should end one step before the first pose repeats.
- **Half credit (1):** "the end and start are the same", "stutter at the loop", "loop mode is wrong".
- **No credit:** "interpolation", "easing", "the frame rate is too low", "needs more frames".

## Acceptable evidence requests
1. "Step the clip frame by frame headless and print the frame index at each 0.1 s step over two loops; no frame index may appear twice in a row."
2. "Show the frame sequence across the loop point (frames 4, 5, 0, 1) at 0.1 s steps, with each shown once."

**Unacceptable:** "Count the keys again", "watch it and see if it stalls", "check the length is 0.6".

## Traps
- The agent's "Discrete" change is harmless for a frame track; do not credit "interpolation artefact" as a catch.
- A student may propose changing the clip to 0.7 s: that is wrong (adds a hold); the right fix removes the duplicate key or shortens the length to 0.5 s with six keys.
- "Loop mode is wrong" gets Term 1 only if the student sees the end-equals-start problem.

**CAP RULE:** if the flaw is missed, the case maximum is 5/10.

## Scored sample answers
**Strong (9/10).** Q1: "The last key at 0.6 s is frame 0, the same as the first key. On loop it shows frame 0 twice, which is a loop seam. The agent's checks only counted keys and never looked at the frame sequence." Q2: "Step the clip headless over two loops and print the frame index each 0.1 s; none may repeat twice in a row." Q3: "Delete the key at 0.6 s and set the length to 0.6 s (six keys at 0.0 to 0.5). Re-run the frame print." Q4: "The first picture in the walk is shown twice where the walk starts over, so there is a tiny pause." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 says "a tiny pause" but not why the picture repeats.*

**Typical (6/10).** Q1: "The last frame is the same as the first so it shows twice when it loops." Q2: "Play the clip and watch it." Q3: "Remove the last key." Q4: "The walk shows the same picture twice at the end." *Catches 3; Term 1 (describes the repeat, no "loop seam"); Evidence 0 ("watch it" is not a check); Fix 1 (removes the key, but does not say what to do with the clip length or re-check); Scope 1.* Total 6. *Reason: right catch in plain words, no measurable check.*

**Fluent but wrong (3/10).** Q1: "The linear interpolation between frame 5 and frame 0 produces an easing artefact; use cubic interpolation with ease-in-out and enable root motion so the cycle is smooth." Q2: "Compare the easing curve in the animation editor." Q3: "Set the interpolation to cubic and add an ease-out curve." Q4: "The motion is not smooth enough between steps." *Catches 0 (accepts the agent's interpolation story); Term 0 (easing and interpolation are the wrong terms here); Evidence 1 (inspecting the clip is a check, not the right one); Fix 1; Scope 1.* Total 3. *Reason: fluent animation words, never looks at the repeated key.*
