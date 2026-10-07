extends Control
## HUD (code-drawn, not generated): HP hearts top-left (UI-HEART), the one-line fail reason,
## the PAUSED overlay and the Cleared screen. Shows state; never changes it.

const PALE := Color("e8e6f0")
const EDGE := Color("1a1420")
const RED := Color("d62839")
const EMPTY := Color("2a1c24")
## 7x6 heart, one string per row.
const HEART := [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]

var hp := 5
var max_hp := 5

var _message: Label
var _sub: Label
var _dim: ColorRect
var _mutes: Label


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_dim = ColorRect.new()
	_dim.color = Color(0.03, 0.035, 0.05, 0.6)
	_dim.set_anchors_preset(Control.PRESET_FULL_RECT)
	_dim.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_dim.visible = false
	add_child(_dim)
	_message = _make_label(24, 140)
	_sub = _make_label(12, 172)
	_mutes = _make_label(10, 4)
	_mutes.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	_mutes.size.x = 632
	hide_message()


## Small note top-right while a bus is muted (M = music, N = sound effects).
func set_mutes(music_muted: bool, sfx_muted: bool) -> void:
	var parts: PackedStringArray = []
	if music_muted:
		parts.append("music off (M)")
	if sfx_muted:
		parts.append("sfx off (N)")
	_mutes.text = "  ".join(parts)


func mute_text() -> String:
	return _mutes.text


func _make_label(size: int, y: float) -> Label:
	var l := Label.new()
	var s := LabelSettings.new()
	s.font_size = size
	s.font_color = PALE
	s.outline_size = 4
	s.outline_color = EDGE
	l.label_settings = s
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.position = Vector2(0, y)
	l.size = Vector2(640, size + 8)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(l)
	return l


func set_hp(value: int, maximum: int) -> void:
	hp = value
	max_hp = maximum
	queue_redraw()


func show_fail(reason: String) -> void:
	_show(reason, "", false)


func show_paused(on: bool) -> void:
	if on:
		_show("PAUSED", "Esc to resume", true)
	else:
		hide_message()


func show_cleared() -> void:
	_show("CLEARED", "R to play again", true)


func hide_message() -> void:
	_message.visible = false
	_sub.visible = false
	_dim.visible = false


func message_text() -> String:
	return _message.text if _message.visible else ""


func _show(main_text: String, sub_text: String, dim: bool) -> void:
	_message.text = main_text
	_sub.text = sub_text
	_message.visible = true
	_sub.visible = not sub_text.is_empty()
	_dim.visible = dim


func _draw() -> void:
	for i in max_hp:
		_draw_heart(Vector2(8 + i * 10, 8), RED if i < hp else EMPTY)


func _draw_heart(at: Vector2, fill: Color) -> void:
	for pass_i in 2:
		for y in HEART.size():
			for x in HEART[y].length():
				if HEART[y][x] != "X":
					continue
				if pass_i == 0:
					draw_rect(Rect2(at + Vector2(x - 1, y - 1), Vector2(3, 3)), EDGE)
				else:
					draw_rect(Rect2(at + Vector2(x, y), Vector2(1, 1)), fill)
