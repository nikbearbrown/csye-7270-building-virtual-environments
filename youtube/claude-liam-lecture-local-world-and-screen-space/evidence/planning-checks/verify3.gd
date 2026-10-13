extends SceneTree
# verify3.gd: the numbers used in Act I and II, the matrix order, and the w = 0 versus w = 1 switch.
# Scene: 1280x720 view, a 128 px Sprite2D (centered) at world (600,400).
#   T1  camera at (890,460): the sprite's top-left corner has local (-64,-64), world (536,336), screen (286,236)
#   T2  camera panned right by 100 to (990,460): world stays (536,336), screen becomes (186,236)
#   T3  camera zoomed x2 on the sprite: right order gives (512,232); the swapped order lands off screen
#   T4  w = 1 (a place) against w = 0 (a direction); the last column of MODEL_MATRIX is the node's position
#   T5  the same with the sprite scaled x2 and rotated 30 degrees: w = 0 keeps the scale and the turn but drops the shift
# Run: godot --path <project dir> --script res://verify3.gd

const Lib := preload("res://probe_lib.gd")
var lib


func _initialize() -> void:
	call_deferred("run")


func corner(mat: ShaderMaterial, idx: Array, px: int, py: int, scale: float = 1.0) -> Array:
	return [await lib.read(mat, idx[0], scale, px, py), await lib.read(mat, idx[1], scale, px, py)]


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
	var cam := Camera2D.new()
	cam.position = Vector2(890, 460)
	root.add_child(cam)
	cam.make_current()
	await lib.frames(4)

	# T1
	var r := {}
	r["camera_position"] = [cam.position.x, cam.position.y]
	r["canvas_transform_origin"] = [root.get_canvas_transform().origin.x, root.get_canvas_transform().origin.y]
	r["local"] = await corner(mat, [0, 1], 286, 236)
	r["world"] = await corner(mat, [2, 3], 286, 236)
	r["screen_by_matrices"] = await corner(mat, [4, 5], 286, 236)
	r["VERTEX_in_fragment"] = await corner(mat, [6, 7], 286, 236)
	r["FRAGCOORD_xy"] = await corner(mat, [8, 9], 286, 236)
	r["note"] = "values are floor() of the fragment-centre value read at screen pixel (286,236), the sprite's top-left corner pixel"
	lib.out("T1-corner-addresses-camera-890-460", r)

	# T2
	cam.position = Vector2(990, 460)
	await lib.frames(4)
	r = {"camera_position": [cam.position.x, cam.position.y], "canvas_transform_origin": [root.get_canvas_transform().origin.x, root.get_canvas_transform().origin.y]}
	r["local"] = await corner(mat, [0, 1], 186, 236)
	r["world"] = await corner(mat, [2, 3], 186, 236)
	r["screen_by_matrices"] = await corner(mat, [4, 5], 186, 236)
	lib.out("T2-after-camera-pan-right-100", r)

	# T3: zoom x2 on the sprite
	cam.position = Vector2(600, 400)
	cam.zoom = Vector2(2, 2)
	await lib.frames(4)
	r = {"canvas_transform_origin": [root.get_canvas_transform().origin.x, root.get_canvas_transform().origin.y], "canvas_transform_x_axis": [root.get_canvas_transform().x.x, root.get_canvas_transform().x.y]}
	r["world"] = await corner(mat, [2, 3], 512, 232)
	r["screen_right_order_CANVAS_x_MODEL"] = await corner(mat, [4, 5], 512, 232)
	r["screen_wrong_order_MODEL_x_CANVAS"] = await corner(mat, [16, 17], 512, 232)
	r["FRAGCOORD_xy"] = await corner(mat, [8, 9], 512, 232)
	lib.out("T3-order-of-the-two-matrices-camera-zoom-2", r)

	# T4: w
	cam.zoom = Vector2(1, 1)
	cam.position = Vector2(640, 360)
	await lib.frames(4)
	r = {}
	r["w1_place_world"] = await corner(mat, [2, 3], 536, 336)
	r["w0_direction"] = await corner(mat, [18, 19], 536, 336)
	r["MODEL_MATRIX_last_column_xy"] = await corner(mat, [20, 21], 536, 336)
	r["sprite_position"] = [spr.position.x, spr.position.y]
	lib.out("T4-w-one-is-a-place-w-zero-is-a-direction", r)

	# T5: scaled and rotated sprite
	spr.scale = Vector2(2, 2)
	spr.rotation = deg_to_rad(30.0)
	await lib.frames(4)
	var gt := spr.get_global_transform()
	var local_corner := Vector2(-64, -64)
	var expect_world := gt * local_corner
	var expect_dir := gt.basis_xform(local_corner)
	# probe a pixel inside the sprite near its centre and compare with the engine's own transform
	var pix := Vector2i(640 + 40, 360 + 20)
	var wv: Array = await corner(mat, [2, 3], pix.x, pix.y, 16.0)
	var wd: Array = await corner(mat, [18, 19], pix.x, pix.y, 16.0)
	var lv: Array = await corner(mat, [0, 1], pix.x, pix.y, 16.0)
	# engine's expectation for that pixel
	var screen_pt := Vector2(pix.x + 0.5, pix.y + 0.5)
	var exp_w := root.get_canvas_transform().affine_inverse() * screen_pt
	var exp_l := gt.affine_inverse() * exp_w
	var exp_dir := gt.basis_xform(exp_l)
	r = {"sprite_scale": 2.0, "sprite_rotation_deg": 30.0,
		"corner_world_by_engine": [expect_world.x, expect_world.y], "corner_offset_without_shift_by_engine": [expect_dir.x, expect_dir.y],
		"probe_pixel": [pix.x, pix.y], "world_read": wv, "world_expected": [exp_w.x, exp_w.y], "local_read": lv, "local_expected": [exp_l.x, exp_l.y],
		"w0_read": wd, "w0_expected": [exp_dir.x, exp_dir.y]}
	lib.out("T5-scaled-and-rotated-w0-keeps-scale-and-turn-drops-shift", r)
	quit(0)
