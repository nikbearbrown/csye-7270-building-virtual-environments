extends SceneTree
## Film capture for the A6 particle effects in play. SCRIPTED INPUT, not a human playtest.
## Runs ONLY in an isolated copy of the submitted project. Instantiates the unmodified res://base.tscn inside a
## 3840x2160 SubViewport (native 4K, real window run with the real GPU, not headless); the view is the
## player's own PlayerCamera. Keys are sent with Input.parse_input_event() through the project's InputMap,
## exactly like the submitted state tests (Space = jump, A = move_left, S = move_back, F = interact).
## One mouse-motion event (pushed into the SubViewport) tilts the camera 23 degrees down at tick 20.
## shot=landing : Effect A. Two single jumps, then four rapid jumps while holding A (each lands inside
##                the previous dust's 1.6 s lifetime: the restart case).
## shot=lights  : Effect B. Stand, walk back to the wall switch with S (held 1 s), F (lights off), F (lights on);
##                then the tree is paused from code for 1 s (the game has no pause feature, as in the
##                state test) and LightDust is hidden from code for 1 s, then shown again.
## cam=film replaces the view with a fixed film camera near ceiling light 1 (labelled in the film); keys are unchanged.
## Every physics tick is logged to JSONL; landed / lights_changed counts are asserted; failure exits 1.
## Run with --fixed-fps 30: offline rendering, NOT evidence of real-time frame rate.
## Usage: godot --path <copy> --fixed-fps 30 --script res://film_capture/play_capture.gd -- shot=landing out=<dir>

const PHYSICS_HZ := 60
const MOUSE_TICK := 20
const WALK_END_TICK := 180
const MOUSE_RELATIVE := Vector2(0, 160)   # 160 px * mouse_sensitivity 0.0025 = 0.40 rad (23 deg) down, so the feet are in frame

var shot := "landing"
var out_dir := "user://capture"
var vp: SubViewport
var base: Node3D
var player: Node3D
var dust_a: Node3D
var dust_b: GPUParticles3D
var lights: Node
var switch_area: Area3D
var tick := 0
var frame := 0
var log_file: FileAccess
var landed_ticks: Array = []
var light_changes: Array = []
var done := false
var end_tick := 0
var events: Array = []    # [tick, kind, arg]
var walking := false
var walk_started := -1
var phase_tick := {}
var cam_mode := "player"   # cam=film: a film camera added by this script (not part of the game), near ceiling light 1
var film_cam: Camera3D
const FILM_CAM_POS := Vector3(0.8, 1.6, -1.2)
const FILM_CAM_LOOK := Vector3(0.0, 1.9, -3.7)      # name -> tick, for the lights shot's code-driven phases


func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.split("=", true, 1)
		if kv[0] == "out":
			out_dir = kv[1]
		elif kv[0] == "cam":
			cam_mode = kv[1]
		elif kv[0] == "shot":
			shot = kv[1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/frames")
	vp = SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	base = load("res://base.tscn").instantiate()
	vp.add_child(base)
	log_file = FileAccess.open(out_dir + "/inputs.jsonl", FileAccess.WRITE)
	if shot == "landing":
		# [tick, key, pressed]
		events = [
			[60, KEY_SPACE, true], [66, KEY_SPACE, false],        # 1.0 s single jump
			[210, KEY_SPACE, true], [216, KEY_SPACE, false],      # 3.5 s single jump
			[330, KEY_A, true],                                    # 5.5 s hold A (move left, toward open floor)
			[340, KEY_SPACE, true], [346, KEY_SPACE, false],      # rapid jump 1
			[400, KEY_SPACE, true], [406, KEY_SPACE, false],      # rapid jump 2, pressed in the air; buffered? logged
			[460, KEY_SPACE, true], [466, KEY_SPACE, false],      # rapid jump 3
			[520, KEY_SPACE, true], [526, KEY_SPACE, false],      # rapid jump 4
			[540, KEY_A, false],
		]
		end_tick = 700
	else:
		events = [[120, KEY_S, true]]   # walk back to the switch; released when inside its area
		end_tick = 100000                # ends after the scripted phases below
	physics_frame.connect(_on_physics_frame)
	RenderingServer.frame_post_draw.connect(_on_post_draw)
	print("PLAY_CAPTURE shot=%s size=%s renderer=%s adapter=%s physics_hz=%d" % [shot, vp.size,
		RenderingServer.get_current_rendering_method(), RenderingServer.get_video_adapter_name(),
		Engine.physics_ticks_per_second])


func _device_for(keycode: Key) -> int:
	for action in InputMap.get_actions():
		for e in InputMap.action_get_events(action):
			if e is InputEventKey and (e as InputEventKey).physical_keycode == keycode:
				return e.device
	return -1


func _key(keycode: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.physical_keycode = keycode
	ev.pressed = pressed
	ev.device = _device_for(keycode)
	Input.parse_input_event(ev)
	log_file.store_line(JSON.stringify({"tick": tick, "game_s": tick / float(PHYSICS_HZ), "frame": frame,
		"input": OS.get_keycode_string(keycode), "pressed": pressed}))


func _on_physics_frame() -> void:
	if done:
		return
	if player == null:
		if cam_mode == "film":
			film_cam = Camera3D.new()
			film_cam.fov = 60.0
			base.add_child(film_cam)
			film_cam.look_at_from_position(FILM_CAM_POS, FILM_CAM_LOOK)
			film_cam.make_current()   # after the tree is ready, so the player's own camera does not take it back
		player = base.get_node("Player")
		dust_a = base.get_node("LandingDust")
		dust_b = base.get_node("LightDust")
		lights = base.get_node("CeilingLights")
		switch_area = base.get_node("LightSwitch/InteractArea")
		player.landed.connect(func(): landed_ticks.append(tick))
		lights.lights_changed.connect(func(on): light_changes.append([tick, on]))
	if tick == MOUSE_TICK:
		var mm := InputEventMouseMotion.new()
		mm.relative = MOUSE_RELATIVE
		vp.push_input(mm)   # a SubViewport without a container gets no window events; player_controller turns the pitch
		log_file.store_line(JSON.stringify({"tick": tick, "frame": frame, "input": "mouse_motion",
			"relative": [MOUSE_RELATIVE.x, MOUSE_RELATIVE.y]}))
	for e in events:
		if e[0] == tick:
			_key(e[1], e[2])
	if shot == "lights":
		_lights_script()
	log_file.store_line(JSON.stringify({"tick": tick, "player": [player.global_position.x, player.global_position.y,
		player.global_position.z], "landing_dust_at": [dust_a.global_position.x, dust_a.global_position.z],
		"lights_on": lights.is_lights_on(), "light_dust_visible": dust_b.is_visible_in_tree(),
		"light_dust_emitting": dust_b.emitting, "paused": paused}))
	tick += 1


## The lights shot's phases. Keys go through the InputMap; pause and hide are set from code and labelled as such.
func _lights_script() -> void:
	if tick == 120:
		walking = true
	if walking and tick >= WALK_END_TICK:   # S held for 60 ticks (1 s); the player has stopped against the wall in front of the switch
		walking = false
		_key(KEY_S, false)
		phase_tick["at_switch"] = tick
	if not phase_tick.has("at_switch"):
		return
	var t0: int = phase_tick["at_switch"]
	if tick == t0 + 60:
		_key(KEY_F, true)       # lights off
	elif tick == t0 + 64:
		_key(KEY_F, false)
	elif tick == t0 + 180:
		_key(KEY_F, true)       # lights on
	elif tick == t0 + 184:
		_key(KEY_F, false)
	elif tick == t0 + 300:
		paused = true           # code-set pause (no pause feature in the game); physics stops, this script keeps going
		phase_tick["pause"] = tick
		log_file.store_line(JSON.stringify({"tick": tick, "code": "get_tree().paused = true"}))
	elif tick == t0 + 360:
		paused = false
		log_file.store_line(JSON.stringify({"tick": tick, "code": "get_tree().paused = false"}))
	elif tick == t0 + 420:
		dust_b.visible = false  # code-set hide, as in the state test
		log_file.store_line(JSON.stringify({"tick": tick, "code": "LightDust.visible = false"}))
	elif tick == t0 + 480:
		dust_b.visible = true
		log_file.store_line(JSON.stringify({"tick": tick, "code": "LightDust.visible = true"}))
	elif tick == t0 + 600:
		end_tick = tick


func _on_post_draw() -> void:
	if done:
		return
	if OS.get_cmdline_user_args().has("diag"):
		print("DIAG frame=%d tick=%d z=%.3f lights=%s overlap=%s" % [frame, tick, player.global_position.z if player else 0.0,
			lights.is_lights_on() if lights else null, switch_area.overlaps_body(player) if switch_area else null])
		if frame > 220:
			quit(0)
	vp.get_texture().get_image().save_png("%s/frames/f%05d.png" % [out_dir, frame])
	frame += 1
	if tick >= end_tick:
		done = true
		log_file.close()
		quit(_check())


func _check() -> int:
	var fails := 0
	print("LANDED ticks: ", landed_ticks)
	print("LIGHTS_CHANGED: ", light_changes)
	print("PHASES: ", phase_tick)
	if shot == "landing":
		if landed_ticks.size() < 4:
			print("FAIL expected at least 4 landings, got ", landed_ticks.size())
			fails += 1
	else:
		if light_changes.size() != 2:
			print("FAIL expected 2 lights_changed, got ", light_changes.size())
			fails += 1
	print("FRAMES %d  RESULT %s" % [frame, "ALL PASS" if fails == 0 else "%d FAIL" % fails])
	return 0 if fails == 0 else 1
