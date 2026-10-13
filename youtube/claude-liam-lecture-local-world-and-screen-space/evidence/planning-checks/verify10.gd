extends SceneTree
# verify10.gd: stretch modes. The film says "in canvas items stretch mode ... the same sprite spans twice as many screen pixels".
# What do the other modes do? Base 640 x 360 shown in a 1280 x 720 window; a 128 px sprite at base (300,200); read world.x and screen.x at its first and last pixel column.
# Run: godot --path <project dir> --script res://verify10.gd
const Lib := preload("res://probe_lib.gd")
var lib


func _initialize() -> void:
	call_deferred("run")


func run() -> void:
	lib = Lib.new(self)
	root.size = Vector2i(1280, 720)
	await lib.frames(3)
	var mat: ShaderMaterial = lib.make_enc_material()
	var spr := Sprite2D.new()
	spr.texture = lib.white_texture(128)
	spr.position = Vector2(300, 200)
	spr.material = mat
	root.add_child(spr)
	await lib.frames(3)
	var modes := {"disabled": Window.CONTENT_SCALE_MODE_DISABLED, "canvas_items": Window.CONTENT_SCALE_MODE_CANVAS_ITEMS, "viewport": Window.CONTENT_SCALE_MODE_VIEWPORT}
	for name in modes.keys():
		root.content_scale_mode = modes[name]
		root.content_scale_size = Vector2i(640, 360) if name != "disabled" else Vector2i(0, 0)
		root.content_scale_aspect = Window.CONTENT_SCALE_ASPECT_KEEP
		await lib.frames(6)
		var img: Image = lib.grab()
		# find the sprite's extent along the horizontal midline by reading the white sprite against the stage colour
		var first := -1
		var last := -1
		for x in range(0, img.get_width()):
			var c: Color = img.get_pixel(x, int(img.get_height() * 0.5))
			if c.r > 0.9 and c.g > 0.9 and c.b > 0.9 and false:
				pass
		# the encoder paints numbers, not white; instead read world.x and screen.x at a probe row and locate the extent by the world value
		var xs: Array = []
		for x in [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200]:
			if x >= img.get_width():
				continue
			mat.set_shader_parameter("which", 2)
			mat.set_shader_parameter("scale", 1.0)
			await lib.frames(2)
			var cw: Color = lib.grab().get_pixel(x, int(img.get_height() * 0.55))
			xs.append([x, roundi(cw.r * 255) * 256 + roundi(cw.g * 255) - 1024 if cw.b < 0.01 and (cw.r < 0.5 or cw.g > 0) else null])
		lib.out("stretch-" + name, {"image_size": [img.get_width(), img.get_height()], "root_size": [root.size.x, root.size.y], "final_transform_scale": root.get_final_transform().x.x,
			"sprite_world_x_samples_along_a_row (pixel x, world x)": xs})
		# screen span and world span between the first and last sprite columns, using the known layout: sprite covers world 236..364
		var scale_factor := (float(img.get_width()) / 640.0) if name != "disabled" else 1.0   # the image is the rendered viewport: 640 wide in viewport mode, 1280 in canvas_items mode
		var left_px := int(236.0 * scale_factor) + 1
		var right_px := int(364.0 * scale_factor) - 2
		var row := int(200.0 * scale_factor)
		var vals := {}
		for item in [["world", 2], ["screen_by_matrices", 4]]:
			var pair: Array = []
			for px in [left_px, right_px]:
				mat.set_shader_parameter("which", item[1])
				mat.set_shader_parameter("scale", 4.0)
				await lib.frames(2)
				var cc: Color = lib.grab().get_pixel(px, row)
				pair.append((float(roundi(cc.r * 255) * 256 + roundi(cc.g * 255)) - 1024.0) / 4.0)
			vals[item[0]] = pair
		lib.out("stretch-" + name + "-spans", {"first_and_last_column_probed": [left_px, right_px], "world_x": vals["world"], "screen_x": vals["screen_by_matrices"],
			"world_span": vals["world"][1] - vals["world"][0], "screen_span": vals["screen_by_matrices"][1] - vals["screen_by_matrices"][0]})
	quit(0)
