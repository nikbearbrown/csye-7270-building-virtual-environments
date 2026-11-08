# CSYE 7270 Building Virtual Environments: practice exam 02: KEY

Total 100 points. Statement key: T = true (check it), F = false (leave it blank).

---

**1.** An agent reports: "Fixed the coin pickup by setting the coin's collision layer to 1 so it overlaps the player." The coin is an Area2D and the player is on layer 1. Check each statement that is true.  *(5 points)*

- [ ] A. The change may have side effects, since other things whose masks include layer 1 will now see the coin as part of the player's layer.
- [ ] B. The fix is right because the coin must be on the same layer as the player to touch it.
- [ ] C. The fix targets the wrong property: the coin detects the player through its collision mask, not its collision layer.
- [ ] D. A follow-up that gives evidence is: print the coin's layer and mask values and run the pickup, reporting whether body_entered fired.
- [ ] E. A follow-up that gives evidence is: ask the agent to re-read the coin's scene file.

**Key:** A=T B=F C=T D=T E=F  |  `MA-k02.5`  |  *Jargon test: reading agent output*  |  source: Collision layer versus mask

- A (true): Layer membership has consequences: enemies or walls that scan layer 1 may now react to the coin.
- B (false): Detection depends on one object's mask matching the other's layer, so objects do not need to share a layer.
- C (true): An Area2D detects bodies whose layer appears in its own mask, so changing the coin's layer does not help it see the player.
- D (true): The printed values show the actual setup, and the signal result shows whether the pickup works in play.
- E (false): Rereading the file reports the same settings but runs nothing, so a pickup that still fails would go unnoticed.

**2.** A producer pairs a described behaviour with a one-line instruction for the agent. Check each pair in which the instruction correctly compresses the behaviour.  *(5 points)*

- [ ] A. "A short tap makes a small hop and holding makes a full jump" is compressed by "add a jump buffer".
- [ ] B. "A short tap makes a small hop and holding makes a full jump" is compressed by "add variable jump height".
- [ ] C. "Players who walk off a ledge can still jump for a split second" is compressed by "add coyote time of 0.1 s".
- [ ] D. "A jump pressed just before landing still happens on landing" is compressed by "add a jump buffer of 0.1 s".
- [ ] E. "Players who walk off a ledge can still jump for a split second" is compressed by "add a jump buffer".

**Key:** A=F B=T C=T D=T E=F  |  `MA-k01.8`  |  *Jargon test: compress and decompress*  |  source: Coyote time, jump buffer, variable jump height

- A (false): A buffer changes when a jump starts, not how high it goes, so the tap and hold behaviour would be missing.
- B (true): Variable jump height makes the apex depend on how long the button is held.
- C (true): Coyote time is the grace window that allows a jump just after leaving the floor.
- D (true): A jump buffer remembers an early press and applies it when the character lands.
- E (false): A buffer remembers an early press; the ledge case needs coyote time, so the wrong feature would be built.

**3.** An assistant application uses a connector to reach a service that exposes editor operations. Which statements name the roles correctly? Check each statement that is true.  *(5 points)*

- [ ] A. A server can run as a local process on the same machine.
- [ ] B. The client is the part of the host that holds the connection to a server.
- [ ] C. The host is the assistant application the user works in.
- [ ] D. The client is the player character in the level that calls the service.
- [ ] E. The server is the service that exposes tools, resources and prompts.

**Key:** A=T B=T C=T D=F E=T  |  `MA-mcp.2`  |  *MCP fundamentals*  |  source: host, client, server

- A (true): Server names a role, not a location.
- B (true): A client maintains one connection to a server on the host's behalf.
- C (true): The host contains the user interaction and the clients.
- D (false): The client is the protocol connector, not an in-game character.
- E (true): Exposing capabilities is the server role.

**4.** A game test passes on some runs and fails on others with unchanged code. It uses a random spawn position and waits a fixed number of rendered frames while the simulation speed varies. Check each statement that is true.  *(5 points)*

- [ ] A. A flaky test is one that gives different results on unchanged code.
- [ ] B. Rerunning until one pass appears is a fix for the intermittent failure.
- [ ] C. Deleting the failing assertion repairs the nondeterminism.
- [ ] D. Waiting for a fixed number of rendered frames is more robust than waiting for a condition with a time bound.
- [ ] E. Recording the random seed lets a failing run be replayed.

**Key:** A=T B=F C=F D=F E=T  |  `MA-verification.5`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Flaky test, seed, bounded wait

- A (true): Flaky names a result that varies without a code change.
- B (false): One pass can hide a failure that is still intermittent.
- C (false): Removing the check removes detection and leaves the cause in place.
- D (false): Rendered frames need not correspond to a fixed amount of simulated time.
- E (true): With the seed, the same spawn sequence can be recreated.

**5.** A material has parameters an agent can set. Check each statement that is true.  *(5 points)*

- [ ] A. Emission is light that the surface gives off by itself.
- [ ] B. Metallic says how much the surface behaves like a metal.
- [ ] C. Roughness controls how sharp or blurry reflections and highlights are.
- [ ] D. Roughness controls how bright the surface is lit.
- [ ] E. Albedo is the base colour of the surface, before lighting.

**Key:** A=T B=T C=T D=F E=T  |  `MA-jargon.35`  |  *Jargon test: shaders and materials*  |  source: Albedo, roughness, metallic and emission

- A (true): An emissive surface appears to glow.
- B (true): Metallic switches between non-metal and metal reflection behaviour.
- C (true): A low roughness gives a mirror-like highlight; a high roughness spreads it out.
- D (false): Brightness comes from lights and emission; roughness shapes the highlight.
- E (true): Albedo is colour without light or shadow.

**6.** An artist hands over a 3D character. Check each statement that is true about the skeleton terms.  *(5 points)*

- [ ] A. Skinning weights say which texture is applied to each bone.
- [ ] B. A bone is a vertex that is hidden from the renderer.
- [ ] C. A rig is a skeleton of bones together with the setup that lets the mesh follow them.
- [ ] D. A rig is a texture that stores the colour of the character's skin.
- [ ] E. A bone is a transform in the skeleton hierarchy that can be rotated to pose the character.

**Key:** A=F B=F C=T D=F E=T  |  `MA-jargon.15`  |  *Jargon test: animation movement*  |  source: Rig, bone and skinning

- A (false): Skinning weights say how strongly each vertex follows each bone.
- B (false): A bone is not a vertex; it is a joint transform.
- C (true): A rig is the skeleton plus the binding of mesh to skeleton.
- D (false): Skin colour comes from textures; the rig is structural.
- E (true): Bones form a parent-child hierarchy and are posed by transforms.

**7.** A smoke effect uses many large transparent quads. Check each statement that is true about the cost terms.  *(5 points)*

- [ ] A. Transparent corners of a quad are still shaded, so they add fragment cost.
- [ ] B. Overdraw is the same screen pixel being shaded more than once by overlapping surfaces.
- [ ] C. Fill rate is how many pixels the GPU can shade and write per second, and overdraw uses it up.
- [ ] D. A fragment is one pixel-sized unit of work for the fragment shader.
- [ ] E. Doubling the width and height of each quad doubles its fragment count.

**Key:** A=T B=T C=T D=T E=F  |  `MA-ch09.14`  |  *None*  |  source: Overdraw, fragment and fill rate

- A (true): Transparent pixels are still shaded and blended.
- B (true): Overdraw describes layers of overlapping surfaces on one pixel.
- C (true): Fill rate is the throughput limit, and many layers per pixel consume it.
- D (true): Each covered pixel of a quad runs the fragment shader once.
- E (false): Area scales with the square of the side, so the count quadruples.

**8.** A character needs states for idle, run, jump and fall. Check each statement that is true about state machines.  *(5 points)*

- [ ] A. A state machine is in exactly one current state at a time.
- [ ] B. A transition is the animation clip played inside a state.
- [ ] C. A transition is a rule that moves the machine from one state to another when a condition becomes true.
- [ ] D. A state machine runs its states in parallel.
- [ ] E. A state machine replaces a pile of nested if checks with named states and transitions.

**Key:** A=T B=F C=T D=F E=T  |  `MA-jargon.47`  |  *Jargon test: sprite sheets, rigs, colliders and state machines*  |  source: State machine

- A (true): One state is active at once.
- B (false): A clip belongs to a state; a transition is the link between states.
- C (true): Transitions carry conditions.
- D (false): Only the current state is active.
- E (true): Named states make behaviour easier to read and extend.

**9.** A Godot task says "load the resource" and a profiling note says "the resource usage is high". Check each statement that is correct.  *(5 points)*

- [ ] A. A Godot Resource is the memory the game is using.
- [ ] B. An agent asked to "reduce resources" could mean files or system load, and should be told which.
- [ ] C. In Godot, a Resource is a data object that can be saved to a file, such as a texture or an animation.
- [ ] D. Loading a Resource file lowers the processor usage.
- [ ] E. Resource usage in a profiling note usually means memory or processor time used by the game.

**Key:** A=F B=T C=T D=F E=T  |  `MA-k03.20`  |  *Jargon test: false friends*  |  source: Resource (false friend)

- A (false): A Resource is a data object, and an agent treating it as memory use would profile when a file load was wanted.
- B (true): The phrase is ambiguous, and guessing could delete data files when the goal was to lower memory use.
- C (true): This is the engine meaning, so "load the resource" calls the load function on a file path.
- D (false): Loading a file adds work, so an agent expecting a performance gain from loading would not fix the profiling issue.
- E (true): This is the system meaning, so the agent should open the profiler rather than load a file.

**10.** A team plans to migrate from an older MCP server to its replacement. Which statements use the terms correctly? Check each statement that is true.  *(5 points)*

- [ ] A. A query that reads is the riskiest first test of a new connection.
- [ ] B. A reversible edit is a change that is impossible to undo.
- [ ] C. A checkpoint is a recoverable snapshot of the project and configuration taken before the change.
- [ ] D. A query that reads changes the scene slightly.
- [ ] E. A rollback route is a documented way to return to the previous setup.

**Key:** A=F B=F C=T D=F E=T  |  `MA-unity.4`  |  *Unity, Spark and agent workflows*  |  source: migration terms

- A (false): Reading is low risk compared with writing.
- B (false): Reversible means it can be undone.
- C (true): It lets the team return to a known state.
- D (false): A query reads and does not modify.
- E (true): Rollback undoes the migration.

**11.** Candidates for a game-programming job are asked what the words scene, level and map mean in the three big engines. Check each statement that is true.  *(5 points)*

- [ ] A. In Unity, more than one scene can be open at the same time, which is called additive loading.
- [ ] B. In Unity, "scene" means a reusable object that is instanced many times, in the way a prefab is.
- [ ] C. A Godot scene can be a single weapon, a character or a whole level, so "scene" does not mean "one screen of the game".
- [ ] D. In Godot, "level" is a special engine type that is different from a scene.
- [ ] E. In Unreal, a level is a saved map that holds the Actors placed in one part of the world.

**Key:** A=T B=F C=T D=F E=T  |  `MA-vocab.1`  |  *Engine vocabulary (Godot, Unity, Unreal)*  |  source: Scene, level and map

- A (true): Additive loading opens a scene on top of the scenes already open, which is how levels are built from several parts.
- B (false): A Unity scene is a container of GameObjects for a level or screen; the reusable, instanced object is the prefab.
- C (true): A Godot scene is a saved tree of nodes of any size, which is why one mechanism serves small objects and whole levels.
- D (false): Godot has no separate level type; a level is a scene, usually one that instances smaller scenes.
- E (true): In Unreal the level (map) file stores the Actors placed in it.

**12.** A producer types "Make the camera swoop in on the boss, then pan back out to show the arena." Check each statement that is true.  *(5 points)*

- [ ] A. A zoom out widens the field of view while the camera stays where it is.
- [ ] B. A pan is a rotation of the camera on the spot, so it does not move the camera back out.
- [ ] C. A dolly out moves the camera body backward along its view direction.
- [ ] D. A dolly changes the lens angle and leaves the camera position unchanged.
- [ ] E. "Pan back out" is the correct term for moving the camera body away from the subject.

**Key:** A=T B=T C=T D=F E=F  |  `MA-jargon.51`  |  *Jargon test: from the essay prompts*  |  source: Rewrite a vague camera prompt

- A (true): Zoom is a lens change, not a position change.
- B (true): A pan turns the camera left or right without changing its position.
- C (true): Dolly names a move of the camera body toward or away from the subject.
- D (false): That describes a zoom; a dolly changes position.
- E (false): Moving the body away is a dolly out; pan is a rotation.

**13.** An Unreal level has twelve Actors created from one Blueprint class. A designer wants one placed Actor to start with a different health value. Check each statement that is true.  *(5 points)*

- [ ] A. A Blueprint class is a template, and a placed Actor is an instance of it.
- [ ] B. An override is an instance value that differs from the class default.
- [ ] C. An instance-level change and a class-default change name the same edit.
- [ ] D. Customizing one instance requires deleting its Blueprint class.
- [ ] E. Editing a class default can reach instances that have not overridden that value.

**Key:** A=T B=T C=F D=F E=T  |  `MA-unreal.3`  |  *Unreal and agent workflows*  |  source: Class, instance, override

- A (true): The class defines defaults; each placement is an instance.
- B (true): Overrides replace the inherited default on that instance.
- C (false): They differ in scope: one object versus the template.
- D (false): Instances can carry overrides while the class stays in place.
- E (true): Non-overridden instances inherit the default.

**14.** A student types this to a coding agent: "Pan the camera 5 metres closer to the player, then zoom out by moving the camera back." Check each statement that is true.  *(5 points)*

- [ ] A. "Zoom out by moving the camera back" mixes terms; moving the camera backward is a dolly out.
- [ ] B. The prompt is precise because it states a distance.
- [ ] C. "Pan" is correct because the camera changes position.
- [ ] D. "Pan" is the wrong word for moving 5 metres closer; the move is a dolly in.
- [ ] E. "Zoom out" is correct whenever the camera node's position changes.

**Key:** A=T B=F C=F D=T E=F  |  `MA-jargon.7`  |  *Jargon test: camera movement*  |  source: Spot the wrong word in a camera prompt

- A (true): A true zoom out widens the lens and leaves the camera where it is.
- B (false): A distance does not repair wrong move names, so the agent could build the wrong move.
- C (false): A pan does not change position.
- D (true): A pan is a rotation; moving along the view direction is a dolly.
- E (false): Position changes are dollies, trucks or pedestals; a zoom is a lens change.

**15.** A credential in a tool log was also committed to version control. Check each statement that is true.  *(5 points)*

- [ ] A. Renaming a configuration file applies encryption.
- [ ] B. Version-control history retains earlier file contents after the file is edited.
- [ ] C. A private repository means each reader has the right to use the credential.
- [ ] D. A least-privilege credential limits the damage if it leaks.
- [ ] E. A leaked credential should be revoked, not just removed from the latest file.

**Key:** A=F B=T C=F D=T E=T  |  `MA-security.18`  |  *Agent security and local versus cloud execution*  |  source: Credential exposure

- A (false): A name gives no protection.
- B (true): Old copies stay in history.
- C (false): Read access and credential privilege differ.
- D (true): Narrow rights narrow the impact.
- E (true): Revocation ends its usefulness.

**16.** A student must write the exact words for platformer jump feel. Check each statement that is true.  *(5 points)*

- [ ] A. Terminal velocity is the speed at the start of a jump.
- [ ] B. Coyote time and a double jump are the same feature.
- [ ] C. Terminal velocity is the highest fall speed the character is allowed to reach.
- [ ] D. Variable jump height lets a short press give a low jump and a long press give a high jump.
- [ ] E. A double jump is an extra jump allowed while in the air.

**Key:** A=F B=F C=T D=T E=T  |  `MA-jargon.29`  |  *Jargon test: game movement*  |  source: Jump-feel vocabulary

- A (false): Terminal velocity is a cap on falling speed.
- B (false): One is a grace window on the ground edge, the other an additional jump.
- C (true): The fall speed is capped.
- D (true): The jump is cut short when the button is released early.
- E (true): A double jump spends an extra mid-air jump.

**17.** An agent reports: "Walk-to-run blending works. I set the AnimationTree speed parameter once in _ready." Check each statement that is true.  *(5 points)*

- [ ] A. The claim is right, because a blend parameter keeps tracking the speed once set.
- [ ] B. The claim is doubtful: a value set once in _ready does not follow the character's changing speed, so the blend stays put.
- [ ] C. The parameter can be set once in _ready to the maximum speed so the blend runs fully.
- [ ] D. A follow-up that gives evidence is: ask the agent whether the AnimationTree node exists.
- [ ] E. A follow-up that gives evidence is: start the game and report the blend value while the character stands still.

**Key:** A=F B=T C=F D=F E=F  |  `MA-k02.15`  |  *Jargon test: reading agent output*  |  source: Blend tree parameters

- A (false): A parameter keeps the last value written to it and does not follow the character's speed by itself.
- B (true): The parameter holds its initial value until code updates it, so walking faster does not change the blend.
- C (false): A fixed maximum would play the run animation constantly, so walking would never appear.
- D (false): A node existing says nothing about whether the blend value changes with speed.
- E (false): A standing character reads the initial value either way, so this check passes the bad claim.

**18.** A designer writes: "The popup eases out, the falling crate eases in." Check each statement that is a correct unpacking.  *(5 points)*

- [ ] A. Ease-in-out starts slowly, moves fastest in the middle and slows again at the end.
- [ ] B. Ease-in starts slowly and speeds up, which suits an object starting to fall.
- [ ] C. Ease-in and ease-out reach different end values.
- [ ] D. Ease-out makes the animation take longer than a linear one of the same set duration.
- [ ] E. Ease-out starts fast and slows at the end, which suits a popup that settles.

**Key:** A=T B=T C=F D=F E=T  |  `MA-k01.19`  |  *Jargon test: compress and decompress*  |  source: Easing

- A (true): It combines both curves, so the speed is low at both ends and peaks mid-way.
- B (true): Ease-in accelerates from rest, resembling a crate that gains speed as it falls.
- C (false): Both reach the same end value; only the speed curve along the way differs.
- D (false): The duration is fixed by the setting; easing only reshapes how the speed varies within it.
- E (true): Ease-out decelerates into rest, so the popup comes gently to its final position.

**19.** A move-object tool is specified for an editor where several objects share a display name. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. An unambiguous identifier should select the target, not the display name.
- [ ] B. An offset moves relative to the current position, while an absolute destination sets the final position.
- [ ] C. The contract states units and coordinate space.
- [ ] D. An offset and an absolute destination give the same result regardless of the starting position.
- [ ] E. A display name is a unique identifier.

**Key:** A=T B=T C=T D=F E=F  |  `MA-mcp.17`  |  *MCP fundamentals*  |  source: tool contract

- A (true): Display names can repeat.
- B (true): They are different input meanings.
- C (true): Without them the number is ambiguous.
- D (false): They agree only by coincidence.
- E (false): Several objects share it.

**20.** An agent says a door that opens only when the player holds a key is complete. A reviewer asks what kinds of evidence would count. Check each statement that is true.  *(5 points)*

- [ ] A. A negative path test checks that the door opens when the key is held.
- [ ] B. Running just the has-key case covers the rejection behaviour.
- [ ] C. Import or compile validation shows that the project loads, not that the door logic is right.
- [ ] D. A negative path test checks that the door stays closed without the key.
- [ ] E. Static inspection reads the implementation and changed assets without running them.

**Key:** A=F B=F C=T D=T E=T  |  `MA-verification.13`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Static, positive and negative evidence

- A (false): Opening with the key is the positive path.
- B (false): The rejection case needs its own test.
- C (true): Validation is a lower level of evidence than a behavioural test.
- D (true): The negative path is the rejection case.
- E (true): Static means examined without execution.
