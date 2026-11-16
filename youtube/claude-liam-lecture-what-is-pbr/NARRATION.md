# What Is PBR?

## BOPEN

C S Y E seventy-two seventy, Building Virtual Environments. What Is PBR? What physically based rendering means, and the five measurements a Godot material is made of.

## BIDEA

Kia ora. This is Liam, in for Bear. Most people picture a material as an image wrapped around a model. In physically based rendering, a material is a set of measurements, and the light does the painting.

## BDEFS

Three terms. Mesh: the shape, a surface made of triangles. Material: what tells Godot how that surface meets light. Texture: an image a material can read.

## B01

P B R stands for physically based rendering. Instead of painting how a surface looks, you measure what it is. Godot's Standard Material 3D holds five measurements: base colour, metallic, roughness, normal and ambient occlusion.

## B02

Base colour, which Godot calls albedo, is the colour the surface reflects. Watch it change from grey to terracotta to teal. The highlight and the shadow stay where they are, because they come from the light, not from the colour.

## B03

Metallic says whether the surface behaves like a metal. At zero, the highlight is white and sits on top of the colour. At one, the colour moves into the reflection itself, and the sphere starts to mirror the sky and the floor.

## B04

Roughness says how blurred the reflections are. Godot's documentation puts it plainly: zero is a perfect mirror, and one blurs the reflection completely. As roughness rises, the highlight spreads out and grows dimmer.

## B05

Put two of them together and you get the classic chart. Roughness rises from left to right, and metallic from top to bottom. Every sphere has the same base colour. Only two numbers change, and each sphere looks like a different material.

## B06

The normal is the direction the surface faces, at a detail smaller than the mesh. A normal map changes it pixel by pixel. Tiles appear and catch the moving light, but the outline stays perfectly round. The light changes. The geometry does not.

## B07

Ambient occlusion is how much of the surrounding light reaches a crevice. By default, Godot applies it to ambient light, not to direct light. Lit by the sky alone, the grooves darken when it switches on. Add the sun, and the sunlight ignores the map.

## B08

None of these five is a colour on the screen yet. For every pixel, in every frame, the renderer combines them with a light and a camera. Only then is there a colour to show.

## B09

So a material is always judged under some light. Here are three materials, plastic, gold and rubber, under a noon sun, a sunset and a dim blue room. The lighting changes. The materials never do.

## B10

One more consequence. Only the base colour is a colour. Metallic, roughness, normal and occlusion are numbers that happen to be stored in image files, so they must be read as numbers.

## BVDT

Let’s recap with Claude. A PBR material is measurements, not a picture. Base colour, metallic, roughness, normal, occlusion. A light and a camera turn them into colour. So judge a material under stated lighting. Liam, in for Bear.

## BHTF

In Godot, add a sphere with a Standard Material 3D and a directional light. Predict what the highlight does as roughness goes from zero to one, then set metallic to one and repeat. Rotate the light. Check two things: The highlight spreads and dims as roughness rises. The base colour never changed while the light moved.

## BOUT

What Is PBR? At Nik Bear Brown.
