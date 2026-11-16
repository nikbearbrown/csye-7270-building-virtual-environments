# Specular Maps: Where It Shines

## BOPEN

Godot Shader Techniques. Specular Maps: Where It Shines. Explain independently packed masks for rim and highlight strength.

## BIDEA

Ahoj. This is Liam, in for Bear. The key correction is that channels can carry independent masks. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Mask: A number controlling a contribution's strength. Channel: One component of a texture sample. Specular: The view-dependent highlight contribution.

## B01

A texture sample can hold controls rather than paint. Here the red channel is a rim mask and the green channel is a highlight mask. Blue does not contribute to either term.

## B02

Multiply the rim contribution by red. A zero removes it at that texel. A one preserves it. Intermediate values scale the contribution, allowing a patterned rim on one material.

## B03

Green independently scales the Phong highlight. A matte cell can suppress a highlight even when the reflection directions line up. Its neighboring cell can retain the same lighting lobe.

## B04

The mask sampler has no source-color hint. These values are controls, not display colors. Color conversion would change intermediate mask strengths and therefore change the material's response.

## B05

Compare an all-white mask with the packed texture. First both effects are allowed everywhere. Then patterned regions suppress them independently. The geometry and light stay the same.

## B06

There is another change in this file: the rim is no longer multiplied by Lambert plus ambient. The mask addition is not the only difference from the diffuse-map shader.

## B07

Because that lighting factor is absent, the rim can remain bright on the unlit side. Do not diagnose that glow as a broken specular map. It follows directly from the changed rim formula.

## B08

Channel meanings belong to this shader. Another material might use red for a different purpose. Read the channel contract before reusing the texture; a valid image can still drive the wrong effect.

## BVDT

Let’s recap with Claude. The specular texture carries data masks. Red controls this shader's rim strength. Green controls its highlight strength. This rim no longer has the diffuse lighting factor. Liam, in for Bear.

## BHTF

Paint the red and green channels of the specular map separately. Predict which channel changes the rim and which changes the highlight. Test a zero mask and a one mask. Check two things: Red masks the rim; green masks the highlight. Mask values are read without source-color conversion.

## BOUT

Specular Maps: Where It Shines. At Nik Bear Brown.
