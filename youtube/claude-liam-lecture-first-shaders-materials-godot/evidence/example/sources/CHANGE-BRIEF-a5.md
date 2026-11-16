# Shader and material instructor-example extension

October 14, 2026, before new shader files. Preserve the original signal-garden/ shaders and all historical tests. A new course-series lab derives from the existing room, with the same gameplay state and charge timing.

State effect: a new instructional shader uses the same ALBEDO = mix(base, active_color.rgb, activation) relation, activation from charge/0.6, texture-free inputs and declared defaults/hints. It shows quiet, partial and full activation. The driver continues to own state; the shader only observes it. Inputs, physics, collision and original tests must stay unchanged.

Textured shader: color sampler with source_color, data/roughness sampler without it, four typed/hinted defaults in two groups, and two saved ShaderMaterials that use the same shader and differ in tint, scale and roughness gain. A separate three-band hint fixture compares the same PNG read as color and data under stated renderer/environment. No normal map is used in this shader; the normal-map check is not applicable to its materials, and the separate generated-StandardMaterial example is labeled diagnostic.

Predictions: missing source_color should be caught by the wiring test even when a set/get succeeds; unknown uniforms should not count as declared; material edits should affect only one saved resource while shader edits affect both; a headless pass cannot certify color. Controlled values use the original specification/oracle and actual native captures.

These instructional shader listings and notes are AI-authored examples. The student brief requires student-authored shader code and explanations; the film must explain that distinction and must never label these files as Bear’s handwritten work.

## Diagnostic ruler revision, before its capture

The hint fixture gains an optional screen-grid toggle. UV still selects the same three texture bands. FRAGCOORD.x and VIEWPORT_SIZE.x place a two-pixel red rule every eighth of the viewport, demonstrating pixel coordinates versus texture coordinates. The toggle defaults off during numeric measurements. This changes only the isolated teaching fixture, not either game shader or the game.
