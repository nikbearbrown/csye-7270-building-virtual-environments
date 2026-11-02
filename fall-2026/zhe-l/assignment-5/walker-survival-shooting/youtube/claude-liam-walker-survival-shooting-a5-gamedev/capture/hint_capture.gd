extends SceneTree
## Film capture for the A5 hint experiment. Runs ONLY in the isolated copy
## (a5/source/project-survival-shooting, exported from local commit 08839a7).
## Instantiates the unmodified res://experiments/hint/hint_experiment.tscn twice:
##   1. in the real window's own viewport -> get_viewport().get_texture().get_image()
##      (the method the assignment names); pixels read at each band centre;
##   2. inside a 3840x2160 SubViewport -> native 4K frame for the film; same pixels read.
## Band centres come from the scene's own Camera3D.unproject_position(), not guessed.
## It never edits or saves a scene, material, shader or texture.
## Usage: godot --path <copy> --script res://film_capture/hint_capture.gd -- out=<dir>

const BAND_X := [-0.4, 0.0, 0.4]          # quad is 1.2 m wide, 3 texels -> 0.4 m per band
const BAND_FILE_VALUE := [64, 128, 192]
const QUADS := ["QuadSourceColor", "QuadRaw"]
const SETTLE_FRAMES := 5

var out_dir := "user://capture"
var win_scene: Node3D
var vp: SubViewport
var vp_scene: Node3D
var frame := 0

func _initialize() -> void:
	for a in OS.get_cmdline_user_args():
		var kv := a.split("=", true, 1)
		if kv[0] == "out":
			out_dir = kv[1]
	DirAccess.make_dir_recursive_absolute(out_dir)
	var packed := load("res://experiments/hint/hint_experiment.tscn") as PackedScene
	win_scene = packed.instantiate()
	root.add_child(win_scene)
	vp = SubViewport.new()
	vp.size = Vector2i(3840, 2160)
	vp.own_world_3d = true
	vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(vp)
	vp_scene = packed.instantiate()
	vp.add_child(vp_scene)
	RenderingServer.frame_post_draw.connect(_on_post_draw)
	print("HINT_CAPTURE window_size=", root.size, " subviewport=", vp.size)
	print("renderer=", RenderingServer.get_current_rendering_method(), " adapter=", RenderingServer.get_video_adapter_name())

func _on_post_draw() -> void:
	frame += 1
	if frame < SETTLE_FRAMES:
		return
	RenderingServer.frame_post_draw.disconnect(_on_post_draw)
	_measure("window", win_scene, root.get_texture().get_image())
	_measure("4k", vp_scene, vp.get_texture().get_image())
	quit(0)

func _measure(tag: String, scene: Node3D, img: Image) -> void:
	var path := "%s/hint_%s_%dx%d.png" % [out_dir, tag, img.get_width(), img.get_height()]
	img.save_png(path)
	print("SAVED ", path, " format=", img.get_format())
	var cam := scene.get_node("Camera3D") as Camera3D
	for q in QUADS:
		var quad := scene.get_node(q) as MeshInstance3D
		for i in BAND_X.size():
			var world := quad.global_transform * Vector3(BAND_X[i], 0.0, 0.0)
			var px := cam.unproject_position(world)
			var p := Vector2i(roundi(px.x), roundi(px.y))
			var c := img.get_pixel(p.x, p.y)
			# 3x3 neighbourhood: all nine must agree, or the band centre is not uniform
			var same := true
			for dy in [-1, 0, 1]:
				for dx in [-1, 0, 1]:
					if img.get_pixel(p.x + dx, p.y + dy) != c:
						same = false
			print("BAND %s %s file=%d pixel=(%d,%d) rgb=(%d,%d,%d) 3x3_uniform=%s" % [
				tag, q, BAND_FILE_VALUE[i], p.x, p.y,
				roundi(c.r * 255.0), roundi(c.g * 255.0), roundi(c.b * 255.0), same])
