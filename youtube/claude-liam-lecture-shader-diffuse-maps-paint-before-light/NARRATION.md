# Diffuse Maps: Paint Before Light

## BOPEN

Godot Shader Techniques. Diffuse Maps: Paint Before Light. Trace a color texture through UV sampling and diffuse multiplication.

## BIDEA

Hei. This is Liam, in for Bear. The key correction is that the texture colors the diffuse term. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. UV: Two-dimensional coordinates used to address a texture. Sampler: A shader input used to read texture data. Texel: An individual texture sample location.

## B01

The shader reads a two-dimensional texture at the mesh's UV coordinates. Those coordinates address the picture. They are not world positions, and they do not add geometry to the sphere.

## B02

The sampler declares a color texture with the source-color hint. This identifies the stored color encoding so Forward Plus can use appropriate values for lighting arithmetic.

## B03

The texture's red, green, and blue channels multiply shader color. White tint preserves the texture. A colored tint changes the base without changing which texels the UV coordinates select.

## B04

The tinted texture is multiplied by Lambert plus ambient. A checker cell still becomes dark when its surface faces away from the light. The texture does not replace the lighting calculation.

## B05

Watch the tint move from white toward terracotta. The checker colors change together because they share the same material uniform. Their positions on the mesh remain fixed.

## B06

The rim and specular highlight are added afterward. They are not multiplied by the diffuse texture in this implementation. That separation is visible where a bright highlight crosses painted cells.

## B07

The repeat hint explicitly requests tiling outside the usual UV interval. State that intent instead of relying on an assumed sampler default. UV transforms later make this choice particularly visible.

## B08

A diffuse map changes color, not normals or silhouette. To distinguish these effects, keep the mesh and light fixed while changing only the color map. The shader's data path tells you what can change.

## BVDT

Let’s recap with Claude. UV coordinates select the texture sample. Color textures use the source-color hint. The sampled color multiplies the diffuse base. Rim and highlight are added separately. Liam, in for Bear.

## BHTF

Change shader color while keeping the checker texture and lighting fixed. Predict which contribution is tinted. Explain why the additive highlight does not follow the same multiplication. Check two things: The base texture is multiplied by shader color. The highlight is added after the diffuse multiplication.

## BOUT

Diffuse Maps: Paint Before Light. At Nik Bear Brown.
