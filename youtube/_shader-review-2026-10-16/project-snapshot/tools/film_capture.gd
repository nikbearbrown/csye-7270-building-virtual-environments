extends "res://tools/harness.gd"

func run() -> void:
	var outdir := ProjectSettings.globalize_path("res://evidence/film-frames")
	DirAccess.make_dir_recursive_absolute(outdir)
	for lesson_text in String(args.get("lessons", "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15")).split(","):
		var lesson := int(lesson_text)
		var scene := Node3D.new()
		root.add_child(scene)
		var rig := Rig.build(scene)
		var mat := Lessons.material(lesson)
		if lesson == 9:
			mat.set_shader_parameter("shader_color", Color.BLACK)
			mat.set_shader_parameter("specular_color", Color.BLACK)
			mat.set_shader_parameter("ambient_color", Color.WHITE)
		if lesson == 15:
			mat.set_shader_parameter("reflection_intensity", 0.0)
			mat.set_shader_parameter("specular_color", Color.BLACK)
		rig["sphere"].material_override = mat
		rig["torus"].material_override = mat
		var layer := CanvasLayer.new()
		scene.add_child(layer)
		var label := Label.new()
		label.position = Vector2(28, 650)
		label.add_theme_color_override("font_color", Color("#3D3929"))
		label.add_theme_font_size_override("font_size", 25)
		layer.add_child(label)
		var frames := outdir + "/" + Lessons.NAMES[lesson]
		DirAccess.make_dir_recursive_absolute(frames)
		await warm(2)
		for frame in range(192):
			var t := float(frame) / 191.0
			var v := clampf((t - 0.2) / 0.6, 0.0, 1.0)
			match lesson:
				0:
					mat.set_shader_parameter("shader_color", Color("#5FA391").lerp(Color("#D97757"), v))
					label.text = "Uniform color changes; no lighting"
				1:
					rig["torus"].rotation.y = v * PI
					label.text = "Rotate mesh; normals become world-space directions"
				2:
					var light := Vector3(0.5, -0.8, -0.6).rotated(Vector3.FORWARD, v * PI)
					mat.set_shader_parameter("light_direction", light)
					label.text = "Rotate light direction; clamp the normal dot light"
				3:
					mat.set_shader_parameter("ambient_color", Color(v * 0.3, v * 0.3, v * 0.3))
					label.text = "ambient_color (sRGB) = %.2f" % (v * 0.3)
				4:
					mat.set_shader_parameter("fresnel_power", 1.0 + v * 5.0)
					label.text = "fresnel_power = %.2f" % (1.0 + v * 5.0)
				5:
					mat.set_shader_parameter("specular_power", 8.0 + v * 92.0)
					label.text = "specular_power = %.2f" % (8.0 + v * 92.0)
				6:
					mat.set_shader_parameter("shader_color", Color.WHITE.lerp(Color("#D97757"), v))
					label.text = "Tint the diffuse texture; highlight added separately"
				7:
					if frame == 0:mat.set_shader_parameter("spec_map", white_texture())
					if frame == 96:mat.set_shader_parameter("spec_map", Lessons.load_texture("spec_rg.png"))
					label.text = "Spec masks: " + ("all one" if frame < 96 else "R rim / G highlight")
				8:
					if frame == 0:mat.set_shader_parameter("normal_map", flat_normal())
					if frame == 96:mat.set_shader_parameter("normal_map", Lessons.load_texture("normal_gl.png"))
					label.text = "Normal map: " + ("flat" if frame < 96 else "domes; unchanged silhouette")
				9:
					var cam: Camera3D = rig["camera"]
					cam.position = Rig.CAM_POS + Vector3(v * 0.9, 0, 0)
					cam.look_at(Vector3.ZERO)
					label.text = "Reflection isolated: base/specular black, ambient white"
				10:
					mat.set_shader_parameter("vert_offset", Vector3(0, v * 0.3, 0))
					label.text = "vert_offset.y = %.2f; normals NOT recomputed" % (v * 0.3)
				11:
					mat.set_shader_parameter("uv_scale_translate", Vector4(1 + v * 2, 1 + v * 2, 0, 0))
					label.text = "UV scale = %.2f; scrolling at 0.1 U / second" % (1 + v * 2)
				12:
					var technique := mini(frame / 48, 3)
					if frame % 48 == 0:
						mat = Lessons.material(lesson, {}, FileAccess.get_file_as_string(Lessons.shader_path(lesson)).replace("#define TECHNIQUE 1", "#define TECHNIQUE %d" % technique))
						rig["sphere"].material_override = mat
						rig["torus"].material_override = mat
					label.text = ["Opaque", "Alpha blend", "Alpha scissor", "Additive"][technique]
				13:
					mat.set_shader_parameter("shader_color", Color.RED.lerp(Color.YELLOW, v))
					label.text = "Change first color; only blend-map R regions respond"
				14:
					mat.set_shader_parameter("fresnel_offset", v * 0.5)
					label.text = "fresnel_offset = %.2f" % (v * 0.5)
				15:
					mat.set_shader_parameter("subsurface_spread", v * 0.5)
					label.text = "spread = %.2f; reflection/specular disabled to expose wrap" % (v * 0.5)
			var img := await shoot(1.0 / 12.0)
			img.save_jpg(frames + "/%04d.jpg" % frame, 0.93)
		say("CAPTURE " + Lessons.NAMES[lesson] + " 192 frames at 12 fps; offline fixed step")
		scene.queue_free()
		await process_frame

func white_texture() -> ImageTexture:
	var im := Image.create(4, 4, false, Image.FORMAT_RGB8)
	im.fill(Color.WHITE)
	return ImageTexture.create_from_image(im)

func flat_normal() -> ImageTexture:
	var im := Image.create(4, 4, false, Image.FORMAT_RGB8)
	im.fill(Color(0.5, 0.5, 1.0))
	return ImageTexture.create_from_image(im)
