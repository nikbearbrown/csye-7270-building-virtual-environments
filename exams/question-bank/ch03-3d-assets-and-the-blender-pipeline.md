# Chapter 3: 3D assets and the Blender pipeline

## MA-ch03.1

A modeller and a coding agent need to talk about the parts of a polygon mesh. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A quad is a face with four sides.
- [ ] B. An n-gon is a face with more than four sides.
- [ ] C. Triangulation is the step that merges two separate meshes into one object.
- [ ] D. A vertex is a single point with a position in 3D space.
- [ ] E. A face is a straight line that joins two vertices.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Quad is the name for a four-sided face.
- B: N-gon is the term for a face with five or more sides.
- C: Triangulation splits faces into triangles; it does not merge meshes.
- D: A vertex is a point; edges and faces are built from vertices.
- E: A straight line joining two vertices is an edge; a face is the surface bounded by edges.

**Source:** Mesh anatomy

## MA-ch03.2

A modelling tool shows a face count and an engine profiler shows a triangle count for the same mesh. Check each statement that is true about the two measures. Each statement is worth 1 point (5 points total).

- [ ] A. A quad contributes two triangles to the triangle count.
- [ ] B. Face count and triangle count are two names for the same number.
- [ ] C. Triangle count is the number of triangles left once the faces have been triangulated.
- [ ] D. Vertex count and triangle count measure the same thing.
- [ ] E. A five-sided face triangulates into five triangles.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: A quad is split along a diagonal into two triangles.
- B: A quad is one face but two triangles, so the numbers differ.
- C: GPUs draw triangles, so the triangle count is taken after triangulation.
- D: Vertices are points; triangles are surfaces made from three of them.
- E: An n-sided face gives n minus 2 triangles, so five sides give three.

**Source:** Triangle count versus face count

## MA-ch03.3

An interviewer says: 'My modelling tool reports 8 vertices for a hard-edged cube, yet the engine's profiler reports 24.' Check each statement that is true as an explanation. Each statement is worth 1 point (5 points total).

- [ ] A. A profiler that reports more vertices than the modelling tool has miscounted.
- [ ] B. A UV seam forces the GPU to split a vertex because the two sides have different UV coordinates.
- [ ] C. A hard edge gives the corner a different normal on each face, so the GPU keeps a separate vertex per normal.
- [ ] D. A GPU vertex carries attributes such as a normal and UV coordinates in addition to a position.
- [ ] E. Smooth shading raises the vertex count by giving each face its own normal at a corner.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: The two tools count different things: corner positions versus full GPU vertices.
- B: The same position with two UV values is two GPU vertices.
- C: A different normal at the same position needs a duplicated GPU vertex.
- D: A GPU vertex bundles position, normal and UV, so differing attributes mean a new vertex.
- E: Smooth shading shares one normal at a corner; separate normals per face describe flat shading.

**Source:** Vertex count in the tool versus on the GPU

## MA-ch03.4

An imported crate has a normal map assigned, yet a teammate asks the agent to 'fix the normals'. Check each statement that is true about the two terms. Each statement is worth 1 point (5 points total).

- [ ] A. A normal is a direction perpendicular to a surface, used for lighting.
- [ ] B. A normal map changes how light is worked out for each pixel and leaves the geometry unchanged.
- [ ] C. A normal map adds real triangles to the mesh to make the surface bumpy.
- [ ] D. A normal map is a texture that stores a direction per texel to fake fine surface detail.
- [ ] E. 'Recalculate the normals' and 'replace the normal map' are the same instruction.

**Key:** A=T B=T C=F D=T E=F

**Why:**

- A: Normals are the geometry directions that lighting uses.
- B: The detail is a lighting effect, not new geometry.
- C: A normal map is image data and leaves the triangle count alone.
- D: The map holds per-texel directions that bend the lighting.
- E: One edits the mesh's face directions, the other edits or swaps an image.

**Source:** Normals versus normal maps

## MA-ch03.5

Some faces of an imported crate look black or vanish when viewed from outside. A developer tells the agent 'fix the shading'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Smooth shading and flipped normals are the same problem.
- [ ] B. Backface culling means deleting the rear faces of an object from the file.
- [ ] C. Faces whose normals point into the object are described as having flipped normals.
- [ ] D. Backface culling skips drawing a face when it is seen from the side its normal points away from.
- [ ] E. 'Fix the shading' is as precise as 'recalculate the normals so they point outward'.

**Key:** A=F B=F C=T D=T E=F

**Why:**

- A: Smooth shading is how normals are shared across faces; flipped normals are a wrong direction.
- B: Culling is a drawing-time skip and leaves the file unchanged.
- C: Flipped normals are inside-out faces.
- D: The renderer discards faces seen from behind, which is why inward faces vanish.
- E: The first phrase does not name the cause; the second names both the term and the direction.

**Source:** Flipped normals and culling

## MA-ch03.6

A coding agent builds a crate mesh and a wood texture. The texture is missing on one object and looks stretched on another. Check each statement that is true about the terms involved. Each statement is worth 1 point (5 points total).

- [ ] A. Unwrapping lays the 3D surface out flat in 2D to produce the UV map.
- [ ] B. A UV map gives each vertex a 2D coordinate in the texture.
- [ ] C. Stretched wood grain points to a poor UV layout rather than a low-resolution image.
- [ ] D. U and V name the axes of texture space, which keeps them distinct from the X, Y and Z of 3D space.
- [ ] E. A texel is one corner of a mesh face.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: Unwrapping produces the flat layout that the UV map stores.
- B: UVs link surface points to image points.
- C: Stretching comes from layout versus surface shape, not the pixel count of the image.
- D: Texture space has its own axes, named U and V.
- E: A texel is one pixel of a texture.

**Source:** UV maps and unwrapping

## MA-ch03.7

A post has a metal pole and a red cloth pennant, held in two material slots on one object. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A material slot is a position on an object that holds a material, and faces are assigned to a slot.
- [ ] B. A material and a texture are two words for the same image.
- [ ] C. A texture is an image; a material describes how a surface is shaded and may use textures as inputs.
- [ ] D. Extra materials on one object add triangles to the mesh.
- [ ] E. A draw call is the count of triangles in a mesh.

**Key:** A=T B=F C=T D=F E=F

**Why:**

- A: Faces point at slots and slots hold materials.
- B: A material is a shading description; a texture is one possible input to it.
- C: Textures feed materials; they are different things.
- D: Materials change draw cost, not the number of triangles.
- E: A draw call is a request to the GPU to draw a batch; it is not a triangle count.

**Source:** Material slots and materials

## MA-ch03.8

A door model rotated by script swings about its middle instead of its edge, and a 1 m crate sinks halfway into the floor placed at y = 0. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The origin, also called the pivot, is the point an object's position and rotation refer to.
- [ ] B. A 1 m crate with its origin at the centre sits exactly on the floor when placed at y = 0.
- [ ] C. Moving the origin in the modelling tool drags the visible mesh along with it.
- [ ] D. The phrase 'make a door' already tells the agent where to put the pivot.
- [ ] E. A swinging door needs its pivot on the hinge edge.

**Key:** A=T B=F C=F D=F E=T

**Why:**

- A: Origin and pivot are the reference point for transforms.
- B: A centred origin puts half the crate's height below y = 0.
- C: The origin can be moved while the geometry stays where it is.
- D: The phrase names the object, not its pivot.
- E: Rotation happens about the origin, so it belongs at the hinge.

**Source:** Origin and pivot

## MA-ch03.9

A modeller thinks in centimetres and builds a tree 540 units tall; the engine treats one unit as one metre. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Scale and size mean the same thing.
- [ ] B. Scaling the tree node down repairs the mesh data itself.
- [ ] C. A model built in centimetres and imported as metres appears one hundred times too large.
- [ ] D. Unit and scale are two names for one property.
- [ ] E. In Godot a unit is conventionally read as one metre.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: Size is the extent of the mesh; scale is a multiplier carried by the object or node.
- B: A node scale hides the problem on that node while the mesh stays the wrong size.
- C: The numbers are kept but read in larger units.
- D: A unit is a measure of distance; scale is a multiplier.
- E: The engine's convention is one unit equals one metre.

**Source:** Units and scale

## MA-ch03.10

A cube mesh is 2 m across. The modeller scales the object to (0.1, 0.1, 0.9) to make a pole and exports without applying transforms. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Applying transforms is a step done in the engine after import.
- [ ] B. A non-unit scale on the imported node is inherited by anything built from it, such as a collider.
- [ ] C. Applying the scale changes how the pole looks in the viewport.
- [ ] D. Applying the scale bakes it into the vertex positions and resets the object's scale to 1.
- [ ] E. Before applying, the mesh data can describe a different size from the size the object appears.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: The step belongs in the modelling tool before export.
- B: A node scale propagates to its children.
- C: Apply keeps the look and changes only where the numbers are stored.
- D: Apply moves the scale into the vertices.
- E: The vertices still describe a 2 m cube; the object scale makes it look like a pole.

**Source:** Applying transforms

## MA-ch03.11

A modelling tool treats +Z as up, while glTF and Godot treat +Y as up. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. Blender uses +Z as up, while glTF and Godot use +Y as up.
- [ ] B. Unreal's editor treats +Z as up, as Blender does.
- [ ] C. Up axis names which axis points up; handedness names whether the axes follow a right-hand or left-hand rule.
- [ ] D. A model that lies on its side after import suggests the up axis was not converted on export.
- [ ] E. Up axis and handedness are two names for the same setting.

**Key:** A=T B=T C=T D=T E=F

**Why:**

- A: That is why a conversion is needed between Blender and Godot.
- B: Unreal's editor is Z-up.
- C: They are two separate properties of a coordinate system.
- D: The height stays on the old up axis, so the model appears tipped.
- E: Fixing one leaves the other unchanged.

**Source:** Up axis and handedness

## MA-ch03.12

A developer asks a coding agent to 'export the model for the engine'. Check each statement that is true about the formats named. Each statement is worth 1 point (5 points total).

- [ ] A. A .gltf file is the single binary form, and .glb is the text form.
- [ ] B. A .glb file packs a glTF asset into one binary file.
- [ ] C. OBJ carries skeletal skinning and animation along with geometry.
- [ ] D. glTF is an open interchange format for 3D assets.
- [ ] E. One glTF asset can describe meshes, materials, textures, skins and animations together.

**Key:** A=F B=T C=F D=T E=T

**Why:**

- A: The roles are swapped: .gltf is text plus separate data files.
- B: GLB is the single-file form.
- C: OBJ lacks skinning and animation.
- D: glTF is an open standard for moving 3D assets between tools.
- E: glTF's scene description covers a whole rigged, textured prop.

**Source:** glTF, GLB and OBJ

## MA-ch03.13

A level has a stone archway the player walks through. A developer asks the agent for 'accurate collision'. Check each statement that is true about the shape terms. Each statement is worth 1 point (5 points total).

- [ ] A. A convex hull is the smallest convex shape that encloses the mesh, so on an archway it fills the opening.
- [ ] B. A concave (trimesh) shape follows the mesh triangles, so it can keep the archway opening passable.
- [ ] C. A convex shape has no dents or holes.
- [ ] D. Primitive shapes, such as box, sphere and capsule, are made of the mesh's own triangles.
- [ ] E. In Godot a concave shape works on moving bodies as well as static ones.

**Key:** A=T B=T C=T D=F E=F

**Why:**

- A: A hull cannot have a hole, so it blocks the doorway.
- B: A trimesh follows the triangles exactly, holes included.
- C: Convex means any line between two inside points stays inside.
- D: Primitives are simple analytic shapes and not built from the mesh.
- E: Godot restricts concave shapes to static bodies.

**Source:** Convex versus concave collision

## MA-ch03.14

A character model has 30,000 triangles including a cape and a sword. A developer says to the agent: 'use the model's mesh as its collider'. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. 'Add a collider' already names the shape and size.
- [ ] B. A collider should copy the cape and the sword so they block the player as they look.
- [ ] C. A collision shape is authored separately from the visual mesh and can be much simpler.
- [ ] D. A capsule is a common primitive shape for a character body.
- [ ] E. 'Use the mesh as the collider' asks for a concave (trimesh) shape, which is a poor fit for a moving character.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: The phrase leaves shape and size open.
- B: Copying protrusions makes the character catch on scenery.
- C: Collision geometry is a separate design choice from the visible mesh.
- D: A capsule slides smoothly past edges and is cheap to test.
- E: A trimesh is the slowest option and works on static bodies only in Godot.

**Source:** Collision shape is not the visual mesh

## MA-ch03.15

A stone archway is fixed in the level, a large rock is fixed in the level, and a crate is pushed by the player. The developer picks collision shapes in Godot. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. A single convex hull on the archway keeps the opening passable.
- [ ] B. The pushable crate should use a trimesh shape in Godot.
- [ ] C. The archway is a static body.
- [ ] D. A concave shape suits the archway because the opening stays passable.
- [ ] E. The pushable crate is a moving body, and a box primitive suits it.

**Key:** A=F B=F C=T D=T E=T

**Why:**

- A: A convex hull fills the opening.
- B: Godot allows concave shapes on static bodies only.
- C: A fixed object that other bodies collide with is a static body.
- D: A concave shape can follow the hole.
- E: A body moved by the simulation is a moving body, and a primitive is cheap.

**Source:** Collision shape choice by body type

## MA-ch03.16

A scene has 50 identical trees. A developer asks the agent to add levels of detail (LOD). Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A visible jump when the engine switches versions is called aliasing.
- [ ] B. Extra LOD meshes add no storage or load time.
- [ ] C. The engine picks the LOD version by distance or screen size.
- [ ] D. LOD reduces the number of trees that are drawn.
- [ ] E. LOD keeps several versions of a mesh with decreasing triangle counts.

**Key:** A=F B=F C=T D=F E=T

**Why:**

- A: The visible switch is called popping; aliasing is jagged edges.
- B: Each version is more data to store and load.
- C: Smaller on screen means a cheaper version.
- D: LOD lowers the triangles per tree and leaves the tree count alone.
- E: That is the definition of level of detail.

**Source:** Level of detail

## MA-ch03.17

A developer asks a coding agent to build a crate with a Python file that uses bpy and runs Blender in background mode. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A script that ends without an error has produced a verified asset.
- [ ] B. bpy is the name of Blender's Python API.
- [ ] C. A script is a reproducible recipe that can be reviewed, diffed and rerun.
- [ ] D. A script run in background mode is unable to read the mesh or export a file.
- [ ] E. Background mode runs Blender with no window.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: A clean run can still encode a wrong size, axis or scale.
- B: bpy gives scripts access to Blender's data and operators.
- C: A file is an artifact that can be versioned and rerun.
- D: The same data operations and exports run without a window.
- E: Background mode is also called headless: no interface is shown.

**Source:** Scripting Blender with bpy

## MA-ch03.18

A developer connects a coding agent to Blender through an MCP server and an add-on. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. The model itself runs inside the Blender process.
- [ ] B. MCP is a standard way for an agent to discover and call tools that another program exposes.
- [ ] C. The add-on receives the tool calls and carries them out in Blender.
- [ ] D. MCP is a file format for storing meshes.
- [ ] E. A run-code tool without guards lets whoever can reach the connection run code as the user.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: The model stays in the agent; Blender only executes the calls.
- B: It defines how tools are listed and called.
- C: The add-on is the Blender side of the connection.
- D: MCP is a protocol for tools and has nothing to do with mesh storage.
- E: Unchecked code execution is a real exposure, so keep it local and trusted.

**Source:** What an MCP server is

## MA-ch03.19

A developer wants numbers a headless test can check after import: a post meant to be 0.2 x 1.8 x 0.2 m with Y up, standing on the floor at y = 0, at unit scale. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A bounding box lists the names of the materials on the mesh.
- [ ] B. A bounding box of (0.2, 0.2, 1.8) in a Y-up engine suggests the post lies on its side.
- [ ] C. A lowest point at y = 0 relative to the origin shows the pivot is at the base.
- [ ] D. A node scale of (1, 1, 1) suggests the transforms were applied.
- [ ] E. A bounding box is the smallest box that encloses the mesh, and its extents give width, height and depth.

**Key:** A=F B=T C=T D=T E=T

**Why:**

- A: Materials are read from the surfaces, not from the bounding box.
- B: The 1.8 m height sits on Z instead of Y.
- C: The base touching the origin height means the object stands on the floor.
- D: An unapplied scale would show as a non-unit value.
- E: Extents are the box's size along each axis.

**Source:** Verifying an asset by measuring

## MA-ch03.20

A developer compares phrases for a crate request to a coding agent. Check each statement that is true about which phrase names a term precisely. Each statement is worth 1 point (5 points total).

- [ ] A. 'Add a collision shape' names the shape and its size.
- [ ] B. 'Origin at base centre' names the pivot.
- [ ] C. 'As a .glb' names the export format.
- [ ] D. 'Export it with the usual settings' names the up axis and scale.
- [ ] E. 'Under 200 triangles' names a budget that can be checked.

**Key:** A=F B=T C=T D=F E=T

**Why:**

- A: It leaves the shape and size to the agent.
- B: It states where the origin goes.
- C: GLB is a specific format.
- D: The phrase names no axis or scale; defaults vary.
- E: A triangle count is a number a test can read.

**Source:** Precise asset request wording

## MA-ch03.21

A developer moves between engines and wants the collision terms straight. Check each statement that is true. Each statement is worth 1 point (5 points total).

- [ ] A. Godot's concave shape corresponds roughly to Unreal's complex collision.
- [ ] B. Simple and complex collision are the same shape in Unreal.
- [ ] C. In Unreal, simple collision is made of primitives and convex hulls.
- [ ] D. In Unreal, complex collision is the per-triangle mesh.
- [ ] E. A simulated Unreal object should use complex collision for its movement.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Both mean exact triangle collision.
- B: They are two different shapes used for different jobs.
- C: Simple collision uses cheap shapes.
- D: Complex collision tests the exact triangles.
- E: Simulated bodies rely on simple shapes.

**Source:** Collision vocabulary across engines

## MA-ch03.22

A developer tells an agent: 'Make me a barrel in Blender and put it in my game so the player can bump into it.' Check each statement that is true about which term the vague phrase hides. Each statement is worth 1 point (5 points total).

- [ ] A. 'Bump into it' leaves open whether a solid collider or a trigger is meant.
- [ ] B. 'Not lying on its side' is a statement about the up axis.
- [ ] C. 'Standing on the floor' is a statement about the pivot or origin.
- [ ] D. 'The right size' is a statement about the pivot.
- [ ] E. 'Cheap to draw' is stated with a triangle budget and a material count.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Collision can mean blocking or only reporting.
- B: Orientation depends on which axis is up.
- C: Where the origin sits decides whether the barrel rests on y = 0.
- D: Size is stated in metres, and the unit convention decides it.
- E: Triangle count and material count are the measurable budgets.

**Source:** Say it to the agent: prop request wording

## MA-ch03.23

An imported model arrives with a problem. Check each statement that pairs the symptom with the term that most likely explains it. Each statement is worth 1 point (5 points total).

- [ ] A. A prop that sinks halfway into the floor points to the up axis.
- [ ] B. A prop that lies on its side points to handedness.
- [ ] C. A prop about one hundred times too large points to a unit mismatch.
- [ ] D. A prop with an odd non-unit node scale points to backface culling.
- [ ] E. A prop that rotates about the wrong point points to the material slots.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: Sinking points to the origin sitting at the prop's centre.
- B: Lying on its side points to the up axis, not handedness.
- C: Centimetres read as metres give a factor of one hundred.
- D: An odd node scale points to a scale that was not applied.
- E: Rotating about the wrong point points to the origin.

**Source:** Why imported models arrive wrong

## MA-ch03.24

A coding agent can drive Blender through an MCP session or through a bpy script. Check each statement that is true when comparing them. Each statement is worth 1 point (5 points total).

- [ ] A. A script and an MCP session are the same artifact.
- [ ] B. MCP suits exploring an open scene or making a one-off fix.
- [ ] C. An MCP session leaves a transcript of tool calls.
- [ ] D. A bpy script is a file that can be rerun to regenerate the asset.
- [ ] E. For a prop that has to be regenerated later, an MCP session is a better record than a script.

**Key:** A=F B=T C=T D=T E=F

**Why:**

- A: One is a file, the other a conversation of calls.
- B: Live calls fit exploration and quick edits.
- C: Each call and result appears in the conversation.
- D: A script is a recipe that gives the same asset when rerun.
- E: A single file is easier to diff and rerun than a transcript.

**Source:** MCP versus scripting

## MA-ch03.25

A team is cutting rendering cost for a scene of trees with two materials each. Check each statement that is true about the terms. Each statement is worth 1 point (5 points total).

- [ ] A. A trimesh collision shape adds draw calls.
- [ ] B. Triangle count and draw call count measure the same cost.
- [ ] C. Merging two materials that share a look reduces draw calls.
- [ ] D. A draw call is the count of triangles in a mesh.
- [ ] E. Merging materials changes the triangle count.

**Key:** A=F B=F C=T D=F E=F

**Why:**

- A: Collision shapes are not drawn.
- B: Triangles are surface work; draw calls are batch requests.
- C: Fewer materials usually mean fewer batches.
- D: A draw call is one request to draw a batch.
- E: Merging materials leaves the geometry alone.

**Source:** Mesh cost and materials

## MA-ch03.26

Three symptoms appear on imported models. Check each statement that matches the symptom to the term that explains it and the phrase that fixes it. Each statement is worth 1 point (5 points total).

- [ ] A. Many draw calls on one object point to many material slots.
- [ ] B. 'Reduce the object to two materials, merging slots that share a look' is a precise fix for the slot problem.
- [ ] C. A missing or stretched texture points to absent or poorly laid-out UVs.
- [ ] D. A stretched texture points to inward normals.
- [ ] E. Black or invisible faces point to inward normals.

**Key:** A=T B=T C=T D=F E=T

**Why:**

- A: Each material typically adds a draw call.
- B: It states a number and what to merge.
- C: UVs link the surface to the image.
- D: Normals affect lighting, not how an image is laid on the surface.
- E: Lighting and culling depend on the direction a face points.

**Source:** Normals, UVs and material slots

## MA-ch03.27

An agent reports that an exported prop 'looks right'. Check each statement that is true about what a headless check and a person can each establish. Each statement is worth 1 point (5 points total).

- [ ] A. Whether a collider feels fair is for a person to judge.
- [ ] B. A headless test can judge whether the prop looks good under the game's lighting.
- [ ] C. Reading the lowest point against the origin catches a prop that sinks or floats.
- [ ] D. A headless test can assert the bounding box, the node scale and the material names.
- [ ] E. 'Looks right' and 'measures right' mean the same thing.

**Key:** A=T B=F C=T D=T E=F

**Why:**

- A: Feel is a human judgement.
- B: Appearance under lighting needs a person looking at a render.
- C: The lowest point relative to the pivot shows resting height.
- D: These are numbers that can be read and compared.
- E: A model can look right on screen while a number is wrong.

**Source:** Verifying an asset by measuring
