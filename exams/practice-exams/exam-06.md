# CSYE 7270 Building Virtual Environments: practice exam 06

**PRACTICE FORM. Drawn at random from the question bank; not the real exam; not signed off by the instructor.**

20 questions, 5 points each, 100 points. Name: ______________________

**Scoring.** Five statements, each true or false, 1 point each. The student checks the statements they believe are true. A statement scores 1 point if it is checked and true, or unchecked and false; otherwise 0. Read every statement on its own and decide whether it is true by itself. Strong words (always, never, every, proves) are often what makes a statement false, but a strong-sounding statement is not false for sounding strong.

---

**1.** An agent reports: "Line of sight works: the enemy's raycast returns a hit, so the enemy can see the player." Check each statement that is true.  *(5 points)*

- [ ] A. A follow-up that gives evidence is: put a wall between enemy and player and report whether the ray still hits something.
- [ ] B. The claim is right, since the ray goes toward the player and so a hit is the player.
- [ ] C. Setting the ray's mask to the player's layer alone is right, because walls are then ignored.
- [ ] D. A follow-up that gives evidence is: confirm line of sight is true with the player standing in plain view, and nothing else.
- [ ] E. The claim is incomplete: a ray hit may be a wall, so the code must check that the first thing hit is the player.

**2.** A designer asks an agent, "Put some checkpoints in the level." Which rewrites use exact terms? Check each statement that is true.  *(5 points)*

- [ ] A. Create three instances of the existing checkpoint prefab asset in the named scene of the named project.
- [ ] B. Find the prefab by its display name alone.
- [ ] C. Leave the prefab asset unchanged unless an approved change is named.
- [ ] D. Set each instance's world-space position to the supplied coordinates, with units stated.
- [ ] E. Make three new prefab assets in the level.

**3.** A student reads an agent's plan and must spot imprecise words. Check each statement that is true.  *(5 points)*

- [ ] A. "Blend the idle and run clips with a blend tree on speed" uses the terms correctly.
- [ ] B. "The tween stores a keyframe in a rig" describes how a tween works.
- [ ] C. "The camera pans toward the boss by moving closer" mixes up pan and dolly.
- [ ] D. "The fragment shader displaces each vertex" gives the wrong stage.
- [ ] E. "The coin is a solid collider so it detects pickups" should say the coin is a trigger.

**4.** An agent raises the frame rate by switching off shadows, but the acceptance criteria require readable character shadows. Check each statement that is true.  *(5 points)*

- [ ] A. Acceptance criteria define what counts as done, and dropping one changes the task rather than meeting it.
- [ ] B. A controlled benchmark compares runs on the same scene and workload.
- [ ] C. Profiling finds the real bottleneck before an optimization is chosen.
- [ ] D. Profiling means guessing which feature is costly and switching it off.
- [ ] E. A higher frame rate alone is acceptance evidence for completion.

**5.** An assistant sends project context to a remote model and calls an MCP editor service on the user's laptop. Check each statement that is true.  *(5 points)*

- [ ] A. A trust boundary is a line where data or control passes between parties with different trust.
- [ ] B. Telemetry is the model's reasoning text.
- [ ] C. Inference is the model producing output from its input, and it can run on a remote server.
- [ ] D. A local MCP server means the model also runs locally.
- [ ] E. Egress means data entering a machine from outside.

**6.** A student asks for "smooth physics" and must say which update loop to use. Check each statement that is true.  *(5 points)*

- [ ] A. Tunnelling is when a fast object passes through a thin collider without a hit being detected.
- [ ] B. A fixed timestep removes the need for colliders.
- [ ] C. A fixed timestep runs physics at a steady interval regardless of how fast frames are drawn.
- [ ] D. Movement of physics bodies belongs in the fixed-timestep step in most engines.
- [ ] E. A per-frame update runs once per drawn frame, so its interval varies.

**7.** A weapon has a cooldown of 0.5 seconds. The agent uses a Timer node. Check each statement that is a correct unpacking.  *(5 points)*

- [ ] A. Starting the timer at fire time, not at button-press time, keeps a refused shot from extending the cooldown.
- [ ] B. wait_time is in seconds.
- [ ] C. One-shot off makes the timer fire once and stay stopped.
- [ ] D. The weapon can fire again as soon as the timer node exists.
- [ ] E. Starting the timer when the weapon fires, and refusing to fire while the timer is running, gives a cooldown.

**8.** A report says "the static light is baked". Check each statement that is correct about the word static in a game project.  *(5 points)*

- [ ] A. Static lighting means light that is recomputed each frame, so the agent skips baking it.
- [ ] B. Static typing makes objects unable to move.
- [ ] C. Static typing in a script means declaring the types of variables.
- [ ] D. StaticBody is a physics body that is not moved by forces.
- [ ] E. A StaticBody2D is pushed around by forces like a RigidBody2D.

**9.** A student wants a more realistic material set-up. Check each statement that is true about PBR.  *(5 points)*

- [ ] A. PBR is a file format for animated meshes.
- [ ] B. PBR materials respond consistently across different lighting conditions.
- [ ] C. PBR stands for physically based rendering and describes materials with measured-style parameters.
- [ ] D. PBR stands for per-bone rendering.
- [ ] E. A PBR material usually combines albedo, roughness, metallic and normal inputs.

**10.** An Unreal agent places Actors in a level and sees them in the editor. The request is a level that a teammate can open. Check each statement that is true.  *(5 points)*

- [ ] A. A dirty asset has changes in memory that are not yet saved.
- [ ] B. A dependency is an asset another asset refers to, and the level needs it present on the teammate's side.
- [ ] C. Saving an unrelated level writes the edited Actors into the requested level.
- [ ] D. A commit is the same as a save in the editor.
- [ ] E. A screenshot of the viewport is evidence of persistence.

**11.** A character must reach for a cup the player can place anywhere on a table. The project has one authored reach clip keyed to reach straight ahead. A developer says "play a reach animation toward the cup". Check each statement that is true.  *(5 points)*

- [ ] A. Inverse kinematics on the arm chain, with the cup's position as target, is the exact request.
- [ ] B. Forward kinematics makes the hand go to the cup because it starts from the target.
- [ ] C. A pole or hint names the elbow direction, since a target alone leaves it open.
- [ ] D. The authored clip reaches the place it was keyed for.
- [ ] E. A blend space between authored reaches stays inside the range of those clips.

**12.** A vague prompt says: "Make the player move nicely and the platforms work." Check each statement that is true.  *(5 points)*

- [ ] A. "Nicely" is an exact term for tuning movement.
- [ ] B. The player can be named as a kinematic character body that is controlled by script.
- [ ] C. The rewrite says movement changes are scaled by delta time.
- [ ] D. The moving platform can be named as a static body.
- [ ] E. Velocity, acceleration, friction and gravity are movement-rule terms.

**13.** A developer asks for a "zoom" on a boss reveal and gets a different feel than expected. Check each statement that is true.  *(5 points)*

- [ ] A. A zoom changes the field of view or focal length while the camera stays where it is.
- [ ] B. When the camera dollies toward a subject, nearby and distant objects shift against each other (parallax); a zoom does not produce that shift.
- [ ] C. In an engine, changing the camera's field-of-view value is a dolly, not a zoom.
- [ ] D. A zoom in and a dolly in give the same perspective because both make the subject larger on screen.
- [ ] E. Moving the camera node closer to the subject changes its field of view.

**14.** A prompt says: "Animate the rig with a sprite sheet and key the bones every frame at 24 bones per second." Check each statement that is true.  *(5 points)*

- [ ] A. "Bones per second" is a standard unit of animation speed.
- [ ] B. "24 bones per second" is the wrong unit; speed of playback is frames per second.
- [ ] C. The prompt is correct because a sprite sheet and a rig mean the same thing.
- [ ] D. "Sprite sheet" is the wrong word for a rig; a rig is animated with clips of bone transforms.
- [ ] E. "Key the bones" is acceptable, since a keyframe stores a bone's transform at a time.

**15.** A client and a server both say they support MCP, yet initialization fails. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. A small call that reads without modifying is a low-risk interoperability check before edits.
- [ ] B. Each side declares the protocol revision it supports during initialization.
- [ ] C. A tutorial's handshake sequence is enough evidence of the current requirements.
- [ ] D. A capability is a rendering feature of the engine exposed to the client.
- [ ] E. The MCP name guarantees both sides support the same revision.

**16.** A Unity script subscribes one of its methods to a C# event on a long-lived manager object. The script's GameObject is later destroyed without the script unsubscribing. Check each statement that is true.  *(5 points)*

- [ ] A. Event systems keep weak references to subscribers, so a long-lived emitter drops a destroyed subscriber without an unsubscribe call.
- [ ] B. The usual remedy is symmetrical: subscribe when the object is enabled and unsubscribe when it is disabled or destroyed.
- [ ] C. The engine queues the event until the next frame, by which time the destroyed object has been cleaned up and no error follows.
- [ ] D. The manager's list of subscribers still holds the destroyed script's method, so the next time the event is raised a call can be made on an object that no longer exists.
- [ ] E. In Godot, when a node whose method is connected to a signal is freed, the engine removes that connection.

**17.** An agent reports: "Combined hitbox and hurtbox into one Area2D so one node handles both." Check each statement that is true.  *(5 points)*

- [ ] A. The change creates a risk: an attack area on the player would overlap the player's own hurtbox and could damage the player.
- [ ] B. The change is a tidy-up, because both are the same thing.
- [ ] C. A follow-up that gives evidence is: swing the player's attack in an empty room and report whether the player takes damage.
- [ ] D. Keeping them separate lets each be on its own layer and mask so attackers hit only what they should.
- [ ] E. A hitbox can have monitoring switched off, because the hurtbox's own mask and monitoring detect the overlap.

**18.** A team compares a general script evaluator with three narrow lighting tools. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. If a legitimate operation is missing, the right step is to extend the narrow tools.
- [ ] B. A general evaluator has a larger blast radius, since it can act far beyond lighting edits.
- [ ] C. Least privilege means giving the agent the smallest set of permissions its task needs.
- [ ] D. Logging old and new values and affected identifiers gives an audit record.
- [ ] E. A general evaluator is the safer design because it is flexible.

**19.** An agent is asked to code enemy behaviour. Check each statement that is true.  *(5 points)*

- [ ] A. Chase and attack are transitions, not states.
- [ ] B. A transition from patrol to chase could fire when the player enters the enemy's sight range.
- [ ] C. An enter or exit action runs once when the machine enters or leaves a state.
- [ ] D. A state machine for an enemy needs a separate script per frame.
- [ ] E. A finite state machine for an enemy might have patrol, chase and attack states.

**20.** A hypothetical batch tool edits ten lights, and its contract says each edit commits separately. The sixth edit fails. Check each statement that is true.  *(5 points)*

- [ ] A. A rollback restores the earlier state after a failure, and this contract gives no such guarantee.
- [ ] B. Sending ten edits in one request makes them atomic.
- [ ] C. After a partial failure, the next step is to inspect the current state of each light before retrying.
- [ ] D. Under this contract the first five edits can remain applied, which is a partial commit.
- [ ] E. An atomic operation applies in full or leaves the state unchanged, with no half-finished state.
