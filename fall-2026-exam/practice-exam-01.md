# CSYE 7270 Building Virtual Environments: Fall 2026 practice exam 01

**PRACTICE ONLY. The real Fall 2026 exam uses different questions.** The answers are kept in a separate file for after you finish.

Name: ______________________

**100 points = 20 multiple-answer questions x 5 points.** Suggested time: about 60 minutes (about 3 minutes per question).

## How to answer

- Each question has five statements, A to E. Check the statements that are true. A question can have anywhere from one to four true statements.
- Each statement is worth 1 point, true or false on its own: you score a point when you check a true statement and a point when you leave a false statement blank.
- The exam tests what the ideas of the course mean and how they differ. It does not ask you to read or write code.
- Read each statement by itself. A strong word such as "always" often makes a statement false, but not every strong-sounding statement is false.

---

**1.** An AI coding agent reports "Done, all tests pass." Check each statement that is true about what that report shows.  *(5 points)*

- [ ] A. A clean import and script check shows that the game's behaviour is right.
- [ ] B. Playing the game yourself once shows what every player on every machine will experience.
- [ ] C. The agent saying "done" shows that the agent produced a message, not that the game works.
- [ ] D. A passing test shows that the game is fun and readable.
- [ ] E. A listing of the changes (a diff) shows exactly what changed but not that the change works.

**2.** A student sets up an AI coding agent on a game project and chooses what it may do without asking.  *(5 points)*

- [ ] A. A permission prompt is a formality to click through quickly, because the agent only asks about commands that are safe.
- [ ] B. A sandbox that confines writing to the project folder can block a harmless write elsewhere, such as a tool saving its own settings, without stopping the rest of the work.
- [ ] C. A permission rule decides which commands the agent may run without asking a person, and a sandbox limits where the agent's commands can write.
- [ ] D. Allowing a program that can run scripts the agent writes is a wide permission, because those scripts can do things the program's name does not suggest.
- [ ] E. The setting that lets an agent run any command without asking is meant only for isolated containers or virtual machines, not for an everyday personal machine.

**3.** A student opens a Godot project folder for the first time and wants to know how it is organised.  *(5 points)*

- [ ] A. A project is a folder with a project settings file at its top level, and paths inside the project are measured from the folder that holds that file.
- [ ] B. A saved scene is a text file listing its nodes, their settings and their signal connections, so a diff can show exactly what changed in it.
- [ ] C. A project whose saved scene holds a single node must be nearly empty, because everything in a running game comes from saved scenes.
- [ ] D. The import cache folder, which the editor rebuilds, should be committed to version control so every machine has the same imported assets.
- [ ] E. Imported pictures and sounds are stored as text, so an agent can read a picture's pixels the same way it reads a saved scene.

**4.** A student asks an image generator for a game sprite and then has to use the result in a 2D game.  *(5 points)*

- [ ] A. To get a character facing both ways, it is better to generate one facing direction and flip it in the game, since generators often draw 'left' and 'right' the same.
- [ ] B. A prompt made of mood words such as menacing and crisp is enough to give a file that can be checked for size and frame layout.
- [ ] C. A request that asks the generator for a transparent background often gets a painted checkerboard, so a plain solid background that is removed afterwards works better.
- [ ] D. A generated image that looks like finished game art in a picture viewer has already met the engine's needs for size, background and frame layout.
- [ ] E. A tool that cuts an image into equal grid cells always works correctly, even on a picture where the generator placed the creatures freely.

**5.** In Blender, an artist makes a thin pole by stretching a large cube, then exports it to Godot. Check each statement that is true.  *(5 points)*

- [ ] A. Stretching the cube changes the object's scale, but the mesh's own vertices still describe the original cube until the transform is applied.
- [ ] B. If the pole looks the right size in the running game, its transform must already have been applied.
- [ ] C. Applying the transform is best left until after the model has been imported into Godot.
- [ ] D. A collision shape generated from a mesh that carries a stretched scale inherits that scale, which is one reason to apply the transform before export.
- [ ] E. Applying the transform before export changes how the pole looks in the game, making it thinner or thicker.

**6.** A teammate suggests that the agent write a Python script for Blender to run with no window, instead of chatting with an open Blender through MCP. Check each statement that is true about the difference.  *(5 points)*

- [ ] A. Exploring an existing scene or adjusting one object in conversation suits a script better than a live MCP connection.
- [ ] B. A script leaves behind a file you can read, compare with earlier versions and rerun to rebuild the same asset.
- [ ] C. A script can reach fewer Blender features than the MCP tools, because the tools use features that scripts cannot.
- [ ] D. A script can encode a wrong assumption and then repeat it faithfully every time it runs.
- [ ] E. With a live MCP connection, the project's version history automatically records how each change to the scene was made.

**7.** A beginner is learning how a Godot game is built. Check each statement that is true.  *(5 points)*

- [ ] A. A scene can only be a whole level.
- [ ] B. A node does one job, such as drawing a sprite, holding a collision shape or counting down a timer.
- [ ] C. Reusing a saved scene as a template is called instancing, and an edit to the source scene shows up in its instances.
- [ ] D. A scene is a saved tree of nodes, and it can be a whole level or a single enemy.
- [ ] E. A signal is a message a node sends when something happens to it, and other nodes can connect to it to react.

**8.** A coin in a 2D Godot game should add to the score when the player touches it, but the player should walk straight through it. Check each statement that is true.  *(5 points)*

- [ ] A. A trigger is an area that reports when something overlaps it and never blocks or pushes.
- [ ] B. The coin should be a solid collider, so the player is stopped by it and the score changes on touch.
- [ ] C. A trigger works from the coin's picture, so it needs no collision shape.
- [ ] D. The shape the physics engine uses is always the same as the picture the player sees.
- [ ] E. A collider is a shape the physics engine uses to detect contact, and a solid one blocks other objects.

**9.** A team is writing requirements for a new checkpoint feature in a 3D Godot world, and for a phone version of that world. They want each requirement to be checkable and honest. Check each statement that is true.  *(5 points)*

- [ ] A. A requirement for a new feature should leave out existing behaviour, so that the requirement stays short and focused.
- [ ] B. Touch simulated with a mouse on a desktop is enough to call the phone version verified.
- [ ] C. A requirement is checkable when a stranger could write its test without having to ask the author what was meant.
- [ ] D. A scripted test cannot press a game's controls, so a feature's requirement has to be judged by a person playing.
- [ ] E. When a scripted test of the feature passes, that shows players can see the feature and will understand it.

**10.** A technical artist is learning what a shader is. Check each statement that is true.  *(5 points)*

- [ ] A. When a shader decides one pixel's colour, it can look at the colour its neighbouring pixel ended up with.
- [ ] B. One part of a shader decides where each corner of a shape lands, and another decides the colour of each pixel the shape covers.
- [ ] C. A shader is a small program that runs on the graphics processor, not the main processor.
- [ ] D. A shader is where the game's rules, such as the score, are written.
- [ ] E. A shader runs once for the whole image, from start to finish.

**11.** A designer asks an AI agent to "make the metal crate look worn". Check each statement that is true about materials and textures.  *(5 points)*

- [ ] A. A shader is the program that turns a surface's inputs and the lighting into the colour of each pixel.
- [ ] B. The roughness and metallic images are colour pictures and are treated like the base colour.
- [ ] C. A material and a texture are the same thing.
- [ ] D. A material of the usual modern kind describes a surface by measurements such as base colour, how metallic it is and how rough it is, not by one picture.
- [ ] E. Of the textures that describe a surface, the base-colour one holds colour, while the roughness and metallic ones hold numbers stored in an image file.

**12.** A texture artist adds a normal map to a stone wall to give it fine surface detail. Check each statement that is true about normal maps.  *(5 points)*

- [ ] A. An image that merely looks like a normal map is not guaranteed to be a valid one, so one made by an AI image tool needs checking.
- [ ] B. A normal map records how much of the surrounding light reaches each crevice of the wall.
- [ ] C. A normal map holds data rather than colour, so reading it as an ordinary colour image would make the lighting come out wrong.
- [ ] D. A normal map records, for each point, which way the surface faces, at a finer detail than the wall's mesh has.
- [ ] E. A normal map records the colour of the stone at each point.

**13.** A student tests a shader's colour fade after a player failure by running the game with no window (a headless run) at several fixed frame rates. Check each statement that is true.  *(5 points)*

- [ ] A. A run with no window can still report a coding mistake in a shader, such as a value of the wrong type.
- [ ] B. A run with no window can check that gameplay code gives the shader the right values at the right moments.
- [ ] C. A fade that counts frames instead of game time can pass at the frame rate usually tested and still be wrong at other frame rates.
- [ ] D. Fixing the frame rate makes a run repeatable, because every frame then covers the same amount of game time.
- [ ] E. A run with no window can show which colour the shader actually drew for each pixel, because the shader still runs on the graphics processor there.

**14.** A game needs two effects: smoke that keeps rising from a chimney, and a burst of sparks that plays once when a barrel breaks. Check each statement that is true.  *(5 points)*

- [ ] A. In a continuous effect the particles are not removed, so the number alive keeps growing the longer the effect runs.
- [ ] B. Lifetime is the number of particles born in one emission cycle.
- [ ] C. Smoke that keeps rising suits a continuous effect, in which new particles keep being born at a steady pace.
- [ ] D. A one-shot effect plays a single emission cycle and then stops.
- [ ] E. In a burst, all of the particles are born together at the start instead of being spread out over time.

**15.** A 2D team is deciding how to animate a character. Check each statement that is true.  *(5 points)*

- [ ] A. A rig is a skeleton of connected bones, and moving the bones moves the pieces of the character attached to them.
- [ ] B. With a rig, every pose is stored as a separate finished drawing.
- [ ] C. Sprite-sheet animation needs a skeleton.
- [ ] D. A rig can pose the same artwork many ways without a new drawing for each pose, while a sprite sheet shows exactly the drawing made for each frame.
- [ ] E. A sprite sheet is one image holding the frames of an animation in a grid, and the animation shows one frame after another.

**16.** A character can be idle, running, jumping or falling, and its animation is organised as a state machine. Check each statement that is true.  *(5 points)*

- [ ] A. A state machine is in one state at a time and moves between states along defined transitions.
- [ ] B. A state machine lets the character be in running and jumping at the same moment.
- [ ] C. A transition is the connection that says when the character may leave one state for another.
- [ ] D. A transition can be set to wait until the current animation has finished before the next state begins.
- [ ] E. A state machine is the way to mix two clips together by a continuous number such as speed.

**17.** A developer is learning when to use a plain sound player and when to use one that gives a sound a place in the world. Check each statement that is true.  *(5 points)*

- [ ] A. Positional sound is only possible in 3D games, because distance needs three dimensions.
- [ ] B. Any sound player attached to a moving enemy gets quieter with distance, because it belongs to the enemy.
- [ ] C. A positional player makes a sound quieter as the listener gets farther from the place the sound comes from.
- [ ] D. Background music and interface clicks suit a plain player, because their loudness should never depend on where the camera is.
- [ ] E. A 3D positional sound can only be heard if the developer adds a listener object to the scene by hand.

**18.** A team wants its Godot game to run at 60 frames per second. Check each statement that is true.  *(5 points)*

- [ ] A. The average frame time alone is enough to tell that the game is smooth.
- [ ] B. Frames per second counts how many frames are drawn each second, and frame time is how long each frame takes.
- [ ] C. An optimization is justified when it is faster by enough to matter against the frame budget on the hardware the game targets.
- [ ] D. A frame budget is the longest time one frame may take and still meet the target frame rate.
- [ ] E. "It is faster" is a good enough reason by itself to make an optimization change.

**19.** A guard that patrols, chases and searches has its brain built as a finite state machine. Check each statement that is true.  *(5 points)*

- [ ] A. States cannot share behavior, so a rule many states need, such as jumping, must be copied into every one of them.
- [ ] B. The order of the states in a list decides which behavior wins, and the list is re-checked from the top on every update.
- [ ] C. In a state machine each state knows its own exits: the rules for leaving a behavior are stored with that behavior.
- [ ] D. Using a larger distance for giving up on the player than for noticing the player stops the guard flipping between chasing and searching at the boundary.
- [ ] E. A stack of states lets a character return to what it was doing before an interruption, such as going back to running after a jump.

**20.** A level generator sometimes produces platformer levels with a gap too wide to jump, and the team wants every level it ships to be playable. Check each statement that is true.  *(5 points)*

- [ ] A. Generate-and-test builds a level, checks it, and throws it away and builds another if the check fails.
- [ ] B. A playability check needs only the level's own data, since what the player can do does not matter.
- [ ] C. A playability check has to be done by a person playing each level, because software cannot model a player's jump.
- [ ] D. Fixing the seed removes the need for a playability check, because the same seed always gives the same level.
- [ ] E. A generator that can produce an impossible level is only half a system; the other half is a check that each level meets a playability rule.

