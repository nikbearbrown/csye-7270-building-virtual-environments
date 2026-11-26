extends Node
## A8 pitch film capture, part 2: scripted input for the tablet OS, the walking rule, the light dust and ThoughtPad.
## NOT a human playtest. Runs only in the isolated copy of commit f13431bf.
## Keys and mouse events are sent with Input.parse_input_event. Injected mouse events carry device INJECT_DEVICE;
## every other mouse event (the real mouse) is dropped, so the real cursor cannot move the camera.
## Movie Maker does not record the system cursor, so a white arrow is drawn where the injected mouse is.
## To click on the held tablet, the script finds the screen point whose ray hits the wanted spot of the tablet screen,
## using the game's own PlayerController._get_mouse_screen_uv() (the same function a real click goes through).
## User args (after --): seq=tablet | seq=dust | seq=mome1 | seq=mome2
## Run: godot --path <copy> res://film_capture/a8_capture_os.tscn --write-movie <dir>/frame.png --fixed-fps 30 --resolution 1920x1080 -- seq=tablet

const BASE_SCENE := "res://base.tscn"
const MOME_SCENE_1 := "res://debug/thought_pad/mome_demo.tscn"
const MOME_SCENE_2 := "res://film_capture/mome_demo_doc2.tscn"
const INJECT_DEVICE := 99
const FPS := 30.0

var _name := ""
var _frame := 0
var _log: FileAccess
var _player: Humanoid
var _controller: Node
var _os_viewport: SubViewport
var _scene: Node
var _cursor: Polygon2D
var _cursor_layer: CanvasLayer
var _mouse := Vector2(960, 540)


func _ready() -> void:
	process_priority = 1000
	for a in OS.get_cmdline_user_args():
		if a.begins_with("seq="):
			_name = a.substr(4)
	_log = FileAccess.open(OS.get_environment("A8_CAPTURE_LOG_DIR").path_join("capture-%s.log" % _name), FileAccess.WRITE)
	_make_cursor()
	match _name:
		"tablet":
			await _load_base()
			await _seq_tablet()
		"dust":
			await _load_base()
			await _seq_dust()
		"mome1":
			await _load_scene(MOME_SCENE_1)
			await _seq_mome(false)
		"mome2":
			await _load_scene(MOME_SCENE_2)
			await _seq_mome(true)
	_out("END frame=%d" % _frame)
	_log.close()
	get_tree().quit()


func _process(_delta: float) -> void:
	_frame += 1


func _input(event: InputEvent) -> void:
	if event is InputEventMouse and event.device != INJECT_DEVICE:
		get_viewport().set_input_as_handled()


# ---------------------------------------------------------------- sequences

func _seq_tablet() -> void:
	_cursor.visible = false
	await _wait(30)
	_mark("B00 1. short Tab: one-hand raise")
	await _tap_key(KEY_TAB, 2)
	await _wait(60)
	_mark("B00 2. long Tab: one hand -> two hands")
	await _tap_key(KEY_TAB, 18)
	await _wait(45)
	_cursor.visible = true
	var os := _os_viewport.get_node("TabletOS")
	_mouse = _screen_for_os_point(Vector2(640, 420))
	_place_cursor()
	await _wait(10)
	_mark("B07 1. double-click This PC")
	await _move_to(_screen_for_os_point(_center(os.get_node("Desktop/ThisPCIcon"))), 20)
	await _double_click()
	await _wait(30)
	var win: Control = os.get_node("WindowLayer").get_child(-1)
	var entries: ItemList = win.find_child("EntryList")
	_mark("B07 2. double-click the first folder (%s)" % (entries.get_item_text(0) if entries.item_count > 0 else "none"))
	var r := entries.get_item_rect(0)
	await _move_to(_screen_for_os_point(entries.get_global_transform() * (r.position + r.size * 0.5)), 20)
	await _double_click()
	await _wait(30)
	_mark("B07 3. click Up")
	await _move_to(_screen_for_os_point(_center(win.find_child("UpButton"))), 18)
	await _click()
	await _wait(30)
	_mark("B07 4. click minimize")
	await _move_to(_screen_for_os_point(_center(win.find_child("MinimizeButton"))), 20)
	await _click()
	await _wait(30)
	var task_buttons := os.get_node("Taskbar/Row/TaskbarButtons")
	if task_buttons.get_child_count() > 0:
		_mark("B07 5. click the taskbar button: window back")
		await _move_to(_screen_for_os_point(_center(task_buttons.get_child(0))), 20)
		await _click()
		await _wait(30)
	_mark("B07 6. click show desktop")
	await _move_to(_screen_for_os_point(_center(os.get_node("Taskbar/Row/ShowDesktopButton"))), 22)
	await _click()
	await _wait(40)
	_cursor.visible = false
	_mark("B13 1. hold W with two hands: the body must not move")
	await _hold_key(KEY_W, 45)
	await _wait(15)
	_mark("B13 2. short Tab: two hands -> one hand")
	await _tap_key(KEY_TAB, 2)
	await _wait(30)
	_mark("B13 3. hold W with one hand: the body walks")
	await _hold_key(KEY_W, 50)
	await _wait(30)


func _seq_dust() -> void:
	_cursor.visible = false
	var pivot := _controller.get_node("CameraPivot") as Node3D
	await _wait(15)
	_mark("dust 1. camera pitched up by the capture script")
	var start := pivot.rotation.x
	for i in 45:
		pivot.rotation.x = lerpf(start, deg_to_rad(float(OS.get_environment("A8_DUST_PITCH"))), (i + 1) / 45.0)
		await get_tree().process_frame
	await _wait(300)


func _seq_mome(editable: bool) -> void:
	var text_edit: TextEdit = _scene.find_child("TextEdit")
	_mouse = Vector2(960, 700)
	_place_cursor()
	await _wait(20)
	var line_rect := Rect2(text_edit.get_global_rect().position + Vector2(12, 8), Vector2(300, 24))
	_mark("mome 1. drag to select the first words")
	await _move_to(line_rect.position + Vector2(0, 12), 20)
	await _drag_to(line_rect.position + Vector2(220, 12), 20)
	await _wait(25)
	_mark("mome 2. click at the end of the text and type")
	await _move_to(text_edit.get_global_rect().position + Vector2(text_edit.size.x * 0.6, 70), 15)
	await _click()
	await _type(" Clue from the north gate." if editable else " Can I type here?")
	await _wait(45)
	_out("TEXT after typing: %s" % text_edit.text.replace("\n", "\\n"))


# ---------------------------------------------------------------- input helpers

func _key(code: Key, pressed: bool, unicode := 0) -> void:
	var ev := InputEventKey.new()
	ev.keycode = code
	ev.physical_keycode = code
	ev.unicode = unicode
	ev.pressed = pressed
	Input.parse_input_event(ev)


func _tap_key(code: Key, hold_frames: int) -> void:
	_key(code, true)
	await _wait(hold_frames)
	_key(code, false)


func _hold_key(code: Key, frames: int) -> void:
	var before := _player.global_position
	_key(code, true)
	await _wait(frames)
	_key(code, false)
	_out("MOVED %.3f m while holding (hold=%s)" % [before.distance_to(_player.global_position), _player.get_tablet_hold()])


func _type(text: String) -> void:
	for ch in text:
		var c := ch.unicode_at(0)
		var code: Key = KEY_SPACE if ch == " " else (KEY_PERIOD if ch == "." else (KEY_QUESTION if ch == "?" else OS.find_keycode_from_string(ch.to_upper())))
		_key(code, true, c)
		await _wait(1)
		_key(code, false, 0)
		await _wait(2)


func _mouse_event_button(pressed: bool, double := false) -> void:
	var ev := InputEventMouseButton.new()
	ev.device = INJECT_DEVICE
	ev.button_index = MOUSE_BUTTON_LEFT
	ev.pressed = pressed
	ev.double_click = double
	ev.button_mask = MOUSE_BUTTON_MASK_LEFT if pressed else 0
	ev.position = _to_window(_mouse)
	ev.global_position = ev.position
	Input.parse_input_event(ev)


func _mouse_motion(to: Vector2, held := false) -> void:
	var ev := InputEventMouseMotion.new()
	ev.device = INJECT_DEVICE
	ev.relative = _to_window(to) - _to_window(_mouse)
	ev.button_mask = MOUSE_BUTTON_MASK_LEFT if held else 0
	_mouse = to
	ev.position = _to_window(_mouse)
	ev.global_position = ev.position
	Input.parse_input_event(ev)
	_place_cursor()


## Injected events are read as window pixels; with Windows display scaling the window is larger than the
## 1920 x 1080 viewport (2048 x 1152 here), so viewport points are turned into window points first.
func _to_window(p: Vector2) -> Vector2:
	return get_viewport().get_final_transform() * p


func _move_to(to: Vector2, frames: int, held := false) -> void:
	var from := _mouse
	for i in frames:
		var t := smoothstep(0.0, 1.0, (i + 1) / float(frames))
		_mouse_motion(from.lerp(to, t), held)
		await get_tree().process_frame


func _click() -> void:
	_mouse_event_button(true)
	await _wait(3)
	_mouse_event_button(false)


func _double_click() -> void:
	_mouse_event_button(true)
	await _wait(2)
	_mouse_event_button(false)
	await _wait(3)
	_mouse_event_button(true, true)
	await _wait(2)
	_mouse_event_button(false)


func _drag_to(to: Vector2, frames: int) -> void:
	_mouse_event_button(true)
	await _wait(2)
	await _move_to(to, frames, true)
	_mouse_event_button(false)


## Finds the window point whose ray hits the tablet screen at the given point of the tablet OS canvas (Newton steps).
func _screen_for_os_point(os_point: Vector2) -> Vector2:
	var target := os_point / Vector2(_os_viewport.size)
	var p := get_viewport().get_visible_rect().size * 0.5
	for i in 12:
		var uv := _uv_at(p)
		var e := 2.0
		var jx := (_uv_at(p + Vector2(e, 0)) - uv) / e
		var jy := (_uv_at(p + Vector2(0, e)) - uv) / e
		var det := jx.x * jy.y - jy.x * jx.y
		if absf(det) < 1e-12:
			break
		var d := target - uv
		p += Vector2((d.x * jy.y - jy.x * d.y) / det, (jx.x * d.y - d.x * jx.y) / det)
	return p


func _uv_at(p: Vector2) -> Vector2:
	var ev := InputEventMouseMotion.new()
	ev.position = p
	return _controller._get_mouse_screen_uv(ev)


func _center(c: Control) -> Vector2:
	var r := c.get_global_rect()
	return r.position + r.size * 0.5


# ---------------------------------------------------------------- setup and log

func _load_base() -> void:
	_scene = load(BASE_SCENE).instantiate()
	add_child(_scene)
	_player = _scene.get_node("Player") as Humanoid
	_controller = _player.get_node("PlayerController")
	_os_viewport = _controller.get_node("TabletOSViewport")
	await get_tree().process_frame
	_out("CAPTURE seq=%s renderer=%s adapter=%s window=%s" % [_name, RenderingServer.get_current_rendering_method(),
		RenderingServer.get_video_adapter_name(), get_window().size])


func _load_scene(path: String) -> void:
	_scene = load(path).instantiate()
	add_child(_scene)
	await get_tree().process_frame
	_out("CAPTURE seq=%s scene=%s window=%s" % [_name, path, get_window().size])


func _make_cursor() -> void:
	_cursor_layer = CanvasLayer.new()
	_cursor_layer.layer = 120
	add_child(_cursor_layer)
	var outline := Polygon2D.new()
	outline.polygon = PackedVector2Array([Vector2(-2, -3), Vector2(-2, 26), Vector2(6, 19), Vector2(12, 31), Vector2(18, 28), Vector2(12, 17), Vector2(22, 17)])
	outline.color = Color(0.08, 0.08, 0.08)
	_cursor = Polygon2D.new()
	_cursor.polygon = PackedVector2Array([Vector2(0, 0), Vector2(0, 22), Vector2(6, 16), Vector2(12, 28), Vector2(15, 26), Vector2(10, 15), Vector2(18, 15)])
	_cursor.color = Color(1, 1, 1)
	_cursor.add_child(outline)
	outline.show_behind_parent = true
	_cursor_layer.add_child(_cursor)
	_place_cursor()


func _place_cursor() -> void:
	_cursor.position = _mouse


func _wait(n: int) -> void:
	for i in n:
		await get_tree().process_frame


func _mark(label: String) -> void:
	var s := ""
	if _player != null:
		s = " | hold=%s lit=%s pos=%s" % [_player.get_tablet_hold(), _player.is_tablet_screen_lit(), _player.global_position]
	_out("EVENT frame=%d t=%.3f %s%s" % [_frame, _frame / FPS, label, s])


func _out(line: String) -> void:
	print(line)
	if _log != null:
		_log.store_line(line)
