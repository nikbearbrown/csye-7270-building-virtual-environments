extends SceneTree
## Audio-cue headless test.
## Run: godot --headless --path godot --script res://tests/test_audio_cues.gd --fixed-fps 60

const Game      = preload("res://game/session.gd")
const AudioCues = preload("res://audio/audio_cues.gd")

var game: Node2D
var cues: Node
var checks: int  = 0
var failures: int = 0

func _initialize() -> void:
	call_deferred("run")

func steps(n: int) -> void:
	for _i in range(n):
		await physics_frame
		await process_frame

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

# ----- scene helpers --------------------------------------------------------

func fresh_with_cues() -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)        # game._ready() runs → player created
	cues = AudioCues.new()
	game.add_child(cues)        # cues._ready() runs with player already alive
	game.start_session()
	game.player.test_control = true
	await steps(3)

func fresh_without_cues() -> void:
	if is_instance_valid(game):
		game.queue_free()
		await process_frame
	game = Game.new()
	game.test_mode = true
	root.add_child(game)
	game.start_session()
	game.player.test_control = true
	await steps(3)

# ----- shared input sequence ------------------------------------------------
# Three jumps, one spike death, auto-retry, pause, resume.

func do_three_jumps() -> void:
	for _i in range(3):
		game.player.test_jump_pressed = true
		game.player.test_jump_held   = true
		await steps(1)
		game.player.test_jump_held = false
		await wait_for_floor(90)
		await steps(4)          # settle on floor before next jump

func do_spike_death() -> void:
	game.player.position = Vector2(330.0, 310.0)
	await steps(4)              # contact_settle_ticks=2, then death

func do_retry_wait() -> void:
	await steps(40)             # 0.55 s retry @ 60 fps ≈ 33 frames

func do_pause_resume() -> void:
	game.set_paused(true)
	await steps(3)
	game.set_paused(false)
	await steps(3)

# ----- main -----------------------------------------------------------------

func run() -> void:
	# ── Part A: with AudioCues ──────────────────────────────────────────────
	await fresh_with_cues()

	await do_three_jumps()
	check("jump-cues: 3 jumps → exactly 3 play() calls", cues.jump_plays == 3)

	await do_spike_death()
	check("fail-cue: spike death → exactly 1 play() call", cues.fail_plays == 1)
	check("fail-cue: game is DYING after spike", game.state == Game.State.DYING)

	await do_retry_wait()

	# Music import settings (loaded fresh from the imported resource)
	var wav := load("res://audio/placeholder/music_loop.wav") as AudioStreamWAV
	check("music-loop: resource loads as AudioStreamWAV", wav != null)
	if wav != null:
		check("music-loop: loop_mode == LOOP_FORWARD",
			wav.loop_mode == AudioStreamWAV.LOOP_FORWARD)
		check("music-loop: loop_begin == 0", wav.loop_begin == 0)
		check("music-loop: loop_end == 176399 (last sample of 4 s @ 44100)",
			wav.loop_end == 176399)

	# Effects have looping disabled
	var j_wav := load("res://audio/placeholder/jump.wav") as AudioStreamWAV
	check("jump.wav: loop_mode == LOOP_DISABLED",
		j_wav != null and j_wav.loop_mode == AudioStreamWAV.LOOP_DISABLED)
	var f_wav := load("res://audio/placeholder/fail.wav") as AudioStreamWAV
	check("fail.wav: loop_mode == LOOP_DISABLED",
		f_wav != null and f_wav.loop_mode == AudioStreamWAV.LOOP_DISABLED)

	# Pause / resume changes stream_paused on the music player
	game.set_paused(true)
	await steps(3)
	var paused_flag: bool = cues._music_stream.stream_paused
	game.set_paused(false)
	await steps(3)
	var resumed_flag: bool = not cues._music_stream.stream_paused
	check("music pauses while PAUSED", paused_flag)
	check("music resumes when PLAYING resumes", resumed_flag)

	# Record outcome with cues present
	var with_state:  int = game.state
	var with_deaths: int = game.deaths

	game.queue_free()
	await process_frame

	# ── Part B: same inputs without AudioCues ───────────────────────────────
	await fresh_without_cues()

	await do_three_jumps()
	await do_spike_death()
	await do_retry_wait()
	await do_pause_resume()

	check("no-cues: game.state matches with-cues run",  game.state  == with_state)
	check("no-cues: game.deaths matches with-cues run", game.deaths == with_deaths)

	game.queue_free()
	await process_frame

	print("\ntest_audio_cues: %d/%d passed" % [checks - failures, checks])
	quit(1 if failures else 0)
