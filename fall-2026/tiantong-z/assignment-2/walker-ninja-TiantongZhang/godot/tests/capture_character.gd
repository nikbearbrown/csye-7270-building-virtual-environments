extends SceneTree
## Character-state captures for the visual-identity check in CHANGE-BRIEF P3.
## Saves the REAL rendered viewport in each readable state and records the
## player/camera world positions so the frames can be cropped and inspected
## without guessing where the body was. It does not modify the game: no
## teleport-to-finish, no disabled collisions, no test-only gameplay shortcut
## beyond the starter's existing `test_control` input injection.
##
## Every capture asserts the state it claims to show. Level 01 geometry leaves
## flat, hazard-free ground at x 0..160, 208..320 and 344..448 (the step block
## occupies 160..208 and the spikes 320..344), so the spots below are chosen to
## be genuinely flat rather than convenient.
const Game = preload("res://game/session.gd")
var game: Node2D
var output: String
var shots: Array = []

func _initialize() -> void:
	call_deferred("run")

func step() -> void:
	await physics_frame
	await process_frame

func capture(label: String, want_floor: bool, want_phase: int = 0) -> void:
	assert(game.player.is_on_floor() == want_floor,
		"%s: expected on_floor=%s, got %s" % [label, want_floor, game.player.is_on_floor()])
	assert(game.player.attack_phase() == want_phase,
		"%s: expected attack phase %d, got %d" % [label, want_phase, game.player.attack_phase()])
	await RenderingServer.frame_post_draw
	var image := root.get_texture().get_image()
	var error := image.save_png(output + "/" + label + ".png")
	assert(error == OK)
	var entry := {
		"label": label,
		"image_size": [image.get_width(), image.get_height()],
		"player": [game.player.position.x, game.player.position.y],
		"camera": [game.camera.position.x, game.camera.position.y],
		"facing": game.player.facing,
		"on_floor": game.player.is_on_floor(),
		"velocity": [game.player.velocity.x, game.player.velocity.y],
		"attack_phase": game.player.attack_phase(),
	}
	# When the swing hitbox is live, record its two endpoints in the player's
	# local space so the contact sheet can draw the thing that actually kills
	# on top of the blade that was actually rendered.
	if game.player.attack_hitbox.monitoring:
		var half: float = game.player.attack_shape.shape.size.x * 0.5
		var along := Vector2.from_angle(game.player.attack_shape.rotation)
		var a: Vector2 = game.player.attack_shape.position - along * half
		var b: Vector2 = game.player.attack_shape.position + along * half
		entry["hitbox"] = [a.x, a.y, b.x, b.y]
		entry["hitbox_thickness"] = game.player.attack_shape.shape.size.y
	shots.append(entry)
	print("captured %-24s facing=%+.0f on_floor=%s vx=%.1f" % [
		label, game.player.facing, game.player.is_on_floor(), game.player.velocity.x])

func hold(axis: float, frames: int) -> void:
	game.player.test_axis = axis
	for i in range(frames):
		await step()

## This script runs ONE continuous session, so a previous swing can still be
## in flight when the next capture is set up. Waiting for phase 0 first is what
## makes each swing capture deterministic.
func wait_idle() -> void:
	for i in range(30):
		if game.player.attack_phase() == 0:
			return
		await step()
	assert(false, "a previous swing never finished")

func ground_at(x: float) -> void:
	game.player.position = Vector2(x, 320)
	game.player.velocity = Vector2.ZERO
	game.player.test_axis = 0.0
	for i in range(30):
		await step()
		if game.player.is_on_floor():
			break
	assert(game.player.is_on_floor(), "could not settle on the floor at x=%.0f" % x)

func run() -> void:
	output = ProjectSettings.globalize_path("res://../evidence/screens")
	DirAccess.make_dir_recursive_absolute(output)
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	for i in range(3):
		await step()
	game.start_session()
	game.player.test_control = true

	# Idle, both facings, on the flat stretch between the step and the spikes.
	await ground_at(250.0)
	await hold(1.0, 12)
	await hold(0.0, 8)
	await capture("char-01-idle-right", true)

	await hold(-1.0, 12)
	await hold(0.0, 8)
	await capture("char-02-idle-left", true)

	# Grounded run on the long flat stretch past the spikes, so the stride tell
	# and the trailing scarf are both active and nothing is in the way.
	await ground_at(360.0)
	await hold(1.0, 24)
	assert(absf(game.player.velocity.x) > 8.0, "run capture is not actually moving")
	await capture("char-03-run-right", true)

	# Airborne before apex, so the pose is unambiguously a jump.
	await ground_at(250.0)
	await hold(1.0, 10)
	game.player.test_jump_pressed = true
	for i in range(12):
		await step()
	await capture("char-04-jump-right", false)

	# Airborne facing left, to prove the mirror is correct off the ground too.
	await ground_at(400.0)
	await hold(-1.0, 10)
	game.player.test_jump_pressed = true
	for i in range(12):
		await step()
	await capture("char-05-jump-left", false)

	# D3 swing: one frame per phase, so CHANGE-BRIEF P6 (two swords at once)
	# and P7 (the arc reaching above the collider) can be judged from pixels.
	# The hitbox endpoints are recorded on the active frame only.
	# Two active frames: early in the sweep (blade still rising) and late
	# (blade swung through to the forward reach), because the forward reach is
	# the part CHANGE-BRIEF P5 is actually about.
	# Frame offsets follow the 4 + 9 + 3 contract of revision 0.6.0. The recovery
	# frame was at 12 under the old 4 + 5 + 5 split; 12 is now still inside the
	# live window, so the phase assertion refused to publish that frame.
	for shot in [["char-06-slash-windup", 2, 1], ["char-07-slash-active-early", 6, 2], ["char-08-slash-active-late", 12, 2], ["char-09-slash-recovery", 14, 3]]:
		await wait_idle()
		await ground_at(250.0)
		await hold(1.0, 6)
		await hold(0.0, 2)
		await wait_idle()
		game.player.test_attack_pressed = true
		for i in range(int(shot[1])):
			await step()
		await capture(String(shot[0]), true, int(shot[2]))
	# Facing left, on an active frame, to show the mirrored hitbox.
	await wait_idle()
	await ground_at(300.0)
	await hold(-1.0, 6)
	await hold(0.0, 2)
	await wait_idle()
	game.player.test_attack_pressed = true
	for i in range(6):
		await step()
	await capture("char-10-slash-active-left", true, 2)
	# Airborne swing, also on an active frame.
	await wait_idle()
	await ground_at(250.0)
	await hold(1.0, 6)
	game.player.test_jump_pressed = true
	for i in range(8):
		await step()
	game.player.test_attack_pressed = true
	for i in range(6):
		await step()
	await capture("char-11-slash-airborne", false, 2)

	var f := FileAccess.open(output + "/char-shots.json", FileAccess.WRITE)
	f.store_string(JSON.stringify({"engine": Engine.get_version_info().string, "shots": shots}, "  "))
	f.close()
	print("CHARACTER CAPTURES: %d frames, all state assertions passed" % shots.size())
	game.queue_free()
	await process_frame
	quit()
