extends Node3D
## A7 film capture: scripted-input recording of the tablet animations (NOT a human playtest).
## Runs only in the isolated copy of commit 42d6cc0d. Loads the unmodified res://base.tscn, turns the player's own
## camera pivot 180 degrees (same as previews/tablet_raise_preview.gd --front) so the character's front is filmed,
## and sends Tab presses with Input.parse_input_event (InputEventKey, physical_keycode KEY_TAB, as the InputMap binds it).
## player_controller.gd: held < 0.4 s then released = SHORT (on release); held >= 0.4 s = LONG (fires on the crossing tick).
## Raise clip phases (CHANGE-BRIEF): anticipation clip frames 0-6, active 7-15, recovery 16-20 (30 fps clip).
## Two-hand turns the body to face the camera's look direction, so the two-hand segments are kept for last.
## Run: godot --path <copy> res://film_capture/tablet_capture.tscn --write-movie <dir>/frame.png --fixed-fps 30 --resolution 1920x1080

const BASE_SCENE := "res://base.tscn"
const CAMERA_PIVOT_PATH := "PlayerController/CameraPivot"
const LOG_PATH := "<film-work>/a7/logs/capture-log.txt"
const TIMELINE_PATH := "<film-work>/a7/captures/play-01-timeline.txt"
const FPS := 30.0

# [movie frame, pressed, label]
var events := [
	[0, null, "start: character at waist idle (tablet on hip), front view"],
	[30, true, "1. Tab down (short press): uninterrupted one-hand raise"],
	[32, false, "1. Tab up -> SHORT: raise_1h starts"],
	[100, true, "2. Tab down (short press): put back to waist"],
	[102, false, "2. Tab up -> SHORT: one-hand -> waist (hold_1h -> hip, 0.2 s blend)"],
	[150, true, "3a. Tab down: raise again"],
	[152, false, "3a. Tab up -> SHORT: raise_1h starts"],
	[154, true, "3a. Tab down: interrupt in ANTICIPATION"],
	[156, false, "3a. Tab up -> SHORT at raise clip ~frame 4 (anticipation): put back to waist"],
	[210, true, "3b. Tab down: raise again"],
	[212, false, "3b. Tab up -> SHORT: raise_1h starts"],
	[220, true, "3b. Tab down: interrupt in ACTIVE"],
	[222, false, "3b. Tab up -> SHORT at raise clip ~frame 10 (active): put back to waist"],
	[270, true, "3c. Tab down: raise again"],
	[272, false, "3c. Tab up -> SHORT: raise_1h starts"],
	[289, true, "3c. Tab down: interrupt in RECOVERY"],
	[291, false, "3c. Tab up -> SHORT at raise clip ~frame 19 (recovery): put back to waist"],
	[340, true, "3d. Tab down: raise again"],
	[342, false, "3d. Tab up -> SHORT: raise_1h starts"],
	[343, true, "3d. Tab down and HOLD: long press will fire 0.4 s later"],
	[355, null, "3d. (expected) LONG fires at raise clip ~frame 13 (active): raise -> two-hand"],
	[365, false, "3d. Tab up (long press already counted)"],
	[420, true, "4a. Tab down (short press): two-hand -> one-hand"],
	[422, false, "4a. Tab up -> SHORT: hold_2h -> hold_1h"],
	[480, true, "4b. Tab down and HOLD: one-hand -> two-hand"],
	[500, false, "4b. Tab up (LONG fired ~0.4 s after down)"],
	[560, true, "4c. Tab down and HOLD: two-hand -> waist"],
	[580, false, "4c. Tab up (LONG fired ~0.4 s after down): hold_2h -> hip"],
	[640, true, "4d. Tab down and HOLD: waist -> two-hand directly"],
	[660, false, "4d. Tab up (LONG fired ~0.4 s after down): hip -> hold_2h"],
	[720, true, "4e. Tab down and HOLD: two-hand -> waist"],
	[740, false, "4e. Tab up (LONG fired): hold_2h -> hip"],
	[790, null, "end"],
]
const END_FRAME := 790

var _player: Node
var _playback: AnimationNodeStateMachinePlayback
var _frame := 0
var _log: FileAccess
var _timeline: FileAccess
var _last_hold := -1
var _last_state := &""


func _ready() -> void:
	process_priority = 1000
	_log = FileAccess.open(LOG_PATH, FileAccess.WRITE)
	_timeline = FileAccess.open(TIMELINE_PATH, FileAccess.WRITE)
	var base: Node = load(BASE_SCENE).instantiate()
	add_child(base)
	_player = base.get_node("Player")
	await get_tree().process_frame
	_playback = _player.get_node("AnimationTree").get("parameters/playback")
	var pivot := _player.get_node(CAMERA_PIVOT_PATH) as Node3D
	pivot.rotation.y += PI
	_out("CAPTURE renderer=%s adapter=%s window=%s physics_hz=%d" % [RenderingServer.get_current_rendering_method(),
		RenderingServer.get_video_adapter_name(), get_window().size, Engine.physics_ticks_per_second])
	_timeline.store_line("# play-01.mp4 timeline (30 fps; time = movie frame / 30). Scripted input, not a playtest.")
	_timeline.store_line("# time_s\tframe\tevent")


func _process(_delta: float) -> void:
	for e in events:
		if e[0] == _frame:
			if e[1] != null:
				_send_tab(e[1])
			_out("INPUT frame=%d t=%.3f %s | %s" % [_frame, _frame / FPS, "" if e[1] == null else ("TAB_DOWN" if e[1] else "TAB_UP"), _state_str()])
			_timeline.store_line("%.3f\t%d\t%s" % [_frame / FPS, _frame, e[2]])
	if _playback != null:
		var hold: int = _player.get_tablet_hold()
		var st := _playback.get_current_node()
		if hold != _last_hold or st != _last_state:
			_out("CHANGE frame=%d t=%.3f | %s" % [_frame, _frame / FPS, _state_str()])
			_timeline.store_line("%.3f\t%d\t  [engine] %s" % [_frame / FPS, _frame, _state_str()])
			_last_hold = hold
			_last_state = st
		_log.store_line("FRAME %d %s" % [_frame, _state_str()])
	if _frame >= END_FRAME:
		_log.close()
		_timeline.close()
		get_tree().quit()
	_frame += 1


func _state_str() -> String:
	if _playback == null:
		return "(tree not ready)"
	return "hold=%s state=%s clip_pos=%.4f fading_from=%s lit=%s raising=%s" % [["NONE", "ONE_HAND", "TWO_HAND"][_player.get_tablet_hold()],
		_playback.get_current_node(), _playback.get_current_play_position(), _playback.get_fading_from_node(),
		_player.is_tablet_screen_lit(), _player.is_raising_tablet()]


func _out(line: String) -> void:
	print(line)
	if _log != null:
		_log.store_line(line)


func _send_tab(pressed: bool) -> void:
	var ev := InputEventKey.new()
	ev.keycode = KEY_TAB
	ev.physical_keycode = KEY_TAB
	ev.pressed = pressed
	Input.parse_input_event(ev)
