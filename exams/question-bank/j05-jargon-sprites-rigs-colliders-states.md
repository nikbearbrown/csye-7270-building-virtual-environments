# Jargon test: sprite sheets, rigs, colliders and state machines

## MA-jargon.43

A team debates the method for each character. Check each statement that is true about sprite-sheet and rig-based animation. Each statement is worth 1 point (5 points total).

- [ ] A. A sprite sheet holds drawn frames, and the animation shows them one after another.
- [ ] B. Characters that share a skeleton can share clips, which separate drawn sprite-sheet frames do not.
- [ ] C. A rig-based clip stores a separate picture for each frame.
- [ ] D. A rig-based animation changes bone transforms, and the mesh follows the bones.
- [ ] E. A sprite sheet stores a skeleton and skinning weights.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Sprite animation is a flipbook of images.
- B: Clips apply to any character with a matching skeleton.
- C: Rig clips store transforms over time, not images.
- D: Skeletal animation poses bones.
- E: Skeleton data belongs to rigs.

**Source:** Sprite sheet versus rig

## MA-jargon.44

An agent must slice and play a sprite sheet. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A frame is one image cell in the sheet.
- [ ] B. Frame order matters, so a prompt should say which cells make the walk and in what order.
- [ ] C. Setting an animation to loop makes it restart after the last frame.
- [ ] D. Frame rate and playback loop are the same setting.
- [ ] E. A sheet of 6 columns and 2 rows holds 12 frames if every cell is used.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Each cell is a frame.
- B: The order is part of the animation.
- C: Looping repeats the sequence.
- D: Frame rate is speed; looping is repeat behaviour.
- E: Six times two is twelve.

**Source:** Sprite sheet slicing

## MA-jargon.45

Two designers argue about blocking and detecting. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A trigger zone around a door blocks the player until the door opens.
- [ ] B. A trigger zone moves the player back out when the player enters it.
- [ ] C. A collision shape on a wall lets characters walk through it while the engine reports an overlap.
- [ ] D. Collision layers and masks choose which kinds of objects can touch each other.
- [ ] E. Collision layers change the colour of the objects.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: A trigger detects overlap and does not block; blocking is a solid collider's job.
- B: Triggers do not push.
- C: A solid collider blocks; reporting an overlap without blocking is a trigger.
- D: Layers say what an object is; masks say what it looks for.
- E: Layers have nothing to do with colour.

**Source:** Collider, trigger and layers

## MA-jargon.46

A student says "enemy hits" and the agent builds the wrong thing. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A hitbox is normally a trigger, since it needs to detect an overlap and not block.
- [ ] B. A hitbox is an area on an attacker that deals damage when it overlaps a target.
- [ ] C. A hurtbox is an area on a character that can receive damage.
- [ ] D. A hurtbox is the weapon area that deals the damage.
- [ ] E. A hitbox and a hurtbox are the same area with two names.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: Detection is enough, so triggers fit.
- B: A hitbox is the attack volume.
- C: A hurtbox is the vulnerable volume.
- D: The weapon area is the hitbox.
- E: They play opposite roles.

**Source:** Hitbox and hurtbox

## MA-jargon.47

A character needs states for idle, run, jump and fall. Check each statement that is true about state machines. Each statement is worth 1 point (5 points total).

- [ ] A. A state machine is in exactly one current state at a time.
- [ ] B. A transition is the animation clip played inside a state.
- [ ] C. A transition is a rule that moves the machine from one state to another when a condition becomes true.
- [ ] D. A state machine runs its states in parallel.
- [ ] E. A state machine replaces a pile of nested if checks with named states and transitions.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: One state is active at once.
- B: A clip belongs to a state; a transition is the link between states.
- C: Transitions carry conditions.
- D: Only the current state is active.
- E: Named states make behaviour easier to read and extend.

**Source:** State machine

## MA-jargon.48

An agent is asked to code enemy behaviour. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Chase and attack are transitions, not states.
- [ ] B. A transition from patrol to chase could fire when the player enters the enemy's sight range.
- [ ] C. An enter or exit action runs once when the machine enters or leaves a state.
- [ ] D. A state machine for an enemy needs a separate script per frame.
- [ ] E. A finite state machine for an enemy might have patrol, chase and attack states.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: They are states; the arrows between them are transitions.
- B: Sight is a typical transition condition.
- C: Entry and exit actions mark the edges of a state.
- D: The machine runs on updates; no per-frame script is needed.
- E: These are typical states.

**Source:** Enemy state machine

## MA-jargon.49

A student must rewrite "make the player move and animate properly". Check each rewrite that uses exact terms correctly. Each statement is worth 1 point (5 points total).

- [ ] A. "Slice the rig into a 4 by 4 grid and set its bones to loop."
- [ ] B. "Make the player a kinematic body that reads input, applies acceleration and gravity scaled by delta time, and moves with collision."
- [ ] C. "Use a state machine with idle, run, jump and fall states, each playing its clip."
- [ ] D. "Make the player a trigger so walls block it."
- [ ] E. "Add a trigger area as the player's hurtbox so enemy hitboxes can detect it."

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: Grids belong to sprite sheets and loops belong to clips.
- B: This names the body type, forces, delta time and collision.
- C: States and clips map cleanly to the player's modes.
- D: A trigger does not get blocked by walls.
- E: A hurtbox area that is a trigger detects overlapping hitboxes.

**Source:** Rewrite a vague gameplay prompt

## MA-jargon.50

A student reads an agent's plan and must spot imprecise words. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. "Blend the idle and run clips with a blend tree on speed" uses the terms correctly.
- [ ] B. "The tween stores a keyframe in a rig" describes how a tween works.
- [ ] C. "The camera pans toward the boss by moving closer" mixes up pan and dolly.
- [ ] D. "The fragment shader displaces each vertex" gives the wrong stage.
- [ ] E. "The coin is a solid collider so it detects pickups" should say the coin is a trigger.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: This is the right use of blend tree and parameter.
- B: A tween is a code interpolation; keyframes live in clips.
- C: Moving closer is a dolly.
- D: Vertices belong to the vertex stage.
- E: Detecting pickups is trigger behaviour.

**Source:** Spot the imprecise word

