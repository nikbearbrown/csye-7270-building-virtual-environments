# Chapter 8: Shader verification

## MA-ch08.1

A coding agent reports: "Done. The shader compiles with no errors and the existing automated tests pass." Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The agent's reply is a claim, and the compile log is evidence of valid syntax rather than of correct output.
- [ ] B. Existing tests that pass before and after a change show that nothing is drawn differently.
- [ ] C. A clean compile shows that the output matches the intended look.
- [ ] D. A shader that multiplies a colour by the wrong factor still compiles.
- [ ] E. A compile error means the source was rejected, while a visual bug means it built and ran but drew a wrong result.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: A claim is a statement, and evidence is something observed that supports it.
- B: Tests cover only what they check, and drawing may be outside them.
- C: A compiler checks syntax and types, not the design.
- D: A wrong formula is valid code, so it compiles.
- E: Compile errors and visual bugs are different failure types caught at different stages.

**Source:** Compile error versus visual bug; claim versus evidence

## MA-ch08.2

A continuous-integration machine has no graphics card. It runs the engine in headless mode with a dummy display driver, or alternatively with a software renderer that draws on the CPU. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A headless run with no errors shows that the shader's output colours are correct.
- [ ] B. A frame time on the software renderer predicts the frame time on players' graphics cards.
- [ ] C. A headless run can check game logic that feeds a shader, such as the value a script writes to a shader parameter.
- [ ] D. A software renderer produces an image, which can be used to check colours.
- [ ] E. A software renderer's image can differ from a real GPU's in precision or filtering.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Headless mode draws no pixels, so colours are never produced.
- B: A CPU rasteriser has a different cost profile than a GPU.
- C: Logic runs without a display, so parameters can be inspected.
- D: A software renderer does rasterise to an image.
- E: Precision and filtering are implementation details that vary between renderers.

**Source:** Headless versus software rendering

## MA-ch08.3

A team verifies a shader change with a golden-image test: a fixed scene is rendered, captured and compared with an approved reference image, using a per-channel tolerance and a limit on the fraction of different pixels. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A reference image captured from a buggy build and approved without anyone looking still lets the test report the bug.
- [ ] B. A wrong-coloured region that is small enough to stay under the allowed fraction of different pixels passes the test.
- [ ] C. A pass on a scene that does not draw the changed part shows that the change is correct.
- [ ] D. A golden image is an approved capture that later captures are compared against.
- [ ] E. A per-channel tolerance prevents tiny rounding differences from failing the test, and also hides very small real colour shifts.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: The test only reports differences from the reference, so an approved bug is baked in.
- B: The pixel-fraction threshold lets small defects pass.
- C: A scene that never exercises the change says nothing about it.
- D: Golden image and reference image are the same idea.
- E: Tolerance trades sensitivity for stability.

**Source:** Golden-image comparison

## MA-ch08.4

An agent rewrote a shader that tints a sprite when the character is damaged and says: "Verified, it works." The developer wants evidence rather than a claim. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Rendering a fixed test scene at tint amounts 0, 0.5 and 1 and comparing pixel values with the specification's predictions is evidence.
- [ ] B. Asking the agent to restate how sure it is gives more evidence.
- [ ] C. A comment in the shader saying it was verified is evidence.
- [ ] D. A compile log is evidence of valid syntax, not of correct output.
- [ ] E. Asking which statements were observed in a run and which were inferred from reading the code separates evidence from claim.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: A controlled input with measured output compared with a specification is an observation.
- B: Restating confidence repeats the claim.
- C: A comment is another claim.
- D: Compiling shows the source parses, nothing more.
- E: Observed and inferred are different kinds of support.

**Source:** Evidence versus a claim of success

## MA-ch08.5

Shader code works with positions in several coordinate spaces. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. View space (also called camera or eye space) measures positions relative to the camera.
- [ ] B. After the camera is moved without rotation, a point's view-space position still differs from its world-space position.
- [ ] C. World space is relative to the camera.
- [ ] D. Screen space is the same as texture coordinates (UV), so a screen position can be read as a UV.
- [ ] E. Local space (also called object or model space) measures positions from the object's own origin and axes.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: In view space the camera is the origin.
- B: Moving the camera shifts every view-space position.
- C: World space is the frame shared by the scene; view space is relative to the camera.
- D: Screen space is a position on the display, while UV is a position on the mesh's surface image.
- E: A vertex keeps its local position when the object moves or rotates.

**Source:** Coordinate spaces

## MA-ch08.6

A coding agent writes a fragment shader for a flood line: surfaces below world height 0.5 are drawn darker. The agent takes height from the vertex position as the mesh stores it and compares it with 0.5, with no transformation. A crate stands at world height 10. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The shader compares a local-space height with a world-space level, which mixes two coordinate spaces.
- [ ] B. Moving the one crate to world height 0 makes the effect correct for the props across the level.
- [ ] C. View space gives a fixed flood line because it does not depend on the camera.
- [ ] D. If the crate is turned upside down, the dark band ends up at its top in the world, because local heights turn with the object.
- [ ] E. The fix is to transform the position by the model matrix into world space before the comparison.

**Key:** A=T B=F C=F D=T E=T

**Why:**

- A: Stored vertex positions are in local space, and the flood line is a world quantity.
- B: One crate at one spot does not fix the mixing of spaces.
- C: View space moves with the camera, so the line would move too.
- D: Local coordinates are attached to the object and rotate with it.
- E: The model matrix takes a local position to world space.

**Source:** Mixing coordinate spaces

## MA-ch08.7

A surface has a tangent t and a normal n that are perpendicular. The object is then scaled non-uniformly, for example four times taller only. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Normalizing a normal after the model matrix repairs its direction under non-uniform scale.
- [ ] B. The model matrix gives correct normals under a non-uniform scale, so the inverse transpose can be skipped.
- [ ] C. For a rotation or a uniform scale, applying the model matrix and then normalizing gives a normal with the right direction.
- [ ] D. Carrying the normal through the inverse transpose of the model matrix keeps it perpendicular to the surface.
- [ ] E. Carrying the normal through the model matrix can leave it not perpendicular to the transformed tangent.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Normalizing fixes length, not direction.
- B: The model matrix only works for normals when the scale is uniform.
- C: Rotation and uniform scale preserve angles, so only length changes.
- D: The inverse transpose (the normal matrix) is the transform that preserves perpendicularity.
- E: Non-uniform scale distorts directions of normals differently than surface directions.

**Source:** Normals and non-uniform scale

## MA-ch08.8

Shading languages offer full precision (32-bit float) and half precision (16-bit float). Half-precision values are spaced coarser as the magnitude grows. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Half precision is fine for world positions in the thousands of units, because its range is large.
- [ ] B. A half-precision variable can hold the value 3001 exactly.
- [ ] C. Half precision loses fine detail on large values, because the gap between neighbouring representable values grows with magnitude.
- [ ] D. Half precision is a routine speed-up that needs no comparison of the picture afterwards.
- [ ] E. Half precision is usually adequate for colours between 0 and 1.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Range is not the issue; spacing between values at that size is coarse.
- B: Above 2048 the spacing is larger than 1, so 3001 is not representable.
- C: Floating-point spacing scales with magnitude.
- D: Reduced precision changes results, so the output is compared with full precision.
- E: Small differences in colour are not visible.

**Source:** Precision: float versus half

## MA-ch08.9

A scrolling-water effect looks smooth on a desktop. On a mid-range phone, after the game runs a while, the texture moves in visible jumps. The shader keeps the texture offset (elapsed time times a speed) in a half-precision variable. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Computing the offset in full precision, or keeping the fractional part alone before storing it in half precision, is a sound fix.
- [ ] B. Raising the frame rate removes the jumps.
- [ ] C. As the offset grows, half precision can represent just coarse steps, so the motion advances in jumps.
- [ ] D. Many desktop GPUs run a half-precision request at full precision, which can hide the problem.
- [ ] E. The smooth desktop result shows the shader is correct.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: A smaller or more precise value avoids coarse steps.
- B: The cause is value spacing, not frame rate.
- C: Large values have wide spacing in half precision.
- D: Platform differences in precision can hide a bug on one device.
- E: The same source can behave differently depending on the hardware's precision.

**Source:** Precision symptoms on a phone

## MA-ch08.10

A GPU runs fragment shaders for neighbouring pixels together in lockstep groups (called warps, wavefronts or SIMD groups). A shader has an `if` whose two sides are each expensive. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A condition from a per-pixel value such as noise costs the same as a condition from a uniform.
- [ ] B. When the condition differs between pixels of a group, the `if` saves time because each pixel runs just its own side.
- [ ] C. A condition from a uniform is constant across the draw, so pixels in a group agree.
- [ ] D. When the group agrees on the condition, it can run just the side taken.
- [ ] E. When pixels of a group disagree, the hardware runs both sides with the non-participating pixels switched off, which is called divergence.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Per-pixel conditions can diverge, uniform ones do not.
- B: With divergence the group pays for both sides.
- C: A uniform has one value for the whole draw.
- D: Uniform agreement lets the hardware skip the other side.
- E: Divergence is the term for lockstep pixels disagreeing about a branch.

**Source:** Branching and divergence

## MA-ch08.11

A shader declares a uniform `flash_amount` with a default of 0.0. A script sets it to 1.0 on one enemy when that enemy is hit. In play, all enemies, which share a single material, flash at once. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A uniform is a value that varies per pixel within a draw.
- [ ] B. The declared default is the value each object has until something overrides it.
- [ ] C. A material is a shared asset, so objects referencing it see a change to its parameter.
- [ ] D. A per-instance parameter (Godot instance uniforms, Unity material property blocks) limits the flash to the enemy hit.
- [ ] E. The problem is a shader compile error that was reported when the shader loaded.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A uniform is constant across a draw call; a varying differs per pixel.
- B: The default is the starting value.
- C: Shared resources propagate changes to every reference.
- D: Per-instance parameters are stored per object.
- E: The shader compiled fine; the cause is sharing.

**Source:** Uniforms, defaults and shared materials

## MA-ch08.12

A damage flash fades over 33 frames, counted by adding 1 to an integer once per rendered frame. The design says the fade lasts 0.55 seconds. The developer checked it only at 60 frames per second. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A frame counter and game time agree at the frame rate the count was calibrated for.
- [ ] B. Passing at 60 frames per second shows the fade is independent of frame rate.
- [ ] C. Driving the fade from elapsed game time, the sum of each frame's delta time, makes its length independent of frame rate.
- [ ] D. At a higher frame rate, a fade counted in frames lasts longer.
- [ ] E. A fade counted in rendered frames lasts longer when the frame rate drops.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: At 60 frames per second, 33 frames is 0.55 seconds.
- B: One setting does not show independence.
- C: Game time uses delta time, which tracks real elapsed time.
- D: More frames per second finish the count sooner.
- E: Fewer frames per second means each frame takes longer.

**Source:** Frame count versus game time

## MA-ch08.13

An agent writes a new automated check for a shader and runs it on the changed code. It passes and the agent says the change is verified. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A check becomes evidence once it fails on a known-bad version and passes on a known-good one.
- [ ] B. A check that fails on a known-good version is a false alarm, and the check needs fixing.
- [ ] C. A check that passes on both the known-bad and known-good versions supports the change under review.
- [ ] D. Running the same check again on the same changed code adds confidence that the check detects the bug.
- [ ] E. A check written by the same agent as the change confirms the change independently of the agent's assumptions.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: Testing the test shows it can tell good from bad.
- B: A failure on good code is a false positive and points to the check.
- C: A check that cannot tell them apart carries no information (a false negative).
- D: Repeating gives the same result and does not test the check.
- E: Shared assumptions can produce a check that repeats the same mistake.

**Source:** Testing the test

## MA-ch08.14

A shader moves a colour from a base colour toward a flash colour by an amount between 0 and 1, with output = base + (flash − base) × amount. The agent's shader has a mistake in the formula, yet the agent's test passes. A test oracle is what a test compares a result against. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An oracle written from the specification stays valid when the shader is rewritten.
- [ ] B. An oracle written from the specification would have caught the mistake.
- [ ] C. The formula is a linear interpolation, called mix in the Godot shading language and lerp in Unity's shader language.
- [ ] D. A CPU calculation of the specification replaces looking at what the GPU drew.
- [ ] E. An oracle copied from the code under test is preferable, because it follows changes to the code.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: A specification does not depend on the implementation.
- B: An oracle independent of the code can disagree with it.
- C: Mix and lerp are the shader-language names for linear interpolation.
- D: The CPU result is a prediction; the drawn image still needs checking.
- E: A copied formula repeats the mistake, so the test is circular.

**Source:** Specification oracle and interpolation

## MA-ch08.15

A game renders at 1920 by 1080. After the scene is drawn, three full-screen translucent layers are drawn on top: fog, a damage vignette and a colour grade. Each layer runs a fragment shader per pixel it covers. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Doubling the resolution in each dimension doubles the fragment shader invocations.
- [ ] B. A layer's cost depends mainly on its triangle count.
- [ ] C. Three full-screen layers run the fragment shader about three times per pixel, which is overdraw.
- [ ] D. A value that varies linearly across a surface is cheaper computed per vertex and interpolated when fragments outnumber vertices.
- [ ] E. Combining the three effects into one full-screen pass shades each pixel once.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Doubling both dimensions multiplies pixels by four.
- B: Cost follows how many pixels are shaded, not triangles.
- C: Overdraw means shading the same pixel more than once.
- D: Fewer vertex invocations do the same job when interpolation is exact.
- E: One pass merges the work, though each shader does more.

**Source:** Fragment cost and overdraw

## MA-ch08.16

A developer prepares controlled inputs, test values chosen so correct and wrong outputs are far apart. Two suspected mistakes are alpha applied twice and a flipped vertical texture coordinate. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A test texture that is red on top and blue on the bottom exposes a vertical flip.
- [ ] B. A texture that is symmetric top to bottom is as good as an asymmetric one for exposing a flip.
- [ ] C. A vertical flip swaps left and right as well as top and bottom.
- [ ] D. A fully opaque test pixel is the best input for exposing alpha applied twice.
- [ ] E. A shader that multiplies colour by alpha and is drawn with ordinary alpha blending applies alpha twice.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Different top and bottom make a swap visible.
- B: A symmetric texture looks the same when flipped.
- C: A vertical flip swaps top and bottom only; a 180 degree rotation swaps both.
- D: At alpha 1.0 doubling alpha changes nothing, so the bug stays hidden.
- E: Premultiplying and then blending applies the factor two times.

**Source:** Controlled inputs for common shader mistakes

## MA-ch08.17

A developer gives a coding agent a specification for a character's hit flash that can be checked on a device with any frame rate. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Stating that at amount 0 the output equals the incoming colour and at 1 equals the flash colour defines the end points of a linear mix.
- [ ] B. "A strong red" is vague, and a precise spec names the flash colour as exact RGB values.
- [ ] C. "Returns to normal" is a precise end condition that a test can check.
- [ ] D. Giving the fade length as a count of rendered frames fixes its length in real time.
- [ ] E. Giving the fade length in seconds of game time keeps its length the same at different frame rates.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: End points plus linear mix fully pin down the rule.
- B: Exact values can be compared with measured pixels.
- C: "Normal" is not a measurable value; the end value should be stated.
- D: A frame count changes length when the frame rate changes.
- E: Game time follows delta time, so it does not depend on frames.

**Source:** A precise specification for an agent

## MA-ch08.18

A reviewer asks for evidence about a shader change and lists kinds of checks. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A headless run is the strongest evidence of how the shader looks.
- [ ] B. A golden-image comparison detects colour changes but does not judge whether the reference was right.
- [ ] C. A run on the target phone is evidence about that phone's precision and driver behaviour.
- [ ] D. Passing existing tests shows the shader draws correctly.
- [ ] E. A compile check is the weakest evidence, showing valid syntax and types.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A headless run draws nothing.
- B: A golden image only compares with an approved reference.
- C: Hardware-specific behaviour needs the actual hardware.
- D: Existing tests may not exercise the shader.
- E: A compile check says nothing about the output.

**Source:** Ladder of evidence

## MA-ch08.19

A developer tells a coding agent: "Add a damage flash to the player and make sure it works." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "A bit red" is acceptable as the flash colour.
- [ ] B. Saying "alpha unchanged" states what the output's transparency does.
- [ ] C. "Make sure it works" gives no pass criterion that a test can check.
- [ ] D. A precise rewrite names a uniform with a stated range, such as 0 to 1.
- [ ] E. "Flash" is precise, because it names the effect.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A vague colour cannot be checked against pixels.
- B: It states one part of the output rule.
- C: A pass criterion needs measurable values.
- D: A named uniform with a range is a testable input.
- E: Flash leaves colour, timing and blend rule open.

**Source:** Rewriting a vague shader prompt

## MA-ch08.20

An agent adds a test for a fade effect by recomputing the expected value with the formula copied from the shader. The test passes on a change containing a real bug. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Varying inputs such as frame rate and amount exposes hidden dependences.
- [ ] B. A copied formula gives an independent oracle.
- [ ] C. A check at a single frame rate can mislead, because behaviour may depend on frame rate.
- [ ] D. A test oracle is what a test compares a result against.
- [ ] E. A check that passes on a known-bad version shows the check is trustworthy.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Several settings test more of the behaviour.
- B: A copied formula repeats the shader's mistake.
- C: One setting can hide a frame-dependent bug.
- D: The oracle is the source of the expected value.
- E: Passing on bad code means the check cannot tell good from bad.

**Source:** Oracles and single-setting checks

## MA-ch08.21

A tester finds a bug caused by mixing two coordinate spaces in a shader. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Local space is relative to the object's origin.
- [ ] B. Screen space uses the mesh's own origin.
- [ ] C. World space is shared by the scene.
- [ ] D. View space has its origin at the world origin.
- [ ] E. A symptom of mixing spaces often changes when the object or camera moves.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: Local space belongs to the object.
- B: Screen space is a position on the display, usually in pixels.
- C: All objects in the scene share world space.
- D: View space has the camera at the origin.
- E: The mixed quantity depends on a transform that changes with movement.

**Source:** Four spaces and mixing them up

## MA-ch08.22

A shader looks right and runs smoothly on a desktop, but on a mid-range phone it shows stepping and the frame rate drops. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Desktop frame time predicts phone frame time because the shader code is the same.
- [ ] B. Half precision on the phone can cause stepping with large values such as time.
- [ ] C. Stepping on the phone is a compile error.
- [ ] D. Full-screen translucent layers multiply fragment invocations and can hurt the phone's fill rate.
- [ ] E. A divergent branch can make the phone pay for both sides.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Hardware differs in speed and precision.
- B: Reduced precision coarsens large values.
- C: A compile error would stop the shader from loading.
- D: More overdraw means more pixel work.
- E: Divergence runs both sides in a lockstep group.

**Source:** Precision, branching and fragment cost on mobile

## MA-ch08.23

A team designs a golden-image test process for a library of shaders. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Per-platform references or tolerances handle platform differences.
- [ ] B. A fixed scene has a fixed camera, resolution, inputs and pinned clock with no randomness.
- [ ] C. A pass shows the shader is correct on hardware that was not tested.
- [ ] D. A pass shows the render matches the approved reference, not that the reference is right.
- [ ] E. One reference image from a desktop GPU is adequate for phone GPUs.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Each platform gets its own reference or tolerance.
- B: Determinism makes any difference come from the shader.
- C: A pass says nothing about untested hardware.
- D: A golden image compares, and a person approves the reference.
- E: Different hardware gives slightly different images.

**Source:** Golden-image test process
