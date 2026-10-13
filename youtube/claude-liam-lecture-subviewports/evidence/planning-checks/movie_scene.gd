extends Node2D
# SubViewports film, capture adapter rehearsal (scale 1, Movie Maker): builds one CaptureScene and steps it by 1/30 s per rendered frame.
# The scene never reads the wall clock; update(t) is called with t rising frame by frame from 0 (its one-shot events fire once, so t must not jump or go back).
#   godot --path <project> --always-on-top --write-movie out/f.png --fixed-fps 30 --quit-after N -- c21 [speed=0.95] [skip=1]
#   speed  scene seconds per clip second (default 1): events at scene time T land at clip time T / speed. Use it once, after the voice, to bring a scene's events onto their words.
#   skip   number of frames held at t = 0 before the clock starts (default 0); drop that many files from the start of the sequence. Frame 0 of a recording lacks the pictures of a SubViewport (run-13b): skip=1 gives a first kept frame that has them.
# --always-on-top matters: a Godot window that other windows cover is drawn on only some frames, and Movie Maker then writes repeated frames (RESULTS.md, the covered window).
var sc: CaptureScene
var frame := 0
var speed := 1.0

func _ready() -> void:
	var id := "c21"
	var skip := 0
	for a: String in OS.get_cmdline_user_args():
		if a.begins_with("speed="):
			speed = float(a.substr(6))
		elif a.begins_with("skip="):
			skip = int(a.substr(5))
		else:
			id = a
	sc = CaptureScene.new(id)
	sc.build(self)
	frame = -skip

func _process(_delta: float) -> void:
	sc.update(maxf(float(frame), 0.0) / 30.0 * speed)
	frame += 1
