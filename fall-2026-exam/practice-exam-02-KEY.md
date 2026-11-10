# Practice exam 02: ANSWER KEY (read it only AFTER doing the exam cold)

Each statement is scored on its own, 1 point. Under every statement is the reason it is true or false, and each question names the course chapter passage it follows. The answers are **awaiting a game developer's check**; if a key looks wrong to you, say so.

## 1. Chapter 0: Checking an agent's report against evidence

**A student is judging whether an agent's change to a game altered anything it should not have, using the kinds of evidence a project can provide.**  *(5 points)*

**True: A, E** (2 of 5)

- **A. TRUE.** Writing down the exact results of a passing test run before a change lets the student see afterwards whether the change altered behaviour under that same run.
  - Why: Identical before-and-after numbers were the strongest evidence that the score feature changed nothing under the route.
- **B. FALSE.** An exported build that runs on the target machine shows that players will want to play the game.
  - Why: Running a build shows the game survives packaging, not that anyone wants to play it.
- **C. FALSE.** A scripted route that passes is the same kind of evidence as a person playing, because it presses the game's real controls.
  - Why: A passing route is evidence about state under one sequence of inputs; it is not a person playing.
- **D. FALSE.** An agent that ran its own new test correctly can be assumed to have run the project's older tests correctly too.
  - Why: Both agents ran the new test fine but ran the old regression test in a way that made it unreliable.
- **E. TRUE.** A test that counts frames while the game moves by seconds can give different results on different runs, so its result is weak evidence until the time step is fixed.
  - Why: Without a pinned time step the result depends on machine speed and load; rung 4 of the ladder requires the pinned step.

*Covered in:* Ch 0, 'The evidence ladder' (rungs 4, 5 and 6); 'My verification' (identical regression numbers before and after are the strongest evidence here, and why a baseline written down in Step 3 is worth having); 'The time trap: frames are not seconds' (a test that counts frames while the game moves by delta time is machine-dependent unless the time step is pinned); 'Where each agent was right and where it was wrong' (both climbed to rung 4 for the new test, then misread the old test because they ran it in a way that made it unreliable).

## 2. Chapter 0: Working safely with an agent (instruction files, permissions, headless runs)

**A student runs a game's automated test from the command line in headless mode, and the run finishes with a success result.**  *(5 points)*

**True: B, C** (2 of 5)

- **A. FALSE.** A headless test that counts sound cues shows that the sound is audible and sounds right.
  - Why: Headless uses a dummy audio driver; a cue counter is a state change, not a sound.
- **B. TRUE.** A headless run has no window and no sound, yet the game's scripts, physics, signals and timers still run.
  - Why: That is the chapter's definition of headless mode: no picture and no sound, everything else runs.
- **C. TRUE.** Because a headless run produces no picture, a test can read values such as positions or a label's text, but it cannot judge whether the label is readable.
  - Why: A headless test observes state, never pixels; readability is a human check.
- **D. FALSE.** A headless run that finishes with a success result printed no errors while it ran.
  - Why: The engine can print script errors while the run still exits with success, so the error output must be read too.
- **E. FALSE.** If a headless test script hits an error before it finishes, the run ends by itself with a failing result, so a time limit is unnecessary.
  - Why: The run can hang forever with no window to close; a time limit turns the hang into a visible failure.

*Covered in:* Ch 0, 'Godot is also a command-line program' (headless means no picture and no sound; scene tree, scripts, physics, signals and timers still run; a headless test observes state, never pixels) and 'The headless test: a script that plays the game' (wrap runs in a time limit because a script that errors before quitting hangs; read the error output even when the exit code is 0). Ch 2, 'Verify' (headless uses the Dummy audio driver; a cue counter is a state change, not a sound).

## 3. Chapter 1: Walker, Godot projects and how a game updates

**A beginner is learning when Godot runs the code that updates a game while it plays.**  *(5 points)*

**True: A, C, E** (3 of 5)

- **A. TRUE.** One kind of update runs once for every drawn frame, so how often it runs depends on how fast the machine can draw.
  - Why: The per-frame update follows the machine's rendering speed.
- **B. FALSE.** A game that moves objects by a distance per second of elapsed time makes them travel farther each second on a machine that draws more frames.
  - Why: Scaling by elapsed time makes the distance per second the same at 30 and at 144 frames per second.
- **C. TRUE.** Another kind of update, used for physics, runs at a fixed rate, so each step covers the same slice of game time.
  - Why: The physics update runs at a fixed rate set in the project settings.
- **D. FALSE.** A test that counts fixed-rate physics steps measures more game time on a fast machine than on a slow one.
  - Why: Each physics step is the same slice of game time, so the count means the same time everywhere.
- **E. TRUE.** A game that moves an object by a fixed distance on every drawn frame makes it move faster on a machine that draws more frames per second.
  - Why: The per-frame update runs once per drawn frame, as often as the machine can manage.

*Covered in:* Ch 1, 'Scripts and the two clocks' (the per-frame update runs once per rendered frame; the physics update runs at a fixed rate, set in Project Settings; nodes with a lower priority run first, so the player moves before the session checks hazards) and 'Running Godot without a window' (the tests count physics ticks and gave identical numbers with and without the fixed-frame-rate flag). Ch 0, 'The time trap' (the ball moves the same distance per second at 30 and at 144 frames per second).

## 4. Chapter 2: Game art and sound (pixel art, asset requests, loops)

**A student adds looping music and short sound effects to a 2D game.**  *(5 points)*

**True: C, D** (2 of 5)

- **A. FALSE.** Short sound effects are usually imported with looping turned on, so that they can be repeated.
  - Why: Effects are imported without looping; music is imported with looping.
- **B. FALSE.** A sound played without any position still gets quieter and pans as the listener moves away from the place it came from.
  - Why: Only the positional players pan and fade with position; the non-positional one does not.
- **C. TRUE.** To play a jump sound once per jump, start it when the player enters the jumping state, not on every frame the player is in that state.
  - Why: Playing on every frame the state is true cuts off the oldest sound and causes stutter; trigger on the transition.
- **D. TRUE.** A one-shot effect plays from start to finish once each time it is triggered, while a loop returns to its loop point and keeps playing until it is stopped.
  - Why: Effects are imported with looping disabled; the music track is set to loop.
- **E. FALSE.** The engine automatically finds a smooth loop point in any music file, so it does not matter where a generated track is cut.
  - Why: The track must be cut at a bar boundary before import; the engine cannot end a loop early for some formats.

*Covered in:* Ch 2, idea 7 'Sound: import, loop, trigger' (WAV loop modes and loop points; effects imported with looping disabled and the music with a forward loop; cut a generated music track at a bar boundary before import because the engine cannot end the loop early for Ogg or MP3; the non-positional player versus the positional ones that pan and attenuate by position; play on the transition into a state, not on every frame the state is true) and idea 8 'Procedural audio is not generative audio'.

## 5. Chapter 3: 3D assets from Blender to Godot

**A 3D artist builds a prop in Blender and brings it into a Godot game. Check each statement that is true about carrying it across.**  *(5 points)*

**True: A, B, D** (3 of 5)

- **A. TRUE.** Blender, glTF and Godot all count one unit of distance as one metre, so a prop built at Blender's standard unit setting arrives at its intended size.
  - Why: All three use metres, so no conversion is needed while the Blender scene keeps its standard unit setting.
- **B. TRUE.** glTF is an interchange format for moving a 3D model between tools, and Godot recommends it for importing models.
  - Why: Godot's documentation lists glTF 2.0 as the recommended import format.
- **C. FALSE.** Godot's physics works the same at any scale, so the size of an imported prop changes how it looks but not how it plays.
  - Why: Godot's physics is tuned for metres; a prop at the wrong scale can become a wall that cannot be climbed or a step that is not noticed.
- **D. TRUE.** Blender treats Z as up while glTF and Godot treat Y as up, so the exporter turns the model's height onto the other axis.
  - Why: Blender is Z-up, glTF and Godot are Y-up, and the exporter converts.
- **E. FALSE.** A prop that arrives in Godot lying on its side was exported at the wrong size.
  - Why: Lying on its side is an up-direction (axis) problem; size is a separate matter.

*Covered in:* Ch 3, 'Units: a metre is a metre, until it is not', 'Axes: Blender is Z-up; glTF and Godot are Y-up' and 'glTF is the interchange format': all three tools use metres; Blender is Z-up while glTF and Godot are Y-up and the exporter converts; glTF 2.0 is Godot's recommended 3D format; a prop at the wrong scale is 'a wall the robot cannot climb or a step it does not notice'.

## 6. Chapter 3: Driving Blender with an agent (MCP and scripts)

**A coding agent reports that it built a prop in Blender and exported it for a Godot game. Check each statement that is true about what to verify afterwards.**  *(5 points)*

**True: C** (1 of 5)

- **A. FALSE.** Once the exported file exists, the script that made it can be thrown away, because the file records how it was built.
  - Why: The source of truth for how the asset was made is the script; the exported file is a build product.
- **B. FALSE.** If the numbers the agent reports match the plan, the prop is known to look right under the game's lights.
  - Why: Numbers do not show how the prop looks lit, or whether it reads as the intended object; those are human checks.
- **C. TRUE.** A script that fails partway can still let Blender finish as if it had succeeded unless told otherwise, so a finished run is not evidence of success.
  - Why: Without the error-exit option Blender exits as success even when the script raises an exception.
- **D. FALSE.** If the agent's own test passes, the collision shape must be correct, since the agent wrote the test to check it.
  - Why: In the worked example a check the agents did not write found part of the pennant inside the collision shape although the agent's tests passed.
- **E. FALSE.** Test output pasted into the agent's report is as good as evidence as running the checks yourself.
  - Why: The chapter says to run the checks yourself and not accept the agent's pasted output as evidence.

*Covered in:* Ch 3, 'Two ways for an agent to drive Blender' (add the error-exit option; without it Blender exits as success when the script raises), 'Ship It' (the .glb is a build product of the script), 'What we actually ran' (a passing agent test still missed the pennant inside the collider) and 'Verify' ('What a pass proves ... What it does not prove: that the post looks right lit ...').

## 7. Chapter 4: Nodes, scenes, signals and groups

**A student asks how the tree of nodes shown in the editor relates to what actually runs when a Godot game plays. Check each statement that is true.**  *(5 points)*

**True: A, B, D** (3 of 5)

- **A. TRUE.** A property changed on one instance of a scene overrides the value from the source scene for that instance alone.
  - Why: Changing a property on an instance overrides the value from the packed scene.
- **B. TRUE.** Code that creates scene instances during play also has to decide who frees them, or unused objects can pile up.
  - Why: Ownership (who creates and who frees an instance) is the design question; getting it wrong leaks objects or frees something still in use.
- **C. FALSE.** Every instance of a scene has to be placed in the editor before play, because new instances cannot be created while the game runs.
  - Why: Scenes can be instanced at run time; the mobs in the example game are created while it plays.
- **D. TRUE.** The running scene tree can contain nodes that scripts add during play, so it can be larger than the tree shown for a saved scene.
  - Why: The saved scene and the running tree are not the same; in one example the saved scene held one node while scripts built the level at run time.
- **E. FALSE.** A signal works by one node reaching into another node and changing its data directly.
  - Why: With signals no object reaches into another; one emits, and the scene says who listens.

*Covered in:* Ch 4, 'The scene tree: what is actually running' (the saved scene and the running tree are not the same thing; scripts add nodes at run time), 'Nodes and scenes: composition you can save' (instancing, edit-time and run-time instances, instance overrides, ownership: who creates it, who frees it) and 'Signals: who tells whom' (react without referencing one another; 'No object reaches into another').

## 8. Chapter 4: Collision (colliders, triggers, layers and masks)

**A 2D platformer has a stone floor, a crate that should tumble when pushed, and a hero steered by the player's own code. Check each statement that is true.**  *(5 points)*

**True: B, D, E** (3 of 5)

- **A. FALSE.** If the hero's artwork is swapped for a wider picture, its collision shape resizes itself to match the new art.
  - Why: The collision shape and the sprite are separate; change the art and nothing moves the collision shape.
- **B. TRUE.** Turning on the display of collision shapes while the game runs lets you compare them with what is drawn.
  - Why: The debug option makes collision shapes visible in the running project, so you can see where they sit against the art.
- **C. FALSE.** A body that the physics engine moves, like the crate, is steered best by having your code overwrite its position every frame.
  - Why: Changing such a body's position or velocity very often may lead to unpredictable behaviour; you give it forces or a starting velocity and the engine moves it.
- **D. TRUE.** A solid fixed body, like the floor, is never moved by the physics engine, but other bodies collide with it.
  - Why: A static body is not moved by the physics engine and others collide with it.
- **E. TRUE.** A body you move yourself, like the hero, gets collision detection but not simulated physics, so your code decides how it moves.
  - Why: A character body has collision detection but no physics; you move it yourself.

*Covered in:* Ch 4, 'Four collision objects, and one way around them' (fixed body: 'not moved by the physics engine'; physics body: you set forces or velocity and the engine moves it, and rewriting its transform very often 'may lead to unpredictable behaviors'; character body: 'collision detection, but no physics', you move it), 'The art is not the collider' ('Change the art and nothing moves the capsule') and 'Use It' (showing collision shapes in the running project).

## 9. Chapter 5: Game design documents and requirements

**A coding agent reads an existing Godot project and writes a design document for the game that is already there, marking each claim with how it is known. Check each statement that is true.**  *(5 points)*

**True: B, C** (2 of 5)

- **A. FALSE.** If the project contains a sprite for a feature, the document can list that feature as a working mechanic.
  - Why: Sprites do not prove a mechanic; a drawing is not behaviour.
- **B. TRUE.** A claim marked 'observed' is meant to be something the code actually does, and one marked 'missing' is something the code cannot tell you.
  - Why: These are the meanings of the evidence tags: observed means the code does it; missing means the code cannot say.
- **C. TRUE.** To check a claim marked 'observed', the student opens the code it points to and reads it.
  - Why: An 'observed' claim is checked by reading the code it cites.
- **D. FALSE.** Numbers the agent finds in the code, such as a jump speed, show the values the team has approved for the final design.
  - Why: Numbers found in code are observed tuning, not approved design.
- **E. FALSE.** Once every claim in the recovered document carries a tag, the design stages count as signed off.
  - Why: A recovered document is not an approval; a person signs each stage, the agent does not.

*Covered in:* Ch 5, 'Provenance tags': [OBSERVED] = the code does this, [INFERRED] = the code strongly implies it, [MISSING] = the code cannot tell you; 'Sprites do not prove a mechanic... a TODO is not a design decision'; numbers found in code are 'observed tuning, not approved design'; 'A tag is a claim about evidence. It is not evidence. The only way to know an [OBSERVED] tag is right is to open the cited line.' Also 'Gates, and who signs them' (a human signs; the agent never signs a gate) and the audit table of nine wrong claims.

## 10. Chapter 6: Shaders

**A student is comparing the different jobs a shader can do in a Godot game. Check each statement that is true.**  *(5 points)*

**True: A, B** (2 of 5)

- **A. TRUE.** A shader can include an optional part that runs for every pixel and every light, which is where it controls how lighting affects a surface.
  - Why: There is an optional per-pixel, per-light part that handles lighting, and it replaces the built-in lighting when present.
- **B. TRUE.** There are different kinds of shader for different jobs, for example one for 3D models, one for 2D sprites and interface, and one for the sky.
  - Why: A shader declares what it draws; the kinds include 3D, 2D, particles, sky and fog.
- **C. FALSE.** Changing where a shape's corners land in a shader does not move the drawing, which can only be moved by the game's own code.
  - Why: The corner part sets positions, so moving a corner moves the drawing.
- **D. FALSE.** The graphics processor runs a shader's pixel part for one pixel at a time, in order, finishing each before starting the next.
  - Why: A shader is run over many pixels in parallel, many times at once.
- **E. FALSE.** The part of a shader that colours pixels runs once for the whole shape, so every pixel of the shape gets the same result.
  - Why: The pixel part runs for every pixel the shape covers, and each run can give a different colour.

*Covered in:* Ch 6, 'Shader types and processor functions' (six shader types, e.g. one for 3D meshes, one for 2D sprites, shapes and UI, one for the sky; vertex part 'runs over all the vertices in the mesh and sets their positions', fragment part 'runs for every pixel covered by the mesh', light part 'runs for every pixel and for every light') and 'A shader is a small program the GPU runs many times at once' (once per vertex, once per pixel covered, optionally once per pixel per light, 'in parallel'); 'Inside a canvas_item shader' (move the vertex position and the drawing moves).

## 11. Chapter 7: Materials (material, shader, texture)

**Ten identical crates in a 3D level use one shared material. A designer wants a single crate to glow red when it is hit. Check each statement that is true about materials.**  *(5 points)*

**True: A, B** (2 of 5)

- **A. TRUE.** A model made of several parts can have a different material on each part, so changing one part's material leaves the others as they were.
  - Why: A ship model has separate materials for hull, rigging and sails; changing the hull's left the others untouched.
- **B. TRUE.** The designer can give the hit crate its own copy of the material, or use a setting kept separately for each object, so the other nine are not affected.
  - Why: Either a duplicated material or a per-object setting gives one object its own value.
- **C. FALSE.** A setting such as the glow amount is stored on the shader program itself, not on any material.
  - Why: The values are set on a material; the shader is only the program.
- **D. FALSE.** The material alone decides the colour a player sees, so a material that looks right in one scene will look right in every other.
  - Why: Light and camera turn the measurements into colour, so a material is judged under stated lighting.
- **E. FALSE.** If the game changes a setting on the shared material, the change affects just the crate that was hit.
  - Why: A change on a shared material affects every object that shares it.

*Covered in:* Ch 6, 'Uniforms and hints: the contract with GDScript': 'Setting a value happens on a material, not on the shader... The ShaderMaterial reference warns that the change affects every node sharing that material, and points to per-instance uniforms or a duplicated material when you need per-node values.' Ch 7, 'A PBR material is a set of measurements, not a picture' (a material that looks right under one light can look wrong under another) and 'Walker example / Hands-on' (the ship's hull, rigging and sails each have their own material; changing the hull's left rigging and sails as they were).

## 12. Chapter 7: Textures (colour, data and normal maps)

**A student copies the textures for a 3D model into a Godot project and notices that each image has import settings. Check each statement that is true about why those settings matter.**  *(5 points)*

**True: B, C, D, E** (4 of 5)

- **A. FALSE.** When an AI agent connects a texture to a material by editing the project's text files, the texture's import settings are adjusted automatically to suit its use.
  - Why: The automatic detection runs only when the editor draws the texture in a 3D material; editing text leaves the settings as they were.
- **B. TRUE.** A normal map has its own import setting, so it can be treated as a normal map instead of as an ordinary picture.
  - Why: The importer has a setting for whether a texture is a normal map.
- **C. TRUE.** Without mipmaps, which are smaller pre-made versions of a texture, distant surfaces on a 3D model shimmer.
  - Why: Mipmaps are recommended in 3D; without them distant surfaces shimmer.
- **D. TRUE.** Textures for a 3D model left in the lossless mode meant for 2D art use more video memory than a compressed mode meant for 3D would.
  - Why: The lossless mode is the 2D default; the compressed mode is the 3D default and reduces video memory.
- **E. TRUE.** Import settings decide how an image is prepared before it reaches the graphics processor, for example how it is compressed.
  - Why: The import file decides what reaches the graphics processor, including compression.

*Covered in:* Ch 7, 'Texture import: the half an agent forgets' (the import file decides what reaches the GPU; compression modes: lossless is the default for 2D, VRAM-compressed the default for 3D and reduces video memory; 'It's recommended to enable mipmaps in 3D. Without them, distant surfaces shimmer'; a normal-map import option; 'The detection trap': Detect 3D and Normal Map Detect run only when the editor's renderer draws the texture in a 3D material, so an agent that edits text leaves import settings unchanged) and the executive summary ('how Godot imports it (compression, mipmaps, whether it is a normal map)'); 'What we actually ran' lists all nine textures imported lossless as a finding.

## 13. Chapter 8: Checking a shader

**A team wants to trust its checks of a shader's colour flash. It writes an automated timing check, a small model that predicts the colours, and a test scene with fixed inputs. Check each statement that is true.**  *(5 points)*

**True: A, B, D** (3 of 5)

- **A. TRUE.** A test scene with fixed inputs is built to be looked at: a person screenshots it and compares sampled pixel colours with the model's predictions.
  - Why: This is the bench step: fixed inputs, a screenshot, and a comparison with the predicted colours.
- **B. TRUE.** Before a new check is trusted, it should be tried on a version known to be wrong and on a version known to be right.
  - Why: Testing the test: it must fail on known-bad code and pass on known-good code, or the check itself may be wrong.
- **C. FALSE.** A check that compares the fade with the current code's own internal countdown still passes after the fade is correctly rewritten to use a different timer.
  - Why: A check tied to the implementation fails equally on a correct rewrite; a check tied to the spec survives it.
- **D. TRUE.** A check that follows the written specification may still need a small tolerance, because the engine's clocks make even correct code differ slightly from the ideal.
  - Why: The first spec check rejected correct code until its tolerance was reasoned out from the engine's frame and physics timing.
- **E. FALSE.** A test that confirms the scene is set up with the intended inputs also confirms that the shader draws the expected colours.
  - Why: A headless setup test passed even on the broken shader; it checks the scene's build, not what is drawn.

*Covered in:* Ch 8, 'Test the spec, not the implementation, and then test the test' (an implementation-coupled check fails on a correct rewrite; a new check must fail on a known-bad and pass on a known-good version), 'The CPU model and the bench' (a bench holds fixed inputs, is screenshotted, and its pixels are compared with the model; a headless test can only check the bench is built right), and 'What we actually ran' (the oracle rejected correct code at the high frame rate until the tolerance was reasoned out).

## 14. Chapter 9: Particle effects

**A mobile game's smoke effect makes the frame rate drop, and a programmer is looking for the cause. Check each statement that is true.**  *(5 points)*

**True: A, E** (2 of 5)

- **A. TRUE.** Large, see-through particles that overlap cost extra to draw, because each covers many pixels and the same pixels get filled again and again.
  - Why: Large, transparent, overlapping particles cost fill rate; overdraw from big see-through pictures is a main drawing cost.
- **B. FALSE.** Particles simulated on the graphics processor cost nothing, so there is no need to limit how many an effect has.
  - Why: Graphics-processor simulation is one of the places particle cost lands, and the particle count is the direct multiplier.
- **C. FALSE.** A test run with no window can measure what a graphics-processor particle effect costs the graphics hardware.
  - Why: A headless run uses a dummy renderer that does no graphics work, so it reports such particles as nearly free.
- **D. FALSE.** An effect that costs little on a powerful desktop computer will cost just as little on a phone.
  - Why: Fill rate is very expensive on mobile, so a cheap-looking effect on a desktop can be costly on a phone.
- **E. TRUE.** Particles simulated on the main processor take more main-processor time each frame as their number grows.
  - Why: Main-processor particles are updated one by one each frame; the measured cost rose steadily with the count.

*Covered in:* Ch 9, 'Where particle cost lands' (main-processor simulation, graphics-processor simulation, and drawing; large, transparent, overlapping quads cost fill rate, which is very expensive on mobile; a headless measurement reports GPU particles as nearly free, a property of the instrument; the particle count is the direct multiplier; overdraw is a cost lever) and the measured main-processor cost rising with particle count.

## 15. Chapter 10: Animation foundations (sprite sheets, rigs, keyframes, inverse kinematics)

**A character has a skeleton of bones with its visible surface attached to them. A designer wants the character's hand to reach toward a target while an animation plays. Check each statement that is true.**  *(5 points)*

**True: A, C, D** (3 of 5)

- **A. TRUE.** Skinning attaches the character's visible surface to the bones, with weights saying how strongly each bone moves each part of the surface.
  - Why: A surface is skinned to the bones with painted weights, from full influence to none.
- **B. FALSE.** A skeleton's rest pose is the pose at the end of the most recent animation that played on it.
  - Why: The rest pose is the skeleton's default pose, which you can return to at any time.
- **C. TRUE.** Inverse kinematics pulls the end of a chain of bones, such as a hand at the end of an arm, toward a target position.
  - Why: The solvers in the example pull the head and arms toward a moving target.
- **D. TRUE.** Inverse kinematics is applied on top of the animation, adjusting the pose that the animation has already produced.
  - Why: Procedural modifiers such as inverse kinematics always run after the animation has played.
- **E. FALSE.** Inverse kinematics blends two animation clips together according to a continuous value such as the character's speed.
  - Why: Blending clips by a value is a blend; inverse kinematics pulls bones toward a target.

*Covered in:* Ch 10, 'Skeletons and IK' (a hierarchy of bones; a surface skinned to the bones with painted weights, where full weight means full influence; the rest pose is the default pose; procedural changes layered on top of animation always run after the animation's playback) and the walker-3d-ik example, where mouse-moved targets make the solvers pull the head and arms toward them.

## 16. Chapter 11: State machines and blending

**A designer adds a lunge attack in which the character's body moves forward as part of the animation, and wants smooth changes between the character's states. Check each statement that is true.**  *(5 points)*

**True: A, D, E** (3 of 5)

- **A. TRUE.** A transition between two states can include a short cross-fade, so the pose changes smoothly instead of cutting at once.
  - Why: Each transition can carry a cross-fade length; without one the change is a cut.
- **B. FALSE.** Root motion is the setting that decides how long a transition between two states takes.
  - Why: The length of a transition's cross-fade is a transition setting; root motion is about where movement comes from.
- **C. FALSE.** A blend of clips driven by speed is the right tool for a jump that must play its takeoff once started, even if the player lets go of the button.
  - Why: Blends suit continuous input; a character that must commit to a jump needs states.
- **D. TRUE.** With root motion, the forward movement of the body comes from the animation itself, as in a lunge that carries the character ahead.
  - Why: Root motion uses clips that move the character's root as part of the animation, such as a lunge or a vault.
- **E. TRUE.** Using root motion hands control of the character's movement to the animation, so tests of that movement become tests of animation data.
  - Why: Root motion hands movement authority to the animation, which changes what a movement test is really testing.

*Covered in:* Ch 11, 'Root motion' (some clips move the root as part of the animation, such as a lunge or a vault; it hands movement authority to the animation, so movement tests become tests of animation data), 'The state machine, as machinery' (a transition has a cross-fade length) and 'BlendSpace: continuous input, continuous pose' (blends suit continuous input and are the wrong tool when the character must commit, such as a jump that has started).

## 17. Chapter 12: Audio and triggers

**A rhythm game plays a short click when the player hits a note well, over a looping background song. Check each statement that is true.**  *(5 points)*

**True: B** (1 of 5)

- **A. FALSE.** A player that can play only one sound at a time layers each new sound on top of the old one, so every rapid hit stays audible.
  - Why: A new sound cuts off the oldest, so fast hits sound like one hit that keeps restarting.
- **B. TRUE.** Game logic usually decides when a sound plays, by reacting to an event such as a hit being scored.
  - Why: Cues are triggered from game events, not by the audio system itself.
- **C. FALSE.** When the game is paused, sound players keep playing as normal, so a pause menu's click needs no special setup.
  - Why: Players pause with the game; a pause-menu sound needs a player that keeps running.
- **D. FALSE.** If a sound player reports that it is playing, that shows players will hear the sound.
  - Why: 'Playing' is a flag at one instant; it does not show routing, level or that anyone hears it.
- **E. FALSE.** A sound set to loop still announces that it has finished each time it reaches its end.
  - Why: A looping sound never reports finishing, because it never ends on its own.

*Covered in:* Ch 12, 'Triggers: signals decide when, not the audio system' (game logic decides when, usually through a signal); 'Polyphony, restart and pause' (one voice by default so a new play cuts off the oldest; the finished notice never fires for a looping stream; players pause with the tree); 'The question' (a playing flag proves only that a flag was true at one instant, not that anyone hears it); 'Import' (looping is an import setting; flip it and the song never ends).

## 18. Chapter 13: Profiling and optimization

**A team's game stutters on its target device, and the team decides to measure before changing anything. Check each statement that is true.**  *(5 points)*

**True: B, C, D, E** (4 of 5)

- **A. FALSE.** A speed-up measured on a desktop tells you exactly how many milliseconds the same change will save on a phone.
  - Why: A desktop result gives at best a ratio to test on the device, not a prediction of its milliseconds.
- **B. TRUE.** A timing taken in a headless run (no display) leaves out the graphics processor's work, so it cannot show whether drawing is the problem.
  - Why: In a headless run draw counts and render times read zero; the numbers are CPU only.
- **C. TRUE.** Turning on a profiler slows the game while it records, so time the game with it off and use the profiler to find where the time went.
  - Why: Recording can slow a project significantly; timing is done with the profiler off.
- **D. TRUE.** Optimization should always be guided by measurement: profile, find the bottleneck, change that one thing, then measure again.
  - Why: The profile, identify, optimize, repeat loop is the discipline stated for optimization.
- **E. TRUE.** Repeating a measurement shows how much a result varies, because other work on the machine can change it, so a single run is weak evidence.
  - Why: Identical code gave very different times between runs; one run is an anecdote.

*Covered in:* Ch 13, 'Frame time is the unit' (always use profiling and timing to guide your efforts, in a loop), 'The human-with-a-screen tools' (the profiler must be started by hand because recording can slow the project; time with it off), 'Headless timing' (draw calls and GPU times read 0 headless), 'My verification' (variance is the machine; one run is an anecdote) and 'Mobile and XR constraints' (a desktop CPU measurement offers a ratio, a hypothesis to test on the device).

## 19. Chapter 14: How game characters decide (state machines, behavior trees)

**An enemy chases the player if it can see them, otherwise searches where it last saw them, otherwise patrols, and its brain is a behavior tree. Check each statement that is true.**  *(5 points)*

**True: A, E** (2 of 5)

- **A. TRUE.** A selector tries its children from left to right and stops at the first one that does not fail, which gives a do-this-otherwise-that priority.
  - Why: A selector is OR with priority: chase if you can, else search, else patrol.
- **B. FALSE.** A sequence stops at the first child that succeeds, so it behaves like an either-or choice.
  - Why: A sequence stops at the first child that does not succeed; it is AND with order. A selector is the either-or.
- **C. FALSE.** A node must report either success or failure straight away, so an action that takes time holds up the whole tree until it finishes.
  - Why: A node can also report that it is still running, which tells the tree to come back to it on the next tick.
- **D. FALSE.** A condition is the kind of leaf that moves the character and keeps reporting that it is still running until it arrives.
  - Why: That is an action; a condition asks a question and answers success or failure at once.
- **E. TRUE.** A blackboard is memory shared by the tree's nodes, where they can leave facts such as the last place the player was seen.
  - Why: The blackboard is the shared memory the leaves read and write.

*Covered in:* Ch 14, 'Behavior trees: priority, re-evaluated or remembered': every node returns SUCCESS, FAILURE or RUNNING (not finished, tick me again); a Condition returns success or failure immediately while an Action moves the guard and usually returns running; a Sequence stops at the first child that does not succeed (AND with order); a Selector stops at the first child that does not fail (OR with priority); the blackboard is the shared memory the leaves read and write.

## 20. Chapter 14: Generating levels (seed, noise, checking)

**A team's validator accepts a generated platformer level as crossable, and a designer asks what that acceptance shows. Check each statement that is true.**  *(5 points)*

**True: A** (1 of 5)

- **A. TRUE.** It shows only that the level fits the validator's model of the player's jumps; things the model leaves out, such as ceilings, could still make it uncrossable.
  - Why: The model ignores ceilings, run-up distance, the player's width and anything a designer would call fun.
- **B. FALSE.** It shows the level is fun and fair to play.
  - Why: The validator checks a playability rule, not fun or fairness.
- **C. FALSE.** It shows the generator can never produce an impossible level.
  - Why: One accepted level says nothing about every other level, and the model can still be wrong.
- **D. FALSE.** It proves that a real player can cross the level.
  - Why: A validator only models the player; acceptance does not establish that a real player can cross.
- **E. FALSE.** The validator's numbers for the player's jump are just as trustworthy when taken from memory as when measured on the real player.
  - Why: A validator is only as good as the numbers it is given, so the real jump is measured first.

*Covered in:* Ch 14, 'Procedural content generation' ('The validator is a model of the game's rules. It is only as good as the numbers you feed it, which is why Lab B measures the player's real jump before writing any validator') and Lab B 'Verify' ('It does not establish that an accepted level can be crossed. The validator's model ignores ceilings, run-up distance before a jump, the player's 14-pixel width, and anything a designer would call fun').

**Total true statements: 48 of 100.**
