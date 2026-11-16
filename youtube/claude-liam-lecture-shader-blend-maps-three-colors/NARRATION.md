# Blend Maps: Three Colors

## BOPEN

Godot Shader Techniques. Blend Maps: Three Colors. Read channel-weighted color mixing without assuming RGB naming order.

## BIDEA

Aloha. This is Liam, in for Bear. The key correction is that the code defines the channel mapping. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Weight: A multiplier applied to a contribution. Channel: A separately readable texture component. Blend map: A texture whose components choose mixture weights.

## B01

The blend texture stores weights. Its channels do not have to be the final visible colors. The material supplies three separate colors that those weights will combine.

## B02

Read the expression carefully. Red weights shader color. Blue weights blended color. Green weights third color. The second and third names do not follow the usual red, green, blue reading order.

## B03

A pure red texel has a red weight of one and the other weights zero. Only the first color survives. Pure blue selects the second; pure green selects the third.

## B04

Intermediate channel values create mixtures. This expression simply adds weighted colors. It does not divide by the sum of weights, so arbitrary maps can make the mixture brighter or darker.

## B05

Watch the first material color change from red toward yellow. Only regions controlled by the blend map's red channel respond directly. The blue and green selections retain their own colors.

## B06

The combined base color is multiplied by diffuse plus ambient lighting. Rim and highlight are added separately. Color selection and surface illumination remain distinguishable parts of the calculation.

## B07

The blend sampler is not marked source color because its channels are weights. Treating those intermediate numbers as display colors would change the mixture. The three actual paint uniforms are marked as colors.

## B08

When a region changes the wrong paint, inspect the channel mapping before repainting the texture. The shader is authoritative: texture names and familiar RGB ordering cannot tell you the mapping by themselves.

## BVDT

Let’s recap with Claude. Texture channels supply mixture weights. The order here is red, blue, then green. Weights are not normalized by this shader. Lighting is applied after choosing the base color. Liam, in for Bear.

## BHTF

Set the first color to yellow, the second to cyan, and the third to magenta. Predict the output in pure red, blue, and green regions of the blend map. Then inspect the shader's channel order. Check two things: Red selects the first color; blue selects the second. Green selects the third color.

## BOUT

Blend Maps: Three Colors. At Nik Bear Brown.
