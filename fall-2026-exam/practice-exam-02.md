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

**1.** A coding agent runs in a sandbox that lets it write inside the project folder. During an import step the engine prints an error that it cannot save its settings file, which lives in the user's home directory, yet the import still produces a usable project. Check each statement that is true.  *(5 points)*

- [ ] A. Running in a sandbox confirms that the code the agent writes is correct.
- [ ] B. A sandbox is a technical limit on what a process may read, write or reach.
- [ ] C. Inside this sandbox the agent can still delete project files, including test output it produced earlier.
- [ ] D. The error fits a sandbox blocking a write outside the project folder while writes inside it succeed.
- [ ] E. A sandbox and a permission prompt are one mechanism under two names.

**2.** A developer tells a coding agent: "Add ten enemies to the level." The agent duplicates the enemy's nodes ten times directly inside the level scene, and later the developer changes the enemy sprite. Check each statement that is true.  *(5 points)*

- [ ] A. Instances of one scene share a single position because they share one scene file.
- [ ] B. Instancing one saved Enemy scene ten times lets an edit to that scene reach each instance.
- [ ] C. Duplicated nodes are independent copies with no link to a shared enemy scene.
- [ ] D. The word "add" does not say whether to duplicate nodes or to instance a scene, which leaves open a choice that affects maintenance.
- [ ] E. "Instance the Enemy scene ten times in the level, at these positions" is a precise version of the instruction.

**3.** A developer asks an image generator for a character sprite "on a transparent background" and gets hero.jpg. In the engine the sprite sits inside a white rectangle. Check each statement that is true.  *(5 points)*

- [ ] A. An alpha channel stores opacity for each pixel.
- [ ] B. Removing a background by colour key can leave light fringe pixels along the edge.
- [ ] C. Lowering the sprite node's opacity makes just the white rectangle transparent.
- [ ] D. A white background painted into the pixels counts as transparency.
- [ ] E. JPEG has no alpha channel, so it does not hold transparency.

**4.** A scene has 50 identical trees. A developer asks the agent to add levels of detail (LOD). Check each statement that is true about the terms.  *(5 points)*

- [ ] A. The engine picks the LOD version by distance or screen size.
- [ ] B. LOD reduces the number of trees that are drawn.
- [ ] C. LOD keeps several versions of a mesh with decreasing triangle counts.
- [ ] D. A visible jump when the engine switches versions is called aliasing.
- [ ] E. Extra LOD meshes add no storage or load time.

**5.** A bomb should damage the enemies within 3 metres in any direction. Check each statement that is true about a shape query (overlap query) and a raycast.  *(5 points)*

- [ ] A. A shape query returns the objects that overlap a given shape, such as a sphere.
- [ ] B. A ray covers a line, not a region.
- [ ] C. One ray from the bomb finds the enemies in the whole area around it.
- [ ] D. A ray is used to ask who is near, and a shape query to ask what stands between two points.
- [ ] E. A shape query finds trigger regions and does not report solid bodies.

**6.** A designer wants a stealth meter that fills while an enemy can see the player. Sort what is built from what emerges using mechanic, dynamic and aesthetic. Check each statement that is true.  *(5 points)*

- [ ] A. A fill rate per second and the threshold at which enemies attack are parameters of the mechanic, and a test can check them.
- [ ] B. Players rushing between blind spots is a mechanic because the player performs it.
- [ ] C. The rule "the meter fills at a set rate while seen and drains when unseen" is a mechanic.
- [ ] D. Players waiting at cover for a patrol gap is an aesthetic.
- [ ] E. The satisfaction of slipping past a guard is a dynamic.

**7.** A simplified chain: vertex data, vertex shader, mapping to the screen, rasterization, fragment shader, depth and stencil tests plus blending, framebuffer. Check each statement that is true.  *(5 points)*

- [ ] A. Blending happens before the fragment shader.
- [ ] B. The vertex shader and the fragment shader are programmable stages.
- [ ] C. Rasterization is fixed-function: configured, not programmed.
- [ ] D. The vertex shader's output is already in screen pixels.
- [ ] E. The fragment shader runs before rasterization to decide which pixels a triangle covers.

**8.** In the metallic-roughness material model, each surface has a metallic value between 0 and 1. Check each statement that is true.  *(5 points)*

- [ ] A. A dielectric is a non-metal such as plastic, wood or skin, and it sits near metallic 0.
- [ ] B. A bare metal with a pure black albedo still shows bright, naturally coloured reflections.
- [ ] C. Specular is the reflection strength of a non-metal, which is a different control from metallic.
- [ ] D. Metallic controls how blurred reflections are, so metallic 1 gives the blurriest reflections.
- [ ] E. Values between 0 and 1 stand for transitions such as rust, dirt or chipped paint on a metal.

**9.** A material pack has albedo, normal map, roughness, ambient occlusion and emission colour images. A colour texture is stored in sRGB and decoded to linear before lighting; a data texture holds numbers used as stored. Check each statement that is true.  *(5 points)*

- [ ] A. Linear means the stored number goes into the shading maths as it is.
- [ ] B. A data texture is another name for a texture with an alpha channel.
- [ ] C. Emission colour is authored like albedo and is treated as sRGB.
- [ ] D. The normal map, roughness and ambient occlusion images are colour textures and are flagged as sRGB like albedo.
- [ ] E. Albedo is a colour texture and is imported as sRGB.

**10.** A coding agent reports: "Done. The shader compiles with no errors and the existing automated tests pass." Check each statement that is true about the terms.  *(5 points)*

- [ ] A. Existing tests that pass before and after a change show that nothing is drawn differently.
- [ ] B. A shader that multiplies a colour by the wrong factor still compiles.
- [ ] C. A compile error means the source was rejected, while a visual bug means it built and ran but drew a wrong result.
- [ ] D. A clean compile shows that the output matches the intended look.
- [ ] E. The agent's reply is a claim, and the compile log is evidence of valid syntax rather than of correct output.

**11.** A smoke emitter runs continuously. Check each statement that is true about the terms that fix how many particles are alive.  *(5 points)*

- [ ] A. Doubling the lifetime at the same rate leaves the live count unchanged.
- [ ] B. Doubling the emission rate at the same lifetime leaves the live count unchanged.
- [ ] C. Lifetime is the number of particles the emitter makes per second.
- [ ] D. The steady-state live count is roughly emission rate times lifetime.
- [ ] E. Lifetime is the time a particle stays alive after it is born, before the system removes it.

**12.** An animator keys a door's rotation to 0 degrees at 0.0 s and to 90 degrees at 1.0 s and sets nothing else. Check each statement that is true about the terms.  *(5 points)*

- [ ] A. Interpolation computes the values between keys, so the door shows intermediate angles.
- [ ] B. A keyframe is an authored value at a chosen time.
- [ ] C. The clip stores one value for each rendered frame.
- [ ] D. A display with a higher refresh rate needs the clip re-authored with more keys.
- [ ] E. Linear interpolation gives 60 degrees at 0.5 s.

**13.** A character has the states Idle, Run, Attack, Hurt and Dead. Hit reactions interrupt an attack, Dead overrides the other states, and Run input does not interrupt an attack. Check each statement that is true.  *(5 points)*

- [ ] A. An interrupt is a transition taken out of the current state before its clip ends.
- [ ] B. Priority or order decides which transition is taken when more than one is valid at the same moment.
- [ ] C. A transition from Any State to Dead expresses that death overrides the other states.
- [ ] D. Priority is needed because two states can be active at once.
- [ ] E. Leaving out an Attack-to-Run transition forbids that interruption, and Attack still needs some exit.

**14.** A cave region adds reverb to the SFX bus from the cave trigger's enter event and removes it on the exit event. Check each statement that is true.  *(5 points)*

- [ ] A. The reverb also colours the Music bus.
- [ ] B. Reverb on a bus is the same as positional attenuation.
- [ ] C. Enter and exit events are paired, and a missed exit can leave the reverb on.
- [ ] D. The reverb applies to sound effects routed through the SFX bus, including ones from far outside the cave.
- [ ] E. The cave trigger blocks the player, or its exit event will not fire.

**15.** A developer is choosing between batching, instancing and a texture atlas to cut draw calls. Check each statement that is true.  *(5 points)*

- [ ] A. Giving each object its own unique material makes batching easier.
- [ ] B. Batching merges geometry that shares a material into fewer draw calls.
- [ ] C. Instancing draws many copies of one mesh and one material in a single call, with per-instance data such as transform.
- [ ] D. A texture atlas packs many images into one texture, so objects that show different images can share a material.
- [ ] E. Instancing draws many copies of different meshes with different materials in one call.

**16.** A designer discusses reward design and deployment of an RL NPC. Check each statement that is true.  *(5 points)*

- [ ] A. Reward shaping removes the need to inspect the trained behavior.
- [ ] B. A sparse reward is feedback that arrives rarely, which makes learning hard.
- [ ] C. A trained policy is expected to keep learning during play by default.
- [ ] D. RL lets designers directly author each behavior.
- [ ] E. Reward hacking is an agent exploiting a loophole that scores well without doing what the designer meant.

**17.** Engines package a reusable game object once and then place many copies of it. Check each statement that is true.  *(5 points)*

- [ ] A. In Unity, a scene and a prefab are the same kind of asset, so loading a prefab replaces the current level.
- [ ] B. In Unity, a prefab is an asset that serves as a template, and each copy placed in a scene is a prefab instance linked to that asset.
- [ ] C. In Godot, a saved scene can be instantiated inside another scene, so one mechanism covers a whole level and a reusable object such as an enemy.
- [ ] D. In Unreal, a Blueprint class is an asset that defines a custom Actor type, and each Actor placed in a level from it is an instance of that class.
- [ ] E. In Unity, a prefab instance in a scene and the prefab asset are one object, so deleting the instance from the scene deletes the asset file.

**18.** An agent remembers a tool name from a tutorial, but the connected server does not list it. Which statements are correct? Check each statement that is true.  *(5 points)*

- [ ] A. A name remembered from a tutorial substitutes for the advertised tool definition.
- [ ] B. An input schema is the list of tools a server has installed.
- [ ] C. Renaming a scene object to the tutorial's tool name makes the server advertise that tool.
- [ ] D. Tool discovery means asking the server for the tools it advertises and then calling one of those.
- [ ] E. Two servers can advertise differently named or shaped tools for the same goal.

**19.** A server labels an operation read-only, and a studio decides whether an agent may call it automatically. Check each statement that is true.  *(5 points)*

- [ ] A. A read-only annotation guarantees the process is blocked from writing files.
- [ ] B. A read-only hint is a label from the server about what a tool does.
- [ ] C. An annotation is metadata, and an enforced permission is a technical limit.
- [ ] D. Provenance is where software came from and who maintains it.
- [ ] E. A description string performs enforcement.

**20.** A test oracle is the source of the expected result in a test. Check each statement that is true about oracles and checks.  *(5 points)*

- [ ] A. A tolerance lets a position comparison pass when the difference is small.
- [ ] B. A negative case proves that the positive case works.
- [ ] C. An oracle taken from the code under test is not independent.
- [ ] D. Floating-point positions are compared with exact equality because they are stored with perfect precision.
- [ ] E. Deliberately breaking the activation path to see the test fail checks that the test can detect the bug.

