# Car Paint: Tuning Reflections

## BOPEN

Godot Shader Techniques. Car Paint: Tuning Reflections. Separate reflection controls from the two specular highlight lobes.

## BIDEA

Merhaba. This is Liam, in for Bear. The key correction is that several contributions shape the finish. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Reflection floor: An added baseline in the rim weight. Contrast power: An exponent applied to cubemap color. Lobe: A concentrated reflection contribution.

## B01

This shader extends a rim-weighted environment lookup. Intensity scales the angular part, while offset adds a baseline. The two controls are not interchangeable even when both make some regions brighter.

## B02

With zero offset, a point facing the camera has zero geometric rim weight. A positive offset lets an environment contribution survive there, still multiplied by the diffuse-plus-ambient lighting factor.

## B03

The contrast control raises each cubemap color component to a power. For components between zero and one, a power above one darkens intermediate values. This is an artistic operation, not a new reflection ray.

## B04

Two powers operate on the same reflection-light alignment. Their independently colored contributions add together. A smaller exponent gives a broader lobe; a larger exponent gives a tighter one.

## B05

Watch the offset increase from zero to one half on the red demo material. Reflection appears more strongly on front-facing regions. The stored environment and the mesh remain the same.

## B06

The reflection contribution and both highlights are added to the diffuse base. This makes the controls easy to inspect, but the sum is not an energy-conserving model of layered automotive paint.

## B07

Godot's vector power call uses a vector exponent here. The scalar contrast is explicitly expanded into three components. That is a language-porting detail, not an extra physical effect.

## B08

Tune each term against a visible goal: reflection at the center, environment contrast, a broad sheen, or a tight highlight. Calling everything shininess hides which calculation you actually changed.

## BVDT

Let’s recap with Claude. Intensity scales the angle-based reflection term. Offset adds a reflection baseline before lighting. A power reshapes the cubemap color. Two specular lobes contribute separate highlights. Liam, in for Bear.

## BHTF

Raise Fresnel offset while keeping intensity fixed, then compare the two specular powers. Explain which change adds front-facing reflection and which changes highlight width. Check two things: Offset allows a nonzero front-facing reflection weight. The two powers shape separate highlight contributions.

## BOUT

Car Paint: Tuning Reflections. At Nik Bear Brown.
