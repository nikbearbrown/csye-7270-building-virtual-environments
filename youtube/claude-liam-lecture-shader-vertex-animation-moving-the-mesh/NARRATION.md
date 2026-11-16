# Vertex Animation: Moving the Mesh

## BOPEN

Godot Shader Techniques. Vertex Animation: Moving the Mesh. Trace a time-dependent displacement and recognize stale lighting inputs.

## BIDEA

Jambo. This is Liam, in for Bear. The key correction is that deformation also needs updated lighting inputs. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Vertex: A mesh position processed by the vertex stage. Amplitude: The size and direction of an offset. Frequency: How quickly a phase varies across space.

## B01

The vertex function adds an offset to the mesh position before Godot projects it. Unlike normal mapping, this operation really moves mesh vertices and can change the visible outline.

## B02

The sine receives time multiplied by speed, plus the original horizontal position multiplied by frequency. Time moves the wave forward. Position makes different vertices sit at different phases.

## B03

The offset vector controls both amplitude and direction. A vertical offset makes an up-and-down deformation. A sideways offset pushes along a different local axis. It is an object-space displacement.

## B04

If the offset is zero, multiplying it by any sine value still produces zero. The untouched default shader does not wobble. The demo material supplies a nonzero override to make the effect visible.

## B05

Watch the vertical offset grow. The silhouette now moves because actual vertices move. The finite mesh resolution limits how smoothly that displacement can describe the intended wave.

## B06

Before changing VERTEX, this port computes the world position used for the eye vector. It therefore keeps the direction to the original position, not the displaced one.

## B07

The normal is also carried from the original mesh. It is not recomputed from the deformed surface. A moving outline with inconsistent shading is an expected limitation of this teaching port.

## B08

For a more complete deformation, update the lighting position and derive suitable deformed normals. The lesson here is the vertex displacement mechanism and the extra responsibilities that come with moving geometry.

## BVDT

Let’s recap with Claude. A sine wave controls the displacement. Time animates its phase. The offset sets amplitude and direction. The port retains undeformed lighting inputs. Liam, in for Bear.

## BHTF

Set the vertex offset to zero, then raise its vertical component. Compare silhouette motion with the highlight. Explain which lighting inputs would need updating for a physically consistent deformed surface. Check two things: Zero offset produces no displacement. The current shader retains its original normal and eye vector.

## BOUT

Vertex Animation: Moving the Mesh. At Nik Bear Brown.
