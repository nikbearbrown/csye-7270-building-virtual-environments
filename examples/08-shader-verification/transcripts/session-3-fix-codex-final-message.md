Fixed both problems without editing `godot/tests/` or committing.

Design: the player still owns the shader effect, but reads the session’s authoritative game-time retry countdown. This avoids a duplicate timer drifting from the actual retry and makes R clear the flash immediately.

Changes:

- [player.gd](<scratch>/ch08/walker-jumpman-clawd/godot/features/player/player.gd:6): replaced the 33-frame counter with `retry_remaining / 0.55`.
- [clawd_flash.gdshader](<scratch>/ch08/walker-jumpman-clawd/godot/features/player/clawd_flash.gdshader:7): now starts from incoming `COLOR`.
- [FRICTIONAL.md](<scratch>/ch08/walker-jumpman-clawd/FRICTIONAL.md:124): recorded the actual work and wrapper failure.

Real headless results:

```text
test_game.gd          60 fps: WALKER TESTS: 25 checks / 0 failures
test_keyboard.gd      60 fps: 9 PASS, exit 0
test_clawd.gd         60 fps: checks=1950, failures=0

test_flash.gd         30 fps: checks=11, failures=0
test_flash.gd         60 fps: checks=11, failures=0
test_flash.gd        144 fps: checks=11, failures=0

verify_flash.gd       30 fps: frames=17, seconds=0.566667, max_gap=0, failures=0
verify_flash.gd       60 fps: frames=34, seconds=0.566667, max_gap=0, failures=0
verify_flash.gd      144 fps: frames=82, seconds=0.570556, max_gap=0, failures=0

verify_flash_spec.gd  30 fps: failures=0
verify_flash_spec.gd  60 fps: failures=0
verify_flash_spec.gd 144 fps: failures=0

flash_model.gd        60 fps: failures=0
test_flash_bench.gd   60 fps: failures=0
```

R-key checks passed at all three rates, with the first subsequent sampled frame showing `flash=0.0`. No `SHADER ERROR` appeared. Godot did print sandbox-related log-file and macOS CA-certificate diagnostics, but all requested test processes exited 0.

Remaining human checks:

- Confirm the CanvasItem shader visibly affects Clawd’s `draw_rect()` output under GL Compatibility.
- Check the tint and linear fade appearance.
- Confirm transparent surroundings remain transparent.
- Confirm the level, HUD, and background remain visually unchanged.
- Confirm R visibly clears the tint immediately.

No human visual approval or playtest is claimed. The worktree contains only the two production changes and the required effort-log update; no test files changed.