# Exam cheat sheet: everything that is fair game

**The exam:** 100 points, 20 multiple-answer questions, each with five statements (A to E) that you mark true or false one at a time. Paper, no laptop, no phone. You have the whole class period, 3:25 to 5:05 (100 minutes); most people will need about 60. Godot only: no Unity or Unreal. No code: you will not read or write GDScript or the Godot shading language.

**How to use this sheet**
1. Find the topic. "Know" says what you need, in plain words.
2. Open the slide after "Go to". It opens that deck at that slide; if the link only opens the file, press **G** for the slide grid. Slide numbers are the ones shown on screen.
3. Several questions are **picture questions**: you get a drawing (a curve, a rig, a state machine, an editor window) and decide what it shows. They are drawn the way the slides draw them, so study the pictures on the slides, not only the words.

**Anything not on this sheet is not on the exam.** This sheet replaces the earlier `EXAM-CHEAT-SHEET.md` (topics 1 to 14 below are that sheet, updated).

---

## Part 1. Working with an agent

### 1. Playtesting
**Know:** An agent can build the game, but only playing it tells you whether it is fun. With an agent, your time moves from writing code to playing and playtesting. A passing test is evidence about the game's state, not a playtest.
**Go to:** [04 Walker and the toolchain, slide 3](decks/04%20Walker%20and%20the%20toolchain.html#3) (playtest is a step in the Walker loop) · [04, slide 10, "The evidence ladder"](decks/04%20Walker%20and%20the%20toolchain.html#10) (rung 5: "you played it") · [01 Game design A, slide 10, "Prototype and play testing"](decks/01%20Game%20design%20A.html#10)

### 2. Directing an agent
**Know:** Be specific, not vague: a good instruction is one a check can pass or fail. Give context (instruction files) and references.
**Go to:** [04, slide 8, "Instruction files and checkable instructions"](decks/04%20Walker%20and%20the%20toolchain.html#8) · [01, slide 7, "Fun, target experience, appeal"](decks/01%20Game%20design%20A.html#7) · [07, slide 7, "Concept art, reference and mood boards"](decks/07%20Art%20principles%20and%20concept%20art.html#7) · every deck's "Say it exactly" slide, for example [12, slide 15](decks/12%20Materials%20and%20textures.html#15)

### 3. MCP
**Know:** MCP is a standard way for an AI app to call tools inside another program. Godot can be scripted directly (command line, headless, text scene files). Blender can be driven two ways: a Python (bpy) script run headless, or an MCP server with an add-on inside Blender. Editor-heavy tools are why an MCP matters.
**Go to:** [04, slide 4, "Command line, flags and headless"](decks/04%20Walker%20and%20the%20toolchain.html#4) · [04, slide 11, "Text scenes, binary scenes, regression tests"](decks/04%20Walker%20and%20the%20toolchain.html#11) · [09 Blender to Godot, slide 3, "MCP: an agent calls a tool inside Blender"](decks/09%20Blender%20to%20Godot.html#3) · [09, slide 4, "bpy scripts, headless Blender and the exit code"](decks/09%20Blender%20to%20Godot.html#4)

## Part 2. Tools and game design

### 4. The Godot editor interface (picture questions)
**Know:** Scene dock (the nodes; the Remote tab shows the running game), FileSystem dock (files under `res://`), Inspector (properties of the selected node), Node dock (its signals and groups). Along the top: 2D, 3D, Script. At the bottom: Output and Debugger. Run Project (F5) starts the main scene; Run Current Scene starts the open one.
**Go to:** [05 Godot editor and scenes, slide 3](decks/05%20Godot%20editor%20and%20scenes.html#3) · [05, slide 4](decks/05%20Godot%20editor%20and%20scenes.html#4)

### 5. The Blender interface (very basic)
**Know:** 3D viewport (see and edit the scene), Outliner (tree of objects and collections), Properties editor (settings for the selected thing), Timeline (frames and keyframes), Workspaces (saved layouts), Object Mode versus Edit Mode.
**Go to:** [08 Blender interface and modeling, slides 3](decks/08%20Blender%20interface%20and%20modeling.html#3), [4](decks/08%20Blender%20interface%20and%20modeling.html#4) and [5](decks/08%20Blender%20interface%20and%20modeling.html#5)

### 6. Normals
**Know:** A normal is the direction a surface faces, straight out from it. If normals are flipped, the surface faces the wrong way and can light wrongly or vanish from one side.
**Go to:** [08, slide 8, "Normals and flipped normals"](decks/08%20Blender%20interface%20and%20modeling.html#8) · [12 Materials and textures, slide 6, "Normal map"](decks/12%20Materials%20and%20textures.html#6) (first part only: a normal map stores surface directions in an image)

### 7. Game design documents and their sixteen sections
**Know:** A GDD says what the game is and how it plays, in enough detail to build and test it. The sixteen sections, in order: Metadata, Vision summary, Pillars, Core loop, PX goals, Mechanics, Systems, Progression, World, Narrative, Characters, Feature list, Out of scope, Technical requirements, Risks, Open questions.
**Go to:** [10 Game design document, slide 3](decks/10%20Game%20design%20document.html#3) · [10, slide 5, "The sixteen sections"](decks/10%20Game%20design%20document.html#5) · [10, slide 6, "Goal to mechanic to test"](decks/10%20Game%20design%20document.html#6) · core loop: [01, slide 5](decks/01%20Game%20design%20A.html#5) · pillars: [03 Game design C, slide 3](decks/03%20Game%20design%20C.html#3)

### 8. Concept art, character art, character sheet
**Know:** Concept art is early drawing that solves a design problem for the team; it is not finished art. Reference and mood boards support it. Character art covers iconic elements, a proxy model, readability, anatomy and the neutral pose.
**Go to:** [07 Art principles and concept art, slide 7](decks/07%20Art%20principles%20and%20concept%20art.html#7) · [07, slide 10](decks/07%20Art%20principles%20and%20concept%20art.html#10) · [07, slide 12](decks/07%20Art%20principles%20and%20concept%20art.html#12)

## Part 3. Art, colour and collision

### 9. Resolution, anti-aliasing and pixelation (pixel art)
**Know:** Resolution is width and height in pixels. For pixel art, Nearest filtering keeps hard edges (Linear blends and smooths), and whole-number scaling keeps every pixel the same width.
**Go to:** [06 2D art and sound assets, slide 3](decks/06%202D%20art%20and%20sound%20assets.html#3) · [06, slide 4](decks/06%202D%20art%20and%20sound%20assets.html#4)

### 10. RGB, alpha, albedo
**Know:** RGBA is four channels: red, green, blue and alpha (opacity). Albedo (base colour) is the colour a surface reflects before any lighting. Black is (0, 0, 0) and white is (1, 1, 1).
**Go to:** [11 Shader foundations, slide 12](decks/11%20Shader%20foundations.html#12) · [06, slide 6](decks/06%202D%20art%20and%20sound%20assets.html#6) · [12, slide 4](decks/12%20Materials%20and%20textures.html#4) (albedo only)

### 11. Tinting (multiplying a colour)
**Know:** Multiply all of a colour's channels by the same number and the ratios stay the same: the same colour, lighter or darker. Multiply the channels by different numbers and the ratios change: a different colour.
**Go to:** [11, slide 9](decks/11%20Shader%20foundations.html#9) · [12, slide 4](decks/12%20Materials%20and%20textures.html#4)

### 12. Colliders, collisions and triggers
**Know:** A collider (collision shape) is what physics treats as solid; it is separate from the art. Static, rigid and character bodies block; an area reports overlap and never blocks, so it is the trigger. Layers and masks say who can notice whom.
**Go to:** [05, slide 10](decks/05%20Godot%20editor%20and%20scenes.html#10) · [05, slide 11](decks/05%20Godot%20editor%20and%20scenes.html#11) · [05, slide 12](decks/05%20Godot%20editor%20and%20scenes.html#12) · [06, slide 9, "The collider is not the art"](decks/06%202D%20art%20and%20sound%20assets.html#9)

## Part 4. Shaders, materials and textures

### 13. Shaders: vertex and fragment (pixel)
**Know:**
- A shader is a small program the graphics processor runs many times at once.
- **Vertex shader:** maps 3D to 2D. Input: one vertex (a corner point of the model). Output: where that vertex lands on the 2D screen.
- **Fragment shader = pixel shader** (two names, one thing): maps 2D to 2D, pixel to pixel. Input: one screen position the shape covers, with values blended from the corners and any textures. Output: the colour of that one pixel.
- **Order:** the vertex shader comes first, then the fragment (pixel) shaders. The 3D-to-2D step happens once; there can be several fragment shaders.
**Go to:** [11 Shader foundations, slide 3](decks/11%20Shader%20foundations.html#3) · [11, slide 4, "The pipeline"](decks/11%20Shader%20foundations.html#4) · [11, slide 5](decks/11%20Shader%20foundations.html#5)

### 14. Materials, textures and PBR (general idea only)
**Know:** A texture is an image the game samples to colour (or describe) a surface. A material is what is applied to a surface: it holds the settings, and the textures, that a shader reads to draw it. A material is not a texture, and a texture alone is not a material.
**PBR, at a general level:** PBR means physically based rendering: an approach that models how light interacts with surfaces. It matters because materials respond consistently and believably when the lighting changes. Knowing what PBR is and why it matters is fair game. No detailed PBR knowledge or experience using a PBR-based No-Bake system is required.
**Go to:** [12 Materials and textures, slide 3](decks/12%20Materials%20and%20textures.html#3) · [06, slide 4, "Texels"](decks/06%202D%20art%20and%20sound%20assets.html#4)

### 15. UV and the UV map
**Know:** UV is a 2D coordinate that maps a surface to a texture, 0 to 1 across it. A UV map is the flat layout of a mesh used to place a texture. A surface position (UV) is not the same as a screen position: two shapes can share UV values but sit at different places on screen.
**Go to:** [11, slide 8](decks/11%20Shader%20foundations.html#8) · [08, slide 13](decks/08%20Blender%20interface%20and%20modeling.html#13) · [12, slide 10](decks/12%20Materials%20and%20textures.html#10)

### 16. Particles
**Know:** A particle is one small image or shape the system draws and moves for a short life. An emitter is where particles come from. A particle system is the whole thing: emitter, particles and the rules that move them. Godot has two kinds, GPU-based and CPU-based: the CPU kind is the safe choice for low-end devices; the GPU kind handles large numbers of particles and has more features.
**Go to:** [14 Particles and VFX, slide 3](decks/14%20Particles%20and%20VFX.html#3) · [14, slide 10](decks/14%20Particles%20and%20VFX.html#10)

## Part 5. Animation (deck 15 and the sprite slides)

### 17. Sprite-based and rig-based animation, skin and skin weights (critical)
**Know:**
- A **sprite sheet** is one image of many frames. **Sprite-based** (frame-by-frame) animation plays those frames in order at a frame rate.
- **Rig-based** animation moves a hierarchy of bones (the rig). The **skin** connects the mesh to the bones; **skin weights** set how much each bone moves each part of the 3D mesh.
- **Picture question:** you get a simple rigged character. Decide what it can and cannot move. A part with no bone cannot move on its own; a child bone follows its parent.
**Go to:** [06, slide 5, "Sprite sheets, atlases and frame rate"](decks/06%202D%20art%20and%20sound%20assets.html#5) · [15 Animation principles, slide 11, "Rig, rest pose and skinning weights"](decks/15%20Animation%20principles.html#11)

### 18. Keyframes and in-betweens
**Know:** A keyframe sets a value at a moment in time. In-betweens are the frames between keys that the computer fills in.
**Go to:** [15, slide 3, "Keys, in-betweens, clips and tweens"](decks/15%20Animation%20principles.html#3) · [15, slide 4, "Linear, step and cubic"](decks/15%20Animation%20principles.html#4)

### 19. Animation curves, timing and spacing (picture questions)
**Know:** A curve shows how a value changes between keys, so you can see where a move is fast and where it is slow. Ease-in starts slow; ease-out ends slow; ease-in-out does both. Timing is how long a move takes; spacing is how far it moves from frame to frame (close together = slow, far apart = fast).
**Picture questions:** a ball moving between two keyframes with its curve, or the ball's spacing. Is it starting fast or slow? Ending fast or slow? The pictures are the ones on these slides.
**Go to:** [15, slide 5, "Easing from first principles"](decks/15%20Animation%20principles.html#5) · [15, slide 6, "Timing, spacing, frame rate and speed scale"](decks/15%20Animation%20principles.html#6)

### 20. Principles of animation, as heuristics
**Know:** Each principle is a rule of thumb with a reason. Know why you would use each one on the slides: pose, silhouette, weight; anticipation, squash and stretch, arcs; follow-through, overlap, secondary motion; plus easing and timing (topic 19).
**Go to:** [15, slide 8](decks/15%20Animation%20principles.html#8) · [15, slide 9](decks/15%20Animation%20principles.html#9) · [15, slide 10](decks/15%20Animation%20principles.html#10)

### 21. Cycles
**Know:** A move that starts and ends on the same pose can be made into a cycle (a loop), such as a walk or an idle. Games use cycles to play a move for as long as needed.
**Go to:** [15, slide 7, "Loop, loop seam and cycle"](decks/15%20Animation%20principles.html#7)

### 22. FK, IK and retargeting (very general)
**Know:** Only what each is and why you would add it, not the maths. FK (forward kinematics): you rotate each joint from the root outward, for full control of a swing. IK (inverse kinematics): you place the end (the hand) and the joints above it follow, for reaching, grabbing or planting feet. Retargeting: reusing one character's animation on a different skeleton.
**Go to:** [15, slide 12, "FK, IK and retargeting"](decks/15%20Animation%20principles.html#12)

### 23. State machines (picture question)
**Know:** A state machine lists a character's states (for example idle, walk, run, jump) and the transitions (arrows) allowed between them. If there is no arrow between two states, the character cannot go straight from one to the other; it has to pass through states that are connected.
**Picture question:** a simple idle / walk / run / jump state machine. Can this transition happen? What states does the character pass through to get from walk to jump?
**Go to:** [15, slide 13, "Root motion, blend tree and state machine"](decks/15%20Animation%20principles.html#13)

## Part 6. Camera

### 24. Camera moves and views
**Know:**
- **Pan, tilt, roll**: the camera turns left-right, up-down, or around its own view line. Moves have names, and when you name one precisely, the AI does exactly that move. (Critical.)
- **Shot sizes**: close-up, medium shot, full-body shot.
- **Orthographic vs perspective**: in perspective, far things look smaller; in orthographic, size does not change with distance.
- **First person vs third person**: the camera is the character's eyes, or the camera sees the character from outside.
**Go to:** [18 Camera, slide 3, "Turn and move"](decks/18%20Camera.html#3) · [18, slide 4, "Pan, tilt, roll"](decks/18%20Camera.html#4) · [18, slide 11, "Perspective and orthographic"](decks/18%20Camera.html#11) · [18, slide 18, "Say it exactly"](decks/18%20Camera.html#18)

---

## Not on this exam (watch the films; they still matter)
- The Godot shading language, GDScript, or any code
- PBR details, including roughness and metallic maps, technical parameters and implementation workflows; the PBR-based No-Bake system. Only the general definition and importance of PBR in topic 14 are in scope.
- Particle trails, paths, sub-emitters and the other particle settings
- Deck 16 Animation foundations and deck 17 Animation and interaction (blend trees, tweens, tracks and so on)
- The rest of the camera deck: dolly, truck, pedestal, orbit, zoom and lens, parallax, follow cameras, screen shake, limits
- Game AI (decks 19 and 20), not yet covered in lecture
- Decks 21 to 25: walkthrough film, game trailer, and Unity and Unreal

---

## For Bear before students see this (delete this section after)
Built 2026-11-13 from the first-half sheet and today's walkthrough (`notes/EXAM-SCOPE-SECOND-HALF-2026-11-13.md`). These are my readings, not yet confirmed:
1. **No slide yet** for shot sizes or first vs third person (topic 24). Add two camera slides, or keep the plain definitions above?
2. **No slide** for five of the twelve principles (staging, straight-ahead vs pose-to-pose, exaggeration, solid drawing, appeal), so topic 20 lists only the ones the slides show.
3. **Shading-language names dropped:** the old topics used `COLOR`, `TEXTURE` and `SCREEN_UV`. Topics 11 and 15 keep the ideas without the names.
4. **PBR scope confirmed by Bear, 2026-11-15:** the general definition and importance of PBR are IN (topic 14). PBR details, roughness and metallic maps, and the PBR-based No-Bake system are OUT. Albedo stays IN.
5. **"Launchers and animations"** read as deck 17. Decks 21 and 22 (walkthrough film, trailer) are OUT because they fall under "etc." in "game AI, etc., has not been discussed in lecture yet".
6. **Phones:** topic 16 says the CPU kind suits low-end devices, not that phones lack a GPU (they have one).
7. **Not yet built:** the picture questions (curves, timing and spacing, rig, state machine), the principles question, and a check that forms A, B and C each ask sprite, rig and skin. The exam forms have not been changed.
