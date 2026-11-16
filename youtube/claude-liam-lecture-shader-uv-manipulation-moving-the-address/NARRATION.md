# UV Manipulation: Moving the Address

## BOPEN

Godot Shader Techniques. UV Manipulation: Moving the Address. Explain centered tiling, translation, and time-based UV scrolling.

## BIDEA

Namaste. This is Liam, in for Bear. The key correction is that larger UV scale repeats more tiles. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. UV: The address used to sample a texture. Tiling: Repeated sampling across a surface. Translation: An offset added to the sampling address.

## B01

This shader changes the coordinates passed to its texture reads. It does not move the mesh. The same surface fragments now ask for different locations in the stored images.

## B02

Subtract one half before scaling and add it back afterward. That makes the center of the UV square the pivot for the scale, instead of the corner.

## B03

A scale of two makes the UV coordinates cover twice the interval along each axis. With repeating enabled, more copies fit across the surface. The apparent texture features become smaller.

## B04

The translation components add a fixed offset. Time multiplied by speed adds a changing offset. These are sampling movements; the visible pattern can travel opposite the direction you move the address.

## B05

In the capture, scale increases while a small horizontal scrolling speed remains active. The tiles become smaller and slide. The sphere and torus keep their geometry and positions.

## B06

The transformed coordinates feed the normal map as well as the color and specular maps. Using the original UV for just one would make the lighting detail slip out of alignment with the paint.

## B07

Set scale to one, translation to zero, and speed to zero. The expression returns the original UV coordinates. That identity case gives a direct check against the normal-mapped material without the transform.

## B08

The texture addresses move, but the tangent frame stays attached to the mesh. This positive-scale, scrolling demonstration works within that limitation. Mirroring or rotating normal-map coordinates needs extra attention to direction conventions.

## BVDT

Let’s recap with Claude. Subtract one half to center the transform. Scale and translate the sampling address. Time adds a scrolling offset. All three maps use the same transformed UV. Liam, in for Bear.

## BHTF

Set UV scale to one, then two, with translation and scrolling disabled. Predict the number of repeats. Then enable scrolling and explain why the object itself does not move. Check two things: Scale two produces more repetitions. Diffuse, mask, and normal reads share the transformed UV.

## BOUT

UV Manipulation: Moving the Address. At Nik Bear Brown.
