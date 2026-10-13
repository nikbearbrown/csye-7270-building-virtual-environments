extends Node2D
# Capture C03 (beat B03): a script-driven marker (moves by delta) beside a pulse square (moves by TIME). The game's time scale drops to one half, then the tree is paused.
# 30 fps, 12 s (360 frames), driven by a FRAME counter (not delta, which the time scale would change).
#   frames   0..83   normal
#   frames  84..209  Engine.time_scale = 0.5          (2.8 s to 7.0 s)
#   frames 210..227  Engine.time_scale = 1.0          (7.0 s to 7.6 s)
#   frame  228..     SceneTree.paused = true           (7.6 s to the end): the marker freezes, the pulse carries on
# Layout: a grey track from x 0.10 to 0.90 at y 0.28; a teal marker (0.05 of the height square) runs along it at 0.20 of the width per game second and wraps;
# the pulse square is centred (0.50, 0.68), 0.34 of the height square.
const C = preload("res://scenes/scene_common.gd")
const MARKER_SCRIPT := "extends ColorRect\nvar track_w := 0.0\nvar start_x := 0.0\nvar speed := 0.0\nfunc _process(delta):\n\tposition.x += speed * delta\n\tif position.x > start_x + track_w:\n\t\tposition.x = start_x\n"
var frame := 0

func _ready() -> void:
	C.stage()
	process_mode = Node.PROCESS_MODE_ALWAYS            # this controller keeps counting frames while the tree is paused
	var vp := get_viewport_rect().size
	add_child(C.plain_rect(Color("#BDB8AC"), Vector2(vp.x * 0.10, vp.y * 0.28 - 2), Vector2(vp.x * 0.80, 4)))
	var side := vp.y * 0.05
	var marker := C.plain_rect(C.TEAL, Vector2(vp.x * 0.10, vp.y * 0.28 - side / 2), Vector2(side, side))
	var s := GDScript.new()
	s.source_code = MARKER_SCRIPT
	s.reload()
	marker.set_script(s)
	marker.process_mode = Node.PROCESS_MODE_PAUSABLE   # the marker obeys the pause
	marker.set("track_w", vp.x * 0.80 - side)
	marker.set("start_x", vp.x * 0.10)
	marker.set("speed", vp.x * 0.20)
	add_child(marker)
	var big := vp.y * 0.34
	add_child(C.shaded_rect(C.shader_text("02-pulse.gdshader"), Vector2(vp.x * 0.5 - big / 2, vp.y * 0.68 - big / 2), Vector2(big, big)))
	if C.wants_verify():
		add_child(C.shaded_rect(C.ENCODER, Vector2(0, 0), Vector2(20, 20)))

func _process(_delta: float) -> void:
	frame += 1
	if frame == 84:
		Engine.time_scale = 0.5
		print("EVENT frame=%d time_scale 0.5" % frame)
	elif frame == 210:
		Engine.time_scale = 1.0
		print("EVENT frame=%d time_scale 1.0" % frame)
	elif frame == 228:
		get_tree().paused = true
		print("EVENT frame=%d paused" % frame)
