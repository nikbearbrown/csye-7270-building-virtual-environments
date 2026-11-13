extends SceneTree
## Assignment 7 capture harness (not a test; prompt 8, step 5): the run cycle's seam and registration in the real game.
## game/main.tscn with the player at x 180 and the wolf at 860 (it never sees her); D pressed before tick 10 and
## released before tick 160 through Input.parse_input_event, so the mage runs for 150 ticks (six 24-tick cycles, short
## of the pit at 520); quits after 180 ticks. Writes one line per physics tick to <out_dir>/ticks.jsonl: tick, process
## frame, player state, x, y, the clip and its position, Sprite2D frame, hframes, offset, position and flip_h. A small
## label (this harness only, debug) shows the tick and the sprite frame, so each Movie Maker frame names its own tick.
## Fixture: the harness places the characters. From assignment-7/ (a 30 fps strip: two physics ticks per movie frame):
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan --resolution 1280x720 --fixed-fps 30
##     --debug-collisions --write-movie <abs scratch>/seam.png --script res://tests/capture_run_seam.gd
##     -- <abs>/captures/run/game-r2-seam
## To watch it at normal speed (no movie, nothing written), pass "watch" as the only user argument.

const GROUND_TOP := 327.0
const EVENTS := [[10, true], [160, false]]   # [tick, D pressed]
const LENGTH := 180


class TickLog extends Node:
	var ticks := 0
	var lines: PackedStringArray = []
	var player: Player
	var label: Label

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		var anim: AnimationPlayer = player.get_node("AnimationPlayer")
		var s: Sprite2D = player.sprite
		var row := {"tick": ticks, "process_frame": Engine.get_process_frames(), "state": Player.State.keys()[player.state],
			"x": snappedf(player.global_position.x, 0.001), "y": snappedf(player.global_position.y, 0.001),
			"clip": str(anim.current_animation), "clip_pos": snappedf(anim.current_animation_position, 0.0001),
			"frame": s.frame, "hframes": s.hframes, "offset": [s.offset.x, s.offset.y],
			"sprite_pos": [s.position.x, s.position.y], "flip_h": s.flip_h}
		lines.append(JSON.stringify(row))
		label.text = "tick %d  %s  frame %d" % [ticks, row.state, row.frame]
		ticks += 1


var logger: TickLog
var out_dir := ""


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	out_dir = args[0] if args.size() > 0 else ProjectSettings.globalize_path("res://").path_join("../captures/run/game-r2-seam")
	if out_dir != "watch":
		DirAccess.make_dir_recursive_absolute(out_dir)
	call_deferred("run")


func setup() -> void:
	var main: Node = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	main.player.global_position = Vector2(180, GROUND_TOP)
	main.get_node("Level/Wolf").global_position = Vector2(860, GROUND_TOP)
	var layer := CanvasLayer.new()
	layer.layer = 50
	var label := Label.new()
	label.position = Vector2(4, 40)
	label.add_theme_font_size_override("font_size", 10)
	layer.add_child(label)
	root.add_child(layer)
	logger = TickLog.new()
	logger.player = main.player
	logger.label = label
	root.add_child(logger)


func key(pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = KEY_D
	ev.physical_keycode = KEY_D
	ev.pressed = pressed
	Input.parse_input_event(ev)


func run() -> void:
	await process_frame
	setup()
	var pending := EVENTS.duplicate()
	while logger.ticks < LENGTH:
		while not pending.is_empty() and pending[0][0] <= logger.ticks:
			key(pending.pop_front()[1])
		await process_frame
	if out_dir != "watch":
		var f := FileAccess.open(out_dir.path_join("ticks.jsonl"), FileAccess.WRITE)
		f.store_string("\n".join(logger.lines) + "\n")
		f.close()
	quit(0)
