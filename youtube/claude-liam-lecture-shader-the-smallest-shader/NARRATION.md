# The Smallest Shader

## BOPEN

Godot Shader Techniques. The Smallest Shader. Separate placing vertices from coloring fragments.

## BIDEA

Hola. This is Liam, in for Bear. The key correction is that a color is enough. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Vertex: A mesh point processed before rasterization. Fragment: A candidate sample produced by rasterization. Uniform: A material parameter shared by shader invocations.

## B01

This shader has two jobs. The vertex function places mesh points. Rasterization turns triangles into fragments. The fragment function assigns their color. Neither function needs to know the whole picture.

## B02

Read the matrix chain from right to left. Model places the object in the world. View expresses that world relative to the camera. Projection produces clip coordinates.

## B03

The fourth coordinate is one because this is a position. Translation must affect it. The result is a four-component clip position; perspective division comes later in the rendering pipeline.

## B04

Now the fragment function writes the same uniform color everywhere. The sphere loses its shading cues and looks like a flat disc. Its geometry has not disappeared.

## B05

Watch the color change from teal to terracotta. Every visible fragment receives the new material value. We changed an input, not the triangle mesh or the shader program.

## B06

Unshaded means Godot does not add its built-in lighting here. A light node will not create a highlight on this material. The silhouette still comes from the mesh.

## B07

The source-color hint identifies a color input. In Forward Plus, color conversion matters. A displayed color is not automatically the same numeric quantity as a linear-light shader value.

## B08

Writing POSITION makes this shader responsible for the entire clip position. Godot can normally do that transformation for you. Keep this explicit version to understand the pipeline, not because every material requires it.

## BVDT

Let’s recap with Claude. The vertex stage positions the mesh. The fragment stage supplies its color. A uniform exposes a material control. Unshaded output has no built-in lighting. Liam, in for Bear.

## BHTF

Make an unshaded Godot material with a color uniform. Change the color, then rotate the mesh. Explain which change alters the flat color and why. Check two things: Rotation changes the silhouette, not the chosen color. The material exposes its color in the Inspector.

## BOUT

The Smallest Shader. At Nik Bear Brown.
