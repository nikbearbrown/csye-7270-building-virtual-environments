# Jargon test: false friends

## MA-k03.1

A teammate says "the signal is not arriving". The bug report concerns a Coin node that should tell the HUD to add a point, and the agent has to know which meaning of "signal" is in use. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. If the report is about a node's body_entered not reaching its handler, the places to check are the connection, the area's mask and monitoring.
- [ ] B. A request that says "handle the signal" without saying which one leaves the agent guessing between event, OS signal and audio or electrical signal.
- [ ] C. A signal emitted with nothing connected to it does nothing visible, so a missing handler call points the agent at the connection.
- [ ] D. In Godot, a signal is a named event a node emits, which other nodes connect functions to.
- [ ] E. In Godot, a signal is a message sent from the operating system to the running game process.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: These are the Godot causes of a missing body_entered call, so the agent inspects the connection and physics settings.
- B: The word has several meanings across software and hardware, so the agent may build the wrong kind of handler.
- C: Emitting without a connected function silently has no effect, which makes the missing connection the first thing to check.
- D: This is the engine meaning, so the agent should look at connections between nodes rather than operating system messages.
- E: That describes an OS signal, and an agent acting on it would write process-level handlers instead of node connections.

**Source:** Signal (false friend)

## MA-k03.2

A designer says "make the forest scene" and also "build the forest level". Check each statement that is correct about the two words in Godot. Each statement is worth 1 point (5 points total).

- [ ] A. A level is a Godot file type with its own extension, so the forest should be saved as a level file.
- [ ] B. A level is a playable area, usually built as a scene in Godot.
- [ ] C. A scene is a saved tree of nodes that can be reused or instanced inside another scene, whether it is a whole area or a single coin.
- [ ] D. A coin should be placed in the levels folder because it is saved as a scene.
- [ ] E. A game has fewer scenes than levels, because levels are made of scenes.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: Godot has no level file type, so the agent would create a file the editor cannot open.
- B: Level is a design word for a playable space, and the engine represents it with an ordinary scene.
- C: Scene is the engine's container type, so a single pickup and an entire area are both scenes.
- D: A coin is a scene but not a level, so the agent would misfile reusable pieces among playable areas.
- E: A level is usually one scene, and the game also has scenes for menus, enemies and items, so scenes outnumber levels.

**Source:** Scene versus level

## MA-k03.3

A request says "set the mask so the laser ignores glass". Check each statement that correctly separates the meanings of mask in a game project. Each statement is worth 1 point (5 points total).

- [ ] A. Setting a collision mask changes how the object is drawn.
- [ ] B. A light cull mask decides which bodies the laser ray ignores, so the agent edits the light node.
- [ ] C. A collision mask and a collision layer are the same setting, so setting the glass's layer is enough to make the laser ignore it.
- [ ] D. An alpha mask in the glass texture is where to make the laser ignore glass, so the agent edits the image.
- [ ] E. A collision mask lists the physics layers an object scans for or is blocked by.

**Key:** A=F B=F C=F D=F E=T

**Why:**

- A: A collision mask is a physics setting, so an agent would be wrong to expect any visual change from it.
- B: A light cull mask picks which render layers a light affects, so editing it leaves the physics ray unchanged.
- C: Layer says what the object is while mask says what it checks, so changing the glass layer would not change the laser.
- D: An alpha mask only controls which pixels are visible, so editing the texture would change looks and leave the laser blocked.
- E: The laser's ray or body checks its mask, so removing the glass layer from that mask makes the laser ignore glass.

**Source:** Mask (false friend)

## MA-k03.4

A build report says "the physics is stable". The next step depends on whether this means resting bodies stay still or something else. Check each statement that is correct about what an agent could be claiming. Each statement is worth 1 point (5 points total).

- [ ] A. It could mean the sort of a list is stable, which means the list is sorted in place.
- [ ] B. It means the physics solver is deterministic, so replays match exactly.
- [ ] C. A stable sort keeps items with equal keys in their original relative order.
- [ ] D. It could mean no jitter or drift when bodies rest on each other.
- [ ] E. "Stable" here is a precise measurement, so the claim needs no follow-up.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Stability in sorting concerns the order of equal items, so an agent confusing it with in-place sorting would build the wrong thing.
- B: Stable simulation means resting bodies do not jitter, and an agent assuming determinism would build replay checks instead of testing resting stacks.
- C: This is a third meaning of the word, unrelated to physics, and matters when sorting a leaderboard by score.
- D: This is simulation stability, and the check is to stack bodies in a scene and watch whether they settle.
- E: The report does not say which meaning or how it was measured, so the agent should ask before accepting it.

**Source:** Stable (false friend)

## MA-k03.5

An agent says "the edit is atomic" after changing three script files for one feature. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. An atomic edit means the change is small, such as one line.
- [ ] B. A claim that the edit is atomic does not say the edit was tested, so the agent still runs the tests.
- [ ] C. An atomic commit groups one logical change, which may touch several files.
- [ ] D. An atomic edit is applied completely or not at all, with no half-applied state left behind.
- [ ] E. If an atomic multi-file change fails on the third file, the first two files are restored.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Atomic describes completeness of application rather than size, so an agent treating it as small would accept a half-applied large edit.
- B: Atomicity and testing are separate properties, and relying on the word alone would let broken code be accepted.
- C: Here atomic refers to a single coherent change, so three related scripts can belong in one atomic commit.
- D: Atomic means all or nothing, so a failed edit must leave the project exactly as it was.
- E: All-or-nothing behaviour means partial results are rolled back, so the project does not end in a mixed state.

**Source:** Atomic (false friend)

## MA-k03.6

A load-time report says "the cache was cleared and loading got slower". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A stale cache can show an old result after a source file changed.
- [ ] B. Clearing a cache costs time once, since the stored results must be rebuilt.
- [ ] C. A cache is the source of truth for the project, so deleting it loses work.
- [ ] D. A cache holds results that were already computed, such as imported assets or compiled shaders, so they need not be computed again.
- [ ] E. A CPU cache and a project import cache are different stores that share a name.

**Key:** A=T B=T C=F D=T E=T

**Why:**

- A: When a cached result is out of date, clearing it is a sensible first fix for odd behaviour.
- B: The slower load is a one-time rebuild cost, so an agent should not treat it as a permanent regression.
- C: A cache can be regenerated from the sources, so an agent that refuses to delete it would waste effort.
- D: A cache saves repeated work, which is why clearing it makes the next load slower.
- E: One is hardware memory near the processor and the other is a folder of converted assets, so clearing one does not affect the other.

**Source:** Cache (false friend)

## MA-k03.7

A designer asks for "a 12 frame walk cycle with keyframes on frames 1, 4 and 7". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. Keyframes on frames 1, 4 and 7 mean frames 2, 3, 5 and 6 stay blank until the agent adds keyframes there.
- [ ] B. A keyframe is a stored value at a specific time, and the frames between come from interpolation in an animation track.
- [ ] C. A frame is one displayed image in time, and a sprite sheet cell holds one.
- [ ] D. Counting an animation's length in frames tells you how many keyframes it holds.
- [ ] E. A frame and a keyframe are the same thing, so 12 frames means 12 keyframes.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: The in-between frames get values by interpolation, so adding more keyframes would change the requested animation.
- B: Keyframes are the stored values, so the agent adds three keys to the track and lets playback fill in the rest.
- C: The agent should plan twelve cells in the sheet because each frame is one displayed image.
- D: Keyframes are only the stored values, so a twelve frame animation can hold three keyframes and an agent counting frames would add too many.
- E: They are different, and an agent treating them as equal would build twelve keys instead of three.

**Source:** Frame versus keyframe

## MA-k03.8

A material request says "use the normal on this surface" in one line and "use the normal map" in another. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. Flipping the normal changes the surface's albedo colour, so the agent edits the colour texture.
- [ ] B. A normal map is an ordinary map for the surface's colour.
- [ ] C. A normal map is a texture that stores a normal for each texel.
- [ ] D. A normal is a direction perpendicular to a surface at a point.
- [ ] E. A normal is the usual, default value of a parameter.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Flipping a normal reverses the direction a surface faces for lighting, so editing colour would leave the lighting error in place.
- B: Colour belongs to the albedo texture, and an agent putting a normal map there would produce a strange purple surface.
- C: A normal map is an image file, so the agent assigns it to a texture slot rather than computing a vector.
- D: A normal is a vector used for lighting, so the agent reads or writes it as a direction.
- E: That is the everyday sense of the word, and an agent using it would reset a parameter instead of reading a surface direction.

**Source:** Normal versus normal map

## MA-k03.9

A report says "the static light is baked". Check each statement that is correct about the word static in a game project. Each statement is worth 1 point (5 points total).

- [ ] A. Static lighting means light that is recomputed each frame, so the agent skips baking it.
- [ ] B. Static typing makes objects unable to move.
- [ ] C. Static typing in a script means declaring the types of variables.
- [ ] D. StaticBody is a physics body that is not moved by forces.
- [ ] E. A StaticBody2D is pushed around by forces like a RigidBody2D.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Static lighting does not change at run time and may be baked, so skipping the bake would leave the scene unlit.
- B: Static typing concerns variable types in scripts, so an agent confusing it with physics would freeze objects needlessly.
- C: This is the language meaning, so the agent adds type annotations rather than changing physics bodies.
- D: A static body stays put under collisions, so an agent uses it for walls and floors.
- E: A static body ignores forces, and an agent using it for a crate that should be pushed would build a crate that never moves.

**Source:** Static (false friend)

## MA-k03.10

A log line says "process finished with errors". The agent has to decide whether to debug a node or the program run. Check each statement that is correct about the word process. Each statement is worth 1 point (5 points total).

- [ ] A. A _process function is a separate operating system process.
- [ ] B. In an operating system, a process is a script function the engine calls each frame.
- [ ] C. Each node's process runs on its own processor core by default.
- [ ] D. In Godot, _process is a function called each rendered frame.
- [ ] E. In a terminal, "Process finished" means the node's _process stopped being called, so the agent debugs the game loop.

**Key:** A=F B=F C=F D=T E=F

**Why:**

- A: It is a function inside the game process, and an agent treating it as a separate program would look for the wrong thing.
- B: An OS process is a running program, and mixing it up with _process leads to the wrong fix.
- C: Godot runs _process on the main thread by default, so an agent expecting parallelism would skip needed safety checks.
- D: This is the engine meaning, so an error in it would show up repeatedly while the game runs.
- E: The message normally refers to the whole program run ending, so the agent should read the exit code and earlier errors.

**Source:** Process (false friend)

## MA-k03.11

A build request mentions "export" in three ways: an exported variable, an exported project, and an export from Blender. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. An exported variable (@export) shows a script property in the Inspector.
- [ ] B. An exported variable and an exported project are unrelated features that share a word, so editing @export does not create a build.
- [ ] C. Exporting a project packages the game into a build for a platform.
- [ ] D. Exporting from Blender writes the model to a file format such as glTF.
- [ ] E. An exported variable is the build file that is shipped.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: This is the script meaning, so the agent adds an annotation to the variable rather than configuring a build.
- B: Adding an annotation changes the Inspector only, and an agent expecting a build from it would never produce one.
- C: This uses an export preset to produce a shippable build, which has nothing to do with Inspector properties.
- D: This is the asset meaning, and the file produced is what Godot later imports.
- E: The shipped file comes from exporting the project, and an agent mixing them up would look for the wrong output.

**Source:** Export (false friend)

## MA-k03.12

A designer says "spawn ten instances". An agent should keep separate the senses of instance. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. GPU instancing and scene instancing are the same feature.
- [ ] B. GPU instancing draws many copies of one mesh in one draw call.
- [ ] C. Instancing a scene in Godot creates a new copy of its node tree.
- [ ] D. An instance of a script class is the class definition in the .gd file, so spawning ten instances means writing ten script files.
- [ ] E. Instancing a scene gives copies that share one set of variable values.

**Key:** A=F B=T C=T D=F E=F

**Why:**

- A: They differ, and an agent that treats them as one would use the wrong tool to spawn gameplay objects.
- B: This is the rendering meaning, used for efficient drawing of grass or crowds.
- C: Each instance_ call builds a fresh node tree, which the agent then adds to the scene.
- D: An instance is an object created from the class, and the agent should call new on one class ten times.
- E: Each instance has its own values, and an agent assuming sharing would write code that fails to update the others.

**Source:** Instance (false friend)

## MA-k03.13

A texture request says "give the crate a metal material" while a physics request says "give the crate a bouncy material". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A physics material controls friction and bounce.
- [ ] B. A render material controls how a surface looks, for example colour and shininess.
- [ ] C. A shiny render material makes the crate slide more easily, so the agent edits the render material for slipperiness.
- [ ] D. The two settings live on different parts of the object.
- [ ] E. A bouncy physics material changes the crate's colour.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: The bouncy request is about motion, so the agent sets bounce on a physics material on the body.
- B: The metal request is about appearance, so the agent edits the render material on the mesh.
- C: Render materials affect appearance, and slipperiness comes from the physics material's friction.
- D: The render material is on the mesh and the physics material is on the body, so both requests need separate edits.
- E: Physics materials set friction and bounce, so an agent editing them would not change the look.

**Source:** Material (false friend)

## MA-k03.14

A designer asks for "a trigger on the door" without saying what kind. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A trigger zone blocks the player like a wall.
- [ ] B. A trigger means the same setting in Godot, Unity and Unreal.
- [ ] C. In an animation system, a trigger can be a parameter that starts a transition.
- [ ] D. In Unity, Is Trigger makes a collider detect overlaps instead of blocking.
- [ ] E. In Godot, a trigger zone is usually an Area2D or Area3D that detects overlaps and does not block.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: A trigger detects overlaps and lets bodies pass, so an agent building a wall would stop the player at the door.
- B: The terms differ between engines, and an agent copying a Unity tutorial would look for a setting that Godot does not have.
- C: This third meaning is a one-shot parameter in an animation state machine rather than a physical zone.
- D: This is the Unity setting, and it explains why Unity tutorials describe triggers differently than Godot ones.
- E: The agent builds an Area node with a collision shape and connects its body_entered signal.

**Source:** Trigger (false friend)

## MA-k03.15

A request says "scale the enemy", "scale the time" and "scale the texture". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. Changing texture scale makes the mesh larger, so the agent uses it to resize the crate.
- [ ] B. Changing a sprite's scale resizes a sibling collision shape automatically.
- [ ] C. Time scale changes how fast game time runs, such as for slow motion.
- [ ] D. Scaling a node by 2 changes the time scale of the game.
- [ ] E. Scaling a node changes its size, and its children inherit the scale.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Texture scale or UV tiling repeats or stretches the pattern, and leaves the mesh size the same.
- B: A sibling shape is a separate node, so the agent must scale it too or the hitbox will not match.
- C: This is the engine setting Engine.time_scale, which affects everything driven by delta.
- D: Node scale and time scale are separate, and an agent mixing them up would double the size when speed was wanted.
- E: The agent sets the node's scale property and children, including collision shapes, grow with it.

**Source:** Scale (false friend)

## MA-k03.16

A rig request says "put the origin at the feet" and also "move the pivot". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. Moving the pivot of a sprite changes the point it rotates around while its position stays fixed.
- [ ] B. Setting the origin at the feet makes placing the character on a floor line simple.
- [ ] C. The world origin is the zero point of the scene's coordinates.
- [ ] D. The origin and the world origin are the same thing.
- [ ] E. A node's origin is the point its position refers to, and rotation happens around it unless an offset is set.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: A pivot shifts the rotation centre, so the agent uses it for a spinning pickup without changing where it stands.
- B: With the origin at the feet, setting the y position to the floor height puts the character on the ground.
- C: All positions are measured from it in global space, so the agent uses it as a reference when placing the rig.
- D: A node origin is local to the node while the world origin is the scene's zero point, so an agent mixing them would misplace objects.
- E: The agent places the node's origin at the feet, so position values describe where the feet stand.

**Source:** Origin and pivot

## MA-k03.17

A report says "lighting is baked", a rig note says "animation baked", and a navigation note says "navmesh baked". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A baked lightmap updates when a light is moved at run time.
- [ ] B. Baking a navigation mesh stores the routes each agent will walk, so a moved obstacle changes the route without a rebake.
- [ ] C. Baking animation turns procedural or constraint-driven motion into stored keyframes.
- [ ] D. Baked means the result can be edited by changing the original settings alone.
- [ ] E. Baking light precomputes lighting into textures so it is not computed at run time.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: A baked lightmap stays fixed, so an agent expecting live shadows from it would see stale lighting.
- B: Baking precomputes the walkable area from level geometry rather than routes, so a moved obstacle needs a rebake or dynamic obstacle handling.
- C: This freezes the motion into keys, so the clip plays back without the original rig logic.
- D: The result must be baked again, and an agent that only edits settings would leave the old baked data in place.
- E: The result is a lightmap, which makes lighting cheap but means it must be baked again after changes.

**Source:** Bake (false friend)

## MA-k03.18

A 2D level request mixes tile, TileSet and TileMap. Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. Changing a tile's collision shape in the TileSet affects each cell that uses that tile.
- [ ] B. A TileSet is the node that holds the level layout, so the agent paints the level on it.
- [ ] C. A TileMap is the node that places tiles from a TileSet into a grid.
- [ ] D. A TileMap is the image file with the tile pictures, so the agent imports it as a texture.
- [ ] E. A TileSet is the collection of tiles, with their images and collision shapes, that can be used.

**Key:** A=T B=F C=T D=F E=T

**Why:**

- A: The shape is shared by the tile, so one edit updates every placed copy of it.
- B: The TileMap holds the layout, and painting on the TileSet would change the palette rather than the level.
- C: The TileMap holds the level layout, so the agent paints cells on it using the TileSet.
- D: The image is the atlas texture used by a TileSet, and importing a TileMap as a picture would give the agent nothing to paint.
- E: The TileSet is the palette resource, so the agent defines tile images and collisions there.

**Source:** Tile, TileSet, TileMap

## MA-k03.19

A rendering note says "shader" and a design note says "material". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A material is an asset that holds a shader and the parameter values, such as textures and colours.
- [ ] B. A shader is a program that runs on the GPU to compute vertex positions or pixel colours.
- [ ] C. A shader holds the specific textures for one crate.
- [ ] D. A material is a program that runs on the GPU.
- [ ] E. Each material needs its own copy of the shader, so ten crate colours mean ten shader programs.

**Key:** A=T B=T C=F D=F E=F

**Why:**

- A: The material supplies the settings, so the agent assigns textures and colours on it.
- B: The shader holds the code, so the agent writes GPU logic there.
- C: The material holds those values, and an agent storing textures in a shader would break reuse across objects.
- D: That describes the shader, and an agent writing code into a material would find nowhere to put it.
- E: Materials can share one shader with different parameter values, and copying the shader would multiply the code to maintain.

**Source:** Shader versus material

## MA-k03.20

A Godot task says "load the resource" and a profiling note says "the resource usage is high". Check each statement that is correct. Each statement is worth 1 point (5 points total).

- [ ] A. A Godot Resource is the memory the game is using.
- [ ] B. An agent asked to "reduce resources" could mean files or system load, and should be told which.
- [ ] C. In Godot, a Resource is a data object that can be saved to a file, such as a texture or an animation.
- [ ] D. Loading a Resource file lowers the processor usage.
- [ ] E. Resource usage in a profiling note usually means memory or processor time used by the game.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A Resource is a data object, and an agent treating it as memory use would profile when a file load was wanted.
- B: The phrase is ambiguous, and guessing could delete data files when the goal was to lower memory use.
- C: This is the engine meaning, so "load the resource" calls the load function on a file path.
- D: Loading a file adds work, so an agent expecting a performance gain from loading would not fix the profiling issue.
- E: This is the system meaning, so the agent should open the profiler rather than load a file.

**Source:** Resource (false friend)
