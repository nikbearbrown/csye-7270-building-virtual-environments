# CSYE 7270 terminology glossary

Every term in every deck in `decks/`, with its meaning and a tag: **in the book text** (the chapters use and explain it), **in the glossary** (a row in `interview-bank/.../GLOSSARY-jargon-midterm.md`), **editor or docs** (defined by the engine's editor or documentation), **outside source**, or **video only** (only from the course videos). Generated from the decks by `make_glossary.js`; edit the decks, not this file.

## Decks

| Deck | Slides | Terms |
|---|---|---|
| [2D art and sound assets in the engine](decks/Terms%20-%202D%20art%20and%20sound%20assets.html) | 16 | 34 |
| [Animation and interaction: state machines and blending](decks/Terms%20-%20Animation%20and%20interaction.html) | 16 | 34 |
| [Animation foundations](decks/Terms%20-%20Animation%20foundations.html) | 14 | 33 |
| [Animation: principles and character animation](decks/Terms%20-%20Animation%20principles.html) | 16 | 34 |
| [Art principles: concept art and character art](decks/Terms%20-%20Art%20principles%20and%20concept%20art.html) | 15 | 34 |
| [Blender: the interface and modeling terms](decks/Terms%20-%20Blender%20interface%20and%20modeling.html) | 16 | 30 |
| [Blender to Godot: MCP, export and measuring a prop](decks/Terms%20-%20Blender%20to%20Godot.html) | 14 | 30 |
| [Terms: Camera](decks/Terms%20-%20Camera.html) | 19 | 20 |
| [Game AI: decisions, generation and systems](decks/Terms%20-%20Game%20AI%20decisions%20and%20systems.html) | 16 | 33 |
| [Game AI: perception, movement and pathfinding](decks/Terms%20-%20Game%20AI%20movement%20and%20pathfinding.html) | 15 | 33 |
| [Game design A: what a game is](decks/Terms%20-%20Game%20design%20A.html) | 14 | 22 |
| [Game design B: choices and challenge](decks/Terms%20-%20Game%20design%20B.html) | 14 | 19 |
| [Game design C: pacing and guidance](decks/Terms%20-%20Game%20design%20C.html) | 15 | 19 |
| [The game design document](decks/Terms%20-%20Game%20design%20document.html) | 16 | 34 |
| [How to make a trailer for your game](decks/Terms%20-%20Game%20trailer.html) | 16 | 32 |
| [Godot, Unity and Unreal: the differences](decks/Terms%20-%20Godot%20Unity%20Unreal.html) | 16 | 34 |
| [Godot: the editor, scenes, nodes, signals and movement](decks/Terms%20-%20Godot%20editor%20and%20scenes.html) | 16 | 34 |
| [Materials and textures](decks/Terms%20-%20Materials%20and%20textures.html) | 16 | 34 |
| [Particles and VFX](decks/Terms%20-%20Particles%20and%20VFX.html) | 16 | 35 |
| [Shaders: foundations](decks/Terms%20-%20Shader%20foundations.html) | 16 | 33 |
| [Shader verification](decks/Terms%20-%20Shader%20verification.html) | 14 | 30 |
| [The Unity editor interface](decks/Terms%20-%20Unity%20editor.html) | 17 | 32 |
| [The Unreal Editor interface](decks/Terms%20-%20Unreal%20editor.html) | 16 | 32 |
| [Walker and the toolchain](decks/Terms%20-%20Walker%20and%20the%20toolchain.html) | 14 | 26 |
| [How to make a walkthrough film: important terms](decks/Terms%20-%20Walkthrough%20film.html) | 14 | 32 |

Total: 25 decks, 763 term entries.

---

## 2D art and sound assets in the engine

[Open the deck](decks/Terms%20-%202D%20art%20and%20sound%20assets.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Resolution | Width and height in pixels. | in the glossary |
| Viewport | The area the game draws into, set in Project Settings; the window scales it. | editor or docs |
| Aspect ratio | Width divided by height. | in the glossary |
| Uniform vs non-uniform | Same factor on both axes versus different factors that distort. | in the glossary |
| Texel | One pixel of a texture. | in the glossary |
| Nearest vs linear | Nearest reads one texel and keeps hard edges; linear blends four and smooths. | in the book text |
| Integer scaling | Scaling by whole numbers so pixel art stays crisp. | in the glossary |
| Sprite sheet | One image of many frames in a grid. | in the book text |
| Texture atlas | Many small images packed into one big texture; a frame is a region of it. | in the book text |
| SpriteFrames | A Godot resource of named animations: frames, speed and a loop flag. | in the book text |
| Frame rate | Frames shown per second. | in the book text |
| Alpha channel | The extra channel storing opacity. | in the glossary |
| Transparent background | Cut the background to alpha 0; ask for a solid colour, not for transparent. | in the book text |
| PNG vs JPEG | Lossless with alpha versus lossy without alpha. | in the book text |
| Fringe (halo) | The halo of edge colour left around a cutout; fix_alpha_border removes it. | in the book text |
| Import settings | Per-asset options controlling how the engine converts it, kept in the .import file. | in the book text |
| Lossless vs lossy | Exact reconstruction versus smaller files with lost detail. | in the glossary |
| Mipmaps | Pre-shrunk copies of a texture used when drawn small; about 33% more memory. | in the book text |
| Silhouette | The outline of an object; it should still read when filled black at game size. | in the book text |
| Readability | How well a character can be understood in the game's real view. | video only |
| Collider | Shape used for contact tests; separate from the art and sized from the body. | in the book text |
| PCM | Uncompressed digital audio samples. | in the glossary |
| Sample rate | Audio samples per second. | in the glossary |
| Nyquist limit | The highest frequency a sample rate can hold: half the rate. | in the glossary |
| Procedural synthesis | Sound made by a formula evaluated sample by sample, with no file and no model. | in the book text |
| WAV vs Ogg Vorbis | WAV for short effects; Ogg Vorbis for music, speech and long sounds. | in the book text |
| Loop point | Where a looping sound jumps back to; WAV has begin and end, Ogg only a start offset. | in the book text |
| One-shot | Plays once and stops. | in the glossary |
| AudioStreamPlayer | Godot node that plays sound with no position. | in the book text |
| Polyphony | How many copies of a sound can play at once; Godot's default is 1. | in the book text |
| Bus | A channel that sounds are routed through for shared volume and effects. | in the book text |
| Decibel | Logarithmic loudness unit. | in the glossary |
| Headroom | Spare level left below the maximum. | in the glossary |
| Clipping | Distortion when a signal exceeds the maximum level. | in the glossary |

## Animation and interaction: state machines and blending

[Open the deck](decks/Terms%20-%20Animation%20and%20interaction.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| AnimationPlayer | Godot node that plays clips. | in the book text |
| Loop | A clip that repeats. | in the book text |
| OneShot | A blend-tree node that plays a clip once over whatever is below it, then returns. | in the book text |
| Animation tree | Godot's graph of blends and state machines. | in the book text |
| State | One named mode of a state machine, such as idle or run. | in the book text |
| Transition | A connection from one state to another, with its own rule for when it fires and how long it blends. | in the book text |
| Condition | A test on a parameter that must hold for a transition. | in the book text |
| Advance mode | Enabled: only travel() uses the transition. Auto: it fires by itself when its condition or expression is true. | in the book text |
| Travel | Ask the machine to go to a state by the shortest path of transitions; with no path it jumps there. | in the book text |
| Priority | Which transition wins when several are true at once; in Godot the lower number is preferred. | in the book text |
| Interrupt | A transition that cuts off the current state early. | in the glossary |
| Exit-time transition (Godot: switch mode At End. Unity: Has Exit Time) | A transition that waits for the clip to reach a set point. | in the book text |
| Cross-fade (also transition time, xfade_time) | Blend smoothly from one clip to the next over a short time. | in the book text |
| get_current_node() | The playback's reading of the current state. During a cross-fade it already names the new state. | in the book text |
| Blend tree | A graph of nodes that mix clips by numbers your code writes. | in the book text |
| Blend space (BlendSpace1D, BlendSpace2D) | Clips placed on a line or a plane; a position between them mixes the nearest ones. | in the book text |
| Parameter | A tunable number on the tree, addressed by a path; code drives the tree by writing it. | in the book text |
| Property track | A track that animates any property, not just bones. | in the glossary |
| Method track (Unity: Animation Event. Unreal: Anim Notify) | A track that calls a function when the playhead reaches a key. | in the book text |
| Tween | Code-made animation of a value toward a target, then discarded; it can be killed halfway. | in the book text |
| Startup | The windup frames before an attack can hit. | in the glossary |
| Active | The frames in which an attack can hit. | in the glossary |
| Recovery | The frames after an attack before the character can act. | in the glossary |
| Hit list | The record of targets already hit so one swing hits each once. | in the glossary |
| Sampling | Reading a value at one moment, so brief events between samples can be missed. | in the book text |
| Intermittent fault | A bug that appears only sometimes. | in the glossary |
| Input probe | A script that loads the real scene, presses only ordinary actions and records what happens. | in the book text |
| Mutation check | Put the old broken version back and run the new test; it must fail. | in the book text |
| Animator Controller | Unity asset holding an animation state machine. | in the book text |
| Unity transition | Moves from one state to another over a set time. | in the book text |
| Unity blend tree | Mixes several clips by a parameter value. | in the book text |
| Animation Blueprint | Unreal asset holding an animation state machine and logic. | in the book text |
| Transition rule | A small graph that outputs true or false; true lets the state change. | in the book text |
| Conduit | A hub that joins many states to many with one set of transitions. | in the book text |

## Animation foundations

[Open the deck](decks/Terms%20-%20Animation%20foundations.html) · 14 slides · 33 terms

| Term | Meaning | Tag |
|---|---|---|
| Animation resource | Stored animation data: a length plus tracks of keys. It does nothing until a player plays it. | in the book text |
| AnimationPlayer | The node that plays animations by name. | in the book text |
| AnimationLibrary | A named collection of animations that a player holds. | in the book text |
| AnimatedSprite2D | A 2D node that plays a list of frames. Simpler than AnimationPlayer, which can key any property. | in the book text |
| Track | One property's keyframes inside a clip, bound to a node path. | in the book text |
| Key | One point on a track: a time, a value and an easing value. | in the book text |
| Playhead | The marker for the current time on the timeline. | in the glossary |
| Interpolation | How values are filled in between keys: nearest, linear or cubic. | in the book text |
| Value track | Sets a property, such as rotation_degrees, to a value at each time. | in the book text |
| Method track | Calls a function at chosen times. Does not fire when you scrub in the editor. | in the book text |
| Bezier track | Fills a value in between keys along a hand-shaped curve. | in the book text |
| Audio track | Plays a sound stream at a chosen time. | in the book text |
| Loop mode | Whether a clip plays once, loops or ping-pongs. | in the glossary |
| Loop seam | A jump where the last value meets the first on a loop. Test that they match. | in the book text |
| Speed scale | A multiplier on how fast a clip plays. 0.5 is half speed. | in the glossary |
| Autoplay | The animation a player starts by itself when its scene loads. | editor or docs |
| animation_finished | A signal sent when a clip ends. A looping clip does not send it. | editor or docs |
| Callback modes | Settings for when animation updates (idle or physics) and when method keys run (deferred or now). | in the book text |
| Update mode | Per value track: update between keys (continuous), or only at the keys (discrete). | in the book text |
| Tween | A value animated from code toward a target, then thrown away. For end values that come from gameplay. | in the book text |
| Easing | The speed curve of a change: slow start (ease-in) or slow end (ease-out). | in the glossary |
| Transition type | The family of curve a tween follows: linear, sine, quad, cubic, back, bounce and more. | editor or docs |
| Kill a tween | Abort a tween where it is. It stops short of its end value. | editor or docs |
| Skeleton | The hierarchy of bones. A child bone moves with its parent. | in the book text |
| Rest pose | The skeleton's default pose, which you can return to at any time. | in the book text |
| Inverse kinematics | Choose a target and compute the joint angles that reach it. | in the book text |
| Pole target | A helper point that sets which way an elbow or knee bends. | in the glossary |
| FABRIK | An IK solver that moves a chain back and forth between target and root until it fits. | outside source |
| Look-at | Turn one bone to face a target. No chain is solved. | editor or docs |
| SkeletonIK3D | The older built-in IK node. Marked Deprecated in the class reference. | in the book text |
| skeleton_updated | A signal sent when the final pose, IK included, is ready to read. | in the book text |
| Fixed frame rate | --fixed-fps n: every frame advances game time by exactly 1/n s. | in the book text |
| Backend limit | Something a headless run cannot test, such as a captured mouse. It stays unverified. | in the book text |

## Animation: principles and character animation

[Open the deck](decks/Terms%20-%20Animation%20principles.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Keyframe | A stored value at a specific time. | in the book text |
| Interpolation (its results are the in-betweens) | Computing the in-between values. | in the book text |
| Clip | An authored animation: tracks of values over time. | in the book text |
| Tween | Code-driven interpolation of a property over a duration. | in the book text |
| Linear | Constant rate of change. | in the book text |
| Step (discrete) | The value holds until the next key, then jumps. | in the book text |
| Cubic | A smooth curve through the keys, with no corner at a key. | editor or docs |
| Easing (ease-in-out is slow at both ends) | The speed curve of a change (ease-in slow start, ease-out slow end). | in the book text |
| Ease-in | Slow start, then it speeds up. | in the glossary |
| Ease-out | Fast start, then it slows to a stop. | in the glossary |
| Timing and spacing | Timing is how long a move takes; spacing is how far it moves between frames. | video only |
| Frame rate | Frames shown per second. | in the book text |
| Playback speed scale | A multiplier on how fast a clip plays. | in the book text |
| Loop | A clip that starts again from its first frame when it ends. | in the book text |
| Loop seam | A visible jump where the last frame meets the first. | in the book text |
| Cycle (walk, run) | One full stride that repeats; the first and last poses match. | in the book text |
| Pose | A single held body position; animation is a series of them. | video only |
| Silhouette | The solid outline of a pose; a clear action reads from the outline alone. | video only |
| Weight and balance | Where the balance falls; stable when it sits over the feet. | video only |
| Anticipation | A short wind-up that tells the player an action is coming. | video only |
| Squash and stretch | Compress on impact, elongate at speed; shows elasticity and inertia. | video only |
| Arcs | Limbs and thrown things move along curves, not straight lines. | outside source |
| Follow-through, overlap | Parts keep moving after the body stops, each settling at its own time. | outside source |
| Secondary motion | Extra movement the main action causes, such as a tail or hair, not keyed by hand. | outside source |
| Rig and skeleton | The skeleton (a hierarchy of bones) plus the binding that makes the mesh follow it. | in the glossary |
| Rest pose (bind pose) | The skeleton's default pose, the one the mesh is fitted to. | in the book text |
| Skinning weights (also bone weights, vertex weights) | How strongly each vertex follows each bone. | in the book text |
| Forward kinematics (FK) | Rotate joints parent-to-child to place the hand. | in the glossary |
| Inverse kinematics (IK) | Give a target and the solver works out the joint angles. | in the book text |
| Retargeting | Applying an animation made for one skeleton to a different one. | in the glossary |
| Root motion | The clip moves the character through the world. | in the book text |
| In-place | The clip stays on the spot; code does the travel. | in the book text |
| Blend tree | Weighted mix of clips driven by parameters. | in the book text |
| State machine | One active state; transitions fire on conditions. | in the book text |

## Art principles: concept art and character art

[Open the deck](decks/Terms%20-%20Art%20principles%20and%20concept%20art.html) · 15 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Clarity | The player can tell at once what is happening. | video only |
| Satisfaction | Actions get quick, responsive feedback. | video only |
| Art style | A consistent look: colour, designs, shapes. | video only |
| Pushed proportions | Exaggerated shapes, as in a cartoon look. | video only |
| Visual hierarchy | The most important things are seen first. | video only |
| Contrast | A difference that pulls the eye to one place. | video only |
| Light and dark contrast | The gap between light and dark areas. | video only |
| Colour contrast | Strong colour or saturation differences. | video only |
| Shape and size contrast | Distinct shapes or sizes make one thing stand out, or point the way. | video only |
| Silhouette | The outline of an object; it should still read when filled black at game size. | in the book text |
| Shape language | How the forms of a design express its personality or idea. | video only |
| Area of focus | The place in the image where the artist wants the eye to land. | video only |
| Rest and high detail | Plain regions beside busy ones, so the busy part reads as important. | video only |
| Atmospheric perspective | Faraway things lose detail and contrast, which adds depth and guides the eye. | video only |
| Concept art | Early drawings that solve a design problem for the team, not finished art. | video only |
| Reference | Real-world images and examples gathered for research. | video only |
| Mood board | A set of reference images showing the theme and tone, shown to the team early. | video only |
| Constraint | A limit that narrows what the artist designs. | video only |
| Thematic constraint | A limit from lore, setting and tone. | video only |
| Perspective constraint | A limit from the view: first, third, top down. | video only |
| Mechanics constraint | A limit from rules and numbers, such as health. | video only |
| Ideation | Many quick, rough ideas before choosing one. | video only |
| Two-tone sketching | Sketching in two colours to avoid small detail. | video only |
| Closing doors | Each round closes the options that failed. | video only |
| Iteration | Repeat draft, feedback and change. | video only |
| Iconic elements | The few features that keep a character recognisable even when tiny on screen. | video only |
| Proxy model | A rough block model of big shapes, used to check proportions and silhouette early. | video only |
| Readability | How well a character can be understood in the game's real view. | video only |
| High-poly sculpt | A very detailed sculpt, too heavy for the engine. | video only |
| Low-poly mesh | A simplified copy with far fewer polygons. | video only |
| UV map and unwrapping | Flat layout of a surface; unwrapping makes it. | in the glossary |
| Texture baking | Sculpt detail stored as an image on the low-poly. | video only |
| Anatomy | Knowing how bones and muscles work, so a sculpt is believable and can be animated. | video only |
| Neutral pose | The default pose a model is built in; some designs fail once the character moves. | video only |

## Blender: the interface and modeling terms

[Open the deck](decks/Terms%20-%20Blender%20interface%20and%20modeling.html) · 16 slides · 30 terms

| Term | Meaning | Tag |
|---|---|---|
| 3D viewport | The area where you see and edit the scene in 3D. | editor or docs |
| Outliner | A tree listing every object and collection in the scene. | editor or docs |
| Properties editor | Tabs of settings for the selected object: transform, modifiers, material. | editor or docs |
| Timeline | Playback controls and a frame scale with keyframes marked. | editor or docs |
| Workspace | A saved arrangement of editors for one job, chosen from the tabs on top. | editor or docs |
| Object Mode | Work on whole objects: move, rotate, scale. | editor or docs |
| Edit Mode | Work on the mesh itself: its vertices, edges and faces. | editor or docs |
| Collection | A named group of objects you can hide, show or export together. | editor or docs |
| Mesh | The vertices, edges and faces that make a 3D shape; the chapter calls it mesh data. | in the book text |
| Vertex | A corner point of a mesh. | in the glossary |
| Edge | A line joining two vertices. | in the glossary |
| Face | A flat surface bounded by edges. | in the glossary |
| Quad | A face with four vertices. | in the glossary |
| Polygon count | Three tallies of one mesh: engines budget by triangles, Blender shows faces, and vertices are split where UVs or normals differ. | in the glossary |
| Normal | The direction a surface faces. | in the glossary |
| Flipped normals | Faces pointing inward, so they look dark or vanish. | in the glossary |
| Transform | Location, rotation and scale: where the object is, how it is turned, how much it is stretched. | in the book text |
| Origin | The point an object's position and rotation are measured from. | in the glossary |
| Pivot | The point an object rotates and scales around. | in the glossary |
| Apply transforms (Also: scale versus size) | Bake position, rotation and scale into the mesh and reset them to neutral. | in the book text |
| Local and global space | Local coordinates are measured from the object's origin; global ones from the scene's. | editor or docs |
| Unit | The length one coordinate step stands for (usually a metre). | in the book text |
| Right-handed, +Z up | Blender: X cross Y gives Z, and Z is up. glTF and Godot put +Y up. | in the book text |
| Modifier | A live step that changes a mesh without editing it. | editor or docs |
| Mirror modifier | Copies the mesh across an axis, so you model one half. | editor or docs |
| Subdivision Surface | Splits and smooths faces; each level makes 4 times as many. | editor or docs |
| Bevel | Turns a sharp edge or corner into a small slanted or rounded one. | editor or docs |
| UV map | The flattened 2D layout of a mesh used to place a texture. | in the glossary |
| Unwrapping | Cutting a mesh and flattening it into a UV map. | in the glossary |
| Material versus texture | A material is the full surface recipe; a texture is one image it uses. | in the glossary |

## Blender to Godot: MCP, export and measuring a prop

[Open the deck](decks/Terms%20-%20Blender%20to%20Godot.html) · 14 slides · 30 terms

| Term | Meaning | Tag |
|---|---|---|
| MCP | A standard way for an AI app to call tools in another program such as Blender. | in the book text |
| MCP tool | A named action the agent may call, with typed arguments. | in the book text |
| MCP server and add-on | A relay the agent starts; an add-on inside Blender receives its calls. | in the book text |
| bpy | Blender's Python module; scripts and MCP tools both drive it. | in the book text |
| Headless Blender (also background mode (-b)) | Running Blender with no window, from the command line. | in the book text |
| --python-exit-code | A flag that makes a script error end Blender with exit code 1, not 0. | in the book text |
| Unit | The length one coordinate step stands for, usually a metre. | in the book text |
| Unit scale | The factor from Blender units to metres; 1.0 means 1 unit is 1 m. | in the book text |
| Up axis (Godot's forward is −Z) | Which axis points up: Z in Blender, Y in glTF and Godot. | in the book text |
| Axis conversion | The exporter's +Y Up option turns Blender's Z extent into Godot's Y. | in the book text |
| Apply transforms | Bake position, rotation and scale into the mesh and reset them to neutral. | in the book text |
| Node scale | A scale left on the node instead of baked into the mesh. | in the book text |
| Origin and pivot | The point position and rotation are measured from; the pivot is what it rotates and scales around. | in the glossary |
| Dimensions | An object's size in metres on each axis, as Blender reports it. | in the book text |
| Bounding box (its half-sizes are the extents) | The smallest axis-aligned box that holds an object. | in the glossary |
| Claim versus measurement | A claim is what a name or script says; a measurement is what a test reads from the file. | in the book text |
| glTF | An open 3D format; the preferred exchange format for engines. | in the book text |
| GLB | glTF packed into a single binary file. | in the book text |
| Material through export | A named Blender material arrives under the same name; Blender-only nodes do not. | in the book text |
| Import file (.import) | The text file beside a model whose settings decide what Godot builds. | in the book text |
| Name suffix | A tail on a mesh name, such as -convcolonly, that tells Godot to build collision. | in the book text |
| Collision shape | The simple shape physics uses, as opposed to the detailed mesh you see. | in the book text |
| Convex and concave | Convex has no dents: a line between two inside points stays inside. Concave has a hollow. | in the glossary |
| Triangle count (not face count or vertex count) | Engines budget by triangles; Blender shows faces; vertices split where UVs or normals differ. | in the glossary |
| High-poly and low-poly | A very detailed sculpt, and the cheap copy of it that the engine runs. | video only |
| Texture baking | Moving the sculpt's fine detail into an image the low-poly mesh wears. | video only |
| LOD | Level of detail: cheaper versions of a model swapped in at distance. | in the glossary |
| Script as source | The script that built the asset is what you commit and rerun; the .glb is its output. | in the book text |
| Version control | Software that records every version of a file and who changed it, and warns of clashes. | video only |
| Naming conventions | Agreed rules for how files and objects are named. | video only |

## Terms: Camera

[Open the deck](decks/Terms%20-%20Camera.html) · 19 slides · 20 terms

| Term | Meaning | Tag |
|---|---|---|
| Pan | Turn left or right on the spot; position unchanged. | in the glossary |
| Tilt | Turn up or down on the spot; position unchanged. | in the glossary |
| Roll | Spin around the viewing direction; the horizon tips. | in the glossary |
| Dolly | Move the camera forward or backward along its view direction. | in the glossary |
| Dolly in / dolly out (also dolly in/out) | Move the camera toward / away from the subject. Dolly in moves toward the subject, dolly out moves away. | in the glossary |
| Truck | Move the camera left or right, still facing the same way. | in the glossary |
| Pedestal | Move the camera straight up or down, still facing the same way. | in the glossary |
| Zoom | Change the lens (field of view or focal length); the camera does not move. | in the glossary |
| Dolly versus zoom | A dolly changes parallax (near and far shift against each other); a zoom only magnifies. | in the glossary |
| Parallax | Nearer things shift more than farther things when the viewpoint moves. | in the glossary |
| Focal length | Lens strength in millimetres; longer means narrower view and more magnification. | in the glossary |
| Orbit | Move around a subject on a curved path while keeping it framed. | in the glossary |
| Follow camera | Tracks a moving target, usually with smoothing. | in the glossary |
| Smoothing (damping) (also smoothing/damping) | Spreads the camera's catch-up over time so it trails slightly. Same idea under both names: the camera eases toward its target instead of snapping. | in the glossary |
| Deadzone | Screen region where the target can move without the camera moving. | in the glossary |
| Look-ahead | Shifts framing toward the direction of travel. | in the glossary |
| Screen shake | Brief, fading random offset of the camera for impact. | in the glossary |
| Camera limits | Clamps that keep the view inside the level. | in the glossary |
| Field of view (FOV) | The lens angle; wider shows more. | in the glossary |
| Perspective / orthographic | Distant things shrink / size does not depend on distance. | in the glossary |

## Game AI: decisions, generation and systems

[Open the deck](decks/Terms%20-%20Game%20AI%20decisions%20and%20systems.html) · 16 slides · 33 terms

| Term | Meaning | Tag |
|---|---|---|
| Finite state machine | A set of states with transitions; one is active. | in the book text |
| Transition table | A list of every state, condition and next state. | in the glossary |
| Flicker | Rapid back-and-forth switching between states. | in the book text |
| Hysteresis | Different thresholds for switching on and off, to stop rapid switching. | in the book text |
| Behavior tree | A tree of nodes that decides what an agent does each tick. | in the book text |
| Tick | One update step; the tree is evaluated again from the root. | in the book text |
| Success/failure/running | The three results a node can return; running means not finished, tick me again. | in the book text |
| Blackboard | A shared memory of facts the AI reads and writes. | in the book text |
| Condition and action | A condition asks a question; an action does the work and may keep running. | in the book text |
| Selector (Also called a fallback) | Tries children in order until one succeeds. | in the book text |
| Sequence | Runs children in order and stops at the first failure. | in the book text |
| Utility AI | Scores every option and picks the highest. | in the glossary |
| Weighted sum | Adding scores, each multiplied by an importance weight. | in the glossary |
| GOAP | Goal-oriented action planning: search for actions that reach a goal. | in the glossary |
| Precondition and effect | Precondition: what must be true before an action runs. Effect: what it changes. | in the glossary |
| Reinforcement learning | Learning behaviour by trial and reward. | in the book text |
| Reward | The number telling the agent how well it did. | in the book text |
| Discount factor | How much future reward is worth compared to now. | in the book text |
| Q-learning | Learning the value of each action in each state. | in the book text |
| Epsilon-greedy | Take a random action with probability epsilon, otherwise the best known one. | in the book text |
| Seed (Pseudo-random: looks random, computed from a seed) | A number that fixes a random sequence. | in the book text |
| Coherent noise | Random values that change smoothly (Perlin, simplex). | in the book text |
| Octave | One layer of noise at a set scale, added to others. | in the glossary |
| Determinism | Same inputs and seed give the same output every run. | in the book text |
| Heightmap | A grid with one height value per position. | in the book text |
| Compute shader | A GPU program run over many cells at once, outside the drawing pipeline. | in the book text |
| Validator | A check that tests generated content against rules. | in the book text |
| Generate-and-test | Make content randomly, then reject what fails. | in the book text |
| Constructive generation | Build content by rules that guarantee validity. | in the book text |
| Safety margin | Extra room left so generated content never just barely passes. | in the book text |
| Authority | The part of the system allowed to change a value. | in the book text |
| RPC | A function one computer asks another computer to run. | in the book text |
| Replication | Copying a value from the peer that owns it to the other peers. | in the book text |

## Game AI: perception, movement and pathfinding

[Open the deck](decks/Terms%20-%20Game%20AI%20movement%20and%20pathfinding.html) · 15 slides · 33 terms

| Term | Meaning | Tag |
|---|---|---|
| Agent | A game character that senses and acts on its own. | outside source |
| Sense, decide, act | The loop every system in Chapter 14 runs, once per tick. | in the book text |
| Sight range | How far an NPC can see. | in the glossary |
| Field-of-view cone | The angle across which the agent can see. | outside source |
| Line of sight | A straight line to the target that nothing blocks. | in the book text |
| Hearing (noise) radius | How far a noise carries to an agent. | outside source |
| Last known position | Where the target was last seen, kept in memory. | in the book text |
| Steering | Behaviours that adjust movement toward a goal. | in the glossary |
| Velocity, max speed | Speed with a direction; max speed caps its size. | in the book text |
| Seek | Steer toward a target. | in the glossary |
| Flee | Steer away from a target. | in the glossary |
| Arrive | Seek and slow down to stop at the target. | in the glossary |
| Pursue | Steer toward where a moving target will be. | in the glossary |
| Wander | Small random turns, so the path meanders. | outside source |
| Separation | Steer away from close neighbours. | in the glossary |
| Alignment | Steer to match neighbours' heading. | in the glossary |
| Cohesion | Steer toward the neighbours' centre. | in the glossary |
| Emergent behavior | Complex group behaviour from simple rules. | in the glossary |
| Graph, edge, weight | Points (nodes) joined by edges, each with a cost. | outside source |
| Grid (AStarGrid2D) | Cells marked solid or free; the light tool for grid games. | in the book text |
| Navigation mesh | Polygons marking where agents can walk. | in the book text |
| Waypoint | A point along a path. | in the glossary |
| Breadth-first search | Expands outward one step at a time and ignores cost. | outside source |
| Dijkstra | Pathfinding that expands by cost so far only, with no heuristic. | in the glossary |
| Open and closed set | Open: found, not yet expanded. Closed: already expanded. | outside source |
| A* | Pathfinding that picks the lowest f = g + h node first. | in the glossary |
| f, g, h | Total estimated cost / cost so far / estimated cost to goal. | in the glossary |
| Manhattan distance | Distance counted along grid axes only. | in the glossary |
| Euclidean distance | Straight-line distance. | outside source |
| Admissible heuristic | An estimate that never overestimates the true cost. | in the glossary |
| NavigationAgent2D | Godot node that follows a navmesh path. | in the book text |
| Path smoothing | Cut corners from a path wherever the straight line is clear. | outside source |
| Local avoidance | Steering around nearby obstacles and agents. | in the glossary |

## Game design A: what a game is

[Open the deck](decks/Terms%20-%20Game%20design%20A.html) · 14 slides · 22 terms

| Term | Meaning | Tag |
|---|---|---|
| Game | An activity that has all four: a goal, opposition, decisions and rules. | video only |
| Goal | The objective the player works toward. | in the glossary |
| Opposition | Obstacles the player must overcome; it makes a game fun and can frustrate. | video only |
| Decisions | The ways the player can get past the opposition. | video only |
| Rules | The framework that limits and governs the whole experience. | video only |
| House rules | Rules a group changes for its own table; they change how the game plays. | video only |
| Mechanic | A rule-governed action in the game. | in the book text |
| Player verb | An action the player can take: jump, shoot, build. | in the glossary |
| Core mechanic | The action players do over and over again. | video only |
| Core loop | The repeated moment-to-moment cycle the player enjoys. | in the glossary |
| Thematic feel | Mechanics alone can set the tone: what a thing does tells the player what it is. | video only |
| Movement pattern | How a character moves gives it personality: a hop is a frog, a wave is a snake. | video only |
| Types of fun (also Eight Kinds of Fun (Marc LeBlanc)) | "Fun" is too vague. Name the kind: fantasy, thrill, fellowship, mastery, exploration, creativity. | video only |
| Target experience | The one specific experience everyone on the team aims at. | video only |
| Appeal | The pull to keep playing; it differs by game and by player. | video only |
| Art, design, engineering | They depend on each other; results are best when all three aim at the same target. | video only |
| Space | The look, sound, lighting and physical setting; it shapes what fits in the game. | video only |
| Components | The objects in the space that players use or meet: characters, weapons, vehicles. | video only |
| Prototype | A simplified version made first to test whether the idea has appeal. | video only |
| Play testing | Letting players challenge the design so it can be revisited and improved. | video only |
| Clear progress | The player can see how close they are to the goal. | video only |
| Climactic arc | Difficulty and tension build toward the goal's resolution. | video only |

## Game design B: choices and challenge

[Open the deck](decks/Terms%20-%20Game%20design%20B.html) · 14 slides · 19 terms

| Term | Meaning | Tag |
|---|---|---|
| Meaningful play | The player acts and the game responds in a way that matters. | in the glossary |
| Descriptive play | The player acts and sees the game respond: the bola hits, the ice shatters. | in the glossary |
| Evaluative play | The player steps back and asks why this action matters to the whole game. | in the glossary |
| Meaningful choice | A choice that changes what happens and that the player has to think about. | in the glossary |
| Agency (autonomy) | The player takes control of how the game is played. | in the glossary |
| Risk versus reward | A harder or riskier action pays more, and the player weighs the factors. | in the glossary |
| Trade-off | Give up one thing to get another. | in the glossary |
| Persistence | The player lives with the consequences of a choice for a set time. | in the glossary |
| Situational choice | The same choice is better or worse depending on the situation the player is in. | in the glossary |
| Unit differentiation (also orthogonal unit differentiation) | Each enemy type does something different, which forces the player to prioritise. | in the glossary |
| Personalisation | Players build their own play style from the decisions they make. | in the glossary |
| Frustration | Some is part of challenge; it has to be the kind the player can learn from. | in the glossary |
| Difficulty | How hard the opposition is; it is separate from fairness. | in the glossary |
| Fairness | Clear expectations and consistent design, so the player can learn from failing. | in the glossary |
| Luck and skill | Luck: chance decides. Skill: the player's ability decides. Games mix the two. | in the glossary |
| Balance | Every advantage has a disadvantage; no role starts with an unfair edge. | in the glossary |
| Rock-paper-scissors | Each option beats one and loses to another, so no option wins everywhere. | in the glossary |
| Downtime | Time a player waits with nothing to do. | in the glossary |
| Probability | The odds of each result; extra rolls change them. | in the glossary |

## Game design C: pacing and guidance

[Open the deck](decks/Terms%20-%20Game%20design%20C.html) · 15 slides · 19 terms

| Term | Meaning | Tag |
|---|---|---|
| Three pillars | A game rests on the player's role, communication and appeal. | in the glossary |
| Player purpose | What the player does and why; the player, not the game, drives it forward. | in the glossary |
| Communication | Showing the player the goal and how to reach it, with clues in the environment. | in the glossary |
| Guiding the focus | Making clear what the player should concentrate on. | in the glossary |
| Linear and nonlinear | Straight from start to end, or with alternate choices along the way. | in the glossary |
| Side quest | A detour from the main storyline. | in the glossary |
| Level design | Planning and building the spaces the player moves through. | in the glossary |
| Teaching through levels | The first level lets the player try each skill, with no text. | in the glossary |
| Design the middle first | Build the engaging middle levels, then the opening levels that lead there. | in the glossary |
| Anticipation | Prepare the player for what comes next, such as a wind-up before an attack. | in the glossary |
| Build-up | A sequence that raises tension toward an event: sound, sparks, camera shake. | in the glossary |
| Logical events | Events behave sensibly and meet the player's unspoken expectations. | in the glossary |
| Consistent rules | Even where physics is bent, it is bent the same way every time. | in the glossary |
| Games can cheat | Hidden help the player does not notice, such as enemies told not to turn around. | in the glossary |
| Dynamic | Many things happening at once, so play stays fresh. | in the glossary |
| Progression | A natural rise in challenge; do not over-stimulate or under-stimulate. | in the glossary |
| Pacing | Alternating intense and calm moments. | in the glossary |
| Waves | A group of enemies sent together: many weak ones or a few strong ones. | in the glossary |
| Spacing | Open areas to admire, or tight ones that feel claustrophobic; leave room for AI. | in the glossary |

## The game design document

[Open the deck](decks/Terms%20-%20Game%20design%20document.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| GDD | What the game is and how it plays, in enough detail to build it and test it. | in the book text |
| Game brief | What the player does, what success is, what can go wrong, what is out. | in the book text |
| Pitch | A short sales description of the game idea. | in the glossary |
| Reverse | Recover a GDD from a game that already exists. | in the book text |
| Draft | Write a GDD from a new idea and mark what you assumed. | in the book text |
| Gate | A named sign-off after a design phase; only a person signs it. | in the book text |
| Sixteen sections | The fixed outline of a GDD, from metadata to open questions. | in the book text |
| Design pillar | A core principle every decision must support. | in the glossary |
| Core loop | The repeated moment-to-moment cycle the player enjoys. | in the glossary |
| PX goal | A feeling or experience the player should have, with an ID like PX-01. | in the book text |
| Mechanic | A rule-governed action in the game. | in the glossary |
| Stable ID | A label that never changes, such as PX-01, M-01 or T-01. | in the book text |
| Linked test | A test row that names the mechanic it checks. | in the book text |
| [OBSERVED] | The code does this; the tag names a file and line. | in the book text |
| [INFERRED] | The code strongly implies it; the evidence is stated. | in the book text |
| [MISSING] | The code cannot tell you this. | in the book text |
| [ASSUMPTION] | A gap the draft filled in; nobody saw it. | in the book text |
| Ghost Center | No locked vision, so nothing anchors the decisions. | in the book text |
| Mechanic Mirage | A PX goal that is really a feature described in disguise. | in the book text |
| Implementation Void | A mechanic with only the happy path written down. | in the book text |
| Priority Inflation | More than 40% of the features tagged CORE. | in the book text |
| Novelist's Trap | Story written for a reader, not for an engineer. | in the book text |
| Completeness Fallacy | Decisions with no recorded reasoning. | in the book text |
| Stagnant Artifact | No version history; never revised after a prototype. | in the book text |
| Scope | Everything the project promises to include. | in the glossary |
| Out of scope | A written list of what will not be built. | in the book text |
| Scope creep | Quiet growth of work beyond what was agreed. | in the glossary |
| Cut, defer, swap | The three ways to handle too much scope: remove, postpone, replace. | in the glossary |
| Acceptance criterion | A concrete condition that must be true for work to count as done. | in the book text |
| Given-when-then | A format for a test: starting state, action, expected result. | in the glossary |
| Tolerance | The allowed difference between expected and actual. | in the book text |
| Direct state write | Setting a value in code instead of producing it through gameplay. | in the book text |
| Invariant | A condition that must stay true throughout. | in the book text |
| False pass | A test that passes though the behaviour is wrong. | in the book text |

## How to make a trailer for your game

[Open the deck](decks/Terms%20-%20Game%20trailer.html) · 16 slides · 32 terms

| Term | Meaning | Tag |
|---|---|---|
| Trailer | A short film that sells a game to a stranger. | outside source |
| Teaser | An early look that hints and shows little. | outside source |
| Gameplay video | Plain footage of play, made to cover, not sell. | outside source |
| Pitch film | A 2 to 4 minute film on what you will build. | outside source |
| Pitch | A short sales description of the game idea. | in the glossary |
| Logline | The game in one sentence: who does what, and what is new. | outside source |
| Tagline | A few memorable words that sit beside the title. | outside source |
| Hook | The most distinctive thing the player does, said in one sentence. | outside source |
| Key art | The one still image that stands for the game: title, character, idea. | outside source |
| Thumbnail | The small preview image; it has to read at a glance. | outside source |
| Beat structure | The order of parts: hook, establish, escalate, peak, title, button, call to action. | outside source |
| Climax (peak) | The biggest payoff, placed on a strong beat after a quiet drop. | outside source |
| Title card | A held card with the game's name, after the peak. | outside source |
| Runtime | How long the film runs; a store trailer is typically 30 to 90 seconds. | outside source |
| Frame rate | Frames shown per second. | in the glossary |
| Resolution | Width and height in pixels. | in the glossary |
| Pacing | How fast the cuts come; it follows how well the viewer understands the game. | outside source |
| Cut on action | Cut while the motion is under way, so the eye carries across the cut. | outside source |
| BPM | Beats per minute of the music; 60 divided by it is the seconds per beat. | outside source |
| Cut on the beat | Place cuts on the music's beats so picture and sound lock together. | outside source |
| Music drop | A quiet moment just before the peak, so the peak lands. | outside source |
| Sound design | Mix so music sets the tone and the game's own hits punch through. | outside source |
| Muted test | Check that the film still makes sense with the sound off. | outside source |
| Accessibility | Captions for speech and no rapid flashing, so more people can watch. | outside source |
| Call to action | One thing to do next: wishlist, play, or follow a link. | outside source |
| Logo sting | A very short logo animation with a sound; better at the end than the start. | outside source |
| Fixed frame rate | Rendering locked to a set number of frames a second so runs match. | in the book text |
| Movie Maker mode | Godot's mode that records a run to a video file, frame by frame. | editor or docs |
| Clean footage | Real play with debug clutter hidden and the HUD that explains a mechanic kept. | outside source |
| Gameplay vs cinematic | Captured play from the real build; a cinematic must be the game's own and labelled. | outside source |
| Honest trailer | Shows only what the game really does; planned features never appear. | outside source |
| Viewer test | Show the cut, unexplained, to someone new and ask what the game is and what they do. | outside source |

## Godot, Unity and Unreal: the differences

[Open the deck](decks/Terms%20-%20Godot%20Unity%20Unreal.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Scene, Level, Map (Godot scene · Unity Scene · Unreal Level) | A saved, reusable tree of objects. Unreal's word for the level file is Map. | in the book text |
| Node, GameObject, Actor (Godot · Unity · Unreal) | One object in the scene. A GameObject does nothing until components are added. | in the book text |
| Component (Godot picks a node type instead) | A piece of behaviour or data attached to a GameObject or an Actor. | in the book text |
| Template | The master that copies come from: a Godot scene, a Unity Prefab, an Unreal Blueprint class. | in the book text |
| Instance | One live copy made from a template. | in the book text |
| Override | A change on one instance. In Unity, Apply pushes it into the Prefab and Revert drops it. | in the book text |
| Data asset | Shared data kept as a file: Godot Resource, Unity ScriptableObject, Unreal Data Asset. | in the book text |
| Signal | Godot's named event. Other nodes connect to it and run when it fires. | in the book text |
| UnityEvent, C# event | Unity's events. A UnityEvent is wired in the Inspector, so reading code alone can miss it. | in the book text |
| Event Dispatcher | Unreal's Blueprint form of a signal. One Call fires every bound event; C++ uses a delegate. | in the book text |
| Autoload, Game Instance | Things that outlive a scene: Godot autoload, Unity DontDestroyOnLoad, Unreal Game Instance. | in the book text |
| GDScript | Godot's own scripting language. Scripts are plain text files. | in the book text |
| C# and MonoBehaviour | Unity's language. A MonoBehaviour is a component script, also plain text. | in the book text |
| Blueprint graph | Unreal's visual scripting. The graph is a binary asset an agent cannot diff as text. | in the book text |
| C++ in Unreal | Unreal's code route. Plain text, but it must be compiled before a change takes effect. | in the book text |
| _process, _physics_process (Godot) | Once per frame, and at a fixed 60 times a second by default. | in the book text |
| Update, FixedUpdate (Unity) | Once per frame, and at fixed 0.02 s steps, which is 50 a second by default. | in the book text |
| Tick (Unreal) | Each Actor ticks every frame. Tick groups such as pre-physics order the work. | in the book text |
| Input action (InputMap · Input System · Enhanced Input) | A named intent such as jump, bound to keys or buttons and kept apart from them. | in the book text |
| Character body (CharacterBody2D · Rigidbody2D · Character) | The body you move on purpose: your script, or Unreal's movement component. | in the book text |
| Trigger (Area2D · Is Trigger · Trigger volume) | A zone that reports overlaps instead of blocking, such as a pickup or a checkpoint. | in the book text |
| Layer and mask (Godot) | Each object has a layer and a mask. A notices B if B's layer is in A's mask: one way. | in the book text |
| Layer Collision Matrix (Unity) | One layer per GameObject. A project-wide grid says which pairs of layers collide. | in the book text |
| Object Type, response (Unreal) | Block, Overlap or Ignore for every type. Both sides must agree before contact happens. | in the book text |
| Up axis, handedness | Godot and Unity are Y-up, Unreal is Z-up. Unity and Unreal are left-handed, Godot is right-handed. | in the book text |
| Units | In Godot and Unity 1 unit is 1 metre. In Unreal 1 unit is 1 centimetre. | in the book text |
| Clip and player (AnimationPlayer · Animator · Sequence) | Keyed data played over time. Unity wraps even one clip in an Animator Controller. | in the book text |
| Event key (Method track · Event · Notify) | A call placed on the timeline. An Anim Notify State has a begin and an end. | in the book text |
| State machine (AnimationTree · Controller · Anim Blueprint) | States joined by transitions with rules. The current state picks the clip. | in the book text |
| Shader and material (Shader code · Shader Graph · Material Editor) | Godot and Unity write shaders as code or graph. Unreal builds materials as node graphs. | in the book text |
| Material parameter (uniform · Material property · parameter) | A named value that your code sets and the shader reads. | in the book text |
| Particle system (GPUParticles · VFX Graph · Niagara) | Many small sprites simulated together. A one-shot burst spawns them all at once. | in the book text |
| Build and export | Godot saves export presets, Unity 6 saves a build profile, Unreal packages and cooks the project. | in the book text |
| Licence | Godot is MIT. Unity is proprietary. Unreal is source-available, not open source. | in the book text |

## Godot: the editor, scenes, nodes, signals and movement

[Open the deck](decks/Terms%20-%20Godot%20editor%20and%20scenes.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Scene dock, Remote tab | Lists the scene's nodes; the Remote tab lists the running game's. | in the book text |
| FileSystem dock | Lists every file in the project, under res://. | editor or docs |
| Inspector | The editor panel for viewing and editing properties. | in the glossary |
| Node dock | Shows the selected node's signals and groups. | editor or docs |
| 2D, 3D and Script views | Tabs along the top: 2D and 3D edit scenes, Script edits code. | editor or docs |
| Output and Debugger | Bottom panels: Output shows printed text, Debugger shows errors. | editor or docs |
| Project Settings | Project-wide values: physics rate, layer names, input actions, autoloads. | in the book text |
| Run and Play buttons | Run Project (F5) starts the main scene; Run Current Scene starts the open one. | editor or docs |
| Project | A folder with a project.godot file at its root; res:// means that folder. | in the book text |
| Scene | A saved, reusable tree of nodes: a level, a character, a menu. | in the book text |
| Node | The smallest building block: one object doing one job. | in the book text |
| Script | Attaches behaviour to a node; GDScript here. | in the book text |
| Scene tree | The live hierarchy of nodes in a running game. | in the book text |
| Instance | One live copy of a saved scene; a change on one instance overrides the template. | in the book text |
| _process | Runs once per rendered frame; the rate varies by machine. | in the book text |
| _physics_process | Runs at a fixed rate, 60 times a second by default. | in the book text |
| Input action | A named intent such as jump, bound to keys or buttons. | in the book text |
| Just-pressed vs held | Just-pressed is true only on the tick a press began; held stays true while down. | in the book text |
| Polling | Asking every tick whether something has happened. | in the book text |
| Event-driven | Code runs only when something announces that it happened. | in the glossary |
| Signal | A named event a node emits; other nodes connect to it. | in the book text |
| Group | A named tag on nodes; one call reaches every node in it. | in the book text |
| Autoload | A script or scene kept loaded across scene changes. | in the book text |
| Resource | A typed data container nodes share, made by extending Resource. | in the book text |
| Export preset, template | A preset is the recipe for one platform; the template is the prebuilt engine it packs your data into. | in the book text |
| Area2D | Detects overlaps and can emit signals; never blocks or pushes. | in the book text |
| StaticBody2D | Not moved by physics; others collide with it. | in the book text |
| RigidBody2D | Simulated physics: you set forces or velocity, the engine moves it. | in the book text |
| CharacterBody2D | Moved by your code; move_and_slide() slides it along what it hits. | in the book text |
| Collision shape | The geometry physics uses, separate from the drawn sprite. | in the book text |
| Collision layer | Where an object is: the layers it appears in. | in the book text |
| Collision mask | What an object scans: it detects B only if B is in a layer it scans. | in the book text |
| Bitmask | A number whose bits switch layers on or off; layer n has the value 2^(n−1). | in the book text |
| Area snapshot | An Area's overlap list is updated once per physics step, so it can be a tick old. | in the book text |

## Materials and textures

[Open the deck](decks/Terms%20-%20Materials%20and%20textures.html) · 16 slides · 34 terms

| Term | Meaning | Tag |
|---|---|---|
| Material | A stack of textures and numbers that says how a surface looks. | in the book text |
| PBR | Physically based rendering: a few measured quantities per pixel, so a material holds up under any light. | in the book text |
| Lighting | Light and camera turn the material's quantities into the colour you see. | in the book text |
| Albedo (also base colour) | The colour the surface reflects, before any lighting. | in the book text |
| Roughness | How blurred the reflections are: 0 is mirror-sharp, 1 is wide and dull. | in the book text |
| Metallic | Whether the surface behaves like a metal: 0 is non-metal, 1 is metal. | in the book text |
| Colour texture | A texture holding colours people see; only the base colour is one. | in the book text |
| Data texture | A texture whose numbers are the values, such as normals or roughness. | in the book text |
| sRGB | The encoding for images shown to people; steps are spaced for eyes. | in the book text |
| Linear and decoding | Values proportional to light. Colour is decoded to linear first; data must not be. | in the book text |
| Normal map | Per-pixel surface direction that fakes bumps in the lighting; red, green, blue are X, Y, Z. | in the book text |
| Tangent space | Normal directions relative to the surface itself, so the map works on any mesh. | in the glossary |
| Green channel convention | Whether green points up (OpenGL, Godot) or down (DirectX). | in the book text |
| Ambient occlusion | Darkening in creases where ambient light cannot reach; direct light is not affected. | in the book text |
| Emission | Light the surface gives off itself. | in the glossary |
| SSAO | Screen-space ambient occlusion: a real-time estimate from the depth image, separate from a texture's AO. | in the book text |
| ORM | A packed map: occlusion in red, roughness in green, metallic in blue. | in the book text |
| Channel packing | Storing different maps in the red, green and blue channels of one image. | in the glossary |
| Map slot naming | The agreed names for each texture slot, such as albedo, normal, roughness. | in the glossary |
| Smoothness | The inverse of roughness: how mirror-like a surface is. | in the glossary |
| HDRP mask map | Unity HDRP's packed map: red metallic, green AO, blue detail mask, alpha smoothness. | in the book text |
| URP Lit maps | Base, Metallic, Normal and Occlusion maps; smoothness comes from an alpha channel. | in the book text |
| UV | 2D coordinates that map each point of a surface to a spot on a texture. | in the book text |
| Unwrapping | Cutting a mesh along seams and flattening it into a UV map. | in the glossary |
| Texture baking | Transferring the detail of a high-poly model into an image used on the low-poly one. | video only |
| Resolution | Width and height of a texture in pixels. | in the glossary |
| Texel density | Texels per unit of world size: texture pixels per metre. Should match across objects. | in the glossary |
| UV scale | A multiplier on UVs that sets how often a texture repeats. | in the glossary |
| Tiling | Repeating a texture across a surface; a seamless texture shows no join. | in the glossary |
| Wrap mode | What sampling outside 0 to 1 does: repeat (tile) or clamp (stretch the edge). | in the glossary |
| Mipmap | One of the pre-shrunk copies of a texture; without them, distant surfaces shimmer. | in the book text |
| Baked lighting | Light and shadow stored in a texture or lightmap ahead of time. | in the glossary |
| Global illumination | Light that bounces off surfaces and lights others; Godot has several techniques. | in the book text |
| Reflection probe | A point that captures the surroundings so shiny surfaces have something to reflect. | in the book text |

## Particles and VFX

[Open the deck](decks/Terms%20-%20Particles%20and%20VFX.html) · 16 slides · 35 terms

| Term | Meaning | Tag |
|---|---|---|
| Particle | One small short-lived sprite or mesh in an effect. | in the book text |
| Emitter | The thing that spawns particles. | in the book text |
| Particle system | The emitter plus the rules for its particles. | in the book text |
| amount | Particles in one emission cycle; a looping emitter never has more alive. | in the book text |
| lifetime | Seconds a particle lives; also the length of one emission cycle. | in the book text |
| Steady state | Births equal deaths, so the live count levels off. | in the glossary |
| explosiveness (a burst is explosiveness = 1) | 0 spreads births across the cycle; 1 emits them all at its start. | in the book text |
| one_shot | Only one emission cycle occurs; otherwise it loops forever. | in the book text |
| preprocess (also called prewarm) | Starts as if the effect had already run this many seconds. | in the book text |
| Emission shape | The volume particles spawn in: point, sphere, box. | in the glossary |
| Initial velocity | The speed and direction a particle starts with. | in the glossary |
| spread | The cone angle of random variation around the emission direction. | in the book text |
| Seed, determinism | Same seed and inputs give the same random choices and output every run. | in the glossary |
| Gravity | Constant downward acceleration applied to particles. | in the glossary |
| Damping | The rate at which particles lose velocity. 100 takes a speed of 100 to 0 in 1 second. | editor or docs |
| Scale curve | A curve for particle size over its life. | in the glossary |
| Colour ramp | A gradient for particle colour over its life. | in the glossary |
| texture | The image drawn for each particle. If null, 1 by 1 pixel squares. | in the book text |
| Additive blending (a blend mode) | Adds the new colour to what is behind it; glows and fire. | in the glossary |
| Billboard (Riot: camera-facing card) | A flat quad that always faces the camera. | in the glossary |
| local_coords (off: world coordinates) | On: particles move with the emitter. Off: they are left behind. | in the book text |
| fixed_fps, interpolate | Update at a fixed rate; interpolate smooths motion between updates. | in the book text |
| visibility_rect (3D: visibility_aabb) | The region that must be on screen for the effect to be active. | in the book text |
| GPUParticles2D / 3D | Simulated on the graphics card; many particles, more features. | in the book text |
| CPUParticles2D / 3D | Simulated on the processor; wider hardware support, fewer particles. | in the book text |
| ParticleProcessMaterial | The resource that holds a GPU particle system's rules for moving and changing. | in the book text |
| Sub-emitter | A second GPU particle system that spawns from the first one's particles. | in the book text |
| Trail (ribbon) | A strip that follows a moving object, textured to look like a tail. | video only |
| Particle shader | A shader that sets each particle's properties in start() and process(). | in the book text |
| Primary to tertiary read | The order the eye notices an effect's parts: head, tail, then sparks. | video only |
| Restraint | Keeping most effects modest so the important ones stand out. | video only |
| Shape language | The same shapes for the same meaning across the whole game. | video only |
| Colour coding | Colours that signal team, damage type or tone. | video only |
| Analogous colours | Neighbouring hues, used to tie an effect to the model that casts it. | video only |
| Timing curve | Varying how fast an effect grows and slows, not a constant rate. | video only |

## Shaders: foundations

[Open the deck](decks/Terms%20-%20Shader%20foundations.html) · 16 slides · 33 terms

| Term | Meaning | Tag |
|---|---|---|
| Shader | A small program on the graphics processor, run many times at once. | in the book text |
| Vertex shader | Runs per vertex; sets positions (waves, displacement). | in the book text |
| Fragment (pixel) shader | Runs per pixel; sets colour (tint, glint). | in the book text |
| Programmable stage | A pipeline step you write a shader for. | in the glossary |
| Fixed-function | Old hardware steps that could be configured but not programmed. | in the glossary |
| Rasterization | Turning triangles into fragments on the screen grid. | in the glossary |
| Fragment | A candidate pixel colour produced by rasterization for one covered screen position. | in the glossary |
| Varying | A value passed from the vertex stage to the fragment stage, interpolated on the way. | in the glossary |
| Interpolation (shader) | Smoothly blending vertex values across a triangle's fragments. | in the glossary |
| shader_type | First line of a shader: says what it draws, and so which functions you can write. | in the book text |
| canvas_item | Godot shader type for 2D drawing: sprites, shapes, UI. | in the book text |
| spatial | Godot shader type for 3D drawing: meshes. | in the book text |
| Godot shading language | Based on GLSL but simplified; the ideas carry over between dialects. | in the book text |
| Compile error | The shader fails to build and gives an error message; a headless run still exits 0. | in the book text |
| UV | 2D coordinates mapping a surface to a texture, 0 to 1 across it. | in the book text |
| SCREEN_UV | Godot built-in: the screen position of the current fragment, 0 to 1. | in the book text |
| Vertex colour | Colour stored on each vertex; can blend textures or paint terrain by height. | video only |
| TEXTURE | The default 2D texture the item was drawn with. | in the book text |
| COLOR | Arrives as vertex colour times TEXTURE colour; what you leave in it is drawn. | in the book text |
| TIME | Seconds since the engine started; repeats after 3,600 s. | in the book text |
| Uniform (also called: shader parameter) | A value set from code, the same across a draw; how scripts steer a shader. | in the book text |
| hint_range | Gives the Inspector a slider; does not clamp values set from code. | in the book text |
| source_color | Marks a colour as sRGB data so it is decoded to linear for the maths. | in the book text |
| Material | A shader plus its parameter values and textures. | in the book text |
| ShaderMaterial | A material that uses a custom Shader program and holds its parameter values. | in the book text |
| set_shader_parameter | Changes one uniform's value on a material, by name; a typo does nothing. | in the book text |
| Shared material | One material used by many objects, so a change hits them all. | in the book text |
| RGBA | Red, green, blue and alpha channels. | in the glossary |
| Linear vs sRGB | sRGB is the encoding for images shown to people; linear values are proportional to light, the right space for maths. | in the book text |
| Mix | Blend two values by a fraction; also called lerp. | in the glossary |
| step(edge, x) | Gives 0 below the edge and 1 from the edge up: a hard switch. | editor or docs |
| smoothstep(e0, e1, x) | Rises from 0 to 1 between two edges along a smooth S-curve. | editor or docs |
| clamp(x, lo, hi) | Holds a value inside a minimum and a maximum. | editor or docs |

## Shader verification

[Open the deck](decks/Terms%20-%20Shader%20verification.html) · 14 slides · 30 terms

| Term | Meaning | Tag |
|---|---|---|
| Evidence ladder | Five kinds of proof, each stronger than the last. | in the book text |
| Claim versus evidence | What is said works, versus a check that shows it. | in the book text |
| Observed versus inferred | Seen in your own run, versus guessed from it. | in the glossary |
| Compile error | The shader fails to build and prints an error. | in the glossary |
| Headless mode | A run with no window, so no pixels are drawn. | in the book text |
| Software renderer | Drawing on the CPU: same output on any machine. | in the glossary |
| Controlled input | Every input fixed, so a run can be repeated. | in the book text |
| Exposing input | Where right and wrong answers are far apart. | in the book text |
| Bench scene | A scene made to be looked at, inputs fixed. | in the book text |
| Test fixture | Fixed setup that a test starts from. | in the glossary |
| Pinned clock | A fixed frame rate: every frame the same length. | in the book text |
| Random seed | A fixed starting number so random results repeat. | in the glossary |
| Frame counter | A fade that counts frames, not game seconds. | in the book text |
| Assertion | A statement a test requires to be true. | in the glossary |
| source_color | A hint: this texture holds colour, so decode it. | in the book text |
| Flat normal texel | The pixel (128, 128, 255): a surface facing out. | in the book text |
| Premultiplied alpha | Colour already multiplied by its alpha. | in the book text |
| Golden image (also reference image) | A saved correct picture to compare renders with. | in the glossary |
| Pixel diff | A count of the pixels where two images differ. | editor or docs |
| Tolerance | The allowed gap between expected and actual. | in the book text |
| Per-platform reference | One reference per platform, as they differ slightly. | in the book text |
| False positive (also called a false pass) | A check passes though the thing is wrong. | in the glossary |
| False negative (also called a false fail) | A check fails though the thing is right. | in the glossary |
| CPU model | The spec written as arithmetic that runs headless. | in the book text |
| Test oracle | The source of the right answer a test compares to. | in the book text |
| Specification oracle | An oracle taken from the spec, not the code. | in the book text |
| Mutation check | Break the code on purpose; the test must fail. | in the book text |
| Test the test | A new check must fail on bad code, pass on good. | in the book text |
| Uniform value check | Compare a shader input's value with the spec. | in the book text |
| Scope violation | Changing something the brief said not to touch. | in the glossary |

## The Unity editor interface

[Open the deck](decks/Terms%20-%20Unity%20editor.html) · 17 slides · 32 terms

| Term | Meaning | Tag |
|---|---|---|
| Scene view | Where you look at the scene and edit it, through a free editor camera. | editor or docs |
| Game view | Shows what the scene's cameras render, as a player sees it. | editor or docs |
| Hierarchy | A tree of every GameObject in the open scene; drag one onto another to nest it. | editor or docs |
| Project window | A file browser for the project's Assets and Packages folders. | editor or docs |
| Inspector | Shows the components and settings of the selected object and lets you edit them. | editor or docs |
| Console | Messages, warnings and errors from your scripts and the editor. | editor or docs |
| Toolbar | The top strip: transform tools, pivot and handle toggles, Play, Pause and Step. | editor or docs |
| Layout and tabs | A saved arrangement of windows; drag tabs to dock them, or pick a layout at top right. | editor or docs |
| GameObject | Unity's object; does nothing until components are added. | in the glossary |
| Component | A piece of behaviour or data attached to a GameObject. | in the glossary |
| Local and world space | Local is relative to the parent object; world is relative to the whole level. | in the glossary |
| Pivot and Local handles | Pivot or Center sets where the handle sits; Local or Global sets how it points. | editor or docs |
| Scene gizmo | The axis widget at the Scene view's top right; click an axis to look along it. | editor or docs |
| Orbit, pan, zoom | Orbit turns around a point, pan slides the view, zoom changes the distance. | editor or docs |
| Flythrough | Hold the right mouse button and press W, A, S, D to move the camera itself. | editor or docs |
| Transform tools | Move, Rotate, Scale, Rect and Hand: the handles for changing a selection. | editor or docs |
| Play Mode | The editor runs the game inside itself; the Play button turns it on and off. | editor or docs |
| Play Mode changes lost | Edits to scene objects made during Play Mode are thrown away when you stop. | editor or docs |
| Enter Play Mode Options | A Project Settings choice to skip reloading code or scene when Play starts, so it starts faster. | editor or docs |
| Prefab | Unity's reusable object template; edits to it flow to every instance. | in the book text |
| Prefab Mode | Opens a prefab asset on its own so you edit the template, not one instance. | editor or docs |
| Overrides dropdown | Lists an instance's changes; Apply pushes one into the prefab, Revert drops it. | in the glossary |
| Tag | A text label on an object for lookup and filtering. | in the glossary |
| Layer | A numbered category, one per object, for rendering or collision filtering; set in the Layer dropdown at the top of the Inspector. | in the book text |
| Asset import settings | Per-asset options such as texture Max Size and compression, shown in the Inspector and saved in the .meta file. | in the book text |
| Package Manager | The window (Window menu) that adds, updates and removes packages; the list is saved in Packages/manifest.json. | editor or docs |
| Project Settings | Settings that belong to the project and are saved in it, such as Tags and Layers, Physics and Time. | editor or docs |
| Preferences | Settings that belong to you and your machine, such as colours, keys and the script editor. | editor or docs |
| Build Profiles | A saved set of build settings for one platform: target and scenes to include, kept as an asset. | in the book text |
| Animation window | Where you key properties over time to make an Animation Clip. | in the book text |
| Animator window | Where an Animator Controller's states and transitions are drawn and tested. | in the book text |
| Profiler | Records each frame's time by system (scripts, rendering, physics) to find what is slow. | in the book text |

## The Unreal Editor interface

[Open the deck](decks/Terms%20-%20Unreal%20editor.html) · 16 slides · 32 terms

| Term | Meaning | Tag |
|---|---|---|
| Level Viewport | The main window onto the level, where you see Actors and move them. | editor or docs |
| Perspective/orthographic | Perspective shows depth; orthographic drops it, so parallel edges stay parallel. | editor or docs |
| View modes | Ways to draw the same scene: Lit, Unlit, Wireframe and others. | editor or docs |
| Right-mouse fly | Hold the right mouse button and press W A S D to fly the viewport camera. | editor or docs |
| Content Browser | Where you browse, import and organize every asset in the project. | editor or docs |
| Content Drawer | A Content Browser that slides up from the bottom-left and hides when you click away. | editor or docs |
| Outliner | A tree of every Actor in the open level, which you can search and put in folders. | editor or docs |
| Details panel | Shows the properties and Components of the selected Actor, and lets you edit them. | editor or docs |
| World Settings | Settings for the open level as a whole, such as its Game Mode and Kill Z. | editor or docs |
| Place Actors panel | A palette of Actor types that you drag into the level. | editor or docs |
| Main toolbar | Save, mode switching, adding content, and the Play and Stop controls. | editor or docs |
| Play In Editor (PIE) | Running the game inside the editor. | in the glossary |
| Simulate | Runs the level's logic and physics with no player; you keep the editor camera. | editor or docs |
| Eject | While playing, release the player so you can fly the camera and select Actors. | editor or docs |
| PIE changes discarded | Edits made to Actors during play are thrown away when you stop; edits made before play stay. | editor or docs |
| Output Log | A window of messages from the editor and the game, with warnings and errors marked. | editor or docs |
| Actor and Component | An Actor is an object you can place in a level; a Component is a piece of behaviour or data attached to it. | in the glossary |
| Blueprint class | Unreal's reusable object template, built visually or in code. | in the glossary |
| Level and Levels window | A level is one playable space, saved as a map file; the Levels window lists the levels in the world. | in the glossary |
| .uasset and .umap | Binary asset and level files that a text tool cannot open or merge. | in the book text |
| Blueprint Editor | Opens on a Blueprint class: Components, My Blueprint, a Viewport, an Event Graph and Details. | editor or docs |
| Event Graph | The node-and-wire view of a Blueprint; white execution wires set the order. | in the glossary |
| Construction Script | A graph that runs when the Actor is built or changed in the editor, before play. | editor or docs |
| Material Editor | A node graph that builds a material; its result node takes Base Color and more. | editor or docs |
| Object type and response | Each object has a type, and a response to every other type: Block, Overlap or Ignore. | in the book text |
| Collision preset | A named bundle of responses, such as BlockAll, OverlapAll or NoCollision. | editor or docs |
| Niagara | Unreal's visual-effects system: a system holds emitters; an emitter is a stack of modules. | in the book text |
| Animation editors | Windows opened from animation assets: Sequence, Montage and Animation Blueprint. | editor or docs |
| Project Settings | Settings saved with the project and shared by everyone who opens it. | editor or docs |
| Editor Preferences | Settings for you and your copy of the editor, not saved with the project. | editor or docs |
| Plugins | Add-on modules you switch on or off per project; most need an editor restart. | editor or docs |
| Build and Package | Package Project turns the project into a runnable game for one platform. | editor or docs |

## Walker and the toolchain

[Open the deck](decks/Terms%20-%20Walker%20and%20the%20toolchain.html) · 14 slides · 26 terms

| Term | Meaning | Tag |
|---|---|---|
| Walker | The working method and its files: brief, build, playtest, inspect, revise, export. | in the book text |
| Repository | A project folder with its full version history. | in the book text |
| Commit | A saved snapshot in version history. | in the book text |
| Diff | The exact lines that changed between two versions. | in the book text |
| CLI and shell | You drive a program by typing commands; the shell (zsh, bash) reads them. | in the book text |
| Flag | An option on a command, such as --headless. | in the book text |
| Headless | Running with no window or display. | in the book text |
| Exit code | A number a program returns; 0 means success. | in the book text |
| Timeout | A limit after which a run is stopped. | in the book text |
| Hang | A run that never finishes. | in the book text |
| Import | Convert a source file into the form the engine uses. | in the book text |
| Cache | Stored results reused to save time, which can also go stale. | in the book text |
| Permission prompt | A question asking you to approve an action. | in the book text |
| Allow rule | A saved permission letting a command run without asking. | in the book text |
| Sandbox | A restricted environment where mistakes cannot reach the rest of the machine. | in the book text |
| Instruction file | A standing file of project rules the agent reads, such as CLAUDE.md or AGENTS.md. | in the book text |
| Spec | A written description of what must be built. | in the glossary |
| Checkable instruction | An instruction written so a check can pass or fail. | in the glossary |
| Claim versus evidence | A claim says what happened; evidence is proof that it did. | in the book text |
| Regression test | A test that guards a behaviour that worked before. | in the book text |
| Deterministic | The same inputs always give the same result. | in the book text |
| Flaky | Passes sometimes and fails sometimes with no change. | in the glossary |
| Game time | The simulation's clock, as opposed to the wall clock. | in the glossary |
| Fixed frame rate | Rendering locked to a set number of frames a second so runs match. | in the book text |
| Pinned time step | A constant step length forced on the simulation. | in the book text |
| Text versus binary scene | Readable scene files diff cleanly; opaque ones do not. | in the book text |

## How to make a walkthrough film: important terms

[Open the deck](decks/Terms%20-%20Walkthrough%20film.html) · 14 slides · 32 terms

| Term | Meaning | Tag |
|---|---|---|
| Walkthrough film | A narrated camera tour of a game or asset that shows what it does and says what it leaves out. | in the book text |
| Central idea | The one sentence every shot must serve; a shot that does not serve it is cut. | video only |
| Beat | One unit of the film: one picture, one idea, and the words spoken over it. | video only |
| Beat sheet (also the shot list: one row per shot) | The film as a table: each beat's picture, words and length, in order. | video only |
| Storyboard | Rough drawings of the key frames in order, made before anything is captured. | outside source |
| Script | The words of the narration, written out and checked before anyone records them. | video only |
| Voice-over | Narration heard over the pictures; the speaker is not shown in the shot. | video only |
| Pacing | How long each beat lasts, set by the route to cover and the time the words need. | video only |
| Shot | One continuous camera take, with a job and something it reveals that no earlier shot did. | video only |
| Route | The planned path the camera travels through the scene, measured before any frame is rendered. | video only |
| Waypoint | A point along the route where the camera passes, turns or stops. | in the glossary |
| Establishing shot | A wide opening shot that shows where everything is before the close looks. | outside source |
| Camera move | Pan, tilt, dolly, truck, orbit and the rest, defined in the Terms - Camera deck. | in the glossary |
| Route check | A script that steps every frame and measures speed, turn rate, roll and height. | video only |
| Real-time capture | Recording the game as it runs live, so frame times vary from frame to frame. | video only |
| Render | Computing each frame offline, as slowly as needed, then joining the frames into a film. | video only |
| Fixed frame rate | Every frame lasts exactly 1/fps seconds of game time, whatever the machine does. | in the book text |
| Deterministic capture | A capture that gives the same frames every take: fixed frame rate, same inputs, same route. | video only |
| Frame rate | How many frames are shown each second. | in the glossary |
| Frame count | Frame rate times duration: how many frames the film needs. | video only |
| Resolution | The width and height of a frame in pixels. | in the glossary |
| Aspect ratio | Width divided by height, such as 16:9 for a landscape film. | in the glossary |
| Cut and transition | A cut jumps to the next shot; a transition, such as a dissolve, overlaps the two. | outside source |
| B-roll | Extra footage laid over the main capture; the main footage carries the claim. | outside source |
| Title card | A full-screen card with the film's name, shown briefly at the start and end. | video only |
| Safe margins | The inner area, inset about 5% on each side, where text and logos must sit. | video only |
| Captions | The narration as text, burned in or in a separate .srt file with start and end times. | video only |
| Decibel (dB, dBFS) | Logarithmic loudness unit; in digital audio 0 dBFS is the maximum level. | in the glossary |
| Loudness (LUFS) | How loud the whole film is on average, measured against a target window. | video only |
| What it is not | A spoken and on-screen statement of what the film leaves out, placed in the first two shots. | video only |
| Call to action | The last request to the viewer: one concrete thing to try, with a way to check it. | video only |
| Claim versus evidence | A claim says what the film asserts; evidence is the capture or output on screen that backs it. | in the book text |

---

## Alphabetical index

| Term | Deck | Meaning |
|---|---|---|
| _physics_process | Godot: the editor, scenes, nodes, signals and movement | Runs at a fixed rate, 60 times a second by default. |
| _process | Godot: the editor, scenes, nodes, signals and movement | Runs once per rendered frame; the rate varies by machine. |
| _process, _physics_process | Godot, Unity and Unreal: the differences | Once per frame, and at a fixed 60 times a second by default. |
| --python-exit-code | Blender to Godot: MCP, export and measuring a prop | A flag that makes a script error end Blender with exit code 1, not 0. |
| .uasset and .umap | The Unreal Editor interface | Binary asset and level files that a text tool cannot open or merge. |
| [ASSUMPTION] | The game design document | A gap the draft filled in; nobody saw it. |
| [INFERRED] | The game design document | The code strongly implies it; the evidence is stated. |
| [MISSING] | The game design document | The code cannot tell you this. |
| [OBSERVED] | The game design document | The code does this; the tag names a file and line. |
| 2D, 3D and Script views | Godot: the editor, scenes, nodes, signals and movement | Tabs along the top: 2D and 3D edit scenes, Script edits code. |
| 3D viewport | Blender: the interface and modeling terms | The area where you see and edit the scene in 3D. |
| A* | Game AI: perception, movement and pathfinding | Pathfinding that picks the lowest f = g + h node first. |
| Acceptance criterion | The game design document | A concrete condition that must be true for work to count as done. |
| Accessibility | How to make a trailer for your game | Captions for speech and no rapid flashing, so more people can watch. |
| Active | Animation and interaction: state machines and blending | The frames in which an attack can hit. |
| Actor and Component | The Unreal Editor interface | An Actor is an object you can place in a level; a Component is a piece of behaviour or data attached to it. |
| Additive blending | Particles and VFX | Adds the new colour to what is behind it; glows and fire. |
| Admissible heuristic | Game AI: perception, movement and pathfinding | An estimate that never overestimates the true cost. |
| Advance mode | Animation and interaction: state machines and blending | Enabled: only travel() uses the transition. Auto: it fires by itself when its condition or expression is true. |
| Agency (autonomy) | Game design B: choices and challenge | The player takes control of how the game is played. |
| Agent | Game AI: perception, movement and pathfinding | A game character that senses and acts on its own. |
| Albedo | Materials and textures | The colour the surface reflects, before any lighting. |
| Alignment | Game AI: perception, movement and pathfinding | Steer to match neighbours' heading. |
| Allow rule | Walker and the toolchain | A saved permission letting a command run without asking. |
| Alpha channel | 2D art and sound assets in the engine | The extra channel storing opacity. |
| Ambient occlusion | Materials and textures | Darkening in creases where ambient light cannot reach; direct light is not affected. |
| amount | Particles and VFX | Particles in one emission cycle; a looping emitter never has more alive. |
| Analogous colours | Particles and VFX | Neighbouring hues, used to tie an effect to the model that casts it. |
| Anatomy | Art principles: concept art and character art | Knowing how bones and muscles work, so a sculpt is believable and can be animated. |
| AnimatedSprite2D | Animation foundations | A 2D node that plays a list of frames. Simpler than AnimationPlayer, which can key any property. |
| Animation Blueprint | Animation and interaction: state machines and blending | Unreal asset holding an animation state machine and logic. |
| Animation editors | The Unreal Editor interface | Windows opened from animation assets: Sequence, Montage and Animation Blueprint. |
| Animation resource | Animation foundations | Stored animation data: a length plus tracks of keys. It does nothing until a player plays it. |
| Animation tree | Animation and interaction: state machines and blending | Godot's graph of blends and state machines. |
| Animation window | The Unity editor interface | Where you key properties over time to make an Animation Clip. |
| animation_finished | Animation foundations | A signal sent when a clip ends. A looping clip does not send it. |
| AnimationLibrary | Animation foundations | A named collection of animations that a player holds. |
| AnimationPlayer | Animation and interaction: state machines and blending | Godot node that plays clips. |
| AnimationPlayer | Animation foundations | The node that plays animations by name. |
| Animator Controller | Animation and interaction: state machines and blending | Unity asset holding an animation state machine. |
| Animator window | The Unity editor interface | Where an Animator Controller's states and transitions are drawn and tested. |
| Anticipation | Animation: principles and character animation | A short wind-up that tells the player an action is coming. |
| Anticipation | Game design C: pacing and guidance | Prepare the player for what comes next, such as a wind-up before an attack. |
| Appeal | Game design A: what a game is | The pull to keep playing; it differs by game and by player. |
| Apply transforms | Blender: the interface and modeling terms | Bake position, rotation and scale into the mesh and reset them to neutral. |
| Apply transforms | Blender to Godot: MCP, export and measuring a prop | Bake position, rotation and scale into the mesh and reset them to neutral. |
| Arcs | Animation: principles and character animation | Limbs and thrown things move along curves, not straight lines. |
| Area of focus | Art principles: concept art and character art | The place in the image where the artist wants the eye to land. |
| Area snapshot | Godot: the editor, scenes, nodes, signals and movement | An Area's overlap list is updated once per physics step, so it can be a tick old. |
| Area2D | Godot: the editor, scenes, nodes, signals and movement | Detects overlaps and can emit signals; never blocks or pushes. |
| Arrive | Game AI: perception, movement and pathfinding | Seek and slow down to stop at the target. |
| Art style | Art principles: concept art and character art | A consistent look: colour, designs, shapes. |
| Art, design, engineering | Game design A: what a game is | They depend on each other; results are best when all three aim at the same target. |
| Aspect ratio | 2D art and sound assets in the engine | Width divided by height. |
| Aspect ratio | How to make a walkthrough film: important terms | Width divided by height, such as 16:9 for a landscape film. |
| Assertion | Shader verification | A statement a test requires to be true. |
| Asset import settings | The Unity editor interface | Per-asset options such as texture Max Size and compression, shown in the Inspector and saved in the .meta file. |
| Atmospheric perspective | Art principles: concept art and character art | Faraway things lose detail and contrast, which adds depth and guides the eye. |
| Audio track | Animation foundations | Plays a sound stream at a chosen time. |
| AudioStreamPlayer | 2D art and sound assets in the engine | Godot node that plays sound with no position. |
| Authority | Game AI: decisions, generation and systems | The part of the system allowed to change a value. |
| Autoload | Godot: the editor, scenes, nodes, signals and movement | A script or scene kept loaded across scene changes. |
| Autoload, Game Instance | Godot, Unity and Unreal: the differences | Things that outlive a scene: Godot autoload, Unity DontDestroyOnLoad, Unreal Game Instance. |
| Autoplay | Animation foundations | The animation a player starts by itself when its scene loads. |
| Axis conversion | Blender to Godot: MCP, export and measuring a prop | The exporter's +Y Up option turns Blender's Z extent into Godot's Y. |
| B-roll | How to make a walkthrough film: important terms | Extra footage laid over the main capture; the main footage carries the claim. |
| Backend limit | Animation foundations | Something a headless run cannot test, such as a captured mouse. It stays unverified. |
| Baked lighting | Materials and textures | Light and shadow stored in a texture or lightmap ahead of time. |
| Balance | Game design B: choices and challenge | Every advantage has a disadvantage; no role starts with an unfair edge. |
| Beat | How to make a walkthrough film: important terms | One unit of the film: one picture, one idea, and the words spoken over it. |
| Beat sheet | How to make a walkthrough film: important terms | The film as a table: each beat's picture, words and length, in order. |
| Beat structure | How to make a trailer for your game | The order of parts: hook, establish, escalate, peak, title, button, call to action. |
| Behavior tree | Game AI: decisions, generation and systems | A tree of nodes that decides what an agent does each tick. |
| Bench scene | Shader verification | A scene made to be looked at, inputs fixed. |
| Bevel | Blender: the interface and modeling terms | Turns a sharp edge or corner into a small slanted or rounded one. |
| Bezier track | Animation foundations | Fills a value in between keys along a hand-shaped curve. |
| Billboard | Particles and VFX | A flat quad that always faces the camera. |
| Bitmask | Godot: the editor, scenes, nodes, signals and movement | A number whose bits switch layers on or off; layer n has the value 2^(n−1). |
| Blackboard | Game AI: decisions, generation and systems | A shared memory of facts the AI reads and writes. |
| Blend space | Animation and interaction: state machines and blending | Clips placed on a line or a plane; a position between them mixes the nearest ones. |
| Blend tree | Animation and interaction: state machines and blending | A graph of nodes that mix clips by numbers your code writes. |
| Blend tree | Animation: principles and character animation | Weighted mix of clips driven by parameters. |
| Blueprint class | The Unreal Editor interface | Unreal's reusable object template, built visually or in code. |
| Blueprint Editor | The Unreal Editor interface | Opens on a Blueprint class: Components, My Blueprint, a Viewport, an Event Graph and Details. |
| Blueprint graph | Godot, Unity and Unreal: the differences | Unreal's visual scripting. The graph is a binary asset an agent cannot diff as text. |
| Bounding box | Blender to Godot: MCP, export and measuring a prop | The smallest axis-aligned box that holds an object. |
| BPM | How to make a trailer for your game | Beats per minute of the music; 60 divided by it is the seconds per beat. |
| bpy | Blender to Godot: MCP, export and measuring a prop | Blender's Python module; scripts and MCP tools both drive it. |
| Breadth-first search | Game AI: perception, movement and pathfinding | Expands outward one step at a time and ignores cost. |
| Build and export | Godot, Unity and Unreal: the differences | Godot saves export presets, Unity 6 saves a build profile, Unreal packages and cooks the project. |
| Build and Package | The Unreal Editor interface | Package Project turns the project into a runnable game for one platform. |
| Build Profiles | The Unity editor interface | A saved set of build settings for one platform: target and scenes to include, kept as an asset. |
| Build-up | Game design C: pacing and guidance | A sequence that raises tension toward an event: sound, sparks, camera shake. |
| Bus | 2D art and sound assets in the engine | A channel that sounds are routed through for shared volume and effects. |
| C# and MonoBehaviour | Godot, Unity and Unreal: the differences | Unity's language. A MonoBehaviour is a component script, also plain text. |
| C++ in Unreal | Godot, Unity and Unreal: the differences | Unreal's code route. Plain text, but it must be compiled before a change takes effect. |
| Cache | Walker and the toolchain | Stored results reused to save time, which can also go stale. |
| Call to action | How to make a trailer for your game | One thing to do next: wishlist, play, or follow a link. |
| Call to action | How to make a walkthrough film: important terms | The last request to the viewer: one concrete thing to try, with a way to check it. |
| Callback modes | Animation foundations | Settings for when animation updates (idle or physics) and when method keys run (deferred or now). |
| Camera limits | Terms: Camera | Clamps that keep the view inside the level. |
| Camera move | How to make a walkthrough film: important terms | Pan, tilt, dolly, truck, orbit and the rest, defined in the Terms - Camera deck. |
| canvas_item | Shaders: foundations | Godot shader type for 2D drawing: sprites, shapes, UI. |
| Captions | How to make a walkthrough film: important terms | The narration as text, burned in or in a separate .srt file with start and end times. |
| Central idea | How to make a walkthrough film: important terms | The one sentence every shot must serve; a shot that does not serve it is cut. |
| Channel packing | Materials and textures | Storing different maps in the red, green and blue channels of one image. |
| Character body | Godot, Unity and Unreal: the differences | The body you move on purpose: your script, or Unreal's movement component. |
| CharacterBody2D | Godot: the editor, scenes, nodes, signals and movement | Moved by your code; move_and_slide() slides it along what it hits. |
| Checkable instruction | Walker and the toolchain | An instruction written so a check can pass or fail. |
| Claim versus evidence | Shader verification | What is said works, versus a check that shows it. |
| Claim versus evidence | Walker and the toolchain | A claim says what happened; evidence is proof that it did. |
| Claim versus evidence | How to make a walkthrough film: important terms | A claim says what the film asserts; evidence is the capture or output on screen that backs it. |
| Claim versus measurement | Blender to Godot: MCP, export and measuring a prop | A claim is what a name or script says; a measurement is what a test reads from the file. |
| clamp(x, lo, hi) | Shaders: foundations | Holds a value inside a minimum and a maximum. |
| Clarity | Art principles: concept art and character art | The player can tell at once what is happening. |
| Clean footage | How to make a trailer for your game | Real play with debug clutter hidden and the HUD that explains a mechanic kept. |
| Clear progress | Game design A: what a game is | The player can see how close they are to the goal. |
| CLI and shell | Walker and the toolchain | You drive a program by typing commands; the shell (zsh, bash) reads them. |
| Climactic arc | Game design A: what a game is | Difficulty and tension build toward the goal's resolution. |
| Climax (peak) | How to make a trailer for your game | The biggest payoff, placed on a strong beat after a quiet drop. |
| Clip | Animation: principles and character animation | An authored animation: tracks of values over time. |
| Clip and player | Godot, Unity and Unreal: the differences | Keyed data played over time. Unity wraps even one clip in an Animator Controller. |
| Clipping | 2D art and sound assets in the engine | Distortion when a signal exceeds the maximum level. |
| Closing doors | Art principles: concept art and character art | Each round closes the options that failed. |
| Coherent noise | Game AI: decisions, generation and systems | Random values that change smoothly (Perlin, simplex). |
| Cohesion | Game AI: perception, movement and pathfinding | Steer toward the neighbours' centre. |
| Collection | Blender: the interface and modeling terms | A named group of objects you can hide, show or export together. |
| Collider | 2D art and sound assets in the engine | Shape used for contact tests; separate from the art and sized from the body. |
| Collision layer | Godot: the editor, scenes, nodes, signals and movement | Where an object is: the layers it appears in. |
| Collision mask | Godot: the editor, scenes, nodes, signals and movement | What an object scans: it detects B only if B is in a layer it scans. |
| Collision preset | The Unreal Editor interface | A named bundle of responses, such as BlockAll, OverlapAll or NoCollision. |
| Collision shape | Blender to Godot: MCP, export and measuring a prop | The simple shape physics uses, as opposed to the detailed mesh you see. |
| Collision shape | Godot: the editor, scenes, nodes, signals and movement | The geometry physics uses, separate from the drawn sprite. |
| COLOR | Shaders: foundations | Arrives as vertex colour times TEXTURE colour; what you leave in it is drawn. |
| Colour coding | Particles and VFX | Colours that signal team, damage type or tone. |
| Colour contrast | Art principles: concept art and character art | Strong colour or saturation differences. |
| Colour ramp | Particles and VFX | A gradient for particle colour over its life. |
| Colour texture | Materials and textures | A texture holding colours people see; only the base colour is one. |
| Commit | Walker and the toolchain | A saved snapshot in version history. |
| Communication | Game design C: pacing and guidance | Showing the player the goal and how to reach it, with clues in the environment. |
| Compile error | Shaders: foundations | The shader fails to build and gives an error message; a headless run still exits 0. |
| Compile error | Shader verification | The shader fails to build and prints an error. |
| Completeness Fallacy | The game design document | Decisions with no recorded reasoning. |
| Component | Godot, Unity and Unreal: the differences | A piece of behaviour or data attached to a GameObject or an Actor. |
| Component | The Unity editor interface | A piece of behaviour or data attached to a GameObject. |
| Components | Game design A: what a game is | The objects in the space that players use or meet: characters, weapons, vehicles. |
| Compute shader | Game AI: decisions, generation and systems | A GPU program run over many cells at once, outside the drawing pipeline. |
| Concept art | Art principles: concept art and character art | Early drawings that solve a design problem for the team, not finished art. |
| Condition | Animation and interaction: state machines and blending | A test on a parameter that must hold for a transition. |
| Condition and action | Game AI: decisions, generation and systems | A condition asks a question; an action does the work and may keep running. |
| Conduit | Animation and interaction: state machines and blending | A hub that joins many states to many with one set of transitions. |
| Consistent rules | Game design C: pacing and guidance | Even where physics is bent, it is bent the same way every time. |
| Console | The Unity editor interface | Messages, warnings and errors from your scripts and the editor. |
| Constraint | Art principles: concept art and character art | A limit that narrows what the artist designs. |
| Construction Script | The Unreal Editor interface | A graph that runs when the Actor is built or changed in the editor, before play. |
| Constructive generation | Game AI: decisions, generation and systems | Build content by rules that guarantee validity. |
| Content Browser | The Unreal Editor interface | Where you browse, import and organize every asset in the project. |
| Content Drawer | The Unreal Editor interface | A Content Browser that slides up from the bottom-left and hides when you click away. |
| Contrast | Art principles: concept art and character art | A difference that pulls the eye to one place. |
| Controlled input | Shader verification | Every input fixed, so a run can be repeated. |
| Convex and concave | Blender to Godot: MCP, export and measuring a prop | Convex has no dents: a line between two inside points stays inside. Concave has a hollow. |
| Core loop | Game design A: what a game is | The repeated moment-to-moment cycle the player enjoys. |
| Core loop | The game design document | The repeated moment-to-moment cycle the player enjoys. |
| Core mechanic | Game design A: what a game is | The action players do over and over again. |
| CPU model | Shader verification | The spec written as arithmetic that runs headless. |
| CPUParticles2D / 3D | Particles and VFX | Simulated on the processor; wider hardware support, fewer particles. |
| Cross-fade | Animation and interaction: state machines and blending | Blend smoothly from one clip to the next over a short time. |
| Cubic | Animation: principles and character animation | A smooth curve through the keys, with no corner at a key. |
| Cut and transition | How to make a walkthrough film: important terms | A cut jumps to the next shot; a transition, such as a dissolve, overlaps the two. |
| Cut on action | How to make a trailer for your game | Cut while the motion is under way, so the eye carries across the cut. |
| Cut on the beat | How to make a trailer for your game | Place cuts on the music's beats so picture and sound lock together. |
| Cut, defer, swap | The game design document | The three ways to handle too much scope: remove, postpone, replace. |
| Cycle (walk, run) | Animation: principles and character animation | One full stride that repeats; the first and last poses match. |
| Damping | Particles and VFX | The rate at which particles lose velocity. 100 takes a speed of 100 to 0 in 1 second. |
| Data asset | Godot, Unity and Unreal: the differences | Shared data kept as a file: Godot Resource, Unity ScriptableObject, Unreal Data Asset. |
| Data texture | Materials and textures | A texture whose numbers are the values, such as normals or roughness. |
| Deadzone | Terms: Camera | Screen region where the target can move without the camera moving. |
| Decibel | 2D art and sound assets in the engine | Logarithmic loudness unit. |
| Decibel (dB, dBFS) | How to make a walkthrough film: important terms | Logarithmic loudness unit; in digital audio 0 dBFS is the maximum level. |
| Decisions | Game design A: what a game is | The ways the player can get past the opposition. |
| Descriptive play | Game design B: choices and challenge | The player acts and sees the game respond: the bola hits, the ice shatters. |
| Design pillar | The game design document | A core principle every decision must support. |
| Design the middle first | Game design C: pacing and guidance | Build the engaging middle levels, then the opening levels that lead there. |
| Details panel | The Unreal Editor interface | Shows the properties and Components of the selected Actor, and lets you edit them. |
| Determinism | Game AI: decisions, generation and systems | Same inputs and seed give the same output every run. |
| Deterministic | Walker and the toolchain | The same inputs always give the same result. |
| Deterministic capture | How to make a walkthrough film: important terms | A capture that gives the same frames every take: fixed frame rate, same inputs, same route. |
| Diff | Walker and the toolchain | The exact lines that changed between two versions. |
| Difficulty | Game design B: choices and challenge | How hard the opposition is; it is separate from fairness. |
| Dijkstra | Game AI: perception, movement and pathfinding | Pathfinding that expands by cost so far only, with no heuristic. |
| Dimensions | Blender to Godot: MCP, export and measuring a prop | An object's size in metres on each axis, as Blender reports it. |
| Direct state write | The game design document | Setting a value in code instead of producing it through gameplay. |
| Discount factor | Game AI: decisions, generation and systems | How much future reward is worth compared to now. |
| Dolly | Terms: Camera | Move the camera forward or backward along its view direction. |
| Dolly in / dolly out | Terms: Camera | Move the camera toward / away from the subject. Dolly in moves toward the subject, dolly out moves away. |
| Dolly versus zoom | Terms: Camera | A dolly changes parallax (near and far shift against each other); a zoom only magnifies. |
| Downtime | Game design B: choices and challenge | Time a player waits with nothing to do. |
| Draft | The game design document | Write a GDD from a new idea and mark what you assumed. |
| Dynamic | Game design C: pacing and guidance | Many things happening at once, so play stays fresh. |
| Ease-in | Animation: principles and character animation | Slow start, then it speeds up. |
| Ease-out | Animation: principles and character animation | Fast start, then it slows to a stop. |
| Easing | Animation foundations | The speed curve of a change: slow start (ease-in) or slow end (ease-out). |
| Easing | Animation: principles and character animation | The speed curve of a change (ease-in slow start, ease-out slow end). |
| Edge | Blender: the interface and modeling terms | A line joining two vertices. |
| Edit Mode | Blender: the interface and modeling terms | Work on the mesh itself: its vertices, edges and faces. |
| Editor Preferences | The Unreal Editor interface | Settings for you and your copy of the editor, not saved with the project. |
| Eject | The Unreal Editor interface | While playing, release the player so you can fly the camera and select Actors. |
| Emergent behavior | Game AI: perception, movement and pathfinding | Complex group behaviour from simple rules. |
| Emission | Materials and textures | Light the surface gives off itself. |
| Emission shape | Particles and VFX | The volume particles spawn in: point, sphere, box. |
| Emitter | Particles and VFX | The thing that spawns particles. |
| Enter Play Mode Options | The Unity editor interface | A Project Settings choice to skip reloading code or scene when Play starts, so it starts faster. |
| Epsilon-greedy | Game AI: decisions, generation and systems | Take a random action with probability epsilon, otherwise the best known one. |
| Establishing shot | How to make a walkthrough film: important terms | A wide opening shot that shows where everything is before the close looks. |
| Euclidean distance | Game AI: perception, movement and pathfinding | Straight-line distance. |
| Evaluative play | Game design B: choices and challenge | The player steps back and asks why this action matters to the whole game. |
| Event Dispatcher | Godot, Unity and Unreal: the differences | Unreal's Blueprint form of a signal. One Call fires every bound event; C++ uses a delegate. |
| Event Graph | The Unreal Editor interface | The node-and-wire view of a Blueprint; white execution wires set the order. |
| Event key | Godot, Unity and Unreal: the differences | A call placed on the timeline. An Anim Notify State has a begin and an end. |
| Event-driven | Godot: the editor, scenes, nodes, signals and movement | Code runs only when something announces that it happened. |
| Evidence ladder | Shader verification | Five kinds of proof, each stronger than the last. |
| Exit code | Walker and the toolchain | A number a program returns; 0 means success. |
| Exit-time transition | Animation and interaction: state machines and blending | A transition that waits for the clip to reach a set point. |
| explosiveness | Particles and VFX | 0 spreads births across the cycle; 1 emits them all at its start. |
| Export preset, template | Godot: the editor, scenes, nodes, signals and movement | A preset is the recipe for one platform; the template is the prebuilt engine it packs your data into. |
| Exposing input | Shader verification | Where right and wrong answers are far apart. |
| f, g, h | Game AI: perception, movement and pathfinding | Total estimated cost / cost so far / estimated cost to goal. |
| FABRIK | Animation foundations | An IK solver that moves a chain back and forth between target and root until it fits. |
| Face | Blender: the interface and modeling terms | A flat surface bounded by edges. |
| Fairness | Game design B: choices and challenge | Clear expectations and consistent design, so the player can learn from failing. |
| False negative | Shader verification | A check fails though the thing is right. |
| False pass | The game design document | A test that passes though the behaviour is wrong. |
| False positive | Shader verification | A check passes though the thing is wrong. |
| Field of view (FOV) | Terms: Camera | The lens angle; wider shows more. |
| Field-of-view cone | Game AI: perception, movement and pathfinding | The angle across which the agent can see. |
| FileSystem dock | Godot: the editor, scenes, nodes, signals and movement | Lists every file in the project, under res://. |
| Finite state machine | Game AI: decisions, generation and systems | A set of states with transitions; one is active. |
| Fixed frame rate | Animation foundations | --fixed-fps n: every frame advances game time by exactly 1/n s. |
| Fixed frame rate | How to make a trailer for your game | Rendering locked to a set number of frames a second so runs match. |
| Fixed frame rate | Walker and the toolchain | Rendering locked to a set number of frames a second so runs match. |
| Fixed frame rate | How to make a walkthrough film: important terms | Every frame lasts exactly 1/fps seconds of game time, whatever the machine does. |
| fixed_fps, interpolate | Particles and VFX | Update at a fixed rate; interpolate smooths motion between updates. |
| Fixed-function | Shaders: foundations | Old hardware steps that could be configured but not programmed. |
| Flag | Walker and the toolchain | An option on a command, such as --headless. |
| Flaky | Walker and the toolchain | Passes sometimes and fails sometimes with no change. |
| Flat normal texel | Shader verification | The pixel (128, 128, 255): a surface facing out. |
| Flee | Game AI: perception, movement and pathfinding | Steer away from a target. |
| Flicker | Game AI: decisions, generation and systems | Rapid back-and-forth switching between states. |
| Flipped normals | Blender: the interface and modeling terms | Faces pointing inward, so they look dark or vanish. |
| Flythrough | The Unity editor interface | Hold the right mouse button and press W, A, S, D to move the camera itself. |
| Focal length | Terms: Camera | Lens strength in millimetres; longer means narrower view and more magnification. |
| Follow camera | Terms: Camera | Tracks a moving target, usually with smoothing. |
| Follow-through, overlap | Animation: principles and character animation | Parts keep moving after the body stops, each settling at its own time. |
| Forward kinematics (FK) | Animation: principles and character animation | Rotate joints parent-to-child to place the hand. |
| Fragment | Shaders: foundations | A candidate pixel colour produced by rasterization for one covered screen position. |
| Fragment (pixel) shader | Shaders: foundations | Runs per pixel; sets colour (tint, glint). |
| Frame count | How to make a walkthrough film: important terms | Frame rate times duration: how many frames the film needs. |
| Frame counter | Shader verification | A fade that counts frames, not game seconds. |
| Frame rate | 2D art and sound assets in the engine | Frames shown per second. |
| Frame rate | Animation: principles and character animation | Frames shown per second. |
| Frame rate | How to make a trailer for your game | Frames shown per second. |
| Frame rate | How to make a walkthrough film: important terms | How many frames are shown each second. |
| Fringe (halo) | 2D art and sound assets in the engine | The halo of edge colour left around a cutout; fix_alpha_border removes it. |
| Frustration | Game design B: choices and challenge | Some is part of challenge; it has to be the kind the player can learn from. |
| Game | Game design A: what a game is | An activity that has all four: a goal, opposition, decisions and rules. |
| Game brief | The game design document | What the player does, what success is, what can go wrong, what is out. |
| Game time | Walker and the toolchain | The simulation's clock, as opposed to the wall clock. |
| Game view | The Unity editor interface | Shows what the scene's cameras render, as a player sees it. |
| GameObject | The Unity editor interface | Unity's object; does nothing until components are added. |
| Gameplay video | How to make a trailer for your game | Plain footage of play, made to cover, not sell. |
| Gameplay vs cinematic | How to make a trailer for your game | Captured play from the real build; a cinematic must be the game's own and labelled. |
| Games can cheat | Game design C: pacing and guidance | Hidden help the player does not notice, such as enemies told not to turn around. |
| Gate | The game design document | A named sign-off after a design phase; only a person signs it. |
| GDD | The game design document | What the game is and how it plays, in enough detail to build it and test it. |
| GDScript | Godot, Unity and Unreal: the differences | Godot's own scripting language. Scripts are plain text files. |
| Generate-and-test | Game AI: decisions, generation and systems | Make content randomly, then reject what fails. |
| get_current_node() | Animation and interaction: state machines and blending | The playback's reading of the current state. During a cross-fade it already names the new state. |
| Ghost Center | The game design document | No locked vision, so nothing anchors the decisions. |
| Given-when-then | The game design document | A format for a test: starting state, action, expected result. |
| GLB | Blender to Godot: MCP, export and measuring a prop | glTF packed into a single binary file. |
| Global illumination | Materials and textures | Light that bounces off surfaces and lights others; Godot has several techniques. |
| glTF | Blender to Godot: MCP, export and measuring a prop | An open 3D format; the preferred exchange format for engines. |
| Goal | Game design A: what a game is | The objective the player works toward. |
| GOAP | Game AI: decisions, generation and systems | Goal-oriented action planning: search for actions that reach a goal. |
| Godot shading language | Shaders: foundations | Based on GLSL but simplified; the ideas carry over between dialects. |
| Golden image | Shader verification | A saved correct picture to compare renders with. |
| GPUParticles2D / 3D | Particles and VFX | Simulated on the graphics card; many particles, more features. |
| Graph, edge, weight | Game AI: perception, movement and pathfinding | Points (nodes) joined by edges, each with a cost. |
| Gravity | Particles and VFX | Constant downward acceleration applied to particles. |
| Green channel convention | Materials and textures | Whether green points up (OpenGL, Godot) or down (DirectX). |
| Grid (AStarGrid2D) | Game AI: perception, movement and pathfinding | Cells marked solid or free; the light tool for grid games. |
| Group | Godot: the editor, scenes, nodes, signals and movement | A named tag on nodes; one call reaches every node in it. |
| Guiding the focus | Game design C: pacing and guidance | Making clear what the player should concentrate on. |
| Hang | Walker and the toolchain | A run that never finishes. |
| HDRP mask map | Materials and textures | Unity HDRP's packed map: red metallic, green AO, blue detail mask, alpha smoothness. |
| Headless | Walker and the toolchain | Running with no window or display. |
| Headless Blender | Blender to Godot: MCP, export and measuring a prop | Running Blender with no window, from the command line. |
| Headless mode | Shader verification | A run with no window, so no pixels are drawn. |
| Headroom | 2D art and sound assets in the engine | Spare level left below the maximum. |
| Hearing (noise) radius | Game AI: perception, movement and pathfinding | How far a noise carries to an agent. |
| Heightmap | Game AI: decisions, generation and systems | A grid with one height value per position. |
| Hierarchy | The Unity editor interface | A tree of every GameObject in the open scene; drag one onto another to nest it. |
| High-poly and low-poly | Blender to Godot: MCP, export and measuring a prop | A very detailed sculpt, and the cheap copy of it that the engine runs. |
| High-poly sculpt | Art principles: concept art and character art | A very detailed sculpt, too heavy for the engine. |
| hint_range | Shaders: foundations | Gives the Inspector a slider; does not clamp values set from code. |
| Hit list | Animation and interaction: state machines and blending | The record of targets already hit so one swing hits each once. |
| Honest trailer | How to make a trailer for your game | Shows only what the game really does; planned features never appear. |
| Hook | How to make a trailer for your game | The most distinctive thing the player does, said in one sentence. |
| House rules | Game design A: what a game is | Rules a group changes for its own table; they change how the game plays. |
| Hysteresis | Game AI: decisions, generation and systems | Different thresholds for switching on and off, to stop rapid switching. |
| Iconic elements | Art principles: concept art and character art | The few features that keep a character recognisable even when tiny on screen. |
| Ideation | Art principles: concept art and character art | Many quick, rough ideas before choosing one. |
| Implementation Void | The game design document | A mechanic with only the happy path written down. |
| Import | Walker and the toolchain | Convert a source file into the form the engine uses. |
| Import file (.import) | Blender to Godot: MCP, export and measuring a prop | The text file beside a model whose settings decide what Godot builds. |
| Import settings | 2D art and sound assets in the engine | Per-asset options controlling how the engine converts it, kept in the .import file. |
| In-place | Animation: principles and character animation | The clip stays on the spot; code does the travel. |
| Initial velocity | Particles and VFX | The speed and direction a particle starts with. |
| Input action | Godot, Unity and Unreal: the differences | A named intent such as jump, bound to keys or buttons and kept apart from them. |
| Input action | Godot: the editor, scenes, nodes, signals and movement | A named intent such as jump, bound to keys or buttons. |
| Input probe | Animation and interaction: state machines and blending | A script that loads the real scene, presses only ordinary actions and records what happens. |
| Inspector | Godot: the editor, scenes, nodes, signals and movement | The editor panel for viewing and editing properties. |
| Inspector | The Unity editor interface | Shows the components and settings of the selected object and lets you edit them. |
| Instance | Godot, Unity and Unreal: the differences | One live copy made from a template. |
| Instance | Godot: the editor, scenes, nodes, signals and movement | One live copy of a saved scene; a change on one instance overrides the template. |
| Instruction file | Walker and the toolchain | A standing file of project rules the agent reads, such as CLAUDE.md or AGENTS.md. |
| Integer scaling | 2D art and sound assets in the engine | Scaling by whole numbers so pixel art stays crisp. |
| Intermittent fault | Animation and interaction: state machines and blending | A bug that appears only sometimes. |
| Interpolation | Animation foundations | How values are filled in between keys: nearest, linear or cubic. |
| Interpolation | Animation: principles and character animation | Computing the in-between values. |
| Interpolation (shader) | Shaders: foundations | Smoothly blending vertex values across a triangle's fragments. |
| Interrupt | Animation and interaction: state machines and blending | A transition that cuts off the current state early. |
| Invariant | The game design document | A condition that must stay true throughout. |
| Inverse kinematics | Animation foundations | Choose a target and compute the joint angles that reach it. |
| Inverse kinematics (IK) | Animation: principles and character animation | Give a target and the solver works out the joint angles. |
| Iteration | Art principles: concept art and character art | Repeat draft, feedback and change. |
| Just-pressed vs held | Godot: the editor, scenes, nodes, signals and movement | Just-pressed is true only on the tick a press began; held stays true while down. |
| Key | Animation foundations | One point on a track: a time, a value and an easing value. |
| Key art | How to make a trailer for your game | The one still image that stands for the game: title, character, idea. |
| Keyframe | Animation: principles and character animation | A stored value at a specific time. |
| Kill a tween | Animation foundations | Abort a tween where it is. It stops short of its end value. |
| Last known position | Game AI: perception, movement and pathfinding | Where the target was last seen, kept in memory. |
| Layer | The Unity editor interface | A numbered category, one per object, for rendering or collision filtering; set in the Layer dropdown at the top of the Inspector. |
| Layer and mask | Godot, Unity and Unreal: the differences | Each object has a layer and a mask. A notices B if B's layer is in A's mask: one way. |
| Layer Collision Matrix | Godot, Unity and Unreal: the differences | One layer per GameObject. A project-wide grid says which pairs of layers collide. |
| Layout and tabs | The Unity editor interface | A saved arrangement of windows; drag tabs to dock them, or pick a layout at top right. |
| Level and Levels window | The Unreal Editor interface | A level is one playable space, saved as a map file; the Levels window lists the levels in the world. |
| Level design | Game design C: pacing and guidance | Planning and building the spaces the player moves through. |
| Level Viewport | The Unreal Editor interface | The main window onto the level, where you see Actors and move them. |
| Licence | Godot, Unity and Unreal: the differences | Godot is MIT. Unity is proprietary. Unreal is source-available, not open source. |
| lifetime | Particles and VFX | Seconds a particle lives; also the length of one emission cycle. |
| Light and dark contrast | Art principles: concept art and character art | The gap between light and dark areas. |
| Lighting | Materials and textures | Light and camera turn the material's quantities into the colour you see. |
| Line of sight | Game AI: perception, movement and pathfinding | A straight line to the target that nothing blocks. |
| Linear | Animation: principles and character animation | Constant rate of change. |
| Linear and decoding | Materials and textures | Values proportional to light. Colour is decoded to linear first; data must not be. |
| Linear and nonlinear | Game design C: pacing and guidance | Straight from start to end, or with alternate choices along the way. |
| Linear vs sRGB | Shaders: foundations | sRGB is the encoding for images shown to people; linear values are proportional to light, the right space for maths. |
| Linked test | The game design document | A test row that names the mechanic it checks. |
| Local and global space | Blender: the interface and modeling terms | Local coordinates are measured from the object's origin; global ones from the scene's. |
| Local and world space | The Unity editor interface | Local is relative to the parent object; world is relative to the whole level. |
| Local avoidance | Game AI: perception, movement and pathfinding | Steering around nearby obstacles and agents. |
| local_coords | Particles and VFX | On: particles move with the emitter. Off: they are left behind. |
| LOD | Blender to Godot: MCP, export and measuring a prop | Level of detail: cheaper versions of a model swapped in at distance. |
| Logical events | Game design C: pacing and guidance | Events behave sensibly and meet the player's unspoken expectations. |
| Logline | How to make a trailer for your game | The game in one sentence: who does what, and what is new. |
| Logo sting | How to make a trailer for your game | A very short logo animation with a sound; better at the end than the start. |
| Look-ahead | Terms: Camera | Shifts framing toward the direction of travel. |
| Look-at | Animation foundations | Turn one bone to face a target. No chain is solved. |
| Loop | Animation and interaction: state machines and blending | A clip that repeats. |
| Loop | Animation: principles and character animation | A clip that starts again from its first frame when it ends. |
| Loop mode | Animation foundations | Whether a clip plays once, loops or ping-pongs. |
| Loop point | 2D art and sound assets in the engine | Where a looping sound jumps back to; WAV has begin and end, Ogg only a start offset. |
| Loop seam | Animation foundations | A jump where the last value meets the first on a loop. Test that they match. |
| Loop seam | Animation: principles and character animation | A visible jump where the last frame meets the first. |
| Lossless vs lossy | 2D art and sound assets in the engine | Exact reconstruction versus smaller files with lost detail. |
| Loudness (LUFS) | How to make a walkthrough film: important terms | How loud the whole film is on average, measured against a target window. |
| Low-poly mesh | Art principles: concept art and character art | A simplified copy with far fewer polygons. |
| Luck and skill | Game design B: choices and challenge | Luck: chance decides. Skill: the player's ability decides. Games mix the two. |
| Main toolbar | The Unreal Editor interface | Save, mode switching, adding content, and the Play and Stop controls. |
| Manhattan distance | Game AI: perception, movement and pathfinding | Distance counted along grid axes only. |
| Map slot naming | Materials and textures | The agreed names for each texture slot, such as albedo, normal, roughness. |
| Material | Materials and textures | A stack of textures and numbers that says how a surface looks. |
| Material | Shaders: foundations | A shader plus its parameter values and textures. |
| Material Editor | The Unreal Editor interface | A node graph that builds a material; its result node takes Base Color and more. |
| Material parameter | Godot, Unity and Unreal: the differences | A named value that your code sets and the shader reads. |
| Material through export | Blender to Godot: MCP, export and measuring a prop | A named Blender material arrives under the same name; Blender-only nodes do not. |
| Material versus texture | Blender: the interface and modeling terms | A material is the full surface recipe; a texture is one image it uses. |
| MCP | Blender to Godot: MCP, export and measuring a prop | A standard way for an AI app to call tools in another program such as Blender. |
| MCP server and add-on | Blender to Godot: MCP, export and measuring a prop | A relay the agent starts; an add-on inside Blender receives its calls. |
| MCP tool | Blender to Godot: MCP, export and measuring a prop | A named action the agent may call, with typed arguments. |
| Meaningful choice | Game design B: choices and challenge | A choice that changes what happens and that the player has to think about. |
| Meaningful play | Game design B: choices and challenge | The player acts and the game responds in a way that matters. |
| Mechanic | Game design A: what a game is | A rule-governed action in the game. |
| Mechanic | The game design document | A rule-governed action in the game. |
| Mechanic Mirage | The game design document | A PX goal that is really a feature described in disguise. |
| Mechanics constraint | Art principles: concept art and character art | A limit from rules and numbers, such as health. |
| Mesh | Blender: the interface and modeling terms | The vertices, edges and faces that make a 3D shape; the chapter calls it mesh data. |
| Metallic | Materials and textures | Whether the surface behaves like a metal: 0 is non-metal, 1 is metal. |
| Method track | Animation and interaction: state machines and blending | A track that calls a function when the playhead reaches a key. |
| Method track | Animation foundations | Calls a function at chosen times. Does not fire when you scrub in the editor. |
| Mipmap | Materials and textures | One of the pre-shrunk copies of a texture; without them, distant surfaces shimmer. |
| Mipmaps | 2D art and sound assets in the engine | Pre-shrunk copies of a texture used when drawn small; about 33% more memory. |
| Mirror modifier | Blender: the interface and modeling terms | Copies the mesh across an axis, so you model one half. |
| Mix | Shaders: foundations | Blend two values by a fraction; also called lerp. |
| Modifier | Blender: the interface and modeling terms | A live step that changes a mesh without editing it. |
| Mood board | Art principles: concept art and character art | A set of reference images showing the theme and tone, shown to the team early. |
| Movement pattern | Game design A: what a game is | How a character moves gives it personality: a hop is a frog, a wave is a snake. |
| Movie Maker mode | How to make a trailer for your game | Godot's mode that records a run to a video file, frame by frame. |
| Music drop | How to make a trailer for your game | A quiet moment just before the peak, so the peak lands. |
| Mutation check | Animation and interaction: state machines and blending | Put the old broken version back and run the new test; it must fail. |
| Mutation check | Shader verification | Break the code on purpose; the test must fail. |
| Muted test | How to make a trailer for your game | Check that the film still makes sense with the sound off. |
| Name suffix | Blender to Godot: MCP, export and measuring a prop | A tail on a mesh name, such as -convcolonly, that tells Godot to build collision. |
| Naming conventions | Blender to Godot: MCP, export and measuring a prop | Agreed rules for how files and objects are named. |
| Navigation mesh | Game AI: perception, movement and pathfinding | Polygons marking where agents can walk. |
| NavigationAgent2D | Game AI: perception, movement and pathfinding | Godot node that follows a navmesh path. |
| Nearest vs linear | 2D art and sound assets in the engine | Nearest reads one texel and keeps hard edges; linear blends four and smooths. |
| Neutral pose | Art principles: concept art and character art | The default pose a model is built in; some designs fail once the character moves. |
| Niagara | The Unreal Editor interface | Unreal's visual-effects system: a system holds emitters; an emitter is a stack of modules. |
| Node | Godot: the editor, scenes, nodes, signals and movement | The smallest building block: one object doing one job. |
| Node dock | Godot: the editor, scenes, nodes, signals and movement | Shows the selected node's signals and groups. |
| Node scale | Blender to Godot: MCP, export and measuring a prop | A scale left on the node instead of baked into the mesh. |
| Node, GameObject, Actor | Godot, Unity and Unreal: the differences | One object in the scene. A GameObject does nothing until components are added. |
| Normal | Blender: the interface and modeling terms | The direction a surface faces. |
| Normal map | Materials and textures | Per-pixel surface direction that fakes bumps in the lighting; red, green, blue are X, Y, Z. |
| Novelist's Trap | The game design document | Story written for a reader, not for an engineer. |
| Nyquist limit | 2D art and sound assets in the engine | The highest frequency a sample rate can hold: half the rate. |
| Object Mode | Blender: the interface and modeling terms | Work on whole objects: move, rotate, scale. |
| Object type and response | The Unreal Editor interface | Each object has a type, and a response to every other type: Block, Overlap or Ignore. |
| Object Type, response | Godot, Unity and Unreal: the differences | Block, Overlap or Ignore for every type. Both sides must agree before contact happens. |
| Observed versus inferred | Shader verification | Seen in your own run, versus guessed from it. |
| Octave | Game AI: decisions, generation and systems | One layer of noise at a set scale, added to others. |
| one_shot | Particles and VFX | Only one emission cycle occurs; otherwise it loops forever. |
| One-shot | 2D art and sound assets in the engine | Plays once and stops. |
| OneShot | Animation and interaction: state machines and blending | A blend-tree node that plays a clip once over whatever is below it, then returns. |
| Open and closed set | Game AI: perception, movement and pathfinding | Open: found, not yet expanded. Closed: already expanded. |
| Opposition | Game design A: what a game is | Obstacles the player must overcome; it makes a game fun and can frustrate. |
| Orbit | Terms: Camera | Move around a subject on a curved path while keeping it framed. |
| Orbit, pan, zoom | The Unity editor interface | Orbit turns around a point, pan slides the view, zoom changes the distance. |
| Origin | Blender: the interface and modeling terms | The point an object's position and rotation are measured from. |
| Origin and pivot | Blender to Godot: MCP, export and measuring a prop | The point position and rotation are measured from; the pivot is what it rotates and scales around. |
| ORM | Materials and textures | A packed map: occlusion in red, roughness in green, metallic in blue. |
| Out of scope | The game design document | A written list of what will not be built. |
| Outliner | Blender: the interface and modeling terms | A tree listing every object and collection in the scene. |
| Outliner | The Unreal Editor interface | A tree of every Actor in the open level, which you can search and put in folders. |
| Output and Debugger | Godot: the editor, scenes, nodes, signals and movement | Bottom panels: Output shows printed text, Debugger shows errors. |
| Output Log | The Unreal Editor interface | A window of messages from the editor and the game, with warnings and errors marked. |
| Override | Godot, Unity and Unreal: the differences | A change on one instance. In Unity, Apply pushes it into the Prefab and Revert drops it. |
| Overrides dropdown | The Unity editor interface | Lists an instance's changes; Apply pushes one into the prefab, Revert drops it. |
| Pacing | Game design C: pacing and guidance | Alternating intense and calm moments. |
| Pacing | How to make a trailer for your game | How fast the cuts come; it follows how well the viewer understands the game. |
| Pacing | How to make a walkthrough film: important terms | How long each beat lasts, set by the route to cover and the time the words need. |
| Package Manager | The Unity editor interface | The window (Window menu) that adds, updates and removes packages; the list is saved in Packages/manifest.json. |
| Pan | Terms: Camera | Turn left or right on the spot; position unchanged. |
| Parallax | Terms: Camera | Nearer things shift more than farther things when the viewpoint moves. |
| Parameter | Animation and interaction: state machines and blending | A tunable number on the tree, addressed by a path; code drives the tree by writing it. |
| Particle | Particles and VFX | One small short-lived sprite or mesh in an effect. |
| Particle shader | Particles and VFX | A shader that sets each particle's properties in start() and process(). |
| Particle system | Godot, Unity and Unreal: the differences | Many small sprites simulated together. A one-shot burst spawns them all at once. |
| Particle system | Particles and VFX | The emitter plus the rules for its particles. |
| ParticleProcessMaterial | Particles and VFX | The resource that holds a GPU particle system's rules for moving and changing. |
| Path smoothing | Game AI: perception, movement and pathfinding | Cut corners from a path wherever the straight line is clear. |
| PBR | Materials and textures | Physically based rendering: a few measured quantities per pixel, so a material holds up under any light. |
| PCM | 2D art and sound assets in the engine | Uncompressed digital audio samples. |
| Pedestal | Terms: Camera | Move the camera straight up or down, still facing the same way. |
| Per-platform reference | Shader verification | One reference per platform, as they differ slightly. |
| Permission prompt | Walker and the toolchain | A question asking you to approve an action. |
| Persistence | Game design B: choices and challenge | The player lives with the consequences of a choice for a set time. |
| Personalisation | Game design B: choices and challenge | Players build their own play style from the decisions they make. |
| Perspective / orthographic | Terms: Camera | Distant things shrink / size does not depend on distance. |
| Perspective constraint | Art principles: concept art and character art | A limit from the view: first, third, top down. |
| Perspective/orthographic | The Unreal Editor interface | Perspective shows depth; orthographic drops it, so parallel edges stay parallel. |
| PIE changes discarded | The Unreal Editor interface | Edits made to Actors during play are thrown away when you stop; edits made before play stay. |
| Pinned clock | Shader verification | A fixed frame rate: every frame the same length. |
| Pinned time step | Walker and the toolchain | A constant step length forced on the simulation. |
| Pitch | The game design document | A short sales description of the game idea. |
| Pitch | How to make a trailer for your game | A short sales description of the game idea. |
| Pitch film | How to make a trailer for your game | A 2 to 4 minute film on what you will build. |
| Pivot | Blender: the interface and modeling terms | The point an object rotates and scales around. |
| Pivot and Local handles | The Unity editor interface | Pivot or Center sets where the handle sits; Local or Global sets how it points. |
| Pixel diff | Shader verification | A count of the pixels where two images differ. |
| Place Actors panel | The Unreal Editor interface | A palette of Actor types that you drag into the level. |
| Play In Editor (PIE) | The Unreal Editor interface | Running the game inside the editor. |
| Play Mode | The Unity editor interface | The editor runs the game inside itself; the Play button turns it on and off. |
| Play Mode changes lost | The Unity editor interface | Edits to scene objects made during Play Mode are thrown away when you stop. |
| Play testing | Game design A: what a game is | Letting players challenge the design so it can be revisited and improved. |
| Playback speed scale | Animation: principles and character animation | A multiplier on how fast a clip plays. |
| Player purpose | Game design C: pacing and guidance | What the player does and why; the player, not the game, drives it forward. |
| Player verb | Game design A: what a game is | An action the player can take: jump, shoot, build. |
| Playhead | Animation foundations | The marker for the current time on the timeline. |
| Plugins | The Unreal Editor interface | Add-on modules you switch on or off per project; most need an editor restart. |
| PNG vs JPEG | 2D art and sound assets in the engine | Lossless with alpha versus lossy without alpha. |
| Pole target | Animation foundations | A helper point that sets which way an elbow or knee bends. |
| Polling | Godot: the editor, scenes, nodes, signals and movement | Asking every tick whether something has happened. |
| Polygon count | Blender: the interface and modeling terms | Three tallies of one mesh: engines budget by triangles, Blender shows faces, and vertices are split where UVs or normals differ. |
| Polyphony | 2D art and sound assets in the engine | How many copies of a sound can play at once; Godot's default is 1. |
| Pose | Animation: principles and character animation | A single held body position; animation is a series of them. |
| Precondition and effect | Game AI: decisions, generation and systems | Precondition: what must be true before an action runs. Effect: what it changes. |
| Prefab | The Unity editor interface | Unity's reusable object template; edits to it flow to every instance. |
| Prefab Mode | The Unity editor interface | Opens a prefab asset on its own so you edit the template, not one instance. |
| Preferences | The Unity editor interface | Settings that belong to you and your machine, such as colours, keys and the script editor. |
| Premultiplied alpha | Shader verification | Colour already multiplied by its alpha. |
| preprocess | Particles and VFX | Starts as if the effect had already run this many seconds. |
| Primary to tertiary read | Particles and VFX | The order the eye notices an effect's parts: head, tail, then sparks. |
| Priority | Animation and interaction: state machines and blending | Which transition wins when several are true at once; in Godot the lower number is preferred. |
| Priority Inflation | The game design document | More than 40% of the features tagged CORE. |
| Probability | Game design B: choices and challenge | The odds of each result; extra rolls change them. |
| Procedural synthesis | 2D art and sound assets in the engine | Sound made by a formula evaluated sample by sample, with no file and no model. |
| Profiler | The Unity editor interface | Records each frame's time by system (scripts, rendering, physics) to find what is slow. |
| Programmable stage | Shaders: foundations | A pipeline step you write a shader for. |
| Progression | Game design C: pacing and guidance | A natural rise in challenge; do not over-stimulate or under-stimulate. |
| Project | Godot: the editor, scenes, nodes, signals and movement | A folder with a project.godot file at its root; res:// means that folder. |
| Project Settings | Godot: the editor, scenes, nodes, signals and movement | Project-wide values: physics rate, layer names, input actions, autoloads. |
| Project Settings | The Unity editor interface | Settings that belong to the project and are saved in it, such as Tags and Layers, Physics and Time. |
| Project Settings | The Unreal Editor interface | Settings saved with the project and shared by everyone who opens it. |
| Project window | The Unity editor interface | A file browser for the project's Assets and Packages folders. |
| Properties editor | Blender: the interface and modeling terms | Tabs of settings for the selected object: transform, modifiers, material. |
| Property track | Animation and interaction: state machines and blending | A track that animates any property, not just bones. |
| Prototype | Game design A: what a game is | A simplified version made first to test whether the idea has appeal. |
| Proxy model | Art principles: concept art and character art | A rough block model of big shapes, used to check proportions and silhouette early. |
| Pursue | Game AI: perception, movement and pathfinding | Steer toward where a moving target will be. |
| Pushed proportions | Art principles: concept art and character art | Exaggerated shapes, as in a cartoon look. |
| PX goal | The game design document | A feeling or experience the player should have, with an ID like PX-01. |
| Q-learning | Game AI: decisions, generation and systems | Learning the value of each action in each state. |
| Quad | Blender: the interface and modeling terms | A face with four vertices. |
| Random seed | Shader verification | A fixed starting number so random results repeat. |
| Rasterization | Shaders: foundations | Turning triangles into fragments on the screen grid. |
| Readability | 2D art and sound assets in the engine | How well a character can be understood in the game's real view. |
| Readability | Art principles: concept art and character art | How well a character can be understood in the game's real view. |
| Real-time capture | How to make a walkthrough film: important terms | Recording the game as it runs live, so frame times vary from frame to frame. |
| Recovery | Animation and interaction: state machines and blending | The frames after an attack before the character can act. |
| Reference | Art principles: concept art and character art | Real-world images and examples gathered for research. |
| Reflection probe | Materials and textures | A point that captures the surroundings so shiny surfaces have something to reflect. |
| Regression test | Walker and the toolchain | A test that guards a behaviour that worked before. |
| Reinforcement learning | Game AI: decisions, generation and systems | Learning behaviour by trial and reward. |
| Render | How to make a walkthrough film: important terms | Computing each frame offline, as slowly as needed, then joining the frames into a film. |
| Replication | Game AI: decisions, generation and systems | Copying a value from the peer that owns it to the other peers. |
| Repository | Walker and the toolchain | A project folder with its full version history. |
| Resolution | 2D art and sound assets in the engine | Width and height in pixels. |
| Resolution | How to make a trailer for your game | Width and height in pixels. |
| Resolution | Materials and textures | Width and height of a texture in pixels. |
| Resolution | How to make a walkthrough film: important terms | The width and height of a frame in pixels. |
| Resource | Godot: the editor, scenes, nodes, signals and movement | A typed data container nodes share, made by extending Resource. |
| Rest and high detail | Art principles: concept art and character art | Plain regions beside busy ones, so the busy part reads as important. |
| Rest pose | Animation foundations | The skeleton's default pose, which you can return to at any time. |
| Rest pose (bind pose) | Animation: principles and character animation | The skeleton's default pose, the one the mesh is fitted to. |
| Restraint | Particles and VFX | Keeping most effects modest so the important ones stand out. |
| Retargeting | Animation: principles and character animation | Applying an animation made for one skeleton to a different one. |
| Reverse | The game design document | Recover a GDD from a game that already exists. |
| Reward | Game AI: decisions, generation and systems | The number telling the agent how well it did. |
| RGBA | Shaders: foundations | Red, green, blue and alpha channels. |
| Rig and skeleton | Animation: principles and character animation | The skeleton (a hierarchy of bones) plus the binding that makes the mesh follow it. |
| Right-handed, +Z up | Blender: the interface and modeling terms | Blender: X cross Y gives Z, and Z is up. glTF and Godot put +Y up. |
| Right-mouse fly | The Unreal Editor interface | Hold the right mouse button and press W A S D to fly the viewport camera. |
| RigidBody2D | Godot: the editor, scenes, nodes, signals and movement | Simulated physics: you set forces or velocity, the engine moves it. |
| Risk versus reward | Game design B: choices and challenge | A harder or riskier action pays more, and the player weighs the factors. |
| Rock-paper-scissors | Game design B: choices and challenge | Each option beats one and loses to another, so no option wins everywhere. |
| Roll | Terms: Camera | Spin around the viewing direction; the horizon tips. |
| Root motion | Animation: principles and character animation | The clip moves the character through the world. |
| Roughness | Materials and textures | How blurred the reflections are: 0 is mirror-sharp, 1 is wide and dull. |
| Route | How to make a walkthrough film: important terms | The planned path the camera travels through the scene, measured before any frame is rendered. |
| Route check | How to make a walkthrough film: important terms | A script that steps every frame and measures speed, turn rate, roll and height. |
| RPC | Game AI: decisions, generation and systems | A function one computer asks another computer to run. |
| Rules | Game design A: what a game is | The framework that limits and governs the whole experience. |
| Run and Play buttons | Godot: the editor, scenes, nodes, signals and movement | Run Project (F5) starts the main scene; Run Current Scene starts the open one. |
| Runtime | How to make a trailer for your game | How long the film runs; a store trailer is typically 30 to 90 seconds. |
| Safe margins | How to make a walkthrough film: important terms | The inner area, inset about 5% on each side, where text and logos must sit. |
| Safety margin | Game AI: decisions, generation and systems | Extra room left so generated content never just barely passes. |
| Sample rate | 2D art and sound assets in the engine | Audio samples per second. |
| Sampling | Animation and interaction: state machines and blending | Reading a value at one moment, so brief events between samples can be missed. |
| Sandbox | Walker and the toolchain | A restricted environment where mistakes cannot reach the rest of the machine. |
| Satisfaction | Art principles: concept art and character art | Actions get quick, responsive feedback. |
| Scale curve | Particles and VFX | A curve for particle size over its life. |
| Scene | Godot: the editor, scenes, nodes, signals and movement | A saved, reusable tree of nodes: a level, a character, a menu. |
| Scene dock, Remote tab | Godot: the editor, scenes, nodes, signals and movement | Lists the scene's nodes; the Remote tab lists the running game's. |
| Scene gizmo | The Unity editor interface | The axis widget at the Scene view's top right; click an axis to look along it. |
| Scene tree | Godot: the editor, scenes, nodes, signals and movement | The live hierarchy of nodes in a running game. |
| Scene view | The Unity editor interface | Where you look at the scene and edit it, through a free editor camera. |
| Scene, Level, Map | Godot, Unity and Unreal: the differences | A saved, reusable tree of objects. Unreal's word for the level file is Map. |
| Scope | The game design document | Everything the project promises to include. |
| Scope creep | The game design document | Quiet growth of work beyond what was agreed. |
| Scope violation | Shader verification | Changing something the brief said not to touch. |
| Screen shake | Terms: Camera | Brief, fading random offset of the camera for impact. |
| SCREEN_UV | Shaders: foundations | Godot built-in: the screen position of the current fragment, 0 to 1. |
| Script | Godot: the editor, scenes, nodes, signals and movement | Attaches behaviour to a node; GDScript here. |
| Script | How to make a walkthrough film: important terms | The words of the narration, written out and checked before anyone records them. |
| Script as source | Blender to Godot: MCP, export and measuring a prop | The script that built the asset is what you commit and rerun; the .glb is its output. |
| Secondary motion | Animation: principles and character animation | Extra movement the main action causes, such as a tail or hair, not keyed by hand. |
| Seed | Game AI: decisions, generation and systems | A number that fixes a random sequence. |
| Seed, determinism | Particles and VFX | Same seed and inputs give the same random choices and output every run. |
| Seek | Game AI: perception, movement and pathfinding | Steer toward a target. |
| Selector | Game AI: decisions, generation and systems | Tries children in order until one succeeds. |
| Sense, decide, act | Game AI: perception, movement and pathfinding | The loop every system in Chapter 14 runs, once per tick. |
| Separation | Game AI: perception, movement and pathfinding | Steer away from close neighbours. |
| Sequence | Game AI: decisions, generation and systems | Runs children in order and stops at the first failure. |
| set_shader_parameter | Shaders: foundations | Changes one uniform's value on a material, by name; a typo does nothing. |
| Shader | Shaders: foundations | A small program on the graphics processor, run many times at once. |
| Shader and material | Godot, Unity and Unreal: the differences | Godot and Unity write shaders as code or graph. Unreal builds materials as node graphs. |
| shader_type | Shaders: foundations | First line of a shader: says what it draws, and so which functions you can write. |
| ShaderMaterial | Shaders: foundations | A material that uses a custom Shader program and holds its parameter values. |
| Shape and size contrast | Art principles: concept art and character art | Distinct shapes or sizes make one thing stand out, or point the way. |
| Shape language | Art principles: concept art and character art | How the forms of a design express its personality or idea. |
| Shape language | Particles and VFX | The same shapes for the same meaning across the whole game. |
| Shared material | Shaders: foundations | One material used by many objects, so a change hits them all. |
| Shot | How to make a walkthrough film: important terms | One continuous camera take, with a job and something it reveals that no earlier shot did. |
| Side quest | Game design C: pacing and guidance | A detour from the main storyline. |
| Sight range | Game AI: perception, movement and pathfinding | How far an NPC can see. |
| Signal | Godot, Unity and Unreal: the differences | Godot's named event. Other nodes connect to it and run when it fires. |
| Signal | Godot: the editor, scenes, nodes, signals and movement | A named event a node emits; other nodes connect to it. |
| Silhouette | 2D art and sound assets in the engine | The outline of an object; it should still read when filled black at game size. |
| Silhouette | Animation: principles and character animation | The solid outline of a pose; a clear action reads from the outline alone. |
| Silhouette | Art principles: concept art and character art | The outline of an object; it should still read when filled black at game size. |
| Simulate | The Unreal Editor interface | Runs the level's logic and physics with no player; you keep the editor camera. |
| Situational choice | Game design B: choices and challenge | The same choice is better or worse depending on the situation the player is in. |
| Sixteen sections | The game design document | The fixed outline of a GDD, from metadata to open questions. |
| Skeleton | Animation foundations | The hierarchy of bones. A child bone moves with its parent. |
| skeleton_updated | Animation foundations | A signal sent when the final pose, IK included, is ready to read. |
| SkeletonIK3D | Animation foundations | The older built-in IK node. Marked Deprecated in the class reference. |
| Skinning weights | Animation: principles and character animation | How strongly each vertex follows each bone. |
| Smoothing (damping) | Terms: Camera | Spreads the camera's catch-up over time so it trails slightly. Same idea under both names: the camera eases toward its target instead of snapping. |
| Smoothness | Materials and textures | The inverse of roughness: how mirror-like a surface is. |
| smoothstep(e0, e1, x) | Shaders: foundations | Rises from 0 to 1 between two edges along a smooth S-curve. |
| Software renderer | Shader verification | Drawing on the CPU: same output on any machine. |
| Sound design | How to make a trailer for your game | Mix so music sets the tone and the game's own hits punch through. |
| source_color | Shaders: foundations | Marks a colour as sRGB data so it is decoded to linear for the maths. |
| source_color | Shader verification | A hint: this texture holds colour, so decode it. |
| Space | Game design A: what a game is | The look, sound, lighting and physical setting; it shapes what fits in the game. |
| Spacing | Game design C: pacing and guidance | Open areas to admire, or tight ones that feel claustrophobic; leave room for AI. |
| spatial | Shaders: foundations | Godot shader type for 3D drawing: meshes. |
| Spec | Walker and the toolchain | A written description of what must be built. |
| Specification oracle | Shader verification | An oracle taken from the spec, not the code. |
| Speed scale | Animation foundations | A multiplier on how fast a clip plays. 0.5 is half speed. |
| spread | Particles and VFX | The cone angle of random variation around the emission direction. |
| Sprite sheet | 2D art and sound assets in the engine | One image of many frames in a grid. |
| SpriteFrames | 2D art and sound assets in the engine | A Godot resource of named animations: frames, speed and a loop flag. |
| Squash and stretch | Animation: principles and character animation | Compress on impact, elongate at speed; shows elasticity and inertia. |
| sRGB | Materials and textures | The encoding for images shown to people; steps are spaced for eyes. |
| SSAO | Materials and textures | Screen-space ambient occlusion: a real-time estimate from the depth image, separate from a texture's AO. |
| Stable ID | The game design document | A label that never changes, such as PX-01, M-01 or T-01. |
| Stagnant Artifact | The game design document | No version history; never revised after a prototype. |
| Startup | Animation and interaction: state machines and blending | The windup frames before an attack can hit. |
| State | Animation and interaction: state machines and blending | One named mode of a state machine, such as idle or run. |
| State machine | Animation: principles and character animation | One active state; transitions fire on conditions. |
| State machine | Godot, Unity and Unreal: the differences | States joined by transitions with rules. The current state picks the clip. |
| StaticBody2D | Godot: the editor, scenes, nodes, signals and movement | Not moved by physics; others collide with it. |
| Steady state | Particles and VFX | Births equal deaths, so the live count levels off. |
| Steering | Game AI: perception, movement and pathfinding | Behaviours that adjust movement toward a goal. |
| Step (discrete) | Animation: principles and character animation | The value holds until the next key, then jumps. |
| step(edge, x) | Shaders: foundations | Gives 0 below the edge and 1 from the edge up: a hard switch. |
| Storyboard | How to make a walkthrough film: important terms | Rough drawings of the key frames in order, made before anything is captured. |
| Sub-emitter | Particles and VFX | A second GPU particle system that spawns from the first one's particles. |
| Subdivision Surface | Blender: the interface and modeling terms | Splits and smooths faces; each level makes 4 times as many. |
| Success/failure/running | Game AI: decisions, generation and systems | The three results a node can return; running means not finished, tick me again. |
| Tag | The Unity editor interface | A text label on an object for lookup and filtering. |
| Tagline | How to make a trailer for your game | A few memorable words that sit beside the title. |
| Tangent space | Materials and textures | Normal directions relative to the surface itself, so the map works on any mesh. |
| Target experience | Game design A: what a game is | The one specific experience everyone on the team aims at. |
| Teaching through levels | Game design C: pacing and guidance | The first level lets the player try each skill, with no text. |
| Teaser | How to make a trailer for your game | An early look that hints and shows little. |
| Template | Godot, Unity and Unreal: the differences | The master that copies come from: a Godot scene, a Unity Prefab, an Unreal Blueprint class. |
| Test fixture | Shader verification | Fixed setup that a test starts from. |
| Test oracle | Shader verification | The source of the right answer a test compares to. |
| Test the test | Shader verification | A new check must fail on bad code, pass on good. |
| Texel | 2D art and sound assets in the engine | One pixel of a texture. |
| Texel density | Materials and textures | Texels per unit of world size: texture pixels per metre. Should match across objects. |
| Text versus binary scene | Walker and the toolchain | Readable scene files diff cleanly; opaque ones do not. |
| texture | Particles and VFX | The image drawn for each particle. If null, 1 by 1 pixel squares. |
| TEXTURE | Shaders: foundations | The default 2D texture the item was drawn with. |
| Texture atlas | 2D art and sound assets in the engine | Many small images packed into one big texture; a frame is a region of it. |
| Texture baking | Art principles: concept art and character art | Sculpt detail stored as an image on the low-poly. |
| Texture baking | Blender to Godot: MCP, export and measuring a prop | Moving the sculpt's fine detail into an image the low-poly mesh wears. |
| Texture baking | Materials and textures | Transferring the detail of a high-poly model into an image used on the low-poly one. |
| Thematic constraint | Art principles: concept art and character art | A limit from lore, setting and tone. |
| Thematic feel | Game design A: what a game is | Mechanics alone can set the tone: what a thing does tells the player what it is. |
| Three pillars | Game design C: pacing and guidance | A game rests on the player's role, communication and appeal. |
| Thumbnail | How to make a trailer for your game | The small preview image; it has to read at a glance. |
| Tick | Game AI: decisions, generation and systems | One update step; the tree is evaluated again from the root. |
| Tick | Godot, Unity and Unreal: the differences | Each Actor ticks every frame. Tick groups such as pre-physics order the work. |
| Tiling | Materials and textures | Repeating a texture across a surface; a seamless texture shows no join. |
| Tilt | Terms: Camera | Turn up or down on the spot; position unchanged. |
| TIME | Shaders: foundations | Seconds since the engine started; repeats after 3,600 s. |
| Timeline | Blender: the interface and modeling terms | Playback controls and a frame scale with keyframes marked. |
| Timeout | Walker and the toolchain | A limit after which a run is stopped. |
| Timing and spacing | Animation: principles and character animation | Timing is how long a move takes; spacing is how far it moves between frames. |
| Timing curve | Particles and VFX | Varying how fast an effect grows and slows, not a constant rate. |
| Title card | How to make a trailer for your game | A held card with the game's name, after the peak. |
| Title card | How to make a walkthrough film: important terms | A full-screen card with the film's name, shown briefly at the start and end. |
| Tolerance | The game design document | The allowed difference between expected and actual. |
| Tolerance | Shader verification | The allowed gap between expected and actual. |
| Toolbar | The Unity editor interface | The top strip: transform tools, pivot and handle toggles, Play, Pause and Step. |
| Track | Animation foundations | One property's keyframes inside a clip, bound to a node path. |
| Trade-off | Game design B: choices and challenge | Give up one thing to get another. |
| Trail (ribbon) | Particles and VFX | A strip that follows a moving object, textured to look like a tail. |
| Trailer | How to make a trailer for your game | A short film that sells a game to a stranger. |
| Transform | Blender: the interface and modeling terms | Location, rotation and scale: where the object is, how it is turned, how much it is stretched. |
| Transform tools | The Unity editor interface | Move, Rotate, Scale, Rect and Hand: the handles for changing a selection. |
| Transition | Animation and interaction: state machines and blending | A connection from one state to another, with its own rule for when it fires and how long it blends. |
| Transition rule | Animation and interaction: state machines and blending | A small graph that outputs true or false; true lets the state change. |
| Transition table | Game AI: decisions, generation and systems | A list of every state, condition and next state. |
| Transition type | Animation foundations | The family of curve a tween follows: linear, sine, quad, cubic, back, bounce and more. |
| Transparent background | 2D art and sound assets in the engine | Cut the background to alpha 0; ask for a solid colour, not for transparent. |
| Travel | Animation and interaction: state machines and blending | Ask the machine to go to a state by the shortest path of transitions; with no path it jumps there. |
| Triangle count | Blender to Godot: MCP, export and measuring a prop | Engines budget by triangles; Blender shows faces; vertices split where UVs or normals differ. |
| Trigger | Godot, Unity and Unreal: the differences | A zone that reports overlaps instead of blocking, such as a pickup or a checkpoint. |
| Truck | Terms: Camera | Move the camera left or right, still facing the same way. |
| Tween | Animation and interaction: state machines and blending | Code-made animation of a value toward a target, then discarded; it can be killed halfway. |
| Tween | Animation foundations | A value animated from code toward a target, then thrown away. For end values that come from gameplay. |
| Tween | Animation: principles and character animation | Code-driven interpolation of a property over a duration. |
| Two-tone sketching | Art principles: concept art and character art | Sketching in two colours to avoid small detail. |
| Types of fun | Game design A: what a game is | "Fun" is too vague. Name the kind: fantasy, thrill, fellowship, mastery, exploration, creativity. |
| Uniform | Shaders: foundations | A value set from code, the same across a draw; how scripts steer a shader. |
| Uniform value check | Shader verification | Compare a shader input's value with the spec. |
| Uniform vs non-uniform | 2D art and sound assets in the engine | Same factor on both axes versus different factors that distort. |
| Unit | Blender: the interface and modeling terms | The length one coordinate step stands for (usually a metre). |
| Unit | Blender to Godot: MCP, export and measuring a prop | The length one coordinate step stands for, usually a metre. |
| Unit differentiation | Game design B: choices and challenge | Each enemy type does something different, which forces the player to prioritise. |
| Unit scale | Blender to Godot: MCP, export and measuring a prop | The factor from Blender units to metres; 1.0 means 1 unit is 1 m. |
| Units | Godot, Unity and Unreal: the differences | In Godot and Unity 1 unit is 1 metre. In Unreal 1 unit is 1 centimetre. |
| Unity blend tree | Animation and interaction: state machines and blending | Mixes several clips by a parameter value. |
| Unity transition | Animation and interaction: state machines and blending | Moves from one state to another over a set time. |
| UnityEvent, C# event | Godot, Unity and Unreal: the differences | Unity's events. A UnityEvent is wired in the Inspector, so reading code alone can miss it. |
| Unwrapping | Blender: the interface and modeling terms | Cutting a mesh and flattening it into a UV map. |
| Unwrapping | Materials and textures | Cutting a mesh along seams and flattening it into a UV map. |
| Up axis | Blender to Godot: MCP, export and measuring a prop | Which axis points up: Z in Blender, Y in glTF and Godot. |
| Up axis, handedness | Godot, Unity and Unreal: the differences | Godot and Unity are Y-up, Unreal is Z-up. Unity and Unreal are left-handed, Godot is right-handed. |
| Update mode | Animation foundations | Per value track: update between keys (continuous), or only at the keys (discrete). |
| Update, FixedUpdate | Godot, Unity and Unreal: the differences | Once per frame, and at fixed 0.02 s steps, which is 50 a second by default. |
| URP Lit maps | Materials and textures | Base, Metallic, Normal and Occlusion maps; smoothness comes from an alpha channel. |
| Utility AI | Game AI: decisions, generation and systems | Scores every option and picks the highest. |
| UV | Materials and textures | 2D coordinates that map each point of a surface to a spot on a texture. |
| UV | Shaders: foundations | 2D coordinates mapping a surface to a texture, 0 to 1 across it. |
| UV map | Blender: the interface and modeling terms | The flattened 2D layout of a mesh used to place a texture. |
| UV map and unwrapping | Art principles: concept art and character art | Flat layout of a surface; unwrapping makes it. |
| UV scale | Materials and textures | A multiplier on UVs that sets how often a texture repeats. |
| Validator | Game AI: decisions, generation and systems | A check that tests generated content against rules. |
| Value track | Animation foundations | Sets a property, such as rotation_degrees, to a value at each time. |
| Varying | Shaders: foundations | A value passed from the vertex stage to the fragment stage, interpolated on the way. |
| Velocity, max speed | Game AI: perception, movement and pathfinding | Speed with a direction; max speed caps its size. |
| Version control | Blender to Godot: MCP, export and measuring a prop | Software that records every version of a file and who changed it, and warns of clashes. |
| Vertex | Blender: the interface and modeling terms | A corner point of a mesh. |
| Vertex colour | Shaders: foundations | Colour stored on each vertex; can blend textures or paint terrain by height. |
| Vertex shader | Shaders: foundations | Runs per vertex; sets positions (waves, displacement). |
| View modes | The Unreal Editor interface | Ways to draw the same scene: Lit, Unlit, Wireframe and others. |
| Viewer test | How to make a trailer for your game | Show the cut, unexplained, to someone new and ask what the game is and what they do. |
| Viewport | 2D art and sound assets in the engine | The area the game draws into, set in Project Settings; the window scales it. |
| visibility_rect | Particles and VFX | The region that must be on screen for the effect to be active. |
| Visual hierarchy | Art principles: concept art and character art | The most important things are seen first. |
| Voice-over | How to make a walkthrough film: important terms | Narration heard over the pictures; the speaker is not shown in the shot. |
| Walker | Walker and the toolchain | The working method and its files: brief, build, playtest, inspect, revise, export. |
| Walkthrough film | How to make a walkthrough film: important terms | A narrated camera tour of a game or asset that shows what it does and says what it leaves out. |
| Wander | Game AI: perception, movement and pathfinding | Small random turns, so the path meanders. |
| WAV vs Ogg Vorbis | 2D art and sound assets in the engine | WAV for short effects; Ogg Vorbis for music, speech and long sounds. |
| Waves | Game design C: pacing and guidance | A group of enemies sent together: many weak ones or a few strong ones. |
| Waypoint | Game AI: perception, movement and pathfinding | A point along a path. |
| Waypoint | How to make a walkthrough film: important terms | A point along the route where the camera passes, turns or stops. |
| Weight and balance | Animation: principles and character animation | Where the balance falls; stable when it sits over the feet. |
| Weighted sum | Game AI: decisions, generation and systems | Adding scores, each multiplied by an importance weight. |
| What it is not | How to make a walkthrough film: important terms | A spoken and on-screen statement of what the film leaves out, placed in the first two shots. |
| Workspace | Blender: the interface and modeling terms | A saved arrangement of editors for one job, chosen from the tabs on top. |
| World Settings | The Unreal Editor interface | Settings for the open level as a whole, such as its Game Mode and Kill Z. |
| Wrap mode | Materials and textures | What sampling outside 0 to 1 does: repeat (tile) or clamp (stretch the edge). |
| Zoom | Terms: Camera | Change the lens (field of view or focal length); the camera does not move. |
