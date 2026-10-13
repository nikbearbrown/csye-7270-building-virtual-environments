extends SceneTree
# broken.gd: load the deliberately broken shader (MODEL_MATRIX read inside fragment()) on a sprite and let the engine log its message.
# It first prints one line saying what fragment() is, so the film's terminal beat has the definition on screen where the word is first
# spoken (the first run, run-9-broken-shader-raw-log.log, had no such line; the engine's own lines are identical in both runs).
# Run: godot --path <project dir> --script res://broken.gd
const Scn := preload("res://scenes_lib.gd")


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	print("fragment() runs once for each pixel the shape covers; sets its color")
	root.size = Vector2i(640, 360)
	var s := Scn.sprite(Scn.white_texture(128), Vector2(320, 180), 1.0, Scn.material("04-broken-matrix-in-fragment.gdshader"))
	root.add_child(s)
	for i in range(4):
		await process_frame
	quit(0)
