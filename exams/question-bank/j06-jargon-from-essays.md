# Jargon test: from the essay prompts

## MA-jargon.51

A producer types "Make the camera swoop in on the boss, then pan back out to show the arena." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A zoom out widens the field of view while the camera stays where it is.
- [ ] B. A pan is a rotation of the camera on the spot, so it does not move the camera back out.
- [ ] C. A dolly out moves the camera body backward along its view direction.
- [ ] D. A dolly changes the lens angle and leaves the camera position unchanged.
- [ ] E. "Pan back out" is the correct term for moving the camera body away from the subject.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Zoom is a lens change, not a position change.
- B: A pan turns the camera left or right without changing its position.
- C: Dolly names a move of the camera body toward or away from the subject.
- D: That describes a zoom; a dolly changes position.
- E: Moving the body away is a dolly out; pan is a rotation.

**Source:** Rewrite a vague camera prompt

## MA-jargon.52

A producer wants the boss reveal written as two exact readings: one where the camera body moves and one where only the lens changes. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. For the camera-body reading, ask for the focal length to change.
- [ ] B. A dolly in changes the parallax between near and far objects.
- [ ] C. A zoom in shifts near objects relative to far objects, which is parallax.
- [ ] D. For the lens reading, ask for the field of view to narrow and then widen with the camera position fixed.
- [ ] E. A zoom in keeps the viewpoint and magnifies the same view.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: Focal length is a lens property, so it belongs to the zoom reading.
- B: Moving the viewpoint shifts near objects more than far ones.
- C: Parallax needs the viewpoint to move, and a zoom does not move it.
- D: Field of view is the lens angle, the quantity a zoom changes.
- E: Only the lens angle changes, so relative positions of objects stay put.

**Source:** Dolly reading versus zoom reading

## MA-jargon.53

A designer asks an agent to "stabilise the camera" and needs the framing words defined. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Screen shake is a smoothing setting that makes the camera trail its target.
- [ ] B. A deadzone is a brief decaying random offset used to sell an impact.
- [ ] C. Look-ahead shifts the framing toward the direction of travel.
- [ ] D. Camera limits clamp the camera so it does not show space outside the level.
- [ ] E. A deadzone is a screen region where the target can move without the camera moving.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Smoothing (damping) does that; screen shake is a brief decaying random offset.
- B: That describes screen shake.
- C: It shows more of the space the target is heading into.
- D: Limits, also called bounds, restrict where the camera can go.
- E: It stops the camera reacting to small movements.

**Source:** Camera framing vocabulary

## MA-jargon.54

Match each described behaviour to its camera term. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An explosion rattles the view for a moment, so the term is camera limits.
- [ ] B. Small twitches of the player should not move the view, so the term is deadzone.
- [ ] C. The camera stops scrolling at the left edge of the level, so the term is look-ahead.
- [ ] D. The camera gently trails the player and catches up, so the term is look-ahead.
- [ ] E. A fast runner needs to see more of the level ahead, so the term is look-ahead.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: A brief rattle is screen shake.
- B: A deadzone ignores movement inside a region.
- C: Stopping at the edge is camera limits (bounds).
- D: Trailing and catching up is smoothing (damping).
- E: Look-ahead offsets the framing in the direction of travel.

**Source:** Pick the camera term for a behaviour

## MA-jargon.55

A student says, "A zoom and a dolly are the same: both make the subject bigger." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A zoom and a dolly produce the same parallax because both enlarge the subject.
- [ ] B. A zoom changes the field of view or focal length while the camera stays put.
- [ ] C. A dolly suits moving through a space so that depth is felt.
- [ ] D. A dolly changes the field of view as it moves the camera.
- [ ] E. A sniper scope view is a typical use of a zoom.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Only the dolly changes perspective and parallax.
- B: The lens changes, the viewpoint does not.
- C: The changing viewpoint produces parallax.
- D: A dolly moves the body and leaves the lens angle alone.
- E: A scope magnifies the same view without moving the viewpoint.

**Source:** Zoom versus dolly

## MA-jargon.56

An artist asks an agent for a "tighter, more dramatic lens". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A narrow field of view gives a magnified look.
- [ ] B. Widening the field of view is called a dolly out.
- [ ] C. A dolly in is done by lowering the field of view.
- [ ] D. Field of view is the angle of the scene that the lens covers.
- [ ] E. A longer focal length widens the field of view.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: The same part of the scene fills the screen more.
- B: Widening the lens angle is a zoom out; a dolly out moves the body.
- C: A dolly in moves the camera body forward.
- D: A wide angle shows more of the scene.
- E: A longer focal length narrows the field of view.

**Source:** Field of view and focal length

## MA-jargon.57

A prompt asks for "a 2D platformer follow camera that feels smooth." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Look-ahead gives an offset in the direction the player faces or travels.
- [ ] B. A follow camera tracks a named target such as the player.
- [ ] C. The deadzone size sets how far the camera runs ahead of the player.
- [ ] D. Screen shake is the setting to raise when the view looks jittery while following.
- [ ] E. Smoothing (damping) makes the camera trail slightly and catch up over a fraction of a second.

**Key:** A=T B=T C=F D=F E=T

**Why:**

- A: It frames the space the player is moving into.
- B: The target is the thing the camera follows.
- C: That is look-ahead; a deadzone is a region where the target moves without the camera.
- D: Screen shake adds motion; jitter is reduced by smoothing and a deadzone.
- E: It softens the camera motion toward the target.

**Source:** Follow-camera tuning words

## MA-jargon.58

After the follow camera is built, a tester describes what to watch for. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A camera offset that fades out after a hit tests the deadzone.
- [ ] B. Standing still near the centre and seeing no camera twitch tests the deadzone.
- [ ] C. The view staying inside the level at the left edge tests look-ahead.
- [ ] D. The camera settling to rest in a fraction of a second after the player stops tests smoothing (damping).
- [ ] E. The camera showing more space to the right while running right tests camera limits.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: A decaying offset after a hit is screen shake.
- B: A deadzone keeps small movements from moving the camera.
- C: Staying inside the level tests camera limits.
- D: Damping controls how quickly the camera catches up.
- E: That is look-ahead.

**Source:** Observable camera checks

## MA-jargon.59

A door opens from 0 to 90 degrees in one second. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A keyframe is a stored value at a specific time, such as 90 degrees at 1 second.
- [ ] B. A tween is a stored value at a given time.
- [ ] C. Easing changes the end values of the door angle.
- [ ] D. Interpolation is the shape of the speed over time, such as a slow start and fast finish.
- [ ] E. A tween is authored by placing keyframes on a timeline in an animation editor.

**Key:** A=T B=F C=F D=F E=F

**Why:**

- A: Keyframes mark the values that the motion passes through.
- B: That is a keyframe; a tween is a code-driven interpolation.
- C: Easing changes the pacing and leaves the end values alone.
- D: That describes easing; interpolation computes the in-between values.
- E: A tween is set up in code with a property, a duration and an easing.

**Source:** Keyframe, interpolation, easing and tween

## MA-jargon.60

A team chooses between an authored clip and a tween for different jobs. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An authored clip suits designed, reusable motion on a rig or sprite.
- [ ] B. Interpolation computes the values between keyframes in an authored clip.
- [ ] C. A quick UI pop-up scale is better suited to an authored clip on a rig than to a tween.
- [ ] D. A tween is a code-driven interpolation of a property over a duration.
- [ ] E. A tween has no use for an easing setting.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Clips hold hand-made motion that can be played repeatedly.
- B: The engine fills in the in-between frames.
- C: Short procedural effects suit tweens.
- D: It is usually given an easing setting.
- E: Easing shapes the speed of a tween over its duration.

**Source:** Authored clip versus tween

## MA-jargon.61

A student writes: "Animate the sprite sheet with bones and use IK to cut it into frames." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Slicing is done by assigning bone weights to each cell.
- [ ] B. A sprite sheet is a grid of image frames, so it has no bones.
- [ ] C. IK is a method of cutting a sprite sheet into frames.
- [ ] D. A sprite sheet is animated by a skeleton of bones.
- [ ] E. A rig is the grid of columns and rows in a sprite sheet.

**Key:** A=F B=T C=F D=F E=F

**Why:**

- A: Bone weights belong to skinning of a mesh.
- B: Bones belong to a rig or skeleton, not to a grid of images.
- C: Inverse kinematics solves joint angles so a limb reaches a target.
- D: A skeleton belongs to a rig; a sprite sheet plays image frames.
- E: A rig is a skeleton of bones with a mesh bound to it.

**Source:** Spot the wrong word in an animation prompt

## MA-jargon.62

An agent is asked for two characters: one from a sprite sheet and one rigged in 3D. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The rigged instruction should name the cell size of the sheet.
- [ ] B. The rigged instruction names the skeleton, the clip, the loop mode, and in-place versus root motion.
- [ ] C. The sprite-sheet instruction names the grid, which frames play in what order, the frame rate and loop.
- [ ] D. Stating the method (sprite sheet or rig) up front removes a guess for the agent.
- [ ] E. The sprite-sheet instruction should name bone weights.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Cell size is a sprite sheet term.
- B: These terms define a bone-driven animation.
- C: Those terms define a flipbook animation.
- D: The two methods use different vocabulary and different tools.
- E: Bone weights apply to skinned meshes, not image grids.

**Source:** Sprite sheet instruction versus rig instruction

## MA-jargon.63

A walking character slides over the floor and also travels twice as far as expected. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An in-place clip keeps the root still and lets the script supply the travel.
- [ ] B. Sliding feet are fixed by raising delta time.
- [ ] C. Double distance can come from a root motion clip while the script also moves the body.
- [ ] D. The fix for double movement is to keep root motion and keep the script moving at walking speed.
- [ ] E. Root motion is movement baked into the clip that drives the character's root through the world.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: In-place is the choice for script-driven movement.
- B: Sliding is a mismatch between travel speed and the foot speed in the clip.
- C: Two sources of travel are added together.
- D: That keeps both sources of travel; one should be removed.
- E: The animation, not the script, supplies the travel.

**Source:** Root motion diagnosis

## MA-jargon.64

A bug report describes feet that slide while walking and a character that travels too far. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Root motion is the name for a clip that loops.
- [ ] B. Raising the script travel speed beyond the clip's foot speed reduces sliding.
- [ ] C. Using root motion and removing the script movement also fixes double movement.
- [ ] D. Using an in-place clip and letting the script move the body fixes double movement.
- [ ] E. Sliding is called tunnelling.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Looping is the loop mode; root motion is movement carried by the clip.
- B: Sliding grows when travel speed and foot speed differ.
- C: Only the clip supplies travel.
- D: Only the script supplies travel.
- E: Tunnelling is a fast body passing through a thin collider.

**Source:** Root motion fixes

## MA-jargon.65

A 3D character idles, walks, runs, jumps and lands. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A blend tree is a weighted mix of clips driven by a parameter such as speed.
- [ ] B. A transition is a named value that the logic reads.
- [ ] C. The gradual mix of idle, walk and run on speed suits a blend tree.
- [ ] D. Jump and land are best handled by a blend tree on speed.
- [ ] E. A state machine has named states with transitions, and one state is active at a time.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: It produces a smooth mix of motions.
- B: That is a parameter; a transition is a rule that moves between states.
- C: A continuous parameter drives a continuous mix.
- D: They are separate states reached by transitions.
- E: It models discrete modes such as jump and land.

**Source:** State machine versus blend tree

## MA-jargon.66

An agent is told to build the locomotion and jump logic. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A parameter is the rule that decides when to switch states.
- [ ] B. A blend tree has one active state and moves between states by transitions.
- [ ] C. A transition is a rule with a condition, such as "on the ground" changing to false.
- [ ] D. An instruction naming the parameter, the clips and the transition conditions removes guessing.
- [ ] E. A parameter is a named value, such as speed, that the logic reads.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: That is a transition.
- B: That describes a state machine.
- C: It decides when the active state changes.
- D: Each missing name would otherwise be a guess.
- E: Parameters feed transition conditions and blend trees.

**Source:** Transition and parameter

## MA-jargon.67

A designer says, "The jump feels unfair." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Coyote time forgives a jump press that came too early.
- [ ] B. Coyote time is a short grace window after leaving a ledge in which a jump is still allowed.
- [ ] C. A jump buffer remembers a jump press made just before landing and performs the jump on landing.
- [ ] D. Both are measured as short durations in seconds or frames.
- [ ] E. A jump buffer forgives a press made after walking off a ledge.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: Early presses are forgiven by the jump buffer.
- B: It forgives a press that came a little late.
- C: It forgives a press that came a little early.
- D: They are time windows.
- E: That is coyote time.

**Source:** Coyote time and jump buffer

## MA-jargon.68

A prompt adds coyote time and a jump buffer to a platformer. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The coyote window starts again when the player lands on the ground.
- [ ] B. Coyote time is measured in pixels.
- [ ] C. "Make the jump feel less unfair" is as precise as naming both features with durations.
- [ ] D. A buffered jump press is cleared once the jump has been performed.
- [ ] E. The jump buffer is the window used after leaving a ledge.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Landing restores the grace window for the next ledge.
- B: It is a duration.
- C: The vague phrase leaves features and values to a guess.
- D: Otherwise it would trigger a second jump.
- E: That is coyote time.

**Source:** Exact jump-forgiveness instruction

## MA-jargon.69

Two players report that movement code works on one machine and not another. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Delta time is the time since the previous frame.
- [ ] B. Delta time is the number of frames drawn each second.
- [ ] C. Speed is the size of the velocity.
- [ ] D. Velocity is speed together with a direction, so it is a vector.
- [ ] E. Acceleration is the rate at which velocity changes.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: It is the length of the last frame.
- B: That is frame rate.
- C: It is the magnitude without direction.
- D: Velocity carries a magnitude and a direction.
- E: It acts on velocity over time.

**Source:** Velocity, speed, acceleration and delta time

## MA-jargon.70

A character runs faster on a 144 frames per second monitor than on a 30 frames per second laptop. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The fix is to scale per-second speed by delta time.
- [ ] B. Running physics in a fixed timestep keeps physics updates at a constant rate.
- [ ] C. Frame-rate independent movement gives the same distance per second on both machines.
- [ ] D. The cause is that velocity was stored as a scalar.
- [ ] E. The cause is movement that adds a fixed amount each frame, so more frames give more distance per second.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Distance then follows real time.
- B: Physics steps no longer depend on the frame rate.
- C: That is what the term means.
- D: Storing velocity as a scalar does not tie movement to frames.
- E: The step is tied to frames, not to time.

**Source:** Delta time diagnosis

## MA-jargon.71

Choose the body or area type for each object in a level. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The player character moved by script is a static body.
- [ ] B. A tumbling crate pushed around by physics is a rigid body.
- [ ] C. A platform moved by a script or animation is a rigid body.
- [ ] D. A coin that detects overlap without blocking is a trigger.
- [ ] E. A wall that does not move is a static body.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: A script-controlled mover is kinematic, not static.
- B: A rigid body is simulated by the physics engine.
- C: A body moved by code or animation is kinematic.
- D: A trigger is a volume that reports overlap and does not block.
- E: Static bodies are fixed in place.

**Source:** Body types for level objects

## MA-jargon.72

A student mixes up the physics vocabulary. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A trigger is a volume that detects overlap without blocking.
- [ ] B. A trigger blocks movement like a wall.
- [ ] C. A collider is the shape used for contact tests.
- [ ] D. A static body falls under gravity when nothing supports it.
- [ ] E. A kinematic body is moved by physics forces and gravity.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: It reports entering and leaving.
- B: Blocking is the job of a solid collider.
- C: It describes where an object touches others.
- D: A static body does not move.
- E: A kinematic body is moved by code or animation.

**Source:** Collider, trigger and body definitions

## MA-jargon.73

A vague prompt says: "Make the player move nicely and the platforms work." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Nicely" is an exact term for tuning movement.
- [ ] B. The player can be named as a kinematic character body that is controlled by script.
- [ ] C. The rewrite says movement changes are scaled by delta time.
- [ ] D. The moving platform can be named as a static body.
- [ ] E. Velocity, acceleration, friction and gravity are movement-rule terms.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: It does not name a quantity that can be set or checked.
- B: Script-driven movement uses a kinematic body.
- C: This keeps movement independent of frame rate.
- D: A static body does not move; a moving platform is kinematic.
- E: They describe how motion is built up and slowed.

**Source:** Rewrite a vague movement prompt

## MA-jargon.74

After a movement rewrite, a tester lists checks and shapes. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A pickup zone is a trigger area.
- [ ] B. Standing on the moving platform and riding along tests that the platform carries the player.
- [ ] C. Measuring speed at 30 and 144 frames per second tests frame-rate independence.
- [ ] D. A capsule is a common collider shape for a character and a box for a simple platform.
- [ ] E. A pickup zone should be a rigid body that blocks the player.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: It detects the player without blocking.
- B: It checks the body type and contact.
- C: Equal speeds show delta time is applied.
- D: Shapes are chosen to match the object.
- E: A pickup should detect overlap, not block.

**Source:** Observable movement checks

## MA-jargon.75

A shader tutorial compares the pipeline stages and inputs. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A uniform is a value that changes for each vertex and is chosen by the vertex stage.
- [ ] B. UV is the 3D world position of a vertex.
- [ ] C. A vertex shader runs per vertex and sets positions.
- [ ] D. A fragment shader runs per vertex and sets positions.
- [ ] E. A varying is a value that the fragment stage sends back to the vertex stage.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: A uniform comes from game code and is the same across a draw call.
- B: UV is a 2D coordinate that maps a surface to a texture.
- C: It can move the vertices of a mesh.
- D: A fragment shader runs per pixel and sets colour.
- E: A varying passes from the vertex stage to the fragment stage and is interpolated.

**Source:** Shader stages and inputs

## MA-jargon.76

An artist wants a water wave and a surface glint, and a script to change them while the game runs. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A tint or glint on the surface is a fragment stage effect.
- [ ] B. A script sets a varying directly from game code each frame.
- [ ] C. A wave that displaces the mesh is a vertex stage effect.
- [ ] D. A script changes the effect while the game runs by setting a uniform each frame.
- [ ] E. UV coordinates are 2D values that map a surface to a texture.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: It changes pixel colour.
- B: Varyings come from the vertex stage.
- C: It changes positions.
- D: A uniform is the input from game code.
- E: They say which texture point goes where.

**Source:** Stage effects and script control

## MA-jargon.77

An artist who has never written a shader asks what the material words mean. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Emission is the blur of the reflections.
- [ ] B. Albedo is the base colour without lighting.
- [ ] C. Roughness controls whether highlights are sharp or blurry.
- [ ] D. Metallic describes how much the surface behaves like a metal.
- [ ] E. A normal map stores a per-pixel surface direction that fakes small bumps in lighting without moving geometry.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Emission is self-lit colour.
- B: It is the colour before lights act on it.
- C: Low roughness gives sharp highlights.
- D: It switches reflection behaviour between non-metal and metal.
- E: It changes shading and not the mesh.

**Source:** Material vocabulary

## MA-jargon.78

Describe a worn metal door with glowing warning lights in material terms. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A normal map can supply the dents.
- [ ] B. An emission colour can supply the glow of the lights.
- [ ] C. PBR means the material behaves consistently under different lights.
- [ ] D. Paint the dents by raising the metallic value.
- [ ] E. Bare metal parts use a high metallic value.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: It changes shading and not the mesh.
- B: Emission is self-lit colour.
- C: It is a physically based set-up.
- D: Dents are faked with a normal map.
- E: Metallic marks metal-like surfaces.

**Source:** Describe a material with exact terms

## MA-jargon.79

A student writes: "Use a normal map to make the lava glow and the fragment shader to move the vertices." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A normal map is the setting that makes a surface glow.
- [ ] B. Moving vertices is vertex shader work.
- [ ] C. A corrected instruction asks for emission on the lava and a vertex shader for the movement.
- [ ] D. Glow is emission, not a normal map.
- [ ] E. The fragment shader is the stage that moves vertices.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: It fakes small bumps in lighting.
- B: Vertex shaders set positions.
- C: Each effect is assigned to its proper term.
- D: Emission is self-lit colour.
- E: It sets pixel colour.

**Source:** Spot the wrong word in a shader prompt

## MA-jargon.80

An artist chooses a blend mode for rising smoke and for a glow. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Additive blending adds light to what is behind it, which suits a glow.
- [ ] B. Additive blending is the better choice for dark smoke.
- [ ] C. Alpha blending mixes by opacity, which suits smoke.
- [ ] D. Alpha blending adds light and brightens the overlap of layers.
- [ ] E. Additive blending darkens the area where layers overlap.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Glows brighten the background.
- B: Dark smoke needs to cover what is behind it, which is alpha blending.
- C: Semi-transparent smoke mixes with what is behind it.
- D: That describes additive blending.
- E: Additive blending brightens where layers overlap.

**Source:** Blend modes

## MA-jargon.81

An agent is asked for an enemy that patrols, chases and attacks. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A hurtbox is the area that deals the attack.
- [ ] B. A sight range is best made a solid collider that blocks the player.
- [ ] C. A hitbox is the area where an attack deals damage.
- [ ] D. A sight trigger area and an attack range can be the conditions for transitions.
- [ ] E. A state machine names patrol, chase and attack as states and defines the transitions between them.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: A hurtbox is where a character can be damaged.
- B: Sight detection is a trigger area, which does not block.
- C: It belongs to the attacker.
- D: They tell the machine when to change states.
- E: Each behaviour is one state at a time.

**Source:** Enemy state machine terms

## MA-jargon.82

A "say it to the agent" paragraph for the enemy uses exact terms. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. An animation state and the enemy's health are the same thing.
- [ ] B. "Make the enemy smart" gives the same detail as naming states and conditions.
- [ ] C. Without a named transition condition the agent has to guess when chase becomes attack.
- [ ] D. A hurtbox is where the enemy deals damage.
- [ ] E. Naming one animation clip per state, with a blend or transition between them, tells the agent how motion changes.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: An animation state is a mode of playback, and health is a value.
- B: It names no state or condition.
- C: The condition is what triggers the change.
- D: The hurtbox takes damage; the hitbox deals it.
- E: Clips are assigned to states.

**Source:** Say it to the agent: enemy behaviour
