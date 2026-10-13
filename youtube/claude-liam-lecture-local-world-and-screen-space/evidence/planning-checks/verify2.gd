extends SceneTree
# verify2.gd: do the ways of reading an address agree? One 128 px Sprite2D, seven setups.
# For each setup: read, at one pixel inside the sprite, local / world / screen-by-matrices / VERTEX in fragment() / FRAGCOORD.xy /
# SCREEN_UV / SCREEN_PIXEL_SIZE, and compare with the engine's own transforms computed in GDScript.
# Run: godot --path <project dir> --script res://verify2.gd

const Lib := preload("res://probe_lib.gd")
var lib


func _initialize() -> void:
	call_deferred("run")


func survey(name: String, mat: ShaderMaterial, spr: Sprite2D, px: int, py: int, img_source: Callable, expect_screen_scale: float = 1.0) -> void:
	var r := {}
	# read positions at 1/16 pixel precision, UV at 1e-5, pixel size at 1e-6
	var names := {0: "local.x", 1: "local.y", 2: "world.x", 3: "world.y", 4: "screen_by_matrices.x", 5: "screen_by_matrices.y",
		6: "VERTEX_in_fragment.x", 7: "VERTEX_in_fragment.y", 8: "FRAGCOORD.x", 9: "FRAGCOORD.y"}
	for k in names.keys():
		mat.set_shader_parameter("which", k)
		mat.set_shader_parameter("scale", 16.0)
		await lib.frames(2)
		r[names[k]] = snappedf(lib.decode(img_source.call().get_pixel(px, py), 16.0), 0.0625)
	for k in [[10, "SCREEN_UV.x"], [11, "SCREEN_UV.y"]]:
		mat.set_shader_parameter("which", k[0])
		mat.set_shader_parameter("scale", 50000.0)
		await lib.frames(2)
		r[k[1]] = snappedf(lib.decode(img_source.call().get_pixel(px, py), 50000.0), 0.00001)
	for k in [[12, "SCREEN_PIXEL_SIZE.x"], [13, "SCREEN_PIXEL_SIZE.y"]]:
		mat.set_shader_parameter("which", k[0])
		mat.set_shader_parameter("scale", 1000000.0)
		await lib.frames(2)
		r[k[1]] = snappedf(lib.decode(img_source.call().get_pixel(px, py), 1000000.0), 0.000001)
	var gt := spr.get_global_transform()
	var ctrans := spr.get_viewport().get_canvas_transform()
	r["engine_global_transform_origin"] = [gt.origin.x, gt.origin.y]
	r["engine_canvas_transform_origin"] = [ctrans.origin.x, ctrans.origin.y]
	r["engine_canvas_transform_x_axis"] = [ctrans.x.x, ctrans.x.y]
	r["pixel_probed"] = [px, py]
	lib.out(name, r)


func grab_root() -> Image:
	return lib.grab()


func run() -> void:
	lib = Lib.new(self)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)
	var mat: ShaderMaterial = lib.make_enc_material()
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(600, 400)
	spr.material = mat
	root.add_child(spr)
	await lib.frames(3)

	# a. baseline: no camera
	await survey("a-baseline-no-camera", mat, spr, 610, 410, grab_root)

	# b. camera panned
	var cam := Camera2D.new()
	cam.position = Vector2(840, 460)
	root.add_child(cam)
	cam.make_current()
	await lib.frames(3)
	await survey("b-camera-at-840-460", mat, spr, 400, 300, grab_root)

	# c. camera zoomed x2 on the sprite
	cam.position = Vector2(600, 400)
	cam.zoom = Vector2(2, 2)
	await lib.frames(3)
	await survey("c-camera-zoom-2-on-sprite", mat, spr, 700, 400, grab_root)

	# d. sprite rotated and scaled, camera back to default
	cam.zoom = Vector2(1, 1)
	cam.position = Vector2(640, 360)
	spr.rotation = deg_to_rad(30.0)
	spr.scale = Vector2(1.5, 1.5)
	await lib.frames(3)
	await survey("d-sprite-rotated-30-scaled-1.5", mat, spr, 640, 420, grab_root)
	spr.rotation = 0.0
	spr.scale = Vector2.ONE

	# e. sprite inside a CanvasLayer with its own transform
	root.remove_child(spr)
	var layer := CanvasLayer.new()
	layer.transform = Transform2D(Vector2(1.25, 0), Vector2(0, 1.25), Vector2(50, 30))
	root.add_child(layer)
	layer.add_child(spr)
	await lib.frames(3)
	# sprite centre lands at layer transform * (600,400) = (800,530); probe a pixel inside it
	await survey("e-canvaslayer-offset-50-30-scale-1.25", mat, spr, 820, 540, grab_root)
	layer.remove_child(spr)
	layer.queue_free()
	root.add_child(spr)
	await lib.frames(3)

	# f. child of a rotated and moved parent: does MODEL_MATRIX include the parent?
	root.remove_child(spr)
	var parent := Node2D.new()
	parent.position = Vector2(500, 300)
	parent.rotation = deg_to_rad(20.0)
	root.add_child(parent)
	spr.position = Vector2(50, 0)
	parent.add_child(spr)
	await lib.frames(3)
	var gp := spr.get_global_transform().origin
	await survey("f-child-of-moved-rotated-parent", mat, spr, int(gp.x) + 3, int(gp.y) + 3, grab_root)
	lib.out("f-parent-note", {"sprite_local_position_in_parent": [spr.position.x, spr.position.y], "sprite_global_position": [gp.x, gp.y]})
	parent.remove_child(spr)
	parent.queue_free()
	spr.position = Vector2(600, 400)
	root.add_child(spr)
	await lib.frames(3)

	# g. stretch: base 640x360, window 1280x720, canvas_items mode (sprite placed in base units)
	root.content_scale_size = Vector2i(640, 360)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
	await lib.frames(5)
	spr.position = Vector2(300, 200)
	cam.position = Vector2(320, 180)   # the camera from case d is still current: centre it on the 640x360 base view
	await lib.frames(3)
	lib.out("g-stretch-env", {"root_size": [root.size.x, root.size.y], "content_scale_size": [root.content_scale_size.x, root.content_scale_size.y],
		"image_size": [lib.grab().get_width(), lib.grab().get_height()], "final_transform": str(root.get_final_transform()),
		"canvas_transform": str(root.get_canvas_transform())})
	await survey("g-stretch-canvas_items-base-640x360-window-1280x720", mat, spr, 610, 410, grab_root)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	root.content_scale_size = Vector2i(0, 0)
	await lib.frames(5)
	quit(0)
