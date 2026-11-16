# Exam cheat sheet: everything that is fair game

**The exam:** 100 points, 20 multiple-answer questions, each with five statements (A to E) that you mark true or false one at a time. Paper, no laptop, no phone. You have the whole class period, 3:25 to 5:05 (100 minutes); most people will need about 60. Godot only: no Unity or Unreal. No code: you will not read or write GDScript or the Godot shading language.

**How to use this sheet**
1. Find the topic. "Know" says what you need, in plain words.
2. "Go to" names the deck, slide number and slide title where it is taught. Slide numbers are the ones shown on screen; in a deck, press **G** for the slide grid.
3. Several questions are **picture questions**: you get a drawing (a curve, a rig, a state machine, an editor window) and decide what it shows. They are drawn the way the slides draw them, so study the pictures on the slides, not only the words.

**Anything not on this sheet is not on the exam.**

---

## Part 1. Working with an agent

### 1. Playtesting
**Know:** An agent can build the game, but only playing it tells you whether it is fun. With an agent, your time moves from writing code to playing and playtesting. A passing test is evidence about the game's state, not a playtest.
**Go to:** Deck 04 Walker and the toolchain, slide 3, "The Walker loop and git" (playtest is a step in the Walker loop) · Deck 04 Walker and the toolchain, slide 10, "The evidence ladder" (rung 5: "you played it") · Deck 01 Game design A, slide 10, "Prototype and play testing"

### 2. Directing an agent
**Know:** Be specific, not vague: a good instruction is one a check can pass or fail. Give context (instruction files) and references.
**Go to:** Deck 04 Walker and the toolchain, slide 8, "Instruction files and checkable instructions" · Deck 01 Game design A, slide 7, "Fun, target experience, appeal" · Deck 07 Art principles and concept art, slide 7, "Concept art, reference and mood boards" · every deck's "Say it exactly" slide, for example Deck 12 Materials and textures, slide 15, "Say it exactly"

### 3. MCP
**Know:** MCP is a standard way for an AI app to call tools inside another program. Godot can be scripted directly (command line, headless, text scene files). Blender can be driven two ways: a Python (bpy) script run headless, or an MCP server with an add-on inside Blender. Editor-heavy tools are why an MCP matters.
**Go to:** Deck 04 Walker and the toolchain, slide 4, "Command line, flags and headless" · Deck 04 Walker and the toolchain, slide 11, "Text scenes, binary scenes, regression tests" · Deck 09 Blender to Godot, slide 3, "MCP: an agent calls a tool inside Blender" · Deck 09 Blender to Godot, slide 4, "bpy scripts, headless Blender and the exit code"

## Part 2. Tools and game design

### 4. The Godot editor interface (picture questions)
**Know:** Scene dock (the nodes; the Remote tab shows the running game), FileSystem dock (files under `res://`), Inspector (properties of the selected node), Node dock (its signals and groups). Along the top: 2D, 3D, Script. At the bottom: Output and Debugger. Run Project (F5) starts the main scene; Run Current Scene starts the open one.
**Go to:** Deck 05 Godot editor and scenes, slide 3, "The docks: Scene, FileSystem, Inspector, Node" · Deck 05 Godot editor and scenes, slide 4, "Views, Output, Debugger, Settings, Run"

### 5. The Blender interface (very basic)
**Know:** 3D viewport (see and edit the scene), Outliner (tree of objects and collections), Properties editor (settings for the selected thing), Timeline (frames and keyframes), Workspaces (saved layouts), Object Mode versus Edit Mode.
**Go to:** Deck 08 Blender interface and modeling, slide 3, "The Blender window: viewport, outliner, properties" · Deck 08 Blender interface and modeling, slide 4, "Workspaces and the timeline" · Deck 08 Blender interface and modeling, slide 5, "Object Mode, Edit Mode and collections"

### 6. Normals
**Know:** Only what a normal is: the direction a surface faces, straight out from it.
**Go to:** Deck 08 Blender interface and modeling, slide 8, "Normals and flipped normals" (the definition only)

### 7. Game design documents and their sixteen sections
**Know:** A GDD says what the game is and how it plays, in enough detail to build and test it. The sixteen sections, in order: Metadata, Vision summary, Pillars, Core loop, PX goals, Mechanics, Systems, Progression, World, Narrative, Characters, Feature list, Out of scope, Technical requirements, Risks, Open questions.
**Go to:** Deck 10 Game design document, slide 3, "GDD, game brief and pitch" · Deck 10 Game design document, slide 5, "The sixteen sections" · Deck 10 Game design document, slide 6, "Goal to mechanic to test" · core loop: Deck 01 Game design A, slide 5, "Mechanic, player verb, core mechanic, core loop" · pillars: Deck 03 Game design C, slide 3, "Three pillars"

### 8. Concept art, character art, character sheet
**Know:** Concept art is early drawing that solves a design problem for the team; it is not finished art. Reference and mood boards support it. Character art covers iconic elements, a proxy model, readability, anatomy and the neutral pose.
**Go to:** Deck 07 Art principles and concept art, slide 7, "Concept art, reference and mood boards" · Deck 07 Art principles and concept art, slide 10, "Iconic elements, proxy and readability" · Deck 07 Art principles and concept art, slide 12, "Anatomy and the neutral pose"

## Part 3. Art, colour and collision

### 9. Resolution, anti-aliasing and pixelation (pixel art)
**Know:** Resolution is width and height in pixels. For pixel art, Nearest filtering keeps hard edges (Linear blends and smooths), and whole-number scaling keeps every pixel the same width.
**Go to:** Deck 06 2D art and sound assets, slide 3, "Resolution, viewport and aspect ratio" · Deck 06 2D art and sound assets, slide 4, "Texels, nearest and linear, integer scaling"

### 10. RGB, alpha, albedo
**Know:** RGBA is four channels: red, green, blue and alpha (opacity). Albedo (base colour) is the colour a surface reflects before any lighting. Black is (0, 0, 0) and white is (1, 1, 1).
**Go to:** Deck 11 Shader foundations, slide 12, "RGBA, linear and sRGB" · Deck 06 2D art and sound assets, slide 6, "Alpha, transparent backgrounds, PNG and JPEG, fringe" · Deck 12 Materials and textures, slide 4, "Albedo, roughness and metallic" (albedo only)

### 11. Tinting (multiplying a colour)
**Know:** Multiply all of a colour's channels by the same number and the ratios stay the same: the same colour, lighter or darker. Multiply the channels by different numbers and the ratios change: a different colour.
**Go to:** Deck 11 Shader foundations, slide 9, "Vertex colour, TEXTURE, COLOR, TIME" · Deck 12 Materials and textures, slide 4, "Albedo, roughness and metallic"

### 12. Colliders, collisions and triggers
**Know:** A collider (collision shape) is what physics treats as solid; it is separate from the art. Static, rigid and character bodies block; an area reports overlap and never blocks, so it is the trigger. Layers and masks say who can notice whom.
**Go to:** Deck 05 Godot editor and scenes, slide 10, "The four collision objects" · Deck 05 Godot editor and scenes, slide 11, "Layers, masks and the bitmask" · Deck 05 Godot editor and scenes, slide 12, "Collision shape and area snapshot" · Deck 06 2D art and sound assets, slide 9, "The collider is not the art"

## Part 4. Shaders, materials and textures

### 13. Shaders: vertex and fragment (pixel)
**Know:**
- A shader is a small program the graphics processor runs many times at once.
- **Vertex shader:** maps 3D to 2D. Input: one vertex (a corner point of the model). Output: where that vertex lands on the 2D screen.
- **Fragment shader = pixel shader** (two names, one thing): maps 2D to 2D, pixel to pixel. Input: one screen position the shape covers, with values blended from the corners and any textures. Output: the colour of that one pixel.
- **Order:** the vertex shader comes first, then the fragment (pixel) shaders. The 3D-to-2D step happens once; there can be several fragment shaders.
**Go to:** Deck 11 Shader foundations, slide 3, "Shader, vertex shader, fragment shader" · Deck 11 Shader foundations, slide 4, "The pipeline: two stages you write, two built in" · Deck 11 Shader foundations, slide 5, "Fragment, varying, interpolation"

### 14. Materials, textures and PBR (general idea only)
**Know:** A texture is an image the game samples to colour (or describe) a surface. A material is what is applied to a surface: it holds the settings, and the textures, that a shader reads to draw it. A material is not a texture, and a texture alone is not a material.
**PBR, at a general level:** PBR means physically based rendering: an approach that models how light interacts with surfaces. It matters because materials respond consistently and believably when the lighting changes. Knowing what PBR is and why it matters is fair game. No detailed PBR knowledge or experience using a PBR-based No-Bake system is required.
**Go to:** Deck 12 Materials and textures, slide 3, "Material, PBR and lighting" · Deck 06 2D art and sound assets, slide 4, "Texels, nearest and linear, integer scaling"

### 15. UV and the UV map
**Know:** UV is a 2D coordinate that maps a surface to a texture, 0 to 1 across it. A UV map is the flat layout of a mesh used to place a texture. A surface position (UV) is not the same as a screen position: two shapes can share UV values but sit at different places on screen.
**Go to:** Deck 11 Shader foundations, slide 8, "UV and SCREEN_UV" · Deck 08 Blender interface and modeling, slide 13, "UV maps, unwrapping, materials and textures" · Deck 12 Materials and textures, slide 10, "UV, unwrapping and baking"

### 16. Particles
**Know:** A particle is one small image or shape the system draws and moves for a short life. An emitter is where particles come from. A particle system is the whole thing: emitter, particles and the rules that move them. Godot has two kinds, GPU-based and CPU-based: the CPU kind is the safe choice for low-end devices; the GPU kind handles large numbers of particles and has more features.
**Go to:** Deck 14 Particles and VFX, slide 3, "Particle, emitter and particle system" · Deck 14 Particles and VFX, slide 10, "GPU nodes, CPU nodes and the process material"

## Part 5. Animation (deck 15 and the sprite slides)

### 17. Sprite-based and rig-based animation, skin and skin weights (critical)
**Know:**
- A **sprite sheet** is one image of many frames. **Sprite-based** (frame-by-frame) animation plays those frames in order at a frame rate.
- **Rig-based** animation moves a hierarchy of bones (the rig). The **skin** connects the mesh to the bones; **skin weights** set how much each bone moves each part of the 3D mesh.
- **Picture question:** you get a simple rigged character. Decide what it can and cannot move. A part with no bone cannot move on its own; a child bone follows its parent.
**Go to:** Deck 06 2D art and sound assets, slide 5, "Sprite sheets, atlases and frame rate" · Deck 15 Animation principles, slide 11, "Rig, rest pose and skinning weights"

### 18. Keyframes and in-betweens
**Know:** A keyframe sets a value at a moment in time. In-betweens are the frames between keys that the computer fills in.
**Go to:** Deck 15 Animation principles, slide 3, "Keys, in-betweens, clips and tweens" · Deck 15 Animation principles, slide 4, "Linear, step and cubic"

### 19. Animation curves, timing and spacing (picture questions)
**Know:** A curve shows how a value changes between keys, so you can see where a move is fast and where it is slow. Ease-in starts slow; ease-out ends slow; ease-in-out does both. Timing is how long a move takes; spacing is how far it moves from frame to frame (close together = slow, far apart = fast).
**Picture questions:** a ball moving between two keyframes with its curve, or the ball's spacing. Is it starting fast or slow? Ending fast or slow? The pictures are the ones on these slides.
**Go to:** Deck 15 Animation principles, slide 5, "Easing from first principles" · Deck 15 Animation principles, slide 6, "Timing, spacing, frame rate and speed scale"

### 20. Principles of animation, as heuristics
**Know:** Each principle is a rule of thumb with a reason. Know why you would use each one on the slides: pose, silhouette, weight; anticipation, squash and stretch, arcs; follow-through, overlap, secondary motion; plus easing and timing (topic 19).
**Go to:** Deck 15 Animation principles, slide 8, "Pose, silhouette and weight" · Deck 15 Animation principles, slide 9, "Anticipation, squash and stretch, arcs" · Deck 15 Animation principles, slide 10, "Follow-through, overlap and secondary motion"

### 21. Cycles
**Know:** A move that starts and ends on the same pose can be made into a cycle (a loop), such as a walk or an idle. Games use cycles to play a move for as long as needed.
**Go to:** Deck 15 Animation principles, slide 7, "Loop, loop seam and cycle"

### 22. FK, IK and retargeting (very general)
**Know:** Only what each is and why you would add it, not the maths. FK (forward kinematics): you rotate each joint from the root outward, for full control of a swing. IK (inverse kinematics): you place the end (the hand) and the joints above it follow, for reaching, grabbing or planting feet. Retargeting: reusing one character's animation on a different skeleton.
**Go to:** Deck 15 Animation principles, slide 12, "FK, IK and retargeting"

### 23. State machines (picture question)
**Know:** A state machine lists a character's states (for example idle, walk, run, jump) and the transitions (arrows) allowed between them. If there is no arrow between two states, the character cannot go straight from one to the other; it has to pass through states that are connected.
**Picture question:** a simple idle / walk / run / jump state machine. Can this transition happen? What states does the character pass through to get from walk to jump?
**Go to:** Deck 15 Animation principles, slide 13, "Root motion, blend tree and state machine"

## Part 6. Camera

### 24. Camera moves and views
**Know:**
- **Pan, tilt, roll**: the camera turns left-right, up-down, or around its own view line. Moves have names, and when you name one precisely, the AI does exactly that move. (Critical.)
- **Shot sizes**: close-up, medium shot, full-body shot.
- **Orthographic vs perspective**: in perspective, far things look smaller; in orthographic, size does not change with distance.
- **First person vs third person**: the camera is the character's eyes, or the camera sees the character from outside.
**Go to:** Deck 18 Camera, slide 3, "Turn and move" · Deck 18 Camera, slide 4, "Pan, tilt, roll" · Deck 18 Camera, slide 11, "Perspective and orthographic" · Deck 18 Camera, slide 18, "Say it exactly"

---

## Not on this exam (watch the films; they still matter)
- The Godot shading language, GDScript, or any code
- PBR details, including roughness and metallic maps, technical parameters and implementation workflows; the PBR-based No-Bake system. Only the general definition and importance of PBR in topic 14 are in scope.
- Particle trails, paths, sub-emitters and the other particle settings
- Deck 16 Animation foundations and deck 17 Animation and interaction (blend trees, tweens, tracks and so on)
- The rest of the camera deck: dolly, truck, pedestal, orbit, zoom and lens, parallax, follow cameras, screen shake, limits
- Game AI (decks 19 and 20), not yet covered in lecture
- Decks 21 to 25: walkthrough film, game trailer, and Unity and Unreal
