# Jargon test: reading agent output

## MA-k02.1

An agent reports: "Made the jump frame-rate independent by multiplying the jump impulse by delta." The jump is a single upward impulse applied at takeoff. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The claim is wrong: an impulse applied once is not a per-second rate, so scaling it by delta makes the jump weaker and still dependent on frame rate.
- [ ] B. The frame-rate dependent part of a jump is usually gravity, which is scaled by delta when it changes the vertical velocity.
- [ ] C. A follow-up that turns the claim into evidence is: run the jump at 30 and 144 frames per second and report the apex height for each.
- [ ] D. The corrected code sets the jump as a one-time velocity change such as velocity.y = jump_velocity, with no delta factor.
- [ ] E. A follow-up that turns the claim into evidence is: ask the agent to explain in words why the change is correct.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: A one-time velocity change has no per-second unit, so multiplying by the varying delta only makes the jump height fluctuate with frame time.
- B: Gravity is an acceleration in units per second squared, so each frame adds gravity times delta to the vertical velocity.
- C: Comparing apex height at two frame rates directly measures frame-rate independence, and matching heights would confirm the fix.
- D: A single velocity assignment at takeoff is the same at any frame rate, so delta does not belong in it.
- E: An explanation is more claim, not a measurement, so a jump that still varies with frame rate would pass unnoticed.

**Source:** Delta, impulse, frame-rate independence

## MA-k02.2

An agent reports: "Fixed the wall clipping by moving the movement code from _physics_process to _process so it updates more often." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The reasoning is right, because more frequent updates mean smaller steps and so the clipping goes away.
- [ ] B. A follow-up that gives evidence is: confirm the code now runs in _process and that the project still compiles.
- [ ] C. A follow-up that gives evidence is: replay the same fast move into the thin wall 100 times and report how many times the body passed through.
- [ ] D. The reasoning is wrong: _process follows the display, so its delta varies, while physics-based movement is meant to run on the fixed physics tick.
- [ ] E. Clipping through thin walls is better addressed with continuous collision detection or a limit on how far a body moves per step.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: _process does not add physics steps, and its delta is irregular, so the body can still jump past thin colliders.
- B: Compiling and running in _process say nothing about whether the body still passes through walls, so the bad claim would be accepted.
- C: A repeated identical test gives a pass-through count that can be compared before and after the change.
- D: Collision handling is tuned to the fixed physics step, and a variable display delta makes per-step distances uneven and unpredictable.
- E: Both options check or restrict the path travelled in a step, which is what stops a fast body from skipping a thin collider.

**Source:** _process versus _physics_process, tunnelling

## MA-k02.3

An agent reports: "Added coyote time. The player can now jump when is_on_floor() is true." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The claim is right, since checking is_on_floor() before jumping is what coyote time means.
- [ ] B. A follow-up that gives evidence is: simulate a jump press 0.05 s after leaving a ledge and report whether the jump happened.
- [ ] C. A follow-up that gives evidence is: confirm is_on_floor() returns true while standing and that the jump works there.
- [ ] D. A correct implementation stores a timer that starts when the character leaves the floor without jumping, and allows the jump while the timer is above zero.
- [ ] E. The claim is wrong: is_on_floor() being true is ordinary jumping; coyote time lets a jump work for a short window after is_on_floor() turns false.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: That check was already how normal jumping worked, so accepting the claim would ship a feature that was never built.
- B: A press just after leaving the floor is exactly the case coyote time must allow, so the result shows whether it works.
- C: Jumping while grounded worked before the change, so this check passes whether or not coyote time exists.
- D: The timer creates the grace window, and it must start only on walking off, not on jumping, or double jumps appear.
- E: Jumping while grounded already worked before, so the claim describes no new behaviour; the feature is the grace window after leaving a ledge.

**Source:** Coyote time

## MA-k02.4

An agent reports: "Added jump buffering: jump_pressed is set to true when the button is pressed and stays true until the player lands." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The implementation is correct, because it remembers the press until the character lands.
- [ ] B. A follow-up that gives evidence is: press jump 0.05 s before landing and then 1 s before landing, and report which of the two jumps on landing.
- [ ] C. A correct version records the time of the press, or runs a short timer, and clears the flag when it expires.
- [ ] D. A follow-up that gives evidence is: ask the agent to rename the flag to jump_buffer.
- [ ] E. The implementation lacks an expiry, so a press made long before landing still causes a jump on landing.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Remembering indefinitely is the bug, since a stale press fires an unwanted jump instead of a forgiving short buffer.
- B: A correct buffer jumps for the near press and ignores the early one, so the two cases expose a missing expiry.
- C: Expiry limits the buffer to a fraction of a second, so only presses just before landing count.
- D: Renaming changes the label but not the missing expiry, so a flag that persists would still be accepted.
- E: A buffer should be a short window; a flag that persists until landing turns an early press into a surprise jump seconds later.

**Source:** Jump buffer

## MA-k02.5

An agent reports: "Fixed the coin pickup by setting the coin's collision layer to 1 so it overlaps the player." The coin is an Area2D and the player is on layer 1. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The change may have side effects, since other things whose masks include layer 1 will now see the coin as part of the player's layer.
- [ ] B. The fix is right because the coin must be on the same layer as the player to touch it.
- [ ] C. The fix targets the wrong property: the coin detects the player through its collision mask, not its collision layer.
- [ ] D. A follow-up that gives evidence is: print the coin's layer and mask values and run the pickup, reporting whether body_entered fired.
- [ ] E. A follow-up that gives evidence is: ask the agent to re-read the coin's scene file.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Layer membership has consequences: enemies or walls that scan layer 1 may now react to the coin.
- B: Detection depends on one object's mask matching the other's layer, so objects do not need to share a layer.
- C: An Area2D detects bodies whose layer appears in its own mask, so changing the coin's layer does not help it see the player.
- D: The printed values show the actual setup, and the signal result shows whether the pickup works in play.
- E: Rereading the file reports the same settings but runs nothing, so a pickup that still fails would go unnoticed.

**Source:** Collision layer versus mask

## MA-k02.6

An agent reports: "Smoothed the camera with lerp(position, target, 0.1) each frame. It's now frame-rate independent." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A delta-aware weight, such as 1 minus exp(-k times delta), makes the catch-up depend on time rather than frames.
- [ ] B. A follow-up that gives evidence is: record how long the camera takes to close half the gap at 30 and at 144 frames per second.
- [ ] C. The claim is wrong because lerp is not suited to cameras.
- [ ] D. The claim is wrong: a fixed weight applied per frame catches up faster at higher frame rates.
- [ ] E. The claim is right because lerp is a time-based function.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: The exponential form gives the same smoothing per second at any frame rate, because delta enters the weight directly.
- B: Equal half-gap times at both frame rates would show true independence; a difference exposes the per-frame weight.
- C: lerp works fine for camera smoothing; the defect is the per-frame weight, so dropping lerp would not address the actual claim.
- D: A weight of 0.1 closes ten percent of the gap per frame, so more frames per second means faster catch-up.
- E: lerp interpolates by a weight between zero and one, not by elapsed time, so it ignores delta unless the weight uses it.

**Source:** Lerp and delta

## MA-k02.7

A request said: "Fix the HUD health bar. Do not modify player.gd." The agent reports: "Fixed the health bar. I also cleaned up player.gd while I was there." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: run the game and confirm the health bar updates, then accept the work.
- [ ] B. A follow-up that gives evidence is: show the diff limited to files changed and confirm player.gd is not in it.
- [ ] C. The agent went outside its scope, and the player.gd change should be reviewed or reverted before the HUD fix is accepted.
- [ ] D. Cleaning up a file keeps behaviour the same, so the report can be accepted.
- [ ] E. The player.gd edits can stay in the commit and be reviewed later.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: A working health bar does not address the scope violation, so the player.gd edits would slip through.
- B: A file-level diff directly shows whether the forbidden file was touched, so it checks the constraint.
- C: The instruction named the file as off limits, so the edit breaks an explicit constraint regardless of how small it looks.
- D: The constraint was explicit, and a claimed same-behaviour cleanup is unverified, so accepting it would let a scope violation through.
- E: The file was off limits, so keeping edits in the commit ships a violation that a later review may miss.

**Source:** Scope violation

## MA-k02.8

An agent reports: "Fixed the jump bug. While there I raised the project's physics ticks per second from 60 to 120 for smoother motion." The request was only to fix the jump bug. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The setting change should be reverted or approved separately, since the request named the jump bug alone.
- [ ] B. The change is acceptable because a higher physics rate is a smoother physics rate.
- [ ] C. The jump fix can be evaluated alone by reverting the project setting and rerunning the jump test.
- [ ] D. A follow-up that gives evidence is: list the project settings changed in the commit.
- [ ] E. Changing physics ticks per second is a project-wide setting that was not requested, and it can change every body's behaviour and the timing of all timers in physics code.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: A project-wide change outside the request needs its own review instead of riding along with an unrelated fix.
- B: Higher rates cost more CPU and can change tuned behaviour, so the change should not pass just because it sounds smoother.
- C: Reverting the extra setting isolates the requested change, so the jump result is attributable to the fix itself.
- D: A settings list reveals scope creep like the tick rate, which a gameplay test would not show.
- E: The tick rate affects how all physics code steps, so it alters tuned behaviour well beyond the jump fix.

**Source:** Scope violation

## MA-k02.9

An agent reports: "Fixed the stutter. Frame time is 40% better." No numbers, scene, or baseline were given. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A percentage improvement means little until the metric is named, such as average frame time or worst frame time.
- [ ] B. The claim can be accepted because a percentage is a precise measurement.
- [ ] C. A follow-up that gives evidence is: profile the same scene on the same machine before and after and report average and worst frame times.
- [ ] D. The claim should not be accepted yet because it has no before value, after value, scene or hardware.
- [ ] E. Worst-case frame time is useful for stutter, because an average can hide spikes.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Stutter is about spikes, so an improved average can hide an unchanged worst case.
- B: A percentage of an unstated quantity is vague, and it could describe average time, a best case or one lucky frame.
- C: Same scene, same machine and both metrics make the comparison repeatable and fair.
- D: A percentage without a baseline, scene and machine cannot be reproduced or checked, so it is not evidence.
- E: Stutter appears as occasional long frames, which show up in the worst-case figure but get diluted in the average.

**Source:** Profiling, baseline

## MA-k02.10

An agent reports: "All tests pass." The project has no test files. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A test framework such as GUT must be installed and at least one test written before a passing run means anything.
- [ ] B. The claim shows the code works, since a test run reported zero failures.
- [ ] C. The claim should be questioned, because with zero tests there is nothing that could have failed.
- [ ] D. A follow-up that gives evidence is: write one test that fails on the old code and passes on the new code.
- [ ] E. A follow-up that gives evidence is: show the command run and its full output, including the number of tests executed.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Without a framework and test cases the runner has nothing to execute, so a pass is meaningless.
- B: Zero failures from zero tests is an empty pass, so it gives no assurance about behaviour.
- C: A run that executes zero tests passes trivially, so it says nothing about whether the code works.
- D: A test that flips from fail to pass proves the change fixed the specific behaviour.
- E: The executed-test count reveals at once whether any tests actually ran.

**Source:** Evidence versus claim

## MA-k02.11

An agent reports: "Changed the enemy's knockback to a force of 500 applied once on hit." The enemy is a RigidBody2D. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: apply the knockback and report the enemy's velocity on the frame after the hit.
- [ ] B. A force applied once is the same thing as an impulse, so the claim is right.
- [ ] C. A one-time instant change in velocity is an impulse, so the term should be impulse.
- [ ] D. Calling apply_central_impulse once gives the intended one-time velocity change, scaled by the body's mass and not by step length.
- [ ] E. With a force applied for one physics step, the result depends on the step length and so is weaker than expected.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: The velocity right after the hit shows whether the push is the intended size.
- B: A force acts over a time step, so a single step gives a small push, while an impulse changes velocity instantly.
- C: Impulse is the correct physics term for a single instantaneous velocity change, and the code should use it.
- D: An impulse is applied as a velocity change divided by mass, so it behaves the same at any frame rate.
- E: A force of 500 over a short physics step yields a small velocity change, so the knockback looks feeble.

**Source:** Impulse versus force

## MA-k02.12

An agent reports: "Used move_and_collide for the player so it slides along walls." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A fix is to keep move_and_collide and raise the player's speed so the body slides along the wall.
- [ ] B. A follow-up that gives evidence is: walk the player diagonally into a wall and report whether it keeps moving along the wall.
- [ ] C. The claim is right, because collide means the body reacts to walls and so slides.
- [ ] D. A follow-up that gives evidence is: ask the agent to print the word slide in the log.
- [ ] E. The claim is wrong: move_and_collide stops at the first hit and reports it; sliding is what move_and_slide does.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Speed does not change the stopping behaviour, so the body would still halt at the wall with extra force.
- B: A diagonal approach shows sliding or stopping directly, which settles whether the claim is true.
- C: The body halts at contact, because move_and_collide leaves any sliding response to code written by the user.
- D: A printed word is not a movement result, so a body that stops dead would still pass.
- E: The two methods differ exactly here: move_and_collide returns the collision and halts, while move_and_slide deflects the motion along the surface.

**Source:** move_and_slide versus move_and_collide

## MA-k02.13

An agent reports: "Enemy movement is now frame-rate independent: velocity = direction * speed * delta, then move_and_slide()." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The claim is right, because multiplying by delta is the standard step for movement.
- [ ] B. The claim is wrong: move_and_slide already applies the time step to the velocity, so scaling by delta as well makes the enemy move much too slowly.
- [ ] C. A follow-up that gives evidence is: report the distance the enemy covers in one second at 30 and 144 frames per second.
- [ ] D. A follow-up that gives evidence is: confirm the enemy moves toward the player at one frame rate.
- [ ] E. Keeping delta in the velocity and raising the speed value to compensate makes the movement frame-rate independent.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: With move_and_slide the multiplication is redundant, because the function already uses velocity as a per-second value.
- B: Double scaling shrinks the per-second speed by the delta value, roughly a sixtieth, so the enemy crawls.
- C: Equal distances per second at both rates, at the intended speed, confirm the fix directly.
- D: The enemy moves toward the player either way, so a slow enemy at one frame rate would still pass.
- E: Delta varies per frame, so a fixed compensation fits only one frame rate and the enemy speed still changes.

**Source:** Delta, move_and_slide

## MA-k02.14

An agent reports: "Variable jump height done: on button release I set velocity.y to 0." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: release the button in the middle of the descent and report the vertical speed on the next frame.
- [ ] B. The claim has a bug: if the button is released while the character is already falling, setting velocity.y to 0 makes it stop in the air briefly.
- [ ] C. The claim is correct, because zero vertical velocity ends the jump cleanly, including while falling.
- [ ] D. A correct version halves velocity.y on release regardless of direction of travel.
- [ ] E. A follow-up that gives evidence is: confirm that tapping the button gives a lower jump than holding it, and stop there.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: A release during descent exposes the hover bug, since the vertical speed would wrongly read near zero.
- B: Zeroing a downward velocity cancels the fall, producing a visible hover before gravity restarts it.
- C: Zeroing the velocity during descent halts the fall, so the claim only holds while rising.
- D: Halving during a fall slows the descent, so the same release-in-descent glitch remains and the bug is kept.
- E: That test covers only the rising case, so the hover bug during descent would pass.

**Source:** Variable jump height

## MA-k02.15

An agent reports: "Walk-to-run blending works. I set the AnimationTree speed parameter once in _ready." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The claim is right, because a blend parameter keeps tracking the speed once set.
- [ ] B. The claim is doubtful: a value set once in _ready does not follow the character's changing speed, so the blend stays put.
- [ ] C. The parameter can be set once in _ready to the maximum speed so the blend runs fully.
- [ ] D. A follow-up that gives evidence is: ask the agent whether the AnimationTree node exists.
- [ ] E. A follow-up that gives evidence is: start the game and report the blend value while the character stands still.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: A parameter keeps the last value written to it and does not follow the character's speed by itself.
- B: The parameter holds its initial value until code updates it, so walking faster does not change the blend.
- C: A fixed maximum would play the run animation constantly, so walking would never appear.
- D: A node existing says nothing about whether the blend value changes with speed.
- E: A standing character reads the initial value either way, so this check passes the bad claim.

**Source:** Blend tree parameters

## MA-k02.16

An agent reports: "The pickup works: I connected the coin's body_entered signal to _on_body_entered in the editor." No output was shown. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The claim is enough, because a connected signal means the handler runs.
- [ ] B. A follow-up that gives evidence is: report the coin's monitoring, layer and mask values.
- [ ] C. A follow-up that gives evidence is: add a print in the handler, walk the player into the coin and show the output.
- [ ] D. The Area2D's mask must include the player's layer for body_entered to fire.
- [ ] E. A connection existing does not show that the signal fires, so the claim lacks evidence.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: The handler runs when the signal is emitted, and that depends on monitoring, mask and the player's layer.
- B: These inputs decide whether an overlap is detected, so wrong values would explain a silent handler.
- C: A printed line in the handler shows the signal fired and the handler ran in play.
- D: An area detects only bodies on layers in its own mask, so a mismatch leaves the signal silent.
- E: A connection only lists a handler; the signal fires when an overlap occurs, which the setup may prevent.

**Source:** Signals, evidence

## MA-k02.17

An agent reports: "Fixed bullet tunnelling by doubling the bullet speed so it spends less time near the wall." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: fire 200 bullets at the thin wall and report how many passed through, before and after.
- [ ] B. The reasoning is right because less time near the wall means less chance of passing through.
- [ ] C. A fix that targets the cause is continuous collision detection or a raycast along the bullet's path.
- [ ] D. A follow-up that gives evidence is: fire one bullet and report that it hit.
- [ ] E. The reasoning is wrong: faster bullets move farther per physics step, which makes tunnelling more likely.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: A pass-through rate over many shots shows whether the fix reduces an intermittent bug.
- B: Time near the wall is not the issue; distance covered per step is, and more speed raises it.
- C: Both check the whole path travelled in a step instead of only the end position, so thin walls are caught.
- D: One sample is not enough for a bug that happens sometimes, so a failing fix could still pass.
- E: Longer steps jump over thin colliders more easily, so doubling speed worsens the problem it claims to fix.

**Source:** Tunnelling

## MA-k02.18

An agent reports: "Applied the normal map to the albedo slot so the bricks look bumpy." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: render the wall with a light moved across it and show whether the highlights change with the light.
- [ ] B. The claim is right, because both are textures that change how the surface looks.
- [ ] C. In StandardMaterial3D the Normal Map feature must be enabled before the texture is read as surface directions.
- [ ] D. The normal map belongs in the material's normal slot.
- [ ] E. The claim is wrong: albedo is base colour, and a normal map stores surface directions, so in the colour slot it shows as purple-blue colour instead of bumps.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Real bumps shade differently as the light moves, while a flat colour texture does not.
- B: The two textures hold different data, so only the normal slot reads directions to bend the lighting.
- C: Without enabling the feature, the assigned texture is ignored and the bricks still look flat.
- D: That slot reads the texture as surface directions, which produces the bump shading under light.
- E: The texture holds direction data, so used as colour it paints the surface blue and gives no lighting detail.

**Source:** Normal map versus albedo

## MA-k02.19

An agent reports: "Made the floor an Area2D so the player can stand on it." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: drop the player onto the floor and report whether is_on_floor() becomes true.
- [ ] B. A follow-up that gives evidence is: ask the agent to add a sprite to the floor.
- [ ] C. The claim is right because a collision node with a shape holds a character up.
- [ ] D. The claim is wrong: an Area2D detects overlaps and does not block, so the player falls through it.
- [ ] E. Matching the Area2D's layer to the player's mask is enough for the player to stand on it.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Landing on a real floor makes is_on_floor() true, so the result tests the claim directly.
- B: A sprite changes the look but not the physics, so a floor the player falls through would pass.
- C: Only solid bodies block movement; an area with a shape just reports overlap, so the player still falls.
- D: An Area2D reports overlaps but exerts no collision response, so a character passes straight through.
- E: Layers and masks control detection between objects, but an area stays non-solid, so the player still falls.

**Source:** Body versus area

## MA-k02.20

An agent reports: "Combined hitbox and hurtbox into one Area2D so one node handles both." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The change creates a risk: an attack area on the player would overlap the player's own hurtbox and could damage the player.
- [ ] B. The change is a tidy-up, because both are the same thing.
- [ ] C. A follow-up that gives evidence is: swing the player's attack in an empty room and report whether the player takes damage.
- [ ] D. Keeping them separate lets each be on its own layer and mask so attackers hit only what they should.
- [ ] E. A hitbox can have monitoring switched off, because the hurtbox's own mask and monitoring detect the overlap.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: A merged node detects its own owner, so the attack can register as damage to the player.
- B: They have different roles, dealing damage versus receiving it, and need different layers and masks.
- C: An empty room isolates self-hits, so damage taken exposes the merged-node bug.
- D: Separate nodes allow separate layer and mask settings, which control who can damage whom.
- E: The hurtbox does the detecting, so the hitbox only needs to be on a layer the hurtbox's mask includes.

**Source:** Hitbox and hurtbox

## MA-k02.21

An agent reports: "Verified the export: the game runs correctly in the editor, so the exported build is fine." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Running in the editor does not test the packaged build, which can differ in file paths, missing resources and export settings.
- [ ] B. The claim is enough because the editor runs the same files as the build.
- [ ] C. A follow-up that gives evidence is: list the resources the export excluded or failed to find.
- [ ] D. Resources loaded by a built string path may be missing from the export unless the preset includes them.
- [ ] E. A follow-up that gives evidence is: export the build, launch the exported executable and report what happens on the first level.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: The exported package has its own file layout and filters, so problems appear only after exporting.
- B: Exports apply filters, presets and packed paths, so the build can differ from the editor.
- C: Missing resources are a common export failure, and a list shows them before the player does.
- D: The export scans references it can see, so a path assembled at run time can be skipped.
- E: Running the real artefact tests what ships and exposes export-only failures.

**Source:** Packaged build versus editor

## MA-k02.22

An agent reports: "Line of sight works: the enemy's raycast returns a hit, so the enemy can see the player." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: put a wall between enemy and player and report whether the ray still hits something.
- [ ] B. The claim is right, since the ray goes toward the player and so a hit is the player.
- [ ] C. Setting the ray's mask to the player's layer alone is right, because walls are then ignored.
- [ ] D. A follow-up that gives evidence is: confirm line of sight is true with the player standing in plain view, and nothing else.
- [ ] E. The claim is incomplete: a ray hit may be a wall, so the code must check that the first thing hit is the player.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: The ray hits the wall, so it reports a hit anyway, and the enemy that sees through cover would pass.
- B: The ray stops at the first collider it meets, which can be a wall between enemy and player.
- C: Ignoring walls lets the ray reach the player through them, so the enemy sees through solid cover.
- D: This tests the positive case alone, so an enemy that sees through walls would pass.
- E: A ray reports the first collider along its path, so a hit alone does not tell what it was.

**Source:** Raycast, line of sight

## MA-k02.23

An agent reports: "Replaced the AnimationTree state machine with a blend tree so the attack plays when the button is pressed." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The change fits poorly: an attack that interrupts movement is a discrete change of state, which a state machine with transitions expresses.
- [ ] B. A follow-up that gives evidence is: press attack while running and report which animation is playing on the next frame.
- [ ] C. A follow-up that gives evidence is: ask the agent to explain the difference between the two in a paragraph.
- [ ] D. A state machine suits mixing walk and run by a speed value, which is why it was replaced.
- [ ] E. The change is right because a blend tree can trigger clips from button presses by itself.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: A state machine switches between named states on events, which matches the attack interrupting movement.
- B: The playing animation after the press shows whether the attack interrupts movement.
- C: A written explanation is not a behaviour test, so a broken attack would pass.
- D: Mixing by a continuous speed value is blend tree work; a state machine only switches between clips.
- E: A blend tree mixes animations by parameters and has no transitions to react to an event.

**Source:** State machine versus blend tree

## MA-k02.24

An agent reports: "Used create_tween() inside _process to move the node smoothly each frame." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The approach is wrong: it creates a new tween every frame, and many tweens fight over the same property.
- [ ] B. Moving by code with move_toward(target, speed * delta) in _process suits a target that changes continually.
- [ ] C. A follow-up that gives evidence is: report how many active tweens exist on the node after 5 seconds.
- [ ] D. A tween should be created once with the target and duration, which suits a fixed destination.
- [ ] E. The approach is right, because a tween is created each frame to stay current.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Overlapping tweens all write to the same property, so the node jitters between their targets.
- B: A per-frame move toward the current target follows it smoothly without creating objects.
- C: A growing tween count shows the per-frame creation bug directly, while one active tween is healthy.
- D: A single tween runs the move on its own, so creating it once avoids conflicts.
- E: One tween covers the whole move, so a fresh one per frame only multiplies the conflicts.

**Source:** Tween

## MA-k02.25

A request said: "Add a double jump. Do not delete any files." The agent reports: "Double jump added. I deleted the unused enemy scenes to keep the project tidy." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The deletion is fine because the scenes were unused.
- [ ] B. A follow-up that shows the constraint was kept is: ask the agent to run the game once and report that it starts.
- [ ] C. An unused file can be referenced by a path in a script, so deletion can break the game later.
- [ ] D. The agent broke an explicit constraint, and the deleted scenes should be restored before the work is accepted.
- [ ] E. A follow-up that gives evidence is: list the files removed in the change and check them against the constraint.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: The agent could not know they were unused where scripts load them by path, and the constraint applied anyway.
- B: Starting does not load the missing scene, so a broken reference would pass.
- C: A scene loaded by a string path is invisible to the editor's reference view, so removal causes a runtime error.
- D: The request forbade deleting files, so the removal is a violation whether or not the scenes seemed unused.
- E: A list of deleted files in the change shows the violation directly.

**Source:** Scope violation

## MA-k02.26

A request said: "Rename the Player node's script variable hp to health." The agent reports: "Renamed hp to health in player.gd. Done." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: search the whole project for the old name and report each remaining match.
- [ ] B. The claim is complete, since the variable is declared in player.gd.
- [ ] C. An exported variable renamed in a script loses its saved Inspector value in scene files, so those scenes need checking.
- [ ] D. The claim is incomplete: other scripts, scenes or animation tracks may still refer to hp.
- [ ] E. A follow-up that gives evidence is: run the game, take damage and report the health value.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: A project-wide search lists remaining references, showing what the rename missed.
- B: Other files can read or write the variable, so declaring it in one place does not cover its uses.
- C: The scene stores values by property name, so the old name's value is dropped.
- D: A rename in one file leaves other callers of hp broken until they are found and updated.
- E: A play-through exercises the renamed variable and shows whether damage still reaches it.

**Source:** Scope, verification

## MA-k02.27

An agent reports: "The test for the damage function passes. I generated the expected value by running the function and pasting its output." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The test is strong, since it passes on the current code.
- [ ] B. The test is weak: it asserts that the function returns what it returned, so it cannot find a wrong formula.
- [ ] C. The test becomes strong once the pasted value is moved into a named constant in the test file.
- [ ] D. A follow-up that gives evidence is: change the damage formula on purpose and report whether the test then fails.
- [ ] E. A follow-up that gives evidence is: run the same test a second time.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: It passes whatever the code does, because the expected value is the code's own output.
- B: The expected value comes from the code under test, so the assertion holds even when the formula is wrong.
- C: A constant holds the same copied output, so a wrong formula still passes.
- D: A test that stays green after a deliberate break cannot detect faults, so this check exposes it.
- E: The same test passes again for the same reason, so it adds no independent check.

**Source:** Evidence versus claim

## MA-k02.28

An agent reports: "Edited the .tscn file by hand and renamed several nodes to match the new naming scheme. Everything still works." The request was to add a light. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Renaming nodes changes node paths, which scripts and signals use, so it can break references that are not tested.
- [ ] B. A follow-up that gives evidence is: open the scene in the editor and report that it loads.
- [ ] C. The rename can stay in the commit since the scene still loads and the light works.
- [ ] D. A follow-up that gives evidence is: ask the agent to restate that everything works.
- [ ] E. Renaming nodes is cosmetic, so it does not affect scripts or signals.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: Calls such as get_node and signal connections store paths, and a renamed node leaves them pointing nowhere.
- B: A scene that loads does not prove scripts and signals still find their nodes.
- C: The rename was outside the request and carries hidden risk, so it should be reverted or approved.
- D: Restating repeats the unverified claim, so a broken reference would pass.
- E: Paths are used in code and connections, so renames can break behaviour.

**Source:** Scope violation

## MA-k02.29

An agent reports: "Fixed the global score: I reload the scene to reset it, and the score now persists across levels because it is an autoload." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A follow-up that gives evidence is: ask if the autoload is registered in the project.
- [ ] B. Both claims hold, because reloading the scene resets scene nodes and the autoload together.
- [ ] C. A follow-up that gives evidence is: collect a coin, reload the scene and report the score before and after.
- [ ] D. The two claims conflict: an autoload survives scene reloads, so reloading the scene does not reset the score.
- [ ] E. Resetting the score needs an explicit reset in the autoload, for example a function called on a new run.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Registration does not show whether the score resets or persists.
- B: The autoload sits outside the scene tree, so a reload cannot reset it.
- C: The before and after values show whether the score survives the reload.
- D: An autoload lives outside the current scene, so changing or reloading scenes leaves its values untouched.
- E: Only code that assigns the score can reset it, so the new-run path must call it.

**Source:** Autoload, evidence
