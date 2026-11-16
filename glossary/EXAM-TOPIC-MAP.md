# CSYE 7270 exam: topics, and where to review each one

**What this is.** The 20 topics of the Fall 2026 exam (one question each, 20 multiple-answer questions, 100 points), and for each topic: the chapter sections on GitHub, the terminology-deck slides, and the course videos that cover it. Use it when you get a question wrong, or to plan what to study. Chapter 15 (the final project) is not on the exam, and the exam is about Godot only: no Unity, no Unreal, no code.

**How to open the slides.** The decks are HTML files in the course repository. Open the deck's link, choose "Download raw file", and open the downloaded file in a web browser. Arrow keys step through each slide's animation; press G for a grid of all slides. The slide number is the number shown on screen.

**About the videos.** Only public videos on the course channel are listed. They were matched to topics by their titles and the assignment they belong to; a video may cover more than the topic. Where a topic has no video, it says so. The Key Terms films (one per deck) will be added here when they are published.

Course repository: https://github.com/nikbearbrown/csye-7270-building-virtual-environments  
Practice exams and keys: https://github.com/nikbearbrown/csye-7270-building-virtual-environments/tree/main/fall-2026-exam

---

## 1. Chapter 0: Checking an agent's report against evidence

**Read (GitHub):**
- [Chapter 0, "The evidence ladder"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#the-evidence-ladder)
- [Chapter 0, "The headless test: a script that plays the game"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#the-headless-test-a-script-that-plays-the-game)

**Slides:**
- [04 Walker and the toolchain, slide 10: The evidence ladder](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [04 Walker and the toolchain, slide 5: Exit code, hang and timeout](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [04 Walker and the toolchain, slide 14: Before you trust an agent’s change](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)

**Watch:**
- [Build a Godot Platformer Without Breaking Its Rules (Assignment 1)](https://youtu.be/QRmpyWPyphA)
- [Building Clawd: Code to Gameplay, One Change at a Time](https://youtu.be/azoGEpdrcqo)

## 2. Chapter 0: Working safely with an agent (instruction files, permissions, headless runs)

**Read (GitHub):**
- [Chapter 0, "Instruction files: how the agent learns your project"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#instruction-files-how-the-agent-learns-your-project)
- [Chapter 0, "Permissions and sandboxes: what the agent may touch"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#permissions-and-sandboxes-what-the-agent-may-touch)
- [Chapter 0, "Godot is also a command-line program"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#godot-is-also-a-command-line-program)
- [Chapter 0, "Why an agent can work on a Godot project at all: it is all text"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#why-an-agent-can-work-on-a-godot-project-at-all-it-is-all-text)

**Slides:**
- [04 Walker and the toolchain, slide 8: Instruction files and checkable instructions](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [04 Walker and the toolchain, slide 7: Permissions and sandbox](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [04 Walker and the toolchain, slide 4: Command line, flags and headless](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [04 Walker and the toolchain, slide 11: Text scenes, binary scenes, regression tests](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)

**Watch:**
- [Godot on Mac: Your First Walker Project with Claude Code](https://youtu.be/uB9lPI6ClU4)

## 3. Chapter 1: Walker, Godot projects and how a game updates

**Read (GitHub):**
- [Chapter 1, "Walker is a method and a set of files, not a program you run"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md#walker-is-a-method-and-a-set-of-files-not-a-program-you-run)
- [Chapter 1, "The project: a text file and a virtual file system"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md#the-project-a-text-file-and-a-virtual-file-system)
- [Chapter 1, "Scripts and the two clocks"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md#scripts-and-the-two-clocks)
- [Chapter 1, "Input: actions, not keys"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md#input-actions-not-keys)
- [Chapter 0, "The time trap: frames are not seconds"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/00-the-toolchain.md#the-time-trap-frames-are-not-seconds)

**Slides:**
- [04 Walker and the toolchain, slide 3: The Walker loop and git](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [04 Walker and the toolchain, slide 9: Frames are not seconds](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [05 Godot editor and scenes, slide 5: Project, scene, node and script](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 8: The two clocks](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 9: Input actions and just-pressed](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)

**Watch:**
- [Godot on Mac: Your First Walker Project with Claude Code](https://youtu.be/uB9lPI6ClU4)
- [Clawd in Walker Jumpman: First Playthrough](https://youtu.be/0yXF1BMiokc)
- [Building Clawd: Code to Gameplay, One Change at a Time](https://youtu.be/azoGEpdrcqo)

## 4. Chapter 2: Game art and sound (pixel art, asset requests, loops)

**Read (GitHub):**
- [Chapter 2, "1. A prompt is a specification, and the engine reads the result"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/02-prompting-game-art.md#1-a-prompt-is-a-specification-and-the-engine-reads-the-result)
- [Chapter 2, "2. Provenance is part of the asset"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/02-prompting-game-art.md#2-provenance-is-part-of-the-asset)
- [Chapter 2, "4. Texture settings that decide whether a sprite survives"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/02-prompting-game-art.md#4-texture-settings-that-decide-whether-a-sprite-survives)
- [Chapter 2, "5. Frames: SpriteFrames and AnimatedSprite2D"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/02-prompting-game-art.md#5-frames-spriteframes-and-animatedsprite2d)
- [Chapter 2, "7. Sound: import, loop, trigger"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/02-prompting-game-art.md#7-sound-import-loop-trigger)

**Slides:**
- [06 2D art and sound assets, slide 3: Resolution, viewport and aspect ratio](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 4: Texels, nearest and linear, integer scaling](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 5: Sprite sheets, atlases and frame rate](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 6: Alpha, transparent backgrounds, PNG and JPEG, fringe](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 7: Import settings, lossy copies and mipmaps](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 11: WAV and Ogg, loop point, one-shot](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [07 Art principles and concept art, slide 10: Iconic elements, proxy and readability](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/07%20Art%20principles%20and%20concept%20art.html)

**Watch:**
- [AI Game Assets That Work Together: Art, Sound and Music (Assignment 2)](https://youtu.be/rQlO6oZsi5k)
- [Building Clawd: Code to Gameplay, One Change at a Time](https://youtu.be/azoGEpdrcqo)

## 5. Chapter 3: 3D assets from Blender to Godot

**Read (GitHub):**
- [Chapter 3, "2. Units: a metre is a metre, until it is not"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md#2-units-a-metre-is-a-metre-until-it-is-not)
- [Chapter 3, "3. Axes: Blender is Z-up; glTF and Godot are Y-up"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md#3-axes-blender-is-z-up-gltf-and-godot-are-y-up)
- [Chapter 3, "4. Apply transforms: the object's scale versus the mesh's size"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md#4-apply-transforms-the-objects-scale-versus-the-meshs-size)
- [Chapter 3, "5. glTF is the interchange format"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md#5-gltf-is-the-interchange-format)
- [Chapter 3, "7. Collision decided at import time"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md#7-collision-decided-at-import-time)

**Slides:**
- [08 Blender interface and modeling, slide 6: Mesh, vertex, edge and face](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/08%20Blender%20interface%20and%20modeling.html)
- [08 Blender interface and modeling, slide 9: Transform, origin and pivot](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/08%20Blender%20interface%20and%20modeling.html)
- [08 Blender interface and modeling, slide 10: Apply transforms, local and global space](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/08%20Blender%20interface%20and%20modeling.html)
- [08 Blender interface and modeling, slide 11: Units and the right-handed +Z up axes](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/08%20Blender%20interface%20and%20modeling.html)
- [09 Blender to Godot, slide 5: Units, up axis and axis conversion](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)
- [09 Blender to Godot, slide 6: Apply transforms, node scale and origin](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)
- [09 Blender to Godot, slide 8: glTF, GLB, materials and the import file](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)
- [09 Blender to Godot, slide 9: Name suffixes, collision shapes, convex and concave](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)
- [09 Blender to Godot, slide 10: Triangle budget, sculpt to low-poly, baking and LOD](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)

**Watch:**
- [Your First 3D Game Assets with Claude and Blender](https://youtu.be/i-2NlEHaGjI)
- [Build a Planet Express Spaceship from Images (Blender learning guide)](https://youtu.be/rPPjGZjVt3I)

## 6. Chapter 3: Driving Blender with an agent (MCP and scripts)

**Read (GitHub):**
- [Chapter 3, "1. Two ways for an agent to drive Blender"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/03-blender-mcp-to-godot.md#1-two-ways-for-an-agent-to-drive-blender)

**Slides:**
- [09 Blender to Godot, slide 3: MCP: an agent calls a tool inside Blender](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)
- [09 Blender to Godot, slide 4: bpy scripts, headless Blender and the exit code](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)
- [09 Blender to Godot, slide 11: Script as source, version control and naming](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/09%20Blender%20to%20Godot.html)

**Watch:**
- [Building the Claude Mascot with Claude Code and the Blender MCP](https://youtu.be/t9N0a1Uz1Tk)
- [Your First 3D Game Assets with Claude and Blender](https://youtu.be/i-2NlEHaGjI)

## 7. Chapter 4: Nodes, scenes, signals and groups

**Read (GitHub):**
- [Chapter 4, "Nodes and scenes: composition you can save"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#nodes-and-scenes-composition-you-can-save)
- [Chapter 4, "The scene tree: what is actually running"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#the-scene-tree-what-is-actually-running)
- [Chapter 4, "Signals: who tells whom"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#signals-who-tells-whom)
- [Chapter 4, "Groups: tags you can call"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#groups-tags-you-can-call)
- [Chapter 4, "Autoloads: nodes that outlive scenes"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#autoloads-nodes-that-outlive-scenes)

**Slides:**
- [05 Godot editor and scenes, slide 5: Project, scene, node and script](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 6: The scene tree and instances](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 7: Polling, event-driven and signals](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 13: Group, autoload, resource and export](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 3: The docks: Scene, FileSystem, Inspector, Node](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)

**Watch:**
- No course video covers this topic yet. Use the chapter and the slides.

## 8. Chapter 4: Collision (colliders, trigger areas, layers and masks)

**Read (GitHub):**
- [Chapter 4, "Four collision objects, and one way around them"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#four-collision-objects-and-one-way-around-them)
- [Chapter 4, "Layers and masks: who can notice whom"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#layers-and-masks-who-can-notice-whom)
- [Chapter 4, "The art is not the collider"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/04-scenes-collision-and-physics.md#the-art-is-not-the-collider)
- [Chapter 1, "Areas are snapshots, and snapshots go stale"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/01-walker-and-godot.md#areas-are-snapshots-and-snapshots-go-stale)

**Slides:**
- [05 Godot editor and scenes, slide 10: The four collision objects](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 11: Layers, masks and the bitmask](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [05 Godot editor and scenes, slide 12: Collision shape and area snapshot](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/05%20Godot%20editor%20and%20scenes.html)
- [06 2D art and sound assets, slide 9: The collider is not the art](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)

**Watch:**
- No course video covers this topic yet. Use the chapter and the slides.

## 9. Chapter 5: Game design documents and requirements

**Read (GitHub):**
- [Chapter 5, "What a GDD is for"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/05-the-gdd-and-virtual-worlds.md#what-a-gdd-is-for)
- [Chapter 5, "Where Zelda came from"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/05-the-gdd-and-virtual-worlds.md#where-zelda-came-from)
- [Chapter 5, "Gates, and who signs them"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/05-the-gdd-and-virtual-worlds.md#gates-and-who-signs-them)
- [Chapter 5, "Provenance tags"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/05-the-gdd-and-virtual-worlds.md#provenance-tags)
- [Chapter 5, "Acceptance criteria that a machine can check"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/05-the-gdd-and-virtual-worlds.md#acceptance-criteria-that-a-machine-can-check)

**Slides:**
- [10 Game design document, slide 3: GDD, game brief and pitch](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/10%20Game%20design%20document.html)
- [10 Game design document, slide 5: The sixteen sections](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/10%20Game%20design%20document.html)
- [10 Game design document, slide 6: Goal to mechanic to test](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/10%20Game%20design%20document.html)
- [10 Game design document, slide 7: Four tags for every claim](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/10%20Game%20design%20document.html)
- [10 Game design document, slide 12: Acceptance criterion, given-when-then, tolerance](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/10%20Game%20design%20document.html)
- [10 Game design document, slide 13: Direct write, invariants, false passes](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/10%20Game%20design%20document.html)
- [01 Game design A, slide 5: Mechanic, player verb, core mechanic, core loop](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/01%20Game%20design%20A.html)
- [03 Game design C, slide 3: Three pillars](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/03%20Game%20design%20C.html)

**Watch:**
- [Write a Game Design Document You Can Check (Assignment 4)](https://youtu.be/AL24eYI1Mi4)
- [Godot GDD Skill: Explain Your Game Design Document](https://youtu.be/_nYqYmafYQw)

## 10. Chapter 6: Shaders

**Read (GitHub):**
- [Chapter 6, "A shader is a small program the GPU runs many times at once"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/06-shader-foundations.md#a-shader-is-a-small-program-the-gpu-runs-many-times-at-once)
- [Chapter 6, "Shader types and processor functions"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/06-shader-foundations.md#shader-types-and-processor-functions)
- [Chapter 6, "Inside a canvas_item shader"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/06-shader-foundations.md#inside-a-canvas_item-shader)
- [Chapter 6, "Uniforms and hints: the contract with GDScript"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/06-shader-foundations.md#uniforms-and-hints-the-contract-with-gdscript)
- [Chapter 6, "Specifying a visible effect before any code exists"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/06-shader-foundations.md#specifying-a-visible-effect-before-any-code-exists)

**Slides:**
- [11 Shader foundations, slide 3: Shader, vertex shader, fragment shader](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)
- [11 Shader foundations, slide 4: The pipeline: two stages you write, two built in](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)
- [11 Shader foundations, slide 5: Fragment, varying, interpolation](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)
- [11 Shader foundations, slide 6: shader_type, canvas_item, spatial](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)
- [11 Shader foundations, slide 8: UV and SCREEN_UV](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)
- [11 Shader foundations, slide 10: Uniform, hint_range, source_color](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)

**Watch:**
- [Godot Shaders](https://youtu.be/kSq45Gsqo8I)
- [Godot Shader Language](https://youtu.be/g0vgKR9Ac7Q)
- [Vertex Shaders](https://youtu.be/4CPj6-aKqgQ)
- [Shaders in 3D](https://youtu.be/m63zZdLMx_Y)
- [Godot Shaders and Materials: Test What You Can Explain (Assignment 5)](https://youtu.be/LwerxU2dmiM)

## 11. Chapter 7: Materials (material, shader, texture)

**Read (GitHub):**
- [Chapter 7, "A PBR material is a set of measurements, not a picture"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/07-materials-and-textures.md#a-pbr-material-is-a-set-of-measurements-not-a-picture)
- [Chapter 7, "StandardMaterial3D, ORMMaterial3D, ShaderMaterial"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/07-materials-and-textures.md#standardmaterial3d-ormmaterial3d-shadermaterial)
- [Chapter 7, "Lighting and global illumination decide what a material can show"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/07-materials-and-textures.md#lighting-and-global-illumination-decide-what-a-material-can-show)

**Slides:**
- [12 Materials and textures, slide 3: Material, PBR and lighting](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 4: Albedo, roughness and metallic](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 7: Ambient occlusion, emission and SSAO](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 8: ORM, channel packing and slot naming](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 13: Baked lighting, global illumination, probes](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [11 Shader foundations, slide 11: Material, ShaderMaterial, set_shader_parameter](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)

**Watch:**
- [Godot Shaders and Materials: Test What You Can Explain (Assignment 5)](https://youtu.be/LwerxU2dmiM)
- [Shaders in 3D](https://youtu.be/m63zZdLMx_Y)
- [Light Shaders](https://youtu.be/uzRymj7oe60)

## 12. Chapter 7: Textures (colour, data and normal maps)

**Read (GitHub):**
- [Chapter 7, "Colour versus data: why the decode matters"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/07-materials-and-textures.md#colour-versus-data-why-the-decode-matters)
- [Chapter 7, "Texture import: the half an agent forgets"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/07-materials-and-textures.md#texture-import-the-half-an-agent-forgets)

**Slides:**
- [12 Materials and textures, slide 5: Colour or data: sRGB and the decode trap](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 6: Normal map, tangent space, green channel](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 10: UV, unwrapping and baking](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 11: Resolution, texel density and UV scale](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [12 Materials and textures, slide 12: Tiling, wrap mode and mipmaps](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/12%20Materials%20and%20textures.html)
- [11 Shader foundations, slide 12: RGBA, linear and sRGB](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/11%20Shader%20foundations.html)
- [08 Blender interface and modeling, slide 13: UV maps, unwrapping, materials and textures](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/08%20Blender%20interface%20and%20modeling.html)

**Watch:**
- [Godot Shaders and Materials: Test What You Can Explain (Assignment 5)](https://youtu.be/LwerxU2dmiM)

## 13. Chapter 8: Checking a shader

**Read (GitHub):**
- [Chapter 8, "The ladder of evidence for a shader change"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/08-shader-verification.md#the-ladder-of-evidence-for-a-shader-change)
- [Chapter 8, "Five families of plausible-but-incorrect change, and the input that exposes each"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/08-shader-verification.md#five-families-of-plausible-but-incorrect-change-and-the-input-that-exposes-each)
- [Chapter 8, "Controlled inputs in a headless Godot run"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/08-shader-verification.md#controlled-inputs-in-a-headless-godot-run)
- [Chapter 8, "Test the spec, not the implementation, and then test the test"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/08-shader-verification.md#test-the-spec-not-the-implementation-and-then-test-the-test)
- [Chapter 8, "Compute shaders: compiled is not run"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/08-shader-verification.md#compute-shaders-compiled-is-not-run)

**Slides:**
- [13 Shader verification, slide 3: The ladder: which rung is the claim on?](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)
- [13 Shader verification, slide 4: Headless shows values, not how it looks](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)
- [13 Shader verification, slide 5: Controlled inputs, the bench and its fixture](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)
- [13 Shader verification, slide 6: Pin the clock and the seed](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)
- [13 Shader verification, slide 7: Colour or data: the decode changes the number](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)
- [13 Shader verification, slide 9: Loose or tight: false passes and false fails](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)
- [13 Shader verification, slide 11: Break it on purpose, test the test, check the diff](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/13%20Shader%20verification.html)

**Watch:**
- [Godot Shaders and Materials: Test What You Can Explain (Assignment 5)](https://youtu.be/LwerxU2dmiM)

## 14. Chapter 9: Particle effects

**Read (GitHub):**
- [Chapter 9, "A particle system is a birth–life–death loop, not a picture"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/09-particle-effects.md#a-particle-system-is-a-birthlifedeath-loop-not-a-picture)
- [Chapter 9, "Four node types, two families"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/09-particle-effects.md#four-node-types-two-families)
- [Chapter 9, "The timing model: one emission cycle"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/09-particle-effects.md#the-timing-model-one-emission-cycle)
- [Chapter 9, "Triggering: a particle node is a node"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/09-particle-effects.md#triggering-a-particle-node-is-a-node)
- [Chapter 9, "Where particle cost lands"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/09-particle-effects.md#where-particle-cost-lands)

**Slides:**
- [14 Particles and VFX, slide 3: Particle, emitter and particle system](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 4: Amount, lifetime and steady state](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 5: Explosiveness, one_shot and preprocess](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 6: Emission shape, velocity, spread and seed](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 9: Local space, update rate and bounds](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 10: GPU nodes, CPU nodes and the process material](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 12: Reads and restraint](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)

**Watch:**
- [Godot Particle Effects That Communicate Game State (Assignment 6)](https://youtu.be/JDASKj6yKhU)

## 15. Chapter 10: Animation foundations (sprite sheets, rigs, keyframes, inverse kinematics)

**Read (GitHub):**
- [Chapter 10, "An animation is data bound to node paths"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/10-animation-foundations.md#an-animation-is-data-bound-to-node-paths)
- [Chapter 10, "Between keys: interpolation, easing, update mode"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/10-animation-foundations.md#between-keys-interpolation-easing-update-mode)
- [Chapter 10, "Tween or AnimationPlayer"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/10-animation-foundations.md#tween-or-animationplayer)
- [Chapter 10, "Frames, sprite sheets and cycles"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/10-animation-foundations.md#frames-sprite-sheets-and-cycles)
- [Chapter 10, "Skeletons and IK"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/10-animation-foundations.md#skeletons-and-ik)

**Slides:**
- [16 Animation foundations, slide 3: Clips, players and libraries](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/16%20Animation%20foundations.html)
- [16 Animation foundations, slide 4: Tracks, keys and the playhead](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/16%20Animation%20foundations.html)
- [16 Animation foundations, slide 8: Tween, easing, transition type and kill](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/16%20Animation%20foundations.html)
- [16 Animation foundations, slide 9: Skeleton, rest pose and inverse kinematics](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/16%20Animation%20foundations.html)
- [15 Animation principles, slide 3: Keys, in-betweens, clips and tweens](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/15%20Animation%20principles.html)
- [15 Animation principles, slide 4: Linear, step and cubic](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/15%20Animation%20principles.html)
- [15 Animation principles, slide 11: Rig, rest pose and skinning weights](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/15%20Animation%20principles.html)
- [15 Animation principles, slide 12: FK, IK and retargeting](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/15%20Animation%20principles.html)
- [06 2D art and sound assets, slide 5: Sprite sheets, atlases and frame rate](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)

**Watch:**
- [Godot Animation: Inspect Keys, Timing and Interruptions (Assignment 7)](https://youtu.be/DT2W6HsLY3s)

## 16. Chapter 11: State machines and blending

**Read (GitHub):**
- [Chapter 11, "AnimationTree plays an AnimationPlayer's clips through a graph"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/11-animation-and-interaction.md#animationtree-plays-an-animationplayers-clips-through-a-graph)
- [Chapter 11, "The blend-tree nodes you will use"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/11-animation-and-interaction.md#the-blend-tree-nodes-you-will-use)
- [Chapter 11, "BlendSpace: continuous input, continuous pose"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/11-animation-and-interaction.md#blendspace-continuous-input-continuous-pose)
- [Chapter 11, "The state machine, as machinery"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/11-animation-and-interaction.md#the-state-machine-as-machinery)
- [Chapter 11, "Root motion"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/11-animation-and-interaction.md#root-motion)

**Slides:**
- [17 Animation and interaction, slide 3: Clips, loops, one-shots and the tree](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/17%20Animation%20and%20interaction.html)
- [17 Animation and interaction, slide 4: Blend tree, blend space and parameters](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/17%20Animation%20and%20interaction.html)
- [17 Animation and interaction, slide 5: State, transition, condition and advance mode](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/17%20Animation%20and%20interaction.html)
- [17 Animation and interaction, slide 6: Travel, priority, interrupt and exit-time](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/17%20Animation%20and%20interaction.html)
- [17 Animation and interaction, slide 7: Cross-fade, transition time and the current node](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/17%20Animation%20and%20interaction.html)
- [15 Animation principles, slide 13: Root motion, blend tree and state machine](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/15%20Animation%20principles.html)

**Watch:**
- [Godot Animation: Inspect Keys, Timing and Interruptions (Assignment 7)](https://youtu.be/DT2W6HsLY3s)

## 17. Chapter 12: Audio and triggers

**Read (GitHub):**
- [Chapter 12, "Three player nodes, one question: where is the listener?"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/12-audio-and-triggers.md#three-player-nodes-one-question-where-is-the-listener)
- [Chapter 12, "Buses: where levels live"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/12-audio-and-triggers.md#buses-where-levels-live)
- [Chapter 12, "Polyphony, restart and pause: the lifecycle of one player"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/12-audio-and-triggers.md#polyphony-restart-and-pause-the-lifecycle-of-one-player)
- [Chapter 12, "Triggers: signals decide when, not the audio system"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/12-audio-and-triggers.md#triggers-signals-decide-when-not-the-audio-system)
- [Chapter 12, "Audio time is not frame time"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/12-audio-and-triggers.md#audio-time-is-not-frame-time)

**Slides:**
- [06 2D art and sound assets, slide 10: PCM, sample rate, Nyquist limit and synthesis](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 11: WAV and Ogg, loop point, one-shot](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 12: AudioStreamPlayer and polyphony](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)
- [06 2D art and sound assets, slide 13: Buses, decibels, headroom and clipping](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/06%202D%20art%20and%20sound%20assets.html)

**Watch:**
- [AI Game Assets That Work Together: Art, Sound and Music (Assignment 2)](https://youtu.be/rQlO6oZsi5k)

## 18. Chapter 13: Profiling and optimization

**Read (GitHub):**
- [Chapter 13, "Frame time is the unit; frames per second is the headline"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/13-profiling-and-optimization.md#frame-time-is-the-unit-frames-per-second-is-the-headline)
- [Chapter 13, "Where a frame's time goes"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/13-profiling-and-optimization.md#where-a-frames-time-goes)
- [Chapter 13, "The Performance singleton, and what its numbers actually are"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/13-profiling-and-optimization.md#the-performance-singleton-and-what-its-numbers-actually-are)
- [Chapter 13, "Nodes, servers and MultiMesh"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/13-profiling-and-optimization.md#nodes-servers-and-multimesh)
- [Chapter 13, "Loading and threads: spikes that are not per-frame cost"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/13-profiling-and-optimization.md#loading-and-threads-spikes-that-are-not-per-frame-cost)

**Slides:**
- No deck covers profiling directly; these three slides are the nearest.
- [04 Walker and the toolchain, slide 9: Frames are not seconds](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/04%20Walker%20and%20the%20toolchain.html)
- [14 Particles and VFX, slide 9: Local space, update rate and bounds](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)
- [14 Particles and VFX, slide 10: GPU nodes, CPU nodes and the process material](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/14%20Particles%20and%20VFX.html)

**Watch:**
- No course video covers this topic yet. Use the chapter and the slides.

## 19. Chapter 14: How game characters decide (state machines, behavior trees)

**Read (GitHub):**
- [Chapter 14, "The tick: where decisions run"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/14-game-ai-and-systems.md#the-tick-where-decisions-run)
- [Chapter 14, "Finite state machines, as this project builds them"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/14-game-ai-and-systems.md#finite-state-machines-as-this-project-builds-them)
- [Chapter 14, "Behavior trees: priority, re-evaluated or remembered"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/14-game-ai-and-systems.md#behavior-trees-priority-re-evaluated-or-remembered)

**Slides:**
- [20 Game AI decisions and systems, slide 3: State machines, and how to stop flicker](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/20%20Game%20AI%20decisions%20and%20systems.html)
- [20 Game AI decisions and systems, slide 4: Behavior trees: tick, results and the blackboard](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/20%20Game%20AI%20decisions%20and%20systems.html)
- [20 Game AI decisions and systems, slide 5: Conditions, actions, selectors and sequences](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/20%20Game%20AI%20decisions%20and%20systems.html)
- [19 Game AI perception and pathfinding, slide 3: Agent, loop, hearing and memory](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/19%20Game%20AI%20perception%20and%20pathfinding.html)

**Watch:**
- [Teach Game-AI Verification with Three Runnable Exercises (Assignment 9)](https://youtu.be/aZPDNxR1ySs)

## 20. Chapter 14: Generating levels (seed, noise, checking)

**Read (GitHub):**
- [Chapter 14, "Procedural content generation: seeds, noise, and proof"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/14-game-ai-and-systems.md#procedural-content-generation-seeds-noise-and-proof)
- [Chapter 14, "Lab B: procedural content with a validator"](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/chapters/14-game-ai-and-systems.md#lab-b-procedural-content-with-a-validator)

**Slides:**
- [20 Game AI decisions and systems, slide 10: Seeds, noise and the same output twice](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/20%20Game%20AI%20decisions%20and%20systems.html)
- [20 Game AI decisions and systems, slide 11: Heightmaps: CPU loop and compute shader](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/20%20Game%20AI%20decisions%20and%20systems.html)
- [20 Game AI decisions and systems, slide 12: Validators, failure policy and the safety margin](https://github.com/nikbearbrown/csye-7270-building-virtual-environments/blob/main/glossary/decks/20%20Game%20AI%20decisions%20and%20systems.html)

**Watch:**
- [Teach Game-AI Verification with Three Runnable Exercises (Assignment 9)](https://youtu.be/aZPDNxR1ySs)

---

## Not on the exam

These decks are useful for the course but are not exam topics: 18 Camera, 21 Walkthrough film, 22 Game trailer, 23 Godot Unity Unreal comparison, 24 Unity editor interface, 25 Unreal editor interface, and Chapter 15 (final projects). Decks 01 to 03 (game design) appear above only where a slide teaches a term the GDD topic uses (core loop, pillars).

*Generated 2026-11-13 from the chapters on GitHub (main), the deck files and the channel's public videos. Every chapter section, slide number and video above was checked to exist when this file was written.*
