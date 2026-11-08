# Jargon test: compress and decompress

## MA-k01.1

A coin is an Area2D on collision layer 4. The player body is on layer 1. The coin must fire body_entered when the player touches it. A reviewer unpacks the layer and mask settings into checkable constraints. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. The player's collision mask must include layer 4 for the coin's body_entered signal to fire.
- [ ] B. The coin's collision mask must include layer 1, because the area scans for bodies on the layers in its mask.
- [ ] C. If the coin's mask is empty, body_entered does not fire even while the player overlaps the coin.
- [ ] D. Moving the coin from layer 4 to layer 1 does not make it detect the player, because detection comes from the mask.
- [ ] E. The coin's collision layer must include layer 1 so that it can see the player.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: The signal depends on the area's mask, not the player's mask, so changing the player's mask does not fix detection.
- B: An area detects a body when the body's layer is in the area's own mask, so the mask must name layer 1.
- C: With no layer in its mask the area scans for nothing, so overlapping bodies are never reported.
- D: Changing the coin's layer changes what the coin is, not what it looks for, so detection stays broken.
- E: The coin's layer declares what the coin is, not what it sees, so adding layer 1 there would not make it detect the player.

**Source:** Collision layer versus mask

## MA-k01.2

A platformer has walls (StaticBody2D, layer 2), enemies (layer 3) and a player CharacterBody2D (layer 1). The player must be stopped by walls and must not be blocked by enemies. Ignore the enemies' own settings. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. The wall's collision mask must include layer 1 for the wall to stop the player.
- [ ] B. The player's collision mask includes layer 2.
- [ ] C. The player's collision mask leaves out layer 3.
- [ ] D. The player's own layer must be set to 2 so that it can hit walls.
- [ ] E. Moving the player from layer 1 to layer 5 does not change whether walls stop it, as long as its mask still includes layer 2.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A static body does not move or scan, so its mask does not decide whether the player is stopped.
- B: A moving body is stopped by the layers listed in its own mask, so layer 2 must be there for walls to block it.
- C: A layer missing from the mask is passed through by this body, so enemies on layer 3 do not block the player.
- D: The player's layer says what the player is; the walls are found through the player's mask, so changing the layer is wrong.
- E: Blocking is decided by the moving body's mask, not by its own layer.

**Source:** Collision layer versus mask

## MA-k01.3

Layers: player 1, walls 2, enemies 3, bullets 4. Spec: "A bullet hits walls and enemies, passes through the player, and passes through other bullets." Check each statement that is a correct unpacking or compression of that spec. Each statement is worth 1 point (5 points total).

- [ ] A. Clearing the bullet's collision layer does not change what the bullet hits, because hits come from its mask.
- [ ] B. Set the bullet's mask to include layers 2 and 3 and exclude layers 1 and 4.
- [ ] C. Putting the bullet on layer 4 labels it as a bullet but does not by itself decide what it hits.
- [ ] D. Leaving layer 4 out of the bullet's mask is what stops bullets from hitting one another.
- [ ] E. Set the bullet's mask to layers 1 and 4.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: The mask still contains the same layers, so the bullet keeps hitting the same things as before.
- B: The mask lists what the bullet checks for, so walls and enemies are in it while the player and bullets are left out.
- C: The layer states what the bullet is; what it hits is chosen by its mask.
- D: A bullet reports only bodies on layers in its mask, so omitting layer 4 lets bullets pass through each other.
- E: That makes the bullet hit the player and other bullets, which is the opposite of the spec and misses walls and enemies.

**Source:** Collision layer versus mask

## MA-k01.4

A programmer pastes the term pair "_physics_process versus _process" into a spec and asks for unpackings that can be checked in code. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. _physics_process is called on the fixed physics tick, so its delta is the same each call.
- [ ] B. _process is called once per rendered frame, so its delta changes when the frame rate changes.
- [ ] C. Defining both functions on one node makes Godot ignore _process.
- [ ] D. _physics_process is called once per rendered frame, so it runs less often on a slow computer.
- [ ] E. A health bar that only needs to animate smoothly on screen fits _process, because it does not touch physics.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: The physics tick runs at a fixed step, so the delta passed in stays constant from call to call.
- B: Rendered frames take varying time, so the delta passed to _process varies with the frame rate.
- C: Godot calls both functions on the node each in its own cycle, so neither one disables the other.
- D: It follows the physics tick instead; on a slow computer it can run more than once per rendered frame to catch up.
- E: Visual updates tied to the display belong in the per-frame callback, since no physics step is involved.

**Source:** _physics_process versus _process

## MA-k01.5

A spec says: "Make the movement frame-rate independent." An agent proposes the changes below. Check each statement that correctly unpacks "frame-rate independent" for a character that moves by changing its position in _process. Each statement is worth 1 point (5 points total).

- [ ] A. Multiplying a per-second speed by delta gives the same distance per second at 30 and 144 frames per second.
- [ ] B. Raise the maximum frame rate until the movement looks the same on the developer's machine and a slow laptop.
- [ ] C. Store the speed in units per second and add speed multiplied by delta to the position each frame.
- [ ] D. Add gravity multiplied by delta to the vertical velocity each frame.
- [ ] E. Multiply the velocity by delta before assigning it to the velocity that move_and_slide uses.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Delta shrinks as the frame rate rises, so more frames each cover a proportionally smaller step.
- B: Frame rate is not guaranteed on other hardware, so the movement would still differ between machines.
- C: Scaling by delta converts a per-second rate into a per-frame step, so distance per second is the same at any frame rate.
- D: Gravity is an acceleration in units per second squared, so it is scaled by delta when it changes velocity.
- E: move_and_slide applies the time step itself, so the velocity is scaled twice and the character moves far too slowly.

**Source:** Delta and frame-rate independence

## MA-k01.6

A level designer writes "coyote time 0.1 s" in the spec. Check each statement that is a correct unpacking into a checkable constraint. Each statement is worth 1 point (5 points total).

- [ ] A. The timer starts when the player presses the jump button.
- [ ] B. A jump press 0.08 s after walking off a ledge still jumps.
- [ ] C. After a real jump the window is cleared, so a second press during the same fall does not give a second jump.
- [ ] D. A jump press 0.08 s before landing still jumps when the character lands.
- [ ] E. The timer starts at the moment the character leaves the floor without jumping.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Starting at the press would build a buffer, not a grace window that opens after leaving the ground.
- B: The press arrives inside the 0.1 s grace window, so the jump is accepted.
- C: Clearing it prevents coyote time from turning into a free double jump.
- D: That behaviour is a jump buffer, a separate feature that remembers early presses, not coyote time.
- E: That moment opens the short grace window in which a jump is still allowed after walking off an edge.

**Source:** Coyote time

## MA-k01.7

A level designer writes "jump buffer 0.1 s" in the spec. Check each statement that is a correct unpacking into a checkable constraint. Each statement is worth 1 point (5 points total).

- [ ] A. A jump press 0.05 s after walking off a ledge results in a jump.
- [ ] B. The press is stored when the character is standing on the floor, and ignored while it is in the air.
- [ ] C. A jump press 0.05 s before landing results in a jump on the landing frame.
- [ ] D. The buffer makes the jump reach a higher apex.
- [ ] E. The remembered press expires after 0.1 s, so a press 0.3 s before landing does not jump on landing.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: That is coyote time, a different feature that allows jumping after leaving the floor.
- B: The press must be stored while airborne, since remembering an early press before landing is the whole purpose.
- C: The early press is remembered for the buffer duration, and the jump fires when the character lands inside that time.
- D: It changes when the jump starts, not how high it goes, so apex height is unaffected.
- E: The buffer is a timer, so presses older than its duration are forgotten.

**Source:** Jump buffer

## MA-k01.8

A producer pairs a described behaviour with a one-line instruction for the agent. Check each pair in which the instruction correctly compresses the behaviour. Each statement is worth 1 point (5 points total).

- [ ] A. "A short tap makes a small hop and holding makes a full jump" is compressed by "add a jump buffer".
- [ ] B. "A short tap makes a small hop and holding makes a full jump" is compressed by "add variable jump height".
- [ ] C. "Players who walk off a ledge can still jump for a split second" is compressed by "add coyote time of 0.1 s".
- [ ] D. "A jump pressed just before landing still happens on landing" is compressed by "add a jump buffer of 0.1 s".
- [ ] E. "Players who walk off a ledge can still jump for a split second" is compressed by "add a jump buffer".

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: A buffer changes when a jump starts, not how high it goes, so the tap and hold behaviour would be missing.
- B: Variable jump height makes the apex depend on how long the button is held.
- C: Coyote time is the grace window that allows a jump just after leaving the floor.
- D: A jump buffer remembers an early press and applies it when the character lands.
- E: A buffer remembers an early press; the ledge case needs coyote time, so the wrong feature would be built.

**Source:** Coyote time, jump buffer, variable jump height

## MA-k01.9

A designer asks for variable jump height. Check each statement that is a correct unpacking of it for a character that jumps by setting an upward velocity. Each statement is worth 1 point (5 points total).

- [ ] A. The apex height stays the same and the time in the air changes.
- [ ] B. Releasing the button while the character is already falling cuts the fall speed.
- [ ] C. A tap and a full hold of the button produce different apex heights.
- [ ] D. If the jump button is released while the character is still rising, the upward velocity is cut to a smaller value.
- [ ] E. Releasing the button after the apex has been reached changes nothing about the jump.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Apex height is what varies with the hold length, so a fixed height would fail the spec.
- B: The cut applies while rising; reducing a fall speed would make the character float instead of shortening the jump.
- C: That difference in apex height is the observable result a test can check.
- D: Cutting the rising velocity on release is the usual implementation, ending the jump early at a lower apex.
- E: The character is already falling, so the height is fixed and release has no effect.

**Source:** Variable jump height

## MA-k01.10

An agent is asked to build a player state machine with Idle, Run and Jump. Check each statement that is a correct unpacking of "state machine" into constraints that can be tested. Each statement is worth 1 point (5 points total).

- [ ] A. Run and Jump are both active while the character runs and jumps at once.
- [ ] B. A state with no transition into it does not become active unless it is the starting state.
- [ ] C. Exactly one state is active at a time.
- [ ] D. Taking a transition makes the new state current, and the old state stops being active.
- [ ] E. Each transition names the state it leaves, the state it enters and the condition that triggers it.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: In a basic state machine one state is current; a jump while running is a transition from Run to Jump.
- B: Without an incoming transition or start role the state is unreachable.
- C: A single current state is what separates a state machine from a pile of independent flags.
- D: Moving between states replaces the current state, which keeps exactly one active.
- E: Transitions are the checkable part: a source, a target and a trigger condition.

**Source:** State machine

## MA-k01.11

A designer wants walk-to-run to change smoothly with speed, and wants an attack to interrupt movement. Check each statement that correctly maps the behaviour to an AnimationTree tool. Each statement is worth 1 point (5 points total).

- [ ] A. A blend tree stores which state is current and the rules for leaving it.
- [ ] B. If the speed parameter is set once in _ready, the walk-to-run blend keeps following the speed.
- [ ] C. A longer blend time between walk and run handles the attack interruption.
- [ ] D. A blend space driven by a speed parameter blends walk into run continuously.
- [ ] E. A blend space is the right tool for choosing one attack clip when the attack button is pressed.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: Tracking the current state and its transition rules is the state machine's job, not the blend tree's.
- B: The parameter must be updated as speed changes, otherwise the blend stays at its initial position.
- C: Blend time only smooths a transition; interrupting movement needs a state machine transition into an Attack state.
- D: A blend space mixes clips smoothly according to a parameter value, which suits a speed-driven change.
- E: Picking one clip on a button press is a discrete change of state, which a state machine handles.

**Source:** Blend tree versus state machine

## MA-k01.12

A designer says: "Slide the menu panel in to x = 200 over 0.5 seconds, slowing as it arrives." Check each statement that is a correct unpacking into a tween. Each statement is worth 1 point (5 points total).

- [ ] A. "Make the panel move smoothly" is as complete a tween spec as the one above.
- [ ] B. A finished tween returns the property to its starting value.
- [ ] C. "Slowing as it arrives" is an ease-out curve.
- [ ] D. The tween needs a property (position), a final value (x = 200) and a duration (0.5 s).
- [ ] E. Easing changes the final value the property reaches.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: It names no property, target value or duration, so an agent would have to guess them.
- B: The property stays at the final value unless another tween or script moves it.
- C: Ease-out decelerates toward the end of the motion, which matches a panel that slows as it arrives.
- D: Those three values are the constraints a tween call needs to be fully specified.
- E: Easing shapes the speed curve over time; the end value and duration stay what was set.

**Source:** Tween and easing

## MA-k01.13

A Godot script has `signal died` and a UI script that should react. Check each statement that is a correct unpacking of "use a signal". Each statement is worth 1 point (5 points total).

- [ ] A. The connected function's return value is sent back to the emitter.
- [ ] B. The emitter declares the signal and calls emit; the listener connects one of its own functions to it.
- [ ] C. Values passed in emit are ignored; the connected function reads them from the emitter.
- [ ] D. Emitting a signal that has no connected function raises an error.
- [ ] E. A signal accepts a single connected function.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: Signals are one-way notifications, so the emitter receives no result from listeners.
- B: The two ends are declaring and emitting on one side and connecting a function on the other.
- C: Parameters travel with the signal and arrive as arguments of the connected function.
- D: Emitting with no listeners simply does nothing, since the emitter does not know or depend on its listeners.
- E: Many functions can connect to one signal, and all of them are called when it is emitted.

**Source:** Signals

## MA-k01.14

A designer says "the child should tell its parent, not reach into it". Check each statement that correctly applies "call down, signal up" to a Door scene that sits inside a Level scene. Each statement is worth 1 point (5 points total).

- [ ] A. The Door can be tested alone because it does not need to know which nodes listen.
- [ ] B. The Door's signal carries a notification and arguments, and the Level's connected function decides what changes.
- [ ] C. The Door calls get_parent() and runs a method of Level directly.
- [ ] D. The Level can connect to the Door's signal after the Door is added to the scene tree.
- [ ] E. The Level calls methods on the Door, and the Door emits a signal when it is opened.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Signals decouple the sender from its receivers, so the Door runs without a Level.
- B: The Level reacts in its own function, so the Door never edits the Level's properties directly.
- C: That ties the Door to one specific parent and breaks when the Door is reused elsewhere.
- D: Connections can be made at runtime whenever both nodes exist, so ordering against add_child is flexible.
- E: Parents call down into children and children signal up, keeping the child independent.

**Source:** Call down, signal up

## MA-k01.15

An Area2D has the properties monitoring and monitorable. A coin Area2D must detect the player body. A hurtbox Area2D must be detectable by enemy hitbox areas. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A hurtbox that enemy hitbox areas must detect needs monitorable on.
- [ ] B. Monitoring is whether this area detects others.
- [ ] C. Monitorable is whether other areas can detect this area.
- [ ] D. Turning monitoring off makes the area block bodies like a wall.
- [ ] E. Setting the coin's monitorable to false stops the coin from detecting the player.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: The hurtbox is the detected side, so other areas can only see it when monitorable is on.
- B: Monitoring controls the detecting side: whether this area reports overlaps with bodies and areas.
- C: Monitorable controls the detected side: whether other areas can see this one.
- D: Areas do not block movement; turning monitoring off just stops the area from reporting overlaps.
- E: The coin's detection depends on its monitoring flag; monitorable affects only whether other areas see the coin.

**Source:** Area monitoring and monitorable

## MA-k01.16

Four game objects need physics bodies: a wall, a player moved by input code that slides along walls, a crate shoved around by forces, and a moving platform driven by an animation that must push the player. Check each statement that is a correct match. Each statement is worth 1 point (5 points total).

- [ ] A. The moving platform is a StaticBody2D, because the animation moves it.
- [ ] B. The player is a RigidBody2D so that the engine handles walking.
- [ ] C. The player is a StaticBody2D, because its movement is written in code.
- [ ] D. The wall is a StaticBody2D.
- [ ] E. The crate is a CharacterBody2D.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: A body that is moved by animation yet must push others is an AnimatableBody2D.
- B: RigidBody2D is driven by forces and gives imprecise walking control, unlike the scripted control of CharacterBody2D.
- C: Static bodies are not meant to be moved; code-driven sliding movement uses a CharacterBody2D with move_and_slide.
- D: A wall does not move, which is exactly what a static body is for.
- E: A crate pushed around by forces and tumbling needs a RigidBody2D, which simulates forces and mass.

**Source:** Body types

## MA-k01.17

An enemy must know whether the player is in line of sight. A tower must find every enemy within 3 metres. Check each statement that is a correct choice and unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. A ray has no width, so it can pass through a gap a wide body could not.
- [ ] B. Finding everything within 3 metres is a shape query or an area with a circle shape.
- [ ] C. Line of sight is a raycast from the enemy toward the player, and the first thing hit must be the player.
- [ ] D. Line of sight is a raycast, and a hit on something means the enemy sees the player.
- [ ] E. A raycast returns the first object along one line, so it is the wrong tool for finding everything within 3 metres.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: A line of zero thickness slips through narrow openings that a wider shape would be blocked by.
- B: A shape query reports overlaps across a region instead of along one line.
- C: If a wall is hit first it blocks the view, so the first hit must be the player.
- D: The ray may hit a wall, so the hit object must be checked to be the player.
- E: One line misses bodies off to the side and hidden behind the first hit, so a region query is needed.

**Source:** Raycast and shape query

## MA-k01.18

A RigidBody2D needs a one-time knockback of 400 pixels per second away from a hit, and also a constant thruster push. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. The knockback is a force applied for a single physics step.
- [ ] B. For a body with mass, an impulse gives a smaller velocity change to a heavier body.
- [ ] C. The knockback is an impulse, an instant change of velocity.
- [ ] D. The thruster is a force applied on every physics step, changing velocity gradually.
- [ ] E. Multiplying the impulse by delta makes the knockback weaker and dependent on frame rate.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: A force acts over time, so one step gives a small, frame-dependent change instead of a fixed 400 pixels per second kick.
- B: An impulse changes momentum, so the velocity change is the impulse divided by mass.
- C: A one-time kick is an impulse, applied once to change the body's velocity immediately.
- D: A continuous push is a force applied each step, building speed over time.
- E: An impulse is not a per-second quantity, so scaling it by delta shrinks it and varies it with frame rate.

**Source:** Impulse versus force

## MA-k01.19

A designer writes: "The popup eases out, the falling crate eases in." Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. Ease-in-out starts slowly, moves fastest in the middle and slows again at the end.
- [ ] B. Ease-in starts slowly and speeds up, which suits an object starting to fall.
- [ ] C. Ease-in and ease-out reach different end values.
- [ ] D. Ease-out makes the animation take longer than a linear one of the same set duration.
- [ ] E. Ease-out starts fast and slows at the end, which suits a popup that settles.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: It combines both curves, so the speed is low at both ends and peaks mid-way.
- B: Ease-in accelerates from rest, resembling a crate that gains speed as it falls.
- C: Both reach the same end value; only the speed curve along the way differs.
- D: The duration is fixed by the setting; easing only reshapes how the speed varies within it.
- E: Ease-out decelerates into rest, so the popup comes gently to its final position.

**Source:** Easing

## MA-k01.20

A camera follows with `position = position.lerp(target, 0.1)` once per rendered frame. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A weight of 0.1 means the camera reaches the target in 0.1 seconds.
- [ ] B. At a higher frame rate the camera catches up faster in real time.
- [ ] C. A frame-rate independent version scales the weight with delta, for example 1 minus exp(-k times delta).
- [ ] D. The amount of catch-up per second depends on the frame rate.
- [ ] E. Doubling the frame rate leaves the real-time catch-up speed unchanged.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: It closes a tenth of the remaining gap each frame and approaches the target gradually.
- B: More lerp steps happen each second, so the gap closes sooner.
- C: A time-based weight gives the same catch-up per second regardless of frame rate.
- D: A fixed weight applies once per frame, so more frames per second mean more catch-up per second.
- E: Doubling the frame rate doubles the lerp steps per second, which speeds up the catch-up.

**Source:** Lerp and delta

## MA-k01.21

A bullet is fast and thin and sometimes passes through thin walls. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. A raycast from the bullet's start to its end position each step misses a wall lying between them.
- [ ] B. Making the sprite larger stops tunnelling.
- [ ] C. Continuous collision detection checks the whole path of the move instead of only the end position.
- [ ] D. Teleporting the bullet to its new position by setting its position is a safe way to avoid tunnelling.
- [ ] E. Tunnelling happens when the move per physics step is longer than the thing it should hit.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A ray covers the whole distance between its endpoints, so it finds the wall even when the bullet would skip over it.
- B: Physics uses the collision shape, not the picture, so a larger sprite changes nothing about collisions.
- C: Checking the swept path catches thin obstacles between steps, which stops tunnelling.
- D: Setting position skips the path in between, so the thin wall is never tested.
- E: The body is on one side of the wall at one step and the other side at the next.

**Source:** Tunnelling and continuous collision detection

## MA-k01.22

A designer separates the terms "hitbox", "hurtbox" and "body collider" for a fighting game. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A hurtbox is the area that deals damage when it overlaps a hitbox.
- [ ] B. A hitbox blocks the other fighter's movement.
- [ ] C. Making the character's sprite bigger enlarges the hurtbox.
- [ ] D. A hitbox is an area that deals damage when it overlaps a hurtbox.
- [ ] E. Hitbox and hurtbox are the same area under two names.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: The roles are swapped: the hurtbox receives damage and the hitbox deals it.
- B: Blocking is the body collider's job; hitboxes just detect overlaps and do not push bodies.
- C: Collision shapes, not the picture, define the hurtbox, so scaling the sprite leaves it unchanged.
- D: The hitbox is the attacking side, detecting overlap with the hurtbox that receives the hit.
- E: They have different roles, attack versus receive damage, and are usually separate shapes.

**Source:** Hitbox, hurtbox, body collider

## MA-k01.23

An AnimatedSprite2D plays an 8-frame idle loop, and a 6-frame jump that must play once and stay on the last frame. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. Eight frames at 8 frames per second last 1 second.
- [ ] B. Looping is on for idle.
- [ ] C. Raising the game's frame rate to 144 makes the sprite animation play faster.
- [ ] D. Looping is off for jump, so it stops on the last frame.
- [ ] E. Doubling an animation's frames-per-second setting doubles its duration.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Duration is frame count divided by frames per second, which gives 1 second here.
- B: An idle animation repeats continuously, so its loop setting is enabled.
- C: The animation has its own frames-per-second setting, independent of the display frame rate.
- D: With looping off the animation plays once and holds its last frame.
- E: Doubling the speed halves the duration, since the same frames are shown in half the time.

**Source:** Sprite animation

## MA-k01.24

A designer asks for a waving flag that moves in the world and a tint that fades on every pixel by a value set from a script. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A varying carries a value from a script into the shader.
- [ ] B. A uniform is computed separately for each pixel by the fragment shader.
- [ ] C. A uniform is a value set from outside the shader, for example by a script, and read by the shader.
- [ ] D. Moving the flag's corners is a fragment shader job.
- [ ] E. Tinting each pixel is a vertex shader job, run once per corner.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: A varying passes values from the vertex stage to the fragment stage, while uniforms bring in script values.
- B: A uniform is set from outside and is the same for the whole draw, not computed per pixel.
- C: A uniform is how a script passes the fade amount into the shader.
- D: Corner positions are handled in the vertex stage; the fragment stage outputs per-pixel colour.
- E: Per-pixel colour comes from the fragment stage, which runs for each pixel.

**Source:** Vertex, fragment, uniform, varying

## MA-k01.25

A game has a Score value that must survive scene changes. Check each statement that is correct about using an autoload (singleton) for it. Each statement is worth 1 point (5 points total).

- [ ] A. An autoload is the right place for the player's sprite, because it keeps it between levels.
- [ ] B. An autoload creates a separate copy for each scene.
- [ ] C. Other scripts can reach it by its autoload name.
- [ ] D. An autoload node is loaded at startup and stays alive while scenes change.
- [ ] E. The score resets to zero each time the current scene is changed, because autoloads belong to the scene.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Scene content belongs in scenes; an autoload suits global state and services, not level visuals.
- B: There is one autoload instance shared by the whole game.
- C: Godot registers the autoload under the name given in project settings, giving global access.
- D: It sits outside the current scene, so changing scenes does not free it.
- E: Autoloads do not belong to the current scene, so their values persist across scene changes.

**Source:** Autoload

## MA-k01.26

A designer wants each enemy to have its own health, but all from one enemy scene. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. Instancing the scene creates a separate copy of its node tree for each enemy.
- [ ] B. Editing a property on one instance changes the other instances of the scene.
- [ ] C. An instance must be added to the scene tree, for example with add_child, to run.
- [ ] D. Calling instantiate edits the saved scene file.
- [ ] E. Two instances share one health variable because they share a script.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Each instance is its own node tree, so state is kept per enemy.
- B: Instances keep their own values, so an edit on one does not touch the others.
- C: An instantiated node that is not in the tree is not processed or drawn.
- D: It creates a node tree in memory and leaves the scene file as it was.
- E: Variables belong to each instance, so each enemy has its own health even with the same script.

**Source:** Scene instancing

## MA-k01.27

An enemy uses NavigationAgent2D to walk to the player. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. The walkable area comes from the NavigationAgent2D's own radius setting.
- [ ] B. The agent finds a path without a navigation region set up.
- [ ] C. The script sets the agent's target position and then reads the next path position each physics step to move toward it.
- [ ] D. The NavigationAgent2D moves the enemy's body by itself once a target is set.
- [ ] E. Collision layers decide where the enemy can walk.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: The walkable area comes from the navigation region; the agent's radius only affects clearance and avoidance.
- B: The navigation map must be provided first, or the agent has nothing to path through.
- C: The agent plans the path; the script is what actually moves the body along it.
- D: It only computes the path, so the body must be moved by code each step.
- E: Navigation data decides the path; layers decide physics collisions, which are a separate system.

**Source:** Navigation

## MA-k01.28

A one-shot explosion uses a particle node. Check each statement that is a correct unpacking of its settings. Each statement is worth 1 point (5 points total).

- [ ] A. With one-shot off, the effect plays once and stops.
- [ ] B. Lifetime is how long each particle lives.
- [ ] C. Amount is how many particles are emitted.
- [ ] D. Lifetime is how long the emitter keeps running.
- [ ] E. One-shot makes the emitter release one burst and then stop.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: With one-shot off the emitter repeats continuously, which would make the explosion loop.
- B: Lifetime is a per-particle duration, after which that particle disappears.
- C: Amount sets the number of particles the emitter creates, as distinct from how long each one lives.
- D: It describes the life of a single particle, not the time the emitter keeps emitting.
- E: With one-shot on, the particles are emitted once instead of continuously.

**Source:** Particle settings

## MA-k01.29

A weapon has a cooldown of 0.5 seconds. The agent uses a Timer node. Check each statement that is a correct unpacking. Each statement is worth 1 point (5 points total).

- [ ] A. Starting the timer at fire time, not at button-press time, keeps a refused shot from extending the cooldown.
- [ ] B. wait_time is in seconds.
- [ ] C. One-shot off makes the timer fire once and stay stopped.
- [ ] D. The weapon can fire again as soon as the timer node exists.
- [ ] E. Starting the timer when the weapon fires, and refusing to fire while the timer is running, gives a cooldown.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: A refused shot should not restart the timer, or the player would wait longer than 0.5 seconds.
- B: The Timer's wait_time property is measured in seconds, not frames, so 0.5 means half a second.
- C: With one-shot off the timer restarts and times out repeatedly, so it would not stay stopped.
- D: The timer must finish counting down first, so merely having the node does not end the cooldown.
- E: That is the core logic: the running timer blocks firing until it finishes.

**Source:** Timer
