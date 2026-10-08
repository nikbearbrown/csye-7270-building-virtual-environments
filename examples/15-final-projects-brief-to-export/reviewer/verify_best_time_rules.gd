extends SceneTree
## Independent check written by the human reviewer, not by the agent.
## Run: godot --headless --path godot --script <this file> --fixed-fps 60
## Every run uses a brand-new directory, so a file left by an earlier run
## cannot make a check pass.
const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")

var failures := 0
var game: Node2D
var run_dir: String

func _initialize() -> void:
	call_deferred("run")

func check(ok: bool, label: String) -> void:
	if not ok:
		failures += 1
	print("PASS " if ok else "FAIL ", label)

func steps(n: int) -> void:
	for i in n:
		await physics_frame
		await process_frame

func session(path: String) -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.best_time_path = path
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	await steps(3)

func finish_route() -> bool:
	var route := Route.new()
	var ticks := 0
	while game.state == Game.State.PLAYING and ticks < 900:
		route.step(game.player)
		await steps(1)
		ticks += 1
	return game.state == Game.State.COMPLETE

func write(path: String, text: String) -> void:
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(text)
	f.close()

func run() -> void:
	run_dir = ProjectSettings.globalize_path("res://../evidence/reviewer-%d" % Time.get_ticks_usec() + "-" + str(Time.get_unix_time_from_system()).replace(".", ""))
	DirAccess.make_dir_recursive_absolute(run_dir)
	print("RUN_DIR ", run_dir)

	# A. First completion in an empty directory writes the finish time.
	var a := run_dir + "/best_time.json"
	await session(a)
	check(not FileAccess.file_exists(a), "A: directory starts empty")
	check(await finish_route(), "A: route completes")
	var saved = JSON.parse_string(FileAccess.get_file_as_string(a)) if FileAccess.file_exists(a) else null
	check(saved is Dictionary and is_equal_approx(float(saved.get("best_seconds", -1)), game.last_finish_time),
		"A: saved best equals last_finish_time (%s vs %s)" % [str(saved.get("best_seconds") if saved is Dictionary else null), str(game.last_finish_time)])
	check(not FileAccess.file_exists(a + ".tmp"), "A: no temporary file left behind")

	# B. A file from a newer build that ALSO renamed another field is still a
	#    newer build's file. Rule: version > 1 is never overwritten.
	var b := run_dir + "/v2_other_level.json"
	var v2 := '{"format":"walker-jumpman-clawd.best","version":2,"level":"first-steps-remix","best_seconds":4.0}'
	write(b, v2)
	await session(b)
	check(await finish_route(), "B: route completes with a version-2 file present")
	check(FileAccess.get_file_as_string(b) == v2, "B: version-2 file with a renamed level survives byte for byte")

	# C. Same, with a renamed format string.
	var c := run_dir + "/v2_other_format.json"
	var v2f := '{"format":"walker-jumpman-clawd.best.v2","version":2,"level":"first-steps","best_seconds":4.0}'
	write(c, v2f)
	await session(c)
	check(await finish_route(), "C: route completes with a version-2 file present")
	check(FileAccess.get_file_as_string(c) == v2f, "C: version-2 file with a renamed format survives byte for byte")

	# D. A save that cannot be written leaves the game complete and the best unset.
	var d := run_dir + "/missing-parent/best_time.json"
	await session(d)
	check(await finish_route(), "D: route completes when the save directory is missing")
	check(game.state == Game.State.COMPLETE and game.best_seconds == 0.0, "D: failed write leaves state COMPLETE and best unset")

	# E. Normal play (test_mode false, no path set) persists to user://.
	#    Run this file with HOME pointed at a scratch folder: it writes there.
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	var real := "user://best_time.json"
	var existed_before := FileAccess.file_exists(real)
	game = Game.new()
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	await steps(3)
	print("USER_DATA_DIR ", OS.get_user_data_dir(), " existed_before=", existed_before)
	check(game.best_time_path == real, "E: normal play resolves the save path to user://best_time.json (got '%s')" % game.best_time_path)
	check(await finish_route(), "E: route completes in normal mode")
	check(FileAccess.file_exists(real), "E: normal play wrote user://best_time.json")

	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	print("RESULT failures=", failures, "; reviewer's own headless check")
	quit.call_deferred(1 if failures else 0)
