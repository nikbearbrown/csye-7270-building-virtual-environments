extends SceneTree
# F: REGION_RECT. Does the built-in tell a shader which part of a sheet is showing (hframes, region_enabled, AtlasTexture frames)?
# Run: godot --path <scratch project> --script res://verify_f_region.gd
const Lib := preload("res://ol_lib.gd")

func _initialize() -> void: call_deferred("run")
func frames(n: int) -> void:
	for i in range(n): await process_frame
func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func region_of(node: Node2D) -> Array:
	var vals: Array = []
	for m in [Vector4(1, 0, 0, 0), Vector4(0, 1, 0, 0), Vector4(0, 0, 1, 0), Vector4(0, 0, 0, 1)]:
		node.material = Lib.material("show-region.gdshader", {"mask": m})
		await frames(3)
		RenderingServer.force_draw(false)
		var img := root.get_texture().get_image()
		vals.append(snappedf(img.get_pixel(320, 180).r, 0.001))
	return vals

func run() -> void:
	RenderingServer.set_default_clear_color(Lib.STAGE)
	root.size = Vector2i(640, 360)
	var sheet_img := Image.create_empty(128, 64, false, Image.FORMAT_RGBA8)
	sheet_img.fill(Color(0.2, 0.6, 0.5, 1.0))
	var sheet := ImageTexture.create_from_image(sheet_img)
	out("env", {"engine": Engine.get_version_info()["string"], "renderer": RenderingServer.get_current_rendering_method()})

	var sp := Sprite2D.new()
	sp.texture = sheet
	sp.hframes = 2
	sp.frame = 1
	sp.position = Vector2(320, 180)
	sp.scale = Vector2(4, 4)
	root.add_child(sp)
	out("F1-hframes-frame1", {"REGION_RECT_xywh": await region_of(sp), "expect_if_it_followed_the_frame": [0.5, 0.0, 0.5, 1.0]})
	sp.hframes = 1; sp.frame = 0
	sp.region_enabled = true
	sp.region_rect = Rect2(64, 0, 64, 64)
	out("F2-region_rect", {"REGION_RECT_xywh": await region_of(sp), "expect": [0.5, 0.0, 0.5, 1.0]})
	sp.queue_free()
	await frames(2)

	var at := AtlasTexture.new(); at.atlas = sheet; at.region = Rect2(64, 0, 64, 64)
	var sp2 := Sprite2D.new()
	sp2.texture = at
	sp2.position = Vector2(320, 180)
	sp2.scale = Vector2(4, 4)
	root.add_child(sp2)
	out("F3-atlas-texture-on-sprite2d", {"REGION_RECT_xywh": await region_of(sp2)})
	sp2.queue_free()
	await frames(2)

	var sf := SpriteFrames.new()
	sf.add_frame("default", at)
	var an := AnimatedSprite2D.new()
	an.sprite_frames = sf
	an.position = Vector2(320, 180)
	an.scale = Vector2(4, 4)
	root.add_child(an)
	out("F4-animatedsprite2d-atlas-frame", {"REGION_RECT_xywh": await region_of(an)})
	quit(0)
