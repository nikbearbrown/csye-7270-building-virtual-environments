# CSYE 7270 Building Virtual Environments: practice exam 06: KEY

Total 100 points. Statement key: T = true (check it), F = false (leave it blank).

---

**1.** An agent reports: "Line of sight works: the enemy's raycast returns a hit, so the enemy can see the player." Check each statement that is true.  *(5 points)*

- [ ] A. A follow-up that gives evidence is: put a wall between enemy and player and report whether the ray still hits something.
- [ ] B. The claim is right, since the ray goes toward the player and so a hit is the player.
- [ ] C. Setting the ray's mask to the player's layer alone is right, because walls are then ignored.
- [ ] D. A follow-up that gives evidence is: confirm line of sight is true with the player standing in plain view, and nothing else.
- [ ] E. The claim is incomplete: a ray hit may be a wall, so the code must check that the first thing hit is the player.

**Key:** A=F B=F C=F D=F E=T  |  `MA-k02.22`  |  *Jargon test: reading agent output*  |  source: Raycast, line of sight

- A (false): The ray hits the wall, so it reports a hit anyway, and the enemy that sees through cover would pass.
- B (false): The ray stops at the first collider it meets, which can be a wall between enemy and player.
- C (false): Ignoring walls lets the ray reach the player through them, so the enemy sees through solid cover.
- D (false): This tests the positive case alone, so an enemy that sees through walls would pass.
- E (true): A ray reports the first collider along its path, so a hit alone does not tell what it was.

**2.** A designer asks an agent, "Put some checkpoints in the level." Which rewrites use exact terms? Check each statement that is true.  *(5 points)*

- [ ] A. Create three instances of the existing checkpoint prefab asset in the named scene of the named project.
- [ ] B. Find the prefab by its display name alone.
- [ ] C. Leave the prefab asset unchanged unless an approved change is named.
- [ ] D. Set each instance's world-space position to the supplied coordinates, with units stated.
- [ ] E. Make three new prefab assets in the level.

**Key:** A=T B=F C=T D=T E=F  |  `MA-unity.15`  |  *Unity, Spark and agent workflows*  |  source: exact instruction for a Unity agent

- A (true): It separates instance, asset, scene and project.
- B (false): Display names can repeat.
- C (true): It protects the shared definition.
- D (true): It names the space and the units.
- E (false): Placed objects in a scene are instances, not new assets.

**3.** A student reads an agent's plan and must spot imprecise words. Check each statement that is true.  *(5 points)*

- [ ] A. "Blend the idle and run clips with a blend tree on speed" uses the terms correctly.
- [ ] B. "The tween stores a keyframe in a rig" describes how a tween works.
- [ ] C. "The camera pans toward the boss by moving closer" mixes up pan and dolly.
- [ ] D. "The fragment shader displaces each vertex" gives the wrong stage.
- [ ] E. "The coin is a solid collider so it detects pickups" should say the coin is a trigger.

**Key:** A=T B=F C=T D=T E=T  |  `MA-jargon.50`  |  *Jargon test: sprite sheets, rigs, colliders and state machines*  |  source: Spot the imprecise word

- A (true): This is the right use of blend tree and parameter.
- B (false): A tween is a code interpolation; keyframes live in clips.
- C (true): Moving closer is a dolly.
- D (true): Vertices belong to the vertex stage.
- E (true): Detecting pickups is trigger behaviour.

**4.** An agent raises the frame rate by switching off shadows, but the acceptance criteria require readable character shadows. Check each statement that is true.  *(5 points)*

- [ ] A. Acceptance criteria define what counts as done, and dropping one changes the task rather than meeting it.
- [ ] B. A controlled benchmark compares runs on the same scene and workload.
- [ ] C. Profiling finds the real bottleneck before an optimization is chosen.
- [ ] D. Profiling means guessing which feature is costly and switching it off.
- [ ] E. A higher frame rate alone is acceptance evidence for completion.

**Key:** A=T B=T C=T D=F E=F  |  `MA-verification.8`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Acceptance criteria, benchmark, profiling

- A (true): Criteria are the agreed definition of done.
- B (true): Holding the workload constant lets the change be attributed to the optimization.
- C (true): A profiler measures where time goes.
- D (false): Guessing is the opposite of profiling, which is measurement.
- E (false): Speed that breaks a required feature is a failure against the criteria.

**5.** An assistant sends project context to a remote model and calls an MCP editor service on the user's laptop. Check each statement that is true.  *(5 points)*

- [ ] A. A trust boundary is a line where data or control passes between parties with different trust.
- [ ] B. Telemetry is the model's reasoning text.
- [ ] C. Inference is the model producing output from its input, and it can run on a remote server.
- [ ] D. A local MCP server means the model also runs locally.
- [ ] E. Egress means data entering a machine from outside.

**Key:** A=T B=F C=T D=F E=F  |  `MA-security.1`  |  *Agent security and local versus cloud execution*  |  source: Local, remote, inference, egress

- A (true): Context sent to a remote model crosses one.
- B (false): Telemetry is usage data a program reports about itself.
- C (true): Inference location is independent of tool location.
- D (false): The tool server and the model are separate components.
- E (false): Egress is data leaving.

**6.** A student asks for "smooth physics" and must say which update loop to use. Check each statement that is true.  *(5 points)*

- [ ] A. Tunnelling is when a fast object passes through a thin collider without a hit being detected.
- [ ] B. A fixed timestep removes the need for colliders.
- [ ] C. A fixed timestep runs physics at a steady interval regardless of how fast frames are drawn.
- [ ] D. Movement of physics bodies belongs in the fixed-timestep step in most engines.
- [ ] E. A per-frame update runs once per drawn frame, so its interval varies.

**Key:** A=T B=F C=T D=T E=T  |  `MA-jargon.30`  |  *Jargon test: game movement*  |  source: Fixed timestep and tunnelling

- A (true): Tunnelling happens when an object moves farther than a collider's thickness in one step.
- B (false): Colliders are still needed for contact tests.
- C (true): Fixed steps give stable simulation.
- D (true): Physics calls such as moving bodies are made in the physics step.
- E (true): Frame time varies, so per-frame steps vary.

**7.** A weapon has a cooldown of 0.5 seconds. The agent uses a Timer node. Check each statement that is a correct unpacking.  *(5 points)*

- [ ] A. Starting the timer at fire time, not at button-press time, keeps a refused shot from extending the cooldown.
- [ ] B. wait_time is in seconds.
- [ ] C. One-shot off makes the timer fire once and stay stopped.
- [ ] D. The weapon can fire again as soon as the timer node exists.
- [ ] E. Starting the timer when the weapon fires, and refusing to fire while the timer is running, gives a cooldown.

**Key:** A=T B=T C=F D=F E=T  |  `MA-k01.29`  |  *Jargon test: compress and decompress*  |  source: Timer

- A (true): A refused shot should not restart the timer, or the player would wait longer than 0.5 seconds.
- B (true): The Timer's wait_time property is measured in seconds, not frames, so 0.5 means half a second.
- C (false): With one-shot off the timer restarts and times out repeatedly, so it would not stay stopped.
- D (false): The timer must finish counting down first, so merely having the node does not end the cooldown.
- E (true): That is the core logic: the running timer blocks firing until it finishes.

**8.** A report says "the static light is baked". Check each statement that is correct about the word static in a game project.  *(5 points)*

- [ ] A. Static lighting means light that is recomputed each frame, so the agent skips baking it.
- [ ] B. Static typing makes objects unable to move.
- [ ] C. Static typing in a script means declaring the types of variables.
- [ ] D. StaticBody is a physics body that is not moved by forces.
- [ ] E. A StaticBody2D is pushed around by forces like a RigidBody2D.

**Key:** A=F B=F C=T D=T E=F  |  `MA-k03.9`  |  *Jargon test: false friends*  |  source: Static (false friend)

- A (false): Static lighting does not change at run time and may be baked, so skipping the bake would leave the scene unlit.
- B (false): Static typing concerns variable types in scripts, so an agent confusing it with physics would freeze objects needlessly.
- C (true): This is the language meaning, so the agent adds type annotations rather than changing physics bodies.
- D (true): A static body stays put under collisions, so an agent uses it for walls and floors.
- E (false): A static body ignores forces, and an agent using it for a crate that should be pushed would build a crate that never moves.

**9.** A student wants a more realistic material set-up. Check each statement that is true about PBR.  *(5 points)*

- [ ] A. PBR is a file format for animated meshes.
- [ ] B. PBR materials respond consistently across different lighting conditions.
- [ ] C. PBR stands for physically based rendering and describes materials with measured-style parameters.
- [ ] D. PBR stands for per-bone rendering.
- [ ] E. A PBR material usually combines albedo, roughness, metallic and normal inputs.

**Key:** A=F B=T C=T D=F E=T  |  `MA-jargon.37`  |  *Jargon test: shaders and materials*  |  source: PBR

- A (false): PBR is a shading approach, not a file format.
- B (true): One set-up looks plausible under varied lights.
- C (true): PBR models how light interacts with surfaces.
- D (false): The letters do not stand for that.
- E (true): These are the common PBR inputs.

**10.** An Unreal agent places Actors in a level and sees them in the editor. The request is a level that a teammate can open. Check each statement that is true.  *(5 points)*

- [ ] A. A dirty asset has changes in memory that are not yet saved.
- [ ] B. A dependency is an asset another asset refers to, and the level needs it present on the teammate's side.
- [ ] C. Saving an unrelated level writes the edited Actors into the requested level.
- [ ] D. A commit is the same as a save in the editor.
- [ ] E. A screenshot of the viewport is evidence of persistence.

**Key:** A=T B=T C=F D=F E=F  |  `MA-unreal.8`  |  *Unreal and agent workflows*  |  source: Saved state, package, dependency

- A (true): Dirty marks unsaved edits.
- B (true): Referenced content has to travel with the level.
- C (false): Each level is saved on its own.
- D (false): Saving writes the package; a commit records files in version control.
- E (false): It shows appearance in memory, not saved content.

**11.** A character must reach for a cup the player can place anywhere on a table. The project has one authored reach clip keyed to reach straight ahead. A developer says "play a reach animation toward the cup". Check each statement that is true.  *(5 points)*

- [ ] A. Inverse kinematics on the arm chain, with the cup's position as target, is the exact request.
- [ ] B. Forward kinematics makes the hand go to the cup because it starts from the target.
- [ ] C. A pole or hint names the elbow direction, since a target alone leaves it open.
- [ ] D. The authored clip reaches the place it was keyed for.
- [ ] E. A blend space between authored reaches stays inside the range of those clips.

**Key:** A=T B=F C=T D=T E=T  |  `MA-ch10.20`  |  *None*  |  source: Inverse kinematics prompt

- A (true): IK solves joint rotations from a target position.
- B (false): FK computes the hand position from rotations; it takes no target.
- C (true): Many joint configurations reach the same point.
- D (true): Keyed rotations are fixed data.
- E (true): A blend space interpolates between authored poses, so it stays inside their range.

**12.** A vague prompt says: "Make the player move nicely and the platforms work." Check each statement that is true.  *(5 points)*

- [ ] A. "Nicely" is an exact term for tuning movement.
- [ ] B. The player can be named as a kinematic character body that is controlled by script.
- [ ] C. The rewrite says movement changes are scaled by delta time.
- [ ] D. The moving platform can be named as a static body.
- [ ] E. Velocity, acceleration, friction and gravity are movement-rule terms.

**Key:** A=F B=T C=T D=F E=T  |  `MA-jargon.73`  |  *Jargon test: from the essay prompts*  |  source: Rewrite a vague movement prompt

- A (false): It does not name a quantity that can be set or checked.
- B (true): Script-driven movement uses a kinematic body.
- C (true): This keeps movement independent of frame rate.
- D (false): A static body does not move; a moving platform is kinematic.
- E (true): They describe how motion is built up and slowed.

**13.** A developer asks for a "zoom" on a boss reveal and gets a different feel than expected. Check each statement that is true.  *(5 points)*

- [ ] A. A zoom changes the field of view or focal length while the camera stays where it is.
- [ ] B. When the camera dollies toward a subject, nearby and distant objects shift against each other (parallax); a zoom does not produce that shift.
- [ ] C. In an engine, changing the camera's field-of-view value is a dolly, not a zoom.
- [ ] D. A zoom in and a dolly in give the same perspective because both make the subject larger on screen.
- [ ] E. Moving the camera node closer to the subject changes its field of view.

**Key:** A=T B=T C=F D=F E=F  |  `MA-jargon.3`  |  *Jargon test: camera movement*  |  source: Zoom versus dolly

- A (true): A zoom is a lens change, so the camera body does not move.
- B (true): A dolly changes the camera's position, so objects at different depths move differently on screen; a zoom just magnifies the same view.
- C (false): Field of view is the lens angle, so editing it is a zoom; a dolly moves the camera body.
- D (false): The subject grows in both cases, but the relationship between near and far objects differs.
- E (false): Position and field of view are separate camera properties.

**14.** A prompt says: "Animate the rig with a sprite sheet and key the bones every frame at 24 bones per second." Check each statement that is true.  *(5 points)*

- [ ] A. "Bones per second" is a standard unit of animation speed.
- [ ] B. "24 bones per second" is the wrong unit; speed of playback is frames per second.
- [ ] C. The prompt is correct because a sprite sheet and a rig mean the same thing.
- [ ] D. "Sprite sheet" is the wrong word for a rig; a rig is animated with clips of bone transforms.
- [ ] E. "Key the bones" is acceptable, since a keyframe stores a bone's transform at a time.

**Key:** A=F B=T C=F D=T E=T  |  `MA-jargon.20`  |  *Jargon test: animation movement*  |  source: Spot the wrong word in an animation prompt

- A (false): There is no such unit.
- B (true): Playback speed is frames per second.
- C (false): They are different animation methods.
- D (true): Sprite sheets are flat image frames; rigs use bone transforms.
- E (true): Keying a bone means storing its transform at a given time.

**15.** A client and a server both say they support MCP, yet initialization fails. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. A small call that reads without modifying is a low-risk interoperability check before edits.
- [ ] B. Each side declares the protocol revision it supports during initialization.
- [ ] C. A tutorial's handshake sequence is enough evidence of the current requirements.
- [ ] D. A capability is a rendering feature of the engine exposed to the client.
- [ ] E. The MCP name guarantees both sides support the same revision.

**Key:** A=T B=T C=F D=F E=F  |  `MA-mcp.11`  |  *MCP fundamentals*  |  source: revision and capabilities

- A (true): It tests communication without changing the scene.
- B (true): Revision is negotiated at the start of the connection.
- C (false): Lifecycle rules change between revisions.
- D (false): Capabilities are optional protocol features each side declares.
- E (false): A product label is not a compatibility guarantee.

**16.** A Unity script subscribes one of its methods to a C# event on a long-lived manager object. The script's GameObject is later destroyed without the script unsubscribing. Check each statement that is true.  *(5 points)*

- [ ] A. Event systems keep weak references to subscribers, so a long-lived emitter drops a destroyed subscriber without an unsubscribe call.
- [ ] B. The usual remedy is symmetrical: subscribe when the object is enabled and unsubscribe when it is disabled or destroyed.
- [ ] C. The engine queues the event until the next frame, by which time the destroyed object has been cleaned up and no error follows.
- [ ] D. The manager's list of subscribers still holds the destroyed script's method, so the next time the event is raised a call can be made on an object that no longer exists.
- [ ] E. In Godot, when a node whose method is connected to a signal is freed, the engine removes that connection.

**Key:** A=F B=T C=F D=T E=T  |  `MA-vocab.18`  |  *Engine vocabulary (Godot, Unity, Unreal)*  |  source: Event lifetime and unsubscribing

- A (false): A C# event holds a normal reference to each subscriber, so a missing unsubscribe causes stale calls.
- B (true): Pairing subscribe and unsubscribe with enable and disable (or destroy) is the standard discipline.
- C (false): A C# event calls its subscribers in the line that raises it; nothing is queued.
- D (true): A stale subscription stays in the list and is called on the next raise.
- E (true): Godot removes the connections of a freed object.

**17.** An agent reports: "Combined hitbox and hurtbox into one Area2D so one node handles both." Check each statement that is true.  *(5 points)*

- [ ] A. The change creates a risk: an attack area on the player would overlap the player's own hurtbox and could damage the player.
- [ ] B. The change is a tidy-up, because both are the same thing.
- [ ] C. A follow-up that gives evidence is: swing the player's attack in an empty room and report whether the player takes damage.
- [ ] D. Keeping them separate lets each be on its own layer and mask so attackers hit only what they should.
- [ ] E. A hitbox can have monitoring switched off, because the hurtbox's own mask and monitoring detect the overlap.

**Key:** A=T B=F C=T D=T E=T  |  `MA-k02.20`  |  *Jargon test: reading agent output*  |  source: Hitbox and hurtbox

- A (true): A merged node detects its own owner, so the attack can register as damage to the player.
- B (false): They have different roles, dealing damage versus receiving it, and need different layers and masks.
- C (true): An empty room isolates self-hits, so damage taken exposes the merged-node bug.
- D (true): Separate nodes allow separate layer and mask settings, which control who can damage whom.
- E (true): The hurtbox does the detecting, so the hitbox only needs to be on a layer the hurtbox's mask includes.

**18.** A team compares a general script evaluator with three narrow lighting tools. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. If a legitimate operation is missing, the right step is to extend the narrow tools.
- [ ] B. A general evaluator has a larger blast radius, since it can act far beyond lighting edits.
- [ ] C. Least privilege means giving the agent the smallest set of permissions its task needs.
- [ ] D. Logging old and new values and affected identifiers gives an audit record.
- [ ] E. A general evaluator is the safer design because it is flexible.

**Key:** A=T B=T C=T D=T E=F  |  `MA-unity.18`  |  *Unity, Spark and agent workflows*  |  source: scope and least privilege

- A (true): Improvising with undocumented calls bypasses the contract.
- B (true): Blast radius is the reach of a possible mistake.
- C (true): Narrow tools apply that principle.
- D (true): An audit record supports review.
- E (false): Flexibility widens what can go wrong.

**19.** An agent is asked to code enemy behaviour. Check each statement that is true.  *(5 points)*

- [ ] A. Chase and attack are transitions, not states.
- [ ] B. A transition from patrol to chase could fire when the player enters the enemy's sight range.
- [ ] C. An enter or exit action runs once when the machine enters or leaves a state.
- [ ] D. A state machine for an enemy needs a separate script per frame.
- [ ] E. A finite state machine for an enemy might have patrol, chase and attack states.

**Key:** A=F B=T C=T D=F E=T  |  `MA-jargon.48`  |  *Jargon test: sprite sheets, rigs, colliders and state machines*  |  source: Enemy state machine

- A (false): They are states; the arrows between them are transitions.
- B (true): Sight is a typical transition condition.
- C (true): Entry and exit actions mark the edges of a state.
- D (false): The machine runs on updates; no per-frame script is needed.
- E (true): These are typical states.

**20.** A hypothetical batch tool edits ten lights, and its contract says each edit commits separately. The sixth edit fails. Check each statement that is true.  *(5 points)*

- [ ] A. A rollback restores the earlier state after a failure, and this contract gives no such guarantee.
- [ ] B. Sending ten edits in one request makes them atomic.
- [ ] C. After a partial failure, the next step is to inspect the current state of each light before retrying.
- [ ] D. Under this contract the first five edits can remain applied, which is a partial commit.
- [ ] E. An atomic operation applies in full or leaves the state unchanged, with no half-finished state.

**Key:** A=T B=F C=T D=T E=T  |  `MA-verification.11`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Atomicity, partial commit, rollback

- A (true): Rollback is a guarantee that must be stated by the contract.
- B (false): Grouping requests does not create transactional behaviour.
- C (true): The current state decides the safe recovery action.
- D (true): Independent commits allow some edits to persist.
- E (true): Atomicity means no visible half-finished state.
