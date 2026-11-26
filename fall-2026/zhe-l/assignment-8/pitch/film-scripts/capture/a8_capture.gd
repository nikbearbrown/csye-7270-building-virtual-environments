extends Node3D
## A8 pitch film capture: scripted-input recording (NOT a human playtest).
## Runs only in the isolated copy of commit f13431bf (course repo assignment-8/walker-survival-shooting/godot).
## Loads the unmodified res://base.tscn and sends key presses with Input.parse_input_event,
## using the physical keycodes the InputMap binds (Tab = tablet, Space = jump).
## The light switch is pressed by calling LightSwitch.interact() (the function F calls), without walking to it.
## User args (after --): seq=b10 (tablet raise + interrupt, front view) or seq=b11 (landing dust + lights).
## Run: godot --path <copy> res://film_capture/a8_capture.tscn --write-movie <dir>/frame.png --fixed-fps 30 --resolution 1920x1080 -- seq=b10

const BASE_SCENE := "res://base.tscn"
const CAMERA_PIVOT_PATH := "PlayerController/CameraPivot"
const FPS := 30.0

# [movie frame, action, pressed or null, label]
const SEQ_B10 := [
	[0, "", null, "start: tablet on the hip, front view"],
	[30, "tab", true, "1. Tab down (short press)"],
	[32, "tab", false, "1. Tab up -> SHORT: uninterrupted one-hand raise"],
	[110, "tab", true, "2. Tab down (short press)"],
	[112, "tab", false, "2. Tab up -> SHORT: put the tablet back on the hip"],
	[170, "tab", true, "3. Tab down: raise again"],
	[172, "tab", false, "3. Tab up -> SHORT: raise starts"],
	[176, "tab", true, "3. Tab down: interrupt early in the raise"],
	[178, "tab", false, "3. Tab up -> SHORT: interrupted, back to the hip, screen never lights"],
	[250, "", null, "end"],
]
const SEQ_B11 := [
	[0, "", null, "start: lights on, default camera"],
	[30, "jump", true, "1. Space down: jump"],
	[34, "jump", false, "1. Space up"],
	[110, "jump", true, "2. Space down: jump again"],
	[114, "jump", false, "2. Space up"],
	[200, "switch", null, "3. LightSwitch.interact(): lights off (called by the capture script)"],
	[290, "switch", null, "4. LightSwitch.interact(): lights on (called by the capture script)"],
	[400, "", null, "end"],
]

var _seq: Array = []
var _front := false
var _name := ""
var _player: Humanoid
var _switch: Node
var _frame := 0
var _log: FileAccess
var _last := ""


func _ready() -> void:
	process_priority = 1000
	for a in OS.get_cmdline_user_args():
		if a == "seq=b10":
			_seq = SEQ_B10; _front = true; _name = "b10"
		elif a == "seq=b11":
			_seq = SEQ_B11; _name = "b11"
	var out_dir := OS.get_environment("A8_CAPTURE_LOG_DIR")
	_log = FileAccess.open(out_dir.path_join("capture-%s.log" % _name), FileAccess.WRITE)
	var base: Node = load(BASE_SCENE).instantiate()
	add_child(base)
	_player = base.get_node("Player") as Humanoid
	_switch = base.get_node("LightSwitch")
	await get_tree().process_frame
	if _front:
		(_player.get_node(CAMERA_PIVOT_PATH) as Node3D).rotation.y += PI
	_out("CAPTURE seq=%s renderer=%s adapter=%s window=%s" % [_name, RenderingServer.get_current_rendering_method(),
		RenderingServer.get_video_adapter_name(), get_window().size])


func _process(_delta: float) -> void:
	for e in _seq:
		if e[0] == _frame:
			match e[1]:
				"tab": _send_key(KEY_TAB, e[2])
				"jump": _send_key(KEY_SPACE, e[2])
				"switch": _switch.interact(_player)
			_out("EVENT frame=%d t=%.3f %s | %s" % [_frame, _frame / FPS, e[3], _state()])
	var s := _state()
	if s != _last:
		_out("CHANGE frame=%d t=%.3f | %s" % [_frame, _frame / FPS, s])
		_last = s
	if _frame >= _seq[-1][0]:
		_log.close()
		get_tree().quit()
	_frame += 1


## Real mouse events are dropped during the capture: when the tablet goes back to the hip the game captures the
## mouse, and the cursor jump turned the camera in the first take. The scripted keys are the only input.
func _input(event: InputEvent) -> void:
	if event is InputEventMouse:
		get_viewport().set_input_as_handled()


func _state() -> String:
	var lights: Node = _switch.ceiling_lights
	return "hold=%s lit=%s raising=%s on_floor=%s lights_on=%s" % [["NONE", "ONE_HAND", "TWO_HAND"][_player.get_tablet_hold()],
		_player.is_tablet_screen_lit(), _player.is_raising_tablet(), _player.is_on_floor(), lights.is_lights_on()]


func _out(line: String) -> void:
	print(line)
	if _log != null:
		_log.store_line(line)


func _send_key(code: Key, pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.pressed = pressed
	Input.parse_input_event(ev)
