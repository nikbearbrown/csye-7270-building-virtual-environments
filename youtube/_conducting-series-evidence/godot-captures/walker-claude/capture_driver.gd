extends Node
## CAPTURE DRIVER (scratch copy only; never part of the source project).
## Autoload that drives the REAL game with REAL keyboard events
## (Input.parse_input_event), and saves rendered viewport frames as PNG.
## Mode and output folder come from user args after `--`:
##   --mode=game|gallery  --out=/abs/folder
## Every key press it makes is printed to the log as "INPUT f=<frame> ...".

var mode := "game"
var out := ""
var frame := 0
var holding_right := false
var jump_marks: Array[float] = [138.0, 292.0, 424.0, 548.0, 712.0] # same marks as tests/route_driver.gd
var next_jump := 0
var jump_release_frame := -1
var game: Node = null
var shots_taken := {}
var finished_frame := -1
var jump_shot_done := false

func _ready() -> void:
	process_priority = -100
	for a in OS.get_cmdline_user_args():
		if a.begins_with("--mode="): mode = a.substr(7)
		if a.begins_with("--out="): out = a.substr(6)
	DirAccess.make_dir_recursive_absolute(out)
	print("CAPTURE DRIVER mode=%s out=%s" % [mode, out])

func key(code: Key, down: bool, label: String) -> void:
	var e := InputEventKey.new()
	e.keycode = code
	e.physical_keycode = code
	e.pressed = down
	Input.parse_input_event(e)
	print("INPUT f=%d t=%.2fs %s %s" % [frame, frame / 30.0, label, "DOWN" if down else "UP"])

func shot(label: String) -> void:
	if shots_taken.has(label): return
	shots_taken[label] = true
	await RenderingServer.frame_post_draw
	var img := get_viewport().get_texture().get_image()
	var path := out + "/" + label + ".png"
	img.save_png(path)
	print("SHOT f=%d t=%.2fs %s %dx%d" % [frame, frame / 30.0, path, img.get_width(), img.get_height()])

func _process(_delta: float) -> void:
	frame += 1
	if mode == "game": _game_step()
	elif mode == "gallery": _gallery_step()

func _game_step() -> void:
	if game == null:
		game = get_tree().current_scene
		if game and "test_mode" in game:
			# Only effect: the game does not auto-pause when the window loses focus.
			game.test_mode = true
	if frame == 25: shot("01-title-screen")
	if frame == 36: key(KEY_ENTER, true, "Enter (start)")
	if frame == 38: key(KEY_ENTER, false, "Enter (start)")
	if frame == 42 and not holding_right:
		key(KEY_RIGHT, true, "Right arrow (move right, held)")
		holding_right = true
	if frame == jump_release_frame: key(KEY_SPACE, false, "Space (jump)")
	if holding_right and game:
		var p: CharacterBody2D = game.player
		if next_jump < jump_marks.size() and p.position.x >= jump_marks[next_jump] and p.is_on_floor():
			key(KEY_SPACE, true, "Space (jump) at x=%.0f" % p.position.x)
			jump_release_frame = frame + 1
			next_jump += 1
		if frame == 53: shot("02-clawd-running")
		if not jump_shot_done and next_jump >= 3 and p.position.x > 463 and p.position.y < 300:
			jump_shot_done = true
			shot("03-clawd-jumping-the-gap")
		if game.state == 4 and finished_frame < 0: # State.COMPLETE
			finished_frame = frame
			key(KEY_RIGHT, false, "Right arrow (move right)")
			holding_right = false
			print("LEVEL COMPLETE f=%d deaths=%d time=%.2f" % [frame, game.deaths, game.last_finish_time])
		if game.state == 3: print("DEATH f=%d" % frame)
	if finished_frame > 0 and frame == finished_frame + 20: shot("04-level-complete")
	if finished_frame > 0 and frame == finished_frame + 40: get_tree().quit()
	if frame > 600: get_tree().quit()

func _gallery_step() -> void:
	# Gallery autoplays pages every 9 s; arrows switch pages manually.
	if frame == 45: shot("05-gallery-page-1")
	if frame == 120: key(KEY_RIGHT, true, "Right arrow (next gallery page)")
	if frame == 121: key(KEY_RIGHT, false, "Right arrow (next gallery page)")
	if frame == 165: shot("06-gallery-page-2")
	if frame == 240: key(KEY_RIGHT, true, "Right arrow (next gallery page)")
	if frame == 241: key(KEY_RIGHT, false, "Right arrow (next gallery page)")
	if frame == 285: shot("07-gallery-page-3")
	if frame == 300: get_tree().quit()
