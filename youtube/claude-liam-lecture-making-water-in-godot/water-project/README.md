# Making Water in Godot: the project behind the film

**What this is.** An openable Godot 4.7.2 project with the finished water of the film "Making Water in Godot": `scenes/water.tscn` (a cove with the water, a sand floor and beach, two rocks, a buoy and a crate), every stage of the shader in `shaders/`, and the two small scripts that make the buoy and the crate ride the waves.
**Why.** So a viewer can open the thing the film shows, restyle it from the Inspector and follow one stage at a time.
**Found.** It runs as a project (verified in a real window on Godot 4.7.2, Forward+: 16,641 vertices, the buoy on a wave). It is a teaching scene, not a game. The shader files are copies of the film's tested files, byte for byte.

## Open it

Open this folder in Godot 4.7.2 or newer (Forward+ is the default) and run `scenes/water.tscn`. Select **Water**, open its **Material Override**, and the Inspector shows folders **Color**, **Clarity**, **Foam**, **Ripples**, **Waves** and **Shore**: those are the shader's `group_uniforms`. Change a number and the water changes.

## The stages

`shaders/01-blue.gdshader` to `06-shore-foam.gdshader` are the film's six layers; each one is a complete shader. To follow one stage, put it in the ShaderMaterial's Shader slot (the later stages need the two noise textures, the earlier ones ignore them). `03a-cells-debug` and `03b-power-curve` are the film's two experiments with the cell noise; `03d-foam-from-texture` is the baked-texture version; `06a-gap-view` shows the depth gap as a map.

- The waves of stages 05 and later are moved by the script `scripts/water_driver.gd`: it writes one clock into the shader's `wave_clock` and puts the buoy and the crate on the surface with `scripts/wave_math.gd`, the same function the shader runs. Without the script the waves stand still.
- `scripts/cove_builder.gd` builds the cove in code; `tools/make_scene.gd` wrote `scenes/water.tscn` from it (run it once more with `godot --headless --path . --script tools/make_scene.gd` if you change the builder). `tools/smoke.gd` runs the scene for three seconds and prints what it finds.
- Compatibility works too (set the renderer in Project Settings); the picture differs a little, and the film says how.

## Provenance and licence

The shaders, scripts and scene are written for the film (see the film's `SOURCES.md` for the algorithms they follow: Worley's cellular noise, a sum of sines, Godot's documented depth recipe). They use no assets from outside the project. Nothing here is taken from the `compute/texture` demo or from the Unity video the film's order of ideas was suggested by. Licence for the viewer's reuse: to be set by Bear (none is chosen yet).
