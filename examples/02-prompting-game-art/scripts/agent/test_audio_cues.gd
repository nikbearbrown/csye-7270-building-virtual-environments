extends SceneTree
## Audio-cue headless test.
## Run: godot --headless --path godot --script res://tests/test_audio_cues.gd --fixed-fps 60

const GameScene = preload("res://game/main.tscn")
const Game = preload("res://game/session.gd")

var game: Node2D
var cues: Node
var checks: int = 0
var failures: int = 0
var observed_jumps: int = 0
var observed_deaths: int = 0
var observed_jump_cues: int = 0
var observed_fail_cues: int = 0
var jump_frames: Array[int] = []
var death_frames: Array[int] = []
var jump_cue_frames: Array[int] = []
var fail_cue_frames: Array[int] = []

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for _i in range(n):
		await physics_frame
		_record_event_frames()
		await process_frame

func _record_event_frames() -> void:
	var frame := Engine.get_physics_frames()
	while game.player.jumps > observed_jumps:
		observed_jumps += 1
		jump_frames.append(frame)
		print("FRAME jump %d: physics=%d" % [observed_jumps, frame])
	while game.deaths > observed_deaths:
		observed_deaths += 1
		death_frames.append(frame)
		print("FRAME death %d: physics=%d" % [observed_deaths, frame])
	if is_instance_valid(cues):
		while cues.jump_plays > observed_jump_cues:
			observed_jump_cues += 1
			jump_cue_frames.append(frame)
			print("FRAME jump cue %d: physics=%d" % [observed_jump_cues, frame])
		while cues.fail_plays > observed_fail_cues:
			observed_fail_cues += 1
			fail_cue_frames.append(frame)
			print("FRAME death cue %d: physics=%d" % [observed_fail_cues, frame])

func check(label: String, passed: bool) -> void:
	checks += 1
	print("%s  %s" % ["PASS" if passed else "FAIL", label])
	if not passed:
		failures += 1

func wait_for_floor(max_steps: int = 90) -> void:
	var waited := 0
	while not game.player.is_on_floor() and waited < max_steps:
		await steps(1)
		waited += 1

func reset_observations() -> void:
	observed_jumps = 0
	observed_deaths = 0
	observed_jump_cues = 0
	observed_fail_cues = 0
	jump_frames.clear()
	death_frames.clear()
	jump_cue_frames.clear()
	fail_cue_frames.clear()

func fresh(with_cues: bool) -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = GameScene.instantiate()
	game.test_mode = true
	root.add_child(game)
	cues = game.get_node("AudioCues")
	if not with_cues:
		game.remove_child(cues)
		cues.queue_free()
		cues = null
	game.start_session()
	game.player.test_control = true
	reset_observations()
	await steps(3)

func do_three_jumps() -> void:
	for jump_index in range(3):
		if jump_index == 2:
			game.player.test_axis = 1.0
		game.player.test_jump_pressed = true
		game.player.test_jump_held = true
		await steps(1)
		game.player.test_jump_held = false
		await wait_for_floor(90)
		game.player.test_axis = 0.0
		await steps(4)

func do_spike_death() -> void:
	game.player.test_axis = 1.0
	var waited := 0
	while game.state == Game.State.PLAYING and waited < 400:
		if game.player.position.x >= 290.0:
			game.player.test_axis = 0.1
		await steps(1)
		waited += 1
	game.player.test_axis = 0.0
	await steps(2)
	print("ROUTE spike attempt: state=%d position=%s ticks=%d" % [game.state, game.player.position, waited])

func do_retry_wait() -> void:
	await steps(40)

func press_pause_action() -> void:
	Input.action_press("pause")
	var event := InputEventAction.new()
	event.action = "pause"
	event.pressed = true
	Input.parse_input_event(event)
	await steps(1)
	Input.action_release("pause")
	event = InputEventAction.new()
	event.action = "pause"
	event.pressed = false
	Input.parse_input_event(event)
	await steps(2)

func do_pause_resume() -> void:
	await press_pause_action()
	await press_pause_action()

func import_loop_mode(path: String) -> Variant:
	var config := ConfigFile.new()
	if config.load(path) != OK:
		return null
	return config.get_value("params", "edit/loop_mode", null)

func run() -> void:
	await fresh(true)

	await do_three_jumps()
	check("jump-cues: 3 jumps → exactly 3 play() calls", cues.jump_plays == 3)

	await do_spike_death()
	check("fail-cue: spike death → exactly 1 play() call", cues.fail_plays == 1)
	check("fail-cue: game is DYING after spike", game.state == Game.State.DYING)
	check("event/cue physics frames are printed and paired",
		jump_frames.size() == 3 and jump_cue_frames.size() == 3
		and death_frames.size() == 1 and fail_cue_frames.size() == 1
		and jump_cue_frames[0] == jump_frames[0] + 1
		and jump_cue_frames[1] == jump_frames[1] + 1
		and jump_cue_frames[2] == jump_frames[2] + 1
		and fail_cue_frames[0] == death_frames[0] + 1)

	await do_retry_wait()

	var wav := load("res://audio/placeholder/music_loop.wav") as AudioStreamWAV
	check("music-loop: resource loads as AudioStreamWAV", wav != null)
	if wav != null:
		check("music-loop: loop_mode == LOOP_FORWARD",
			wav.loop_mode == AudioStreamWAV.LOOP_FORWARD)
		check("music-loop: loop_begin == 0", wav.loop_begin == 0)
		check("music-loop: loop_end == 176399 (last sample of 4 s @ 44100)",
			wav.loop_end == 176399)

	var j_wav := load("res://audio/placeholder/jump.wav") as AudioStreamWAV
	check("jump.wav: loop_mode == LOOP_DISABLED",
		j_wav != null and j_wav.loop_mode == AudioStreamWAV.LOOP_DISABLED)
	var f_wav := load("res://audio/placeholder/fail.wav") as AudioStreamWAV
	check("fail.wav: loop_mode == LOOP_DISABLED",
		f_wav != null and f_wav.loop_mode == AudioStreamWAV.LOOP_DISABLED)
	check("music_loop.wav.import: edit/loop_mode == LOOP_FORWARD",
		import_loop_mode("res://audio/placeholder/music_loop.wav.import") == 2)
	check("jump.wav.import: edit/loop_mode == LOOP_DISABLED",
		import_loop_mode("res://audio/placeholder/jump.wav.import") == 1)
	check("fail.wav.import: edit/loop_mode == LOOP_DISABLED",
		import_loop_mode("res://audio/placeholder/fail.wav.import") == 1)

	await press_pause_action()
	var paused_flag: bool = cues._music_stream.stream_paused
	await press_pause_action()
	var resumed_flag: bool = not cues._music_stream.stream_paused
	check("music pauses while PAUSED", paused_flag)
	check("music resumes when PLAYING resumes", resumed_flag)

	var with_state: int = game.state
	var with_deaths: int = game.deaths
	game.queue_free()
	await process_frame

	await fresh(false)
	await do_three_jumps()
	await do_spike_death()
	await do_retry_wait()
	await do_pause_resume()

	check("no-cues: game.state matches with-cues run", game.state == with_state)
	check("no-cues: game.deaths matches with-cues run", game.deaths == with_deaths)

	game.queue_free()
	await process_frame
	print("\ntest_audio_cues: %d/%d passed" % [checks - failures, checks])
	quit(1 if failures else 0)
