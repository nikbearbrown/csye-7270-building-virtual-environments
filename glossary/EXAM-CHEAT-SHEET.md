# Exam cheat sheet: where to find each exam topic

**How to use this sheet**
1. Find the topic the question is about. Each topic says what to know in one or two sentences.
2. Open the link after "Go to:". It opens that deck at that slide. If the link only opens the file, press **G** for the slide grid and find the slide number.
3. "Chapter" says where the course text explains it. "No slide yet" means no deck slide covers it; the nearest slide or chapter section is named instead.

Anything not listed here is not on the exam. Decks are in `decks/`. Slide numbers are 1-based, the same as the number shown on screen.

---

### 1. Playtesting
**Know:** An AI agent can build the game, but you cannot tell if it is fun unless you play it. With an agent, your time moves from low-level code to playing and playtesting. A passing test is state evidence, not a playtest.
**Go to:** No slide yet for the idea that the human playtest is yours. Nearest, in reading order:
- [04 Walker and the toolchain, slide 3, "The Walker loop and git"](decks/04%20Walker%20and%20the%20toolchain.html#3) (playtest is a step in the Walker loop)
- [04 Walker and the toolchain, slide 10, "The evidence ladder"](decks/04%20Walker%20and%20the%20toolchain.html#10) (rung 5: "you played it")
- [01 Game design A, slide 10, "Prototype and play testing"](decks/01%20Game%20design%20A.html#10) (what play testing is: players challenge the design)

**Chapter:** `chapters/00-the-toolchain.md`, "The evidence ladder" and the summary ("The playtest is still yours"). Also `01-walker-and-godot.md`, "What remains unverified".

### 2. Directing an agent
**Know:** Be specific, not vague: an instruction should be one a check can pass or fail. Give context (instruction files) and references.
**Go to:** No slide yet for giving context, images and references. Nearest:
- [04 Walker and the toolchain, slide 8, "Instruction files and checkable instructions"](decks/04%20Walker%20and%20the%20toolchain.html#8) ("make the ball faster" versus a number and a test)
- [01 Game design A, slide 7, "Fun, target experience, appeal"](decks/01%20Game%20design%20A.html#7) ("fun" is too vague; name the kind)
- [07 Art principles and concept art, slide 7, "Concept art, reference and mood boards"](decks/07%20Art%20principles%20and%20concept%20art.html#7) (references)
- Every deck has a "Say it exactly" slide (vague request to exact request); for example [12 Materials and textures, slide 15](decks/12%20Materials%20and%20textures.html#15).

**Chapter:** `chapters/02-prompting-game-art.md`, "1. A prompt is a specification, and the engine reads the result". Also `00-the-toolchain.md`, "Instruction files"; `06-shader-foundations.md`, "Specifying a visible effect before any code exists".

### 3. The Godot editor interface (picture questions)
**Know:** Scene dock (the nodes; Remote tab shows the running game), FileSystem dock (files under `res://`), Inspector (properties of the selected node), Node dock (its signals and groups). Along the top: 2D, 3D, Script. At the bottom: Output and Debugger. Run Project (F5) starts the main scene; Run Current Scene starts the open one.
**Go to:**
- [05 Godot editor and scenes, slide 3, "The docks: Scene, FileSystem, Inspector, Node"](decks/05%20Godot%20editor%20and%20scenes.html#3)
- [05 Godot editor and scenes, slide 4, "Views, Output, Debugger, Settings, Run"](decks/05%20Godot%20editor%20and%20scenes.html#4)

**Chapter:** `chapters/01-walker-and-godot.md`, "The project: a text file and a virtual file system" (Scene dock Remote tab). The FileSystem and Node docks are not defined in the chapters; the slide tags say so.

### 4. The Blender interface (very basic)
**Know:** 3D viewport (see and edit the scene), Outliner (tree of objects and collections), Properties editor (settings for the selected thing), Timeline (frames and keyframes), Workspaces (saved layouts), Object Mode versus Edit Mode.
**Go to:**
- [08 Blender interface and modeling, slide 3, "The Blender window: viewport, outliner, properties"](decks/08%20Blender%20interface%20and%20modeling.html#3)
- [08 Blender interface and modeling, slide 4, "Workspaces and the timeline"](decks/08%20Blender%20interface%20and%20modeling.html#4)
- [08 Blender interface and modeling, slide 5, "Object Mode, Edit Mode and collections"](decks/08%20Blender%20interface%20and%20modeling.html#5)

**Chapter:** none; `chapters/03-blender-mcp-to-godot.md` names only the 3D viewport (press N). The slides draw on the Blender manual.

### 5. Sprite sheets, sprite animation, skeleton animation, and how they differ
**Know:** A sprite sheet is one image of many frames; sprite (frame-by-frame) animation plays those frames in order at a frame rate. Skeleton (bone) animation moves a hierarchy of bones, and skinning weights make the mesh follow.
**Go to (read in this order):**
- [06 2D art and sound assets, slide 5, "Sprite sheets, atlases and frame rate"](decks/06%202D%20art%20and%20sound%20assets.html#5)
- [16 Animation foundations, slide 3, "Clips, players and libraries"](decks/16%20Animation%20foundations.html#3) (two ways to play a sprite sheet)
- [15 Animation principles, slide 7, "Loop, loop seam and cycle"](decks/15%20Animation%20principles.html#7) (frame cycles)
- [15 Animation principles, slide 11, "Rig, rest pose and skinning weights"](decks/15%20Animation%20principles.html#11)
- [16 Animation foundations, slide 9, "Skeleton, rest pose and inverse kinematics"](decks/16%20Animation%20foundations.html#9)

**No slide yet** that sets sprite-based and rig-based animation side by side; the five slides above cover the two halves.
**Chapter:** `chapters/10-animation-foundations.md`, "Frames, sprite sheets and cycles" and "Skeletons and IK". Also `02-prompting-game-art.md`, "5. Frames: SpriteFrames and AnimatedSprite2D".

### 6. Resolution, anti-aliasing and pixelation (pixel art)
**Know:** Resolution is width and height in pixels. For pixel art, Nearest filtering keeps hard edges (Linear blends and smooths), and whole-number scaling keeps every pixel the same width.
**Go to:**
- [06 2D art and sound assets, slide 3, "Resolution, viewport and aspect ratio"](decks/06%202D%20art%20and%20sound%20assets.html#3)
- [06 2D art and sound assets, slide 4, "Texels, nearest and linear, integer scaling"](decks/06%202D%20art%20and%20sound%20assets.html#4)

**No slide yet for anti-aliasing**: no deck defines it (Linear blending on slide 4 is the nearest idea). It is not defined in the chapters either; Chapter 13 only names a project called `walker-3d-antialiasing`.
**Chapter:** `chapters/02-prompting-game-art.md`, "4. Texture settings that decide whether a sprite survives".

### 7. RGB, alpha, albedo
**Know:** RGBA is four channels: red, green, blue, and alpha (opacity). Albedo (also base colour) is the colour the surface reflects before any lighting. Black is (0, 0, 0) and white is (1, 1, 1).
**Go to:**
- [11 Shader foundations, slide 12, "RGBA, linear and sRGB"](decks/11%20Shader%20foundations.html#12)
- [06 2D art and sound assets, slide 6, "Alpha, transparent backgrounds, PNG and JPEG, fringe"](decks/06%202D%20art%20and%20sound%20assets.html#6)
- [12 Materials and textures, slide 4, "Albedo, roughness and metallic"](decks/12%20Materials%20and%20textures.html#4)
- [12 Materials and textures, slide 3, "Material, PBR and lighting"](decks/12%20Materials%20and%20textures.html#3) (albedo versus the colour you see)

**No slide yet** states that black is (0, 0, 0) and white is (1, 1, 1); slide 12 above only has the 0 to 1 scale.
**Chapter:** `chapters/07-materials-and-textures.md`, "A PBR material is a set of measurements, not a picture".

### 8. Tinting (multiplying a colour)
**Know:** Multiply a colour by one number and the channel ratios stay the same (same colour, lighter or darker). Multiply the channels by different numbers and the ratios change (a different colour).
**Go to:** No slide yet states this rule. Nearest:
- [11 Shader foundations, slide 9, "Vertex colour, TEXTURE, COLOR, TIME"](decks/11%20Shader%20foundations.html#9) (COLOR is vertex colour times TEXTURE, multiplied channel by channel)
- [12 Materials and textures, slide 4, "Albedo, roughness and metallic"](decks/12%20Materials%20and%20textures.html#4) (a metal's colour is tinted by albedo)

**Chapter:** `chapters/06-shader-foundations.md`, "Inside a `canvas_item` shader" (the COLOR definition and the failure flash).

### 9. Colliders, collisions and triggers
**Know:** A collider (collision shape) is what physics treats as solid; it is separate from the art. Static, rigid and character bodies block; an Area2D reports overlap and never blocks, so it is the trigger. Layers and masks say who can notice whom.
**Go to (in order):**
- [05 Godot editor and scenes, slide 10, "The four collision objects"](decks/05%20Godot%20editor%20and%20scenes.html#10)
- [05 Godot editor and scenes, slide 11, "Layers, masks and the bitmask"](decks/05%20Godot%20editor%20and%20scenes.html#11)
- [05 Godot editor and scenes, slide 12, "Collision shape and area snapshot"](decks/05%20Godot%20editor%20and%20scenes.html#12)
- [06 2D art and sound assets, slide 9, "The collider is not the art"](decks/06%202D%20art%20and%20sound%20assets.html#9)
- [23 Godot Unity Unreal comparison, slide 8, "Input action, character body and trigger"](decks/23%20Godot%20Unity%20Unreal%20comparison.html#8) (trigger versus collider, in three engines)

**Chapter:** `chapters/04-scenes-collision-and-physics.md`, "Four collision objects, and one way around them" and "Layers and masks: who can notice whom". Also `01-walker-and-godot.md`, "Bodies, shapes, layers" and "Areas are snapshots, and snapshots go stale".

### 10. MCP
**Know:** MCP is a standard way for an AI app to call tools in another program. Godot is scripted directly (command line, headless, text scene files). Blender can be driven two ways: a Python (bpy) script run headless, or an MCP server with an add-on inside Blender. Editor-heavy tools (Unity, Unreal) are why an MCP matters.
**Go to:**
- [04 Walker and the toolchain, slide 4, "Command line, flags and headless"](decks/04%20Walker%20and%20the%20toolchain.html#4) and [slide 11, "Text scenes, binary scenes, regression tests"](decks/04%20Walker%20and%20the%20toolchain.html#11) (why Godot can be scripted directly)
- [09 Blender to Godot, slide 3, "MCP: an agent calls a tool inside Blender"](decks/09%20Blender%20to%20Godot.html#3) (the MCP route)
- [09 Blender to Godot, slide 4, "bpy scripts, headless Blender and the exit code"](decks/09%20Blender%20to%20Godot.html#4) (the script route; slide 3 sets the two side by side)

**No slide yet** for why an MCP matters for Unity and Unreal; decks 24 and 25 do not mention MCP. The text-versus-binary point on slide 11 above is the nearest. (Slide 25:8 covers why Unreal's `.umap` and `.uasset` cannot be diffed.)
**Chapter:** `chapters/03-blender-mcp-to-godot.md`, "1. Two ways for an agent to drive Blender" and "Compare the two routes (practice)". Also `00-the-toolchain.md`, "Godot is also a command-line program".

### 11. Game design documents and their sixteen sections
**Know:** A GDD says what the game is and how it plays in enough detail to build and test it. The sixteen sections, in order: Metadata, Vision summary, Pillars, Core loop, PX goals, Mechanics, Systems, Progression, World, Narrative, Characters, Feature list, Out of scope, Technical requirements, Risks, Open questions.
**Go to:**
- [10 Game design document, slide 3, "GDD, game brief and pitch"](decks/10%20Game%20design%20document.html#3)
- [10 Game design document, slide 5, "The sixteen sections"](decks/10%20Game%20design%20document.html#5)
- [10 Game design document, slide 6, "Goal to mechanic to test"](decks/10%20Game%20design%20document.html#6) (PX goal, mechanic and test linked by IDs)

**No slide yet** explains each section on its own; slide 5 lists them with the core loop and pillar defined. For core loop and mechanic: [01 Game design A, slide 5](decks/01%20Game%20design%20A.html#5). For pillars: [03 Game design C, slide 3](decks/03%20Game%20design%20C.html#3).
**Chapter:** `chapters/05-the-gdd-and-virtual-worlds.md`, "What a GDD is for" and "Where Zelda came from" (lists the sixteen sections).

### 12. Shaders
**Know:** A shader is a small program on the graphics processor, run many times at once. The vertex shader runs per vertex and sets positions; the fragment (pixel) shader runs per pixel and sets colour. The pipeline has two stages you write and two built in.
**Go to:**
- [11 Shader foundations, slide 3, "Shader, vertex shader, fragment shader"](decks/11%20Shader%20foundations.html#3)
- [11 Shader foundations, slide 4, "The pipeline: two stages you write, two built in"](decks/11%20Shader%20foundations.html#4)
- [11 Shader foundations, slide 5, "Fragment, varying, interpolation"](decks/11%20Shader%20foundations.html#5)

**No slide yet** says there can be several fragment shaders. Slide 3 shows the fragment shader running once per covered pixel.
**Chapter:** `chapters/06-shader-foundations.md`, "A shader is a small program the GPU runs many times at once" and "Shader types and processor functions".

### 13. UV and the UV map; UV versus SCREEN_UV
**Know:** UV is a 2D coordinate that maps a surface to a texture, 0 to 1 across it. A UV map is the flat layout of a mesh used to place a texture. SCREEN_UV is the screen position of the current fragment, 0 to 1; two quads can share UV values but not SCREEN_UV values.
**Go to:**
- [11 Shader foundations, slide 8, "UV and SCREEN_UV"](decks/11%20Shader%20foundations.html#8)
- [08 Blender interface and modeling, slide 13, "UV maps, unwrapping, materials and textures"](decks/08%20Blender%20interface%20and%20modeling.html#13)
- [12 Materials and textures, slide 10, "UV, unwrapping and baking"](decks/12%20Materials%20and%20textures.html#10)

**Chapter:** `chapters/06-shader-foundations.md`, "Inside a `canvas_item` shader".

### 14. Concept art, character art, character sheet (pending)
**Know:** Concept art is early drawing that solves a design problem for the team, not finished art. Reference and mood boards support it. Character art covers iconic elements, a proxy model, readability, anatomy and the neutral pose. **Pending: the course text does not yet define these**; the slides come from Riot's "So You Wanna Make Games??" series (episodes 2 and 3), tagged "video only".
**Go to:**
- [07 Art principles and concept art, slide 7, "Concept art, reference and mood boards"](decks/07%20Art%20principles%20and%20concept%20art.html#7)
- [07 Art principles and concept art, slide 10, "Iconic elements, proxy and readability"](decks/07%20Art%20principles%20and%20concept%20art.html#10)
- [07 Art principles and concept art, slide 12, "Anatomy and the neutral pose"](decks/07%20Art%20principles%20and%20concept%20art.html#12)

**No slide yet defines a character sheet.** The phrase appears once in `chapters/02-prompting-game-art.md` (a table row: "three to six hex values from your character sheet"), undefined.
**Chapter:** none yet.
