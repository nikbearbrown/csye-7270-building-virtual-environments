extends SceneTree
## Assignment 7 capture harness (not a test): the wolf's lunge in the real game for a windowed Movie Maker strip
## (CHANGE-BRIEF "Watching and evidence"). A debug-only overlay drawn by this harness, never by the game, shows over the
## wolf's head its phase, the tick within the phase, the tick since the growl began and the clip frame.
## Scenarios (first user argument):
##   take_lunge   the pin scenario: player 780, wolf 860; the wolf lunges leftward into the player.
##   lunge_right  player 940, wolf 860: the wolf turns and lunges rightward into the player.
## No input. Writes <out_dir>/ticks.jsonl, one line per physics tick: tick, wolf state, phase tick, ticks since the growl
## began, clip and clip frame, Facing.scale.x, and the rig: Rig position and scale, FrontPivot and RearPivot rotation
## (degrees). The scene is added one frame after start: Movie Maker frame n shows tick n - 1. From assignment-7/:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan --resolution 1280x720 --fixed-fps 60
##     --debug-collisions --write-movie <abs>/captures/lunge/<run>/f.png --script res://tests/capture_lunge.gd
##     -- <scenario> <abs out_dir>

const GROUND_TOP := 327.0
const LENGTH := 140


class TickLog extends Node:
	var ticks := 0
	var lines: PackedStringArray = []
	var wolf: Wolf
	var label: Label
	var growl_start := -1
	var phase := ""
	var phase_start := 0

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		var s: String = Wolf.State.keys()[wolf.state]
		if s != phase:
			phase = s
			phase_start = ticks
		if s == "GROWL" and growl_start < 0:
			growl_start = ticks
		var rig: Node2D = wolf.get_node("Facing/Rig")
		var row := {"tick": ticks, "w_state": s, "phase_tick": ticks - phase_start,
			"since_growl": ticks - growl_start if growl_start >= 0 else -1, "clip": str(wolf.anim.assigned_animation),
			"clip_frame": roundi(wolf.anim.current_animation_position * 60.0), "facing": wolf.get_node("Facing").scale.x,
			"rig_x": snappedf(rig.position.x, 0.001), "rig_scale": [snappedf(rig.scale.x, 0.001), snappedf(rig.scale.y, 0.001)],
			"front_deg": snappedf(rad_to_deg(wolf.get_node("Facing/Rig/FrontPivot").rotation), 0.01),
			"rear_deg": snappedf(rad_to_deg(wolf.get_node("Facing/Rig/RearPivot").rotation), 0.01),
			"rig_visible": wolf.get_node("Facing").visible}
		lines.append(JSON.stringify(row))
		label.text = "%s %d\ng+%d f%d" % [s, row.phase_tick, row.since_growl, row.clip_frame]
		label.position = wolf.global_position + Vector2(-24, -66)
		ticks += 1


var log_node: TickLog
var out_dir := ""
var scenario := "take_lunge"


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	scenario = args[0] if args.size() > 0 else "take_lunge"
	out_dir = args[1] if args.size() > 1 else ProjectSettings.globalize_path("res://").path_join("../captures/lunge/" + scenario)
	DirAccess.make_dir_recursive_absolute(out_dir)
	call_deferred("run")


func run() -> void:
	var main: Node = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	main.player.global_position = Vector2(780.0 if scenario == "take_lunge" else 940.0, GROUND_TOP)
	var wolf: Wolf = main.get_node("Level/Wolf")
	wolf.global_position = Vector2(860, GROUND_TOP)
	var label := Label.new()   # debug overlay, this harness only
	label.add_theme_font_size_override("font_size", 8)
	label.add_theme_color_override("font_color", Color(1, 1, 0.4))
	label.z_index = 100
	main.add_child(label)
	Input.warp_mouse(root.get_final_transform() * Vector2(600, 24))
	log_node = TickLog.new()
	log_node.wolf = wolf
	log_node.label = label
	root.add_child(log_node)
	while log_node.ticks < LENGTH:
		await process_frame
	var f := FileAccess.open(out_dir.path_join("ticks.jsonl"), FileAccess.WRITE)
	f.store_string("\n".join(log_node.lines) + "\n")
	f.close()
	quit(0)
