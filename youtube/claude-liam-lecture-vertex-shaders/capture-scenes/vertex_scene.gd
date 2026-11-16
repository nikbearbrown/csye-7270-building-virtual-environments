extends Node
# Adapter between the shared capture harness and the film's scene library (capture_scenes.gd, copied from evidence/planning-checks/scratch-project/).
# Scene id from V_ID, clip length D from CLIP_L (events are fractions of D). The scene's own logical canvas (640 x 360 or 1280 x 720) is applied to the
# capture viewport via size_2d_override, so pixel numbers in the film are logical pixels. tick(ctx, t) runs before every draw with t = frame / 30.
var CS
var ctx: Dictionary
func harness_setup(c: Dictionary) -> void:
	CS = load("/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders/capture-scenes/capture_scenes.gd")
	var holder := Node2D.new()
	add_child(holder)
	var d := 12.0
	if OS.get_environment("CLIP_L") != "":
		d = float(OS.get_environment("CLIP_L"))
	ctx = CS.build(OS.get_environment("V_ID"), holder, "/Users/bear/Documents/CoWork/bear-textbooks/books/csye-7270-building-virtual-environments/youtube/claude-liam-lecture-vertex-shaders/lab-shaders", d)
	var canvas: Vector2i = ctx["canvas"]
	c["stage"].size_2d_override = canvas
func harness_frame(t: float) -> void:
	CS.tick(ctx, t)
