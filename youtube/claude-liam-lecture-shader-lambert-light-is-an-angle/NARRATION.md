# Lambert: Light Is an Angle

## BOPEN

Godot Shader Techniques. Lambert: Light Is an Angle. Predict diffuse brightness from the dot product of normalized directions.

## BIDEA

Bonjour. This is Liam, in for Bear. The key correction is that brightness measures alignment. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Normal: The surface's outward direction. Dot product: A measure of alignment between directions. Clamp: Restrict a value to a specified interval.

## B01

Start with a unit surface normal and a unit direction toward the light. Their dot product is the cosine of the angle between them. That is the entire diffuse brightness model here.

## B02

When both directions line up, the dot product is one. Multiply the surface color by one and its diffuse contribution reaches full strength. This is a lighting weight, not a screen-byte measurement.

## B03

At sixty degrees, the dot product is one half. The diffuse contribution is halved before display conversion. Do not assume the displayed pixel will be half as bright numerically.

## B04

At ninety degrees, the dot product reaches zero. Beyond ninety degrees it becomes negative. Clamp removes that negative contribution; the back of the object cannot receive negative light.

## B05

Watch the direction rotate around the object. The bright region follows the surfaces facing the incoming light. We never changed a light's distance, because this shader has no light position.

## B06

The stored direction points along the traveling light. Negating it points back toward the source. If the vector points upward before negation, the shader lights downward-facing surfaces.

## B07

The normal is transformed into world space before interpolation. The light direction is also world space. A plausible-looking dot product can still be wrong when its vectors use different spaces.

## B08

This manually computed Lambert material does not ask Godot for scene-light shadows or distance falloff. It teaches one mechanism: surface orientation controls the diffuse term. Those other effects need additional machinery.

## BVDT

Let’s recap with Claude. Normalize both directions. Their dot product measures alignment. Clamp away negative light. This directional-light model has no distance attenuation. Liam, in for Bear.

## BHTF

For unit directions separated by zero, sixty, and ninety degrees, predict the Lambert weights. Then rotate the light in Godot and explain why the back-facing side stays black. Check two things: The predicted weights are one, one half, and zero. Negative dot products are clamped to zero.

## BOUT

Lambert: Light Is an Angle. At Nik Bear Brown.
