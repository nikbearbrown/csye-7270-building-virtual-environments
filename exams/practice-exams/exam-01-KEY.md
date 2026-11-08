# CSYE 7270 Building Virtual Environments: practice exam 01: KEY

Total 100 points. Statement key: T = true (check it), F = false (leave it blank).

---

**1.** After a movement rewrite, a tester lists checks and shapes. Check each statement that is true.  *(5 points)*

- [ ] A. A pickup zone is a trigger area.
- [ ] B. Standing on the moving platform and riding along tests that the platform carries the player.
- [ ] C. Measuring speed at 30 and 144 frames per second tests frame-rate independence.
- [ ] D. A capsule is a common collider shape for a character and a box for a simple platform.
- [ ] E. A pickup zone should be a rigid body that blocks the player.

**Key:** A=T B=T C=T D=T E=F  |  `MA-jargon.74`  |  *Jargon test: from the essay prompts*  |  source: Observable movement checks

- A (true): It detects the player without blocking.
- B (true): It checks the body type and contact.
- C (true): Equal speeds show delta time is applied.
- D (true): Shapes are chosen to match the object.
- E (false): A pickup should detect overlap, not block.

**2.** A texture file was copied into a Unity project and the editor is still importing it. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. An import error shows that the file was not copied.
- [ ] B. The file's presence on disk shows the asset is ready.
- [ ] C. Copying the file again is a way to wait for import.
- [ ] D. Assigning a placeholder proves the requested texture imported.
- [ ] E. A file on disk becomes an asset the engine can use once the editor imports it.

**Key:** A=F B=F C=F D=F E=T  |  `MA-unity.13`  |  *Unity, Spark and agent workflows*  |  source: import readiness

- A (false): Copying and importing are separate steps.
- B (false): Filesystem presence and engine readiness differ.
- C (false): Duplicates add ambiguity.
- D (false): A placeholder is a different asset.
- E (true): Import is the processing step.

**3.** An agent changes an Actor during a play session, but the designer expected the saved level to change. Check each statement that is true.  *(5 points)*

- [ ] A. A runtime instance and the authoring level asset are the same object.
- [ ] B. A change to a play-session Actor is transient and is discarded when play ends.
- [ ] C. Play-in-editor runs a temporary copy of the level's Actors.
- [ ] D. Authoring data is the saved level and asset content that lasts on disk.
- [ ] E. Persisting a change means leaving the play session running longer.

**Key:** A=F B=T C=T D=T E=F  |  `MA-unreal.10`  |  *Unreal and agent workflows*  |  source: Authoring versus runtime state

- A (false): They are different objects with different persistence.
- B (true): Transient means not persisted.
- C (true): The play world is separate from the authored level.
- D (true): Authoring is what a save writes.
- E (false): Persistence needs a save to the authoring data.

**4.** A team chooses how to list permitted export locations. Check each statement that is true.  *(5 points)*

- [ ] A. An allowlist of export directories fits a write boundary better than a denylist.
- [ ] B. An allowlist names the permitted items and refuses the rest.
- [ ] C. A denylist names the forbidden items and permits the rest.
- [ ] D. An allowlist for export names the directories where writes are permitted.
- [ ] E. A denylist of folder names is a complete boundary against unknown paths.

**Key:** A=T B=T C=T D=T E=F  |  `MA-security.17`  |  *Agent security and local versus cloud execution*  |  source: Allowlist and denylist

- A (true): Unknown paths are refused by default.
- B (true): Anything unlisted is blocked.
- C (true): Anything unlisted is allowed.
- D (true): Permitted locations are listed.
- E (false): Unlisted paths remain permitted.

**5.** A rigged character needs to blend and switch motions. Check each statement that is true.  *(5 points)*

- [ ] A. A blend tree decides when the character is allowed to die.
- [ ] B. A state machine holds states and the transitions that move between them when conditions are met.
- [ ] C. A state machine blends clips by weight and has no concept of transitions.
- [ ] D. A blend tree is the right tool to switch from the idle clip to a death clip when health reaches zero.
- [ ] E. A blend tree mixes several clips together according to one or more parameters, such as speed.

**Key:** A=F B=T C=F D=F E=T  |  `MA-jargon.14`  |  *Jargon test: animation movement*  |  source: Blend tree versus state machine

- A (false): Life and death are game logic; the animation system only shows the result.
- B (true): States such as idle and jump are linked by transitions with conditions.
- C (false): Transitions are the core idea of a state machine.
- D (false): A one-time switch on a condition is a state machine transition; a blend tree mixes clips by a parameter.
- E (true): A blend tree outputs a weighted mix of clips driven by parameters.

**6.** A Godot script has `signal died` and a UI script that should react. Check each statement that is a correct unpacking of "use a signal".  *(5 points)*

- [ ] A. The connected function's return value is sent back to the emitter.
- [ ] B. The emitter declares the signal and calls emit; the listener connects one of its own functions to it.
- [ ] C. Values passed in emit are ignored; the connected function reads them from the emitter.
- [ ] D. Emitting a signal that has no connected function raises an error.
- [ ] E. A signal accepts a single connected function.

**Key:** A=F B=T C=F D=F E=F  |  `MA-k01.13`  |  *Jargon test: compress and decompress*  |  source: Signals

- A (false): Signals are one-way notifications, so the emitter receives no result from listeners.
- B (true): The two ends are declaring and emitting on one side and connecting a function on the other.
- C (false): Parameters travel with the signal and arrive as arguments of the connected function.
- D (false): Emitting with no listeners simply does nothing, since the emitter does not know or depend on its listeners.
- E (false): Many functions can connect to one signal, and all of them are called when it is emitted.

**7.** An agent reports: "Applied the normal map to the albedo slot so the bricks look bumpy." Check each statement that is true.  *(5 points)*

- [ ] A. A follow-up that gives evidence is: render the wall with a light moved across it and show whether the highlights change with the light.
- [ ] B. The claim is right, because both are textures that change how the surface looks.
- [ ] C. In StandardMaterial3D the Normal Map feature must be enabled before the texture is read as surface directions.
- [ ] D. The normal map belongs in the material's normal slot.
- [ ] E. The claim is wrong: albedo is base colour, and a normal map stores surface directions, so in the colour slot it shows as purple-blue colour instead of bumps.

**Key:** A=T B=F C=T D=T E=T  |  `MA-k02.18`  |  *Jargon test: reading agent output*  |  source: Normal map versus albedo

- A (true): Real bumps shade differently as the light moves, while a flat colour texture does not.
- B (false): The two textures hold different data, so only the normal slot reads directions to bend the lighting.
- C (true): Without enabling the feature, the assigned texture is ignored and the bricks still look flat.
- D (true): That slot reads the texture as surface directions, which produces the bump shading under light.
- E (true): The texture holds direction data, so used as colour it paints the surface blue and gives no lighting detail.

**8.** An agent must slice and play a sprite sheet. Check each statement that is true.  *(5 points)*

- [ ] A. A frame is one image cell in the sheet.
- [ ] B. Frame order matters, so a prompt should say which cells make the walk and in what order.
- [ ] C. Setting an animation to loop makes it restart after the last frame.
- [ ] D. Frame rate and playback loop are the same setting.
- [ ] E. A sheet of 6 columns and 2 rows holds 12 frames if every cell is used.

**Key:** A=T B=T C=T D=F E=T  |  `MA-jargon.44`  |  *Jargon test: sprite sheets, rigs, colliders and state machines*  |  source: Sprite sheet slicing

- A (true): Each cell is a frame.
- B (true): The order is part of the animation.
- C (true): Looping repeats the sequence.
- D (false): Frame rate is speed; looping is repeat behaviour.
- E (true): Six times two is twelve.

**9.** A tool call returns a structured reply saying the named scene object could not be found. Which statements describe the failure correctly? Check each statement that is true.  *(5 points)*

- [ ] A. This is a transport failure, so the next step is changing the network port.
- [ ] B. The object identity is irrelevant to the next investigation.
- [ ] C. Reinstalling the language model is the first diagnosis the evidence supports.
- [ ] D. A structured reply shows that the object was modified.
- [ ] E. This is a tool execution error: the operation ran and reported failure in its result.

**Key:** A=F B=F C=F D=F E=T  |  `MA-mcp.10`  |  *MCP fundamentals*  |  source: layered errors

- A (false): The reply arrived, so delivery worked.
- B (false): The error concerns the target, so identity and scene state are next.
- C (false): Nothing points at the model.
- D (false): The reply states the opposite.
- E (true): Domain failure travels inside a successful exchange.

**10.** A game has a moving platform, a crate that tumbles, and a player character. Check each statement that is true about body types.  *(5 points)*

- [ ] A. A static body is moved around by applying impulses.
- [ ] B. A crate that should tumble under physics is a good fit for a static body.
- [ ] C. A rigid body is moved by the physics simulation using forces, mass and collisions.
- [ ] D. A kinematic body falls under gravity by itself without any code.
- [ ] E. A kinematic body is moved by code (or animation) and is not pushed around by forces.

**Key:** A=F B=F C=T D=F E=T  |  `MA-jargon.26`  |  *Jargon test: game movement*  |  source: Kinematic versus rigid body

- A (false): A static body does not move.
- B (false): A static body does not move; a tumbling crate needs a rigid body.
- C (true): Rigid bodies are simulated.
- D (false): A kinematic body only moves when code moves it.
- E (true): Kinematic bodies obey the script, and can still push other bodies.

**11.** A texture looks stretched on a model. Check each statement that is true about UVs.  *(5 points)*

- [ ] A. A stretched texture means the image file is too small to use.
- [ ] B. UV coordinates store the direction in which the surface faces.
- [ ] C. UV stands for the ultraviolet value of a pixel.
- [ ] D. UV coordinates store a colour for each point on a surface.
- [ ] E. UV unwrapping flattens a 3D mesh into 2D so it can be painted.

**Key:** A=F B=F C=F D=F E=T  |  `MA-jargon.33`  |  *Jargon test: shaders and materials*  |  source: UV coordinates

- A (false): Stretching usually comes from an uneven UV layout, not from the image.
- B (false): Surface direction is stored by the normal.
- C (false): U and V are the names of the two texture axes.
- D (false): UVs are 2D lookup coordinates; colour comes from the texture they look up.
- E (true): Unwrapping produces the UV layout.

**12.** A game test fails intermittently. It spawns at a random position, and it uses an asset that is imported asynchronously. Check each statement that is true.  *(5 points)*

- [ ] A. An import failure and a gameplay failure are the same cause.
- [ ] B. An asynchronous import finishes later than the request, so a test that proceeds at once may use an asset that is not ready.
- [ ] C. Reporting the first passing rerun is adequate evidence that an intermittent failure is gone.
- [ ] D. A fixed timestep advances the simulation by a different amount depending on rendering speed.
- [ ] E. Rendered frames and elapsed game time are interchangeable when the simulation speed varies.

**Key:** A=F B=T C=F D=F E=F  |  `MA-verification.16`  |  *Agent testing, troubleshooting and engine comparisons*  |  source: Asynchronous import, fixed timestep

- A (false): They are different causes and a test should tell them apart.
- B (true): Asynchronous means the work completes without blocking the caller.
- C (false): Intermittent failures need repeated runs under controlled setup.
- D (false): A fixed timestep advances by a constant amount each tick.
- E (false): Frame count measures drawing, not simulated time.

**13.** Most engines give an object a hook that runs once when it is ready to be used (Godot's _ready, Unity's Start, Unreal's BeginPlay) and a hook that runs repeatedly (Godot's _process, Unity's Update, Unreal's Tick). Check each statement that is true.  *(5 points)*

- [ ] A. A hook that runs one time is unsuitable for starting a looping timer, because the hook does not repeat.
- [ ] B. In Godot, _ready is called again each time a node is removed from the scene tree and added back.
- [ ] C. A per-frame hook is the right place to build the player's starting inventory, because it keeps retrying until it succeeds.
- [ ] D. In Godot, children's _ready callbacks run before the parent's, so the parent can rely on its children being set up.
- [ ] E. In Unity, Start is called before the script's first frame update, and when the script instance is enabled.

**Key:** A=F B=F C=F D=T E=T  |  `MA-vocab.15`  |  *Engine vocabulary (Godot, Unity, Unreal)*  |  source: Start hook versus per-frame hook

- A (false): A once-only hook can start a repeating process; it starts it once.
- B (false): _ready is called once per node unless it is explicitly requested again.
- C (false): Setup in a per-frame hook repeats each frame or needs a guard flag; setup belongs in the once-only hook.
- D (true): Children are ready first, then the parent.
- E (true): Start runs before the first frame update for an enabled script.

**14.** A material request says "use the normal on this surface" in one line and "use the normal map" in another. Check each statement that is correct.  *(5 points)*

- [ ] A. Flipping the normal changes the surface's albedo colour, so the agent edits the colour texture.
- [ ] B. A normal map is an ordinary map for the surface's colour.
- [ ] C. A normal map is a texture that stores a normal for each texel.
- [ ] D. A normal is a direction perpendicular to a surface at a point.
- [ ] E. A normal is the usual, default value of a parameter.

**Key:** A=F B=F C=T D=T E=F  |  `MA-k03.8`  |  *Jargon test: false friends*  |  source: Normal versus normal map

- A (false): Flipping a normal reverses the direction a surface faces for lighting, so editing colour would leave the lighting error in place.
- B (false): Colour belongs to the albedo texture, and an agent putting a normal map there would produce a strange purple surface.
- C (true): A normal map is an image file, so the agent assigns it to a texture slot rather than computing a vector.
- D (true): A normal is a vector used for lighting, so the agent reads or writes it as a direction.
- E (false): That is the everyday sense of the word, and an agent using it would reset a parameter instead of reading a surface direction.

**15.** A vague prompt reads "make the camera feel more alive when the player gets hit". Check each rewrite that uses the exact camera jargon correctly to ask for a sensible hit effect.  *(5 points)*

- [ ] A. "Add a deadzone around the player when hit so the camera freezes in place."
- [ ] B. "Truck the camera up and down on hit so it looks up at the player."
- [ ] C. "On hit, briefly reduce the field of view by a few degrees (a quick zoom in), then ease it back."
- [ ] D. "Add screen shake on hit: 0.2 seconds, small random offset of the camera position, with the amplitude decaying to zero."
- [ ] E. "Dolly the lens narrower when hit."

**Key:** A=F B=F C=T D=T E=F  |  `MA-jargon.8`  |  *Jargon test: camera movement*  |  source: Rewrite a vague camera prompt

- A (false): A deadzone is a framing region for following; it does not freeze the camera on an event.
- B (false): Up and down movement is a pedestal, and looking up is a tilt; a truck is sideways.
- C (true): A field-of-view punch is a valid zoom effect and is described with exact terms.
- D (true): This names the effect, its duration, what moves and how it fades.
- E (false): A dolly moves the camera body; a narrower lens is a zoom.

**16.** A developer tells a coding agent: "Make the hull shinier." The hull material has a weathered-wood albedo, metallic 0 and roughness 0.8. Check each statement that is true about the terms.  *(5 points)*

- [ ] A. Lowering roughness makes reflections sharper and highlights tighter, which reads as shinier.
- [ ] B. In an engine that exposes smoothness instead of roughness, shinier means a lower smoothness value.
- [ ] C. Brightening the albedo texture is a gloss change, because lighter surfaces reflect sharper images.
- [ ] D. "Shinier" is an imprecise word, because glossy paint (metallic 0, low roughness) and polished metal (metallic near 1, low roughness) are different setups.
- [ ] E. Raising the emission colour is the exact term-level change for shine, because emission adds highlights.

**Key:** A=T B=F C=F D=T E=F  |  `MA-ch07.2`  |  *None*  |  source: Shinier versus roughness, metallic and specular

- A (true): Roughness is the blur of reflections, so a lower value gives a sharper highlight.
- B (false): Smoothness is roughly the inverse of roughness, so shinier means a higher smoothness.
- C (false): Albedo changes the base colour, not the sharpness of reflections.
- D (true): A precise prompt names roughness and metallic instead of the vague word shinier.
- E (false): Emission is light a surface gives off by itself, which makes it glow rather than reflect.

**17.** Choose the body or area type for each object in a level. Check each statement that is true.  *(5 points)*

- [ ] A. The player character moved by script is a static body.
- [ ] B. A tumbling crate pushed around by physics is a rigid body.
- [ ] C. A platform moved by a script or animation is a rigid body.
- [ ] D. A coin that detects overlap without blocking is a trigger.
- [ ] E. A wall that does not move is a static body.

**Key:** A=F B=T C=F D=T E=T  |  `MA-jargon.71`  |  *Jargon test: from the essay prompts*  |  source: Body types for level objects

- A (false): A script-controlled mover is kinematic, not static.
- B (true): A rigid body is simulated by the physics engine.
- C (false): A body moved by code or animation is kinematic.
- D (true): A trigger is a volume that reports overlap and does not block.
- E (true): Static bodies are fixed in place.

**18.** A scene has twenty instances of a lamp prefab, and one named lamp should turn blue. Which statements use the terms correctly? Check each statement that is true.  *(5 points)*

- [ ] A. Reverting an override returns the instance to the prefab's value.
- [ ] B. A prefab instance is a placed copy in the scene that stays linked to its prefab asset.
- [ ] C. Deleting the prefab asset is a way to isolate one lamp.
- [ ] D. An override changes a value on one instance without changing the prefab asset.
- [ ] E. Applying an override to the prefab keeps the change on one instance.

**Key:** A=T B=T C=F D=T E=F  |  `MA-unity.7`  |  *Unity, Spark and agent workflows*  |  source: prefab instance versus asset

- A (true): Revert discards the per-instance difference.
- B (true): Instances derive from the prefab asset.
- C (false): That damages the reusable asset.
- D (true): Overrides are per-instance differences.
- E (false): Applying writes the change into the prefab asset, so other instances pick it up.

**19.** An Unreal editor MCP server lets an external assistant call editor operations. A designer asks whether this makes the assistant the NPC's runtime AI. Check each statement that is true.  *(5 points)*

- [ ] A. Editor automation and runtime AI are two names for the same role.
- [ ] B. An MCP server connected to the editor becomes the NPC's behaviour in the packaged build.
- [ ] C. An MCP server exposes tools that an external assistant can call.
- [ ] D. A tool call that places an Actor is an example of runtime AI.
- [ ] E. Runtime AI is the NPC's decision logic executing while the game is played.

**Key:** A=F B=F C=T D=F E=T  |  `MA-unreal.1`  |  *Unreal and agent workflows*  |  source: Editor automation versus runtime AI

- A (false): One changes the project; the other controls behaviour in play.
- B (false): The packaged game needs its own gameplay logic.
- C (true): A server publishes named operations (tools) that a client can invoke.
- D (false): Placing an Actor is editor automation, a development-time change.
- E (true): Runtime means during play of the built or running game.

**20.** A local service was reachable from other machines, and the team sees unexpected edits. Check each statement that is true.  *(5 points)*

- [ ] A. Blast radius is the extent of what an incident could affect.
- [ ] B. Containment means deleting the logs.
- [ ] C. Recovery and containment are the same step.
- [ ] D. Containment limits further damage, for example by stopping an exposed service.
- [ ] E. Evidence preservation means keeping logs and change records.

**Key:** A=T B=F C=F D=T E=T  |  `MA-security.10`  |  *Agent security and local versus cloud execution*  |  source: Incident terms

- A (true): It sizes the possible impact.
- B (false): Containment limits further access; deleting logs destroys evidence.
- C (false): Containment comes first; recovery restores state.
- D (true): It stops the spread.
- E (true): They support scoping the incident.
