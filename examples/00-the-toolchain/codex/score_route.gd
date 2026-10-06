extends SceneTree
## Headless score route using normal input actions only.
## It observes contacts and scores; it never writes the ball or either score.

const ACTIONS := ["left_move_up", "left_move_down", "right_move_up", "right_move_down"]
const MAX_FRAMES := 60 * 45

var game: Node
var frame := 0
var phase := 0
var wall_contacts := {"LeftWall": 0, "RightWall": 0}


func _initialize() -> void:
	seed(7375)
	root.size = Vector2i(640, 400)
	root.content_scale_size = Vector2i(640, 400)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
	call_deferred("_start_game")


func _start_game() -> void:
	game = load("res://pong.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	for wall_name in wall_contacts:
		game.get_node(wall_name).area_entered.connect(func(area: Area2D) -> void:
			if area.name == "Ball":
				wall_contacts[wall_name] += 1
		)


func _process(_delta: float) -> bool:
	if game == null:
		return false
	for action in ACTIONS:
		Input.action_release(action)

	var ball := game.get_node("Ball") as Area2D
	var left := game.get_node("Left") as Area2D
	var right := game.get_node("Right") as Area2D
	if phase == 0:
		# Move Left away so the initial left-moving ball exits through LeftWall.
		Input.action_press("left_move_up")
		if wall_contacts.LeftWall > 0:
			phase = 1
	else:
		# Track with Left to return the reset ball; move Right away so it exits there.
		_press_toward("left", ball.position.y, left.position.y)
		Input.action_press("right_move_up" if ball.position.y > 200.0 else "right_move_down")

	frame += 1
	if wall_contacts.RightWall > 0 or frame >= MAX_FRAMES:
		_finish()
	return false


func _press_toward(player: String, target_y: float, paddle_y: float) -> void:
	if absf(target_y - paddle_y) > 2.0:
		Input.action_press(player + ("_move_down" if target_y > paddle_y else "_move_up"))


func _finish() -> void:
	for action in ACTIONS:
		Input.action_release(action)
	var score := game.get_node("Score")
	var checks := {
		"left_score_matches_right_wall": score.left_score == wall_contacts.RightWall,
		"right_score_matches_left_wall": score.right_score == wall_contacts.LeftWall,
		"left_score_visible": score.get_node("LeftScore").text == str(score.left_score),
		"right_score_visible": score.get_node("RightScore").text == str(score.right_score),
		"both_sides_scored": score.left_score > 0 and score.right_score > 0,
	}
	var passed := true
	for result in checks.values():
		passed = passed and result
	var report := {
		"engine": Engine.get_version_info().string,
		"method": "scripted normal input actions; no score or ball writes",
		"frames": frame,
		"wall_contacts": wall_contacts,
		"scores": {"left": score.left_score, "right": score.right_score},
		"checks": checks,
		"passed": passed,
	}
	print(JSON.stringify(report))
	quit(0 if passed else 1)
