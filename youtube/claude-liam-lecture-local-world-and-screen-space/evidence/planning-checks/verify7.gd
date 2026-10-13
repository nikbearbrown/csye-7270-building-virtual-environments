extends SceneTree
# verify7.gd: three more numbers used in the narration.
#   N1  VERTEX read inside fragment() at the sprite's top-left corner pixel is the pixel CENTRE: 286.5, 236.5 (camera at 890,460)
#   N2  a stretched window (base 640 x 360 shown in 1280 x 720): the same 128 px sprite spans 128 world pixels and 256 screen pixels
#   N3  spacing out: set `amount` from code, then tween it 0 -> 1; colour at the blob centre moves from the sprite's teal to the sky
# Run: godot --path <project dir> --script res://verify7.gd

const Lib := preload("res://probe_lib.gd")
const Scn := preload("res://scenes_lib.gd")
var lib


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	lib = Lib.new(self)
	RenderingServer.set_default_clear_color(Scn.STAGE)
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

	# N1
	var r := {}
	r["VERTEX_in_fragment_x2_at_corner_pixel_286_236"] = [await lib.read(mat, 6, 2.0, 286, 236), await lib.read(mat, 7, 2.0, 286, 236)]
	r["FRAGCOORD_x2_at_the_same_pixel"] = [await lib.read(mat, 8, 2.0, 286, 236), await lib.read(mat, 9, 2.0, 286, 236)]
	r["local_x2_at_the_same_pixel"] = [await lib.read(mat, 0, 2.0, 286, 236), await lib.read(mat, 1, 2.0, 286, 236)]
	lib.out("N1-vertex-in-fragment-is-the-pixel-centre", r)

	# N2 stretch
	cam.position = Vector2(320, 180)
	spr.position = Vector2(300, 200)
	root.content_scale_size = Vector2i(640, 360)
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS
	root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
	await lib.frames(5)
	# sprite spans world x 236..364 -> screen x 472..728 (window 1280 wide). Read the first and last pixel columns on the midline y=400.
	var left_world = await lib.read(mat, 2, 4.0, 472, 400)
	var right_world = await lib.read(mat, 2, 4.0, 727, 400)
	var left_screen = await lib.read(mat, 4, 4.0, 472, 400)
	var right_screen = await lib.read(mat, 4, 4.0, 727, 400)
	var left_local = await lib.read(mat, 0, 4.0, 472, 400)
	var right_local = await lib.read(mat, 0, 4.0, 727, 400)
	lib.out("N2-stretched-window-world-versus-screen-width", {"window": [root.size.x, root.size.y], "content_scale_size": [640, 360],
		"world_x_at_first_and_last_pixel_column": [left_world, right_world], "world_span": right_world - left_world,
		"screen_x_at_first_and_last_pixel_column": [left_screen, right_screen], "screen_span": right_screen - left_screen,
		"local_x_at_first_and_last_pixel_column": [left_local, right_local],
		"note": "spans measured between pixel centres of the first and last column, so each is one pixel (or half a world pixel) short of the full width"})
	root.content_scale_mode = Window.CONTENT_SCALE_MODE_DISABLED
	root.content_scale_size = Vector2i(0, 0)
	await lib.frames(5)
	spr.queue_free()
	await lib.frames(2)

	# N3 spacing out
	cam.position = Vector2(640, 360)
	var sky: Texture2D = Scn.sky_texture(1536)
	var m9 := Scn.material("09-spacing-out.gdshader", {"sky": sky})
	var blob := Scn.sprite(Scn.blob_texture(256), Vector2(852, 240), 1.0, m9)
	root.add_child(blob)
	await lib.frames(3)
	m9.set_shader_parameter("amount", 0.0)    # the start value is set from code first (a tween on a never-set uniform fails)
	await lib.frames(3)
	var before = lib.grab().get_pixel(852, 240)
	var tw := create_tween()
	tw.tween_property(m9, "shader_parameter/amount", 1.0, 1.0)
	await create_timer(0.5).timeout
	var mid = lib.grab().get_pixel(852, 240)
	await tw.finished
	await lib.frames(3)
	var after = lib.grab().get_pixel(852, 240)
	lib.out("N3-spacing-out-tween", {"centre_before_rgb": [roundi(before.r * 255), roundi(before.g * 255), roundi(before.b * 255)],
		"centre_mid_rgb": [roundi(mid.r * 255), roundi(mid.g * 255), roundi(mid.b * 255)], "centre_after_rgb": [roundi(after.r * 255), roundi(after.g * 255), roundi(after.b * 255)],
		"amount_after": m9.get_shader_parameter("amount"), "note": "the blob centre sits on the planet (cream body) so 'after' is the sky's planet, 'before' the sprite's teal"})
	lib.grab().save_png("/private/tmp/claude-501/godot-shaders-local-world-and-screen-space/scratch/out/spacing-out-end.png")
	quit(0)
