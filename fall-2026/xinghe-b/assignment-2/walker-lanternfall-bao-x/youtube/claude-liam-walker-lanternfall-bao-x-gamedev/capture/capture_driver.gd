extends Node
## Film capture driver — used only in an isolated copy of the game at the film's source revision.
## It plays Lanternfall through the game's real input map (Input.action_press / InputEventAction), so the
## session reads the same actions a player's keys produce. Scripted input, labelled on screen.
## The one shortcut: the run starts with game.start_run(seed) instead of a random-seeded Enter press, so a
## take can be reproduced exactly. Disclosed in CAPTURE.md and FACTCHECK.md.
##
##   godot --path . res://capture_main.tscn --write-movie out.avi --fixed-fps 30 -- <take> <seed>
##   godot --headless --path . res://capture_main.tscn --fixed-fps 30 -- <take> <seed> [stop_after_s]   (dry run:
##   same 2 physics ticks per frame as the capture, so frames and input timing match it exactly)

const Session = preload("res://game/session.gd")
const GS = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")

const TITLE_FRAMES := 180          # 3 s of title screen before the run starts (physics frames, 60/s)
const PAUSE_AT_S := 40.0           # main take: pause 40 s into the run ...
const PAUSE_FOR_FRAMES := 180      # ... for 3 s
const END_HOLD_FRAMES := 300       # hold the result screen 5 s
const CARD_HOLD_FRAMES := 120      # each card screen stays up 2 s before the scripted pick, so it can be read
const CARD_PRIORITY := ["sunflare", "beam_rate", "beam_pierce", "moth_new", "moth_count", "moth_radius",
	"pass_damage", "pass_haste", "pass_magnet", "pass_speed", "pass_hp", "heal"]

var game
var take := "main"
var run_seed := 1
var f := 0
var started_at := -1
var ended_at := -1
var restart_at := -1
var paused_at := -1
var card_seen_at := -1      # physics frame the current card screen was first seen
var card_pressed_f := -1000  # frame of the last scripted pick (its input event lands a frame or two later)
var log_lines: Array = []
var label: Label
var stop_after_s := -1.0   # optional third arg: end the take after this many seconds of run time
var watch := {}            # film diagnostic: bolt/monster sprite overlaps, see _watch_beams()
var stale: Array = []      # process frames written while the window could not draw (see _hold_for_window)
var last_stale := -1
var track: Array = []      # optional (LF_LOG_TRACK=1): per movie frame, the courier's viewport position and zoom
var sfx_seen := 0          # how much of the AudioBus play log has been copied to the capture log

func _ready() -> void:
	process_physics_priority = -100   # act before the session reads the input this frame
	process_mode = Node.PROCESS_MODE_ALWAYS   # keeps running while _hold_for_window() pauses the tree
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		take = args[0]
	if args.size() > 1:
		run_seed = int(args[1])
	if args.size() > 2:
		stop_after_s = float(args[2])
	game = Session.new()
	game.process_mode = Node.PROCESS_MODE_PAUSABLE   # as when it runs as the main scene (the driver itself is ALWAYS)
	add_child(game)
	if OS.get_environment("LF_LOG_EVENTS") == "1":   # optional, read-only: every kill and gem, for the film's counters
		game.enemy_killed.connect(func(_p): _log("killed", {}))
		game.gem_collected.connect(func(_v): _log("gem", {}))
	var layer := CanvasLayer.new()
	layer.layer = 50
	add_child(layer)
	label = Label.new()
	label.text = "Real engine capture · scripted input"
	label.add_theme_font_size_override("font_size", 9)
	label.modulate = Color(1, 1, 1, 0.55)
	label.position = Vector2(8, 340)
	layer.add_child(label)

func _physics_process(_d: float) -> void:
	if _hold_for_window():
		return
	f += 1
	if f % 2 == 1 and f > 1 and OS.get_environment("LF_LOG_TRACK") == "1":
		# first physics step of an iteration: the transform and position are the ones the previous frame was drawn with
		var t: Transform2D = get_viewport().get_canvas_transform()
		var p: Vector2 = t * game.player.position
		track.append([snappedf(p.x, 0.1), snappedf(p.y, 0.1), snappedf(t.get_scale().x, 0.001), snappedf(t.get_rotation(), 0.001)])
	if game.audio and game.audio.play_log.size() > sfx_seen:
		for i in range(sfx_seen, game.audio.play_log.size()):
			_log("sfx", {"id": game.audio.play_log[i]["id"]})
		sfx_seen = game.audio.play_log.size()
	if f == 1:
		_log("first_frame", {"process_frame": Engine.get_process_frames()})
	if f == TITLE_FRAMES:
		game.start_run(run_seed)
		started_at = f
		_log("start_run", {"seed": run_seed})
	if started_at < 0:
		return
	_watch_beams()
	if stop_after_s > 0.0 and game.tick_count >= int(stop_after_s * 60):
		_finish()
		return
	var st: int = game.state.current
	if st == GS.LEVELUP:
		_release_moves()
		if f - card_pressed_f < 4:      # the last pick has not landed yet
			return
		if card_seen_at < 0:
			card_seen_at = f
		elif f >= card_seen_at + CARD_HOLD_FRAMES:
			_choose_card()
			card_pressed_f = f
			card_seen_at = -1
		return
	card_seen_at = -1
	if st == GS.WON or st == GS.LOST:
		_release_moves()
		if ended_at < 0:
			ended_at = f
			_log("ended", {"state": GS.NAMES[st], "run_s": game.tick_count / 60.0, "level": game.prog.level, "kills": game.kills, "evolved": game.prog.evolved_sunflare})
		if take == "lose" and st == GS.LOST and f == ended_at + 15 and restart_at < 0:
			restart_at = f
			_action("restart")
		if f >= ended_at + END_HOLD_FRAMES:
			_finish()
		return
	if restart_at > 0:
		if f >= restart_at + 180:
			_finish()
		_steer(Vector2.ZERO)
		return
	match take:
		"main":
			if paused_at < 0 and game.tick_count >= int(PAUSE_AT_S * 60):
				paused_at = f
				_release_moves()
				_action("pause")
				return
			if st == GS.PAUSED:
				if f >= paused_at + PAUSE_FOR_FRAMES:
					_action("pause")
				return
			_steer(_smart_axis())
		"beam":
			_steer(_smart_axis())
		"lose":
			_steer(_smart_axis() if game.tick_count < 20 * 60 else Vector2.ZERO)
		"props":
			_props_take()

## Movie Maker writes one frame per engine iteration, but macOS skips drawing while the window is occluded (another
## Space, a full-screen app) and the writer then repeats the last picture. So while the window cannot draw, the
## whole tree — game and audio — is paused and the iteration is logged as stale; the edit drops those frames and
## their audio, which leaves the take continuous. The game's own code and state are untouched by this.
## The AudioBus normally runs with PROCESS_MODE_ALWAYS; during a hold it is made pausable so its players pause
## too (the music resumes on the exact sample), and it is set back to ALWAYS as soon as the window draws again.
func _hold_for_window() -> bool:
	if DisplayServer.get_name() == "headless":   # dry runs draw nothing, so there is nothing to hold for
		return false
	if not DisplayServer.window_can_draw():
		var it := Engine.get_process_frames()
		if it != last_stale:
			last_stale = it
			stale.append(it)
		if not get_tree().paused:
			get_tree().paused = true
			if game.audio:
				game.audio.process_mode = Node.PROCESS_MODE_PAUSABLE
		return true
	if get_tree().paused:
		if game.audio:
			game.audio.process_mode = Node.PROCESS_MODE_ALWAYS
		get_tree().paused = false
	return false

func _props_take() -> void:
	var t: int = game.tick_count
	var stall: Vector2 = _nearest("stall")
	var box: Rect2 = game.ground._solid_box("stall", stall)
	var target := Vector2(box.position.x - 40, box.get_center().y)
	if t < 360:
		var to: Vector2 = target - game.player.position
		_steer(to.normalized() if to.length() > 6 else Vector2.ZERO)
	elif t < 480:
		_steer(Vector2.RIGHT)                            # walk into the stall's side
	elif t < 600:
		_steer(Vector2(1, 1).normalized())               # push diagonally: slide along it
	elif t < 1320:
		_steer(Vector2.ZERO)
		var k := t - 600
		if k == 0 or k == 120:
			_action("mute_all")
		if k == 240 or k == 360:
			_action("mute_music")
		if k == 480 or k == 600:
			_action("mute_sfx")
	else:
		_finish()

## Visible half-extents of the enemy sprites (measured from enemy_moth.png / enemy_wraith.png; the same numbers
## the a51af69 fix put in Tuning), so the diagnostic also works on builds from before that fix.
const SPRITE_HALF := {"moth": Vector2(11, 7), "wraith": Vector2(13, 19)}

## Film diagnostic only — it reads the session and never changes it. Each tick: which bolts visibly overlap a
## monster's sprite? When an overlap ends: if the bolt is still flying and never counted that monster, log
## "pass_through" (what Bao saw); if it hit although its centre stayed outside the old radius test, "edge_hit".
func _watch_beams() -> void:
	var seen := {}
	for s in game.shots:
		if not is_instance_valid(s):
			continue
		for e in game.enemies:
			if not is_instance_valid(e) or e.dead or not SPRITE_HALF.has(e.kind):
				continue
			if not _bolt_over_sprite(s, e):
				continue
			var key := "%d:%d" % [s.get_instance_id(), e.get_instance_id()]
			seen[key] = true
			if not watch.has(key):
				watch[key] = {"first": f, "shot": s, "enemy": e.get_instance_id(), "kind": e.kind,
					"radius": e.radius, "d_min": INF, "at": e.position, "view_first": _view(s, e)}
			watch[key]["last"] = f
			watch[key]["view_last"] = _view(s, e)
			watch[key]["d_min"] = minf(watch[key]["d_min"], s.position.distance_to(e.position))
			watch[key]["at"] = e.position
	for key in watch.keys():
		if seen.has(key):
			continue
		var w: Dictionary = watch[key]
		watch.erase(key)
		var s = w["shot"]
		var alive: bool = is_instance_valid(s) and game.shots.has(s)
		var hit: bool = (not alive) or s.hit_ids.has(w["enemy"])
		var old_reach: float = w["radius"] + 4.0   # the pre-fix test: centre distance < radius + BEAM_RADIUS (4)
		var data := {"first": w["first"], "last": w["last"], "kind": w["kind"], "d_min": snappedf(w["d_min"], 0.1),
			"x": snappedf(w["at"].x, 0.1), "y": snappedf(w["at"].y, 0.1),
			"view_first": w["view_first"], "view_last": w["view_last"]}
		if alive and not hit:
			_log("pass_through", data)
		elif hit and w["d_min"] >= old_reach:
			_log("edge_hit", data)

## Where the bolt and the monster are on screen, in 640 x 360 viewport pixels (x 6 for the 4K window).
func _view(s, e) -> Dictionary:
	var t: Transform2D = get_viewport().get_canvas_transform()
	var b: Vector2 = t * s.position
	var m: Vector2 = t * e.position
	return {"bolt": [snappedf(b.x, 0.1), snappedf(b.y, 0.1)], "monster": [snappedf(m.x, 0.1), snappedf(m.y, 0.1)],
		"dir": [snappedf(s.dir.x, 0.01), snappedf(s.dir.y, 0.01)], "zoom": snappedf(t.get_scale().x, 0.001)}

func _bolt_over_sprite(s, e) -> bool:
	var half: Vector2 = SPRITE_HALF[e.kind]
	var a: Vector2 = s.position - s.dir * 7.0
	var b: Vector2 = s.position + s.dir * 7.0
	for i in 9:
		var q: Vector2 = (a.lerp(b, i / 8.0) - e.position).abs()
		if q.x <= half.x + 1.0 and q.y <= half.y + 1.0:
			return true
	return false

func _smart_axis() -> Vector2:
	var p: Vector2 = game.player.position
	var push := Vector2.ZERO
	for e in game.enemies:
		var d: Vector2 = p - e.position
		if d.length() < 90.0:
			push += d.normalized() * (90.0 - d.length())
	if push.length() > 1.0:
		return push.normalized()
	if not game.gems.is_empty():
		var best: Vector2 = game.gems[0].position
		for g in game.gems:
			if g.position.distance_to(p) < best.distance_to(p):
				best = g.position
		return (best - p).normalized()
	var a := float(game.tick_count) / 90.0
	return Vector2(cos(a), sin(a))

func _choose_card() -> void:
	for want in CARD_PRIORITY:
		var i: int = game.offered.find(want)
		if i >= 0:
			_action("card_%d" % (i + 1))
			_log("card", {"picked": want, "offered": game.offered})
			return

func _steer(axis: Vector2) -> void:
	_set_action("move_right", maxf(axis.x, 0.0))
	_set_action("move_left", maxf(-axis.x, 0.0))
	_set_action("move_down", maxf(axis.y, 0.0))
	_set_action("move_up", maxf(-axis.y, 0.0))

func _set_action(a: String, strength: float) -> void:
	if strength > 0.0:
		Input.action_press(a, strength)
	else:
		Input.action_release(a)

func _release_moves() -> void:
	_steer(Vector2.ZERO)

func _action(a: String) -> void:
	var ev := InputEventAction.new()
	ev.action = a
	ev.pressed = true
	Input.parse_input_event(ev)
	var up := InputEventAction.new()
	up.action = a
	up.pressed = false
	Input.parse_input_event(up)
	_log("action", {"action": a})

func _nearest(kind: String) -> Vector2:
	var best := Vector2.INF
	for p in game.ground.props:
		if p["kind"] == kind and p["pos"].length() < best.length():
			best = p["pos"]
	return best

func _log(what: String, data: Dictionary) -> void:
	var line := {"frame": f, "pf": Engine.get_process_frames(), "tick": game.tick_count if game.prog else 0, "event": what}
	line.merge(data)
	log_lines.append(line)
	print(JSON.stringify(line))

func _finish() -> void:
	_log("movie_frames", {"process_frame": Engine.get_process_frames(), "stale": stale})
	if not track.is_empty():
		_log("track", {"note": "entry i = courier viewport position [x, y], zoom, rotation as drawn in movie frame i", "frames": track})
	var path := OS.get_environment("LF_CAPTURE_LOG")
	if path != "":
		var fh := FileAccess.open(path, FileAccess.WRITE)
		for l in log_lines:
			fh.store_line(JSON.stringify(l))
		fh.close()
	get_tree().quit()
