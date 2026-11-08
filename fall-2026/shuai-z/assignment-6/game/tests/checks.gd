extends Node
## Headless checks for the greybox. Run from the repository root:
##   Godot --headless --path game --fixed-fps 60 res://tests/checks.tscn
## Prints one line per check and exits with code 1 if any check fails.
## Step 1a: the scenes have their nodes, Rudy's capsule matches the character
## sheet, his movement states, turning on the spot, the camera, and the jump
## sound's guard (one Sfx "jump" per takeoff, CHANGE-BRIEF.md).
## Step 1b: the layout, a fall below a cliff, the respawn at the last
## checkpoint, the waystone, the teleport circle and the end card, a clean
## route from the opening to the circle, and how forgiving the widest cliff is.
## Sounds counted: "fall", "checkpoint", "portal", each once per event.
## Step 1c: hearts, spikes, goblins, the stomp, invulnerability, knockback, the
## camera shake, defeat at zero hearts, and every monster back after a death.
## Sounds counted: "hurt" once per heart lost, "stomp" once per goblin stomped.
## Step 1d: the sword-and-shield pickup, the sword form, the slash and its
## reach, the gear knocked away by a hit, and the pickup back after a death.
## Sounds counted: "pickup" once per pickup, "slash" once per swing.
## Step 2a: Rudy's generated frames: every frame in frames.json is in his look
## at the canvas size, drawn with its body origin on his and at 1/density, with
## mipmaps and the outline material; and every pose he took in the checks above
## showed its own frame.
## Step 2b: Level 1's layers and ground: the ground art's walk line is the
## segments' top, each cliff face in the art is where the collision gap starts,
## the tiles meet the cliff pieces at the start of a period, the far layer
## fills the screen everywhere and during the pull-back, and the fields move at
## their share of the camera's motion in the same frame. After the 2b
## playtest, the spikes: each row stands between two tall wheat tufts, and the
## box that hurts covers the row of spikes and stops below the tips.
## Step 2c: the props, the goblin, the hearts and the end card: every sprite is
## drawn at 1/density from its props.json origin, with mipmaps; the outline is
## on the goblins and the spikes only; the goblin walks in two frames facing its
## way and is squashed when defeated; its box fits its art; the waystone's art
## lights; the flying gear is the pickup's art; and the end card's picture
## fades in under the text.
## Step 2d: the title over the opening: the game opens on it with Rudy idle,
## out of control, and the hearts hidden; Enter fades it out and the hearts in,
## and play starts on the same screen; it shows once per run.
## Step 3: the audio. The buses; each of the six sounds plays its own file on
## the SFX bus, and every sound the scripts play has a file (a fall now plays
## "hurt", and the waystone lights without a sound, so the checks above count
## its lights instead); each jump sound plays on the takeoff tick. The music:
## it starts on the title and Enter does not start it again; a hit dips it
## 6 dB for 0.6 s; Esc pauses play, and only play, with the music 12 dB down
## and the sound effects paused; a death dips it 9 dB until he is back in
## control, and neither a respawn nor a start-over starts it again; it fades
## out on the teleport circle, the end card is silent, and playing again starts
## it from the top. M and N mute the buses, even while paused, and with both
## muted the route from the opening runs the same, tick for tick.
## Step 5: every file the game's scenes, resources and scripts name by a res://
## path is in the project, so a fresh copy of the repository has every asset
## the slice uses; and, after my playtest, the debug line is hidden at the start.
## A headless run's audio driver never mixes, so a playing sound never ends or
## moves on: the checks read what the players were told to do, not what is
## heard, and the sounds still registered with the audio server are reported
## as leaked at exit.

const MAIN := preload("res://app/main.tscn")
const REQUIRED_NODES := {
	"res://app/main.tscn": ["Level1", "Rudy", "Camera", "Hud", "Level1/Waystone", "Level1/Portal"],
	"res://content/rudy/rudy.tscn": ["Body", "Look", "SwordHitbox/Shape"],
	"res://content/level_1/level_1.tscn": [
		"Backdrop", "Backdrop/Far/Sky", "PitShade", "Ground/Segment1", "Ground/Segment2",
		"Ground/Segment3", "Hazards/SpikesA", "Hazards/SpikesB", "Enemies/GoblinA", "Enemies/GoblinB",
		"Enemies/GoblinC", "SwordPickup", "Waystone/SpawnPoint", "Portal", "Bounds/Left", "Bounds/Right", "StartPoint",
	],
	"res://content/goblin/goblin.tscn": ["Art", "Shape"],
	"res://content/level_1/spikes.tscn": ["Art", "Shape"],
	"res://content/level_1/waystone.tscn": ["Art", "Shape", "SpawnPoint"],
	"res://content/level_1/portal.tscn": ["Art", "Shape"],
	"res://content/sword_pickup/sword_pickup.tscn": ["Art", "Shape"],
	"res://ui/hud.tscn": [
		"Hearts", "Debug", "Title/Name", "Title/Level", "Title/Hint", "Fade", "EndCard/Picture",
		"EndCard/Lines/Title", "EndCard/Lines/Hint",
	],
}
const CLIFF_LEAD := 100.0 ## the route jumps this far before a cliff's edge
const SPIKES_LEAD := 100.0 ## ...before a row of spikes
const GOBLIN_LEAD := 220.0 ## ...before a live goblin, which may be walking toward him

var _failures := 0
var _main: Main
var _rudy: Rudy
var _camera: Camera2D
var _restart_requests := 0
# What the checks see Rudy do, measured from his motion rather than from Sfx.
var _takeoffs := 0
var _takeoff_ticks: Array[int] = [] # the ticks on which the checks saw a takeoff...
var _jump_sound_ticks: Array[int] = [] # ...and a jump sound
var _tick := 0
var _was_on_floor := true
var _lights := 0 # times the waystone lit
var _trail: Array[StringName] = [] # each pose, once per change
# Every pose Rudy took in all the checks, and any tick his look showed another pose's frame.
var _poses_taken: Dictionary[StringName, bool] = {}
var _frame_mismatches: PackedStringArray = []


func _ready() -> void:
	_check_scenes()
	_start_level()
	await _run_1a()
	await _run_1b()
	await _run_1c()
	await _run_1d()
	_run_2a()
	await _run_2b()
	await _run_2c()
	await _run_2d()
	await _run_3()
	_run_5()
	print("all checks passed" if _failures == 0 else "%d check(s) FAILED" % _failures)
	get_tree().quit(1 if _failures > 0 else 0)


func _physics_process(_delta: float) -> void:
	if not is_instance_valid(_rudy):
		return
	_tick += 1
	var on_floor := _rudy.is_on_floor()
	if _was_on_floor and not on_floor and _rudy.velocity.y < 0.0:
		_takeoffs += 1
		_takeoff_ticks.append(_tick)
	_was_on_floor = on_floor
	if Sfx.count(&"jump") > _jump_sound_ticks.size():
		_jump_sound_ticks.append(_tick)
	if _trail.is_empty() or _trail[-1] != _rudy.pose:
		_trail.append(_rudy.pose)
	_poses_taken[_rudy.pose] = true
	var shown := (_rudy.get_node("Look") as RudyLook).frame()
	if shown != RudyLook.FRAMES.get(_rudy.pose) and _frame_mismatches.size() < 5:
		_frame_mismatches.append("%s showed %s" % [_rudy.pose, shown.resource_path.get_file() if shown else "nothing"])


## A fresh level; without `with_title` it skips the title and starts in play.
func _start_level(with_title := false) -> void:
	Main.title_shown = not with_title
	_main = MAIN.instantiate()
	add_child(_main)
	_main.restart_requested.connect(_on_restart_requested)
	(_main.get_node("Level1/Waystone") as Waystone).activated.connect(func(_w: Waystone) -> void: _lights += 1)
	_rudy = _main.get_node("Rudy")
	_camera = _main.get_node("Camera")
	_was_on_floor = true


func _on_restart_requested() -> void:
	_restart_requests += 1


func _run_1a() -> void:
	# The movement checks run over the spikes and the first goblin; switch them off.
	_set_threats(false)
	var body: CollisionShape2D = _rudy.get_node("Body")
	var capsule := body.shape as CapsuleShape2D
	_check("the capsule is 40 x 136 px with its bottom on the soles",
		capsule.radius == 20.0 and capsule.height == 136.0 and body.position == Vector2(0, -68))

	await _frames(10)
	_check("Rudy starts on the ground at the start point",
		_rudy.is_on_floor() and is_equal_approx(_rudy.global_position.x, 300.0),
		"x %.1f, y %.1f" % [_rudy.global_position.x, _rudy.global_position.y])
	_check("standing still shows CHAR-IDLE", _rudy.pose == &"CHAR-IDLE", _rudy.pose)

	# Run right for two seconds.
	var x0 := _rudy.global_position.x
	_trail.clear()
	Input.action_press(&"move_right")
	await _frames(60)
	var ran := _rudy.global_position.x - x0
	_check("he runs right at about run_speed", ran > 0.9 * _rudy.run_speed and ran <= _rudy.run_speed,
		"%.0f px in 1 s" % ran)
	_check("the run alternates CHAR-RUN-A and CHAR-RUN-B",
		_trail.count(&"CHAR-RUN-A") >= 3 and _trail.count(&"CHAR-RUN-B") >= 3, _trail_text())
	await _frames(60)
	var view := _camera.get_screen_center_position()
	_check("the camera follows him sideways, less than his height behind, and keeps its height",
		absf(view.x - _rudy.global_position.x) < 160.0 and is_equal_approx(view.y, 540.0),
		"view centre %.0f, %.0f; Rudy x %.0f" % [view.x, view.y, _rudy.global_position.x])
	Input.action_release(&"move_right")
	await _frames(15)
	_check("he stops and shows CHAR-IDLE again",
		_rudy.pose == &"CHAR-IDLE" and _rudy.velocity.x == 0.0, _rudy.pose)

	# One tap in place: one takeoff and one jump sound; RISE all the way down, then IDLE on landing.
	_reset_counts()
	var floor_y := _rudy.global_position.y
	# His height after each tick. A key pressed from inside a physics tick, as
	# here, counts from the next tick, so the takeoff is the first tick above 0.
	var heights: Array[float] = []
	Input.action_press(&"jump")
	for i in 90:
		await _frames(1)
		if i == 2:
			Input.action_release(&"jump")
		heights.append(floor_y - _rudy.global_position.y)
	_check("a tap jumps once, with one jump sound", _takeoffs == 1 and Sfx.count(&"jump") == 1, _counts_text())
	_check("a jump in place shows CHAR-RISE all the way down, then CHAR-IDLE",
		_trail == [&"CHAR-IDLE", &"CHAR-RISE", &"CHAR-IDLE"], _trail_text())
	var expected := _expected_jump()
	var takeoff := 0
	while takeoff < heights.size() - 1 and heights[takeoff] <= 0.0:
		takeoff += 1
	var apex: float = heights.max()
	var apex_at := heights.find(apex)
	var landed_at := apex_at
	while landed_at < heights.size() - 1 and heights[landed_at] > 0.01:
		landed_at += 1
	var rise_ticks := apex_at - takeoff + 1
	var fall_ticks := landed_at - apex_at
	_check("the apex matches jump_velocity and gravity", absf(apex - expected.x) < 2.0,
		"%.1f px, expected %.1f" % [apex, expected.x])
	_check("the fall is quicker than the rise, as fall_gravity sets",
		fall_ticks < rise_ticks and absi(rise_ticks - int(expected.y)) <= 1 and absi(fall_ticks - int(expected.z)) <= 1,
		"rise %d ticks, fall %d; expected %d and %d" % [rise_ticks, fall_ticks, int(expected.y), int(expected.z)])
	# The body rests within the physics safe margin (0.08 px) of the ground, so
	# compare to within half a pixel.
	_check("he lands on the ground again", _rudy.is_on_floor() and absf(_rudy.global_position.y - floor_y) < 0.5,
		"on the floor %s, y %.3f, before the jump %.3f" % [_rudy.is_on_floor(), _rudy.global_position.y, floor_y])

	# Holding the key: one jump, and no new jump on landing.
	_reset_counts()
	Input.action_press(&"jump")
	await _frames(100)
	Input.action_release(&"jump")
	await _frames(10)
	_check("holding jump jumps once, not again on landing",
		_takeoffs == 1 and Sfx.count(&"jump") == 1, _counts_text())

	# A second press in the air does nothing.
	_reset_counts()
	await _tap(&"jump")
	await _frames(12)
	await _tap(&"jump")
	await _frames(80)
	_check("a press in the air does not jump", _takeoffs == 1 and Sfx.count(&"jump") == 1, _counts_text())

	# Mashing: every takeoff has exactly one jump sound, and nothing else does.
	_reset_counts()
	for i in 160:
		if i % 2 == 0:
			Input.action_press(&"jump")
		else:
			Input.action_release(&"jump")
		await _frames(1)
	Input.action_release(&"jump")
	await _frames(80)
	_check("mashing jump: one jump sound per takeoff",
		_takeoffs >= 2 and Sfx.count(&"jump") == _takeoffs, _counts_text())
	_check("each jump sound plays on the tick he leaves the ground, not on a press",
		_takeoff_ticks.size() >= 2 and _jump_sound_ticks == _takeoff_ticks,
		"takeoffs on ticks %s, jump sounds on %s" % [_takeoff_ticks, _jump_sound_ticks])

	# On the ground a tap of the other direction turns him in place: neither he
	# nor the camera moves.
	await _frames(90) # let the camera settle
	var look: Node2D = _rudy.get_node("Look")
	var x_still := _rudy.global_position.x
	var view_still := _camera.get_screen_center_position()
	var tick := 1.0 / Engine.physics_ticks_per_second
	Input.action_press(&"move_left")
	await _frames(floori(_rudy.turn_hold_time / tick) - 2)
	Input.action_release(&"move_left")
	await _frames(30)
	var view_moved := _camera.get_screen_center_position().distance_to(view_still)
	_check("a tap of the other direction turns him in place; he and the camera stay put",
		_rudy.facing == -1 and look.scale.x == -1.0
		and absf(_rudy.global_position.x - x_still) < 0.01 and view_moved < 0.5,
		"facing %d, he moved %.2f px, the view %.2f px" % [_rudy.facing, _rudy.global_position.x - x_still, view_moved])

	# Holding the other direction turns him, then moves him after turn_hold_time.
	var held_ticks := 0
	Input.action_press(&"move_right")
	while absf(_rudy.global_position.x - x_still) < 0.01 and held_ticks < 60:
		await _frames(1)
		held_ticks += 1
	_check("holding the other direction moves him after about turn_hold_time",
		_rudy.facing == 1 and absf(held_ticks * tick - _rudy.turn_hold_time) <= 2.0 * tick,
		"he moved after %.3f s; turn_hold_time %.3f s" % [held_ticks * tick, _rudy.turn_hold_time])

	# From a run, the other direction stops him at once, with no slide.
	await _frames(40)
	var x_run := _rudy.global_position.x
	Input.action_release(&"move_right")
	Input.action_press(&"move_left")
	var slid := 0.0
	for i in 5:
		await _frames(1)
		slid = maxf(slid, _rudy.global_position.x - x_run)
	_check("from a run, the other direction stops him at once, with no slide",
		_rudy.facing == -1 and slid < 0.01, "slid %.2f px" % slid)
	await _frames(30)
	_check("holding it then runs him the other way",
		_rudy.velocity.x < 0.0 and _rudy.global_position.x < x_run, "speed %.0f" % _rudy.velocity.x)

	# A running jump comes down in CHAR-FALL. Let go before the top and he drops
	# straight down in CHAR-RISE; either way the pose changes at most once in the air.
	_reset_counts()
	await _tap(&"jump")
	await _wait_until(func() -> bool: return _rudy.is_on_floor(), 90)
	var air := _trail.filter(func(id: StringName) -> bool: return not String(id).begins_with("CHAR-RUN-"))
	_check("a running jump shows CHAR-RISE, then CHAR-FALL", air == [&"CHAR-RISE", &"CHAR-FALL"], _trail_text())
	await _frames(5)
	_reset_counts()
	await _tap(&"jump")
	await _frames(4)
	Input.action_release(&"move_left")
	await _wait_until(func() -> bool: return _rudy.is_on_floor(), 90)
	await _frames(2)
	air = _trail.filter(func(id: StringName) -> bool: return not String(id).begins_with("CHAR-RUN-"))
	_check("letting go before the top: he drops in CHAR-RISE all the way down",
		air == [&"CHAR-RISE", &"CHAR-IDLE"], _trail_text())
	Input.action_release(&"move_left")

	# In the air there is no turning delay: the facing and the speed change at once.
	Input.action_press(&"move_right")
	await _frames(30)
	await _tap(&"jump")
	await _frames(4)
	Input.action_release(&"move_right")
	Input.action_press(&"move_left")
	await _frames(10)
	_check("in the air, the other direction turns him and changes his speed at once",
		not _rudy.is_on_floor() and _rudy.facing == -1 and _rudy.velocity.x < 0.0,
		"speed %.0f" % _rudy.velocity.x)

	# The left bound stops him on the ground.
	await _frames(250)
	Input.action_release(&"move_left")
	await _frames(15)
	_check("the left bound stops him at the edge, on the ground",
		_rudy.global_position.x > 19.0 and _rudy.global_position.x < 21.0 and _rudy.is_on_floor(),
		"x %.1f" % _rudy.global_position.x)
	_check("the camera stops at the level's left edge",
		is_equal_approx(_camera.get_screen_center_position().x, 960.0),
		"view centre x %.1f" % _camera.get_screen_center_position().x)
	_set_threats(true)


func _run_1b() -> void:
	var level: Node2D = _main.get_node("Level1")
	var waystone: Waystone = level.get_node("Waystone")
	var portal: Portal = level.get_node("Portal")
	var start := (level.get_node("StartPoint") as Marker2D).global_position
	var spawn := waystone.spawn_point.global_position
	var gaps := _gaps(level)
	_check("Level 1 has two cliffs, after the waystone and before the teleport circle",
		gaps.size() == 2 and gaps[0].x > spawn.x and gaps[-1].y < portal.global_position.x, str(gaps))

	# A fall before the waystone: one heart, one fall sound, back at the start.
	_reset_counts()
	var hearts_before := _rudy.hearts
	_teleport(Vector2(gaps[0].x - 120.0, start.y)) # past the waystone, without touching it
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 240)
	Input.action_release(&"move_right")
	var hud: Hud = _main.get_node("Hud")
	_check("a fall below a cliff costs one heart, with one hurt sound",
		_main.state == Main.State.DYING and _rudy.mode == Rudy.Mode.FALLEN and Sfx.count(&"hurt") == 1
		and _rudy.hearts == hearts_before - 1 and hud.hearts_shown() == _rudy.hearts,
		"state %s, hurt sounds %d, hearts %d -> %d" % [
			Main.State.keys()[_main.state], Sfx.count(&"hurt"), hearts_before, _rudy.hearts])
	var back_after: int = await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("after a fade he is back at the start, the last checkpoint, in control, with the hearts he had left",
		_main.state == Main.State.PLAYING and _rudy.mode == Rudy.Mode.PLAY
		and _rudy.global_position.distance_to(start) < 1.0 and _rudy.is_on_floor()
		and _rudy.hearts == hearts_before - 1,
		"after %.2f s, at x %.0f, hearts %d" % [back_after / 60.0, _rudy.global_position.x, _rudy.hearts])
	_check("the kill line counted the fall once, though he stayed below it",
		Sfx.count(&"hurt") == 1, "hurt sounds %d" % Sfx.count(&"hurt"))
	_check("he gets back up in CHAR-RESPAWN, then stands in CHAR-IDLE",
		_trail.has(&"CHAR-RESPAWN") and _rudy.pose == &"CHAR-IDLE", _trail_text())
	_check("the camera comes back with him", absf(_camera.get_screen_center_position().x - 960.0) < 1.0,
		"view centre x %.0f" % _camera.get_screen_center_position().x)
	_check("the waystone is still dark", not waystone.lit)

	# The waystone lights once and becomes the checkpoint.
	_reset_counts()
	_teleport(Vector2(waystone.global_position.x - 300.0, start.y))
	await _hold_until(&"move_right", func() -> bool: return _rudy.global_position.x > spawn.x, 120)
	_check("the waystone lights the first time he touches it, and becomes the checkpoint",
		waystone.lit and _lights == 1 and _main.checkpoint_name == "waystone", "lit %d times" % _lights)
	await _hold(&"move_left", 30)
	await _hold(&"move_right", 24)
	_check("crossing it again does not light it again", _lights == 1, "lit %d times" % _lights)

	# A fall after the waystone brings him back at the waystone, one heart fewer.
	_reset_counts()
	hearts_before = _rudy.hearts
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 240)
	Input.action_release(&"move_right")
	await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("after a fall past the waystone he gets back up at the waystone, one heart fewer",
		_rudy.global_position.distance_to(spawn) < 1.0 and Sfx.count(&"hurt") == 1
		and _rudy.hearts == hearts_before - 1,
		"at x %.0f, spawn x %.0f; hearts %d -> %d" % [_rudy.global_position.x, spawn.x, hearts_before, _rudy.hearts])

	# From the waystone, over both cliffs, onto the teleport circle.
	_reset_counts()
	var route_ticks: int = await _run_route(gaps, 900)
	_check("from the waystone he clears both cliffs and reaches the teleport circle, unhurt",
		route_ticks > 0 and _main.state == Main.State.COMPLETE and Sfx.count(&"hurt") == 0,
		"state %s, hurt sounds %d" % [Main.State.keys()[_main.state], Sfx.count(&"hurt")])
	await _frames(2) # his pose follows on his next tick
	_check("the circle completes the level once: one portal sound; he celebrates",
		Sfx.count(&"portal") == 1 and _rudy.mode == Rudy.Mode.CELEBRATING and _rudy.pose == &"CHAR-CELEBRATE",
		"portal sounds %d, pose %s" % [Sfx.count(&"portal"), _rudy.pose])
	await _frames(20) # let him come to a stop
	var x_done := _rudy.global_position.x
	await _hold(&"move_left", 30)
	await _tap(&"jump")
	await _frames(20)
	_check("input stops on the circle", absf(_rudy.global_position.x - x_done) < 0.01 and _rudy.is_on_floor(),
		"moved %.2f px" % (_rudy.global_position.x - x_done))
	var card_after: int = await _wait_until(func() -> bool: return hud.is_showing_end_card(), 300)
	_check("the camera pulls back and the screen fades to the end card",
		hud.is_showing_end_card() and _camera.zoom.is_equal_approx(Main.END_ZOOM),
		"after %.2f s more; zoom %.2f" % [card_after / 60.0, _camera.zoom.x])
	portal.reached.emit() # as if he stepped onto the circle again
	await _frames(2)
	_check("stepping onto the circle again does not complete the level again", Sfx.count(&"portal") == 1,
		"portal sounds %d" % Sfx.count(&"portal"))
	await _tap(&"restart")
	await _frames(5)
	_check("Enter on the end card plays the level again", _restart_requests == 1,
		"restart requests %d" % _restart_requests)

	# A fresh level from the opening, the way Enter starts it: the whole route, timed.
	_main.queue_free()
	await _frames(1)
	_start_level()
	_reset_counts()
	await _frames(5)
	var fresh_waystone: Waystone = _main.get_node("Level1/Waystone")
	_check("the level starts again at the opening, with the waystone dark",
		_main.state == Main.State.PLAYING and not fresh_waystone.lit
		and _rudy.global_position.distance_to(start) < 1.0)
	route_ticks = await _run_route(gaps, 1800)
	_check("a clean route from the opening reaches the circle: the waystone lights once; no falls, no hits",
		route_ticks > 0 and _lights == 1 and Sfx.count(&"portal") == 1 and Sfx.count(&"hurt") == 0,
		"%.1f s from the opening at full speed, jumping the cliffs, spikes and goblins; hurt sounds %d" % [
			route_ticks / 60.0, Sfx.count(&"hurt")])

	# How forgiving the widest cliff is, measured: full-speed takeoffs every 5 px
	# from 300 px before its edge to 40 px past it, on a fresh level.
	_main.queue_free()
	await _frames(1)
	_start_level()
	await _frames(5)
	var widest := gaps[0]
	for gap in gaps:
		if gap.y - gap.x > widest.y - widest.x:
			widest = gap
	var window := await _takeoff_window(widest)
	var window_s := (window.y - window.x) / _rudy.run_speed
	_check("the widest cliff can be cleared by full-speed takeoffs spread over at least 0.3 s",
		window_s >= 0.3,
		"takeoffs from %s to %s clear it: %.0f px, %.2f s of running" % [
			_from_edge(window.x), _from_edge(window.y), window.y - window.x, window_s])


func _run_1c() -> void:
	_main.queue_free()
	await _frames(1)
	_start_level()
	await _frames(5)
	var level: Node2D = _main.get_node("Level1")
	var hud: Hud = _main.get_node("Hud")
	var look: Node2D = _rudy.get_node("Look")
	var spikes: Spikes = level.get_node("Hazards/SpikesA")
	var goblin_a: Goblin = level.get_node("Enemies/GoblinA")
	var goblin_b: Goblin = level.get_node("Enemies/GoblinB")
	var goblin_c: Goblin = level.get_node("Enemies/GoblinC")
	var goblins: Array[Goblin] = [goblin_a, goblin_b, goblin_c]
	var start := (level.get_node("StartPoint") as Marker2D).global_position
	var ground_y := start.y
	_check("Rudy starts with three hearts, and the HUD shows three",
		_rudy.hearts == 3 and hud.hearts_shown() == 3, "hearts %d, shown %d" % [_rudy.hearts, hud.hearts_shown()])

	# Spikes: one heart, one hurt sound, a knockback, a shake and a flash.
	_reset_counts()
	_teleport(Vector2(spikes.global_position.x - 220.0, ground_y))
	await _frames(2)
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.hearts < 3, 120)
	Input.action_release(&"move_right")
	var hit_x := _rudy.global_position.x
	_check("touching the spikes costs one heart, with one hurt sound; the HUD shows two",
		_rudy.hearts == 2 and Sfx.count(&"hurt") == 1 and hud.hearts_shown() == 2,
		"hearts %d, hurt sounds %d, shown %d" % [_rudy.hearts, Sfx.count(&"hurt"), hud.hearts_shown()])
	_check("the hit knocks him back, away from the spikes, and turns him toward them",
		_rudy.mode == Rudy.Mode.HURT and _rudy.velocity.x < 0.0 and _rudy.facing == 1,
		"mode %s, speed %.0f, facing %d" % [Rudy.Mode.keys()[_rudy.mode], _rudy.velocity.x, _rudy.facing])
	await _frames(2)
	_check("he shows CHAR-HURT, and the camera shakes",
		_rudy.pose == &"CHAR-HURT" and _camera.offset != Vector2.ZERO,
		"pose %s, camera offset %s" % [_rudy.pose, _camera.offset])
	var alphas := {}
	for i in 24:
		await _frames(1)
		alphas[snappedf(look.modulate.a, 0.01)] = true
	_check("he flashes while he is invulnerable", alphas.size() == 2 and _rudy.is_invulnerable(),
		"alphas seen %s" % str(alphas.keys()))
	_check("the camera shake is over after 0.2 s", _camera.offset == Vector2.ZERO, str(_camera.offset))
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY, 60)
	_check("control returns after the knockback", _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(),
		"knocked back %.0f px" % (hit_x - _rudy.global_position.x))

	# The spikes and a goblin at once: one heart, one hurt sound.
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	goblin_a.speed = 0.0
	goblin_a.position.x = spikes.global_position.x + 50.0 # outside its patrol, until a reset
	_reset_counts()
	_teleport(Vector2(spikes.global_position.x + 40.0, ground_y))
	await _frames(3)
	_check("touching the spikes and a goblin at once costs one heart, with one hurt sound",
		_rudy.hearts == 1 and Sfx.count(&"hurt") == 1, "hearts %d, hurt sounds %d" % [_rudy.hearts, Sfx.count(&"hurt")])

	# Standing on the spikes: nothing while he is invulnerable, then his last heart goes.
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 60)
	_teleport(Vector2(spikes.global_position.x - 30.0, ground_y))
	var hit_while_invulnerable := false
	while _rudy.is_invulnerable():
		await _frames(1)
		if Sfx.count(&"hurt") != 1:
			hit_while_invulnerable = true
			break
	await _frames(3)
	_check("standing on the spikes hurts again only once his invulnerability is over",
		not hit_while_invulnerable and Sfx.count(&"hurt") == 2, "hurt sounds %d" % Sfx.count(&"hurt"))
	_check("with his last heart gone he is defeated (CHAR-DEFEAT), and the level is dying; no fall",
		_rudy.hearts == 0 and _rudy.mode == Rudy.Mode.DEFEATED and _rudy.pose == &"CHAR-DEFEAT"
		and _main.state == Main.State.DYING,
		"hearts %d, pose %s, state %s" % [_rudy.hearts, _rudy.pose, Main.State.keys()[_main.state]])
	var back_after: int = await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("after the fade the level starts over: he is at the start with three hearts, flashing",
		_rudy.global_position.distance_to(start) < 1.0 and _rudy.hearts == 3 and hud.hearts_shown() == 3
		and _rudy.is_invulnerable(),
		"after %.2f s; hearts %d" % [back_after / 60.0, _rudy.hearts])
	_check("the goblin that was moved is back in its patrol",
		not goblin_a.dead and goblin_a.position.x >= 1500.0 and goblin_a.position.x <= 1500.0 + goblin_a.patrol_distance,
		"x %.0f" % goblin_a.position.x)
	goblin_a.speed = 100.0

	# Landing on a goblin from above: one stomp sound, no hit, and a bounce.
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	_reset_counts()
	_teleport(Vector2(goblin_a.global_position.x, ground_y - Goblin.HEIGHT - 60.0))
	_rudy.velocity = Vector2(0, 200)
	await _frames(1) # is_on_floor() is stale until his next move
	await _wait_until(func() -> bool: return goblin_a.dead or _rudy.is_on_floor(), 60)
	await _frames(2)
	_check("landing on a goblin from above defeats it, with one stomp sound and no hit",
		goblin_a.dead and Sfx.count(&"stomp") == 1 and Sfx.count(&"hurt") == 0 and _rudy.hearts == 3,
		"stomp sounds %d, hurt sounds %d" % [Sfx.count(&"stomp"), Sfx.count(&"hurt")])
	_check("the stomp bounces him up", _rudy.velocity.y < 0.0 and not _rudy.is_on_floor(),
		"speed y %.0f" % _rudy.velocity.y)
	await _frames(60)
	_check("a defeated goblin ignores him when he comes down on it again, then disappears",
		Sfx.count(&"hurt") == 0 and Sfx.count(&"stomp") == 1 and not goblin_a.visible)

	# Walking into a goblin: a heart, a knockback away from it, and it stays.
	await _wait_until(func() -> bool:
		return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable(), 120)
	_reset_counts()
	_teleport(Vector2(goblin_b.global_position.x - 250.0, ground_y))
	await _frames(2)
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.hearts < 3, 120)
	Input.action_release(&"move_right")
	_check("walking into a goblin costs a heart and knocks him back from it; the goblin stays",
		_rudy.hearts == 2 and Sfx.count(&"hurt") == 1 and Sfx.count(&"stomp") == 0
		and _rudy.velocity.x < 0.0 and not goblin_b.dead,
		"hearts %d, speed %.0f" % [_rudy.hearts, _rudy.velocity.x])

	# Landing on two goblins in the same tick: two stomp sounds, no hit.
	await _wait_until(func() -> bool:
		return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable(), 120)
	for goblin: Goblin in [goblin_b, goblin_c]:
		goblin.speed = 0.0
	goblin_b.position.x = 2200.0 # clear of the spikes, the first patrol and the pickup
	goblin_c.position.x = 2240.0
	_reset_counts()
	_teleport(Vector2(2220.0, ground_y - Goblin.HEIGHT - 60.0))
	_rudy.velocity = Vector2(0, 200)
	await _frames(1) # is_on_floor() is stale until his next move
	await _wait_until(func() -> bool: return goblin_b.dead or goblin_c.dead or _rudy.is_on_floor(), 60)
	await _frames(2)
	_check("landing on two goblins in the same tick: two stomp sounds, no hit",
		goblin_b.dead and goblin_c.dead and Sfx.count(&"stomp") == 2 and Sfx.count(&"hurt") == 0,
		"stomp sounds %d, hurt sounds %d" % [Sfx.count(&"stomp"), Sfx.count(&"hurt")])
	for goblin: Goblin in [goblin_b, goblin_c]:
		goblin.speed = 100.0

	# A fall: every goblin comes back, and it costs a heart.
	await _frames(30)
	var hearts_before := _rudy.hearts
	_teleport(Vector2(4400.0, 700.0)) # over the first cliff, past the waystone without touching it
	await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 120)
	await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	var back := PackedStringArray()
	for goblin in goblins:
		if not goblin.dead and goblin.visible:
			back.append(goblin.name)
	_check("after a death every goblin is back, the defeated ones too", back.size() == goblins.size(),
		"back: %s" % ", ".join(back))
	var homes: Array[float] = [1500.0, 3000.0, 5600.0] # where level_1.tscn starts them
	var in_patrol := true
	for i in goblins.size():
		var x := goblins[i].position.x
		if x < homes[i] or x > homes[i] + goblins[i].patrol_distance:
			in_patrol = false
	_check("each goblin is back in its own patrol", in_patrol,
		"x %.0f, %.0f, %.0f" % [goblin_a.position.x, goblin_b.position.x, goblin_c.position.x])
	_check("a fall costs a heart and does not refill the others",
		hearts_before == 2 and _rudy.hearts == 1 and hud.hearts_shown() == 1,
		"hearts before %d, after %d" % [hearts_before, _rudy.hearts])

	# A stomp at full falling speed: from the top of a jump onto a goblin.
	await _wait_until(func() -> bool:
		return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable(), 120)
	goblin_a.speed = 0.0
	_reset_counts()
	var apex := _expected_jump().x
	_teleport(Vector2(goblin_a.global_position.x, ground_y - apex))
	await _frames(1)
	var landing_speed := 0.0
	for i in 60:
		landing_speed = _rudy.velocity.y
		await _frames(1)
		if goblin_a.dead or _rudy.is_on_floor():
			break
	_check("falling from the top of a jump onto a goblin still counts as a stomp, not a hit",
		goblin_a.dead and Sfx.count(&"stomp") == 1 and Sfx.count(&"hurt") == 0,
		"falling at %.0f px/s; stomp sounds %d, hurt sounds %d" % [landing_speed, Sfx.count(&"stomp"), Sfx.count(&"hurt")])
	goblin_a.speed = 100.0

	# A fall that takes his last heart starts the level over from the opening,
	# even after the waystone was lit.
	var waystone: Waystone = level.get_node("Waystone")
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 120)
	_teleport(Vector2(waystone.global_position.x - 200.0, ground_y))
	await _frames(2)
	await _hold_until(&"move_right", func() -> bool:
		return _rudy.global_position.x > waystone.spawn_point.global_position.x, 120)
	var lit_before := waystone.lit and _main.checkpoint_name == "waystone"
	_reset_counts()
	hearts_before = _rudy.hearts
	_teleport(Vector2(4400.0, 700.0))
	await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 120)
	var hearts_at_fall := _rudy.hearts
	await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("a fall that takes his last heart starts the level over: at the start, three hearts, the waystone dark",
		lit_before and hearts_before == 1 and hearts_at_fall == 0
		and _rudy.global_position.distance_to(start) < 1.0 and _rudy.hearts == 3 and hud.hearts_shown() == 3
		and not waystone.lit and _main.checkpoint_name == "start"
		and Sfx.count(&"hurt") == 1,
		"waystone lit before %s; hearts %d -> %d at the fall -> %d; at x %.0f; waystone lit now %s" % [
			lit_before, hearts_before, hearts_at_fall, _rudy.hearts, _rudy.global_position.x, waystone.lit])
	var all_alive := true
	for goblin in goblins:
		all_alive = all_alive and not goblin.dead and goblin.visible
	_check("starting over brings every goblin back", all_alive)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 120)
	_teleport(Vector2(waystone.global_position.x - 200.0, ground_y))
	await _frames(2)
	await _hold_until(&"move_right", func() -> bool:
		return _rudy.global_position.x > waystone.spawn_point.global_position.x, 120)
	_check("after starting over, the waystone lights again", waystone.lit and _lights == 1, "lit %d times" % _lights)

	# Hits that take his last heart start the level over too, even after the waystone.
	var spikes_b: Spikes = level.get_node("Hazards/SpikesB")
	_reset_counts()
	for i in 3:
		await _wait_until(func() -> bool:
			return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable(), 120)
		var hearts_now := _rudy.hearts
		_teleport(Vector2(spikes_b.global_position.x, ground_y))
		await _wait_until(func() -> bool: return _rudy.hearts < hearts_now, 30)
	var defeated := _main.state == Main.State.DYING and _rudy.mode == Rudy.Mode.DEFEATED and Sfx.count(&"hurt") == 3
	await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("hits that take his last heart start the level over too: at the start, three hearts, the waystone dark",
		defeated and _rudy.global_position.distance_to(start) < 1.0 and _rudy.hearts == 3
		and not waystone.lit and _main.checkpoint_name == "start",
		"defeated %s; at x %.0f; hearts %d; waystone lit %s" % [defeated, _rudy.global_position.x, _rudy.hearts, waystone.lit])


func _run_1d() -> void:
	_main.queue_free()
	await _frames(1)
	_start_level()
	await _frames(5)
	var level: Node2D = _main.get_node("Level1")
	var pickup: SwordPickup = level.get_node("SwordPickup")
	var spikes: Spikes = level.get_node("Hazards/SpikesA")
	var goblin_b: Goblin = level.get_node("Enemies/GoblinB")
	var goblin_c: Goblin = level.get_node("Enemies/GoblinC")
	var start := (level.get_node("StartPoint") as Marker2D).global_position
	var ground_y := start.y
	_check("Rudy starts without gear, in the default form",
		_rudy.gear == Rudy.Gear.NONE and _rudy.pose == &"CHAR-IDLE", _rudy.pose)

	# Without the sword, slash does nothing.
	_reset_counts()
	await _tap(&"slash")
	await _frames(20)
	_check("without the sword, slash does nothing", Sfx.count(&"slash") == 0 and not _rudy.is_slashing())

	# The pickup: the sword form, one pickup sound, and it is gone.
	_reset_counts()
	_teleport(Vector2(pickup.global_position.x - 200.0, ground_y))
	await _frames(2)
	await _hold_until(&"move_right", func() -> bool: return _rudy.gear == Rudy.Gear.SWORD, 120)
	await _frames(2)
	_check("touching the pickup gives him the sword and shield, with one pickup sound; it disappears",
		_rudy.gear == Rudy.Gear.SWORD and Sfx.count(&"pickup") == 1 and pickup.taken and not pickup.visible,
		"pickup sounds %d" % Sfx.count(&"pickup"))
	_check("with the sword he shows the sword form's poses", String(_rudy.pose).begins_with("CHAR-SWORD-"), _rudy.pose)
	await _hold(&"move_left", 40)
	await _hold(&"move_right", 40)
	_check("crossing the pickup's place again gives nothing more", Sfx.count(&"pickup") == 1)

	# One tap: one swing and one slash sound; the swing ends after slash_time.
	await _wait_until(func() -> bool: return _rudy.is_on_floor() and _rudy.velocity.x == 0.0, 60)
	_reset_counts()
	await _tap(&"slash")
	_check("a tap swings the sword once (CHAR-SWORD-SLASH), with one slash sound",
		Sfx.count(&"slash") == 1 and _rudy.pose == &"CHAR-SWORD-SLASH", "pose %s" % _rudy.pose)
	var swing_ticks: int = await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	await _frames(1)
	_check("the swing ends after about slash_time, back in CHAR-SWORD-IDLE",
		_rudy.pose == &"CHAR-SWORD-IDLE" and absf((swing_ticks + 2) / 60.0 - _rudy.slash_time) <= 2.0 / 60.0,
		"%.2f s; pose %s" % [(swing_ticks + 2) / 60.0, _rudy.pose])

	# Holding the key: one swing. Mashing it: one sound per swing.
	_reset_counts()
	await _hold(&"slash", 60)
	await _frames(30)
	_check("holding slash swings once", Sfx.count(&"slash") == 1, "slash sounds %d" % Sfx.count(&"slash"))
	_reset_counts()
	var swings := 0
	var was_slashing := false
	for i in 120:
		if i % 2 == 0:
			Input.action_press(&"slash")
		else:
			Input.action_release(&"slash")
		await _frames(1)
		if _rudy.is_slashing() and not was_slashing:
			swings += 1
		was_slashing = _rudy.is_slashing()
	Input.action_release(&"slash")
	await _frames(30)
	_check("mashing slash: one slash sound per swing, and no swing starts during another",
		swings >= 3 and Sfx.count(&"slash") == swings and swings <= ceili(2.0 / _rudy.slash_time),
		"%d swings in 2 s, slash sounds %d" % [swings, Sfx.count(&"slash")])

	# A cut in reach defeats a goblin in one hit: no stomp sound, no hit.
	goblin_b.speed = 0.0
	goblin_c.speed = 0.0
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and not _rudy.is_slashing(), 60)
	_reset_counts()
	_teleport(Vector2(goblin_b.global_position.x - 70.0, ground_y))
	await _frames(2)
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	_check("a cut in reach defeats a goblin in one hit, with no stomp sound and no hit",
		goblin_b.dead and Sfx.count(&"stomp") == 0 and Sfx.count(&"hurt") == 0 and Sfx.count(&"slash") == 1,
		"dead %s; stomp %d, hurt %d" % [goblin_b.dead, Sfx.count(&"stomp"), Sfx.count(&"hurt")])

	# The cut reaches only in front of him, and only so far.
	_teleport(Vector2(goblin_c.global_position.x + 70.0, ground_y)) # the goblin behind him
	await _frames(2)
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	var behind_alive := not goblin_c.dead
	_teleport(Vector2(goblin_c.global_position.x - 150.0, ground_y)) # in front, out of reach
	await _frames(2)
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	_check("a cut misses a goblin behind him, and one 150 px ahead", behind_alive and not goblin_c.dead)
	_teleport(Vector2(goblin_c.global_position.x + 70.0, ground_y))
	await _frames(2)
	await _tap(&"move_left") # a tap turns him on the spot
	await _frames(2)
	await _tap(&"slash")
	await _wait_until(func() -> bool: return not _rudy.is_slashing(), 60)
	_check("turned around, the cut reaches the goblin that was behind him", _rudy.facing == -1 and goblin_c.dead,
		"facing %d, dead %s" % [_rudy.facing, goblin_c.dead])
	goblin_b.speed = 100.0
	goblin_c.speed = 100.0

	# A hit while he carries the gear: it flies off instead of a heart.
	await _wait_until(func() -> bool:
		return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor() and not _rudy.is_invulnerable(), 120)
	var hearts_before := _rudy.hearts
	_reset_counts()
	_teleport(Vector2(spikes.global_position.x - 220.0, ground_y))
	await _frames(2)
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.gear == Rudy.Gear.NONE, 120)
	Input.action_release(&"move_right")
	var flying := 0
	for child in _main.get_children():
		if child is FlyingGear:
			flying += 1
	_check("a hit while he carries the gear knocks it away instead of a heart, with one hurt sound",
		_rudy.gear == Rudy.Gear.NONE and _rudy.hearts == hearts_before and Sfx.count(&"hurt") == 1
		and _rudy.mode == Rudy.Mode.HURT,
		"hearts %d -> %d, hurt sounds %d" % [hearts_before, _rudy.hearts, Sfx.count(&"hurt")])
	_check("the sword and shield fly off", flying == 1, "%d flying" % flying)
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY, 60)
	await _frames(40)
	flying = 0
	for child in _main.get_children():
		if child is FlyingGear:
			flying += 1
	_check("they fade and are gone; he is back in the default form; the pickup stays away",
		flying == 0 and not String(_rudy.pose).begins_with("CHAR-SWORD-") and not pickup.visible,
		"%d flying, pose %s" % [flying, _rudy.pose])

	# Without the gear, the next hit costs a heart.
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	_teleport(Vector2(spikes.global_position.x, ground_y))
	await _wait_until(func() -> bool: return _rudy.hearts < hearts_before, 30)
	_check("without the gear, the next hit costs a heart", _rudy.hearts == hearts_before - 1 and Sfx.count(&"hurt") == 2)

	# A death brings the pickup back, and he gets back up without gear.
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 120)
	_teleport(Vector2(4400.0, 700.0)) # a fall over the first cliff, past the waystone
	await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 120)
	await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("after a death the pickup is back where it was", pickup.visible and not pickup.taken)
	_reset_counts()
	_teleport(Vector2(pickup.global_position.x - 200.0, ground_y))
	await _frames(2)
	await _hold_until(&"move_right", func() -> bool: return _rudy.gear == Rudy.Gear.SWORD, 120)
	var had_sword := _rudy.gear == Rudy.Gear.SWORD and Sfx.count(&"pickup") == 1
	await _wait_until(func() -> bool: return _rudy.is_on_floor(), 60)
	_teleport(Vector2(4400.0, 700.0)) # his last heart: the level starts over
	await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 120)
	await _wait_until(func() -> bool: return _main.state == Main.State.PLAYING, 300)
	_check("he gets back up without gear, even when he fell with it, and the pickup is back",
		had_sword and _rudy.gear == Rudy.Gear.NONE and pickup.visible and _rudy.pose == &"CHAR-IDLE",
		"had the sword %s; gear %s; pose %s" % [had_sword, Rudy.Gear.keys()[_rudy.gear], _rudy.pose])


func _run_2a() -> void:
	var manifest: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://content/rudy/frames/frames.json"))
	var canvas := Vector2(manifest.canvas[0], manifest.canvas[1])
	var origin := Vector2(manifest.origin[0], manifest.origin[1])
	var density: float = manifest.density
	var problems: PackedStringArray = []
	for id: String in manifest.frames:
		var frame: Texture2D = RudyLook.FRAMES.get(StringName(id))
		if frame == null:
			problems.append("%s missing" % id)
		elif Vector2(frame.get_size()) != canvas:
			problems.append("%s is %s" % [id, frame.get_size()])
		elif not FileAccess.get_file_as_string(frame.resource_path + ".import").contains("mipmaps/generate=true"):
			problems.append("%s has no mipmaps" % id)
	_check("every frame in frames.json is in Rudy's look, at the canvas size, with mipmaps",
		problems.is_empty() and RudyLook.FRAMES.size() == manifest.frames.size(), ", ".join(problems))

	var look: RudyLook = _rudy.get_node("Look")
	var sprite: Sprite2D = look.get_node("Sprite")
	_check("each frame is drawn at 1/density with its body origin on Rudy's origin (his soles)",
		not sprite.centered and sprite.position == Vector2.ZERO and sprite.offset == -origin
		and sprite.scale == Vector2.ONE / density,
		"offset %s, scale %s; frames.json origin %s, density %s" % [sprite.offset, sprite.scale, origin, density])
	var material := sprite.material as ShaderMaterial
	_check("the frames draw with linear mipmap filtering and the 4 px outline",
		look.texture_filter == CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
		and sprite.texture_filter == CanvasItem.TEXTURE_FILTER_PARENT_NODE
		and material != null and material.shader.resource_path == "res://systems/art/outline.gdshader"
		and is_equal_approx(material.get_shader_parameter(&"width"), 4.0 * density),
		"filter %d, width %s" % [look.texture_filter, material.get_shader_parameter(&"width") if material else null])

	# Every pose the controller can pick: every frame but the block, which waits for step 4.
	var not_taken: PackedStringArray = []
	for id: StringName in RudyLook.FRAMES:
		if id != &"CHAR-SWORD-BLOCK" and not _poses_taken.has(id):
			not_taken.append(id)
	_check("every pose he took in the checks showed its own frame, and he took all fifteen",
		_frame_mismatches.is_empty() and not_taken.is_empty(),
		"; ".join(_frame_mismatches) + ("" if not_taken.is_empty() else " not taken: " + ", ".join(not_taken)))


func _run_2b() -> void:
	_main.queue_free()
	await _frames(1)
	_start_level()
	await _frames(5)
	_set_threats(false)
	var level: Node2D = _main.get_node("Level1")
	var env: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://content/level_1/art/env.json"))
	var tile: Dictionary = env.layers.ground_tile
	var right: Dictionary = env.layers.ground_cliff_right
	var left: Dictionary = env.layers.ground_cliff_left
	var segments: Array[GroundSegment] = []
	for node in level.get_node("Ground").get_children():
		segments.append(node as GroundSegment)
	var on_line := segments.all(func(seg: GroundSegment) -> bool: return seg.position.y == env.ground_y)
	_check("the ground art's walk line is the segments' top, as env.json gives it",
		on_line and tile.y - env.ground_y == GroundSegment.ART_TOP
		and tile.walk_row_texture_px / tile.density == -GroundSegment.ART_TOP
		and tile.density == GroundSegment.DENSITY and tile.size[0] == GroundSegment.TILE_WIDTH
		and right.size[0] == GroundSegment.CLIFF_WIDTH and right.cliff_edge_game_px == GroundSegment.CLIFF_FACE
		and left.cliff_edge_game_px == GroundSegment.CLIFF_WIDTH - GroundSegment.CLIFF_FACE,
		"art top %.1f, walk row %.1f px below it" % [tile.y - env.ground_y, tile.walk_row_texture_px / tile.density])

	# The cliff faces, measured in the art as prepare_env.py does: the outermost
	# opaque column 40 px or more below the walk line.
	var below := int(tile.walk_row_texture_px) + 40 * int(tile.density)
	var right_face: float = _opaque_columns("res://content/level_1/art/ground_cliff_right.png", below).y / tile.density
	var left_face: float = _opaque_columns("res://content/level_1/art/ground_cliff_left.png", below).x / tile.density
	var faces: PackedStringArray = []
	var off := 0.0
	for seg in segments:
		if seg.cliff_right:
			var art: float = seg.position.x + seg.size.x - GroundSegment.CLIFF_FACE + right_face
			off = maxf(off, absf(art - (seg.position.x + seg.size.x)))
			faces.append("%s right: art %.1f, collision %.0f" % [seg.name, art, seg.position.x + seg.size.x])
		if seg.cliff_left:
			var art: float = seg.position.x + GroundSegment.CLIFF_FACE - GroundSegment.CLIFF_WIDTH + left_face
			off = maxf(off, absf(art - seg.position.x))
			faces.append("%s left: art %.1f, collision %.0f" % [seg.name, art, seg.position.x])
	_check("each cliff face in the art is where the collision gap starts, within 1 px",
		faces.size() == 4 and off <= 1.0, "; ".join(faces))

	var runs: PackedStringArray = []
	var runs_ok := true
	for seg in segments:
		var run := seg.tile_run()
		var start: float = run.from
		var end: float = run.from + run.count * run.period
		var need_from := GroundSegment.CLIFF_FACE if seg.cliff_left else 0.0
		var need_to := seg.size.x - GroundSegment.CLIFF_FACE if seg.cliff_right else seg.size.x
		runs_ok = runs_ok and start <= need_from + 0.01 and end >= need_to - 0.01
		runs_ok = runs_ok and (not seg.cliff_left or is_equal_approx(start, need_from))
		runs_ok = runs_ok and (not seg.cliff_right or is_equal_approx(end, need_to))
		runs.append("%s: %d tiles of %.1f px (%+.1f%%) from %.1f" % [seg.name, run.count, run.period,
			(run.period / GroundSegment.TILE_WIDTH - 1.0) * 100.0, seg.position.x + start])
	var first := segments[0].tile_run()
	var last := segments[-1].tile_run()
	var level_end := (level.get_node("Bounds/Right") as Node2D).global_position.x
	runs_ok = runs_ok and segments[0].position.x + first.from <= -Main.SHAKE_PX
	runs_ok = runs_ok and segments[-1].position.x + last.from + last.count * last.period >= level_end + Main.SHAKE_PX
	runs_ok = runs_ok and segments.all(func(seg: GroundSegment) -> bool:
		return absf(seg.tile_run().period / GroundSegment.TILE_WIDTH - 1.0) <= 0.035)
	_check("the tiles meet each cliff piece at the start of a period, cover the level past a shake, and stretch by 3.5% at most",
		runs_ok, "; ".join(runs))

	# The far layer and the fields, with the camera at points along the level.
	var backdrop: Backdrop = level.get_node("Backdrop")
	var sky: Sprite2D = level.get_node("Backdrop/Far/Sky")
	var gaps_seen: PackedStringArray = []
	var sky_xs: Array[float] = []
	for x: float in [300.0, 1500.0, 3000.0, 4200.0, 4700.0, 5500.0, 6300.0, 6900.0, 7650.0]:
		_teleport(Vector2(x, 840.0))
		_main._snap_camera()
		await _drawn()
		sky_xs.append(sky.position.x)
		var gap := _backdrop_gap(backdrop, sky)
		if not gap.is_empty():
			gaps_seen.append("at x %d: %s" % [x, gap])
	_check("the far layer and the fields fill the screen along the level, and the far layer scrolls its spare width",
		gaps_seen.is_empty() and sky_xs[0] == 0.0 and absf(sky_xs[-1] + (sky.texture.get_width() - 1920.0)) < 1.0,
		"; ".join(gaps_seen) + " far layer x from %.1f to %.1f" % [sky_xs[0], sky_xs[-1]])

	# The fields move with the camera in the same frame, at their share of its motion.
	_teleport(Vector2(600.0, 840.0))
	_main._snap_camera()
	await _drawn()
	var worst := 0.0
	Input.action_press(&"move_right")
	for i in 60:
		await get_tree().process_frame
		worst = maxf(worst, absf(backdrop.position.x - backdrop.view_left_x() * (1.0 - Backdrop.FIELDS_MOTION)))
	Input.action_release(&"move_right")
	_check("while he runs, the fields move at %.1f of the camera in the same frame, with no lag" % Backdrop.FIELDS_MOTION,
		worst < 0.01, "worst %.2f px" % worst)

	# The pull-back on the teleport circle.
	var portal: Portal = level.get_node("Portal")
	_teleport(Vector2(portal.global_position.x - 300.0, 840.0))
	_main._snap_camera()
	await _hold_until(&"move_right", func() -> bool: return _main.state == Main.State.COMPLETE, 120)
	await _frames(roundi(Main.ZOOM_TIME * Engine.physics_ticks_per_second) + 5)
	await _drawn()
	var gap := _backdrop_gap(backdrop, sky)
	_check("pulled back on the teleport circle, the far layer and the fields still fill the screen",
		is_equal_approx(_camera.zoom.x, Main.END_ZOOM.x) and gap.is_empty(), "zoom %.2f %s" % [_camera.zoom.x, gap])
	_set_threats(true)

	# The spikes: no tall wheat tuft behind a row, and the box inside the row of spikes.
	var tufts := _tall_tufts(segments)
	var crowded: PackedStringArray = []
	var rows: PackedStringArray = []
	for spikes: Spikes in level.get_node("Hazards").get_children():
		var x := spikes.global_position.x
		rows.append("%s at %d" % [spikes.name, x])
		for tuft in tufts:
			if tuft.y > x - 53.0 and tuft.x < x + 53.0:
				crowded.append("%s at %d: tuft %d to %d" % [spikes.name, x, tuft.x, tuft.y])
	_check("no tall wheat tuft stands behind a row of spikes", crowded.is_empty() and rows.size() == 2,
		"; ".join(crowded) if not crowded.is_empty() else ", ".join(rows))
	var art := _spikes_art()
	var box := ((level.get_node("Hazards/SpikesA/Shape") as CollisionShape2D).shape as RectangleShape2D).size
	_check("the spikes' box covers the row of spikes, from the plank to below the tips",
		box.x == Spikes.WIDTH and absf(box.x - art.x) <= 2.0 and box.y < art.y - 8.0 and box.y > art.z,
		"box %s; in the art the row is %.1f px wide, the tips %.1f px up, the plank %.1f px" % [box, art.x, art.y, art.z])


func _run_2c() -> void:
	_main.queue_free()
	await _frames(1)
	_start_level()
	await _frames(5)
	var level: Node2D = _main.get_node("Level1")
	var props: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://content/level_1/art/props.json")).frames
	var placed := {
		"Hazards/SpikesA/Art": "ENV-SPIKES", "Hazards/SpikesB/Art": "ENV-SPIKES", "Waystone/Art": "ENV-WAYSTONE",
		"Portal/Art": "ENV-PORTAL", "SwordPickup/Art": "PROP-SWORDSHIELD", "Enemies/GoblinA/Art": "ENEMY-GOBLIN-WALK-A",
	}
	var problems: PackedStringArray = []
	for path: String in placed:
		var frame: Dictionary = props[placed[path]]
		var sprite: Sprite2D = level.get_node(path)
		var size: float = SwordPickup.SCALE if path.begins_with("SwordPickup") else 1.0 # the pickup is shown larger
		if sprite.centered or sprite.offset != -Vector2(frame.origin[0], frame.origin[1]) \
				or sprite.scale != Vector2.ONE * size / frame.density or sprite.texture.resource_path != "res://" + frame.file:
			problems.append("%s: offset %s, scale %s, %s" % [path, sprite.offset, sprite.scale, sprite.texture.resource_path])
	var gear: Dictionary = props["PROP-SWORDSHIELD"]
	if FlyingGear.ORIGIN != Vector2(gear.origin[0], gear.origin[1]) or FlyingGear.DENSITY != gear.density:
		problems.append("FlyingGear")
	for id: String in props:
		if not FileAccess.get_file_as_string("res://" + props[id].file + ".import").contains("mipmaps/generate=true"):
			problems.append("%s has no mipmaps" % id)
	var hearts: Hearts = _main.get_node("Hud/Hearts")
	if Hearts.DENSITY != props["UI-HEART-FULL"].density or hearts.texture_filter != CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS \
			or level.texture_filter != CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS:
		problems.append("hearts or level filtering")
	_check("every prop, the goblin and the hearts draw at 1/density from props.json's origin, with mipmaps",
		problems.is_empty(), "; ".join(problems))
	var pickup_art: Sprite2D = level.get_node("SwordPickup/Art")
	var pickup_shape: CollisionShape2D = level.get_node("SwordPickup/Shape")
	var reach := (pickup_shape.shape as CircleShape2D).radius
	var art_width: float = props["PROP-SWORDSHIELD"].body_game_px[0] * SwordPickup.SCALE
	_check("the pickup shows at 1.5 times its art's size, floating at its height, with a touch area to match",
		pickup_shape.position.y == -SwordPickup.HEIGHT and absf(2.0 * reach - art_width) < 0.15 * art_width
		and pickup_art.position.y >= -SwordPickup.HEIGHT - SwordPickup.BOB - 0.01
		and pickup_art.position.y <= -SwordPickup.HEIGHT + SwordPickup.BOB + 0.01,
		"%.0f px across, touch radius %.0f, at %.0f px" % [art_width, reach, -pickup_art.position.y])

	var outlined: PackedStringArray = []
	for path: String in placed:
		if (level.get_node(path) as Sprite2D).material != null:
			outlined.append(path.get_slice("/", path.get_slice_count("/") - 2))
	_check("the outline is on the goblins and the spikes, not on the glowing waystone, circle and pickup",
		outlined == PackedStringArray(["SpikesA", "SpikesB", "GoblinA"]), ", ".join(outlined))

	# The goblin's box against its art.
	var art := _goblin_art()
	var box := ((level.get_node("Enemies/GoblinA/Shape") as CollisionShape2D).shape as RectangleShape2D).size
	_check("the goblin's box reaches the top of its head and is as wide as its body, not its arms",
		box == Vector2(Goblin.WIDTH, Goblin.HEIGHT) and absf(box.y - art.x) <= 4.0 and box.x >= art.y and box.x < art.z,
		"box %s; in the art the head's top is %.1f px up, the body %.1f px wide, the arms %.1f" % [box, art.x, art.y, art.z])

	# The goblin walks in two frames, facing its way; squashed when defeated, then gone.
	var goblin: Goblin = level.get_node("Enemies/GoblinB")
	var goblin_art: Sprite2D = goblin.get_node("Art")
	var seen := {}
	var faced_wrong := 0
	for i in 120:
		await _frames(1)
		seen[goblin_art.texture] = true
		if goblin_art.flip_h != (goblin.facing < 0):
			faced_wrong += 1
	goblin.position.x = goblin._start_x + goblin.patrol_distance # it turns at the end of its patrol
	await _frames(3)
	var turned := goblin.facing == -1 and goblin_art.flip_h
	_check("a walking goblin shows walk A and B in turn, and is mirrored when it walks left",
		seen.size() == 2 and seen.has(Goblin.WALK_A) and seen.has(Goblin.WALK_B) and faced_wrong == 0 and turned,
		"frames seen %d, facing wrong %d ticks, turned %s" % [seen.size(), faced_wrong, turned])
	goblin.defeat(&"slash")
	await _frames(2)
	var squashed := goblin_art.texture == Goblin.SQUASH and goblin.visible
	await _frames(roundi(Goblin.SQUASH_TIME * Engine.physics_ticks_per_second) + 2)
	var gone := not goblin.visible
	goblin.reset()
	await _frames(1)
	_check("a defeated goblin shows the squashed frame, then disappears; reset, it walks again",
		squashed and gone and goblin.visible and goblin_art.texture != Goblin.SQUASH, "squashed %s, gone %s" % [squashed, gone])

	# The waystone's art.
	_set_threats(false)
	var waystone: Waystone = level.get_node("Waystone")
	var stone_art: Sprite2D = waystone.get_node("Art")
	var halo: Sprite2D = waystone.get_node("Halo")
	var dark_first := stone_art.texture == Waystone.DARK and not halo.visible and not waystone.is_ringing()
	_teleport(waystone.global_position)
	await _frames(3)
	var lit := stone_art.texture == Waystone.LIT and halo.visible and waystone.is_ringing()
	await _frames(roundi(Waystone.RING_TIME * Engine.physics_ticks_per_second) + 3)
	var ring_once := not waystone.is_ringing() and halo.visible
	waystone.reset()
	_check("the waystone shows the dark stone; lit, its halo and, once, a ring of light; dark again after a start-over",
		dark_first and lit and ring_once and stone_art.texture == Waystone.DARK and not halo.visible,
		"dark at first %s, lit with halo and ring %s, the ring over and the halo on %s" % [dark_first, lit, ring_once])

	# The flying gear is the pickup's art.
	var pickup: SwordPickup = level.get_node("SwordPickup")
	_teleport(pickup.global_position + Vector2(-100.0, 0.0))
	await _hold_until(&"move_right", func() -> bool: return _rudy.gear == Rudy.Gear.SWORD, 120)
	await _wait_until(func() -> bool: return not _rudy.is_invulnerable(), 120)
	_rudy.take_hit(_rudy.global_position + Vector2(50.0, 0.0))
	await _frames(1)
	var flying := _main.get_children().filter(func(n: Node) -> bool: return n is FlyingGear)
	_check("the gear that flies off is the pickup's art",
		flying.size() == 1 and (flying[0] as FlyingGear).texture == pickup.get_node("Art").texture, "%d flying" % flying.size())

	# The end card fades in, its picture under the text.
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY, 60)
	var portal: Portal = level.get_node("Portal")
	_teleport(Vector2(portal.global_position.x - 200.0, 840.0))
	await _hold_until(&"move_right", func() -> bool: return _main.state == Main.State.COMPLETE, 120)
	var hud: Hud = _main.get_node("Hud")
	var card: Control = hud.get_node("EndCard")
	await _wait_until(func() -> bool: return hud.is_showing_end_card(), 300)
	var faint := card.modulate.a < 0.5
	await _frames(roundi(Main.FADE_TIME * Engine.physics_ticks_per_second) + 3)
	var picture: TextureRect = card.get_node("Picture")
	_check("the end card fades in, with the picture of the road to the castle under the text",
		faint and is_equal_approx(card.modulate.a, 1.0) and picture.get_index() < card.get_node("Lines").get_index()
		and picture.texture.resource_path == "res://content/level_1/art/endcard.jpg",
		"faint at first %s, alpha %.2f" % [faint, card.modulate.a])
	_set_threats(true)


func _run_2d() -> void:
	_main.queue_free()
	await _frames(1)
	_start_level(true)
	await _frames(5)
	var hud: Hud = _main.get_node("Hud")
	var title: Control = hud.get_node("Title")
	var hearts: Control = hud.get_node("Hearts")
	var start := _rudy.global_position
	_check("the game opens on the title over the start of the level: Rudy idle, the hearts hidden",
		_main.state == Main.State.TITLE and hud.is_showing_title() and title.modulate.a == 1.0
		and hearts.modulate.a == 0.0 and _rudy.pose == &"CHAR-IDLE" and _rudy.mode == Rudy.Mode.WAITING,
		"state %s, hearts alpha %.1f, pose %s" % [Main.State.keys()[_main.state], hearts.modulate.a, _rudy.pose])
	_reset_counts()
	await _hold(&"move_right", 30)
	await _tap(&"jump")
	await _frames(30)
	_check("on the title, moving and jumping do nothing",
		_rudy.global_position.distance_to(start) < 0.01 and _takeoffs == 0 and Sfx.count(&"jump") == 0,
		"moved %.1f px, takeoffs %d" % [_rudy.global_position.distance_to(start), _takeoffs])
	var main_before := _main
	var requests_before := _restart_requests
	await _tap(&"restart")
	await _frames(2)
	var playing := _main.state == Main.State.PLAYING and _rudy.mode == Rudy.Mode.PLAY
	var fading := title.visible and title.modulate.a < 1.0
	await _frames(roundi(Main.FADE_TIME * Engine.physics_ticks_per_second) + 3)
	_check("Enter starts play on the same screen, fading the title out and the hearts in",
		playing and fading and not hud.is_showing_title() and is_equal_approx(hearts.modulate.a, 1.0)
		and _main == main_before and _restart_requests == requests_before,
		"playing %s, fading %s, hearts alpha %.2f" % [playing, fading, hearts.modulate.a])
	await _hold(&"move_right", 30)
	_check("then he is the player's at once, and the title will not show again this run",
		_rudy.global_position.x > start.x + 100.0 and Main.title_shown,
		"moved %.0f px" % (_rudy.global_position.x - start.x))


func _run_3() -> void:
	var music_bus := AudioServer.get_bus_index(Music.BUS)
	var sfx_bus := AudioServer.get_bus_index(Sfx.BUS)
	_check("the Music and SFX buses feed Master",
		music_bus > 0 and sfx_bus > 0 and AudioServer.get_bus_send(music_bus) == &"Master"
		and AudioServer.get_bus_send(sfx_bus) == &"Master",
		"Music at %.0f dB, SFX at %.0f dB" % [AudioServer.get_bus_volume_db(music_bus), AudioServer.get_bus_volume_db(sfx_bus)])

	# The six sounds, each from a stop.
	var wrong: PackedStringArray = []
	for id: StringName in Sfx.STREAMS:
		var player := Sfx.player(id)
		player.stop()
		Sfx.play(id)
		if player.stream.resource_path.get_file() != "SFX-%s.wav" % String(id).to_upper() or player.bus != Sfx.BUS or not player.playing:
			wrong.append(id)
	Sfx.reset_counts()
	_check("Sfx.play starts each of the six sounds from its own file, on the SFX bus",
		Sfx.STREAMS.size() == 6 and wrong.is_empty(), ", ".join(wrong))
	var asked := _sounds_played_in(["res://app", "res://content", "res://ui"])
	var no_file := asked.filter(func(id: StringName) -> bool: return not Sfx.STREAMS.has(id))
	var never := Sfx.STREAMS.keys().filter(func(id: StringName) -> bool: return not asked.has(id))
	_check("every sound the game's scripts play has a file, and every file is played somewhere",
		no_file.is_empty() and never.is_empty(), "no file: %s; never played: %s" % [no_file, never])
	var loop := Music.player().stream as AudioStreamOggVorbis
	_check("the music is MUS-LOOP, looping, 24 bars (54.87 s), on the Music bus",
		loop.resource_path.get_file() == "MUS-LOOP.ogg" and loop.loop and absf(loop.get_length() - 54.867) < 0.01
		and Music.player().bus == Music.BUS, "%.3f s, loop %s" % [loop.get_length(), loop.loop])

	# The game opens: the music starts under the title and plays on into play.
	_main.queue_free()
	await _frames(1)
	Music.player().stop() # as before the game opens
	var starts := Music.starts
	_start_level(true)
	await _frames(5)
	_check("the music starts from the top under the title, at full level",
		_main.state == Main.State.TITLE and Music.is_playing() and Music.starts == starts + 1 and Music.volume_db() == 0.0,
		"playing %s, starts %d, %.1f dB" % [Music.is_playing(), Music.starts - starts, Music.volume_db()])
	await _tap(&"pause")
	await _frames(3)
	_check("Esc does nothing on the title", not _main.is_paused() and _main.state == Main.State.TITLE)
	await _tap(&"restart")
	await _frames(10)
	_check("Enter starts play under the same music: it does not start again",
		_main.state == Main.State.PLAYING and Music.is_playing() and Music.starts == starts + 1,
		"starts %d" % (Music.starts - starts))

	# A hit: 6 dB down for 0.6 s, then back.
	var level: Node2D = _main.get_node("Level1")
	var hud: Hud = _main.get_node("Hud")
	var ground_y := (level.get_node("StartPoint") as Marker2D).global_position.y
	var spikes: Spikes = level.get_node("Hazards/SpikesA")
	_teleport(Vector2(spikes.global_position.x - 220.0, ground_y))
	await _frames(2)
	Input.action_press(&"move_right")
	await _wait_until(func() -> bool: return _rudy.hearts < 3, 120)
	Input.action_release(&"move_right")
	var heading := Music.target_db()
	await _frames(_ticks(Music.RAMP_TIME) + 2)
	var dipped := Music.volume_db()
	var back_after: int = await _wait_until(func() -> bool: return Music.volume_db() == 0.0, 120)
	var dip_ticks := _ticks(Music.RAMP_TIME) + 2 + back_after
	_check("a hit dips the music 6 dB for 0.6 s under the hurt sound, then it comes back",
		heading == Music.HURT_DIP and is_equal_approx(dipped, Music.HURT_DIP)
		and absi(dip_ticks - _ticks(Music.HURT_TIME + Music.RAMP_TIME)) <= 3,
		"%.1f dB; back at full level after %.2f s" % [dipped, dip_ticks / 60.0])

	# Esc pauses: everything stops but the music, which plays on 12 dB down.
	await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 60)
	var goblin: Goblin = level.get_node("Enemies/GoblinA")
	await _tap(&"pause")
	await _frames(1)
	var x_paused := _rudy.global_position.x
	var goblin_x := goblin.position.x
	Input.action_press(&"move_right")
	await _frames(_ticks(Music.RAMP_TIME) + 30)
	Input.action_release(&"move_right")
	_check("Esc in play pauses the game and shows \"Paused\": Rudy and the goblins stand still",
		_main.is_paused() and hud.is_showing_paused() and _rudy.global_position.x == x_paused and goblin.position.x == goblin_x,
		"paused %s; Rudy moved %.1f px, the goblin %.1f px" % [
			_main.is_paused(), _rudy.global_position.x - x_paused, goblin.position.x - goblin_x])
	_check("while paused the music plays on 12 dB down, and the sound effects pause",
		Music.is_playing() and not Music.player().stream_paused and is_equal_approx(Music.volume_db(), Music.PAUSE_DIP)
		and Sfx.player(&"hurt").stream_paused, "%.1f dB" % Music.volume_db())
	await _tap(&"mute_music")
	await _frames(1)
	var music_muted := AudioServer.is_bus_mute(music_bus) and not AudioServer.is_bus_mute(sfx_bus)
	await _tap(&"mute_sfx")
	await _frames(1)
	var both_muted := AudioServer.is_bus_mute(music_bus) and AudioServer.is_bus_mute(sfx_bus)
	await _tap(&"mute_music")
	await _frames(1)
	await _tap(&"mute_sfx")
	await _frames(1)
	_check("M mutes the music and N the sound effects, and again unmutes them, even while paused",
		music_muted and both_muted and not AudioServer.is_bus_mute(music_bus) and not AudioServer.is_bus_mute(sfx_bus))
	await _tap(&"pause")
	await _frames(_ticks(Music.RAMP_TIME) + 2)
	Input.action_press(&"move_right")
	await _frames(10)
	Input.action_release(&"move_right")
	_check("Esc again resumes: he moves, the music is back at full level, the sound effects play on",
		not _main.is_paused() and not hud.is_showing_paused() and _rudy.global_position.x > x_paused
		and Music.volume_db() == 0.0 and not Sfx.player(&"hurt").stream_paused and Music.starts == starts + 1,
		"moved %.1f px, %.1f dB" % [_rudy.global_position.x - x_paused, Music.volume_db()])

	# A fall: 9 dB down through the fade and the respawn; the music does not start again.
	var gaps := _gaps(level)
	for fall in 2: # the second fall takes his last heart: the level starts over from the opening
		await _wait_until(func() -> bool: return _rudy.mode == Rudy.Mode.PLAY and _rudy.is_on_floor(), 120)
		_teleport(Vector2(gaps[0].x - 120.0, ground_y))
		Input.action_press(&"move_right")
		await _wait_until(func() -> bool: return _main.state == Main.State.DYING, 240)
		Input.action_release(&"move_right")
		await _tap(&"pause")
		await _frames(_ticks(Music.RAMP_TIME))
		var paused := _main.is_paused()
		var levels := {}
		while _main.state == Main.State.DYING:
			levels[snappedf(Music.volume_db(), 0.01)] = true
			await _frames(1)
		await _frames(_ticks(Music.RAMP_TIME) + 2)
		_check("a fall%s dips the music 9 dB through the fade and the respawn, then it comes back; it does not start again" % (
			" that starts the level over" if fall == 1 else ""),
			not paused and levels.keys() == [Music.DEATH_DIP] and Music.volume_db() == 0.0
			and Music.is_playing() and Music.starts == starts + 1 and (fall == 0 or _main.checkpoint_name == "start"),
			"levels while dying %s; Esc paused it %s; starts %d" % [levels.keys(), paused, Music.starts - starts])

	# The teleport circle: the music fades out and stops, and the end card is silent.
	var portal: Portal = level.get_node("Portal")
	_teleport(Vector2(portal.global_position.x - 200.0, ground_y))
	await _hold_until(&"move_right", func() -> bool: return _main.state == Main.State.COMPLETE, 120)
	var fading := Music.target_db() == Music.SILENCE
	var stopped_after: int = await _wait_until(func() -> bool: return not Music.player().playing, 180)
	_check("on the teleport circle the music fades out over 1.5 s and stops",
		fading and not Music.player().playing and absi(stopped_after - _ticks(Music.FADE_OUT_TIME)) <= 3,
		"stopped after %.2f s" % (stopped_after / 60.0))
	await _wait_until(func() -> bool: return hud.is_showing_end_card(), 300)
	await _tap(&"pause")
	await _frames(3)
	_check("the end card is silent, and Esc does nothing there", not Music.player().playing and not _main.is_paused())
	# Enter plays again: the game reloads the scene, and Main starts the music.
	_main.queue_free()
	await _frames(1)
	_start_level()
	await _frames(5)
	_check("playing again starts the music from the top, at full level",
		Music.is_playing() and Music.starts == starts + 2 and Music.volume_db() == 0.0, "starts %d" % (Music.starts - starts))

	# Sound decides nothing: muted, the route from the opening runs the same.
	var runs: PackedStringArray = []
	for muted: bool in [false, true]:
		AudioServer.set_bus_mute(music_bus, muted)
		AudioServer.set_bus_mute(sfx_bus, muted)
		_main.queue_free()
		await _frames(1)
		_start_level()
		await _frames(5)
		_reset_counts()
		var ticks: int = await _run_route(_gaps(_main.get_node("Level1")), 1800)
		runs.append("%d ticks, at x %.3f, sounds %s" % [ticks, _rudy.global_position.x, Sfx.summary()])
	AudioServer.set_bus_mute(music_bus, false)
	AudioServer.set_bus_mute(sfx_bus, false)
	_check("with both buses muted the route from the opening runs the same, tick for tick, with the same sounds",
		runs[0] == runs[1] and not runs[0].begins_with("-1"), " | ".join(runs))


func _run_5() -> void:
	_main.queue_free()
	_start_level(true)
	var debug: Label = _main.get_node("Hud/Debug")
	_check("the game opens with the debug line hidden", not debug.visible)
	var named := _res_paths_named_in("res://")
	var missing: PackedStringArray = []
	for path: String in named:
		if not FileAccess.file_exists(path) and not DirAccess.dir_exists_absolute(path):
			missing.append("%s (named in %s)" % [path, named[path]])
	_check("every file the scenes, resources and scripts name by a res:// path is in the project",
		named.size() > 50 and missing.is_empty(), "%d paths; missing: %s" % [named.size(), ", ".join(missing)])


## The goblin's walk frame, in game px: the height of the top of its head (the
## highest row at least 16 px wide, above the wisps of hair), the width of its
## body 60 px up, and the width of its swinging arms 40 px up.
func _goblin_art() -> Vector3:
	var image := Image.load_from_file(ProjectSettings.globalize_path("res://content/goblin/frames/ENEMY-GOBLIN-WALK-A.png"))
	var origin := Vector2i(179, 269) # props.json
	var widths: Array[Vector2i] = []
	for y in image.get_height():
		var left := image.get_width()
		var right := -1
		for x in image.get_width():
			if image.get_pixel(x, y).a > 0.5:
				left = mini(left, x)
				right = maxi(right, x)
		widths.append(Vector2i(left, right))
	var head_row := 0
	while head_row < widths.size() and widths[head_row].y - widths[head_row].x + 1 < 32:
		head_row += 1
	var body := widths[origin.y - 120]
	var arms := widths[origin.y - 80]
	return Vector3(origin.y - head_row, body.y - body.x + 1, arms.y - arms.x + 1) / 2.0


## The tall wheat tufts in the ground art, more than 30 px above the walk line, as (from x, to x) in the level.
func _tall_tufts(segments: Array[GroundSegment]) -> Array[Vector2]:
	var image := Image.load_from_file(ProjectSettings.globalize_path("res://content/level_1/art/ground_tile.png"))
	var top_rows := int(-GroundSegment.ART_TOP * GroundSegment.DENSITY) - int(30 * GroundSegment.DENSITY)
	var spans: Array[Vector2] = []
	var from := -1
	for x in image.get_width() + 1:
		var tall := false
		if x < image.get_width():
			for y in top_rows:
				if image.get_pixel(x, y).a > 0.5:
					tall = true
					break
		if tall and from < 0:
			from = x
		elif not tall and from >= 0:
			spans.append(Vector2(from, x) / GroundSegment.DENSITY)
			from = -1
	var tufts: Array[Vector2] = []
	for seg in segments:
		var run := seg.tile_run()
		var stretch: float = run.period / GroundSegment.TILE_WIDTH
		for i in int(run.count):
			var left: float = seg.position.x + run.from + i * run.period
			for span in spans:
				tufts.append(Vector2(left + span.x * stretch, left + span.y * stretch))
	return tufts


## The spikes' art, in game px: the width of the row of spikes just above the
## plank, the height of the tips, and the height of the plank.
func _spikes_art() -> Vector3:
	var image := Image.load_from_file(ProjectSettings.globalize_path("res://content/level_1/art/ENV-SPIKES.png"))
	var origin_y := 140 # props.json
	var widths: Array[int] = []
	var first_row := -1
	for y in image.get_height():
		var n := 0
		for x in image.get_width():
			if image.get_pixel(x, y).a > 0.5:
				n += 1
		widths.append(n)
		if n > 0 and first_row < 0:
			first_row = y
	var widest: int = widths.max()
	var plank_top := widths.find_custom(func(n: int) -> bool: return n > 0.8 * widest)
	var row := plank_top - 3
	var left := image.get_width()
	var right := 0
	for x in image.get_width():
		if image.get_pixel(x, row).a > 0.5:
			left = mini(left, x)
			right = maxi(right, x + 1)
	return Vector3(right - left, origin_y - first_row, origin_y - plank_top) / 2.0


## What of the screen the far layer or the fields fail to cover; empty if nothing.
func _backdrop_gap(backdrop: Backdrop, sky: Sprite2D) -> String:
	var view_left := backdrop.view_left_x()
	var view_right := view_left + 1920.0 / _camera.zoom.x
	var fields := backdrop.fields_span()
	var problems: PackedStringArray = []
	if sky.position.x > 0.0 or sky.position.x + sky.texture.get_width() < 1920.0 or sky.texture.get_height() < 1080:
		problems.append("far layer at %.1f" % sky.position.x)
	if fields.x > view_left or fields.y < view_right:
		problems.append("fields %.0f to %.0f, view %.0f to %.0f" % [fields.x, fields.y, view_left, view_right])
	return ", ".join(problems)


## The first and last column with an opaque pixel (alpha over half) at or below `from_row`.
func _opaque_columns(path: String, from_row: int) -> Vector2:
	var image := Image.load_from_file(ProjectSettings.globalize_path(path))
	var first := image.get_width()
	var last := -1
	for x in image.get_width():
		for y in range(from_row, image.get_height()):
			if image.get_pixel(x, y).a > 0.5:
				first = mini(first, x)
				last = maxi(last, x)
				break
	return Vector2(first, last + 1)


## Waits until the frame after the next one has been processed, so the camera and the layers have both moved.
func _drawn() -> void:
	await get_tree().process_frame
	await get_tree().process_frame


## The cliffs: the gaps between ground segments, as (from x, to x).
func _gaps(level: Node2D) -> Array[Vector2]:
	var segments: Array[GroundSegment] = []
	for child in level.get_node("Ground").get_children():
		if child is GroundSegment:
			segments.append(child)
	segments.sort_custom(func(a: GroundSegment, b: GroundSegment) -> bool: return a.position.x < b.position.x)
	var gaps: Array[Vector2] = []
	for i in range(1, segments.size()):
		var end := segments[i - 1].global_position.x + segments[i - 1].size.x
		var begin := segments[i].global_position.x
		if begin > end:
			gaps.append(Vector2(end, begin))
	return gaps


## Runs at the cliff at full speed and jumps, once for each aim point every
## 5 px from 300 px before its edge to 40 px past it. Returns the earliest and
## the latest takeoff that cleared it, as x from the edge (before it is negative).
func _takeoff_window(gap: Vector2) -> Vector2:
	var earliest := INF
	var latest := -INF
	var aim := -300.0
	while aim <= 40.0:
		_teleport(Vector2(gap.x - 500.0, 840.0))
		await _frames(2) # let him settle: is_on_floor() is stale until his next move
		Input.action_press(&"move_right")
		# Past the edge he keeps moving right while he falls, so every aim is reached.
		await _wait_until(func() -> bool: return _rudy.global_position.x >= gap.x + aim, 240)
		Input.action_press(&"jump")
		var takeoff_x := NAN
		var floor_x := _rudy.global_position.x
		for t in 120:
			await _frames(1)
			if t == 2:
				Input.action_release(&"jump")
			if _rudy.is_on_floor():
				if is_nan(takeoff_x):
					floor_x = _rudy.global_position.x
				elif _rudy.global_position.x > gap.y:
					break # landed beyond the cliff
			elif is_nan(takeoff_x) and _rudy.velocity.y < 0.0:
				takeoff_x = floor_x # where he stood on the takeoff tick
			if _rudy.global_position.y > 880.0:
				break # in the pit
		Input.action_release(&"move_right")
		Input.action_release(&"jump")
		if not is_nan(takeoff_x) and _rudy.is_on_floor() and _rudy.global_position.x > gap.y:
			earliest = minf(earliest, takeoff_x - gap.x)
			latest = maxf(latest, takeoff_x - gap.x)
		aim += 5.0
	return Vector2(earliest, latest)


func _from_edge(x: float) -> String:
	if x < 0.0:
		return "%.0f px before the edge" % -x
	return "%.0f px past the edge" % x


## Holds right and jumps over each cliff, row of spikes and live goblin ahead,
## until the level is complete. Returns the ticks it took, or -1 if he died or
## ran out of time.
func _run_route(gaps: Array[Vector2], max_ticks: int) -> int:
	var release_jump_at := -1
	Input.action_press(&"move_right")
	for t in max_ticks:
		await _frames(1)
		if t == release_jump_at:
			Input.action_release(&"jump")
		if _main.state == Main.State.COMPLETE:
			Input.action_release(&"move_right")
			Input.action_release(&"jump")
			return t + 1
		if _main.state == Main.State.DYING:
			break
		if release_jump_at < t and _rudy.is_on_floor() and _obstacle_ahead(gaps):
			Input.action_press(&"jump")
			release_jump_at = t + 3
	Input.action_release(&"move_right")
	Input.action_release(&"jump")
	return -1


## True when a cliff, a row of spikes or a live goblin starts close enough ahead
## that the route should jump now.
func _obstacle_ahead(gaps: Array[Vector2]) -> bool:
	var x := _rudy.global_position.x
	for gap in gaps:
		if x >= gap.x - CLIFF_LEAD and x < gap.x:
			return true
	for spikes in _main.get_node("Level1/Hazards").get_children():
		var left := (spikes as Node2D).global_position.x - Spikes.WIDTH / 2.0
		if x >= left - SPIKES_LEAD and x < left:
			return true
	for goblin in _main.get_node("Level1/Enemies").get_children():
		if not (goblin as Goblin).dead:
			var left := (goblin as Node2D).global_position.x - Goblin.WIDTH / 2.0
			if x >= left - GOBLIN_LEAD and x < left:
				return true
	return false


## Switches the spikes and the goblins on or off, for checks of movement alone.
func _set_threats(enabled: bool) -> void:
	for path: String in ["Level1/Hazards", "Level1/Enemies"]:
		_main.get_node(path).process_mode = Node.PROCESS_MODE_INHERIT if enabled else Node.PROCESS_MODE_DISABLED


func _check_scenes() -> void:
	for path: String in REQUIRED_NODES:
		var root := (load(path) as PackedScene).instantiate()
		var missing: PackedStringArray = []
		for node_path: String in REQUIRED_NODES[path]:
			if not root.has_node(node_path):
				missing.append(node_path)
		_check("%s has its nodes" % path.get_file(), missing.is_empty(),
			"" if missing.is_empty() else "missing " + ", ".join(missing))
		root.free()


## The jump the controller should make, stepped the way it moves: the takeoff
## tick moves at the full jump velocity; from the next tick, gravity is added
## before each move, fall_gravity once he is coming down. Returns the apex in px,
## then the ticks of the rise and of the fall.
func _expected_jump() -> Vector3:
	var dt := 1.0 / Engine.physics_ticks_per_second
	var speed := -_rudy.jump_velocity # negative is up
	var y := 0.0
	var apex := 0.0
	var rise_ticks := 0
	for tick in range(1, 600):
		if tick > 1:
			speed += (_rudy.fall_gravity if speed >= 0.0 else _rudy.gravity) * dt
		y += speed * dt
		if -y > apex:
			apex = -y
			rise_ticks = tick
		if y >= 0.0:
			return Vector3(apex, rise_ticks, tick - rise_ticks)
	return Vector3.ZERO


## The sound IDs that the scripts under `dirs` pass to Sfx.play.
func _sounds_played_in(dirs: Array[String]) -> Array[StringName]:
	var found: Array[StringName] = []
	var call := RegEx.create_from_string(r'Sfx\.play\(&"(\w+)"\)')
	var pending := dirs.duplicate()
	while not pending.is_empty():
		var dir: String = pending.pop_back()
		for sub in DirAccess.get_directories_at(dir):
			pending.append(dir.path_join(sub))
		for file in DirAccess.get_files_at(dir):
			if file.ends_with(".gd"):
				for found_call in call.search_all(FileAccess.get_file_as_string(dir.path_join(file))):
					var id := StringName(found_call.get_string(1))
					if not found.has(id):
						found.append(id)
	return found


## Every res:// path named in the project's scenes, resources, shaders, scripts
## and project.godot, under `root` (skipping the engine's .godot cache), with
## the first file that names it.
func _res_paths_named_in(root: String) -> Dictionary[String, String]:
	var named: Dictionary[String, String] = {}
	var path_in_text := RegEx.create_from_string(r'res://[\w./-]+')
	var pending: Array[String] = [root]
	while not pending.is_empty():
		var dir: String = pending.pop_back()
		for sub in DirAccess.get_directories_at(dir):
			if not sub.begins_with("."):
				pending.append(dir.path_join(sub))
		for file in DirAccess.get_files_at(dir):
			if file.get_extension() in ["gd", "tscn", "tres", "gdshader", "godot"]:
				var source := dir.path_join(file)
				for found in path_in_text.search_all(FileAccess.get_file_as_string(source)):
					if not named.has(found.get_string()):
						named[found.get_string()] = source
	return named


func _ticks(seconds: float) -> int:
	return roundi(seconds * Engine.physics_ticks_per_second)


func _check(what: String, ok: bool, detail: String = "") -> void:
	print("%s  %s%s" % ["PASS" if ok else "FAIL", what, "" if detail.is_empty() else "  (%s)" % detail])
	if not ok:
		_failures += 1


func _frames(n: int) -> void:
	for i in n:
		await get_tree().physics_frame


## Waits until `condition` is true, for at most `max_ticks`; returns the ticks waited.
func _wait_until(condition: Callable, max_ticks: int) -> int:
	for t in max_ticks:
		if condition.call():
			return t
		await get_tree().physics_frame
	return max_ticks


func _hold(action: StringName, ticks: int) -> void:
	Input.action_press(action)
	await _frames(ticks)
	Input.action_release(action)


func _hold_until(action: StringName, condition: Callable, max_ticks: int) -> void:
	Input.action_press(action)
	await _wait_until(condition, max_ticks)
	Input.action_release(action)


func _tap(action: StringName) -> void:
	Input.action_press(action)
	await _frames(2)
	Input.action_release(action)


func _teleport(spot: Vector2) -> void:
	_rudy.global_position = spot
	_rudy.velocity = Vector2.ZERO


func _reset_counts() -> void:
	Sfx.reset_counts()
	_takeoffs = 0
	_takeoff_ticks.clear()
	_jump_sound_ticks.clear()
	_lights = 0
	_trail.clear()
	_trail.append(_rudy.pose)


func _counts_text() -> String:
	return "takeoffs %d, Sfx jump %d" % [_takeoffs, Sfx.count(&"jump")]


func _trail_text() -> String:
	return " > ".join(PackedStringArray(_trail))
