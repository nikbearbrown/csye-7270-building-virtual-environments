extends CanvasLayer
## All on-screen text and bars. Every event that has a sound also has a visual here or on the sprite.

const GameState = preload("res://game/game_state.gd")
const Tuning = preload("res://features/tuning.gd")
const Progression = preload("res://features/progression/progression.gd")
const PlayerScript = preload("res://features/player/player.gd")
const Art = preload("res://features/art.gd")

const W := 640.0
const H := 360.0
const INK := Color("#14121C")
const CREAM := Color("#FFF1C9")
const GOLD := Color("#F2B84B")
const RED := Color("#B5523B")
const MIST := Color("#C7D0E0")

var session
var view: Control
var card_cursor := 0
var portrait: Texture2D
var _lines := PackedStringArray()

func setup(s) -> void:
	session = s
	layer = 10
	view = Control.new()
	view.size = Vector2(W, H)
	view.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(view)
	view.draw.connect(_draw_view)
	portrait = Art.texture(Art.PC_SHEET)
	s.state.changed.connect(_on_state_changed)

func _on_state_changed(_from: int, to: int) -> void:
	if to == GameState.LEVELUP:
		card_cursor = 0

func _process(_d: float) -> void:
	view.queue_redraw()

func move_card(delta: int) -> void:
	card_cursor = wrapi(card_cursor + delta, 0, maxi(1, session.offered.size()))

## Text currently on screen; rebuilt from state so tests can read it without drawing.
func lines() -> PackedStringArray:
	_lines = PackedStringArray()
	var st: int = session.state.current
	_lines.append("MUSIC %s  SFX %s  [M/9/0]" % ["off" if _muted("Music") or _muted("Master") else "on", "off" if _muted("SFX") or _muted("Master") else "on"])
	if st == GameState.MENU:
		_lines.append_array(["LANTERNFALL", "Survive the fog for 3:00", "Move: WASD / arrows / left stick", "Enter / A to start"])
		return _lines
	var secs: int = session.tick_count / Tuning.TICK_HZ
	_lines.append("%d:%02d" % [secs / 60, secs % 60])
	_lines.append("HP %d/%d" % [session.player.hp, session.player.max_hp])
	_lines.append("Lv %d   XP %d/%d" % [session.prog.level, session.prog.xp, session.prog.xp_needed()])
	_lines.append("Kills %d" % session.kills)
	if session.prog.evolved_sunflare:
		_lines.append("Sunflare Lighthouse")
	else:
		_lines.append("Beam %d/3  Moths %d/3" % [session.prog.beam_level, session.prog.moth_level])
	if session.banner_ticks > 0 and st == GameState.PLAYING:
		_lines.append("SUNFLARE LIGHTHOUSE")
	match st:
		GameState.LEVELUP:
			for i in session.offered.size():
				var t: Array = Progression.CARD_TEXT[session.offered[i]]
				_lines.append("[%d] %s — %s" % [i + 1, session.prog.card_title(session.offered[i]), t[1]])
		GameState.PAUSED:
			_lines.append("PAUSED — Esc/P resume · R restart")
		GameState.LOST:
			_lines.append("The lamp went out — %d:%02d" % [secs / 60, secs % 60])
			_lines.append("R / Y to retry")
		GameState.WON:
			_lines.append("3:00 — The fog lifts")
			_lines.append("R / Y to play again")
	return _lines

func _muted(bus: String) -> bool:
	var i := AudioServer.get_bus_index(bus)
	return i >= 0 and AudioServer.is_bus_mute(i)

func _text(pos: Vector2, s: String, size := 12, color := CREAM, align := HORIZONTAL_ALIGNMENT_LEFT, width := -1.0) -> void:
	view.draw_string(ThemeDB.fallback_font, pos, s, align, width, size, color)

func _pose(p: String, rect: Rect2) -> void:
	if portrait:
		var i := PlayerScript.POSES.find(p)
		view.draw_texture_rect_region(portrait, rect, Rect2(i * 32, 0, 32, 32))

func _draw_view() -> void:
	var l := lines()
	var st: int = session.state.current
	_text(Vector2(0, 14), l[0], 9, MIST, HORIZONTAL_ALIGNMENT_RIGHT, W - 6)
	if st == GameState.MENU:
		view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.55))
		_pose("turn_front", Rect2(W / 2 - 48, 70, 96, 96))
		_text(Vector2(0, 200), l[1], 32, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
		_text(Vector2(0, 228), l[2], 12, CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
		_text(Vector2(0, 250), l[3], 10, MIST, HORIZONTAL_ALIGNMENT_CENTER, W)
		_text(Vector2(0, 300), l[4], 14, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
		return
	var p = session.player
	if p.iframes > Tuning.IFRAME_TICKS - 10:
		view.draw_rect(Rect2(0, 0, W, H), Color(RED, 0.22))
	view.draw_rect(Rect2(8, 8, 120, 10), Color(INK, 0.8))
	view.draw_rect(Rect2(8, 8, 120.0 * p.hp / p.max_hp, 10), RED)
	_text(Vector2(10, 30), l[2], 10)
	_text(Vector2(0, 20), l[1], 16, CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
	_text(Vector2(10, 44), l[3] + "   " + l[4], 10, MIST)
	_text(Vector2(10, 58), l[5], 10, GOLD)
	var prog = session.prog
	view.draw_rect(Rect2(0, H - 6, W, 6), Color(INK, 0.8))
	view.draw_rect(Rect2(0, H - 6, W * float(prog.xp) / prog.xp_needed(), 6), GOLD)
	if session.banner_ticks > 0 and st == GameState.PLAYING:
		view.draw_rect(Rect2(0, 120, W, 40), Color(INK, 0.7))
		_text(Vector2(0, 148), "SUNFLARE LIGHTHOUSE", 22, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
	match st:
		GameState.LEVELUP:
			view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.6))
			_text(Vector2(0, 70), "LEVEL UP — choose one", 18, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
			for i in session.offered.size():
				var r := Rect2(40 + i * 195, 90, 175, 190)
				var t: Array = Progression.CARD_TEXT[session.offered[i]]
				view.draw_rect(r, CREAM if i != card_cursor else GOLD)
				view.draw_rect(r, INK, false, 2.0)
				_text(r.position + Vector2(8, 22), "[%d]" % (i + 1), 12, INK)
				_text(r.position + Vector2(8, 60), session.prog.card_title(session.offered[i]), 13, INK, HORIZONTAL_ALIGNMENT_LEFT, r.size.x - 16)
				_text(r.position + Vector2(8, 90), t[1], 10, INK, HORIZONTAL_ALIGNMENT_LEFT, r.size.x - 16)
			_pose("levelup", Rect2(8, H - 104, 96, 96))
		GameState.PAUSED:
			view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.6))
			_text(Vector2(0, 180), "PAUSED", 28, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
			_text(Vector2(0, 210), "Esc/P resume · R restart · M/9/0 audio", 11, CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
		GameState.LOST, GameState.WON:
			var won := st == GameState.WON
			if won:
				# P9: the fog lifts — the screen washes towards mist while the camera pulls back
				view.draw_rect(Rect2(0, 0, W, H), Color(MIST, 0.45 * session.camera.fog_lift()))
				view.draw_rect(Rect2(0, 44, W, 262), Color(INK, 0.55))
			else:
				view.draw_rect(Rect2(0, 0, W, H), Color(INK, 0.65))
			_pose("victory" if won else "defeat", Rect2(W / 2 - 64, 60, 128, 128))
			_text(Vector2(0, 220), l[-2], 22, GOLD if won else CREAM, HORIZONTAL_ALIGNMENT_CENTER, W)
			_text(Vector2(0, 246), "Kills %d · Level %d" % [session.kills, prog.level], 12, MIST, HORIZONTAL_ALIGNMENT_CENTER, W)
			_text(Vector2(0, 280), l[-1], 14, GOLD, HORIZONTAL_ALIGNMENT_CENTER, W)
