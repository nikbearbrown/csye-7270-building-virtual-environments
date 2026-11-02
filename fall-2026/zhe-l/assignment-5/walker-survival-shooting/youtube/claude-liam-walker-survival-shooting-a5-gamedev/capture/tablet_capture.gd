extends SceneTree
## Film capture for the A5 screen-glow shader in play. SCRIPTED INPUT, not a human playtest.
## Runs ONLY in an isolated copy. Instantiates the unmodified res://base.tscn inside a
## 3840x2160 SubViewport (native 4K, real window run, not headless); the view is the
## player's own PlayerCamera. Inputs: Tab key events sent with Input.parse_input_event()
## (InputMap action "tablet" -> player_controller.gd -> intent -> humanoid.gd), and one
## mouse-motion event delivered into the SubViewport with push_input() (a SubViewport
## without a container receives no window events) so player_controller._unhandled_input()
## turns the camera to the player's left-back, where the one-hand tablet is not hidden by
## the body. No teleporting, no state set by code.
## Every physics tick is logged (hold state + the player's pad_light_data) to a JSONL
## input log, and the expected screen behaviour is asserted; any failure exits 1.
## Run with --fixed-fps 30: offline rendering, NOT evidence of real-time frame rate.
## Usage: godot --path <copy> --fixed-fps 30 --script res://film_capture/tablet_capture.gd -- out=<dir>

const PHYSICS_HZ := 60
# Tab key route, in physics ticks (60 per second of game time): [tick, pressed]
const ROUTE := [
	[90, true], [99, false],      # 1.50 s short press  -> ONE_HAND, lights on arrival
	[240, true], [282, false],    # 4.00 s long press   -> TWO_HAND, must never go dark
	[420, true], [462, false],    # 7.00 s long press   -> NONE, dark at once
	[540, true], [549, false],    # 9.00 s short press  -> ONE_HAND ...
	[556, true], [561, false],    # 9.27 s short press  -> NONE before arrival: never lit
	[630, true], [672, false],    # 10.5 s long press   -> TWO_HAND straight from the hip, lights on arrival
]
const MOUSE_TICK := 30            # 0.5 s, still NONE: camera turns, body does not (idle)
const MOUSE_RELATIVE := Vector2(244, 0)   # x 244 px * mouse_sensitivity 0.0025 = 0.61 rad (35 deg)
const END_TICK := 780              # 13.0 s
const TAB_KEYCODE := KEY_TAB

var out_dir := "user://capture"
var vp: SubViewport
var base: Node3D
var body: Node
var screen_mat: ShaderMaterial
var tick := 0
var frame := 0
var log_file: FileAccess
var samples: Array = []   # [tick, hold, light]
var done := false

func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.split("=", true, 1)
		if kv[0] == "out":
			out_dir = kv[1]
	DirAccess.make_dir_recursive_absolute(out_dir + "/frames")
	vp = SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	base = load("res://base.tscn").instantiate()
	vp.add_child(base)
	log_file = FileAccess.open(out_dir + "/tablet-inputs.jsonl", FileAccess.WRITE)
	physics_frame.connect(_on_physics_frame)
	RenderingServer.frame_post_draw.connect(_on_post_draw)
	print("TABLET_CAPTURE size=%s renderer=%s physics_hz=%d" % [vp.size,
		RenderingServer.get_current_rendering_method(), Engine.physics_ticks_per_second])

func _on_physics_frame() -> void:
	if done:
		return
	if body == null:
		body = base.get_node("Player")
		var tablet := body.get_node("Visual/TabletDevice")
		screen_mat = tablet.get_screen().get_surface_override_material(0) as ShaderMaterial
	if tick == MOUSE_TICK:
		var mm := InputEventMouseMotion.new()
		mm.relative = MOUSE_RELATIVE
		vp.push_input(mm)
		log_file.store_line(JSON.stringify({"tick": tick, "game_s": tick / float(PHYSICS_HZ),
			"frame": frame, "input": "mouse_motion", "relative": [MOUSE_RELATIVE.x, MOUSE_RELATIVE.y],
			"mouse_mode": Input.mouse_mode}))
	for step in ROUTE:
		if step[0] == tick:
			var ev := InputEventKey.new()
			ev.physical_keycode = TAB_KEYCODE
			ev.keycode = TAB_KEYCODE
			ev.pressed = step[1]
			Input.parse_input_event(ev)
			log_file.store_line(JSON.stringify({"tick": tick, "game_s": tick / float(PHYSICS_HZ),
				"frame": frame, "input": "Tab", "pressed": step[1]}))
	# This runs before the nodes' _physics_process for this tick, so the state read here is
	# the result of the previous tick; it is logged under the previous tick number.
	if tick > 0:
		var hold: int = body.get_tablet_hold()
		var light: float = screen_mat.get_shader_parameter(&"pad_light_data")
		samples.append([tick - 1, hold, light])
		log_file.store_line(JSON.stringify({"tick": tick - 1, "hold": hold, "pad_light_data": light}))
	tick += 1

func _on_post_draw() -> void:
	if done:
		return
	vp.get_texture().get_image().save_png("%s/frames/f%05d.png" % [out_dir, frame])
	frame += 1
	if tick >= END_TICK:
		done = true
		log_file.close()
		quit(_check())

## Asserts the screen rules from CHANGE-BRIEF part 1 on the logged samples. Returns the exit code.
func _check() -> int:
	var fails := 0
	var change_ticks: Array = []   # [tick, old, new]
	for i in range(1, samples.size()):
		if samples[i][1] != samples[i - 1][1]:
			change_ticks.append([samples[i][0], samples[i - 1][1], samples[i][1]])
	print("STATE CHANGES (tick, old, new): ", change_ticks)
	if change_ticks.size() != 6:
		print("FAIL expected 6 state changes, got ", change_ticks.size())
		return 1
	# 1. NONE -> ONE_HAND: dark at the change, lit 0.39 from arrival (21 ticks incl. the change tick)
	var c0: int = change_ticks[0][0]
	fails += _expect(_light_at(c0) == 0.0, "dark on the tick the state becomes ONE_HAND")
	var lit0 := _first_lit_after(c0)
	fails += _expect(lit0 - c0 + 1 == 21, "lit 21 physics ticks (0.35 s) after the change, got %d" % (lit0 - c0 + 1))
	fails += _expect(is_equal_approx(_light_at(lit0), 0.39), "lit value is 0.39")
	# 2. ONE_HAND -> TWO_HAND: never dark between the two changes
	var c1: int = change_ticks[1][0]
	var c2: int = change_ticks[2][0]
	fails += _expect(_min_light(lit0, c2 - 1) > 0.0, "never dark from ONE_HAND through TWO_HAND")
	# 3. TWO_HAND -> NONE: dark on the change tick
	fails += _expect(_light_at(c2) == 0.0, "dark on the tick the state becomes NONE")
	# 4. ONE_HAND then NONE before arrival: never lit
	var c3: int = change_ticks[3][0]
	var c4: int = change_ticks[4][0]
	fails += _expect(c4 - c3 + 1 < 21, "second put-away happens before arrival (%d ticks)" % (c4 - c3 + 1))
	var c5: int = change_ticks[5][0]
	fails += _expect(_max_light(c3, c5 - 1) == 0.0, "never lit when put away before arrival")
	# 5. NONE -> TWO_HAND straight from the hip: dark at the change, lit 21 ticks later
	fails += _expect(change_ticks[5][2] == 2, "last change is NONE -> TWO_HAND")
	fails += _expect(_light_at(c5) == 0.0, "dark on the tick the state becomes TWO_HAND")
	var lit5 := _first_lit_after(c5)
	fails += _expect(lit5 - c5 + 1 == 21, "lit 21 physics ticks after NONE -> TWO_HAND, got %d" % (lit5 - c5 + 1))
	print("CHANGE TICKS one=%d two=%d none=%d one=%d none=%d two=%d first_lit=%d,%d frames=%d" % [c0, c1, c2, c3, c4, c5, lit0, lit5, frame])
	print("RESULT %s" % ("ALL PASS" if fails == 0 else "%d FAIL" % fails))
	return 0 if fails == 0 else 1

func _expect(ok: bool, what: String) -> int:
	print(("PASS " if ok else "FAIL ") + what)
	return 0 if ok else 1

func _light_at(t: int) -> float:
	for s in samples:
		if s[0] == t:
			return s[2]
	return -1.0

func _first_lit_after(t: int) -> int:
	for s in samples:
		if s[0] >= t and s[2] > 0.0:
			return s[0]
	return -1

func _min_light(a: int, b: int) -> float:
	var m := 1e9
	for s in samples:
		if s[0] >= a and s[0] <= b:
			m = min(m, s[2])
	return m

func _max_light(a: int, b: int) -> float:
	var m := -1.0
	for s in samples:
		if s[0] >= a and s[0] <= b:
			m = max(m, s[2])
	return m
