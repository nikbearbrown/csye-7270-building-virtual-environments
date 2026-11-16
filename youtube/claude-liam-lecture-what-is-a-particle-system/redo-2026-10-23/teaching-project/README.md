# Particle fundamentals: original Godot teaching lab

Open project.godot in Godot 4.7.2. The Compatibility renderer is used. `lesson.tscn` is an original, live `@tool` particle visualization; its exported properties are editable in the Inspector. `render_game.tscn` centers the same visualization for standalone playback.

The chapter's conceptual progression is credited to Daniel Shiffman, [The Nature of Code: Particle Systems](https://natureofcode.com/particles/). This GDScript is an original time-based adaptation, not the p5.js source and not a production particle-engine replacement.

The scene exposes birth rate, lifetime, gravity, wind, speed, spread, fade, shrink, cleanup and moving-emitter controls. The deliberately disabled cleanup case keeps expired records; a 600-record cap bounds that fault. The LIVE counter includes retained dead records in that experiment.

`builtin_fountain.tscn` is the actual GPUParticles2D comparison. Its node amount is a population setting; do not interpret it as the teaching model's births per second.

All filmed operations were scripted in the actual Godot editor through the supported project-local EditorPlugin. No simulated editor was used. Original source versions, actions and checkpoints are retained in `.lecture/` and in the film's `captures/` directory. New readable source formatting does not change the motion equations. Ordinary human input and human playtesting are not claimed.

Run lifecycle checks: `godot --headless --path . --script test_lifecycle.gd`.

The separate `capture_4k.gd` uses a native 3840×2160 SubViewport with the logical scene scaled threefold. Its fixed-frame recording is rendering evidence, not a real-time benchmark.

The delivered copy disables the capture plugin by default. To replay recorded operations, enable Lecture Capture in Project Settings → Plugins and write one request at a time to `.lecture/request.json`, waiting for its ID in `.lecture/actions.jsonl`. The original action timing is retained in the film capture manifests. A raw request file is intentionally omitted so opening the project cannot replay the last production command.

One-shot comparison: change the continuous fountain’s preprocess from 2 seconds to 0 before setting one_shot true and explosiveness 1. Otherwise the pre-roll advances its short burst before you see the onset. The repaired native take records zero pre-roll and three complete trials. `blank_tool.tscn` is the explicit empty starter shown receiving the original script.
