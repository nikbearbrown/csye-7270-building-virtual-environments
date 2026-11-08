# CSYE 7270 Building Virtual Environments: practice exam 04

**PRACTICE FORM. Drawn at random from the question bank; not the real exam; not signed off by the instructor.**

20 questions, 5 points each, 100 points. Name: ______________________

**Scoring.** Five statements, each true or false, 1 point each. The student checks the statements they believe are true. A statement scores 1 point if it is checked and true, or unchecked and false; otherwise 0. Read every statement on its own and decide whether it is true by itself. Strong words (always, never, every, proves) are often what makes a statement false, but a strong-sounding statement is not false for sounding strong.

---

**1.** A tool reports a successful scene edit, but after closing and reopening the project the change is gone. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. A success result can describe a completed mutation without a completed save.
- [ ] B. In-memory state is the scene as the open editor holds it, and saved state is the scene file on disk.
- [ ] C. The missing change shows the language model forgot the scene.
- [ ] D. Reopening the saved scene is a persistence check.
- [ ] E. A dirty scene is one with unsaved changes.

**2.** Which statements give the correct meaning of the three server primitives? Check each statement that is true.  *(5 points)*

- [ ] A. A tool is an operation the model can invoke with arguments, and it may have side effects.
- [ ] B. A prompt is a reusable message or workflow template that a server offers.
- [ ] C. A tool is readable content identified by a URI.
- [ ] D. A prompt is the text the model writes back to the user.
- [ ] E. A resource is an operation that changes the scene when it is called.

**3.** A headless test script is supposed to call a quit function after its last check. A bug raises an error before the quit call is reached, and the engine keeps running its main loop with no window to close. Check each statement that is true.  *(5 points)*

- [ ] A. Running the command under a timeout utility turns a stuck test into a failure after a set number of seconds.
- [ ] B. A sensible timeout is longer than a healthy run takes, with some margin.
- [ ] C. The process can run indefinitely: nothing tells it to stop and no window exists to close.
- [ ] D. A timeout speeds up a slow test by telling the engine to skip waiting between frames.
- [ ] E. Because the script's last line calls quit, a timeout adds no protection.

**4.** A developer asks a coding agent: "Make the enemy move right 5 pixels every frame." The agent writes position.x += 5 in the per-frame update function, and the game is tested on a 60 Hz screen and a 144 Hz screen. Check each statement that is true.  *(5 points)*

- [ ] A. Delta time is the count of frames drawn in the last second.
- [ ] B. position.x += 5 is movement per frame, so the enemy covers more distance per second when more frames are drawn each second.
- [ ] C. Movement of 5 pixels per frame is frame-rate independent, so the enemy looks the same speed at 60 and at 144 frames per second.
- [ ] D. Asking for "move right at 300 pixels per second" and writing position.x += 300 * delta gives the same on-screen speed at 60 and at 144 frames per second.
- [ ] E. Multiplying a step by delta changes its unit from "per frame" to "per second", so the number 5 may need to be raised to keep the old speed.

**5.** A game prompt says "make the camera follow the player". Check each statement that is true about the terms involved.  *(5 points)*

- [ ] A. An orbit moves the camera around a subject along a curved path while the subject stays framed.
- [ ] B. Smoothing (damping) on a follow camera makes it jump straight onto the target in a single frame.
- [ ] C. An orbit and a pan are the same move, because both rotate the camera.
- [ ] D. A follow camera and a camera that stays in one place and only turns to face the target are the same thing.
- [ ] E. A follow camera keeps tracking a moving target, usually with some smoothing.

**6.** A shared editor service has reviewer and builder roles. Reviewers inspect, and builders edit one level but cannot publish. Check each statement that is true.  *(5 points)*

- [ ] A. Deny by default means an operation is refused unless a rule allows it.
- [ ] B. Publishing is part of the permission to edit a level.
- [ ] C. An authenticated builder has the right to publish.
- [ ] D. Enforcing a role in the user interface is enforcement at the service.
- [ ] E. Role-based access control grants permissions through roles such as reviewer and builder.

**7.** A RigidBody2D needs a one-time knockback of 400 pixels per second away from a hit, and also a constant thruster push. Check each statement that is correct.  *(5 points)*

- [ ] A. The knockback is a force applied for a single physics step.
- [ ] B. For a body with mass, an impulse gives a smaller velocity change to a heavier body.
- [ ] C. The knockback is an impulse, an instant change of velocity.
- [ ] D. The thruster is a force applied on every physics step, changing velocity gradually.
- [ ] E. Multiplying the impulse by delta makes the knockback weaker and dependent on frame rate.

**8.** A student asks an agent for "faster movement" and gets the wrong change. Check each statement that is true about the movement terms.  *(5 points)*

- [ ] A. Acceleration is the rate at which velocity changes.
- [ ] B. Acceleration is another word for speed.
- [ ] C. Speed is the direction of the velocity, with no size.
- [ ] D. Velocity is speed together with a direction, so it is a vector.
- [ ] E. Velocity is the distance travelled so far.

**9.** A student must rewrite "make the player move and animate properly". Check each rewrite that uses exact terms correctly.  *(5 points)*

- [ ] A. "Slice the rig into a 4 by 4 grid and set its bones to loop."
- [ ] B. "Make the player a kinematic body that reads input, applies acceleration and gravity scaled by delta time, and moves with collision."
- [ ] C. "Use a state machine with idle, run, jump and fall states, each playing its clip."
- [ ] D. "Make the player a trigger so walls block it."
- [ ] E. "Add a trigger area as the player's hurtbox so enemy hitboxes can detect it."

**10.** A student must tell an agent which shader stage to edit. Check each statement that is true.  *(5 points)*

- [ ] A. A vertex shader runs once per vertex and decides where that vertex ends up on screen.
- [ ] B. Tinting every pixel of a surface by distance to the player is a job for the fragment shader.
- [ ] C. Making a flag wave by moving its mesh points is a job for the vertex shader.
- [ ] D. A fragment shader runs once per covered pixel (fragment) and decides its colour.
- [ ] E. A fragment shader runs once per vertex of the mesh.

**11.** A bug report describes feet that slide while walking and a character that travels too far. Check each statement that is true.  *(5 points)*

- [ ] A. Root motion is the name for a clip that loops.
- [ ] B. Raising the script travel speed beyond the clip's foot speed reduces sliding.
- [ ] C. Using root motion and removing the script movement also fixes double movement.
- [ ] D. Using an in-place clip and letting the script move the body fixes double movement.
- [ ] E. Sliding is called tunnelling.

**12.** An agent says "the edit is atomic" after changing three script files for one feature. Check each statement that is correct.  *(5 points)*

- [ ] A. An atomic edit means the change is small, such as one line.
- [ ] B. A claim that the edit is atomic does not say the edit was tested, so the agent still runs the tests.
- [ ] C. An atomic commit groups one logical change, which may touch several files.
- [ ] D. An atomic edit is applied completely or not at all, with no half-applied state left behind.
- [ ] E. If an atomic multi-file change fails on the third file, the first two files are restored.

**13.** An agent reports: "Replaced the AnimationTree state machine with a blend tree so the attack plays when the button is pressed." Check each statement that is true.  *(5 points)*

- [ ] A. The change fits poorly: an attack that interrupts movement is a discrete change of state, which a state machine with transitions expresses.
- [ ] B. A follow-up that gives evidence is: press attack while running and report which animation is playing on the next frame.
- [ ] C. A follow-up that gives evidence is: ask the agent to explain the difference between the two in a paragraph.
- [ ] D. A state machine suits mixing walk and run by a speed value, which is why it was replaced.
- [ ] E. The change is right because a blend tree can trigger clips from button presses by itself.

**14.** A student rewrites the vague prompt "animate the character walking". Check each rewrite that uses the exact terms for a 3D rigged character correctly.  *(5 points)*

- [ ] A. "Play the walk clip from the rig, looping, in place, and move the body in script at the speed value."
- [ ] B. "Cut the walk clip into a 4 by 2 grid and show each cell for 100 ms."
- [ ] C. "Give the walk clip a frame rate of 12 and a sprite sheet of 8 bones."
- [ ] D. "Rotate the walk of the rig by tweening its UV."
- [ ] E. "Add a blend tree on the speed parameter that mixes the idle, walk and run clips."

**15.** A test oracle is the source of the expected result in a test. Check each statement that is true about oracles and checks.  *(5 points)*

- [ ] A. Deliberately breaking the activation path to see the test fail checks that the test can detect the bug.
- [ ] B. An oracle taken from the code under test is not independent.
- [ ] C. A negative case proves that the positive case works.
- [ ] D. A tolerance lets a position comparison pass when the difference is small.
- [ ] E. Floating-point positions are compared with exact equality because they are stored with perfect precision.

**16.** An agent reports work done after several checks. Check the vocabulary used about verification. Check each statement that is true.  *(5 points)*

- [ ] A. Compile and play test name the same activity.
- [ ] B. Acceptance criteria are conditions that define when work counts as done.
- [ ] C. A smoke test is a long review of rare edge cases.
- [ ] D. Diagnostics are the assets a test places in the level.
- [ ] E. To validate an asset is to check it against rules, and to test is to run it and observe behaviour.

**17.** After a script change, an agent plans its repair steps. Which statements use the terms correctly? Check each statement that is true.  *(5 points)*

- [ ] A. Suppressing the error message counts as addressing the diagnostics.
- [ ] B. The sequence is compile, reload, inspect the component, set the field, read it back, then test the behaviour.
- [ ] C. A read-back means reading the value from the editor after setting it.
- [ ] D. Compiler diagnostics are the messages that name the location and cause of an error.
- [ ] E. Reading the script file's text is equivalent to a read-back from the component.

**18.** A designer asks an agent, "Hook the AI up to the lighting stuff." Which statements are exact rewrites? Check each statement that is true.  *(5 points)*

- [ ] A. Expose create-light as a tool with arguments for target scene and intensity.
- [ ] B. Expose the scene inventory as a resource.
- [ ] C. Reading the inventory resource first lets the agent choose where to call the create-light tool.
- [ ] D. Expose the review checklist as a resource that runs the review when read.
- [ ] E. Expose the reusable checklist as a prompt template.

**19.** A modelling tool treats +Z as up, while glTF and Godot treat +Y as up. Check each statement that is true about the terms.  *(5 points)*

- [ ] A. Blender uses +Z as up, while glTF and Godot use +Y as up.
- [ ] B. Unreal's editor treats +Z as up, as Blender does.
- [ ] C. Up axis names which axis points up; handedness names whether the axes follow a right-hand or left-hand rule.
- [ ] D. A model that lies on its side after import suggests the up axis was not converted on export.
- [ ] E. Up axis and handedness are two names for the same setting.

**20.** A designer wants a health bar to float 40 units above an enemy's head, follow the enemy as it walks and turns, and still be right when the enemy is scaled up to be a boss. The bar is made a child of the enemy. Check each statement that is true.  *(5 points)*

- [ ] A. A local position of (0, 0) places the child at the world origin.
- [ ] B. The bar's local position is measured relative to its parent, so a fixed local offset of 40 units up stays the same while the bar's world position changes as the enemy walks.
- [ ] C. When the parent is rotated, the engine rotates the child's local offset with it, so the bar swings around the enemy.
- [ ] D. When the parent is scaled up, the child's local offset is scaled with it, so the bar sits farther away unless scale inheritance is handled.
- [ ] E. World (global) space measures positions from the parent object's own origin.
