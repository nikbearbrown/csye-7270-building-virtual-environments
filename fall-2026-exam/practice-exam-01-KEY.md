# Practice exam 01: ANSWER KEY (read it only AFTER doing the exam cold)

Each statement is scored on its own, 1 point. Under every statement is the reason it is true or false, and each question names the course chapter passage it follows. The answers are **awaiting a game developer's check**; if a key looks wrong to you, say so.

## 1. Chapter 0: Checking an agent's report against evidence

**An AI coding agent reports "Done, all tests pass." Check each statement that is true about what that report shows.**  *(5 points)*

**True: C, E** (2 of 5)

- **A. FALSE.** A clean import and script check shows that the game's behaviour is right.
  - Why: It shows only that the project and scripts parse.
- **B. FALSE.** Playing the game yourself once shows what every player on every machine will experience.
  - Why: It shows only what you experienced.
- **C. TRUE.** The agent saying "done" shows that the agent produced a message, not that the game works.
  - Why: Rung 1 of the evidence ladder.
- **D. FALSE.** A passing test shows that the game is fun and readable.
  - Why: A scripted test does not establish feel or readability.
- **E. TRUE.** A listing of the changes (a diff) shows exactly what changed but not that the change works.
  - Why: Rung 2.

*Covered in:* Ch 0, 'The evidence ladder'.

## 2. Chapter 0: Working safely with an agent (instruction files, permissions, headless runs)

**A student sets up an AI coding agent on a game project and chooses what it may do without asking.**  *(5 points)*

**True: B, C, D, E** (4 of 5)

- **A. FALSE.** A permission prompt is a formality to click through quickly, because the agent only asks about commands that are safe.
  - Why: The chapter says to treat the prompt as a review, not a formality.
- **B. TRUE.** A sandbox that confines writing to the project folder can block a harmless write elsewhere, such as a tool saving its own settings, without stopping the rest of the work.
  - Why: Codex's sandbox blocked the editor's settings file but the project's own files and later commands worked.
- **C. TRUE.** A permission rule decides which commands the agent may run without asking a person, and a sandbox limits where the agent's commands can write.
  - Why: Allow rules name what runs without a prompt; the sandbox policies read-only, workspace-write and full access limit writing.
- **D. TRUE.** Allowing a program that can run scripts the agent writes is a wide permission, because those scripts can do things the program's name does not suggest.
  - Why: An allow rule is a boundary around programs, and a program that runs code is no boundary at all.
- **E. TRUE.** The setting that lets an agent run any command without asking is meant only for isolated containers or virtual machines, not for an everyday personal machine.
  - Why: The bypass mode is listed as 'Everything. For isolated containers and VMs only'.

*Covered in:* Ch 0, 'Permissions and sandboxes: what the agent may touch': the permission modes and allow rules (what runs without asking); Codex's three sandbox policies; a wide rule such as an allowed program that runs any script ('a program that runs code is no boundary at all'; 'treat the permission prompt as a review, not a formality'); the Codex sandbox blocking a write to the editor settings outside the project folder; the mode that runs everything is 'for isolated containers and VMs only'.

## 3. Chapter 1: Walker, Godot projects and how a game updates

**A student opens a Godot project folder for the first time and wants to know how it is organised.**  *(5 points)*

**True: A, B** (2 of 5)

- **A. TRUE.** A project is a folder with a project settings file at its top level, and paths inside the project are measured from the folder that holds that file.
  - Why: The project file at the root marks the project, and the project path prefix means that folder.
- **B. TRUE.** A saved scene is a text file listing its nodes, their settings and their signal connections, so a diff can show exactly what changed in it.
  - Why: Scenes are saved as text, so an agent can read them and version control can diff them.
- **C. FALSE.** A project whose saved scene holds a single node must be nearly empty, because everything in a running game comes from saved scenes.
  - Why: The starter platformer's saved scene is six lines, yet code builds the whole level when the game starts.
- **D. FALSE.** The import cache folder, which the editor rebuilds, should be committed to version control so every machine has the same imported assets.
  - Why: The cache is rebuilt from the project files and is left out of version control on purpose.
- **E. FALSE.** Imported pictures and sounds are stored as text, so an agent can read a picture's pixels the same way it reads a saved scene.
  - Why: Images and audio are binary; the agent sees file names and import settings, not pixels or sounds.

*Covered in:* Ch 1, 'The project: a text file and a virtual file system' (a project is a folder with a project settings file at its root; the resource path prefix means the folder containing that file), 'Nodes, scenes, and the scene tree' (scenes are saved as text; the starter's saved scene is six lines and everything else is built by code when the game starts) and 'What an agent can read' (images, models, audio are binary; the editor cache is not committed).

## 4. Chapter 2: Game art and sound (pixel art, asset requests, loops)

**A student asks an image generator for a game sprite and then has to use the result in a 2D game.**  *(5 points)*

**True: A, C** (2 of 5)

- **A. TRUE.** To get a character facing both ways, it is better to generate one facing direction and flip it in the game, since generators often draw 'left' and 'right' the same.
  - Why: The chapter says to generate one facing direction and flip it at runtime.
- **B. FALSE.** A prompt made of mood words such as menacing and crisp is enough to give a file that can be checked for size and frame layout.
  - Why: The engine responds to numbers such as size and frame count; mood words give a picture, not a checkable file.
- **C. TRUE.** A request that asks the generator for a transparent background often gets a painted checkerboard, so a plain solid background that is removed afterwards works better.
  - Why: Generators tend to paint a checkerboard rather than real transparency.
- **D. FALSE.** A generated image that looks like finished game art in a picture viewer has already met the engine's needs for size, background and frame layout.
  - Why: The viewer shows none of the engine's constraints; size, background, layout and collider are all still open.
- **E. FALSE.** A tool that cuts an image into equal grid cells always works correctly, even on a picture where the generator placed the creatures freely.
  - Why: A freely laid-out image is not a grid; the cutting tool still reports success while cutting the creatures in pieces.

*Covered in:* Ch 2, idea 1 'A prompt is a specification, and the engine reads the result' (mood words versus the engine's numbers; solid background, never 'transparent'; one facing direction, flipped at runtime, because 'facing left' and 'right' often come out identical; the constraint table), 'The question' (an image viewer shows none of the engine's questions) and 'The Walker asset helpers' (the grid assumption fails on a freely laid-out image).

## 5. Chapter 3: 3D assets from Blender to Godot

**In Blender, an artist makes a thin pole by stretching a large cube, then exports it to Godot. Check each statement that is true.**  *(5 points)*

**True: A, D** (2 of 5)

- **A. TRUE.** Stretching the cube changes the object's scale, but the mesh's own vertices still describe the original cube until the transform is applied.
  - Why: A Blender object has a transform and separate mesh data; scaling the object leaves the vertices describing the cube.
- **B. FALSE.** If the pole looks the right size in the running game, its transform must already have been applied.
  - Why: A pole with an unapplied scale can look identical in game; the mesh is then a cube wearing a scale.
- **C. FALSE.** Applying the transform is best left until after the model has been imported into Godot.
  - Why: The advice is to apply the object transform in the modeling software before exporting.
- **D. TRUE.** A collision shape generated from a mesh that carries a stretched scale inherits that scale, which is one reason to apply the transform before export.
  - Why: Anything generated from the mesh inherits the scale, and Godot's guidance is to avoid scaling collision shapes.
- **E. FALSE.** Applying the transform before export changes how the pole looks in the game, making it thinner or thicker.
  - Why: Applying moves the stretch into the vertices and resets the scale; the look does not change.

*Covered in:* Ch 3, 'Apply transforms: the object's scale versus the mesh's size' and 'The question' (the no_apply case): the object has a transform and mesh data; a pole made from a scaled 2 m cube still has cube vertices; the drawn size can look right while the node carries a non-unit scale; 'anything generated from that mesh inherits the scale'; apply the transform in the modeling software before exporting.

## 6. Chapter 3: Driving Blender with an agent (MCP and scripts)

**A teammate suggests that the agent write a Python script for Blender to run with no window, instead of chatting with an open Blender through MCP. Check each statement that is true about the difference.**  *(5 points)*

**True: B, D** (2 of 5)

- **A. FALSE.** Exploring an existing scene or adjusting one object in conversation suits a script better than a live MCP connection.
  - Why: The chapter gives that job to the live MCP connection; a script suits making an asset reproducibly.
- **B. TRUE.** A script leaves behind a file you can read, compare with earlier versions and rerun to rebuild the same asset.
  - Why: With the script route you keep a .py file you can diff, rerun and review.
- **C. FALSE.** A script can reach fewer Blender features than the MCP tools, because the tools use features that scripts cannot.
  - Why: The script calls the same Blender Python interface that the MCP tools call.
- **D. TRUE.** A script can encode a wrong assumption and then repeat it faithfully every time it runs.
  - Why: That is the stated failure mode of the script route.
- **E. FALSE.** With a live MCP connection, the project's version history automatically records how each change to the scene was made.
  - Why: The failure mode of the MCP route is that the scene changes and version history records nothing about how.

*Covered in:* Ch 3, 'Two ways for an agent to drive Blender', the MCP-versus-script comparison table (what you keep; good for; failure mode) and 'The script calls the same bpy API the MCP tools call.'

## 7. Chapter 4: Nodes, scenes, signals and groups

**A beginner is learning how a Godot game is built. Check each statement that is true.**  *(5 points)*

**True: B, C, D, E** (4 of 5)

- **A. FALSE.** A scene can only be a whole level.
  - Why: A scene can be as small as one enemy.
- **B. TRUE.** A node does one job, such as drawing a sprite, holding a collision shape or counting down a timer.
  - Why: A node does one job.
- **C. TRUE.** Reusing a saved scene as a template is called instancing, and an edit to the source scene shows up in its instances.
  - Why: Changing the source scene updates all instances.
- **D. TRUE.** A scene is a saved tree of nodes, and it can be a whole level or a single enemy.
  - Why: A scene can be a whole level or a single creep.
- **E. TRUE.** A signal is a message a node sends when something happens to it, and other nodes can connect to it to react.
  - Why: Signals let one node react to another without referencing it.

*Covered in:* Ch 4, 'Nodes and scenes: composition you can save' and 'Signals: who tells whom'.

## 8. Chapter 4: Collision (colliders, triggers, layers and masks)

**A coin in a 2D Godot game should add to the score when the player touches it, but the player should walk straight through it. Check each statement that is true.**  *(5 points)*

**True: A, E** (2 of 5)

- **A. TRUE.** A trigger is an area that reports when something overlaps it and never blocks or pushes.
  - Why: A detection area reports overlaps and never blocks or pushes.
- **B. FALSE.** The coin should be a solid collider, so the player is stopped by it and the score changes on touch.
  - Why: A solid collider would stop the player; the coin needs a non-blocking trigger.
- **C. FALSE.** A trigger works from the coin's picture, so it needs no collision shape.
  - Why: A trigger still needs a shape; the picture is not the collider.
- **D. FALSE.** The shape the physics engine uses is always the same as the picture the player sees.
  - Why: Nothing ties the collision shape to the art except the author's care.
- **E. TRUE.** A collider is a shape the physics engine uses to detect contact, and a solid one blocks other objects.
  - Why: A collision shape is geometry the physics engine uses; a solid body blocks.

*Covered in:* Ch 4, 'Four collision objects' (a detection area reports overlaps, never blocks or pushes) and 'The art is not the collider'.

## 9. Chapter 5: Game design documents and requirements

**A team is writing requirements for a new checkpoint feature in a 3D Godot world, and for a phone version of that world. They want each requirement to be checkable and honest. Check each statement that is true.**  *(5 points)*

**True: C** (1 of 5)

- **A. FALSE.** A requirement for a new feature should leave out existing behaviour, so that the requirement stays short and focused.
  - Why: A good criterion also says what must not change, such as the existing checks that must still pass.
- **B. FALSE.** Touch simulated with a mouse on a desktop is enough to call the phone version verified.
  - Why: Mouse-emulated touch is not a phone; what needs a device stays unverified.
- **C. TRUE.** A requirement is checkable when a stranger could write its test without having to ask the author what was meant.
  - Why: This is the chapter's test for a requirement a machine can check.
- **D. FALSE.** A scripted test cannot press a game's controls, so a feature's requirement has to be judged by a person playing.
  - Why: Scripted input can drive the game's ordinary controls; machine-checkable criteria are the point.
- **E. FALSE.** When a scripted test of the feature passes, that shows players can see the feature and will understand it.
  - Why: A pass shows the written criterion was met in that run, not that the feature is visible, understandable or fun.

*Covered in:* Ch 5, 'Acceptance criteria that a machine can check' (testable when a stranger could write the test without asking; name the quantity and unit, a tolerance, a time box, how the state is reached, what must not change, and what is out of scope), 'What a pass proves' under Verify (a pass does not prove the pad is visible, understandable, fair or worth having), and 'Scoping mobile, networked, and XR versions of a world' ('Mouse-emulated touch is not a phone'; name what stays unverified).

## 10. Chapter 6: Shaders

**A technical artist is learning what a shader is. Check each statement that is true.**  *(5 points)*

**True: B, C** (2 of 5)

- **A. FALSE.** When a shader decides one pixel's colour, it can look at the colour its neighbouring pixel ended up with.
  - Why: Each run is independent; a pixel cannot ask its neighbour.
- **B. TRUE.** One part of a shader decides where each corner of a shape lands, and another decides the colour of each pixel the shape covers.
  - Why: The vertex part and the per-pixel part.
- **C. TRUE.** A shader is a small program that runs on the graphics processor, not the main processor.
  - Why: The chapter's first definition.
- **D. FALSE.** A shader is where the game's rules, such as the score, are written.
  - Why: A shader draws; game rules live in game scripts.
- **E. FALSE.** A shader runs once for the whole image, from start to finish.
  - Why: It runs many times at once, once per vertex or pixel.

*Covered in:* Ch 6, 'A shader is a small program the GPU runs many times at once' and 'Shader types and processor functions'.

## 11. Chapter 7: Materials (material, shader, texture)

**A designer asks an AI agent to "make the metal crate look worn". Check each statement that is true about materials and textures.**  *(5 points)*

**True: A, D, E** (3 of 5)

- **A. TRUE.** A shader is the program that turns a surface's inputs and the lighting into the colour of each pixel.
  - Why: The shader computes pixel colour from its inputs.
- **B. FALSE.** The roughness and metallic images are colour pictures and are treated like the base colour.
  - Why: They are data, not colour.
- **C. FALSE.** A material and a texture are the same thing.
  - Why: A texture is one input; a material is the whole set of measurements.
- **D. TRUE.** A material of the usual modern kind describes a surface by measurements such as base colour, how metallic it is and how rough it is, not by one picture.
  - Why: A PBR material is a set of measurements, not a picture.
- **E. TRUE.** Of the textures that describe a surface, the base-colour one holds colour, while the roughness and metallic ones hold numbers stored in an image file.
  - Why: The base colour is a colour; the other measurements are data stored in image files.

*Covered in:* Ch 7, 'A PBR material is a set of measurements, not a picture' and 'Colour versus data'.

## 12. Chapter 7: Textures (colour, data and normal maps)

**A texture artist adds a normal map to a stone wall to give it fine surface detail. Check each statement that is true about normal maps.**  *(5 points)*

**True: A, C, D** (3 of 5)

- **A. TRUE.** An image that merely looks like a normal map is not guaranteed to be a valid one, so one made by an AI image tool needs checking.
  - Why: A generated 'normal map' is a picture that looks like one; nothing guarantees its directions are valid.
- **B. FALSE.** A normal map records how much of the surrounding light reaches each crevice of the wall.
  - Why: That is ambient occlusion, a separate measurement.
- **C. TRUE.** A normal map holds data rather than colour, so reading it as an ordinary colour image would make the lighting come out wrong.
  - Why: Converting a normal map as colour tilts a flat surface and lights it wrongly (darker and lopsided).
- **D. TRUE.** A normal map records, for each point, which way the surface faces, at a finer detail than the wall's mesh has.
  - Why: The normal measurement is which way the surface faces at a detail smaller than the mesh.
- **E. FALSE.** A normal map records the colour of the stone at each point.
  - Why: The colour of the surface is the base colour; a normal map holds directions.

*Covered in:* Ch 7, 'A PBR material is a set of measurements, not a picture' (Normal: which way the surface faces at a detail smaller than the mesh; Ambient occlusion: how much of the surrounding light reaches a crevice; 'Only the base colour is a colour. The rest are data'); 'Colour versus data: why the decode matters' (decoding a flat normal-map texel as colour tilts the surface and lights it wrongly); 'Attribution is part of the material' ('A generated normal map is a picture that looks like a normal map, and nothing guarantees its vectors are unit length or its blue channel is above 0.5').

## 13. Chapter 8: Checking a shader

**A student tests a shader's colour fade after a player failure by running the game with no window (a headless run) at several fixed frame rates. Check each statement that is true.**  *(5 points)*

**True: A, B, C, D** (4 of 5)

- **A. TRUE.** A run with no window can still report a coding mistake in a shader, such as a value of the wrong type.
  - Why: The shader source is still compiled in a headless run, so such errors show up as shader error lines.
- **B. TRUE.** A run with no window can check that gameplay code gives the shader the right values at the right moments.
  - Why: Sampling the values the game feeds the shader every frame is something a headless run can do.
- **C. TRUE.** A fade that counts frames instead of game time can pass at the frame rate usually tested and still be wrong at other frame rates.
  - Why: The seeded frame-counting bug was invisible at the usual rate and failed at the other rates.
- **D. TRUE.** Fixing the frame rate makes a run repeatable, because every frame then covers the same amount of game time.
  - Why: Pinning the frame rate removes the machine-speed variation, so each frame is a fixed slice of game time.
- **E. FALSE.** A run with no window can show which colour the shader actually drew for each pixel, because the shader still runs on the graphics processor there.
  - Why: A headless run uses a dummy renderer; what the graphics processor actually drew needs a real screen and a person.

*Covered in:* Ch 8, 'The ladder of evidence' (parse and driver rungs are headless-checkable, observation is not), 'Controlled inputs in a headless Godot run' (pin the frame rate so each frame is an exact slice of game time and the run is repeatable), and the seeded change whose frame-counted fade passed at the usual rate and failed at others. Ch 9 also states that the headless dummy renderer still compiles shader source and does no drawing.

## 14. Chapter 9: Particle effects

**A game needs two effects: smoke that keeps rising from a chimney, and a burst of sparks that plays once when a barrel breaks. Check each statement that is true.**  *(5 points)*

**True: C, D, E** (3 of 5)

- **A. FALSE.** In a continuous effect the particles are not removed, so the number alive keeps growing the longer the effect runs.
  - Why: Each particle dies at the end of its lifetime, so the number alive stays capped.
- **B. FALSE.** Lifetime is the number of particles born in one emission cycle.
  - Why: Lifetime is how long each particle lives (and the length of a cycle); the number born per cycle is a different setting.
- **C. TRUE.** Smoke that keeps rising suits a continuous effect, in which new particles keep being born at a steady pace.
  - Why: A looping effect with births spread evenly over the cycle is the continuous kind; the chapter uses smoke as its example.
- **D. TRUE.** A one-shot effect plays a single emission cycle and then stops.
  - Why: One-shot means only one emission cycle occurs.
- **E. TRUE.** In a burst, all of the particles are born together at the start instead of being spread out over time.
  - Why: A burst is the case where every particle is emitted at the start of the cycle.

*Covered in:* Ch 9, 'The timing model: one emission cycle' (lifetime is how long each particle lives and the length of one cycle; the amount is the number emitted per cycle; a spread of zero births evenly across the cycle and full explosiveness emits all at the start, which is a burst; one-shot means only one cycle; at most the set number are alive) and the mention of smoke already rising when a level loads.

## 15. Chapter 10: Animation foundations (sprite sheets, rigs, keyframes, inverse kinematics)

**A 2D team is deciding how to animate a character. Check each statement that is true.**  *(5 points)*

**True: A, D, E** (3 of 5)

- **A. TRUE.** A rig is a skeleton of connected bones, and moving the bones moves the pieces of the character attached to them.
  - Why: A skeleton is a hierarchy of bones; parts skinned to them follow.
- **B. FALSE.** With a rig, every pose is stored as a separate finished drawing.
  - Why: A rig stores bone poses, not a drawing per pose.
- **C. FALSE.** Sprite-sheet animation needs a skeleton.
  - Why: A sheet just swaps images; no bones are involved.
- **D. TRUE.** A rig can pose the same artwork many ways without a new drawing for each pose, while a sprite sheet shows exactly the drawing made for each frame.
  - Why: This is the practical difference between the two methods.
- **E. TRUE.** A sprite sheet is one image holding the frames of an animation in a grid, and the animation shows one frame after another.
  - Why: A sheet is cut into a grid of frames that play in turn.

*Covered in:* Ch 10, 'Frames, sprite sheets and cycles' and 'Skeletons and IK'.

## 16. Chapter 11: State machines and blending

**A character can be idle, running, jumping or falling, and its animation is organised as a state machine. Check each statement that is true.**  *(5 points)*

**True: A, C, D** (3 of 5)

- **A. TRUE.** A state machine is in one state at a time and moves between states along defined transitions.
  - Why: States connected in a graph; one is current.
- **B. FALSE.** A state machine lets the character be in running and jumping at the same moment.
  - Why: One state is current at a time.
- **C. TRUE.** A transition is the connection that says when the character may leave one state for another.
  - Why: Each connection in the graph is a transition.
- **D. TRUE.** A transition can be set to wait until the current animation has finished before the next state begins.
  - Why: A transition's switch setting can wait for the current state's playback to end.
- **E. FALSE.** A state machine is the way to mix two clips together by a continuous number such as speed.
  - Why: That is a blend space, which takes a continuous input.

*Covered in:* Ch 11, 'The state machine, as machinery' and 'BlendSpace: continuous input, continuous pose'.

## 17. Chapter 12: Audio and triggers

**A developer is learning when to use a plain sound player and when to use one that gives a sound a place in the world. Check each statement that is true.**  *(5 points)*

**True: C, D** (2 of 5)

- **A. FALSE.** Positional sound is only possible in 3D games, because distance needs three dimensions.
  - Why: There is a positional player for 2D too, for sounds with a place on a 2D screen.
- **B. FALSE.** Any sound player attached to a moving enemy gets quieter with distance, because it belongs to the enemy.
  - Why: A plain player has no position at all; only the positional kinds attenuate with distance.
- **C. TRUE.** A positional player makes a sound quieter as the listener gets farther from the place the sound comes from.
  - Why: Positional players attenuate with distance to the listener.
- **D. TRUE.** Background music and interface clicks suit a plain player, because their loudness should never depend on where the camera is.
  - Why: The plain player is for music and interface sounds and does not use position.
- **E. FALSE.** A 3D positional sound can only be heard if the developer adds a listener object to the scene by hand.
  - Why: By default the current camera acts as the listener.

*Covered in:* Ch 12, 'Three player nodes, one question: where is the listener?': the plain player is for music and interface sounds and 'does not' use position; the 2D player is 'attenuated with distance to the listener'; the 3D player is attenuated and panned relative to the current camera or a listener node; 'Choose by asking where the listener is'.

## 18. Chapter 13: Profiling and optimization

**A team wants its Godot game to run at 60 frames per second. Check each statement that is true.**  *(5 points)*

**True: B, C, D** (3 of 5)

- **A. FALSE.** The average frame time alone is enough to tell that the game is smooth.
  - Why: A good average can hide stutter.
- **B. TRUE.** Frames per second counts how many frames are drawn each second, and frame time is how long each frame takes.
  - Why: Two views of the same thing; frame time is the unit.
- **C. TRUE.** An optimization is justified when it is faster by enough to matter against the frame budget on the hardware the game targets.
  - Why: The chapter's own test.
- **D. TRUE.** A frame budget is the longest time one frame may take and still meet the target frame rate.
  - Why: Budget per frame is 1000 divided by the target rate.
- **E. FALSE.** "It is faster" is a good enough reason by itself to make an optimization change.
  - Why: The chapter says 'faster' is not a justification.

*Covered in:* Ch 13, 'Frame time is the unit; frames per second is the headline' and the chapter opening.

## 19. Chapter 14: How game characters decide (state machines, behavior trees)

**A guard that patrols, chases and searches has its brain built as a finite state machine. Check each statement that is true.**  *(5 points)*

**True: C, D, E** (3 of 5)

- **A. FALSE.** States cannot share behavior, so a rule many states need, such as jumping, must be copied into every one of them.
  - Why: Hierarchical states share behavior through a parent, so the rule is written once.
- **B. FALSE.** The order of the states in a list decides which behavior wins, and the list is re-checked from the top on every update.
  - Why: That describes a behavior tree's priority ordering, not a state machine.
- **C. TRUE.** In a state machine each state knows its own exits: the rules for leaving a behavior are stored with that behavior.
  - Why: A state machine keeps its transition logic on the states and their connections.
- **D. TRUE.** Using a larger distance for giving up on the player than for noticing the player stops the guard flipping between chasing and searching at the boundary.
  - Why: This is hysteresis: two different distances keep the guard from flickering at the edge.
- **E. TRUE.** A stack of states lets a character return to what it was doing before an interruption, such as going back to running after a jump.
  - Why: A pushdown stack puts the interrupting state on top and pops back to the earlier one.

*Covered in:* Ch 14, 'Finite state machines, as this project builds them' (hierarchical states share behavior through a parent so a transition is written once; the pushdown stack pops back after a jump; 'where the transition logic lives': an FSM stores it on the edges, each state knows its exits) and 'Build It, Task 2' (a larger lose distance than sight distance is hysteresis, so the guard does not flicker at the boundary). The list-order statement is the behavior tree's selector priority ('Behavior trees: priority, re-evaluated or remembered').

## 20. Chapter 14: Generating levels (seed, noise, checking)

**A level generator sometimes produces platformer levels with a gap too wide to jump, and the team wants every level it ships to be playable. Check each statement that is true.**  *(5 points)*

**True: A, E** (2 of 5)

- **A. TRUE.** Generate-and-test builds a level, checks it, and throws it away and builds another if the check fails.
  - Why: Reject and re-roll is the generate-and-test policy for failures.
- **B. FALSE.** A playability check needs only the level's own data, since what the player can do does not matter.
  - Why: The check models the player, such as how high and far the jump goes, so it needs those limits.
- **C. FALSE.** A playability check has to be done by a person playing each level, because software cannot model a player's jump.
  - Why: A validator is a software model of the game's rules, built from the player's measured jump.
- **D. FALSE.** Fixing the seed removes the need for a playability check, because the same seed always gives the same level.
  - Why: A seed makes a level repeatable, not playable; a repeated impossible level is still impossible.
- **E. TRUE.** A generator that can produce an impossible level is only half a system; the other half is a check that each level meets a playability rule.
  - Why: The chapter states this directly: the generator needs a validator.

*Covered in:* Ch 14, 'Procedural content generation: seeds, noise, and proof': 'A generator that can emit an impossible level is only half a system. The other half is a check that each output meets a playability rule', with a policy for failures: reject and re-roll (generate-and-test) or build the level so it cannot fail (constructive); 'The validator is a model of the game's rules'. Lab B: the validator decides crossability from a jump model.

**Total true statements: 52 of 100.**
