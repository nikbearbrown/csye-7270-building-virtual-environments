extends SceneTree
# Does the code shown in B43 work? A node script with _unhandled_key_input, a pushed key event, a tween on shader_parameter/radius.
# Run: godot --path <project dir> --script res://verify5.gd
const IRIS := "shader_type canvas_item;\nuniform float radius : hint_range(0.0, 0.8) = 0.0;\nvoid fragment() {\n\tif (distance(UV, vec2(0.5)) > radius) {\n\t\tdiscard;\n\t}\n\tCOLOR = texture(TEXTURE, UV);\n}\n"
const HANDLER := "extends Node\nfunc _unhandled_key_input(event):\n\tif event.pressed:\n\t\tvar tween := create_tween()\n\t\ttween.tween_property($Sprite.material, \"shader_parameter/radius\", 0.8, 0.5)\n"

func _initialize() -> void: call_deferred("run")

func out(id: String, d: Dictionary) -> void:
	d["id"] = id
	print("RESULT " + JSON.stringify(d))

func frames(n: int) -> void:
	for i in range(n): await process_frame

func center() -> Array:
	RenderingServer.force_draw(false)
	var img := root.get_texture().get_image()
	var c := img.get_pixel(img.get_width() / 2, img.get_height() / 2)
	return [snappedf(c.r, 0.001), snappedf(c.g, 0.001), snappedf(c.b, 0.001)]

func run() -> void:
	root.size = Vector2i(320, 180)
	var holder := Node.new()
	var scr := GDScript.new()
	scr.source_code = HANDLER
	var err := scr.reload()
	holder.set_script(scr)
	var im := Image.create(128, 128, false, Image.FORMAT_RGBA8)
	im.fill(Color("#5FA391"))
	var spr := Sprite2D.new()
	spr.name = "Sprite"
	spr.texture = ImageTexture.create_from_image(im)
	spr.position = Vector2(160, 90)
	var sh := Shader.new()
	sh.code = IRIS
	var mat := ShaderMaterial.new()
	mat.shader = sh
	spr.material = mat
	holder.add_child(spr)
	root.add_child(holder)
	await frames(3)
	var before := center()
	var ev := InputEventKey.new()
	ev.keycode = KEY_SPACE
	ev.physical_keycode = KEY_SPACE
	ev.pressed = true
	root.push_input(ev)
	await create_timer(0.8).timeout
	await frames(2)
	var after := center()
	out("I-key-press-opens-iris", {"script_reload_error": err, "centre_before_key": before, "centre_after_key": after,
		"reading": "before = stage colour (radius 0 discards everything); after = sprite colour (radius tweened to 0.8)"})
	quit(0)
