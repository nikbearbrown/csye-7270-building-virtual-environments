extends SceneTree

const Game = preload("res://game/session.gd")
const Route = preload("res://tests/route_driver.gd")

var results: Array[Dictionary] = []
var failures: int = 0
var game: Node2D

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for i in range(n):
		await physics_frame
		await process_frame

func check(id: String, passed: bool, observation: Dictionary) -> void:
	results.append({"id": id, "status": "PASS" if passed else "FAIL", "observed": observation})
	if not passed:
		failures += 1
	print(JSON.stringify(results.back()))

func make_dir(rel: String) -> String:
	var abs_path := ProjectSettings.globalize_path("res://../evidence/" + rel)
	DirAccess.make_dir_recursive_absolute(abs_path)
	return abs_path

func kill_game() -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame

func fresh_game(save_path: String) -> void:
	await kill_game()
	game = Game.new()
	game.best_time_path = save_path
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	await steps(3)

func drive_to_completion() -> bool:
	var route := Route.new()
	var ticks := 0
	while game.state == Game.State.PLAYING and ticks < 900:
		route.step(game.player)
		await steps(1)
		ticks += 1
	return game.state == Game.State.COMPLETE

func write_file(path: String, content: String) -> void:
	var f := FileAccess.open(path, FileAccess.WRITE)
	f.store_string(content)
	f.close()

func read_file(path: String) -> String:
	return FileAccess.get_file_as_string(path)

func run() -> void:
	var run_id := str(Time.get_unix_time_from_system())

	# ── Case 01: route completes and writes a valid schema ──────────────────
	var dir01 := make_dir("test_best_time/" + run_id + "/01-write")
	var path01 := dir01 + "/best_time.json"
	await fresh_game(path01)
	var completed01 := await drive_to_completion()
	check("01-route-complete", completed01, {"state": game.state})
	check("01-file-exists", FileAccess.file_exists(path01), {"path": path01})
	var recorded_best: float = 0.0
	if FileAccess.file_exists(path01):
		var raw := read_file(path01)
		var p = JSON.parse_string(raw)
		check("01-schema-format", p is Dictionary and p.get("format") == "walker-jumpman-clawd.best", {"format": p.get("format") if p is Dictionary else null})
		check("01-schema-version", p is Dictionary and (p.get("version") == 1 or p.get("version") == 1.0), {"version": p.get("version") if p is Dictionary else null})
		check("01-schema-level", p is Dictionary and p.get("level") == "first-steps", {"level": p.get("level") if p is Dictionary else null})
		var bs = p.get("best_seconds") if p is Dictionary else null
		var bs_ok := (bs is float or bs is int) and is_finite(float(bs)) and float(bs) > 0.0
		check("01-schema-best-seconds", bs_ok, {"best_seconds": bs})
		if bs_ok:
			recorded_best = float(bs)
	check("01-session-best-set", game.best_seconds > 0.0, {"best_seconds": game.best_seconds})

	# ── Case 02: a NEW session loads the same best from disk ─────────────────
	var dir02 := make_dir("test_best_time/" + run_id + "/02-load")
	DirAccess.copy_absolute(path01, dir02 + "/best_time.json")
	var path02 := dir02 + "/best_time.json"
	await fresh_game(path02)
	check("02-load-matches", recorded_best > 0.0 and absf(game.best_seconds - recorded_best) < 0.001, {"expected": recorded_best, "got": game.best_seconds})

	# ── Case 03: a slower completion does not replace the best ────────────────
	var dir03 := make_dir("test_best_time/" + run_id + "/03-slower")
	DirAccess.copy_absolute(path01, dir03 + "/best_time.json")
	var path03 := dir03 + "/best_time.json"
	var original_content := read_file(path03)
	await fresh_game(path03)
	var loaded_best: float = game.best_seconds
	game.elapsed = loaded_best + 15.0
	game.resolve_contacts(false, true)
	check("03-memory-unchanged", game.best_seconds == loaded_best, {"best_seconds": game.best_seconds, "slower": loaded_best + 15.0})
	check("03-file-unchanged", read_file(path03) == original_content, {"identical": read_file(path03) == original_content})

	# ── Case 04: invalid JSON → game playable → completion replaces the file ──
	var dir04 := make_dir("test_best_time/" + run_id + "/04-invalid-json")
	var path04 := dir04 + "/best_time.json"
	write_file(path04, "not { valid : json }")
	await fresh_game(path04)
	check("04-invalid-json-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("04-invalid-json-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})
	var completed04 := await drive_to_completion()
	check("04-invalid-json-completed", completed04, {"state": game.state})
	if FileAccess.file_exists(path04):
		var p04 = JSON.parse_string(read_file(path04))
		check("04-invalid-json-replaced", p04 is Dictionary and p04.get("format") == "walker-jumpman-clawd.best", {"parsed": str(p04)})
	else:
		check("04-invalid-json-replaced", false, {"error": "file missing after completion"})

	# ── Case 05: JSON array (not a dict) → game playable, best = 0 ───────────
	var dir05 := make_dir("test_best_time/" + run_id + "/05-not-dict")
	var path05 := dir05 + "/best_time.json"
	write_file(path05, "[1, 2, 3]")
	await fresh_game(path05)
	check("05-not-dict-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("05-not-dict-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})

	# ── Case 06: wrong format field → game playable, best = 0 ───────────────
	var dir06 := make_dir("test_best_time/" + run_id + "/06-wrong-format")
	var path06 := dir06 + "/best_time.json"
	write_file(path06, JSON.stringify({"format": "other-game.save", "version": 1, "level": "first-steps", "best_seconds": 30.0}))
	await fresh_game(path06)
	check("06-wrong-format-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("06-wrong-format-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})

	# ── Case 07: wrong level field → game playable, best = 0 ────────────────
	var dir07 := make_dir("test_best_time/" + run_id + "/07-wrong-level")
	var path07 := dir07 + "/best_time.json"
	write_file(path07, JSON.stringify({"format": "walker-jumpman-clawd.best", "version": 1, "level": "other-level", "best_seconds": 30.0}))
	await fresh_game(path07)
	check("07-wrong-level-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("07-wrong-level-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})

	# ── Case 08a: best_seconds = 0 (not > 0) ─────────────────────────────────
	var dir08a := make_dir("test_best_time/" + run_id + "/08a-zero-seconds")
	var path08a := dir08a + "/best_time.json"
	write_file(path08a, '{"format":"walker-jumpman-clawd.best","version":1,"level":"first-steps","best_seconds":0}')
	await fresh_game(path08a)
	check("08a-zero-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("08a-zero-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})

	# ── Case 08b: best_seconds = -1.5 (not > 0) ─────────────────────────────
	var dir08b := make_dir("test_best_time/" + run_id + "/08b-negative-seconds")
	var path08b := dir08b + "/best_time.json"
	write_file(path08b, '{"format":"walker-jumpman-clawd.best","version":1,"level":"first-steps","best_seconds":-1.5}')
	await fresh_game(path08b)
	check("08b-negative-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("08b-negative-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})

	# ── Case 08c: best_seconds = null (not a number) ─────────────────────────
	var dir08c := make_dir("test_best_time/" + run_id + "/08c-nonnumeric-seconds")
	var path08c := dir08c + "/best_time.json"
	write_file(path08c, '{"format":"walker-jumpman-clawd.best","version":1,"level":"first-steps","best_seconds":null}')
	await fresh_game(path08c)
	check("08c-nonnumeric-playable", game.state == Game.State.PLAYING, {"state": game.state})
	check("08c-nonnumeric-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})

	# ── Case 09: version-2 file (all fields valid) survives byte for byte ─────
	var dir09 := make_dir("test_best_time/" + run_id + "/09-version2-valid-fields")
	var path09 := dir09 + "/best_time.json"
	var v2_data := {"format": "walker-jumpman-clawd.best", "version": 2, "level": "first-steps", "best_seconds": 25.0, "future_field": "data from newer build"}
	var v2_content := JSON.stringify(v2_data)
	write_file(path09, v2_content)
	await fresh_game(path09)
	check("09-version2-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})
	check("09-version2-future-flag", game._best_from_future_version == true, {"flag": game._best_from_future_version})
	var completed09 := await drive_to_completion()
	check("09-version2-completed", completed09, {"state": game.state})
	var after09 := read_file(path09)
	check("09-version2-file-identical", after09 == v2_content, {"before_len": v2_content.length(), "after_len": after09.length(), "identical": after09 == v2_content})

	# ── Case 10: version-2 file with wrong level survives (version checked first)
	var dir10 := make_dir("test_best_time/" + run_id + "/10-version2-wrong-level")
	var path10 := dir10 + "/best_time.json"
	var v2_wrong_level := JSON.stringify({"format": "walker-jumpman-clawd.best", "version": 2, "level": "first-steps-remix", "best_seconds": 4.0})
	write_file(path10, v2_wrong_level)
	await fresh_game(path10)
	check("10-version2-wrong-level-future-flag", game._best_from_future_version == true, {"flag": game._best_from_future_version})
	check("10-version2-wrong-level-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})
	var completed10 := await drive_to_completion()
	check("10-version2-wrong-level-completed", completed10, {"state": game.state})
	var after10 := read_file(path10)
	check("10-version2-wrong-level-file-identical", after10 == v2_wrong_level, {"identical": after10 == v2_wrong_level})

	# ── Case 11: version-2 file with wrong format survives (version checked first)
	var dir11 := make_dir("test_best_time/" + run_id + "/11-version2-wrong-format")
	var path11 := dir11 + "/best_time.json"
	var v2_wrong_fmt := JSON.stringify({"format": "other-game.best", "version": 2, "level": "first-steps", "best_seconds": 4.0})
	write_file(path11, v2_wrong_fmt)
	await fresh_game(path11)
	check("11-version2-wrong-format-future-flag", game._best_from_future_version == true, {"flag": game._best_from_future_version})
	check("11-version2-wrong-format-no-best", game.best_seconds == 0.0, {"best_seconds": game.best_seconds})
	var completed11 := await drive_to_completion()
	check("11-version2-wrong-format-completed", completed11, {"state": game.state})
	var after11 := read_file(path11)
	check("11-version2-wrong-format-file-identical", after11 == v2_wrong_fmt, {"identical": after11 == v2_wrong_fmt})

	# ── Finish ────────────────────────────────────────────────────────────────
	var out := ProjectSettings.globalize_path("res://../evidence/test_best_time")
	DirAccess.make_dir_recursive_absolute(out)
	var report := {"scope": "FEAT-10 personal best persistence; not full GDD acceptance or human playtesting", "engine": Engine.get_version_info().string, "created_at": Time.get_datetime_string_from_system(true), "results": results, "failures": failures}
	var rf := FileAccess.open(out + "/best-time-" + run_id + ".json", FileAccess.WRITE)
	rf.store_string(JSON.stringify(report, "  "))
	rf.close()
	print("WALKER TESTS: %d checks / %d failures" % [results.size(), failures])
	await kill_game()
	quit(1 if failures else 0)
