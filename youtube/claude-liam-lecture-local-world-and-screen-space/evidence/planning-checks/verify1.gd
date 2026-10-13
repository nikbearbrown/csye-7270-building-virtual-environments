extends SceneTree
# verify1.gd: baseline built-in values. Run: godot --path <project dir> --script res://verify1.gd
# S1: a full-view ColorRect, no camera: FRAGCOORD / VERTEX (fragment) / SCREEN_UV / SCREEN_PIXEL_SIZE / TEXTURE_PIXEL_SIZE at three pixels.
# S2: a 128 px Sprite2D at world (600,400), Camera2D at (840,460): the three addresses of the sprite's top-left corner.

const Lib := preload("res://probe_lib.gd")


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	var lib := Lib.new(self)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)
	var probe := lib.grab()
	lib.out("env", {"engine": Engine.get_version_info()["string"], "root_size": [root.size.x, root.size.y],
		"image_size": [probe.get_width(), probe.get_height()], "adapter": RenderingServer.get_video_adapter_name(),
		"renderer": RenderingServer.get_current_rendering_method(), "canvas_transform": str(root.get_canvas_transform())})

	# ---- S1: full-view ColorRect, no camera
	var mat := lib.make_enc_material()
	var rect := ColorRect.new()
	rect.size = Vector2(1280, 720)
	rect.material = mat
	root.add_child(rect)
	await lib.frames(2)
	var pts := [[0, 0], [639, 359], [1279, 719]]
	var res := {}
	for p in pts:
		var key := "%d,%d" % [p[0], p[1]]
		res[key] = {
			"FRAGCOORD": [await lib.read(mat, 8, 1.0, p[0], p[1]), await lib.read(mat, 9, 1.0, p[0], p[1])],
			"FRAGCOORD_x2": [await lib.read(mat, 8, 2.0, p[0], p[1]), await lib.read(mat, 9, 2.0, p[0], p[1])],
			"VERTEX_in_fragment_x2": [await lib.read(mat, 6, 2.0, p[0], p[1]), await lib.read(mat, 7, 2.0, p[0], p[1])],
			"SCREEN_UV_x50000": [await lib.read(mat, 10, 50000.0, p[0], p[1]), await lib.read(mat, 11, 50000.0, p[0], p[1])],
			"SCREEN_PIXEL_SIZE_x1e6": [await lib.read(mat, 12, 1000000.0, p[0], p[1]), await lib.read(mat, 13, 1000000.0, p[0], p[1])],
			"TEXTURE_PIXEL_SIZE_x1000_ColorRect_no_art": [await lib.read(mat, 14, 1000.0, p[0], p[1]), await lib.read(mat, 15, 1000.0, p[0], p[1])],
		}
	lib.out("S1-colorrect-no-camera", res)
	rect.queue_free()
	await lib.frames(2)

	# ---- S2: sprite at world (600,400), camera at (840,460) -> canvas transform translation (-200,-100)
	var cam := Camera2D.new()
	cam.position = Vector2(840, 460)
	root.add_child(cam)
	cam.make_current()
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(600, 400)
	var mat2 := lib.make_enc_material()
	spr.material = mat2
	root.add_child(spr)
	await lib.frames(4)
	var ct := root.get_canvas_transform()
	var corner_px := [336, 236]   # expected screen pixel of the sprite's top-left corner
	var r2 := {"canvas_transform_origin": [ct.origin.x, ct.origin.y], "sprite_global_position": [spr.global_position.x, spr.global_position.y]}
	for name_i in [[0, "local.x"], [1, "local.y"], [2, "world.x"], [3, "world.y"], [4, "screen_by_matrices.x"], [5, "screen_by_matrices.y"],
			[6, "VERTEX_in_fragment.x"], [7, "VERTEX_in_fragment.y"], [8, "FRAGCOORD.x"], [9, "FRAGCOORD.y"]]:
		r2[name_i[1]] = await lib.read(mat2, name_i[0], 1.0, corner_px[0], corner_px[1])
	r2["TEXTURE_PIXEL_SIZE_x1e6_128px_sprite"] = [await lib.read(mat2, 14, 1000000.0, 400, 300), await lib.read(mat2, 15, 1000000.0, 400, 300)]
	# GDScript's own answer for the same corner, by the docs' chain
	var local_corner := Vector2(-64, -64)
	r2["gdscript_global_transform_x_local"] = [(spr.get_global_transform() * local_corner).x, (spr.get_global_transform() * local_corner).y]
	var with_canvas := spr.get_global_transform_with_canvas() * local_corner
	r2["gdscript_global_transform_with_canvas_x_local"] = [with_canvas.x, with_canvas.y]
	var screen_c := get_root().get_screen_transform() * with_canvas
	r2["gdscript_screen_transform_x_that"] = [screen_c.x, screen_c.y]
	lib.out("S2-sprite-600-400-camera-840-460", r2)
	quit(0)
