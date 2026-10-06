extends SceneTree
## Score-check — tests/score_check.gd
## Drives the real game with normal input actions only.
## No direct writes to the score, ball, or paddles.
## Asserts: scoreboard.left_score  == wall_contacts["RightWall"]
##          scoreboard.right_score == wall_contacts["LeftWall"]
var game: Node
var frame := 0
var wall_contacts := {"LeftWall": 0, "RightWall": 0}
var route_fps := 60
var actions := ["left_move_up", "left_move_down", "right_move_up", "right_move_down"]

func _initialize() -> void:
	seed(7375)
	if not OS.get_environment("WALKER_ROUTE_FPS").is_empty():
		route_fps = int(OS.get_environment("WALKER_ROUTE_FPS"))
	if route_fps not in [30, 60]:
		quit(2)
		return
	root.size = Vector2i(640, 400)
	root.content_scale_size = Vector2i(640, 400)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
	call_deferred("start_game")

func start_game() -> void:
	game = load("res://pong.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	for wall in ["LeftWall", "RightWall"]:
		game.get_node(wall).area_entered.connect(func(area: Area2D):
			if area.name == "Ball":
				wall_contacts[wall] += 1
		)

func _process(_delta: float) -> bool:
	if game == null:
		return false
	for action in actions:
		Input.action_release(action)
	var left := game.get_node("Left") as Area2D
	var right := game.get_node("Right") as Area2D
	var ball := game.get_node("Ball") as Area2D
	var route_tick := frame * (60.0 / route_fps)
	# Replicate the input_route sequence so we know misses occur.
	if route_tick < 150:
		Input.action_press("left_move_up")
		Input.action_press("right_move_down")
	elif route_tick < 390:
		Input.action_press("left_move_down")
		Input.action_press("right_move_up")
	elif route_tick >= 2700 and route_tick < 3000:
		# Deliberate miss: both paddles move away from ball.
		Input.action_press("left_move_up")
		Input.action_press("right_move_up")
	else:
		for pair in [[left, "left"], [right, "right"]]:
			var error: float = ball.position.y - pair[0].position.y
			if absf(error) > 2.0:
				Input.action_press(pair[1] + ("_move_down" if error > 0 else "_move_up"))
	frame += 1
	if frame >= 3300:
		finish()
	return false

func finish() -> void:
	for action in actions:
		Input.action_release(action)
	var score_board := game.get_node("ScoreBoard")
	var left_score: int = score_board.left_score
	var right_score: int = score_board.right_score
	var checks := {
		"left_score_matches_right_wall_contacts": left_score == wall_contacts["RightWall"],
		"right_score_matches_left_wall_contacts": right_score == wall_contacts["LeftWall"],
		"at_least_one_wall_contact": wall_contacts["LeftWall"] + wall_contacts["RightWall"] > 0,
	}
	var passed := true
	for value in checks.values():
		passed = passed and value
	var report := {
		"method": "scripted-input; no gameplay state writes",
		"frames": frame,
		"wall_contacts": wall_contacts,
		"left_score": left_score,
		"right_score": right_score,
		"checks": checks,
		"passed": passed,
	}
	print(JSON.stringify(report))
	quit(0 if passed else 1)
