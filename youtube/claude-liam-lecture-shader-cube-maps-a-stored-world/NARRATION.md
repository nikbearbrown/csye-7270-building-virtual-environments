# Cube Maps: A Stored World

## BOPEN

Godot Shader Techniques. Cube Maps: A Stored World. Explain direction-based environment lookup and rim weighting.

## BIDEA

Salaam. This is Liam, in for Bear. The key correction is that the reflection samples a stored world. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Cubemap: Six images addressed by a direction. Reflection vector: The direction used to look into the environment. Rim weight: A view-dependent multiplier near the silhouette.

## B01

A cubemap stores surroundings on six faces. The shader addresses it with a three-dimensional direction, not the mesh's two-dimensional UV coordinates. The runtime assembles the six generated test images.

## B02

Normalize the eye vector and normal, then mirror the eye direction with the correct sign. This produces the direction into the stored environment that should appear at this surface point.

## B03

The texture call reads the cubemap along that reflection direction. It does not trace through the current scene. The returned color is whatever the stored environment contains there.

## B04

The environment sample is multiplied by the rim term before being added. That term depends on both the viewing angle and the diffuse-plus-ambient lighting factor in this implementation.

## B05

Watch the camera move while the environment stays fixed. The eye vectors change, so the lookup directions change. The reflected pattern can move without replacing any cubemap image.

## B06

At a point facing directly toward the camera, the rim's geometric weight is zero. Its cubemap contribution disappears there. That missing reflection is a consequence of the formula, not a failed texture.

## B07

The Phong highlight remains a separate addition. A bright center does not prove the cubemap is contributing at that point. Separate the highlight and environment terms when debugging.

## B08

Adding a moving object beside this sphere will not put that object into the stored cubemap. For dynamic local reflections, you need additional rendering machinery. This shader teaches the lookup and its weighting.

## BVDT

Let’s recap with Claude. A direction selects a cubemap sample. The reflection vector depends on the viewer. The rim weights the reflection in this shader. The cubemap is not a live scene reflection. Liam, in for Bear.

## BHTF

Move the camera while keeping the cubemap fixed. Then add an unrelated object to the scene. Explain which change affects the lookup and why the new object does not appear automatically. Check two things: The reflection direction changes with the camera. A static cubemap does not capture new scene objects.

## BOUT

Cube Maps: A Stored World. At Nik Bear Brown.
