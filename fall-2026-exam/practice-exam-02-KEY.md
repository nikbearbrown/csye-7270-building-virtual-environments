# Practice exam 02: ANSWER KEY (instructors and TAs; students read it only AFTER doing the exam cold)

How cases are scored: catches the flaw 3, uses the exact term 2, asks for evidence 2, gives a fix or next step 2, keeps scope and plain language 1. If the flaw is missed, the case is capped at 5/10. Grammar and polish earn nothing.

Physics and shader cases (chapters 1, 4, 6, 7, 8) are **awaiting a game developer's check**.

---

# Part A: Cases

## Case 1: Movement on the wrong clock
*Chapter 1, Walker and Godot*

**The flaw.** The hero moves and collides inside `_process`, which runs once per rendered frame at a variable rate, instead of `_physics_process`, the fixed-rate tick physics uses, so on slow machines steps get large and the hero can sink into floors or tunnel through thin colliders; scaling by delta fixes distance per second but not collision.

**Terms that earn the Exact-term credit**
- **Full credit (2):** `_physics_process` / physics tick / fixed timestep, with the explanation that collision needs fixed steps; "tunnelling" used correctly.
- **Half credit (1):** "should use the physics callback" with no reason; "frame-rate independence" alone (the agent claimed it, so naming it only repeats the claim); "delta is wrong".
- **No credit:** "needs a higher frame rate", "gravity too weak", "should cap the FPS".

**Acceptable evidence requests**
1. "Run the headless movement test with a deliberately slowed frame rate (e.g. 15 and 144 FPS) and show the hero stays on the floor and cannot pass through the 4-pixel ledge at both."
2. "Move the logic into `_physics_process`, run the existing floor and ledge checks with `--fixed-fps` pinned at two values, and show matching positions after 2 seconds."

**Unacceptable:** "Look at the code again", "run the game on my laptop and see", "verified by reasoning" repeated.

**One strong sample answer.** Q1: "Movement and collision are in `_process`, which runs at the frame rate. They belong in `_physics_process`, the fixed timestep. At low FPS each step is big enough to sink into the floor or tunnel through a thin ledge; delta only fixes speed, not contact." Q2: "Run the floor and ledge test at 15 and 144 FPS and show no sinking or passing through." Q3: "Move velocity and `move_and_slide` into `_physics_process`, keep gravity there, and remove the `* 60.0`. Re-run the test at two frame rates." Q4: "The game checks for walls only once per picture, and on slow laptops pictures come far apart, so the hero can jump into the floor between checks, which is why the fix has to be about how often the game checks." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct, but Q4 is one long sentence a designer would not follow.*

---

## Case 2: The checkpoint post that was "2 metres"
*Chapter 3, 3D assets and the Blender pipeline*

**The flaw.** The post's 2 m height comes from an object scale of 4 stretched over a 0.5 m mesh (the transform was not applied), while the collision hull has scale 1 and is only 0.5 m tall, so the visual mesh and the collider disagree and "confirmed" rested on the wrong number.

**Terms that earn the Exact-term credit**
- **Full credit (2):** apply transforms / scale left on the object (node scale) vs real mesh size; collision shape not matching the visual mesh.
- **Half credit (1):** "units are wrong", "scale problem", "axis problem", "collider too small" with no link to the unapplied transform.
- **No credit:** "poly count", "wrong file format", "export setting".

**Acceptable evidence requests**
1. "Apply all transforms in Blender, re-export, and report the mesh bounding box and the collision shape size in Godot from a headless script; both must be 0.4 x 0.4 x 2.0 m with node scale (1,1,1)."
2. "Print the node scale and the collision-shape extents for the post and hull in Godot; show they match within 1 cm."

**Unacceptable:** "Open it in Godot and look", "confirm in Blender again", "check the polygon count".

**One strong sample answer.** Q1: "The scale of 4 on Z was left on the object instead of applying transforms, so the mesh is really 0.5 m tall and the 2 m comes only from stretching. The hull is a true 0.5 m with scale 1, so the collider does not match the visual mesh." Q2: "Print the node scale and mesh/collider extents in Godot; they should both be 2 m with scale 1." Q3: "In Blender, apply transforms to both objects, re-export, then show the post and hull extents in Godot." Q4: "The post looks tall but the invisible wall around it is only a quarter as tall and in the wrong place, so the player meets the wall, not the post." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 misstates where the hull is ("wrong place").*

---

## Case 3: The checkpoint that "activates quickly"
*Chapter 5, The GDD and virtual worlds*

**The flaw.** The criterion ("quickly", "responsive") has no number or tolerance so nothing can fail it, and the test teleports the player onto the pad (a direct state write) instead of making the player walk in, so it skips the very contact the pad depends on and passes whatever the pad does.

**Terms that earn the Exact-term credit**
- **Full credit (2):** acceptance criterion that is measurable / checkable / has a tolerance; direct state write / teleport instead of scripted input; false pass; given-when-then.
- **Half credit (1):** "criterion is vague", "test is too simple", "not realistic", with no further term.
- **No credit:** "needs more tests", "the pad should be bigger", "use a different node".

**Acceptable evidence requests**
1. "Rewrite the criterion as: given the player on the ground 3 m from the pad, when scripted input walks onto it, then `pad.is_active` is true within 0.2 s (12 physics ticks); run it and show both the pass and a failing run with the pad moved away."
2. "Run the test with scripted input, not a position write, and show it fails if the pad's collision shape is deleted."

**Unacceptable:** "play it and see if it feels responsive", "add more asserts", "make the test longer".

**One strong sample answer.** Q1: "The criterion has no tolerance, so nothing can fail it; 'quickly' needs a number. The test teleports the player by setting position, a direct state write, so it never uses real contact and is a false pass." Q2: "Given-when-then: given the player 3 m away, when scripted input walks in, then the pad is active within 12 ticks. Show it fails when the collision shape is removed." Q3: "Rewrite the criterion with the number, drive the player by scripted input, and add a negative case." Q4: "The test put the player on the pad by magic instead of walking, so it never tested walking." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; "by magic" is not a plain reason players failed.*

---

## Case 4: The hull that turned to plastic
*Chapter 7, Materials and textures*

**The flaw.** The roughness map is data, not colour, but it was imported with the sRGB (colour) setting on, so its values are decoded as if they were colours and the roughness the shader reads is wrong (typically too low, so too shiny); the agent's checks only proved that the slots were filled.

**Terms that earn the Exact-term credit**
- **Full credit (2):** data texture vs colour texture; sRGB-to-linear decode / sRGB flag should be off for roughness (linear); import settings.
- **Half credit (1):** "wrong import setting", "texture compression", "texture is not linear" with no data/colour reasoning.
- **No credit:** "needs a normal map", "increase roughness to 1", "polygon count", "lighting is too bright" (this repeats the agent's excuse).

**Acceptable evidence requests**
1. "Report the import colour-space setting for each map and show that albedo is sRGB and roughness is linear; then render the hull under a fixed light before and after and show the highlight is broader."
2. "Read back the roughness value at three known pixels of hull_rough.png in the engine and compare to the file; they should match."

**Unacceptable:** "check the slots are filled" (already claimed), "view it in the editor", "try other lights".

**One strong sample answer.** Q1: "Roughness is a data texture, but the agent left sRGB on, so its numbers were decoded as colour, giving wrong roughness. It also accepted 'lights' as the cause without evidence." Q2: "Report each map's import setting: albedo sRGB, roughness linear, then render under a fixed light." Q3: "Turn off sRGB on hull_rough.png (import as linear/data), re-import, and show the before and after render." Q4: "The map that says how rough each spot is got read as a picture instead of numbers, so the wood came out too shiny." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 never says what Lin should expect to see after the fix.*

---

## Case 5: The death burst nobody sees
*Chapter 9, Particle effects*

**The flaw.** The burst is a child of the creep, and `queue_free()` removes the creep and its children in the same frame, so the particles are deleted before they are drawn; the test only checked the emitter's settings (state), not that particles live on screen (visual intent).

**Terms that earn the Exact-term credit**
- **Full credit (2):** parenting (attach the effect to something that outlives the creep, e.g. the level, in world coordinates); node lifetime; state vs visual intent.
- **Half credit (1):** "the node is freed", "queue_free is the problem", "effect is deleted", with no parenting or lifetime reasoning.
- **No credit:** "too few particles", "lifetime too short", "needs a GPU particle shader", "CPU vs GPU".

**Acceptable evidence requests**
1. "In a headless test, kill a creep, step 10 physics ticks, then count live particle nodes in the scene tree and require at least 1 burst node with emitting or particles alive; fail if there are none."
2. "Report the burst node's parent and show it is not the freed creep; then a screenshot 0.1 s after the death showing sparks."

**Unacceptable:** "Check amount is 24" (already tested), "run the test again", "make the burst longer".

**One strong sample answer.** Q1: "The Burst is parented to the creep, which is freed on the next line, so the effect is deleted with it. This is a parenting and node-lifetime error. The test checked the emitter's properties (state), not that sparks appear." Q2: "Kill a creep, step ten ticks, and require a live burst node in the tree." Q3: "Make the burst its own scene instead of a child of the creep." Q4: "The sparks were stuck to the creep, and when the creep vanished they vanished too." *Catches 3, Term 2, Evidence 2, Fix 1, Scope 1.* Total 9. *Reason: all correct, but the fix does not say where the new scene goes or when it is freed.*

---

## Case 6: Walk and run as two states
*Chapter 11, Animation and interaction*

**The flaw.** Continuous input (how hard the stick is pushed) needs a blend space (blend tree) that mixes walk and run clips by the speed parameter, but the agent used discrete states with a threshold, so the pose jumps at the threshold; the test checked the order of states, not smoothness.

**Terms that earn the Exact-term credit**
- **Full credit (2):** blend space / blend tree driven by a parameter (speed); state machine vs blend space; threshold.
- **Half credit (1):** "should blend instead", "needs smoothing", "cross-fade is too short".
- **No credit:** "needs a longer cross-fade" as the only fix; "root motion"; "needs IK".

**Acceptable evidence requests**
1. "Ramp speed from 0 to 6 in small steps and print the blend weights or the bone pose each step; the pose must change a little each step with no jump larger than a set limit."
2. "Sample the pose at speed 3.9, 4.0 and 4.1 and show the difference between consecutive samples is small."

**Unacceptable:** "Check the state sequence again" (already claimed), "watch it", "make the cross-fade longer and test".

**One strong sample answer.** Q1: "The agent used separate walk and run states with a threshold. Smooth control by stick pressure needs a blend space driven by speed. At 4.0 the state flips and the pose snaps; the cross-fade only softens it. The test checked state order, not smoothness." Q2: "Sample the pose at 3.9, 4.0 and 4.1 and show consecutive samples differ little." Q3: "Put walk and run into a one-dimensional blend space driven by speed, inside a locomotion state, and keep the state machine for idle and jump. Re-run the sampling." Q4: "It switches from one animation to another at a line instead of mixing them gradually, so the change is sudden." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 does not mention the stick.*

---

## Case 7: The guard that cannot decide
*Chapter 14, Game AI and systems*

**The flaw.** Both transitions use the same 200 px threshold, so a player hovering near 200 px flips the guard between states every tick (flicker) and the fix is hysteresis (a larger distance to stop chasing than to start); the test only checked 150 px and 250 px, far from the boundary.

**Terms that earn the Exact-term credit**
- **Full credit (2):** hysteresis (different thresholds to enter and leave); flicker; boundary / edge case near the threshold.
- **Half credit (1):** "needs a delay", "a cooldown", "the guard switches too fast", "needs smoothing".
- **No credit:** "use A*", "use a behavior tree" as the only answer, "increase sight range", "navigation mesh".

**Acceptable evidence requests**
1. "Move the player slowly back and forth across 190 to 210 px for 100 ticks and count state changes; require at most 1 or 2 changes, not one per tick."
2. "Test the boundary: player at 199, 200 and 201 px, and a path that wobbles around 200; report the state each tick."

**Unacceptable:** "Test at 100 px and 300 px" (already done), "play it", "run the same test twice".

**One strong sample answer.** Q1: "Both transitions use one threshold, 200 px, so near the edge the guard flickers between chase and patrol. It needs hysteresis. The tests used 150 and 250 px, far from the boundary." Q2: "Move the player back and forth across 190 to 210 px for 100 ticks and count state changes." Q3: "Start chasing under 200 px but only return to patrol past 260 px, and add a boundary test that counts changes." Q4: "The guard has one line for 'I see you' and the same one for 'I lost you', so it flips back and forth at the line." *Catches 3, Term 2, Evidence 2, Fix 2, Scope 0.* Total 9. *Reason: all correct; Q4 uses "line" without saying what the line is.*

---

# Part B: Multiple-answer questions

T = true (should be checked), F = false (should be blank).

**1.** (`MA-ch02.1`, None)

- A = T: A 32 by 48 image has a resolution of 32 by 48 pixels.
- B = F: The two words name different things.
- C = T: A sprite is a drawn 2D object.
- D = F: Aspect ratio is the proportion of width to height.
- E = T: Texture names the image data and sprite names the thing drawn from it.

**2.** (`MA-ch05.1`, None)

- A = F: A pillar is a short statement of the intended experience, not a feature.
- B = F: A GDD describes intended behaviour; code is the implementation.
- C = F: A GDD is revised as prototypes and playtests teach the team; an unrevised one becomes stale.
- D = T: The brief is the compact form; the GDD is the detailed one.
- E = T: A GDD is the detailed shared description of intended behaviour.

**3.** (`MA-ch07.1`, None)

- A = T: Albedo is the intrinsic diffuse colour, and the renderer applies lighting on top of it.
- B = T: A metal has little diffuse colour, so its base colour supplies the tint of its reflections.
- C = F: Blur of reflections is set by roughness, not albedo.
- D = T: Baked lighting is shading precomputed into the image, so it stacks with runtime lighting and looks double-shaded.
- E = F: The on-screen colour also depends on light colour, light direction, shadows and reflections.

**4.** (`MA-ch10.1`, None)

- A = F: An image holds pixels only; order, timing and looping come from animation data that refers to it.
- B = F: A sprite sheet's cells are poses to play in sequence, whereas a tilemap's tiles build a level.
- C = T: An atlas is a general packing of many images with a lookup table.
- D = T: A sprite sheet stores the poses of an animation in one image, and playing them in sequence is frame-by-frame animation.
- E = F: A tilemap places reusable tiles on a level grid; poses to play in sequence belong to a sprite sheet.

**5.** (`MA-ch12.1`, None)

- A = T: Attenuation, also called falloff, is the distance-dependent loss of level.
- B = F: A menu click has no place in the world, and a positional player would change its level and pan with the camera.
- C = T: A positional sound is heard relative to a listener, which Godot takes from the current camera unless told otherwise.
- D = F: The listener is the receiver (the ears), and one is active at a time.
- E = T: A non-positional player ignores listener position, which suits music and interface sounds.

**6.** (`MA-ch14.1`, None)

- A = T: A finite state machine has states and one current state at a time.
- B = T: Transitions are the rules that connect states.
- C = F: Ordered children ticked from a root describe a behavior tree.
- D = T: A missing or unreachable exit leaves the NPC stuck in that state.
- E = F: An FSM has one current state, so blending needs a different design.

