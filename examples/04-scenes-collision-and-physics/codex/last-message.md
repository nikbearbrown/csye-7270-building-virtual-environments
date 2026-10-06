Implemented one shield-pickup mechanic without changing existing speeds, spawn paths, timer intervals, HUD, assets, mobs, or `test_input.gd`.

Key changes:

- Added code-drawn `pickup.tscn`/`pickup.gd` on named physics layer `Pickups`.
- Added `PickupTimer` spawning pickups at random on-screen positions.
- Player detects pickups, receives a visible ring shield for 3 seconds, and survives mob contact while shielded.
- Shield expiry checks existing overlaps and immediately triggers a hit when necessary.
- Restart clears pickups and shield state; game over stops pickup spawning.
- Added `godot/tests/test_shield.gd` using real D-key input and physics-frame waits.
- No commit created.

Test results:

```text
$ godot --headless --path godot --script res://test_input.gd
PASS initial player hidden
PASS start resets player score and music state
PASS downward orientation
PASS horizontal movement resets orientation
PASS diagonal motion normalized near 400px/s
PASS left boundary clamps
PASS timer spawns mobs
PASS timed score updates label
PASS physics collision hides/disables player
PASS collision stops gameplay timers
PASS game over stops music state
PASS restart offered after messages
PASS restart restores player and score
PASS restart clears mobs
RESULT failures=0; headless state and collision fixture, not footage
EXIT_CODE=0
```

```text
$ godot --headless --path godot --script res://tests/test_shield.gd
PASS real D-key movement collects pickup and enables shield
PASS shielded mob contact does not hide or disable player
PASS shielded mob contact keeps gameplay timers running
PASS overlapping mob hits within 10 physics frames of shield expiry
PASS restart clears pickups
PASS restart clears shield
RESULT failures=0; headless shield state and collision fixtures, not footage
EXIT_CODE=0
```

Godot also emitted environment warnings about its unwritable `user://logs` location and macOS system CA certificates; neither affected the exit codes.

These headless tests cannot verify:

- The shield/pickup’s rendered appearance or animation quality.
- Audio audibility.
- Long-play spawn balance or pickup placement feel.
- Real keyboard latency, GPU rendering, or windowed-platform behavior.