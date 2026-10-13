extends SceneTree
# verify4.gd: small facts used in the narration.
#   V4a  a ColorRect's local zero is its top-left corner (a centered Sprite2D's is its center)
#   V4b  a child's world position is its parent's position plus its own (Inspector value is relative to the parent)
#   V4c  panning the camera changes the canvas matrix but not the model matrix (its last column stays the node's world position)
#   V4d  sliding the sprite changes its world numbers and leaves its local numbers alone
#   V4e  TEXTURE_PIXEL_SIZE: one over the node's own texture size (64 px art, 128 px art, and no art at all)
#   V4f  SCREEN_UV is the screen pixel divided by the window size; SCREEN_PIXEL_SIZE is one over the window size
#   V4g  UV is local space with the zero moved to the top-left corner and the far edge squeezed to one
# Run: godot --path <project dir> --script res://verify4.gd

const Lib := preload("res://probe_lib.gd")
var lib


func _initialize() -> void:
	call_deferred("run")


func pair(mat: ShaderMaterial, idx: Array, px: int, py: int, scale: float = 1.0) -> Array:
	return [await lib.read(mat, idx[0], scale, px, py), await lib.read(mat, idx[1], scale, px, py)]


func run() -> void:
	lib = Lib.new(self)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)

	# ---- V4a ColorRect
	var mat_r: ShaderMaterial = lib.make_enc_material()
	var cr := ColorRect.new()
	cr.position = Vector2(200, 100)
	cr.size = Vector2(300, 200)
	cr.material = mat_r
	root.add_child(cr)
	await lib.frames(3)
	var r := {}
	r["local_at_top_left_pixel_(200,100)"] = await pair(mat_r, [0, 1], 200, 100)
	r["local_at_bottom_right_pixel_(499,299)"] = await pair(mat_r, [0, 1], 499, 299)
	r["world_at_top_left_pixel"] = await pair(mat_r, [2, 3], 200, 100)
	r["TEXTURE_PIXEL_SIZE_x1000_no_art"] = await pair(mat_r, [14, 15], 300, 200, 1000.0)
	lib.out("V4a-colorrect-local-zero-is-its-top-left", r)
	cr.queue_free()
	await lib.frames(2)

	# ---- V4b parent and child
	var parent := Node2D.new()
	parent.position = Vector2(500, 300)
	root.add_child(parent)
	var mat_c: ShaderMaterial = lib.make_enc_material()
	var child := Sprite2D.new()
	child.texture = lib.white_texture(128)
	child.position = Vector2(50, 0)
	child.material = mat_c
	parent.add_child(child)
	await lib.frames(3)
	r = {"child_position_in_inspector": [child.position.x, child.position.y], "child_global_position": [child.global_position.x, child.global_position.y]}
	r["world_of_child_top_left_corner"] = await pair(mat_c, [2, 3], 486, 236)
	r["MODEL_MATRIX_last_column"] = await pair(mat_c, [20, 21], 486, 236)
	lib.out("V4b-child-inspector-position-is-relative-to-parent", r)
	parent.queue_free()
	await lib.frames(2)

	# ---- V4c/d/f/g: sprite at world (600,400), camera at (890,460)
	var mat: ShaderMaterial = lib.make_enc_material()
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(600, 400)
	spr.material = mat
	root.add_child(spr)
	var cam := Camera2D.new()
	cam.position = Vector2(890, 460)
	root.add_child(cam)
	cam.make_current()
	await lib.frames(4)
	r = {}
	r["camera_890_460_MODEL_MATRIX_last_column"] = await pair(mat, [20, 21], 286, 236)
	r["camera_890_460_canvas_origin"] = [root.get_canvas_transform().origin.x, root.get_canvas_transform().origin.y]
	cam.position = Vector2(990, 460)
	await lib.frames(4)
	r["camera_990_460_MODEL_MATRIX_last_column"] = await pair(mat, [20, 21], 186, 236)
	r["camera_990_460_canvas_origin"] = [root.get_canvas_transform().origin.x, root.get_canvas_transform().origin.y]
	lib.out("V4c-camera-pan-changes-canvas-not-model", r)

	cam.position = Vector2(890, 460)
	await lib.frames(4)
	r = {}
	r["sprite_at_600_400_world_corner"] = await pair(mat, [2, 3], 286, 236)
	r["sprite_at_600_400_local_corner"] = await pair(mat, [0, 1], 286, 236)
	spr.position = Vector2(700, 400)
	await lib.frames(4)
	r["sprite_at_700_400_world_corner"] = await pair(mat, [2, 3], 386, 236)
	r["sprite_at_700_400_local_corner"] = await pair(mat, [0, 1], 386, 236)
	spr.position = Vector2(600, 400)
	await lib.frames(4)
	lib.out("V4d-slide-the-sprite-world-changes-local-does-not", r)

	r = {}
	r["SCREEN_UV_x50000_at_pixel_286_236"] = await pair(mat, [10, 11], 286, 236, 50000.0)
	r["expected_(286.5/1280,236.5/720)"] = [286.5 / 1280.0, 236.5 / 720.0]
	r["SCREEN_PIXEL_SIZE_x1e6"] = await pair(mat, [12, 13], 286, 236, 1000000.0)
	r["expected_(1/1280,1/720)"] = [1.0 / 1280.0, 1.0 / 720.0]
	lib.out("V4f-screen-uv-and-pixel-size", r)

	r = {}
	r["local_at_pixel_286_236"] = await pair(mat, [0, 1], 286, 236, 16.0)
	r["UV_x50000_at_pixel_286_236"] = await pair(mat, [22, 23], 286, 236, 50000.0)
	r["expected_UV_if_UV=(local+64)/128"] = [(-63.5 + 64.0) / 128.0, (-63.5 + 64.0) / 128.0]
	var far := await pair(mat, [22, 23], 413, 363, 50000.0)   # bottom-right pixel of the sprite on screen: (286+127, 236+127)
	r["UV_x50000_at_bottom_right_pixel_413_363"] = far
	r["expected_UV_there"] = [(63.5 + 64.0) / 128.0, (63.5 + 64.0) / 128.0]
	lib.out("V4g-uv-is-local-rescaled", r)
	spr.queue_free()
	await lib.frames(2)

	# ---- V4e TEXTURE_PIXEL_SIZE on 64 px and 128 px art
	cam.position = Vector2(640, 360)
	var m64: ShaderMaterial = lib.make_enc_material()
	var s64 := Sprite2D.new()
	s64.texture = lib.white_texture(64)
	s64.position = Vector2(300, 300)
	s64.material = m64
	root.add_child(s64)
	var m128: ShaderMaterial = lib.make_enc_material()
	var s128 := Sprite2D.new()
	s128.texture = lib.white_texture(128)
	s128.position = Vector2(700, 300)
	s128.material = m128
	root.add_child(s128)
	await lib.frames(4)
	r = {}
	r["TEXTURE_PIXEL_SIZE_x1e6_64px_art"] = await pair(m64, [14, 15], 300, 300, 1000000.0)
	r["TEXTURE_PIXEL_SIZE_x1e6_128px_art"] = await pair(m128, [14, 15], 700, 300, 1000000.0)
	r["expected_(1/64,1/128)"] = [1.0 / 64.0, 1.0 / 128.0]
	lib.out("V4e-texture-pixel-size-follows-the-art", r)
	quit(0)
