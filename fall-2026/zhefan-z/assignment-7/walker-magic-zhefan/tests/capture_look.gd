extends SceneTree
## Assignment 7 capture harness (not a test): fixture runs of the real game for windowed Movie Maker frames
## (captures/look/). Uses only what exists both now and at the baseline 2276069 (main.tscn, test_mode, the player and
## wolf positions, real input through Input.parse_input_event), so the same file can run in a baseline worktree.
## Scenarios (first user argument):
##   take_lunge   player 780, wolf 860, no input: the pin scenario (growl, lunge into the player, hurt, recover).
##   cast_ground  player 200, wolf 860: a click aimed at (300, 340) before tick 10, into the ground (trail, impact).
## The mouse is parked at screen (600, 24) before tick 0 (the crosshair draws there), except where a scenario aims.
## Writes <out_dir>/ticks.jsonl, one line per physics tick: tick, player state and sprite visibility, wolf state,
## fireballs alive, impacts alive. The scene is added one frame after start: Movie Maker frame n shows tick n - 1.
## From assignment-7/, windowed:
##   Godot_v4.7.2-stable_win64_console.exe --path walker-magic-zhefan --resolution 1280x720 --fixed-fps 60
##     --write-movie <abs>/captures/look/<run>/f.png --script res://tests/capture_look.gd -- <scenario> <abs out_dir>

const GROUND_TOP := 327.0
const IMPACT_SCENE := "res://effects/fireball_impact.tscn"
const LENGTH := {"take_lunge": 70, "cast_ground": 70}


class TickLog extends Node:
	var ticks := 0
	var lines: PackedStringArray = []
	var main: Node

	func _init() -> void:
		process_physics_priority = 1000

	func _physics_process(_delta: float) -> void:
		var player: Player = main.player
		var wolf: Node = main.get_node_or_null("Level/Wolf")
		var fireballs := main.get_children().filter(func(n: Node) -> bool: return n is Fireball).size()
		var impacts := main.get_children().filter(func(n: Node) -> bool: return n.scene_file_path == IMPACT_SCENE).size()
		lines.append(JSON.stringify({"tick": ticks, "p_state": Player.State.keys()[player.state],
			"p_visible": player.sprite.visible, "p_x": snappedf(player.global_position.x, 0.01),
			"w_state": Wolf.State.keys()[wolf.state] if wolf else "FREED", "fireballs": fireballs, "impacts": impacts}))
		ticks += 1


var scenario := "take_lunge"
var out_dir := ""
var log_node: TickLog
var main: Node


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	scenario = args[0] if args.size() > 0 else "take_lunge"
	out_dir = args[1] if args.size() > 1 else ProjectSettings.globalize_path("res://").path_join("../captures/look/" + scenario)
	DirAccess.make_dir_recursive_absolute(out_dir)
	call_deferred("run")


## Event positions are window pixels; a windowed run stretches the 640x360 viewport 2x, so viewport points go through
## the root's final transform (identity headless).
func to_window(viewport_point: Vector2) -> Vector2:
	return root.get_final_transform() * viewport_point


func motion(screen: Vector2) -> void:
	var ev := InputEventMouseMotion.new()
	ev.position = to_window(screen)
	ev.global_position = ev.position
	Input.parse_input_event(ev)


func click(screen: Vector2, pressed: bool) -> void:
	var ev := InputEventMouseButton.new()
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = pressed
	ev.position = to_window(screen)
	ev.global_position = ev.position
	Input.parse_input_event(ev)


func run() -> void:
	main = load("res://game/main.tscn").instantiate()
	main.test_mode = true
	root.add_child(main)
	var player_x := 780.0 if scenario == "take_lunge" else 200.0
	main.player.global_position = Vector2(player_x, GROUND_TOP)
	main.get_node("Level/Wolf").global_position = Vector2(860, GROUND_TOP)
	log_node = TickLog.new()
	log_node.main = main
	root.add_child(log_node)
	motion(Vector2(600, 24))
	var aim_screen := Vector2.ZERO
	while log_node.ticks < LENGTH[scenario]:
		if scenario == "cast_ground":
			if log_node.ticks == 10 and aim_screen == Vector2.ZERO:
				aim_screen = Vector2(300, 340) - Vector2(main.camera.get_screen_center_position().x - 320.0, 0.0)
				motion(aim_screen)
				click(aim_screen, true)
			elif log_node.ticks == 14:
				click(aim_screen, false)
		await process_frame
	var f := FileAccess.open(out_dir.path_join("ticks.jsonl"), FileAccess.WRITE)
	f.store_string("\n".join(log_node.lines) + "\n")
	f.close()
	quit(0)
