# CSYE 7270 Building Virtual Environments: practice exam 01

**PRACTICE FORM. Drawn at random from the question bank; not the real exam; not signed off by the instructor.**

20 questions, 5 points each, 100 points. Name: ______________________

**Scoring.** Five statements, each true or false, 1 point each. The student checks the statements they believe are true. A statement scores 1 point if it is checked and true, or unchecked and false; otherwise 0. Read every statement on its own and decide whether it is true by itself. Strong words (always, never, every, proves) are often what makes a statement false, but a strong-sounding statement is not false for sounding strong.

---

**1.** After a movement rewrite, a tester lists checks and shapes. Check each statement that is true.  *(5 points)*

- [ ] A. A pickup zone is a trigger area.
- [ ] B. Standing on the moving platform and riding along tests that the platform carries the player.
- [ ] C. Measuring speed at 30 and 144 frames per second tests frame-rate independence.
- [ ] D. A capsule is a common collider shape for a character and a box for a simple platform.
- [ ] E. A pickup zone should be a rigid body that blocks the player.

**2.** A texture file was copied into a Unity project and the editor is still importing it. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. An import error shows that the file was not copied.
- [ ] B. The file's presence on disk shows the asset is ready.
- [ ] C. Copying the file again is a way to wait for import.
- [ ] D. Assigning a placeholder proves the requested texture imported.
- [ ] E. A file on disk becomes an asset the engine can use once the editor imports it.

**3.** An agent changes an Actor during a play session, but the designer expected the saved level to change. Check each statement that is true.  *(5 points)*

- [ ] A. A runtime instance and the authoring level asset are the same object.
- [ ] B. A change to a play-session Actor is transient and is discarded when play ends.
- [ ] C. Play-in-editor runs a temporary copy of the level's Actors.
- [ ] D. Authoring data is the saved level and asset content that lasts on disk.
- [ ] E. Persisting a change means leaving the play session running longer.

**4.** A team chooses how to list permitted export locations. Check each statement that is true.  *(5 points)*

- [ ] A. An allowlist of export directories fits a write boundary better than a denylist.
- [ ] B. An allowlist names the permitted items and refuses the rest.
- [ ] C. A denylist names the forbidden items and permits the rest.
- [ ] D. An allowlist for export names the directories where writes are permitted.
- [ ] E. A denylist of folder names is a complete boundary against unknown paths.

**5.** A rigged character needs to blend and switch motions. Check each statement that is true.  *(5 points)*

- [ ] A. A blend tree decides when the character is allowed to die.
- [ ] B. A state machine holds states and the transitions that move between them when conditions are met.
- [ ] C. A state machine blends clips by weight and has no concept of transitions.
- [ ] D. A blend tree is the right tool to switch from the idle clip to a death clip when health reaches zero.
- [ ] E. A blend tree mixes several clips together according to one or more parameters, such as speed.

**6.** A Godot script has `signal died` and a UI script that should react. Check each statement that is a correct unpacking of "use a signal".  *(5 points)*

- [ ] A. The connected function's return value is sent back to the emitter.
- [ ] B. The emitter declares the signal and calls emit; the listener connects one of its own functions to it.
- [ ] C. Values passed in emit are ignored; the connected function reads them from the emitter.
- [ ] D. Emitting a signal that has no connected function raises an error.
- [ ] E. A signal accepts a single connected function.

**7.** An agent reports: "Applied the normal map to the albedo slot so the bricks look bumpy." Check each statement that is true.  *(5 points)*

- [ ] A. A follow-up that gives evidence is: render the wall with a light moved across it and show whether the highlights change with the light.
- [ ] B. The claim is right, because both are textures that change how the surface looks.
- [ ] C. In StandardMaterial3D the Normal Map feature must be enabled before the texture is read as surface directions.
- [ ] D. The normal map belongs in the material's normal slot.
- [ ] E. The claim is wrong: albedo is base colour, and a normal map stores surface directions, so in the colour slot it shows as purple-blue colour instead of bumps.

**8.** An agent must slice and play a sprite sheet. Check each statement that is true.  *(5 points)*

- [ ] A. A frame is one image cell in the sheet.
- [ ] B. Frame order matters, so a prompt should say which cells make the walk and in what order.
- [ ] C. Setting an animation to loop makes it restart after the last frame.
- [ ] D. Frame rate and playback loop are the same setting.
- [ ] E. A sheet of 6 columns and 2 rows holds 12 frames if every cell is used.

**9.** A tool call returns a structured reply saying the named scene object could not be found. Which statements describe the failure correctly? Check each statement that is true.  *(5 points)*

- [ ] A. This is a transport failure, so the next step is changing the network port.
- [ ] B. The object identity is irrelevant to the next investigation.
- [ ] C. Reinstalling the language model is the first diagnosis the evidence supports.
- [ ] D. A structured reply shows that the object was modified.
- [ ] E. This is a tool execution error: the operation ran and reported failure in its result.

**10.** A game has a moving platform, a crate that tumbles, and a player character. Check each statement that is true about body types.  *(5 points)*

- [ ] A. A static body is moved around by applying impulses.
- [ ] B. A crate that should tumble under physics is a good fit for a static body.
- [ ] C. A rigid body is moved by the physics simulation using forces, mass and collisions.
- [ ] D. A kinematic body falls under gravity by itself without any code.
- [ ] E. A kinematic body is moved by code (or animation) and is not pushed around by forces.

**11.** A texture looks stretched on a model. Check each statement that is true about UVs.  *(5 points)*

- [ ] A. A stretched texture means the image file is too small to use.
- [ ] B. UV coordinates store the direction in which the surface faces.
- [ ] C. UV stands for the ultraviolet value of a pixel.
- [ ] D. UV coordinates store a colour for each point on a surface.
- [ ] E. UV unwrapping flattens a 3D mesh into 2D so it can be painted.

**12.** A game test fails intermittently. It spawns at a random position, and it uses an asset that is imported asynchronously. Check each statement that is true.  *(5 points)*

- [ ] A. An import failure and a gameplay failure are the same cause.
- [ ] B. An asynchronous import finishes later than the request, so a test that proceeds at once may use an asset that is not ready.
- [ ] C. Reporting the first passing rerun is adequate evidence that an intermittent failure is gone.
- [ ] D. A fixed timestep advances the simulation by a different amount depending on rendering speed.
- [ ] E. Rendered frames and elapsed game time are interchangeable when the simulation speed varies.

**13.** Most engines give an object a hook that runs once when it is ready to be used (Godot's _ready, Unity's Start, Unreal's BeginPlay) and a hook that runs repeatedly (Godot's _process, Unity's Update, Unreal's Tick). Check each statement that is true.  *(5 points)*

- [ ] A. A hook that runs one time is unsuitable for starting a looping timer, because the hook does not repeat.
- [ ] B. In Godot, _ready is called again each time a node is removed from the scene tree and added back.
- [ ] C. A per-frame hook is the right place to build the player's starting inventory, because it keeps retrying until it succeeds.
- [ ] D. In Godot, children's _ready callbacks run before the parent's, so the parent can rely on its children being set up.
- [ ] E. In Unity, Start is called before the script's first frame update, and when the script instance is enabled.

**14.** A material request says "use the normal on this surface" in one line and "use the normal map" in another. Check each statement that is correct.  *(5 points)*

- [ ] A. Flipping the normal changes the surface's albedo colour, so the agent edits the colour texture.
- [ ] B. A normal map is an ordinary map for the surface's colour.
- [ ] C. A normal map is a texture that stores a normal for each texel.
- [ ] D. A normal is a direction perpendicular to a surface at a point.
- [ ] E. A normal is the usual, default value of a parameter.

**15.** A vague prompt reads "make the camera feel more alive when the player gets hit". Check each rewrite that uses the exact camera jargon correctly to ask for a sensible hit effect.  *(5 points)*

- [ ] A. "Add a deadzone around the player when hit so the camera freezes in place."
- [ ] B. "Truck the camera up and down on hit so it looks up at the player."
- [ ] C. "On hit, briefly reduce the field of view by a few degrees (a quick zoom in), then ease it back."
- [ ] D. "Add screen shake on hit: 0.2 seconds, small random offset of the camera position, with the amplitude decaying to zero."
- [ ] E. "Dolly the lens narrower when hit."

**16.** A developer tells a coding agent: "Make the hull shinier." The hull material has a weathered-wood albedo, metallic 0 and roughness 0.8. Check each statement that is true about the terms.  *(5 points)*

- [ ] A. Lowering roughness makes reflections sharper and highlights tighter, which reads as shinier.
- [ ] B. In an engine that exposes smoothness instead of roughness, shinier means a lower smoothness value.
- [ ] C. Brightening the albedo texture is a gloss change, because lighter surfaces reflect sharper images.
- [ ] D. "Shinier" is an imprecise word, because glossy paint (metallic 0, low roughness) and polished metal (metallic near 1, low roughness) are different setups.
- [ ] E. Raising the emission colour is the exact term-level change for shine, because emission adds highlights.

**17.** Choose the body or area type for each object in a level. Check each statement that is true.  *(5 points)*

- [ ] A. The player character moved by script is a static body.
- [ ] B. A tumbling crate pushed around by physics is a rigid body.
- [ ] C. A platform moved by a script or animation is a rigid body.
- [ ] D. A coin that detects overlap without blocking is a trigger.
- [ ] E. A wall that does not move is a static body.

**18.** A scene has twenty instances of a lamp prefab, and one named lamp should turn blue. Which statements use the terms correctly? Check each statement that is true.  *(5 points)*

- [ ] A. Reverting an override returns the instance to the prefab's value.
- [ ] B. A prefab instance is a placed copy in the scene that stays linked to its prefab asset.
- [ ] C. Deleting the prefab asset is a way to isolate one lamp.
- [ ] D. An override changes a value on one instance without changing the prefab asset.
- [ ] E. Applying an override to the prefab keeps the change on one instance.

**19.** An Unreal editor MCP server lets an external assistant call editor operations. A designer asks whether this makes the assistant the NPC's runtime AI. Check each statement that is true.  *(5 points)*

- [ ] A. Editor automation and runtime AI are two names for the same role.
- [ ] B. An MCP server connected to the editor becomes the NPC's behaviour in the packaged build.
- [ ] C. An MCP server exposes tools that an external assistant can call.
- [ ] D. A tool call that places an Actor is an example of runtime AI.
- [ ] E. Runtime AI is the NPC's decision logic executing while the game is played.

**20.** A local service was reachable from other machines, and the team sees unexpected edits. Check each statement that is true.  *(5 points)*

- [ ] A. Blast radius is the extent of what an incident could affect.
- [ ] B. Containment means deleting the logs.
- [ ] C. Recovery and containment are the same step.
- [ ] D. Containment limits further damage, for example by stopping an exposed service.
- [ ] E. Evidence preservation means keeping logs and change records.
