extends Node
## Input-only capture driver for the film (scripted input, not a human playtest).
##
## Every action is a real input event sent through Input.parse_input_event:
## InputEventAction for move/jump/pause/mute, and InputEventMouseMotion +
## InputEventMouseButton (left) for aiming and casting, in window coordinates. For aiming,
## the real OS cursor is also moved there with Input.warp_mouse (a windowed Godot reads it).
## They reach the game's own code paths: Input.get_axis / is_action_just_pressed in
## player.gd, get_global_mouse_position() for the aim, and SessionInput._unhandled_input
## for Esc, M and N.
##
## The driver READS the player, wolf, HUD and audio state to decide when to press and to
## assert the result. It WRITES nothing to the game: no position, velocity, HP, state,
## collision or test-only hook (the player's `use_scripted` stays false).
## Runs at physics priority -20, ahead of the player, so a press counts on the tick it is
## issued. Every action and every game event is logged against the physics tick.

const GROUND_TOP := 327.0

var main: Node
var to_window: Callable   # world -> window pixels, provided by the harness
var to_root: Callable     # world -> root-viewport pixels (Input.warp_mouse applies the stretch itself)
var mode := ""
var attempt := 1
var log_path := ""
var done := false
var exit_code := 0
var tail_frames := 120
var events := {"cast": 0, "hurt": 0, "wolf_down": 0, "fail": 0, "clear": 0}

var _tick := 0
var _phase := 0
var _wait := 0
var _release_next: Array[String] = []
var _held := {}
var _mouse_up_next := false
var _lines: PackedStringArray = []
var _flushed := false
var _notes := {}


func _ready() -> void:
	process_physics_priority = -20
	process_mode = Node.PROCESS_MODE_ALWAYS   # must be able to press Esc again while paused
	var p: Node = main.player
	p.cast_fired.connect(func(o: Vector2, d: Vector2) -> void: _event("cast", {"origin": [o.x, o.y], "dir": [snappedf(d.x, 0.001), snappedf(d.y, 0.001)]}))
	p.hurt.connect(func(hp: int) -> void: _event("hurt", {"hp": hp}))
	p.failed.connect(func(r: String) -> void: _event("fail", {"reason": r}))
	p.cleared.connect(func() -> void: _event("clear", {}))
	for w in get_tree().get_nodes_in_group("wolves"):
		w.defeated.connect(func() -> void: _event("wolf_down", {}))
	var win := DisplayServer.window_get_size()
	var root_size := get_tree().root.get_visible_rect().size
	_log({"event": "start", "mode": mode, "attempt": attempt, "window": [win.x, win.y], "root_viewport": [root_size.x, root_size.y]})


# ---------------------------------------------------------------- input (the only way in)

func _send_action(action: String, pressed: bool, kind := "") -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)
	Input.flush_buffered_events()   # effective on this tick, before the player reads input
	_log({"event": kind if kind != "" else ("press" if pressed else "release"), "action": action})


func _hold(action: String) -> void:
	_held[action] = true
	_send_action(action, true)


func _let_go(action: String) -> void:
	_held.erase(action)
	_send_action(action, false)


func _tap(action: String) -> void:
	_send_action(action, true)
	_release_next.append(action)


## Move the mouse to a world point and press the left button (released next tick).
func _cast_at(world: Vector2) -> void:
	var window: Vector2 = to_window.call(world)
	# In a real window Godot reads the OS cursor, which overrides injected motion events
	# (seen in the windowed probe), so the real cursor is moved there first. Headless has no
	# OS cursor and uses the motion event below.
	Input.warp_mouse(window)   # window pixels (measured: warp_mouse(p) reads back p)
	var motion := InputEventMouseMotion.new()
	motion.position = window
	motion.global_position = window
	Input.parse_input_event(motion)
	var click := InputEventMouseButton.new()
	click.button_index = MOUSE_BUTTON_LEFT
	click.pressed = true
	click.position = window
	click.global_position = window
	Input.parse_input_event(click)
	Input.flush_buffered_events()
	_mouse_up_next = true
	_log({"event": "click", "aim_world": [snappedf(world.x, 0.1), snappedf(world.y, 0.1)], "window": [snappedf(window.x, 0.1), snappedf(window.y, 0.1)]})


func _mouse_up() -> void:
	var up := InputEventMouseButton.new()
	up.button_index = MOUSE_BUTTON_LEFT
	up.pressed = false
	Input.parse_input_event(up)


# ---------------------------------------------------------------- reading the game

func _player() -> Node:
	return main.player


func _wolf() -> Node:
	return main.get_node_or_null("Level/Wolf")


func _wolf_target() -> Vector2:
	return _wolf().global_position + Vector2(0, -14)


func _bus_muted(bus: String) -> bool:
	return AudioServer.is_bus_mute(AudioServer.get_bus_index(bus))


# ---------------------------------------------------------------- the takes

func _physics_process(_delta: float) -> void:
	if done:
		return
	_tick += 1
	# A held action the OS released (window focus loss) is pressed again before the player
	# reads it, so the scripted hold stays continuous. Logged as "reassert".
	for a: String in _held:
		if not Input.is_action_pressed(a):
			_send_action(a, true, "reassert")
	for a in _release_next:
		_let_go(a)
	_release_next.clear()
	if _mouse_up_next:
		# What the game itself reads back for the aim, one tick after the click (read-only).
		_log({"event": "mouse_seen", "game_mouse_world": [snappedf(_player().get_global_mouse_position().x, 0.1), snappedf(_player().get_global_mouse_position().y, 0.1)]})
		_mouse_up()
		_mouse_up_next = false
	if _wait > 0:
		_wait -= 1
		return
	match mode:
		"probe": _probe()
		"run-01": _run_01()
		"run-02": _run_02()
		"run-03": _run_03()
		"run-04": _run_04()
		_: _fail_take("unknown WALKER_CAPTURE_MODE '%s'" % mode)


## Short probe: run, jump the pit, one cast at the wolf.
func _probe() -> void:
	var p := _player()
	match _phase:
		0: _wait = 30; _phase = 1
		1: _hold("move_right"); _phase = 2
		2:
			if p.global_position.x >= 506.0:
				_hold("jump"); _phase = 3; _wait = 25
		3: _let_go("jump"); _phase = 4
		4:
			if p.is_on_floor() and p.global_position.x >= 600.0:
				_let_go("move_right"); _phase = 5; _wait = 20
		5: _cast_at(_wolf_target()); _phase = 6; _wait = 60
		6:
			_check(not p.is_failing and p.global_position.x > 590.0 and events.cast == 1,
				"probe: landed past the pit and cast once")


## The route: run, jump the pit, walk into the wolf's sight and take one lunge, defeat it
## with fireballs, reach the exit.
func _run_01() -> void:
	var p := _player()
	var w := _wolf()
	match _phase:
		0: _wait = 45; _phase = 1
		1: _hold("move_right"); _phase = 2
		2:
			if p.global_position.x >= 506.0:
				_hold("jump"); _phase = 3; _wait = 25
		3: _let_go("jump"); _phase = 4
		4:
			# Keep walking toward the wolf until it growls (its telegraph), close in a little
			# more so its lunge can reach, then stand still and take the hit.
			if w and w.state == Wolf.State.GROWL:
				_phase = 5; _wait = 10
		5: _let_go("move_right"); _phase = 6
		6:
			if events.hurt >= 1:
				_phase = 7; _wait = 20       # knockback / hurt hold
		7:
			if events.wolf_down >= 1:
				_phase = 8; _wait = 50       # the down image is held, then the wolf is gone
			elif _tick % 22 == 0:
				_cast_at(_wolf_target())
		8: _hold("move_right"); _phase = 9
		9:
			if events.clear >= 1:
				_let_go("move_right"); tail_frames = 150
				_check(events.clear == 1 and events.wolf_down == 1 and events.hurt >= 1 and events.fail == 0 and events.cast >= 2,
					"run-01: hurt, wolf defeated, exit reached, no fail")


## A real pit fall, the reload, and the music back from the top.
func _run_02() -> void:
	var p := _player()
	if attempt == 1:
		match _phase:
			0: _wait = 30; _phase = 1
			1: _hold("move_right"); _phase = 2
			2:
				if events.fail >= 1:
					_let_go("move_right"); _phase = 3   # the game reloads itself after 1.2 s
		return
	match _phase:
		0: _wait = 150; _phase = 1
		1:
			tail_frames = 30
			_check(main.audio.music.playing and p.hp == 5 and not p.is_failing,
				"run-02: after the reload the music plays again and the mage is back")


## M and N: music off, effects off (a silent cast), effects on (an audible cast), music on.
func _run_03() -> void:
	match _phase:
		0: _wait = 40; _phase = 1
		1: _tap("mute_music"); _phase = 2; _wait = 90
		2: _notes["music_muted"] = _bus_muted("Music"); _tap("mute_sfx"); _phase = 3; _wait = 40
		3: _notes["sfx_muted"] = _bus_muted("SFX"); _cast_at(_player().global_position + Vector2(160, -60)); _phase = 4; _wait = 60
		4: _tap("mute_sfx"); _phase = 5; _wait = 30
		5: _cast_at(_player().global_position + Vector2(160, -60)); _phase = 6; _wait = 60
		6: _tap("mute_music"); _phase = 7; _wait = 120
		7:
			_check(_notes.get("music_muted", false) and _notes.get("sfx_muted", false) and events.cast == 2
				and not _bus_muted("Music") and not _bus_muted("SFX"),
				"run-03: M muted music, N muted effects, both restored, two casts")


## Esc pause and resume.
func _run_04() -> void:
	var p := _player()
	match _phase:
		0: _wait = 30; _phase = 1
		1: _hold("move_right"); _phase = 2; _wait = 40
		2: _tap("pause"); _phase = 3; _wait = 3
		3: _notes["x_paused"] = p.global_position.x; _notes["paused"] = get_tree().paused; _phase = 4; _wait = 117
		4: _notes["x_after"] = p.global_position.x; _tap("pause"); _phase = 5; _wait = 60
		5:
			_let_go("move_right")
			_check(_notes.paused and absf(_notes.x_after - _notes.x_paused) < 0.01 and p.global_position.x > _notes.x_after + 20.0,
				"run-04: Esc froze play and Esc resumed it")


# ---------------------------------------------------------------- log and verdict

func _check(ok: bool, what: String) -> void:
	_log({"event": "assert", "ok": ok, "what": what, "events": events.duplicate()})
	exit_code = 0 if ok else 1
	if not ok:
		push_error("ASSERT FAIL: " + what)
	done = true


## Called by the harness when the window loses focus. Logged; held actions are re-asserted
## on the next physics tick (see _physics_process). The reference gate judges the take.
func note_focus_loss(frame: int) -> void:
	_log({"event": "focus_lost", "frame": frame})


func _fail_take(why: String) -> void:
	_log({"event": "assert", "ok": false, "what": why})
	exit_code = 1
	done = true


func _event(kind: String, extra: Dictionary) -> void:
	events[kind] += 1
	var d := {"event": "game:" + kind}
	d.merge(extra)
	_log(d)


func _log(d: Dictionary) -> void:
	var p: Node = main.player if main else null
	var row := {"tick": _tick, "attempt": attempt}
	if p:
		row["x"] = snappedf(p.global_position.x, 0.01)
		row["y"] = snappedf(p.global_position.y, 0.01)
		row["state"] = Player.State.keys()[p.state]
	row.merge(d)
	_lines.append(JSON.stringify(row))


func finish(reason: String) -> void:
	if _flushed:
		return
	_flushed = true
	_log({"event": "finish", "reason": reason})
	if log_path.is_empty():
		return
	var f := FileAccess.open(log_path, FileAccess.READ_WRITE if attempt > 1 and FileAccess.file_exists(log_path) else FileAccess.WRITE)
	f.seek_end()
	f.store_string("\n".join(_lines) + "\n")
	f.close()


func _exit_tree() -> void:
	# run-02 attempt 1 ends by the game's own reload, not by the harness: keep its log.
	finish("scene reloaded by the game")
