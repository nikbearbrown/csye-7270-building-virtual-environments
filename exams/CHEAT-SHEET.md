# CSYE 7270 Building Virtual Environments: exam cheat sheet

**Status: DRAFT v0.1, 2026-11-08, for TA review.** Written by Claude from the midterm glossary and the question bank. **The instructor has not signed it off.** Every definition is from the glossary; lines that add general knowledge are marked *(not checked)*.

Full term list: [GLOSSARY-jargon-midterm.md](/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/exams/GLOSSARY-jargon-midterm.md). Practice: [practice-exams](/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/exams/practice-exams) and the [question bank](/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/exams/question-bank/INDEX.md).

## Executive summary

**What this is.** One sheet of the words the midterm is built on, grouped by topic. The exam is a language test: precise words let you tell an animation, shader, material, camera or movement tool exactly what to build. "Dolly in, 1.5 seconds, ease-out" gets that. "Swoop in" gets a guess.

**How to use it.** Read the ten-second version, then the "tell apart" table: most wrong answers swap two near-neighbour terms. A line you cannot say in your own words goes to the glossary; then take a practice exam.

**What the exam asks.** Multiple-answer: five statements per question, each true or false on its own, 1 point each. Meanings hold for Godot, Unity, Unreal and Blender unless a row names an engine. Many questions turn on mapping one idea to each engine's name.

## The ten-second version

- Pan and tilt turn the camera on the spot; dolly and truck move it. A dolly changes parallax; a zoom only changes the lens.
- Multiply per-second values by **delta time** or the game runs at different speeds on different machines.
- A **collider** blocks; a **trigger** (Area, Is Trigger, Overlap) detects and does not block.
- Shader: **vertex** stage sets positions, **fragment** stage sets pixel colour. A uniform comes from code.
- A **normal map** fakes bumps in lighting; it does not change the silhouette. **Displacement** moves vertices.
- Colour textures are sRGB; data textures (normals, roughness) are linear.
- A **state machine** has one active state and transitions that fire on conditions; unreachable and dead-end states are bugs.
- Check the **evidence**, not the agent's **claim**.
- Least privilege, deny by default, and a person approves what the agent may do.

## Tell apart (most wrong answers are here)

| Pair | The difference |
|---|---|
| Pan vs truck | turn left or right on the spot / move sideways, still facing the same way |
| Tilt vs pedestal | turn up or down / move straight up or down |
| Dolly vs zoom | move along the view direction (parallax changes) / change the lens (camera does not move) |
| Orbit vs follow | curve around a subject / track a moving target, often smoothed |
| Perspective vs orthographic | distance shrinks things / size independent of distance |
| Scene vs level vs map | saved tree of objects / one playable scene / Unreal's level file |
| Prefab vs Blueprint class | Unity template / Unreal template |
| Node vs GameObject vs Actor | Godot / Unity (needs components) / Unreal (placeable in a level) |
| Instancing vs inheriting | place a scene inside another / extend it as a new type |
| Local vs world vs screen space | relative to parent / whole level / pixels on screen |
| Up axis | Y in Godot and Unity; Z in Unreal and Blender |
| Polling vs event-driven | ask every frame / run when something announces it |
| Signal vs delegate | Godot's event / Unreal's and C#'s typed function list |
| Just pressed vs pressed | first frame only / while held |
| `_ready` vs `_init` vs `_enter_tree` | node and children in tree / constructor, before tree / node joins, before children ready |
| `_process` vs `_physics_process` | every frame / fixed steps |
| `queue_free` vs `free` | delete at end of frame / delete now |
| `_input` vs `_unhandled_input` | every event / only events nobody used |
| Call down, signal up | parents call children; children announce to parents |
| Rigid vs kinematic vs static body | forces / your code / never moves |
| CharacterBody2D `move_and_slide` vs `move_and_collide` | slides along surfaces / stops at first hit and reports it |
| Collision layer vs mask | what an object is / what it looks for |
| Force vs impulse | push over time / instant velocity change |
| Raycast vs shape query | line, first hit / what overlaps a shape now |
| Hitscan vs projectile | instant along a ray / flies |
| Enter / stay / exit event | first frame of overlap / every step during / when it ends |
| Detection vs response | noticing contact / deciding what happens |
| Tunnelling vs continuous collision detection | fast object skips a thin collider / checks the whole path |
| Coyote time vs jump buffer | jump still works just after leaving a ledge / early press remembered until landing |
| Hitbox vs hurtbox | deals damage / takes damage |
| Keyframe vs tween vs clip | stored value at a time / code interpolation / authored track set |
| FK vs IK | rotate parent to child / give a target, solver finds the angles |
| Root motion vs in-place | clip moves the character / code supplies travel |
| Blend tree vs state machine | weighted mix by parameter / one active state, transitions |
| Rig vs sprite sheet | skeleton plus binding / grid of frames |
| Albedo vs diffuse vs base colour | base colour, no lighting (same idea) / matte scattered light |
| Roughness vs smoothness | blurry highlights / its inverse |
| Metallic workflow vs specular workflow | albedo + metallic mask / diffuse + specular colour map |
| Alpha blend vs additive | mix by opacity / add to background (glow, fire) |
| Material vs texture vs shader | surface recipe / one image / GPU program |
| Shared material vs material instance | edit hits all users / child with own values |
| Normal vs normal map | direction at a point / texture storing it per pixel |
| Nearest vs linear filtering | hard-edged pixels / smooth blend |
| Mipmaps vs LOD | pre-shrunk textures / cheaper models at distance |
| Repeat vs clamp | tile past 0 to 1 / stretch the edge pixel |
| Triangle vs face vs vertex count | engines budget by triangles; Blender shows faces |
| Trimesh vs convex hull vs primitive | exact triangles, static only / tightest convex wrap / box, sphere, capsule |
| Collision shape vs visual mesh | simple physics shape / detailed picture |
| glTF vs GLB vs OBJ | open exchange format / glTF in one binary / old mesh-only format |
| CPU- vs GPU-bound | processor limits the frame / graphics card limits it |
| CPU vs GPU particles | flexible, fewer / many, less control |
| Local vs world coordinates (particles) | move with emitter / left behind |
| Mean vs median vs 99th percentile (frame time) | average / middle, ignores outliers / the worst-case tail players feel |
| Hitch vs stutter | one long frame / repeated uneven frames |
| Selector vs sequence (behavior tree) | tries children until one succeeds / runs until first failure |
| A* vs Dijkstra | cost so far plus heuristic / cost so far only |
| White vs coherent noise | unrelated values / smooth (Perlin, simplex) |
| Generate-and-test vs constructive generation | make then reject / rules guarantee validity |
| Tool vs resource vs prompt (MCP) | named action / read-only data by URI / reusable message template |
| Host vs client vs server (MCP) | AI app / its connection to one server / offers tools |
| Request vs notification | expects a reply / one-way |
| Transport failure vs tool execution error | channel broke / tool ran and reported failure |
| Verification vs claim | independent check / what was said |
| Allowlist vs denylist | what is permitted / what is forbidden (deny by default is stricter) |
| Authentication vs authorization | proving who you are / deciding whether you may act |
| Idempotent vs atomic | repeat = same result / all or nothing |
| Resume vs restore | continue where it stopped / go back to an earlier state |

## By topic

**Toolchain.** CLI, shell, flag, headless (no window), exit code (0 = success), timeout vs hang. Import converts source files; caches can go stale. Sandbox, permission prompt, allow rule. Instruction file (such as CLAUDE.md) holds standing rules. Acceptance test decides acceptance. **Claim vs evidence.** Flaky tests pass and fail with no change; deterministic ones do not (fixed frame rate, pinned time step, fixed seed). Text scenes diff cleanly, binary ones do not.

**Engine vocabulary.** Tick, frame, fixed step, catch-up. Input action maps a name ("jump") to keys; just-pressed vs held. Asset, resource (Godot), ScriptableObject (Unity), Data Asset (Unreal). Singleton: autoload (Godot), DontDestroyOnLoad (Unity), Game Instance (Unreal). Export (Godot) = build; export templates are required.

**Game movement.** Velocity, acceleration, friction, gravity. Delta time and frame-rate independence. Fixed timestep for physics. Cutting a jump = reduce upward velocity on release, only while rising. Double scaling = multiplying by delta and passing to a call that already scales.

**Collision and physics.** Layers and masks are bitmasks. Physics material (friction, bounce) is not the render material. `is_on_floor`. One-way platform. Query vs event.

**2D art and sound.** Texture atlas, tileset vs tilemap, padding/bleed, seamless tiling. Integer scaling and nearest filtering keep pixel art crisp. PNG lossless with alpha; JPEG lossy without. Sample rate and the Nyquist limit (half the rate); bit depth sets dynamic range; clipping, headroom, ducking, bus, master bus, 0 dB unity gain. Keep a lossless master. Provenance, licence terms, attribution.

**3D and Blender.** Normals, flipped normals, backface culling, UV unwrapping and seams, origin vs pivot, apply transforms (bake scale), unit (usually a metre), handedness. bpy, headless Blender, add-ons. LOD popping. Capsule collider for characters; convex or primitive for moving bodies; trimesh only for static.

**Design documents.** GDD, pillar, core loop vs meta loop vs game loop, mechanic/dynamic/aesthetic, prototype vs vertical slice vs MVP, scope creep, cut/defer/swap. Acceptance criterion in given-when-then form with a tolerance. Loosening a check to pass is a false pass. Direct state write is not gameplay.

**Shaders.** Rasterization turns triangles into fragments; interpolation blends vertex values; overdraw; depth and stencil tests; alpha test and `discard`. Godot types: `canvas_item` (2D), `spatial` (3D); built-ins `TIME`, `SCREEN_UV`. Spaces: local, world, view, clip, screen; normals need the inverse transpose when scale is uneven. Full vs half precision. Divergence slows the GPU.

**Materials and textures.** PBR energy conservation; dielectric vs metal; height, bump, normal, displacement; tangent space and the green channel convention (OpenGL up, DirectX down); ambient occlusion, SSAO; texel density; channel packing and ORM (occlusion R, roughness G, metallic B); block compression; VRAM.

**Shader verification.** Compile error vs visual bug. Observed vs inferred. Golden or reference image, software renderer for identical output everywhere, per-platform references, pinned clock, controlled input. Test oracle; false positive vs false negative checks.

**Particles.** Emitter, emission shape, rate vs burst, lifetime, spread, steady state (births = deaths), prewarm, scale curve, colour ramp, normalised age. Billboard vs mesh particles. Fill rate and overdraw cost. Seed gives determinism. Check state, visual intent and cost separately; headless runs show no visuals.

**Animation.** States, conditions, guards, interrupts, priority; Any State; stuck state, dead end, unreachable state; forced state skips transitions. AnimationPlayer/AnimationTree (Godot), Animator Controller (Unity), Animation Blueprint (Unreal). Startup / active / recovery frames; cancel window; hit list so one swing hits each target once; input buffer; cooldown. Single source of truth and authority for state.

**Audio.** Positional vs non-positional players; listener; attenuation, falloff, max distance. Bus effects (reverb, side-chain), gain staging, dBFS. Voice and polyphony. Audio clock vs game time; mix boundary and output latency. Signal vs polling for triggers; node lifetime decides whether a sound finishes.

**Profiling.** Frame budget 16.7 ms at 60 FPS. Judge with percentiles, not just mean. Bottleneck, main vs render thread. Instancing, frustum and occlusion culling, LOD, object pooling (acquire, release, exhaustion). Garbage collection hitches. Warm-up and noise: take a baseline before a change. Profile a release build on target hardware. No premature optimization: find the hot spot first.

**Game AI.** FSM, behavior tree (success / failure / running), utility AI, GOAP (preconditions and effects). Hysteresis stops flicker. Steering: seek, pursue, arrive, flee, separation, alignment, cohesion (emergent flocking). Navmesh is baked; agent radius matters. A*: f = g + h; admissible heuristic never overestimates. Octaves of coherent noise. RL: agent, environment, reward, policy, return, discount factor; reward hacking vs reward shaping.

**Agent workflow.** MCP uses JSON-RPC over stdio or streamable HTTP; initialization sets protocol revision and capabilities. Validate arguments against the input schema; mind units and coordinate space; read back to confirm. Stale references: re-resolve. Narrow tool vs general script evaluator (blast radius). Partial failure, targeted retry, idempotency key, atomic transaction, rollback route, checkpoint. Security: trust boundary, egress, prompt injection (indirect injection arrives in content the agent reads), path traversal and canonicalization, rotation, never hardcode secrets, audit log, approval granularity, containment. Unreal: game thread, Blueprint compile, dynamic material instance, duplicate binding fires twice. Unity: prefab apply vs revert, MaterialPropertyBlock, in-memory vs saved state, dirty scene.

## Wrong word, right word

- "Pan closer" is a **dolly in**.
- "A normal map for colour" is **albedo**; "fragment shader moves vertices" is a **vertex shader**.
- "A trigger that blocks" is a **collider**.
- "Fast on a fast PC" means the movement is missing **delta time**.
- "The agent said it works" is a **claim**; evidence is output, a measurement or a test that failed before and passes now.
- A test whose expected value was copied from the code's own output is **tautological**; break the code on purpose (mutation check) to see if it fails.

## Not covered here

Anything outside the glossary. Essay questions are retired. Chapter 14 depth beyond the Game AI terms above is thin on this sheet *(not checked against the lecture slides)*.
