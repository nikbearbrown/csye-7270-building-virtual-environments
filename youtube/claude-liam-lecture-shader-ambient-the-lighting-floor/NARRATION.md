# Ambient: The Lighting Floor

## BOPEN

Godot Shader Techniques. Ambient: The Lighting Floor. Distinguish a constant ambient approximation from simulated bounced light.

## BIDEA

Ciao. This is Liam, in for Bear. The key correction is that ambient supplies a constant floor. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Diffuse: The orientation-dependent lighting contribution. Ambient: A simple background lighting approximation. Linear light: Values proportional to light intensity.

## B01

Lambert alone returns zero on the back-facing side. Real scenes often contain indirect illumination. This shader uses a constant ambient color as a cheap stand-in for that missing light.

## B02

Look at the parentheses. Ambient is added to the Lambert term first. The sum is multiplied by the surface color, so the background contribution inherits the same surface tint.

## B03

Start with ambient set to black. That adds nothing. The material returns to plain Lambert behavior, which gives us a clean baseline for seeing what the extra term does.

## B04

Now raise ambient gradually. The dark side becomes visible even where the light-facing dot product is zero. This reveals color; it does not calculate the shape of bounced illumination.

## B05

The ambient input is marked as a color. In Forward Plus, an sRGB gray of zero point fifteen converts to roughly zero point zero one nine six in linear light.

## B06

That conversion means the Forward Plus sum is not automatically one plus zero point fifteen. Add the values the shader actually receives. Display colors and linear-light contributions are different quantities.

## B07

There is no neighborhood query in this shader. An exposed surface and a hidden crevice receive the same ambient input. A constant floor cannot produce contact shadows or color bleeding.

## B08

Use this material to separate the direct-light term from an ambient approximation. If you need convincing indirect illumination, this constant alone is insufficient. The useful lesson is where each contribution enters.

## BVDT

Let’s recap with Claude. Ambient is added to the diffuse weight. The surface color multiplies both contributions. A constant floor cannot compute occlusion. Color conversion changes the arithmetic values. Liam, in for Bear.

## BHTF

Set ambient color to black, then raise it gradually. Predict which side of the object changes most visibly. Explain why this constant term cannot reproduce contact shadows. Check two things: The previously dark side becomes visible. No geometry-dependent occlusion is computed.

## BOUT

Ambient: The Lighting Floor. At Nik Bear Brown.
