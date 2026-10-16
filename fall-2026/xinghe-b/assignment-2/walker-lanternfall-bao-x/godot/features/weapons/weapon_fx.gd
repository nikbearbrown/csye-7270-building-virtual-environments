extends Node2D
## Draws orbiting moths and the Sunflare ring from session data.
const Tuning = preload("res://features/tuning.gd")
const Art = preload("res://features/art.gd")

var session
var moth_tex: Texture2D
var flare_tex: Texture2D

func _ready() -> void:
	z_index = 3
	reload()

func reload() -> void:
	moth_tex = Art.texture(Art.ORBIT_MOTH)
	flare_tex = Art.texture(Art.SUNFLARE)

## The burst ring is hidden once the run has ended so the result panel reads cleanly.
func ring_visible() -> bool:
	return session != null and session.sunflare_ring > 0 and not session.state.is_terminal()

func _process(_d: float) -> void:
	queue_redraw()

func _draw() -> void:
	if session == null or session.prog == null:
		return
	for p in session.orbit_positions():
		if moth_tex:
			draw_texture(moth_tex, p - moth_tex.get_size() / 2)
		else:
			draw_circle(p, 4, Color("#FFF1C9"))
	if ring_visible():
		var t := 1.0 - float(session.sunflare_ring) / Tuning.SUNFLARE_RING_TICKS
		var r := Tuning.SUNFLARE_RADIUS * t
		var c: Vector2 = session.player.position
		if flare_tex:
			draw_texture_rect(flare_tex, Rect2(c - Vector2(r, r), Vector2(r, r) * 2), false, Color(1, 1, 1, 1.0 - t))
		else:
			draw_arc(c, r, 0, TAU, 64, Color(0.95, 0.72, 0.29, 1.0 - t), 4.0)
