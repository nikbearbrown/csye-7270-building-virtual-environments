## Checks (run from the repository root)

Import once after cloning: `godot --headless --path godot --import`

Regression route — the route counts frames but the game moves by seconds, so it
is only deterministic with `--fixed-fps 60`. Without it the result depends on
machine speed. Expected: exit 0, "passed": true.

`WALKER_EVIDENCE_DIR="$PWD/evidence-local" godot --headless --path godot --fixed-fps 60 --script "$PWD/tests/input_route.gd"`

Run any new test the same way, with `--fixed-fps 60`.
