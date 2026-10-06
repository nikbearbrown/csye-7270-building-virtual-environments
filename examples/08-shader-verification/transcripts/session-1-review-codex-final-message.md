Verdict: **do not merge**. The commit breaks both the visible rendering and frame-rate-independent fade required by the specification.

## Specification review

1. **Not preserved.** `flash_amount` remains a ranged float uniform at [clawd_flash.gdshader:3](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/clawd_flash.gdshader:3), but the fade now counts 33 process frames at [player.gd:6](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:6) and [player.gd:96](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:96). It ignores `_process(delta)` and decrements once per frame at [player.gd:102](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:102). At 30 FPS the retry occurs while the flash is still `0.5152`; at 144 FPS it reaches zero roughly 0.23 seconds into the 0.55-second failure.

2. **Preserved at the next process/render frame.** Every non-failure state resets the counter at [player.gd:98](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:98), and the zero is assigned to the uniform at [player.gd:101](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:101). Both measured runs confirmed that R produces zero on the following frame.

3. **Preserved.** `flash_color` is still a color uniform with the normalized `#25354a` default at [clawd_flash.gdshader:4](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/clawd_flash.gdshader:4).

4. **Not preserved.** The new shader reads `texture(TEXTURE, UV)` at [clawd_flash.gdshader:7](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/clawd_flash.gdshader:7). Clawd is made from untextured `draw_rect()` calls whose body and eye colors arrive through `COLOR`, so this discards the original `#dd775b` body and black eyes. The previous `vec4 col = COLOR` was necessary for exact appearance at zero.

5. **Preserved structurally.** The material is assigned only to the player CanvasItem at [player.gd:36](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:36). HEAD does not alter the level, HUD, background, or gallery.

6. **Not fully preserved.** Collision and movement code remain unchanged, and the presentation code only reads failure state at [player.gd:95](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/player.gd:95). The mechanics, keyboard, and Clawd suites pass. However, the existing `test_flash.gd` expectations now fail, violating the explicit requirement that existing tests remain unchanged and pass.

7. **Not preserved as a working effect.** Godot 4.7.2’s shader parser accepts the shader, but [clawd_flash.gdshader:7](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/features/player/clawd_flash.gdshader:7) uses the wrong input for this project’s vector-drawn CanvasItem. Dummy rendering cannot validate the visible GL Compatibility result.

8. **Not preserved.** HEAD adds no test change, and the existing evidence detects the regression. The real-time comparison at [verify_flash.gd:98](<scratch>/ch08/codex-review/walker-jumpman-clawd/godot/tests/verify_flash.gd:98) fails at both 30 and 144 FPS. The direct flash suite also fails its midpoint and retry-threshold assertions.

## Problems, most severe first

1. **The shader discards Clawd’s vector-drawing colors.**

   At `flash_amount == 0`, it samples `TEXTURE` instead of preserving the incoming `COLOR`. This can turn the body and eyes into the default texture sample rather than their original colors.

   Human proof:

   1. Open `godot/project.godot` in Godot 4.7.2.
   2. Confirm the renderer is GL Compatibility.
   3. Run `res://game/main.tscn`.
   4. Before causing a failure, compare Clawd with the gallery/reference appearance: body must be `#dd775b`, eyes black, surroundings transparent.
   5. Trigger a spike or fall and observe the flash.
   6. Confirm that immediately after retry the exact original body and eye colors return.

   Specifically inspect both `flash_amount = 0` and `1`; headless mode cannot read pixels.

2. **The fade is tied to frame count rather than wall-clock time.**

   `FLASH_FRAMES := 33` lasts approximately 1.1 seconds at 30 FPS, 0.55 seconds at 60 FPS, and 0.229 seconds at 144 FPS. Since retry remains 0.55 seconds, the 30 FPS effect is cut off halfway, while the 144 FPS effect finishes early.

   Headless proof:

   ```bash
   godot --headless --path godot \
     --script res://tests/verify_flash.gd --fixed-fps 30
   ```

   Result: failure; last pre-retry flash `0.5151515`, maximum gap from the countdown `0.5151515`.

   ```bash
   godot --headless --path godot \
     --script res://tests/verify_flash.gd --fixed-fps 144
   ```

   Result: failure; maximum gap from the countdown `0.6060606`.

3. **The required flash evidence suite is red.**

   The existing direct test reports `0.969697` where the midpoint should be `0.5`, and `0.939394` where the retry threshold should be zero.

   Headless proof:

   ```bash
   godot --headless --path godot \
     --script res://tests/test_flash.gd --fixed-fps 30
   ```

   The same two failures occur with `--fixed-fps 144`. Exit status is 1.

## Regression results

- `test_game.gd`, 60 FPS: **25 checks, 0 failures**
- `test_keyboard.gd`, 60 FPS: **9 checks passed**
- `test_clawd.gd`, 60 FPS: **1,950 checks, 0 failures**
- `test_flash.gd`, 30 and 144 FPS: **failed**
- `verify_flash.gd`, 30 and 144 FPS: **failed**
- No `SHADER ERROR` appeared. The recurring macOS CA-certificate warning is unrelated to shader parsing or the game tests.

No repository files were edited.