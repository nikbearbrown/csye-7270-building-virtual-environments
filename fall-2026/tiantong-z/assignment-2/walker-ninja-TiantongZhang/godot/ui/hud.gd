extends Control
var game: Node2D
const INK := Color("25354a")
# CONCEPT revision 1.3. The two HUD bands now sit on a dungeon instead of a
# cream sky, so they are dark and their text is light. The pop-up CARDS (menu,
# pause, complete, death) stay light with INK text: they are overlays that
# bring their own background, and a light card on a dark world is the clearest
# thing in the build. Only the bands changed.
const BAND := Color("1b1620")
const CHALK := Color("c6cedb")
# Death-screen geometry as named constants so the overlay and the starter's
# death panel can be asserted not to overlap. The first build put the cat
# straight over the panel and hid the death reason.
const DEATH_PANEL := Rect2(180, 128, 280, 68)
const DEATH_CAT := Rect2(476, 86, 150, 153)

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

func text_at(text: String, position: Vector2, size_px: int = 14, color: Color = INK) -> void:
	draw_string(ThemeDB.fallback_font, position, text, HORIZONTAL_ALIGNMENT_LEFT, -1, size_px, color)

func centered(text: String, y: float, font_size: int, color: Color = INK) -> void:
	var width := ThemeDB.fallback_font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	text_at(text, Vector2((640-width)/2, y), font_size, color)

func _draw() -> void:
	if not is_instance_valid(game):
		return
	draw_rect(Rect2(0,0,640,74), BAND)
	text_at("WALKER / JUMPMAN", Vector2(22,27), 18, CHALK)
	text_at("FIRST STEPS", Vector2(497,27), 14, CHALK)
	text_at("A/D move   Space jump x2   Shift dash   L-click slash   R retry   Esc pause   0 mute", Vector2(22,50), 13, CHALK)
	draw_rect(Rect2(22,63,596,3), Color("3a3344"))
	# Derived from the level instead of the starter's hard-coded 852, which was
	# (finish 916 - spawn 64) and stopped being true when the finish moved.
	var span: float = maxf(1.0, float(game.level.finish[0]) - float(game.level.spawn[0]))
	var progress: float = clampf((game.player.position.x - float(game.level.spawn[0])) / span, 0, 1)
	draw_rect(Rect2(22,63,596*progress,3), Color("287c68"))
	draw_rect(Rect2(0,335,640,25), BAND)
	text_at("No lives. Just another try.", Vector2(22,353), 13, CHALK)
	if game.muted:
		# Warm, so it cannot be mistaken for the chalk status text beside it. The
		# assignment requires the slice to be understandable with sound off, and
		# that claim is only testable if the player can see which state they are in.
		text_at("MUTED", Vector2(362,353), 13, Color("c89a5a"))
	text_at("RETRIES %02d     %04.1fs" % [game.deaths, game.elapsed], Vector2(440,353), 13, CHALK)
	# Death reaction. Drawn BEFORE the PLAYING early-return, because the
	# overlay is meant to outlast the 0.55 s respawn and stay up for as long
	# as the laugh is still going.
	if game.death_fx_remaining > 0.0 and game.cat_texture:
		draw_rect(DEATH_CAT.grow(4.0), CHALK)
		draw_texture_rect(game.cat_texture, DEATH_CAT, false)
	if game.state == game.State.PLAYING:
		return
	if game.state == game.State.DYING:
		draw_rect(DEATH_PANEL, Color("fff9ee"))
		centered(game.death_reason, 155, 21, Color("a23e36"))
		centered("Back at the start in a moment.", 180, 13)
		return
	draw_rect(Rect2(0,74,640,261), Color(0.10,0.16,0.20,0.16))
	draw_rect(Rect2(163,103,318,159), Color("fffdf7"))
	draw_rect(Rect2(163,103,318,4), Color("ef875f"))
	var title := "First steps. Real jumps."
	var detail := "Cross two gaps. Clear the spikes. Reach the flag."
	var button := "ENTER  /  START"
	if game.state == game.State.PAUSED:
		title = "Take a breath."
		detail = "R: restart attempt    M: main menu"
		button = "ENTER  /  RESUME"
	elif game.state == game.State.COMPLETE:
		title = "Course complete."
		detail = "%.1f seconds   /   %d retries" % [game.last_finish_time, game.deaths]
		button = "ENTER  /  PLAY AGAIN"
	centered(title, 143, 24)
	centered(detail, 177, 12)
	centered("Two jumps. One air dash. Unlimited retries.", 197, 12)
	draw_rect(Rect2(220,215,200,34), Color("287c68"))
	centered(button, 237, 14, Color("fffdf7"))
