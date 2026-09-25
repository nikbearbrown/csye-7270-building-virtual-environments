# Component coverage

This is an assignment-focused teardown of the unchanged starter, not an exhaustive reading of every line. The hashed inventory and exact excerpts are in `gamedev-evidence.json`.

| Code → result | Component | Visible evidence |
| --- | --- | --- |
| B07 → B08 | Procedural character drawing | Actual Godot art preview at two staged facing values |
| B09 → B10 | Collision rectangle and origin | Actual collider-node dimensions overlaid on the staged engine preview |
| B11 → B12 | Acceleration, braking and facing | Scripted normal-input movement recording |
| B13 → B14 | Level rectangles and finish trigger | Recorded landings, gaps and completion |
| B15 → B16 | Hazard art versus hazard collision | Recorded spike failure and retry |
| B17 → B18 | Camera clamp and level width | Recorded world scrolling; fixed interface |
| B19 → B20 | Progress-bar distance | Recorded progress approaching the original finish |
| B21 → B22 | Pause and input recovery | Recorded pause, resume, restart, focus-loss simulation and menu |

B02–B04 cover installation, the two repositories and importing the existing main scene. B23 explains the different scopes of mechanical tests, keyboard-event tests, route fixtures and staged screenshot helpers. B06 and B24–B28 connect these mechanisms to the assignment, prediction, human playtesting, revision and submission.

No sprite-sheet, TileMap, soundtrack, export-preset workflow or finished student extension is invented. Diagnostic art views are labeled staged; the gameplay is archived same-build engine output, not newly performed human playtesting. Asset appearance does not prove collision behavior, and one recorded route does not establish every route.
