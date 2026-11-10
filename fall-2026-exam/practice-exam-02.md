# CSYE 7270 Building Virtual Environments: Fall 2026 practice exam 02

**PRACTICE ONLY. The real Fall 2026 exam uses different questions.** The answers are kept in a separate file for after you finish.

Name: ______________________

**100 points = 20 multiple-answer questions x 5 points.** Suggested time: about 60 minutes (about 3 minutes per question).

## How to answer

- Each question has five statements, A to E. Check the statements that are true. A question can have anywhere from one to four true statements.
- Each statement is worth 1 point, true or false on its own: you score a point when you check a true statement and a point when you leave a false statement blank.
- The exam tests what the ideas of the course mean and how they differ. It does not ask you to read or write code.
- Read each statement by itself. A strong word such as "always" often makes a statement false, but not every strong-sounding statement is false.

---

**1.** A student is judging whether an agent's change to a game altered anything it should not have, using the kinds of evidence a project can provide.  *(5 points)*

- [ ] A. Writing down the exact results of a passing test run before a change lets the student see afterwards whether the change altered behaviour under that same run.
- [ ] B. An exported build that runs on the target machine shows that players will want to play the game.
- [ ] C. A scripted route that passes is the same kind of evidence as a person playing, because it presses the game's real controls.
- [ ] D. An agent that ran its own new test correctly can be assumed to have run the project's older tests correctly too.
- [ ] E. A test that counts frames while the game moves by seconds can give different results on different runs, so its result is weak evidence until the time step is fixed.

**2.** A student runs a game's automated test from the command line in headless mode, and the run finishes with a success result.  *(5 points)*

- [ ] A. A headless test that counts sound cues shows that the sound is audible and sounds right.
- [ ] B. A headless run has no window and no sound, yet the game's scripts, physics, signals and timers still run.
- [ ] C. Because a headless run produces no picture, a test can read values such as positions or a label's text, but it cannot judge whether the label is readable.
- [ ] D. A headless run that finishes with a success result printed no errors while it ran.
- [ ] E. If a headless test script hits an error before it finishes, the run ends by itself with a failing result, so a time limit is unnecessary.

**3.** A beginner is learning when Godot runs the code that updates a game while it plays.  *(5 points)*

- [ ] A. One kind of update runs once for every drawn frame, so how often it runs depends on how fast the machine can draw.
- [ ] B. A game that moves objects by a distance per second of elapsed time makes them travel farther each second on a machine that draws more frames.
- [ ] C. Another kind of update, used for physics, runs at a fixed rate, so each step covers the same slice of game time.
- [ ] D. A test that counts fixed-rate physics steps measures more game time on a fast machine than on a slow one.
- [ ] E. A game that moves an object by a fixed distance on every drawn frame makes it move faster on a machine that draws more frames per second.

**4.** A student adds looping music and short sound effects to a 2D game.  *(5 points)*

- [ ] A. Short sound effects are usually imported with looping turned on, so that they can be repeated.
- [ ] B. A sound played without any position still gets quieter and pans as the listener moves away from the place it came from.
- [ ] C. To play a jump sound once per jump, start it when the player enters the jumping state, not on every frame the player is in that state.
- [ ] D. A one-shot effect plays from start to finish once each time it is triggered, while a loop returns to its loop point and keeps playing until it is stopped.
- [ ] E. The engine automatically finds a smooth loop point in any music file, so it does not matter where a generated track is cut.

**5.** A 3D artist builds a prop in Blender and brings it into a Godot game. Check each statement that is true about carrying it across.  *(5 points)*

- [ ] A. Blender, glTF and Godot all count one unit of distance as one metre, so a prop built at Blender's standard unit setting arrives at its intended size.
- [ ] B. glTF is an interchange format for moving a 3D model between tools, and Godot recommends it for importing models.
- [ ] C. Godot's physics works the same at any scale, so the size of an imported prop changes how it looks but not how it plays.
- [ ] D. Blender treats Z as up while glTF and Godot treat Y as up, so the exporter turns the model's height onto the other axis.
- [ ] E. A prop that arrives in Godot lying on its side was exported at the wrong size.

**6.** A coding agent reports that it built a prop in Blender and exported it for a Godot game. Check each statement that is true about what to verify afterwards.  *(5 points)*

- [ ] A. Once the exported file exists, the script that made it can be thrown away, because the file records how it was built.
- [ ] B. If the numbers the agent reports match the plan, the prop is known to look right under the game's lights.
- [ ] C. A script that fails partway can still let Blender finish as if it had succeeded unless told otherwise, so a finished run is not evidence of success.
- [ ] D. If the agent's own test passes, the collision shape must be correct, since the agent wrote the test to check it.
- [ ] E. Test output pasted into the agent's report is as good as evidence as running the checks yourself.

**7.** A student asks how the tree of nodes shown in the editor relates to what actually runs when a Godot game plays. Check each statement that is true.  *(5 points)*

- [ ] A. A property changed on one instance of a scene overrides the value from the source scene for that instance alone.
- [ ] B. Code that creates scene instances during play also has to decide who frees them, or unused objects can pile up.
- [ ] C. Every instance of a scene has to be placed in the editor before play, because new instances cannot be created while the game runs.
- [ ] D. The running scene tree can contain nodes that scripts add during play, so it can be larger than the tree shown for a saved scene.
- [ ] E. A signal works by one node reaching into another node and changing its data directly.

**8.** A 2D platformer has a stone floor, a crate that should tumble when pushed, and a hero steered by the player's own code. Check each statement that is true.  *(5 points)*

- [ ] A. If the hero's artwork is swapped for a wider picture, its collision shape resizes itself to match the new art.
- [ ] B. Turning on the display of collision shapes while the game runs lets you compare them with what is drawn.
- [ ] C. A body that the physics engine moves, like the crate, is steered best by having your code overwrite its position every frame.
- [ ] D. A solid fixed body, like the floor, is never moved by the physics engine, but other bodies collide with it.
- [ ] E. A body you move yourself, like the hero, gets collision detection but not simulated physics, so your code decides how it moves.

**9.** A coding agent reads an existing Godot project and writes a design document for the game that is already there, marking each claim with how it is known. Check each statement that is true.  *(5 points)*

- [ ] A. If the project contains a sprite for a feature, the document can list that feature as a working mechanic.
- [ ] B. A claim marked 'observed' is meant to be something the code actually does, and one marked 'missing' is something the code cannot tell you.
- [ ] C. To check a claim marked 'observed', the student opens the code it points to and reads it.
- [ ] D. Numbers the agent finds in the code, such as a jump speed, show the values the team has approved for the final design.
- [ ] E. Once every claim in the recovered document carries a tag, the design stages count as signed off.

**10.** A student is comparing the different jobs a shader can do in a Godot game. Check each statement that is true.  *(5 points)*

- [ ] A. A shader can include an optional part that runs for every pixel and every light, which is where it controls how lighting affects a surface.
- [ ] B. There are different kinds of shader for different jobs, for example one for 3D models, one for 2D sprites and interface, and one for the sky.
- [ ] C. Changing where a shape's corners land in a shader does not move the drawing, which can only be moved by the game's own code.
- [ ] D. The graphics processor runs a shader's pixel part for one pixel at a time, in order, finishing each before starting the next.
- [ ] E. The part of a shader that colours pixels runs once for the whole shape, so every pixel of the shape gets the same result.

**11.** Ten identical crates in a 3D level use one shared material. A designer wants a single crate to glow red when it is hit. Check each statement that is true about materials.  *(5 points)*

- [ ] A. A model made of several parts can have a different material on each part, so changing one part's material leaves the others as they were.
- [ ] B. The designer can give the hit crate its own copy of the material, or use a setting kept separately for each object, so the other nine are not affected.
- [ ] C. A setting such as the glow amount is stored on the shader program itself, not on any material.
- [ ] D. The material alone decides the colour a player sees, so a material that looks right in one scene will look right in every other.
- [ ] E. If the game changes a setting on the shared material, the change affects just the crate that was hit.

**12.** A student copies the textures for a 3D model into a Godot project and notices that each image has import settings. Check each statement that is true about why those settings matter.  *(5 points)*

- [ ] A. When an AI agent connects a texture to a material by editing the project's text files, the texture's import settings are adjusted automatically to suit its use.
- [ ] B. A normal map has its own import setting, so it can be treated as a normal map instead of as an ordinary picture.
- [ ] C. Without mipmaps, which are smaller pre-made versions of a texture, distant surfaces on a 3D model shimmer.
- [ ] D. Textures for a 3D model left in the lossless mode meant for 2D art use more video memory than a compressed mode meant for 3D would.
- [ ] E. Import settings decide how an image is prepared before it reaches the graphics processor, for example how it is compressed.

**13.** A team wants to trust its checks of a shader's colour flash. It writes an automated timing check, a small model that predicts the colours, and a test scene with fixed inputs. Check each statement that is true.  *(5 points)*

- [ ] A. A test scene with fixed inputs is built to be looked at: a person screenshots it and compares sampled pixel colours with the model's predictions.
- [ ] B. Before a new check is trusted, it should be tried on a version known to be wrong and on a version known to be right.
- [ ] C. A check that compares the fade with the current code's own internal countdown still passes after the fade is correctly rewritten to use a different timer.
- [ ] D. A check that follows the written specification may still need a small tolerance, because the engine's clocks make even correct code differ slightly from the ideal.
- [ ] E. A test that confirms the scene is set up with the intended inputs also confirms that the shader draws the expected colours.

**14.** A mobile game's smoke effect makes the frame rate drop, and a programmer is looking for the cause. Check each statement that is true.  *(5 points)*

- [ ] A. Large, see-through particles that overlap cost extra to draw, because each covers many pixels and the same pixels get filled again and again.
- [ ] B. Particles simulated on the graphics processor cost nothing, so there is no need to limit how many an effect has.
- [ ] C. A test run with no window can measure what a graphics-processor particle effect costs the graphics hardware.
- [ ] D. An effect that costs little on a powerful desktop computer will cost just as little on a phone.
- [ ] E. Particles simulated on the main processor take more main-processor time each frame as their number grows.

**15.** A character has a skeleton of bones with its visible surface attached to them. A designer wants the character's hand to reach toward a target while an animation plays. Check each statement that is true.  *(5 points)*

- [ ] A. Skinning attaches the character's visible surface to the bones, with weights saying how strongly each bone moves each part of the surface.
- [ ] B. A skeleton's rest pose is the pose at the end of the most recent animation that played on it.
- [ ] C. Inverse kinematics pulls the end of a chain of bones, such as a hand at the end of an arm, toward a target position.
- [ ] D. Inverse kinematics is applied on top of the animation, adjusting the pose that the animation has already produced.
- [ ] E. Inverse kinematics blends two animation clips together according to a continuous value such as the character's speed.

**16.** A designer adds a lunge attack in which the character's body moves forward as part of the animation, and wants smooth changes between the character's states. Check each statement that is true.  *(5 points)*

- [ ] A. A transition between two states can include a short cross-fade, so the pose changes smoothly instead of cutting at once.
- [ ] B. Root motion is the setting that decides how long a transition between two states takes.
- [ ] C. A blend of clips driven by speed is the right tool for a jump that must play its takeoff once started, even if the player lets go of the button.
- [ ] D. With root motion, the forward movement of the body comes from the animation itself, as in a lunge that carries the character ahead.
- [ ] E. Using root motion hands control of the character's movement to the animation, so tests of that movement become tests of animation data.

**17.** A rhythm game plays a short click when the player hits a note well, over a looping background song. Check each statement that is true.  *(5 points)*

- [ ] A. A player that can play only one sound at a time layers each new sound on top of the old one, so every rapid hit stays audible.
- [ ] B. Game logic usually decides when a sound plays, by reacting to an event such as a hit being scored.
- [ ] C. When the game is paused, sound players keep playing as normal, so a pause menu's click needs no special setup.
- [ ] D. If a sound player reports that it is playing, that shows players will hear the sound.
- [ ] E. A sound set to loop still announces that it has finished each time it reaches its end.

**18.** A team's game stutters on its target device, and the team decides to measure before changing anything. Check each statement that is true.  *(5 points)*

- [ ] A. A speed-up measured on a desktop tells you exactly how many milliseconds the same change will save on a phone.
- [ ] B. A timing taken in a headless run (no display) leaves out the graphics processor's work, so it cannot show whether drawing is the problem.
- [ ] C. Turning on a profiler slows the game while it records, so time the game with it off and use the profiler to find where the time went.
- [ ] D. Optimization should always be guided by measurement: profile, find the bottleneck, change that one thing, then measure again.
- [ ] E. Repeating a measurement shows how much a result varies, because other work on the machine can change it, so a single run is weak evidence.

**19.** An enemy chases the player if it can see them, otherwise searches where it last saw them, otherwise patrols, and its brain is a behavior tree. Check each statement that is true.  *(5 points)*

- [ ] A. A selector tries its children from left to right and stops at the first one that does not fail, which gives a do-this-otherwise-that priority.
- [ ] B. A sequence stops at the first child that succeeds, so it behaves like an either-or choice.
- [ ] C. A node must report either success or failure straight away, so an action that takes time holds up the whole tree until it finishes.
- [ ] D. A condition is the kind of leaf that moves the character and keeps reporting that it is still running until it arrives.
- [ ] E. A blackboard is memory shared by the tree's nodes, where they can leave facts such as the last place the player was seen.

**20.** A team's validator accepts a generated platformer level as crossable, and a designer asks what that acceptance shows. Check each statement that is true.  *(5 points)*

- [ ] A. It shows only that the level fits the validator's model of the player's jumps; things the model leaves out, such as ceilings, could still make it uncrossable.
- [ ] B. It shows the level is fun and fair to play.
- [ ] C. It shows the generator can never produce an impossible level.
- [ ] D. It proves that a real player can cross the level.
- [ ] E. The validator's numbers for the player's jump are just as trustworthy when taken from memory as when measured on the real player.

