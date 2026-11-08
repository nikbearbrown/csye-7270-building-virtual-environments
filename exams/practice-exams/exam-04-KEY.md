# CSYE 7270 Building Virtual Environments: practice exam 04: KEY

Total 100 points. Statement key: T = true (check it), F = false (leave it blank).

---

**1.** A tool reports a successful scene edit, but after closing and reopening the project the change is gone. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. A success result can describe a completed mutation without a completed save.
- [ ] B. In-memory state is the scene as the open editor holds it, and saved state is the scene file on disk.
- [ ] C. The missing change shows the language model forgot the scene.
- [ ] D. Reopening the saved scene is a persistence check.
- [ ] E. A dirty scene is one with unsaved changes.

**Key:** A=T B=T C=F D=T E=T  |  `MA-unity.12`  |  *Unity, Spark and agent workflows*  |  source: in-memory versus saved

- A (true): The tool contract defines what success covers.
- B (true): They can differ until a save.
- C (false): Persistence is an editor and storage matter.
- D (true): It tests whether the change survives a reload.
- E (true): The editor marks such scenes as dirty.

**2.** Which statements give the correct meaning of the three server primitives? Check each statement that is true.  *(5 points)*

- [ ] A. A tool is an operation the model can invoke with arguments, and it may have side effects.
- [ ] B. A prompt is a reusable message or workflow template that a server offers.
- [ ] C. A tool is readable content identified by a URI.
- [ ] D. A prompt is the text the model writes back to the user.
- [ ] E. A resource is an operation that changes the scene when it is called.

**Key:** A=T B=T C=F D=F E=F  |  `MA-mcp.4`  |  *MCP fundamentals*  |  source: tool, resource, prompt definitions

- A (true): Tools perform actions.
- B (true): Prompts are templates the client can retrieve.
- C (false): That describes a resource.
- D (false): That is the model's reply, not a prompt primitive.
- E (false): A resource supplies readable context; it is not an action.

**3.** A headless test script is supposed to call a quit function after its last check. A bug raises an error before the quit call is reached, and the engine keeps running its main loop with no window to close. Check each statement that is true.  *(5 points)*

- [ ] A. Running the command under a timeout utility turns a stuck test into a failure after a set number of seconds.
- [ ] B. A sensible timeout is longer than a healthy run takes, with some margin.
- [ ] C. The process can run indefinitely: nothing tells it to stop and no window exists to close.
- [ ] D. A timeout speeds up a slow test by telling the engine to skip waiting between frames.
- [ ] E. Because the script's last line calls quit, a timeout adds no protection.

**Key:** A=T B=T C=T D=F E=F  |  `MA-ch00.4`  |  *None*  |  source: Timeouts

- A (true): A timeout turns a hang into a detectable failure.
- B (true): A limit that is too short kills healthy runs and creates false failures.
- C (true): With no quit call and no window, the main loop does not end by itself.
- D (false): A timeout stops the run when the limit is hit; it does not speed anything up.
- E (false): If an error stops execution before that line, the quit call is not reached.

**4.** A developer asks a coding agent: "Make the enemy move right 5 pixels every frame." The agent writes position.x += 5 in the per-frame update function, and the game is tested on a 60 Hz screen and a 144 Hz screen. Check each statement that is true.  *(5 points)*

- [ ] A. Delta time is the count of frames drawn in the last second.
- [ ] B. position.x += 5 is movement per frame, so the enemy covers more distance per second when more frames are drawn each second.
- [ ] C. Movement of 5 pixels per frame is frame-rate independent, so the enemy looks the same speed at 60 and at 144 frames per second.
- [ ] D. Asking for "move right at 300 pixels per second" and writing position.x += 300 * delta gives the same on-screen speed at 60 and at 144 frames per second.
- [ ] E. Multiplying a step by delta changes its unit from "per frame" to "per second", so the number 5 may need to be raised to keep the old speed.

**Key:** A=F B=T C=F D=T E=T  |  `MA-vocab.11`  |  *Engine vocabulary (Godot, Unity, Unreal)*  |  source: Frame-rate independence

- A (false): Delta time is a duration in seconds, not a count of frames.
- B (true): A fixed step per frame makes speed depend on the number of frames per second.
- C (false): A per-frame step is the textbook example of movement that is not frame-rate independent.
- D (true): A rate in units per second scaled by the time per frame covers the same distance per second at any frame rate.
- E (true): With delta, the number is a rate per second, so a per-frame value needs converting.

**5.** A game prompt says "make the camera follow the player". Check each statement that is true about the terms involved.  *(5 points)*

- [ ] A. An orbit moves the camera around a subject along a curved path while the subject stays framed.
- [ ] B. Smoothing (damping) on a follow camera makes it jump straight onto the target in a single frame.
- [ ] C. An orbit and a pan are the same move, because both rotate the camera.
- [ ] D. A follow camera and a camera that stays in one place and only turns to face the target are the same thing.
- [ ] E. A follow camera keeps tracking a moving target, usually with some smoothing.

**Key:** A=T B=F C=F D=F E=T  |  `MA-jargon.4`  |  *Jargon test: camera movement*  |  source: Orbit and follow camera

- A (true): In an orbit the camera body travels around the subject.
- B (false): Smoothing spreads the catch-up over time, so the camera trails slightly instead of jumping.
- C (false): A pan turns the camera in place; an orbit changes the camera position.
- D (false): A camera that only turns toward a target is a look-at (or fixed tracking) camera; a follow camera also changes position.
- E (true): A follow camera moves with its target; smoothing softens the motion.

**6.** A shared editor service has reviewer and builder roles. Reviewers inspect, and builders edit one level but cannot publish. Check each statement that is true.  *(5 points)*

- [ ] A. Deny by default means an operation is refused unless a rule allows it.
- [ ] B. Publishing is part of the permission to edit a level.
- [ ] C. An authenticated builder has the right to publish.
- [ ] D. Enforcing a role in the user interface is enforcement at the service.
- [ ] E. Role-based access control grants permissions through roles such as reviewer and builder.

**Key:** A=T B=F C=F D=F E=T  |  `MA-security.16`  |  *Agent security and local versus cloud execution*  |  source: Roles and enforcement

- A (true): Unlisted operations are blocked.
- B (false): They are separate permissions.
- C (false): Publishing is a separate permission.
- D (false): The service has to check the call.
- E (true): Roles bundle permissions.

**7.** A RigidBody2D needs a one-time knockback of 400 pixels per second away from a hit, and also a constant thruster push. Check each statement that is correct.  *(5 points)*

- [ ] A. The knockback is a force applied for a single physics step.
- [ ] B. For a body with mass, an impulse gives a smaller velocity change to a heavier body.
- [ ] C. The knockback is an impulse, an instant change of velocity.
- [ ] D. The thruster is a force applied on every physics step, changing velocity gradually.
- [ ] E. Multiplying the impulse by delta makes the knockback weaker and dependent on frame rate.

**Key:** A=F B=T C=T D=T E=T  |  `MA-k01.18`  |  *Jargon test: compress and decompress*  |  source: Impulse versus force

- A (false): A force acts over time, so one step gives a small, frame-dependent change instead of a fixed 400 pixels per second kick.
- B (true): An impulse changes momentum, so the velocity change is the impulse divided by mass.
- C (true): A one-time kick is an impulse, applied once to change the body's velocity immediately.
- D (true): A continuous push is a force applied each step, building speed over time.
- E (true): An impulse is not a per-second quantity, so scaling it by delta shrinks it and varies it with frame rate.

**8.** A student asks an agent for "faster movement" and gets the wrong change. Check each statement that is true about the movement terms.  *(5 points)*

- [ ] A. Acceleration is the rate at which velocity changes.
- [ ] B. Acceleration is another word for speed.
- [ ] C. Speed is the direction of the velocity, with no size.
- [ ] D. Velocity is speed together with a direction, so it is a vector.
- [ ] E. Velocity is the distance travelled so far.

**Key:** A=T B=F C=F D=T E=F  |  `MA-jargon.21`  |  *Jargon test: game movement*  |  source: Velocity, speed and acceleration

- A (true): Acceleration changes velocity over time.
- B (false): Speed is how fast; acceleration is how quickly the speed changes.
- C (false): Speed is the size of the velocity; direction is the other part of velocity.
- D (true): Velocity has magnitude and direction.
- E (false): Distance travelled is a different quantity.

**9.** A student must rewrite "make the player move and animate properly". Check each rewrite that uses exact terms correctly.  *(5 points)*

- [ ] A. "Slice the rig into a 4 by 4 grid and set its bones to loop."
- [ ] B. "Make the player a kinematic body that reads input, applies acceleration and gravity scaled by delta time, and moves with collision."
- [ ] C. "Use a state machine with idle, run, jump and fall states, each playing its clip."
- [ ] D. "Make the player a trigger so walls block it."
- [ ] E. "Add a trigger area as the player's hurtbox so enemy hitboxes can detect it."

**Key:** A=F B=T C=T D=F E=T  |  `MA-jargon.49`  |  *Jargon test: sprite sheets, rigs, colliders and state machines*  |  source: Rewrite a vague gameplay prompt

- A (false): Grids belong to sprite sheets and loops belong to clips.
- B (true): This names the body type, forces, delta time and collision.
- C (true): States and clips map cleanly to the player's modes.
- D (false): A trigger does not get blocked by walls.
- E (true): A hurtbox area that is a trigger detects overlapping hitboxes.

**10.** A student must tell an agent which shader stage to edit. Check each statement that is true.  *(5 points)*

- [ ] A. A vertex shader runs once per vertex and decides where that vertex ends up on screen.
- [ ] B. Tinting every pixel of a surface by distance to the player is a job for the fragment shader.
- [ ] C. Making a flag wave by moving its mesh points is a job for the vertex shader.
- [ ] D. A fragment shader runs once per covered pixel (fragment) and decides its colour.
- [ ] E. A fragment shader runs once per vertex of the mesh.

**Key:** A=T B=T C=T D=T E=F  |  `MA-jargon.31`  |  *Jargon test: shaders and materials*  |  source: Vertex versus fragment shader

- A (true): The vertex stage outputs the position of each vertex.
- B (true): Per-pixel colour is fragment work.
- C (true): Displacing vertices changes the shape, which is vertex work.
- D (true): The fragment stage outputs colour per fragment.
- E (false): Per-vertex execution describes the vertex shader.

**11.** A bug report describes feet that slide while walking and a character that travels too far. Check each statement that is true.  *(5 points)*

- [ ] A. Root motion is the name for a clip that loops.
- [ ] B. Raising the script travel speed beyond the clip's foot speed reduces sliding.
- [ ] C. Using root motion and removing the script movement also fixes double movement.
- [ ] D. Using an in-place clip and letting the script move the body fixes double movement.
- [ ] E. Sliding is called tunnelling.

**Key:** A=F B=F C=T D=T E=F  |  `MA-jargon.64`  |  *Jargon test: from the essay prompts*  |  source: Root motion fixes

- A (false): Looping is the loop mode; root motion is movement carried by the clip.
- B (false): Sliding grows when travel speed and foot speed differ.
- C (true): Only the clip supplies travel.
- D (true): Only the script supplies travel.
- E (false): Tunnelling is a fast body passing through a thin collider.

**12.** An agent says "the edit is atomic" after changing three script files for one feature. Check each statement that is correct.  *(5 points)*

- [ ] A. An atomic edit means the change is small, such as one line.
- [ ] B. A claim that the edit is atomic does not say the edit was tested, so the agent still runs the tests.
- [ ] C. An atomic commit groups one logical change, which may touch several files.
- [ ] D. An atomic edit is applied completely or not at all, with no half-applied state left behind.
- [ ] E. If an atomic multi-file change fails on the third file, the first two files are restored.

**Key:** A=F B=T C=T D=T E=T  |  `MA-k03.5`  |  *Jargon test: false friends*  |  source: Atomic (false friend)

- A (false): Atomic describes completeness of application rather than size, so an agent treating it as small would accept a half-applied large edit.
- B (true): Atomicity and testing are separate properties, and relying on the word alone would let broken code be accepted.
- C (true): Here atomic refers to a single coherent change, so three related scripts can belong in one atomic commit.
- D (true): Atomic means all or nothing, so a failed edit must leave the project exactly as it was.
- E (true): All-or-nothing behaviour means partial results are rolled back, so the project does not end in a mixed state.

**13.** An agent reports: "Replaced the AnimationTree state machine with a blend tree so the attack plays when the button is pressed." Check each statement that is true.  *(5 points)*

- [ ] A. The change fits poorly: an attack that interrupts movement is a discrete change of state, which a state machine with transitions expresses.
- [ ] B. A follow-up that gives evidence is: press attack while running and report which animation is playing on the next frame.
- [ ] C. A follow-up that gives evidence is: ask the agent to explain the difference between the two in a paragraph.
- [ ] D. A state machine suits mixing walk and run by a speed value, which is why it was replaced.
- [ ] E. The change is right because a blend tree can trigger clips from button presses by itself.

**Key:** A=T B=T C=F D=F E=F  |  `MA-k02.23`  |  *Jargon test: reading agent output*  |  source: State machine versus blend tree

- A (true): A state machine switches between named states on events, which matches the attack interrupting movement.
- B (true): The playing animation after the press shows whether the attack interrupts movement.
- C (false): A written explanation is not a behaviour test, so a broken attack would pass.
- D (false): Mixing by a continuous speed value is blend tree work; a state machine only switches between clips.
- E (false): A blend tree mixes animations by parameters and has no transitions to react to an event.

**14.** A student rewrites the vague prompt "animate the character walking". Check each rewrite that uses the exact terms for a 3D rigged character correctly.  *(5 points)*

- [ ] A. "Play the walk clip from the rig, looping, in place, and move the body in script at the speed value."
- [ ] B. "Cut the walk clip into a 4 by 2 grid and show each cell for 100 ms."
- [ ] C. "Give the walk clip a frame rate of 12 and a sprite sheet of 8 bones."
- [ ] D. "Rotate the walk of the rig by tweening its UV."
- [ ] E. "Add a blend tree on the speed parameter that mixes the idle, walk and run clips."

**Key:** A=T B=F C=F D=F E=T  |  `MA-jargon.19`  |  *Jargon test: animation movement*  |  source: Rewrite a vague animation prompt

- A (true): This names the clip, loop mode, root handling and who moves the body.
- B (false): Cutting into a grid describes a sprite sheet, not a rigged clip.
- C (false): A sprite sheet has frames, not bones; the terms are mixed up.
- D (false): UV is a texture coordinate and is not a thing to rotate to make a walk.
- E (true): Blending clips by a parameter is the tool for idle, walk and run.

**15.** A test oracle is the source of the expected result in a test. Check each statement that is true about oracles and checks.  *(5 points)*

- [ ] A. Deliberately breaking the activation path to see the test fail checks that the test can detect the bug.
- [ ] B. An oracle taken from the code under test is not independent.
- [ ] C. A negative case proves that the positive case works.
- [ ] D. A tolerance lets a position comparison pass when the difference is small.
- [ ] E. Floating-point positions are compared with exact equality because they are stored with perfect precision.

**Key:** A=T B=T C=F D=T E=F  |  `MA-verification.18`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Test oracle, tolerance, negative case

- A (true): A test that cannot fail on broken code gives false confidence.
- B (true): An independent oracle comes from the requirement, not from the implementation.
- C (false): Each case tests its own path.
- D (true): A tolerance is an allowed difference for numeric results.
- E (false): Floating-point results often differ in the last digits, so a tolerance is used.

**16.** An agent reports work done after several checks. Check the vocabulary used about verification. Check each statement that is true.  *(5 points)*

- [ ] A. Compile and play test name the same activity.
- [ ] B. Acceptance criteria are conditions that define when work counts as done.
- [ ] C. A smoke test is a long review of rare edge cases.
- [ ] D. Diagnostics are the assets a test places in the level.
- [ ] E. To validate an asset is to check it against rules, and to test is to run it and observe behaviour.

**Key:** A=F B=T C=F D=F E=T  |  `MA-unreal.19`  |  *Unreal and agent workflows*  |  source: Validate, test, accept, diagnose

- A (false): Compiling checks structure; play testing observes behaviour.
- B (true): They set the pass line before work starts.
- C (false): A smoke test is a quick check that the basics run.
- D (false): Diagnostics are messages and logs explaining a result.
- E (true): Validation inspects; testing exercises.

**17.** After a script change, an agent plans its repair steps. Which statements use the terms correctly? Check each statement that is true.  *(5 points)*

- [ ] A. Suppressing the error message counts as addressing the diagnostics.
- [ ] B. The sequence is compile, reload, inspect the component, set the field, read it back, then test the behaviour.
- [ ] C. A read-back means reading the value from the editor after setting it.
- [ ] D. Compiler diagnostics are the messages that name the location and cause of an error.
- [ ] E. Reading the script file's text is equivalent to a read-back from the component.

**Key:** A=F B=T C=T D=T E=F  |  `MA-unity.11`  |  *Unity, Spark and agent workflows*  |  source: repair and read-back

- A (false): The cause remains.
- B (true): Each step depends on the one before.
- C (true): It confirms the stored state.
- D (true): They guide the code fix.
- E (false): The component's loaded state is a different thing.

**18.** A designer asks an agent, "Hook the AI up to the lighting stuff." Which statements are exact rewrites? Check each statement that is true.  *(5 points)*

- [ ] A. Expose create-light as a tool with arguments for target scene and intensity.
- [ ] B. Expose the scene inventory as a resource.
- [ ] C. Reading the inventory resource first lets the agent choose where to call the create-light tool.
- [ ] D. Expose the review checklist as a resource that runs the review when read.
- [ ] E. Expose the reusable checklist as a prompt template.

**Key:** A=T B=T C=T D=F E=T  |  `MA-mcp.16`  |  *MCP fundamentals*  |  source: mapping a vague request to primitives

- A (true): An operation with inputs is a tool.
- B (true): Readable context fits the resource primitive.
- C (true): Context informs the action.
- D (false): Reading a resource supplies content and does not run a review.
- E (true): Reusable templates are prompts.

**19.** A modelling tool treats +Z as up, while glTF and Godot treat +Y as up. Check each statement that is true about the terms.  *(5 points)*

- [ ] A. Blender uses +Z as up, while glTF and Godot use +Y as up.
- [ ] B. Unreal's editor treats +Z as up, as Blender does.
- [ ] C. Up axis names which axis points up; handedness names whether the axes follow a right-hand or left-hand rule.
- [ ] D. A model that lies on its side after import suggests the up axis was not converted on export.
- [ ] E. Up axis and handedness are two names for the same setting.

**Key:** A=T B=T C=T D=T E=F  |  `MA-ch03.11`  |  *None*  |  source: Up axis and handedness

- A (true): That is why a conversion is needed between Blender and Godot.
- B (true): Unreal's editor is Z-up.
- C (true): They are two separate properties of a coordinate system.
- D (true): The height stays on the old up axis, so the model appears tipped.
- E (false): Fixing one leaves the other unchanged.

**20.** A designer wants a health bar to float 40 units above an enemy's head, follow the enemy as it walks and turns, and still be right when the enemy is scaled up to be a boss. The bar is made a child of the enemy. Check each statement that is true.  *(5 points)*

- [ ] A. A local position of (0, 0) places the child at the world origin.
- [ ] B. The bar's local position is measured relative to its parent, so a fixed local offset of 40 units up stays the same while the bar's world position changes as the enemy walks.
- [ ] C. When the parent is rotated, the engine rotates the child's local offset with it, so the bar swings around the enemy.
- [ ] D. When the parent is scaled up, the child's local offset is scaled with it, so the bar sits farther away unless scale inheritance is handled.
- [ ] E. World (global) space measures positions from the parent object's own origin.

**Key:** A=F B=T C=T D=T E=F  |  `MA-vocab.7`  |  *Engine vocabulary (Godot, Unity, Unreal)*  |  source: Local versus world space

- A (false): A local position of (0, 0) is the parent's own origin, wherever the parent is in the world.
- B (true): A local position is stored relative to the parent and does not change when the parent moves.
- C (true): The world position is built from the chain of parent transforms, including rotation.
- D (true): Parent scale applies to the child's offset, so a boss at scale 2 puts the bar twice as far away.
- E (false): World space is measured from the world origin; local space is measured from the parent.
