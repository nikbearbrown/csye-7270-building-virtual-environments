# Normal Maps Without New Geometry

## BOPEN

Godot Shader Techniques. Normal Maps Without New Geometry. Explain tangent-space normal decoding and its unchanged silhouette.

## BIDEA

Shalom. This is Liam, in for Bear. The key correction is that normal maps change lighting directions. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Tangent: A direction along the surface. Binormal: The second direction along the surface. Tangent space: Coordinates relative to the local surface frame.

## B01

The normal map stores direction components in RGB. Multiplying by two and subtracting one converts the stored zero-to-one range into signed components between minus one and one.

## B02

Tangent, binormal, and normal form the surface frame. The vertex stage carries these directions into world space so the sampled direction can be expressed where the light and eye vectors live.

## B03

The sampled red component weights the tangent, green weights the binormal, and blue weights the normal. Add the weighted directions and normalize the result. That becomes the lighting normal.

## B04

The perturbed normal drives diffuse, rim, and specular calculations. The shader does not merely paint shadows onto the texture. It changes the direction used by the lighting formulas.

## B05

Compare a flat map with the dome map. The surface appears bumpy because the directions vary across each cell. Look at the outside edge: the actual sphere has not grown those domes.

## B06

This version expects the supplied OpenGL-style map. A DirectX-style green channel has the opposite sign. Flipping that channel without adapting the shader reverses the vertical lighting detail.

## B07

This teaching port transforms tangents with the normal matrix too. That agrees for uniform scale, but it is not a general tangent-frame solution for nonuniform scaling. Keep this demonstration uniformly scaled.

## B08

All the apparent bumps happen in the fragment lighting. There is no vertex displacement here. If the outline must change, a normal map alone cannot provide that geometry.

## BVDT

Let’s recap with Claude. Decode the texture into signed components. Use the tangent frame to obtain a world normal. Lighting uses the perturbed direction. The mesh silhouette remains unchanged. Liam, in for Bear.

## BHTF

Compare a flat normal map with the dome map. Inspect the outline, then invert green. Explain why the lighting changes while the mesh silhouette remains the same. Check two things: The silhouette stays unchanged. The green convention matches the expected map.

## BOUT

Normal Maps Without New Geometry. At Nik Bear Brown.
