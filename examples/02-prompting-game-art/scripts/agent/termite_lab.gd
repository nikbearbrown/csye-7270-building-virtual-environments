extends Node2D
const Art = preload("res://features/player/clawd_art.gd")
var seconds: float = 0.0

func _process(delta: float) -> void:
	seconds += delta
	queue_redraw()

func _draw() -> void:
	var font := ThemeDB.fallback_font
	draw_rect(Rect2(0, 0, 640, 360), Color("faf9f5"))
	draw_string(font, Vector2(16, 22), "Termite lab — human inspection only; not a playtest", HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color("3d3929"))
	draw_string(font, Vector2(16, 40), "Soldiers at cut scale (48 px cell). Clawd at game scale (0.32).", HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color("888"))
	draw_line(Vector2(0, 280), Vector2(640, 280), Color("c8c5be"), 1)
	Art.paint(self, "idle", seconds, Vector2(90, 280))
	draw_string(font, Vector2(90, 298), "Clawd", HORIZONTAL_ALIGNMENT_CENTER, 80, 11, Color("3d3929"))
	for i: int in 3:
		var labels: Array = ["black", "red", "yellow"]
		draw_string(font, Vector2(280.0 + i * 100, 298), labels[i], HORIZONTAL_ALIGNMENT_CENTER, 80, 11, Color("3d3929"))
