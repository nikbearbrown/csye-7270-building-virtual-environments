# CSYE 7270 midterm glossary: say it exactly

The midterm is a language test. Precise words let you tell an animation, shader, material, camera or movement tool exactly what to build. If you can say "dolly in, 1.5 seconds, ease-out" you get that. If you say "swoop in" the agent guesses.

Each table gives the term and one plain sentence. Meanings hold for Godot, Unity, Unreal and Blender unless a row names an engine.

## Camera

| Term | Meaning |
|---|---|
| Pan | Turn left or right on the spot; position unchanged |
| Tilt | Turn up or down on the spot; position unchanged |
| Roll | Spin around the viewing direction; the horizon tips |
| Dolly | Move the camera forward or backward along its view direction |
| Dolly in/out | Dolly in moves toward the subject, dolly out moves away |
| Dolly in / dolly out | Move the camera toward / away from the subject |
| Truck | Move the camera left or right, still facing the same way |
| Pedestal | Move the camera straight up or down, still facing the same way |
| Zoom | Change the lens (field of view or focal length); the camera does not move |
| Dolly versus zoom | A dolly changes parallax (near and far shift against each other); a zoom only magnifies |
| Parallax | Nearer things shift more than farther things when the viewpoint moves |
| Focal length | Lens strength in millimetres; longer means narrower view and more magnification |
| Orbit | Move around a subject on a curved path while keeping it framed |
| Follow camera | Tracks a moving target, usually with smoothing |
| Smoothing (damping) | Spreads the camera's catch-up over time so it trails slightly |
| Smoothing/damping | Same idea under both names: the camera eases toward its target instead of snapping |
| Deadzone | Screen region where the target can move without the camera moving |
| Look-ahead | Shifts framing toward the direction of travel |
| Screen shake | Brief, fading random offset of the camera for impact |
| Camera limits | Clamps that keep the view inside the level |
| Field of view (FOV) | The lens angle; wider shows more |
| Perspective / orthographic | Distant things shrink / size does not depend on distance |

## Animation

| Term | Meaning |
|---|---|
| Keyframe | A stored value at a specific time |
| Interpolation | Computing the in-between values |
| Easing | The speed curve of a change (ease-in slow start, ease-out slow end) |
| Linear | Constant rate of change |
| Tween | Code-driven interpolation of a property over a duration |
| Clip | An authored animation: tracks of values over time |
| Authored clip | A clip an artist keyed by hand, as opposed to a tween made in code |
| Blend tree | Weighted mix of clips driven by parameters (walk to run on speed) |
| State machine | Named states, one active, with transitions that fire on conditions |
| Transition | The rule and condition that moves a state machine to another state |
| Parameter | A named value (number, bool, trigger) that code sets and transitions or blends read |
| Rig | Skeleton plus the binding that makes the mesh follow it |
| Rig/skeleton | The bone hierarchy that drives a mesh |
| Bone | A joint transform in the skeleton hierarchy |
| Bone weights | How strongly each vertex follows each bone |
| Skinning weights | How strongly each vertex follows each bone |
| Root motion | The clip's movement drives the character through the world |
| In-place | The clip runs on the spot; code supplies the travel |
| FK / IK | Rotate joints parent-to-child / solve joint angles to reach a target |
| IK | Inverse kinematics: give a target and the solver works out the joint angles |
| Sprite sheet | One image of many frames in a grid |
| Sprite sheet (cell size, grid) | Frames laid out in rows and columns, each cell the same size |
| Frame rate | Frames shown per second |

## Game movement and collision

| Term | Meaning |
|---|---|
| Velocity | Speed with a direction (a vector) |
| Speed | The size of the velocity |
| Acceleration | The rate velocity changes |
| Friction / deceleration | Loss of speed over time with no input |
| Gravity | Steady downward acceleration |
| Delta time | Time since the previous frame; scale per-second values by it |
| Frame-rate independence | Behaviour that comes out the same at 30 or 144 frames per second |
| Fixed timestep | Physics ticks at a steady interval |
| Tunnelling | A fast object passes through a thin collider unnoticed |
| Coyote time | Grace window after leaving a ledge in which a jump still works |
| Jump buffer | Remembers an early jump press and jumps on landing |
| Collider | Shape used for contact tests |
| Trigger | Volume that detects overlap and does not block |
| Hitbox / hurtbox | Area that deals damage / area that can take damage |
| Layers and masks | What an object is / what it looks for |
| Rigid body | Moved by the physics simulation |
| Kinematic body | Moved by code or animation, not by forces |
| Static body | Does not move |
| Rigid/kinematic/static body | The three body kinds: simulated by forces, moved by code, never moved |

## Shaders and materials

| Term | Meaning |
|---|---|
| Vertex shader | Runs per vertex; sets positions (waves, displacement) |
| Fragment shader | Runs per pixel; sets colour (tint, glint) |
| Uniform | Value set from code, the same across a draw; how scripts steer a shader |
| Varying | Value passed from the vertex to the fragment stage, interpolated |
| UV | 2D coordinates mapping a surface to a texture |
| Albedo | Base colour before lighting |
| Normal map | Per-pixel surface direction; fakes bumps in lighting, no new geometry |
| Roughness | How sharp or blurry highlights and reflections are |
| Metallic | How much the surface behaves like a metal |
| Emission | Light the surface gives off itself |
| PBR | Physically based rendering: consistent materials under varied lights |
| Blend mode | How output combines with what is behind it (alpha, additive, multiply) |
| Alpha blending | Mixes the new colour with the background by its opacity |
| Additive blending | Adds the new colour to the background; glows and fire |
| Material | A shader plus its parameter values and textures |

## Engine vocabulary

| Term | Meaning |
|---|---|
| Scene | A saved, reusable tree of objects (a level, a character, a menu) |
| Level | A scene that is one playable space |
| Map | Unreal's word for a level file |
| Prefab | Unity's reusable object template; edits to it flow to every instance |
| Instance | One live copy made from a template |
| Blueprint class | Unreal's reusable object template, built visually or in code |
| Override | A change on one instance that differs from its template |
| Template | The master definition that instances are copied from |
| Node | Godot's building block: one object in the scene tree |
| GameObject | Unity's object; does nothing until components are added |
| Actor | Unreal's object that can be placed in a level |
| Component | A piece of behaviour or data attached to a GameObject or Actor |
| Group | A named set of nodes you can call or query together (Godot) |
| Tag | A text label on an object for lookup and filtering |
| Layer | A numbered category used for rendering or collision filtering |
| Local space | Coordinates relative to the parent object |
| World space | Coordinates relative to the whole level |
| Screen space | Coordinates in pixels or normalised units on the screen |
| Up axis | Which axis points up: Y in Godot and Unity, Z in Unreal and Blender |
| Y-down | 2D screen convention where y grows downward |
| Tick | One update step of the game loop |
| Frame | One image drawn, with one round of per-frame updates |
| Fixed step | An update at a constant interval, independent of rendering speed |
| Catch-up | Running several fixed steps in one frame to make up lost time |
| Polling | Asking every frame whether something has happened |
| Event-driven | Code runs only when something announces that it happened |
| Signal | Godot's named event that other nodes can connect to |
| Event | A notice that something happened, sent to whoever listens |
| Delegate | Unreal's (and C#'s) typed list of functions to call when an event fires |
| Callback | A function handed over to be called later |
| Unsubscribe | Disconnect a listener so it stops receiving events |
| Input action | A named intent such as "jump", mapped to physical keys or buttons |
| Just-pressed | True only on the frame a button went down |
| Held state | True for as long as a button stays down |
| Binding | The link from a physical input or event to an action or function |
| Asset | Any file the project uses: model, texture, sound, scene, data |
| Resource | Godot's shareable data object saved as a file (also a general MCP term, see below) |
| ScriptableObject | Unity's data asset that lives in the project, not in a scene |
| Data Asset | Unreal's data-only asset for configuration |
| Singleton | A single globally reachable object |
| Autoload | Godot's way to keep a script or scene always loaded as a global |
| DontDestroyOnLoad | Unity call that keeps an object alive across scene changes |
| Game Instance | Unreal's object that lives for the whole play session |
| Editor | The authoring application where you build the game |
| Export | Package the project for a platform (Godot's word for a build) |
| Build | The packaged, runnable output of a project |
| Export templates | Godot's prebuilt runtime binaries needed to export |
| Cross-engine mapping | Matching the same idea to each engine's name (scene, Scene, Level; node, GameObject, Actor) |

## Toolchain

| Term | Meaning |
|---|---|
| CLI | Command-line interface: you drive a program by typing commands |
| Shell | The program that reads typed commands (zsh, bash) |
| Flag | An option on a command, such as `--headless` |
| Environment variable | A named setting a program reads from its surroundings |
| Headless | Running with no window or display |
| Exit code | Number a program returns; 0 means success |
| Timeout | A limit after which a run is stopped |
| Hang | A run that never finishes |
| Import | Convert a source file into the form the engine uses |
| Cache | Stored results reused to save time, which can also go stale |
| Repository | A project folder with its full version history |
| Diff | The exact lines that changed between two versions |
| Commit | A saved snapshot in version history |
| Push | Send commits to a remote repository |
| Allow rule | A saved permission letting a tool or command run without asking |
| Permission prompt | A question asking the user to approve an action |
| Sandbox | A restricted environment where mistakes cannot reach the rest of the machine |
| Spec | A written description of what must be built |
| Context | Everything the model can see in the current conversation |
| Instruction file | A standing file of project rules the agent reads (such as CLAUDE.md) |
| Acceptance test | A check that decides whether the work is accepted |
| Claim vs evidence | What was said happened versus proof that it did |
| Flaky | Passes sometimes and fails sometimes with no change |
| Deterministic | Same inputs always give the same result |
| Fixed frame rate | Rendering locked to a set number of frames per second so runs match |
| Pinned time step | A constant step length forced on the simulation |
| Game time | The simulation's clock, as opposed to the wall clock |
| Checkable instruction | An instruction written so a check can pass or fail |
| Text vs binary scene | Readable scene files that diff cleanly versus opaque ones that do not |
| Regression test | A test that guards a behaviour that worked before |

## Scenes, nodes and signals

| Term | Meaning |
|---|---|
| Scene tree | The live hierarchy of nodes in a running Godot game |
| Instancing vs inheriting | Placing a scene inside another as a child versus extending it as a new type |
| PackedScene | Godot's loaded scene resource, ready to be instantiated |
| Instantiate | Create a live copy of a scene |
| add_child | Attach a node under a parent so it joins the tree |
| Transform inheritance | A child's position, rotation and scale are applied on top of its parent's |
| _enter_tree | Callback when a node joins the tree, before its children are ready |
| _ready | Callback once the node and its children are in the tree |
| _init | Constructor-time callback, before the node is in the tree |
| _process | Per-frame callback |
| _physics_process | Per-physics-step callback at a fixed rate |
| Delta | The time passed to _process or _physics_process since the last call |
| @onready | Godot annotation that fills a variable when the node is ready |
| GDScript | Godot's Python-like scripting language |
| Extends | GDScript keyword naming the class a script builds on |
| Emit | Fire a signal |
| Connect | Subscribe a function to a signal |
| Deferred connection | A connection whose call waits until the end of the frame |
| Call down / signal up | Parents call children's functions; children announce upward with signals |
| Coupling | How much one piece depends on another's details |
| @export | Annotation that shows a variable in the Inspector |
| Inspector | The editor panel for viewing and editing properties |
| Resource (custom) | Your own data class saved as a Godot resource file |
| Shared resource | One resource used by several nodes so a change affects all |
| Export timing | Exported values are set before _ready runs |
| Input Map | Godot's table of actions and their keys |
| Just pressed vs pressed | True on the first frame only / true while held |
| Physical key vs printed character | The key's position on the board versus the letter it prints |
| _input | Callback that receives every input event |
| _unhandled_input | Callback that receives only events nobody else used |
| Handled event | An event marked as consumed so later callbacks skip it |
| get_node | Look up a node by path |
| Relative vs absolute path | A path from the current node versus one from the tree root |
| Unique name (%) | A scene-unique node name reachable with a % prefix |
| queue_free vs free | Delete at a safe moment end-of-frame versus delete immediately |

## 2D art and sound assets

| Term | Meaning |
|---|---|
| Texture | An image used by the GPU |
| Sprite | A 2D image drawn as an object in the world |
| Resolution | Width and height in pixels |
| Aspect ratio | Width divided by height |
| Uniform vs non-uniform scaling | Same factor on both axes versus different factors that distort |
| Alpha channel | The extra channel storing opacity |
| Transparency | How much of what is behind shows through |
| PNG vs JPEG | Lossless with alpha versus lossy without alpha |
| Colour key / fringe | A reserved transparent colour / the halo of edge colour left around a cutout |
| Nearest vs linear filtering | Hard-edged pixel sampling versus smooth blended sampling |
| Texel | One pixel of a texture |
| Integer scaling | Scaling by whole numbers so pixel art stays crisp |
| Texture atlas | Many small images packed into one big texture |
| Tileset | A set of tile images for building maps |
| Tilemap | A grid that places tiles from a tileset |
| Batching | Drawing many objects in one draw call |
| Draw call | One request to the GPU to draw something |
| Padding / bleed | Extra border pixels that stop neighbouring cells leaking in |
| Seamless (tileable) | An image whose edges match so it repeats without a visible seam |
| Repeat vs clamp | Tile the texture past 0 to 1 versus stretch the edge pixels |
| Tiling scale | How many times a texture repeats across a surface |
| Palette | The limited set of colours an art style uses |
| Indexed colour | Each pixel stores a position in a palette instead of a colour |
| Anti-aliasing | Smoothing jagged edges by blending |
| Import settings | Per-asset options controlling how the engine converts it |
| Lossless vs lossy compression | Exact reconstruction versus smaller files with lost detail |
| Mipmaps | Pre-shrunk copies of a texture used at distance |
| Sample rate | Audio samples per second |
| Nyquist limit | The highest frequency a sample rate can hold: half the rate |
| Bit depth | Bits per audio sample; sets dynamic range |
| Mono / stereo channels | One audio channel versus two |
| PCM | Uncompressed digital audio samples |
| Loop point | Where a looping sound jumps back to |
| One-shot | Plays once and stops |
| Streaming | Reading audio from disk as it plays instead of loading it all |
| Lossless master | The untouched full-quality source you keep and export from |
| Bus | A channel that sounds are routed through for shared volume and effects |
| Master bus | The final bus everything feeds into |
| Decibel | Logarithmic loudness unit |
| Unity gain | A level setting that leaves volume unchanged (0 dB) |
| Clipping | Distortion when a signal exceeds the maximum level |
| Headroom | Spare level left below the maximum |
| Ducking | Lowering one sound automatically while another plays |
| Polyphony | How many copies of a sound can play at once |
| Pixel art | Art drawn at low resolution where single pixels matter |
| Provenance | Where an asset came from and who made it |
| Licence terms | What the asset's licence lets you do |
| Attribution | Crediting the creator as the licence requires |

## 3D assets and Blender

| Term | Meaning |
|---|---|
| Vertex | A corner point of a mesh |
| Edge | A line joining two vertices |
| Face | A flat surface bounded by edges |
| Quad | A face with four vertices |
| N-gon | A face with more than four vertices |
| Triangulation | Splitting faces into triangles, which is what the GPU draws |
| Triangle count versus face count versus vertex count | Three different tallies of the same mesh: engines budget by triangles, Blender shows faces, and vertices are split where UVs or normals differ |
| GPU vertex | A vertex as the GPU counts it; duplicated wherever UV, normal or material differs |
| Hard edge | An edge shaded with a visible crease because normals are not smoothed across it |
| UV seam | An edge where the UV map is cut, so the texture is split there |
| Flipped normals | Faces pointing inward, so they look dark or vanish |
| Backface culling | Not drawing faces that point away from the camera |
| Normal | The direction a surface faces |
| UV map | The flattened 2D layout of a mesh used to place a texture |
| Unwrapping | Cutting a mesh and flattening it into a UV map |
| Material slot | A named place on a mesh where a material is assigned |
| Material versus texture | A material is the full surface recipe; a texture is one image it uses |
| Origin | The point an object's position and rotation are measured from |
| Pivot | The point an object rotates and scales around |
| Unit | The length one coordinate step stands for (usually a metre) |
| Scale versus size | The multiplier on an object versus its real dimensions |
| Apply transforms | Bake position, rotation and scale into the mesh and reset them to neutral |
| Node scale | A scale left on an object or node instead of baked into the mesh |
| Handedness | Whether the coordinate system is right- or left-handed, which flips mirrored axes |
| glTF | An open 3D format; the preferred exchange format for engines |
| GLB | glTF packed into a single binary file |
| OBJ | A simple old mesh format with no animation or rigs |
| Convex | A shape with no dents; any line between two inside points stays inside |
| Concave | A shape with a dent or hollow |
| Trimesh | A collision shape that copies the exact triangles; accurate and costly, for static things |
| Convex hull | The tightest convex shape wrapped around a mesh |
| Primitive shape | A simple box, sphere or capsule used as a collider |
| Capsule | A cylinder with rounded ends; the usual character collider |
| Moving body | A body that moves, which needs a cheap collision shape |
| Collision shape versus visual mesh | The simple shape physics uses versus the detailed mesh you see |
| LOD | Level of detail: cheaper versions of a model swapped in at distance |
| Popping | A visible jump when one level of detail switches to another |
| bpy | Blender's Python module |
| Background (headless) mode | Running Blender with no window, from the command line |
| MCP | A standard way for an AI app to call tools in another program such as Blender |
| Add-on | A plug-in that extends Blender |
| Bounding box | The smallest axis-aligned box that holds an object |
| Extents | The half-sizes of a bounding box |
| Simple and complex collision (Unreal) | Unreal's cheap primitive shapes versus per-triangle mesh collision |

## Collision and physics

| Term | Meaning |
|---|---|
| Area2D/Area3D | Godot node that detects overlaps without blocking |
| Is Trigger | Unity checkbox that makes a collider detect overlaps instead of blocking |
| Unreal Overlap response | Unreal setting where objects pass through but fire overlap events |
| StaticBody2D | Godot body that never moves |
| RigidBody2D | Godot body moved by physics forces |
| CharacterBody2D | Godot body moved by your code, with built-in sliding |
| AnimatableBody2D | Godot body moved by animation or code that still pushes other bodies |
| Static/dynamic/kinematic body | Never moves / moved by forces / moved by code |
| move_and_slide | Godot call that moves a character and slides along surfaces |
| move_and_collide | Godot call that moves and stops at the first hit, reporting it |
| Collision layer | The categories an object belongs to |
| Collision mask | The categories an object checks for contact |
| Bitmask | A number whose binary digits switch layers on or off |
| Layer number | The numbered slot of a layer in the bitmask |
| Layer collision matrix | Unity's grid of which layers collide with which |
| Physics material | Friction and bounce settings for a collider |
| Friction | Resistance to sliding |
| Bounce | How much speed is kept after an impact |
| Render material | The look of a surface, unrelated to physics |
| Raycast | A line shot into the world that reports what it hits first |
| Shape query (overlap query) | Asking what overlaps a given shape right now |
| Hitscan | A weapon that hits instantly along a ray rather than flying a projectile |
| Line of sight | A clear straight path between two points |
| Continuous collision detection | Checking the whole path of a move to stop tunnelling |
| Force | A push applied over time, changing velocity gradually |
| Impulse | An instant change of velocity |
| Teleport | Setting a position directly, skipping the path in between |
| Detection versus response | Noticing a contact versus deciding what happens because of it |
| Fixed time step | Physics advances in equal slices |
| Body collider | The collider that blocks movement, as opposed to a hitbox |
| One-way platform | A surface solid from above and passable from below |
| Enter event | Fired on the first frame an overlap begins |
| Exit event | Fired when the overlap ends |
| Stay event | Fired every step while overlap continues |
| Query versus event | Asking now whether a contact exists versus being told when it begins |
| is_on_floor | Godot check for whether the body stands on the ground |
| Collision shape versus sprite | The invisible shape physics uses versus the picture drawn |

## Game design documents

| Term | Meaning |
|---|---|
| GDD | Game design document: what the game is and how it plays |
| Brief | A short statement of the task and its limits |
| Pitch | A short sales description of the game idea |
| Design pillar | A core principle every decision must support |
| Requirement | A statement of something the build must do |
| Core loop | The repeated moment-to-moment cycle the player enjoys |
| Game loop | The program cycle of input, update, draw |
| Meta loop | The longer cycle around many core loops (progress, unlocks) |
| Player verb | An action the player can take: jump, shoot, build |
| Mechanic | A rule-governed action in the game |
| Dynamic | Behaviour that emerges when mechanics interact |
| Aesthetic | The feeling the player is meant to get |
| Prototype | A rough build made to test an idea |
| Vertical slice | One small piece finished to full quality |
| MVP | Minimum viable product: the smallest version that works |
| Scope | Everything the project promises to include |
| Scope creep | Quiet growth of work beyond what was agreed |
| Out-of-scope list | A written list of what will not be built |
| Cut/defer/swap | The three ways to handle too much scope: remove, postpone, replace |
| Level design | Planning and building the spaces the player moves through |
| Worldbuilding | Inventing the setting, history and rules of the game world |
| Acceptance criterion | A concrete condition that must be true for work to count as done |
| Given-when-then | A format for a test: starting state, action, expected result |
| Tolerance | The allowed difference between expected and actual |
| Specification | The precise statement of what the system must do |
| Implementation | The code or assets that carry out the specification |
| Refactor | Restructure code without changing its behaviour |
| Invariant | A condition that must stay true throughout |
| Change surface | The set of places a change touches |
| Loosening | Weakening a check so a failing result passes |
| False pass | A test that passes though the behaviour is wrong |
| Playtest | Watching real players try the game |
| Automated test | A check that runs by script with no human |
| Physics tick | One fixed physics step |
| Edge case | An unusual input or situation at the limits |
| Direct state write | Setting a value in code instead of producing it through gameplay |
| Emulation | Imitating an input or system instead of using the real one |
| Loopback | A connection from a machine to itself |

## Shader foundations

| Term | Meaning |
|---|---|
| Fragment | A candidate pixel colour produced by rasterization for one covered screen position |
| Pixel | One dot of the final image |
| Rasterization | Turning triangles into fragments on the screen grid |
| Interpolation (shader) | Smoothly blending vertex values across a triangle's fragments |
| Overdraw | The same pixel being drawn more than once |
| SCREEN_UV | Godot built-in giving the screen position of the current fragment as 0 to 1 |
| Blending | Combining a fragment's colour with what is already on screen |
| Alpha test | Keep or throw away a fragment by comparing alpha to a cutoff |
| Discard | Shader command that throws the current fragment away |
| canvas_item | Godot shader type for 2D drawing |
| Spatial | Godot shader type for 3D drawing |
| RGBA | Red, green, blue and alpha channels |
| Mix | Blend two values by a fraction (also called lerp) |
| Modulate | Multiply a colour by a tint |
| TIME | Godot built-in clock in seconds for animating shaders |
| Fixed-function | Old hardware steps that could be configured but not programmed |
| Programmable stage | A pipeline step you write a shader for |
| Depth test | Keeping the nearer fragment and rejecting the farther one |
| Stencil test | Keeping or rejecting fragments by a mask value |
| Clip space | The coordinate space the vertex shader outputs, before the screen mapping |
| CPU-bound | Limited by processor work, not the graphics card |
| GPU-bound | Limited by graphics card work, not the processor |
| Filtering (nearest, linear) | How a texture is sampled between texels: blocky or smoothed |
| Wrap mode (repeat, clamp) | What sampling outside 0 to 1 does: tile or stretch the edge |
| Shared material | One material used by many objects, so a change hits them all |

## Textures and materials

| Term | Meaning |
|---|---|
| Base colour | The surface colour with no lighting, same as albedo |
| Baked lighting | Light and shadow stored in the texture or a lightmap ahead of time |
| De-lighting | Removing lighting from a photo-derived texture so it can be relit |
| Diffuse | Light scattered evenly from a surface; the matte colour |
| Smoothness | The inverse of roughness: how mirror-like a surface is |
| Dielectric | A non-metal; reflects only a small, uncoloured amount of light |
| Specular | The bright mirror-like reflection of a light |
| Energy conservation | A surface never reflects more light than it receives |
| Metallic workflow | PBR style using albedo plus a metallic mask |
| Specular workflow | PBR style using a diffuse colour plus a specular colour map |
| Height map | Greyscale image of surface height |
| Bump mapping | Fake relief by changing lighting from a height map |
| Displacement | Actually moving vertices to add real relief |
| Silhouette | The outline of an object; normal maps cannot change it, displacement can |
| Tangent space | Normal map directions relative to the surface itself, usable on any mesh |
| Green channel convention | Whether green points up (OpenGL) or down (DirectX) in a normal map |
| Ambient occlusion | Darkening in creases where ambient light cannot reach |
| SSAO | Screen-space ambient occlusion: a real-time estimate from the depth image |
| Colour texture | A texture that holds colours people see |
| Data texture | A texture that holds numbers, such as normals or roughness |
| sRGB | The colour encoding for images shown to people |
| Linear | Colour values proportional to light, the right space for maths |
| sRGB-to-linear decode | Converting sRGB texture values to linear before lighting |
| Mipmap | One of the pre-shrunk copies of a texture |
| Minification | A texture shown smaller than its size, so many texels share a pixel |
| Magnification | A texture shown larger than its size, so one texel covers many pixels |
| Texture filtering | The method used to sample a texture |
| Bilinear | Blends the four nearest texels |
| Trilinear | Bilinear plus blending between two mip levels |
| Anisotropic | Extra sampling that keeps textures sharp at steep viewing angles |
| Block compression | GPU texture compression that stores small blocks of pixels |
| Video memory | The graphics card's own memory, also called VRAM |
| Tiling | Repeating a texture across a surface |
| UV scale | Multiplier on UVs that sets how often a texture repeats |
| Seamless texture | A texture that repeats with no visible join |
| Texel density | Texels per unit of world size; should match across objects |
| Shader | A program that runs on the GPU to compute positions or colours |
| Material instance | A child of a material with its own parameter values |
| Per-instance parameter | A value that differs for each object while the material is shared |
| Padding (gutter) | Empty border pixels between atlas pieces to stop bleeding |
| Channel packing | Storing different maps in the red, green and blue channels of one image |
| ORM | Packed map: occlusion in red, roughness in green, metallic in blue |
| Map slot naming | The agreed names for each texture slot (albedo, normal, roughness) |

## Shader verification

| Term | Meaning |
|---|---|
| Compile error | The shader fails to build and gives an error message |
| Visual bug | The shader builds but the picture is wrong |
| Claim versus evidence | What someone says works versus a check that shows it |
| Observed versus inferred | What you actually saw versus what you guessed from it |
| Headless mode | Running with no window |
| Software renderer | Drawing on the CPU, giving the same output on any machine |
| Golden image | A saved correct output that new renders are compared against |
| Reference image | An image a render is compared to |
| Controlled input | Fixing every input so a run can be repeated |
| Local/world/view/screen space | The four coordinate spaces: relative to the object, the level, the camera, and the display |
| Model matrix | Maths that turns local coordinates into world coordinates |
| Inverse transpose (normal matrix) | The matrix that transforms normals correctly when scale is uneven |
| Normalize | Rescale a vector to length 1 |
| Full precision | 32-bit floating point numbers in a shader |
| Half precision | 16-bit floating point numbers; faster but coarser |
| Divergence | Neighbouring fragments taking different branches, which slows the GPU |
| Warp/wavefront | A group of GPU threads that run in lockstep |
| Default value | The value a parameter has when nothing sets it |
| Test oracle | The source of the right answer a test compares to |
| Specification oracle | A test oracle derived from the written spec |
| False positive | A check passes though the thing is wrong |
| False negative | A check fails though the thing is right |
| Linear interpolation (mix/lerp) | Blending two values by a fraction from 0 to 1 |
| Fragment invocation | One run of the fragment shader for one fragment |
| Full-screen pass | A shader drawn over the whole screen, such as a post effect |
| Premultiplied alpha | Colour already multiplied by alpha |
| Vertical flip | An image upside down because the engines' y directions differ |
| Pinned clock | A fixed time value so animated shaders render the same each run |
| Per-platform reference | A separate reference image for each platform's slight differences |

## Particles

| Term | Meaning |
|---|---|
| Particle | One small short-lived sprite or mesh in an effect |
| Emitter | The thing that spawns particles |
| Particle system | The emitter plus the rules for its particles |
| Emission shape | The volume particles spawn in: point, sphere, box |
| Initial velocity | The speed and direction a particle starts with |
| Spread | The cone angle of random variation around the emission direction |
| Emission rate | Particles spawned per second |
| Burst | Many particles spawned at one instant |
| Looping | The effect repeats forever |
| Lifetime | How many seconds a particle lives |
| Live count | How many particles exist right now |
| Steady state | The point where births equal deaths so live count levels off |
| Prewarm | Starting an effect as if it had already run a while |
| Gravity (particles) | Constant downward acceleration applied to particles |
| Scale curve | A curve for particle size over its life |
| Colour ramp | A gradient for particle colour over its life |
| Normalised age | A particle's age from 0 at birth to 1 at death |
| CPU particles | Simulated on the processor; flexible, fewer particles |
| GPU particles | Simulated on the graphics card; many particles, less control |
| Simulation | The step that updates particle positions and states |
| Cosmetic effect | An effect that changes looks only, never gameplay |
| Local coordinates | Particles move with the emitter |
| World coordinates | Particles are left behind as the emitter moves |
| Billboard | A flat quad that always faces the camera |
| Mesh particle | A particle drawn as a 3D mesh instead of a flat quad |
| Fill rate | How many pixels the GPU can draw per second |
| Random seed | Starting number for random choices; same seed, same result |
| Determinism | Same inputs and seed give the same output every run |
| Parenting | Attaching the effect to another object so it follows |
| Headless run | Running without a window, so visuals are not shown |
| Dummy renderer | A do-nothing renderer used for headless runs |
| State vs visual intent vs cost | Three things to check: what the system holds, what it should look like, and what it costs to draw |
| Process material | Godot's resource that holds a GPU particle system's rules |
| Peak live count | The most particles alive at once |
| Average live count | The mean number alive over time |

## Animation foundations

| Term | Meaning |
|---|---|
| Texture atlas (animation) | One packed image holding frames or sprites |
| Frame-by-frame | Animation made of separate drawn images played in order |
| Frame index | The number of the frame currently shown |
| Cell | One frame slot in a sprite sheet grid |
| Grid | Rows and columns that divide a sheet into cells |
| Cutout | 2D animation of separate body parts moved and rotated |
| Procedural | Motion generated by code or maths instead of authored by hand |
| Retargeting | Applying an animation made for one skeleton to a different one |
| Blend | Mix two animations together |
| Blend weight | How much each animation contributes, from 0 to 1 |
| Blend space | A 1D or 2D map of clips mixed by parameter values |
| Nearest-neighbour and linear filtering | Blocky versus smooth texture sampling |
| Resolution independence | Looks right at any size, as vector art does |
| Blend shapes | Stored vertex shapes mixed by weight, for faces (morph targets) |
| Skinning | Deforming the mesh by the bones |
| Vertex weights | The per-vertex influence of each bone |
| Skeleton | The hierarchy of bones |
| Armature | Blender's word for a skeleton |
| Track | One property's keyframes inside a clip |
| Timeline | The time axis showing keyframes |
| Playhead | The marker for the current time on the timeline |
| Animation player | The node or component that plays clips (AnimationPlayer in Godot) |
| Easing (ease-in, ease-out) | Slow start / slow end speed curve |
| Forward kinematics | Rotate each joint from the parent downward to pose the limb |
| Inverse kinematics | Choose a target and compute the joints that reach it |
| Pole or hint | A helper target that sets which way an IK elbow or knee bends |
| In-place animation | A clip that does not travel; code moves the character |
| Loop seam | A visible jump where the last frame meets the first on a loop |
| Loop mode | Setting for whether a clip plays once, loops or ping-pongs |
| Ping-pong | Play forward then backward repeatedly |
| Playback speed scale | A multiplier on how fast a clip plays |
| Fixed physics step | Physics updated in equal slices of time |
| Animation event | A function call triggered at a point in a clip |
| Method track | Godot track that calls a function at a chosen time |
| Authored clip versus tween | A clip drawn by an artist versus motion computed by code |

## Animation and interaction

| Term | Meaning |
|---|---|
| State | One named mode of a state machine, such as idle or run |
| Condition | A test on a parameter that must hold for a transition |
| Guard | A condition that must be true before a transition may fire |
| Interrupt | A transition that cuts off the current state early |
| Priority | Which transition wins when several are true at once |
| Any State | Unity node whose transitions can fire from every state |
| Stuck state | A state the machine cannot leave |
| Exit-time transition | A transition that waits for the clip to reach a set point |
| Impossible (missing) transition | A path the design needs but no transition provides |
| Forced state | A state set directly in code, skipping transitions |
| Reachable | Can be entered from the start state by some sequence of transitions |
| Dead end | A state with no exit |
| Animation tree | Godot's graph of blends and state machines |
| AnimationPlayer | Godot node that plays clips |
| Animator Controller | Unity asset holding an animation state machine |
| Animation Blueprint | Unreal asset holding an animation state machine and logic |
| Nesting | A state machine placed inside a state of another |
| Trigger (Unity parameter) | A one-shot flag that clears itself after a transition uses it |
| Update | The per-frame step that advances logic |
| Sampling | Reading a value at one moment, so brief events between samples can be missed |
| Intermittent fault | A bug that appears only sometimes |
| Input lock | Ignoring player input during an animation |
| Restart | Playing a clip again from the start |
| Input buffer | Remembering a press for a few frames and acting on it later |
| Cooldown | A wait before an action can be used again |
| Animation lock | The action cannot be changed until the animation finishes |
| Jump buffering | Remembering an early jump press until landing |
| Property track | A track that animates any property, not just bones |
| Finished signal | Event sent when a clip ends |
| Startup | The windup frames before an attack can hit |
| Active | The frames in which an attack can hit |
| Recovery | The frames after an attack before the character can act |
| Hit list | The record of targets already hit so one swing hits each once |
| Cancel window | The frames in which an action may be interrupted by another |
| Cross-fade | Blend smoothly from one clip to the next over a short time |
| Loop | A clip that repeats |
| Threshold | The value at which a condition or blend changes |
| Single source of truth | One place holds the state; everything else reads it |
| Authority | The part of the system allowed to change a value |
| Enumerable transitions | A transition list short enough to list and check completely |

## Audio and triggers

| Term | Meaning |
|---|---|
| AudioStreamPlayer | Godot node that plays sound with no position |
| AudioStreamPlayer3D | Godot node that plays sound from a point in 3D |
| Positional and non-positional | Sound that comes from a place versus sound heard equally everywhere |
| Listener | The point the sound is heard from, usually the camera or player |
| Attenuation | Sound getting quieter with distance |
| Falloff | The shape of how volume drops with distance |
| Maximum distance | Past this distance the sound is silent |
| Handler | The function that responds to a signal |
| Stream | The audio data being played |
| Bus effect | An effect such as reverb added to a bus |
| Reverb | Echo of a space, giving a sense of room |
| Side-chain | Using one sound's level to control an effect on another |
| Gain staging | Setting levels at each step so nothing clips or gets too quiet |
| dBFS | Decibels relative to digital full scale; 0 is the maximum |
| Enter, stay and exit events | Fired when an overlap starts, continues and ends |
| Contact event | A signal from a collision or overlap |
| Voice | One playing instance of a sound |
| Audio clock | The sound hardware's own timing, which is the true audio time |
| Mixing block | A small chunk of audio mixed at once; sets timing precision |
| Output latency | Delay between playing a sound and hearing it |
| Mix boundary | The edge of a mixing block, where timing snaps |
| Cue | A named sound event in an audio system |
| Sound Cue | Unreal asset that combines and randomises sounds |
| Process mode | Setting for whether a node runs while the game is paused |
| Signal versus polling | Being told when something happens versus checking every frame |
| Node lifetime | How long a node exists, which decides whether its sound finishes |
| AudioClip | Unity asset holding the sound data |
| AudioSource | Unity component that plays an AudioClip |
| AudioListener | Unity component that hears sound, one per scene |
| Audio Mixer group | Unity's bus for routing and effects |
| Play Sound 2D | Unreal node that plays an unpositioned sound |
| Play Sound at Location | Unreal node that plays a sound at a world position |
| Attached audio component | Unreal sound source that follows its parent Actor |

## Profiling and optimization

| Term | Meaning |
|---|---|
| Frame time | Milliseconds taken to produce one frame |
| Frame budget | The frame time you can afford: 16.7 ms at 60 FPS |
| FPS | Frames per second |
| Refresh rate | How often the display updates, in hertz |
| Hitch | A single long frame |
| Stutter | Repeated uneven frame times |
| Percentile | The value below which a share of frames fall (the 99th percentile shows worst cases) |
| Mean | The average |
| Median | The middle value; ignores outliers |
| Bottleneck | The slowest stage that limits everything |
| Main thread | The thread running game logic |
| Render thread | The thread preparing drawing work |
| Pipeline | The chain of stages work passes through |
| Instancing | Drawing many copies of one mesh in a single call |
| Frustum culling | Skipping objects outside the camera's view |
| Occlusion culling | Skipping objects hidden behind others |
| Level of detail | Cheaper models used at distance |
| Object pooling | Reusing a fixed set of objects instead of creating and destroying them |
| Acquire | Take an object from the pool |
| Release | Return an object to the pool |
| Pool exhaustion | Every pooled object is in use when another is requested |
| Garbage | Memory no longer used and waiting to be freed |
| Garbage collection | Automatic freeing of unused memory, which can cause hitches |
| Allocation | Asking for new memory |
| VRAM | Graphics card memory |
| Mipmap chain | The full set of shrunken mip levels |
| Texture compression | Storing textures in a smaller GPU format |
| Texture streaming | Loading texture detail only when needed |
| Warm-up | Early frames that run slow while things load and compile |
| Variance | How much measurements differ run to run |
| Noise | Random fluctuation in measurements |
| Vertical sync | Waiting for the display refresh before showing a frame |
| Release build | The optimised build players get |
| Debug build | A slower build with extra checks |
| Target hardware | The device the game must run well on |
| Headroom (frame) | Spare time left in the frame budget |
| Premature optimization | Speeding up something before measuring that it matters |
| Hot spot | The code that takes most of the time |
| Profiler | A tool that measures where time and memory go |
| Capture | A recorded profiler session |

## Game AI

| Term | Meaning |
|---|---|
| Finite state machine | A set of states with transitions; one is active |
| Transition table | A list of every state, condition and next state |
| Behavior tree | A tree of nodes that decides what an agent does each tick |
| Selector | Tries children in order until one succeeds |
| Sequence | Runs children in order and stops at the first failure |
| Success/failure/running | The three results a behavior tree node can return |
| Utility AI | Scores every option and picks the highest |
| GOAP | Goal-oriented action planning: search for actions that reach a goal |
| Precondition | What must be true before an action can run |
| Effect | What an action changes in the world |
| Hysteresis | Different thresholds for switching on and off, to stop rapid switching |
| Flicker | Rapid back-and-forth switching between states |
| Steering | Behaviours that adjust movement toward a goal |
| Seek | Steer toward a target |
| Pursue | Steer toward where a moving target will be |
| Arrive | Seek and slow down to stop at the target |
| Flee | Steer away from a target |
| Separation | Steer away from close neighbours |
| Alignment | Steer to match neighbours' heading |
| Cohesion | Steer toward the neighbours' centre |
| Emergent behavior | Complex group behaviour from simple rules |
| Pathfinding | Finding a route through the world |
| Navigation mesh | Polygons marking where agents can walk |
| Baking | Precomputing data, such as a navmesh, once ahead of time |
| Agent radius | The size of the walker used when building a navmesh |
| A* | Pathfinding that picks the lowest f = g + h node first |
| f/g/h | Total estimated cost / cost so far / estimated cost to goal |
| Admissible heuristic | An estimate that never overestimates the true cost |
| Dijkstra | Pathfinding that expands by cost so far only, with no heuristic |
| Manhattan distance | Distance counted along grid axes only |
| NavigationAgent2D | Godot node that follows a navmesh path |
| Sight range | How far an NPC can see |
| Blackboard | A shared memory of facts the AI reads and writes |
| Omniscient NPC | An NPC that knows everything, including what it should not |
| White noise | Random values with no relation to neighbours |
| Coherent noise | Random values that change smoothly (Perlin, simplex) |
| Octave | One layer of noise at a set scale, added to others |
| Seed | A number that fixes a random sequence |
| Pseudo-random | Looks random but is computed from a seed |
| Validator | A check that tests generated content against rules |
| Generate-and-test | Make content randomly, then reject what fails |
| Constructive generation | Build content by rules that guarantee validity |
| Safety margin | Extra room left so generated content never just barely passes |
| Reinforcement learning | Learning behaviour by trial and reward |
| Agent (RL) | The learner that acts |
| Environment | What the agent acts in |
| Reward | The number telling the agent how well it did |
| Policy | The agent's rule for choosing actions |
| Return | The total reward over time |
| Discount factor | How much future reward is worth compared to now |
| Learning rate | How big each learning update is |
| Q-learning | Learning the value of each action in each state |
| Sparse reward | Reward given only rarely |
| Reward hacking | The agent finds a loophole that scores high but defeats the goal |
| Reward shaping | Adding small hints of reward to guide learning |
| Waypoint | A point along a path |
| Local avoidance | Steering around nearby obstacles and agents |
| Weighted sum | Adding scores each multiplied by an importance weight |

## Agent workflow terms: MCP fundamentals

| Term | Meaning |
|---|---|
| Protocol | An agreed set of message rules two programs follow |
| Model | The AI that reads context and decides what to do |
| Inference | Running the model to get an answer |
| Tool execution | The server actually carrying out a requested tool in the engine |
| Gameplay execution | The game running for the player, separate from the editor-side agent |
| Host | The AI application that contains the model and runs clients |
| Client | The part of the host that talks to one MCP server |
| Server | The program that offers tools and resources to the client |
| Local process | A program running on the same machine |
| Tool | A named action the model may call, with typed arguments |
| Resource | Read-only data the server exposes, identified by a URI |
| Prompt | A reusable message template a server offers |
| URI | A text address that names a resource |
| Tool discovery | The client asking the server which tools exist |
| Advertise | A server announcing the tools and capabilities it offers |
| Input schema | The machine-readable description of a tool's arguments |
| Schema validation | Checking arguments against the input schema before running |
| Semantics | What a name or value actually means, beyond its type |
| Units | The measure a number is in: metres, degrees, pixels |
| Coordinate space | Which frame (local or world) a position is expressed in |
| Read-back | Querying the result after a change to confirm it |
| JSON-RPC | The message format MCP uses: JSON requests and responses |
| Request | A message asking for something and expecting a reply |
| Response | The reply to a request |
| Notification | A one-way message that expects no reply |
| Id | The number tying a response to its request |
| Correlation | Matching related messages or log entries together |
| Stdio | Talking through standard input and output of a subprocess |
| Subprocess | A program started and controlled by another program |
| Streamable HTTP | MCP's network transport for remote servers |
| Transport | The channel messages travel over |
| Transport failure | The channel broke, as opposed to the tool failing |
| Tool execution error | The tool ran and reported a failure |
| Initialization | The opening handshake that sets versions and capabilities |
| Protocol revision | A dated version of the protocol both sides must agree on |
| Capability | A feature a side declares it supports |
| Interoperability check | Testing that different clients and servers work together |
| Snapshot | A saved copy of state at one moment |
| Stale | Out of date, no longer matching reality |
| Re-resolve | Look the target up again instead of trusting an old reference |
| Actor vs GameObject | Unreal's and Unity's names for the same idea of a scene object |
| Retry limit | A cap on how many times a failed step is tried again |
| Stopping condition | The rule that tells the agent to stop |
| Acceptance criterion (agent) | The checkable condition that says the task is finished |
| Verification | Confirming a result with an independent check |
| Identifier vs display name | A unique ID versus a label that may repeat or change |
| Offset vs absolute destination | Move by an amount versus move to a place |
| Argument validation | Rejecting bad arguments before acting |
| Execution failure | The action started but did not complete |
| Data-disclosure boundary | The line past which data must not leave |
| Permission boundary | The limit of what the agent is allowed to do |
| Context filtering | Giving the model only the data it needs |
| Scoped tool | A tool limited to a narrow job or area |
| Minimal trace | A log that keeps only what is needed |
| Lock | A marker preventing two agents editing the same thing |
| Conflict | Two changes that cannot both apply |
| Shared layer | A layer or space several agents or people edit at once |
| Adapter | Code that translates between one interface and another |

## Agent workflow terms: Unity workflows

| Term | Meaning |
|---|---|
| Spark | Unity's earlier AI assistant feature name, here an example of a product that was replaced |
| MCP (Model Context Protocol) | The open standard for connecting AI apps to tools and data |
| Deprecated | Still present but scheduled for removal; do not start new work on it |
| Replacement | The newer feature to use instead of a deprecated one |
| Checkpoint | A saved state you can return to |
| Rollback route | The planned way to undo a change |
| Read query | A request that only looks and changes nothing |
| Reversible edit | A change that can be undone cleanly |
| Authorization | Deciding whether an identity may do an action |
| Project identity vs scene identity | Which project is open versus which scene inside it |
| Asset path | The location of an asset inside the project |
| Prefab asset | The saved prefab file |
| Prefab instance | A copy of a prefab placed in a scene |
| Apply | Push an instance's change back into its prefab |
| Revert | Discard an instance's override and match the prefab |
| Shared material | The material asset used by many objects; editing it changes all |
| MaterialPropertyBlock | Unity object giving per-renderer values without making a new material |
| Serialized field | A field Unity saves and shows in the Inspector |
| Compilation error | A script fails to compile and nothing new runs |
| Compiler diagnostics | The error and warning messages from the compiler |
| In-memory vs saved state | Changes in the open editor versus those written to disk |
| Dirty scene | A scene with unsaved changes |
| Local vs world transform | Position relative to the parent versus to the level |
| Partial failure | Some parts of a batch succeeded and some failed |
| Idempotent | Repeating it gives the same result as doing it once |
| Targeted retry | Retrying only the part that failed |
| Narrow tool | A tool that does one specific thing |
| General script evaluator | A tool that runs arbitrary code; powerful and risky |
| Validation | Checking that something is correct before or after |
| Blast radius | How much can be damaged if something goes wrong |
| Least privilege | Give only the access the job needs |
| Audit record | A log of who did what |
| Provenance | Where something came from |
| Target platform | The device or OS the build is for |
| Observable check | A check you can see the result of |

## Agent workflow terms: Unreal workflows

| Term | Meaning |
|---|---|
| MCP server | The program offering tools to the AI app |
| Toolset | A named group of related tools |
| Catalog | The list of tools a server offers |
| Endpoint | The address a server listens on |
| Editor automation | Using tools to build and change the project in the editor |
| Runtime AI | AI used while the game runs, such as NPC behaviour |
| Spawn | Create an Actor in the level |
| Collision response | Unreal's setting for block, overlap or ignore |
| Graph | The node-and-wire view of a Blueprint |
| Branch | A Blueprint node that picks a path by a true or false test |
| Compile | Build the Blueprint or code so changes take effect |
| Game thread | The main thread where Unreal runs gameplay and editor actions |
| Serial | One after another |
| Concurrent | Overlapping in time |
| Latency | Delay between request and result |
| Throughput | How much work is done per unit of time |
| Synchronous | The caller waits for the answer |
| Asynchronous | The caller continues and gets the answer later |
| Job identifier | An ID for a long task used to check on it later |
| Dirty | Changed in memory but not yet saved |
| Package | Unreal's saved asset file |
| Dependency | Something else that this item needs |
| Assertion | A statement in a test that must be true |
| Fixture | Fixed setup data a test starts from |
| Play-in-editor | Running the game inside the editor |
| Transient | Temporary, not saved |
| Authoring data | The editable source content, versus runtime data |
| Material instance | A material child with its own parameter values |
| Dynamic material instance | A material instance created and changed at run time |
| Preflight | Checks run before an operation starts |
| Per-target result | A separate success or failure for each item in a batch |
| Target identity | The exact object an action is aimed at |
| Port forwarding | Passing traffic from one machine's port to another |
| Transform | Position, rotation and scale together |
| Relative space | Coordinates measured from another object |
| Overlap event | Event fired when two objects begin overlapping |
| Duplicate binding | The same event hooked to a function twice, so it runs twice |
| Mutating tool | A tool that changes things |
| Parameter | A named input to a function or tool |
| Argument | The value passed for a parameter |
| Validate | Check that input or output is correct |
| Smoke test | A quick check that the basics work |
| Diagnostics | Messages that explain what went wrong |

## Agent workflow terms: security

| Term | Meaning |
|---|---|
| Local | Runs on your own machine |
| Remote | Runs on another machine over a network |
| Cloud | Run on a provider's servers |
| On-premises | Run on hardware your organisation owns |
| Hybrid | A mix of local and cloud |
| Context minimization | Sending the model as little data as the task needs |
| Egress | Data leaving your system |
| Telemetry | Usage data sent back to a vendor |
| Trust boundary | A line where data passes between trusted and untrusted parties |
| Scope | The set of things a permission or task covers |
| Prompt injection | Hidden instructions in input that try to steer the model |
| Indirect injection | Injected instructions arriving in content the agent reads, not the user's message |
| Untrusted content | Data from a source you do not control |
| Egress filtering | Blocking data from going to unapproved destinations |
| Authentication | Proving who you are |
| Encryption in transit | Scrambling data while it travels |
| Secret | A key, token or password that must stay private |
| Rotation | Replacing a secret regularly |
| Hardcoding | Writing a secret directly in code |
| Relative path | A file path measured from the current folder |
| Absolute path | A full path from the root of the file system |
| Canonicalization | Turning a path into its single true form before checking it |
| Path traversal | Using ../ to escape an allowed folder |
| Symbolic link | A file that points to another location |
| Annotation | A label that describes a tool's behaviour, such as read-only |
| Enforcement | Actually blocking a rule, as opposed to just stating it |
| Approval granularity | How fine each approval is: per action, per tool or blanket |
| Containment | Limiting damage once something goes wrong |
| Evidence preservation | Keeping logs and state intact for investigation |
| Offline | No network connection |
| Local inference | Running the model on your own machine |
| Pinning | Fixing a version so it does not change unexpectedly |
| Disposable project | A throwaway copy where mistakes cost nothing |
| Audit log | A tamper-resistant record of actions |
| Redaction | Removing sensitive parts from data |
| Retention | How long data is kept |
| Correlation identifier | An ID that ties related log lines together |
| Quarantine | Isolating something suspect |
| Sanitize | Clean input so it cannot cause harm |
| Exfiltration | Stealing data out of a system |
| Role-based access control | Permissions given by role |
| Deny by default | Anything not explicitly allowed is blocked |
| Allowlist | A list of what is permitted |
| Denylist | A list of what is forbidden |
| Revocation | Withdrawing a permission or credential |
| Confidentiality | Only the right people can read the data |
| Integrity | Data is not altered improperly |
| Availability | The system is up when needed |

## Agent workflow terms: verification

| Term | Meaning |
|---|---|
| Claim vs evidence (agent) | The agent's statement versus the artefact that proves it |
| Acceptance evidence | The proof collected to show a criterion is met |
| Acceptance criteria | The conditions that must hold for the work to be accepted |
| Compile/import validation | Checking that scripts compile and assets import |
| Behavioural test | A test of what the game does when it runs |
| Tautology | A test that cannot fail because it checks itself |
| Assertion (test) | A statement a test requires to be true |
| Negative case | A test that expects rejection or failure |
| Positive path | A test of the normal, successful case |
| Static inspection | Examining files or code without running them |
| Random seed (test) | A fixed starting number so random results repeat |
| Nondeterminism | Different results from the same inputs |
| Simulation step | One advance of the simulated game |
| Flaky test | A test that passes and fails with no change |
| Bounded wait | Waiting up to a limit, then failing |
| Asynchronous import | Import that finishes later in the background |
| Idempotency / idempotency key | Same request twice has one effect / the label that lets a retry be recognised |
| Existence check | Confirm something is there before acting on it |
| Stable identifier | An ID that does not change when names or positions do |
| Operation record | A log entry of what was done |
| Atomic | All of it happens or none of it |
| Partial commit | Only some of a batch applied |
| Rollback | Undo to the last good state |
| Transaction | A group of changes treated as one unit |
| Recovery record | Saved data needed to put things back |
| Precondition check | Verify the starting condition before acting |
| Resume vs restore | Continue where it stopped versus go back to an earlier state |
| Unit (measurement) | The measure a value is in |
| Tool contract | The agreed inputs, outputs and behaviour of a tool |
| Engine-neutral specification | A requirement written in terms that fit any engine |
| MCP vs tool catalogue | The protocol versus the list of tools one server offers |
| Tool inventory | A list of which tools exist |
| Fair comparison | Comparing options under the same conditions |
| Controlled failure | A failure caused on purpose to test handling |
| Frame rate | Frames per second |
| Benchmark | A repeatable measurement for comparison |
| Profiling | Measuring where time and memory go |
| Packaged build vs editor | The shipped game versus running inside the editor |
| Export configuration | The settings used when packaging a build |

## Wrong word, right word

- "Pan closer" is a **dolly in**. "Zoom out by moving back" is a **dolly out**.
- "A normal map for colour" is **albedo**. "Fragment shader moves vertices" is a **vertex shader**.
- "A trigger that blocks" is a **collider**. "A bone in a sprite sheet" is a **rig** (bones) or a **sprite sheet** (frames), not both.
- "Fast on a fast PC" means the movement is missing **delta time**.

## Compress, read and tell apart (sets k01 to k03)

| Term | Meaning |
|---|---|
| Unpacking a term | Turning a word into constraints you can check, such as a window length, a trigger and a result |
| Compressing a behaviour | Choosing the one exact term that names a described behaviour |
| Monitoring / monitorable | Area setting for detecting others / area setting for being detectable by other areas |
| Call down, signal up | A parent calls its child's methods; a child tells its parent by emitting a signal |
| Apex | The highest point of a jump |
| Cutting the jump | Reducing upward velocity on button release, only while rising, for variable jump height |
| Double scaling | Multiplying by delta and then handing the result to a call that already applies the time step |
| Evidence versus claim | A claim says it works; evidence is output, a measurement or a failing-then-passing test |
| Baseline | The measurement taken before a change, so the change can be compared with it |
| Scope violation | The agent changed something it was told not to touch, or was never asked to touch |
| Tautological test | A test whose expected value was copied from the code's own output, so it cannot find a wrong formula |
| Mutation check | Break the code on purpose and confirm the test fails |
| False friend | A word with two meanings, or a near neighbour, that sounds like the one you meant |
| Scene versus level | A scene is a saved node tree (any size); a level is a playable area, usually built as a scene |
| Stable | Depends on context: no jitter, a stable release, or a sort that keeps equal items in order |
| Normal versus normal map | A direction at a point on a surface / a texture storing that direction per texel |
| Static | StaticBody (physics), static typing (script), static lighting (rendering) |
| Origin versus pivot | The point a position refers to / the point rotation happens around |
| TileSet versus TileMap | The palette of tiles and their shapes / the node that places tiles on a grid |
