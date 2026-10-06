# PREDICTION.md — speed 160 → 192

Change: `tuning.gd` speed 160.0 → 192.0. All other constants unchanged.

Physics constants used in reasoning:
- speed: 192 (was 160)
- acceleration: 1280 → 1280/60 ≈ 21.33 px/frame
- deceleration: 1920 → 1920/60 = 32 px/frame
- Physics tick: 60 Hz (delta = 1/60 s)

---

## test_game.gd

### launch-grounded — PASS
Checks is_on_floor() and PLAYING state after 3 frames from spawn. No speed dependency.

### speed-cap — FAIL
`is_equal_approx(game.player.velocity.x, 160)` after axis=1 for 8 frames.

With acceleration 21.33/frame and target 192:
- After 8 frames: 8 × 21.33 = 170.67 px/s (never hits 192 cap yet)
- At old speed (160): 8 frames would overshoot 160, clamping to 160 → PASS
- At new speed (192): target is 192, 170.67 < 192, so velocity stays at ~170.67
- is_equal_approx(170.67, 160) is false → FAIL

Expected observed velocity_x ≈ 170.67

### neutral-stop — FAIL
`is_zero_approx(game.player.velocity.x)` after axis=0 for 5 frames, starting from ~170.67.

Deceleration 32/frame via move_toward(v, 0, 32):
- Frame 1: 138.67
- Frame 2: 106.67
- Frame 3: 74.67
- Frame 4: 42.67
- Frame 5: 10.67

10.67 ≠ 0 → FAIL. (At 160 it was exactly 160 − 5×32 = 0.)

Expected observed velocity_x ≈ 10.67

### simultaneous-directions — PASS
`is_zero_approx(game.player.velocity.x)` after both directions for 5 frames, starting from ~10.67.

test_control=false, Input both directions → axis=0, target=0.
move_toward(10.67, 0, 32) → 0 in 1 frame (step > remaining distance), stays 0 for all 5. PASS.

### left-wall — PASS
Checks position.x ∈ [9, 11] after 70 frames moving left.
player.gd line 67: `position.x = maxf(position.x, 10.0)` enforces x≥10.
Higher speed just hits the wall faster. PASS.

### fixed-jump-and-no-double — PASS
Checks jump count == 1 and rise height ≈ 53.33 px.
Rise uses jump_velocity (−320) and gravity (960) only — not speed. PASS.

### held-jump-no-bounce — PASS
Checks jumps==1 and on floor after arc. Jump/gravity physics unchanged. PASS.

### coyote-5 — PASS
Manipulates last_floor_tick; checks whether jump fires within coyote window.
No speed dependency. PASS.

### coyote-6 — PASS
Same reasoning as coyote-5. PASS.

### coyote-7 — PASS
Same reasoning. PASS.

### buffer-5 — PASS
Manipulates jump_request_tick; checks buffer window. No speed dependency. PASS.

### buffer-6 — PASS
Same reasoning. PASS.

### buffer-7 — PASS
Same reasoning. PASS.

### low-ceiling — PASS
Ceiling geometry cuts jump short; only jump_velocity and gravity matter. PASS.

### pause-freezes — PASS
Checks position unchanged while paused. No speed dependency. PASS.

### focus-loss-pauses — PASS
Checks PAUSED state on focus loss. No speed dependency. PASS.

### actual-spike-collision — PASS
Player placed at (330, 310); spike collision detection independent of speed. PASS.

### duplicate-death-ignored — PASS
resolve_contacts(true,true) on already-DYING player. No speed dependency. PASS.

### respawn — PASS
After 38 frames from DYING, checks PLAYING and spawn position. No speed dependency. PASS.

### manual-restart-not-death — PASS
restart_attempt() doesn't increment deaths. No speed dependency. PASS.

### twenty-retries — PASS
20 death/respawn cycles, checks deaths==21 and max ticks ≤ 60. No speed dependency. PASS.

### death-before-finish — PASS
resolve_contacts triggers DYING before COMPLETE. No speed dependency. PASS.

### fall-boundary — PASS
Player at (415, 432) triggers fall death. No speed dependency. PASS.

### complete-real-route — FAIL (predicted)
`game.state == Game.State.COMPLETE and game.deaths == 0` using route_driver.gd.

route_driver triggers jumps at x marks [138, 292, 424, 548, 712] and always drives right.
Jump arc duration ≈ 40 frames (jump_velocity −320, gravity 960).
- At 160 px/s: horizontal travel per jump = 160 × 40/60 ≈ 106.7 px
- At 192 px/s: horizontal travel per jump = 192 × 40/60 ≈ 128 px (≈21 px overshoot per jump)

Jump marks were calibrated for 160 px/s. At 192 the player lands ~21 px further per jump,
likely overshooting platforms and causing a death or the 900-tick timeout. FAIL predicted.

### replay-idempotent — PASS
Calls start_session() twice after route test (whether it completes or times out).
start_session() resets to PLAYING, deaths=0, jumps=0 regardless. PASS.

---

## test_keyboard.gd

### enter-start — PASS
KEY_ENTER starts game. No speed dependency. PASS.

### keyboard-move — PASS
Checks position.x > 85 after ~12 frames with D held + 2 frames release.
At 192 px/s the player travels ~30 px (64 + 30 ≈ 94 > 85). PASS.
(Was already PASS at 160; even more margin at 192.)

### keyboard-jump — PASS
Checks jumps==1 and velocity.y < 0. Jump mechanics independent of speed. PASS.

### escape-pause — PASS
ESC → PAUSED state. No speed dependency. PASS.

### enter-resume — PASS
ENTER → PLAYING state. No speed dependency. PASS.

### r-retry — PASS
R resets player to spawn (64, 320). No speed dependency. PASS.

### enter-replay — PASS
resolve_contacts(false,true) → COMPLETE, then ENTER replays. No speed dependency. PASS.

### pause-main-menu — PASS
P then M → MENU state. No speed dependency. PASS.

### menu-start-again — PASS
ENTER from MENU → PLAYING. No speed dependency. PASS.

---

## Summary

| Suite | Predicted FAILs |
|---|---|
| test_game.gd | speed-cap, neutral-stop, complete-real-route |
| test_keyboard.gd | (none) |
