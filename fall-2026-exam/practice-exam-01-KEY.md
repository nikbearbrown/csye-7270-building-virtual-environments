# Practice exam 01: ANSWER KEY (instructors and TAs; students read it only AFTER doing the exam cold)

How cases are scored: catches the flaw 3, uses the exact term 2, asks for evidence 2, gives a fix or next step 2, keeps scope and plain language 1. If the flaw is missed, the case is capped at 5/10. Grammar and polish earn nothing.

Physics and shader cases (chapters 1, 4, 6, 7, 8) are **awaiting a game developer's check**.

---

# Part A: Cases

## Case 1: The test that "passed" after loosening
*Chapter 0, The toolchain*

**The flaw.** The test was run without a pinned frame rate (`--fixed-fps 60`), so it failed for a timing reason, and the agent widened the tolerance until it passed (loosening), which turns a real warning into a false pass.

**Terms that earn the Exact-term credit**
- **Full credit (2):** fixed frame rate / pinned time step / `--fixed-fps`; loosening the check; false pass; claim vs evidence (any one, used correctly).
- **Half credit (1):** "flaky", "timing issue", "not deterministic", "test was changed" with no mention of pinning or of loosening as the problem.
- **No credit:** "bug in the scoring code", "Godot is slow", "needs more tests".

**Acceptable evidence requests**
1. "Re-run the original, unmodified test with `--fixed-fps 60` and show the output; it should pass at 180 +/- 3."
2. "Revert the tolerance, run it three times with the frame rate pinned, and show that the tick numbers are identical each time."

**Unacceptable:** "Run it a few more times and see if it passes", "check that it looks fine", "make the test more robust".

**One strong sample answer.** Q1: "The agent changed the test until it passed. The real cause was that the headless run was not pinned to a fixed frame rate, so the tick count drifted. Widening to ±40 is loosening, and the PASS is a false pass." Q2: "Revert the tolerance and run `--fixed-fps 60`, original numbers expected." Q3: "Restore ±3. Run the test with `--fixed-fps 60`. If it still fails, report the numbers; do not edit the test." Q4: "It only passed because the agent loosened the test, a false pass, so we do not know the game is unchanged." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: everything is right, but Q4 reuses jargon for a non-technical reader.*

---

## Case 2: The sprite that was "crisp"
*Chapter 2, Game art and sound assets*

**The flaw.** The sprite is sampled with linear filtering (and mipmaps) at a non-integer scale (3.5), which blends neighbouring texels and blurs hard pixel edges; a clean source file says nothing about how the engine samples it.

**Terms that earn the Exact-term credit**
- **Full credit (2):** nearest filtering (vs linear); integer scaling (a whole-number factor such as 3 or 4); import settings (the filter/mipmap import options).
- **Half credit (1):** "anti-aliasing is on", "resolution is the problem", "texture quality setting", "compression" with no mention of filtering.
- **No credit:** "needs a higher-resolution image", "convert to JPEG", "turn on smoothing".

**Acceptable evidence requests**
1. "Render one frame at game size, crop the hero and enlarge it; show that each source pixel appears as a solid square (zoom screenshot) with Filter = Nearest."
2. "Report the sprite's filter setting and the scale factor from the project, and show a screenshot at scale 3 or 4."

**Unacceptable:** "Confirm the PNG has no compression", "check the file is 16x16" (that is already claimed), "ask the artist".

**One strong sample answer.** Q1: "The agent proved the file is clean but never looked at how Godot samples it. The filter is Linear, which blends texels, and 3.5 is a non-integer scale. Pixel art needs Nearest filtering and integer scaling." Q2: "Zoom screenshot at game size: each source pixel must be a solid square with Nearest set." Q3: "Set the sprite's texture filter to Nearest, turn mipmaps off, and use a scale of 3 or 4. Show a cropped screenshot." Q4: "The game is smoothing the edges between the pixels, so the picture looks soft; we need it to keep them hard and use a whole-number size." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 never says which whole number to use.*

---

## Case 3: The shield nobody can pick up
*Chapter 4, Scenes, collision and physics*

**The flaw.** The shield's layer and mask are swapped (it sits on the player's layer and looks for pickups), so the engine never reports the player overlapping it, and the test hid this by firing the `body_entered` signal by hand instead of letting physics produce it.

**Terms that earn the Exact-term credit**
- **Full credit (2):** collision layer vs collision mask (what an object is vs what it looks for), stated correctly or the swap named; detection vs response is also acceptable; "emitted the signal by hand / bypassed detection".
- **Half credit (1):** "collision settings are wrong", "wrong layer", "bitmask" with no explanation, "the area is not detecting".
- **No credit:** "needs a bigger shape", "z-index", "the timer is wrong", "signal not connected".

**Acceptable evidence requests**
1. "Run a test that moves the player into the shield with the real physics (no hand-emitted signal) and show the shield activates; also show it does not activate when the player is far."
2. "Print the shield's layer and mask and the player's layer and mask; show that the shield's layer is in the player's mask, or the player's layer is in the shield's mask."

**Unacceptable:** "Run the same test again", "check the timer is 3 seconds" (it already passes), "play it and see".

**One strong sample answer.** Q1: "The shield's layer and mask are swapped. It is on layer 1, the player's layer, and its mask looks for layer 3, where nothing lives; the player's mask is 2, so the player does not look for the shield either. The engine never detects the overlap. The test passed only because it emitted the signal by hand." Q2: "Run a test where the real player moves into the shield with physics and check the shield activates." Q3: "Put the shield on layer 3 (pickups) and set its mask to 1 (player). Rewrite the test to walk the player in through physics and remove the hand-emitted signal." Q4: "The game treats the shield and the player as things that do not look at each other, so touching does not count." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 is vague about why they do not look at each other.*

---

## Case 4: The failure flash that draws a box
*Chapter 6, Shader foundations*

**The flaw.** `mix(tex, ink, flash)` mixes all four RGBA channels, so as `flash` rises the alpha of the transparent area rises to the ink's alpha of 1.0 and a dark rectangle appears around the sprite; the checks (compiles, parameter reaches 1.0) cannot see this, so "done" has no visual evidence.

**Terms that earn the Exact-term credit**
- **Full credit (2):** alpha channel / RGBA overwritten (alpha should be kept from the texture: mix only `.rgb`, keep `tex.a`); compile error vs visual bug.
- **Half credit (1):** "the transparency is lost", "the shader tints the whole sprite sheet", "should use modulate" with no mention of alpha.
- **No credit:** "wrong shader type", "uniform should be a varying", "TIME is not used".

**Acceptable evidence requests**
1. "Render one frame with flash = 1.0 over a bright background and show a screenshot; the area outside the character must still show the background."
2. "Test the fragment output at a transparent pixel: with flash = 1.0, alpha at that pixel must still be 0."

**Unacceptable:** "Check it compiled again", "check the parameter reaches 1.0" (already checked), "run the game and tell me if it looks fine" (no pass/fail).

**One strong sample answer.** Q1: "`mix` runs on all four channels, so alpha is mixed toward the ink's alpha of 1. The transparent background turns opaque and shows as a dark box. Alpha should be kept from the texture. The checks only proved it compiles and the number moves." Q2: "Render one frame at flash = 1.0 over a bright background and check the area outside the sprite still shows the background." Q3: "Mix only the rgb and set COLOR.a to the texture's alpha, then show the screenshot." Q4: "She will see a dark square around the hero instead of just the hero turning dark." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 describes the bug, as asked, but does not say what will be seen after the fix.*

---

## Case 5: The golden image that agreed with itself
*Chapter 8, Shader verification*

**The flaw.** The agent replaced the golden image with the new shader's own output, so the test compares the new behaviour to itself (a circular test oracle) and passes by construction; the real difference (0.07) was the regression the test existed to catch.

**Terms that earn the Exact-term credit**
- **Full credit (2):** test oracle (the reference must come from somewhere independent, such as the old build or the spec); golden/reference image regenerated from the thing under test; false pass; loosening is not the term here (the check was replaced, not widened).
- **Half credit (1):** "cheated", "reset the test", "not a real test", "reference is wrong".
- **No credit:** "needs a higher frame rate", "compile error", "should use a software renderer" (that is a fix detail, not the flaw).

**Acceptable evidence requests**
1. "Restore the original golden image from version control, render the old and new build at the same pinned frame and clock, and show the difference between them; explain the 0.07 before accepting any new reference."
2. "Check frame 30 of the new build against the old build's frame 30 with the clock pinned; report the difference and a screenshot."

**Unacceptable:** "Run the test again" (it will pass), "check it compiles", "compare it to itself with a tighter tolerance".

**One strong sample answer.** Q1: "The agent overwrote the golden image with the new output. That makes the golden image come from the code being tested, a circular test oracle, so the PASS is a false pass. The 0.07 difference was the regression." Q2: "Restore the old golden from version control, render old and new at the same pinned clock and frame, and show the difference image." Q3: "Revert the golden image. Do not regenerate it. Explain the 0.07 difference before changing any reference." Q4: "It compared the new picture to a copy of itself, a circular oracle, so it could never disagree." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 repeats jargon for a non-expert.*

---

## Case 6: The walk cycle with a hitch
*Chapter 10, Animation foundations*

**The flaw.** The last key (t = 0.6, frame 0) repeats the first pose, and the loop wraps at 0.6 s back to frame 0, so frame 0 is shown for two steps in a row at the loop point: a loop seam; the agent's checks (key count, length, loop mode set) cannot detect it.

**Terms that earn the Exact-term credit**
- **Full credit (2):** loop seam; duplicate first/last keyframe; the clip length should end one step before the first pose repeats.
- **Half credit (1):** "the end and start are the same", "stutter at the loop", "loop mode is wrong".
- **No credit:** "interpolation", "easing", "the frame rate is too low", "needs more frames".

**Acceptable evidence requests**
1. "Step the clip frame by frame headless and print the frame index at each 0.1 s step over two loops; no frame index may appear twice in a row."
2. "Show the frame sequence across the loop point (frames 4, 5, 0, 1) at 0.1 s steps, with each shown once."

**Unacceptable:** "Count the keys again", "watch it and see if it stalls", "check the length is 0.6".

**One strong sample answer.** Q1: "The last key at 0.6 s is frame 0, the same as the first key. On loop it shows frame 0 twice, which is a loop seam. The agent's checks only counted keys and never looked at the frame sequence." Q2: "Step the clip headless over two loops and print the frame index each 0.1 s; none may repeat twice in a row." Q3: "Delete the key at 0.6 s and set the length to 0.6 s (six keys at 0.0 to 0.5). Re-run the frame print." Q4: "The first picture in the walk is shown twice where the walk starts over, so there is a tiny pause." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 says "a tiny pause" but not why the picture repeats.*

---

## Case 7: The click that is twice as loud
*Chapter 12, Audio and triggers*

**The flaw.** `hit_judged` is connected to the handler twice (editor connection and `connect()` in `_ready`), so one hit calls the handler twice and starts two voices on the polyphonic player that sum, roughly doubling the level and clipping; the test only asserts "is playing", which is true with one or two voices.

**Terms that earn the Exact-term credit**
- **Full credit (2):** a signal connected twice / duplicate connection (handler called twice); voice / polyphony (two voices); clipping.
- **Half credit (1):** "plays twice", "doubled sound", "too loud", "volume is too high" without the double-connection cause.
- **No credit:** "bus volume too high" as the cause; "sample rate"; "attenuation".

**Acceptable evidence requests**
1. "Force one Perfect hit and count handler calls and the number of active voices on the click player; require exactly 1 of each."
2. "Count the connections on `hit_judged` and require exactly one."

**Unacceptable:** "Assert it is playing" (already tested), "listen to it", "lower the bus volume and check".

**One strong sample answer.** Q1: "The signal is connected twice: once in the editor and again in code. One hit calls the handler twice and starts two voices, which sum and clip. The test asserted only that the player was playing." Q2: "Force one hit and count the handler calls and the voices; both must be 1." Q3: "Remove one of the two connections, keep the one in code, and assert exactly one connection and one voice per hit." Q4: "The same click was started twice at the same moment, so it adds up to be too loud and crackly." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 says "crackly" but does not say it only happens on hits.*

---

# Part B: Multiple-answer questions

T = true (should be checked), F = false (should be blank).

**1.** (`MA-ch01.1`, None)

- A = F: An instance is the set of nodes created from a scene, not the file.
- B = F: The scene tree is the live hierarchy of nodes in the running game.
- C = F: A scene holds any number of nodes arranged in a tree.
- D = T: Godot builds everything from nodes, such as Sprite2D or Timer, and the type gives the abilities.
- E = T: A scene is a tree of nodes saved as a file that other scenes can reuse.

**2.** (`MA-ch04.1`, None)

- A = T: The agent might build a solid body that stops the player.
- B = F: Detection reads the collision shape; the sprite is only a drawing.
- C = T: An area is a detection region that reports overlap and applies no response.
- D = T: Each element of the behaviour is named.
- E = F: Pushing back is a solid body's response, not an area's.

**3.** (`MA-ch06.1`, None)

- A = T: Interpolation fills in values between corners.
- B = T: Rasterization emits one fragment per covered position.
- C = T: The other fragment is wasted work (overdraw).
- D = F: A vertex is a corner point; fragments come from rasterization.
- E = F: A fragment can still be rejected by depth test or discard, or be blended.

**4.** (`MA-ch09.1`, None)

- A = T: The emitter is where particles are born, and its rate or burst settings say when.
- B = T: A particle is a lightweight record with a life cycle: it is born, updated each step and removed.
- C = T: The system covers emission, simulation and drawing, and a larger effect can use more than one emitter.
- D = F: Particles are data processed in bulk by the system, not individual objects with scripts.
- E = F: The whole effect is the particle system; the emitter is only the part that creates particles.

**5.** (`MA-ch11.1`, None)

- A = F: That describes a condition; the transition is the route the condition guards.
- B = T: Transitions are the explicit connections that say which state may follow which.
- C = T: A state machine has one current state, which separates it from a set of independent flags.
- D = F: That describes a transition; a condition is the test that lets a transition fire.
- E = T: Parameters are the inputs that the game writes and the conditions read.

**6.** (`MA-ch13.1`, None)

- A = F: A higher target rate leaves less time per frame, so the budget gets smaller.
- B = T: Because FPS is the reciprocal of frame time, equal FPS drops are not equal millisecond costs.
- C = T: Frame time is the time one frame takes, usually given in milliseconds.
- D = F: Refresh rate is how often the display updates, not how often the GPU renders.
- E = T: The budget is 1000 divided by the target rate, so 60 Hz gives about 16.7 ms.

