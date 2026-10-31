# Downfall — Assignment 5

Godot 4.7.2, **Forward+ / D3D12** on Windows.

This complete project adds a state-driven burning-bottle flame, lit cargo-panel materials, and color/normal experiments to the existing game. Open project.godot, import resources, and run game/main.tscn. WASD moves, mouse buttons attack, E interacts, and Esc pauses or closes a window. Two hall crate_stack props use separate cargo materials sharing one shader.

The three custom programs are in shaders/. standard_generated.gdshader is a comparison export and is not referenced by game materials. Read CHANGE-BRIEF.md for the rules and original predictions, LANGUAGE-NOTES.md for language questions, MATERIALS.md for the sampler audit, TEST-REPORT.md for results, and SOURCES.md / FRICTIONAL.md for provenance.

With Git Bash and GODOT set to the engine executable:

```bash
TEST_TIMEOUT=1200 ./scripts/run-test.sh test_fire_shader.gd 30
TEST_TIMEOUT=1200 ./scripts/run-test.sh test_fire_shader.gd 60
TEST_TIMEOUT=1200 ./scripts/run-test.sh test_fire_shader.gd 144
./scripts/run-test.sh test_materials.gd 60
./scripts/run-test.sh normal_map_check.gd 60
```

The wrapper is unchanged. The capture scripts require a real renderer and must run without --headless. Calibration uses 1280×720 because the predicted pixel coordinates depend on it.

The resolved baseline result is 70/73, including an isolated performance repeat; three pre-existing suites still fail. See the report before interpreting an exit code as an A5 regression. Evidence is under evidence/a5/. Film/audio and regenerable .godot caches stay outside GitHub. SUBMISSION.md identifies the final package and course location.

