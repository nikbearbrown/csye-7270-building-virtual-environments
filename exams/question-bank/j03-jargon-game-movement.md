# Jargon test: game movement

## MA-jargon.21

A student asks an agent for "faster movement" and gets the wrong change. Check each statement that is true about the movement terms. Each statement is worth 1 point (5 points total).

- [ ] A. Acceleration is the rate at which velocity changes.
- [ ] B. Acceleration is another word for speed.
- [ ] C. Speed is the direction of the velocity, with no size.
- [ ] D. Velocity is speed together with a direction, so it is a vector.
- [ ] E. Velocity is the distance travelled so far.

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: Acceleration changes velocity over time.
- B: Speed is how fast; acceleration is how quickly the speed changes.
- C: Speed is the size of the velocity; direction is the other part of velocity.
- D: Velocity has magnitude and direction.
- E: Distance travelled is a different quantity.

**Source:** Velocity, speed and acceleration

## MA-jargon.22

A game runs at 30 frames per second on one laptop and 144 on another, and the character moves at different speeds. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Delta time is the total time since the game started.
- [ ] B. Multiplying a per-second speed by delta time makes movement per frame match real time.
- [ ] C. Movement code that adds a fixed amount each frame gives the same real-time speed on both laptops.
- [ ] D. Delta time is the time that passed since the previous frame.
- [ ] E. Delta time is a setting that raises the frame rate.

**Key:** A=F B=T C=F D=T E=F

**Why:**

- A: That is elapsed time, not delta time.
- B: Scaling by delta time gives frame-rate independent movement.
- C: A fixed amount per frame covers more distance per second when more frames are drawn per second.
- D: Delta time is the length of the last frame.
- E: Delta time measures frames; it does not change them.

**Source:** Delta time and frame-rate independence

## MA-jargon.23

A platformer feels unfair because jumps fail by a hair. Check each statement that is true about the forgiveness terms. Each statement is worth 1 point (5 points total).

- [ ] A. A jump buffer helps a player who presses jump a moment early.
- [ ] B. Coyote time helps a player who presses jump a moment late.
- [ ] C. Coyote time makes the character fall more slowly after leaving a ledge.
- [ ] D. Coyote time is a short grace window after leaving a ledge in which a jump is still allowed.
- [ ] E. A jump buffer remembers a jump press made just before landing and performs the jump on landing.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Early presses are held until landing.
- B: Late presses still count inside the window.
- C: It changes when a jump is allowed, not the fall speed.
- D: Coyote time extends the ground check after the feet leave.
- E: The input is stored for a few frames and used when the character lands.

**Source:** Coyote time and jump buffer

## MA-jargon.24

A student types: "Make the jump forgiving." Check each rewrite that uses exact terms correctly. Each statement is worth 1 point (5 points total).

- [ ] A. "Add a jump buffer of 0.12 seconds so a press just before landing still jumps."
- [ ] B. "Add coyote time so the jump input is remembered until landing."
- [ ] C. "Add a jump buffer so the character can jump again after leaving the ground."
- [ ] D. "Add coyote time of 0.1 seconds after the character leaves a platform."
- [ ] E. "Set delta time to 0.1 so the jump lasts longer."

**Key:** A=T B=F C=F D=T E=F

**Why:**

- A: This is a jump buffer, named with its window.
- B: Remembering a press until landing is the jump buffer.
- C: A mid-air extra jump is a double jump, not a buffer.
- D: This is coyote time, named with its window.
- E: Delta time is measured, not a tuning value for jump length.

**Source:** Rewrite a vague jump prompt

## MA-jargon.25

A designer must choose between collision shapes and areas. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A collider shape is a copy of the visible mesh, triangle for triangle.
- [ ] B. A trigger detects that something overlapped it but does not block movement.
- [ ] C. A trigger stops a character the same way a wall collider does.
- [ ] D. A pickup coin is better made as a solid collider than as a trigger.
- [ ] E. A collider is a shape that the physics system uses to detect contact.

**Key:** A=F B=T C=F D=F E=T

**Why:**

- A: Colliders are usually simple shapes that approximate the mesh.
- B: Triggers report overlaps (often through an area or signal) without pushing back.
- C: A solid collider blocks; a trigger does not.
- D: Collecting needs detection without blocking, which is what a trigger does.
- E: Colliders define the shape used for collision tests.

**Source:** Collider versus trigger

## MA-jargon.26

A game has a moving platform, a crate that tumbles, and a player character. Check each statement that is true about body types. Each statement is worth 1 point (5 points total).

- [ ] A. A static body is moved around by applying impulses.
- [ ] B. A crate that should tumble under physics is a good fit for a static body.
- [ ] C. A rigid body is moved by the physics simulation using forces, mass and collisions.
- [ ] D. A kinematic body falls under gravity by itself without any code.
- [ ] E. A kinematic body is moved by code (or animation) and is not pushed around by forces.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A static body does not move.
- B: A static body does not move; a tumbling crate needs a rigid body.
- C: Rigid bodies are simulated.
- D: A kinematic body only moves when code moves it.
- E: Kinematic bodies obey the script, and can still push other bodies.

**Source:** Kinematic versus rigid body

## MA-jargon.27

An agent is told to "make the character slide to a stop instead of stopping dead". Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Acceleration also describes the speed-up from standing still when input starts.
- [ ] B. Gravity is a force that gives a steady downward acceleration.
- [ ] C. Deceleration changes the direction of the velocity but not its size.
- [ ] D. Setting velocity to zero when input stops gives an instant stop.
- [ ] E. Friction or deceleration reduces velocity over time when no input is held.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: Acceleration applies both for speeding up and slowing down.
- B: Gravity accelerates things downward.
- C: Deceleration reduces the size of velocity.
- D: An assignment to zero stops at once.
- E: Friction removes speed gradually.

**Source:** Friction, deceleration and gravity

## MA-jargon.28

A prompt reads: "Use delta time to make the kinematic body fall, and give it a trigger so it blocks the player." Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. The prompt is correct, since a trigger and a solid collider are the same.
- [ ] B. A kinematic body falls without code because physics owns it.
- [ ] C. A trigger does not block, so "trigger so it blocks the player" uses the wrong word; a collider blocks.
- [ ] D. A kinematic body does not fall by itself, so code has to add gravity to its velocity.
- [ ] E. Multiplying the gravity change by delta time keeps the fall the same at any frame rate.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: They differ in blocking behaviour.
- B: That is true of rigid bodies only.
- C: Blocking is done by a collider; a trigger only detects.
- D: Kinematic bodies rely on code for their motion.
- E: Scaling by delta time makes the result independent of frame rate.

**Source:** Spot the wrong word in a movement prompt

## MA-jargon.29

A student must write the exact words for platformer jump feel. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Terminal velocity is the speed at the start of a jump.
- [ ] B. Coyote time and a double jump are the same feature.
- [ ] C. Terminal velocity is the highest fall speed the character is allowed to reach.
- [ ] D. Variable jump height lets a short press give a low jump and a long press give a high jump.
- [ ] E. A double jump is an extra jump allowed while in the air.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: Terminal velocity is a cap on falling speed.
- B: One is a grace window on the ground edge, the other an additional jump.
- C: The fall speed is capped.
- D: The jump is cut short when the button is released early.
- E: A double jump spends an extra mid-air jump.

**Source:** Jump-feel vocabulary

## MA-jargon.30

A student asks for "smooth physics" and must say which update loop to use. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Tunnelling is when a fast object passes through a thin collider without a hit being detected.
- [ ] B. A fixed timestep removes the need for colliders.
- [ ] C. A fixed timestep runs physics at a steady interval regardless of how fast frames are drawn.
- [ ] D. Movement of physics bodies belongs in the fixed-timestep step in most engines.
- [ ] E. A per-frame update runs once per drawn frame, so its interval varies.

**Key:** A=T B=F C=T D=T E=T

**Why:**

- A: Tunnelling happens when an object moves farther than a collider's thickness in one step.
- B: Colliders are still needed for contact tests.
- C: Fixed steps give stable simulation.
- D: Physics calls such as moving bodies are made in the physics step.
- E: Frame time varies, so per-frame steps vary.

**Source:** Fixed timestep and tunnelling

