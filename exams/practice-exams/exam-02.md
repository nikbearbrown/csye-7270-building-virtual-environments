# CSYE 7270 Building Virtual Environments: practice exam 02

**PRACTICE FORM. Drawn at random from the question bank; not the real exam; not signed off by the instructor.**

20 questions, 5 points each, 100 points. Name: ______________________

**Scoring.** Five statements, each true or false, 1 point each. The student checks the statements they believe are true. A statement scores 1 point if it is checked and true, or unchecked and false; otherwise 0. Read every statement on its own and decide whether it is true by itself. Strong words (always, never, every, proves) are often what makes a statement false, but a strong-sounding statement is not false for sounding strong.

---

**1.** An agent reports: "Fixed the coin pickup by setting the coin's collision layer to 1 so it overlaps the player." The coin is an Area2D and the player is on layer 1. Check each statement that is true.  *(5 points)*

- [ ] A. The change may have side effects, since other things whose masks include layer 1 will now see the coin as part of the player's layer.
- [ ] B. The fix is right because the coin must be on the same layer as the player to touch it.
- [ ] C. The fix targets the wrong property: the coin detects the player through its collision mask, not its collision layer.
- [ ] D. A follow-up that gives evidence is: print the coin's layer and mask values and run the pickup, reporting whether body_entered fired.
- [ ] E. A follow-up that gives evidence is: ask the agent to re-read the coin's scene file.

**2.** A producer pairs a described behaviour with a one-line instruction for the agent. Check each pair in which the instruction correctly compresses the behaviour.  *(5 points)*

- [ ] A. "A short tap makes a small hop and holding makes a full jump" is compressed by "add a jump buffer".
- [ ] B. "A short tap makes a small hop and holding makes a full jump" is compressed by "add variable jump height".
- [ ] C. "Players who walk off a ledge can still jump for a split second" is compressed by "add coyote time of 0.1 s".
- [ ] D. "A jump pressed just before landing still happens on landing" is compressed by "add a jump buffer of 0.1 s".
- [ ] E. "Players who walk off a ledge can still jump for a split second" is compressed by "add a jump buffer".

**3.** An assistant application uses a connector to reach a service that exposes editor operations. Which statements name the roles correctly? Check each statement that is true.  *(5 points)*

- [ ] A. A server can run as a local process on the same machine.
- [ ] B. The client is the part of the host that holds the connection to a server.
- [ ] C. The host is the assistant application the user works in.
- [ ] D. The client is the player character in the level that calls the service.
- [ ] E. The server is the service that exposes tools, resources and prompts.

**4.** A game test passes on some runs and fails on others with unchanged code. It uses a random spawn position and waits a fixed number of rendered frames while the simulation speed varies. Check each statement that is true.  *(5 points)*

- [ ] A. A flaky test is one that gives different results on unchanged code.
- [ ] B. Rerunning until one pass appears is a fix for the intermittent failure.
- [ ] C. Deleting the failing assertion repairs the nondeterminism.
- [ ] D. Waiting for a fixed number of rendered frames is more robust than waiting for a condition with a time bound.
- [ ] E. Recording the random seed lets a failing run be replayed.

**5.** A material has parameters an agent can set. Check each statement that is true.  *(5 points)*

- [ ] A. Emission is light that the surface gives off by itself.
- [ ] B. Metallic says how much the surface behaves like a metal.
- [ ] C. Roughness controls how sharp or blurry reflections and highlights are.
- [ ] D. Roughness controls how bright the surface is lit.
- [ ] E. Albedo is the base colour of the surface, before lighting.

**6.** An artist hands over a 3D character. Check each statement that is true about the skeleton terms.  *(5 points)*

- [ ] A. Skinning weights say which texture is applied to each bone.
- [ ] B. A bone is a vertex that is hidden from the renderer.
- [ ] C. A rig is a skeleton of bones together with the setup that lets the mesh follow them.
- [ ] D. A rig is a texture that stores the colour of the character's skin.
- [ ] E. A bone is a transform in the skeleton hierarchy that can be rotated to pose the character.

**7.** A smoke effect uses many large transparent quads. Check each statement that is true about the cost terms.  *(5 points)*

- [ ] A. Transparent corners of a quad are still shaded, so they add fragment cost.
- [ ] B. Overdraw is the same screen pixel being shaded more than once by overlapping surfaces.
- [ ] C. Fill rate is how many pixels the GPU can shade and write per second, and overdraw uses it up.
- [ ] D. A fragment is one pixel-sized unit of work for the fragment shader.
- [ ] E. Doubling the width and height of each quad doubles its fragment count.

**8.** A character needs states for idle, run, jump and fall. Check each statement that is true about state machines.  *(5 points)*

- [ ] A. A state machine is in exactly one current state at a time.
- [ ] B. A transition is the animation clip played inside a state.
- [ ] C. A transition is a rule that moves the machine from one state to another when a condition becomes true.
- [ ] D. A state machine runs its states in parallel.
- [ ] E. A state machine replaces a pile of nested if checks with named states and transitions.

**9.** A Godot task says "load the resource" and a profiling note says "the resource usage is high". Check each statement that is correct.  *(5 points)*

- [ ] A. A Godot Resource is the memory the game is using.
- [ ] B. An agent asked to "reduce resources" could mean files or system load, and should be told which.
- [ ] C. In Godot, a Resource is a data object that can be saved to a file, such as a texture or an animation.
- [ ] D. Loading a Resource file lowers the processor usage.
- [ ] E. Resource usage in a profiling note usually means memory or processor time used by the game.

**10.** A team plans to migrate from an older MCP server to its replacement. Which statements use the terms correctly? Check each statement that is true.  *(5 points)*

- [ ] A. A query that reads is the riskiest first test of a new connection.
- [ ] B. A reversible edit is a change that is impossible to undo.
- [ ] C. A checkpoint is a recoverable snapshot of the project and configuration taken before the change.
- [ ] D. A query that reads changes the scene slightly.
- [ ] E. A rollback route is a documented way to return to the previous setup.

**11.** Candidates for a game-programming job are asked what the words scene, level and map mean in the three big engines. Check each statement that is true.  *(5 points)*

- [ ] A. In Unity, more than one scene can be open at the same time, which is called additive loading.
- [ ] B. In Unity, "scene" means a reusable object that is instanced many times, in the way a prefab is.
- [ ] C. A Godot scene can be a single weapon, a character or a whole level, so "scene" does not mean "one screen of the game".
- [ ] D. In Godot, "level" is a special engine type that is different from a scene.
- [ ] E. In Unreal, a level is a saved map that holds the Actors placed in one part of the world.

**12.** A producer types "Make the camera swoop in on the boss, then pan back out to show the arena." Check each statement that is true.  *(5 points)*

- [ ] A. A zoom out widens the field of view while the camera stays where it is.
- [ ] B. A pan is a rotation of the camera on the spot, so it does not move the camera back out.
- [ ] C. A dolly out moves the camera body backward along its view direction.
- [ ] D. A dolly changes the lens angle and leaves the camera position unchanged.
- [ ] E. "Pan back out" is the correct term for moving the camera body away from the subject.

**13.** An Unreal level has twelve Actors created from one Blueprint class. A designer wants one placed Actor to start with a different health value. Check each statement that is true.  *(5 points)*

- [ ] A. A Blueprint class is a template, and a placed Actor is an instance of it.
- [ ] B. An override is an instance value that differs from the class default.
- [ ] C. An instance-level change and a class-default change name the same edit.
- [ ] D. Customizing one instance requires deleting its Blueprint class.
- [ ] E. Editing a class default can reach instances that have not overridden that value.

**14.** A student types this to a coding agent: "Pan the camera 5 metres closer to the player, then zoom out by moving the camera back." Check each statement that is true.  *(5 points)*

- [ ] A. "Zoom out by moving the camera back" mixes terms; moving the camera backward is a dolly out.
- [ ] B. The prompt is precise because it states a distance.
- [ ] C. "Pan" is correct because the camera changes position.
- [ ] D. "Pan" is the wrong word for moving 5 metres closer; the move is a dolly in.
- [ ] E. "Zoom out" is correct whenever the camera node's position changes.

**15.** A credential in a tool log was also committed to version control. Check each statement that is true.  *(5 points)*

- [ ] A. Renaming a configuration file applies encryption.
- [ ] B. Version-control history retains earlier file contents after the file is edited.
- [ ] C. A private repository means each reader has the right to use the credential.
- [ ] D. A least-privilege credential limits the damage if it leaks.
- [ ] E. A leaked credential should be revoked, not just removed from the latest file.

**16.** A student must write the exact words for platformer jump feel. Check each statement that is true.  *(5 points)*

- [ ] A. Terminal velocity is the speed at the start of a jump.
- [ ] B. Coyote time and a double jump are the same feature.
- [ ] C. Terminal velocity is the highest fall speed the character is allowed to reach.
- [ ] D. Variable jump height lets a short press give a low jump and a long press give a high jump.
- [ ] E. A double jump is an extra jump allowed while in the air.

**17.** An agent reports: "Walk-to-run blending works. I set the AnimationTree speed parameter once in _ready." Check each statement that is true.  *(5 points)*

- [ ] A. The claim is right, because a blend parameter keeps tracking the speed once set.
- [ ] B. The claim is doubtful: a value set once in _ready does not follow the character's changing speed, so the blend stays put.
- [ ] C. The parameter can be set once in _ready to the maximum speed so the blend runs fully.
- [ ] D. A follow-up that gives evidence is: ask the agent whether the AnimationTree node exists.
- [ ] E. A follow-up that gives evidence is: start the game and report the blend value while the character stands still.

**18.** A designer writes: "The popup eases out, the falling crate eases in." Check each statement that is a correct unpacking.  *(5 points)*

- [ ] A. Ease-in-out starts slowly, moves fastest in the middle and slows again at the end.
- [ ] B. Ease-in starts slowly and speeds up, which suits an object starting to fall.
- [ ] C. Ease-in and ease-out reach different end values.
- [ ] D. Ease-out makes the animation take longer than a linear one of the same set duration.
- [ ] E. Ease-out starts fast and slows at the end, which suits a popup that settles.

**19.** A move-object tool is specified for an editor where several objects share a display name. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. An unambiguous identifier should select the target, not the display name.
- [ ] B. An offset moves relative to the current position, while an absolute destination sets the final position.
- [ ] C. The contract states units and coordinate space.
- [ ] D. An offset and an absolute destination give the same result regardless of the starting position.
- [ ] E. A display name is a unique identifier.

**20.** An agent says a door that opens only when the player holds a key is complete. A reviewer asks what kinds of evidence would count. Check each statement that is true.  *(5 points)*

- [ ] A. A negative path test checks that the door opens when the key is held.
- [ ] B. Running just the has-key case covers the rejection behaviour.
- [ ] C. Import or compile validation shows that the project loads, not that the door logic is right.
- [ ] D. A negative path test checks that the door stays closed without the key.
- [ ] E. Static inspection reads the implementation and changed assets without running them.
