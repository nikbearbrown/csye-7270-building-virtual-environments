# Phong: The Moving Highlight

## BOPEN

Godot Shader Techniques. Phong: The Moving Highlight. Explain why a specular highlight depends on view direction and exponent.

## BIDEA

Hej. This is Liam, in for Bear. The key correction is that the highlight is computed from directions. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Specular: A view-dependent reflection highlight. Reflection: Mirroring a direction around the surface normal. Exponent: The control for highlight concentration.

## B01

A painted white spot stays attached to the object. A reflection highlight depends on where the viewer stands. This shader introduces the eye vector alongside the surface normal and light direction.

## B02

The eye vector points away from the surface. The shader negates its reflected value to obtain the outward mirror direction. The sign matters because reflect expects an incident direction.

## B03

The mirrored direction is compared with the direction toward the light. Alignment produces a value near one. Misalignment reduces it. Clamp prevents negative values from entering the power.

## B04

Raise that alignment to a positive power. A larger exponent suppresses everything except close alignment. Watch the highlight tighten as the power increases from eight toward one hundred.

## B05

The highlight has its own color control. Its contribution is added after the diffuse term. That is why changing the base color does not simply repaint every highlight by the same factor.

## B06

The final line combines diffuse lighting, ambient, the rim, and this highlight. Reading those terms separately lets you identify which control changes a broad shading gradient and which changes the bright spot.

## B07

This is a manually specified directional light. The shader does not trace a ray to a lamp or ask whether another object blocks it. A highlight is not proof of a traced reflection.

## B08

Phong gives a compact model for a shiny lobe. The exponent is an artistic concentration control, not a physical roughness measurement. The key mechanism is the relationship among light, normal, and viewer.

## BVDT

Let’s recap with Claude. Reflect the view direction about the normal. Compare that reflected direction with the light. The exponent controls the highlight's width. This Phong model is an artistic lighting approximation. Liam, in for Bear.

## BHTF

Compare specular powers of eight and one hundred while keeping the light fixed. Then move the camera. Explain the highlight's width and why it is not attached like painted texture. Check two things: Higher power produces a tighter highlight. Camera movement changes the highlight position.

## BOUT

Phong: The Moving Highlight. At Nik Bear Brown.
