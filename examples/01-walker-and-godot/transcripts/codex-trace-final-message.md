No files were edited.

## Space-to-screen trace

1. **Space is bound to the `jump` action**  
   [godot/game/session.gd:24](<scratch>/ch01/walker-jumpman/godot/game/session.gd:24) calls `_setup_input()` during startup.  
   [godot/game/session.gd:48](<scratch>/ch01/walker-jumpman/godot/game/session.gd:48) maps `"jump"` to `KEY_SPACE`; lines 49–56 create the action and add the physical-key event if it does not already exist.

2. **The action is read each physics tick**  
   [godot/features/player/player.gd:46](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:46) reads whether `jump` is held.  
   [godot/features/player/player.gd:47](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:47) reads the fresh press with `Input.is_action_just_pressed("jump")`.  
   Lines 49–55 require a release and record the press tick for jump buffering.

3. **Eligibility is checked and jump velocity is applied**  
   [godot/features/player/player.gd:51](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:51) refreshes grounded eligibility.  
   [godot/features/player/player.gd:61](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:61) checks that the floor/coyote opportunity is unconsumed and that both coyote and buffered-input ages are valid.  
   [godot/features/player/player.gd:62](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:62) assigns `velocity.y = tuning.jump_velocity`. The configured value is `-320 px/s` at [godot/features/player/tuning.gd:6](<scratch>/ch01/walker-jumpman/godot/features/player/tuning.gd:6).

4. **Gravity and movement are integrated**  
   [godot/features/player/player.gd:60](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:60) adds `gravity * delta` to vertical velocity and applies the terminal-velocity cap. Gravity is `960 px/s²` at [godot/features/player/tuning.gd:7](<scratch>/ch01/walker-jumpman/godot/features/player/tuning.gd:7).  
   [godot/features/player/player.gd:66](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:66) calls `move_and_slide()`, which moves the `CharacterBody2D` and resolves floor, wall, and ceiling collisions.  
   The project runs physics at 60 Hz: [godot/project.godot:18](<scratch>/ch01/walker-jumpman/godot/project.godot:18).

5. **The moved character is redrawn on screen**  
   [godot/features/player/player.gd:68](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:68) requests a redraw after movement.  
   [godot/features/player/player.gd:70](<scratch>/ch01/walker-jumpman/godot/features/player/player.gd:70) begins `_draw()`; lines 74–80 draw the character from rectangles in its local coordinates. Godot renders that drawing using the body’s new transformed position, producing the visible upward motion.

## Checks exercising this path

Direct physical-key path:

- `keyboard-jump` — synthesizes `KEY_SPACE`, passes it through Godot Input, and checks that one jump occurred with upward velocity: [godot/tests/test_keyboard.gd:43](<scratch>/ch01/walker-jumpman/godot/tests/test_keyboard.gd:43).

Controller and movement path, using test inputs rather than the physical Space binding:

- `fixed-jump-and-no-double`
- `held-jump-no-bounce`
- `coyote-5`, `coyote-6`, `coyote-7`
- `buffer-5`, `buffer-6`, `buffer-7`
- `low-ceiling`
- `pause-freezes`
- `complete-real-route`

These are defined in [godot/tests/test_game.gd](<scratch>/ch01/walker-jumpman/godot/tests/test_game.gd). None of the checks directly asserts the pixels produced by the player’s `_draw()` method.

## What the tests establish

- Space reaches the `jump` action and creates one upward launch.
- The jump rises approximately 53.3 px, does not double-jump or auto-bounce, and respects ceiling collision.
- Six-tick coyote and buffer windows are accepted; age seven is rejected.
- Jump motion freezes while paused, and scripted jumps can complete the real course.

## What only a person playing can judge

- Whether the jump feels responsive, satisfying, and predictable.
- Whether its height, timing, forgiveness, animation, and landings are visually readable and enjoyable.