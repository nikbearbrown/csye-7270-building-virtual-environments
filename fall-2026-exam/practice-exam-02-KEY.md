# Practice exam 02: ANSWER KEY (read it only AFTER doing the exam cold)

Each statement is scored on its own, 1 point. Under every statement is the reason it is true or false, and each question names the course topic to review.

The physics, shader, audio and animation answers are **awaiting a game developer's check**. If a key looks wrong to you on those, say so.

---

## 1. Chapter 0: The toolchain (agents, repositories, sandboxes, instruction files)

**A coding agent runs in a sandbox that lets it write inside the project folder. During an import step the engine prints an error that it cannot save its settings file, which lives in the user's home directory, yet the import still produces a usable project. Check each statement that is true.**  *(5 points)*

**True: B, C, D** (3 of 5)

- **A. FALSE.** Running in a sandbox confirms that the code the agent writes is correct.
  - Why: A sandbox limits damage; it says nothing about correctness.
- **B. TRUE.** A sandbox is a technical limit on what a process may read, write or reach.
  - Why: Sandboxes restrict capabilities at the operating-system level.
- **C. TRUE.** Inside this sandbox the agent can still delete project files, including test output it produced earlier.
  - Why: Deleting is a kind of write, and writes inside the workspace are allowed.
- **D. TRUE.** The error fits a sandbox blocking a write outside the project folder while writes inside it succeed.
  - Why: The settings file is outside the project folder, and the cache is inside it.
- **E. FALSE.** A sandbox and a permission prompt are one mechanism under two names.
  - Why: A prompt asks a human before a command runs; a sandbox enforces limits on what a running command can touch.

## 2. Chapter 1: Scenes, nodes and signals

**A developer tells a coding agent: "Add ten enemies to the level." The agent duplicates the enemy's nodes ten times directly inside the level scene, and later the developer changes the enemy sprite. Check each statement that is true.**  *(5 points)*

**True: B, C, D, E** (4 of 5)

- **A. FALSE.** Instances of one scene share a single position because they share one scene file.
  - Why: Each instance has its own transform.
- **B. TRUE.** Instancing one saved Enemy scene ten times lets an edit to that scene reach each instance.
  - Why: Instances stay linked to the scene file they came from.
- **C. TRUE.** Duplicated nodes are independent copies with no link to a shared enemy scene.
  - Why: Plain duplicates are unlinked, so each needs the edit by hand.
- **D. TRUE.** The word "add" does not say whether to duplicate nodes or to instance a scene, which leaves open a choice that affects maintenance.
  - Why: Duplicating and instancing give different results later, so the verb needs to be exact.
- **E. TRUE.** "Instance the Enemy scene ten times in the level, at these positions" is a precise version of the instruction.
  - Why: It names the term (instance), the scene and the placement.

## 3. Chapter 2: Game art and sound assets

**A developer asks an image generator for a character sprite "on a transparent background" and gets hero.jpg. In the engine the sprite sits inside a white rectangle. Check each statement that is true.**  *(5 points)*

**True: A, B, E** (3 of 5)

- **A. TRUE.** An alpha channel stores opacity for each pixel.
  - Why: Alpha is the extra channel for opacity.
- **B. TRUE.** Removing a background by colour key can leave light fringe pixels along the edge.
  - Why: Anti-aliased edge pixels blend the character with the old background.
- **C. FALSE.** Lowering the sprite node's opacity makes just the white rectangle transparent.
  - Why: Node opacity fades the whole image, character and background.
- **D. FALSE.** A white background painted into the pixels counts as transparency.
  - Why: Painted white is colour content, not an alpha value.
- **E. TRUE.** JPEG has no alpha channel, so it does not hold transparency.
  - Why: PNG stores alpha and JPEG does not.

## 4. Chapter 3: 3D assets and the Blender pipeline

**A scene has 50 identical trees. A developer asks the agent to add levels of detail (LOD). Check each statement that is true about the terms.**  *(5 points)*

**True: A, C** (2 of 5)

- **A. TRUE.** The engine picks the LOD version by distance or screen size.
  - Why: Smaller on screen means a cheaper version.
- **B. FALSE.** LOD reduces the number of trees that are drawn.
  - Why: LOD lowers the triangles per tree and leaves the tree count alone.
- **C. TRUE.** LOD keeps several versions of a mesh with decreasing triangle counts.
  - Why: That is the definition of level of detail.
- **D. FALSE.** A visible jump when the engine switches versions is called aliasing.
  - Why: The visible switch is called popping; aliasing is jagged edges.
- **E. FALSE.** Extra LOD meshes add no storage or load time.
  - Why: Each version is more data to store and load.

## 5. Chapter 4: Collision and physics

**A bomb should damage the enemies within 3 metres in any direction. Check each statement that is true about a shape query (overlap query) and a raycast.**  *(5 points)*

**True: A, B** (2 of 5)

- **A. TRUE.** A shape query returns the objects that overlap a given shape, such as a sphere.
  - Why: A shape query tests a region at this moment.
- **B. TRUE.** A ray covers a line, not a region.
  - Why: A ray is a single line.
- **C. FALSE.** One ray from the bomb finds the enemies in the whole area around it.
  - Why: A 3 metre region needs a shape query or many rays.
- **D. FALSE.** A ray is used to ask who is near, and a shape query to ask what stands between two points.
  - Why: The roles are swapped: a shape query finds who is near and a ray checks what is in between.
- **E. FALSE.** A shape query finds trigger regions and does not report solid bodies.
  - Why: Shape queries test colliders in general, solid bodies included.

## 6. Chapter 5: Game design documents and virtual worlds

**A designer wants a stealth meter that fills while an enemy can see the player. Sort what is built from what emerges using mechanic, dynamic and aesthetic. Check each statement that is true.**  *(5 points)*

**True: A, C** (2 of 5)

- **A. TRUE.** A fill rate per second and the threshold at which enemies attack are parameters of the mechanic, and a test can check them.
  - Why: Numbers and observable results make a mechanic buildable and checkable.
- **B. FALSE.** Players rushing between blind spots is a mechanic because the player performs it.
  - Why: Emergent player behaviour is a dynamic; the mechanic is the rule that makes it worthwhile.
- **C. TRUE.** The rule "the meter fills at a set rate while seen and drains when unseen" is a mechanic.
  - Why: It is a rule the designer builds.
- **D. FALSE.** Players waiting at cover for a patrol gap is an aesthetic.
  - Why: That is behaviour that emerges, so it is a dynamic.
- **E. FALSE.** The satisfaction of slipping past a guard is a dynamic.
  - Why: A felt response is an aesthetic.

## 7. Chapter 6: Shader foundations (what a shader is and does)

**A simplified chain: vertex data, vertex shader, mapping to the screen, rasterization, fragment shader, depth and stencil tests plus blending, framebuffer. Check each statement that is true.**  *(5 points)*

**True: B, C** (2 of 5)

- **A. FALSE.** Blending happens before the fragment shader.
  - Why: Blending uses the shader's output colour, so it comes after.
- **B. TRUE.** The vertex shader and the fragment shader are programmable stages.
  - Why: Developers write both in a shader language.
- **C. TRUE.** Rasterization is fixed-function: configured, not programmed.
  - Why: Developers do not write it.
- **D. FALSE.** The vertex shader's output is already in screen pixels.
  - Why: It typically outputs clip-space positions that are converted later.
- **E. FALSE.** The fragment shader runs before rasterization to decide which pixels a triangle covers.
  - Why: It runs on fragments rasterization produced.

## 8. Chapter 7: Materials and textures (material, shader, texture)

**In the metallic-roughness material model, each surface has a metallic value between 0 and 1. Check each statement that is true.**  *(5 points)*

**True: A, C, E** (3 of 5)

- **A. TRUE.** A dielectric is a non-metal such as plastic, wood or skin, and it sits near metallic 0.
  - Why: Dielectric is the term for a non-metal, and metallic 0 selects that behaviour.
- **B. FALSE.** A bare metal with a pure black albedo still shows bright, naturally coloured reflections.
  - Why: A metal takes its reflection tint from the base colour, so a black albedo gives almost no reflection.
- **C. TRUE.** Specular is the reflection strength of a non-metal, which is a different control from metallic.
  - Why: Specular scales reflection on non-metals, while metallic switches the kind of material.
- **D. FALSE.** Metallic controls how blurred reflections are, so metallic 1 gives the blurriest reflections.
  - Why: Reflection blur is roughness, not metallic.
- **E. TRUE.** Values between 0 and 1 stand for transitions such as rust, dirt or chipped paint on a metal.
  - Why: A real point is metal or not, so in-between values stand for mixed or partly covered areas.

## 9. Chapter 7: Materials and textures (physically based surface properties)

**A material pack has albedo, normal map, roughness, ambient occlusion and emission colour images. A colour texture is stored in sRGB and decoded to linear before lighting; a data texture holds numbers used as stored. Check each statement that is true.**  *(5 points)*

**True: A, C, E** (3 of 5)

- **A. TRUE.** Linear means the stored number goes into the shading maths as it is.
  - Why: Linear values are used directly in lighting calculations.
- **B. FALSE.** A data texture is another name for a texture with an alpha channel.
  - Why: A data texture is defined by its content being numbers, not by having alpha.
- **C. TRUE.** Emission colour is authored like albedo and is treated as sRGB.
  - Why: Emission colour is a colour and follows the colour path.
- **D. FALSE.** The normal map, roughness and ambient occlusion images are colour textures and are flagged as sRGB like albedo.
  - Why: Those three hold numbers or vectors, so they are data textures and are read as linear.
- **E. TRUE.** Albedo is a colour texture and is imported as sRGB.
  - Why: Albedo is authored as colour for human vision and decoded to linear.

## 10. Chapter 8: Shader verification (evidence that a shader is right)

**A coding agent reports: "Done. The shader compiles with no errors and the existing automated tests pass." Check each statement that is true about the terms.**  *(5 points)*

**True: B, C, E** (3 of 5)

- **A. FALSE.** Existing tests that pass before and after a change show that nothing is drawn differently.
  - Why: Tests cover only what they check, and drawing may be outside them.
- **B. TRUE.** A shader that multiplies a colour by the wrong factor still compiles.
  - Why: A wrong formula is valid code, so it compiles.
- **C. TRUE.** A compile error means the source was rejected, while a visual bug means it built and ran but drew a wrong result.
  - Why: Compile errors and visual bugs are different failure types caught at different stages.
- **D. FALSE.** A clean compile shows that the output matches the intended look.
  - Why: A compiler checks syntax and types, not the design.
- **E. TRUE.** The agent's reply is a claim, and the compile log is evidence of valid syntax rather than of correct output.
  - Why: A claim is a statement, and evidence is something observed that supports it.

## 11. Chapter 9: Particle effects

**A smoke emitter runs continuously. Check each statement that is true about the terms that fix how many particles are alive.**  *(5 points)*

**True: D, E** (2 of 5)

- **A. FALSE.** Doubling the lifetime at the same rate leaves the live count unchanged.
  - Why: A longer life means particles pile up for longer before removal, so the count grows.
- **B. FALSE.** Doubling the emission rate at the same lifetime leaves the live count unchanged.
  - Why: Live count scales with the rate, so doubling the rate doubles the count.
- **C. FALSE.** Lifetime is the number of particles the emitter makes per second.
  - Why: That describes emission rate, not lifetime.
- **D. TRUE.** The steady-state live count is roughly emission rate times lifetime.
  - Why: Births per second times seconds of life gives the number alive once the effect has settled.
- **E. TRUE.** Lifetime is the time a particle stays alive after it is born, before the system removes it.
  - Why: Lifetime is the length of a particle's life in seconds.

## 12. Chapter 10: Animation foundations (sprite sheets, rigs, kinematics)

**An animator keys a door's rotation to 0 degrees at 0.0 s and to 90 degrees at 1.0 s and sets nothing else. Check each statement that is true about the terms.**  *(5 points)*

**True: A, B** (2 of 5)

- **A. TRUE.** Interpolation computes the values between keys, so the door shows intermediate angles.
  - Why: Interpolation fills in the in-betweens.
- **B. TRUE.** A keyframe is an authored value at a chosen time.
  - Why: A key is a value pinned to a time.
- **C. FALSE.** The clip stores one value for each rendered frame.
  - Why: The clip stores two keys; the engine computes values for frames.
- **D. FALSE.** A display with a higher refresh rate needs the clip re-authored with more keys.
  - Why: Values are sampled from time, so any display rate works with the same keys.
- **E. FALSE.** Linear interpolation gives 60 degrees at 0.5 s.
  - Why: Linear interpolation halfway between 0 and 90 gives 45 degrees.

## 13. Chapter 11: Animation and interaction (state machines, blending)

**A character has the states Idle, Run, Attack, Hurt and Dead. Hit reactions interrupt an attack, Dead overrides the other states, and Run input does not interrupt an attack. Check each statement that is true.**  *(5 points)*

**True: A, B, C, E** (4 of 5)

- **A. TRUE.** An interrupt is a transition taken out of the current state before its clip ends.
  - Why: An interrupt leaves a state early, through a transition that does not wait for the clip to finish.
- **B. TRUE.** Priority or order decides which transition is taken when more than one is valid at the same moment.
  - Why: Equal-looking choices are settled by an order, which should be stated.
- **C. TRUE.** A transition from Any State to Dead expresses that death overrides the other states.
  - Why: Any State is a special source that stands for the states in the machine.
- **D. FALSE.** Priority is needed because two states can be active at once.
  - Why: A machine has one active state; priority chooses between several valid transitions.
- **E. TRUE.** Leaving out an Attack-to-Run transition forbids that interruption, and Attack still needs some exit.
  - Why: A missing transition is how a machine forbids a change, but a state without an exit sticks.

## 14. Chapter 12: Audio and triggers

**A cave region adds reverb to the SFX bus from the cave trigger's enter event and removes it on the exit event. Check each statement that is true.**  *(5 points)*

**True: C, D** (2 of 5)

- **A. FALSE.** The reverb also colours the Music bus.
  - Why: Only sounds routed through SFX are processed.
- **B. FALSE.** Reverb on a bus is the same as positional attenuation.
  - Why: Reverb adds reflections; attenuation lowers level with distance.
- **C. TRUE.** Enter and exit events are paired, and a missed exit can leave the reverb on.
  - Why: A toggle driven by two events is correct only if both arrive.
- **D. TRUE.** The reverb applies to sound effects routed through the SFX bus, including ones from far outside the cave.
  - Why: A bus effect is not positional.
- **E. FALSE.** The cave trigger blocks the player, or its exit event will not fire.
  - Why: A trigger reports enter and exit without blocking.

## 15. Chapter 13: Profiling and optimization

**A developer is choosing between batching, instancing and a texture atlas to cut draw calls. Check each statement that is true.**  *(5 points)*

**True: B, C, D** (3 of 5)

- **A. FALSE.** Giving each object its own unique material makes batching easier.
  - Why: Unique materials split the groups and defeat batching.
- **B. TRUE.** Batching merges geometry that shares a material into fewer draw calls.
  - Why: Shared material is the condition for merging into fewer calls.
- **C. TRUE.** Instancing draws many copies of one mesh and one material in a single call, with per-instance data such as transform.
  - Why: Per-instance data such as transform is supplied alongside the shared mesh.
- **D. TRUE.** A texture atlas packs many images into one texture, so objects that show different images can share a material.
  - Why: An atlas lets different pictures live in one texture and one material.
- **E. FALSE.** Instancing draws many copies of different meshes with different materials in one call.
  - Why: Instances share one mesh and one material.

## 16. Chapter 14: Game AI and systems

**A designer discusses reward design and deployment of an RL NPC. Check each statement that is true.**  *(5 points)*

**True: B, E** (2 of 5)

- **A. FALSE.** Reward shaping removes the need to inspect the trained behavior.
  - Why: Shaping adds guiding rewards; the result still has to be inspected.
- **B. TRUE.** A sparse reward is feedback that arrives rarely, which makes learning hard.
  - Why: Rare reward gives little signal.
- **C. FALSE.** A trained policy is expected to keep learning during play by default.
  - Why: A trained policy typically runs as a fixed decision function.
- **D. FALSE.** RL lets designers directly author each behavior.
  - Why: Behavior is learned, so it is hard to author or debug directly.
- **E. TRUE.** Reward hacking is an agent exploiting a loophole that scores well without doing what the designer meant.
  - Why: The agent optimizes the score, not the intent.

## 17. Across engines: Godot, Unity and Unreal vocabulary

**Engines package a reusable game object once and then place many copies of it. Check each statement that is true.**  *(5 points)*

**True: B, C, D** (3 of 5)

- **A. FALSE.** In Unity, a scene and a prefab are the same kind of asset, so loading a prefab replaces the current level.
  - Why: Scenes and prefabs are different asset types; opening a prefab does not replace the level.
- **B. TRUE.** In Unity, a prefab is an asset that serves as a template, and each copy placed in a scene is a prefab instance linked to that asset.
  - Why: The prefab asset is the template; instances in scenes are linked copies of it.
- **C. TRUE.** In Godot, a saved scene can be instantiated inside another scene, so one mechanism covers a whole level and a reusable object such as an enemy.
  - Why: In Godot a scene file is both the level format and the reusable-object format, and scenes nest.
- **D. TRUE.** In Unreal, a Blueprint class is an asset that defines a custom Actor type, and each Actor placed in a level from it is an instance of that class.
  - Why: A Blueprint class is the definition; each placed copy is an instance of that class.
- **E. FALSE.** In Unity, a prefab instance in a scene and the prefab asset are one object, so deleting the instance from the scene deletes the asset file.
  - Why: The instance is a separate object in the scene; removing it leaves the asset untouched.

## 18. Agents and tools: MCP (what it is and its parts)

**An agent remembers a tool name from a tutorial, but the connected server does not list it. Which statements are correct? Check each statement that is true.**  *(5 points)*

**True: D, E** (2 of 5)

- **A. FALSE.** A name remembered from a tutorial substitutes for the advertised tool definition.
  - Why: Names and arguments differ between integrations.
- **B. FALSE.** An input schema is the list of tools a server has installed.
  - Why: A schema describes one tool's arguments.
- **C. FALSE.** Renaming a scene object to the tutorial's tool name makes the server advertise that tool.
  - Why: Object names do not register server operations.
- **D. TRUE.** Tool discovery means asking the server for the tools it advertises and then calling one of those.
  - Why: Discovery grounds the call in the live server.
- **E. TRUE.** Two servers can advertise differently named or shaped tools for the same goal.
  - Why: Tool catalogs are implementation-specific.

## 19. Agents and safety: permissions and untrusted text

**A server labels an operation read-only, and a studio decides whether an agent may call it automatically. Check each statement that is true.**  *(5 points)*

**True: B, C, D** (3 of 5)

- **A. FALSE.** A read-only annotation guarantees the process is blocked from writing files.
  - Why: An annotation is metadata, not a technical limit.
- **B. TRUE.** A read-only hint is a label from the server about what a tool does.
  - Why: It describes intent.
- **C. TRUE.** An annotation is metadata, and an enforced permission is a technical limit.
  - Why: Only the limit constrains behaviour.
- **D. TRUE.** Provenance is where software came from and who maintains it.
  - Why: It informs how much to trust it.
- **E. FALSE.** A description string performs enforcement.
  - Why: Enforcement comes from permissions or sandboxing.

## 20. Agents and checking: claim versus evidence, tests that test

**A test oracle is the source of the expected result in a test. Check each statement that is true about oracles and checks.**  *(5 points)*

**True: A, C, E** (3 of 5)

- **A. TRUE.** A tolerance lets a position comparison pass when the difference is small.
  - Why: A tolerance is an allowed difference for numeric results.
- **B. FALSE.** A negative case proves that the positive case works.
  - Why: Each case tests its own path.
- **C. TRUE.** An oracle taken from the code under test is not independent.
  - Why: An independent oracle comes from the requirement, not from the implementation.
- **D. FALSE.** Floating-point positions are compared with exact equality because they are stored with perfect precision.
  - Why: Floating-point results often differ in the last digits, so a tolerance is used.
- **E. TRUE.** Deliberately breaking the activation path to see the test fail checks that the test can detect the bug.
  - Why: A test that cannot fail on broken code gives false confidence.

**Total true statements: 53 of 100.**
