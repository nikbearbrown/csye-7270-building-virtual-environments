# Render States: Four Behaviors

## BOPEN

Godot Shader Techniques. Render States: Four Behaviors. Distinguish shading calculations from opaque, blended, cutout, and additive rendering.

## BIDEA

Halo. This is Liam, in for Bear. The key correction is that render state determines how alpha is used. We will trace the code, inspect its output, and test where the model stops working.

## BDEFS

Three terms. Blend: Combine a fragment with the background. Cutout: Discard fragments below an alpha threshold. Render mode: A shader's rendering-state declaration.

## B01

This file keeps the lighting calculation largely shared and selects a rendering behavior with a compile-time definition. The number chooses the render mode; it is not a runtime material slider.

## B02

In opaque mode, the shader does not write ALPHA. The rim can still affect color, but it does not make the object transparent. Alpha's existence in another branch does not change this selected branch.

## B03

The blending mode writes the rim value to alpha. Small alpha reveals more background; larger alpha contributes more object color. In this model, the front-facing center can become nearly transparent.

## B04

Alpha scissor uses a threshold of zero point three. Values below that threshold are discarded. This is a cutout decision, not a partially transparent mixture with the background.

## B05

Watch the same material cycle through opaque, blended, scissored, and additive variants. The geometry and lighting formula stay shared. The different silhouettes and background interactions come from rendering state.

## B06

Additive rendering contributes the fragment's color weighted by alpha to the destination. It can brighten the background. It does not behave like an opaque coat of paint.

## B07

The original lesson discarded values equal to the threshold too. This Godot alpha-scissor version keeps the equality boundary. That tiny difference is documented rather than claimed as a bit-exact port.

## B08

These are four alternatives, not four passes stacked together. Choose one compiled variant for a material. A multi-pass effect is a different design, and this file does not implement one.

## BVDT

Let’s recap with Claude. The shading formula and render state are separate. Opaque output ignores the unused rim alpha. Blending mixes; scissor discards. Additive contributes light to the background. Liam, in for Bear.

## BHTF

Compare opaque, alpha blend, alpha scissor, and additive modes using the same rim alpha. Explain whether each pixel replaces, mixes with, disappears from, or brightens the background. Check two things: Cutout discards instead of partially mixing. Additive brightens the destination rather than replacing it.

## BOUT

Render States: Four Behaviors. At Nik Bear Brown.
