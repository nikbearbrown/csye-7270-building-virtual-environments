# PBR Textures Are Data, Not Pictures

## BOPEN

C S Y E seventy-two seventy, Building Virtual Environments. PBR Textures Are Data, Not Pictures Which PBR maps hold colour and which hold numbers, what a normal map stores, and why reading data as colour breaks the lighting.

## BIDEA

Aloha. This is Liam, in for Bear. Texture maps look like pictures, so it is natural to treat them all as pictures. Only one of them is. The rest are tables of numbers.

## BDEFS

Three terms. Texel: one pixel of a texture. Channel: the red, green, blue or alpha part of a texel. S R G B: a colour encoding whose steps are spaced for human eyes.

## B01

A P B R material usually arrives as a set of texture maps, one per measurement. Watch this sphere gain them one at a time: base colour, normal, roughness, metallic and ambient occlusion.

## B02

Lay the maps side by side. Only the base colour map is a colour meant for your eyes. The other four are data. They look like grey or blue pictures only because an image file is a handy way to store a grid of numbers.

## B03

Zoom into the roughness map and read the texels. The tiles hold values near point three. The grout holds point nine. White means rough, and black means smooth. Those numbers are the whole point of the map.

## B04

Plug that grid into the roughness slot and the shine follows it. As the light sweeps across, the smooth tiles flash and the rough grout stays matte. One image, many roughness values.

## B05

A normal is the direction a surface faces: an arrow standing straight out of it. Lighting depends on the angle between that arrow and the light. Tilt the arrow away from the light, and the surface gets darker.

## B06

A normal map stores one arrow per texel. Red is X, green is Y, and blue is Z. A flat texel is one twenty-eight, one twenty-eight, two fifty-five: an arrow pointing straight out. That is why normal maps look pale blue.

## B07

In Godot, the normal map tilts the light texel by texel. Tiles appear and catch the moving light, yet the outline of the sphere stays perfectly round, because the geometry never moved.

## B08

Because these maps are just numbers, files often pack three into one. A Poly Haven A R M file keeps ambient occlusion in red, roughness in green and metallic in blue. Godot's O R M Material 3D reads that same order.

## B09

Here colour and data part ways. Colour values are stored in S R G B and decoded before lighting. Decode a flat normal that way, and one twenty-eight over two fifty-five, about point five, becomes about point two two. The arrow tilts thirty-nine degrees.

## B10

Here is that mistake in Godot. Both spheres use the same flat normal map, lit straight on. The left reads it as data and is lit evenly. The right reads it as colour, and its lighting slides off to one side.

## BVDT

Let’s recap with Claude. Only the base colour map is a colour. Roughness, metallic, AO and normal maps hold numbers. A normal map stores one arrow per texel. Read data as colour and the lighting breaks. Liam, in for Bear.

## BHTF

In Godot, open a Standard Material 3D and load a texture into each slot. For every map, predict whether it holds colour or data. Then open a normal map texture and read one texel near a flat area. Check two things: Only the base colour map should be treated as colour. A flat normal texel reads close to 128, 128, 255.

## BOUT

PBR Textures Are Data, Not Pictures At Nik Bear Brown.
